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
