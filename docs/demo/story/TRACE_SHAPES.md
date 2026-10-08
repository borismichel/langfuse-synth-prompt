# Trace detail amendment

On 2026-10-08 the user requested: “Remember proper trace shapes for both live
companion and history add some tool calls etc”. This adds inspectable operations
without changing the prompt-first presenter journey, source facts, prompt texts,
datasets, evaluator rubrics or promotion decision.

Each PR-01/02/03 application turn has this shape:

```text
handle-chat-turn (SPAN; current user message → assistant reply)
├── retrieve-product-context (RETRIEVER; validated local fictional catalog)
├── calculate-fee (TOOL; only when explicit monthly withdrawal facts permit it)
└── generate-response (GENERATION; full model conversation, exact managed prompt)
```

The application retrieves and validates the source record before providing it to
the model. A PR-02 question with an explicit withdrawal count and calendar-month
period invokes the real fee calculator. Its structured arguments and result show
how the allowance and excess fee were applied. An ambiguous correction or a
question without those facts has no calculator span. No account is inspected and
no bank service is called. These are application functions, not model-selected
calls, so no fictional tool-call messages or IDs are inserted.

The source record remains separate from the derived calculation context. The
model receives both when calculation runs; the recorded generation input is the
actual provider payload. Evaluator reference context remains the original source.
History uses the same deterministic calculation and explicit synthetic timing and
provenance. Authored answers and score expectations stay unchanged, including
historically wrong answers even when the tool returned the correct calculation.

Each child belongs to its request and session, finishes inside its parent, and
retrieval/calculation finish before generation starts. Roots contain only the new
exchange; generations keep the actual prior conversation. Input evaluators target
the root; reply evaluators target the generation. Neither subject propagates to
retrieval or calculation operations. Fixed task and experiment orchestration uses
SPAN roots; FLOW-01's source lookup is a RETRIEVER. Stable generation operation
names are independent of the linked prompt name.

Native prompt experiments use the dataset's supplied reference context. They test
prompt/model output rather than execute the companion application, so their
historical examples do not falsely claim this application tool pipeline ran.
FLOW-01 retains its separately described authored multi-prompt reference lookup.

For seed 42, the 1,080 planned chat turns add one retrieval each and 61 explicit
fee calculations. The full arithmetic plan has 5,101 observations; 1,620 requests,
2,100 generations and 9,320 eligible outcomes remain unchanged. The 24-request
fixture has 77 observations, including one calculation. Calculator counts depend
on the deterministic template selection, so the planner uses the same seed and
selection logic. These are offline/planned counts, not a revised history import.

This refinement implements the user's follow-up request to use the Langfuse skill
for a good trace shape. It replaces the earlier redundant TOOL/retriever wrapper
with a meaningful optional calculation while retaining the accepted story.

Based on the current official [data model](https://langfuse.com/docs/observability/data-model),
[observation types](https://langfuse.com/docs/observability/features/observation-types)
and [sessions](https://langfuse.com/docs/observability/features/sessions) documentation.
