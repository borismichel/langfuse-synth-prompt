"""Post-import mapping migration preserves native experiments and seeded history."""
from copy import deepcopy
from dataclasses import asdict
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from synth import assets, verify
from synth.catalog import dataset_items, load_fixture, score_definitions
from synth.cli import build_parser
from synth.config import Config, Evaluation, Generation, Live, Target
from synth.scores import SCORE_CONTRACT
from synth.state import RunState
from test_model_policy_setup import PolicyAPI
from test_experiment_mapping import native_metadata_shape, select


@pytest.fixture
def mapping_setup(monkeypatch, tmp_path):
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path))
    cfg = Config(Target('https://example.invalid'), Generation(42, 3, date(2026, 10, 8)),
                 Evaluation('openai', 'test-model'), Live('test-model'))
    api = PolicyAPI()
    assets.configure_evaluators(cfg, api=api)
    provisioning = assets.provision_assets(cfg, api=api)
    provisioning['historical_experiments'] = [{'experiment_id': str(i)} for i in range(18)]
    state = RunState(base_url=cfg.target.base_url, project_id='project-test', target_traces=3,
                     seed=42, spooled_events=100, import_status='imported', provisioning=provisioning,
                     run_receipt={'schema_version': 1, 'score_contract': SCORE_CONTRACT,
                                  'run_date': '2026-10-08T00:00:00+00:00', 'seed': 42,
                                  'target_traces': 3, 'spooled_events': 100,
                                  'representative_traces': [{'id': 'history'}], 'spool_sha256': 'a' * 64})
    state.save()
    from langfuse_synth_core.seed import ingest
    monkeypatch.setattr(ingest, 'assert_demo_project', lambda *a: ('project-test', 'Demo'))
    verification_calls = []
    def successful_verification(*args, **kwargs):
        assert not api.writes and not api.updates
        verification_calls.append(True)
        return SimpleNamespace(ok=True)
    monkeypatch.setattr(verify, 'run_verify', successful_verification)
    api.writes.clear()
    def create_mapping_rule(path, body):
        assert not body['enabled'] or body['evaluatorAssignments'], 'API forbids enabled rules with no evaluators'
        api.writes.append((path, deepcopy(body)))
        result = {**deepcopy(body), 'id': f'mapping-rule-{len(api.writes)}'}
        api.created[path + '/' + result['id']] = result
        return deepcopy(result)
    api.create = create_mapping_rule
    return cfg, api, verification_calls


def test_post_seed_setup_preserves_definitions_ids_history_and_native_overrides(mapping_setup):
    cfg, api, checked = mapping_setup
    before = deepcopy(api.created)
    before_state = asdict(RunState.load())
    original_update = api.update
    def update_only_after_every_rule_was_saved(path, body):
        assert checked == [True]
        assert len(api.writes) == 7
        for dataset in assets.experiment_evaluator_prompts():
            assert any(r.get('name') == f"prompt/{dataset['dataset_id']}/experiments"
                       for p, r in api.created.items() if '/evaluation-rules/' in p)
        original_update(path, body)
    api.update = update_only_after_every_rule_was_saved
    result = assets.configure_evaluator_mappings(cfg, api=api, log=lambda _: None)
    assert len(api.writes) == 7 and len(api.updates) == 9
    assert len(result['experiment_rules']) == 7
    assert not {'DS-04', 'DS-07'} & result['experiment_rules'].keys()
    assert all(p == '/api/public/v2/evaluation-rules' for p, _ in api.writes)
    after = RunState.load()
    assert after.provisioning['evaluator_mapping_mode'] == 'live'
    assert after.run_receipt == before_state['run_receipt']
    assert after.import_status == before_state['import_status']
    for key in ('prompts', 'datasets', 'score_configs', 'models', 'historical_experiments', 'evaluator_rules'):
        assert after.provisioning[key] == before_state['provisioning'][key]
    for eid, receipt in result['evaluators'].items():
        path = '/api/public/v2/evaluators/' + receipt['id']
        old, current = before[path], api.created[path]
        assert current['variableMapping'] == assets.variable_mapping(eid, live=True)
        assert {k: v for k, v in old.items() if k not in {'variableMapping', 'version', 'versionId'}} == {
            k: v for k, v in current.items() if k not in {'variableMapping', 'version', 'versionId'}}
        assert current['id'] == old['id']
    for prompt in assets.experiment_evaluator_prompts():
        receipt = result['experiment_rules'][prompt['dataset_id']]
        rule = api.created['/api/public/v2/evaluation-rules/' + receipt['id']]
        expected = assets.experiment_rule_body(prompt, after.provisioning['datasets'][prompt['dataset_id']]['id'], result['evaluators'])
        assert assets._experiment_rule_matches(rule, expected)
        assert len(rule['filter']) == 2
    api.writes.clear(); api.updates.clear(); checked.clear()
    saved = Path(RunState.state_path()).read_bytes()
    assert assets.configure_evaluator_mappings(cfg, api=api, log=lambda _: None) == result
    assert not api.writes and not api.updates
    assert Path(RunState.state_path()).read_bytes() == saved


