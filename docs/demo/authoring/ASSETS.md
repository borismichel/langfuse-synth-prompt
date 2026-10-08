# Native asset provisioning

`synth.assets.provision_assets(cfg)` prepares a fresh kit namespace. Reads use
the pinned core `lfread` seam; writes use core HTTP with one attempt per create.
An uncertain create outcome is not retried. The coordinator owns the durable
seed guard and partial-failure recovery. The original build phase made no live
requests. Subsequent [live pilot evidence](evidence/live-pilot.json) records 219
passing checks and four pending prerequisites, including 36 exact trace checks
and 18 exact historical experiment links; the pilot made no model calls.

Before writing, the provisioner completely inventories prompt, dataset,
score-config and model names. A collision with any of the nine authored prompt
names, nine kit dataset names, twelve score names or three synthetic model names
stops the operation before its first write. Existing unrelated records are not
changed. This does not replace the coordinator's single-writer guard: another
writer racing the preflight could still change a server resource.

The fresh payload contains 72 prompt versions: every family's v7 has
`production`, and v8 has `development`. Each is a chat prompt with the exact
authored system text, a separate reference-context system message, a
`conversation_history` placeholder, and the `user_message` variable. This same
prompt shape can run in native prompt experiments and in the companion. There
are 32 dataset cases: eight PR-01 examples and three for each secondary family.
Dataset metadata preserves case identity, authored expected scores and an
`evaluation_context` containing current message, prior turns and source record.
It also supplies top-level `eval_current_user_message`, `eval_prior_messages` and
`eval_reference_context` leaves. The latter two serialize their full JSON values
so native experiment metadata flattening does not discard nested evaluator context.
Reference JSON is also serialised for prompt substitution without altering source
facts or the retained structured provenance.

Each dataset snapshot uses the maximum `updatedAt` (or `createdAt`) timestamp
returned by its item writes, then reads the versioned dataset-item endpoint to
prove that timestamp contains exactly the intended item IDs. No client-clock
guess is used for a dataset version.

Three synthetic pricing definitions use the story's `demo-compact-v1`,
`demo-standard-v1`, and `demo-reasoning-v1` labels and declared token prices.
They are accounting fixtures, never model-provider identifiers. Set `live.model`
to a real supported identifier for native experiments.

## Managed evaluation configuration

The separate `configure_evaluators(cfg)` developer setup **may call the model**:
saving a managed evaluator performs model validation. Invoke it explicitly before
seeding, with provider use authorised. It writes no RunState. `provision_assets`
only discovers and validates already-configured evaluator/rule resources and
cannot create them. Missing setup is recorded, never executed implicitly.

If model setup happens after a successful seed, run the explicit developer
command `synth seed --config config/demo.yaml --refresh-configuration`, with
the same target, state directory and generation overrides as the imported run.
It reads already-configured evaluators and rules through the same discovery
checks, requires all ten managed evaluator/rule pairs, and atomically refreshes
their saved configuration receipts. Only `seed` writes RunState. No prompt,
dataset, score, model, evaluator or rule is created; no history is generated or
imported. The event receipt, IDs, spool and import status remain unchanged.
Missing or conflicting setup, an unsuccessful seed, a different target,
authenticated project or generation configuration, or an earlier numeric score
contract fails without changing state. Old numeric pilot history is not migrated
by refreshing configuration: it requires a fresh authorised target or separately
authorised reset to establish categorical history.
This mode cannot be combined with `--dry-run`.

Refresh removes only resolved evaluator-setup prerequisites and the missing
`live.model` prerequisite when that setting is now present. It retains unrelated
prerequisites and manual checks. For a matching categorical run it removes the
obsolete nullable-judge gate only after all ten definitions and rules match.
A successful refresh is configuration evidence, not proof that live judges executed; run
`verify` again and rehearse the remaining live outcomes separately.

With `evaluation.provider` and `evaluation.model` configured, setup checks
the selected provider's existing Langfuse LLM connection, then inventories
evaluator/rule names before any writes. Matching existing definitions/rules are
reused only after exact readback; conflicting names or definitions stop setup.
It creates up to ten runnable rubric definitions:
E-01–E-08, E-10 and E-11. E-02/E-03 use the user-approved single-match
`CATEGORICAL` results `Pass`, `Fail`, `Not applicable`. E-09 and E-12 are
authored-case deterministic criteria;
they are not silently replaced with model judgments. No provider key is created
or changed by this module.

Definitions use the stable `POST /api/public/v2/evaluators` contract. Their
default mappings read the top-level dataset-item `$.eval_*` metadata paths for
experiment context and the selected experiment item output for reply judgments.
Live rules use
`POST /api/public/v2/evaluation-rules`, overriding those same rubric variables
to observation metadata. Input criteria cannot read assistant output. E-07 sees
only the current user message. One rule per criterion filters to `prompt-live`,
the correct `evaluation_subject` and the applicable prompt-ID tags. Historical
and authored experiment environments therefore cannot trigger these rules.
The companion must propagate its prompt-ID tag to the scored observations.

Saving the evaluator can execute a validation model request. A subsequent matching live
observation, an explicitly launched prompt experiment, or evaluator test may
execute a provider model. Stable evaluator IDs are reusable in experiments;
rules follow their latest definition version. Receipts retain version identity,
and verification fails if a definition changes during the demo.

