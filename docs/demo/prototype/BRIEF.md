# Prompt portfolio prototype

Prepared 2026-10-08. **Accepted for authoring on 2026-10-08.**
Input: [accepted story](../story/STORY_BRIEF.md) and D-01–D-31 in its contract.
The user reviewed the prototype, accepted it with “Looks good hand off to authoring”,
and requested the complete kit while preserving the prototype and story.

## Question and audience

Can a presenter move from an established prompt portfolio through an experiment
and admin promotion to a chatbot conversation with inspectable version provenance
and both evaluation tracks? Audience: prompt owners and AI application/platform
engineers. The business problem is managing a growing prompt portfolio and
understanding changes. Ongoing improvement is the cause of the intervention;
there is no invented opening incident or required failing prompt.

The intervention changes PR-01's speaking style, holding product truth, question,
history, model placeholder and rubric fixed. The payoff is a changed reply,
followed by a session that exposes what the assistant said and what it heard.
Presenter discretion remains decisive even with disappointing scores.

## Delivered surfaces

| Surface | Reviewable behaviour | Fidelity |
| --- | --- | --- |
| Prompt portfolio | Nine searchable families; eight opening versions each; purposes, live/history split, task datasets, uneven usage and synthetic cost differences | Local simulation; actual native prompt UI not copied |
| Main prompt | Exact v7/v9 system text, staged editor, immutable saved version, labels, version intent, source/context and eight examples | Local simulation; older complete text is an identified storyboard |
| Metrics | PR-01 version use, cost from usage/prices, median latency, numeric medians/coverage and factual-check category counts; secondary current-version costs | Authored aggregate preview, not derived from representative traces |
| Experiment | Two runs × eight cases × four output criteria; inspect paired outputs, reasons and controls; expected/mixed/flat scenarios; pending state | Authored outcomes, no judge/model execution |
| Promotion | Member rejected; admin allowed independent of scores; old calls retain versions | Simulated roles; no native security verification |
| Companion | Three chatbots, scripted replies, feedback, fresh conversations, explicit fetch/evaluation completion controls | Local simulation; no account actions or live LLM |
| Session | Four-turn reference plus locally created sessions; ordered messages once; root/reply links, score chips and identity | Custom session adaptation; not native replay parity |
| Trace | Expand/collapse, select operations, type rows and scores | Actual pinned Langfuse tree, row/type and score components |
| Trace detail | Role-aware I/O, system disclosure, raw JSON, evaluator context, prompt/model and score reasons | Local inspector, not upstream detail composition |
| Story & coverage | Connected steps, unique record counts, definitions, actual targets, zero-score features and authored population | Local review surface |

The primary presenter entry is prompts, preserving the accepted exception to the
skill's generic companion-first entry. A direct `?view=companion` entry is supplied.
Three reversible companion layouts compare left bot navigation, centred chat tabs,
and right context. The default is left navigation. Layout selection is not yet
accepted by the user. No separate companion sentiment dashboard was added.

## Shared model and concrete examples

- [Model/state transitions](../../../design/prototype/src/model.mjs) own all local
  traces, scores, promotion state, experiment runs and feedback targets.
- [Copied packet fixtures](../../../design/prototype/src/data/) retain incoming
  source/case/prompt IDs and exact original examples. Provenance hashes identify
  the authoritative packet inputs.
- [Eight supplemental dataset items](../../../design/prototype/src/data/dataset-extras.json)
  add PX-02–PX-09, one missing-information example for each secondary family.
  Alongside the supplied normal/control pairs, every secondary dataset has three
  inspectable items. These are prototype-authored extensions, not user decisions
  or generated data. They do not alter source truth.
- [Population preview](../../../design/prototype/src/population.mjs) holds authored
  aggregates separately from the representative traces. Current-version average
  token usage for secondary prompts is a prototype assumption; prices/model labels
  come from the story's fictional accounting contract.

Initial evidence: **24 traces, 51 observations, 137 numeric/categorical outcomes and
12 active criterion definitions**. The thirteenth planned definition is optional
customer feedback; it has no record until used. One completed comparison adds
16 traces and 64 outcomes. A four-turn PR-01 chat adds eight observations and 32
outcomes (16 input, 16 reply), plus feedback if supplied. Repeated runs get unique
IDs; coverage retains previous runs. Authored E-02/E-03 values 1/0/null map to Pass/Fail/Not applicable. Category
counts replace their numeric averages/medians; execution status remains separate.

Root input scores E-05–E-08 do not migrate to selected generations. Output scores
E-01–E-04 belong to the answering generation. Both targets carry the current
message and appropriate prior context; output targets also carry the actual source
record and answer. Live judges must not depend on offline expected answers.

## Operation and session boundaries

