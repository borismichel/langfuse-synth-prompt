# Depot admission access and deployment prerequisites

Checked 2026-10-08 through read-only source inspection, container metadata,
configuration-presence flags and one database-schema query. No browser interaction,
cookie extraction, credential creation, secret output, admission request, service
change, registry edit or publication occurred.

Workspace status before consuming the handoff: story **accepted**, prototype
**accepted**, authoring **ready**. This report supplements
[READINESS_RESEARCH.md](READINESS_RESEARCH.md); it does not establish admission or
delivered rehearsal success.

## Established session cannot currently drive admission

The existing signed-in administrator browser is sufficient for Depot's normal
admin controls. The inspected deployment does **not** expose an admission browser
action, an admission API proxy, or a normal session-token export control.

The supported admission endpoint is on the API origin:

```text
POST http://localhost:8000/api/v1/admin/admission
GET  http://localhost:8000/api/v1/admin/admission/{run_id}
```

The POST body, once its prerequisites are met, is:

```json
{
  "slug": "prompt",
  "repo_url": "https://github.com/borismichel/langfuse-synth-prompt",
  "ref": "<immutable CI-published signed release tag>"
}
```

The web runs on `http://localhost:3009`; it is not a general API reverse proxy.
Its API requests are made server-side: `authorizedFetch` receives a validated
Auth.js session and creates a separate five-minute API bearer internally.
The Auth.js session callback returns user/provider information, not this bearer.
The API validates its separate issuer/audience JWT contract. Reusing or exporting
a browser cookie is neither necessary nor an established admission workflow.

The local admin guide explicitly calls admission **API-only** and documents a
direct-signing example. That example requires the session-signing secret and
therefore does **not** satisfy the user's no-auth-workaround constraint. It was
not executed. The authoring delivery reference likewise requires an established
admin-session credential through an approved credential workflow; it does not
supply one from the browser.

**Concrete prerequisite:** Depot's operator must supply an approved admission
access path that preserves the authenticated identity without exporting cookies
or signing credentials manually. A deliberately supported, authenticated
server-side admission action/proxy would meet that shape, but it is absent in
this deployed web build and adding it is Depot work, not a kit-side workaround.
An operator-provided supported external session credential workflow is another
possible prerequisite, but none was found or claimed here.

## Running deployment facts

| Check | Observed result | Consequence |
| --- | --- | --- |
| Checkout revision | `edf5e853b36b04a5a88ea5f3accf2453c7ff5f86` | Source provenance only; no running image revision label is set |
| API/worker image ID | `sha256:40e94bc86737eb113f34e709dbfa21df64db5d0b45607c32f9dde7eabcfb1101` | Both containers created 2026-10-01 |
| Web image ID | `sha256:bc63e9312e18894102d669d1ee0786a3b576b4ddda66ad32400114153c05f3d1` | Container created 2026-09-18 |
| Running API source comparison | Admission orchestration, admission router, use-case model, registry sync and settings files all hash-identical to checkout | Findings below apply to the inspected running API files, not merely an unbuilt checkout |
| Running web route manifest | Auth, artifact, use-case asset, job-log and live-surface routes; no admission proxy or token-export route | No general `/api/v1/*` forwarding route exists |
| Manifest-slug guard | **Absent** in inspected router/orchestration | The release-specific delivery requirement for a current Depot with the guard is not met |
| New catalog entry visibility | **Published**, confirmed from the running database's `use_cases.visibility` column default | First registry sync could expose the kit to members; do not assume staging |
| Existing catalog entry visibility | Sync omits visibility from updates | Existing admin choices survive re-sync |
| `ADMISSION_SCRATCH_BASE_URL` nonempty | **true** in running API environment | Presence only |
| `ADMISSION_SCRATCH_HOST_KIND` nonempty | **true** in running API environment | Presence only; value not recorded |
| `ADMISSION_SCRATCH_SECRET_PATH` nonempty | **true** in running API environment | Presence only; value not recorded |

Scratch presence meets the source's simple configured check (nonempty base URL
and secret-path reference), but does **not** verify the referenced keys, target
health, isolation, reset state, or permission to reuse that project for this kit.
No secret-store reads were made. A disposable target must be confirmed before
admission because its seed writes append observations.

The missing slug guard is concrete: `_prepare_candidate` reads the manifest and
resolves the image without comparing `manifest.slug` to the requested slug;
`start_admission_run` validates and parses it, then stores the separately supplied
`candidate_slug` without that comparison. No candidate was submitted to test it.

## Delivery sequence once prerequisites are resolved

1. Use a deployed Depot with the Manifest-slug guard and confirmed staging-first
   catalog behavior, or an explicitly reviewed equivalent staging procedure.
   Updating Depot belongs in its own repository and deployment workflow.
2. Establish a supported admission access path and confirm the configured scratch
   target is disposable, ready and authorized for this candidate.
3. Submit the exact immutable CI-published signed candidate using the API or a
   separately installed newer authoring CLI. Preserve runtime core `v4.1.1`.
4. Retain the run ID, resolved commit, image digest and complete ladder verdict;
   resume with GET. Only `eligible_to_pin: true` permits registry pinning.
5. Verify the actual entry remains in staging and is inaccessible to members,
   then rehearse the delivered runbook before any authorized publication.

**Admission remains pending:** the current deployment lacks the required slug
guard, defaults new catalog entries to published, and has no supported browser
session-to-admission access surface under the user's constraints. Scratch
configuration exists, but its operational suitability remains unverified.

## Sources

Paths below are in neighbouring `langfuse-demo-depot` at the recorded revision.

- `docs/user/admin-guide.md:177–243`: API-only admission, token contract and POST/GET.
- `web/lib/api.ts:497–519`, `web/lib/session-token.ts:28–47`: server-side API session bearer.
- `web/auth.ts:308–321`: browser session projection.
- `web/next.config.ts`: headers only; no API rewrites.
- Running web `/app/.next/server/app-paths-manifest.json`: deployed route inventory.
- `api/app/auth.py:65–120`: API bearer/cookie extraction and JWT validation.
- `api/app/routers/admission.py:57–88` and `api/app/admission.py:590–635`: candidate preparation and admission registration.
- `api/app/models/tables.py:119–130`, `tools/sync_ops.py:359–387`,
  `api/alembic/versions/0028_use_case_visibility.py:40–50`: published default and visibility-preserving sync.
- Running PostgreSQL schema query of `information_schema.columns` for
  `public.use_cases.visibility`: returned `'published'::use_case_visibility`.
- `api/app/config.py:475–487`, `api/app/admission.py:449–463`: scratch configuration and configured check.
- `infra/docker-compose.host.yml:28–91`: loopback API/web topology.
- `/Users/bmichel/.agents/skills/author-langfuse-demo-kit/references/delivery.md`:
  current Depot, guarded slug, disposable target, admission and staging requirements.
