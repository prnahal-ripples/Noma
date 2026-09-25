# The master key card — owner artwork, 2026-08-20

Seven source renders from the owner, and the WebP derivatives the prototypes
embed. Same two-tier arrangement as [`../README.md`](../README.md): the PNG is
the archive, `web/` is what ships.

| File | What it is |
|---|---|
| `card-1.png` … `card-5.png` | The five colourways of ONE piece of art |
| `sleeve-back.png` | The wallet layer that sits **behind** the card |
| `sleeve-front.png` | The pocket that sits **in front** of it |

## The five are one artwork

Measured, not assumed: the luminance channels of `card-1..5` are the same
render — only the hue differs. So the card is never re-composited per colourway;
`data-kc` on `.phone` swaps one background image.

**The order is the owner's mapping, verbatim:** default → card 1, pink → card 2,
yellow → card 3, blue → card 4, green → card 5. That order is canonical in
`src/tokens/design.tokens.js` as `keycard.ways`, and `build-prototype.py` reads
it from there rather than restating it. Renaming a file here without changing
the tokens breaks the mapping silently — the swatch would select the wrong card.

## The sleeve is two layers, not a backdrop

The card slots **between** them, which is what makes it read as inserted rather
than pasted on. `sleeve-front` is shorter than `sleeve-back` — it is the pocket,
not the whole sleeve — so it is anchored to the bottom and sized by its own
aspect ratio (572/656).

⚠ **The two panels therefore have different heights.** A single percentage
`translateY` travels two different distances and leaves the shorter one on
screen; the slide-out uses a shared px distance for that reason.

## ⚠ Re-exporting invalidates measured numbers

`keycard.face` in the tokens holds the inset of the card's printed face inside
the artwork's outer tray, measured by scanning the alpha channel — **not**
derived at build time. The shimmer and the identity block are both positioned
against that box. If any `card-*.png` is re-exported at a different size or
crop, re-measure: longest contiguous alpha run ≥ 245 per edge.

## Regenerating `web/`

`sips` on this Mac reads WebP but cannot write it, so encode with PIL — the same
snippet as `../README.md`, at the widths below (q70).

```python
from PIL import Image
from pathlib import Path
W = {"card": 528, "sleeve-back": 600, "sleeve-front": 572}
d = Path("design-elements/brand/keycard")
(d / "web").mkdir(exist_ok=True)
for p in sorted(d.glob("*.png")):
    w = W["card"] if p.stem.startswith("card") else W[p.stem]
    im = Image.open(p).convert("RGBA")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(d / "web" / f"{p.stem}.webp", "WEBP", quality=70, method=6)
```
