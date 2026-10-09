# Developer mode: replace authored history in the same project

Use this procedure when the already imported authored history needs different
model identities, explicit synthetic costs or operation naming. Langfuse
v4 observations are immutable; posting the old IDs again appends observations.
This procedure transforms the complete original spool, deletes only its recorded
trace IDs, and imports the transformed events once under a new ID namespace.
It does not regenerate conversations or perform an ordinary seed.

The migration module never changes prompts, labels, datasets, model definitions,
evaluators, rules, model connections or project settings. Separately authorised
asset-policy changes must be completed and read back before deletion, then passed
as a verified receipt. The source imported state remains immutable; replacement
state is written to a new directory only after deletion has been verified.

## 1. Prepare and inspect the local plan

The supported planning command is offline and needs no credentials. Use the
complete imported spool named by the receipt, including both the original sample
and supplement after a history expansion. The supplement alone is not complete.
For the full-volume 2026-10-09 source:

```sh
.venv/bin/synth history-replacement-plan \
  --source-spool .scratch/full-volume-expanded-state/combined-evidence.ndjson \
  --destination .scratch/model-policy-replacement-state \
  --project-id cmv0gc1710815ad0k7nnnd6v5 \
  --run-date 2026-10-09T12:00:00+00:00 \
  --revision models-2026-10-v1 \
  --expected-traces 1638 \
  --expected-observations 5150 \
  --expected-scores 9356
```

Review `replacement-plan.json`, `id-maps.json` and `events.ndjson` in the new
folder. The plan contains exact source and replacement hashes, project/date,
counts and the complete explicit deletion scope. `pre-replacement-state.json`
preserves the original anchors. No deletion guard or live write is created by
planning. A second plan may be prepared for review in another new directory,
but the exclusive source guard permits only one application attempt.

The transformation preserves event order, timestamps, observation input/output,
scores and tool trees. Trace, observation, score, score-envelope and session IDs
are remapped deterministically. Root observation IDs preserve core’s derivation
from the new trace ID, so root identification and verification remain valid. Exact nested ID values in JSON attributes are
updated too. Existing experiment IDs, dataset IDs and dataset-item IDs stay
stable; each experiment's root-observation reference moves to the new observation.
Operation names match the companion, history and live requests share the `production`
environment, and experiments retain `experiment`. Prompt IDs are the only trace
tags. `evaluation_mode=replay` and authored provenance remain in metadata; live
evaluators select `evaluation_mode=online`. Experiment labels describe the prompt
version comparison. New generation uses conversation/customer identifiers.
Models and explicit synthetic costs come from `synth.model_policy`. Native prompt
name/version associations stay on generation observations. The
`synth.prompt_references` helper removes redundant root `prompt_references`,
`prompt_name`, `prompt_version` and `resolved_version` metadata. Exact legacy
experiment descriptions are replaced with an operational comparison description,
and the fixed authored-fixture score comment prefix is removed. Full rubric text
and authored/replay provenance on score-target metadata remain.

## 2. Prepare the authenticated callbacks and asset receipt

The supported apply interface is `synth.migration.delete_replacement` followed
by `synth.migration.import_replacement`. Keep a single operator/runner as the
live writer. The caller supplies official Langfuse CLI callbacks for project
identity, exhaustive reads and trace deletion. Core's `Ingestor` remains the
only trace/score import transport. The migration module does not create another
HTTP transport or silently read credentials from local files.

Discover the installed CLI's current schemas before constructing its commands:

```sh
npx langfuse-cli api projects list --help
npx langfuse-cli api observations list --help
npx langfuse-cli api scores list --help
npx langfuse-cli api traces --help
```

Authenticate the exact `base_url` and `project_id` in the plan. Do not infer
project identity from a display name. The callback contracts are:

| Callback | Contract |
| --- | --- |
| `inventory()` | Returns `(observations, scores)` containing every modern observation and score page in the project. Observations require `id`, `traceId`, `projectId`, `sessionId`; scores require `id`, `traceId`, `observationId`, `projectId`. Reject truncated data, exhausted item caps, repeated cursors, errors and incomplete pagination. |
| `delete_batch(trace_ids)` | Sends one official CLI request for `DELETE /api/public/traces` with `{"traceIds": trace_ids}`. No retry. Raise on any failure or ambiguous response. The migration passes at most 40 IDs by default, never more than 50. |
| `import_spool(path)` | Calls the pinned core importer once, with `max_retries=1` and `confirm_cleared=False`. Never opens/re-generates the spool or removes an import marker. |

Modern read routes are `/api/public/v2/observations` and `/api/public/v3/scores`.
Use explicit complete time bounds that cover source and preserved project data;
check account read-window restrictions. A clipped view cannot establish that
unrelated data will remain intact. The established project's expected preflight
contains nine nonseed traces; retain their full readback alongside the plan.
The module records and protects every unrelated trace, observation and score ID
returned by the inventory.

The policy receipt is supplied separately and has this shape:

```python
policy_receipt = {
    "project_id": authenticated_project_id,
    "model_policy_revision": MODEL_POLICY_REVISION,
    "verified": True,  # set only after actual asset readback
    "provisioning": refreshed_provisioning,  # full original anchors plus verified policy updates
    "evaluator_rules": refreshed_evaluator_rules,  # optional when unchanged
}
```

