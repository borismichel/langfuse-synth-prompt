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


def test_tool_readback_rejects_leaked_evaluator_subject_and_wrong_timing():
    from dataclasses import replace
    e = expected()
    observation = e['observations'][0]
    observation.update(type='TOOL', evaluation_subject=None,
                       end_time='2026-01-01T00:00:01+00:00',
                       operation_metadata={'invocation': 'application'})
    value = actual()
    e['scores'] = []
    value.scores.clear()
    tool = replace(value.observations[0], type='TOOL',
                   end_time=datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
                   metadata={'invocation': 'application'})
    value.observations[0] = tool
    assert verify_trace(reader_for(value), e).ok
    value.observations[0] = replace(tool, metadata={'invocation': 'application', 'evaluation_subject': 'user_input'})
    assert not verify_trace(reader_for(value), e).ok
    value.observations[0] = replace(tool, end_time=None)
    assert not verify_trace(reader_for(value), e).ok
    value.observations[0] = replace(tool, metadata={'invocation': 'model'})
    assert not verify_trace(reader_for(value), e).ok


def test_receipt_keeps_conditional_calculator_evidence_and_synthetic_provenance(tmp_path):
    from langfuse_synth_core.seed.otlp import finalize
    from synth.materialize import build_events
    from synth.receipt import make_receipt
    from synth.reference_tools import FEE_TOOL_NAME
    events = finalize(build_events(24, {"seed": 42}, run_date=datetime(2026, 10, 8, tzinfo=timezone.utc)))
    spool = tmp_path / 'events.ndjson'
    spool.write_text('offline receipt test')
    receipt = make_receipt(events, spool, run_date=datetime(2026, 10, 8, tzinfo=timezone.utc), seed=42, target_traces=24)
    calculations = [o for trace in receipt['representative_traces'] for o in trace['observations']
                    if o['name'] == FEE_TOOL_NAME]
    assert calculations
    for operation in calculations:
        assert operation['type'] == 'TOOL'
        assert operation['input']['withdrawal_count'] == 3
        assert operation['output']['total_fee'] == '1.50'
        assert operation['evaluation_subject'] is None
        assert operation['operation_metadata']['evidence_kind'] == 'authored-synthetic-history'

    for trace in receipt['representative_traces']:
        tool = next((o for o in trace['observations'] if o['name'] == FEE_TOOL_NAME), None)
        if tool is not None:
            generation = next(o for o in trace['observations'] if o['type'] == 'GENERATION')
            assert generation['operation_metadata']['calculation_results'] == [{
                'operation': FEE_TOOL_NAME, 'arguments': tool['input'], 'result': tool['output']}]
