# Historical population and metric contract

Status: **accepted fictional story population**, with the model/cost policy amended
on 2026-10-09. These are coverage and consistency requirements, not generated
traffic or statistical claims.

## Cohorts and chronology

Use a movable demo anchor `D0`. Historical production covers the 28 complete
calendar days D-28 through D-1 in Europe/Berlin, converting each local midnight to
UTC separately (DST-safe). `PORTFOLIO.json` owns each prompt's version-use periods.
PR-01 v7 is production on entry; v8 is an unused draft; v9 does not exist until
stage two. No pre-promotion production calls use v9. Moving the label leaves old
generations linked to their actual versions.

Historical production and live companion calls both use environment `production`;
experiments use `experiment`. Separate origin/cohort metadata distinguishes
authored history from real companion calls without changing operational names.
These fields record provenance, not independent security boundaries. Version
labels such as production/staging select prompts and are a separate concept.
Historical inspection filters the authored cohort and its date window, excluding
experiments and new live calls. Experiments use fixed DS-01/r1 and identical
histories across prompt variants. New live chat appears after D0 and remains
recognisable through timestamps and origin metadata.

## Coverage-driven population

Proposed compact story population: 360 historical customer conversations with
1,080 reply turns across the three chatbot families. Every conversation has a
fictional stable user ID, session ID and per-turn request ID. 216 distinct users:
144 have one conversation, 72 have three (144 + 216 = 360). No real identities.

| Prompt | Conversations | Reply turns | Reason for share |
| --- | ---: | ---: | --- |
| PR-01 product explainer | 180 | 540 | Main entry point and presenter focus |
| PR-02 fee explainer | 108 | 325 | Smaller, frequent bounded fee questions |
| PR-03 application guide | 72 | 215 | Less frequent document follow-up |

Use approximately 40% two-turn, 40% three-turn and 20% five-turn conversations,
with exact integer allocations: PR-01 has 72×2 + 72×3 + 36×5 = 540 turns;
PR-02 has 43×2 + 43×3 + 22×5 = 325; PR-03 has 29×2 + 29×3 + 14×5 = 215.
These sum to 360 conversations and 1,080 turns. Each live session uses one primary
chatbot; the historical multi-prompt flow below has a different application shape.

Additional historical-only work:

- 240 APP-04 request reviews, each with OP-04 intent, OP-05 query rewrite, simulated
  reference lookup and OP-09 handoff. This adds 720 prompt-linked generations.
- 120 APP-05 summaries, 80 APP-06 extractions, 100 APP-07 messages: 300 generations.
- Total planned history: **1,620 request traces and 2,100 prompt-linked generations**.
  Root/tool observations add to total observation count; do not equate traces,
  generations and all observations.

These volumes provide a legible prototype population preview and a later seed
brief. They do not justify significance claims. The prototype authors a small
representative sample and explicitly labelled aggregate previews; it does not
build all 2,100 generations. Authoring scales only `generation.target_traces`,
preserving accepted proportions, coverage, session timing and relationships. The
asset inventory stays fixed: nine prompt families, eight opening versions each,
nine datasets and eighteen historical experiment examples. Trace scaling neither
adds prompt families/versions nor multiplies the historical experiment cohort.

## Variation and time

Consumer chat uses a broad daily curve: 25% 00:00–09:00, 40% 09:00–17:00, 35%
17:00–24:00 local, with 25% of conversations on weekends. Internal historical work
runs predominantly during weekday 09:00–18:00, reflecting internal teams. These
are synthetic patterns, not observations about a customer. Each active version
has enough cases to show metric and score coverage; use unequal counts proportional
to its usage interval and its application volume, not equal counts per version.

Human gaps are 15–120 seconds in ordinary conversations, with a minority of
5–20 minute resumptions. Server generation latency is separate. Increasing seed
volume must not shorten human gaps or convert them into model latency. Reference
SESSION-01 gives one concrete chronology.

Case mix for PR-01: waiver questions 35%, fee/allowance questions 25%, opening
requirements 20%, missing terms/action boundaries 20%. Cover qualifying and
nonqualifying deposits, explicit corrections, disagreement, quoted profanity,
and ordinary friendly questions. Inputs containing profanity must also include
some calm quotations so the input dimensions are not identical.

