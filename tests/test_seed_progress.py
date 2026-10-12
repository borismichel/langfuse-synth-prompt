"""Deployment stdout must report work before a slow provisioning request finishes."""
import os
from pathlib import Path
import selectors
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_plan_requires_depot_confirmation_before_setup_or_seed():
    pipeline = yaml.safe_load((ROOT / 'usecase.yaml').read_text())['pipeline']
    plan = next(step for step in pipeline if step['id'] == 'plan')
    assert plan.get('gate') == 'confirm'
    assert pipeline.index(plan) < next(i for i, step in enumerate(pipeline) if step['id'] == 'configure-evaluators')


def test_seed_progress_reaches_pipe_while_asset_setup_is_still_running(tmp_path):
    env = {k: v for k, v in os.environ.items()
           if not any(word in k for word in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD'))}
    env.pop('PYTHONUNBUFFERED', None)  # CLI must also work outside the container.
    env.update(PYTHONPATH=str(ROOT / 'src'), SYNTH_STATE_DIR=str(tmp_path))
    script = '''import sys
from synth import assets, seed
from synth.cli import main
seed.assert_demo_project = lambda *args: ('test-project', 'test-demo')
def hold_provisioning(cfg, **kwargs):
    print('Provisioning entered', file=sys.stderr, flush=True)
    sys.stdin.readline()
    raise RuntimeError('Test stopped before network or import')
assets.provision_assets = hold_provisioning
main(['seed', '--config', sys.argv[1], '--set', 'generation.target_traces=1'])
'''
    process = subprocess.Popen([sys.executable, '-c', script, str(ROOT / 'config/demo.yaml')],
                               cwd=tmp_path, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        with selectors.DefaultSelector() as ready:
            ready.register(process.stderr, selectors.EVENT_READ)
            assert ready.select(timeout=10), 'Seed never reached provisioning'
            assert b'Provisioning entered' in os.read(process.stderr.fileno(), 4096)
        with selectors.DefaultSelector() as progress:
            progress.register(process.stdout, selectors.EVENT_READ)
            assert progress.select(timeout=2), 'No seed progress reached stdout while provisioning was running'
            output = os.read(process.stdout.fileno(), 65536).decode()
        assert 'provision' in output.lower(), output
        assert process.poll() is None, 'Progress must arrive while work is in progress'
    finally:
        process.terminate()
        process.communicate(timeout=5)
