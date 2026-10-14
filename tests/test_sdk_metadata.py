"""Actual SDK/export regression for trace metadata overwriting scoped rubrics.

Public OtelIngestionProcessor.ts (c106bb3d) lines 438–474 merges observation
metadata then trace metadata. SDK v5 JSON-encodes structured values once.
Observe actual spans and public score HTTP delivery without external networking.
"""
import json
import httpx
import pytest
from langfuse import Langfuse
from langfuse.api.prompts.types.prompt import Prompt_Chat
from langfuse.model import ChatPromptClient
from langfuse_synth_core.live.emit import LiveEmitter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from synth.assets import chat_prompt
from synth.catalog import dataset_items, rubric_revisions
from synth.companion.preview import FixtureAdapter
from synth.companion.service import ConversationService
from synth.operation_names import ROOT_NAME_BY_PROMPT
from synth.reference_tools import GENERATION_OPERATION_NAME, REFERENCE_RETRIEVER_NAME


def merged_exported_metadata(attrs):
    """Apply the verified public ingestion precedence to actual exported attrs."""
    result = {}
    for prefix in ('langfuse.observation.metadata.', 'langfuse.trace.metadata.'):
        for key, value in attrs.items():
            if key.startswith(prefix):
                try:
                    value = json.loads(value)
                except (ValueError, TypeError):
                    pass
                result[key.removeprefix(prefix)] = value
    return result


@pytest.fixture
def sdk_emitter(monkeypatch, request):
    import socket
    monkeypatch.setattr(socket.socket, 'connect', lambda *a, **k: pytest.fail('No network allowed'))
    exporter = InMemorySpanExporter()
    scores = []

    def receive(request):
        assert request.method == 'POST' and request.url.path == '/api/public/scores'
        scores.extend(json.loads(request.content))
        return httpx.Response(202, json={'message': 'Accepted'})

    client = Langfuse(public_key='pk-offline-' + request.node.name, secret_key='sk-offline',
                      base_url='http://offline.invalid', tracer_provider=TracerProvider(),
                      span_exporter=exporter,
                      httpx_client=httpx.Client(transport=httpx.MockTransport(receive)))
    emitter = LiveEmitter('http://offline.invalid', client=client)
    try:
        yield emitter, exporter, scores
    finally:
        client.shutdown()


@pytest.mark.parametrize('distinct', [False, True])
def test_real_export_preserves_structured_metadata_and_scoped_ownership(sdk_emitter, distinct):
    emitter, exporter, _ = sdk_emitter
    full = rubric_revisions('PR-03')
    scoped = rubric_revisions('PR-03', subject='user_input')
    key = 'trace_rubric_revisions' if distinct else 'rubric_revisions'
    with emitter.trace('request', metadata={key: full}) as root:
        root.update(metadata={'rubric_revisions': scoped})
    attrs = dict(exporter.get_finished_spans()[0].attributes)
    merged = merged_exported_metadata(attrs)
    assert (merged['rubric_revisions'] == scoped) is distinct
    # Exactly one decode yields a dictionary, not a pre-serialized JSON string.
    assert json.loads(attrs['langfuse.trace.metadata.' + key]) == full


