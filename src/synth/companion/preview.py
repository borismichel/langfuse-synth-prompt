"""Isolated fixture preview of the same app; no credentials or outbound connections."""
from __future__ import annotations

import argparse
import os
import socket
from contextlib import contextmanager
from types import SimpleNamespace
from uuid import uuid4
from typing import Any

from langfuse_synth_core.companion import ReadinessReport
from langfuse_synth_core.companion.llm import ChatResult


class FixtureObservation:
    def __init__(self, adapter, *, root=False, trace_id=None, **fields):
        self.adapter = adapter
        self.trace_id = trace_id or uuid4().hex
        self.observation_id = uuid4().hex[:16]
        self.id = self.trace_id if root else self.observation_id
        self.fields = fields
        self.root = root
        adapter.observations.append(self)

    def update(self, **fields):
        self.fields.update(fields)
        return self

    @contextmanager
    def generation(self, name, **fields):
        generation = FixtureObservation(self.adapter, trace_id=self.trace_id, name=name,
                                        parent_id=self.observation_id, **fields)
        yield generation


class FixtureEmitter:
    def __init__(self, adapter):
        self.adapter = adapter

    @contextmanager
    def trace(self, name, **fields):
        root = FixtureObservation(self.adapter, root=True, name=name, **fields)
        yield root

    def score(self, name, value, **fields):
        if self.adapter.fail_feedback:
            raise RuntimeError("Fixture feedback failure")
        self.adapter.feedback[fields["score_id"]] = {"name": name, "value": value, **fields}

    def flush(self):
        pass


class FixturePrompt:
    def __init__(self, pid, version):
        self.pid = pid
        self.version = version
        self.is_fallback = False

    def compile(self, *, reference_context, conversation_history, user_message):
        from synth.catalog import system_prompt
        return [{"role": "system", "content": system_prompt(self.pid, self.version)},
                {"role": "system", "content": "Reference context: " + reference_context},
                *conversation_history, {"role": "user", "content": user_message}]


class FixtureAdapter:
    """Explicit local fixtures. It never inherits or constructs a real client."""
    is_fixture = True
    base_url = "https://fixture.invalid"
    health_path = "/healthz"

    def __init__(self):
        self.versions = {"PR-01": 7, "PR-02": 7, "PR-03": 7}
        self.observations = []
        self.feedback = {}
        self.prompt_fetches = []
        self.completions = []
        self.fail_model = False
        self.fail_prompt = False
        self.fail_feedback = False
        self.fail_scores = False
        self.score_rows = []

    def readiness(self):
        return ReadinessReport(False, False, {"mode": "preview", "admission": False})

    def read_json(self, path, params=None, *, throttle=0):
        if path == "/api/public/projects":
            return {"data": [{"id": "fixture-project"}]}
        raise NotImplementedError("No preview fixture for " + path)

    def langfuse(self):
        return self

    def get_prompt(self, name, *, label, cache_ttl_seconds, type):
        from synth.catalog import load_fixture
        self.prompt_fetches.append({"name": name, "label": label, "ttl": cache_ttl_seconds, "type": type})
        if self.fail_prompt:
            raise RuntimeError("Fixture prompt failure")
        if label != "production" or cache_ttl_seconds != 0 or type != "chat":
            raise ValueError("Preview exercises the exact managed production fetch contract")
        pid = next(p["id"] for p in load_fixture("portfolio")["prompts"] if p["name"] == name)
        return FixturePrompt(pid, self.versions[pid])

    def emitter(self, **kw):
        return FixtureEmitter(self)

    def llm(self, model=None):
        return SimpleNamespace(model="fixture/no-model", provider="fixture", complete=self.complete)

    def complete(self, *, system, messages, temperature, max_tokens):
        from synth.catalog import load_fixture
        self.completions.append({"system": system, "messages": messages})
        if self.fail_model:
            raise RuntimeError("Fixture provider failure")
        user = messages[-1]["content"]
        product = load_fixture("product")
        styled = "Speaking style: use a recognisable theatrical space-villain voice" in system
        # SESSION-01 wording differs slightly from the plain historical waiver case.
        # Both are accepted fixture records: resolve the same semantic turn by index,
        # while retaining the actual request wording/history in instrumentation.
        plain_turns = next(c for c in load_fixture("conversations")["PR-01"]
                           if c["theme"] == "waiver")["turns"]
        for index, turn in enumerate(product["conversation"]["turns"]):
            if turn["user"] == user:
                reply = turn["assistant"] if styled else plain_turns[index]["assistant_reply"]
                return ChatResult(reply, 0, 0)
        for case in product["cases"]:
            if case["input"]["user_message"] == user:
                return ChatResult(case["candidate_output"] if styled else case["baseline_output"], 0, 0)
        for case in load_fixture("examples")["cases"]:
            if case["input"] == user:
                return ChatResult(case["expected_output"], 0, 0)
            if case["control_input"] == user:
                return ChatResult(case["control_output"], 0, 0)
        raise ValueError("Preview supports the displayed authored suggestions only")

    def reader(self, **kw):
        return self

    def scores(self, **kw):
        if self.fail_scores:
            raise RuntimeError("Fixture score read failure")
        return self.score_rows

    def serve(self, app, *, host, port):
        if host != "127.0.0.1":
            raise ValueError("Preview binds only to loopback")
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level="warning")


def _deny_connection(*args: Any, **kwargs: Any):
    from langfuse_synth_core.authoring.egress import EgressBlockedError
    raise EgressBlockedError("Preview permits no outgoing connections, including loopback")


def create_preview_app():
    """Permanently isolates this process. Use a fresh process for any live work."""
    keep = {key: value for key, value in os.environ.items()
            if key in ("PATH", "SYSTEMROOT", "TMPDIR", "TEMP", "TMP", "LANG", "LC_ALL")}
    os.environ.clear()
    os.environ.update(keep)
    from langfuse_synth_core.authoring.egress import install_guard
    install_guard()
    socket.create_connection = _deny_connection
    socket.socket.connect = _deny_connection
    socket.socket.connect_ex = _deny_connection
    from .app import create_app
    return create_app(FixtureAdapter(), preview=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Isolated fixture preview, not live readiness")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535")
    app = create_preview_app()
    print(f"Fixture preview: http://127.0.0.1:{args.port} — no model or Langfuse connection", flush=True)
    FixtureAdapter().serve(app, host="127.0.0.1", port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
