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


def test_role_models_override_legacy_global_pin_without_mutating_environment(monkeypatch):
    from synth.companion.app import RoleModelAdapter
    from synth.config import load_config
    from synth.model_policy import MODEL_BY_PROMPT
    monkeypatch.setenv('LLM_MODEL', 'claude-sonnet-4-6')
    monkeypatch.setenv('LLM_PROVIDER', 'anthropic')
    adapter = RoleModelAdapter(load_config('config/demo.yaml'))
    clients = [adapter.llm(MODEL_BY_PROMPT[pid]) for pid in ('PR-01', 'PR-02', 'PR-03')]
    assert [client.model for client in clients] == ['claude-sonnet-5-5', 'claude-opus-5-5', 'claude-opus-5-5']
    assert clients[1] is clients[2] and clients[0] is not clients[1]
    import os
    assert os.environ['LLM_MODEL'] == 'claude-sonnet-4-6'


def test_role_model_rejects_incompatible_provider(monkeypatch):
    from synth.companion.app import RoleModelAdapter
    from synth.config import load_config
    monkeypatch.setenv('LLM_PROVIDER', 'openai')
    with pytest.raises(ValueError, match='Anthropic'):
        RoleModelAdapter(load_config('config/demo.yaml')).llm('claude-sonnet-5-5')
