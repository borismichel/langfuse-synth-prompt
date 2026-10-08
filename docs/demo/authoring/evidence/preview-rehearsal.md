# Implemented companion preview rehearsal

2026-10-08, local loopback preview on port 8767. This is fixture evidence only.

The implementation agent checked all three bots, their question suggestions,
feedback submission, light/wide and dark/narrow layouts, and browser errors. The
parent independently replayed the four product-explainer suggestions:

| Action | Observed result |
| --- | --- |
| Monthly fee | Plain reply explains EUR 4, salary waiver threshold and own-transfer exception. |
| Correct the deposit | Plain reply acknowledges the correction and excludes own transfers. |
| Disagree with the reply | Plain reply acknowledges frustration and explains the same rule. |
| Opening documents | Plain reply retains photo ID, address evidence and two-working-day condition. |

The first parent review caught a fixture bug: the second turn was theatrical even
though v7 remained selected. The implementation was corrected to use plain
conversation fixtures for v7 and the accepted styled fixture for v9. Both complete
four-turn paths now have assertions for replies, roles, history and prompt versions.
The parent repeated all four v7 actions after restart and confirmed the corrected
replies. Screenshot [companion-four-turns.jpg](companion-four-turns.jpg) shows the
final reply with the preview boundary visible.

The surface explicitly identifies fixtures, leaves native links disabled in
preview, and reports no live readiness. No model or managed judge was called.
**Open session**, native prompt metrics, protected promotion and experiment results
still require the real target; this is not the delivered live rehearsal.
