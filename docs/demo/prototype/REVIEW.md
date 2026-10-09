# Prototype review

2026-10-08. **Accepted for authoring on 2026-10-08.**
The user reviewed the running prototype and said “Looks good hand off to authoring”,
then requested finishing the complete kit using the skills and preserving the
prototype and story. This accepts the local prototype and requests implementation;
it does not turn simulated evidence into verified live behaviour.

| Deliverable | Status | Evidence |
| --- | --- | --- |
| Logic and cases | Accepted | Pure model checks, packet copies, supplemental missing-information items |
| Companion | Accepted | All three bots, local feedback, baseline/candidate flow, three layout variants |
| Trace | Accepted | Running upstream tree/type/score components; local detail fidelity disclosed |
| Session | Accepted | Four exchanges, 32 input/reply outcomes, exact observation links |
| Story and coverage | Accepted | Connected three-stage path, actual record IDs, zero-score features, aggregate preview |
| Live integrations | Pending authoring | No credentials, model, evaluator, seed or deployment executed |

## Rehearsed interactions

- Browsed the portfolio, created PR-01 v9 and saved staging.
- Ran a mixed-outcome experiment. Pending state had no result records. Completion
  exposed 64 paired outcomes; C-02 preserved its factuality/grounding failures.
- Member promotion was denied; admin promotion succeeded after that mixed result.
  No score gate or forced rerun was introduced. Local document links, fixture JSON and the exclusion of private
customer identifiers were checked. Pinned upstream IOPreviewPretty and ChatMessage
were fetched read-only from GitHub and matched the inspected source hashes.
- Used the main chatbot for four turns, then clicked its primary **Open session**
  action. The session contained four requests and 32 distinct outcomes.
- Explicit self-correction was not a contradiction; later disagreement/frustration/
  profanity remained separate input signals, alongside reply-quality scores.
- Followed an input score to its request root and inspected comments. The reply
  generation retained its own different score set and prompt version.
- Used both fee and application assistants. Unsupported free text displayed an
  honest fixture limitation instead of pretending to run a model.
- Saved a feedback comment on a reply. The model checks verified stable root target,
  upsert rather than duplication, and isolation from another selected request.
- Expanded/collapsed the actual Langfuse tree; selected the multi-prompt flow's
  lookup and confirmed it had no prompt. Selected a generation and its scores.
- Tested layout switching, arrow keys outside input, arrow-key isolation inside
  the composer, and layout/view/theme retention on URL reload. Reload correctly
  resets in-memory interaction state.

## Verification

[Model checks](evidence/model-check.txt) verify source hashes, unique records,
subject identity, session propagation/context, pending states, 64-outcome paired
runs, old version immutability, mixed-score promotion, feedback targeting,
all three bots, population totals, reset and coverage across multiple runs.

The [production Vite bundle builds](evidence/build.txt). This validates the local harness, not a demo
runtime, deployment or Langfuse integration. No production test infrastructure
was introduced. Local document links, fixture JSON and the exclusion of private
customer identifiers were checked. Pinned upstream IOPreviewPretty and ChatMessage
were fetched read-only from GitHub and matched the inspected source hashes.

Visual checks covered a 1280×800 laptop, 1440×900 wide and 390×844 narrow viewport,
light/dark themes, composer focus, disabled send/session/run controls and native
trace layout. Fonts were checked as loaded. Small screens use scrolling tables
and a wrapping/scrolling navigation; the main laptop chat composer is immediately
visible. Native trace components retain their own theme scope.

Screenshots:

- [Laptop companion](evidence/companion-laptop.jpg)
- [Wide session](evidence/session-wide.jpg)
- [Input scores on the root](evidence/input-scores-wide.jpg)
- [Native tree and score detail in dark mode](evidence/trace-dark.jpg)
- [Dark companion](evidence/companion-dark-wide.jpg)
- [Narrow light companion](evidence/companion-light-narrow.jpg)

## Deliberate limits and review decisions

- All replies, timing, usage and evaluator values are authored or locally simulated.
  Manual completion controls expose pending fetch/run/evaluation states. They are
  review controls, not proposed production customer interactions.
- Prompt metrics/editor/permissions/experiments and session replay are local
  adaptations. Reused source components establish only trace tree/type/score
  fidelity. Native product behaviour remains a live verification task.
- Main comparison is detailed. Secondary full historic prompt text and full
  per-version metric series are labelled storyboards. Their three-item datasets
  remain inspectable and matching to task/source truth.
