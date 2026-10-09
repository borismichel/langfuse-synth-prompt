# Depot onboarding — 2026-10-09

The user authorized Depot onboarding, registration and shipment, then approved
creating a dedicated project in Boris Demo Enterprise with a name ending in
`demo`. The existing final-seed project is preserved.

## Admission target

- Organization: Boris Demo Enterprise, enterprise plan.
- Project: `prompt-admission-demo` (`cmv0magyy08o7ad0e54ath8wi`).
- Host: Langfuse EU Cloud.
- Created through the authenticated organization UI; project-scoped credentials
  stored privately and then in Depot's existing Infisical admission reference.
- Replaced the previously configured credentials that returned HTTP 401.
- Depot secret readback now authenticates against the exact new project; initial
  inventory was zero traces and zero datasets.
- Anthropic connection and ten accepted LLM judges with ten production rules
  configured before admission; Sonnet 5.5 remains the judge/experiment model.

[Creation evidence](evidence/depot-admission-project.png) shows organization,
project name and empty trace state without credentials.

## Supported admin admission access

[Depot PR #275](https://github.com/borismichel/langfuse-demo-depot/pull/275) adds an
admin submission form and saved result page through the existing signed-in
server-side API flow. No cookie extraction or manual token workaround is used.
The implementation belongs to Depot's repository, not this kit. Its local
validation passed 465 web tests, type checking, production build and documentation
anchor checks. GitHub initially reported no CI checks; none are claimed passed.

PR #275 is merged and deployed at `4bc52097a30de56cdd18b1d4a68060608f56ac75`.
The database is at `0034_staging_default`; new catalog entries default to staging.
API health returned 200, the signed-in admin admission form was verified in the
browser, and both existing companion containers remained running unchanged.
No active jobs were interrupted. The API/worker image is
`sha256:0de769d465b093820ad579e0a56dca564d2ec260ae41e55d4d8639407b40872d`;
web image is `sha256:3bf369c18d91191526ee91539f8799fabe43b200a5e08f5953d13d28b6e9ef8b`.

## Automatic model connection setup

At the user's request, both first-run evaluator setup and seed now provision a
missing Langfuse model connection when the demo has a compatible provider key.
They reuse compatible existing connections without replacing credentials. The
connection API stores configuration only; historical generation remains
model-free. Keys never enter event data, state receipts, public artifacts or
browser responses. A custom provider endpoint requires explicit connection
configuration instead of silently sending credentials to an assumed endpoint.

## Candidate and delivery evidence

Release `v0.1.0` is source `689ba53c82e50200ccc3c2667ed5fc0ab5939cfc`.
[CI](https://github.com/borismichel/langfuse-synth-prompt/actions/runs/37897590410)
and the [signed image build](https://github.com/borismichel/langfuse-synth-prompt/actions/runs/37897591896) passed.
Image: `ghcr.io/borismichel/langfuse-synth-prompt@sha256:2f1f56612c90b09c3177069ea86a26606a5a8a5683009c83d3269ae32554976c`.

Admission `0712efe4-be64-484d-aeb1-d057943be4bc` passed all six checks and is
eligible to pin. Its deployment is `3d9b5e26-18e1-49e2-90d8-84e05449aebc`.
[Admission evidence](evidence/depot-admission-v0.1.0.json) records the exact
candidate. This populated project must not be reseeded.

[Registry PR #276](https://github.com/borismichel/langfuse-demo-depot/pull/276)
merged at `338d0c6cb9a865f7ef190cbe79aec81b855f6b8c`. The running API was rebuilt
and the registry synced through Admin. The user explicitly requested publication;
the registered `prompt` entry was published and visibly appeared as the fourth
catalog card. [Catalog evidence](evidence/depot-published-catalog-v0.1.0.png).
The earlier similarly named `admission:prompt@689ba53c82e5` entry was an internal
admission carrier, excluded from the catalog regardless of its visibility setting.
Its misleading Admin publish control is being corrected in Depot.

After admission imported and verified the full history, the exact released image
ran `configure-evaluators --update-mappings` against its existing state volume.
It exited successfully with ten managed definitions and seven native experiment
assignments. No history was imported again. Production label protection was
configured in the native UI; a fresh member-account demonstration remains
separate from the user's earlier confirmation of enforcement.

Full delivered rehearsal remains pending. The admission deployment's project
shortcut currently points at the regional host because admission does not record
its project ID through the normal deployment verification flow. Use the exact
[admission project](https://cloud.langfuse.com/project/cmv0magyy08o7ad0e54ath8wi)
for this rehearsal; do not present the host-only shortcut as a working project link.

## Requested follow-up release

After initial registration, add three or four reusable text prompt components
under a separate prompt folder, compose them into the agent prompts through
Langfuse's native prompt references, verify resolution/version behavior, and
update the presenter story. This is an authorized follow-up release, not an
unrecorded change to the initial admission candidate.
