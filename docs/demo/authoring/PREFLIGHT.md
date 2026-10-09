# Probe and offline plan

The runtime pipeline now starts with `probe` and `plan`, followed by the existing
evaluator setup, seed, experiment mapping setup and final scenario verification.
The core pin remains v4.2.0. Generation, fixtures and accepted story are unchanged.

## Target probe

`synth probe --config config/demo.yaml` delegates to core's `run_backdate_probe`.
It guards the selected demo project, writes a root observation and marker with fresh
throwaway IDs, and polls their historical timestamp through `LangfuseReader.trace`.
In v4.2.0 that read is assembled from `/api/public/v2/observations`; there is no
legacy trace endpoint call. Probe failures produce a nonzero exit status, stopping
the fatal pipeline step before setup and seed. Only Langfuse credentials are needed.

Each probe execution adds two observations, independently of seed. It does not
write the seed spool, import marker or receipt. Probe is a target mutation, so it
must only be run against an authorised demo project.

## Offline plan and Depot contract

`synth plan --config config/demo.yaml --set generation.target_traces=1620` follows
the existing seeded population calculator, including conditional fee calculations,
and adds the fixed authored experiment cohort from the catalog. No trace payloads,
spool, state, artifacts or external writes are produced. No keys or network are needed.

For seed 42 and 1,620 production-history traces:

| Scope | Derived traces | Observations | Generations (within observations) | Scores |
| --- | ---: | ---: | ---: | ---: |
| Production history | 1,620 | 5,101 | 2,100 | 9,320 |
| Fixed historical experiments | 18 | 36 | 18 | 36 |
| Seed total | 1,638 | 5,137 | 2,118 | 9,356 |

The seed totals **14,493 billable units: observations + scores**. Derived traces
are not added again because their root observations are already counted. The
probe contributes two further units per execution. Dataset items, experiment
links and prompt assets are excluded from event-volume accounting, consistent
with the pinned core's `count_spool` contract. Live operations after seed are not
included. This follows Langfuse's [v4 observation data model](https://langfuse.com/docs/observability/data-model).

The output includes the generic, versioned line:

```text
PLAN_COUNTS={"version":1,"traces":1638,"observations":5137,"scores":9356}
```

The manifest extracts that JSON with `parse.plan_counts`; Depot derives billable
units as observations + scores. The separate `total_traces: 1638` line and
`parse.event_count` preserve the raw count consumed by older Depot versions.
Those older versions can only show their generic ratio estimate. The final JSON
line adds the separate production/experiment cohorts, probe overhead and cost basis.

Historical seed provider calls and model spend are both zero. The displayed model
costs are synthetic fixture accounting using the existing three-times multiplier;
they are not incurred provider spend. No account-specific Langfuse ingestion price
is supplied, so the plan reports units and leaves ingestion USD unset. Evaluator
model validation, future native experiments, managed evaluations and companion
calls may incur costs and are outside this seed estimate.

## Verification boundary

`tests/test_preflight.py` compares plans against the core counter on actual
finalized events at 1, 24, 72 and 1,620 history traces with varied seeds. The
manifest command runs in an isolated process without credentials, with networking
blocked and existing spool, receipt and import marker checked byte for byte.
Probe tests exercise real core ingestion assembly and the v4 read adapter with
mocked transport for success, changed timestamps, missing observations and guard
rejection. The pipeline test dispatches all six manifest commands in order.

These checks establish offline behavior. The released candidate subsequently passed a
[live probe](evidence/preflight-live-probe.txt) in `prompt-preflight-demo` within
Boris Demo Enterprise. It wrote two observations and preserved the historical
timestamp. All six deployed steps subsequently passed admission; the exact plan totals were
displayed in Depot. Publication and rollout evidence is recorded in
[SHIP_CHECKLIST.md](SHIP_CHECKLIST.md).
The user's existing deployment and companion were preserved.

The pinned core's `synth-authoring check` completed with `local_ready: true`:
manifest validation, conformance and all 334 tests passed. The 100,000-history-trace
offline plan also completed, reporting 100,018 derived traces, 315,231 observations,
575,347 scores and 890,578 seed units without materializing a spool.
