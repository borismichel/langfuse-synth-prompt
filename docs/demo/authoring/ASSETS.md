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
Reference JSON is serialised for prompt substitution without altering that
structured metadata.

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
checks, requires all eight currently supported pairs, and atomically refreshes
their saved configuration receipts. Only `seed` writes RunState. No prompt,
dataset, score, model, evaluator or rule is created; no history is generated or
imported. The event receipt, IDs, spool and import status remain unchanged.
Missing or conflicting setup, an unsuccessful seed, or a different target,
authenticated project or generation configuration fails without changing state.
This mode cannot be combined with `--dry-run`.

Refresh removes only resolved evaluator-setup prerequisites and the missing
`live.model` prerequisite when that setting is now present. It retains unrelated
prerequisites, manual checks and the E-02/E-03 null-semantics blocker. A successful
refresh is configuration evidence, not proof that live judges executed; run
`verify` again and rehearse the remaining live outcomes separately.

With `evaluation.provider` and `evaluation.model` configured, setup checks
the selected provider's existing Langfuse LLM connection, then inventories
evaluator/rule names before any writes. Matching existing definitions/rules are
reused only after exact readback; conflicting names or definitions stop setup.
It creates up to eight runnable rubric definitions:
E-01, E-04–E-08, E-10 and E-11. E-02/E-03 remain pending for the null-semantics
reason below. E-09 and E-12 are authored-case deterministic criteria;
they are not silently replaced with model judgments. No provider key is created
or changed by this module.

Definitions use the stable `POST /api/public/v2/evaluators` contract. Their
default mappings read dataset-item `evaluation_context` for experiment inputs
and the selected observation output for reply judgments. Live rules use
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
requires separate rehearsal evidence. A programmatic gap remains for
E-02/E-03 inapplicability. Their accepted rubrics permit null; the native numeric
output schema provides numeric values and has no nullable/omission option.
Their managed definitions and live rules are therefore not installed; their
authored score configs and calibration fixtures remain present. Do not count an inapplicable judgment as zero or claim complete
live equivalence before this gate is resolved. A potential separate integration
could ask an external judge for applicability plus a nullable result, omit the
numeric score for NA, and preserve reasoning/applicability metadata. That would
produce API-sourced scores rather than native managed-EVAL results and therefore
requires an explicit story-contract decision; it is not silently substituted.

## Historical experiments and verification

After provisioning and before import, `bind_historical_experiments(events,
provisioning, links)` returns `(bound_events, receipts)`. This pure function uses
the core's public `otlp.string_attr` builder to append official experiment
identity, dataset ID, item ID/version and canonical observation attributes to the
18 authored experiment traces. It retains every authored trace/observation ID,
timestamp, input/output, score subject and count. No SDK runner or second write
creates duplicate observations. The answering generation is the canonical
experiment item observation, preserving the accepted output-score subject.
Its item metadata includes the same structured `evaluation_context` used by
native dataset items. Experiment identity hashes dataset ID and run name, so
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
Anthropic connection with `claude-sonnet-4-6`, then configured eight evaluator
and eight live-rule definitions. E-02/E-03 remain explicitly excluded.
Configuration refresh adopted those exact receipts without regenerating history.
Four new interactive PR-01 turns yielded 24 EVAL results (six applicable criteria
per turn). This proves actual execution of those six criteria; E-10/E-11 have
configuration readback only. See [live evidence](evidence/live-model-session.json).
