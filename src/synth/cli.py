"""The kit's `synth` runtime CLI (walking skeleton).

Registers the pipeline verbs the manifest wires — including `probe`, `plan`, `seed` and `verify` — each running
through the shared library. The invocation these verbs answer is the Contract's:
`synth <verb> --config {config}`, with `--set dotted.key=value` overrides appended on
pipeline steps only (CONTRACT.md §"The container invocation" — live and resume commands
never receive `--set`). A step id that is a reserved verb (seed/verify/...) must run
`synth <that verb>` — the manifest keeps that contract, so grow new verbs here and in
`usecase.yaml` together.
"""
from __future__ import annotations

import argparse
import sys

from .config import load_config
from .seed import run_seed
from .verify import run_verify
from .preflight import run_plan, run_probe


def _add_config_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", required=True, help="path to the kit config YAML")
    parser.add_argument(
        "--set",
        action="append",
        metavar="dotted.key=value",
        help="override a config value (repeatable); applied before validation",
    )


def _cmd_seed(args: argparse.Namespace) -> int:
    cfg = load_config(args.config, overrides=args.set)
    run_seed(cfg, dry_run=args.dry_run, refresh_configuration=args.refresh_configuration,
             expand_existing=args.expand_existing)
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    cfg = load_config(args.config, overrides=args.set)
    return 0 if run_verify(cfg).ok else 1


def _cmd_probe(args: argparse.Namespace) -> int:
    return 0 if run_probe(load_config(args.config, overrides=args.set)) else 1


def _cmd_plan(args: argparse.Namespace) -> int:
    run_plan(load_config(args.config, overrides=args.set))
    return 0


def _cmd_configure_evaluators(args: argparse.Namespace) -> int:
    from langfuse_synth_core.seed.ingest import assert_demo_project
    from .assets import configure_evaluators, configure_evaluator_mappings
    cfg = load_config(args.config, overrides=args.set)
    assert_demo_project(cfg.target.base_url, cfg.target.project_hint)
    result = (configure_evaluator_mappings(cfg) if args.update_mappings
              else configure_evaluators(cfg, update_model=args.update_model))
    print(f"Configured {len(result.get('evaluators', {}))} managed evaluator definitions.")
    for missing in result.get('missing', []):
        print(f"Pending: {missing}")
    return 1 if result.get('missing') else 0


def _cmd_history_replacement_plan(args: argparse.Namespace) -> int:
    from pathlib import Path
    from .migration import prepare_replacement
    plan = prepare_replacement(
        Path(args.source_spool), Path(args.destination),
        expected_project_id=args.project_id, expected_run_date=args.run_date,
        revision=args.revision,
        expected_counts={'trace': args.expected_traces,
                         'observation': args.expected_observations,
                         'score': args.expected_scores},
    )
    print(f"Prepared local replacement plan: {plan}")
    print("No live data changed. Follow docs/demo/authoring/HISTORY_REPLACEMENT.md for the guarded apply procedure.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="synth", description="Demo Depot synth kit runtime.")
    sub = parser.add_subparsers(dest="command", metavar="<verb>")

    probe = sub.add_parser("probe", help="check backdated ingestion with two throwaway observations")
    _add_config_args(probe)
    probe.set_defaults(func=_cmd_probe)

    plan = sub.add_parser("plan", help="estimate seed volume and costs offline, without writing state or spool")
    _add_config_args(plan)
    plan.set_defaults(func=_cmd_plan)

    seed = sub.add_parser("seed", help="generate + ingest the backdated demo data")
    _add_config_args(seed)
    seed_mode = seed.add_mutually_exclusive_group()
    seed_mode.add_argument("--dry-run", action="store_true", help="spool only; no network")
    seed_mode.add_argument("--refresh-configuration", action="store_true",
                           help="developer mode: read existing evaluators/rules into a successful seed receipt; no import")
    seed_mode.add_argument("--expand-existing", metavar="IMPORTED_SPOOL",
                           help="developer mode: add missing history to the imported project once, preserving existing assets and events")
    seed.set_defaults(func=_cmd_seed)

    verify = sub.add_parser("verify", help="read the data back and assert the floor checks")
    _add_config_args(verify)
    verify.set_defaults(func=_cmd_verify)

    setup = sub.add_parser("configure-evaluators", help="configure managed judges separately; Langfuse may validate models on save")
    _add_config_args(setup)
    setup_mode = setup.add_mutually_exclusive_group()
    setup_mode.add_argument("--update-model", action="store_true",
                       help="explicitly update only the model of existing accepted judges; preserve rubrics and rules")
    setup_mode.add_argument("--update-mappings", action="store_true",
                       help="post-seed only: verify imported history, preserve dataset overrides, then use live evaluator defaults")
    setup.set_defaults(func=_cmd_configure_evaluators)

    replacement = sub.add_parser(
        "history-replacement-plan",
        help="developer mode: prepare an offline authored-history replacement plan; no network or asset writes",
    )
    replacement.add_argument("--source-spool", required=True,
                             help="complete imported spool beside its .synth_state.json (combined evidence after expansion)")
    replacement.add_argument("--destination", required=True, help="new, nonexistent directory for the replacement plan")
    replacement.add_argument("--project-id", required=True, help="expected existing project ID")
    replacement.add_argument("--run-date", required=True, help="exact timezone-aware run_date from the imported receipt")
    replacement.add_argument("--revision", required=True, help="new descriptive deterministic replacement ID namespace")
    replacement.add_argument("--expected-traces", required=True, type=int, help="exact authored trace count including experiments")
    replacement.add_argument("--expected-observations", required=True, type=int, help="exact authored observation count")
    replacement.add_argument("--expected-scores", required=True, type=int, help="exact authored score count")
    replacement.set_defaults(func=_cmd_history_replacement_plan)

    return parser


def main(argv: list[str] | None = None) -> int:
    # `synth companion` is the live surface (Spec G): the Adapter's fixed
    # --config/--host/--port invocation, never a pipeline --set, so it skips the
    # seed/verify argparse and dispatches to the companion app (which parses via the
    # Adapter's parse_invocation helper).
    _argv = sys.argv[1:] if argv is None else argv
    if _argv[:1] == ["companion"]:
        from .companion.app import main as companion_main

        return companion_main(_argv[1:])
    if _argv[:1] == ["preview"]:
        from .companion.preview import main as preview_main
        return preview_main(_argv[1:])
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if not hasattr(args, "func"):  # no subcommand given
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
