# Depot onboarding — 2026-10-09

The user authorized Depot onboarding, registration and shipment, then approved
creating a dedicated project in Boris Demo Enterprise with a name ending in
`demo`. The existing final-seed project is preserved.

## Current release: v0.2.1

The exact signed `v0.2.1` candidate passed all six admission checks and the complete
delivered walkthrough in `prompt-components-demo`, inside Boris Demo Enterprise.
Automatic connection/evaluator setup, provider-free seed, post-import mappings,
native components, two real experiments, protected-label promotion, four live
turns, feedback and session links are verified. See the
[final rehearsal](COMPONENTS_REHEARSAL.md) and
[admission receipt](evidence/depot-admission-v0.2.1.json).
[Registry PR #280](https://github.com/borismichel/langfuse-demo-depot/pull/280)
merged at `386524cb70561ca3a4623b9fd2fec4fdc32759b1`. The primary Depot checkout
was fast-forwarded to that commit, preserving all seven unrelated untracked paths.
The final API image is
`sha256:7806a10e3be2e785b9e1144e25492dd75782c47532e5f5aa1716d6678e0dc462`;
health returned 200. The worker on the merged setup capability, PR #277 frontend,
and all three running companions were preserved. Authenticated registry sync
completed at `2026-10-09T08:25:39.024583Z`: `prompt` is v0.2.1, active and
Published with the exact admitted digest. The catalog visibly shows Financial
Services and prompt-management, experiments, evaluators plus four additional
features. The detail page lists all seven features and the text-component story.
[Catalog proof](evidence/depot-published-catalog-v0.2.1.png).

Local registry validation passed on the exact PR head, resolving all four release
pins. Depot's legacy self-hosted CI runner remained queued; no remote CI pass is
claimed for PR #280. Kit release CI and signed image publication both passed.
Release-tag documentation is an immutable pre-admission snapshot; main contains
the retrospective final receipts and current readiness statement.

The sections below preserve the earlier delivery sequence; their pending states
describe those historical checkpoints, not the final rehearsal verdict.

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

## Text-component release sequence

`v0.2.0` (`fc661fc88b06eed45eaf00670cc3d4fb5b55795f`) contains the text
components, catalog metadata and explicit setup pipeline. Its
[CI](https://github.com/borismichel/langfuse-synth-prompt/actions/runs/37900030832)
and [signed build](https://github.com/borismichel/langfuse-synth-prompt/actions/runs/37900034373)
passed. It has not been admitted or pinned in Depot.

Deployment review then found a shared contract gap: the original core/Depot
pipeline intentionally provides only Langfuse credentials to jobs, so an explicit
model-connection setup stage cannot receive Depot's provider key. The coordinated
follow-up adds an explicit custom-step secret declaration. It must retain the
provider-free seed boundary and avoid silently granting credentials to old kits.
The next kit release will opt in only for connection/evaluator setup. The immutable
`v0.2.0` tag will not move.

The fresh project `prompt-components-demo` (`cmv0nl149090gad0f8c5p5xcb`) was
created in Boris Demo Enterprise for that candidate. The user approved its project-scoped API key at action time. Credentials were
stored in Depot's existing admission reference and verified against this exact
project using observations v2 and datasets; both were empty. No model connection
or evaluator was manually created, so admission can prove the complete setup.
Production-label protection is enabled; final admission remains pending. Existing populated targets remain intact.

Depot's [PR #278](https://github.com/borismichel/langfuse-demo-depot/pull/278)
fixes the misleading admission-carrier publish controls; 20 relevant router tests
passed. It merged at `2b4622b46c70b7bd755a98bef184300a32d83dab`. The independent
catalog grouping cleanup in PR #277 is preserved and its frontend image is already
running locally. Final API/worker rebuild will include both and the final kit pin.

Core [PR #61](https://github.com/borismichel/langfuse-synth-core/pull/61) merged
with all three CI checks passing. Immutable `v4.2.0` points to
`f81f505b58b6a72f48a8a3d2d9919c75e2f90580`. Kit candidate `v0.2.1` pins that
release and opts only its initial evaluator-setup step into `LLM_API_KEY` delivery.
Its 325 tests and all conformance checks passed on that exact installed release.
The final kit release/admission and catalog sync are still pending.
