# Prompt Portfolio

A Langfuse demo kit about an established prompt portfolio: inspect its history,
try an improvement in native experiments, then promote a version and hear it in
an instrumented conversation.

The companion contains three fictional financial-services assistants. Nine managed
prompt families, eight opening versions each, four reusable text building blocks,
matching datasets and two evaluation
subjects support the story. Input signals describe what the assistant hears; reply
criteria describe what it generates. The two factual checks use **Pass**, **Fail**
and **Not applicable** across history, experiments and live chats, reported as
separate category counts. The presenter decides whether to promote,
independent of score thresholds.

Start with the [Presenter Runbook](DEMO_SCRIPT.md). The accepted
[story](docs/demo/story/STORY_BRIEF.md) and [prototype](docs/demo/prototype/BRIEF.md)
remain the specification. The [workspace dossier](docs/demo/DOSSIER.md) tracks stage
handoffs. Authoring evidence distinguishes offline checks from live readiness.

## Local development

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/synth preview --port 8765
```

The preview uses the delivered app with an explicit fixture adapter. It strips
credentials and blocks outgoing connections. It supports the displayed authored
questions, does not run models or evaluations, and never claims live readiness.
Native prompt, experiment and session screens are available only on a connected
Langfuse project; the accepted visual prototype remains in `design/prototype`.

```sh
.venv/bin/synth-authoring validate usecase.yaml
.venv/bin/synth-authoring conformance .
.venv/bin/python -m pytest -q
```

The pinned core release is v4.2.0; the Langfuse Python SDK is 4.17.0. CI runs the
same tests and conformance checks. The golden spool covers 24 history traces plus
18 authored experiment examples. Process-repeatability checks vary Python hash
seeds with egress blocked. No model generates seed content.

## Deployment

Use a dedicated, fresh demo project and the supported Depot secret workflow.
`.env.example` names the required environment variables; neither the CLI nor the
repository silently loads secret files. A model connection inside Langfuse powers
native experiments and managed evaluators; the companion separately receives its
Anthropic provider key. The default Langfuse connection name is `anthropic`; set
`LANGFUSE_EVAL_PROVIDER` if the existing Anthropic connection has a different name.
Native experiments and evaluators use `claude-sonnet-5-5`. Companion product
explanations use `claude-sonnet-5-5`; fee explanations and application guidance use
`claude-opus-5-5`. The companion's per-role policy takes precedence over the legacy
global `LLM_MODEL` setting. Depot advertises Anthropic as the supported provider.

All recorded model names are the original provider IDs. Synthetic history uses
the shared role policy, including `claude-fable-5-1` for the two complex history
roles. Its explicit cost details are multiplied by three; model registry prices,
real companion calls and native experiments retain base prices. No suffixed model
aliases are created.

`generation.target_traces` is the only volume control. It scales production
history while keeping **nine agent prompts, eight initial versions per agent, four
text building blocks, nine datasets and eighteen authored experiment traces** fixed. There is no prompt-count
or prompt-scale option. Promoting a presenter-created version is a separate action.

The `building-blocks` folder contains reusable text prompts for reference context,
factual boundaries, voice and structured output. Agent prompts use native Langfuse
references; their resolved opening instructions retain the accepted story. The
presenter can append the shared `playful` voice reference to a staging candidate.

Depot runs **probe → plan → evaluator setup → history seed → experiment mapping setup → verification**.
Probe uses the shared core's demo-project guard, writes two throwaway observations,
and verifies that their backdated timestamp survives through the v4 observations API.
It does not change the historical seed spool or receipt. A failed probe stops the pipeline.
Plan runs offline, requires no credentials, and leaves existing spool, import markers
and state untouched. It reports exact observations and scores for the selected history
volume plus the fixed experiment cohort. Root observations count once; derived traces
are shown separately. The two probe observations are additional to the seed estimate.
The manifest exposes versioned `PLAN_COUNTS` for Depot's exact volume display and retains
the raw trace-count field for older Depot versions, whose generic ratio remains approximate.

Historical seed model cost is **USD 0** with **zero provider calls**. The synthetic
model costs displayed in Langfuse are authored demo accounting and are not incurred spend.
Langfuse ingestion is reported in billable units; no dollar price is invented for the
account's plan. Evaluator model validation, later live chats and real experiments are
outside this model-free seed estimate and may incur actual provider costs.

Only the explicitly declared evaluator-setup step receives the selected provider key;
probe, seed and verify receive only Langfuse credentials; plan uses none.
Setup creates a missing compatible Langfuse model connection when a provider key is
available, or reuses the existing connection without changing its key. Evaluator
setup is a separate model-using operation because Langfuse may validate the selected
model on save. The historical seed remains model-free.
Read [native asset setup](docs/demo/authoring/ASSETS.md),
[companion integration](docs/demo/authoring/COMPANION.md), and
[generation semantics](docs/demo/authoring/GENERATION.md). The
[preflight contract](docs/demo/authoring/PREFLIGHT.md) records counts and verification scope.

For a local offline estimate, use:

```sh
.venv/bin/synth plan --config config/demo.yaml --set generation.target_traces=1620
```

The separate developer command `synth probe --config config/demo.yaml` writes its
two-observation check to the authorised target; planning alone makes no network calls.

`usecase.yaml` is the Depot integration contract. `Dockerfile` runs as a non-root
user. The signed image workflow is pinned to the same core release and triggers
only on a matching immutable version tag. Nothing is published by local tests.
Release v0.2.1 passed all six admission checks and the delivered rehearsal, and is
published in Depot. The final source/image and rollout receipts are recorded in
[Depot onboarding](docs/demo/authoring/DEPOT_ONBOARDING.md).

Ingestion appends. The kit refuses a repeated live seed in the same state
directory after provisioning/import begins. A partial failure requires a fresh
approved target or a separately authorised reset; it must never be blindly retried.

## Readiness

On 2026-10-09, the exact signed v0.2.1 image completed automatic setup, full seed,
verification and companion smoke in `prompt-components-demo` within Boris Demo
Enterprise. The final [delivered rehearsal](docs/demo/authoring/COMPONENTS_REHEARSAL.md)
then exercised native text components, prompt metrics, two real eight-case Sonnet
5.5 experiments, owner promotion, four live turns and explicit feedback.

The comparison produced 16 outputs and 128 actual EVAL results. Style averaged
0 for v7 and 0.3375 for composed v9; both factual criteria passed all eight cases,
with respectful tone 1. The promoted live conversation used v9 on every turn,
scored 0.5 for style, and produced 32 input/reply evaluations plus a thumbs-down
score on the intended third reply. No score gate or quality-driven retry ran.
Online observation mappings and experiment item overrides were verified separately.

The user independently verified protected-label enforcement. The final rehearsal
used an owner account and does not claim a fresh member-denial test. The admission
carrier's project shortcut remains host-only; use the exact project or companion
session links documented in the rehearsal. Earlier projects, experiments and
calibration failures are preserved in [authoring review](docs/demo/authoring/REVIEW.md).

The full population specification is 1,620 production-history traces, 2,100
generations and 9,320 eligible outcomes over 28 complete days, plus eighteen small
historical experiment traces. E-02/E-03 include explicit Not applicable categories;
missing, pending and failed executions remain distinct.
History, products, accounting prices, user identities and replies are synthetic.

Original Claude model IDs, shared historical/live operation names, generation-native
prompt links and BOOLEAN thumbs/comments remain part of the delivered contract.
The [operational revision](docs/demo/authoring/OPERATIONAL_REVISION.md) preserves
the earlier migration evidence; the final fresh-target evidence is linked above.
