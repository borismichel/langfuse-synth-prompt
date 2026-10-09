"""Scoped replacement of immutable authored history, with no asset writes.

Plan locally; verify complete modern inventories; delete only the recorded trace
IDs; wait for their observations AND scores to disappear; import once. Callbacks
keep official CLI access and core transport at the caller's existing seams.
Deletion is asynchronous (normally within 15 minutes), so polling can resume,
but neither an ambiguous deletion batch nor an import is ever retried here.
"""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import time

from langfuse_synth_core.seed import otlp

from .model_policy import MODEL_POLICY_REVISION, apply_model_policy
from .prompt_references import annotate_prompt_references, ROOT_PROMPT_METADATA
from .operation_names import (normalize_operations, experiment_run_name, normalize_surface_descriptions,
                              LEGACY_EXPERIMENT_DESCRIPTION, EXPERIMENT_DESCRIPTION, LEGACY_SCORE_COMMENT_PREFIX)
from .receipt import attributes, make_receipt
from .scores import SCORE_CONTRACT


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _write(path, value, *, exclusive=False):
    with Path(path).open('x' if exclusive else 'w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def _events(path):
    return [json.loads(line) for line in Path(path).read_bytes().splitlines() if line.strip()]


def _trace(event):
    return event['traceId'] if otlp.is_span(event) else event['body']['traceId']


def _identities(events):
    result = {'trace': set(), 'observation': set(), 'score': set(), 'event': set(), 'session': set()}
    for event in events:
        result['trace'].add(_trace(event))
        if otlp.is_span(event):
            result['observation'].add(event['spanId'])
            session = attributes(event).get(otlp.SESSION_ID)
            if session:
                result['session'].add(session)
        else:
            if event.get('type') != 'score-create':
                raise RuntimeError('Replacement supports only observations and authored scores.')
            result['score'].add(event['body']['id'])
            result['event'].add(event['id'])
    return result


def remap_references(value, mapping):
    """Replace exact ID values, including inside JSON-encoded OTLP attributes.

    Text containing an ID as a substring is left intact. JSON is only re-encoded
    when a nested value changes, preserving all other original payload bytes.
    """
    if isinstance(value, dict):
        return {key: remap_references(item, mapping) for key, item in value.items()}
    if isinstance(value, list):
        return [remap_references(item, mapping) for item in value]
    if not isinstance(value, str):
        return value
    if value in mapping:
        return mapping[value]
    if value[:1] in {'{', '['}:
        try:
            decoded = json.loads(value)
        except ValueError:
            return value
        changed = remap_references(decoded, mapping)
        if changed != decoded:
            return json.dumps(changed, separators=(',', ':'), ensure_ascii=False)
    return value


def transform_history(events, *, revision, project_id):
    """Preserve event order, payloads, outcomes and chronology under fresh IDs."""
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{2,79}', revision):
        raise ValueError('Revision must be a descriptive 3–80 character identifier.')
    identities = _identities(events)
    maps = {}
    for kind, values in identities.items():
        maps[kind] = {}
        for old in sorted(values):
            digest = _sha(f'prompt-history-replacement:{project_id}:{revision}:{kind}:{old}'.encode())
            maps[kind][old] = ('conversation-' + digest[:24]) if kind == 'session' else digest[:16 if kind == 'observation' else 32]
    # Core identifies a trace root by its deterministic ID, not parent absence.
    # Keep that relationship under the new trace namespace so both enrichment
    # helpers and core finalization still recognize every root after remapping.
    for event in events:
        if otlp.is_trace_root(event):
            maps['observation'][event['spanId']] = otlp.trace_root_span_id(maps['trace'][event['traceId']])
    flat = {}
    for mapping in maps.values():
        for old, new in mapping.items():
            if old in flat and flat[old] != new:
                raise RuntimeError('Source IDs overlap between identity types.')
            flat[old] = new
    if len(set(flat.values())) != len(flat) or set(flat) & set(flat.values()):
        raise RuntimeError('Replacement IDs collide with source identities.')
    rewritten = remap_references(events, flat)
    rewritten = normalize_operations(annotate_prompt_references(apply_model_policy(rewritten)))
    rewritten, _ = _normalize_user_identifiers(rewritten)
    if {key: len(value) for key, value in _identities(rewritten).items()} != {key: len(value) for key, value in identities.items()}:
        raise RuntimeError('Transformation changed source identity cardinality.')
    return rewritten, maps


def prepare_replacement(source_spool: Path, destination: Path, *, expected_project_id: str,
                        expected_run_date: str, revision: str, expected_counts: dict | None = None) -> Path:
    """Create reviewable files without contacting or mutating a live project."""
    source_spool, destination = Path(source_spool).resolve(), Path(destination).resolve()
    source_state = source_spool.parent / '.synth_state.json'
    raw_state, raw_spool = source_state.read_bytes(), source_spool.read_bytes()
    state = json.loads(raw_state)
    receipt = state.get('run_receipt', {})
    run_date = datetime.fromisoformat(receipt.get('run_date', ''))
    if (state.get('import_status') != 'imported' or state.get('dry_run') is not False
            or state.get('project_id') != expected_project_id
            or state.get('provisioning', {}).get('project_id') != expected_project_id
            or receipt.get('run_date') != expected_run_date or run_date.tzinfo is None
            or receipt.get('schema_version') != 1 or receipt.get('score_contract') != SCORE_CONTRACT
            or receipt.get('seed') != state.get('seed') or receipt.get('target_traces') != state.get('target_traces')
            or receipt.get('spool_sha256') != _sha(raw_spool)):
        raise RuntimeError('Source must be the complete imported receipt for the expected project, date and spool hash.')
    events = _events(source_spool)
    identities = _identities(events)
    counts = {key: len(identities[key]) for key in ('trace', 'observation', 'score')}
    if (len(events) != receipt.get('spooled_events') or len(events) != state.get('spooled_events')
            or counts['observation'] + counts['score'] != len(events)
            or len(identities['event']) != counts['score']
            or counts['score'] != receipt.get('actual_scores')
            or counts['trace'] != receipt.get('actual_traces')
            or (expected_counts is not None and counts != expected_counts)):
        raise RuntimeError('Source cardinalities differ from the imported receipt or requested exact scope.')
    experiments = state['provisioning'].get('historical_experiments', [])
    if (len(experiments) != 18 or not {e['trace_id'] for e in experiments} <= identities['trace']
            or counts['trace'] != state['target_traces'] + 18):
        raise RuntimeError('Source must cover all authored history and eighteen recorded experiments.')
    observation_traces = {e['spanId']: e['traceId'] for e in events if otlp.is_span(e)}
    for event in events:
        if not otlp.is_span(event):
            if observation_traces.get(event['body'].get('observationId')) != event['body']['traceId']:
                raise RuntimeError('Source score has no authored observation target.')
            continue
        a = attributes(event)
        tags = a.get('langfuse.trace.tags', {}).get('values', [])
        legacy_tags = {'stringValue': 'authored-history'} in tags and {'stringValue': 'fictional'} in tags
        replay_provenance = (a.get(otlp.OBS_METADATA_PREFIX + 'evidence_kind') == 'authored-synthetic-history'
                             and a.get(otlp.OBS_METADATA_PREFIX + 'evaluation_mode') == 'replay')
        if not legacy_tags and not replay_provenance:
            raise RuntimeError('Source contains observations outside recorded authored history.')
        if event.get('parentSpanId') and observation_traces.get(event['parentSpanId']) != event['traceId']:
            raise RuntimeError('Source has an external or missing parent observation.')
    if destination == source_spool.parent or destination.exists():
        raise RuntimeError('Replacement requires a new destination; preserve original imported files.')
    guard = source_spool.parent / '.history-replacement-attempt.json'
    if guard.exists():
        raise RuntimeError('This source already has a replacement attempt; do not create another plan.')
    rewritten, maps = transform_history(events, revision=revision, project_id=expected_project_id)
    output = b''.join((json.dumps(event, separators=(',', ':'), ensure_ascii=False) + '\n').encode() for event in rewritten)
    # Core finalization must be identity-preserving before any destructive action.
    if otlp.finalize(deepcopy(rewritten)) != rewritten:
        raise RuntimeError('Replacement is not a stable core-finalised spool.')
    destination.mkdir(parents=True)
    (destination / 'events.ndjson').write_bytes(output)
    (destination / 'pre-replacement-state.json').write_bytes(raw_state)
    _write(destination / 'id-maps.json', maps, exclusive=True)
    plan = {'schema_version': 1, 'revision': revision, 'model_policy_revision': MODEL_POLICY_REVISION,
            'project_id': expected_project_id, 'base_url': state['base_url'], 'run_date': expected_run_date,
            'source_spool': str(source_spool), 'source_state': str(source_state),
            'source_spool_sha256': _sha(raw_spool), 'source_state_sha256': _sha(raw_state),
            'replacement_spool': str(destination / 'events.ndjson'), 'replacement_spool_sha256': _sha(output),
            'maps_sha256': _sha((destination / 'id-maps.json').read_bytes()),
            'guard': str(guard), 'counts': counts, 'delete_trace_ids': sorted(identities['trace']),
            'asset_policy': 'Preserve prompts, labels, datasets, experiment IDs and connections; migration writes tracing data only.'}
    _write(destination / 'replacement-plan.json', plan, exclusive=True)
    return destination / 'replacement-plan.json'


def _load_plan(plan_path):
    plan_path = Path(plan_path)
    plan = json.loads(plan_path.read_text())
    amendment = plan.get('presentation_amendment')
    if not amendment and (plan_path.parent / 'presentation-amendment').exists():
        raise RuntimeError('An uncommitted presentation amendment exists; reconcile its local transaction.')
    if amendment:
        audit_path = Path(amendment['audit'])
        if _sha(audit_path.read_bytes()) != amendment['audit_sha256']:
            raise RuntimeError('Presentation amendment audit changed.')
        audit = json.loads(audit_path.read_text())
        committed = audit_path.parent / 'committed.json'
        if (not committed.exists() or json.loads(committed.read_text()) != {
                'plan_sha256': _sha(plan_path.read_bytes()), 'audit_sha256': amendment['audit_sha256']}):
            raise RuntimeError('Presentation amendment is not committed; reconcile its local transaction.')
        old_plan_raw = (audit_path.parent / 'replacement-plan.before.json').read_bytes()
        if (_sha(old_plan_raw) != audit['previous_plan_sha256']
                or _sha((audit_path.parent / 'events.before.ndjson').read_bytes()) != audit['previous_spool_sha256']):
            raise RuntimeError('Presentation amendment backup changed.')
        old_plan = json.loads(old_plan_raw)
        old_plan['replacement_spool_sha256'] = audit['replacement_spool_sha256']
        old_plan['presentation_amendment'] = amendment
        if old_plan != plan:
            raise RuntimeError('Presentation amendment changed the deletion scope or plan outside its fixed scope.')
    for file_key, hash_key in [('source_spool', 'source_spool_sha256'), ('source_state', 'source_state_sha256'),
                               ('replacement_spool', 'replacement_spool_sha256')]:
        if _sha(Path(plan[file_key]).read_bytes()) != plan[hash_key]:
            raise RuntimeError(f'Replacement preflight hash changed: {file_key}.')
    maps_path = plan_path.parent / 'id-maps.json'
    if _sha(maps_path.read_bytes()) != plan['maps_sha256']:
        raise RuntimeError('Replacement ID map changed.')
    source, replacement = _events(plan['source_spool']), _events(plan['replacement_spool'])
    if plan['delete_trace_ids'] != sorted(_identities(source)['trace']):
        raise RuntimeError('Deletion scope differs from the exact source spool.')
    if json.loads(Path(plan['source_state']).read_text())['project_id'] != plan['project_id']:
        raise RuntimeError('Plan project differs from imported state.')
    roots = [event for event in replacement if otlp.is_trace_root(event)]
    if len(roots) != plan['counts']['trace']:
        raise RuntimeError('Replacement roots must preserve core root identity; prepare a current plan.')
    return plan, source, replacement, json.loads(maps_path.read_text())


def validate_inventory(observations, scores, source, replacement, project_id):
    """Require exact source coverage and no replacement collision, across all pages."""
    if any(row.get('projectId') != project_id or not row.get('id') or not row.get('traceId') for row in observations):
        raise RuntimeError('Invalid or foreign-project observation inventory.')
    if any(row.get('projectId') != project_id or not row.get('id') for row in scores):
        raise RuntimeError('Invalid or foreign-project score inventory.')
    old, new = _identities(source), _identities(replacement)
    expected_obs = Counter((e['traceId'], e['spanId']) for e in source if otlp.is_span(e))
    actual_obs = Counter((r['traceId'], r['id']) for r in observations if r['traceId'] in old['trace'])
    expected_scores = Counter((e['body']['traceId'], e['body']['observationId'], e['body']['id']) for e in source if not otlp.is_span(e))
    actual_scores = Counter((r.get('traceId'), r.get('observationId'), r['id']) for r in scores
                            if r.get('traceId') in old['trace'] or r['id'] in old['score'])
    if expected_obs != actual_obs or expected_scores != actual_scores:
        raise RuntimeError('Live source observations/scores are missing, additional, duplicated or differently bound.')
    if (new['trace'] & {r['traceId'] for r in observations} or new['observation'] & {r['id'] for r in observations}
            or new['session'] & {r.get('sessionId') for r in observations} or new['score'] & {r['id'] for r in scores}
            or new['trace'] & {r.get('traceId') for r in scores}
            or new['observation'] & {r.get('observationId') for r in scores}):
        raise RuntimeError('Replacement identities already exist in the target; import would duplicate data.')
    return {'observation_ids': sorted(r['id'] for r in observations if r['traceId'] not in old['trace']),
            'trace_ids': sorted({r['traceId'] for r in observations} - old['trace']),
            'score_ids': sorted(r['id'] for r in scores if r['id'] not in old['score'])}


def delete_replacement(plan_path: Path, *, authenticated_project_id: str, inventory,
                       delete_batch, policy_receipt: dict, batch_size: int = 40, log=print):
    """Execute each DELETE batch once. Callbacks must use fully paginated reads.

    policy_receipt is a separately verified asset-policy receipt with project_id,
    model_policy_revision, verified=True and refreshed provisioning anchors.
    """
    if not 1 <= batch_size <= 50:
        raise ValueError('Trace deletion batches must be at most 50 IDs.')
    plan, source, replacement, _ = _load_plan(plan_path)
    root = Path(plan_path).parent
    if (authenticated_project_id != plan['project_id'] or policy_receipt.get('project_id') != plan['project_id']
            or policy_receipt.get('model_policy_revision') != plan['model_policy_revision']
            or policy_receipt.get('verified') is not True
            or policy_receipt.get('provisioning', {}).get('project_id') != plan['project_id']):
        raise RuntimeError('Authenticated project and independently verified model-policy receipt are required.')
    # Asset updates may change models/evaluator anchors; prompt and dataset bindings cannot move.
    original = json.loads(Path(plan['source_state']).read_text())['provisioning']
    for key in ('prompts', 'datasets', 'historical_experiments'):
        expected = deepcopy(original.get(key))
        actual = deepcopy(policy_receipt['provisioning'].get(key))
        if key == 'historical_experiments':
            # This one human-facing field may reflect the same canonical rename.
            # All IDs, dataset/version bindings and other anchors remain exact.
            for item in expected or []:
                item['run_name'] = experiment_run_name(item['prompt_id'], item['version'])
            for item in actual or []:
                canonical = experiment_run_name(item['prompt_id'], item['version'])
                original_name = next((row['run_name'] for row in original[key]
                                      if row['trace_id'] == item['trace_id']), None)
                if item['run_name'] not in (canonical, original_name):
                    raise RuntimeError('Policy receipt changed experiment name outside canonical normalization.')
                item['run_name'] = canonical
        if expected != actual:
            raise RuntimeError(f'Policy receipt changed protected {key} anchors.')
    if Path(plan['guard']).exists() or (root / 'replacement-status.json').exists():
        raise RuntimeError('Deletion already attempted. Never retry an ambiguous deletion batch.')
    observations, scores = inventory()
    preserved = validate_inventory(observations, scores, source, replacement, plan['project_id'])
    _load_plan(plan_path)
    plan_hash = _sha(Path(plan_path).read_bytes())
    _write(plan['guard'], {'plan_sha256': plan_hash, 'plan': str(Path(plan_path).resolve())}, exclusive=True)
    _write(root / 'policy-receipt.json', policy_receipt, exclusive=True)
    status = {'phase': 'deleting', 'plan_sha256': plan_hash, 'policy_sha256': _sha((root / 'policy-receipt.json').read_bytes()),
              'preserved': preserved, 'submitted_trace_ids': [], 'current_batch': []}
    _write(root / 'replacement-status.json', status, exclusive=True)
    try:
        for offset in range(0, len(plan['delete_trace_ids']), batch_size):
            batch = plan['delete_trace_ids'][offset:offset + batch_size]
            status['current_batch'] = batch
            _write(root / 'replacement-status.json', status)
            delete_batch(batch)
            status['submitted_trace_ids'].extend(batch)
            status['current_batch'] = []
            _write(root / 'replacement-status.json', status)
            log(f'· requested deletion of {len(status["submitted_trace_ids"])} / {len(plan["delete_trace_ids"])} authored traces')
        status['phase'] = 'awaiting_deletion'
        _write(root / 'replacement-status.json', status)
    except BaseException:
        status['phase'] = 'delete_failed_requires_reconciliation'
        _write(root / 'replacement-status.json', status)
        raise
    return status


def _import_replacement(plan_path: Path, *, authenticated_project_id: str, inventory, import_spool,
                       timeout_seconds=960, poll_seconds=30, log=print):
    """Poll read-only, then call core's non-resumable importer exactly once.

    Safe to repeat only if a prior call timed out while awaiting deletion. Once
    importing starts, failure/unknown outcome requires manual reconciliation.
    """
    if timeout_seconds < 0 or not 0 < poll_seconds <= 60:
        raise ValueError('Polling needs a non-negative timeout and intervals of at most 60 seconds.')
    plan, source, replacement, maps = _load_plan(plan_path)
    root = Path(plan_path).parent
    status = json.loads((root / 'replacement-status.json').read_text())
    guard = json.loads(Path(plan['guard']).read_text())
    plan_hash = _sha(Path(plan_path).read_bytes())
    if (authenticated_project_id != plan['project_id'] or status['phase'] != 'awaiting_deletion'
            or status['plan_sha256'] != plan_hash or guard['plan_sha256'] != plan_hash
            or status['submitted_trace_ids'] != plan['delete_trace_ids'] or status['current_batch']):
        raise RuntimeError('Import requires completed deletion requests for this exact unchanged plan and project.')
    old = _identities(source)
    deadline = time.monotonic() + timeout_seconds
    while True:
        observations, scores = inventory()
        if any(r.get('projectId') != plan['project_id'] or not r.get('id') or not r.get('traceId') for r in observations):
            raise RuntimeError('Invalid observation inventory while waiting for deletion.')
        if any(r.get('projectId') != plan['project_id'] or not r.get('id') for r in scores):
            raise RuntimeError('Invalid score inventory while waiting for deletion.')
        preserved = status['preserved']
        if (not set(preserved['observation_ids']) <= {r['id'] for r in observations}
                or not set(preserved['trace_ids']) <= {r['traceId'] for r in observations}
                or not set(preserved['score_ids']) <= {r['id'] for r in scores}):
            raise RuntimeError('Unrelated live evidence disappeared; stop for reconciliation.')
        old_obs = sum(r['traceId'] in old['trace'] or r['id'] in old['observation'] for r in observations)
        old_scores = sum(r.get('traceId') in old['trace'] or r['id'] in old['score'] for r in scores)
        if not old_obs and not old_scores:
            validate_inventory(observations, scores, [], replacement, plan['project_id'])
            break
        log(f'· awaiting deletion: {old_obs} old observations and {old_scores} old scores remain')
        if time.monotonic() >= deadline:
            raise TimeoutError('Deletion still pending; rerun only import_replacement to continue read-only polling.')
        time.sleep(min(poll_seconds, max(0, deadline - time.monotonic())))
    _load_plan(plan_path)
    if _sha((root / 'policy-receipt.json').read_bytes()) != status['policy_sha256']:
        raise RuntimeError('Verified policy receipt changed after deletion.')
    policy = json.loads((root / 'policy-receipt.json').read_text())
    state = json.loads(Path(plan['source_state']).read_text())
    state['provisioning'] = deepcopy(policy['provisioning'])
    if 'evaluator_rules' in policy:
        state['evaluator_rules'] = deepcopy(policy['evaluator_rules'])
    flat = {old: new for mapping in maps.values() for old, new in mapping.items()}
    state['provisioning']['historical_experiments'] = remap_references(state['provisioning']['historical_experiments'], flat)
    for item in state['provisioning']['historical_experiments']:
        item['run_name'] = experiment_run_name(item['prompt_id'], item['version'])
    state['run_receipt'] = make_receipt(replacement, Path(plan['replacement_spool']),
                                       run_date=datetime.fromisoformat(plan['run_date']), seed=state['seed'], target_traces=state['target_traces'])
    state['run_receipt']['replacement'] = {'revision': plan['revision'], 'source_spool_sha256': plan['source_spool_sha256'],
                                         'model_policy_revision': plan['model_policy_revision'], 'plan_sha256': plan_hash,
                                         'preserved_live_trace_ids': status['preserved']['trace_ids']}
    # The original expansion remains provenance, not a reusable seed/import marker.
    state['spooled_events'] = len(replacement)
    state['import_status'] = 'importing'
    _write(root / '.synth_state.json', state, exclusive=True)
    _write(root / '.replacement-import-attempt.json', {'plan_sha256': plan_hash}, exclusive=True)
    status['phase'] = 'importing'
    _write(root / 'replacement-status.json', status)
    try:
        import_spool(Path(plan['replacement_spool']))
    except BaseException:
        status['phase'] = state['import_status'] = 'failed_requires_reconciliation'
        _write(root / 'replacement-status.json', status)
        _write(root / '.synth_state.json', state)
        raise
    status['phase'] = state['import_status'] = 'imported'
    _write(root / 'replacement-status.json', status)
    _write(root / '.synth_state.json', state)
    return root / '.synth_state.json'


def _normalize_user_identifiers(events):
    """Rename only legacy user attributes, preserving stable user grouping."""
    users = {attributes(event).get(otlp.USER_ID) for event in events if otlp.is_span(event)} - {None}
    mapping = {old: 'customer-' + old[len('fictional-user-'):] for old in sorted(users)
               if old.startswith('fictional-user-')}
    if len(set(mapping.values())) != len(mapping) or set(mapping.values()) & users:
        raise RuntimeError('Legacy user normalization would merge distinct users.')
    result = deepcopy(events)
    for event in result:
        if otlp.is_span(event):
            for item in event['attributes']:
                if item['key'] == otlp.USER_ID:
                    old = item['value'].get('stringValue')
                    if old in mapping:
                        item['value']['stringValue'] = mapping[old]
    return result, mapping


@contextmanager
def _transition_lock(root):
    """Serialize local amendment/import transitions; a process crash fails closed."""
    lock = Path(root) / '.replacement-transition.lock'
    try:
        with lock.open('x') as stream:
            stream.write('Exclusive replacement state transition in progress.\n')
    except FileExistsError:
        raise RuntimeError('Another replacement transition is active or was interrupted; reconcile its lock.') from None
    try:
        yield
    finally:
        lock.unlink()


def _atomic_bytes(path, raw):
    path = Path(path)
    temporary = path.with_name(path.name + '.amending.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def amend_preimport_presentation(plan_path: Path, *, expected_project_id: str,
                                expected_plan_sha256: str, expected_replacement_sha256: str) -> Path:
    """Apply the explicitly scoped presentation corrections before import.

    Only user prefixes, root prompt fields and exact legacy descriptions change.
    No deletion is sent and no arbitrary replacement contents are accepted. Old
    files are backed up; an interrupted transaction cannot pass import guards.
    """
    plan_path = Path(plan_path).resolve()
    root = plan_path.parent
    with _transition_lock(root):
        plan, _, before, _ = _load_plan(plan_path)
        status_path = root / 'replacement-status.json'
        guard_path = Path(plan['guard'])
        raw_plan, raw_spool = plan_path.read_bytes(), Path(plan['replacement_spool']).read_bytes()
        raw_status, raw_guard = status_path.read_bytes(), guard_path.read_bytes()
        status, guard = json.loads(raw_status), json.loads(raw_guard)
        markers = (root / '.synth_state.json', root / '.replacement-import-attempt.json',
                   Path(plan['replacement_spool'] + '.imported'))
        if (plan['project_id'] != expected_project_id or _sha(raw_plan) != expected_plan_sha256
                or _sha(raw_spool) != expected_replacement_sha256
                or status['phase'] != 'awaiting_deletion' or any(path.exists() for path in markers)
                or status['plan_sha256'] != expected_plan_sha256 or guard['plan_sha256'] != expected_plan_sha256
                or guard['plan'] != str(plan_path)
                or status['submitted_trace_ids'] != plan['delete_trace_ids'] or status['current_batch']):
            raise RuntimeError('Amendment requires this exact guarded, fully submitted plan before any import attempt.')
        if _sha((root / 'policy-receipt.json').read_bytes()) != status['policy_sha256']:
            raise RuntimeError('Verified policy receipt changed before amendment.')
        changed, users = _normalize_user_identifiers(before)
        changed = normalize_surface_descriptions(annotate_prompt_references(changed))
        experiment_descriptions = sum(attributes(event).get("langfuse.experiment.description") == LEGACY_EXPERIMENT_DESCRIPTION
                                      for event in before if otlp.is_span(event))
        score_comments = sum(event.get("type") == "score-create"
                             and event["body"].get("comment", "").startswith(LEGACY_SCORE_COMMENT_PREFIX) for event in before)
        root_fields = sum(sum(item['key'] in ROOT_PROMPT_METADATA for item in event['attributes'])
                          for event in before if otlp.is_trace_root(event))
        if not users and not root_fields and not experiment_descriptions and not score_comments:
            raise RuntimeError('There are no supported legacy presentation fields to amend.')
        # Changed lines are already canonical kit JSON. Keep every unchanged byte
        # and line ending, and prove no unapproved structure changed.
        lines = raw_spool.splitlines(keepends=True)
        if len(lines) != len(before):
            raise RuntimeError('Amendment requires one canonical event per spool line.')
        output = []
        user_attributes = 0
        for line, original, amended in zip(lines, before, changed):
            if original == amended:
                output.append(line)
                continue
            canonical = lambda event: json.dumps(event, separators=(',', ':'), ensure_ascii=False).encode()
            if line.rstrip(b'\r\n') != canonical(original):
                raise RuntimeError('Changed spool lines are not canonical; refuse unrelated byte changes.')
            if otlp.is_span(original):
                user_attributes += attributes(original).get(otlp.USER_ID) in users
                allowed = deepcopy(original)
                for item in allowed['attributes']:
                    if item['key'] == otlp.USER_ID and item['value'].get('stringValue') in users:
                        item['value']['stringValue'] = users[item['value']['stringValue']]
                    if (item['key'] == 'langfuse.experiment.description'
                            and item['value'].get('stringValue') == LEGACY_EXPERIMENT_DESCRIPTION):
                        item['value']['stringValue'] = EXPERIMENT_DESCRIPTION
                if otlp.is_trace_root(allowed):
                    allowed['attributes'] = [item for item in allowed['attributes'] if item['key'] not in ROOT_PROMPT_METADATA]
                if allowed != amended:
                    raise RuntimeError('Amendment changed fields outside its fixed presentation scope.')
            elif original.get('type') == 'score-create':
                allowed = deepcopy(original)
                comment = allowed['body'].get('comment', '')
                if comment.startswith(LEGACY_SCORE_COMMENT_PREFIX):
                    allowed['body']['comment'] = comment[len(LEGACY_SCORE_COMMENT_PREFIX):]
                if allowed != amended:
                    raise RuntimeError('Amendment changed score fields beyond the exact legacy comment prefix.')
            else:
                raise RuntimeError('Amendment cannot alter this event type.')
            ending = line[len(line.rstrip(b'\r\n')):]
            output.append(canonical(amended) + ending)
        new_spool = b''.join(output)
        if otlp.finalize(changed) != changed or _identities(before) != _identities(changed):
            raise RuntimeError('Amendment changed core finalization or tracing identities.')
        audit_dir = root / 'presentation-amendment'
        audit_dir.mkdir()  # Exclusive one-shot amendment, including after interruption.
        for name, raw in [('replacement-plan.before.json', raw_plan), ('events.before.ndjson', raw_spool),
                          ('replacement-status.before.json', raw_status), ('source-guard.before.json', raw_guard)]:
            (audit_dir / name).write_bytes(raw)
        audit = {'schema_version': 1, 'scope': ['legacy-user-attribute-prefix', 'remove-redundant-root-prompt-metadata',
                       'exact-legacy-experiment-description', 'exact-legacy-score-comment-prefix'],
                 'project_id': plan['project_id'], 'previous_plan_sha256': expected_plan_sha256,
                 'previous_spool_sha256': expected_replacement_sha256, 'replacement_spool_sha256': _sha(new_spool),
                 'user_id_map': users, 'changed_user_attributes': user_attributes,
                 'removed_root_prompt_fields': root_fields, 'experiment_descriptions': experiment_descriptions,
                 'score_comment_prefixes': score_comments, 'source_spool_sha256': plan['source_spool_sha256'],
                 'source_state_sha256': plan['source_state_sha256'], 'maps_sha256': plan['maps_sha256']}
        _write(audit_dir / 'amendment.json', audit, exclusive=True)
        audit_hash = _sha((audit_dir / 'amendment.json').read_bytes())
        new_plan = deepcopy(plan)
        new_plan['replacement_spool_sha256'] = _sha(new_spool)
        new_plan['presentation_amendment'] = {'audit': str(audit_dir / 'amendment.json'), 'audit_sha256': audit_hash}
        new_plan_raw = _json_bytes(new_plan)
        new_hash = _sha(new_plan_raw)
        # Fail closed across multiple atomic file replacements. Import accepts only
        # awaiting_deletion + equal hashes, committed as the final state change.
        status['phase'] = 'presentation_amendment_in_progress'
        _atomic_bytes(status_path, _json_bytes(status))
        _atomic_bytes(Path(plan['replacement_spool']), new_spool)
        _atomic_bytes(plan_path, new_plan_raw)
        guard['plan_sha256'] = new_hash
        guard['presentation_amendment_sha256'] = audit_hash
        _atomic_bytes(guard_path, _json_bytes(guard))
        status['plan_sha256'] = new_hash
        status['presentation_amendment_sha256'] = audit_hash
        status['phase'] = 'awaiting_deletion'
        _atomic_bytes(status_path, _json_bytes(status))
        _write(audit_dir / 'committed.json', {'plan_sha256': new_hash, 'audit_sha256': audit_hash}, exclusive=True)
        return audit_dir / 'amendment.json'


def import_replacement(plan_path: Path, *, authenticated_project_id: str, inventory, import_spool,
                       timeout_seconds=960, poll_seconds=30, log=print):
    """Serialize polling/import with any authorised pre-import local amendment."""
    with _transition_lock(Path(plan_path).parent):
        return _import_replacement(plan_path, authenticated_project_id=authenticated_project_id,
                                   inventory=inventory, import_spool=import_spool,
                                   timeout_seconds=timeout_seconds, poll_seconds=poll_seconds, log=log)
