# Story packet review

Prepared 2026-10-08. **Accepted for prototyping on 2026-10-08.**
The user subsequently instructed: “Run proto on the packet”. This accepts the
completed packet as the input to this prototype. It does not accept the future
prototype or authorise a production build.

## Agreed story

1. **Understand the portfolio:** enter through prompts, inspect versions,
   protected labels, cost/latency and applicable output metrics; also inspect
   user-message signals and trends. Traces explain prompt/version provenance.
2. **Try a change:** edit a prompt, save a staging version and run an experiment
   using its existing dataset, model and applicable evaluators. Inspect actual
   results. The presenter decides what to do; no automatic score gate or retry loop.
3. **Show the effect:** an authorised admin can promote the version; a companion
   chatbot retrieves it as its system prompt. Have a short multi-turn conversation,
   then open its Langfuse session. Both user-message and reply evaluations run;
   underlying observations expose details and exact prompt versions.

The main chatbot explains fictional financial-services product information.
**The Dark Side of Customer Service** demonstrates a measurable playful speaking
style alongside serious factuality, grounding and respectful-tone criteria.
User disagreement, contradiction, frustration and profanity are a separate,
required evaluation track, with no additional companion dashboard.

Customer identity stays out of all demo materials. The story demonstrates what
the tool reveals and how the workflow connects, not a guaranteed quality win or
the presenter's ability to make every judge happy. Accepted decisions are D-01–D-31
in [story-contract.yaml](story-contract.yaml).

## Concrete proposals prepared for this review

| Proposal | Chosen detail | Authoritative file |
| --- | --- | --- |
| Portfolio size | Nine families, eight stored versions each; main v9 created during the walkthrough | [Portfolio](PORTFOLIO.json) |
| Live companion | Three bots: product explainer, fee explainer, application guide | [Portfolio](PORTFOLIO.json) |
| Main case | Fictional account terms; salary versus own-account transfer makes an inspectable condition | [Main cases](cases/product-explainer.json) |
| Comparison | Plain v7 versus style-modified v9; eight cases, fixed dataset/model/context | [Main cases](cases/product-explainer.json) |
| Controls | Exclusion, absent terms, correction, contradiction, quoted profanity, action boundary, wrong facts and disrespect | [Main cases](cases/product-explainer.json) |
| Live session | Four exchanges: question, correction, disagreement/frustration, next-step question | [Main cases](cases/product-explainer.json) |
| Remaining prompts | One concrete source/example/control per family; historical multi-prompt flow | [Other cases](cases/portfolio-examples.json) |
| Evaluation detail | Eight main criteria; four historical-task criteria; explicit subjects, ranges, context and expected outcomes | [Evaluation plan](EVALUATION_PLAN.md) |
| History | 28 complete days, 360 conversations/1,080 chat turns plus historical-only workflows; declared denominators and coverage | [Population](POPULATION.md) |
| Prototype scope | Connected local fixtures, golden session/trace inspection, companion and coverage preview; native UI/API questions explicit | [Prototype handoff](PROTOTYPE_HANDOFF.md) |

These concrete details are now accepted as the prototype input. The
fictional examples and synthetic accounting rates are original demo assumptions.
No model, judge or live Langfuse mutation was executed to produce them.

## Readiness assessment

- A receiving agent can explain the actor, business problem, intervention,
  three-stage presenter path and companion payoff from STORY_BRIEF.md.
- Full source truth, inputs, outputs, baseline/candidate comparison and controls
  exist. Their provenance is explicit; source facts are independent of bad output.
- Operation, prompt, dataset, version and application relationships have stable IDs.
- Input and output score subjects, required context, ranges, expected values,
  counts, sampling/coverage and availability are specified at story level.
- Population totals, metric denominators, pricing assumptions, usage periods and
  historical/experiment/live distinctions are coherent and reviewable.
- Native product claims are linked to official sources. Unsupported score rollups,
  session score layout, runtime mappings, permissions and cache behaviour are
  receiving-stage checks, not asserted successes.
- The full packet has been checked for broken local links, invalid JSON, duplicate
  IDs, orphaned references, inconsistent planned totals and customer identifiers.
- Checks establish packet consistency only; acceptance is the user decision below.

## Decision to record

On 2026-10-08 the user requested “Run proto on the packet”. Proceed with the
accepted packet and a local fixture prototype. No change to D-01–D-31.
Prototype acceptance and any production implementation remain separate decisions.
