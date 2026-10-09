"""Native storage references preserve resolved fixtures and SDK compilation."""
from copy import deepcopy
import json
import re
from urllib.parse import unquote

from langfuse.api.prompts.types.prompt import Prompt_Chat
from langfuse.model import ChatPromptClient
import pytest

from synth.assets import AssetConflict, chat_prompt, provision_assets, stored_chat_prompt, verify_assets
from synth.catalog import dataset_items, load_fixture, system_prompt
from synth.prompt_composition import COMPOSITION_REVISION, building_blocks, compose_chat_prompt, prompt_reference
from test_assets import FakeAPI, config


TAG = re.compile(r'@@@langfusePrompt:name=([^|]+)\|version=(\d+)@@@')


class NativePromptAPI(FakeAPI):
    """Public get contract: raw opt-out, otherwise resolve text dependencies."""
    def __init__(self):
        super().__init__()
        self.reads = []

    def stored(self, name, version):
        return next(v for p, v in self.created.items() if p.startswith('/api/public/v2/prompts/')
                    and v['name'] == name and v['version'] == version)

    def read(self, path, params=None):
        self.reads.append((path, deepcopy(params)))
        if path.startswith('/api/public/v2/prompts/'):
            name = unquote(path.removeprefix('/api/public/v2/prompts/'))
            params = params or {}
            candidates = [v for p, v in self.created.items() if p.startswith('/api/public/v2/prompts/') and v['name'] == name]
            version = params.get('version')
            actual = deepcopy(next(v for v in candidates if v['version'] == version)) if version else deepcopy(
                next(v for v in candidates if params.get('label', 'production') in v['labels']))
            actual['resolutionGraph'] = None
            if params.get('resolve') in (False, 'false'):
                return actual
            dependencies = []
            def substitute(match):
                child = self.stored(match[1], int(match[2]))
                assert child['type'] == 'text'
                dependencies.append({'name': child['name'], 'version': child['version']})
                return child['prompt']
            if isinstance(actual['prompt'], str):
                actual['prompt'] = TAG.sub(substitute, actual['prompt'])
            else:
                for message in actual['prompt']:
                    if 'content' in message:
                        message['content'] = TAG.sub(substitute, message['content'])
            if dependencies:
                actual['resolutionGraph'] = {'dependencies': {'parent': dependencies}}
            return actual
        return super().read(path, params)


@pytest.fixture
def seeded():
    api = NativePromptAPI()
    return api, provision_assets(config(), api=api)


def test_four_text_families_are_created_before_all_nine_chat_families(seeded):
    api, receipt = seeded
    bodies = [body for path, body in api.writes if path == '/api/public/v2/prompts']
    assert [body['type'] for body in bodies] == ['text'] * 5 + ['chat'] * 72
    assert len({body['name'] for body in bodies if body['type'] == 'text'}) == 4
    assert len({body['name'] for body in bodies if body['type'] == 'chat'}) == 9
    assert receipt['prompt_composition'] == COMPOSITION_REVISION
    assert set(receipt['building_blocks']) == set(building_blocks())
    assert len(receipt['prompts']) == 9
    for body in bodies[5:]:
        references = TAG.findall(json.dumps(body['prompt']))
        assert references
        assert ('building-blocks/reference-context', '1') in references
        for name, version in references:
            assert api.stored(name, int(version))['type'] == 'text'
    assert api.stored('building-blocks/voice', 1)['labels'] == ['production']
    assert api.stored('building-blocks/voice', 2)['labels'] == ['playful']


def test_every_resolved_agent_version_is_byte_identical_to_accepted_fixture(seeded):
    api, _ = seeded
    for prompt in load_fixture('portfolio')['prompts']:
        for version in range(1, 9):
            path = '/api/public/v2/prompts/' + prompt['name']
            resolved = api.read(path, {'version': version})
            assert resolved['prompt'] == chat_prompt(prompt['id'], version)
            assert resolved['prompt'][0]['content'] == system_prompt(prompt['id'], version)
            assert resolved['resolutionGraph']
            raw = api.read(path, {'version': version, 'resolve': 'false'})
            assert raw['prompt'] == stored_chat_prompt(prompt['id'], version)
            assert raw['resolutionGraph'] is None
            assert raw['prompt'] != resolved['prompt']


def compile_prompt(messages, version, variables):
    return ChatPromptClient(Prompt_Chat(name='test', version=version, config={}, labels=[], tags=[],
                                      prompt=messages)).compile(**variables)


