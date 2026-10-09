"""Production operation names are shared by authored replay and the live app."""
from copy import deepcopy
from datetime import datetime, timezone

from langfuse_synth_core.seed import otlp

from synth.materialize import build_events, build_historical_experiment_events
from synth.operation_names import ROOT_NAME_BY_PROMPT, SERVICE_FLOW_NAME, experiment_run_name, normalize_operations
from synth.receipt import attributes

DATE = datetime(2026, 10, 9, 12, tzinfo=timezone.utc)


def test_new_history_uses_operational_names_and_hidden_replay_provenance():
    events = otlp.finalize(build_events(48, {'seed': 42}, run_date=DATE))
    seen = set()
    for event in events:
        if not otlp.is_span(event):
            assert event['body']['environment'] == 'production'
            continue
        a = attributes(event)
        assert a['langfuse.environment'] == 'production'
        assert a[otlp.OBS_METADATA_PREFIX + 'evaluation_mode'] == 'replay'
        assert a[otlp.OBS_METADATA_PREFIX + 'evidence_kind'] == 'authored-synthetic-history'
        assert a[otlp.OBS_METADATA_PREFIX + 'cohort'] == 'production'
        tags = [v['stringValue'] for v in a['langfuse.trace.tags']['values']]
        assert tags and all(tag in ROOT_NAME_BY_PROMPT for tag in tags)
        expected = ROOT_NAME_BY_PROMPT[tags[0]] if len(tags) == 1 else SERVICE_FLOW_NAME
        assert a['langfuse.trace.name'] == expected
        if otlp.is_trace_root(event):
            assert event['name'] == expected
            seen.add(expected)
        if a.get(otlp.SESSION_ID): assert a[otlp.SESSION_ID].startswith('conversation-')
        if a.get('langfuse.user.id'): assert a['langfuse.user.id'].startswith('customer-')
    assert {'explain-product', 'explain-fees', 'guide-application', SERVICE_FLOW_NAME} <= seen


def test_normalization_preserves_identity_payload_timing_and_scores_and_is_idempotent():
    original = otlp.finalize(build_events(48, {'seed': 42}, run_date=DATE))
    legacy = deepcopy(original)
    for event in legacy:
        if not otlp.is_span(event):
            event['body']['environment'] = 'production-history'
            continue
        if otlp.is_trace_root(event): event['name'] = 'Authored history'
        for item in event['attributes']:
            if item['key'] == 'langfuse.environment': item['value'] = {'stringValue': 'production-history'}
            if item['key'] == 'langfuse.trace.name': item['value'] = {'stringValue': 'Authored history'}
            if item['key'] == 'langfuse.trace.tags': item['value'] = {'arrayValue': {'values': [{'stringValue': 'authored-history'}]}}
    snapshot = deepcopy(legacy)
    result = normalize_operations(legacy)
    assert legacy == snapshot
    assert normalize_operations(result) == result
    for before, after in zip(legacy, result):
        if not otlp.is_span(before):
            assert {k: v for k, v in before['body'].items() if k != 'environment'} == {k: v for k, v in after['body'].items() if k != 'environment'}
            continue
        for key in ('traceId', 'spanId', 'parentSpanId', 'startTimeUnixNano', 'endTimeUnixNano'):
            assert before.get(key) == after.get(key)
        for key in (otlp.OBS_INPUT, otlp.OBS_OUTPUT, otlp.SESSION_ID, 'langfuse.user.id', 'langfuse.observation.cost_details'):
            assert attributes(before).get(key) == attributes(after).get(key)


def test_experiment_names_describe_version_comparison_and_preserve_experiment_environment():
    events, links = build_historical_experiment_events({'seed': 42}, run_date=DATE)
    for item in links:
        assert item['run_name'] == experiment_run_name(item['prompt_id'], item['version'])
        assert 'authored' not in item['run_name'] and 'historical' not in item['run_name']
    for event in events:
        if otlp.is_span(event):
            assert attributes(event)['langfuse.environment'] == 'experiment'
            assert attributes(event)[otlp.OBS_METADATA_PREFIX + 'evaluation_mode'] == 'replay'


def test_existing_experiment_label_changes_without_rebinding_assets():
    events, links = build_historical_experiment_events({'seed': 42}, run_date=DATE)
    trace = links[0]['trace_id']
    for event in events:
        if event.get('traceId') == trace:
            event['attributes'].extend([
                otlp.string_attr('langfuse.experiment.name', 'authored-history-PR-01-v2-r1'),
                otlp.string_attr('langfuse.experiment.id', 'existing-experiment'),
                otlp.string_attr('langfuse.experiment.dataset.id', 'existing-dataset'),
                otlp.string_attr('langfuse.experiment.item.id', 'existing-item'),
                otlp.string_attr('langfuse.experiment.item.root_observation_id', links[0]['observation_id']),
            ])
    result = normalize_operations(events)
    for before, after in zip(events, result):
        if before.get('traceId') == trace:
            old, new = attributes(before), attributes(after)
            assert new['langfuse.experiment.name'] == experiment_run_name(links[0]['prompt_id'], links[0]['version'])
            for key in ('langfuse.experiment.id', 'langfuse.experiment.dataset.id',
                        'langfuse.experiment.item.id', 'langfuse.experiment.item.root_observation_id'):
                assert new[key] == old[key]


def test_surface_description_cleanup_is_exact_and_keeps_score_meaning():
    from synth.operation_names import (normalize_surface_descriptions, LEGACY_SCORE_COMMENT_PREFIX,
                                       LEGACY_EXPERIMENT_DESCRIPTION, EXPERIMENT_DESCRIPTION)
    events = [
        {'traceId':'trace','spanId':'generation','attributes':[
            otlp.string_attr('langfuse.experiment.description', LEGACY_EXPERIMENT_DESCRIPTION),
            otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'evidence_kind', 'authored-synthetic-history'),
            otlp.string_attr(otlp.OBS_METADATA_PREFIX + 'evaluation_mode', 'replay')]},
        {'id':'envelope','type':'score-create','timestamp':'2026-10-09T12:00:00Z','body':{
            'id':'score','traceId':'trace','observationId':'generation','value':'Pass',
            'dataType':'CATEGORICAL','comment':LEGACY_SCORE_COMMENT_PREFIX + 'E-02/r2; exact full rubric. '}},
        {'type':'score-create','body':{'comment':'A quoted ' + LEGACY_SCORE_COMMENT_PREFIX + 'must stay unchanged.'}},
    ]
    before = deepcopy(events)
    result = normalize_surface_descriptions(events)
    assert events == before
    assert attributes(result[0])['langfuse.experiment.description'] == EXPERIMENT_DESCRIPTION
    assert attributes(result[0])[otlp.OBS_METADATA_PREFIX + 'evidence_kind'] == 'authored-synthetic-history'
    assert result[1]['body']['comment'] == 'E-02/r2; exact full rubric. '
    expected = deepcopy(events[1]); expected['body']['comment'] = result[1]['body']['comment']
    assert result[1] == expected
    assert result[2] == events[2]
    assert normalize_surface_descriptions(result) == result
