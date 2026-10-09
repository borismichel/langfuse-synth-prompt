"""Model-free seed, strict fresh target, bounded receipts, append-safe failure state."""
from __future__ import annotations
from datetime import datetime
import os
from pathlib import Path
import shutil
import sys
import tempfile
from langfuse_synth_core.seed.ingest import Ingestor, assert_demo_project
from langfuse_synth_core.seed import otlp
from langfuse_synth_core.timegen import resolve_run_date
from .config import Config
from .materialize import build_events, build_historical_experiment_events
from .receipt import make_receipt
from .state import RunState
from .scores import SCORE_CONTRACT

DEFAULT_SPOOL = Path('.synth_spool') / 'events.ndjson'


def _refresh_configuration(cfg: Config, *, log=print) -> None:
    """Read existing evaluator configuration; never regenerate or import events."""
    from .assets import AssetAPI, LEGACY_NULLABLE_GATE, _evaluation_assets
    from .catalog import score_definitions

    if not RunState.exists():
        raise RuntimeError('Configuration refresh requires a successful live seed receipt.')
    path = Path(RunState.state_path())
    original = path.read_bytes()
    state = RunState.load()
    receipt = state.run_receipt
    valid = (not state.dry_run and state.import_status == 'imported'
             and state.base_url.rstrip('/') == cfg.target.base_url
             and bool(state.project_id) and state.provisioning.get('project_id') == state.project_id
             and state.seed == cfg.generation.seed == receipt.get('seed')
             and state.target_traces == cfg.generation.target_traces == receipt.get('target_traces')
             and receipt.get('schema_version') == 1
             and state.spooled_events > 0 and state.spooled_events == receipt.get('spooled_events')
             and bool(receipt.get('representative_traces'))
             and isinstance(receipt.get('spool_sha256'), str) and len(receipt['spool_sha256']) == 64)
    try:
        run_date = datetime.fromisoformat(receipt.get('run_date', ''))
        valid = valid and run_date.tzinfo is not None
        if cfg.generation.as_of_date:
            valid = valid and run_date.date() == cfg.generation.as_of_date
    except (TypeError, ValueError):
        valid = False
    if not valid:
        raise RuntimeError('Configuration refresh requires a complete imported receipt matching this target and generation configuration.')
    if receipt.get('score_contract') != SCORE_CONTRACT:
        raise RuntimeError('Existing receipt uses the earlier score contract; categorical history requires a fresh target or authorised reset, not configuration refresh.')
    project_id, _ = assert_demo_project(cfg.target.base_url, cfg.target.project_hint)
    if project_id != state.project_id:
        raise RuntimeError('Configuration refresh authenticated project does not match the seeded project.')

    class ReadOnlyAssets:
        # No create method: discovery cannot provision assets even accidentally.
        def __init__(self):
            self.read = AssetAPI(cfg.target.base_url).read

    discovered = _evaluation_assets(cfg, ReadOnlyAssets(), create=False)
    expected = {eid for eid, definition in score_definitions().items()
                if definition['producer'] == 'llm-judge'}
    if set(discovered['evaluators']) != expected or set(discovered['evaluator_rules']) != expected:
        raise RuntimeError('Configuration refresh requires all supported evaluator definitions and live rules; complete evaluator setup first.')

    # Remove obsolete evaluator-setup gates only after all ten definitions and rules match.
    setup_gates = {
        LEGACY_NULLABLE_GATE,
        'Set evaluation.provider/model and run the separate model-using evaluator setup before seed.',
        'Selected judge provider/model is not available through a configured Langfuse LLM connection.',
        *(f'{eid}: managed evaluator requires separate model-using setup before seed.' for eid in expected),
        *(f'{eid}: live rule requires separate evaluator setup before seed.' for eid in expected),
    }
    if cfg.live.model:
        setup_gates.add('Select live.model for native prompt experiments; synthetic history model names are not runnable.')
    retained = [missing for missing in state.provisioning.get('missing', []) if missing not in setup_gates]
    state.provisioning['missing'] = list(dict.fromkeys(retained + discovered['missing']))
    state.provisioning['evaluators'] = discovered['evaluators']
    state.provisioning['evaluator_rules'] = discovered['evaluator_rules']
    state.evaluator_rules = discovered['evaluator_rules']
    # Save through core IO to a sibling, then atomically replace. Failed reads,
    # discovery, validation or serialization leave the prior receipt untouched.
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.configuration-', delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        state.save(str(temporary_path))
        if path.read_bytes() != original:
            raise RuntimeError('Seed state changed during configuration refresh; no refresh was saved.')
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
    log(f'· refreshed {len(expected)} existing evaluator definitions and live rules; seed receipt and import unchanged')


def deliver_artifacts(out_dir: Path | None = None) -> Path:
    out = out_dir or Path(os.environ.get('SYNTH_OUT_DIR', '/app/out' if Path('/app').is_dir() else 'out'))
    out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parents[2] / 'DEMO_SCRIPT.md'
    if not source.is_file():
        source = Path(sys.prefix) / 'share' / 'prompt' / 'DEMO_SCRIPT.md'
    shutil.copy2(source, out / 'DEMO_SCRIPT.md')
    return out / 'DEMO_SCRIPT.md'


def run_seed(cfg: Config, *, dry_run: bool=False, do_import: bool=True,
             spool_path: str | Path | None=None, refresh_configuration: bool=False,
             expand_existing: str | Path | None=None, log=print) -> Path:
    spool_path = Path(spool_path) if spool_path else DEFAULT_SPOOL
    if expand_existing is not None:
        if dry_run or not do_import or refresh_configuration:
            raise ValueError('Expansion cannot be combined with dry-run, spool-only or configuration refresh.')
        from .expansion import run_expansion
        delta = run_expansion(cfg, previous_spool=Path(expand_existing), log=log)
        deliver_artifacts()
        return delta
    if refresh_configuration:
        if dry_run or not do_import:
            raise ValueError('Configuration refresh cannot be combined with dry-run or spool-only mode.')
        _refresh_configuration(cfg, log=log)
        return spool_path
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
