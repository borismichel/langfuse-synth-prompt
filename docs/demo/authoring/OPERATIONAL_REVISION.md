# Operational naming, model policy and feedback revision

Verified 2026-10-09 in `prompt-portfolio-demo`, project
`cmv0gc1710815ad0k7nnnd6v5`. This supersedes the earlier full-volume spool's
model names and presentation labels while retaining the accepted cases and story.

## Delivered behaviour

- Historical and companion requests share operation names: `explain-product`,
  `explain-fees`, `guide-application` and the corresponding background task names.
  Both use `production`; experiment records use `experiment`.
- Original provider IDs are used: `claude-sonnet-5-5`, `claude-opus-5-5`,
  `claude-fable-5-1`. Langfuse's managed definitions and standard pricing tiers are
  reused. Three unused fictional model definitions were removed after checking
  that no surviving observation used them.
- The role policy is canonical in `src/synth/fixtures/model_policy.json`.
  Experiments and all ten managed evaluator definitions use Sonnet 5.5.
  Authored cost details use the explicit 3× multiplier; actual chats retain real
  token usage and base pricing. Existing actual executions retain their models.
- Native prompt associations stay on **generations**, following the user's final
  clarification. Roots contain request context and input evaluations, without
  redundant prompt reference inventories.
- Each reply offers thumbs up/down and an optional comment. One final BOOLEAN
  `user-thumbs` score targets that reply's request root. Exact retries deduplicate;
  a second changed submission is rejected. Evaluator-inferred disagreement is
  separate, and no score controls promotion.
- Experiment labels, customer/session identifiers and score comments use normal
  application wording. Authored provenance remains in metadata and documentation.
  The population still covers 28 complete days; no real customer traffic is claimed.

## Same-project replacement evidence

The complete prior spool was preserved. A guarded replacement deleted exactly
its 1,638 trace IDs, waited for their observations **and scores** to disappear,
and imported once under fresh tracing IDs. Prompts, labels, datasets and experiment
identities were preserved. A reviewed local pre-import amendment applied the
user's generation-only clarification and remaining presentation cleanup, with
backups and hashes; it issued no additional deletion.

Final spool SHA-256:
`d556e07180fd7bd26c1e8afcc579a285dc64c10614b1cc23a3fb0d7c79789d5b`.

[Exhaustive readback](evidence/operational-history-inventory.json) verified:

- **1,638 traces, 5,150 observations, 9,356 scores**, without duplicate IDs.
- **2,118 native prompt-linked generations:** 1,038 Sonnet, 720 Opus, 360 Fable.
- Correct names, environments, user/session IDs, model IDs, explicit costs and
  score values/subjects. Replay observations did not trigger online judges.
- Every non-seed record present at deletion preflight remained: 27 traces,
  33 observations and 24 scores, including existing chats and new verification
  evidence. Records created subsequently also remain outside the replacement.

The kit's [current-run verification](evidence/operational-history-verification.json)
passed **248 checks**, including representative payloads, timing, tool shapes,
all prompt versions, datasets, evaluator rules and eighteen renamed experiments.
Original source input/output strings and timestamps were preserved.

## Live and offline verification

A two-turn Sonnet conversation produced sixteen native evaluator results, plus
one thumbs-up and one thumbs-down with their written comments, each attached to
the correct request root. A fee turn used Opus and recorded a real retrieval and
`calculate-fee` application tool. After the generation-only clarification, a
new Opus application-guide turn showed the exact native `applications/guide` v7
link and no duplicate root prompt fields. Earlier real test records are preserved.
See [live feedback evidence](evidence/operational-live-feedback.json) and
[native generation screenshot](evidence/operational-generation-prompt.png).

Offline: **273 tests passed**; manifest validation and every conformance check
passed. The prototype checks and production build passed. The golden was frozen
only after fresh-process repeatability passed for the deliberate content changes.
The [local container smoke](evidence/operational-container-smoke.json) verifies
installed modules/assets/runbook, all three fixture HTTP journeys and feedback
under a non-root, read-only, network-isolated execution without credentials.

## Depot boundary

The manifest exposes `generation.target_traces` as its only volume control,
defaulting to 1,620 historical traces. Nine prompt families, eight opening versions,
nine datasets and eighteen experiment examples remain fixed. It defines the
seed/verify pipeline, presenter runbook, companion command/health route and secrets.

Local kit checks and this live-project rehearsal do not establish Depot delivery.
Signed release, admission and delivered staging rehearsal remain pending for the
previously recorded [Depot prerequisites](DEPOT_ACCESS.md). No release or public
catalog entry was created in this revision.
