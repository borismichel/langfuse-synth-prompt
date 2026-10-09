# Fresh project verification

Verified 2026-10-09 using implementation `2ab6285755330c6fdd36f86bf7834698be8c09e3`.
The user created and supplied access to `prompt-portfolio-demo`
(`cmv0gc1710815ad0k7nnnd6v5`, EU Cloud). Credentials remain in ignored local
configuration; the previous pilot and its private configuration were preserved.
The accepted story, prototype and runtime were unchanged.

## Setup and exact readback

The official CLI authenticated the project and found no prompts, datasets,
observations or model connections before setup. The previously authorised Depot
Anthropic credential was configured for `claude-sonnet-4-6`. Ten managed evaluators
and ten enabled live rules were created and read back before seeding, with no
missing setup. In native Chrome settings, `production` was added to Protected Labels.
No member role or access grant was changed.

The seed ran once with seed 42, `target_traces=48`, and explicit as-of date
2026-10-09. It imported 500 events: 66 traces (48 history plus 18 authored experiment
examples), 80 generations and 312 authored scores. Its final bound spool SHA-256 is
`bb228efcad880e575e4d04a38a01957402fb75cde7051c8d01ab4e00e58f96c6`.
All **244 verification checks passed**, including exact current-run observations,
categorical score values and subjects, prompt versions and labels, tools, rubric
metadata, dataset cases and historical experiment links.

[Verification and receipt](evidence/fresh-project-verification.json) distinguish
whole-spool counts from the representative records read back. The small import
has no claim to full-volume statistical coverage or all possible category outcomes.

## Native inspection

- Product versions: eight opening versions, v7 `production`, v8 `development`.
- Product Metrics: authored v1–v5 rows have cost/latency and categorical counts;
  for example v3 has two Fail and three Pass results on each factual criterion,
  while v5 has seven Pass results. A real v7 turn is shown separately by score
  source. The small sample leaves v6 without usage; v8 is intentionally unpublished.
- Historical fee trace `91f9306952345f25e5622491d574969c`: root request → reference
  retriever, calculator tool and reply generation. The tool takes three withdrawals,
  two included, EUR 1.50 per additional withdrawal, and returns EUR 1.50. Four input
  scores attach to the root; three reply scores attach to the generation. Its
  metadata explicitly identifies authored synthetic history and no executed judge.
- Native Experiments lists all eighteen authored runs with their dataset and prompt
  links, one item each, zero displayed item errors, and authored score results.

Screenshots: [protected label](evidence/fresh-protected-label.png),
[prompt metrics](evidence/fresh-prompt-metrics.png),
[historical calculator](evidence/fresh-historical-tool.png),
[authored experiments](evidence/fresh-authored-experiments.png).

## One bounded live connection check

The delivered companion at local port 8774 was connected to this project's seed
receipt. Clicking **Monthly fee** made one actual model call using
`products/explainer` v7. The reply correctly described the EUR 4 fee, qualifying
salary waiver, own-account-transfer exclusion and per-calendar-month assessment.
The model also described the supplied card replacement and withdrawal fees.

Session `prompt-live-af106f29edd14167bae431e59551e3f9` has three observations and
eight actual EVAL results: four user-input criteria on the root and four reply
criteria on the generation. Both categorical factual checks returned Pass;
respectful tone was 1, theatrical style 0, and all four input signals 0. Actual
results are retained without a quality retry. Observation-scoped rubric maps and
separate trace inventory are verified in the [live readback](evidence/fresh-project-live.json).

**Open session** opened the correct native chat view, displaying this user/reply
once. [Companion](evidence/fresh-live-companion.png) and
[native session](evidence/fresh-native-session.png) screenshots record the result.
This one-turn connection check complements the earlier multi-turn, calculator,
experiment and promotion rehearsals; it does not replace or relabel their evidence.

## What remains

Member-role denial has not been observed: only the owner session is available.
Protected-label configuration is verified, while role enforcement is a separate
presenter check. The earlier corrected native v7/v9 experiments and owner promotion
remain valid evidence for unchanged behaviour and were not repeated on this target.

The full 1,620-history-trace import remains pending. This small target must not be
reseeded: imports append. Use a different fresh target or a separately authorised
established reset, with fresh state and the same seed/date.

Signed release, Depot admission and delivered staging rehearsal remain pending
for the concrete deployment prerequisites in [Depot access](DEPOT_ACCESS.md).
A passing small import is not a claim of completed Depot delivery.
