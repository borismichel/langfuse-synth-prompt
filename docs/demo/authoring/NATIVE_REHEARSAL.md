# Native Chrome rehearsal

The fresh 2026-10-09 project, corrected import and bounded live connection check
are recorded in [Fresh project verification](FRESH_PROJECT.md). The earlier
rehearsal below remains preserved against its original target.
On 2026-10-09 the user separately confirmed that protection works; the pending
permission check below is now closed by [user verification](evidence/protected-label-user-verification.json),
without claiming the agent observed that separate test.

Recorded 2026-10-08 in the user's existing authenticated Chrome session.
Target: `prompt-dev-demo` (`cmuzyfy1f0481ad0f7rajddig`), EU Cloud,
Langfuse v4.55.0, Enterprise organization. This supersedes the earlier IAB
sign-in limitation; it does not establish Depot admission readiness.

## Verified native steps

- Opened the refined fee session `prompt-live-1f4d2b384f8b49e091c7d04022a4fb6c`.
  Native chat view shows three turns, one system prompt, and each user/reply once.
- Opened its first turn `ed1b4f04268d9aea69c7d6fdca465280` from the session.
  Tree shows `handle-chat-turn`, `retrieve-product-context`, `calculate-fee`,
  `generate-response`. Four input scores appear on the request root and
  `respectful_tone` on the reply. The generation links to `fees/explainer - v7`,
  model `claude-sonnet-4-6`, and actual token/cost values.
- In native Settings → Protected Labels, added `production` and observed the
  saved protected label. Protection was previously absent. No role was changed.
- Project Members shows the authenticated presenter as owner and a separate
  existing member identity. Member-denial rehearsal has not been performed;
  an owner session cannot establish it.
- Browsed product prompt versions and Metrics. Eight opening versions are present;
  v7 production and v8 development. Past-30-days metrics show seeded v1–v5 usage,
  cost, latency and authored scores plus real v7 traffic/scores. The small pilot
  does not populate every version; no full-history claim is made.
- Saved product v9 from v7 using the exact runbook style addition, preserving
  reference/history/user placeholders, and assigned `staging`. Production remains
  v7 at this checkpoint. This is a rehearsal candidate, not a seed overwrite.
- Native experiment setup validates all eight cases for `reference_context`,
  `conversation_history`, and `user_message`. Selected actual model
  `claude-sonnet-4-6` and the most recent explicit dataset version.

Screenshots: [native session and trace](evidence/native-session-trace.png),
[protected production](evidence/native-protected-production.png),
[prompt metrics](evidence/native-prompt-metrics.png),
[staged candidate](evidence/native-staging-v9.png).

## Approved categorical evaluator change

User approved Pass / Fail / Not applicable for E-02 and E-03. Their two native
managed definitions and live rules were created and read back exactly through the
Langfuse CLI. Existing eight managed definitions/rules were retained. Old numeric
pilot history remains untouched and must not count as categorical seed evidence.

## Corrected native experiment comparison

The first candidate run `cmv01el1b05dcad0j56r61tio` completed but its factual
measurements were invalid: native experiment metadata flattens nested objects,
so the original `$.evaluation_context.*` mappings supplied empty context.
Its actual outputs, scores and reasons remain preserved; it was not deleted or
rewritten. The initial empty results screen was transient loading, not a broken
experiment route.

A shared metadata builder now provides serialized top-level `eval_*` fields.
All 32 dataset items were read before and after the metadata-only repair; their
IDs, inputs and expected outputs are unchanged. Nine evaluator default mappings
were repaired and read back, while live observation mappings remain unchanged.
The four dataset evaluator attachments were reattached to adopt those defaults.
[Repair receipt](evidence/experiment-context-repair.json).

Exactly one corrected run per version used the frozen dataset snapshot
`2026-10-08T21:23:35.546Z`, model `claude-sonnet-4-6`, identical eight item IDs and
versions, and identical four evaluator version IDs:

- Baseline v7: `cmv01r0p10588ad0ker6o0mcf`.
- Candidate v9: `cmv01x3te04vrad0nfxuqhykt`.

| Criterion | v7 | v9 |
| --- | --- | --- |
| Dark-side delivery mean | 0.00 | 0.75 |
| Respectful tone mean | 1.00 | 1.00 |
| Record fidelity | 8 Pass | 8 Pass |
| Claim support | 8 Pass | 8 Pass |

All 16 outputs and 64 EVAL outcomes were read back, including actual generation
prompt/model identity and judge reasons. Candidate C-02 and C-06 retain ordinary
prose and score 0 for theatrical delivery. No retry-until-pass occurred.
[Full evidence](evidence/native-experiments.json) and
[native comparison](evidence/native-corrected-comparison.png).

## Owner promotion

After inspecting the comparison, the authenticated owner selected v9's protected
`production` label and saved the promotion through the native UI. The label moved
from v7 to v9; `staging` remains on v9. No role or protection was weakened.
[Production v9 screenshot](evidence/native-production-v9.png).