@pytest.mark.parametrize('pid', ['PR-01', 'PR-02', 'PR-03'])
def test_service_real_sdk_preserves_scoped_rubrics_and_context(sdk_emitter, pid):
    emitter, exporter, _ = sdk_emitter
    class Adapter(FixtureAdapter):
        is_fixture = False
        def emitter(self, **kwargs):
            return emitter
        def get_prompt(self, name, **kwargs):
            return ChatPromptClient(Prompt_Chat(name=name, version=7, config={}, labels=['production'],
                tags=[], prompt=chat_prompt(pid, 7)))
    service = ConversationService(Adapter())
    session = service.new(pid)
    turn = service.turn(session['session_id'], session['token'],
        dataset_items(pid)[0]['input']['user_message'], 'sdk-metadata-test')
    assert turn['status'] == 'complete'
    spans = {span.name: dict(span.attributes) for span in exporter.get_finished_spans()}
    for name, subject in ((ROOT_NAME_BY_PROMPT[pid], 'user_input'), (GENERATION_OPERATION_NAME, 'assistant_reply')):
        attrs = spans[name]
        merged = merged_exported_metadata(attrs)
        assert merged['rubric_revisions'] == rubric_revisions(pid, subject=subject)
        assert merged['trace_rubric_revisions'] == rubric_revisions(pid)
        assert merged['evaluation_subject'] == subject
        assert merged['evaluation_mode'] == 'online'
        assert merged['current_user_message'] == turn['user']
        reference = merged['reference_context']
        assert reference['id'] == 'SRC-01'
        assert reference['monthly_fee'] == 4
        assert reference['waiver']['fee'] == 0
        assert reference['waiver']['exclusions'] == ['Transfers from your own accounts do not count as salary deposits.']
        assert merged['prior_messages'] == []
        assert 'langfuse.trace.metadata.rubric_revisions' not in attrs
        assert json.loads(attrs['langfuse.trace.metadata.trace_rubric_revisions']) == rubric_revisions(pid)
    retriever = merged_exported_metadata(spans[REFERENCE_RETRIEVER_NAME])
    assert 'rubric_revisions' not in retriever and 'evaluation_subject' not in retriever
    assert 'evaluation_mode' not in retriever
    assert retriever['trace_rubric_revisions'] == rubric_revisions(pid)
    generation = spans[GENERATION_OPERATION_NAME]
    assert json.loads(generation['langfuse.observation.usage_details']) == turn['usage']
    assert generation['langfuse.observation.model.name'] == turn['model']
    assert json.loads(generation['langfuse.observation.output']) == [{'role': 'assistant', 'content': turn['reply']}]
    root_attrs = spans[ROOT_NAME_BY_PROMPT[pid]]
    assert json.loads(root_attrs['langfuse.observation.input']) == {'messages': [{'role': 'user', 'content': turn['user']}]}
    assert root_attrs['langfuse.observation.output'] == generation['langfuse.observation.output']
    assert generation['langfuse.observation.prompt.name'] == turn['prompt_name']
    assert generation['langfuse.observation.prompt.version'] == 7
    root = merged_exported_metadata(spans[ROOT_NAME_BY_PROMPT[pid]])
    for key in ('prompt_name', 'prompt_version', 'resolved_version', 'prompt_label', 'prompt_references'):
        assert key not in root
        assert key not in retriever
    prompt_metadata = merged_exported_metadata(generation)
    assert prompt_metadata['prompt_name'] == turn['prompt_name']
    assert prompt_metadata['prompt_version'] == prompt_metadata['resolved_version'] == 7
    assert prompt_metadata['prompt_label'] == 'production'
    # Prompt association belongs to the actual model invocation, never invented
    # on the application SPAN or reference retriever.
    assert 'langfuse.observation.prompt.name' not in spans[ROOT_NAME_BY_PROMPT[pid]]
    assert 'langfuse.observation.prompt.name' not in spans[REFERENCE_RETRIEVER_NAME]


def test_feedback_real_sdk_delivers_once_to_saved_root_after_a_later_reply(sdk_emitter):
    emitter, exporter, scores = sdk_emitter
    class Adapter(FixtureAdapter):
        is_fixture = False
        def emitter(self, **kwargs):
            return emitter
        def get_prompt(self, name, **kwargs):
            return ChatPromptClient(Prompt_Chat(name=name, version=7, config={}, labels=['production'],
                tags=[], prompt=chat_prompt('PR-01', 7)))
    service = ConversationService(Adapter())
    session = service.new('PR-01')
    first = service.turn(session['session_id'], session['token'],
                         dataset_items('PR-01')[0]['input']['user_message'], 'first-sdk-reply')
    second = service.turn(session['session_id'], session['token'],
                          dataset_items('PR-01')[0]['input']['user_message'], 'second-sdk-reply')
    for _ in range(2):
        receipt = service.feedback(session['session_id'], session['token'],
                                   first['request_id'], 0, 'I disagree with this explanation.')
    emitter.flush()
    assert receipt['status'] == 'submitted'
    assert len(scores) == 1
    payload = scores[0]
    assert payload['name'] == 'user-thumbs'
    assert payload['dataType'] == 'BOOLEAN' and payload['value'] == 0
    assert payload['traceId'] == first['trace_id'] != second['trace_id']
    assert payload['observationId'] == first['root_observation_id'] != first['generation_id']
    assert payload['id'] == receipt['score_id']
    assert payload['comment'] == 'I disagree with this explanation.'
    assert payload['metadata']['signal_source'] == 'explicit-user-feedback'
    roots = [s for s in exporter.get_finished_spans() if s.name == ROOT_NAME_BY_PROMPT['PR-01']]
    assert len(roots) == 2
    assert [format(s.context.trace_id, '032x') for s in roots] == [first['trace_id'], second['trace_id']]
    assert [format(s.context.span_id, '016x') for s in roots] == [first['root_observation_id'], second['root_observation_id']]
