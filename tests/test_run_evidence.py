"""Evidence tests: prevent unrelated data and partial imports from passing."""
from datetime import datetime, timezone
from types import SimpleNamespace
from pathlib import Path
import pytest
from langfuse_synth_core.read import Observation, Score, Trace
from synth.config import Config, Generation, Target, Verification
from synth.state import RunState
from synth.verify import verify_trace, run_verify

@pytest.fixture
def isolated(monkeypatch,tmp_path):
    monkeypatch.setenv('SYNTH_STATE_DIR',str(tmp_path/'state'))
    monkeypatch.setenv('SYNTH_OUT_DIR',str(tmp_path/'out'))
    monkeypatch.delenv('LANGFUSE_BASE_URL',raising=False)
    return tmp_path


def expected():
    return {'id':'a'*32,'observations':[{'id':'b'*16,'parent_id':None,'type':'AGENT','name':'request',
        'start_time':'2026-01-01T00:00:00+00:00','prompt_name':None,'prompt_version':None,
        'session_id':'session1','input':{'messages':[{'role':'user','content':'No, that is wrong.'}]},
        'output':[{'role':'assistant','content':'Let me clarify.'}],'evaluation_subject':'user_input'}],
        'scores':[{'id':'s1','name':'user_disagreement','observationId':'b'*16,'value':1,'dataType':'NUMERIC'}]}


def reader_for(item):
    return SimpleNamespace(trace=lambda _:item)


def actual():
    e=expected(); o=e['observations'][0]
    return Trace(id=e['id'], observations=[Observation(id=o['id'], trace_id=e['id'],
        name=o['name'],type=o['type'],start_time=datetime(2026,1,1,tzinfo=timezone.utc),
        session_id=o['session_id'],input=o['input'],output=o['output'],metadata={'evaluation_subject':'user_input'})],
        scores=[Score(id='s1',name='user_disagreement',observation_id=o['id'],numeric_value=1)])


def test_exact_observation_subjects_required():
    value=actual()
    assert verify_trace(reader_for(value),expected()).ok
    value.scores[0]=Score(id='s1',name='user_disagreement',observation_id='c'*16,numeric_value=1)
    assert not verify_trace(reader_for(value),expected()).ok


def test_missing_current_trace_and_duplicate_observation_fail():
    assert not verify_trace(reader_for(None),expected()).ok
    value=actual();value.observations.append(value.observations[0])
    assert not verify_trace(reader_for(value),expected()).ok


def test_dry_receipt_cannot_be_live_success(isolated):
    cfg=Config(Target(),Generation(target_traces=1))
    RunState(base_url=cfg.target.base_url,seed=42,target_traces=1,dry_run=True,
             import_status='dry_run',run_receipt={'representative_traces':[expected()]}).save()
    assert not run_verify(cfg,reader=reader_for(actual())).ok


def test_partial_seed_blocks_reimport_before_network(isolated):
    from synth.seed import run_seed
    cfg=Config(Target(),Generation(target_traces=1))
    RunState(import_status='failed',dry_run=False).save()
    with pytest.raises(RuntimeError,match='already records'):
        run_seed(cfg,spool_path=isolated/'events.ndjson')


def test_dry_seed_delivers_runbook_and_evidence(isolated):
    from synth.seed import run_seed
    cfg=Config(Target(),Generation(target_traces=3,as_of_date=datetime(2026,1,1).date()))
    path=run_seed(cfg,dry_run=True,spool_path=isolated/'events.ndjson',log=lambda _:None)
    state=RunState.load()
    assert path.is_file() and state.dry_run and state.import_status=='dry_run'
    assert state.run_receipt['actual_traces']>=3
    assert state.run_receipt['representative_traces']
    runbook=isolated/'out'/'DEMO_SCRIPT.md'
    assert runbook.read_bytes()==Path('DEMO_SCRIPT.md').read_bytes()
