"""Typed, retargetable kit configuration. Secrets come only from the environment."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from langfuse_synth_core.config import load_config as _load_config
from langfuse_synth_core.derivation import identity_derivation
from langfuse_synth_core.timegen import parse_as_of_date
from synth.model_policy import EVALUATION_MODEL, EXPERIMENT_MODEL

@dataclass
class Target:
    host: str = 'http://localhost:3000'
    project_hint: str = 'demo'

    @property
    def base_url(self) -> str:
        return os.environ.get('LANGFUSE_BASE_URL', self.host).rstrip('/')

@dataclass
class Generation:
    seed: int = 42
    target_traces: int = 1620
    as_of_date: date | None = None

@dataclass
class Evaluation:
    # This is a provider connection name already configured in Langfuse, not a key.
    provider: str = ''
    model: str = EVALUATION_MODEL

@dataclass
class Live:
    model: str = EXPERIMENT_MODEL

@dataclass
class Verification:
    timeout_seconds: int = 90
    poll_seconds: float = 3

@dataclass
class Config:
    target: Target
    generation: Generation
    evaluation: Evaluation = field(default_factory=Evaluation)
    live: Live = field(default_factory=Live)
    verification: Verification = field(default_factory=Verification)


def _model_factory(raw: dict) -> Config:
    raw = raw or {}
    target, generation = raw.get('target') or {}, raw.get('generation') or {}
    evaluation, live = raw.get('evaluation') or {}, raw.get('live') or {}
    verification = raw.get('verification') or {}
    count = int(generation.get('target_traces', 1620))
    seed = int(generation.get('seed', 42))
    if not 1 <= count <= 100000 or seed < 0:
        raise ValueError('target_traces must be 1..100000 and seed must be non-negative')
    return Config(
        Target(str(target.get('host', 'http://localhost:3000')), str(target.get('project_hint', 'demo'))),
        Generation(seed, count, parse_as_of_date(generation.get('as_of_date'))),
        Evaluation(os.environ.get('LANGFUSE_EVAL_PROVIDER', str(evaluation.get('provider', ''))),
                   os.environ.get('LANGFUSE_EVAL_MODEL', str(evaluation.get('model') or EVALUATION_MODEL))),
        Live(os.environ.get('LLM_MODEL', str(live.get('model') or EXPERIMENT_MODEL))),
        Verification(max(0, min(300, int(verification.get('timeout_seconds', 90)))),
                     max(.1, min(10, float(verification.get('poll_seconds', 3))))),
    )


def load_config(path: str | Path, overrides: list[str] | None = None) -> Config:
    return _load_config(path, _model_factory, overrides)

DERIVATION_HOOK = identity_derivation
