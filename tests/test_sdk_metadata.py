"""Actual SDK/export regression for trace metadata overwriting scoped rubrics.

Public OtelIngestionProcessor.ts (c106bb3d) lines 438–474 merges observation
metadata then trace metadata. SDK 4.17.0 propagation coerces non-strings with
str(value); observation updates JSON-encode structured metadata. No networking.
"""
import json
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
from synth.reference_tools import CHAT_OPERATION_NAME, GENERATION_OPERATION_NAME, REFERENCE_RETRIEVER_NAME


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
    client = Langfuse(public_key='pk-offline-' + request.node.name, secret_key='sk-offline',
                      base_url='http://offline.invalid', tracer_provider=TracerProvider(),
                      span_exporter=exporter)
    emitter = LiveEmitter('http://offline.invalid', client=client)
    try:
        yield emitter, exporter
    finally:
        client.shutdown()


@pytest.mark.parametrize('distinct,serialize', [(False, False), (False, True), (True, False), (True, True)])
def test_real_export_isolates_metadata_collision_and_python_repr(sdk_emitter, distinct, serialize):
    emitter, exporter = sdk_emitter
    full = rubric_revisions('PR-03')
    scoped = rubric_revisions('PR-03', subject='user_input')
    key = 'trace_rubric_revisions' if distinct else 'rubric_revisions'
    with emitter.trace('request', metadata={key: json.dumps(full) if serialize else full}) as root:
        root.update(metadata={'rubric_revisions': scoped})
    attrs = dict(exporter.get_finished_spans()[0].attributes)
    merged = merged_exported_metadata(attrs)
    assert (merged['rubric_revisions'] == scoped) is distinct
    raw = attrs['langfuse.trace.metadata.' + key]
    if serialize:
        assert json.loads(raw) == full
    else:
        assert raw == str(full)
        with pytest.raises(ValueError):
            json.loads(raw)


def test_service_real_sdk_preserves_scoped_rubrics_and_context(sdk_emitter):
    emitter, exporter = sdk_emitter
    class Adapter(FixtureAdapter):
        is_fixture = False
        def emitter(self, **kwargs):
            return emitter
        def get_prompt(self, name, **kwargs):
            return ChatPromptClient(Prompt_Chat(name=name, version=7, config={}, labels=['production'],
                tags=[], prompt=chat_prompt('PR-03', 7)))
    service = ConversationService(Adapter())
    session = service.new('PR-03')
    turn = service.turn(session['session_id'], session['token'],
        dataset_items('PR-03')[0]['input']['user_message'], 'sdk-metadata-test')
    assert turn['status'] == 'complete'
    spans = {span.name: dict(span.attributes) for span in exporter.get_finished_spans()}
    for name, subject in ((CHAT_OPERATION_NAME, 'user_input'), (GENERATION_OPERATION_NAME, 'assistant_reply')):
        attrs = spans[name]
        merged = merged_exported_metadata(attrs)
        assert merged['rubric_revisions'] == rubric_revisions('PR-03', subject=subject)
        assert merged['trace_rubric_revisions'] == rubric_revisions('PR-03')
        assert merged['evaluation_subject'] == subject
        assert merged['current_user_message'] == turn['user']
        assert 'reference_context' in merged
        assert 'langfuse.trace.metadata.rubric_revisions' not in attrs
        assert json.loads(attrs['langfuse.trace.metadata.trace_rubric_revisions']) == rubric_revisions('PR-03')
    retriever = merged_exported_metadata(spans[REFERENCE_RETRIEVER_NAME])
    assert 'rubric_revisions' not in retriever and 'evaluation_subject' not in retriever
    assert retriever['trace_rubric_revisions'] == rubric_revisions('PR-03')
