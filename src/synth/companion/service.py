"""Live prompt-first conversations, independent of HTTP and seed generation.

The adapter owns credentials and transport. Only interactive turns call the model.
Runtime conversations are ephemeral; Langfuse is the durable observation/score store.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import threading
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote
from uuid import uuid4

from synth.scores import read_score_value, CATEGORIES
from synth.catalog import load_fixture, prompt_by_id, score_definitions, rubric_revisions
from synth.reference_tools import (
    CHAT_OPERATION_NAME, GENERATION_OPERATION_NAME, REFERENCE_RETRIEVER_NAME, FEE_TOOL_NAME,
    reference_arguments, validate_reference, fee_arguments, calculate_fee, generation_reference,
)

LIVE_ENVIRONMENT = "prompt-live"


class ConversationError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


@dataclass
class Conversation:
    id: str
    token: str
    prompt_id: str
    turns: list[dict] = field(default_factory=list)
    touched: float = field(default_factory=time.monotonic)
    lock: Any = field(default_factory=threading.Lock)


class ConversationService:
    def __init__(self, adapter: Any, *, preview: bool = False):
        if preview != bool(getattr(adapter, "is_fixture", False)):
            raise ValueError("Preview requires the explicit fixture adapter")
        self.adapter = adapter
        self.preview = preview
        self.sessions: dict[str, Conversation] = {}
        self.lock = threading.Lock()
        self._project_id: str | None = None
        self._emitter = None

    def emitter(self):
        if self._emitter is None:
            self._emitter = self.adapter.emitter(environment=LIVE_ENVIRONMENT)
        return self._emitter

    def close(self):
        if self._emitter is not None and hasattr(self._emitter, "shutdown"):
            self._emitter.shutdown()

    def project_id(self) -> str:
        if self._project_id is None:
            projects = self.adapter.read_json("/api/public/projects").get("data", [])
            if len(projects) != 1 or not projects[0].get("id"):
                raise ConversationError("The connected project could not be resolved.", 503)
            self._project_id = projects[0]["id"]
        return self._project_id

    def link(self, path: str) -> str | None:
        if self.preview:
            return None
        return f"{self.adapter.base_url}/project/{quote(self.project_id(), safe='')}/{path}"

    def new(self, prompt_id: str) -> dict:
        if prompt_id not in ("PR-01", "PR-02", "PR-03"):
            raise ConversationError("Choose one of the three connected assistants.")
        with self.lock:
            now = time.monotonic()
            for sid, old in list(self.sessions.items()):
                if now - old.touched > 86400 and not old.lock.locked():
                    del self.sessions[sid]
            if len(self.sessions) >= 1000:
                raise ConversationError("Conversation capacity reached; try again later.", 503)
            session = Conversation("prompt-live-" + uuid4().hex, secrets.token_urlsafe(32), prompt_id)
            self.sessions[session.id] = session
        return {"session_id": session.id, "token": session.token, "prompt_id": prompt_id}

    def get(self, sid: str, token: str) -> Conversation:
        with self.lock:
            session = self.sessions.get(sid)
        if session is None or not secrets.compare_digest(session.token, token):
            raise ConversationError("Conversation expired or unavailable. Start a new conversation.", 404)
        session.touched = time.monotonic()
        return session

    def turn(self, sid: str, token: str, message: str, request_id: str) -> dict:
        session = self.get(sid, token)
        message = message.strip()
        if not message:
            raise ConversationError("Write a message first.")
        if not session.lock.acquire(blocking=False):
            raise ConversationError("A reply is already in progress in this conversation.", 409)
        try:
            previous = next((t for t in session.turns if t["request_id"] == request_id), None)
            if previous:
                if previous["user"] != message:
                    raise ConversationError("This request identifier already belongs to another message.", 409)
                return previous
            if len(session.turns) >= 40:
                raise ConversationError("Start a fresh conversation after 40 turns.", 409)
            record = self._run(session, message, request_id)
            session.turns.append(record)
            return record
        finally:
            session.lock.release()

    def _run(self, session: Conversation, message: str, request_id: str) -> dict:
        spec = prompt_by_id(session.prompt_id)
        history = []
        for turn in session.turns:
            if turn["status"] == "complete":
                history.extend([{"role": "user", "content": turn["user"]},
                                {"role": "assistant", "content": turn["reply"]}])
        context = {"current_user_message": message, "prior_messages": history}
        root_input = {"messages": [{"role": "user", "content": message}]}
        metadata = {"kit": "prompt", "evidence_kind": "live" if not self.preview else "fixture",
                    "application_id": spec["application_id"], "prompt_id": session.prompt_id,
                    "prompt_name": spec["name"], "rubric_revisions": rubric_revisions(session.prompt_id, subject="user_input"),
                    "evaluation_subject": "user_input", "request_id": request_id, **context}
        record = {"request_id": request_id, "session_id": session.id, "user": message,
                  "reply": "", "status": "failed", "prompt_name": spec["name"],
                  "prompt_version": None, "trace_id": None, "root_observation_id": None,
                  "generation_id": None, "evaluation_status": "pending", "preview": self.preview}
        try:
            emitter = self.emitter()
            # SDK propagation stringifies dicts with Python repr; ingestion also
            # lets trace metadata win same-name observation keys. Keep the trace
            # inventory separate and valid JSON, never overwriting scoped maps.
            with emitter.trace(CHAT_OPERATION_NAME, session_id=session.id,
                               environment=LIVE_ENVIRONMENT, tags=["prompt", "live", session.prompt_id],
                               input=root_input, metadata={**{k: metadata[k] for k in ("kit", "evidence_kind", "application_id", "prompt_id", "prompt_name", "request_id")},
                                                          "trace_rubric_revisions": json.dumps(rubric_revisions(session.prompt_id), sort_keys=True)}) as root:
                root.update(metadata=metadata)
                record.update(trace_id=root.id, root_observation_id=root.observation_id)
                try:
                    # These are application actions, not model-selected tool calls.
                    arguments = reference_arguments(session.prompt_id)
                    with root.observation(REFERENCE_RETRIEVER_NAME, as_type="retriever", input=arguments,
                                          metadata={"invocation": "application", "source_id": arguments["source_id"],
                                                    "source": "local-product-catalog"}) as retriever:
                        try:
                            reference = validate_reference(load_fixture("product")["source"], arguments)
                            retriever.update(output=reference)
                        except Exception as exc:
                            retriever.update(level="ERROR", status_message=type(exc).__name__)
                            raise
                    calculation = fee_arguments(session.prompt_id, message, reference)
                    result = None
                    if calculation is not None:
                        with root.observation(FEE_TOOL_NAME, as_type="tool", input=calculation,
                                              metadata={"invocation": "application", "source_id": reference["id"]}) as tool:
                            try:
                                result = calculate_fee(calculation)
                                tool.update(output=result)
                            except Exception as exc:
                                tool.update(level="ERROR", status_message=type(exc).__name__)
                                raise
                    model_reference = generation_reference(reference, calculation, result)
                    context = {**context, "reference_context": reference}
                    metadata = {**metadata, **context}
                    root.update(metadata=metadata)
                    # No cache/fallback: each request resolves the real production label.
                    prompt = self.adapter.langfuse().get_prompt(
                        spec["name"], label="production", cache_ttl_seconds=0, type="chat")
                    if getattr(prompt, "is_fallback", False):
                        raise ValueError("Managed prompt fallback is not permitted")
                    compiled = prompt.compile(reference_context=json.dumps(model_reference, ensure_ascii=False),
                                              conversation_history=history, user_message=message)
                    if not isinstance(compiled, list) or not compiled:
                        raise ValueError("Production must be a managed chat prompt")
                    system_parts = [m["content"] for m in compiled if m.get("role") == "system"]
                    messages = [m for m in compiled if m.get("role") != "system"]
                    if not system_parts or not messages or any(m.get("role") not in ("user", "assistant") for m in messages):
                        raise ValueError("Managed chat prompt has unsupported conversation roles")
                    system_with_reference = "\n\n".join(system_parts)
                    record["prompt_version"] = prompt.version
                    metadata = {**metadata, "prompt_version": prompt.version}
                    root.update(metadata=metadata)
                    # Core provider seam takes one system string; these are its exact inputs.
                    model_messages = [{"role": "system", "content": system_with_reference}, *messages]
                    llm = self.adapter.llm()
                    generation_metadata = {**metadata, "evaluation_subject": "assistant_reply",
                                           "rubric_revisions": rubric_revisions(session.prompt_id, subject="assistant_reply")}
                    if calculation is not None:
                        generation_metadata["calculation_results"] = model_reference["calculation_results"]
                    with root.generation(GENERATION_OPERATION_NAME, model=llm.model, prompt=prompt,
                                         input={"messages": model_messages},
                                         model_parameters={"max_tokens": 700, **({"temperature": 0} if llm.provider == "openai" else {})},
                                         metadata=generation_metadata) as generation:
                        record["generation_id"] = generation.id
                        try:
                            result = llm.complete(system=system_with_reference, messages=messages,
                                                  temperature=0, max_tokens=700)
                            if not result.text.strip():
                                raise ValueError("The provider returned no text")
                            output = [{"role": "assistant", "content": result.text}]
                            generation.update(output=output, usage_details={"input": result.input_tokens, "output": result.output_tokens})
                            root.update(output=output)
                            record.update(reply=result.text, status="complete", model=llm.model,
                                          usage={"input": result.input_tokens, "output": result.output_tokens})
                        except Exception as exc:
                            generation.update(level="ERROR", status_message=type(exc).__name__)
                            raise
                except Exception as exc:
                    root.update(level="ERROR", status_message=type(exc).__name__,
                                output={"error": "The reply could not be completed.", "error_type": type(exc).__name__})
                    record.update(error="The reply could not be completed. Inspect the request or try a new message.",
                                  error_type=type(exc).__name__, evaluation_status="unavailable")
        except Exception as exc:
            # Never turn telemetry transport failures into a fictional successful delivery.
            record.update(error="The request could not be confirmed in Langfuse.", error_type=type(exc).__name__,
                          evaluation_status="unavailable", delivery_status="unconfirmed")
            if not record["reply"]:
                record["status"] = "failed"
        try:
            record["session_url"] = self.link("sessions/" + quote(session.id, safe=""))
            record["trace_url"] = self.link("traces/" + str(record["trace_id"])) if record["trace_id"] else None
            record["observation_url"] = (record["trace_url"] + "?observation=" + record["generation_id"]) if record.get("trace_url") and record["generation_id"] else None
        except Exception:
            record.update(session_url=None, trace_url=None, observation_url=None)
        return record

    def feedback(self, sid: str, token: str, request_id: str, value: int, comment: str) -> dict:
        session = self.get(sid, token)
        with session.lock:
            record = next((t for t in session.turns if t["request_id"] == request_id), None)
            if not record or record["status"] != "complete" or not record["root_observation_id"]:
                raise ConversationError("Feedback requires a completed reply in this conversation.", 404)
            score_id = hashlib.sha256((record["root_observation_id"] + ":user-helpfulness").encode()).hexdigest()[:32]
            try:
                emitter = self.emitter()
                emitter.score("user-helpfulness", value, trace_id=record["trace_id"],
                              observation_id=record["root_observation_id"], data_type="BOOLEAN",
                              comment=comment, score_id=score_id,
                              metadata={"origin": "companion-feedback", "subject": "request_root"})
                emitter.flush()
            except Exception:
                raise ConversationError("Feedback could not be delivered. Please try again.", 502) from None
            record["feedback"] = {"value": value, "comment": comment, "score_id": score_id}
            return {**record["feedback"], "observation_id": record["root_observation_id"],
                    "status": "fixture" if self.preview else "submitted"}

    def evaluations(self, sid: str, token: str, request_id: str) -> dict:
        session = self.get(sid, token)
        record = next((t for t in session.turns if t["request_id"] == request_id), None)
        if not record:
            raise ConversationError("Reply unavailable.", 404)
        if self.preview:
            return {"status": "fixture", "scores": [], "message": "Preview does not run evaluators."}
        if record["status"] != "complete":
            return {"status": "unavailable", "scores": [], "message": "Reply generation failed."}
        try:
            rows = self.adapter.reader().scores(trace_id=record["trace_id"], limit_pages=2)
        except Exception:
            return {"status": "unavailable", "scores": [], "message": "Score readback is unavailable; inspect native evaluation logs."}
        definitions = score_definitions()
        expected = {(definitions[e]["name"], record["root_observation_id"] if definitions[e]["subject"] == "user_input" else record["generation_id"]): definitions[e]
                    for e in prompt_by_id(session.prompt_id)["evaluation_ids"]}
        actual = {}
        invalid = False
        for row in rows:
            key = (row.name, row.observation_id)
            if key in expected:
                definition = expected[key]
                if row.data_type != definition["data_type"] or (row.data_type == "CATEGORICAL" and read_score_value(row) not in CATEGORIES):
                    invalid = True
                    continue
                if key in actual:
                    invalid = True
                    continue
                actual[key] = {"id": row.id, "name": row.name, "value": read_score_value(row), "data_type": row.data_type,
                               "comment": row.comment, "observation_id": row.observation_id}
        return {"status": "invalid" if invalid else "complete" if len(actual) == len(expected) else "pending",
                "scores": list(actual.values()), "received": len(actual), "expected": len(expected),
                "message": "Unexpected score type, category, or duplicate; inspect native evaluation logs." if invalid else "Missing outcomes may be queued or failed; inspect native evaluation logs." if len(actual) < len(expected) else "Actual evaluator outcomes received."}
