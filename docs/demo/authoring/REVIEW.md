# Authoring implementation review

Recorded 2026-10-08. **Implementation available for review; not demo-ready.**
The user accepted the prototype and requested the complete kit with clean-context
subagents for generation and implementation, the Langfuse skill and brand assets.
That authorisation is not recorded as acceptance of this new implementation.

## Delivered implementation

- Supported v4.1.1 scaffold reconciled into the existing workspace; core runtime,
  authoring and image workflow pins match. Langfuse SDK 4.17.0; provider clients
  OpenAI 3.26.1 and Anthropic 1.12.1 are included in the runtime image.
- Nine prompt families, eight authored opening versions, nine matching datasets
  with 32 cases, three accounting models, twelve score definitions and explicit
  input/reply subjects. Model-free history and eighteen authored historical
  experiment examples use core event builders and transport.
- Native experiment context binds server dataset/item identities to deterministic
  spans before their single import. The answering generation is the canonical
  experiment observation. Final wire hashes and exact readback receipts are saved.
- Three actual companion adapters fetch managed chat prompts at `production` with
  cache TTL zero, call the selected provider, record request/generation context,
  preserve roles/history and return a primary native-session link. User feedback
  attaches to the saved root. Evaluations are read back from their exact subjects.
- The accepted Langfuse tokens, bundled fonts and disclosed display-font
  substitution shape the delivered companion. Presenter controls are collapsed.
  Native Langfuse screens are not reimplemented in the live companion.
- Model-using evaluator configuration is explicitly separate from seed. Seed
  discovers existing definitions/rules; it never creates a judge that can trigger
  provider validation. Fresh-namespace and partial-import guards prevent blind
  duplicate writes.
- Read-only configuration refresh adopts later evaluator setup into the successful
  seed receipt without regenerating/importing history. It validates the authenticated
  project and generation identity and preserves state on incomplete setup or errors.
- Presenter runbook, source manifest, image workflow, dependency declarations,
  current-run verification and isolated credential-free preview are included.

## Observed checks

| Gate | Result | Evidence |
| --- | --- | --- |
| Manifest | Passed | [manifest.txt](evidence/manifest.txt) |
| Pinned core conformance | Passed, no skipped checks | [conformance.txt](evidence/conformance.txt) |
| Scenario/integration suite | 131 passed after trace refinement | [tests.txt](evidence/tests.txt) |
| Process repeatability | Identical full spool for hash seeds 0, 1, 2 with networking denied | Included in test suite |
| Package dependencies | No broken requirements | [dependencies.txt](evidence/dependencies.txt) |
| Public request schemas | 144 asset/setup payloads validated against official OpenAPI snapshot, no errors | [schema-check.json](evidence/schema-check.json) |
| Local runtime image | Built; non-root UID 10001, network disabled, small seed and runbook delivery succeeded; both provider clients bind without calls | [container-smoke.json](evidence/container-smoke.json) |
| Companion browser | Three bots and feedback reviewed by implementation agent; parent replayed four product turns, corrected and rechecked consistent v7 voice | [preview-rehearsal.md](evidence/preview-rehearsal.md), [screenshot](evidence/companion-four-turns.jpg) |
| Prior pilot seed/readback (before tool enrichment) | 219 passed, 4 readiness checks pending; all 36 representative traces and 18 experiment associations matched | [live-pilot.json](evidence/live-pilot.json) |
| Configured evaluators/readback | 235 passed; two N/A/coverage checks remain failed | [configuration-refresh-readback.json](evidence/configuration-refresh-readback.json) |
| Actual PR-01 live session | Four turns, 16 observations, 24 EVAL scores; 76 structural assertions passed; two calibration mismatches preserved | [live-model-session.json](evidence/live-model-session.json) |
| Refined live fee session | Three turns, 11 observations, two correct fee tools, 15 EVAL results and one saved-root feedback score | [refined-live-session.json](evidence/refined-live-session.json) |
| Refined packaged runtime | Non-root, network disabled; 24 history + 18 experiment traces, 113 observations, 174 scores; runbook delivered; source hashes match | [refined-container-smoke.json](evidence/refined-container-smoke.json) |
| Intended population | Arithmetic plan reconciles 1,620 history traces / 2,100 generations / 9,320 eligible outcomes | [generation notes](GENERATION.md) |

