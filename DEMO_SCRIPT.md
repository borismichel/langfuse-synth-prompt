# Prompt Portfolio — inspect, experiment, promote

A team already operates several assistants. The work today is ordinary improvement:
find their managed instructions, compare a proposed change, and decide whether to
release it. There is no opening incident and no automatic score gate.

| Beat | Delivered screen | Presenter action | Expected result | Evidence |
| --- | --- | --- | --- | --- |
| Understand the portfolio | Langfuse Prompts → versions and Metrics → linked observations | Browse nine prompt families. Open `products/explainer`, compare its production v7 with older versions, then inspect a linked request and reply. | Versions, usage, cost, latency and available score breakdowns explain what each application is doing. Input signals show what it hears. | Eight opening versions per prompt, nine datasets, historical prompt links, root and generation scores. |
| Try a change | Langfuse prompt editor → native Experiments | Create v9 from v7, add the theatrical style, label it `staging`, and compare against v7 on the same eight cases and real model. | Actual results show changes in delivery alongside factual fidelity, supported claims and respectful tone. | Same dataset snapshot and E-01–E-04 evaluator definitions. Inspect individual examples as well as aggregates. |
| Show the effect | Protected `production` label → companion → Langfuse Session | An authorised administrator decides whether to promote. Complete four exchanges in a fresh product chat and choose **Open session**. | A real conversation uses the newly resolved prompt. Its session exposes the exchanges, exact prompt versions and both evaluation subjects. | Four root/generation pairs; up to 16 input and 16 reply outcomes once judges finish. |

## Before the audience arrives

Use the dedicated demo project produced by the seed run. Confirm the current seed
receipt passed verification; offline preview fixtures are not live evidence. The
intended full portfolio has 1,620 history traces, 2,100 generations and 9,320 eligible
synthetic outcomes across 28 complete days, plus a separate small historical
experiment cohort. Seeded scores are authored examples, not historical model-judge
runs. These are fictional products, users, conversations and accounting prices.

Confirm that the project has a usable model connection, active managed evaluators,
and protected-label support. Protect `production` in native project settings; rehearse
with a member account and an administrator/owner. An API key does not demonstrate
member permissions. Public API provisioning cannot configure this protection.

Open the native prompt portfolio and the companion in separate tabs. Use a readable
browser scale. The companion has three bots; keep the product explainer selected.
Its muted **Presenter tools** disclosure contains supporting links and evidence.
Native experiment and role-control navigation must be rehearsed on the actual target;
local preview does not establish native behaviour.

## Beat 1 — a portfolio with history

Start with the nine prompt families. Three power the live chatbots; the other six
have meaningful history, cases and versions but no companion screen. Open
`products/explainer`: v7 has `production`, v8 is an unused draft. Versions 2 and 4
belong to small authored historical experiments; the other released versions have
unequal traffic periods. Do not imply equal sample sizes.

Use the prompt's Metrics view for cost, latency and usage. Synthetic model prices
make historical accounting explicit. Inspect the available per-version quality
scores and sample counts; use native observation/score views for user-message
signals if the prompt view does not aggregate scores from request roots. Do not
promise that root scores appear in a generation-level chart.

Show one request root and its answer generation. The generation names its exact
prompt and version. Answer criteria attach there. The request root has the separate
input criteria: contradiction, expressed frustration, profanity and disagreement.
These describe what the assistant hears; they are not defects in every reply.
For example, an explicit self-correction is not an unresolved contradiction and
quoted profanity is not automatically user frustration. The fee assistant also
has a worsening disagreement cohort, giving the team a reason for future work.

For optional tool detail, open the fee explainer and ask: “I made three cash
withdrawals this calendar month. What withdrawal fee applies?” The trace shows
source retrieval, a real calculation of one chargeable withdrawal at EUR 1.50,
and the linked answer generation. An explicit two-withdrawal version of the same
question calculates EUR 0.00. The calculator supports this precise statement form;
it does not infer ambiguous counts or periods from free text. Explain that these
are application-invoked operations, not model-selected tools. Return to the
product prompt for the main experiment story.

## Beat 2 — compare a proposed improvement

From product explainer v7, save a new version with this addition to its **first
system message**, retaining all fact and task instructions and the variable messages:

> Deliver the same accurate answer in a restrained theatrical space-villain voice:
> short, commanding sentences, occasional cosmic imagery, and unmistakable dramatic
> presence. Remain respectful. Never threaten, belittle, invent product facts, or
> obscure fees, exceptions, eligibility or required actions.

This becomes v9 when the opening project is untouched. Label it `staging`. The
presenter may write their own equivalent instruction. Version numbers are resolved
from the native editor, never assumed after previous rehearsals.

Open the matching product-explainer dataset and run a native prompt experiment with
v7, then v9. Select the same actual provider/model, parameters, dataset snapshot and
E-01–E-04 definitions for both. Dataset inputs supply `reference_context`,
`conversation_history` and `user_message`. Do not substitute one of the fictional
history model names as a real provider model.

Review **dark_side_delivery**, **record_fidelity**, **claim_support** and
**respectful_tone**. The playful criterion should make the difference audible;
serious criteria make the trade-off inspectable. Review a normal salary-waiver case,
the own-transfer exception and the unsupported-overdraft case. The separate
calibration controls illustrate confidently wrong, invented and insulting answers;
they are not expected answers to the normal cases.

For **record_fidelity** and **claim_support**, compare the **Pass**, **Fail** and
**Not applicable** counts separately, keeping pending/error states visible.
Use these same categories in historical inspection, experiments and live chats.
The other criteria retain their numeric values. A Not applicable result is a
completed judgment, not a passing result or a missing execution.

