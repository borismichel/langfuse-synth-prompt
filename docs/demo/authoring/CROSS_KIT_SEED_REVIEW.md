# Cross-kit seed review — 2026-10-12

Compared registered EV v0.7.0, MRM/lender v0.6.4, Prompt v0.2.3 and Depot
b16d46f. v0.2.4 consolidates the resulting Prompt fixes. Scenario differences
are distinguished from platform requirements; older APIs and unsafe resume
advice are not copied from reference kits.

| Area | EV / MRM | Prompt finding and disposition |
| --- | --- | --- |
| Pipeline structure | Probe → plan → atomic seed → scenario verification; MRM adds evaluator setup. | Same supported atomic seed contract. Extra model-validation and experiment-mapping steps are dependency-driven, not a separate UI. |
| Confirmation | Both declare `gate: confirm` after plan. | Omitted in v0.2.2; restored before evaluator setup or seed. Depot owns the decision screen. |
| Estimate | Older trace/density estimates; dry-run planning writes a spool. | Preserve exact observation+score counts and non-mutating plan. Default 1,638 total traces, 5,137 observations, 9,356 scores = 14,493 units. |
| Billing cap | Both registered manifests use atomic seed, without the split `generate` stage required for measured cap enforcement. | Shared limitation, not a missing Prompt stage. Confirmation is not a hard cap. The memory ceiling below is also not a billing cap. |
| Seed logs | EV flushes progress; MRM reports verification incrementally with wait notices. | Flushed output starts before work; asset/batch updates plus shared 15-second quiet-period notices cover setup and verification. |
| Volume range | EV streams generation; MRM volumes have different session-derived semantics. | Advertised 100,000 fails at Depot's 2 GiB memory limit. Runtime and manifest now cap history at a validated 6,000 traces. Default 1,620 unchanged. |
| Secrets/models | Provider credentials scoped to required setup/live operations. | History remains model-free. Only initial evaluator setup gets the provider credential; historical fixtures never call models. |
| Import/recovery | Core transport handles retryable HTTP errors and rejects ambiguous replay; old resume comments are not a safe recovery procedure. | Preserve collision checks, provisioning/import failure receipt and append-only guard. No new resume/re-import path. |
| Verification | Scenario-specific checks; MRM caches genuinely reused reads. | Preserve exact current-run observations, prompt versions, payloads, scores and assets. Report each check; keep bounded visibility retries without skipping first reads. |
| Reset guidance | Both expose manifest `teardown.note`. | Add the missing note. Portal teardown does not clear Langfuse data; use a fresh project or explicitly clear it in Langfuse. |
| Companion readiness | Core v4.2.0 defines health HTTP success as liveness; admission separately reads readiness fields. | Preserve that contract. Missing managed prompts, rules or matching anchors produce `ready:false`; this is not a kit HTTP-status defect. |
| Delivered page | Depot owns deployment presentation. | Hide planned-volume card after success, and avoid duplicating it during the standard confirmation banner. Actual totals remain. |
| Artifacts/state | Shared output directory and anchors contract; scenario-specific runbooks. | Existing runbook delivery and AnchorsIO are correct. No need to copy unrelated scenario artifacts. |

## Regression evidence

Both original symptoms were reproduced before fixes: the actual manifest had no
confirmation gate, and the real seed CLI emitted nothing to a pipe while
provisioning was blocked. New regressions verify output while seed, verification,
evaluator setup, nested mapping verification and initial target validation remain
in progress. Failure cleanup stops the heartbeat and excludes raw exception
payloads. A proposed health-status change was rejected by core conformance: its
offline probe deliberately reports `ready:false` with HTTP 200 for liveness. The
original health contract and explicit readiness checks are retained. Mounted Depot
tests cover active → succeeded hiding and
confirmation-banner deduplication.

## Container scale evidence

The signed v0.2.3 image
`sha256:44dc831c7022e29865e9a34cede4c82eac2e3187e3f476ef77630bdf7b998e48`
was exercised with two CPUs, 2 GiB memory/swap, no network, no real credentials,
a read-only root and isolated disposable spool/output volumes.

| History traces | Path | Result |
| ---: | --- | --- |
| 100,000 | Actual dry-run generation | OOMKilled, exit 137 after 51.63 seconds, before provisioning/import. |
| 1,620 | Actual dry-run | Passed in 3.80 seconds, peak 271,780 KiB; 14,493 events. |
| 6,000 | Generation → fake remote asset API → actual binding → spool → receipt | Passed in 16.43 seconds, peak 838,540 KiB; 53,494 events; 108,035,982-byte spool; 18 bound experiment traces. |

The 6,000 run used actual image code; only authentication and remote import were
mocked. This establishes local materialization memory behaviour, not a live
6,000-trace ingest. All test containers and volumes were removed. The revised
ceiling leaves headroom for the worker container; it does not guarantee a bill
below 50,000 units (the measured seed contains 53,494 units).

## Sources and scope

- EV [v0.7.0 manifest](https://github.com/borismichel/langfuse-synth-ev/blob/v0.7.0/usecase.yaml), `src/synth/cli.py`, `src/synth/seed/run.py`, `src/synth/verify.py` at that tag.
- MRM [v0.6.4 manifest](https://github.com/borismichel/langfuse-synth-lender/blob/v0.6.4/usecase.yaml), corresponding seed/CLI/verification files at that tag.
- Depot `api/app/manifest.py`, `deployments.py`, `worker/runner.py`, `worker/service.py`, `job_stall.py`, `live_assets.py` at b16d46f.
- Prompt [preflight contract](PREFLIGHT.md), `seed.py`, `assets.py`, `verify.py`, `progress.py`, `companion/app.py` and regression tests.

No additional concrete transport, target/state, model-isolation or artifact gap
was found. This is a bounded comparison, not a claim that every possible failure
has been eliminated. Release, admission and rendered-page verification are
recorded separately in the release checklist.
