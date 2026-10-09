# Companion implementation evidence

Implemented 2026-10-08 against core **v4.1.1** and installed Langfuse Python **4.17.0**.
The accepted companion styling and all three assistants are preserved. Prompt browsing,
editing, experiment execution, protected-label promotion, sessions and observation detail
belong to native Langfuse. The companion links there; it does not reproduce those pages.

The user's 2026-10-09 request adds restrained lime accents, the exact brand corner
masks and a small stripe motif. Layout and behaviour remain unchanged; see
[brand refinement and visual checks](BRAND_REFINEMENT.md).

## Delivered surface

- Product explainer PR-01, fee explainer PR-02 and application guide PR-03 share the same
  server and UI. The accepted suggestion sets remain available, alongside free-text live input.
- **Open session** is the primary inspection action. Individual generation links, exact
  resolved versions, root feedback targets and evaluator readback are inside the collapsed
  **Presenter tools** disclosure. Native links are disabled in the explicit fixture preview.
- New conversation starts a fresh session for the selected bot; switching bots preserves
  each bot's current conversation. Each turn has a separate trace/root and reply generation.
- Accepted layout variants remain available in Presenter tools, with arrow-key switching
  outside editable fields. Theme and layout are retained in the URL.

The CSS includes the brand skill's unchanged website token/component stylesheet. Inter,
Geist Mono and their licenses are local assets copied from the accepted prototype.
**Space Grotesk is the disclosed display-face substitute for F37 Analog.** The Langfuse
name is plain text, not a fabricated logo. The dark small-text contrast adaptation from the
accepted prototype remains. No exact native UI or website parity is claimed.

## Request and observation contract

`ConversationService` gets all real clients from `CompanionAdapter`. Every request retrieves
its managed **chat** prompt with `label="production"`, `cache_ttl_seconds=0` and no fallback.
It compiles the supplied reference record, role-bearing prior messages and current question
through the managed template. Core's provider seam takes a single system string, so the
compiled system messages are joined with a blank line; the generation input records that
exact system string plus the actual history and current message sent to the provider.
The generation receives the real SDK prompt object, retaining its resolved version.

Each request emits a `handle-chat-turn` SPAN root, a validated
`retrieve-product-context` RETRIEVER, an optional `calculate-fee` TOOL,
and a sibling `generate-response` GENERATION, with
`environment=prompt-live` and the same session ID. The root's `input.messages` contains only
the new user message; its output contains only the new assistant message, avoiding repeated
history in session replay. Root and generation both expose:

- `current_user_message`, `prior_messages` and `reference_context` in metadata;
- application/prompt IDs, prompt name, resolved prompt version and per-criterion rubric revisions;
- `evaluation_subject=user_input` on the root, `assistant_reply` on the generation.

The retriever executes a real catalog read and validates its required fields.
For PR-02's supported explicit current-message monthly withdrawal count, a separate
tool calculates the excess fee from that record. Its structured result is added
to a copied reference context for the model and retained in generation metadata
as `calculation_results`; evaluator `reference_context` stays the original source.
The strict parser skips ambiguous corrections, hypotheticals and unsupported
wording rather than inventing tool arguments. Tool/retriever observations carry no
evaluation subject or managed-prompt attachment. Errors mark the failed operation
and request and prevent a provider call. These are application operations, so no
fictional model-selected tool messages are inserted.

Only short correlation fields use propagated metadata because the SDK truncates propagated
values. Full structured evaluator context is set explicitly on each observation. Input
judges never need to join a child, and reply judges never need to join the root.
The provider's actual model and input/output token usage are recorded; costs are left to
Langfuse's model pricing. No guessed live cost or authored live score is written.

The four input and applicable reply evaluator tracks run through the provisioned native
observation rules. Readback matches exact `(criterion name, observation ID)` pairs; unrelated
scores cannot satisfy completion. Missing results stay pending, read failures are unavailable,
and the UI points to native evaluation logs because an absent score alone cannot establish
whether the judge is queued or failed. There is no score gate, automatic promotion or
retry-until-pass loop. E-02/E-03 now expect the approved CATEGORICAL labels
`Pass`, `Fail`, `Not applicable`. Readback uses the category string, never an
internal numeric category code. Unexpected types, labels or duplicate criterion/
subject rows are invalid; missing results stay pending. A completed Not applicable
judgment does not imply a pass, missing result or failed execution. The native
rules are configured; new live outcome/calibration checks remain separate.

## Feedback and failure behaviour

