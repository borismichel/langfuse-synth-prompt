# Prompt Portfolio

A Langfuse demo kit about an established prompt portfolio: inspect its history,
try an improvement in native experiments, then promote a version and hear it in
an instrumented conversation.

The companion contains three fictional financial-services assistants. Nine managed
prompt families, eight opening versions each, matching datasets and two evaluation
subjects support the story. Input signals describe what the assistant hears; reply
criteria describe what it generates. The presenter decides whether to promote,
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

The pinned core release is v4.1.1; the Langfuse Python SDK is 4.17.0. CI runs the
same tests and conformance checks. The golden spool covers 24 history traces plus
18 authored experiment examples. Process-repeatability checks vary Python hash
seeds with egress blocked. No model generates seed content.

## Deployment

Use a dedicated, fresh demo project and the supported Depot secret workflow.
`.env.example` names the required environment variables; neither the CLI nor the
repository silently loads secret files. A model connection inside Langfuse powers
native experiments and managed evaluators; the companion separately receives its
selected provider key.

Managed evaluator setup is a separate model-using operation because Langfuse may
validate the selected model on save. The historical seed remains model-free.
Read [native asset setup](docs/demo/authoring/ASSETS.md),
[companion integration](docs/demo/authoring/COMPANION.md), and
[generation semantics](docs/demo/authoring/GENERATION.md).

`usecase.yaml` is the Depot integration contract. `Dockerfile` runs as a non-root
user. The signed image workflow is pinned to the same core release and triggers
only on a matching immutable version tag. Nothing is published by local tests.

Ingestion appends. The kit refuses a repeated live seed in the same state
directory after provisioning/import begins. A partial failure requires a fresh
approved target or a separately authorised reset; it must never be blindly retried.

## Readiness

This implementation is undergoing authoring checks. Live project verification,
managed evaluator calibration, protected-label role checks, signed release,
admission and staging rehearsal require separate evidence. Consult
[authoring review](docs/demo/authoring/REVIEW.md) for the current recorded status.

The full population specification is 1,620 production-history traces, 2,100
generations and 9,320 eligible outcomes over 28 complete days, plus eighteen small
historical experiment traces. Numeric scores omit genuinely inapplicable outcomes.
History, products, accounting prices, user identities and replies are synthetic.
