# Prompt portfolio: inspect, experiment, promote

Status: **accepted for prototyping**. Prepared 2026-10-08.
The user's agreed decisions are preserved as D-01–D-31 in
[the story contract](story-contract.yaml). Concrete records, counts and rubrics in
this packet are agent-authored proposals implementing those decisions.

## The story

A fictional financial-services team manages a portfolio of prompts used by
several agents and applications. They need to find prompts, understand which
versions have been used, compare cost and quality, and control who changes
production. Ongoing iteration is normal; no opening incident is required.

The presenter starts with established prompt history, tries a new version in an
experiment using existing evaluators, decides how to respond to the actual
results, then demonstrates a production-label change in a working chatbot. A
multi-turn conversation leads directly into Langfuse's session view, with live
input/output evaluations and underlying prompt-version provenance.

The audience takeaway is **visibility, control and continuity across the prompt
lifecycle**. Scores inform the presenter; they do not impose a release gate,
mandatory revision or repeat-until-pass loop. An unexpected score is information
to inspect, not a failed demonstration or a test of the presenter's writing skill.

## Audience and responsibilities

Proposed audience: prompt/content owners and AI application/platform engineers.
The presenter acts as a prompt editor, then an authorised admin for protected
production promotion. The fictional end user asks about product terms. Protected
labels demonstrate permission boundaries; they do not establish two-person
approval. Actual target-plan and API enforcement need verification.

All records, people and interactions are fictional. No real customer identities,
private source links or procurement documents belong in this public packet,
prototype or delivered demo. Public capability sources are recorded separately
in [product research](PRODUCT_RESEARCH.md).

## Scope proposed from the agreed ranges

- **Nine prompt families**, each with **eight stored versions**: three live
  chatbots and six historical-only prompt families.
- Main chatbot: **product explainer**. Additional live chatbots: **fee explainer**
  and **application guide**. The other families support classification, query
  rewriting, summarisation, extraction, drafting and handoff examples.
- A matching dataset for every prompt. PR-01's complete eight-item dataset is
  supplied; each other family has a representative case and adjacent control.
- PR-01 v7 is production on entry, v8 is an unused draft, and v9 is created during
  the demonstration by adding a speaking-style instruction.
- Historical prompts have meaningful version changes, uneven usage, costs and
  scores. Historical-only applications need no companion UI, but remain coherent
  when inspected. FLOW-01 shows several differently linked prompts in one trace.

[PORTFOLIO.json](PORTFOLIO.json) owns the application → operation → prompt → version
and dataset relationships. [POPULATION.md](POPULATION.md) owns history, cohorts,
metric denominators, coverage and synthetic accounting assumptions.

## Three presenter discoveries

### P-01 — We can understand the portfolio we already have

Start in the Langfuse prompt surface. Find `products/explainer`, inspect its version
history, protected production label and native metrics. Compare historical cost,
latency and applicable response scores. Show that user-message evaluations also
surface disagreement and frustration over time, giving the team reasons to revisit
an agent or prompt. Those input signals coexist with reply-quality evaluations.

Evidence: the nine-family portfolio, version periods, population preview and
criterion definitions. Trace drill-down P-03 explains exact generation/version
links, including FLOW-01. Native prompt metrics documents numeric median score values; E-02/E-03 use
Pass/Fail/Not applicable counts under approved D-32;
use the appropriate native score/observation surface when an input metric cannot
be rolled up on that page. Do not fabricate native UI capabilities.

Next question: what happens when we try a new prompt version?

### P-02 — We can inspect what a proposed change actually does

Open PR-01's current version, add the agreed theatrical space-villain instruction,
save v9 under `staging`, and create an experiment on DS-01/r1 with the existing
model and evaluator definitions. Compare it with v7 on identical inputs, source
records and conversation context. The precise candidate text, full outputs and
controls are in [the main case file](cases/product-explainer.json).

The playful **The Dark Side of Customer Service** score should recognise the new
style in authored examples. Serious checks still inspect record fidelity, claim
support and respectful tone. CTRL-01 deliberately sounds theatrical while getting
the fee rule wrong: it proves style and correctness are different dimensions.
Actual live scores may improve, worsen or stay flat. Explain what happened and
leave the next action to the presenter.

Next question: what does choosing a production version change for the application?

### P-04 — We can see the selected prompt operating in a real conversation

An authorised admin may promote v9 to the protected production label. The
companion retrieves that label as its system prompt. Use a fresh conversation
and a verified refresh/cache policy; no application deployment or hidden local
behaviour toggle supplies the effect.

The authored four-turn SESSION-01 starts with a product-fee question, adds a
user correction, then disagreement/frustration/profanity, and ends with a document
question. Both input and reply evaluators run. The companion's primary link opens
the **session chat view**, not a single trace. Use underlying observations to
inspect detailed score reasoning and exact prompt versions where needed.

This is the delivered demo's required live payoff. Prototype evidence is local
simulation; actual model execution, ingestion, evaluations and readback are
verified only during authoring. New live records must remain distinguishable from
historical fixtures. Show pending results or ingestion delay honestly.

### P-03 — Supporting provenance, available throughout

Every prompt-using generation names its actual prompt and version. A shared trace
can contain several differently linked generations; tools do not receive invented
prompt assignments. Old records retain resolved versions after production labels
move. Session navigation preserves per-turn request boundaries and role-bearing
messages without repeating all prior turns in the visible chat.

## Concrete business truth and comparison

SRC-01 is the fictional Everyday Account record. Its EUR 4 monthly fee is waived
only when at least EUR 1200 in qualifying salary deposits arrives that calendar
month; transfers from the person's own accounts are excluded. The same record
contains other fees, eligibility and document requirements, and explicitly leaves
some terms unknown. It is authored truth, not financial advice or a real product.

C-01 compares accurate plain and theatrical answers to the same fee question.
C-02 tests the own-account exclusion; C-03 tests absent information; C-04 tests a
legitimate user correction; C-05 disagreement and frustration; C-06 an unacknowledged
contradiction; C-07 quoted profanity; C-08 the boundary between explanation and
account action. Negative controls isolate false facts and disrespectful tone.
All exact records and outputs live in the case file, not duplicated here.

## Two evaluation tracks

[The evaluation plan](EVALUATION_PLAN.md) defines twelve criteria, including eight
for the main chatbot. Output scores describe the answer generation. Input scores
describe the current user message with the context needed to interpret it. Rising
input-signal rates may suggest investigation; they do not prove a prompt caused
user frustration. Identical experiment input should not appear improved merely
because the answer prompt changed.

The same rubric and necessary evidence carry from historical examples into
experiments and live observations. Live judges cannot depend on offline expected
answers. Authored expected scores are clearly separate from executed judge
results. Score definitions, score records, applicability and completion are
separate concepts; there is no universal quality average.

## Review and next stage

See [REVIEW.md](REVIEW.md) for the complete proposal recap and readiness checks.
The user accepted this packet for prototyping with “Run proto on the packet”.
[PROTOTYPE_HANDOFF.md](PROTOTYPE_HANDOFF.md) specifies the next stage's questions,
inspectable evidence and verification limits. It preserves the prompt-first
presenter journey and direct companion entry for chatbot users.