APP-01/02/03 own their request root and answer generation. Each reply returns a
trace ID and explicit root/generation IDs; the whole conversation has one session.
Every observation carries that session ID. A fresh conversation gets a new one.
The replay displays only new user/assistant messages once, while generation input
retains its system message, reference context and earlier turns.

FLOW-01 is an APP-04 historical simulation: OP-04 intent → OP-05 query rewrite →
SIM-LOOKUP reference tool → OP-09 handoff. Three generations link PR-04/05/09 v7
independently; the tool has no invented prompt. No live APP-04 runtime is promised.

Customer feedback is explicitly attached to the saved reply's **request root**,
with a stable ID per request. Updating its value/comment replaces that record.
Selecting another turn or layout cannot retarget it. This is distinct from a
managed judge of the reply generation and distinct from a session-level score.

The prototype resolves production on every simulated request (TTL 0). It snapshots
the version into the saved generation. A pending request keeps the version it
already resolved if production changes before its reply. Authoring must prove a
real refresh policy and actual fetch/version linkage.

## Population carried forward

The story's 28 complete local days, 360 conversations, 216 users, 1,080 chat turns,
1,620 traces, 2,100 prompt-linked generations and 9,320 planned outcomes remain
unchanged. Day/hour arrivals and 2/3/5-turn distributions reconcile separately.
History is dated before D0; experiments, controls, reference session and new demo
chat remain separate cohorts. Human gaps are independent of generation duration.

PR-02's 6/80 → 12/80 disagreement example is an explicitly authored aggregate,
with 100% eligible coverage in each seven-day window. A link to C-05 explains the
signal but does not claim that this PR-01 example belongs to that PR-02 cohort.
Synthetic token prices are not live vendor quotes or runnable model identifiers.

## Incoming questions: results and limits

| Question | Prototype finding | Remaining verification |
| --- | --- | --- |
| Q-01 prompt score metrics | Generation targets and rubric-specific N/coverage are coherent; input metrics stay separate | Native prompt metrics aggregation requires live UI/API readback; local table is not proof |
| Q-02 session evidence | Session → exact root/generation navigation works; history is not duplicated | Exact native per-bubble score presentation remains unverified |
| Q-03 evaluator equivalence | Logical mappings use current_user_message, prior_messages, reference_context, assistant_reply on each target | Confirm actual managed evaluator mappings and experimentDatasetId on the chosen server |
| Q-04 prompt refresh | Per-request resolution, pending state, preserved old versions and new session work locally | Real SDK/cache configuration and generation prompt linkage |
| Q-05 protected labels | Simulated member denial/admin success works even after a poor score | Enterprise plan, native role/API boundary; no four-eyes claim |
| Q-06 portfolio/layout | Nine prompts and three usable chatbots; three layouts share state | User preference and presenter acceptance |
| Q-07 input signals | Explicit correction, contradiction, quoted profanity and direct disagreement are distinguishable | Judge calibration and live accuracy; no sentiment/causality claim |
| Q-08 coverage | Unique IDs and actual target links reconcile, including feedback and reruns | Persisted Langfuse ingestion/readback for the actual kit |

## Source and visual provenance

Langfuse source revision **9aca47c2b2879677122712b9a97f2f27f270a1f5**.
Sixteen unchanged upstream files are hash-verified in the check command. MIT
notices are preserved. The existing local fixture harness provided the reuse
starting point; its application-specific code/data were not retained.
[PROVENANCE.json](PROVENANCE.json) separates unchanged files, local provider
stubs, inspected message sources and source hashes. [The source receipt](../../../design/prototype/vendor/langfuse/provenance.json)
contains individual upstream hashes.

The native theme declarations are retained with root/dark selectors scoped to
`.native-scope`. Brand CSS is the actual skill snapshot. Inter and Geist Mono are
loaded from local licensed font files. **Space Grotesk substitutes for F37 Analog**,
which was unavailable. Dark small text uses the brand secondary colour for contrast.
No exact website or complete native-view parity is claimed.

Tree rows omit comment hover buttons at the provider boundary because the pinned
row composition nests them inside another button. Full comments remain in the
selected observation's actual ScoreBadge and local record inspector. Upstream
files stay unchanged. The local hover-card adapter is deliberately lightweight.
The upstream virtualiser emits a non-blocking smooth-scroll warning on selection.

## Authoring boundary

After prototype acceptance and a separate build request, hand this packet to
`author-langfuse-demo-kit`. Preserve examples, prompt/session links, both eval
tracks, discretion over promotion and the population contract. Prove live prompt
fetch, authorised label changes, real model output, session ingestion, evaluator
execution/calibration and score readback. Select actual supported model/server/SDK
versions then; MODEL-BASE is intentionally not a runnable model ID here.
