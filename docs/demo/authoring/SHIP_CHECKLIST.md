# Deployment pipeline follow-up — release checklist

This checklist records published v0.2.2. The unchanged story and companion carry
forward the completed v0.2.1 presenter rehearsal recorded in
[COMPONENTS_REHEARSAL.md](COMPONENTS_REHEARSAL.md). Those results do not establish
that the new deployment stages have run.

The requested change adds explicit target validation and cost estimation, retains
final verification, and exposes custom setup progress in Depot outside the logs.
It preserves the accepted story, seed content and companion interactions.

| Check | Status | Evidence / remaining work |
| --- | --- | --- |
| Accepted story | Passed, carried forward | Accepted story/prototype and v0.2.1 rehearsal; no story, fixture or companion implementation changed. |
| Required pipeline | Passed | All six deployed steps succeeded in order. [Admission receipt](evidence/preflight-admission.json). |
| Cost estimate | Passed | Finalised-event count tests pass; deployed UI shows 14,493 units with 5,137 observations and 9,356 scores. [Screenshot](evidence/preflight-custom-step.png). |
| Custom progress | Passed | Live evaluator setup displayed running with elapsed time outside closed logs, then advanced to seed. A later polling gap was fixed in PR #282 with mounted transition tests; final rebuilt page was checked. Failure/queued/quiet/completion states have Depot test coverage. [Screenshot](evidence/preflight-custom-step.png). |
| Offline checks | Passed | Candidate validation, conformance and 334 tests; see [preflight evidence](PREFLIGHT.md). |
| Seed and scale | Passed offline | Planned counts match finalised events at 1, 24, 72 and 1,620 history traces; golden unchanged. |
| Runtime assets | Passed | Automatic evaluator/model setup, post-seed experiment mappings and final current-run verification passed on the fresh project. |
| Live verification | Passed | Both the standalone and pipeline probes passed; final verification passed in `prompt-preflight-demo` within Boris Demo Enterprise. [Admission receipt](evidence/preflight-admission.json). |
| Companion | Passed, carried forward | v0.2.2 admission companion smoke passed; v0.2.1 delivered four-turn session and feedback remain applicable because companion code is unchanged. |
| Runbook/artifacts | Passed for this change | [README](../../../README.md) and [preflight guide](PREFLIGHT.md) document stages, scope and probe overhead; presenter journey unchanged. |
| Release/admission | Passed | v0.2.2 source `acb09ae2` and signed image passed CI and all six admission rungs in run `e86c64cd-b17d-4abe-aea0-0155aa17af7d`. [Release receipt](evidence/preflight-release.json), [admission](evidence/preflight-admission.png). |
| Publication/rollout | Passed | Kit and Depot changes merged to main; local Depot rebuilt, four existing companions preserved; registry sync shows v0.2.2 active and Published. [Rollout receipt](evidence/preflight-rollout.json), [member catalog](evidence/preflight-catalog.png). |
| Authoring skill | Passed locally | Maintained source, installed skill and packaged archive updated; local skills commit `b3d7e1a`. Frontmatter, local references and package/source parity checked. |

v0.2.2 is published and ready within the evidence scope above. The live run exercised
all six pipeline steps; a polling race found between seed and experiment setup was
fixed and tested in Depot PR #282. The rebuilt completed page was checked without
re-seeding. No second full live transition sequence after that UI fix is claimed.
The unchanged presenter journey uses the cited v0.2.1 rehearsal. The skill's full
checklist is maintained in `author-langfuse-demo-kit/SKILL.md`.
