"""A production image must include every provider advertised by the manifest."""
import pytest
from langfuse_synth_core.companion.llm import LLMClient

@pytest.mark.parametrize('provider,variable',[('openai','OPENAI_API_KEY'),('anthropic','ANTHROPIC_API_KEY')])
def test_supported_provider_constructs_without_network(provider,variable,monkeypatch):
    import socket
    def denied(*a,**k): raise AssertionError('Provider binding must not make a model call')
    monkeypatch.setattr(socket.socket,'connect',denied)
    monkeypatch.setenv(variable,'test-key-not-a-real-credential')
    client=LLMClient(provider,'test-model').bind()
    assert client is not None
    client.close()
