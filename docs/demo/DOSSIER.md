# prompt — demo workspace

Generated from `.demo/project.json`; rerun `python3 scripts/demo_workspace.py render`.
This reports handoff state, not runtime or deployment readiness.

Kit repository: https://github.com/borismichel/langfuse-synth-prompt
Core: https://github.com/borismichel/langfuse-synth-core at `v4.1.1` (`6b86ac16d797cd0c6a80da1cdd68e8fc8998c18d`). Runtime adoption is verified during authoring.
Depot: https://github.com/borismichel/langfuse-demo-depot

Association is recorded here. Catalog registration and admission are separate delivery actions.
Before a signed release, use this workspace in GitHub/local files. Depot Docs later shows a released snapshot.

| Stage | Effective status | Skill |
| --- | --- | --- |
| story | accepted | `develop-langfuse-demo-story` |
| prototype | accepted | `prototype-langfuse-demo` |
| authoring | ready | `author-langfuse-demo-kit` |

## Handoffs

A changed upstream checkpoint makes its consumers stale. Re-review and record a new checkpoint.
An accepted authoring handoff is not evidence that admission, deployment or rehearsal passed.

### story: accepted

Accepted story plus user instruction on 2026-10-08 to add proper live and historical tool trace shapes; business facts and presenter journey unchanged.

Recorded decision/evidence: `docs/demo/story/REVIEW.md`

- [docs/demo/story/EVALUATION_PLAN.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/EVALUATION_PLAN.md) — `5c05a051fea8`
- [docs/demo/story/GLOSSARY.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/GLOSSARY.md) — `ac56ee54c22c`
- [docs/demo/story/POPULATION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/POPULATION.md) — `6cfb9e5717b1`
- [docs/demo/story/PORTFOLIO.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PORTFOLIO.json) — `4b6e61a4741c`
- [docs/demo/story/PRODUCT_RESEARCH.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PRODUCT_RESEARCH.md) — `67caaddd1d07`
- [docs/demo/story/PROTOTYPE_HANDOFF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PROTOTYPE_HANDOFF.md) — `f007f51d1dd5`
- [docs/demo/story/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/REVIEW.md) — `efed84d33043`
- [docs/demo/story/STORY_BRIEF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/STORY_BRIEF.md) — `2e98b327d563`
- [docs/demo/story/TRACE_SHAPES.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/TRACE_SHAPES.md) — `34d8f08d1fb2`
- [docs/demo/story/cases/portfolio-examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/cases/portfolio-examples.json) — `7ae9d676f805`
- [docs/demo/story/cases/product-explainer.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/cases/product-explainer.json) — `030098d3c310`
- [docs/demo/story/story-contract.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/story-contract.yaml) — `020556c45f38`

### prototype: accepted

Retains user acceptance of prototype; compatibility reviewed for additive runtime trace-detail instruction. Original prototype screenshots do not claim to verify new tool spans.

Recorded decision/evidence: `docs/demo/prototype/REVIEW.md`

