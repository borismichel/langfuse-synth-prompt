# Prompt portfolio prototype

A local, deterministic rehearsal of the accepted story packet. No model,
Langfuse ingestion, paid evaluation, deployment or production kit is connected.

From the repository root, install once with Node 22.12+:

```sh
npm ci --prefix design/prototype
```

Start the preview:

```sh
npm run dev --prefix design/prototype
```

Open http://127.0.0.1:4185/ for the prompt-first presenter journey.
Open http://127.0.0.1:4185/?view=companion for direct chatbot entry.
The server binds to loopback only. Stop it with Ctrl-C.

```sh
npm run check --prefix design/prototype
npm run build --prefix design/prototype
```

All interaction state lives in memory. Reset or reload starts a clean rehearsal;
view, theme and layout remain in the URL. Example prompts route to authored
responses; unsupported text or arbitrary edited system prompts never receive
fabricated model results.

## Rehearse

1. Open `products/explainer`. Inspect Metrics, Versions and Dataset. The other
   eight prompts have matching examples; their historic full-text versions and
   per-version metric series are explicitly lighter storyboards.
2. Create version 9. Keep or restore the supplied style change, then save to
   staging. Versions are immutable after saving; reset to explore a different draft.
3. Open the experiment. Pick expected, mixed or non-improving fixture outcomes;
   run, then **Complete fixture run**. Inspect a paired case and the controls.
4. Try promotion as Member, then use the review-role selector to switch to Admin
   and promote. Scores never prevent promotion or force another run.
5. Open Chatbots. Click Monthly fee → **Receive fixture reply** → **Complete
   fixture evaluations**. Continue with Correct the deposit, Disagree with the
   reply, and Opening documents. Explicit completion controls let the reviewer
   inspect pending states; they are not intended production UI.
6. **Open session** is the primary evidence link. User-input chips open request
   roots; answer chips open reply generations. Inspect scores, exact prompt
   versions, raw/formatted messages and prior context.
7. Leave feedback on a saved reply. Its root target stays fixed. Switch prompts,
   layouts and sessions; no feedback moves to a different operation.
8. Story & coverage exposes exact score records and authored population previews.
   Reset restores the opening state. Existing reference SESSION-01 is always a
   separate authored rehearsal, never pre-promotion production traffic.

Three companion layouts share the same state. Use the bottom selector or left/right
keys outside inputs. `?variant=Focused%20conversation` selects the centred layout;
`?variant=Conversation%20%26%20context` puts context on the right.

See [prototype brief](../../docs/demo/prototype/BRIEF.md),
[review evidence](../../docs/demo/prototype/REVIEW.md) and
[source inventory](../../docs/demo/prototype/PROVENANCE.json).
