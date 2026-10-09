"""Replacement never broadens deletion or replays a partially imported spool."""
from copy import deepcopy
from datetime import date, datetime, timezone
import json
from pathlib import Path

import pytest
from langfuse_synth_core.seed import otlp

from synth import migration, seed
from synth.config import Config, Generation, Target
from synth.materialize import build_historical_experiment_events
from synth.model_policy import MODEL_POLICY_REVISION, apply_model_policy
from synth.prompt_references import annotate_prompt_references
from synth.operation_names import normalize_operations
from synth.receipt import attributes
from synth.state import RunState


@pytest.fixture
def prepared(monkeypatch, tmp_path):
    old = tmp_path / 'original'
    monkeypatch.setenv('SYNTH_STATE_DIR', str(old))
    monkeypatch.setenv('SYNTH_OUT_DIR', str(tmp_path / 'out'))
    monkeypatch.delenv('LANGFUSE_BASE_URL', raising=False)
    cfg = Config(Target('https://example.invalid'), Generation(42, 6, date(2026, 10, 9)))
    spool = old / 'events.ndjson'
    seed.run_seed(cfg, dry_run=True, spool_path=spool, log=lambda _: None)
    state = RunState.load()
    state.dry_run = False
    state.import_status = 'imported'
    state.project_id = 'project-test'
    _, experiments = build_historical_experiment_events({'seed': 42}, run_date=datetime(2026, 10, 9, 12, tzinfo=timezone.utc))
    for index, experiment in enumerate(experiments):
        experiment['experiment_id'] = f'existing-experiment-{index}'
    state.provisioning = {'project_id': 'project-test', 'historical_experiments': experiments,
                          'prompts': {'preserve': '72-versions-and-labels'}, 'datasets': {'preserve': 'all-items'}}
    state.save()
    original = {p: p.read_bytes() for p in old.iterdir()}
    events = migration._events(spool)
    rows = [{'id': e['spanId'], 'traceId': e['traceId'], 'projectId': 'project-test',
             'sessionId': attributes(e).get(otlp.SESSION_ID)} for e in events if otlp.is_span(e)]
    scores = [{'id': e['body']['id'], 'traceId': e['body']['traceId'], 'observationId': e['body']['observationId'],
               'projectId': 'project-test'} for e in events if not otlp.is_span(e)]
    rows.append({'id': 'live-observation', 'traceId': 'live-trace', 'projectId': 'project-test', 'sessionId': 'live-session'})
    scores.append({'id': 'live-score', 'traceId': 'live-trace', 'observationId': 'live-observation', 'projectId': 'project-test'})
    plan = migration.prepare_replacement(spool, tmp_path / 'replacement', expected_project_id='project-test',
                                          expected_run_date=state.run_receipt['run_date'], revision='models-2026-10-v1')
    policy = {'project_id': 'project-test', 'model_policy_revision': MODEL_POLICY_REVISION,
              'verified': True, 'provisioning': deepcopy(state.provisioning)}
    return plan, events, rows, scores, policy, original


def delete(prepared, callback=None):
    plan, _, rows, scores, policy, _ = prepared
    def perform(ids):
        rows[:] = [r for r in rows if r['traceId'] not in ids]
        scores[:] = [r for r in scores if r['traceId'] not in ids]
    return migration.delete_replacement(plan, authenticated_project_id='project-test', inventory=lambda: (rows, scores),
                                        delete_batch=callback or perform, policy_receipt=policy, log=lambda _: None)


def complete(prepared, callback, **kwargs):
    plan, _, rows, scores, _, _ = prepared
    return migration.import_replacement(plan, authenticated_project_id='project-test', inventory=lambda: (rows, scores),
                                        import_spool=callback, log=lambda _: None, **kwargs)