The golden is a deliberate replacement of the scaffold example: 24 history traces
plus eighteen authored experiment traces. It is a small full-wire snapshot, frozen
with the supported authoring command. Source fixtures preserve the accepted packet.
The production-volume events have **not** been generated: the skill requires a
complete small live walkthrough before scaling. The small seed is now imported and
read back; model setup and four real companion turns are now verified. Native UI rehearsal remains pending.

## Required decisions and external evidence

1. **Live target:** the supplied credentials authenticated an empty dedicated project.
   Imported once: 48 history traces plus 18 authored experiment traces, 80 generations
   and 312 scores. All current-run trace and historical-experiment checks passed.
   Credentials remain in ignored local configuration. No re-import occurred.
   The user authorised reuse of Depot model credentials. Its Anthropic connection
   and eight managed evaluator/rule pairs are now configured and read back. Four
   real production-v7 companion turns persisted with 24 EVAL results. Browser access
   redirects to sign-in, so native UI rehearsal requires an authenticated session.
2. **Nullable criteria:** accepted E-02 factual fidelity and E-03 claim support allow
   not-applicable outcomes. The current native numeric judge schema cannot return
   or omit such an outcome. These two managed definitions/rules are deliberately
   uninstalled; the other eight judges are now configured and read back.
   Proposed decision, awaiting the user: categorical **Pass / Fail / Not applicable**
   for E-02/E-03 consistently across history, native experiments and live scores.
   This preserves meaning but replaces their numeric averages with category
   breakdowns, so it needs an explicit story/prototype contract update. No change
   to the accepted scores has been made pending that decision.
3. **Native prerequisites:** finish judge calibration,
   protected-label support, member denial and administrator promotion, prompt
   metrics, native experiment comparisons, session replay and exact score placement.
4. **Delivery:** signed immutable release, authenticated Depot admission, confirmed
   staging-only visibility and a full delivered-surface rehearsal are pending.
   No release tag, image publication, registry change or public deployment occurred.

The full goal remains open. Live companion ingestion and applicable evaluations have
now been observed; permission enforcement, promotion and native session rendering
remain separate, unexecuted checks.

## Skill boundary for the pending scale check

[author-langfuse-demo-kit SKILL.md](/Users/bmichel/.agents/skills/author-langfuse-demo-kit/SKILL.md) stage 3 says:
“Keep scaling pending until the complete small walkthrough works; useful offline
fixes can continue while a target is unavailable.” All available offline work has
continued; the remaining rubric decision and native UI walkthrough must be resolved
before the intended-volume run, admission and final rehearsal can be claimed.

## Live verification compatibility correction

The pinned core dataset-name lookup uses a legacy endpoint that returned 404 for
these dataset names. Verification now queries experiments by name through the
public core reader and requires exact experiment and dataset IDs. V4 exposes the
seeded dataset item identity as `experimentItemId` (`ExperimentItem.id`), so the
assertion checks that field plus the exact trace and generation. Eight regression
cases reject wrong run, dataset, item, trace and observation identities. All eighteen
associations passed on readback; no core transport change or duplicate import was
needed. Historical examples remain authored illustrations, not executed model runs.

## User-requested trace enrichment (after the pilot)

The user requested meaningful tool operations in live companion and history.
[TRACE_SHAPES.md](../story/TRACE_SHAPES.md) specifies the shared request → reference
tool → nested retriever, then reply generation shape. The live path executes the
local catalog lookup and validation; history records explicit synthetic versions.
Input and reply evaluator subjects remain separate from tool observations.

The prior 219 passing live checks apply to the pre-enrichment pilot. New tool
shapes now have real companion persistence evidence for four turns. Revised history
remains offline-only until a fresh/reset authorised pilot is imported and read back.
Existing history was not appended or overwritten.

The revised scenario suite passes 103 tests, including exact historical hierarchy,
session/timing containment, live read/validation failures, correct evaluator
subjects and reference-to-model payload identity. Cross-process seed output
matched under Python hash seeds 0, 1 and 2 before the deliberate golden refresh.
The supported freeze produced a 596,592-byte golden. Manifest and pinned core
conformance pass. [Trace-shape evidence](evidence/trace-shapes.json) records the
four actual fixture observations; it explicitly excludes live persistence claims.

