# Authoring implementation review

Updated 2026-10-09. **Implementation available for review; final delivery pending.**
The user accepted the story/prototype and authorised the complete kit, clean-context
subagents, Langfuse skill and brand assets. The user subsequently approved categorical
Pass / Fail / Not applicable for the two factual criteria. This does not record
acceptance of a finished implementation or claim the remaining delivery checks passed.

## Delivered implementation

- Pinned synth-core v4.1.1 runtime and image workflow; Langfuse SDK 4.17.0 with
  Anthropic 1.12.1 and OpenAI 3.26.1 provider clients.
- Nine prompt families with eight opening versions, nine datasets with 32 cases,
  twelve score definitions, model-free authored history and eighteen authored
  historical experiment examples. Explicit provenance separates synthetic history
  from real model runs.
- Three companion assistants retrieve managed `production` chat prompts on every
  turn, preserve roles/history, invoke the model and link primarily to the native
  session. The accepted layout, tokens, fonts and display-font substitution remain.
- Meaningful live observations: request SPAN → reference RETRIEVER, optional real
  fee-calculation TOOL, answer GENERATION. Input evaluators target the request root;
  reply evaluators target the generation. Tool operations receive no evaluator subjects.
- Ten managed evaluator/rule pairs: reply quality and style plus user disagreement,
  contradiction, agitation and profanity. E-02/E-03 use categorical strings; nominal
  category codes are not quality values. Missing/invalid outcomes remain distinct
  from an explicit Not applicable result.
- Native experiment metadata uses serialized top-level `eval_*` fields, avoiding
  the platform's nested-metadata flattening. Live observation mappings remain nested
  and unchanged. Regression coverage includes all 32 cases and nonempty history.
- Exact-run receipts, partial-import guards, configuration refresh and credential-free
  preview are included. Legacy numeric history receipts cannot be relabelled as the
  new categorical contract. Seed remains model-free and never provisions paid judges.

## Current evidence

| Check | Observed result | Evidence |
| --- | --- | --- |
| Scenario/integration suite | 170 passed | [tests](evidence/tests.txt) |
| Manifest and pinned core conformance | Passed, no skips | [manifest](evidence/manifest.txt), [conformance](evidence/conformance.txt) |
| Current local image | Brand-refined image built; UID 10001, no network/credentials, read-only root; exact page/static assets served. Earlier image verified seed, runbook and SDK export. | [brand refinement](BRAND_REFINEMENT.md), [categorical build](CATEGORICAL_BUILD.md) |
| Process repeatability | Same complete spool across hash seeds with networking denied | Test suite |
| Approved categorical contract | Source, prototype, golden, readback and native definitions updated | [categorical setup](evidence/categorical-evaluators.json) |
| Native experiment context | 32 existing dataset items preserved; nine default mappings repaired and read back | [repair receipt](evidence/experiment-context-repair.json) |
| Native comparison | 16 real outputs / 64 EVAL scores; same dataset/item/evaluator versions and model | [experiments](evidence/native-experiments.json) |
| Native prompt portfolio | Opening versions and metrics inspected; protected production saved; v9 staged then promoted by owner | [native rehearsal](NATIVE_REHEARSAL.md) |
| Refined fee conversation | Three turns, eleven observations, two real calculations, fifteen EVAL scores and saved-root feedback; native session/tree inspected | [fee evidence](evidence/refined-live-session.json) |
| Latest promoted conversation | Four v9 turns, twelve observations, 32 correctly targeted EVAL scores; native session and generation link verified | [live readback](evidence/categorical-live-session.json), [native rehearsal](NATIVE_REHEARSAL.md) |
| Application guide and final provenance | Two actual guide turns / 14 EVAL scores; one post-fix turn / 7 EVAL scores verifies distinct trace inventory and subject-scoped observation maps | [guide readback](evidence/application-guide-live.json), [metadata repair](evidence/application-guide-metadata-fixed.json) |
| Full population offline spool | 1,620 history traces / 2,100 generations / 9,320 scores, including six explicit N/A outcomes; plus 18 experiment traces. No network or import. | [generation](GENERATION.md), [spool evidence](evidence/full-volume-spool.json) |
| Fresh categorical history | User-created `prompt-portfolio-demo`; one import of 48 history + 18 authored experiment traces; 244 checks passed | [fresh verification](evidence/fresh-project-verification.json) |
| Full-volume same-project history | 1,620 history + 18 experiment traces, 5,150 observations and 9,356 authored scores; exhaustive inventory passed; original sample and nine nonseed traces preserved | [full-volume evidence](FULL_VOLUME.md) |
| Fresh target live connection | One v7 product turn, three observations, eight EVAL results on the correct subjects; native session link verified | [fresh live readback](evidence/fresh-project-live.json), [fresh project rehearsal](FRESH_PROJECT.md) |
| Protected-label enforcement | User independently verified protection on 2026-10-09; accepted as closing the permission check | [user verification](evidence/protected-label-user-verification.json) |
| Requested companion brand details | Lime marker and accents, exact corner masks and subtle stripes; light/dark desktop/phone checks and 28 runtime checks passed | [brand refinement](BRAND_REFINEMENT.md) |

