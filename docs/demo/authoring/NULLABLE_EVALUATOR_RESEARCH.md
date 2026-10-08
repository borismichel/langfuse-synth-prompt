# Nullable evaluator capability check

Checked 2026-10-08 using the Langfuse skill, current official documentation,
public Cloud OpenAPI, and public Langfuse implementation. Workspace status before
consuming the handoffs: story accepted, prototype accepted, authoring ready.
No credentials, project data, model calls, evaluator writes or deployment changes
were used for the original capability research. The later deployment evidence
linked below was recorded separately; it does not change that research provenance.

## Current decision and evidence

The user subsequently answered **“Sure”** to the proposal for E-02/E-03
**Pass / Fail / Not applicable** categories consistently across history,
experiments and live chats, with category counts instead of numeric averages.
Story decision D-32 records this approval. The original recommendation below is
retained as historical capability research; its proposed external nullable adapter
was not selected and is not the implementation contract.

The selected contract keeps `record_fidelity` and `claim_support` semantically
separate, using single-match native categorical judges. Existing authored 1/0/null
labels map explicitly to Pass/Fail/Not applicable. Category codes in score configs
are nominal identifiers, never a numeric quality scale. Missing, pending, failed
or invalid results are not Not applicable.

[Native configuration readback](evidence/categorical-evaluators.json) verifies
both categorical definitions and enabled live rules. A later
[context repair](evidence/experiment-context-repair.json) preserves 32 dataset
case IDs and source facts while adding top-level serialized `eval_*` context
leaves and correcting evaluator JSONPaths. E-02/E-03 definitions are version 2
after that mapping change; their semantic rubrics remain unchanged.

The first native v9 experiment received empty factual context, so its eight
outputs and 32 stored scores are retained with invalid factual measurements.
Corrected v7 completed eight outputs and 32 EVAL results with all eight factual
judgments Pass per criterion. This establishes actual categorical execution on
that baseline, not calibration reliability or full live parity. The corrected
candidate and further rehearsal evidence are tracked in
[native experiments](evidence/native-experiments.json) and
[native rehearsal](NATIVE_REHEARSAL.md). Earlier numeric pilot history remains
untouched. Full-scale categorical history, live Pass/Fail/Not applicable coverage,
member-denial checks, signed release and Depot admission remain separate gates.

## Original capability finding (before D-32)

**A native managed numeric LLM judge cannot itself return null, omit its score,
or declare an N/A result in the current implementation. Native rules can skip
observations using explicit metadata, but do not perform semantic applicability
judgment. The numeric 0/1/null story does not require a categorical redesign.**

The prior claim that an installed numeric judge cannot emit N/A is confirmed;
the broader implication that categorical conversion is the only resolution is
not. The original recommendation was to keep E-02 `record_fidelity` and E-03
`claim_support` separate and numeric, with null represented by an omitted numeric
score plus explicit applicability evidence. An absent score alone is ambiguous.
D-32 superseded that recommendation with explicit categorical outcomes.

## Original capability evidence

| Question | Current supported contract |
| --- | --- |
| Nullable numeric output definition? | `EvaluatorOutputDefinition` permits `NUMERIC`, `BOOLEAN`, or `CATEGORICAL`. `PublicEvaluatorNumericScore` exposes optional numeric bounds and instructions, with no nullable-result/skip switch. Nullable bounds mean an omitted bound, not a nullable result. |
| Can a prompt instruct the judge to return null anyway? | `buildResultSchemaForResolvedOutputDefinition` constructs required `score: z.number()` with optional bounds. `validateEvalOutputResult` parses against that schema. Null/missing values fail validation rather than become N/A. |
| Can a categorical result preserve numeric 0/1/null internally? | Managed categories are strings, not objects with optional numeric mappings. There is no per-category null numeric value in the evaluator definition. Multi-match output requires at least one category; an empty list is not a skip mechanism. It remains a categorical result and does not preserve the accepted numeric metric by itself. |
| Can rules avoid scoring known N/A observations? | Yes. `metadata` supports `stringObject` filters on a top-level key, with `=` and key-presence operators. All filter conditions must pass. The scheduler returns no jobs for unmatched observations. |
| Can a rule infer “no factual issue” or “no substantive claims,” or wait for another judge's score? | No supported rule column provides semantic predicates or another score. Rule matching reads observation fields before scheduling. Applicability must already be present in the observation, or an external process must decide it. |
| Can a native code evaluator call an LLM and skip? | Not this way: the documented sandbox has no network egress, a two-second limit, and requires at least one score. Code evaluators are not a replacement semantic judge for these rubrics. |

