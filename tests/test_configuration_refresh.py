"""An existing import can adopt evaluator receipts without replaying any events."""
from copy import deepcopy
from dataclasses import asdict
from datetime import date
from pathlib import Path

import pytest

from synth import assets, seed
from synth.cli import main
from synth.config import Config, Evaluation, Generation, Live, Target
from synth.state import RunState
from test_assets import FakeAPI


@pytest.fixture
def imported(monkeypatch, tmp_path):
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path / 'state'))
    monkeypatch.setenv('SYNTH_OUT_DIR', str(tmp_path / 'out'))
    monkeypatch.delenv('LANGFUSE_BASE_URL', raising=False)
    cfg = Config(Target('https://example.invalid'), Generation(42, 3, date(2026, 10, 8)),
                 Evaluation('openai', 'test-model'), Live('test-model'))
    spool = tmp_path / 'events.ndjson'
    seed.run_seed(cfg, dry_run=True, spool_path=spool, log=lambda _: None)
    state = RunState.load()
    state.dry_run = False
    state.import_status = 'imported'
    state.project_id = 'project-test'
    state.project_name = 'demo test'
    state.provisioning = {
        'project_id': 'project-test', 'prompts': {'prompt': {'id': 'prompt-id', 'version': 7}},
        'datasets': {'dataset': {'id': 'dataset-id', 'version': 'snapshot'}},
        'historical_experiments': [{'experiment_id': 'experiment-id', 'trace_id': 'trace-id'}],
        'score_configs': {'E-01': {'id': 'score-id'}}, 'models': {'model': {'id': 'model-id'}},
        'evaluators': {}, 'evaluator_rules': {}, 'manual_prerequisites': ['Check label permissions'],
        'missing': ['Set evaluation.provider/model and run the separate model-using evaluator setup before seed.',
                    'Selected judge provider/model is not available through a configured Langfuse LLM connection.',
                    'E-01: managed evaluator requires separate model-using setup before seed.',
                    'E-04: live rule requires separate evaluator setup before seed.',
                    assets.LEGACY_NULLABLE_GATE, 'Unrelated prerequisite'],
    }
    state.save()
    marker = tmp_path / 'import-marker'
    marker.write_text('completed import')
    api = FakeAPI()
    configured = assets.configure_evaluators(cfg, api=api)
    api.writes.clear()
    monkeypatch.setattr(assets, 'AssetAPI', lambda _: api)
    monkeypatch.setattr(seed, 'assert_demo_project', lambda *a: ('project-test', 'demo test'))

    def forbidden(*args, **kwargs):
        raise AssertionError('Refresh must not generate, provision, import, or rewrite artifacts')

    for name in ('build_events', 'build_historical_experiment_events', 'deliver_artifacts'):
        monkeypatch.setattr(seed, name, forbidden)
    monkeypatch.setattr(seed.Ingestor, 'from_env', forbidden)
    monkeypatch.setattr(assets, 'provision_assets', forbidden)
    monkeypatch.setattr(api, 'create', forbidden)
    return cfg, spool, marker, api, configured


def refresh(imported):
    cfg, spool, *_ = imported
    return seed.run_seed(cfg, spool_path=spool, refresh_configuration=True, log=lambda _: None)


def test_refresh_preserves_import_and_all_non_evaluator_evidence(imported):
    _, spool, marker, api, configured = imported
    before = asdict(RunState.load())
    immutable = {p: p.read_bytes() for p in (spool, marker, spool.parent / 'out' / 'DEMO_SCRIPT.md')}
    assert refresh(imported) == spool
    after = asdict(RunState.load())
    expected = deepcopy(before)
    expected['evaluator_rules'] = configured['evaluator_rules']
    expected['provisioning'].update(evaluators=configured['evaluators'], evaluator_rules=configured['evaluator_rules'],
                                    missing=['Unrelated prerequisite', *configured['missing']])
    assert after == expected
    assert len(after['evaluator_rules']) == 10
    assert not any('E-02/E-03' in item for item in after['provisioning']['missing'])
    assert all(p.read_bytes() == contents for p, contents in immutable.items())
    assert not api.writes
    saved = Path(RunState.state_path()).read_bytes()
    refresh(imported)
    assert Path(RunState.state_path()).read_bytes() == saved