@pytest.mark.parametrize('mutation', ['missing', 'dry_run', 'importing', 'wrong_target', 'wrong_seed',
                                      'missing_experiments', 'wrong_date', 'bad_hash'])
def test_incomplete_import_never_reads_or_writes_remote(mapping_setup, monkeypatch, mutation):
    cfg, api, _ = mapping_setup
    path = Path(RunState.state_path())
    state = RunState.load()
    if mutation == 'missing': path.unlink()
    else:
        if mutation == 'dry_run': state.dry_run = True
        if mutation == 'importing': state.import_status = 'importing'
        if mutation == 'wrong_target': state.base_url = 'https://other.invalid'
        if mutation == 'wrong_seed': state.seed = 99
        if mutation == 'missing_experiments': state.provisioning['historical_experiments'].pop()
        if mutation == 'wrong_date': state.run_receipt['run_date'] = '2026-10-01T00:00:00+00:00'
        if mutation == 'bad_hash': state.run_receipt['spool_sha256'] = ''
        state.save()
    from langfuse_synth_core.seed import ingest
    monkeypatch.setattr(ingest, 'assert_demo_project', lambda *a: pytest.fail('Must guard before networking'))
    with pytest.raises(assets.AssetConflict, match='imported'):
        assets.configure_evaluator_mappings(cfg, api=api)
    assert not api.writes and not api.updates


def test_failed_full_verification_cannot_enable_rules(mapping_setup, monkeypatch):
    cfg, api, _ = mapping_setup
    monkeypatch.setattr(verify, 'run_verify', lambda *a, **k: SimpleNamespace(ok=False))
    with pytest.raises(assets.AssetConflict, match='full verification'):
        assets.configure_evaluator_mappings(cfg, api=api)
    assert not api.writes and not api.updates


@pytest.mark.parametrize('field,bad', [('prompt', 'changed rubric'), ('variableMapping', []),
                                     ('modelConfig', {'provider': 'openai', 'model': 'other'})])
def test_preflight_rejects_changed_evaluator_before_rule_creation(mapping_setup, field, bad):
    cfg, api, _ = mapping_setup
    last = list(RunState.load().provisioning['evaluators'].values())[-1]
    api.created['/api/public/v2/evaluators/' + last['id']][field] = bad
    with pytest.raises(assets.AssetConflict):
        assets.configure_evaluator_mappings(cfg, api=api)
    assert not api.writes and not api.updates


def test_conflicting_dataset_assignment_preflight_prevents_all_changes(mapping_setup):
    cfg, api, _ = mapping_setup
    state = RunState.load()
    prompt = load_fixture('portfolio')['prompts'][-1]
    body = assets.experiment_rule_body(prompt, state.provisioning['datasets'][prompt['dataset_id']]['id'], state.provisioning['evaluators'])
    body['evaluatorAssignments'][0]['variableMapping'] = []
    api.created['/api/public/v2/evaluation-rules/conflict'] = {**body, 'id': 'conflict'}
    with pytest.raises(assets.AssetConflict, match='conflicts'):
        assets.configure_evaluator_mappings(cfg, api=api)
    assert not api.writes and not api.updates


