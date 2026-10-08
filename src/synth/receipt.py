"""Bounded scenario evidence selected from core-finalised seed events.

This inspects core's public event representation; it does not construct transport.
Every expected ID/value comes from the actual spool that was imported.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from langfuse_synth_core.seed import otlp


def attributes(event: dict) -> dict:
    return {a['key']: next(iter(a['value'].values())) for a in event.get('attributes', [])}


def _decoded(value):
    if not isinstance(value, str): return value
    try: return json.loads(value)
    except (ValueError, TypeError): return value


def make_receipt(events: list[dict], spool_path: Path, *, run_date: datetime, seed: int, target_traces: int) -> dict:
    spans = [e for e in events if otlp.is_span(e)]
    trace_ids, seen = [], set()
    # One trace per actual prompt/version, plus all other operations in that trace.
    for e in spans:
        a = attributes(e)
        name = a.get(otlp.PROMPT_NAME)
        if not name: continue
        key = (name, int(a.get(otlp.PROMPT_VERSION, 0)))
        if key not in seen:
            seen.add(key)
            if e['traceId'] not in trace_ids: trace_ids.append(e['traceId'])
    if not trace_ids:
        trace_ids = list(dict.fromkeys(e['traceId'] for e in spans))[:3]
    trace_ids = trace_ids[:72]
    traces = []
    for tid in trace_ids:
        observations = []
        for e in spans:
            if e['traceId'] != tid: continue
            a = attributes(e)
            observations.append({
                'id': e['spanId'], 'parent_id': e.get('parentSpanId') or None,
                'name': e['name'], 'type': a.get(otlp.OBS_TYPE, 'span').upper(),
                'start_time': datetime.fromtimestamp(int(e['startTimeUnixNano']) / 1e9, timezone.utc).isoformat(),
                'end_time': datetime.fromtimestamp(int(e['endTimeUnixNano']) / 1e9, timezone.utc).isoformat(),
                'prompt_name': a.get(otlp.PROMPT_NAME),
                'prompt_version': int(a[otlp.PROMPT_VERSION]) if otlp.PROMPT_VERSION in a else None,
                'session_id': a.get(otlp.SESSION_ID),
                'input': _decoded(a.get(otlp.OBS_INPUT)), 'output': _decoded(a.get(otlp.OBS_OUTPUT)),
                'evaluation_subject': _decoded(a.get(otlp.OBS_METADATA_PREFIX + 'evaluation_subject')),
                'operation_metadata': {key: _decoded(a[otlp.OBS_METADATA_PREFIX + key])
                    for key in ('invocation', 'simulated', 'source_id')
                    if otlp.OBS_METADATA_PREFIX + key in a},
            })
        scores = []
        for e in events:
            if e.get('type') != 'score-create' or e['body'].get('traceId') != tid: continue
            b = e['body']
            scores.append({k: b.get(k) for k in ('id','name','value','observationId','dataType')})
        traces.append({'id':tid,'observations':observations,'scores':scores})
    return {'schema_version':1,'run_date':run_date.isoformat(),'seed':seed,'target_traces':target_traces,
            'spool_sha256':hashlib.sha256(spool_path.read_bytes()).hexdigest(),
            'spooled_events':len(events),'representative_traces':traces,
            'actual_traces':len({e['traceId'] for e in spans}),
            'actual_generations':sum(attributes(e).get(otlp.OBS_TYPE,'').lower()=='generation' for e in spans),
            'actual_scores':sum(e.get('type')=='score-create' for e in events)}
