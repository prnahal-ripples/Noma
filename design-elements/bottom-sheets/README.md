# Bottom sheets — @magic-spells, skinned with NOMA tokens

Static HTML/CSS demo. No build step — open `index.html` directly or serve the
folder with any static file server.

- **[index.html](./index.html)** — gallery of 10 bottom-sheet types (basic,
  action menu, confirmation, scrollable, snap points, inset, form, filter,
  detail, media). Each is a real instance of the component, not a mockup.
- **[single-demo.html](./single-demo.html)** — the original one-sheet demo
  (device settings), kept for reference.

## What this is

[`@magic-spells/bottom-sheet`](https://github.com/magic-spells/bottom-sheet)
and [`@magic-spells/dialog-panel`](https://github.com/magic-spells/dialog-panel)
(Cory Schulz, MIT), restyled entirely with NOMA design tokens instead of
their default look. The gesture/physics behavior (drag, flick-to-dismiss,
velocity-aware snap settling) is the package's own — untouched.

- `vendor/` — the built dist files (`.esm.js` + `.css`) for both packages,
  vendored directly rather than via `node_modules` so this folder has zero
  install step. Version pins: `bottom-sheet@2.0.2`, `dialog-panel@2.0.1`.
- `fonts/` — Google Sans Flex (SIL OFL), copied from
  [`src/fonts/google-sans-flex/`](../../src/fonts/google-sans-flex/).

## Tokens

Hand-copied from [`src/tokens/design.tokens.js`](../../src/tokens/design.tokens.js)
and [`src/tokens/motion.tokens.js`](../../src/tokens/motion.tokens.js) — this
is a static-HTML scratch surface with no build step wired to the JS token
files, so it cannot import them directly. If tokens drift, the JS files win;
re-sync this folder by hand.

Reflects the **rebuilt** token file (2026-08-11, five laws: gradient ground,
green never solid, white means raised, ink CTA, bespoke insurance card).

Two open gaps this demo surfaces, both already tracked in the token file
rather than invented here:
- **No destructive color.** `colors.status` is `null` (ADR-001 O-6), so
  sheet 3's "Remove" reads identically to an ordinary confirm.
- **No spring-physics token.** The snap-settle spring (sheet 5) uses the
  package's own default tuning — only cubic-bezier easings exist in
  `motion.tokens.js`.

## Motion compliance

Per [`.claude/rules/motion.md`](../../.claude/rules/motion.md):
- Open/close transitions stay on the package's decelerate-only curve, not
  `easings.springBold` — that one CSS property drives both directions, and
  rule 3 says exits never bounce.
- `prefers-reduced-motion` is handled twice: CSS collapses transition/
  animation durations, and a small script sets `spring="none"` on the
  snap-point sheets, because the snap settle runs on a JS `requestAnimationFrame`
  spring that never sees the CSS media query.