The updated local companion is running at `http://127.0.0.1:8771` for the final
multi-turn session rehearsal. It still points at the original pilot, whose legacy
numeric seed receipt is intentionally not rewritten to claim corrected categorical
history. A fresh project/key approval is pending for revised history verification.

## Promoted four-turn session

The companion's primary **Open session** link opened native session
`prompt-live-381cc985538e488295567fdfd65d2a99`. Native chat view contains four
request/reply pairs once each and one system-prompt section. Its third-turn peek
shows a request root with four input scores, the reference retriever, and a reply
generation with four reply scores including categorical `claim_support: Pass`.
The generation links to `products/explainer - v9` and `claude-sonnet-4-6`.

Readback confirms twelve observations, 32 EVAL outcomes, correct parentage,
full ordered history/reference context, and the exact official v9 system text
including the theatrical addition. Actual generation cost totals USD 0.019287.
Both factual criteria return four Passes; respectful tone is 1 on every reply.
The theatrical score is **0 on all four replies**, despite the instruction being
present. Promotion retrieval works, but this live run does not demonstrate a
successful audible style change. This limitation is preserved for the presenter;
there was no quality-driven retry or score gate.

The explicit correction in turn two was incorrectly flagged by the contradiction
and disagreement judges against the accepted rubric. Turn three correctly surfaces
frustration, disagreement and profanity. These are independent input evaluations,
in addition to the reply-quality checks, with no extra companion analysis screen.

The companion displays all eight outcomes for each turn. Its connection warning
still reflects the old pilot provisioning receipt, which lacks the two newly
configured categorical rules; this receipt has not been falsified. A fresh target
is needed for a fully current history/configuration receipt.

[Complete readback](evidence/categorical-live-session.json),
[companion outcomes](evidence/categorical-live-companion.png),
[native session](evidence/categorical-native-session.png),
[native trace and prompt link](evidence/categorical-native-trace.png).

## Final provenance refinement

Review found that the captured traces' umbrella `rubric_revision: r1` no longer
expresses the mixed criterion revisions accurately. The implementation now derives
per-criterion `rubric_revisions` from definitions, scoped to each evaluation subject.
E-02/E-03 are r2, other criteria r1. Existing recorded traces and judge results are
preserved; this metadata-only refinement is verified locally and does not change
rule matching, model requests, score targets or the recorded experiment comparison.

## Application-guide verification — final implementation checkpoint

The third companion was exercised from the actual UI at `http://127.0.0.1:8772`
using implementation commit `99a4caf`. Its two-turn native session is
`prompt-live-b77a310e4bb546ae9c88f9a240b6b550`. It rejects proof of address dated
five months ago and declines to claim access to application approval status.
The primary link opens a native session with two request/reply pairs once each.

Readback confirms applications/guide v7, the actual selected model, six observations
(two roots, two retrievers, two generations) and fourteen EVAL outcomes, all on the
correct input/reply targets. Both factual checks passed both turns and tone is 1;
all input flags are zero. The replies also add general document examples and provider
capability suggestions absent from the record. The judges accepted those caveats;
the original outputs and reasoning are retained as calibration concerns.

This check exposed a real provenance defect: readback shows the full trace-level
rubric map on every observation, as a Python-representation string, instead of the
intended subject-scoped maps. Actual evaluation subjects and context remain correct.
The preceding local-only provenance result is therefore insufficient; an adapter-level
repair and another bounded live metadata check are required before closing this issue.

[Actual readback](evidence/application-guide-live.json),
[companion outcomes](evidence/application-guide-companion.png),
[native two-turn session](evidence/application-guide-session.png).

## Rubric propagation repair — verified live

The actual SDK/export regression and public ingestion code confirmed two causes:
trace metadata takes precedence over observation metadata with the same key, and
SDK trace propagation converts a dictionary with Python `str()`. The kit now uses
a distinct `trace_rubric_revisions` JSON field for the complete inventory and keeps
`rubric_revisions` scoped to the observation. No core or Langfuse source was changed.
Readback accepts a structured map or valid JSON; old Python-representation strings
and the wrong full map are rejected.

One bounded post-fix application-guide turn produced session
`prompt-live-629a9fe5f85943d8a326e281b6b24958`. Its actual readback verifies:

- Root: E-05–E-08 r1 map and `evaluation_subject=user_input`.
- Generation: E-02/E-03 r2 plus E-04 r1 map and `assistant_reply` subject.
- Retriever: no observation rubric map or evaluation subject.
- All three observations: separate complete trace inventory decoded as JSON.
- Seven EVAL outcomes correctly targeted, applications/guide v7 and the actual model.

This follow-up repaired instrumentation, not answer quality. The original two-turn
session and all judge decisions remain intact. General document examples still
appear in the new answer and the judge accepts the caveat; that limitation remains.
[Corrected live evidence](evidence/application-guide-metadata-fixed.json),
[companion readback](evidence/application-guide-fixed-companion.png), and
[adapter-level diagnosis](evidence/rubric-propagation.json).
