# Model policy and explicit user feedback

Accepted user change on 2026-10-09: replace anonymous synthetic model tiers with
Sonnet 5.5, Opus 5.5 and Fable 5.1; select models by agent role; make demo costs more
visible; keep experiments and evaluators on Sonnet 5.5. The user also requested
prompt/version metadata on all traces and explicit thumbs plus written feedback.
These changes preserve the three-beat story and existing fictional cases.

The executable policy is [model_policy.json](../../../src/synth/fixtures/model_policy.json).
The kit generator, live companion and prototype consume that policy or a tested
byte-identical copy. Model choices below are demo design decisions, not benchmark
claims or recommendations for regulated decision-making.

| Prompt | Model | Rationale |
| --- | --- | --- |
| PR-01 Product explainer | Sonnet 5.5 | Straightforward retrieval and explanation |
| PR-02 Fee explainer | Opus 5.5 | Preserve conditions, amounts and calculator results |
| PR-03 Application guide | Opus 5.5 | Faithful requirements, deadlines and missing-status boundaries |
| PR-04 Intent classifier | Sonnet 5.5 | Bounded classification |
| PR-05 Reference query rewriter | Sonnet 5.5 | Concise retrieval query with material constraints |
| PR-06 Conversation summariser | Fable 5.1 | Reconcile conversation history and unresolved work |
| PR-07 Document field extractor | Opus 5.5 | Exact identifiers, amounts and absent fields |
| PR-08 Customer-message drafter | Opus 5.5 | External communication without invented promises |
| PR-09 Handoff-note writer | Fable 5.1 | Synthesize the multi-step review into a reliable handoff |

All authored experiments and future native experiment selections use
`claude-sonnet-5-5`, regardless of the agent's production model. Managed evaluators
also use Sonnet 5.5. Existing real executions retain their actual recorded models.
Prompt version configuration is immutable; when rerunning experiments on an older
stored version, select Sonnet 5.5 explicitly in the native experiment model picker.
New kits provision Sonnet 5.5 as their experiment default.

The verified API IDs are `claude-sonnet-5-5`, `claude-opus-5-5` and
`claude-fable-5-1`. Base input/output prices per million tokens are $2/$10, $4/$20
and $10/$50 respectively, checked against [Anthropic's model documentation](https://platform.claude.com/docs/en/models/fable-5-1/overview)
on 2026-10-09. Authored history uses an explicit **3× synthetic cost multiplier**.
Stored usage still determines each cost; costs are not independently randomized.
The 3× multiplier applies only to explicit authored history/experiment cost details;
the model registry retains normal base rates so live accounting is not inflated.
Real companion/evaluator calls retain actual usage and normal provider accounting.
Metadata discloses synthetic usage, pricing basis, multiplier and policy revision.

Each prompt-using generation retains its native Langfuse managed-prompt link
to the exact name and resolved version. Multi-prompt workflows preserve a separate
association on each generation. Prompt references are not duplicated on roots.
Langfuse displays the native prompt association on the generation ([prompt linkage](https://langfuse.com/docs/prompt-management/features/link-to-traces)).

Explicit feedback uses `user-thumbs`, a BOOLEAN score on the saved request root,
with value `1` for thumbs up or `0` for thumbs down, plus an optional comment. It is independent of E-08 `user_disagreement`, which is
an evaluator inference from the incoming user message. A negative thumb does not
by itself assert factual error or disagreement. Submission is final for that reply;
identical retries do not emit another score. The current selection or newest turn
must never retarget feedback. This follows the [Langfuse user-feedback pattern](https://langfuse.com/docs/observability/features/user-feedback)
and the skill's v4 observation-target guidance.


Normal application, trace and experiment names describe their operation or task.
History and companion calls use the same operation names. Authored origin and
cost multipliers remain explicit in metadata and documentation rather than being
inserted into every product label; this does not reclassify authored history as
measured customer traffic.
