# Trace detail amendment

On 2026-10-08 the user requested: “Remember proper trace shapes for both live
companion and history add some tool calls etc”. This adds inspectable operations
without changing the prompt-first presenter journey, source facts, prompt texts,
datasets, evaluator rubrics or promotion decision.

Each PR-01/02/03 application turn has this shape:

```text
request (SPAN; current user message → assistant reply)
├── resolve_product_reference (TOOL; application invoked)
│   └── read_product_record (RETRIEVER; local fictional catalog)
└── reply (GENERATION; full model conversation, exact managed prompt version)
```

The application resolves the configured source record and validates its required
facts before providing it to the model. The tool returns the exact record that
becomes reference context. Inputs and outputs remain structured on the tool and
retriever. These operations do not inspect real accounts or call banking services.
They are application-invoked functions, not fabricated model-selected function
calls, so no provider tool-call messages or made-up tool-call IDs are inserted.

History carries the same nested reference operations with deterministic synthetic
durations and explicit simulated provenance. Generations retain the accepted
answers, score expectations and prompt links. Each child belongs to its request
and session, finishes inside its parent, and reference resolution completes before
generation begins. Request roots contain only the new exchange; generations keep
prior conversation. Input evaluators target the root; reply evaluators target the
generation. Neither evaluator subject propagates to reference operations.

Native prompt experiments use the dataset's supplied reference context. They test
prompt/model output rather than execute the companion application, so their
historical examples do not falsely claim this application tool pipeline ran.
FLOW-01 retains its separately described authored multi-prompt reference lookup.

The 1,080 planned historical chat turns gain two observations each: the planned
full history has 6,120 observations, while 1,620 requests, 2,100 generations and
9,320 eligible outcomes remain unchanged. The 24-request fixture gains 32
observations, for 92 in total. These are planned/offline counts, not an assertion
that the revised data has been imported into the existing pilot.

Based on the current official [data model](https://langfuse.com/docs/observability/data-model),
[observation types](https://langfuse.com/docs/observability/features/observation-types)
and [sessions](https://langfuse.com/docs/observability/features/sessions) documentation.
