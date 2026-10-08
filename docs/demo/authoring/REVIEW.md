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
| Scenario/integration suite | 89 passed | [tests.txt](evidence/tests.txt) |
| Process repeatability | Identical full spool for hash seeds 0, 1, 2 with networking denied | Included in test suite |
| Package dependencies | No broken requirements | [dependencies.txt](evidence/dependencies.txt) |
| Public request schemas | 144 asset/setup payloads validated against official OpenAPI snapshot, no errors | [schema-check.json](evidence/schema-check.json) |
| Local runtime image | Built; non-root UID 10001, network disabled, small seed and runbook delivery succeeded; both provider clients bind without calls | [container-smoke.json](evidence/container-smoke.json) |
| Companion browser | Three bots and feedback reviewed by implementation agent; parent replayed four product turns, corrected and rechecked consistent v7 voice | [preview-rehearsal.md](evidence/preview-rehearsal.md), [screenshot](evidence/companion-four-turns.jpg) |
| Small live seed/readback | 219 passed, 4 readiness checks pending; all 36 representative traces and 18 experiment associations matched | [live-pilot.json](evidence/live-pilot.json) |
| Intended population | Arithmetic plan reconciles 1,620 history traces / 2,100 generations / 9,320 eligible outcomes | [generation notes](GENERATION.md) |

The golden is a deliberate replacement of the scaffold example: 24 history traces
plus eighteen authored experiment traces. It is a small full-wire snapshot, frozen
with the supported authoring command. Source fixtures preserve the accepted packet.
The production-volume events have **not** been generated: the skill requires a
complete small live walkthrough before scaling. The small seed is now imported and
read back; model setup and native UI rehearsal remain pending.

## Required decisions and external evidence

1. **Live target:** the supplied credentials authenticated an empty dedicated project.
   Imported once: 48 history traces plus 18 authored experiment traces, 80 generations
   and 312 scores. All current-run trace and historical-experiment checks passed.
   Credentials remain in ignored local configuration. No re-import occurred.
   The project has no model connection; an approved provider credential source was
   requested for native experiments/evaluators and the companion. Browser access
   redirects to sign-in, so native UI rehearsal requires an authenticated session.
2. **Nullable criteria:** accepted E-02 factual fidelity and E-03 claim support allow
   not-applicable outcomes. The current native numeric judge schema cannot return
   or omit such an outcome. These two managed definitions/rules are deliberately
   uninstalled; the other eight judges have implementation and schema tests.
   Proposed decision, awaiting the user: categorical **Pass / Fail / Not applicable**
   for E-02/E-03 consistently across history, native experiments and live scores.
   This preserves meaning but replaces their numeric averages with category
   breakdowns, so it needs an explicit story/prototype contract update. No change
   to the accepted scores has been made pending that decision.
3. **Native prerequisites:** verify actual model connections, judge calibration,
   protected-label support, member denial and administrator promotion, prompt
   metrics, native experiment comparisons, session replay and exact score placement.
4. **Delivery:** signed immutable release, authenticated Depot admission, confirmed
   staging-only visibility and a full delivered-surface rehearsal are pending.
   No release tag, image publication, registry change or public deployment occurred.

The full goal remains open. Offline success is not evidence that live evaluation,
permission enforcement, promotion, ingestion or session navigation has succeeded.

## Skill boundary for the pending scale check

[author-langfuse-demo-kit SKILL.md](/Users/bmichel/.agents/skills/author-langfuse-demo-kit/SKILL.md) stage 3 says:
“Keep scaling pending until the complete small walkthrough works; useful offline
fixes can continue while a target is unavailable.” All available offline work has
continued; the pending model setup and rubric decision must be resolved before the live
walkthrough, intended-volume run, admission and final rehearsal can be claimed.

## Live verification compatibility correction

The pinned core dataset-name lookup uses a legacy endpoint that returned 404 for
these dataset names. Verification now queries experiments by name through the
public core reader and requires exact experiment and dataset IDs. V4 exposes the
seeded dataset item identity as `experimentItemId` (`ExperimentItem.id`), so the
assertion checks that field plus the exact trace and generation. Eight regression
cases reject wrong run, dataset, item, trace and observation identities. All eighteen
associations passed on readback; no core transport change or duplicate import was
needed. Historical examples remain authored illustrations, not executed model runs.