- [design/prototype/README.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/README.md) — `cf38d2c4577b`
- [design/prototype/index.html](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/index.html) — `f7b447417c84`
- [design/prototype/package-lock.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/package-lock.json) — `655e56e9ba14`
- [design/prototype/package.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/package.json) — `68641f7936cc`
- [design/prototype/public/fonts/GeistMono-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/GeistMono-OFL.txt) — `1781d2806a07`
- [design/prototype/public/fonts/Inter-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/Inter-OFL.txt) — `5b9321a4298c`
- [design/prototype/public/fonts/SpaceGrotesk-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/SpaceGrotesk-OFL.txt) — `564ce565c371`
- [design/prototype/public/fonts/geist-mono.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/geist-mono.ttf) — `5c1b7b77c2d6`
- [design/prototype/public/fonts/inter.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/inter.ttf) — `29160a80ff49`
- [design/prototype/public/fonts/space-grotesk.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/public/fonts/space-grotesk.ttf) — `3e699ead1876`
- [design/prototype/src/Link.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/Link.tsx) — `72a940f07081`
- [design/prototype/src/PayloadView.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/PayloadView.tsx) — `2f1f81bfce10`
- [design/prototype/src/TraceView.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/TraceView.tsx) — `b8ef81c141f0`
- [design/prototype/src/brand.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/brand.css) — `e392c790cb75`
- [design/prototype/src/check.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/check.mjs) — `c4439a9b1066`
- [design/prototype/src/data/dataset-extras.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/dataset-extras.json) — `45b26ac81f0f`
- [design/prototype/src/data/examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/examples.json) — `7ae9d676f805`
- [design/prototype/src/data/portfolio.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/portfolio.json) — `4b6e61a4741c`
- [design/prototype/src/data/product.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/product.json) — `030098d3c310`
- [design/prototype/src/langfuse-theme.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/langfuse-theme.css) — `c8e3182f9bce`
- [design/prototype/src/main.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/main.tsx) — `a018c7cb1765`
- [design/prototype/src/model.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/model.mjs) — `c100dab0009e`
- [design/prototype/src/population.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/population.mjs) — `1a143da3e2e4`
- [design/prototype/src/style.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/style.css) — `ed035dc53feb`
- [design/prototype/vendor/langfuse/LICENSE](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/LICENSE) — `fd09d42b5b16`
- [design/prototype/vendor/langfuse/provenance.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/provenance.json) — `28a898a55746`
- [design/prototype/vendor/langfuse/web/src/components/ItemBadge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ItemBadge.tsx) — `a5593e734b51`
- [design/prototype/vendor/langfuse/web/src/components/ScoreBadge/ScoreBadge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ScoreBadge/ScoreBadge.tsx) — `e5c74f8239c0`
- [design/prototype/vendor/langfuse/web/src/components/ScoreValue.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ScoreValue.tsx) — `75a6ea666492`
- [design/prototype/vendor/langfuse/web/src/components/design-system/Badge/Badge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/design-system/Badge/Badge.tsx) — `147f0396988c`
- [design/prototype/vendor/langfuse/web/src/components/design-system/HoverCard/HoverCard.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/design-system/HoverCard/HoverCard.tsx) — `ec83df5253fa`
- [design/prototype/vendor/langfuse/web/src/components/design-system/Spinner/Spinner.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/design-system/Spinner/Spinner.tsx) — `df5c76040ef5`
- [design/prototype/vendor/langfuse/web/src/components/design-system/Tooltip/Tooltip.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/design-system/Tooltip/Tooltip.tsx) — `e4a235125c7f`
- [design/prototype/vendor/langfuse/web/src/components/grouped-score-badge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/grouped-score-badge.tsx) — `3e5892e0f7f3`
- [design/prototype/vendor/langfuse/web/src/components/score-tag.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/score-tag.tsx) — `555c4071ee23`
- [design/prototype/vendor/langfuse/web/src/components/ui/CodeJsonViewer.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ui/CodeJsonViewer.tsx) — `5d25cc8a7970`
- [design/prototype/vendor/langfuse/web/src/components/ui/badge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ui/badge.tsx) — `adb415adb039`
- [design/prototype/vendor/langfuse/web/src/components/ui/button.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/components/ui/button.tsx) — `928f507d74a5`
- [design/prototype/vendor/langfuse/web/src/features/comments/CommentCountIcon.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/comments/CommentCountIcon.tsx) — `0418b35cf186`
- [design/prototype/vendor/langfuse/web/src/features/traces/components/ObservationLevelBadge.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/components/ObservationLevelBadge.tsx) — `ef333f0f4bdd`
- [design/prototype/vendor/langfuse/web/src/features/traces/components/SpanContent.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/components/SpanContent.tsx) — `e386aae550e7`
- [design/prototype/vendor/langfuse/web/src/features/traces/components/TraceTree.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/components/TraceTree.tsx) — `7ba9d54e57de`
- [design/prototype/vendor/langfuse/web/src/features/traces/components/VirtualizedTree.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/components/VirtualizedTree.tsx) — `4b4e9dca13c8`
- [design/prototype/vendor/langfuse/web/src/features/traces/components/VirtualizedTreeNodeWrapper.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/components/VirtualizedTreeNodeWrapper.tsx) — `4faecb12e900`
- [design/prototype/vendor/langfuse/web/src/features/traces/contexts/SelectionContext.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/contexts/SelectionContext.tsx) — `2a439c0bc32e`
- [design/prototype/vendor/langfuse/web/src/features/traces/contexts/TraceDataContext.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/contexts/TraceDataContext.tsx) — `6dd24c97adcc`
- [design/prototype/vendor/langfuse/web/src/features/traces/contexts/ViewPreferencesContext.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/contexts/ViewPreferencesContext.tsx) — `e7dbdb285fd8`
- [design/prototype/vendor/langfuse/web/src/features/traces/fns/flattenTree.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/fns/flattenTree.ts) — `a39fb852a61c`
- [design/prototype/vendor/langfuse/web/src/features/traces/fns/metricEmphasis.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/fns/metricEmphasis.ts) — `b29d843e742e`
- [design/prototype/vendor/langfuse/web/src/features/traces/fns/nodeScores.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/fns/nodeScores.ts) — `88379766b17b`
- [design/prototype/vendor/langfuse/web/src/features/traces/fns/visualDepth.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/fns/visualDepth.ts) — `5f30b05614ab`
- [design/prototype/vendor/langfuse/web/src/features/traces/hooks/useHandlePrefetchObservation.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/hooks/useHandlePrefetchObservation.ts) — `9b3a1e4f6370`
- [design/prototype/vendor/langfuse/web/src/features/traces/hooks/useSelectTraceNode.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/features/traces/hooks/useSelectTraceNode.ts) — `f01ed9d8844e`
- [design/prototype/vendor/langfuse/web/src/fixture-context.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/fixture-context.tsx) — `4ac0ad0e6c2a`
- [design/prototype/vendor/langfuse/web/src/hooks/useProjectIdFromURL.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/hooks/useProjectIdFromURL.ts) — `2c41cf029451`
- [design/prototype/vendor/langfuse/web/src/utils/dates.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/utils/dates.ts) — `3173e4feeff6`
- [design/prototype/vendor/langfuse/web/src/utils/numbers.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/utils/numbers.ts) — `7ba1d8d92b98`
- [design/prototype/vendor/langfuse/web/src/utils/tailwind.ts](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vendor/langfuse/web/src/utils/tailwind.ts) — `3bdbf0cbe0fb`
- [design/prototype/vite.config.js](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/vite.config.js) — `e073e0acc225`
- [docs/demo/prototype/BRIEF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/BRIEF.md) — `a749b72d4448`
- [docs/demo/prototype/PROVENANCE.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/PROVENANCE.json) — `ca908ddec9fe`
- [docs/demo/prototype/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/REVIEW.md) — `f4ddfe8104df`
- [docs/demo/prototype/evidence/build.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/build.txt) — `0e324e7cf7d7`
- [docs/demo/prototype/evidence/companion-dark-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-dark-wide.jpg) — `bc0b2d0d1e33`
- [docs/demo/prototype/evidence/companion-laptop.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-laptop.jpg) — `b18cbec7a3da`
- [docs/demo/prototype/evidence/companion-light-narrow.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-light-narrow.jpg) — `b87c67114118`
- [docs/demo/prototype/evidence/input-scores-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/input-scores-wide.jpg) — `43e5e9124875`
- [docs/demo/prototype/evidence/model-check.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/model-check.txt) — `d068a283a8bf`
- [docs/demo/prototype/evidence/session-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/session-wide.jpg) — `7004122d1237`
- [docs/demo/prototype/evidence/trace-dark.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/trace-dark.jpg) — `6604419e5c86`

