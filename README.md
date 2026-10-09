# Prompt Portfolio

A Langfuse demo kit about an established prompt portfolio: inspect its history,
try an improvement in native experiments, then promote a version and hear it in
an instrumented conversation.

The companion contains three fictional financial-services assistants. Nine managed
prompt families, eight opening versions each, matching datasets and two evaluation
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

The pinned core release is v4.1.1; the Langfuse Python SDK is 4.17.0. CI runs the
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
history while keeping **nine prompts, eight initial versions per prompt, nine
datasets and eighteen authored experiment traces** fixed. There is no prompt-count
or prompt-scale option. Promoting a presenter-created version is a separate action.

Managed evaluator setup is a separate model-using operation because Langfuse may
validate the selected model on save. The historical seed remains model-free.
Read [native asset setup](docs/demo/authoring/ASSETS.md),
[companion integration](docs/demo/authoring/COMPANION.md), and
[generation semantics](docs/demo/authoring/GENERATION.md).

`usecase.yaml` is the Depot integration contract. `Dockerfile` runs as a non-root
user. The signed image workflow is pinned to the same core release and triggers
only on a matching immutable version tag. Nothing is published by local tests.
The updated Depot manifest and local checks do not establish deployment; signed
release, Depot admission and delivery of this revision remain pending.

Ingestion appends. The kit refuses a repeated live seed in the same state
directory after provisioning/import begins. A partial failure requires a fresh
approved target or a separately authorised reset; it must never be blindly retried.

## Readiness

Authoring checks verify the native prompt/metrics flow, protected-label owner
promotion and a four-turn live session with 32 input/reply EVAL scores. The corrected
native v7/v9 experiment pair produced 16 outputs and 64 scores: style 0.00 → 0.75,
both factual criteria eight Passes per version, tone 1.00. The promoted live run
resolved v9 correctly but retained ordinary prose on all four turns. Results and
input-judge calibration failures are preserved; no score gate or quality retry ran.
The initial invalid-context experiment is retained separately.
See [native rehearsal](docs/demo/authoring/NATIVE_REHEARSAL.md) and
[authoring review](docs/demo/authoring/REVIEW.md) for evidence and remaining gates.

Live evaluator calibration, signed release and Depot admission remain pending.
Full-scale categorical history is verified in the user-selected project. Earlier numeric pilot history
is preserved and does not establish the new categorical contract.

On 2026-10-09 the fresh `prompt-portfolio-demo` project passed all 244 checks
after one corrected small import: 48 history traces plus 18 authored experiments.
One actual companion turn also produced eight correctly targeted evaluator results.
See the [fresh project evidence](docs/demo/authoring/FRESH_PROJECT.md).
The user independently verified protected-label enforcement on the same date,
closing the small walkthrough's remaining permission check.

The same project now contains 1,620 history traces plus 18 authored experiment
traces, 2,118 generations, 74 calculator tool observations and 9,356 authored
scores. A guarded expansion added 1,572 traces without replacing the sample,
assets or live chats. Exhaustive readback found no missing or duplicate records.
See [full-volume evidence](docs/demo/authoring/FULL_VOLUME.md).

The full population specification is 1,620 production-history traces, 2,100
generations and 9,320 eligible outcomes over 28 complete days, plus eighteen small
historical experiment traces. E-02/E-03 include explicit Not applicable categories;
missing, pending and failed executions remain distinct.
History, products, accounting prices, user identities and replies are synthetic.

The current [operational revision](docs/demo/authoring/OPERATIONAL_REVISION.md)
replaced that earlier spool in the same project with original Claude model IDs,
shared application trace names, generation-native prompt links and cleaned
presentation labels. Explicit thumbs/comments now persist as BOOLEAN scores.
All 248 live checks and the full inventory audit passed; existing non-seed records
were preserved. Depot admission and delivered staging rehearsal remain pending.
