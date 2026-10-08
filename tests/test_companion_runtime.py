"""Scenario assertions at the actual companion HTTP and adapter seams, no egress."""
from types import SimpleNamespace
import subprocess
import sys
import os

import pytest
from fastapi.testclient import TestClient

from synth.catalog import load_fixture, score_definitions
from synth.companion.app import create_app
from synth.companion.preview import FixtureAdapter
from synth.companion.service import ConversationService


class TestAdapter(FixtureAdapter):
    __test__ = False
    is_fixture = False


def setup_client(preview=False):
    adapter = FixtureAdapter() if preview else TestAdapter()
    client = TestClient(create_app(adapter, preview=preview))
    return adapter, client


def session(client, pid="PR-01"):
    response = client.post("/api/conversations", json={"prompt_id": pid})
    assert response.status_code == 200
    return response.json()


def post_turn(client, state, message=None, request_id="request-0001"):
    if message is None:
        message = load_fixture("product")["conversation"]["turns"][0]["user"]
    return client.post(f"/api/conversations/{state['session_id']}/turns",
                       headers={"X-Conversation-Token": state["token"]},
                       json={"message": message, "request_id": request_id})


def test_each_turn_refreshes_prompt_and_old_reply_retains_resolved_version():
    adapter, client = setup_client()
    state = session(client)
    first = post_turn(client, state).json()
    adapter.versions["PR-01"] = 9
    second = post_turn(client, state, request_id="request-0002").json()
    assert first["prompt_version"] == 7
    assert second["prompt_version"] == 9
    assert first["session_id"] == second["session_id"]
    assert first["trace_id"] != second["trace_id"]
    assert first["root_observation_id"] != first["generation_id"]
    assert "/sessions/" in first["session_url"]
    assert "?observation=" in first["observation_url"]
    assert [f["ttl"] for f in adapter.prompt_fetches] == [0, 0]
    assert all(f["label"] == "production" and f["type"] == "chat" for f in adapter.prompt_fetches)
    assert len(adapter.completions) == 2
    assert adapter.completions[1]["messages"] == [
        {"role": "user", "content": first["user"]},
        {"role": "assistant", "content": first["reply"]},
        {"role": "user", "content": second["user"]}]
    roots = [o for o in adapter.observations if o.root]
    gens = [o for o in adapter.observations if not o.root]
    assert len(roots) == len(gens) == 2
    for root, gen in zip(roots, gens):
        assert root.fields["metadata"]["evaluation_subject"] == "user_input"
        assert gen.fields["metadata"]["evaluation_subject"] == "assistant_reply"
        assert root.fields["input"]["messages"] == [{"role": "user", "content": first["user"]}]
        for key in ("current_user_message", "prior_messages", "reference_context"):
            assert root.fields["input"][key] == gen.fields["input"][key]
            assert root.fields["metadata"][key] == gen.fields["metadata"][key]
        assert gen.fields["prompt"].version == root.fields["metadata"]["prompt_version"]
        assert gen.fields["usage_details"] == {"input": 0, "output": 0}
        assert root.fields["output"][0]["role"] == "assistant"


def test_feedback_uses_saved_root_after_new_turn_and_upserts_same_score():
    adapter, client = setup_client()
    state = session(client)
    first = post_turn(client, state).json()
    second = post_turn(client, state, request_id="request-0002").json()
    path = f"/api/conversations/{state['session_id']}/feedback"
    headers = {"X-Conversation-Token": state["token"]}
    for value in (1, 0):
        result = client.post(path, headers=headers, json={"request_id": first["request_id"], "value": value, "comment": "Review first reply"})
        assert result.status_code == 200
        assert result.json()["observation_id"] == first["root_observation_id"]
    assert len(adapter.feedback) == 1
    score = next(iter(adapter.feedback.values()))
    assert score["value"] == 0 and score["data_type"] == "BOOLEAN"
    assert score["trace_id"] == first["trace_id"] != second["trace_id"]
    assert score["observation_id"] != first["generation_id"]
    assert client.post(path, headers={"X-Conversation-Token": "wrong"}, json={"request_id": first["request_id"], "value": 1}).status_code == 404
    adapter.fail_feedback = True
    assert client.post(path, headers=headers, json={"request_id": first["request_id"], "value": 1}).status_code == 502


