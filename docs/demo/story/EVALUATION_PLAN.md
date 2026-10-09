# Evaluation plan

Status: **proposed details for review**, implementing user-accepted categories.
E-02/E-03 use categorical rubric revision `r2`; all other definitions remain
revision `r1`. The factual criteria retain their semantic meaning. The user accepted
the two parallel tracks and the playful style direction; these thresholds, mappings and examples
are authoring proposals, not measured evaluator reliability.

## Two tracks and explicit subjects

**What the chatbot says:** E-01–E-04 evaluate the reply generation. Store the actual
resolved prompt reference on that generation, with the current question, supplied
reference record and necessary history accessible to its evaluator.

**What the chatbot hears:** E-05–E-08 evaluate the request root's current user
message, with prior user statements and the preceding assistant reply available
on that same observation. These are required for live use, alongside output
checks. They reveal disagreement, contradiction, expressed frustration and
profanity over time in Langfuse; no separate companion dashboard is requested.

The session is the navigation and conversation-replay surface. Each request has
its own trace/root and generation; scores identify the particular observation.
A session does not turn all those records into a single session-level judge.
The exact native mapping/UI must be verified as described in
[product research](PRODUCT_RESEARCH.md).

## Explicit user feedback

Each saved companion reply can receive one final `user-thumbs` score with explicit
`BOOLEAN` type: `1` for thumbs up or `0` for thumbs down, and an optional written
comment. It targets that reply's saved request-root observation ID with trace
correlation. An identical retry reuses the same score; changing the selected turn
cannot retarget it. No feedback is inferred when the user does not submit it.

This direct user signal is separate from E-08 `user_disagreement`, which infers
whether the incoming message challenges the preceding answer. Neither signal by
itself establishes factual error. Explicit feedback adds no automatic judge call
and is outside the fixed evaluator outcome counts below. See
[the feedback policy](MODEL_POLICY.md).

## Rubrics and producers

Managed LLM judges are proposed for E-01–E-08 because their criteria concern
natural-language meaning and tone. E-02/E-03 return one categorical value; other
criteria return a numeric value. Each includes a short reason referencing the
actual relevant text. Calibrate against the positive and
negative authored examples before authoring claims about reliability. Pin rubric
revision and judge model/settings for comparisons; never infer reliability from
these illustrative expected scores. All managed judge connections and experiment
runs use `claude-sonnet-5-5` under [the model policy](MODEL_POLICY.md).

| ID / stored name | Subject | Range and explicit rule | Required evidence |
| --- | --- | --- | --- |
| E-01 / `dark_side_delivery` | Reply generation | 0 = ordinary voice; 0.5 = isolated theatrical wording; 1 = recognisable space-villain delivery using short commanding phrasing and theatrical language, with at most one restrained space metaphor. Do not require a named character or exact quote. | Reply and this fixed rubric. |
| E-02 / `record_fidelity` | Reply generation | Pass = answers the requested factual issue accurately and retains material conditions; Fail = wrong amount/condition, material omission, unsupported financial assertion or failure to answer an answerable factual question. Not applicable only if no factual issue is applicable. Honest uncertainty passes when the record genuinely lacks the answer. | Current question, supplied record, relevant prior turns and reply. |
| E-03 / `claim_support` | Reply generation | Pass = every substantive product/action claim is supported by the supplied record; Fail = at least one unsupported claim. Not applicable if there are no substantive claims. An explicit statement that the record lacks information is judged against the record. Metaphors do not count as financial facts. | The same record actually supplied to the answering model, reply and question. |
| E-04 / `respectful_tone` | Reply generation | 1 = no personal insult, threat, contempt or mockery directed at the user; 0 = any such behaviour. A theatrical voice and firm factual correction can pass. This is not a general friendliness or competence score. | Reply and preceding conversational context. |
| E-05 / `user_contradiction` | Request root | 1 = current factual self-report conflicts with an earlier user statement about the same situation without acknowledging a correction; 0 = no conflict, no relevant earlier statement, explicit correction, or a hypothetical. Treat changed preferences as updates. | Current user message and prior user statements, with sufficient surrounding context. |
| E-06 / `expressed_frustration` | Request root | 1 = current user wording explicitly expresses frustration/agitation; 0 = absent, neutral disagreement or merely quoting another person's frustration. This describes language, not a person's mental state. | Current user message and context needed to resolve quotations. |
| E-07 / `user_profanity` | Request root | 1 = an actual profanity occurs in the current message, including a quotation; 0 = none. Mentioning the concept of swearing is not profanity. Retain comment `quoted` or `direct` so presence is not confused with abuse. | Current user message only. |
| E-08 / `user_disagreement` | Request root | 1 = user challenges, rejects or corrects a preceding assistant assertion; 0 = a neutral new question, agreement, or correction solely of the user's own earlier statement. It does not prove the assistant was wrong. | Current message and relevant preceding assistant response. |

E-02 judges whether the answer gets the requested facts right; E-03 judges whether
its claims are supported. They can overlap, but remain interpretable separately:
a fully supported answer can omit an important qualification and fail E-02.
Never combine the dimensions into a single universal quality average.

