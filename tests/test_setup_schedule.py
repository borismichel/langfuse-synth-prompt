"""Operator date and rehearsal evidence through the emitted seed spool."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json

import pytest
from langfuse_synth_core.seed.otlp import finalize
from synth.materialize import build_events, build_historical_experiment_events

@pytest.mark.parametrize('anchor,first', [('2026-10-16','2026-09-19'), ('2026-10-18','2026-09-21'), ('2026-10-25','2026-09-28'), ('2026-03-29','2026-03-02'), ('2028-02-29','2028-02-02'), ('2027-01-01','2026-12-05')])
def test_inclusive_28_local_days_bound_every_observation(anchor, first):
    run_date = datetime.fromisoformat(anchor).replace(tzinfo=timezone.utc)
    events = finalize(build_events(270, {'seed':42}, run_date=run_date) + build_historical_experiment_events({'seed':42}, run_date=run_date)[0])
    dates = [datetime.fromtimestamp(int(e[k])/1e9, timezone.utc).astimezone(ZoneInfo('Europe/Berlin')).date().isoformat()
             for e in events if 'spanId' in e for k in ('startTimeUnixNano','endTimeUnixNano')]
    assert min(dates) == first
    assert max(dates) == anchor

@pytest.mark.parametrize('count', [1, 7, 24])
def test_custom_smallest_volumes_include_selected_weekend_day(count):
    events = finalize(build_events(count, {'seed':42}, run_date=datetime(2026,10,18,tzinfo=timezone.utc)))
    assert max(datetime.fromtimestamp(int(e['endTimeUnixNano'])/1e9, timezone.utc).astimezone(ZoneInfo('Europe/Berlin')).date().isoformat() for e in events if 'spanId' in e) == '2026-10-18'


def test_seed_delivers_actual_schedule_artifact(tmp_path, monkeypatch):
    from synth.config import load_config
    from synth.seed import run_seed
    from synth.state import RunState
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path/'state'))
    monkeypatch.setenv('SYNTH_OUT_DIR', str(tmp_path/'out'))
    cfg=load_config('config/demo.yaml', ['generation.target_traces=270', 'generation.as_of_date=2026-10-16'])
    spool=run_seed(cfg, dry_run=True, do_import=False, spool_path=tmp_path/'events.ndjson', log=lambda _:None)
    schedule=json.loads((tmp_path/'out/SCHEDULE.json').read_text())
    assert schedule['requested']=={'as_of_date':'2026-10-16','history_days':28,'timezone':'Europe/Berlin','end':'inclusive'}
    assert RunState.load().run_receipt['schedule'] == schedule
    spans=[json.loads(line) for line in spool.read_text().splitlines() if '"spanId"' in line]
    stamps=[int(e[k]) for e in spans for k in ('startTimeUnixNano','endTimeUnixNano')]
    assert datetime.fromisoformat(schedule['generated_range']['start']).timestamp()==pytest.approx(min(stamps)/1e9)
    assert datetime.fromisoformat(schedule['generated_range']['end']).timestamp()==pytest.approx(max(stamps)/1e9)


def test_rehearsal_is_declared_and_preserves_authored_catalog():
    import yaml
    from synth.catalog import load_fixture
    manifest=yaml.safe_load(open('usecase.yaml'))
    assert manifest['setup']['schedule']=={'timezone':'Europe/Berlin','end':'inclusive','history':{'fixed_days':28}}
    count=manifest['setup']['presets']['quick_rehearsal']['values']['generation.target_traces']
    assert count==270
    events=finalize(build_events(count, {'seed':42}, run_date=datetime(2026,10,16,tzinfo=timezone.utc)))
    from test_generation import attributes, metadata
    spans=[e for e in events if 'spanId' in e]
    assert len({e['traceId'] for e in spans})==270
    assert {metadata(e).get('prompt_id') for e in spans if attributes(e).get('langfuse.observation.type')=='generation'}=={f'PR-{i:02}' for i in range(1,10)}
    assert len(load_fixture('portfolio')['prompts'])==9
    assert len(build_historical_experiment_events({'seed':42},run_date=datetime(2026,10,16,tzinfo=timezone.utc))[1])==18

@pytest.mark.parametrize('count', [270,1620])
def test_preset_seed_readback_preserves_prompt_versions_scores_and_experiments(count, tmp_path, monkeypatch):
    from collections import Counter
    from types import SimpleNamespace
    from langfuse_synth_core.read import Trace, Observation, Score
    from synth.config import load_config
    from synth.seed import run_seed
    from synth.state import RunState
    from synth.verify import verify_trace
    monkeypatch.setenv('SYNTH_STATE_DIR',str(tmp_path/'state'))
    monkeypatch.setenv('SYNTH_OUT_DIR',str(tmp_path/'out'))
    cfg=load_config('config/demo.yaml',[f'generation.target_traces={count}','generation.as_of_date=2026-10-16'])
    spool=run_seed(cfg,dry_run=True,do_import=False,spool_path=tmp_path/'events.ndjson',log=lambda _:None)
    events=[json.loads(line) for line in spool.read_text().splitlines()]
    from test_generation import attributes, metadata
    spans=[e for e in events if 'spanId' in e]
    assert len({e['traceId'] for e in spans})==count+18
    experiments=[e for e in spans if attributes(e).get('langfuse.environment')=='experiment']
    assert len({e['traceId'] for e in experiments})==18
    assert Counter(metadata(e).get('resolved_version') for e in experiments if attributes(e).get('langfuse.observation.type')=='generation')=={2:9,4:9}
    assert {metadata(e).get('prompt_id') for e in spans if attributes(e).get('langfuse.observation.type')=='generation'}=={f'PR-{i:02}' for i in range(1,10)}
    def decode(value):
        if value is None:return None
        try:return json.loads(value)
        except (TypeError,ValueError):return value
    traces={tid:Trace(id=tid,observations=[],scores=[]) for tid in {e['traceId'] for e in spans}}
    for e in spans:
        a=attributes(e)
        traces[e['traceId']].observations.append(Observation(id=e['spanId'],trace_id=e['traceId'],
            parent_id=e.get('parentSpanId') or None,name=e['name'],type=a.get('langfuse.observation.type','span').upper(),
            start_time=datetime.fromtimestamp(int(e['startTimeUnixNano'])/1e9,timezone.utc),
            end_time=datetime.fromtimestamp(int(e['endTimeUnixNano'])/1e9,timezone.utc),
            prompt_name=a.get('langfuse.observation.prompt.name'),
            prompt_version=int(a['langfuse.observation.prompt.version']) if 'langfuse.observation.prompt.version' in a else None,
            session_id=a.get('langfuse.session.id'),input=decode(a.get('langfuse.observation.input')),
            output=decode(a.get('langfuse.observation.output')),metadata=metadata(e)))
    for e in events:
        if e.get('type')!='score-create':continue
        b=e['body']
        traces[b['traceId']].scores.append(Score(id=b['id'],name=b['name'],observation_id=b.get('observationId'),
            data_type=b['dataType'],numeric_value=b['value'] if isinstance(b['value'],(float,int)) else None,
            string_value=b['value'] if isinstance(b['value'],str) else None))
    checks=[verify_trace(SimpleNamespace(trace=traces.get),expected) for expected in RunState.load().run_receipt['representative_traces']]
    assert checks and all(c.ok for c in checks), [(c.name,c.detail) for c in checks if not c.ok]


def test_custom_maximum_finishes_all_observations_inside_selected_dst_day():
    events=finalize(build_events(6000, {'seed':60}, run_date=datetime(2026,10,25,tzinfo=timezone.utc)))
    spans=[e for e in events if 'spanId' in e]
    assert len({e['traceId'] for e in spans})==6000
    assert all(datetime(2026,9,27,22,tzinfo=timezone.utc).timestamp() <= int(e[k])/1e9 < datetime(2026,10,25,23,tzinfo=timezone.utc).timestamp()
               for e in spans for k in ('startTimeUnixNano','endTimeUnixNano'))
    assert any(datetime.fromtimestamp(int(e['endTimeUnixNano'])/1e9,timezone.utc).astimezone(ZoneInfo('Europe/Berlin')).date().isoformat()=='2026-10-25' for e in spans)
