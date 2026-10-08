# Authoring readiness and product API research

Checked 2026-10-08. Read-only discovery; no external data was seeded, reset,
changed, released, registered or published. No credentials were read from files
or copied into this report. This is prerequisite research, not live verification.

`python3 scripts/demo_workspace.py status` reported story **accepted**, prototype
**accepted**, authoring **not-started** at discovery. The accepted
[prototype brief](../prototype/BRIEF.md) and [product research](../story/PRODUCT_RESEARCH.md)
remain authoritative. Runtime core stays `v4.1.1`, commit
`6b86ac16d797cd0c6a80da1cdd68e8fc8998c18d`.

## Target and credential findings

| Item | Observed fact | Remaining prerequisite |
| --- | --- | --- |
| Depot repository | `borismichel/langfuse-demo-depot`; neighbouring checkout inspected at `edf5e853b36b04a5a88ea5f3accf2453c7ff5f86` | Source revision does not identify deployed revision |
| Local portal | `http://localhost:3009` responds with the Demo Depot web page; an older kit release record names this as its operator-selected portal | Establish this kit's intended delivery instance and authenticated admin session |
| Local API | `infra/docker-compose.host.yml` maps API to `127.0.0.1:8000`; `GET http://localhost:8000/api/v1/contract-version` returned **401** | Any authenticated Depot session can read contract-version; admin required for admission |
| Wrong API origin trap | Port 3009 `/api/v1/contract-version` returns **200 HTML**, not contract JSON; port 8009 refused connection | Use API origin `http://localhost:8000` for this local topology after confirming deployment |
| Langfuse test project | No Prompt-specific approved project identity found in this kit's metadata or reviewed delivery guides | Dedicated demo/disposable project, its region/base URL, project ID and scoped keys |
| Shell access | `LANGFUSE_HOST`, `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `DEMO_DEPOT_TOKEN` all unset | Load through approved environment/secret workflow; never paste keys into chat or commit them |
| Admission scratch | Source defines `ADMISSION_SCRATCH_BASE_URL`, `ADMISSION_SCRATCH_HOST_KIND`, `ADMISSION_SCRATCH_SECRET_PATH`; unset configuration causes 503 | Admin confirms configured disposable target; current configuration was not read |
| Native promotion proof | Requires protected label plus member and admin/owner identities | Qualifying plan and both roles on the actual target |

Other kits' records establish that demo infrastructure has existed. Their project
IDs, credentials, retained datasets and destructive-reset authorisations are not
permission to reuse them for this kit. No customer documents or identities were
copied.

Depot's documented credential path is the deployment wizard's Target step: it
stores per-deployment keys in Infisical and retains only the secret path in the
database. The authoring admission client needs an established short-lived **Depot
admin session**, conventionally in `DEMO_DEPOT_TOKEN`; it does not need the
deployment's session-signing secret. A Langfuse key is not a Depot session.

The inspected local TEST LOGIN implementation is enabled by
`AUTH_LOCAL_ENABLED=true`. It validates an existing roster user's password
against bcrypt via the web's internal roster service; it does not document a
plaintext login-password environment variable. `AUTH_LOCAL_USERS` remains in an
old example environment file but is retired in current runtime source. Use a
known roster credential or Google SSO. An invited user's one-time password
requires rotation; a lost password requires an administrator's explicit reset.
The web creates a five-minute API bearer server-side using `AUTH_SESSION_SECRET`
with issuer `demo-depot-web` and audience `demo-depot-api`; an Auth.js browser
cookie is not automatically that API bearer. Do not recover hashes or read the
signing secret as a substitute for an established login. Normal Depot launch
accepts existing Langfuse project credentials; it does not provision a Cloud
project. The scratch setting's source comment explicitly treats provisioning as
an external prerequisite.
See [Depot deploy guide](https://github.com/borismichel/langfuse-demo-depot/blob/main/docs/user/ae-demo-deploy.md),
[secret handling](https://github.com/borismichel/langfuse-demo-depot/blob/main/docs/runbooks/secret-rotation.md),
and [admission connection guide](https://github.com/borismichel/langfuse-synth-core/blob/main/docs/ADMISSION.md).

## Current public Langfuse API contract

The official [OpenAPI schema](https://cloud.langfuse.com/generated/api/openapi.yml)
was downloaded and parsed on 2026-10-08. These paths are relative to the target's
regional/base URL and use project Basic authentication. Recheck server capability
before writes; a current Cloud schema does not prove an older self-hosted server
supports it. Langfuse v4.36.0+ serves its own schema at `/api/openapi.yaml`.
[Public API guide](https://langfuse.com/docs/api-and-data-platform/features/public-api)

| Resource | Exact operations | Implementation consequence |
| --- | --- | --- |
| Evaluator definitions | `POST`, `GET /api/public/v2/evaluators`; `GET`, `PATCH`, `DELETE /api/public/v2/evaluators/{evaluatorId}`; `GET /api/public/v2/evaluators/{evaluatorId}/versions` | Stable resource ID; definition changes version it |
| Live evaluation rules | `POST`, `GET /api/public/v2/evaluation-rules`; `GET`, `PATCH`, `DELETE /api/public/v2/evaluation-rules/{evaluationRuleId}` | Rules select observations and assign evaluator IDs |
| Model connections | `GET`, `PUT /api/public/llm-connections` | Read supported provider identifiers; setup requires an approved provider connection |
| Prompt creation/list | `POST`, `GET /api/public/v2/prompts` | Create immutable prompt versions and list names/labels |
| Prompt retrieval | `GET /api/public/v2/prompts/{promptName}` | Use either `label` or `version`, never both; slash-bearing names must be encoded |
| Label assignment | `PATCH /api/public/v2/prompts/{name}/versions/{version}` with `{"newLabels":["production"]}` | Moves a label to the selected version; does not configure protection |
| Experiment readback | `GET /api/public/experiments`; `GET /api/public/experiment-items` | Cursor pagination; `fromStartTime` required; include upper bound and exact run/dataset IDs |
| Session/trace observation readback | `GET /api/public/v2/observations` | Filter `sessionId`/`traceId` and time range; request needed field groups |
| Score readback | `GET /api/public/v3/scores` | Request `subject,details` to verify actual target and reason; observation filter needs trace ID |

An LLM evaluator create body uses `name`, `type: "llm_as_judge"`, `prompt`,
`outputDefinition`, optional `modelConfig: {provider, model}` and
`variableMapping`. The output definition carries `dataType` plus the score
definition fields in the schema. Mappings use `{variable, source, jsonPath?}`;
sources are `input`, `output`, `metadata`, `tool_calls`, `expected_output`,
`experiment_item_metadata`. Supply exactly one mapping per declared variable.
Use explicit metadata fields for current message and history; input-only judges
must not read assistant output. Live evaluations must not depend on expected
answers available only to experiments.

**Model-free seed boundary:** saving an evaluator can validate its model by
making a provider request. Therefore managed evaluator creation belongs to the
explicit model-using developer setup command before seeding. Seed only reads and
validates existing evaluator/rule configuration. It must never automatically
create an evaluator on discovering it missing.

**Current rules differ from older examples:** create requires `name`, `enabled`
and `evaluatorAssignments`, with optional `sampling` and `filter`. Assignments
contain `evaluatorId` and optional `variableMapping` override. No `target`,
`status`, `evalTemplateId`, or `datasetId` field belongs in this create body.
An empty filter matches every incoming observation; scope to this kit and the
actual root/reply operation. Preserve E-05–E-08 on request roots and E-01–E-04 on
answer generations. Rules follow the evaluator's latest version, so record
definition/version receipts and freeze changes during a comparison.
[Programmatic evaluator setup](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)

The installed skill's migration reference still mentions unstable resources and
`datasetId`; those details are superseded by the current stable schema and
[official migration guide](https://langfuse.com/faq/all/llm-as-a-judge-migration).
That guide maps legacy dataset context to `experimentDatasetId` in filters and
experiment-item mappings; this is not a top-level new-rule target parameter.
Use the native UI/SDK experiment configuration for experiment execution and
selected evaluators. The two experiment REST paths above are **read** endpoints,
not a public POST for launching a prompt experiment.

## Protection, experiments and links

Protected labels are documented for Pro with Teams add-on, Enterprise, and
self-hosted Enterprise Edition. Admins/owners configure protection in project
settings; members/viewers cannot modify protected labels. The fetched public
OpenAPI contains no label-protection configuration endpoint. Do not invent one
or treat a project API key as a member identity. Use supported native settings
and rehearse member denial plus admin success, independently of score quality.
[Version control and protected labels](https://langfuse.com/docs/prompt-management/features/prompt-version-control)

Native prompt experiments require an LLM connection, usable prompt variables
matching dataset input keys, and a fixed dataset version for comparison.
Preserve the eight accepted PR-01 cases and four separate output criteria.
MODEL-BASE and the story's accounting prices are fictional; they are not runnable
provider settings. Inspect a supported actual model on the selected project.
[UI experiments](https://langfuse.com/docs/evaluation/experiments/experiments-via-ui)

Propagate the same session ID to every observation of a conversation. Session
replay groups those observations and traces; session annotations differ from
root/generation scores. Managed judges do not join a conversation automatically.
Keep root/new-message I/O distinct from the generation's full role-bearing
history. [Sessions](https://langfuse.com/docs/observability/features/sessions)

For delivered links, retain project ID, session ID, trace ID, explicit root and
generation IDs, dataset ID and experiment ID in receipts. Existing sibling
integration code constructs `/project/{projectId}/sessions/{sessionId}`, but that
is an inspected implementation convention, **not proof of this target's route**.
Obtain actual experiment/session URLs through the native UI or supported SDK
results and open them during rehearsal. Do not hard-code legacy dataset-run
comparison routes or claim the session shows every per-observation score beside
each bubble. Native session-to-turn-to-score navigation remains a live check.

## Release and admission prerequisites

Core v4.1.1 lacks `synth-authoring admit`. Preserve the runtime pin and use either
the documented manual Depot API or a separately installed newer authoring CLI.
Manual operations are `POST /api/v1/admin/admission` with
`{"slug":"prompt","repo_url":"https://github.com/borismichel/langfuse-synth-prompt","ref":"<immutable-release-tag>"}`,
then `GET /api/v1/admin/admission/{run_id}`. No request was made here.

Before POST, the exact candidate must have a CI-published, signed GHCR image and
immutable release tag. Retain resolved source commit, image digest, run ID and
per-rung results: register, build, spawn, seed, verify, Companion smoke. Pin the
registry only after `eligible_to_pin: true`. A healthy Companion is not a
completed presenter rehearsal.
[Kit author guide](https://github.com/borismichel/langfuse-demo-depot/blob/main/docs/user/kit-author-guide.md)

The locally inspected Depot guide says new catalog entries default to published;
the current delivery skill expects newer staging-default behaviour and the
Manifest-slug guard. This discrepancy must be resolved against the deployed
instance before registration. Explicitly confirm staging visibility and member
inaccessibility; do not infer it from a source checkout or skill text.

## Concrete next actions

1. Finish scaffold, deterministic data, native assets, companion, verification and
   runbook offline against pinned core. Preserve the accepted examples and split
   input/output score targets. No access dependency blocks this work.
2. Establish the selected Depot admin session; read its contract version. Confirm
   Manifest identity guard, staging behaviour and configured disposable scratch
   target without exporting secrets.
3. Select a Prompt-specific demo project and supported model connection. Supply
   its keys through the deployment secret workflow; verify server version/plan,
   protected-label support and two role identities.
4. Seed one fresh authorised target, configure/validate the current managed
   evaluators, and read back exact current-run records. Validate score placement,
   dataset versions, generation prompt links and rubric coverage. Spool appends;
   a partial failure needs an authorised reset or new target, not blind replay.
5. Release the exact candidate, obtain admission verdict, register in staging,
   then execute the full portfolio → experiment → admin promotion → chatbot →
   session journey using delivered runbook links. Capture timestamped evidence.

At the end of this discovery, **live verification, admission and delivered
rehearsal are pending**. Missing prerequisites are explicit above; no stage is
claimed passed from source research or fixture behaviour.
