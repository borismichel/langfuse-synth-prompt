"""Model-free preflight: core owns target probing; the kit owns volume planning."""
from __future__ import annotations

import json

from langfuse_synth_core.probe import run_backdate_probe

from .catalog import historical_experiment_cases, score_definitions
from .config import Config
from .materialize import WINDOW_DAYS, population_plan
from .model_policy import MODEL_POLICY_REVISION, SYNTHETIC_COST_MULTIPLIER


def run_probe(cfg: Config, *, log=print) -> bool:
    """Write two throwaway observations and verify backdating through core's v4 reader.

    This intentionally changes the target project, but never touches the seed spool
    or receipt. Core guards the demo project and uses fresh probe IDs on every run.
    """
    return run_backdate_probe(
        cfg.target.base_url, cfg.target.project_hint, cfg.generation.seed,
        window_days=WINDOW_DAYS, name="prompt.probe.backdate_check",
        environment="synth-probe", tags=("synth-probe", "prompt"), log=log,
    )


def build_plan(cfg: Config) -> dict:
    """Calculate the seed's v4 volume without materializing or writing its spool.

    The historical population calculator follows the same seeded template choices
    as generation, including conditional fee tools. Experiments form a fixed cohort.
    Trace IDs group observations; adding traces to billable units would count roots
    twice. Dataset rows and experiment links are REST assets, not billable events.
    """
    history = population_plan(cfg.generation.target_traces, {"seed": cfg.generation.seed})
    cases, definitions = historical_experiment_cases(), score_definitions()
    experiments = {
        "traces": len(cases), "observations": 2 * len(cases), "generations": len(cases),
        "scores": sum(definitions[eid]["subject"] == "assistant_reply"
                      for case in cases for eid in case["metadata"]["expected_scores"]),
    }
    production = {"traces": history["target_traces"], "observations": history["observations"],
                  "generations": history["generations"], "scores": history["outcomes"]}
    total = {key: production[key] + experiments[key] for key in production}
    total["billable_units"] = total["observations"] + total["scores"]
    return {
        "schema_version": 1,
        "seed": cfg.generation.seed,
        "target_traces": cfg.generation.target_traces,
        "production_history": production,
        "historical_experiments": experiments,
        "seed_total": total,
        "probe": {"traces": 1, "observations": 2, "scores": 0, "billable_units": 2},
        "cost": {
            "seed_provider_calls": 0, "seed_model_usd": 0,
            "langfuse_ingestion_usd": None,
            "langfuse_ingestion_basis": "Account-specific pricing is not supplied; use the billable units above.",
            "displayed_model_cost": {
                "basis": "Authored synthetic accounting, not incurred provider spend",
                "multiplier": SYNTHETIC_COST_MULTIPLIER,
                "policy_revision": MODEL_POLICY_REVISION,
            },
            "excluded": "Model validation during evaluator setup, future live chats, real experiments and managed evaluations; these depend on actual execution.",
        },
    }


def run_plan(cfg: Config, *, log=print) -> dict:
    result = build_plan(cfg)
    total = result["seed_total"]
    # Depot's parse.event_count is a raw trace count used by its generic advisory
    # estimator, not a place for billable units. PLAN_COUNTS carries exact v4 counts.
    log(f"total_traces: {total['traces']}")
    log("PLAN_COUNTS=" + json.dumps(
        {"version": 1, **{key: total[key] for key in ("traces", "observations", "scores")}},
        separators=(",", ":"),
    ))
    log(f"billable_units: {total['billable_units']} (observations + scores; roots included once)")
    log("Seed model cost: USD 0; provider calls: 0. Displayed model costs are synthetic accounting.")
    log("Langfuse ingestion price: not estimated (account-specific). Probe: 2 additional units per execution.")
    log(json.dumps(result, sort_keys=True))
    return result