## Follow-up skill audit

[Trace design audit](TRACE_DESIGN_AUDIT.md) applies the freshly fetched Langfuse
best-practices page and instrumentation skill. The implemented hierarchy has
correct parent/session/score relationships, but the generic tool wrapper around
retrieval provides limited additional value. The audit recommends specific
retrieval types, distinct real tool actions and consistent operation naming.
The refinement below now implements these recommendations; older evidence remains
labelled with its prior shape.

## Depot model connection and actual live session

The user authorised Depot credential reuse on 2026-10-08. The existing shared
Anthropic credential was read from Depot's secret manager after its cap check;
a secret-free audit event records the use. The credential is private, ignored
local configuration. The model connection uses `claude-sonnet-4-6`; no Depot
source, shared cap, authentication or existing deployment was changed.

Eight managed evaluator definitions and eight live observation rules passed exact
configuration readback. The separate refresh command adopted those receipts into
the original seed state without importing additional history. Subsequent
[verification](evidence/configuration-refresh-readback.json) passed 235 checks;
two checks remain failed for the documented E-02/E-03 coverage/N/A decision.

[Live session evidence](evidence/live-model-session.json) records four real PR-01
turns, four traces, sixteen observations and twenty-four managed EVAL results.
All generations used `products/explainer` production v7 and actual model usage/cost.
Input scores target each request root; reply scores target the generation.
Tool/retriever observations have no evaluation subjects. Native session UI replay
is still pending an authenticated browser session.

The explicit self-correction in turn two scored 1 for both contradiction and
disagreement, despite accepted E-05/E-08 expecting 0. This is a calibration finding,
not a passing quality result. The original scores and reasoning are preserved;
no prompt rewrite, score replacement, automatic gate or retry-until-pass occurred.
The baseline dark-side style score is 0 and respectful tone is 1 on all four turns.
E-02/E-03 remain unconfigured pending the N/A representation decision.

The live screenshot precedes a small display fix: assistant Markdown now uses
safe text nodes and elements; user input, HTML and links remain inert plaintext.
The full local suite still passes 103 tests, plus the offline renderer safety
regression, manifest and core conformance.

## Trace refinement and remaining access

The runtime now uses one source RETRIEVER and an optional real fee-calculation
TOOL as siblings of the answer GENERATION. Fixed orchestration roots are SPANs;
FLOW-01 lookup is a RETRIEVER. The 24-trace history fixture has 77 observations,
including one calculation. Seed 42's full arithmetic plan has 5,101 observations
and 61 calculations; no full-volume history has been generated or imported.

[Fresh nullable-evaluator research](NULLABLE_EVALUATOR_RESEARCH.md) confirms the
native numeric limitation against current official code/schema. An external
nullable judge adapter for just E-02/E-03 could preserve numeric semantics, but
would change the producer and require automatic processing of native experiment
outputs. Categorical Pass/Fail/N/A is another possible contract change. Neither
has been substituted silently for the accepted managed-evaluator workflow.

The native Langfuse session page currently reports no access and offers Sign In.
Depot redirects to its sign-in page. Automatic approval review rejected initiating
Depot's Google sign-in because account-use authorization was not established;
explicit approval has been requested. No authentication bypass was attempted.


## Refined live readback

A new three-turn PR-02 session exercised the refined runtime without reimporting
history. Readback contains eleven observations: three request roots, three
retrievers, three generations and two actual fee calculations. Three withdrawals
produce EUR 1.50; two produce EUR 0.00. The third incomplete correction has no
calculator observation or stale derived context. Fifteen managed EVAL outcomes
attach to the correct request/reply subjects. A labelled rehearsal feedback score
was read back on the third request root. See
[refined live evidence](evidence/refined-live-session.json) and
[companion screenshot](evidence/refined-companion-feedback.jpg).

This closes the revised companion trace/feedback persistence checks, not native
UI replay, permission enforcement, promotion, experiment comparison or admission.
