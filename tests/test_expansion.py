"""An imported pilot can grow once without rewriting any existing project data."""
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
from datetime import date, datetime, timezone
import json
from pathlib import Path

import pytest
from langfuse_synth_core.seed import otlp

from synth import expansion, seed
from synth.cli import main
from synth.config import Config, Generation, Target
from synth.materialize import build_historical_experiment_events
from synth.receipt import attributes
from synth.state import RunState


@pytest.fixture
def pilot(monkeypatch, tmp_path):
    old = tmp_path / 'pilot'
    new = tmp_path / 'expanded'
    monkeypatch.setenv('SYNTH_STATE_DIR', str(old))
    monkeypatch.setenv('SYNTH_OUT_DIR', str(tmp_path / 'out'))
    monkeypatch.delenv('LANGFUSE_BASE_URL', raising=False)
    cfg = Config(Target('https://example.invalid'), Generation(42, 6, date(2026, 10, 9)))
    spool = old / 'events.ndjson'
    seed.run_seed(cfg, dry_run=True, spool_path=spool, log=lambda _: None)
    events = [json.loads(line) for line in spool.read_text().splitlines()]
    state = RunState.load()
    state.dry_run = False
    state.import_status = 'imported'
    state.project_id = 'project-test'
    _, links = build_historical_experiment_events({'seed': 42}, run_date=datetime(2026, 10, 9, 12, tzinfo=timezone.utc))
    state.provisioning = {'project_id': 'project-test', 'historical_experiments': links, 'retained': 'all-assets'}
    state.save()
    (old / 'events.ndjson.imported').write_text('original import marker')
    snapshot = {path: path.read_bytes() for path in old.iterdir()}
    rows = [{'id': e['spanId'], 'traceId': e['traceId'], 'projectId': state.project_id,
             'sessionId': attributes(e).get(otlp.SESSION_ID)} for e in events if otlp.is_span(e)]
    rows.append({'id': 'unrelated-observation', 'traceId': 'unrelated-live-trace',
                 'projectId': state.project_id, 'sessionId': 'unrelated-live-session'})
    scores = [{'id': e['body']['id'], 'projectId': state.project_id} for e in events if not otlp.is_span(e)]
    calls, imported = [], []

    class ReadOnlyAPI:
        def read(self, path, params):
            calls.append((path, params))
            # Exercise two pages, including when the final page is short.
            data = rows if path.endswith('observations') else scores
            return {'data': data[2:] if params.get('cursor') else data[:2],
                    'meta': {'cursor': None if params.get('cursor') else 'next'}}

    monkeypatch.setattr(expansion, 'AssetAPI', lambda _: ReadOnlyAPI())
    monkeypatch.setattr(expansion, 'assert_demo_project', lambda *a: ('project-test', 'demo'))
    monkeypatch.setattr(expansion, 'verify_assets', lambda *a, **kw: [('assets', True, 'verified')])
    monkeypatch.setenv('LANGFUSE_PUBLIC_KEY', 'test-public')
    monkeypatch.setenv('LANGFUSE_SECRET_KEY', 'test-secret')

    def import_once(self, path, **kwargs):
        assert self.max_retries == 1 and kwargs['confirm_cleared'] is False
        imported.extend(json.loads(line) for line in path.read_text().splitlines())

    monkeypatch.setattr(expansion.Ingestor, 'import_spool', import_once)
    monkeypatch.setenv('SYNTH_STATE_DIR', str(new))
    cfg.generation.target_traces = 30
    return cfg, spool, state, snapshot, rows, scores, calls, imported


def run(pilot):
    return seed.run_seed(pilot[0], expand_existing=pilot[1], log=lambda _: None)


def test_expansion_only_imports_disjoint_history_and_preserves_original_bytes(pilot):
    cfg, spool, previous, snapshot, rows, _, calls, imported = pilot
    delta = run(pilot)
    state = RunState.load()
    assert all(path.read_bytes() == content for path, content in snapshot.items())
    assert state.provisioning == previous.provisioning
    assert state.target_traces == 30 and state.run_receipt['actual_traces'] == 48
    assert state.expansion['supplement_seed'] == 43
    assert state.expansion['added_history_traces'] == 24
    assert state.expansion['status'] == state.import_status == 'imported'
    assert state.expansion['previous_live_observations'] == len(rows)
    assert state.expansion['added_events'] == len(imported)
    assert {e['traceId'] for e in imported if otlp.is_span(e)}.isdisjoint({r['traceId'] for r in rows})
    assert all(attributes(e).get(otlp.ENVIRONMENT) != 'experiment' for e in imported if otlp.is_span(e))
    combined = Path(state.expansion['combined_evidence'])
    assert combined.read_bytes() == spool.read_bytes() + delta.read_bytes()
    assert state.spooled_events == previous.spooled_events + len(imported)
    assert Path(state.expansion['combined_evidence']).name == 'combined-evidence.ndjson'
    assert (delta.parent / 'pre-expansion-state.json').read_bytes() == snapshot[spool.parent / '.synth_state.json']
    assert any(p['cursor'] == 'next' for _, p in calls if 'cursor' in p)
    assert all(p['fromStartTime'] == '1970-01-01T00:00:00Z' for path, p in calls if path.endswith('observations'))