Feedback is submitted server-side as BOOLEAN `user-helpfulness` on the saved **root observation**,
with its trace correlation, comment and deterministic score ID. Subsequent edits upsert that
score; changing bots or adding another reply does not change the target. An opaque conversation
capability is required, and the server resolves the target from its saved reply rather than
trusting a browser-supplied observation ID.

Prompt/provider errors retain the request identity and an ERROR observation. Exception types
are recorded without leaking arbitrary provider messages. No fixture or local prompt fallback
runs in live mode. A transport error marks delivery unconfirmed, even when a model reply was
already produced. Request IDs deduplicate repeated submissions; an ID cannot be reused for a
different message. Concurrent turns in one conversation return a conflict rather than
interleaving history. Provider calls occur only for interactive turns, never seeding or health.

Working history/capabilities are **in memory** (40 turns per session; 1,000 concurrent sessions;
idle entries pruned after 24 hours on new-session creation). A process restart requires a new
conversation. Actual observations and scores persist in Langfuse. The companion reads seed
anchors only: core v4.1.1's Depot spool is mounted read-only, so it never writes conversation
state or feedback receipts under `SYNTH_STATE_DIR`.

## Health, proxy and preview

Live `/healthz` returns HTTP 200 when the process serves requests, as core v4.1.1 specifies.
Its JSON `ready` is independent and remains false when the write/model binding, managed
production prompts, target-matched anchors or enabled evaluator rules are unavailable.
`/api/connection` returns the same story prerequisite report, exposed by **Refresh connection
and prompts**. Health does not prove a provider completion or executed evaluator result.
The eight companion evaluator rule IDs are read back, not merely trusted from the receipt.
The full kit provisions ten managed pairs, including two additional portfolio criteria.
An earlier numeric seed receipt does not establish categorical history readiness.

All internal assets/API/navigation respect `LIVE_BASE_PATH`; routes themselves stay mounted
at `/`, matching Depot's prefix-stripping proxy. Native Langfuse URLs use the adapter's actual
project and host. Static files/fonts require no external browser network requests.

Developer-only preview:

```bash
python -m synth.companion.preview --port 8767
```

This starts the **same app factory** with `FixtureAdapter`, clears inherited credentials and
target configuration, and blocks all outbound socket connections, including loopback. It binds
only to `127.0.0.1`. Unsupported messages fail honestly; displayed suggestions have authored
fixture replies. Preview health always returns **HTTP 503, ready:false**. Preview cannot
establish live readiness, inference, evaluator execution, prompt promotion or admission.

## Checks performed

`tests/test_companion_runtime.py`: **14 passed**. Coverage includes all three bots, exact
root/generation context and message roles, installed SDK chat-placeholder compilation,
TTL-zero refresh, immutable old versions, four-turn v7 plain/v9 theatrical preview replies
with exact actual history, feedback identity/upsert, session isolation,
request deduplication, concurrent-turn rejection, prompt/provider/feedback errors, exact
score target readback, active-rule/project readiness, proxy-prefix assets, and preview
credential/egress isolation. Tests use explicit fixture clients and make no external calls.
A Starlette/httpx deprecation notice is non-blocking.

The core companion conformance check serves the index and health without credentials.
Its live HTTP-200/JSON-ready-false distinction is deliberate; preview stays HTTP 503.

Browser rehearsal used the isolated app on loopback, exercised all three bots and a saved
feedback comment, inspected wide light/dark and 390px dark views, and confirmed no horizontal
overflow at 390px and no console errors. Screenshots were visually inspected in the browser
tool. Presenter controls are collapsed on entry. Local font requests return successfully;
computed heading style selects Space Grotesk. Reload resets the in-memory browser conversation.

**Live evidence now observed:** four actual PR-01 turns with production v7,
provider usage and cost, sixteen persisted request/tool/retriever/generation
observations and twenty-four EVAL scores on their exact input/reply subjects.
See [the sanitized readback](evidence/live-model-session.json) and
[actual conversation screenshot](evidence/live-companion-four-turns.jpg).
The turn-two self-correction produced false-positive contradiction/disagreement
signals; this remains visible as a judge-calibration finding.

**Later native evidence:** authenticated Chrome now verifies session chat rendering,
the refined trace, prompt metrics, saved production-label protection and staged
PR-01 v9. Ten managed criteria are configured, including categorical E-02/E-03.
The corrected native v7 experiment completed eight outputs and 32 scores after
explicit evaluator-context repair. See [native rehearsal](NATIVE_REHEARSAL.md)
and [experiment readback](evidence/native-experiments.json) for the evolving
comparison and promotion evidence; the earlier IAB sign-in limitation is superseded.

