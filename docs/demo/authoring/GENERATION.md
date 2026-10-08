# Deterministic generation contract

The generator replays authored fictional records. It makes no model, evaluator or
network call. Historical scores are expected outcomes attached to their actual
subjects, with `judge_executed=false` and explicit provenance. These fixtures do
not establish judge reliability or predict a live experiment result.

The accepted story and prototype are preserved, with the user-requested
[trace-detail amendment](../story/TRACE_SHAPES.md). Four source fixtures
are copied byte-for-byte into `src/synth/fixtures`: portfolio, product, examples,
and dataset extras. Additional authored files supply 72 distinct prompt texts,
the twelve accepted rubric definitions, and coherent two-, three- and five-turn
conversations. PR-01 v7 and the proposed v9 retain the exact accepted text. The
candidate is available for live creation; the opening seed contains no v9.

## Shared catalog

- `load_fixture(name)` returns a fresh decoded object; caller changes cannot alter
  subsequent reads.
- `prompt_by_id(prompt_id)` resolves the stable portfolio relationship.
- `system_prompt(prompt_id, version)` returns the actual authored instructions.
  Eight stored versions per family contain material task-specific changes.
- `dataset_items(prompt_id)` returns eight main items or three secondary items
  (normal, adjacent control, missing information), each with complete source,
  role-bearing prior messages, current question and expected output.
- `score_definitions()` maps E-01–E-12 to the accepted name, subject, numeric type,
  r1 rubric and required evidence.
- `calibration_cases()` exposes the three accepted negative controls separately.
  Their style, factuality and respectfulness dimensions remain independent.
- `historical_experiment_cases()` exposes eighteen fixed v2/v4 examples. Their
  expected results are authored replay, not executed judges.

## Counts and cohort boundaries

`generation.target_traces` counts production-history request traces. It excludes
the fixed historical experiments and any later live records. Largest-remainder
allocation preserves the exact requested total at smaller and larger volumes.

| History scale | Request traces | Generations | All observations | Outcomes | Chat turns | Chat sessions | Chat users |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Small fixture, seed 42 | 24 | 32 | 77 | 138 | 16 | 6 | 4 |
| Accepted full plan, arithmetic only, seed 42 | 1,620 | 2,100 | 5,101 | 9,320 | 1,080 | 360 | 216 |

The full plan preserves 180/108/72 conversations and 540/325/215 turns across
PR-01/02/03. Session length allocations are respectively 72/72/36, 43/43/22 and
29/29/14 for two/three/five turns. It assigns 144 users one session each and 72
users three sessions each. FLOW-01 contributes 240 requests with three prompt
generations and one unprompted simulated lookup each. Other historical work
contributes 120 summaries, 80 extractions and 100 drafted messages.

`build_historical_experiment_events` separately returns eighteen traces,
36 observations, 36 output-score records, and native dataset-run link receipts.
Each prompt has v2 and v4 history. These records use the `experiment` cohort;
no input metric is copied onto a generation to improve a native prompt chart.
Provisioning attaches their dataset run items after successful import.

An outcome is not necessarily a numeric score. Inapplicable outcomes remain on
their exact subject as `{value: null, status: inapplicable}`. Numeric score writes
exclude those outcomes because Langfuse numeric scores require numbers. Missing
values are never recorded as a passing score or zero. The accepted 9,320 is the
numeric-or-null denominator, not an unconditional score-record count.

## Chronology and identities

Every timestamp derives from the supplied run date. The history covers D-28
through D-1 in Europe/Berlin. Each local midnight converts to UTC independently,
so daylight-saving days retain their actual 23 or 25 hours. Synthetic source
document dates in accepted dataset records remain verbatim source facts; they
are not used as the generation clock.

Chat arrival allocation is 25% overnight, 40% daytime and 35% evening, with 25%
of conversations on weekends (nearest integer at small scale). The final local
hour is reserved for conversation completion. Ordinary human gaps are 15–120
seconds; an 8% authored sampling probability selects 5–20 minute resumptions.
These gaps occur after the previous reply and are separate from generation
latency. Internal tasks occur in business hours, predominantly on weekdays;
the first representative record is on D-1 to expose the current version.

