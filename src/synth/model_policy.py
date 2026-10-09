"""Shared model selection and base provider prices for the demo.

Only authored history applies the explicit synthetic cost multiplier. Live calls
and model registry definitions retain provider prices and actual token usage.
"""
from __future__ import annotations

from importlib.resources import files
from copy import deepcopy
import json


def load_model_policy() -> dict:
    """Return an independent copy for runtime consumers and prototype export."""
    return json.loads(files("synth.fixtures").joinpath("model_policy.json").read_text())


_POLICY = load_model_policy()
MODEL_BY_PROMPT = _POLICY["model_by_prompt"]
MODEL_PRICES = {model: (prices["input_per_million"], prices["output_per_million"])
                for model, prices in _POLICY["models"].items()}
EXPERIMENT_MODEL = _POLICY["experiment_model"]
EVALUATION_MODEL = _POLICY["evaluation_model"]
SYNTHETIC_COST_MULTIPLIER = _POLICY["synthetic_cost_multiplier"]
MODEL_POLICY_REVISION = _POLICY["revision"]


def authored_cost_details(model: str, usage: dict) -> dict:
    """Synthetic demo accounting only; never use this for a paid model response."""
    input_rate, output_rate = MODEL_PRICES[model]
    input_cost = usage["input"] * input_rate * SYNTHETIC_COST_MULTIPLIER / 1_000_000
    output_cost = usage["output"] * output_rate * SYNTHETIC_COST_MULTIPLIER / 1_000_000
    return {"input": input_cost, "output": output_cost, "total": input_cost + output_cost}


def apply_model_policy(events: list[dict]) -> list[dict]:
    """Rewrite authored spool accounting without touching payloads or identities.

    A live generation is rejected even when its environment looks historical.
    Existing usage must explicitly declare that it is synthetic. Non-generation
    records pass through unchanged. This is suitable for local migration plans.
    """
    from langfuse_synth_core.seed import otlp
    from .receipt import attributes

    result = deepcopy(events)
    prefix = "langfuse.observation.metadata."
    for event in result:
        if not otlp.is_span(event):
            continue
        attrs = attributes(event)
        if attrs.get(otlp.OBS_TYPE) != "generation":
            continue
        synthetic = attrs.get(prefix + "synthetic_usage")
        if isinstance(synthetic, str):
            synthetic = json.loads(synthetic)
        environment = attrs.get("langfuse.environment")
        if synthetic is not True or environment not in ("production-history", "production", "experiment"):
            raise ValueError("Model policy rewriting requires explicitly synthetic history generations")
        prompt_id = attrs.get(prefix + "prompt_id")
        # Metadata may be a plain string or a JSON string on the OTLP wire.
        if isinstance(prompt_id, str) and prompt_id.startswith('"'):
            prompt_id = json.loads(prompt_id)
        if prompt_id not in MODEL_BY_PROMPT:
            raise ValueError("Model policy rewriting requires a known prompt ID")
        model = EXPERIMENT_MODEL if environment == "experiment" else MODEL_BY_PROMPT[prompt_id]
        usage = json.loads(attrs["langfuse.observation.usage_details"])
        if any(isinstance(usage.get(key), bool) or not isinstance(usage.get(key), (int, float))
               or usage[key] < 0 for key in ("input", "output")):
            raise ValueError("Model policy rewriting requires nonnegative input/output usage")
        updates = {
            "langfuse.observation.model.name": model,
            "langfuse.observation.cost_details": json.dumps(authored_cost_details(model, usage), separators=(",", ":")),
            prefix + "synthetic_pricing": "true",
            prefix + "synthetic_cost_multiplier": json.dumps(SYNTHETIC_COST_MULTIPLIER),
            prefix + "cost_basis": "synthetic-demo-provider-price-multiple",
            prefix + "model_policy_revision": MODEL_POLICY_REVISION,
        }
        event["attributes"] = [otlp.string_attr(attr["key"], updates.pop(attr["key"]))
                               if attr["key"] in updates else attr for attr in event["attributes"]]
        event["attributes"].extend(otlp.string_attr(key, value) for key, value in updates.items())
    return result
