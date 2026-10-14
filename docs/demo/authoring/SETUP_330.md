# Inclusive schedule and wizard configuration — Depot #330

Candidate Prompt 0.2.6 uses released core v4.3.0 (ba4a4a276079ed49865becffc7955acde148147a). Runtime, companion extra, authoring extra and publishing workflow were repinned with `synth-authoring repin`. SDK 4.17.0 and the existing main-branch prompt retrieval/variable companion example remain unchanged.

## Date convention

The fixed history is 28 Europe/Berlin calendar days **including** the selected as-of date: D−27 through D0. The accepted portfolio fixtures retain their original authored D−28 through D−1 era definitions. Materialization translates those eras forward one calendar day, including historical experiment placements, so ordering and each version's duration remain coherent. The latest production version therefore covers the selected day. The first task is on D0 even on weekends; a single-trace Custom run also includes D0. Weekday/weekend scheduling otherwise retains its existing allocation.

Generation derives local midnight boundaries independently, preserving 23/25-hour DST days. Tests inspect every finalized observation start and end, not just root timestamps. They cover future Friday 16 October, weekend 18 October, both DST transitions, leap day, year rollover, minimum Custom volume and the 6000-trace maximum with seed60 on the autumn DST date. No emitted endpoint escapes the inclusive range.

`SCHEDULE.json` records the requested date, 28-day constraint, timezone and actual generated bounds. It is delivered beside the runbook and retained in the receipt, including the existing authorized expansion path. It is never a fabricated nominal range.

## Presentation, Quick rehearsal and Custom

Presentation remains 1620 production traces. Quick rehearsal is an authored 270-production-trace preset, with all nine prompt families represented across the seven production request types. The fixed 18 historical experiment traces (nine v2, nine v4) remain separate, as do nine datasets, their items, prompt versions and reusable building blocks. Custom preserves the declared1–6000 volume range, integer seed, judge connection name and provider model ID. Very small Custom volumes can omit production families; the form states this. Provider connection names are configuration, never credentials. Existing model validation and secret-bound evaluator setup remain authoritative.

Real seed/readback evidence for16October2026, seed42:

| Mode | Production traces | Total traces | Generations | Scores | Actual UTC bounds |
|---|---:|---:|---:|---:|---|
| Quick rehearsal |270|288|368|1590|19Sep04:18:09 –16Oct16:19:16.129|
| Presentation |1620|1638|2118|9356|19Sep01:28:23 –16Oct18:09:30.913|

[Machine-readable generation evidence](setup-330/generation.json) retains exact timestamps. Tests run the real seed and project its emitted Spool into the existing public core reader interface, then run the existing per-trace verifier for the persisted representative records. They assert all nine families and fixed experiment versions independently. This proves offline emitted-data/readback agreement, not remote ingestion or paid judge execution. Existing asset/provider tests separately preserve real validation behavior.

## Golden review

The reviewed chronology update preserves42traces,113observations,174scores, all observation IDs, operation-name counts and score values in the24-production-trace golden. Dates and production-era associations move consistently with the new inclusive convention. [Golden inventory comparison](setup-330/golden-review.json). The golden was regenerated with the core freeze command after the independent process-hash-seed repeatability gate passed; accepted story/prototype files were not rewritten.

## Verification and delivery status

- **Passed:** strict authoring check reports `local_ready:true`: manifest validation, conformance and362tests. An additional maximum-volume/date-bound test passed after that complete check; current suite contains363tests. All three existing JavaScript companion checks also pass. [Check receipt](setup-330/offline-check.json).
- **Passed:** authenticated Depot fixture on localhost4340, future date and fixed history; Custom450/seed17/provider connection/model; selected co-presenter; save/resume and review; launch reaches the existing plan approval and confirmation. Two route tests cover rehearsal and Custom independently. Desktop1280×900 and mobile390×844, light/dark captures are in Depot `design/demo-wizard-324/330/`. No portal slug branch or visual-style change was introduced. Fixture estimate12000 and successful post-approval state are test-boundary responses, not this kit's actual measured output.
- **Preserved:** accepted upstream story/prototype, original provider/model policy, native version/label semantics and probe→plan(confirm)→configure-evaluators→seed→configure-experiments→verify pipeline. This change does not rerun prior live companion/label-protection evidence.
- **Pending:** independent release review, immutable0.2.6 source tag, signed image and Depot registry consumption are coordinated by the implementation root. No release or production deployment is claimed here. Existing-kit updates follow the normal reviewed release path; no new-kit scratch admission was performed.
- **Not run:** live seed/readback, provider calls, deployed-image runtime/admission or delivered companion rehearsal for this candidate. Prior0.2.5live evidence is historical, not relabelled as0.2.6proof. Container-limit performance at6000retains previous release evidence; this slice rechecks offline data/date bounds at that volume.

Authoring is ready for review, not newly user-accepted. The user requested this work via Depot324; the upstream acceptance files remain untouched.

Langfuse dependency entrypoint SHA256: `e8908ea1c924374ba7bc5e82b220709d107db6a3450a0c4d72228a91a2a7534a`. Current product references checked14October2026: [Prompt version control](https://langfuse.com/docs/prompt-management/features/prompt-version-control) and [LLM-as-a-judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge). No product API/observation modeling change was required.
