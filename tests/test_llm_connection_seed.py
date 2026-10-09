"""Seed connection configuration without model calls or persisted credentials."""
from copy import deepcopy
import json
from types import SimpleNamespace
import traceback

import pytest

from synth.assets import AssetAPI, AssetConflict, configure_evaluators, ensure_llm_connection, provision_assets
from synth.config import Config, Evaluation, Generation, Live, Target
from synth.model_policy import MODEL_PRICES
from test_assets import FakeAPI


TEST_KEY = 'synthetic-connection-key-not-a-provider-credential'


@pytest.fixture(autouse=True)
def isolated_credentials(monkeypatch):
    for name in ('LLM_PROVIDER', 'LLM_API_KEY', 'ANTHROPIC_API_KEY', 'OPENAI_API_KEY',
                 'LLM_BASE_URL', 'ANTHROPIC_BASE_URL', 'OPENAI_BASE_URL', 'LANGFUSE_BASE_URL'):
        monkeypatch.delenv(name, raising=False)


def config():
    return Config(Target('https://demo.invalid'), Generation(42, 3),
                  Evaluation('anthropic', 'claude-sonnet-5-5'), Live('claude-sonnet-5-5'))


class ConnectionAPI(FakeAPI):
    def __init__(self, connections=None, **kwargs):
        super().__init__(**kwargs)
        self.connections = deepcopy(connections or [])
        self.connection_writes = []
        self.connection_reads = 0

    def read(self, path, params=None):
        if path == '/api/public/llm-connections':
            self.connection_reads += 1
            return {'data': deepcopy(self.connections), 'meta': {'totalPages': 1}}
        return super().read(path, params)

    def create_llm_connection(self, body):
        self.connection_writes.append(deepcopy(body))
        self.connections.append({**{k: deepcopy(v) for k, v in body.items() if k != 'secretKey'},
                                 'id': 'llm-connection', 'displaySecretKey': 'MASKED-DO-NOT-PERSIST',
                                 'baseURL': None, 'extraHeaderKeys': [], 'config': None})


@pytest.mark.parametrize('key_mode', ['canonical', 'generic', 'both'])
def test_seed_provisions_connection_before_evaluator_lookup_without_judge_calls(monkeypatch, capsys, key_mode):
    if key_mode in {'canonical', 'both'}: monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    if key_mode in {'generic', 'both'}:
        monkeypatch.setenv('LLM_PROVIDER', 'anthropic')
        monkeypatch.setenv('LLM_API_KEY', TEST_KEY)
    api = ConnectionAPI()
    original_read = api.read
    def read_after_connection(path, params=None):
        if path == '/api/public/v2/evaluators':
            assert len(api.connection_writes) == 1
        return original_read(path, params)
    api.read = read_after_connection
    receipt = provision_assets(config(), api=api)
    assert api.connection_writes == [{'provider': 'anthropic', 'adapter': 'anthropic', 'secretKey': TEST_KEY,
                                     'withDefaultModels': True, 'customModels': sorted(MODEL_PRICES)}]
    assert not any('evaluat' in path for path, _ in api.writes)
    assert receipt['evaluators'] == {}
    assert all('LLM connection' not in missing for missing in receipt['missing'])
    persisted = json.dumps(receipt)
    assert TEST_KEY not in persisted and 'MASKED-DO-NOT-PERSIST' not in persisted and 'secretKey' not in persisted
    assert TEST_KEY not in capsys.readouterr().out
    ensure_llm_connection(config(), api=api)
    assert len(api.connection_writes) == 1


def test_missing_key_preserves_optional_setup_gate_and_creates_no_connection():
    api = ConnectionAPI()
    receipt = provision_assets(config(), api=api)
    assert api.connection_writes == []
    assert any('configured Langfuse LLM connection' in message for message in receipt['missing'])


