# Categorical factual-check verification

2026-10-08. Local prototype only; no Langfuse writes or judge calls.

- `npm run check`: passed. Initial totals remain 24 traces, 51 observations,
  137 outcomes and 12 active definitions. Rehearsal totals remain 47 traces,
  97 observations and 256 outcomes.
- Explicit checks cover Pass/Fail/Not applicable conversion for both E-02 and
  E-03, authored 1/0/null preservation, history/experiment/live category parity,
  category counts and exclusion of pending/failed execution from completed counts.
  The existing CTRL-03 remains E-02 Fail and E-03 Not applicable.
- `npm run build`: passed, 1,631 modules transformed, Vite 6.1.0. Output:
  index.html 0.38 kB; CSS 82.38 kB; JS 399.84 kB. Node reported its existing
  `module.register()` deprecation warning; no build error occurred.
- Browser verification at the default desktop viewport: SESSION-01 shows Pass;
  CTRL-03 shows Fail and Not applicable; native score badges show the same labels
  on the original reply generation. History Metrics shows category counts and
  completion coverage instead of the former fidelity median. Light session and
  dark session/trace/metrics were inspected; existing typography and layout remain.
- [Dark categorical control](categorical-control-dark.jpg) records the local
  control session. It is authored fixture evidence, not native deployment proof.
- A narrow viewport override was rejected by automatic approval review as
  unrequested responsive testing. No override was applied or bypass attempted;
  narrow-screen revalidation is not claimed by this amendment.

## Rubric revision provenance correction

2026-10-08. The prototype's shared definitions now assign `r2` to E-02/E-03
and retain `r1` for all other criteria. Each authored score receives its revision
and ID suffix from that definition. Trace identity reads the score's recorded
revision; the score-definition view reads the shared definition revision.
Dataset revision labels remain `r1`; score values and layout are unchanged.

`npm run check` passed after this correction, including assertions that every
history, experiment, live and feedback record matches its definition revision,
that E-02/E-03 score IDs end in `r2`, and that other criteria remain `r1`.
The earlier screenshot verifies category rendering; it does not independently
verify the later revision-label correction.

Fresh `npm run build` also passed after the correction: Vite 6.1.0 transformed
1,631 modules in 1m 40s. Output was index.html 0.38 kB, unchanged CSS 82.38 kB,
and JS 399.95 kB. The existing Node `module.register()` deprecation warning was
non-blocking. `git diff --check` passed.