@pytest.mark.parametrize('change', [
    'missing-state', 'dry-run', 'failed', 'importing', 'spooled-only', 'wrong-host',
    'wrong-project', 'wrong-seed', 'wrong-count', 'wrong-date', 'missing-receipt',
    'receipt-seed', 'receipt-count', 'receipt-events', 'receipt-hash', 'receipt-date',
    'receipt-traces', 'receipt-schema',
])
def test_invalid_receipt_fails_before_any_network(imported, monkeypatch, change):
    state = RunState.load()
    path = Path(RunState.state_path())
    if change == 'dry-run': state.dry_run = True
    elif change in ('failed', 'importing', 'spooled-only'): state.import_status = change
    elif change == 'wrong-host': state.base_url = 'https://other.invalid'
    elif change == 'wrong-project': state.provisioning['project_id'] = 'another-project'
    elif change == 'wrong-seed': state.seed += 1
    elif change == 'wrong-count': state.target_traces += 1
    elif change == 'wrong-date': state.run_receipt['run_date'] = '2026-10-07T00:00:00+00:00'
    elif change == 'missing-receipt': state.run_receipt = {}
    elif change == 'receipt-seed': state.run_receipt['seed'] += 1
    elif change == 'receipt-count': state.run_receipt['target_traces'] += 1
    elif change == 'receipt-events': state.run_receipt['spooled_events'] += 1
    elif change == 'receipt-hash': state.run_receipt['spool_sha256'] = ''
    elif change == 'receipt-date': state.run_receipt['run_date'] = 'invalid'
    elif change == 'receipt-traces': state.run_receipt['representative_traces'] = []
    elif change == 'receipt-schema': state.run_receipt['schema_version'] = 0
    state.save()
    before = path.read_bytes()
    if change == 'missing-state': path.unlink()

    def forbidden(*args):
        raise AssertionError('Invalid receipt must be rejected before network')

    monkeypatch.setattr(seed, 'assert_demo_project', forbidden)
    with pytest.raises(RuntimeError, match='receipt'):
        refresh(imported)
    assert (not path.exists()) if change == 'missing-state' else path.read_bytes() == before


def test_authenticated_project_mismatch_does_not_discover_or_save(imported, monkeypatch):
    path = Path(RunState.state_path())
    before = path.read_bytes()
    monkeypatch.setattr(seed, 'assert_demo_project', lambda *a: ('wrong-project', 'demo other'))
    monkeypatch.setattr(imported[3], 'read', lambda *a: pytest.fail('Must not discover another project'))
    with pytest.raises(RuntimeError, match='authenticated project'):
        refresh(imported)
    assert path.read_bytes() == before


@pytest.mark.parametrize('failure', ['connection', 'provider', 'missing-evaluator', 'missing-rule', 'conflict', 'read-error'])
def test_failed_discovery_never_changes_existing_state(imported, monkeypatch, failure):
    cfg, spool, _, api, _ = imported
    if failure == 'connection': api.connected = False
    elif failure == 'provider': cfg.evaluation.provider = ''
    elif failure == 'missing-evaluator':
        api.created = {k: v for k, v in api.created.items() if not k.startswith('/api/public/v2/evaluator')}
    elif failure == 'missing-rule':
        del api.created[next(k for k in api.created if k.startswith('/api/public/v2/evaluation-rules/'))]
    elif failure == 'conflict':
        api.created[next(k for k in api.created if k.startswith('/api/public/v2/evaluators/'))]['prompt'] = 'wrong rubric'
    else:
        monkeypatch.setattr(api, 'read', lambda *a, **kw: (_ for _ in ()).throw(RuntimeError('Read failed')))
    path = Path(RunState.state_path())
    before, spool_before = path.read_bytes(), spool.read_bytes()
    with pytest.raises(RuntimeError):
        refresh(imported)
    assert path.read_bytes() == before and spool.read_bytes() == spool_before
    assert not api.writes


def test_failed_save_is_atomic(imported, monkeypatch):
    path = Path(RunState.state_path())
    before = path.read_bytes()

    def fail_save(self, temporary):
        Path(temporary).write_text('incomplete serialization')
        raise OSError('Disk write failed')

    monkeypatch.setattr(RunState, 'save', fail_save)
    with pytest.raises(OSError, match='Disk write failed'):
        refresh(imported)
    assert path.read_bytes() == before
    assert not list(path.parent.glob('.configuration-*'))


@pytest.mark.parametrize('live_model', ['', 'test-model'])
def test_refresh_reconciles_live_model_gate_only_when_configured(imported, live_model):
    imported[0].live.model = live_model
    gate = 'Select live.model for native prompt experiments; synthetic history model names are not runnable.'
    state = RunState.load()
    state.provisioning['missing'].append(gate)
    state.save()
    refresh(imported)
    assert (gate in RunState.load().provisioning['missing']) is (not bool(live_model))


@pytest.mark.parametrize('options', [{'dry_run': True}, {'do_import': False}])
def test_refresh_rejects_incompatible_generation_modes(imported, options):
    before = Path(RunState.state_path()).read_bytes()
    with pytest.raises(ValueError, match='cannot be combined'):
        seed.run_seed(imported[0], refresh_configuration=True, **options)
    assert Path(RunState.state_path()).read_bytes() == before


def test_cli_refresh_dispatch_and_dry_run_exclusion(imported, monkeypatch):
    monkeypatch.setattr('synth.cli.load_config', lambda *a, **kw: imported[0])
    assert main(['seed', '--config', 'unused.yaml', '--refresh-configuration']) == 0
    assert len(RunState.load().evaluator_rules) == 10
    with pytest.raises(SystemExit) as failure:
        main(['seed', '--config', 'unused.yaml', '--refresh-configuration', '--dry-run'])
    assert failure.value.code == 2


def test_old_numeric_pilot_receipt_requires_fresh_target_before_any_network(imported, monkeypatch):
    state = RunState.load()
    state.run_receipt.pop('score_contract')
    state.save()
    path = Path(RunState.state_path())
    before = path.read_bytes()
    monkeypatch.setattr(seed, 'assert_demo_project', lambda *a: pytest.fail('Must not access old pilot'))
    with pytest.raises(RuntimeError, match='fresh target'):
        refresh(imported)
    assert path.read_bytes() == before