Primary evidence:

- [Cloud OpenAPI schema](https://cloud.langfuse.com/generated/api/openapi.yml),
  fetched SHA-256 `a1fd11bd0d27985a0167c36fcb4f6b2b3cbc62cb0ed0076f6d517d41287dcb47`.
  Relevant definitions: `EvaluatorOutputDefinition`, `PublicEvaluatorNumericScore`,
  `PublicEvaluatorCategoricalScore`, `EvaluationRuleFilter`, and
  `StringObjectEvaluationRuleFilter`.
- [Required numeric result and categorical minimum](https://github.com/langfuse/langfuse/blob/c106bb3d945323688e6f6079f65fb0ab28203b53/packages/shared/src/features/evals/outputDefinition.ts#L286):
  numeric schema begins at line 336; result validation at line 406. This is the
  public `main` revision observed during this check, not a claim that the selected
  Cloud target runs this exact commit.
- [Rule matching before scheduling](https://github.com/langfuse/langfuse/blob/c106bb3d945323688e6f6079f65fb0ab28203b53/worker/src/features/evaluation/observationEval/scheduleObservationEvals.ts#L117).
- [Managed judge documentation](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge):
  rules select observation fields; experiment evaluator selection is a separate
  path. Selecting an evaluator in a prompt experiment does not promise to apply
  a separately configured live rule's applicability filter.
- [Native code evaluator runtime constraints](https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators#runtime-constraints).

## Original unselected producer proposal

Preserve the accepted rubrics, fixtures, numeric averages, observation targets,
and eligible-case denominator. Change only the producer for E-02/E-03 to an
external semantic judge adapter, with validated `{value: 0 | 1 | null, reason}`
results. Publish 0/1 through the supported score API/SDK on the exact reply
generation; for null, omit that criterion's numeric score and retain explicit
N/A evidence with reason, rubric revision, judge configuration and observation ID.
Retain distinct pending/error/not-applicable states. This is a proposed producer
adjustment, not a silent change to the story or a claim of completed execution.

The same adapter should handle live replies and newly generated native experiment
observations. Native prompt experiments can still be launched and compared in
Langfuse; the adapter would score their exact resulting observations afterward.
Do not attach the unsupported numeric E-02/E-03 managed definitions to all native
experiment items. This postprocessing must be implemented and rehearsed before
claiming an automatic presenter workflow. Historical seed remains model-free.
[External score ingestion](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
and [SDK experiment evaluators](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)
are supported extension points; no native nullable score write is proposed.

If retaining a managed numeric producer is mandatory, a semantic applicability
gate can instead run before the observation is finalized and emit separate
metadata keys, e.g. `e02_applicability="applicable"` and
`e03_applicability="not_applicable"`, then the corresponding native rules select
only `"applicable"`. This needs semantic model work for arbitrary live replies,
and a separately verified experiment execution path. It is more moving parts
than a single external nullable judgment per criterion.

Do not substitute prompt-family membership, an empty string check, dataset input
labels, or keyword heuristics for actual applicability: E-03 depends on the
generated reply, and E-02 must still fail an answerable factual question that the
reply evades. Authored expected N/A labels are calibration truth, not live results.
Do not insert 0 or 1 for N/A, use an out-of-range sentinel, treat model errors as
N/A, or infer N/A solely from missing score rows.

## Verification proposed for the unselected numeric adapter

Check one applicable pass, one applicable fail, and one explicit N/A for each
criterion against actual generated replies. Verify 0/1 score subjects and
provenance, absence of numeric scores only for the two proven N/A outcomes,
separate error/pending states, and averages based only on applicable completed
outcomes. Inspect native experiment comparison and live session navigation. The
current research resolves the product capability question; it does not resolve
these live execution checks.
