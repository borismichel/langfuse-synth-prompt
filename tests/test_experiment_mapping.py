"""Regression for native experiment metadata exposed as literal dotted keys.

Observed in the native experiment on 2026-10-08. The public worker's
convertEventRecordToObservationForEval zips metadata path arrays without
unflattening them; extractObservationVariables parses JSON leaf values before
applying the selector. Exercise our real provisioning/mapping boundary against
that storage shape, including prior turns and complete reference objects.
"""
import json
import pytest
from synth.assets import provision_assets, variable_mapping, bind_historical_experiments
from synth.catalog import dataset_items, load_fixture
from test_assets import FakeAPI, config


def native_metadata_shape(value):
    result = {}
    def visit(item, prefix):
        if isinstance(item, dict):
            for key, nested in item.items():
                visit(nested, f'{prefix}.{key}' if prefix else key)
        else:
            # String leaves survive flattening; arrays are represented as JSON.
            result[prefix] = item if isinstance(item, str) else json.dumps(item)
    visit(value, '')
    for key, value in result.items():
        try:
            result[key] = json.loads(value)
        except (ValueError, TypeError):
            pass
    return result


def select(metadata, path):
    value = metadata
    for key in path.removeprefix('$.').split('.'):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def test_native_experiment_judge_gets_question_prior_turns_and_full_record():
    api = FakeAPI()
    provision_assets(config(), api=api)
    bodies = [body for path, body in api.writes if path.endswith('/dataset-items')]
    by_case = {item['case_id']: item for prompt in load_fixture('portfolio')['prompts']
               for item in dataset_items(prompt['id'])}
    assert len(bodies) == 32
    for body in bodies:
        item = by_case[body['metadata']['case_id']]
        native = native_metadata_shape(body['metadata'])
        expected = {'current_user_message': item['input']['user_message'],
                    'prior_messages': item['input']['conversation_history'],
                    'reference_context': item['input']['reference_context']}
        for mapping in variable_mapping('E-02', live=False):
            if mapping['source'] == 'output':
                continue
            actual = select(native, mapping['jsonPath'])
            assert actual == expected[mapping['variable']], (item['case_id'], mapping['variable'])


def test_serialized_context_preserves_whole_record_and_nonempty_prior_turns():
    from synth.assets import experiment_item_metadata
    item = next(item for item in dataset_items('PR-01') if item['input']['conversation_history'])
    metadata = experiment_item_metadata(item)
    assert all(isinstance(metadata[key], str) for key in
               ('eval_current_user_message', 'eval_prior_messages', 'eval_reference_context'))
    assert json.loads(metadata['eval_prior_messages']) == item['input']['conversation_history']
    assert json.loads(metadata['eval_reference_context']) == item['input']['reference_context']
    assert metadata['eval_current_user_message'] == item['input']['user_message']
    assert select(native_metadata_shape(metadata), '$.evaluation_context.reference_context') is None
    assert select(native_metadata_shape(metadata), '$.eval_reference_context') == item['input']['reference_context']


def test_historical_experiment_binding_carries_the_same_native_context():
    from datetime import datetime, timezone
    from synth.materialize import build_historical_experiment_events
    from synth.assets import experiment_item_metadata
    api = FakeAPI()
    provisioning = provision_assets(config(), api=api)
    events, links = build_historical_experiment_events({'seed': 42},
        run_date=datetime(2026, 10, 8, tzinfo=timezone.utc))
    bound, _ = bind_historical_experiments(events, provisioning, links)
    spans = {event['spanId']: event for event in bound if 'spanId' in event}
    for link in links:
        item = next(item for item in dataset_items(link['prompt_id']) if item['case_id'] == link['case_id'])
        expected = experiment_item_metadata(item)
        attrs = {entry['key']: entry['value']['stringValue']
                 for entry in spans[link['observation_id']]['attributes'] if 'stringValue' in entry['value']}
        for field in ('eval_current_user_message', 'eval_prior_messages', 'eval_reference_context'):
            assert attrs['langfuse.experiment.item.metadata.' + field] == expected[field]


@pytest.mark.parametrize('eid', [f'E-{index:02}' for index in range(1, 12)])
def test_experiment_defaults_change_without_changing_live_rule_context(eid):
    for mapping in variable_mapping(eid, live=True):
        if mapping['source'] == 'output':
            continue
        assert mapping == {'variable': mapping['variable'], 'source': 'metadata',
                           'jsonPath': '$.' + mapping['variable']}
    for mapping in variable_mapping(eid, live=False):
        if mapping['source'] == 'output':
            continue
        assert mapping == {'variable': mapping['variable'], 'source': 'experiment_item_metadata',
                           'jsonPath': '$.eval_' + mapping['variable']}
