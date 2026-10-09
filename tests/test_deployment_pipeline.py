"""A normal Depot deployment must prepare judges without model calls in seed."""
from pathlib import Path
import shlex
from types import SimpleNamespace

import yaml

from synth import assets, cli


def test_manifest_dispatches_setup_seed_experiment_setup_and_final_verification(monkeypatch):
    manifest = Path(__file__).resolve().parents[1] / 'usecase.yaml'
    document = yaml.safe_load(manifest.read_text())
    stages = document['pipeline']
    assert [stage['id'] for stage in stages] == [
        'configure-evaluators', 'seed', 'configure-experiments', 'verify',
    ]
    assert all(stage['fatal'] is True for stage in stages)
    calls = []
    configs = []
    from langfuse_synth_core.seed import ingest
    monkeypatch.setattr(ingest, 'assert_demo_project', lambda *a: ('project', 'demo'))

    def setup(cfg, *, update_model):
        assert not calls and update_model is False
        configs.append(cfg)
        calls.append('prepare-model-validated-evaluators')
        return {'evaluators': {'judge': {}}, 'missing': []}

    def seed(cfg, **kwargs):
        assert calls == ['prepare-model-validated-evaluators']
        assert kwargs == {'dry_run': False, 'refresh_configuration': False, 'expand_existing': None}
        configs.append(cfg)
        calls.append('import-model-free-history')

    def mappings(cfg):
        assert calls == ['prepare-model-validated-evaluators', 'import-model-free-history']
        configs.append(cfg)
        calls.append('verify-history-before-enabling-experiment-rules')
        return {'evaluators': {'judge': {}}, 'missing': []}

    def verify(cfg):
        assert calls[-1] == 'verify-history-before-enabling-experiment-rules'
        configs.append(cfg)
        calls.append('verify-final-configuration')
        return SimpleNamespace(ok=True)

    monkeypatch.setattr(assets, 'configure_evaluators', setup)
    monkeypatch.setattr(assets, 'configure_evaluator_mappings', mappings)
    monkeypatch.setattr(cli, 'run_seed', seed)
    monkeypatch.setattr(cli, 'run_verify', verify)
    config_path = manifest.parent / document['base_config']['default']
    for stage in stages:
        command = shlex.split(stage['run'].replace('{config}', str(config_path)))
        assert command[0] == 'synth'
        assert cli.main(command[1:]) == 0
    assert calls == ['prepare-model-validated-evaluators', 'import-model-free-history',
                     'verify-history-before-enabling-experiment-rules', 'verify-final-configuration']
    assert all(cfg == configs[0] for cfg in configs)