def test_transform_preserves_payloads_outcomes_chronology_and_experiment_links(prepared):
    plan, source, _, _, _, _ = prepared
    detail, _, replacement, maps = migration._load_plan(plan)
    reverse = {new: old for mapping in maps.values() for old, new in mapping.items()}
    reverted = migration.remap_references(replacement, reverse)
    expected = normalize_operations(annotate_prompt_references(apply_model_policy(source)))
    # JSON-valued references may be re-serialized when an ID changes; compare
    # their decoded structures while separately preserving the actual I/O bytes.
    def decoded(value):
        if isinstance(value, dict): return {k: decoded(v) for k, v in value.items()}
        if isinstance(value, list): return [decoded(v) for v in value]
        if isinstance(value, str) and value[:1] in {'[', '{'}:
            try: return decoded(json.loads(value))
            except ValueError: pass
        return value
    assert decoded(reverted) == decoded(expected)
    for original, restored in zip(source, reverted):
        if otlp.is_span(original):
            for key in (otlp.OBS_INPUT, otlp.OBS_OUTPUT):
                assert attributes(original).get(key) == attributes(restored).get(key)
    assert source != replacement
    assert sum(otlp.is_trace_root(e) for e in replacement) == detail['counts']['trace']
    for event in replacement:
        if otlp.is_trace_root(event):
            assert 'langfuse.observation.metadata.prompt_references' not in attributes(event)
    assert {e.get('startTimeUnixNano') for e in source} == {e.get('startTimeUnixNano') for e in replacement}
    assert detail['delete_trace_ids'] == sorted(maps['trace'])
    for event, changed in zip(source, replacement):
        if not otlp.is_span(event):
            assert event['body']['value'] == changed['body']['value']
            continue
        before, after = attributes(event), attributes(changed)
        for key in before:
            if key.startswith('langfuse.experiment.') and not key.endswith('root_observation_id'):
                assert before[key] == after[key]


def test_remaps_exact_nested_json_ids_without_changing_unrelated_formatting():
    value = {'plain': 'before old-id after', 'nested': '{ "x": ["old-id"] }', 'unchanged': '{ "a": 1 }'}
    assert migration.remap_references(value, {'old-id': 'new-id'}) == {
        'plain': 'before old-id after', 'nested': '{"x":["new-id"]}', 'unchanged': '{ "a": 1 }'}


def test_delete_only_authored_import_once_preserves_original_and_live_data(prepared):
    plan, _, rows, scores, policy, original = prepared
    requested = []
    def callback(ids):
        assert len(ids) <= 40
        requested.extend(ids)
        rows[:] = [r for r in rows if r['traceId'] not in ids]
        scores[:] = [r for r in scores if r['traceId'] not in ids]
    delete(prepared, callback)
    assert 'live-trace' not in requested
    assert len(rows) == len(scores) == 1
    imports = []
    state_path = complete(prepared, lambda path: imports.append(path))
    result = json.loads(state_path.read_text())
    assert result['import_status'] == 'imported' and len(imports) == 1
    assert result['provisioning']['prompts'] == policy['provisioning']['prompts']
    assert result['provisioning']['datasets'] == policy['provisioning']['datasets']
    assert result['provisioning']['historical_experiments'][0]['experiment_id'] == policy['provisioning']['historical_experiments'][0]['experiment_id']
    assert result['provisioning']['historical_experiments'][0]['trace_id'] != policy['provisioning']['historical_experiments'][0]['trace_id']
    assert all(path.read_bytes() == raw for path, raw in original.items())
    with pytest.raises(RuntimeError, match='already attempted'):
        delete(prepared, callback)
    with pytest.raises(RuntimeError, match='completed deletion'):
        complete(prepared, lambda _: pytest.fail('duplicate import'))


@pytest.mark.parametrize('damage', ['missing_observation', 'extra_score', 'wrong_score_binding', 'foreign_project', 'replacement_collision'])
def test_inventory_mismatch_blocks_all_deletion(prepared, damage):
    plan, _, rows, scores, _, _ = prepared
    if damage == 'missing_observation': rows.pop(0)
    if damage == 'extra_score': scores.append({**scores[0], 'id': 'unexpected-judge-score'})
    if damage == 'wrong_score_binding': scores[0]['observationId'] = 'wrong-target'
    if damage == 'foreign_project': rows[0]['projectId'] = 'another-project'
    if damage == 'replacement_collision':
        replacement = migration._events(plan.parent / 'events.ndjson')
        rows.append({'id': replacement[0]['spanId'], 'traceId': replacement[0]['traceId'], 'projectId': 'project-test'})
    with pytest.raises(RuntimeError):
        delete(prepared, lambda _: pytest.fail('unsafe deletion'))
    assert not (plan.parent / 'replacement-status.json').exists()


def test_ambiguous_deletion_is_not_retried_and_import_is_blocked(prepared):
    def failed(_): raise RuntimeError('connection lost after sending')
    with pytest.raises(RuntimeError, match='connection lost'): delete(prepared, failed)
    with pytest.raises(RuntimeError, match='already attempted'): delete(prepared)
    with pytest.raises(RuntimeError, match='completed deletion'):
        complete(prepared, lambda _: pytest.fail('import before deletion resolved'))


