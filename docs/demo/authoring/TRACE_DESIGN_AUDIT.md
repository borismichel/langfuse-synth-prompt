# Trace design audit against the Langfuse skill

Reviewed 2026-10-08 after the user's request to use the Langfuse skill to find a
good trace shape. This is a design audit of revision d63c85f, not a claim that a
new live trace was sent or inspected.

## Recommended shape for this application

```text
session: one conversation
└── handle-chat-turn (SPAN; one trace per turn)
    ├── retrieve-product-context (RETRIEVER)
    ├── calculate-fee (TOOL, only when a real calculation is performed)
    └── generate-response (GENERATION; managed prompt/version + model usage)
```

These names illustrate operation roles; they are not a claim that the current
runtime already implements a fee calculator. Keep the main demo prompt-first:
the reference and any calculated results support the same product explanation.
A simple reference-based reply needs retrieval and generation only. Do not pad
that path with tool observations solely to make the tree larger.

If a future runtime genuinely lets a model select tools, use a separate generation
for its tool request, the requested tool as a sibling, then another generation
for the answer. Preserve actual provider tool-call IDs, JSON arguments, matching
results and per-call usage. Do not invent that conversation shape for the current
application-directed retrieval path.

## Audit of the current implementation

- Correct: each turn has a separate root; the conversation shares a session ID.
- Correct: actual model messages, managed prompt version and token usage are
  recorded on the generation. Evaluator-only context lives in metadata.
- Correct: user-input scores and feedback target the root; response scores target
  the answer generation. Reference observations do not inherit evaluator subjects.
- Correct: the existing live reference read and validation really execute, with
  errors captured; historical counterparts are explicitly synthetic.
- Refinement needed: `resolve_product_reference` TOOL encloses
  `read_product_record` RETRIEVER, with essentially identical returned records.
  This does capture validation failure separately, but adds little business
  information. Prefer a single RETRIEVER for retrieval; add TOOL only for a
  separately useful action, such as a real fee calculation. This conclusion is
  our application-specific judgment, not a prohibition on nested tools in Langfuse.
- Naming refinement: use consistent stable action names across history and live
  operations. Prompt identity belongs in the prompt link, independent of an
  operation name. Existing historical generation names use prompt paths while the
  live generation is named `reply`; reconcile deliberately with affected filters.
- Type refinement: the historical FLOW-01 reference lookup only retrieves data,
  so RETRIEVER is more specific than its current TOOL type. Fixed task/experiment
  roots should use SPAN or CHAIN; AGENT should describe actual agent orchestration.

No further trace-shape code change or seed import was made during this audit.
A subsequent authorised model setup enabled four actual PR-01 turns. Exact
readback now confirms sixteen persisted observations with the implemented
request/tool/retriever/generation hierarchy, linked prompt v7, usage/cost and
correct score subjects. See [live evidence](evidence/live-model-session.json).
This verifies the current implementation; the recommended design refinements above
remain pending. The older seeded history still does not prove the revised shape.

## Sources and completion condition

The active skill's instrumentation reference requires: “Execute the instrumented
path end-to-end so a trace is actually sent.” It then requires fetching that trace
and auditing against freshly read best practices. Local tests alone do not meet
that completion condition.

- [Langfuse skill](https://github.com/langfuse/skills/tree/main/skills/langfuse)
- [What does a good trace look like?](https://langfuse.com/docs/observability/best-practices)
- [Observation types](https://langfuse.com/docs/observability/features/observation-types)
- [Data model](https://langfuse.com/docs/observability/data-model)
- [Sessions](https://langfuse.com/docs/observability/features/sessions)
- [Observation evaluator migration and score cardinality](https://langfuse.com/faq/all/llm-as-a-judge-migration)
