# Final fresh-project seed — 2026-10-09

The user supplied a new blank project for the final run before Depot onboarding.
The credential file is ignored and private; credentials are not part of this evidence.

Target: [`prompt-final-demo`](https://cloud.langfuse.com/project/cmv0kpfl209mmad0kft5wn5h9/prompts),
project `cmv0kpfl209mmad0kft5wn5h9`. Preflight found no observations, prompts,
datasets or LLM connections. Prior projects were not changed.

## Seed and readback

The current kit generated its full population directly, without a history migration
or expansion. Seed 42, target 1,620 historical traces, run anchor
`2026-10-09T12:00:00+00:00`. History covers the preceding 28 complete days.
A separate setup step configured the authorized Anthropic connection and ten
Sonnet 5.5 evaluators with ten production rules; seed itself remained model-free.
The spool was imported exactly once and the durable state is `imported`.

- Nine prompts, 72 versions; production v7 and development v8.
- Nine datasets with 32 cases; eighteen historical experiment examples.
- 1,638 traces, 5,137 observations and 9,356 authored scores.
- 2,118 generations: 1,038 Sonnet 5.5, 720 Opus 5.5 and 360 Fable 5.1.
- Every generation has its native prompt association; roots have no redundant prompt references.
- Operational names, original model IDs, explicit historical costs and replay exclusion
  from online judges all match the spool. No asset-setup gaps remain.

Spool SHA-256: `ac7e97af87650183b730ed85fd1869a8ac698bd1ae2db6841533bacd9c720a6d`.
Private reproducibility state/spool: `.scratch/final-seed-state/`.
This canonical fresh run has 13 fewer observations than the previous same-project
replacement, whose combined incremental history was intentionally preserved; trace,
generation and score counts are unchanged. Exact current-spool verification is authoritative.

[Exhaustive inventory](evidence/final-seed-inventory.json) passed with zero failures.
[Scenario verification](evidence/final-seed-verification.json) passed **266/266 checks**.
The delivered presenter runbook is in `.scratch/final-seed-artifacts/DEMO_SCRIPT.md`.
The unchanged implementation previously passed 273 tests, manifest validation and all
conformance gates, with local container evidence in the operational revision report.

## Live verification and UI

The companion at `http://127.0.0.1:8776` uses this final target. A real two-turn
Sonnet conversation produced sixteen native evaluator outcomes: input checks on each
request root and reply checks on each generation. A thumbs-up and a thumbs-down,
with comments, were read back as BOOLEAN `user-thumbs` scores on their correct roots.
Both generations resolve `products/explainer` v7; root prompt reference fields are absent.

[Live session](https://cloud.langfuse.com/project/cmv0kpfl209mmad0kft5wn5h9/sessions/conversation-7564fc8b84aa408f86694c4b9bf367ae)
· [Live evidence](evidence/final-seed-live.json).
These two actual requests and their scores are additional to the seed counts above.

Protected `production` was enabled through the native project settings and visually
confirmed. This establishes configuration; it does not repeat the earlier separate
member-versus-admin enforcement test in this new project.
[Protection screenshot](evidence/final-seed-protected-label.png).
The native prompt metrics page visibly shows all eight versions, historical latency,
cost and factual-quality distributions, plus the two new live outcomes.
[Metrics screenshot](evidence/final-seed-prompt-metrics.png).

No prompt version was promoted during this final seed check; the opening story state
is intact. A new intervention experiment and delivered Depot rehearsal were not run here.

## Onboarding boundary

The final seed and live checks pass. They do not establish Depot admission or publication.
[The refreshed Depot access report](DEPOT_ACCESS.md#recheck-on-2026-10-09-before-final-onboarding)
records the running deployment prerequisites. This project now contains the final demo
and must not be reused as a blank admission scratch target. Release, admission, staging
rehearsal and shipping remain separate pending steps.
