"""Accepted authored assets shared by historical generation and live adapters.

Expected scores are calibration labels, never a replacement for live judges.
The fixture files preserve accepted packet bytes; adapters return independent copies.
"""
from __future__ import annotations

import json
from importlib.resources import files
from typing import Any
from .scores import outcome_values


def load_fixture(name: str) -> Any:
    if name not in {"portfolio", "product", "examples", "dataset_extras", "prompt_versions", "score_definitions", "conversations"}:
        raise ValueError(f"Unknown fixture: {name}")
    return json.loads(files("synth.fixtures").joinpath(f"{name}.json").read_text())


def prompt_by_id(prompt_id: str) -> dict:
    for prompt in load_fixture("portfolio")["prompts"]:
        if prompt["id"] == prompt_id:
            return prompt
    raise ValueError(f"Unknown prompt: {prompt_id}")


def system_prompt(prompt_id: str, version: int) -> str:
    """Return real version-specific text; candidate 9 is only available for live creation."""
    prompt_by_id(prompt_id)
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("Prompt version must be an integer")
    if prompt_id == "PR-01" and version == 9:
        return load_fixture("product")["prompt_comparison"]["candidate_system"]
    try:
        return load_fixture("prompt_versions")[prompt_id][str(version)]
    except KeyError as exc:
        raise ValueError(f"No authored {prompt_id} version {version}") from exc


def score_definitions() -> dict[str, dict]:
    return load_fixture("score_definitions")


def rubric_revisions(prompt_id: str, *, subject: str | None = None) -> dict[str, str]:
    """Actual applicable criterion revisions, optionally scoped to a score target."""
    definitions = score_definitions()
    return {eid: definitions[eid]["revision"]
            for eid in sorted(prompt_by_id(prompt_id)["evaluation_ids"])
            if subject is None or definitions[eid]["subject"] == subject}


def decode_rubric_revisions(value) -> dict[str, str] | None:
    """Normalize supported readback JSON without accepting corrupted Python repr."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return None
    if not isinstance(value, dict) or not all(isinstance(key, str) and isinstance(revision, str)
                                              for key, revision in value.items()):
        return None
    return value


def dataset_items(prompt_id: str) -> list[dict]:
    """The eight main cases or a normal/control/missing-information secondary triple."""
    prompt = prompt_by_id(prompt_id)
    product = load_fixture("product")
    result = []

    def item(case_id, question, source, answer, scores, history=(), **extra):
        return {"case_id": case_id, "input": {"reference_context": source,
                "conversation_history": list(history), "user_message": question},
                "expected_output": answer, "metadata": {
                    "prompt_id": prompt_id, "dataset_id": prompt["dataset_id"],
                    "dataset_version": "r1", "source_id": extra.pop("source_id", "SRC-01"),
                    "evidence_kind": "authored-calibration-labels", "expected_scores": outcome_values(scores), **extra}}

    if prompt_id == "PR-01":
        for case in product["cases"]:
            result.append(item(case["id"], case["input"]["user_message"], product["source"],
                case["baseline_output"], case["expected_baseline_scores"],
                case["input"]["conversation_history"], source_id=case["source_id"],
                purpose=case["purpose"], candidate_output=case["candidate_output"],
                expected_candidate_scores=outcome_values(case["expected_candidate_scores"])))
        return result
    case = next(c for c in load_fixture("examples")["cases"] if c["prompt_id"] == prompt_id)
    source = case.get("source", product["source"])
    scores = dict(case["expected_scores"])
    if prompt["live_companion"]:
        scores.update({f"E-{i:02}": 0 for i in range(5, 9)})
    result.append(item(case["id"], case["input"], source, case["expected_output"], scores,
                       source_id=case["source_id"], kind="normal"))
    result.append(item(case["id"] + "-CTRL", case["control_input"], case.get("control_source", source),
                       case["control_output"], dict(scores), source_id=case["source_id"], kind="boundary-control"))
    extra = next(c for c in load_fixture("dataset_extras") if c["prompt_id"] == prompt_id)
    extra_scores = dict(extra["expected_scores"])
    if prompt["live_companion"]:
        extra_scores.update({f"E-{i:02}": 0 for i in range(5, 9)})
    result.append(item(extra["id"], extra["input"], extra["source"], extra["expected_output"], extra_scores,
                       source_id=extra["source_id"], kind=extra["kind"]))
    return result


def calibration_cases() -> list[dict]:
    """Negative controls remain outside historical/experiment result claims."""
    cases = {item["case_id"]: item for item in dataset_items("PR-01")}
    result = []
    for control in load_fixture("product")["negative_controls"]:
        case = cases[control["case_id"]]
        result.append({**case, "case_id": control["id"], "expected_output": control["output"],
                       "metadata": {**case["metadata"], "origin_case_id": control["case_id"],
                                    "expected_scores": outcome_values(control["expected"]), "reason": control["reason"],
                                    "cohort": "calibration-control"}})
    return result


def historical_experiment_cases() -> list[dict]:
    """Fixed v2/v4 authored results for native dataset-run provisioning, outside history."""
    result = []
    for prompt in load_fixture("portfolio")["prompts"]:
        case = dataset_items(prompt["id"])[0]
        for version in (2, 4):
            result.append({**case, "prompt_id": prompt["id"], "prompt_version": version,
                           "metadata": {**case["metadata"], "cohort": "experiment",
                                        "execution_kind": "authored-historical-experiment",
                                        "live_judge_executed": False}})
    return result
