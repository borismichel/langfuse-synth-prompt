# prompt — demo workspace

Generated from `.demo/project.json`; rerun `python3 scripts/demo_workspace.py render`.
This reports handoff state, not runtime or deployment readiness.

Kit repository: https://github.com/borismichel/langfuse-synth-prompt
Core: https://github.com/borismichel/langfuse-synth-core at `v4.2.0` (`f81f505b58b6a72f48a8a3d2d9919c75e2f90580`). Runtime adoption is verified during authoring.
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

User correction: seeded, task-specific building-block references with selective coverage and working shared voice transitions.

Recorded decision/evidence: `docs/demo/story/REVIEW.md`

- [docs/demo/story/EVALUATION_PLAN.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/EVALUATION_PLAN.md) — `c8edaf12b445`
- [docs/demo/story/GLOSSARY.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/GLOSSARY.md) — `ac56ee54c22c`
- [docs/demo/story/MODEL_POLICY.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/MODEL_POLICY.md) — `ca380ff02182`
- [docs/demo/story/POPULATION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/POPULATION.md) — `c3e5edb6177a`
- [docs/demo/story/PORTFOLIO.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PORTFOLIO.json) — `4b6e61a4741c`
- [docs/demo/story/PRODUCT_RESEARCH.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PRODUCT_RESEARCH.md) — `67caaddd1d07`
- [docs/demo/story/PROTOTYPE_HANDOFF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/PROTOTYPE_HANDOFF.md) — `54b0336004ac`
- [docs/demo/story/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/REVIEW.md) — `11eab947b4bf`
- [docs/demo/story/STORY_BRIEF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/STORY_BRIEF.md) — `59218302ac17`
- [docs/demo/story/TRACE_SHAPES.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/TRACE_SHAPES.md) — `4dfcffb3b814`
- [docs/demo/story/cases/portfolio-examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/cases/portfolio-examples.json) — `7ae9d676f805`
- [docs/demo/story/cases/product-explainer.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/cases/product-explainer.json) — `95f81e1fa906`
- [docs/demo/story/story-contract.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/story/story-contract.yaml) — `cb9ce9b0b719`

### prototype: accepted

Accepted layout retained; user-directed composition correction aligned in shared baseline/candidate case. Live production reference resolution rehearsed.

Recorded decision/evidence: `docs/demo/prototype/REVIEW.md`

- [design/prototype/README.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/README.md) — `cf38d2c4577b`
- [design/prototype/index.html](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/index.html) — `aa8747f55236`
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
- [design/prototype/src/TraceView.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/TraceView.tsx) — `24d36a031ec2`
- [design/prototype/src/brand.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/brand.css) — `e392c790cb75`
- [design/prototype/src/check.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/check.mjs) — `f7f66a5d3a14`
- [design/prototype/src/data/dataset-extras.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/dataset-extras.json) — `45b26ac81f0f`
- [design/prototype/src/data/examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/examples.json) — `7ae9d676f805`
- [design/prototype/src/data/model-policy.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/model-policy.json) — `695ca751bf29`
- [design/prototype/src/data/portfolio.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/portfolio.json) — `4b6e61a4741c`
- [design/prototype/src/data/product.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/data/product.json) — `95f81e1fa906`
- [design/prototype/src/langfuse-theme.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/langfuse-theme.css) — `c8e3182f9bce`
- [design/prototype/src/main.tsx](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/main.tsx) — `6e64f8a682b6`
- [design/prototype/src/model.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/model.mjs) — `09b7da708ddd`
- [design/prototype/src/population.mjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/design/prototype/src/population.mjs) — `80110dd536cf`
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
- [docs/demo/prototype/BRIEF.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/BRIEF.md) — `68bbb357edf8`
- [docs/demo/prototype/PROVENANCE.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/PROVENANCE.json) — `ca908ddec9fe`
- [docs/demo/prototype/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/REVIEW.md) — `1955235f427d`
- [docs/demo/prototype/evidence/build.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/build.txt) — `0e324e7cf7d7`
- [docs/demo/prototype/evidence/categorical-checks.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/categorical-checks.md) — `36f177d57ebf`
- [docs/demo/prototype/evidence/categorical-control-dark.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/categorical-control-dark.jpg) — `8e1305c7ed89`
- [docs/demo/prototype/evidence/companion-dark-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-dark-wide.jpg) — `bc0b2d0d1e33`
- [docs/demo/prototype/evidence/companion-laptop.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-laptop.jpg) — `b18cbec7a3da`
- [docs/demo/prototype/evidence/companion-light-narrow.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/companion-light-narrow.jpg) — `b87c67114118`
- [docs/demo/prototype/evidence/input-scores-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/input-scores-wide.jpg) — `43e5e9124875`
- [docs/demo/prototype/evidence/model-check.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/model-check.txt) — `d068a283a8bf`
- [docs/demo/prototype/evidence/session-wide.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/session-wide.jpg) — `7004122d1237`
- [docs/demo/prototype/evidence/trace-dark.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/prototype/evidence/trace-dark.jpg) — `6604419e5c86`