def test_async_delete_waits_for_scores_and_can_resume_only_polling(prepared):
    plan, _, rows, scores, _, _ = prepared
    def remove_observations(ids): rows[:] = [r for r in rows if r['traceId'] not in ids]
    delete(prepared, remove_observations)
    with pytest.raises(TimeoutError):
        complete(prepared, lambda _: pytest.fail('import while old scores remain'), timeout_seconds=0)
    scores[:] = [s for s in scores if s['id'] == 'live-score']
    imports = []
    complete(prepared, lambda path: imports.append(path), timeout_seconds=0)
    assert len(imports) == 1


def test_ambiguous_import_retains_failed_state_and_cannot_repeat(prepared):
    delete(prepared)
    def failed(_): raise RuntimeError('partial upload')
    with pytest.raises(RuntimeError, match='partial upload'): complete(prepared, failed)
    assert json.loads((prepared[0].parent / '.synth_state.json').read_text())['import_status'] == 'failed_requires_reconciliation'
    with pytest.raises(RuntimeError): complete(prepared, lambda _: pytest.fail('duplicate import'))


def test_preserved_live_evidence_loss_blocks_import(prepared):
    delete(prepared)
    prepared[2].clear()
    with pytest.raises(RuntimeError, match='Unrelated live evidence disappeared'):
        complete(prepared, lambda _: pytest.fail('import after unrelated loss'))


def test_source_tamper_or_policy_anchor_changes_blocks_deletion(prepared):
    plan, _, _, _, policy, _ = prepared
    policy['provisioning']['prompts'] = {'changed': 'bad'}
    with pytest.raises(RuntimeError, match='protected prompts'):
        delete(prepared, lambda _: pytest.fail('delete after prompt anchor mutation'))
    detail = json.loads(plan.read_text())
    Path(detail['source_spool']).write_text('tampered')
    with pytest.raises(RuntimeError, match='hash changed'):
        delete(prepared, lambda _: pytest.fail('delete after source mutation'))


def test_cli_plan_prepares_reviewable_artifacts_without_live_calls(prepared, capsys):
    from synth.cli import main
    plan, _, _, _, _, original = prepared
    source_plan = json.loads(plan.read_text())
    destination = plan.parent.parent / 'cli-plan'
    counts = source_plan['counts']
    args = ['history-replacement-plan', '--source-spool', source_plan['source_spool'],
            '--destination', str(destination), '--project-id', 'project-test',
            '--run-date', source_plan['run_date'], '--revision', 'cli-review-v1',
            '--expected-traces', str(counts['trace']), '--expected-observations', str(counts['observation']),
            '--expected-scores', str(counts['score'])]
    assert main(args) == 0
    result = json.loads((destination / 'replacement-plan.json').read_text())
    assert result['counts'] == counts
    assert result['revision'] == 'cli-review-v1'
    assert not (destination / '.synth_state.json').exists()
    assert not Path(result['guard']).exists()
    assert all(path.read_bytes() == raw for path, raw in original.items())
    assert 'No live data changed' in capsys.readouterr().out


def test_cli_plan_requires_explicit_scope():
    from synth.cli import main
    with pytest.raises(SystemExit) as error:
        main(['history-replacement-plan', '--source-spool', 'source.ndjson'])
    assert error.value.code == 2


@pytest.fixture
def awaiting_amendment(prepared):
    """Represent a reviewed legacy presentation plan before its single import."""
    plan, _, _, _, _, _ = prepared
    detail = json.loads(plan.read_text())
    events = migration._events(detail['replacement_spool'])
    for event in events:
        if not otlp.is_span(event):
            event['body']['comment'] = migration.LEGACY_SCORE_COMMENT_PREFIX + event['body'].get('comment', '')
            continue
        if attributes(event).get('langfuse.environment') == 'experiment':
            event['attributes'].append(otlp.string_attr('langfuse.experiment.description', migration.LEGACY_EXPERIMENT_DESCRIPTION))
        for attr in event['attributes']:
            if attr['key'] == otlp.USER_ID:
                attr['value']['stringValue'] = attr['value']['stringValue'].replace('customer-', 'fictional-user-', 1)
        if otlp.is_trace_root(event):
            event['attributes'].extend([
                otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'prompt_references', '[{"prompt_name":"products/explainer"}]'),
                otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'prompt_name', 'products/explainer'),
                otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'prompt_version', '7'),
                otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'resolved_version', '7'),
            ])
    raw = b''.join((json.dumps(e, separators=(',', ':'), ensure_ascii=False) + '\n').encode() for e in events)
    Path(detail['replacement_spool']).write_bytes(raw)
    detail['replacement_spool_sha256'] = migration._sha(raw)
    migration._write(plan, detail)
    delete(prepared)
    return prepared


