"""The kit's `synth` runtime CLI (walking skeleton).

Registers the pipeline verbs the manifest wires — `seed` and `verify` — each running
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


def _cmd_configure_evaluators(args: argparse.Namespace) -> int:
    from langfuse_synth_core.seed.ingest import assert_demo_project
    from .assets import configure_evaluators
    cfg = load_config(args.config, overrides=args.set)
    assert_demo_project(cfg.target.base_url, cfg.target.project_hint)
    result = configure_evaluators(cfg)
    print(f"Configured {len(result.get('evaluators', {}))} managed evaluator definitions.")
    for missing in result.get('missing', []):
        print(f"Pending: {missing}")
    return 1 if result.get('missing') else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="synth", description="Demo Depot synth kit runtime.")
    sub = parser.add_subparsers(dest="command", metavar="<verb>")

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
    setup.set_defaults(func=_cmd_configure_evaluators)

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