### authoring: ready

Optional prompt retrieval/variable example installed on requested current companion and saved in source. Visual and syntax checks pass. Existing published v0.2.5 image unchanged; example awaits next release.

Recorded decision/evidence: `docs/demo/authoring/REVIEW.md`

- [.dockerignore](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.dockerignore) — `be988156e3df`
- [.github/workflows/ci.yml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.github/workflows/ci.yml) — `c4a1fbb32d36`
- [.github/workflows/publish.yml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/.github/workflows/publish.yml) — `e6091cc13e45`
- [DEMO_SCRIPT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/DEMO_SCRIPT.md) — `c8699cf6ab09`
- [Dockerfile](https://github.com/borismichel/langfuse-synth-prompt/blob/main/Dockerfile) — `086aaccafa08`
- [README.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/README.md) — `ec35d35e3b85`
- [config/demo.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/config/demo.yaml) — `f11d13f1d2db`
- [docs/demo/authoring/ASSETS.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/ASSETS.md) — `77c79438053d`
- [docs/demo/authoring/BRAND_REFINEMENT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/BRAND_REFINEMENT.md) — `84c62a32fc75`
- [docs/demo/authoring/BUILDING_BLOCKS.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/BUILDING_BLOCKS.md) — `c41cb2b90f6a`
- [docs/demo/authoring/CATEGORICAL_BUILD.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/CATEGORICAL_BUILD.md) — `4e0f30230e11`
- [docs/demo/authoring/COMPANION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/COMPANION.md) — `4b751107be1e`
- [docs/demo/authoring/COMPONENTS_REHEARSAL.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/COMPONENTS_REHEARSAL.md) — `cf1f6f90f97c`
- [docs/demo/authoring/CROSS_KIT_SEED_REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/CROSS_KIT_SEED_REVIEW.md) — `484b3a80a986`
- [docs/demo/authoring/DEPOT_ACCESS.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/DEPOT_ACCESS.md) — `642083047cfa`
- [docs/demo/authoring/DEPOT_ONBOARDING.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/DEPOT_ONBOARDING.md) — `b01893367f54`
- [docs/demo/authoring/EVALUATOR_MAPPING_REPAIR.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/EVALUATOR_MAPPING_REPAIR.md) — `bb4188ac4cc6`
- [docs/demo/authoring/FINAL_SEED.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/FINAL_SEED.md) — `5ab944374d79`
- [docs/demo/authoring/FRESH_PROJECT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/FRESH_PROJECT.md) — `328d75f111bc`
- [docs/demo/authoring/FULL_VOLUME.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/FULL_VOLUME.md) — `dd7ae7764258`
- [docs/demo/authoring/GENERATION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/GENERATION.md) — `0b41220a4b17`
- [docs/demo/authoring/HISTORY_REPLACEMENT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/HISTORY_REPLACEMENT.md) — `f7bfe7356aec`
- [docs/demo/authoring/NATIVE_REHEARSAL.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/NATIVE_REHEARSAL.md) — `70f2eb321608`
- [docs/demo/authoring/NULLABLE_EVALUATOR_RESEARCH.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/NULLABLE_EVALUATOR_RESEARCH.md) — `7376545a02d1`
- [docs/demo/authoring/OPERATIONAL_REVISION.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/OPERATIONAL_REVISION.md) — `836e3abe436e`
- [docs/demo/authoring/PREFLIGHT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/PREFLIGHT.md) — `f26b9e7dd9cb`
- [docs/demo/authoring/READINESS_RESEARCH.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/READINESS_RESEARCH.md) — `f2d8eb33bb46`
- [docs/demo/authoring/REVIEW.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/REVIEW.md) — `a8c9b18b2c29`
- [docs/demo/authoring/SHIP_CHECKLIST.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/SHIP_CHECKLIST.md) — `4bcf466003b2`
- [docs/demo/authoring/TRACE_DESIGN_AUDIT.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/TRACE_DESIGN_AUDIT.md) — `3399ccf4c7d7`
- [docs/demo/authoring/V4_COMPATIBILITY.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/V4_COMPATIBILITY.md) — `f99cc56d1d6f`
- [docs/demo/authoring/evidence/application-guide-companion.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/application-guide-companion.png) — `e58fce90b9be`
- [docs/demo/authoring/evidence/application-guide-fixed-companion.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/application-guide-fixed-companion.png) — `48ae0ca0e637`
- [docs/demo/authoring/evidence/application-guide-live.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/application-guide-live.json) — `fba8593e64cb`
- [docs/demo/authoring/evidence/application-guide-metadata-fixed.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/application-guide-metadata-fixed.json) — `b64709a50389`
- [docs/demo/authoring/evidence/application-guide-session.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/application-guide-session.png) — `e9270bac6158`
- [docs/demo/authoring/evidence/brand-companion-dark-mobile.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-dark-mobile.png) — `6dccb4da7188`
- [docs/demo/authoring/evidence/brand-companion-dark-wide.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-dark-wide.png) — `f2f1f3a882e7`
- [docs/demo/authoring/evidence/brand-companion-focus.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-focus.png) — `163442e767c8`
- [docs/demo/authoring/evidence/brand-companion-light-mobile.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-light-mobile.png) — `f91f862c5ce7`
- [docs/demo/authoring/evidence/brand-companion-light-wide.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-light-wide.png) — `d5e7ce0ace5c`
- [docs/demo/authoring/evidence/brand-companion-live.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-companion-live.png) — `37942b0cbbd3`
- [docs/demo/authoring/evidence/brand-container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/brand-container-smoke.json) — `ab161adb9452`
- [docs/demo/authoring/evidence/categorical-container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-container-smoke.json) — `6963b76ba0ff`
- [docs/demo/authoring/evidence/categorical-evaluators.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-evaluators.json) — `910536bbfd5c`
- [docs/demo/authoring/evidence/categorical-live-companion.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-live-companion.png) — `b9f8c7603ca4`
- [docs/demo/authoring/evidence/categorical-live-session.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-live-session.json) — `19589315edbd`
- [docs/demo/authoring/evidence/categorical-native-session.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-native-session.png) — `a3cd84912f84`
- [docs/demo/authoring/evidence/categorical-native-trace.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/categorical-native-trace.png) — `5259bf906040`
- [docs/demo/authoring/evidence/chat-controls-hotfix.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/chat-controls-hotfix.json) — `3b44381a598c`
- [docs/demo/authoring/evidence/chat-controls-thinking.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/chat-controls-thinking.png) — `56731a1e1ca9`
- [docs/demo/authoring/evidence/chat-pending-hotfix.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/chat-pending-hotfix.json) — `3d732e147608`
- [docs/demo/authoring/evidence/chat-pending.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/chat-pending.png) — `8377f503dc13`
- [docs/demo/authoring/evidence/companion-four-turns.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/companion-four-turns.jpg) — `f72337cd508f`
- [docs/demo/authoring/evidence/companion-prompt-example.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/companion-prompt-example.png) — `59b3c772db2c`
- [docs/demo/authoring/evidence/components-before-promotion.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-before-promotion.png) — `d283675fdea0`
- [docs/demo/authoring/evidence/components-experiments.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-experiments.json) — `6c8791365c34`
- [docs/demo/authoring/evidence/components-folder.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-folder.png) — `4e334311ad50`
- [docs/demo/authoring/evidence/components-generation-prompt.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-generation-prompt.png) — `2157f329f25e`
- [docs/demo/authoring/evidence/components-live-feedback.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-live-feedback.png) — `51858acf8337`
- [docs/demo/authoring/evidence/components-live-session.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-live-session.json) — `47bcb0c6a7f8`
- [docs/demo/authoring/evidence/components-native-comparison.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-native-comparison.png) — `61f4f6745529`
- [docs/demo/authoring/evidence/components-native-session.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-native-session.png) — `bc05a3455567`
- [docs/demo/authoring/evidence/components-production-protection.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-production-protection.png) — `5edb16d8d3c8`
- [docs/demo/authoring/evidence/components-production-v9.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-production-v9.png) — `7a6d71f613e7`
- [docs/demo/authoring/evidence/components-project-empty.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-project-empty.png) — `8e3d76977c23`
- [docs/demo/authoring/evidence/components-prompt-metrics.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-prompt-metrics.png) — `17629d60333d`
- [docs/demo/authoring/evidence/components-staging-v9.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-staging-v9.png) — `ab6cce52ed71`
- [docs/demo/authoring/evidence/components-voice.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/components-voice.png) — `fd6a90b32ce9`
- [docs/demo/authoring/evidence/configuration-refresh-readback.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/configuration-refresh-readback.json) — `8e98338bda07`
- [docs/demo/authoring/evidence/conformance-v0.2.1.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/conformance-v0.2.1.txt) — `a9b96c0c2377`
- [docs/demo/authoring/evidence/conformance.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/conformance.txt) — `a9b96c0c2377`
- [docs/demo/authoring/evidence/container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/container-smoke.json) — `41d8fd061ae9`
- [docs/demo/authoring/evidence/dependencies.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/dependencies.txt) — `9261363b7330`
- [docs/demo/authoring/evidence/depot-admission-project.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-admission-project.png) — `70633097170f`
- [docs/demo/authoring/evidence/depot-admission-v0.1.0.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-admission-v0.1.0.json) — `5d1ef0129759`
- [docs/demo/authoring/evidence/depot-admission-v0.2.1.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-admission-v0.2.1.json) — `371939b5b6bd`
- [docs/demo/authoring/evidence/depot-production-protection.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-production-protection.png) — `a15b2e8d089b`
- [docs/demo/authoring/evidence/depot-published-catalog-v0.1.0.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-published-catalog-v0.1.0.png) — `e2ef73fcc286`
- [docs/demo/authoring/evidence/depot-published-catalog-v0.2.1.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/depot-published-catalog-v0.2.1.png) — `17bcd2b7410f`
- [docs/demo/authoring/evidence/evaluator-experiment-mappings.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/evaluator-experiment-mappings.png) — `e4f9b30605f2`
- [docs/demo/authoring/evidence/evaluator-live-mappings.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/evaluator-live-mappings.png) — `84e96adf273f`
- [docs/demo/authoring/evidence/evaluator-mapping-readback.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/evaluator-mapping-readback.json) — `52e11dc89726`
- [docs/demo/authoring/evidence/experiment-context-repair.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/experiment-context-repair.json) — `5cc23ae1917e`
- [docs/demo/authoring/evidence/final-seed-inventory.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/final-seed-inventory.json) — `e5ea848beef3`
- [docs/demo/authoring/evidence/final-seed-live.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/final-seed-live.json) — `5096f00c9f1a`
- [docs/demo/authoring/evidence/final-seed-prompt-metrics.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/final-seed-prompt-metrics.png) — `dcc16e408983`
- [docs/demo/authoring/evidence/final-seed-protected-label.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/final-seed-protected-label.png) — `9d19e7a1dbf2`
- [docs/demo/authoring/evidence/final-seed-verification.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/final-seed-verification.json) — `38762c6f2233`
- [docs/demo/authoring/evidence/fresh-authored-experiments.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-authored-experiments.png) — `7c6213f858e6`
- [docs/demo/authoring/evidence/fresh-historical-tool.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-historical-tool.png) — `0a8c83b06417`
- [docs/demo/authoring/evidence/fresh-live-companion.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-live-companion.png) — `7d56d6d1beb9`
- [docs/demo/authoring/evidence/fresh-native-session.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-native-session.png) — `97317d1fbd02`
- [docs/demo/authoring/evidence/fresh-project-live.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-project-live.json) — `4233bc8c1536`
- [docs/demo/authoring/evidence/fresh-project-verification.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-project-verification.json) — `c749d27a8c52`
- [docs/demo/authoring/evidence/fresh-prompt-metrics.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-prompt-metrics.png) — `25db6154517c`
- [docs/demo/authoring/evidence/fresh-protected-label.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/fresh-protected-label.png) — `4cb0f2dc039b`
- [docs/demo/authoring/evidence/full-volume-container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/full-volume-container-smoke.json) — `6e4bab3fd8eb`
- [docs/demo/authoring/evidence/full-volume-inventory.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/full-volume-inventory.json) — `ef7e405b4cd0`
- [docs/demo/authoring/evidence/full-volume-prompt-metrics.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/full-volume-prompt-metrics.png) — `f407125697ae`
- [docs/demo/authoring/evidence/full-volume-spool.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/full-volume-spool.json) — `83408ab0a77f`
- [docs/demo/authoring/evidence/full-volume-verification.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/full-volume-verification.json) — `50d5e2a6c1e7`
- [docs/demo/authoring/evidence/live-companion-formatted.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/live-companion-formatted.jpg) — `ce0d2cbe887d`
- [docs/demo/authoring/evidence/live-companion-four-turns.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/live-companion-four-turns.jpg) — `c57d64946d4d`
- [docs/demo/authoring/evidence/live-model-session.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/live-model-session.json) — `781fa0417fd8`
- [docs/demo/authoring/evidence/live-pilot.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/live-pilot.json) — `9e74ab3c774c`
- [docs/demo/authoring/evidence/manifest.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/manifest.txt) — `7d5842c99f93`
- [docs/demo/authoring/evidence/native-corrected-comparison.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-corrected-comparison.png) — `e117e8d817a7`
- [docs/demo/authoring/evidence/native-experiments.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-experiments.json) — `c0df8598ebbf`
- [docs/demo/authoring/evidence/native-production-v9.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-production-v9.png) — `a4e81e42dad1`
- [docs/demo/authoring/evidence/native-prompt-metrics.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-prompt-metrics.png) — `502ebd8eeb3c`
- [docs/demo/authoring/evidence/native-protected-production.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-protected-production.png) — `e7f86c66c558`
- [docs/demo/authoring/evidence/native-session-trace.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-session-trace.png) — `b51ce004886b`
- [docs/demo/authoring/evidence/native-staging-v9.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/native-staging-v9.png) — `797ed66fe574`
- [docs/demo/authoring/evidence/operational-companion-feedback.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-companion-feedback.png) — `c5f414e268b2`
- [docs/demo/authoring/evidence/operational-container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-container-smoke.json) — `832cfcc199ae`
- [docs/demo/authoring/evidence/operational-generation-prompt.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-generation-prompt.png) — `eec596adf322`
- [docs/demo/authoring/evidence/operational-history-inventory.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-history-inventory.json) — `6f15e56b2050`
- [docs/demo/authoring/evidence/operational-history-verification.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-history-verification.json) — `12940f92371c`
- [docs/demo/authoring/evidence/operational-live-feedback.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/operational-live-feedback.json) — `001a41be57d5`
- [docs/demo/authoring/evidence/preflight-admission.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-admission.json) — `6129a30d3ede`
- [docs/demo/authoring/evidence/preflight-admission.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-admission.png) — `884ab3dd680e`
- [docs/demo/authoring/evidence/preflight-catalog.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-catalog.png) — `cf42a1266f06`
- [docs/demo/authoring/evidence/preflight-completed.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-completed.png) — `2bb4136f9917`
- [docs/demo/authoring/evidence/preflight-custom-step.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-custom-step.png) — `33bb88a8fa71`
- [docs/demo/authoring/evidence/preflight-live-probe.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-live-probe.txt) — `b3cb70e2dad0`
- [docs/demo/authoring/evidence/preflight-offline.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-offline.json) — `7665778230b9`
- [docs/demo/authoring/evidence/preflight-project.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-project.png) — `2113372287e1`
- [docs/demo/authoring/evidence/preflight-release.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-release.json) — `c54f5f7dbf13`
- [docs/demo/authoring/evidence/preflight-rollout.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preflight-rollout.json) — `23d1ef8eedbf`
- [docs/demo/authoring/evidence/preview-rehearsal.md](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/preview-rehearsal.md) — `ca43efbb71b4`
- [docs/demo/authoring/evidence/protected-label-user-verification.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/protected-label-user-verification.json) — `6810a9ffc476`
- [docs/demo/authoring/evidence/refined-companion-feedback.jpg](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/refined-companion-feedback.jpg) — `1b30f3b66837`
- [docs/demo/authoring/evidence/refined-container-smoke.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/refined-container-smoke.json) — `02f3f82197c8`
- [docs/demo/authoring/evidence/refined-live-session.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/refined-live-session.json) — `92d8c7e83f89`
- [docs/demo/authoring/evidence/release-023-admission.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-023-admission.json) — `4001a7ede71a`
- [docs/demo/authoring/evidence/release-023-admission.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-023-admission.png) — `f2926cab4fdc`
- [docs/demo/authoring/evidence/release-023-custom-step.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-023-custom-step.png) — `d2d1d87d6461`
- [docs/demo/authoring/evidence/release-023-project.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-023-project.png) — `c2d40b83ed70`
- [docs/demo/authoring/evidence/release-023-seed-start.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-023-seed-start.png) — `0893f46fac7d`
- [docs/demo/authoring/evidence/release-024-admission.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-admission.json) — `eb31c78586e5`
- [docs/demo/authoring/evidence/release-024-admission.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-admission.png) — `d9ff92d04f80`
- [docs/demo/authoring/evidence/release-024-catalog.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-catalog.png) — `6ae332518acf`
- [docs/demo/authoring/evidence/release-024-companion-response.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-companion-response.png) — `5c08266c476a`
- [docs/demo/authoring/evidence/release-024-completed-page.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-completed-page.png) — `7501dc7c1f4c`
- [docs/demo/authoring/evidence/release-024-empty-target.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-empty-target.json) — `09464db2dce1`
- [docs/demo/authoring/evidence/release-024-evaluator-progress.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-evaluator-progress.png) — `b4fb0ee6b275`
- [docs/demo/authoring/evidence/release-024-experiment-progress.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-experiment-progress.png) — `79dd03001bb2`
- [docs/demo/authoring/evidence/release-024-project.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-project.png) — `df3274839624`
- [docs/demo/authoring/evidence/release-024-release.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-release.json) — `89bd51f92417`
- [docs/demo/authoring/evidence/release-024-seed-progress.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-seed-progress.png) — `6d8541ed8033`
- [docs/demo/authoring/evidence/release-024-standard-confirmation.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-standard-confirmation.png) — `9ccdb899f4c2`
- [docs/demo/authoring/evidence/release-024-standard-gate-awaiting_confirm.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-standard-gate-awaiting_confirm.json) — `4549c4951050`
- [docs/demo/authoring/evidence/release-024-thinking.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-thinking.png) — `d8a64c51c922`
- [docs/demo/authoring/evidence/release-024-verify-progress.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-024-verify-progress.png) — `78c6dcc023e5`
- [docs/demo/authoring/evidence/release-025-depot.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-025-depot.json) — `6b81a55ffb6e`
- [docs/demo/authoring/evidence/release-025-release.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/release-025-release.json) — `0afe0cec003b`
- [docs/demo/authoring/evidence/rubric-propagation.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/rubric-propagation.json) — `38ea2e9c3ccb`
- [docs/demo/authoring/evidence/schema-check.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/schema-check.json) — `29a3c2b107a4`
- [docs/demo/authoring/evidence/seeded-blocks-live-repair.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/seeded-blocks-live-repair.json) — `44acc8c89979`
- [docs/demo/authoring/evidence/seeded-blocks-live.png](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/seeded-blocks-live.png) — `4f617a1eb962`
- [docs/demo/authoring/evidence/tests-v0.2.1.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/tests-v0.2.1.txt) — `6459cae42d15`
- [docs/demo/authoring/evidence/tests.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/tests.txt) — `e75eebae240f`
- [docs/demo/authoring/evidence/trace-shapes.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/docs/demo/authoring/evidence/trace-shapes.json) — `c895df736326`
- [pyproject.toml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/pyproject.toml) — `60ce639849ff`
- [src/synth/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/__init__.py) — `21d4cf5ad7b9`
- [src/synth/assets.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/assets.py) — `e71cb3ba3aa9`
- [src/synth/catalog.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/catalog.py) — `8057d63ee4d6`
- [src/synth/cli.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/cli.py) — `2db729601b57`
- [src/synth/companion/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/__init__.py) — `37d535e6c923`
- [src/synth/companion/app.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/app.py) — `016d47e5f70e`
- [src/synth/companion/preview.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/preview.py) — `67a282650966`
- [src/synth/companion/service.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/service.py) — `7456433fc416`
- [src/synth/companion/static/app.js](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/app.js) — `6d1a3e752639`
- [src/synth/companion/static/brand.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/brand.css) — `e392c790cb75`
- [src/synth/companion/static/fonts/GeistMono-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/GeistMono-OFL.txt) — `1781d2806a07`
- [src/synth/companion/static/fonts/Inter-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/Inter-OFL.txt) — `5b9321a4298c`
- [src/synth/companion/static/fonts/SpaceGrotesk-OFL.txt](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/SpaceGrotesk-OFL.txt) — `564ce565c371`
- [src/synth/companion/static/fonts/geist-mono.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/geist-mono.ttf) — `5c1b7b77c2d6`
- [src/synth/companion/static/fonts/inter.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/inter.ttf) — `29160a80ff49`
- [src/synth/companion/static/fonts/space-grotesk.ttf](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/fonts/space-grotesk.ttf) — `3e699ead1876`
- [src/synth/companion/static/style.css](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/static/style.css) — `c7e472a233c4`
- [src/synth/companion/templates/index.html](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/companion/templates/index.html) — `d5897ecd06c7`
- [src/synth/config.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/config.py) — `26147f00ec70`
- [src/synth/expansion.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/expansion.py) — `2e0d3039cc8f`
- [src/synth/fixtures/__init__.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/__init__.py) — `e3b0c44298fc`
- [src/synth/fixtures/conversations.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/conversations.json) — `645d3b660bc8`
- [src/synth/fixtures/dataset_extras.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/dataset_extras.json) — `45b26ac81f0f`
- [src/synth/fixtures/examples.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/examples.json) — `7ae9d676f805`
- [src/synth/fixtures/legacy_product_prompts.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/legacy_product_prompts.json) — `1932db294da9`
- [src/synth/fixtures/model_policy.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/model_policy.json) — `695ca751bf29`
- [src/synth/fixtures/portfolio.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/portfolio.json) — `4b6e61a4741c`
- [src/synth/fixtures/product.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/product.json) — `95f81e1fa906`
- [src/synth/fixtures/prompt_versions.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/prompt_versions.json) — `7d355eda9673`
- [src/synth/fixtures/score_definitions.json](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/fixtures/score_definitions.json) — `45f9514f4464`
- [src/synth/materialize.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/materialize.py) — `8d2a4b32e8d8`
- [src/synth/migration.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/migration.py) — `42335368b306`
- [src/synth/model_policy.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/model_policy.py) — `672fec0be5bb`
- [src/synth/operation_names.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/operation_names.py) — `a5f77e596a34`
- [src/synth/preflight.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/preflight.py) — `d8e60695f212`
- [src/synth/progress.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/progress.py) — `38e8f9c04317`
- [src/synth/prompt_composition.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/prompt_composition.py) — `0b3a972b0d5f`
- [src/synth/prompt_references.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/prompt_references.py) — `f8aad1de9e12`
- [src/synth/receipt.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/receipt.py) — `85398fa4a15e`
- [src/synth/reference_tools.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/reference_tools.py) — `442b7b4ad70b`
- [src/synth/scores.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/scores.py) — `f8c00006852f`
- [src/synth/seed.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/seed.py) — `e510c27309ba`
- [src/synth/state.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/state.py) — `1e59a02ec9f5`
- [src/synth/verify.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/src/synth/verify.py) — `17855b0cb177`
- [tests/golden/prompt_spool.ndjson](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/golden/prompt_spool.ndjson) — `21790c0bc26d`
- [tests/golden_seed.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/golden_seed.py) — `89ca40c5528d`
- [tests/test_assets.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_assets.py) — `0a1b3dab0d53`
- [tests/test_chat_composer.cjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_chat_composer.cjs) — `768c191e21a2`
- [tests/test_chat_pending.cjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_chat_pending.cjs) — `fd0bedc496d3`
- [tests/test_companion_runtime.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_companion_runtime.py) — `caefad24eb49`
- [tests/test_configuration_refresh.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_configuration_refresh.py) — `9cc12336c713`
- [tests/test_deployment_pipeline.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_deployment_pipeline.py) — `f90e4395227f`
- [tests/test_determinism.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_determinism.py) — `24549a562ff4`
- [tests/test_evaluator_mapping_setup.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_evaluator_mapping_setup.py) — `70324f117326`
- [tests/test_expansion.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_expansion.py) — `d9623f121cd7`
- [tests/test_experiment_mapping.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_experiment_mapping.py) — `9ccfc230970a`
- [tests/test_generation.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_generation.py) — `e34886cb9842`
- [tests/test_llm_connection_seed.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_llm_connection_seed.py) — `bbdaa6981672`
- [tests/test_migration.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_migration.py) — `2d8b58f466b9`
- [tests/test_model_policy_setup.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_model_policy_setup.py) — `530cbdee659e`
- [tests/test_operation_names.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_operation_names.py) — `9b821e80221c`
- [tests/test_preflight.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_preflight.py) — `0699ab9405bf`
- [tests/test_prompt_composition.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_prompt_composition.py) — `0d69adab4a0e`
- [tests/test_provider_binding.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_provider_binding.py) — `6cfa11de4bcc`
- [tests/test_reference_tools.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_reference_tools.py) — `64438dd18890`
- [tests/test_repeatability.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_repeatability.py) — `548fe48e355f`
- [tests/test_reply_rendering.cjs](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_reply_rendering.cjs) — `35133a3330ef`
- [tests/test_retargeting.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_retargeting.py) — `c537b647b91f`
- [tests/test_run_evidence.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_run_evidence.py) — `82c534a689ab`
- [tests/test_sdk_metadata.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_sdk_metadata.py) — `8016ae25512a`
- [tests/test_seed_progress.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_seed_progress.py) — `a39d930b2fb5`
- [tests/test_validate.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_validate.py) — `4239adddcbef`
- [tests/test_verification_progress.py](https://github.com/borismichel/langfuse-synth-prompt/blob/main/tests/test_verification_progress.py) — `c52333bd5bf7`
- [usecase.yaml](https://github.com/borismichel/langfuse-synth-prompt/blob/main/usecase.yaml) — `9e8128ce356e`

## Readiness

Authoring must report offline checks, current-run live verification, signed release,
Depot admission and delivered presenter rehearsal separately, with evidence.
Neither this status file nor an accepted document performs those checks.
