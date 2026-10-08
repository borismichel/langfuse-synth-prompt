# Prototype handoff

Status: **prepared for story review; execution waits for story acceptance and a
prototype request**. Read STORY_BRIEF.md, story-contract.yaml, PORTFOLIO.json,
EVALUATION_PLAN.md, POPULATION.md, both case files and PRODUCT_RESEARCH.md.
Preserve accepted D-01–D-31 and stable IDs; list proposed changes for review.

## Question to answer

Can a presenter move convincingly from an established prompt portfolio through
an experiment and admin promotion to a chatbot session whose behaviour, input
signals, output quality and exact prompt-version provenance are inspectable?

The three-stage shape and presenter discretion are settled. The receiving agent
must not invent an opening incident, require a better score, add a retry loop,
replace input evaluators with reply evaluators, or change the primary companion
link from session to trace.

## Scope and surface responsibilities

- Preserve a **prompt-first presenter entry**, overriding the prototype skill's
  generic companion-first presentation default. Provide a separate direct
  companion entry for a person simply using a chatbot.
- Create a small connected local prototype. Use Langfuse's own components at a
  recorded revision for golden trace/session inspection where the skill requires;
  distinguish actual reused components from simulated product interactions.
- Companion: three selectable chatbots in one shell is a proposed reversible
  layout. Open a chatbot directly on its conversation. No dedicated live user-
  sentiment dashboard or presenter documentation embedded in the customer flow.
- Story/coverage: show the three beats, exact linked evidence, population preview
  and uncovered requirements. This may share one supporting surface.
- Native product work belongs in Langfuse in the eventual demo. A local portfolio,
  experiment or promotion simulation must be visibly identified as simulation,
  not advertised as an existing native page or a production integration.

Use in-memory state and deterministic fixtures. Do not execute models, seed a live
project, create paid evaluators, scaffold runtime, release or deploy at this stage.
The eventual live requirements remain mandatory authoring evidence.

## Required representative evidence

1. All nine prompt families are inspectable with a sensible purpose and version
   history; PR-01's complete comparison is the primary example. Keep other families
   lighter while preserving their source/expected-output/control relationships.
2. PR-01 v7 → staging v9, protected production initially v7; a member cannot perform
   the simulated admin-only promotion. Show actual available permissions later;
   a fixture permission state is not a live security test.
3. Experiment baseline/candidate/control view uses C-01–C-08 and CTRL-01–CTRL-03.
   Same dataset/model/context, real score meanings, explicit authored provenance.
   Permit good, mixed and non-improving outcomes without forcing reruns.
4. SESSION-01 displays four exchanges with coherent prior context. Root input
   scores and generation reply scores remain distinct. Include a golden inspected
   trace for one turn and FLOW-01 for the multi-prompt historical shape.
5. Promotion changes the system-prompt version for a fresh conversation. Preserve
   before/after histories; don't retroactively relabel old calls. Simulate pending
   fetch/ingestion/evaluation states honestly and define the delivery test.
6. Population preview shows day/hour shape, session lengths, version usage,
   cost/latency, output scores and user-input trend coverage. Aggregate previews
   are labelled separately from values computed from representative fixtures.

## Prototype questions and review criteria

| ID | Question | Reviewable result |
| --- | --- | --- |
| Q-01 | Which native prompt metrics can display the chosen generation scores? | Record tested component/server revision and supported score aggregation. Preserve N/coverage. Route unsupported input metrics to a real native score/observation surface rather than a fabricated prompt tab. |
| Q-02 | Can the session chat view expose the necessary evaluation detail directly? | A clickable session → observation route retaining chat context, with score reasoning and exact prompt version. Do not promise every score appears beside every bubble. |
| Q-03 | Do UI experiment and live rules accept equivalent evaluator inputs? | Explicit mapping of message, history, record and response for each criterion; no dependence on unavailable offline truth. Record any required integration. |
| Q-04 | How are prompts refreshed after promotion? | Demonstrate a defined fresh-request/new-conversation boundary, resolved version, loading state and cache-policy explanation. |
| Q-05 | Does native protected-label behaviour match the proposed roles? | Distinguish verified product docs, simulated prototype roles and later live UI/API enforcement. Do not imply four-eyes approval. |
| Q-06 | Is the portfolio and three-chatbot layout understandable? | User can find a prompt, understand its application and navigate a coherent example without all nine apps needing a live runtime. |
| Q-07 | Are input signals distinct and useful? | Correction, disagreement, contradiction, direct/quoted profanity and frustration examples yield distinguishable evidence; a trend can lead back to relevant conversations. |
| Q-08 | Does every claimed operation have its required evidence? | Coverage map joins discovery IDs to source, case, operation, prompt version, score subject and surface. List unsupported or untested claims explicitly. |

## Later live verification, not prototype acceptance

Authoring must prove actual protected-label behaviour, API prompt fetch and cache
behaviour, real model replies, persisted prompt/generation links, multi-turn
session ingestion, both evaluator tracks and evaluator readback. It must retain
actual scores even if they disappoint. A working local simulation or accepted
story proves none of these.

No fixed real model/API credentials are required for this story/prototype packet.
Choose and record an available model and compatible model settings before live
execution. Baseline and candidate keep that choice fixed. Validate exact current
API/SDK/server versions then, preserving the kit's separately pinned core release.
