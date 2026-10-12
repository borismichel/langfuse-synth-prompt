# Seeded component coverage

The 2026-10-12 user correction makes composition present from the start and varies
it by task. Four text families are seeded before the nine chat families. Current
v7/v8 prompts use the following references; earlier v1–6 retain their instructions
and reference-context dependency.

| Agent | Reference context | Factual boundaries | Voice | Structured output |
|---|---|---|---|---|
| Product explainer | v1 | v1 | production | — |
| Fee explainer | v1 | v1 | production | — |
| Application guide | v1 | v1 | production | — |
| Intent classifier | v1 | — | — | v1 |
| Query rewriter | v1 | — | — | — |
| Conversation summariser | v1 | v1 | — | — |
| Field extractor | v1 | v1 | — | v1 |
| Message drafter | v1 | v1 | production | — |
| Handoff note | v1 | v1 | — | — |

A dash means task instructions remain local, not that accuracy or response format
is unconstrained. Query rewriting and internal handoffs do not follow customer
personality changes. Structured agents retain their own output constraints.

Product Explainer's baseline has the same factual and respectful plain-English
intent, now expressed using the existing shared boundaries and voice text. The
playful candidate replaces the baseline voice instead of appending a conflicting
style. Source fixtures, prototype case and historical generation share that text.
All historical v1–6 instructions remain unchanged.

The voice production label starts on v1; playful is v2. Changing the production
label affects the four customer-facing dependents on their next prompt retrieval.
For isolated experiments, replace the existing reference with playful in a new
parent version and promote that parent after comparison. Frozen comparisons
should pin the voice version; a shared mutable label can change resolved content
without changing the parent version. Captured generation input records actual
resolved instructions used for each call.

Langfuse resolves references natively before SDK compilation, per its
[prompt composability documentation](https://langfuse.com/docs/prompt-management/features/composability).
No local live resolver or model call is added to seeding. New receipts use
native-text-components-v2. Verification recognises v1 and uncomposed legacy
receipts using their original Product Explainer text and pinned reference policy.

Validation covers exact dependency membership for all 18 current prompt versions,
label changes reaching only the four intended agents, native-shaped resolution,
real SDK compilation, candidate style replacement and previous receipt formats.

Post-demo verification follows the current voice label when label checks are
explicitly disabled, while still checking every stored parent reference and all
pinned component versions. Strict fresh-seed verification requires the baseline.
Expansion of a seed from an older composition revision must use its original kit
release; this release rejects that operation before network access rather than
recording revised instructions against an older parent prompt. Verification of
old receipts remains supported.

Current dry-run project repair created new production/development parent versions
for eight affected families; field extraction already had the intended coverage.
Existing parent versions and history were preserved. The user's production voice
selection (v2) was retained. All updated raw references and resolved texts were
read back. A real Product Explainer turn used parent v9 and the selected voice,
while retaining EUR 4, EUR 1,200 qualifying salary and the own-transfer exclusion.
See [repair receipt](evidence/seeded-blocks-live-repair.json) and
[live response](evidence/seeded-blocks-live.png).