`provisioning.project_id` must match the source. Prompt, dataset and historical
experiment anchors must equal the source anchors at deletion preflight, with one
explicit exception: an experiment `run_name` may be its original name or the exact
canonical value from `experiment_run_name(prompt_id, version)`. All experiment IDs
and dataset/version bindings remain exact. Include
full model/evaluator anchors needed by subsequent verification. Merely setting
`verified=True` is not evidence of asset readback; save the readback with the
operator's execution record.

## 3. Request scoped deletion, wait, and import once

The following is the integration contract for the authenticated operator runner;
`inventory` and `delete_batch` are the official CLI callbacks described above.
It is not a replacement for implementing and verifying those callbacks.

```python
from pathlib import Path
from langfuse_synth_core.seed.ingest import Ingestor
from synth.migration import delete_replacement, import_replacement

plan_path = Path(".scratch/model-policy-replacement-state/replacement-plan.json")

delete_replacement(
    plan_path,
    authenticated_project_id=authenticated_project_id,
    inventory=inventory,
    delete_batch=delete_batch,
    policy_receipt=policy_receipt,
)

def import_once(path):
    ingestor = Ingestor.from_env(plan_base_url, spool_path=path, max_retries=1)
    ingestor.import_spool(path=path, confirm_cleared=False, log=print)

replacement_state = import_replacement(
    plan_path,
    authenticated_project_id=authenticated_project_id,
    inventory=inventory,
    import_spool=import_once,
    timeout_seconds=960,
    poll_seconds=30,
)
```

Deletion preflight requires the exact observation and score identities and score
subjects from the source, with no missing, extra or duplicate authored records.
It rejects any replacement trace, observation, session or score collision. An
unexpected managed-judge score on an authored trace is a discrepancy to resolve,
not permission to broaden the scope.

An exclusive `.history-replacement-attempt.json` beside the source records the
one-shot attempt. The destination records `policy-receipt.json` and
`replacement-status.json`, including each submitted batch and the current batch
before sending. Deletion is asynchronous. The import phase polls until **all**
old observations and scores disappear while the unrelated inventory remains.
Only then does it write a new `.synth_state.json`, create an exclusive import
attempt record, and call core once. It never fakes an empty project or a clean
seed state. No project-wide deletion is part of this procedure.

## Recovery and verification

| Recorded phase | Permitted next step |
| --- | --- |
| Plan only, no source guard | Review or create another offline plan; no live changes have occurred. |
| `deleting` or `delete_failed_requires_reconciliation` | Inspect saved batches and live readback. An interrupted/ambiguous DELETE is not retried automatically. Do not import. |
| `awaiting_deletion` after polling timeout | Call only `import_replacement` again to continue read-only polling, using the same unchanged plan and authenticated project. Do not repeat `delete_replacement`. |
| `importing` or `failed_requires_reconciliation` | Treat the import as non-resumable. Keep markers, source, replacement spool and state. Investigate partial ingestion; do not retry or create another revision to evade the guard. |
| `imported` | Read back the replacement and all protected assets/live records. Do not repeat the import. |

A successful importer return is transport evidence, not final verification. Use
the replacement directory as `SYNTH_STATE_DIR` for the existing `synth verify`
command with the same project, seed, date and target volume. Also compare exhaustive
replacement observation/score inventories against the prepared spool, including
models, costs, generation prompt associations, parent relationships, session chronology and
experiment item links. Confirm the nine nonseed traces and all preserved asset
snapshots remain. Record current-run checks before switching any delivered surface
to the replacement anchors.

References: [v4 tracing updates](https://langfuse.com/faq/all/tracing-data-updates),
[trace deletion and asynchronous verification](https://langfuse.com/docs/administration/data-deletion),
[API deletion batch limits](https://langfuse.com/faq/all/api-limits).

## Fixed presentation amendment before the first import

If deletion requests are complete and the status is still `awaiting_deletion`,
the narrow `amend_preimport_presentation` API can apply the user's explicit
presentation corrections locally: rename only `langfuse.user.id` values from
`fictional-user-…` to `customer-…`, and remove the four redundant root prompt
metadata fields named above. It also replaces only the exact legacy experiment
description with “Prompt version comparison against the regression dataset.” and
removes only the exact score-comment prefix “Authored fixture expectation; no judge
executed. ”. Every remaining comment character is retained; authored provenance
stays on target observation metadata. It accepts no arbitrary edited spool. Generation
prompt associations, all observation/trace/session/score IDs, input/output,
timestamps, costs and the exact deletion scope remain unchanged. It refuses any
user mapping that would merge existing user groups.

```python
from synth.migration import amend_preimport_presentation

audit_path = amend_preimport_presentation(
    plan_path,
    expected_project_id=authenticated_project_id,
    expected_plan_sha256=reviewed_plan_sha256,
    expected_replacement_sha256=reviewed_replacement_sha256,
)
```

Supply the previously reviewed hashes, not hashes guessed from a failed attempt.
The amendment checks the source, plan, guard, policy receipt and completed deletion
batches, and refuses any import state/marker. It and the importer share an
exclusive local transition lock. `presentation-amendment/` retains byte-for-byte
backups of the old spool, plan, status and source guard, a user-ID mapping,
counts and an audit hash. Each file replacement is atomic; status is marked
`presentation_amendment_in_progress` before changes and returns to
`awaiting_deletion` only after the new spool/plan/guard hashes agree. A committed
audit binds the resulting plan. Any interrupted amendment or missing commit
blocks import and requires local reconciliation; it is never repeated blindly.
This amendment makes no live calls and never submits another deletion request.