def test_real_sdk_compiles_resolved_composition_with_every_dataset_input(seeded):
    api, _ = seeded
    for prompt in load_fixture('portfolio')['prompts']:
        for version in (7, 8):
            native = api.read('/api/public/v2/prompts/' + prompt['name'], {'version': version})['prompt']
            for item in dataset_items(prompt['id']):
                variables = {**item['input'], 'reference_context': json.dumps(item['input']['reference_context'], ensure_ascii=False)}
                compiled = compile_prompt(native, version, variables)
                assert compiled == compile_prompt(chat_prompt(prompt['id'], version), version, variables)
                assert compiled[1]['content'] == 'Supplied reference_context:\n' + variables['reference_context']
                assert compiled[2:-1] == item['input']['conversation_history']
                assert compiled[-1] == {'role': 'user', 'content': item['input']['user_message']}
                assert '@@@langfusePrompt:' not in json.dumps(compiled)


def test_existing_playful_candidate_can_use_shared_voice_without_new_wording(seeded):
    api, _ = seeded
    messages = stored_chat_prompt('PR-01', 9)
    assert prompt_reference('building-blocks/voice', 2) in messages[0]['content']
    assert building_blocks()['voice']['versions'][1]['prompt'] == load_fixture('product')['prompt_comparison']['change']
    api.create('/api/public/v2/prompts', {'name': 'presenter-candidate', 'type': 'chat', 'prompt': messages, 'labels': []})
    resolved = api.read('/api/public/v2/prompts/presenter-candidate', {'version': 1})['prompt']
    assert resolved == chat_prompt('PR-01', 9)
    item = dataset_items('PR-01')[0]
    variables = {**item['input'], 'reference_context': json.dumps(item['input']['reference_context'])}
    assert compile_prompt(resolved, 9, variables) == compile_prompt(chat_prompt('PR-01', 9), 9, variables)


def test_verifier_requires_raw_references_resolved_content_and_all_blocks(seeded):
    api, receipt = seeded
    checks = {name: ok for name, ok, _ in verify_assets(config(), receipt, api=api)}
    relevant = {name: ok for name, ok in checks.items() if name.startswith(('prompt-', 'building-block-'))}
    assert relevant and all(relevant.values())
    assert len([name for name in relevant if name.startswith('prompt-raw-')]) == 72
    # Identical resolved text alone cannot conceal missing actual composition.
    stored = api.stored('products/explainer', 7)
    stored['prompt'] = chat_prompt('PR-01', 7)
    checks = {name: ok for name, ok, _ in verify_assets(config(), receipt, api=api)}
    assert not checks['prompt-raw-PR-01-v7'] and not checks['prompt-PR-01-v7']
    del receipt['building_blocks']['voice']
    checks = {name: ok for name, ok, _ in verify_assets(config(), receipt, api=api)}
    assert not checks['building-block-coverage'] and not checks['building-block-voice-v1']


def test_changed_shared_content_fails_both_component_and_resolved_checks(seeded):
    api, receipt = seeded
    api.stored('building-blocks/factual-boundaries', 1)['prompt'] += ' Changed rule.'
    checks = {name: ok for name, ok, _ in verify_assets(config(), receipt, api=api)}
    assert not checks['building-block-factual-boundaries-v1']
    assert not checks['prompt-PR-02-v7']
    assert checks['prompt-raw-PR-02-v7']


def test_legacy_uncomposed_receipts_remain_verifiable(seeded):
    api, receipt = seeded
    receipt.pop('prompt_composition')
    receipt.pop('building_blocks')
    for prompt in load_fixture('portfolio')['prompts']:
        for version in range(1, 9):
            api.stored(prompt['name'], version)['prompt'] = chat_prompt(prompt['id'], version)
    checks = {name: ok for name, ok, _ in verify_assets(config(), receipt, api=api)}
    assert all(ok for name, ok in checks.items() if name.startswith('prompt-'))
    assert not any(name.startswith('prompt-raw-') for name in checks)


def test_shared_namespace_collision_fails_before_any_asset_write():
    api = FakeAPI(collision=('/api/public/v2/prompts', 'building-blocks/voice'))
    with pytest.raises(AssetConflict, match='Fresh namespace'):
        provision_assets(config(), api=api)
    assert not api.writes


def test_composition_preserves_input_and_rejects_already_composed_input():
    resolved = chat_prompt('PR-02', 7)
    before = deepcopy(resolved)
    composed = compose_chat_prompt(resolved)
    assert resolved == before
    with pytest.raises(ValueError, match='resolved fixture'):
        compose_chat_prompt(composed)
