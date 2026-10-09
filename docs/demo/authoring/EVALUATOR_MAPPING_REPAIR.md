# Evaluator mapping repair — 2026-10-09

The final-project editor preview exposed a real configuration mismatch: nine
judge definitions used experiment-item metadata defaults, while their sample
observations came from live requests. The production rules already supplied
correct observation-metadata overrides. The sixteen recorded live executions
completed with the intended conversation/reference inputs; this did not prove
that the evaluator editor's default preview worked.

| Variable | Live/editor default | Native experiment assignment |
| --- | --- | --- |
| `current_user_message` | Metadata `$.current_user_message` | Experiment Item Metadata `$.eval_current_user_message` |
| `prior_messages` | Metadata `$.prior_messages` | Experiment Item Metadata `$.eval_prior_messages` |
| `reference_context` | Metadata `$.reference_context` | Experiment Item Metadata `$.eval_reference_context` |
| `assistant_reply` | Output, no JSONPath | Output, no JSONPath |

Output deliberately has no field selector. Historical generation output is an
assistant-message object, companion output is a message array, and native prompt
experiment output is text. A universal `$.content` selector would fail for the
latter two. The complete output contains the reply in all three shapes. Native
judge responses use `score` and `scoreExplanation`; numeric and categorical score
contracts remain unchanged.

The kit now exposes explicit post-import setup:
`configure-evaluators --update-mappings`. It verifies the exact completed import,
preflights definitions and rules, saves native dataset overrides, and then changes
only evaluator default mappings. It preserves evaluator IDs, rubrics, models,
production rules, historical observations and scores. The style judge already
uses output alone and needs no default change. Seven datasets have LLM judges;
the intent and field-extraction datasets use deterministic checks and must not
receive empty enabled LLM rules.

This must remain separate from model-free seed. Native experiment assignment
rules also match subsequently imported experiment roots. Creating them before
seed would cause historical replay to run judges. Inactive rules and additional
replay-exclusion filters do not populate the native experiment chooser, so they
are not substitutes. Setup is therefore a post-seed, pre-rehearsal step.

Interrupted configuration is recovered by inspecting target readback, using the
existing configuration-only refresh to reconcile accepted evaluator versions,
and rerunning mapping setup. Never replay seed for this repair. A simulated
interruption after one evaluator update verified that explicit recovery preserves
seed evidence and reuses existing dataset rules.

## Verification status

Both preflight runs passed all 266 scenario checks. The first attempt stopped on
an empty enabled rule for a deterministic dataset, before any default mapping
changed. The corrected attempt reused its three valid rules, created the remaining
four, and updated nine defaults. The style judge remained unchanged.

[API readback](evidence/evaluator-mapping-readback.json) verifies all ten default
mappings and seven exact dataset assignment rules. The reproducible mapping audit
now reports zero editor-default mismatches. The live evaluator editor shows all
context fields resolving from Metadata without warnings; native experiment setup
loads all eight product-explainer judges with valid mappings and retains the
Experiment Item Metadata overrides. See [live editor](evidence/evaluator-live-mappings.png)
and [experiment setup](evidence/evaluator-experiment-mappings.png). No native
experiment was submitted during this mapping check.

Final scenario verification passes **274/274 checks**, including the seven
experiment rules and their coverage. The repair preserves evaluator IDs, history
and model settings.
Exhaustive post-repair readback still finds exactly 1,638 authored traces, 5,137
observations and 9,356 authored scores, with zero failures. No online judge scores
were added to historical replay.

## Product references

- [LLM-as-a-judge mapping and overrides](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)
- [Native UI experiments](https://langfuse.com/docs/evaluation/experiments/experiments-via-ui)
- [Native evaluator selection implementation](https://github.com/langfuse/langfuse/blob/dff385dd2e1a0b53ea85564c6255813ae00ca413/web/src/features/experiments/hooks/useExperimentV2EvaluatorSelection.ts)