Missing provider/model settings or absent connections leave managed evaluators
uncreated and record an explicit missing prerequisite. Native label
protection/role enforcement lives in `manual_prerequisites`; it does not force
automated asset checks to fail after an operator has configured it, and it still
requires separate rehearsal evidence. The user approved categorical E-02/E-03
under story decision D-32. Their semantic criteria and IDs are unchanged;
authored calibration values map `1` → `Pass`, `0` → `Fail`, `null` →
`Not applicable`. Native score-config numeric category codes are nominal IDs,
not measurements: report category counts, never averages of those codes.
A completed Not applicable result is distinct from pending, missing, invalid or
failed execution. Native definition/rule creation is recorded below; calibration
and exact live outcome readback remain separate from configuration checks.

## Historical experiments and verification

After provisioning and before import, `bind_historical_experiments(events,
provisioning, links)` returns `(bound_events, receipts)`. This pure function uses
the core's public `otlp.string_attr` builder to append official experiment
identity, dataset ID, item ID/version and canonical observation attributes to the
18 authored experiment traces. It retains every authored trace/observation ID,
timestamp, input/output, score subject and count. No SDK runner or second write
creates duplicate observations. The answering generation is the canonical
experiment item observation, preserving the accepted output-score subject.
Its item metadata includes the same structured `evaluation_context` and
top-level serialized `eval_*` leaves used by native dataset items. Experiment identity hashes dataset ID and run name, so
multiple items in a run share one experiment ID.

The caller writes the bound events once with the core Ingestor, computes the
final wire receipt/hash, and imports that spool once. Store binding receipts in
`historical_experiments`. The materializer's golden remains independent of
server-assigned dataset IDs; binding is deterministic for the same explicit
provisioning map. The final bound wire bytes and mapping are deployment evidence,
not a substitute for the unbound generation golden. Metadata labels the results
as authored history, never live judge output. See the official
[experiment OTEL attributes](https://langfuse.com/integrations/native/opentelemetry/experiments).

`verify_assets(cfg, provisioning)` returns `(name, ok, detail)` checks for the
authenticated project, exact prompt content/version/production selection,
dataset content, score definitions, model pricing, evaluator definition versions
and rules. Historical run/item reads use core `LangfuseReader`. Missing managed
configuration yields a failed coverage check. The `missing` list remains failed
evidence until the coordinator records a real resolution; it must not simply be
cleared to obtain a green report. Native session, metric and permission UI
rehearsal remain separate gates.

Current primary sources and access findings are in
[READINESS_RESEARCH.md](READINESS_RESEARCH.md). Tests exercise later-page
collision rejection before writes, accepted counts/labels, input-only mappings,
live-only targeting, missing-provider behaviour and exact historical attachment.

## Observed setup after authorised Depot credential reuse

On 2026-10-08 the user authorised the existing Depot shared Anthropic credential
for this kit. A separate setup operation created and read back the Langfuse
Anthropic connection with `claude-sonnet-4-6`, then initially configured eight evaluator
and eight live-rule definitions. E-02/E-03 were excluded at that earlier checkpoint.
Configuration refresh adopted those exact receipts without regenerating history.
Four new interactive PR-01 turns yielded 24 EVAL results (six applicable criteria
per turn). This proves actual execution of those six criteria; E-10/E-11 have
configuration readback only. See [live evidence](evidence/live-model-session.json).


## Approved categories and native experiment context repair

Subsequently, the user's “Sure” approved `Pass`, `Fail`, `Not applicable` for
E-02/E-03 across history, experiments and live chat. Their definitions and enabled
live rules were created and verified without changing the earlier eight pairs.
[categorical-evaluators.json](evidence/categorical-evaluators.json) records that
initial version-1 configuration. The later
[context repair](evidence/experiment-context-repair.json) verifies all 32 dataset
items and ten evaluator mappings; E-02/E-03 and the other context-dependent
judges advanced to version 2, while reply-only E-01 remained version 1. Item IDs,
inputs, expected outputs and source truth were preserved. The new dataset version
is explicit in each resulting experiment receipt.

The initial native v9 rehearsal produced eight outputs and 32 scores, but nested
context paths reached E-02/E-03 as empty values. Its factual judgments remain
stored as invalid measurements; they are not answer-quality evidence. Corrected
v7 `cmv01r0p10588ad0ker6o0mcf` then completed eight outputs and 32 EVAL scores,
with both factual criteria returning eight Pass judgments. Exact corrected
context and judge reasoning are read back in
[native experiments](evidence/native-experiments.json). At that checkpoint the
corrected v9 comparison was pending; consult [native rehearsal](NATIVE_REHEARSAL.md)
for subsequent progress. This was a context repair, not a retry to obtain better
quality scores. Native experiment scores identify the experiment item observation;
its child generation supplies the resolved prompt/model provenance. Companion
output scores continue to identify the actual reply generation.

Authenticated Chrome now verifies native session/trace navigation, seeded prompt
metrics, saved `production` label protection and staged PR-01 v9. Owner access
and a saved protected label do not verify member denial. Full-scale categorical
history, member-denial rehearsal, signed release, Depot proxy/admission and the
remaining live categorical checks are still separate gates. Existing numeric
pilot history remains untouched and cannot establish the categorical seed contract.