def test_dataset_rule_failure_never_changes_evaluator_defaults(mapping_setup):
    cfg, api, _ = mapping_setup
    def failed_create(path, body):
        raise TimeoutError('Unknown create outcome')
    api.create = failed_create
    with pytest.raises(TimeoutError):
        assets.configure_evaluator_mappings(cfg, api=api)
    assert not api.updates


def test_mapping_contract_resolves_all_accepted_dataset_contexts():
    for prompt in load_fixture('portfolio')['prompts']:
        for item in dataset_items(prompt['id']):
            expected = {'current_user_message': item['input']['user_message'],
                        'prior_messages': item['input']['conversation_history'],
                        'reference_context': item['input']['reference_context']}
            native = native_metadata_shape(assets.experiment_item_metadata(item))
            for eid in prompt['evaluation_ids']:
                if score_definitions()[eid]['producer'] != 'llm-judge': continue
                for live, source in ((True, expected), (False, native)):
                    for mapping in assets.variable_mapping(eid, live=live):
                        if mapping['source'] == 'output':
                            assert 'jsonPath' not in mapping
                            continue
                        assert select(source, mapping['jsonPath']) == expected[mapping['variable']]


def test_verifier_checks_saved_native_assignments_and_live_defaults(mapping_setup):
    cfg, api, _ = mapping_setup
    result = assets.configure_evaluator_mappings(cfg, api=api, log=lambda _: None)
    provisioning = deepcopy(RunState.load().provisioning)
    # Historical readback is covered by the full migration preflight, not this
    # focused configuration check (which must never access a real project).
    provisioning['historical_experiments'] = []
    checks = {name: ok for name, ok, _ in assets.verify_assets(cfg, provisioning, api=api)}
    assert all(checks['experiment-rule-' + p['dataset_id']] for p in assets.experiment_evaluator_prompts())
    assert checks['experiment-rule-coverage']
    for eid in result['evaluators']:
        assert checks['evaluator-' + eid]
    first = next(iter(result['experiment_rules'].values()))
    api.created['/api/public/v2/evaluation-rules/' + first['id']]['evaluatorAssignments'][0]['variableMapping'] = []
    evaluator = result['evaluators']['E-02']
    api.created['/api/public/v2/evaluators/' + evaluator['id']]['variableMapping'] = assets.variable_mapping('E-02', live=False)
    checks = {name: ok for name, ok, _ in assets.verify_assets(cfg, provisioning, api=api)}
    assert not checks['experiment-rule-DS-01']
    assert not checks['evaluator-E-02']


def test_update_modes_are_explicit_and_mutually_exclusive():
    parser = build_parser()
    args = parser.parse_args(['configure-evaluators', '--config', 'config.yaml', '--update-mappings'])
    assert args.update_mappings and not args.update_model
    with pytest.raises(SystemExit):
        parser.parse_args(['configure-evaluators', '--config', 'config.yaml', '--update-mappings', '--update-model'])


@pytest.mark.parametrize('prompt_id', ['PR-04', 'PR-07'])
def test_deterministic_only_datasets_cannot_create_enabled_empty_rules(prompt_id):
    prompt = next(p for p in load_fixture('portfolio')['prompts'] if p['id'] == prompt_id)
    with pytest.raises(assets.AssetConflict, match='no managed LLM evaluators'):
        assets.experiment_rule_body(prompt, 'dataset-id', {})


def test_resume_reuses_existing_rules_before_updating_any_defaults(mapping_setup):
    cfg, api, _ = mapping_setup
    state = RunState.load()
    existing = {}
    for prompt in assets.experiment_evaluator_prompts()[:3]:
        body = assets.experiment_rule_body(prompt, state.provisioning['datasets'][prompt['dataset_id']]['id'], state.provisioning['evaluators'])
        identifier = 'existing-' + prompt['dataset_id']
        api.created['/api/public/v2/evaluation-rules/' + identifier] = {**body, 'id': identifier}
        existing[prompt['dataset_id']] = identifier
    result = assets.configure_evaluator_mappings(cfg, api=api, log=lambda _: None)
    assert len(api.writes) == 4 and len(api.updates) == 9
    assert all(result['experiment_rules'][dataset]['id'] == identifier for dataset, identifier in existing.items())