def test_explicit_evaluator_setup_creates_missing_connection_before_judges(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    api = ConnectionAPI()
    original_create = api.create
    def require_connection(path, body):
        assert len(api.connection_writes) == 1
        return original_create(path, body)
    api.create = require_connection
    receipt = configure_evaluators(config(), api=api)
    assert len(receipt['evaluators']) == len(receipt['evaluator_rules']) == 10
    assert not receipt['missing']
    assert TEST_KEY not in json.dumps(receipt)
    assert configure_evaluators(config(), api=api) == receipt
    assert len(api.connection_writes) == 1


def test_existing_compatible_connection_is_reused_without_reading_or_overwriting_key(monkeypatch):
    existing = {'provider': 'anthropic', 'adapter': 'anthropic', 'id': 'existing',
                'withDefaultModels': True, 'customModels': ['custom-model'], 'baseURL': 'https://gateway.invalid'}
    api = ConnectionAPI([existing])
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    monkeypatch.setenv('LLM_API_KEY', 'different-unused-key')
    monkeypatch.setenv('LLM_PROVIDER', 'anthropic')
    ensure_llm_connection(config(), api=api)
    assert api.connections == [existing] and not api.connection_writes


@pytest.mark.parametrize('connection', [
    {'provider': 'anthropic', 'adapter': 'openai', 'withDefaultModels': True},
    {'provider': 'anthropic', 'adapter': 'anthropic', 'withDefaultModels': False, 'customModels': ['claude-old']},
])
def test_existing_incompatible_connection_is_never_overwritten(monkeypatch, connection):
    api = ConnectionAPI([connection])
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    with pytest.raises(AssetConflict, match='incompatible'):
        provision_assets(config(), api=api)
    assert api.connections == [connection] and not api.connection_writes and not api.writes


@pytest.mark.parametrize('conflict', ['provider', 'keys', 'model', 'base_url'])
def test_ambiguous_or_incompatible_credentials_fail_without_writes(monkeypatch, conflict):
    api, cfg = ConnectionAPI(), config()
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    if conflict == 'provider':
        monkeypatch.setenv('LLM_PROVIDER', 'openai')
        monkeypatch.setenv('OPENAI_API_KEY', 'other-provider-key')
    if conflict == 'keys':
        monkeypatch.setenv('LLM_PROVIDER', 'anthropic')
        monkeypatch.setenv('LLM_API_KEY', 'different-key')
    if conflict == 'model': cfg.live.model = 'gpt-5'
    if conflict == 'base_url': monkeypatch.setenv('ANTHROPIC_BASE_URL', 'https://gateway.invalid')
    with pytest.raises(AssetConflict):
        ensure_llm_connection(cfg, api=api)
    assert not api.connection_writes and not api.writes


def test_generic_key_requires_explicit_provider_binding(monkeypatch):
    monkeypatch.setenv('LLM_API_KEY', TEST_KEY)
    api = ConnectionAPI()
    ensure_llm_connection(config(), api=api)
    assert not api.connection_writes


def test_fresh_namespace_conflict_prevents_even_connection_creation(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    api = ConnectionAPI(collision=('/api/public/v2/prompts', 'products/explainer'))
    with pytest.raises(AssetConflict, match='Fresh namespace'):
        provision_assets(config(), api=api)
    assert not api.connection_writes and not api.writes


def test_readback_mismatch_stops_before_seed_assets(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    api = ConnectionAPI()
    create = api.create_llm_connection
    def wrong_adapter(body):
        create(body)
        api.connections[0]['adapter'] = 'openai'
    api.create_llm_connection = wrong_adapter
    with pytest.raises(AssetConflict, match='read back'):
        provision_assets(config(), api=api)
    assert len(api.connection_writes) == 1 and not api.writes


def test_secret_bearing_put_stays_on_configured_langfuse_origin(monkeypatch):
    from langfuse_synth_core import http, lfread
    calls = []
    monkeypatch.setattr(lfread, 'auth_from_env', lambda: ('public', 'secret'))
    def request(*args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(status_code=201)
    monkeypatch.setattr(http, 'request_retry', request)
    assert AssetAPI('https://demo.invalid/langfuse').create_llm_connection({'secretKey': TEST_KEY}) is None
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args == ('PUT', 'https://demo.invalid/langfuse/api/public/llm-connections')
    assert kwargs['allow_redirects'] is False and kwargs['attempts'] == 1


@pytest.mark.parametrize('failure', [307, 401, 500, 'transport'])
def test_connection_errors_never_expose_secret_response_or_request(monkeypatch, failure):
    from langfuse_synth_core import http, lfread
    monkeypatch.setattr(lfread, 'auth_from_env', lambda: ('public', 'secret'))
    def request(*args, **kwargs):
        if failure == 'transport': raise RuntimeError('request contained ' + TEST_KEY)
        return SimpleNamespace(status_code=failure, text=TEST_KEY)
    monkeypatch.setattr(http, 'request_retry', request)
    try:
        AssetAPI('https://demo.invalid').create_llm_connection({'secretKey': TEST_KEY})
    except AssetConflict:
        assert TEST_KEY not in traceback.format_exc()
    else:
        pytest.fail('Failed or redirected requests must stop setup')


def test_dry_run_with_key_never_provisions_connection_or_persists_key(monkeypatch, tmp_path):
    from synth import seed
    monkeypatch.setenv('ANTHROPIC_API_KEY', TEST_KEY)
    monkeypatch.setenv('SYNTH_STATE_DIR', str(tmp_path / 'state'))
    monkeypatch.setenv('SYNTH_OUT_DIR', str(tmp_path / 'out'))
    monkeypatch.setattr(AssetAPI, 'create_llm_connection', lambda *a: pytest.fail('No connection write in dry run'))
    seed.run_seed(config(), dry_run=True, spool_path=tmp_path / 'events.ndjson', log=lambda _: None)
    assert all(TEST_KEY.encode() not in path.read_bytes() for path in tmp_path.rglob('*') if path.is_file())