- The three layout directions, supplemental dataset examples and authored cost
  series await review. None changes the accepted causal story.
- An upstream virtualiser smooth-scroll warning remains; tree selection and
  collapse/expand were exercised. Nested-button warnings were eliminated from the
  tree by omitting comment triggers there; full comments remain in detail.

Acceptance and the build request are now recorded above. Authoring must retain
the accepted story and prototype and verify the required live behaviour. Use the [brief](BRIEF.md) and
[start/rehearsal instructions](../../../design/prototype/README.md).

## Compatibility with the later trace-detail instruction

The user subsequently requested proper tool-call shapes in live companion and
history. The [trace amendment](../story/TRACE_SHAPES.md) adds explicit retrieval and conditional fee calculation
in the authored runtime. It preserves the accepted companion layout, prompt-first
journey, session entry point and distinct evaluation subjects. The prototype's
original screenshots/counts remain evidence of the earlier prototype; they do not
verify these added operations. Runtime assertions and fresh native readback must
establish the amended shape. No additional visual acceptance is claimed.

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

Local verification for the amendment is recorded in
[categorical checks](evidence/categorical-checks.md): model checks and production
build passed; desktop browser inspection confirmed category labels, native badges
and historical category counts. No new user acceptance of this implementation is
recorded. Narrow-screen revalidation remains unclaimed.

## User-requested model, provenance and feedback update — 2026-10-09

The user requested current Claude models by prompt role, Sonnet 5.5 for experiments
and evaluation, three-times authored history cost, prompt associations that can be
inspected from request roots, and explicit thumbs with optional written feedback.
This update implements that requested scope in the existing accepted prototype;
the layout, brand styles, case outcomes and presenter journey are retained.
No additional user acceptance of rendered or live behaviour is inferred.

The prototype imports a byte-equivalent copy of the runtime model-policy fixture.
Sonnet 5.5 serves PR-01/04/05; Opus 5.5 serves PR-02/03/07/08; Fable 5.1 serves
PR-06/09. Experiment generations use Sonnet 5.5. Authored history and experiment
cost estimates use base model prices multiplied by three; simulated live chat
cost estimates retain base prices. All remain fixtures, not billed usage.
Single-prompt roots record the resolved name/version and an exact generation
reference. FLOW-01 records three separate references without assigning one prompt
to the whole workflow. The root inspector links to those generation details.

F-01 is now BOOLEAN `user-thumbs`, an explicit signal separate from inferred
E-08 `user_disagreement`. It saves the comment on the rated reply's root, accepts
one submission, deduplicates exact retries and rejects edits. This supersedes the
earlier prototype upsert behaviour described in the original rehearsal above.

Validation on this update: `npm run check` and `npm run build` passed. The checks
cover canonical policy parity, every generation's role model, Sonnet experiments,
price calculations, root reference cardinality/identity, Boolean feedback values,
single submission and target isolation. In the running Chrome preview, the root
prompt link opened the correct Sonnet generation; FLOW-01 showed all three prompt
links; submitting thumbs down with a comment added one root outcome, disabled both
rating buttons for that reply, and displayed the saved comment beside `user-thumbs`
in the root's score view. The wide light trace view was visually inspected. Narrow
viewports and dark-theme revalidation are not claimed for this focused amendment.

### Subsequent prompt-link clarification

The user clarified: “Prompt references should stay on generation. Sorry for that.
If there was a misunderstanding they don't need to be on the root trace.” This
supersedes the root-reference portion of the amendment above. The final prototype
keeps native prompt/version associations on each generation and removes redundant
root prompt references. Request-root input evaluation and explicit user feedback
retain their existing subjects. The companion's Inspect generation link opens the observation with its native
managed-prompt association and resolved version.


## User-requested reusable text prompts — 2026-10-09

After registration, the user explicitly requested a new prompt folder containing
three or four reusable text components, actual native references from agent
prompts, and a new release. Four `building-blocks` prompts implement that addition:
reference context, factual boundaries, voice and structured output. Voice includes
the existing accepted playful instruction. The opening resolved agent content,
source facts, evaluations and three-beat journey remain unchanged; the presenter
can reuse the playful component when creating a candidate.

This records an additive user instruction and its compatibility with the accepted
prototype, not a new user acceptance of runtime tests or release evidence. The
companion layout and behaviour remain as prototyped. Fresh live resolution and
release/admission checks are required for the new revision.