E-02/E-03 use exactly `Pass`, `Fail`, `Not applicable` as single-match
`CATEGORICAL` results in history, experiments and live chats. The user approved
this representation on 2026-10-08 (see [review](REVIEW.md)); the semantic criteria,
stable names and IDs remain unchanged. Existing authored case values are retained
as calibration labels and mapped explicitly: `1` → `Pass`, `0` → `Fail`,
`null` → `Not applicable`. These labels are never live applicability heuristics.
A completed `Not applicable` result is distinct from pending, missing or errored
execution. Report the three category counts and completed/target coverage for
each criterion; do not compute a numeric average or median for these categories.

Native managed judges support categorical outputs with allowed labels; use the
same output definition across observation and experiment evaluation. Deployment
and actual outcome readback still require verification.
[Langfuse managed judge documentation](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge).

For remaining historical-only tasks:

| ID / name | Producer and range | Rule and evidence |
| --- | --- | --- |
| E-09 / `intent_correct` | Deterministic, 0/1 | Compare selected intent to the authored case label. Exact correctness needs the case truth; allowed-label validity alone is not this score. Applies to labelled historical/experiment cases, no live classifier is promised. |
| E-10 / `query_constraints_preserved` | Managed judge, 0/1 | Every material entity, amount, deposit type and period in the question survives the query; no new constraint added. Give the judge question and query. |
| E-11 / `handoff_fidelity` | Managed judge, 0/1 | Summary/note accurately preserves material source facts, acknowledged corrections, uncertainty and unresolved work without inventing actions. Give it the actual source conversation/record and output. |
| E-12 / `extraction_match` | Deterministic, 0/1 | Parsed fields equal the authored expected object, including null missing fields; ignore JSON key order. This is semantic field correctness, not JSON-validity checking. Applies to labelled historical/experiment cases only. |

All these are application-specific criteria. PR-02 and PR-03 reuse the applicable
record/grounding/tone and input rubrics; the playful rubric is only on PR-01.
Source facts for each case live in the case files, not in hidden judge knowledge.

## Score examples and controls

[Main cases](cases/product-explainer.json) provide expected scores and complete
input/output examples. They are authored labels for review and calibration.

- C-01: baseline E-01=0; styled candidate E-01=1; both E-02/E-03=Pass and E-04=1.
- C-02 versus CTRL-01: wrong waiver eligibility fails E-02/E-03 even with E-01=1.
- C-03 versus CTRL-02: acknowledging absent overdraft terms passes; invented rate fails.
- C-04: explicit correction is E-05=0 and E-08=0.
- C-05: disagreement, frustration and direct profanity are each 1; respectful reply E-04=1.
- C-06: incompatible, unacknowledged age statement is E-05=1. Reply asks for clarification.
- C-07: quoted profanity E-07=1, with `quoted` explanation, but E-06=0.
- CTRL-03: insulting the user fails E-04; response completeness and grounding are judged separately.

In actual experiments and live interactions, report the real returned scores and
comments. If a judge differs from the expected label, show that disagreement;
there is no requirement to retry until the judge agrees.

## Experiment/live equivalence and counts

DS-01/r1 has eight cases. Baseline v7 and candidate v9 use identical cases, source
records, histories, model/settings and rubrics. Four output evaluations per case
produce up to **64 numeric/categorical evaluation outcomes** across the two runs:
8 cases × 2 runs × 4 definitions. Not applicable is a completed factual-check
category, never a pass. Record execution completion and applicability separately.
Main experiment input checks are optional and are not included in this output count.

SESSION-01 has four turns. Four root input evaluations and four generation output
evaluations per turn produce **32 outcomes**: 16 input, 16 output. If any are
pending, unavailable or failed, disclose that status rather than
filling in synthetic values. A retry may create another execution attempt; the
metric view selects one resolved outcome per `(criterion revision, target)`.

The same rubric can be reused with explicit field mappings. Live judges use
current-message, actual reference-context and conversation-history fields; they
must not depend on an experiment's expected output or offline-only item metadata.
Mapping names are a prototype/API verification task. The story's equivalent
logical payload is:

- `current_user_message`: only the current input, never an accidental full concatenation;
- `prior_messages`: prior messages with roles; available on the evaluation subject;
- `reference_context`: exactly the source facts the answer generation received;
- `assistant_reply`: actual generated response, for output checks only.

Expose subject intent in filtering metadata (`evaluation_subject=user_input` on
roots; `evaluation_subject=assistant_reply` on reply generations). Also retain
application ID, prompt name, resolved version and environment for correlation.
Those are proposed metadata fields, not invented Langfuse API fields. Input
checks must not double-score both root and generation; evaluator generations
must not recursively match the chatbot filters.

## Presenter discretion and visibility

User-message trends are a distinct required story discovery. Identical inputs in
a controlled experiment keep the same expected input labels; the new prompt does
not magically improve what it was given. A real later user message can change.

The presenter decides what to do with observed experiment results and whether to
promote. There is no automatic release gate, required threshold or mandatory
revision loop. A higher style score with stable serious checks is illustrative,
not required for demo success. Never manufacture improved live scores.

For numeric criteria, prompt metrics document median score values. E-02/E-03
need category counts; exact root/generation score
visibility and rollup need verification. Keep output scores on the generation
that used the prompt. Do not copy input scores there just to make a chart work.
Use a native score or observation view for input trends when necessary, filtered
by the recorded agent/prompt metadata. In the session view, navigate to observation
score detail if per-message score badges or reasoning are unavailable.