@pytest.mark.parametrize('change', ['hash', 'failed', 'dry', 'date', 'seed', 'count', 'score-contract', 'expanded', 'missing-experiment'])
def test_invalid_pilot_rejected_before_network(pilot, monkeypatch, change):
    cfg, spool, state, *_ = pilot
    if change == 'hash': spool.write_text(spool.read_text() + '\n')
    elif change == 'failed': state.import_status = 'failed'
    elif change == 'dry': state.dry_run = True
    elif change == 'date': cfg.generation.as_of_date = date(2026, 10, 8)
    elif change == 'seed': cfg.generation.seed += 1
    elif change == 'count': cfg.generation.target_traces = state.target_traces
    elif change == 'score-contract': state.run_receipt['score_contract'] = 'old'
    elif change == 'expanded': state.expansion = {'status': 'failed'}
    else: state.provisioning['historical_experiments'].pop()
    state.save(str(spool.parent / '.synth_state.json'))
    monkeypatch.setattr(expansion, 'assert_demo_project', lambda *a: pytest.fail('Invalid local receipt reached network'))
    with pytest.raises(RuntimeError): run(pilot)
    assert not pilot[-1]


@pytest.mark.parametrize('change', ['missing', 'duplicate', 'extra-old', 'foreign', 'trace-collision', 'span-collision', 'session-collision', 'score-collision'])
def test_live_inventory_discrepancies_block_all_imports(pilot, change):
    cfg, spool, state, _, rows, scores, *_ = pilot
    _, supplement, _ = expansion.prepare_expansion(cfg, state, spool)
    span = next(e for e in supplement if otlp.is_span(e))
    if change == 'missing': rows.pop(0)
    elif change == 'duplicate': rows.append(deepcopy(rows[0]))
    elif change == 'extra-old': rows.append({**rows[0], 'id': 'extra-observation'})
    elif change == 'foreign': rows[0]['projectId'] = 'wrong-project'
    elif change == 'trace-collision': rows[-1]['traceId'] = span['traceId']
    elif change == 'span-collision': rows[-1]['id'] = span['spanId']
    elif change == 'session-collision': rows[-1]['sessionId'] = next(iter(expansion._sessions(supplement)))
    else: scores.append({'id': next(e['body']['id'] for e in supplement if not otlp.is_span(e)), 'projectId': state.project_id})
    with pytest.raises(RuntimeError): run(pilot)
    assert not pilot[-1]
    assert not (spool.parent / '.history-expansion-attempt.json').exists()


def test_project_or_asset_mismatch_has_no_write(pilot, monkeypatch):
    monkeypatch.setattr(expansion, 'assert_demo_project', lambda *a: ('other-project', 'demo'))
    with pytest.raises(RuntimeError, match='authenticated project'): run(pilot)
    monkeypatch.setattr(expansion, 'assert_demo_project', lambda *a: ('project-test', 'demo'))
    monkeypatch.setattr(expansion, 'verify_assets', lambda *a, **kw: [('wrong-asset', False, 'mismatch')])
    with pytest.raises(RuntimeError, match='read-only verification'): run(pilot)
    assert not pilot[-1]


@pytest.mark.parametrize('fail', [False, True])
def test_attempt_cannot_be_retried_even_in_another_destination(pilot, monkeypatch, tmp_path, fail):
    if fail:
        def ambiguous(self, **kwargs):
            raise RuntimeError('ambiguous transport result')
        monkeypatch.setattr(expansion.Ingestor, 'import_spool', ambiguous)
        with pytest.raises(RuntimeError, match='ambiguous'): run(pilot)
        assert RunState.load().import_status == 'failed'
    else:
        run(pilot)
    before = Path(RunState.state_path()).read_bytes()
    with pytest.raises(RuntimeError, match='empty state directory'): run(pilot)
    assert Path(RunState.state_path()).read_bytes() == before
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path / 'another-destination'))
    monkeypatch.setattr(expansion, 'assert_demo_project', lambda *a: pytest.fail('Repeat must fail before network'))
    with pytest.raises(RuntimeError, match='already prepared or attempted'): run(pilot)


@pytest.mark.parametrize('meta', [{'cursor': 'same'}, {'truncated': True}])
def test_incomplete_cursor_inventory_fails_closed(meta):
    class API:
        def read(self, *args): return {'data': [], 'meta': meta}
    with pytest.raises(RuntimeError): expansion.observation_inventory(API())


def test_cli_expansion_dispatch_and_modes(pilot, monkeypatch):
    monkeypatch.setattr('synth.cli.load_config', lambda *a, **kw: pilot[0])
    assert main(['seed', '--config', 'unused', '--expand-existing', str(pilot[1])]) == 0
    with pytest.raises(SystemExit):
        main(['seed', '--config', 'unused', '--expand-existing', str(pilot[1]), '--dry-run'])


def test_full_volume_plan_preserves_coherent_sessions_and_fixed_experiments(pilot):
    cfg, spool, state, *_ = pilot
    cfg.generation.target_traces = 1620
    previous, supplement, provenance = expansion.prepare_expansion(cfg, state, spool)
    assert provenance['added_history_traces'] == 1614
    assert len({expansion._trace(e) for e in previous + supplement}) == 1638
    roots = [e for e in supplement if otlp.is_span(e) and not e.get('parentSpanId')]
    by_session = {}
    for root in roots:
        a = attributes(root)
        sid = a.get(otlp.SESSION_ID)
        if sid:
            by_session.setdefault(sid, []).append(a)
    assert by_session
    for session in by_session.values():
        lengths = {int(a[otlp.OBS_METADATA_PREFIX + 'session_length']) for a in session}
        turns = {int(a[otlp.OBS_METADATA_PREFIX + 'session_turn']) for a in session}
        assert lengths == {len(session)} and turns == set(range(1, len(session) + 1))