**Still separate gates at this checkpoint:** complete corrected comparison and
production-label refresh after promotion; live E-02/E-03 Pass/Fail/Not applicable
calibration and exact-target readback; judge failure handling; member-denial
rehearsal; full-scale categorical history; signed release and Depot proxy/admission.
Existing live sessions above predate the categorical change and cannot prove it.

Assistant replies render a small Markdown subset (headings, flat lists, tables,
rules, paragraphs, bold and inline code) using text nodes and safe elements.
No model HTML executes and no automatic links are created; user input remains
plaintext. Existing pre-wrap styling preserves paragraph line breaks. The offline
renderer safety regression is included in CI.

## Official references inspected

- [Prompt caching / TTL zero](https://langfuse.com/docs/prompt-management/features/caching)
- [Managed message placeholders](https://langfuse.com/docs/prompt-management/features/message-placeholders)
- [Prompt-generation links](https://langfuse.com/docs/prompt-management/features/link-to-traces)
- [Sessions](https://langfuse.com/docs/observability/features/sessions)
- [Observation data model](https://langfuse.com/docs/observability/data-model)
- [SDK instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation)
- [Observation evaluator migration](https://langfuse.com/faq/all/llm-as-a-judge-migration)
- [User feedback](https://langfuse.com/docs/observability/features/user-feedback)
- [Score ingestion](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [Trace best practices](https://langfuse.com/docs/observability/best-practices)

## Additional real UI smoke checks

After the four-turn PR-01 session, PR-02 explained the third-withdrawal fee as
EUR 1.50. PR-03 rejected proof of address from five months ago and preserved the
three-month limit. Both returned native session links. The PR-03 screenshot
[shows the final reply renderer](evidence/live-companion-formatted.jpg), including
headings, bold text and lists. These are UI smoke checks, not the separately
validated four-turn session or claims of evaluator correctness for every bot.
The PR-03 answer also supplied common document examples absent from the fictional
reference; retain this as a grounding review example, not a verified factual pass.

- PR-02 session: `prompt-live-e088c7ce0e804129a22fe8e11623ee95`
- PR-03 session: `prompt-live-3ee8c16b9127473385f1dd4b29ad7a68`


## Refined live readback

A new three-turn PR-02 session exercised the refined runtime without reimporting
history. Readback contains eleven observations: three request roots, three
retrievers, three generations and two actual fee calculations. Three withdrawals
produce EUR 1.50; two produce EUR 0.00. The third incomplete correction has no
calculator observation or stale derived context. Fifteen managed EVAL outcomes
attach to the correct request/reply subjects. A labelled rehearsal feedback score
was read back on the third request root. See
[refined live evidence](evidence/refined-live-session.json) and
[companion screenshot](evidence/refined-companion-feedback.jpg).

This closes the revised companion trace/feedback persistence checks. Subsequent
native UI replay was observed in authenticated Chrome and is recorded in
[NATIVE_REHEARSAL.md](NATIVE_REHEARSAL.md). Permission denial, promotion effects,
experiment comparison and release/Depot admission require their own evidence;
this earlier three-turn session does not establish categorical evaluator execution.

## Promoted categorical live rehearsal

[The new four-turn session](evidence/categorical-live-session.json) verifies 32
outcomes across both subjects, exact v9 system instructions, ordered history,
request/retriever/generation parentage, and categorical Pass results for both
factual criteria. Native **Open session** and the linked v9 generation were
inspected in Chrome. The model retained ordinary prose and all four style scores
are zero; two input-judge false positives on the correction remain visible.
This evidence predates the final per-criterion metadata provenance refinement;
its actual managed evaluator versions remain recorded unchanged.
[Native walkthrough and screenshots](NATIVE_REHEARSAL.md).

## Third assistant and SDK propagation verification

The application guide now has independent live evidence for its document-recency
question and missing-status boundary: two turns, six observations and fourteen
correctly targeted EVAL outcomes. Native session replay shows each exchange once.
[Evidence](evidence/application-guide-live.json) retains general suggestions outside
the source and the judges' actual Pass decisions.

That run exposed SDK trace metadata overriding an observation key of the same name.
The trace inventory is now a distinct, explicitly JSON-encoded
`trace_rubric_revisions`; observation `rubric_revisions` retains the applicable input
or reply criteria. A real SDK/export regression and [one new live turn](evidence/application-guide-metadata-fixed.json)
verify the repair, including no evaluation subject/rubric map on the retriever.
