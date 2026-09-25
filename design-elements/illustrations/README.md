# Illustrations

Owner-supplied page illustrations — the large visual in a screen's `pgt()`
half. Distinct from `../engraved-icons/`: those are a monochrome *icon*
register pressed into the surface, these are small scenes with their own
composition and, where the owner's artwork calls for it, colour.

| File | Used by | Notes |
|---|---|---|
| `geofencing.svg` | first run node 24 (L1, L1D) | House inside a dashed boundary, plus the "you" dot. Supplied 2026-08-19, replacing a CSS-drawn stand-in. |

## How these are consumed

Embedded as a **base64 data URI background-image**, never inlined — the same
rule `GLYPH_B64` documents in `docs/features/first-run/build-prototype.py`:
Figma exports carry `filter0_di_…` / `paint0_linear_…` ids that collide the
moment two screens share the DOM, which the seamless screen swap guarantees
during every transition.

⚠ `geofencing.svg` is consumed in TWO pieces. The build strips the green
"you" dot out of the plate and re-draws it as a positioned element so it can
animate across the dashed boundary — the behaviour the CSS stand-in had, and
which the owner asked to keep. The stripper asserts on the dot's markup, so
re-exporting this file with a different dot fails the build loudly rather
than silently shipping two dots. Geometry for the overlay is PARSED from this
file, not hardcoded, so the two cannot drift.

⚠ The green dot (`#7CF280`) is the only colour in first run's page
illustrations. `build-prototype.py`'s own visual direction says "no accent
green anywhere in this file"; this is owner-supplied artwork and overrides
that for this one mark. Flagged rather than quietly recoloured.
