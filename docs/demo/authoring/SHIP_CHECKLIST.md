# Deployment pipeline follow-up — release checklist

This checklist tracks the candidate after v0.2.1. The published v0.2.1 release and
its completed presenter rehearsal remain recorded in
[COMPONENTS_REHEARSAL.md](COMPONENTS_REHEARSAL.md). Those results do not establish
that the new deployment stages have run.

The requested change adds explicit target validation and cost estimation, retains
final verification, and exposes custom setup progress in Depot outside the logs.
It preserves the accepted story, seed content and companion interactions.

| Check | Status | Evidence / remaining work |
| --- | --- | --- |
| Accepted story | Passed, carried forward | Accepted story/prototype and v0.2.1 rehearsal; no story or fixture change intended. |
| Required pipeline | Passed offline | Probe → plan → evaluator setup → seed → experiment setup → verify; test actual Manifest dispatch. |
| Cost estimate | Pending | Compare planned v4 observations/scores with finalised seed data, including fixed experiment overhead; display exact estimate in Depot. |
| Custom progress | Pending | Depot must show the current setup step, elapsed/liveness, failure and completion outside logs. |
| Offline checks | Passed | Candidate validation, conformance and 334 tests; see [preflight evidence](PREFLIGHT.md). |
| Seed and scale | Passed offline | Planned counts match finalised events at 1, 24, 72 and 1,620 history traces; golden unchanged. |
| Runtime assets | Passed, carried forward | v0.2.1 automatic setup and current-run native evaluator mappings; provisioning implementation unchanged. New pipeline order still needs admission. |
| Live verification | Pending | Exercise the new probe and retain exact-current-run final verification on a fresh admission target. |
| Companion | Passed, carried forward | v0.2.1 delivered four-turn session and feedback; companion code unchanged. |
| Runbook/artifacts | Pending | Document new preflight stages and estimate scope in the delivered instructions. |
| Release/admission | Pending | New immutable release and its admission run; never re-import a populated project. |
| Publication/rollout | Pending | Merge owning repositories, preserve active companions, rebuild Depot and verify member catalog release. |
| Authoring skill | Passed locally | Maintained source, installed skill and packaged archive updated; local skills commit `b3d7e1a`. Frontmatter, local references and package/source parity checked. |

Readiness remains pending for this candidate until the applicable rows above have
observed evidence. The skill's full checklist is maintained in
`author-langfuse-demo-kit/SKILL.md`.
