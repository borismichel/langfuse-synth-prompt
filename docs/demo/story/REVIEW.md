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
the presenter's ability to make every judge happy. The original accepted decisions are D-01–D-31
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

## Subsequent authoring instruction: trace detail

On 2026-10-08 the user explicitly requested proper live/history trace shapes with
tool calls. [TRACE_SHAPES.md](TRACE_SHAPES.md) records this additive instruction.
It leaves the accepted three-beat journey and business/evaluation truth intact.


The subsequent trace-design refinement applies the user's instruction to use the
Langfuse skill: a single retrieval and optional real fee calculation replace the
redundant wrapper. Prompt-first flow, source facts, rubrics, examples and presenter
discretion are unchanged. This is implementation compatibility under the existing
request; it does not record a new user review of the runtime or live evidence.

## Approved factual-check representation amendment

On 2026-10-08 the user answered **“Sure”** to the proposal to use
**Pass / Fail / Not applicable** for the two factual checks consistently across
history, experiments and live chats, with category counts instead of numeric
averages because native numeric evaluators cannot return not applicable.
This is acceptance of that representation amendment (D-32), not a new acceptance
of implementation, deployment or live evidence. E-02 `record_fidelity` and E-03
`claim_support` retain their distinct semantic rules, IDs, subjects and cases.
Authored `1` / `0` / `null` values remain calibration inputs and map explicitly
to `Pass` / `Fail` / `Not applicable`; absent or failed results do not map to N/A.
The earlier screenshots and native numeric readbacks do not verify the amended
categorical implementation. Fresh implementation checks/readback remain required.


## User-directed model, provenance, feedback and scale amendment

On 2026-10-09 the user instructed:

> Please keep the model names original. I don't want any fake models in there, so people can relate to the data they see by seeing the model names they are used to seeing every day.

> Make sure this is anchored in the demo kit.

The role direction was higher-risk/higher-fidelity agents on Opus, simple
retrieval chats on Sonnet-55 and selected higher-impact work on Fable-51, with:

> Keep any experiment runs and LLM connections for evaluators on Sonnet-55, though.

[MODEL_POLICY.md](MODEL_POLICY.md) records the exact Anthropic IDs and the concrete
per-role assignments in the canonical executable policy. Authored historical
cost details use an explicit 3× multiplier; normal model registry prices and
actual live usage remain the basis for live accounting.

For prompt/version provenance the user specified **“not just tags.”** They then
clarified: **“Prompt references should stay on generation. Sorry for that. If
there was a misunderstanding they don't need to be on the root trace.”** This
supersedes the proposed root-level reference inventory: retain each generation's
native managed-prompt association and remove redundant root prompt references.

For direct user feedback the user instructed:

> We should also add thumbs up, thumbs down, and feedback to the chats as a way for users to provide feedback on disagreement, in addition to having it run on the evaluators and create a score associated with that. Check the Langfuse score for a good implementation here.

The implementation contract is explicit BOOLEAN `user-thumbs` (1/0) with an
optional comment on the saved reply's actual request root, separate from E-08
`user_disagreement`. One final submission is allowed per reply and identical
retries do not create another score. This records the agreed implementation
semantics, not a claim that a thumb proves factual error.

On scale the user clarified:

> For Trace scaling, etc., I think we don't need any other prompt scale or something.

Only `generation.target_traces` scales. The nine prompt families, eight opening
versions each, nine datasets and eighteen historical experiment examples remain
fixed. These directives amend model identity, accounting, provenance, feedback
and volume controls; they do not redesign the accepted presenter journey, cases,
rubrics or promotion decision, and do not invent acceptance of new live evidence,
deployment or release.


## User-directed operational naming amendment

The user then called out authored-history/synthetic wording on product surfaces,
asked for the application to look like a real running application, and required
companion trace names to match historical trace names. They explicitly included
the spool and generation scripts in the requested fix, with a last-month history
experience. This is a naming and presentation amendment, not permission to claim
that authored records are real customer traffic.

Use consistent application operation names across generated history and companion
requests, ordinary production/experiment environment labels, and meaningful
experiment names. Keep synthetic provenance, cost multipliers and origin in
structured metadata and these documents. The accepted 28 complete days remain
the last-month history window; no source facts, counts or scale axes change.
