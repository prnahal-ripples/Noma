# Brand — the NOMA wordmark

Owner-supplied, 2026-08-17. One asset: the real wordmark, replacing the
letter-spaced CSS text that stood in for it in every prototype until now.
Canonical registry: [`manifest.json`](./manifest.json).

## What this is, and what it isn't

This is a **static brand asset**, not a component and not an icon in the
sense `design-elements/3d-icons/` uses that word — it is one fixed mark, not
a set with usage rules per screen. It lives here anyway because
`design-elements/` is the closest existing home for "a real design asset
skinned into the product," and because a wordmark benefits from the exact
same discipline the icons do: one canonical source, a registered crop, a web
derivative, and a manifest saying where it's used so a future change doesn't
have to be rediscovered by grep.

⚠ **Neither of this repo's two icon/component gates quite fits a wordmark.**
`.claude/rules/design-system.md` has "Approved components" (interactive UI)
and a separate "Icon set" section (tier-1/tier-2 glyphs) — a brand mark is
neither. Flagged here rather than forced into either: an owner call on
whether this needs its own gate, or whether "Approved components" should
just widen to cover brand assets, same shape as the open call the icon set
entry already carries.

## The asset

| File | What it is | Size | Bytes |
|---|---|---|---|
| `noma-wordmark.png` | Source crop, transparent | 1189×308 | 48.8 KB |
| `web/noma-wordmark.webp` | Web derivative for embedding | 640×166 | 13.5 KB |

**Where it came from.** The owner pasted the mark into chat. No available
tool extracts a pasted image's raw bytes to disk — the same gap logged
against the 3D icons on 2026-08-14 — so it was located instead at the file
already saved on this machine, `~/Downloads/Noma/Noma Logo 2.png`
(1500×1500, transparent), verified pixel-identical to what was pasted before
use. A second file arrived alongside it, `~/Downloads/Noma Logo.png`
(14000×8000, flattened to white, no alpha) — same mark, no transparency,
print-resolution rather than a UI asset, and **not** the one checked in here.

**The crop.** The source canvas is mostly empty transparent space; the mark
itself occupies a 1061×192 region near vertical centre. Cropped to that
content box plus 6% horizontal padding and 30% vertical padding — a
wordmark wants air around its x-height, a tight box makes it look clipped
the moment it sits inside anything with its own padding (a sheet, a header).

**The web derivative.** Same convention as `design-elements/3d-icons/`: a
WebP under `web/`, sized for embedding as a base64 data URI so a prototype
stays one portable file with no relative-path assumptions across the three
depths these get viewed from (disk, a local server, Vercel). 640px wide is
roughly 6-9x the largest size it currently renders at (96px), which keeps it
crisp on a retina display without the source PNG's byte cost.

## Where it renders

Both current placements are in
[`docs/features/first-run/build-auth.py`](../../docs/features/first-run/build-auth.py)
→ `auth-prototype.html`, replacing the letter-spaced `NOMA` CSS text that
stood in for the mark in both spots before 2026-08-17:

- **Splash (`S0`)** — full-bleed image, mark near the foot, 96px wide.
- **Login sheet (`A1`)** — small, above the "A calmer kind of smart home"
  tagline, 72px wide.

⚠ **Not yet swapped everywhere the app shows the word "NOMA."** The older
45-screen flow (`first-run-prototype.html` / `first-run-flow.html`, built
from `build-prototype.py`) has its own node-1 "door" screen with the
wordmark rendered as choreographed CSS text, tuned in detail over several
owner passes (see `memory/session-handoff.md`, 2026-08-06 entries — light
from behind the door, the white dissolve, etc.). That screen was left alone:
it's a heavily-tuned, separately-built surface outside today's scope, and
swapping in an image there is a real edit to that choreography, not a
drop-in. Flagged for an owner call, not done silently.

## To replace the mark

1. Drop the new source file at `noma-wordmark.png` in this folder (any
   reasonable resolution; transparent background if the mark should sit on
   the sheet's gradient rather than a white box).
2. Re-run the encode snippet below to regenerate the WebP derivative.
3. Re-run `python3 docs/features/first-run/build-auth.py` — it reads this
   folder at build time and re-embeds automatically. No code change needed
   unless the new mark's aspect ratio is drastically different, in which
   case check the `width`/`aspect-ratio` pair on `.mark img` in the CSS.

```bash
python3 - <<'PY'
from PIL import Image
src = Image.open("design-elements/brand/noma-wordmark.png").convert("RGBA")
web_w = 640
web = src.resize((web_w, round(web_w / src.width * src.height)), Image.LANCZOS)
web.save("design-elements/brand/web/noma-wordmark.webp", "WEBP", quality=92)
PY
```

## The master key card — 2026-08-17

`key-card.png` (+ `web/key-card.webp`). Owner-supplied artwork for node 4's
Setup profile screen, where the card is both the profile and the key to the
home: *"without this key, you cannot access your home."*

**Used as the base, written over.** The bevel, the grain, the rule and the key
glyph are all in the image and nothing in code redraws them. Exactly four
things sit on top, and all four are live — bound to the two fields underneath:

| On the card | Comes from |
|---|---|
| Avatar | initials of the first two words of the name, or a picture off disk |
| Serif initial, top right | first letter of the name |
| Name | the NAME field |
| Email | the EMAIL field |

Positions are **percentages of the card**, measured off the owner's frame, so
the whole thing scales as one object.

⚠ **The web derivative is q72, not the q92 used elsewhere.** The artwork is a
soft gradient plus film grain, and grain is the most expensive thing a lossy
codec can encode: q92 came to 388 KB for something that renders at 244pt.
138 KB is still ~2.6× the rendered size and shows no artefacts at 1×.

## Instrument Serif — one glyph only

`src/fonts/instrument-serif/InstrumentSerif-Regular.ttf` (SIL OFL, licence
vendored beside it). Loaded for **exactly one character**: the initial on the
key card. It is not a second body face and must not become one — every other
character in the product is Google Sans Flex. If a second serif use appears,
that is a type-system decision and belongs in ADR-001, not in a screen.
