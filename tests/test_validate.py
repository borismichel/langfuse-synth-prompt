"""The scaffolded `usecase.yaml` passes `synth-authoring validate` with no edits.

Runs the same importable validator the portal uses at sync time, so "green here" ==
"passes portal sync" by construction. Skips on a bare install without the [authoring]
extra (which ships the validator).
"""
import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("jsonschema") is None,
    reason="validate ships in langfuse-synth-core[authoring]; install the [dev] extra to run it",
)

MANIFEST = Path(__file__).resolve().parent.parent / "usecase.yaml"


def test_manifest_is_valid():
    from langfuse_synth_core.authoring.validate import validate_path

    errors = validate_path(MANIFEST)
    assert errors == [], "usecase.yaml is invalid:\n" + "\n".join(errors)


def test_manifest_exposes_the_canonical_volume_knob():
    import yaml

    doc = yaml.safe_load(MANIFEST.read_text())
    props = doc["config_schema"]["properties"]
    assert "generation.target_traces" in props
    assert props["generation.target_traces"]["type"] == "integer"
    assert set(props) == {"generation.seed", "generation.target_traces",
                          "evaluation.provider", "evaluation.model"}


def test_depot_model_defaults_match_original_provider_ids_and_runtime_policy():
    import yaml
    from synth.model_policy import EVALUATION_MODEL, EXPERIMENT_MODEL, MODEL_BY_PROMPT

    doc = yaml.safe_load(MANIFEST.read_text())
    config = yaml.safe_load((MANIFEST.parent / doc["base_config"]["default"]).read_text())
    props = doc["config_schema"]["properties"]
    assert doc["llm"]["providers"] == ["anthropic"]
    assert props["evaluation.provider"]["default"] == config["evaluation"]["provider"] == "anthropic"
    assert props["evaluation.model"]["default"] == config["evaluation"]["model"] == EVALUATION_MODEL == "claude-sonnet-5-5"
    assert config["live"]["model"] == EXPERIMENT_MODEL == "claude-sonnet-5-5"
    assert set(MODEL_BY_PROMPT.values()) == {"claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1"}
    sample = dict(line.split("=", 1) for line in (MANIFEST.parent / ".env.example").read_text().splitlines()
                  if line and not line.startswith("#"))
    assert sample["LLM_PROVIDER"] == "anthropic" and "ANTHROPIC_API_KEY" in sample
    assert "OPENAI_API_KEY" not in sample
    assert sample["LLM_MODEL"] == EXPERIMENT_MODEL
    assert sample["LANGFUSE_EVAL_PROVIDER"] == "anthropic"
    assert sample["LANGFUSE_EVAL_MODEL"] == EVALUATION_MODEL
