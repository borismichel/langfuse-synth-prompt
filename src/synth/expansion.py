"""One-shot, additive history expansion of a verified imported project.

The imported spool is immutable. A distinct deterministic seed generates only the
missing history volume, with complete sessions and no repeated experiments. Core
owns finalisation and transport; a combined spool is evidence, never an import.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path

from langfuse_synth_core.seed import otlp
from langfuse_synth_core.seed.ingest import Ingestor, assert_demo_project

from .assets import AssetAPI, verify_assets
from .materialize import build_events
from .receipt import attributes, make_receipt
from .scores import SCORE_CONTRACT
from .state import RunState


def _trace(event):
    return event['traceId'] if otlp.is_span(event) else event['body']['traceId']


def _identity(event):
    return ('observation', event['spanId']) if otlp.is_span(event) else ('score', event['body']['id'])


def _sessions(events):
    return {attributes(e)[otlp.SESSION_ID] for e in events
            if otlp.is_span(e) and attributes(e).get(otlp.SESSION_ID)}


def prepare_expansion(cfg, state: RunState, previous_spool: Path) -> tuple[list[dict], list[dict], dict]:
    """Pure local preflight: validate the receipt and derive a disjoint supplement."""
    receipt = state.run_receipt
    try:
        run_date = datetime.fromisoformat(receipt.get('run_date', ''))
        valid_date = run_date.tzinfo is not None and (
            not cfg.generation.as_of_date or run_date.date() == cfg.generation.as_of_date)
    except (ValueError, TypeError):
        valid_date = False
    valid = (not state.dry_run and state.import_status == 'imported' and not state.expansion
             and state.base_url.rstrip('/') == cfg.target.base_url.rstrip('/')
             and bool(state.project_id) and state.provisioning.get('project_id') == state.project_id
             and state.seed == cfg.generation.seed == receipt.get('seed')
             and 0 < state.target_traces == receipt.get('target_traces') < cfg.generation.target_traces
             and state.spooled_events == receipt.get('spooled_events')
             and receipt.get('schema_version') == 1 and receipt.get('score_contract') == SCORE_CONTRACT
             and bool(receipt.get('representative_traces')) and valid_date)
    if not valid:
        raise RuntimeError('Expansion requires an unexpanded imported receipt matching this project, seed and date, with a larger target volume.')
    raw = previous_spool.read_bytes()
    if hashlib.sha256(raw).hexdigest() != receipt.get('spool_sha256'):
        raise RuntimeError('Previous spool hash does not match the imported receipt.')
    previous = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if len(previous) != state.spooled_events or len({_identity(e) for e in previous}) != len(previous):
        raise RuntimeError('Previous spool has an invalid event count or duplicate identities.')
    experiments = {e['trace_id'] for e in state.provisioning.get('historical_experiments', [])}
    previous_traces = {_trace(e) for e in previous}
    if (len(experiments) != 18 or not experiments <= previous_traces
            or len(previous_traces) != state.target_traces + len(experiments)
            or receipt.get('actual_traces') != len(previous_traces)):
        raise RuntimeError('Previous receipt must include its complete history and eighteen historical experiments.')
    supplement_count = cfg.generation.target_traces - state.target_traces
    supplement_seed = cfg.generation.seed + 1
    supplement = otlp.finalize(build_events(supplement_count, {'seed': supplement_seed}, run_date=run_date))
    ids = {_identity(e) for e in supplement}
    if (len(ids) != len(supplement) or ids & {_identity(e) for e in previous}
            or {_trace(e) for e in supplement} & previous_traces
            or _sessions(supplement) & _sessions(previous)
            or len({_trace(e) for e in supplement}) != supplement_count):
        raise RuntimeError('Supplement must have distinct event, trace and session identities and the exact requested volume.')
    provenance = {'schema_version': 1, 'strategy': 'preserve-existing-plus-independent-history',
                  'original_seed': state.seed, 'supplement_seed': supplement_seed,
                  'original_target_traces': state.target_traces, 'added_history_traces': supplement_count,
                  'target_traces': cfg.generation.target_traces, 'run_date': run_date.isoformat(),
                  'previous_spool_sha256': receipt['spool_sha256'],
                  'previous_spool': str(previous_spool.resolve()), 'project_id': state.project_id}
    return previous, supplement, provenance


def _cursor_inventory(api, path, params) -> list[dict]:
    """Read every modern page; never infer absence from a truncated response."""
    rows, seen = [], set()
    params = params.copy()
    for _ in range(10000):
        result = api.read(path, params.copy())
        if not isinstance(result.get('data'), list) or not isinstance(result.get('meta'), dict):
            raise RuntimeError('Invalid modern observation inventory response.')
        rows.extend(result['data'])
        cursor = result['meta'].get('cursor')
        if result['meta'].get('truncated'):
            raise RuntimeError('Truncated observation inventory cannot authorise expansion.')
        if not cursor:
            return rows
        if cursor in seen:
            raise RuntimeError('Repeated observation cursor; inventory is incomplete.')
        seen.add(cursor)
        params['cursor'] = cursor
    raise RuntimeError('Observation inventory exceeded the page bound.')


def observation_inventory(api) -> list[dict]:
    return _cursor_inventory(api, '/api/public/v2/observations', {
        'limit': 1000, 'fields': 'core,basic', 'fromStartTime': '1970-01-01T00:00:00Z'})


def check_score_collisions(api, supplement, project_id):
    rows = _cursor_inventory(api, '/api/public/v3/scores', {'limit': 100, 'fields': 'subject'})
    if any(row.get('projectId') != project_id or not row.get('id') for row in rows):
        raise RuntimeError('Score inventory contains invalid or foreign-project rows.')
    if {e['body']['id'] for e in supplement if not otlp.is_span(e)} & {r['id'] for r in rows}:
        raise RuntimeError('Supplement collides with existing live score identities.')


def check_live_inventory(rows, previous, supplement, project_id):
    if any(row.get('projectId') != project_id or not row.get('id') or not row.get('traceId') for row in rows):
        raise RuntimeError('Observation inventory contains invalid or foreign-project rows.')
    old_traces = {_trace(e) for e in previous}
    expected = Counter((e['traceId'], e['spanId']) for e in previous if otlp.is_span(e))
    actual = Counter((r['traceId'], r['id']) for r in rows if r['traceId'] in old_traces)
    if actual != expected:
        raise RuntimeError('Existing live observations differ from the imported spool (missing, extra or duplicate observations).')
    if ({_trace(e) for e in supplement} & {r['traceId'] for r in rows}
            or {e['spanId'] for e in supplement if otlp.is_span(e)} & {r['id'] for r in rows}
            or _sessions(supplement) & {r.get('sessionId') for r in rows}):
        raise RuntimeError('Supplement collides with existing live traces, observations or sessions.')


def run_expansion(cfg, *, previous_spool: Path, log=print) -> Path:
    previous_state_path = previous_spool.parent / '.synth_state.json'
    if not previous_state_path.is_file():
        raise RuntimeError('Expansion requires an imported receipt beside the previous spool.')
    state_path = Path(RunState.state_path())
    if state_path.parent.resolve() == previous_spool.parent.resolve() or state_path.exists():
        raise RuntimeError('Expansion requires a new empty state directory; preserve the original imported state.')
    original_state = previous_state_path.read_bytes()
    state = RunState.load(str(previous_state_path))
    previous, supplement, provenance = prepare_expansion(cfg, state, previous_spool)
    # Lock the source, so selecting a different destination cannot replay a supplement.
    guard = previous_spool.parent / '.history-expansion-attempt.json'
    delta = state_path.parent / 'events.ndjson'
    combined = state_path.parent / 'combined-evidence.ndjson'
    backup = state_path.parent / 'pre-expansion-state.json'
    # None of these files may be replaced: an ambiguous attempt is non-resumable.
    if any(p.exists() for p in (guard, delta, combined, backup)):
        raise RuntimeError('Expansion already prepared or attempted; never retry an ambiguous append import.')
    project_id, _ = assert_demo_project(cfg.target.base_url, cfg.target.project_hint)
    if project_id != state.project_id:
        raise RuntimeError('Expansion authenticated project differs from the imported project.')
    api = AssetAPI(cfg.target.base_url)
    failures = [name for name, ok, _ in verify_assets(cfg, state.provisioning, api=api, check_labels=False) if not ok]
    if failures:
        raise RuntimeError('Existing assets failed read-only verification: ' + ', '.join(failures))
    rows = observation_inventory(api)
    check_live_inventory(rows, previous, supplement, project_id)
    check_score_collisions(api, supplement, project_id)
    if previous_state_path.read_bytes() != original_state or hashlib.sha256(previous_spool.read_bytes()).hexdigest() != provenance['previous_spool_sha256']:
        raise RuntimeError('Imported state or spool changed during expansion preflight.')
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation is the one-shot lock, acquired before any local state or live write.
    with guard.open('x') as file:
        json.dump(provenance, file, sort_keys=True)
    with backup.open('xb') as file:
        file.write(original_state)
    state.expansion = deepcopy(provenance)
    state.expansion.update(status='preparing', delta_spool=str(delta.resolve()), combined_evidence=str(combined.resolve()))
    try:
        ingestor = Ingestor.from_env(cfg.target.base_url, spool_path=delta, max_retries=1)
        ingestor.open_spool()
        ingestor.extend(supplement)
        ingestor.close_spool()
        # Preserve the original bytes; only the delta goes through the importer.
        with combined.open('xb') as file:
            file.write(previous_spool.read_bytes())
            if not previous_spool.read_bytes().endswith(b'\n'):
                file.write(b'\n')
            file.write(delta.read_bytes())
        actual_delta = [json.loads(line) for line in delta.read_bytes().splitlines() if line.strip()]
        if actual_delta != supplement:
            raise RuntimeError('Core spool finalisation changed the prepared supplement.')
        receipt = make_receipt(previous + actual_delta, combined, run_date=datetime.fromisoformat(provenance['run_date']),
                               seed=state.seed, target_traces=cfg.generation.target_traces)
        state.expansion['delta_sha256'] = hashlib.sha256(delta.read_bytes()).hexdigest()
        state.expansion['previous_live_observations'] = len(rows)
        state.expansion['added_events'] = len(actual_delta)
        receipt['expansion'] = deepcopy(state.expansion)
        state.target_traces = cfg.generation.target_traces
        state.spooled_events = len(previous) + len(actual_delta)
        state.run_receipt = receipt
        state.import_status = state.expansion['status'] = 'importing'
        state.save()
        log(f'· importing {len(actual_delta)} new events for {provenance["added_history_traces"]} history traces; existing data and assets retained')
        ingestor.import_spool(path=delta, confirm_cleared=False, log=log)
        state.import_status = state.expansion['status'] = 'imported'
        state.run_receipt['expansion'] = deepcopy(state.expansion)
        state.save()
    except Exception:
        state.import_status = state.expansion['status'] = 'failed'
        state.save()
        raise
    log(f'· expanded receipt: {state_path}; combined evidence is never an import input')
    return delta