The corrected native comparison has baseline style 0.00 and candidate style 0.75;
both versions have eight Pass outcomes on each factual criterion and tone 1.00.
Candidate cases C-02 and C-06 remain ordinary prose. Original invalid-context v9
results are retained separately and cannot be interpreted as answer quality.
The comparison was rerun once per version to repair observed instrumentation,
not to obtain a preferred score. Promotion remains a presenter decision.

The live promoted run kept ordinary prose on all four replies despite verified v9
style instructions. That visible-style payoff remains unreliable; it is recorded,
not hidden or retried. The input judges also retain two correction false positives.

The application-guide live check exposed trace/observation rubric-key precedence
and SDK dictionary stringification. An actual SDK/export regression reproduced both;
distinct trace metadata and explicit JSON fixed them. One new live turn confirms
correct scoped maps. Existing results remain preserved.

## Remaining gates

1. **Follow-up release.** The original `v0.1.0` is signed, passed all six
   admission checks and is registered/published in Depot. The `v0.2.0` candidate
   adds native reusable text components, complete fresh-project setup stages and
   catalog metadata; its release/admission is pending until observed.
   [Delivery evidence](DEPOT_ONBOARDING.md).
2. **Delivered rehearsal.** The final Depot-served runbook, companion, composed
   prompts, experiments and session still need a complete run on the new revision.

## Text-component amendment

The user's post-registration request adds four reusable text prompt families and
five versions under `building-blocks`. All nine agent families use native references.
The 72 resolved opening chat versions preserve the accepted fixture text exactly.
Voice v2 carries the existing playful candidate instruction. Shared component
versions are pinned in seeded agent prompts; the presenter may use the `playful`
label when composing a new staging candidate. No historical generation changes.

The fresh Depot pipeline explicitly configures evaluators, seeds without model
calls, installs experiment mappings after import, and verifies the final result.
The production metadata and experiment item metadata mappings remain separate.
The feature requires a fresh project for new seeding; populated earlier projects
are preserved and must not be replayed. This records requested implementation,
not user acceptance of unexecuted release or rehearsal checks.

## Preserved earlier evidence

[Prior pilot](evidence/live-pilot.json) and
[configuration refresh](evidence/configuration-refresh-readback.json) document the
old numeric receipt and its two N/A failures. They are not current-contract passes.
[Earlier product conversation](evidence/live-model-session.json) preserves two
input-judge calibration mismatches on an explicit correction; neither was erased.
[Trace design audit](TRACE_DESIGN_AUDIT.md) explains the later specific retriever
and calculator refinement. [Nullable research](NULLABLE_EVALUATOR_RESEARCH.md)
records the schema limitation and subsequent approved categorical decision.

## Skill boundary

[author-langfuse-demo-kit SKILL.md](/Users/bmichel/.agents/skills/author-langfuse-demo-kit/SKILL.md)
stage 3 says: “Keep scaling pending until the complete small walkthrough works;
useful offline fixes can continue while a target is unavailable.” Offline work and
all available authenticated native rehearsal continue. The corrected small target
is verified, and the user independently verified protection. The small walkthrough
gate is complete. Full-volume same-project history and readback are now complete;
Depot delivery remains open until the prerequisites above are resolved.

## 2026-10-09 operational revision

The user's later instructions replace anonymous model labels with original Claude
IDs, keep experiments/judges on Sonnet 5.5, add explicit BOOLEAN thumbs/comments,
make visible names resemble a running application, and retain prompt associations
on generations only. This revision implements those changes without redesigning
the accepted prototype or introducing prompt-volume scaling.

[Operational revision evidence](OPERATIONAL_REVISION.md) records the same-project
replacement, 248 successful live checks, exhaustive 5,150-observation/9,356-score
readback, real Sonnet/Opus turns, feedback and generation linkage, 273 offline
tests and refreshed isolated container. Authoring remains ready with Depot
admission and delivered rehearsal pending; this is not new user acceptance of
an unperformed deployment.

## Final fresh-target seed — 2026-10-09

The user requested a final run in a newly supplied blank project before onboarding
and shipping. [Final seed evidence](FINAL_SEED.md) records the one-time full import,
266 passing scenario checks, exhaustive readback, production-label protection,
and a real two-turn chat with sixteen evaluator outcomes and two feedback scores.
This is ready for review; no new user acceptance or Depot admission is inferred.
The generation-only prompt association correction remains authoritative.

## Evaluator editor correction and onboarding — 2026-10-09

The user reported JSONPath warnings in the final project's judge editor and
authorized Depot registration. [Mapping repair](EVALUATOR_MAPPING_REPAIR.md)
records the corrected live defaults and native experiment overrides, verified
in both product surfaces. The seed remains model-free. A separate post-import
configuration step is included in the runbook. Depot admission remains pending
until a released candidate completes its actual ladder; no local test is treated
as admission. Reusable text-prompt components are requested for a subsequent
release after registration.
