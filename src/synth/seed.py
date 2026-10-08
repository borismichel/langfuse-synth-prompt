"""Model-free seed, strict fresh target, bounded receipts, append-safe failure state."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import sys
from langfuse_synth_core.seed.ingest import Ingestor, assert_demo_project
from langfuse_synth_core.seed import otlp
from langfuse_synth_core.timegen import resolve_run_date
from .config import Config
from .materialize import build_events, build_historical_experiment_events
from .receipt import make_receipt
from .state import RunState

DEFAULT_SPOOL = Path('.synth_spool') / 'events.ndjson'


def deliver_artifacts(out_dir: Path | None = None) -> Path:
    out = out_dir or Path(os.environ.get('SYNTH_OUT_DIR', '/app/out' if Path('/app').is_dir() else 'out'))
    out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parents[2] / 'DEMO_SCRIPT.md'
    if not source.is_file():
        source = Path(sys.prefix) / 'share' / 'prompt' / 'DEMO_SCRIPT.md'
    shutil.copy2(source, out / 'DEMO_SCRIPT.md')
    return out / 'DEMO_SCRIPT.md'


def run_seed(cfg: Config, *, dry_run: bool=False, do_import: bool=True,
             spool_path: str | Path | None=None, log=print) -> Path:
    spool_path = Path(spool_path) if spool_path else DEFAULT_SPOOL
    run_date = resolve_run_date(cfg.generation.as_of_date)
    # Do not allow regeneration to sidestep the core import marker after partial import.
    if RunState.exists():
        previous = RunState.load()
        if not previous.dry_run and previous.import_status in {'provisioning','importing','imported','failed'}:
            raise RuntimeError('This state directory already records a live seed attempt. Use a fresh authorised project and state directory; never re-import into an uncleared project.')
    project_id, project_name = None, ''
    if not dry_run:
        project_id, project_name = assert_demo_project(cfg.target.base_url, cfg.target.project_hint)
    state = RunState(base_url=cfg.target.base_url, project_name=project_name, project_id=project_id,
                     target_traces=cfg.generation.target_traces, seed=cfg.generation.seed, dry_run=dry_run)
    events = build_events(cfg.generation.target_traces, {'seed':cfg.generation.seed}, run_date=run_date)
    experiment_events, experiment_links = build_historical_experiment_events({'seed':cfg.generation.seed}, run_date=run_date)
    events.extend(experiment_events)
    try:
        if not dry_run and do_import:
            from .assets import provision_assets, bind_historical_experiments
            state.import_status = 'provisioning'
            state.save()
            state.provisioning = provision_assets(cfg)
            state.evaluator_rules = state.provisioning.get('evaluator_rules', {})
            events, experiments = bind_historical_experiments(events, state.provisioning, experiment_links)
            state.provisioning['historical_experiments'] = experiments
        ingestor = Ingestor.from_env(cfg.target.base_url, dry_run=dry_run, spool_path=spool_path)
        ingestor.open_spool()
        ingestor.extend(events)
        ingestor.close_spool()
        state.spooled_events = ingestor.spooled
        state.run_receipt = make_receipt(otlp.finalize(events), spool_path, run_date=run_date,
                                         seed=cfg.generation.seed, target_traces=cfg.generation.target_traces)
        log(f'· spooled {ingestor.spooled} events; run anchor {run_date.isoformat()}')
        if not dry_run and do_import:
            state.import_status = 'importing'
            state.save()
            ingestor.import_spool(path=spool_path, log=log)
            state.import_status = 'imported'
        else:
            state.import_status = 'dry_run' if dry_run else 'spooled_only'
    except Exception:
        state.import_status = 'failed'
        state.save()
        raise
    state.save()
    deliver_artifacts()
    log(f'· run receipt: {RunState.state_path()}')
    return spool_path
