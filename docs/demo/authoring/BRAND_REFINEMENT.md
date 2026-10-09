# Companion brand refinement

Implemented and visually checked 2026-10-09 following the user's request for
“a little lime, corners, etc in the companion app”. This is an authorised visual
refinement of the accepted companion, preserving its layout, wording and story.
Prompt retrieval, trace shapes, score routing and model behaviour are unchanged.

## Design source and changes

Used `langfuse-brand-assets` and its captured langfuse.com style guide (2026-09-20).
The existing bundled `brand.css` remains byte-identical to that source.

- The word “clarity.” uses the existing `lf-marker` recipe: #FBFF7A multiply layer,
  .76em height and −52% translation, with text above the layer.
- The chat panel uses the exact four 8px SVG corner masks with curved inner joints.
  The flush variant fits the panel's clipped border. Bot choices use the source
  hover masks; selected and keyboard-focused choices retain them as an intentional
  interaction adaptation. All decorative layers ignore pointer events.
- Assistant badge and selected bot number use `--surface-cta-primary`: #FBFF81 in
  light mode and the source #4C4D23 olive in dark mode. Main action buttons retain
  the brand's ink treatment. The dark marker keeps the source multiply blend, so
  it is subtle rather than fluorescent.
- A small sidebar motif uses the source 315° / 4px stripe recipe.
- Changed stylesheet and script URLs carry a revision query, resolving the observed
  browser cache that initially combined fresh markup with the prior static assets.

Inter and Geist Mono remain the body/meta fonts. **Space Grotesk remains the
explicitly disclosed substitute for licensed F37 Analog.** No exact font match
or full website parity is claimed.

## Observed verification

The same delivered companion ran in its isolated fixture preview at port 8775.
Chrome checks covered 1440×960 and 390×844 viewports in light and dark themes.
Both widths had no document horizontal overflow. Browser font checks returned
loaded for Inter, Geist Mono and Space Grotesk.

Computed styles verified 8px masks on all four corners, the light corner ink
#404039, positioned panel hosts, and exact light/dark accent fills. Selecting the
fee bot updated the heading and selection. Tabbing to the unselected application
bot showed a 2px focus outline plus its corner overlay; the hovered fee bot also
showed its corners. Empty-input Send and preview-only native links stayed disabled.
The monthly-fee suggestion returned its expected fixture reply at phone width.
No model call or Langfuse write was made for these visual checks.

Accent text contrast is 14.97:1 in light mode and 7.14:1 in dark mode, calculated
with the skill's contrast helper. The temporary viewport override was restored.

The connected live companion at port 8774 also served the revised markup/assets
and resolved its project navigation links. Its screenshot records the empty
conversation, without generating another live reply.

- [Live companion](evidence/brand-companion-live.png)
- [Light desktop](evidence/brand-companion-light-wide.png)
- [Dark desktop](evidence/brand-companion-dark-wide.png)
- [Light phone](evidence/brand-companion-light-mobile.png)
- [Dark phone](evidence/brand-companion-dark-mobile.png)
- [Keyboard focus](evidence/brand-companion-focus.png)

All **28 companion runtime checks passed**, JavaScript syntax validation passed,
and `git diff --check` passed. No new tests were added for the decorative change.
The previously recorded 170-test full-suite result remains its earlier checkpoint.

Rebuilt local image `langfuse-synth-prompt:brand-local`:
`sha256:ed13b4d5ef433e972fd6f774852f31fce78c1166dd3d3d5e1fa38003dc849d5d`.
A UID-10001, network-disabled, read-only-root container served the page and all
three static resources, including revision query strings. Installed asset hashes
match this workspace; see [container evidence](evidence/brand-container-smoke.json).
This image is local only. Earlier history/model evidence remains valid for the
unchanged runtime behaviour; this refinement does not establish Depot admission
or full-volume live verification.