Core `Rng` substreams mint IDs and every random value. One session has one
fictional stable user, one request root per turn, and role-bearing new messages
on each root. Generation input retains prior messages once. Core finalization
propagates session/user attributes to children. The stored prompt version is
selected from each family's accepted historical interval.

The root combines attributes emitted by core's `trace_event` shell and typed
`observation_event` builder. This retains a SPAN root and observation-local
evaluation metadata while avoiding trace metadata that would inherit an input
evaluator selector onto every child. Core continues to own OTLP transport and
finalization; the kit does not maintain another wire encoder.

## Evaluation and accounting

E-05–E-08 identify the request root and inspect `current_user_message`,
`prior_messages` and `reference_context` on that subject. Reply criteria identify
the actual generation, with `assistant_reply` and the same relevant context.
FLOW-01 has independent prompt links on intent, rewrite and handoff generations;
the lookup has no prompt assignment.

Early authored history contains explicit errors tied to version purposes: a
waiver exclusion mistake, withdrawal allowance omission and document-recency
mistake. Later examples retain the correct supplied conditions. Expected scores
describe those visible outputs. A prompt instruction is not treated as a
guarantee that a real model would produce either output.

Token counts and duration vary deterministically by prompt, historical version
and conversation context. Cost is computed from those token counts and the
story's declared fictional compact/standard/reasoning rates; it is never
independently randomized. All three model names and their rates are synthetic,
not runnable provider choices or actual vendor prices. Judge cost is not
invented because no historical judge executes.

## Verification and remaining gates

`tests/test_generation.py` verifies the catalog, exact accepted text, meaningful
version distinctions, nine-family small coverage, explicit score subjects,
context/replay consistency, human timing, FLOW-01 links, usage-derived costs,
historical version intervals, DST bounds, deterministic replay, and the eighteen
separate historical experiment links. Full-volume counts are tested as a pure
plan without materializing that population.

The 24-trace sample covers main v1/v7 contrasts, disagreement, correction,
contradiction and quoted profanity. A bounded 48-trace sample covers all active
historical versions across the portfolio. Samples of 24, 48 and 72 were inspected;
the 1,620-trace dataset has not been generated. Its full-volume checks remain
pending the complete small live walkthrough, as required by the authoring skill.
Golden updates belong to the parent seed path and must use the supported freeze
command after process-repeatability checks; none were hand-edited here.

Live persistence, native dataset-run linkage, prompt metrics and session UI,
actual judges/calibration, protected-label enforcement, admission and presenter
rehearsal are separate verification gates. Local fixtures establish none of them.

Current official semantics checked during authoring:
[sessions](https://langfuse.com/docs/observability/features/sessions),
[observation types](https://langfuse.com/docs/observability/features/observation-types),
and [prompt links](https://langfuse.com/docs/prompt-management/features/link-to-traces).

## Reference operations

Each historical chat turn includes one validated catalog RETRIEVER. Explicit
PR-02 calendar-month withdrawal counts additionally execute a deterministic
`calculate-fee` TOOL; unclear or absent counts do not. For seed 42 there is one
such calculation in the 24-trace fixture and 61 in the full arithmetic plan.
Operation counts are derived with the same template-selection substreams as the
generator. Tools carry structured arguments/results, simulated provenance and
stable IDs, without prompt links or evaluation subjects. Source reference facts
stay separate from derived calculation context. Existing root, generation and
score identities remain stable. Historical native prompt experiments remain
prompt-only because their context comes from dataset inputs.

The existing live pilot predates this amendment. Its saved verification report
remains evidence of the prior shape, not these new spans. Do not reimport the
changed spool into that populated project; use a fresh authorised target or an
authorised reset when the complete small live walkthrough can proceed.
