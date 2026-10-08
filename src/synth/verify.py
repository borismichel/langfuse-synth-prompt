"""Read exact current-run evidence via core; unrelated project data cannot pass."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import time
from langfuse_synth_core.target import TargetProfile
from .config import Config
from .state import RunState
from .scores import read_score_value, SCORE_CONTRACT

@dataclass
class Check:
    name: str
    ok: bool
    detail: str

@dataclass
class VerifyReport:
    checks: list[Check] = field(default_factory=list)
    def add(self, name: str, ok: bool, detail: str):
        self.checks.append(Check(name, bool(ok), detail))
    @property
    def ok(self) -> bool:
        return bool(self.checks) and all(c.ok for c in self.checks)


def verify_trace(reader, expected: dict) -> Check:
    tid = expected['id']
    actual = reader.trace(tid)
    if not actual:
        return Check(f'trace:{tid}', False, 'Current-run trace not visible yet')
    problems = []
    observations = {o.id:o for o in actual.observations}
    for e in expected['observations']:
        o = observations.get(e['id'])
        if not o:
            problems.append(f"missing observation {e['id']}"); continue
        for attr in ('parent_id','name','prompt_name','prompt_version','session_id'):
            if getattr(o, attr) != e.get(attr): problems.append(f"{e['id']} wrong {attr}")
        if (o.type or '').upper() != e['type']: problems.append(f"{e['id']} wrong type")
        if o.input != e['input'] or o.output != e['output']: problems.append(f"{e['id']} payload differs")
        start = datetime.fromisoformat(e['start_time'])
        if o.start_time is None or abs((o.start_time-start).total_seconds()) > .001:
            problems.append(f"{e['id']} wrong timestamp")
        if e.get('end_time'):
            end = datetime.fromisoformat(e['end_time'])
            if o.end_time is None or abs((o.end_time-end).total_seconds()) > .001:
                problems.append(f"{e['id']} wrong end timestamp")
        if (o.metadata or {}).get('evaluation_subject') != e.get('evaluation_subject'):
            problems.append(f"{e['id']} wrong evaluator subject")
        if 'rubric_revisions' in e and (o.metadata or {}).get('rubric_revisions') != e['rubric_revisions']:
            problems.append(f"{e['id']} wrong rubric revisions")
        for key, value in e.get('operation_metadata', {}).items():
            if (o.metadata or {}).get(key) != value:
                problems.append(f"{e['id']} wrong operation metadata {key}")
    if len(actual.observations) != len(expected['observations']):
        problems.append('observation count differs (possible duplicate import)')
    scores = {s.id:s for s in actual.scores}
    for e in expected['scores']:
        s = scores.get(e['id'])
        if not s:
            problems.append(f"missing score {e['id']}"); continue
        if s.name != e['name'] or s.observation_id != e['observationId'] or read_score_value(s) != e['value'] or s.data_type != e['dataType']:
            problems.append(f"score {e['id']} name/subject/type/value differs")
    if len(actual.scores) != len(expected['scores']):
        problems.append('score count differs (unexpected judge or duplicate result)')
    return Check(f'trace:{tid}', not problems, '; '.join(problems[:8]) if problems else 'Exact observations, prompt versions, payloads, session, timestamps and score subjects match')


def run_verify(cfg: Config, *, log=print, reader=None, clock=time.monotonic, sleep=time.sleep) -> VerifyReport:
    report = VerifyReport()
    if not RunState.exists():
        report.add('receipt',False,'No seed receipt in this state directory'); log('✗ No seed receipt in this state directory'); return report
    state = RunState.load()
    valid = (not state.dry_run and state.import_status=='imported' and state.base_url==cfg.target.base_url
             and state.seed==cfg.generation.seed and state.target_traces==cfg.generation.target_traces
             and bool(state.project_id) and bool(state.run_receipt.get('representative_traces')))
    report.add('receipt',valid,'Current target and generation inputs match an imported run' if valid else 'Receipt is missing, dry-run, incomplete, or belongs to another target/config')
    if not valid:
        log("✗ Seed receipt is missing, dry-run, incomplete, or for another target/config")
        return report
    categorical_history = state.run_receipt.get('score_contract') == SCORE_CONTRACT
    report.add('score-contract', categorical_history,
               'Current categorical factual score contract' if categorical_history else
               'Categorical factual history requires a fresh target or authorised reset; earlier numeric pilot data is unchanged.')
    if cfg.generation.as_of_date:
        report.add('as_of_date',state.run_receipt['run_date'][:10]==cfg.generation.as_of_date.isoformat(),'Run anchor matches requested date')
    if reader is None:
        reader = TargetProfile.detect(cfg.target.base_url).resolved().reader()
    pending = {e['id']:e for e in state.run_receipt['representative_traces']}
    checks = {}
    deadline = clock() + cfg.verification.timeout_seconds
    while pending:
        for tid,e in list(pending.items()):
            try: check=verify_trace(reader,e)
            except Exception as exc: check=Check(f'trace:{tid}',False,f'Read failed ({type(exc).__name__}); inspect target access/ingestion')
            checks[tid]=check
            if check.ok: del pending[tid]
        if not pending or clock() >= deadline: break
        sleep(min(cfg.verification.poll_seconds,max(0,deadline-clock())))
    report.checks.extend(checks.values())
    # Asset verifier independently reads prompt labels/versions, dataset items and rules.
    from .assets import verify_assets
    for name, ok, detail in verify_assets(cfg, state.provisioning):
        report.add(name,ok,detail)
    for check in report.checks:
        log(f"{'✓' if check.ok else '✗'} {check.name}: {check.detail}")
    return report
