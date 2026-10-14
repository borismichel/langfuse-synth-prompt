# Python SDK v5 candidate — 2026-10-14

Depot issue [#322](https://github.com/borismichel/langfuse-demo-depot/issues/322)
requests this maintenance of the accepted Prompt package. Candidate 0.2.7 pins
Langfuse Python SDK **5.0.1** and released synth-core **v5.0.0**, commit
`5f56e75f9a8b5d160ddf54a8fcde380d0d15a205`. Runtime, companion extra,
authoring extra and image publication workflow use that same core release.
The isolated installation resolved those exact versions and passed `pip check`.
The target requirement is Langfuse Cloud or self-hosted Langfuse >=4.59.0.

## Behavior and regression evidence

The v4 workaround serialized `trace_rubric_revisions` before passing it to the
SDK. Under v5, a single decode of exported metadata consequently returned a
string instead of the intended dictionary. Real SDK tests reproduced that
failure on all three connected assistants before the service was changed to
pass the structured dictionary. Observation-scoped rubric maps retain their
separate ownership: `user_input` on the request root and `assistant_reply` on
the generation. The retriever carries the trace-wide inventory without an
evaluation subject or scoped rubric map.

Six real-SDK tests pass against controlled export and HTTP sinks. They verify
single JSON decoding, rubric scope, evaluation subject/mode, complete structured
reference context, root input/output, model usage, and generation-only prompt
association. The feedback test completes two replies, submits the same feedback
for the first reply twice, flushes the actual SDK, and observes exactly one
public `/api/public/scores` record with the saved first root's IDs and the
intended BOOLEAN type, value, comment and score ID. It no longer intercepts a
private SDK score queue. These checks prove exported/delivered requests, not
server ingestion or model quality.

The historical Spool and all accepted story/prototype fixtures are unchanged.
The existing full-payload golden and cross-process repeatability checks remain
the deterministic-history acceptance gate; no fixture was re-blessed.

## Local checks and remaining release work

- Full Python suite: 361 passed, zero skips, including the unchanged golden and
  cross-process repeatability checks.
- All three Node checks pass: reply rendering, chat composer and pending chat.
- Manifest validation and strict contract conformance pass without advisories.
- Golden SHA-256 remains `e4af1b12a746b60f97a90c27edbdc1f4eced6c2edcf8ffab0280bd9fa941f069`.

This is an offline implementation checkpoint ready for review, not new human
acceptance of the story or prototype. Publication, installed-image provenance,
fresh-target admission and the complete Presenter Runbook rehearsal remain
required release milestones. Existing historical evidence documents retain
their original release/version claims and do not establish v5 live success.


## v0.2.7 live regression and v0.2.8 correction — 2026-10-14

The signed v0.2.7 image passed admission and the full seeded asset audit. Two
native eight-case experiments completed with all four reply evaluators, using
fixed v7/v9 prompts, the same dataset snapshot and Sonnet 5.5 settings. The
native experiment mapping already preserves its complete reference record.

The subsequent live chat rehearsal exposed a release-blocking mapping defect.
E-02 and E-03 received an empty reference record on all three connected bots.
Product Explainer turns one and four, Fee Calculator and Application Assistant
received factual failures; turns two and three passed only by using earlier
assistant messages as context. These outcomes are preserved, not rescored.
Correct-looking model replies do not establish a working evaluation pipeline.

The exact SDK 4.17.0 and 5.0.1 exports both serialize the source dictionary in a
per-key OTLP attribute. Cloud treats their versions differently: v4 leaves that
attribute as a string; v5 decodes the structured object before metadata storage.
Storage flattens the latter into literal keys such as
`reference_context.monthly_fee`, so the existing `$.reference_context` selector
has no value. The evaluator parses JSON string leaves before applying JSONPath.

Candidate 0.2.8 preserves the structured `reference_context`, separate scoped
`rubric_revisions`, and structured trace-wide `trace_rubric_revisions`. It adds
only `eval_reference_context`, an intentional JSON string leaf containing the
same complete record, and changes the live reference selector to
`$.eval_reference_context`. Question, history, output, prompt association,
evaluator identities/rubrics and native experiment mappings remain unchanged.
Source datasets, historical Spool and accepted story/prototype inputs are
unchanged. The published v0.2.7 target has not been repaired in place.

The new regression drives the public ConversationService through the real SDK
for two turns on each connected bot. It then models the observed Cloud storage
shape, including v5 preservation of JSON-looking string values and evaluator
leaf parsing, and applies the actual configured selectors. All three cases
failed with missing reference context before the correction and pass with the
complete source record afterward. Existing SDK tests continue to assert root
and generation rubric ownership and prompt association. This is offline
compatibility evidence; a fresh released-image admission and live judge readback
are still required before claiming the correction works in Cloud.

The v0.2.7 rehearsal also verified owner promotion with a protected production
label, four related chat turns, and one BOOLEAN feedback score on the saved
first root. A genuine Member-role denial remains unverified. The UI disables
feedback controls after saving, so duplicate live transport was not exercised;
the existing real-SDK HTTP regression covers repeated earlier-reply feedback.

Primary implementation references (immutable source revision):

- [SDK-gated per-key metadata decoding and JSON-string preservation](https://github.com/langfuse/langfuse/blob/bc1ade0aacca75104bad934e92d70a454ec16e67/packages/shared/src/server/otel/OtelIngestionProcessor.ts#L3635)
- [Evaluator field parsing before JSON selection](https://github.com/langfuse/langfuse/blob/bc1ade0aacca75104bad934e92d70a454ec16e67/packages/shared/src/server/evals/extractObservationVariables.ts#L54)
- [Bounded nested JSON parsing](https://github.com/langfuse/langfuse/blob/bc1ade0aacca75104bad934e92d70a454ec16e67/packages/shared/src/utils/json.ts#L143)

Candidate 0.2.8 offline gates: **364 Python tests pass**, all three Node checks
pass, manifest validation and strict six-gate conformance pass. The unchanged
golden SHA-256 is `e4af1b12a746b60f97a90c27edbdc1f4eced6c2edcf8ffab0280bd9fa941f069`.
The authoring handoff is refreshed as ready for review; story and prototype
acceptance are retained without changes.
