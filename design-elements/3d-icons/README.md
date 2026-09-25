# 3D icons — tier 1 of the two-tier icon system

Owner-supplied, 2026-08-14. Assets are in place and rendering as L2 page
headers across the app. Canonical registry: [`manifest.json`](./manifest.json).

## The two-tier system this belongs to

Raised in conversation on 2026-08-13 when auditing what the app needs icons
for, and now a real, running folder:

- **Tier 1 — 3D icons (this folder).** Rendered objects, soft studio
  lighting, transparent background. Reserved for higher-importance,
  higher-visibility moments — the things a person recognizes as an object
  or a primary destination, not a row in a list. Used **sparingly**: one per
  L2 inner page, at the top, as the page header. Never a row icon, never
  decoration.
- **Tier 2 — flat icons.** Monoline SVG, already live in code:
  [`docs/features/settings/_kit.py`](../../docs/features/settings/_kit.py)'s
  `ICONS` dict (22 icons — back, chevron, home, people, bell, palette, globe,
  shield, and the rest) and the equivalent set in
  [`build-onboarding.py`](../../docs/features/first-run/build-onboarding.py).
  Dense settings rows, chrome, anything scanned rather than looked at.

⚠ **This folder's four original names override an earlier draft split.**
When the tiers were first proposed, `notifications` and `appearance` were
suggested as tier-2 flat (they're settings rows — `bell` and `palette`
already exist as flat icons for exactly this). The owner's 2026-08-14
direction promotes both to tier 1 alongside `info` and `family`. **Where a
flat and a 3D icon now both exist for the same row (`bell`/`notifications`,
`palette`/`appearance`), which one ships is still an open call** — see
`manifest.json`'s `conflict` fields.

## The six icons

Five are real renders; one is a placeholder awaiting artwork.

| Name | File | What it shows | Status |
|---|---|---|---|
| **Info** | `info.png` | Brushed-steel bezel, lowercase *i* | Real |
| **Appearance** | `appearance.png` | Wooden painter's palette, loaded brush and knife | Real ⚠ palette conflict |
| **Notifications** | `notifications.png` | White rounded tile, red "1" badge | Real ⚠ palette conflict |
| **Family** | `family.png` | Three figures walking, holding hands | Real |
| **Rooms** | `rooms.png` | Isometric diorama room — armchair, floor lamp, side table, window | Real |
| **Filter** | `filter.png` (not yet supplied) | — | Placeholder |

Source PNGs are 800×1000, transparent background. Each has a `web/*.webp`
derivative at 288px (~11–23 KB, about a tenth of the PNG) built for embedding
as a base64 data URI — the same reason the fonts are embedded in the
prototypes: a single portable file, no external requests, no relative-path
mismatches across the three different depths these are viewed from (disk,
local server, Vercel).

To regenerate a `web/*.webp` after replacing a source PNG:

```bash
python3 - <<'PY'
from PIL import Image
import pathlib
src = pathlib.Path("design-elements/3d-icons")
for name in ["info", "appearance", "notifications", "family", "rooms", "filter"]:
    p = src / f"{name}.png"
    if not p.exists():
        continue
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    side = max(im.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    square = square.resize((288, 288), Image.LANCZOS)
    out = src / "web" / f"{name}.webp"
    square.save(out, "WEBP", quality=90)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
PY
```

## Where these render

- **Device settings** (`docs/features/settings/build-device-settings.py`):
  `info` on Device info, `filter` (placeholder) on Filter management.
- **Profile settings** (`docs/features/settings/build-profile-settings.py`):
  `family` on Family, `notifications` on Notifications, `appearance` on
  Appearance, `rooms` on Rooms & devices.

All six are built through one shared function,
[`page_header()` in `_kit.py`](../../docs/features/settings/_kit.py), so the
two settings surfaces render the pattern identically and can't drift. Icons
render at **62px** — `design.tokens.js`'s `layout.iconHeaderSize`, which
`_kit.py`'s `ICON_PX` and the Vercel dashboard both read rather than restate.
Taken down twice by the owner on 2026-08-14, 96 → 77 → 62, each a 0.8× step:
at 96 and again at 77 the render read too heavy against a 29px title. The
assets stay 288px, so even at 62 they are well over 3× and lose no
sharpness.

**A page can claim an icon that hasn't been drawn.** `icon3d()` falls back to
a flat, grey, dashed, name-labelled placeholder rather than failing the
build — deliberately not a plausible icon, so a stand-in can't quietly become
the design. Drop `filter.png` into this folder, run the resize snippet
above, and the real icon takes over with no code change — the same path
`rooms.png` took on 2026-08-14.

## Open questions, deliberately not resolved here

1. **Palette.** `appearance.png` and `notifications.png` carry real-world
   colours (paint reds/blues/yellows, a red notification badge) outside the
   2026-08-12 product palette rule (white, grey, the two greens only — LAW 2
   in `design.tokens.js`). That rule was written for the product's own
   surfaces; whether it also constrains a photographic/3D icon rendering a
   real object is an owner call, not something to assume either way. This is
   the reason **3D Icons still has no row** in
   [`.claude/rules/design-system.md`](../../.claude/rules/design-system.md)
   Approved Components, despite the assets existing and being verified —
   per that gate's own rule, a folder existing here is not the gate, a row
   there is.
2. **`filter` is undrawn.** That page ships today with a visibly placeholder
   icon rather than being blocked on artwork. (`rooms` was in the same state
   until 2026-08-14, when the owner supplied it.)
3. **Where each one actually ships, beyond settings.** The manifest's
   `usedFor` fields are this folder's best reading of where each icon
   replaces or sits beside existing flat icons or CSS-drawn placeholders
   (the bottom-nav tabs and My Home's bell are both currently CSS shapes,
   not real icons). Confirm rather than assume before extending beyond
   settings.

This is also the first real content for the **"icon set" gate** that
[`.claude/rules/design-system.md`](../../.claude/rules/design-system.md) has
stubbed out since the file was created — populated, not yet closed.
