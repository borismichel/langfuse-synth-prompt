"""The accepted companion surface; native Langfuse pages remain native."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from html import escape
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langfuse_synth_core.companion import CompanionAdapter, parse_invocation
from langfuse_synth_core.companion.llm import LLMClient, resolve_provider
from langfuse_synth_core.live import paths
from pydantic import BaseModel, Field, field_validator

from synth.catalog import load_fixture, prompt_by_id
from .service import ConversationError, ConversationService

HEALTH_PATH = "/healthz"
REQUIRES_SECRETS = ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LLM_API_KEY")


class RoleModelAdapter(CompanionAdapter):
    """Keep provider transport in core; apply the kit's explicit per-role model.

    The legacy global LLM_MODEL pin cannot replace a requested role model. Model
    selection never mutates process environment or another request's client.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._role_clients = {}

    def llm(self, model=None):
        if model is None:
            return super().llm()
        provider = resolve_provider()
        if provider != "anthropic":
            raise ValueError("The configured role models require the Anthropic provider")
        if model not in self._role_clients:
            self._role_clients[model] = LLMClient(provider, model)
        return self._role_clients[model]


class NewConversation(BaseModel):
    prompt_id: Literal["PR-01", "PR-02", "PR-03"] = "PR-01"


class TurnRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    request_id: str = Field(min_length=8, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")


class FeedbackRequest(BaseModel):
    request_id: str
    value: Literal[0, 1]
    comment: str = Field(default="", max_length=1000)

    @field_validator("value", mode="before")
    @classmethod
    def exact_boolean_score(cls, value):
        if type(value) is not int or value not in (0, 1):
            raise ValueError("A thumbs rating must be the integer 0 or 1")
        return value


def create_app(adapter: CompanionAdapter, *, preview: bool = False) -> FastAPI:
    service = ConversationService(adapter, preview=preview)
    @asynccontextmanager
    async def lifespan(_app):
        yield
        await asyncio.to_thread(service.close)

    app = FastAPI(title="Everyday assistants", docs_url=None, redoc_url=None, lifespan=lifespan)
    app.state.service = service
    directory = Path(__file__).parent
    app.mount("/static", StaticFiles(directory=directory / "static"), name="static")

    @app.middleware("http")
    async def headers(request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        if preview:
            response.headers["X-Demo-Mode"] = "preview"
        return response

    @app.exception_handler(ConversationError)
    async def conversation_error(_request, exc):
        return JSONResponse({"detail": str(exc)}, status_code=exc.status)

    @app.get("/", response_class=HTMLResponse)
    def index():
        return (directory / "templates/index.html").read_text().replace("__BASE__", escape(paths.base_path(), quote=True)).replace("__PREVIEW__", str(preview).lower())

    @app.get("/api/catalog")
    def catalog():
        product = load_fixture("product")
        examples = load_fixture("examples")
        bots = []
        for pid in ("PR-01", "PR-02", "PR-03"):
            spec = prompt_by_id(pid)
            if pid == "PR-01":
                suggestions = [{"label": label, "message": turn["user"]} for label, turn in zip(
                    ["Monthly fee", "Correct the deposit", "Disagree with the reply", "Opening documents"], product["conversation"]["turns"])]
            else:
                case = next(c for c in examples["cases"] if c["prompt_id"] == pid)
                suggestions = [{"label": "Try a question", "message": case["input"]}, {"label": "Try the boundary", "message": case["control_input"]}]
            bots.append({"id": pid, "title": spec["title"], "suggestions": suggestions})
        return {"bots": bots, "preview": preview}

    @app.get("/api/connection")
    def connection():
        if preview:
            return {"ready": False, "mode": "preview", "gaps": ["Fixture preview: no live connections or evaluators."], "links": {}}
        report = adapter.readiness().as_dict()
        gaps = []
        prompts = {}
        links = {}
        if not report["ready"]:
            gaps.append("Langfuse write path or model client is unavailable.")
        try:
            links = {"portfolio": service.link("prompts"), "experiments": service.link("datasets"), "sessions": service.link("sessions")}
            for pid in ("PR-01", "PR-02", "PR-03"):
                p = adapter.langfuse().get_prompt(prompt_by_id(pid)["name"], label="production", cache_ttl_seconds=0, type="chat")
                prompts[pid] = p.version
        except Exception:
            gaps.append("The connected project or a managed production prompt is unavailable.")
        try:
            from synth.state import RunState
            state = RunState.load()
            if state.base_url.rstrip("/") != adapter.base_url:
                raise ValueError("Anchors target differs from runtime")
            if getattr(state, "project_id", None) != service.project_id():
                raise ValueError("Anchors project differs from runtime")
            rules = getattr(state, "evaluator_rules", {})
            missing = [f"E-{n:02d}" for n in range(1, 9) if not rules.get(f"E-{n:02d}")]
            if missing:
                gaps.append("Managed evaluator provisioning is missing: " + ", ".join(missing))
            else:
                for criterion in (f"E-{n:02d}" for n in range(1, 9)):
                    rule = adapter.read_json("/api/public/v2/evaluation-rules/" + rules[criterion]["id"])
                    if not rule.get("enabled"):
                        gaps.append("Managed evaluator rule is disabled: " + criterion)
        except Exception:
            gaps.append("Current-target evaluator provisioning receipt is unavailable.")
        return {**report, "ready": report["ready"] and not gaps, "gaps": gaps, "prompts": prompts, "links": links,
                "evaluation_notice": "Readiness checks configuration; actual evaluator execution is verified on each reply."}

    @app.get(HEALTH_PATH)
    def health():
        report = connection()
        return JSONResponse(report, status_code=503 if preview else 200)

    @app.post("/api/conversations")
    def new(request: NewConversation):
        return service.new(request.prompt_id)

    @app.post("/api/conversations/{sid}/turns")
    def turn(sid: str, request: TurnRequest, x_conversation_token: str = Header(default="")):
        return service.turn(sid, x_conversation_token, request.message, request.request_id)

    @app.post("/api/conversations/{sid}/feedback")
    def feedback(sid: str, request: FeedbackRequest, x_conversation_token: str = Header(default="")):
        return service.feedback(sid, x_conversation_token, request.request_id, request.value, request.comment)

    @app.get("/api/conversations/{sid}/evaluations/{request_id}")
    def evaluations(sid: str, request_id: str, x_conversation_token: str = Header(default="")):
        return service.evaluations(sid, x_conversation_token, request_id)

    return app


def main(argv: list[str] | None = None) -> int:
    from synth.config import load_config
    invocation = parse_invocation(argv)
    config = load_config(invocation.config)
    adapter = RoleModelAdapter(config, requires_secrets=REQUIRES_SECRETS,
                               health_path=HEALTH_PATH, llm_model_default=getattr(getattr(config, "live", None), "model", None))
    # Custom health reports story prerequisites, not merely process liveness.
    adapter.serve(create_app(adapter), host=invocation.host, port=invocation.port, mount_health=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