def amend(prepared):
    plan = prepared[0]
    detail = json.loads(plan.read_text())
    return migration.amend_preimport_presentation(
        plan, expected_project_id='project-test', expected_plan_sha256=migration._sha(plan.read_bytes()),
        expected_replacement_sha256=detail['replacement_spool_sha256'])


def test_preimport_amendment_is_scoped_audited_and_imports_once(awaiting_amendment):
    plan = awaiting_amendment[0]
    old_plan = json.loads(plan.read_text())
    before = migration._events(old_plan['replacement_spool'])
    audit_path = amend(awaiting_amendment)
    audit = json.loads(audit_path.read_text())
    new_plan, _, after, _ = migration._load_plan(plan)
    assert audit['user_id_map'] and audit['removed_root_prompt_fields'] == old_plan['counts']['trace'] * 4
    assert audit['score_comment_prefixes'] == old_plan['counts']['score']
    assert audit['experiment_descriptions'] == 36
    assert old_plan['delete_trace_ids'] == new_plan['delete_trace_ids']
    assert old_plan['maps_sha256'] == new_plan['maps_sha256']
    assert old_plan['source_spool_sha256'] == new_plan['source_spool_sha256']
    for old, new in zip(before, after):
        if not otlp.is_span(old):
            expected_score = deepcopy(old)
            expected_score['body']['comment'] = old['body']['comment'][len(migration.LEGACY_SCORE_COMMENT_PREFIX):]
            assert new == expected_score
            continue
        a, b = attributes(old), attributes(new)
        for key in (otlp.OBS_INPUT, otlp.OBS_OUTPUT, otlp.SESSION_ID, 'langfuse.observation.cost_details',
                    'langfuse.observation.prompt.name', 'langfuse.observation.prompt.version'):
            assert a.get(key) == b.get(key)
        if otlp.USER_ID in a:
            assert b[otlp.USER_ID] == audit['user_id_map'][a[otlp.USER_ID]]
        assert {k:v for k,v in old.items() if k != 'attributes'} == {k:v for k,v in new.items() if k != 'attributes'}
        if otlp.is_trace_root(old):
            assert not migration.ROOT_PROMPT_METADATA & b.keys()
    imports = []
    complete(awaiting_amendment, lambda path: imports.append(path))
    assert len(imports) == 1
    with pytest.raises(RuntimeError, match='before any import'):
        amend(awaiting_amendment)


@pytest.mark.parametrize('marker', ['.replacement-import-attempt.json', '.synth_state.json', 'events.ndjson.imported'])
def test_amendment_refuses_any_import_marker(awaiting_amendment, marker):
    plan = awaiting_amendment[0]
    (plan.parent / marker).write_text('import begun')
    with pytest.raises(RuntimeError, match='before any import'):
        amend(awaiting_amendment)
    assert not (plan.parent / 'presentation-amendment').exists()


def test_amendment_refuses_unrelated_spool_tampering(awaiting_amendment):
    plan = awaiting_amendment[0]
    spool = plan.parent / 'events.ndjson'
    spool.write_bytes(spool.read_bytes().replace(b'generate-response', b'wrong-output-name', 1))
    with pytest.raises(RuntimeError, match='hash changed'):
        amend(awaiting_amendment)


def test_interrupted_amendment_fails_closed_before_import(awaiting_amendment, monkeypatch):
    original = migration._atomic_bytes
    def interrupted(path, raw):
        if Path(path).name == 'replacement-plan.json':
            raise OSError('simulated crash after spool replacement')
        original(path, raw)
    monkeypatch.setattr(migration, '_atomic_bytes', interrupted)
    with pytest.raises(OSError, match='simulated crash'):
        amend(awaiting_amendment)
    status = json.loads((awaiting_amendment[0].parent / 'replacement-status.json').read_text())
    assert status['phase'] == 'presentation_amendment_in_progress'
    with pytest.raises(RuntimeError):
        complete(awaiting_amendment, lambda _: pytest.fail('import from incomplete amendment'))


def test_user_identifier_normalization_refuses_merging_users():
    events = [{'traceId':'t','spanId':'o','attributes':[
        otlp.string_attr(otlp.USER_ID, 'fictional-user-one')]},
        {'traceId':'t','spanId':'p','attributes':[otlp.string_attr(otlp.USER_ID, 'customer-one')]}]
    with pytest.raises(RuntimeError, match='merge distinct users'):
        migration._normalize_user_identifiers(events)