Scores can improve, worsen, remain mixed, take time, or fail. Show what actually
returned. Pending is not zero. Do not rerun until a desired result appears. The
presenter decides whether this candidate is worth promoting, demonstrating the
information Langfuse surfaces rather than their skill at prompt writing.

## Beat 3 — promotion reaches a real conversation

Demonstrate member denial for the protected label, then use the administrator/owner
to move `production` to the chosen version. This permission check is independent
of experiment scores. If protection is unavailable, say that this part has not
been demonstrated rather than simulating success in the companion.

In the companion, start a new product-explainer chat and send these four messages:

1. “What does the Everyday Account cost, and when is the monthly fee waived?”
2. “I said €1,200 earlier, but I meant €1,100 in salary each month. Does that qualify?”
3. “That’s not what I meant. This damn fee is frustrating — does transferring my own money count?”
4. “Okay. What documents do I need, and how long does it take after everything is submitted?”

Each turn fetches the managed `production` prompt afresh. The reply is a real model
result and may differ from authored history. Check the recorded prompt version in
Presenter tools. Give feedback on one saved reply if useful; feedback is bound
to that reply's root observation, not whichever turn is currently selected.

Choose **Open session**, the primary link. The native session should show each new
user/assistant exchange once. Open a turn's underlying observations to inspect its
prompt version and scores. Reply evaluators run on the generation; input evaluators
run on the request root. Give the asynchronous judges time to complete and explain
missing or failed jobs honestly. Do not represent the four input flags as output
quality or suggest that changing a prompt changes an unchanged user input.

## Recovery and repeatability

A new conversation clears the live chat context, not Langfuse history. To repeat the
before/after, the administrator can move `production` back to the previously
recorded version and start another conversation. Keep real experiment outcomes and
sessions visible; do not erase inconvenient scores.

A failed prompt fetch, model call or telemetry export produces an explicit error.
Resolve the underlying setup and start a new conversation if necessary. Preview
mode is visibly labelled and cannot stand in for live health or native evidence.

## Developer mode — installation, seed and verification

Install the pinned kit with `python -m pip install -e '.[dev]'`. Core is pinned to
v4.1.1; this version uses the separate offline commands:

```sh
synth-authoring validate usecase.yaml
synth-authoring conformance .
pytest -q
```

For a credential-free companion preview, run `synth preview --port 8765`. It uses the
same app factory with a fixture adapter and deliberately reports live health as not
ready. See `docs/demo/authoring/COMPANION.md` for the isolated preview boundary.

Load credentials through the approved environment workflow, never into committed
configuration. `.env.example` lists names; this CLI does not silently load `.env`.
A Langfuse judge connection is separate from the companion provider key. Set
`evaluation.provider` and `evaluation.model` (or their documented environment
variables) to the existing Langfuse connection and usable model.

Use a fresh approved demo project and a fresh state directory. Start with 48 history
traces; complete the small live journey before generating the intended full volume.
Run `synth configure-evaluators --config config/demo.yaml` once before the seed; this separate setup may invoke the configured judge model for validation. The seed provisions the nine prompt families, datasets and score configurations, and reads the existing managed evaluators without invoking them. It then
spools deterministic history, imports once and records exact evidence.

```sh
export SYNTH_STATE_DIR=/your/writable/prompt-small-state
export SYNTH_OUT_DIR=/your/writable/prompt-small-artifacts
synth seed --config config/demo.yaml --set generation.target_traces=48
synth verify --config config/demo.yaml --set generation.target_traces=48
synth companion --config config/demo.yaml --host 127.0.0.1 --port 8765
```

If this project was successfully seeded before evaluator setup, complete
`configure-evaluators` with authorised model use, then refresh its configuration
receipt using the **same target, state directory, seed, trace count and explicit
as-of date** as that import:

```sh
synth seed --config config/demo.yaml --set generation.target_traces=48 --refresh-configuration
synth verify --config config/demo.yaml --set generation.target_traces=48
```

Refresh only reads existing evaluator definitions/rules and saves their validated
receipts. It preserves seeded events, IDs, the spool and import status, and never
provisions assets or reimports data. Incomplete or conflicting configuration
leaves the receipt unchanged. Categorical E-02/E-03 live verification and other
unresolved prerequisites remain visible; a refresh does not establish live evaluator results. The companion reads
the updated receipt on its next connection check.

For the intended 1,620-trace run, use the same seed and as-of date on a **different
fresh project** after the small walkthrough succeeds. The seed runbook is copied
to the configured output directory (`/app/out` in Depot). The anchors file on the
spool volume contains project identity, provisioned assets and representative
current-run records; the live container reads it without modifying it.

**Ingestion appends.** Do not repeat an import after partial failure. There is no
kit command that deletes or resets a project. An operator must select a fresh
project, or separately authorise and complete an established demo-only reset,
then use a fresh state directory. A documentation/UI change needs no re-seed.

Protected-label setup and both role checks are native project prerequisites.
See `docs/demo/authoring/READINESS_RESEARCH.md` for release/admission access. A signed,
immutable candidate and passed staging rehearsal are required before describing
this kit as demo-ready. Publishing is a separate step.

## Recorded rehearsal caveats

The 2026-10-08 corrected native comparison improved theatrical delivery from
0.00 to 0.75 while factual checks passed and respectful tone stayed 1.00. The
subsequent four-turn live session used production v9 with the exact style instruction,
but every reply retained ordinary prose. Do not promise a deterministic voice change;
show the resolved version and actual outcomes. Two user-input judges also flagged
an explicit self-correction incorrectly. See [native rehearsal](docs/demo/authoring/NATIVE_REHEARSAL.md)
for the preserved results, correct context mappings and remaining permission/delivery checks.