### authoring: ready

Implementation available for review; fresh Langfuse skill audit records trace-design refinements. Prior 103-test offline evidence remains; revised live tracing, model/evaluation setup and admission/rehearsal pending.

Recorded decision/evidence: `docs/demo/authoring/REVIEW.md`

- [.dockerignore](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.dockerignore) — `be988156e3df`
- [.github/workflows/ci.yml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.github/workflows/ci.yml) — `8f2ce277c9ea`
- [.github/workflows/publish.yml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.github/workflows/publish.yml) — `23fc4ffe24a0`
- [DEMO_SCRIPT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/DEMO_SCRIPT.md) — `8b05336c2adc`
- [Dockerfile](https://github.com/borismichel/langfuse-synth-prompt/blob/main/Dockerfile) — `deba3d44aa16`
- [README.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/README.md) — `10ce77c85435`
- [config/demo.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/config/demo.yaml) — `928ae61db19d`
- [docs/demo/authoring/ASSETS.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/ASSETS.md) — `f3f55a3b1fea`
- [docs/demo/authoring/COMPANION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/COMPANION.md) — `a11cebc25d9c`
- [docs/demo/authoring/GENERATION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/GENERATION.md) — `43c1f53bf7ac`
- [docs/demo/authoring/READINESS_RESEARCH.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/READINESS_RESEARCH.md) — `81808b79557a`
- [docs/demo/authoring/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/REVIEW.md) — `e06ecfb0a5d6`
- [docs/demo/authoring/TRACE_DESIGN_AUDIT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/TRACE_DESIGN_AUDIT.md) — `1a06ee2459d7`
- [docs/demo/authoring/evidence/companion-four-turns.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/companion-four-turns.jpg) — `f72337cd508f`
- [docs/demo/authoring/evidence/conformance.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/conformance.txt) — `a9b96c0c2377`
- [docs/demo/authoring/evidence/container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/container-smoke.json) — `41d8fd061ae9`
- [docs/demo/authoring/evidence/dependencies.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/dependencies.txt) — `9261363b7330`
- [docs/demo/authoring/evidence/live-pilot.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/live-pilot.json) — `9e74ab3c774c`
- [docs/demo/authoring/evidence/manifest.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/manifest.txt) — `7d5842c99f93`
- [docs/demo/authoring/evidence/preview-rehearsal.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preview-rehearsal.md) — `ca43efbb71b4`
- [docs/demo/authoring/evidence/schema-check.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/schema-check.json) — `29a3c2b107a4`
- [docs/demo/authoring/evidence/tests.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/tests.txt) — `eaa5159d31e6`
- [docs/demo/authoring/evidence/trace-shapes.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/trace-shapes.json) — `c895df736326`
- [pyproject.toml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/pyproject.toml) — `fda8837ecbae`
- [src/synth/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/__init__.py) — `21d4cf5ad7b9`
- [src/synth/assets.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/assets.py) — `e2ac8f837110`
- [src/synth/catalog.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/catalog.py) — `24c0a467ce81`
- [src/synth/cli.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/cli.py) — `44c23d7a243a`
- [src/synth/companion/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/__init__.py) — `37d535e6c923`
- [src/synth/companion/app.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/app.py) — `a501d568d6e2`
- [src/synth/companion/preview.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/preview.py) — `c123ab034561`
- [src/synth/companion/service.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/service.py) — `af8e99ea4355`
- [src/synth/companion/static/app.js](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/app.js) — `e1a3565d2ef5`
- [src/synth/companion/static/brand.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/brand.css) — `e392c790cb75`
- [src/synth/companion/static/fonts/GeistMono-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/GeistMono-OFL.txt) — `1781d2806a07`
- [src/synth/companion/static/fonts/Inter-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/Inter-OFL.txt) — `5b9321a4298c`
- [src/synth/companion/static/fonts/SpaceGrotesk-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/SpaceGrotesk-OFL.txt) — `564ce565c371`
- [src/synth/companion/static/fonts/geist-mono.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/geist-mono.ttf) — `5c1b7b77c2d6`
- [src/synth/companion/static/fonts/inter.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/inter.ttf) — `29160a80ff49`
- [src/synth/companion/static/fonts/space-grotesk.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/space-grotesk.ttf) — `3e699ead1876`
- [src/synth/companion/static/style.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/style.css) — `d6176629480e`
- [src/synth/companion/templates/index.html](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/templates/index.html) — `66067fc31796`
- [src/synth/config.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/config.py) — `ef06dea8b1c4`
- [src/synth/fixtures/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/__init__.py) — `e3b0c44298fc`
- [src/synth/fixtures/conversations.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/conversations.json) — `645d3b660bc8`
- [src/synth/fixtures/dataset_extras.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/dataset_extras.json) — `45b26ac81f0f`
- [src/synth/fixtures/examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/examples.json) — `7ae9d676f805`
- [src/synth/fixtures/portfolio.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/portfolio.json) — `4b6e61a4741c`
- [src/synth/fixtures/product.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/product.json) — `030098d3c310`
- [src/synth/fixtures/prompt_versions.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/prompt_versions.json) — `ae39acd9b97e`
- [src/synth/fixtures/score_definitions.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/score_definitions.json) — `ac07b3e27505`
- [src/synth/materialize.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/materialize.py) — `a7b5d27f09d0`
- [src/synth/receipt.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/receipt.py) — `9854ce86edff`
- [src/synth/reference_tools.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/reference_tools.py) — `2c79963ce389`
- [src/synth/seed.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/seed.py) — `8c83ac4af7e1`
- [src/synth/state.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/state.py) — `14bb31fb1607`
- [src/synth/verify.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/verify.py) — `4b1a92d85e8b`
- [tests/golden/prompt_spool.ndjson](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/golden/prompt_spool.ndjson) — `77cd4ce99d3a`
- [tests/golden_seed.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/golden_seed.py) — `89ca40c5528d`
- [tests/test_assets.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_assets.py) — `ad15b34bae4f`
- [tests/test_companion_runtime.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_companion_runtime.py) — `7a7523d058a5`
- [tests/test_configuration_refresh.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_configuration_refresh.py) — `07c12bdf77d6`
- [tests/test_determinism.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_determinism.py) — `24549a562ff4`
- [tests/test_generation.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_generation.py) — `db0798ab7362`
- [tests/test_provider_binding.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_provider_binding.py) — `79cf5dd1b2b9`
- [tests/test_reference_tools.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_reference_tools.py) — `af580e58cad2`
- [tests/test_repeatability.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_repeatability.py) — `f1cd978ab6ba`
- [tests/test_retargeting.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_retargeting.py) — `c537b647b91f`
- [tests/test_run_evidence.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_run_evidence.py) — `dcbf5bfb10c6`
- [tests/test_validate.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_validate.py) — `07384e5e7acd`
- [usecase.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/usecase.yaml) — `7067c1d4c6dd`

## Readiness

Authoring must report offline checks, current-run live verification, signed release,
Depot admission and delivered presenter rehearsal separately, with evidence.
Neither this status file nor an accepted document performs those checks.
