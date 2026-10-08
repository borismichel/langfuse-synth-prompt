# Authoring implementation review

Recorded 2026-10-08. **Implementation available for review; final delivery pending.**
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
| Scenario/integration suite | 161 passed | [tests](evidence/tests.txt) |
| Manifest and pinned core conformance | Passed, no skips | [manifest](evidence/manifest.txt), [conformance](evidence/conformance.txt) |
| Current local image | Built; UID 10001, no network/credentials, read-only root; small seed, runbook and preview passed | [categorical build](CATEGORICAL_BUILD.md) |
| Process repeatability | Same complete spool across hash seeds with networking denied | Test suite |
| Approved categorical contract | Source, prototype, golden, readback and native definitions updated | [categorical setup](evidence/categorical-evaluators.json) |
| Native experiment context | 32 existing dataset items preserved; nine default mappings repaired and read back | [repair receipt](evidence/experiment-context-repair.json) |
| Native comparison | 16 real outputs / 64 EVAL scores; same dataset/item/evaluator versions and model | [experiments](evidence/native-experiments.json) |
| Native prompt portfolio | Opening versions and metrics inspected; protected production saved; v9 staged then promoted by owner | [native rehearsal](NATIVE_REHEARSAL.md) |
| Refined fee conversation | Three turns, eleven observations, two real calculations, fifteen EVAL scores and saved-root feedback; native session/tree inspected | [fee evidence](evidence/refined-live-session.json) |
| Latest promoted conversation | Four v9 turns, twelve observations, 32 correctly targeted EVAL scores; native session and generation link verified | [live readback](evidence/categorical-live-session.json), [native rehearsal](NATIVE_REHEARSAL.md) |
| Intended population arithmetic | 1,620 history traces / 2,100 generations / 9,320 scores, including six explicit N/A outcomes | [generation](GENERATION.md) |

The corrected native comparison has baseline style 0.00 and candidate style 0.75;
both versions have eight Pass outcomes on each factual criterion and tone 1.00.
Candidate cases C-02 and C-06 remain ordinary prose. Original invalid-context v9
results are retained separately and cannot be interpreted as answer quality.
The comparison was rerun once per version to repair observed instrumentation,
not to obtain a preferred score. Promotion remains a presenter decision.

The live promoted run kept ordinary prose on all four replies despite verified v9
style instructions. That visible-style payoff remains unreliable; it is recorded,
not hidden or retried. The input judges also retain two correction false positives.

## Remaining gates

1. **Corrected history target.** The earlier pilot was imported once: 48 history
   traces plus eighteen authored experiments, 80 generations and 312 old-contract
   scores. It is preserved. A fresh project and scoped key were requested to verify
   revised categorical/tool-enriched history without duplicate append ingestion.
   Approval is pending; no fresh key or project has been created.
2. **Member-role denial.** Owner promotion and protected-label configuration are
   observed. An actual member session is still needed to demonstrate denied
   production promotion. Owner/API access cannot stand in for that evidence.
3. **Full population.** Arithmetic/model-free regression checks pass. Full-volume
   delivery and live readback remain pending completion of the small walkthrough.
4. **Signed release and Depot admission.** No release tag, image publication,
   registry mutation or public deployment occurred. Authenticated Chrome access
   works; the deployed Depot lacks the required slug guard and supported admission
   access surface, and new entries default to published. Scratch configuration
   presence is known, but disposable-target suitability is unverified.
   [Concrete deployment findings](DEPOT_ACCESS.md).
5. **Delivered rehearsal.** Staging visibility and the final Depot-served runbook,
   companion, history, evaluations and reset behaviour still need verification.

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
all available authenticated native rehearsal continue. Full delivery remains open
until the target, role and Depot prerequisites above are resolved.