## Metric definitions

| Metric | Definition and denominator | Missing data and comparison |
| --- | --- | --- |
| Total token cost | Sum recorded generation cost in USD for the selected application/version/environment and window | Exclude missing prices from sum and report priced-generation coverage; do not treat missing as free |
| Cost per generation | Sum cost / count of generations with complete usage and pricing | Compare same task cohorts; more traffic changes total cost independently |
| Request cost | Sum all model/evaluator costs attributed to that request, explicitly separated from answer-only cost | Keep judge cost separate if it is outside the native prompt metric |
| Generation latency | Generation start-to-end duration; show native median in prompt view, optional p95 in a suitable native view | Exclude missing/invalid durations; not time between user messages |
| Output quality/style | Numeric criteria: per-criterion values on completed reply generations. E-02/E-03: separate Pass, Fail and Not applicable counts | Display completed/target coverage; never average or take medians of factual-check categories |
| User disagreement rate | E-08=1 / completed applicable E-08 root scores in the selected cohort/window | Also show eligible user-turn count and coverage; one input outcome per turn |
| User frustration/profanity/contradiction | Same fraction with the respective root criterion | Report separately; rates may overlap; they must not sum to 100% |
| Experiment comparison | Per-case baseline/candidate outputs and scores on the exact same dataset version | Preserve case pairing, show pending/failed execution and completed Not applicable categories and sample size; no production-prevalence claim |

For a seven-day trend compare D-14..D-8 and D-7..D-1, same application and input
cohort, reporting denominators for both. Example authored aggregates for a preview:
PR-02 disagreements 6/80 then 12/80, with 100% eligible coverage in each window.
This illustrates a reason to investigate; it does not prove the prompt caused the
increase. Keep these preview numbers distinct from any computed fixture metric.

## Prices and improvement story

[MODEL_POLICY.md](MODEL_POLICY.md) and the canonical executable policy define the
real Anthropic model IDs by role: Sonnet 5.5, Opus 5.5 and Fable 5.1. Historical
production uses that role mapping; all historical experiment examples use
`claude-sonnet-5-5`. Model registry rates remain normal provider base rates.
Authored history and historical experiment cost details apply an explicit **3×**
multiplier to recorded token usage × those rates, with synthetic provenance.
Never independently randomise token counts and costs.

Illustrative PR-01 Sonnet 5.5 examples at $2 input/$10 output per million tokens,
including the 3× historical multiplier:

- Earlier prompt: 800 input + 240 output tokens -> USD 0.01200/generation.
- Later concise prompt: 680 input + 180 output tokens -> USD 0.00948/generation.

These are authored accounting examples, not benchmarks. Historical versions can
show lower cost and better record fidelity on selected cohorts while other
measures stay flat. Do not imply every version improves every metric. The new
style version may consume more tokens and still demonstrate the feature well.

Actual companion calls use the role-assigned model; native experiments and
managed evaluator connections use `claude-sonnet-5-5`. Their real usage is priced
at normal applicable rates without the historical multiplier. Show the distinction from synthetic history; do not compare
fictional historic costs with real live cost as if they were one measured trial.

## Evaluation coverage and timing

Propose 100% applicable E-01–E-08 coverage on PR-01 historical turns; E-02–E-08
on PR-02/03. Thus the expected history has up to 4,320 PR-01 outcomes plus 3,780
PR-02/03 outcomes = **8,100 numeric/categorical outcomes**. Historical-only task
criteria add 1,220 outcomes: 240 each on PR-04/05/09, 120 on PR-06, 80 on PR-07,
300 on PR-08. Total **9,320 outcomes** before exclusions; E-02/E-03 include
explicit completed Not applicable categories when relevant. Pending, failed and
missing executions remain separate from completed counts. These are authored
scores tied to records, not
claims that paid judges already ran.

For live companion calls and the selected experiment, execute the applicable real evaluators
and show pending/failed states. The historical criteria already exist at opening;
creating an evaluator during the demo cannot retroactively explain those scores.
Any reduced sampling introduced in authoring must be visible and preserve the
presenter examples' coverage. Never silently count missing as passing.