@pytest.mark.parametrize("failure", ["fail_prompt", "fail_model"])
def test_errors_preserve_request_identity_without_a_fabricated_reply(failure):
    adapter, client = setup_client()
    setattr(adapter, failure, True)
    state = session(client)
    response = post_turn(client, state).json()
    assert response["status"] == "failed" and response["reply"] == ""
    assert response["root_observation_id"] and response["trace_id"]
    assert response["evaluation_status"] == "unavailable"
    assert adapter.observations[0].fields["level"] == "ERROR"
    assert adapter.observations[0].fields["metadata"]["reference_context"]["id"] == "SRC-01"
    if failure == "fail_model":
        assert adapter.observations[1].fields["level"] == "ERROR"
    # Same request is not automatically retried (and therefore cannot double bill).
    post_turn(client, state)
    assert len(adapter.completions) == (1 if failure == "fail_model" else 0)


def test_repeated_request_is_idempotent_but_cannot_change_message():
    adapter, client = setup_client()
    state = session(client)
    first = post_turn(client, state).json()
    assert post_turn(client, state).json() == first
    assert len(adapter.completions) == 1
    assert post_turn(client, state, message="different").status_code == 409
    assert post_turn(client, state, message="  ", request_id="request-0002").status_code == 400


def test_all_three_bots_and_separate_sessions():
    adapter, client = setup_client()
    catalog = client.get("/api/catalog").json()
    ids = set()
    for bot in catalog["bots"]:
        state = session(client, bot["id"])
        turn = post_turn(client, state, bot["suggestions"][0]["message"]).json()
        assert turn["status"] == "complete" and turn["reply"]
        ids.add(turn["session_id"])
    assert len(ids) == 3
    assert client.post("/api/conversations", json={"prompt_id": "PR-04"}).status_code == 422


def test_preview_is_explicit_and_health_never_claims_live_readiness(monkeypatch):
    adapter, client = setup_client(preview=True)
    assert client.get("/healthz").status_code == 503
    assert client.get("/healthz").json()["ready"] is False
    assert client.get("/").headers["X-Demo-Mode"] == "preview"
    state = session(client)
    turn = post_turn(client, state).json()
    assert turn["preview"] and turn["session_url"] is None
    with pytest.raises(ValueError):
        create_app(FixtureAdapter())
    with pytest.raises(ValueError):
        create_app(TestAdapter(), preview=True)
    monkeypatch.setenv("LIVE_BASE_PATH", "/live/demo")
    html = client.get("/").text
    assert '/live/demo/static/app.js' in html and '/live/demo/static/style.css' in html
    assert client.get('/static/fonts/inter.ttf').status_code == 200


def test_preview_process_clears_credentials_and_blocks_even_loopback():
    code = '''
from synth.companion.preview import create_preview_app
import os, socket
app=create_preview_app()
assert 'LANGFUSE_SECRET_KEY' not in os.environ
assert 'LANGFUSE_BASE_URL' not in os.environ
try: socket.create_connection(('127.0.0.1',9))
except Exception as e: assert type(e).__name__=='EgressBlockedError'
else: raise AssertionError('preview allowed outbound connection')
print('isolated')
'''
    env = {**os.environ, "LANGFUSE_SECRET_KEY": "sentinel-not-a-secret", "LANGFUSE_BASE_URL": "https://invalid.example"}
    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert "isolated" in result.stdout


def test_evaluation_readback_filters_exact_targets_and_never_invents_missing_scores():
    adapter, client = setup_client()
    state = session(client)
    turn = post_turn(client, state).json()
    path = f"/api/conversations/{state['session_id']}/evaluations/{turn['request_id']}"
    headers = {"X-Conversation-Token": state["token"]}
    empty = client.get(path, headers=headers).json()
    assert empty["status"] == "pending" and empty["received"] == 0 and empty["expected"] == 8
    definitions = score_definitions()
    for index in range(1, 9):
        definition = definitions[f"E-{index:02d}"]
        target = turn["root_observation_id"] if definition["subject"] == "user_input" else turn["generation_id"]
        adapter.score_rows.append(SimpleNamespace(id=str(index), name=definition["name"], observation_id=target, value=0.5, comment="Actual judge result"))
    adapter.score_rows.append(SimpleNamespace(id="unrelated", name="record_fidelity", observation_id="unrelated", value=1, comment="Wrong subject"))
    complete = client.get(path, headers=headers).json()
    assert complete["status"] == "complete" and complete["received"] == 8
    assert all(s["value"] == 0.5 for s in complete["scores"])
    adapter.fail_scores = True
    assert client.get(path, headers=headers).json()["status"] == "unavailable"


