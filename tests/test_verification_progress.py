"""Long deployment reads must be visible before their results become available."""
import os
from pathlib import Path
import selectors
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('command', ['verify', 'configure-evaluators', 'configure-experiments', 'setup-target'])
def test_cli_reports_pending_work_while_remote_read_is_blocked(tmp_path, command):
    env = {key: value for key, value in os.environ.items()
           if not any(word in key for word in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD'))}
    env.pop('PYTHONUNBUFFERED', None)
    env.update(PYTHONPATH=str(ROOT / 'src'), SYNTH_STATE_DIR=str(tmp_path))
    script = '''
import sys
from types import SimpleNamespace
from synth import assets, progress, verify
from synth.cli import main
from synth.config import load_config
from synth.scores import SCORE_CONTRACT
from synth.state import RunState
from langfuse_synth_core.seed import ingest
progress.PROGRESS_INTERVAL_SECONDS = 0.05
def blocked(*args, **kwargs):
    print('REMOTE_READ_BLOCKED', file=sys.stderr, flush=True)
    sys.stdin.readline()
    raise RuntimeError('private request payload must never enter progress')
ingest.assert_demo_project = lambda *args: ('project-test', 'test-demo')
if sys.argv[2] == 'setup-target':
    ingest.assert_demo_project = blocked
cfg = load_config(sys.argv[1])
RunState(base_url=cfg.target.base_url, seed=cfg.generation.seed,
         target_traces=cfg.generation.target_traces, project_id='project-test',
         import_status='imported', spooled_events=1,
         provisioning={'project_id':'project-test', 'historical_experiments':[{}]*18},
         run_receipt={'score_contract': SCORE_CONTRACT, 'schema_version':1,
         'run_date':'2026-10-12T00:00:00+00:00', 'seed':cfg.generation.seed,
         'target_traces':cfg.generation.target_traces, 'spooled_events':1, 'spool_sha256':'a'*64,
         'representative_traces': [{'id': 'trace-test', 'observations': [], 'scores': []}]}).save()
verify.TargetProfile.detect = lambda *args: SimpleNamespace(
    resolved=lambda: SimpleNamespace(reader=lambda: SimpleNamespace(trace=blocked)))
assets.AssetAPI.read = blocked
command = 'configure-evaluators' if sys.argv[2] in {'configure-experiments', 'setup-target'} else sys.argv[2]
extra = ['--update-mappings'] if sys.argv[2] == 'configure-experiments' else []
main([command, '--config', sys.argv[1], *extra])
'''
    process = subprocess.Popen(
        [sys.executable, '-c', script, str(ROOT / 'config/demo.yaml'), command],
        cwd=tmp_path, env=env, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        with selectors.DefaultSelector() as ready:
            ready.register(process.stderr, selectors.EVENT_READ)
            assert ready.select(timeout=10), 'Command never reached the remote read'
            assert b'REMOTE_READ_BLOCKED' in os.read(process.stderr.fileno(), 4096)
        output = b''
        with selectors.DefaultSelector() as ready:
            ready.register(process.stdout, selectors.EVENT_READ)
            for _ in range(20):
                assert ready.select(timeout=1), 'No progress while the remote read is blocked'
                output += os.read(process.stdout.fileno(), 65536)
                if b'Still waiting' in output:
                    break
        assert b'Starting' in output
        assert b'Still waiting' in output
        assert b'private request payload' not in output
        assert process.poll() is None
    finally:
        process.terminate()
        process.communicate(timeout=5)


def test_asset_check_result_is_reported_before_next_read():
    from synth.assets import verify_assets
    from synth.config import Config, Target, Generation

    lines = []
    results_seen_before_next_read = []

    class API:
        reads = 0

        def read(self, *args, **kwargs):
            self.reads += 1
            if self.reads == 1:
                return {'data': [{'id': 'project-test'}]}
            results_seen_before_next_read.append(any('PASS asset-project' in line for line in lines))
            return {}

    verify_assets(Config(Target(), Generation()), {'project_id': 'project-test'}, api=API(), log=lines.append)
    assert results_seen_before_next_read and all(results_seen_before_next_read)


def test_progress_stops_after_failure_and_omits_exception_payload(monkeypatch):
    import threading
    from synth import progress

    monkeypatch.setattr(progress, 'PROGRESS_INTERVAL_SECONDS', 0.01)
    waiting = threading.Event()
    lines = []

    def log(line):
        lines.append(line)
        if 'Still waiting' in line:
            waiting.set()

    before = set(threading.enumerate())
    with pytest.raises(RuntimeError):
        with progress.progress_scope('Starting controlled read.', log):
            assert waiting.wait(1)
            raise RuntimeError('SECRET request payload')
    assert set(threading.enumerate()) == before
    assert 'Work stopped (RuntimeError)' in lines[-1]
    assert all('SECRET' not in line for line in lines)


def test_verification_reads_every_trace_once_but_stops_retries_at_deadline(tmp_path, monkeypatch):
    from synth import assets
    from synth.config import Config, Generation, Target, Verification
    from synth.scores import SCORE_CONTRACT
    from synth.state import RunState
    from synth.verify import run_verify

    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path))
    monkeypatch.setattr(assets, 'verify_assets', lambda *a, **k: [])
    cfg = Config(Target(), Generation(target_traces=2), verification=Verification(timeout_seconds=10, poll_seconds=1))
    RunState(base_url=cfg.target.base_url, seed=42, target_traces=2, project_id='project-test',
             import_status='imported', run_receipt={'score_contract': SCORE_CONTRACT,
             'representative_traces': [{'id': name} for name in ['a', 'b']]}).save()
    elapsed, reads = [0], []

    class Reader:
        def trace(self, tid):
            reads.append(tid)
            elapsed[0] += 20 if len(reads) > 2 else 1
            return None

    result = run_verify(cfg, reader=Reader(), clock=lambda: elapsed[0],
                        sleep=lambda seconds: elapsed.__setitem__(0, elapsed[0] + seconds), log=lambda _: None)
    assert reads == ['a', 'b', 'a']
    assert {c.name for c in result.checks if not c.ok} == {'trace:a', 'trace:b'}
