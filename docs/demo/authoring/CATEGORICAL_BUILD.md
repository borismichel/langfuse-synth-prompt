# Categorical local container verification

This records the earlier runtime verification. The 2026-10-09
[brand-refined image](BRAND_REFINEMENT.md) supersedes it for companion presentation;
the underlying generation, tracing and evaluation implementation is unchanged.

Checked 2026-10-08. Rebuilt `langfuse-synth-prompt:categorical-local` from the
current workspace; local image only, never published. Image ID:
`sha256:65e71429e78c4ccd06f6b1a12e6cbaa87f8ab6c31fcca058134dcf566484f171`.
The recorded hashes of six installed runtime modules and the delivered runbook
match the current workspace.
[Sanitized evidence](evidence/categorical-container-smoke.json).

The smoke adapted `.scratch/container_refined_smoke.py` into
`.scratch/container_categorical_smoke.py`, running the image with UID 10001,
`--network none`, a read-only root, temporary `/tmp`, all capabilities removed,
and no credentials or host mounts. It verified model-free seed generation,
byte-identical runbook delivery, categorical definitions, serialized native
experiment context, and the fixture preview's page and chat request. Preview
health deliberately returns 503 with `ready: false`; it does not claim live
readiness. The initial harness assumptions about the health path/status were
corrected to the application's declared `/healthz` preview contract before the
successful final run. No application correction was needed for those checks.

The final rebuild includes criterion-specific `rubric_revisions`: root input
subjects contain applicable input criteria (r1), reply generations contain their
applicable reply criteria (including E-02/E-03 r2), and the distinct trace key `trace_rubric_revisions` contains
all criteria for the prompts in that trace. Live trace propagation explicitly
serializes that inventory as JSON. This prevents trace-level merging from
overwriting an observation's own map or converting the inventory to Python repr. The isolated smoke checked this
provenance through the actual core and SDK exporter with fixture prompt/model,
as well as the fixture chat and generated history/experiments. The prior
fixture-only smoke did not cover SDK propagation. The regression and controlled
probes are recorded in [diagnostic evidence](evidence/rubric-propagation.json). Earlier live
evidence with the umbrella r1 field remains archived unchanged; this check makes
no new live-execution claim. The final offline suite reports **170 passed**;
manifest validation and all conformance checks pass. The supported golden freeze
followed identical output across process hash seeds 0, 1 and 2.

With seed 42 and date 2026-10-08:

| Population | Traces | Observations | Scores | Total events |
| --- | ---: | ---: | ---: | ---: |
| Production history | 1,620 | 5,101 | 9,320 | 14,421 |
| Fixed authored experiments | 18 | 36 | 36 | 72 |
| Combined full seed | 1,638 | 5,137 | 9,356 | 14,493 |

Each factual criterion has 1,134 **Pass**, 43 **Fail**, and 3 **Not applicable**
historical results. The six explicit N/A scores account for the increase from
9,314 numeric historical scores to 9,320 categorical historical scores. The
small smoke remains 42 traces, 113 observations and 174 scores (24 historical
traces plus the fixed 18 experiments).

All counts were generated offline inside the image; nothing was imported.
Existing live data and pilot receipts remain unchanged. The categorical history
still needs a fresh target or authorised reset before importing. This local
check does not establish current-target history verification, Depot admission,
or completion of the live presenter rehearsal. Handoff status was stale during
concurrent authorised edits; the parent workflow owns checkpoint renewal.