def test_concurrent_turn_is_rejected_without_interleaving_history():
    from synth.companion.service import ConversationError
    adapter = TestAdapter()
    service = ConversationService(adapter)
    state = service.new("PR-01")
    current = service.get(state["session_id"], state["token"])
    with current.lock:
        with pytest.raises(ConversationError) as error:
            service.turn(current.id, current.token, "question", "request-0001")
        assert error.value.status == 409
    assert not adapter.completions


def test_health_requires_current_project_active_rules_and_managed_prompts(monkeypatch):
    from synth.state import RunState
    from langfuse_synth_core.companion import ReadinessReport
    adapter = TestAdapter()
    adapter.readiness = lambda: ReadinessReport(True, True, {})
    state = SimpleNamespace(base_url=adapter.base_url, project_id="fixture-project",
                            evaluator_rules={f"E-{n:02d}": {"id": f"rule-{n}"} for n in range(1, 9)})
    monkeypatch.setattr(RunState, "load", classmethod(lambda cls: state))
    original_read = adapter.read_json
    disabled = set()
    def read(path, *args, **kw):
        if path.startswith("/api/public/v2/evaluation-rules/"):
            return {"enabled": path.rsplit("/", 1)[1] not in disabled}
        return original_read(path, *args, **kw)
    adapter.read_json = read
    client = TestClient(create_app(adapter))
    assert client.get("/healthz").status_code == 200
    disabled.add("rule-5")
    failed = client.get("/healthz")
    assert failed.status_code == 200 and failed.json()["ready"] is False and "disabled: E-05" in str(failed.json())
    disabled.clear()
    state.project_id = "another-project"
    assert client.get("/healthz").json()["ready"] is False
    state.project_id = "fixture-project"
    adapter.fail_prompt = True
    assert client.get("/healthz").json()["ready"] is False


def test_installed_sdk_compiles_managed_history_placeholder_without_losing_roles():
    from langfuse.api.prompts.types.prompt import Prompt_Chat
    from langfuse.model import ChatPromptClient
    from synth.assets import chat_prompt
    adapter, client = setup_client()
    fetch = adapter.get_prompt
    def managed_prompt(name, **kw):
        fixture = fetch(name, **kw)
        return ChatPromptClient(Prompt_Chat(name=name, version=fixture.version,
                                prompt=chat_prompt(fixture.pid, fixture.version),
                                config={}, labels=["production"], tags=[]))
    adapter.get_prompt = managed_prompt
    state = session(client)
    first = post_turn(client, state).json()
    second = post_turn(client, state, request_id="request-0002").json()
    assert first["status"] == second["status"] == "complete"
    assert len(adapter.completions[1]["messages"]) == 3
    assert "{{reference_context}}" not in adapter.completions[1]["system"]
    assert '"id": "SRC-01"' in adapter.completions[1]["system"]
    assert adapter.completions[1]["messages"][1] == {"role": "assistant", "content": first["reply"]}
    assert isinstance(adapter.observations[1].fields["prompt"], ChatPromptClient)


@pytest.mark.parametrize("version", [7, 9])
def test_four_turn_preview_conversation_keeps_version_voice_and_exact_context(version):
    adapter, client = setup_client(preview=True)
    adapter.versions["PR-01"] = version
    state = session(client)
    styled_turns = load_fixture("product")["conversation"]["turns"]
    plain_turns = next(c for c in load_fixture("conversations")["PR-01"]
                       if c["theme"] == "waiver")["turns"]
    history = []
    for index, authored in enumerate(styled_turns):
        response = post_turn(client, state, authored["user"], f"request-{index:04d}").json()
        expected = authored["assistant"] if version == 9 else plain_turns[index]["assistant_reply"]
        assert response["status"] == "complete"
        assert response["reply"] == expected
        assert response["prompt_version"] == version
        assert adapter.completions[index]["messages"] == [*history, {"role": "user", "content": authored["user"]}]
        root, generation = adapter.observations[index * 2:index * 2 + 2]
        for observation in (root, generation):
            assert observation.fields["input"]["current_user_message"] == authored["user"]
            assert observation.fields["input"]["prior_messages"] == history
        history.extend([{"role": "user", "content": authored["user"]},
                        {"role": "assistant", "content": expected}])
    assert len(adapter.prompt_fetches) == 4
