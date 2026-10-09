"""Preflight contract through CLI dispatch, actual v4 counting and isolated processes."""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

import pytest
import yaml
from langfuse_synth_core.seed import otlp
from langfuse_synth_core.seed.count import count_spool

from synth import cli
from synth.config import Config, Generation, Target
from synth.materialize import build_events, build_historical_experiment_events
from synth.preflight import build_plan

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = datetime(2026, 10, 8, tzinfo=timezone.utc)


@pytest.mark.parametrize('count,seed', [(1, 42), (24, 19), (72, 73), (1620, 42)])
def test_plan_matches_actual_seed_wire_including_fixed_experiments(tmp_path, count, seed):
    cfg = Config(Target(), Generation(seed=seed, target_traces=count))
    plan = build_plan(cfg)
    history = build_events(count, {'seed': seed}, run_date=ANCHOR)
    experiments, _ = build_historical_experiment_events({'seed': seed}, run_date=ANCHOR)
    for name, events in [('production_history', history), ('historical_experiments', experiments),
                         ('seed_total', history + experiments)]:
        finalized = otlp.finalize(events)
        spool = tmp_path / f'{name}.ndjson'
        spool.write_text(''.join(json.dumps(event) + '\n' for event in finalized))
        measured = count_spool(spool)
        assert {key: plan[name][key] for key in ('traces', 'observations', 'scores')} == {
            key: measured[key] for key in ('traces', 'observations', 'scores')}
        if name == 'seed_total':
            assert plan[name]['billable_units'] == measured['total']
    assert plan['historical_experiments']['traces'] == 18
    assert plan['cost']['seed_provider_calls'] == plan['cost']['seed_model_usd'] == 0
    assert plan['cost']['langfuse_ingestion_usd'] is None


def test_manifest_plan_runs_without_keys_network_or_state_changes(tmp_path):
    document = yaml.safe_load((ROOT / 'usecase.yaml').read_text())
    stage = next(s for s in document['pipeline'] if s['id'] == 'plan')
    config = ROOT / document['base_config']['default']
    command = shlex.split(stage['run'].replace('{config}', str(config)))
    command += ['--set', 'generation.target_traces=24', '--set', 'generation.seed=19']
    spool = tmp_path / '.synth_spool'
    spool.mkdir()
    for name in ('events.ndjson', 'events.ndjson.imported', '.synth_state.json'):
        (spool / name).write_text(f'preserve existing {name}')
    before = {str(p.relative_to(tmp_path)): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    env = {k: v for k, v in os.environ.items()
           if not any(word in k for word in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD'))}
    env.update(PYTHONPATH=str(ROOT / 'src'), SYNTH_STATE_DIR=str(spool), SYNTH_OUT_DIR=str(tmp_path / 'out'))
    script = '''import socket, sys
def blocked(*args, **kwargs):
    raise AssertionError('plan attempted network access')
socket.socket.connect = socket.socket.connect_ex = socket.getaddrinfo = socket.create_connection = blocked
from synth.cli import main
raise SystemExit(main(sys.argv[1:]))
'''
    process = subprocess.run([sys.executable, '-c', script, *command[1:]], cwd=tmp_path,
                             env=env, text=True, capture_output=True, check=True)
    result = json.loads(process.stdout.splitlines()[-1])
    assert result['seed'] == 19 and result['target_traces'] == 24
    assert result['seed_total']['traces'] == 42
    pattern = stage['parse']['event_count'].removeprefix('regex:')
    assert int(re.search(pattern, process.stdout).group(1)) == 42
    counts_pattern = stage['parse']['plan_counts'].removeprefix('regex:')
    counts = json.loads(re.search(counts_pattern, process.stdout).group(1))
    assert counts == {'version': 1, **{key: result['seed_total'][key]
                                     for key in ('traces', 'observations', 'scores')}}
    assert counts['observations'] + counts['scores'] == result['seed_total']['billable_units']
    assert {str(p.relative_to(tmp_path)): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()} == before


@pytest.mark.parametrize('readback,expected_code', [('ok', 0), ('changed', 1), ('missing', 1)])
def test_probe_cli_uses_core_ingestion_and_v4_observation_readback(monkeypatch, tmp_path, readback, expected_code):
    from langfuse_synth_core import probe
    from langfuse_synth_core.read import LangfuseReader
    from langfuse_synth_core.seed.ingest import Ingestor

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path))
    monkeypatch.setenv('LANGFUSE_BASE_URL', 'https://selected-target.invalid')
    monkeypatch.setenv('LANGFUSE_PUBLIC_KEY', 'test-public')
    monkeypatch.setenv('LANGFUSE_SECRET_KEY', 'test-secret')
    for key in ('LLM_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY'):
        monkeypatch.delenv(key, raising=False)
    calls, uploaded = [], []

    def guard(url, hint):
        assert url == 'https://selected-target.invalid' and hint == 'demo'
        calls.append('guard')
        return 'project', 'demo'

    def flush(self):
        assert calls == ['guard']
        assert self.base_url == 'https://selected-target.invalid'
        uploaded.extend(otlp.finalize(self._events))
        calls.append('write')

    def read(self, path, params=None):
        assert calls[:2] == ['guard', 'write']
        assert path == '/api/public/v2/observations'
        assert params['traceId'] == uploaded[0]['traceId']
        calls.append('read')
        if readback == 'missing':
            return {'data': [], 'meta': {}}
        rows = []
        for event in uploaded:
            start = datetime.fromtimestamp(int(event['startTimeUnixNano']) / 1e9, timezone.utc)
            if readback == 'changed':
                start += timedelta(days=1)
            rows.append({'id': event['spanId'], 'traceId': event['traceId'],
                         'startTime': start.isoformat(), 'type': 'SPAN',
                         'parentObservationId': event.get('parentSpanId')})
        return {'data': rows, 'meta': {}}

    monkeypatch.setattr(probe, 'assert_demo_project', guard)
    monkeypatch.setattr(probe.time, 'sleep', lambda *_: None)
    monkeypatch.setattr(Ingestor, 'flush', flush)
    monkeypatch.setattr(LangfuseReader, '_get', read)
    assert cli.main(['probe', '--config', str(ROOT / 'config/demo.yaml'),
                     '--set', 'generation.seed=73']) == expected_code
    assert len(uploaded) == 2 and all(otlp.is_span(event) for event in uploaded)
    assert len(set(event['traceId'] for event in uploaded)) == 1
    assert calls.count('read') == (10 if readback == 'missing' else 1)
    assert list(tmp_path.iterdir()) == []


def test_probe_guard_failure_prevents_ingestion(monkeypatch):
    from langfuse_synth_core import probe
    from langfuse_synth_core.seed.ingest import Ingestor

    def reject(*args):
        raise RuntimeError('not a demo project')

    def forbidden(*args, **kwargs):
        pytest.fail('probe attempted ingestion after guard rejection')

    monkeypatch.setattr(probe, 'assert_demo_project', reject)
    monkeypatch.setattr(Ingestor, 'from_env', forbidden)
    with pytest.raises(RuntimeError, match='not a demo project'):
        cli.main(['probe', '--config', str(ROOT / 'config/demo.yaml')])
