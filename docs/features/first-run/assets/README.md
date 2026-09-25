# First-run assets

## The sign-in background

`auth-prototype.html` opens on a full-bleed image with the sheet floating over
it. **This is the real photo now** — `first-run-bg.jpg`, owner-supplied
2026-08-17: a minimalist pitched-roof house, foggy sky, a lit doorway, and a
reflecting pool the roofline mirrors in. `bg_plate()` in `build-auth.py` —
which draws the earlier reference's composition (arch, stair flight, two soft
foreground crops) out of the neutral ramp — still exists as the **fallback**
if this file is ever moved or deleted, same convention as `icon3d()`'s
placeholder for a missing 3D icon. It is not what renders today.

**Where it came from.** Owner-supplied 2026-08-20, replacing the pitched-roof
house that had been here since 2026-08-17: a white minimal interior — curved
plaster wall, arched niches, a curved sofa, floor-to-ceiling glass with the
light blown out. Located on disk at `~/Downloads/Noma/Key Kard/New Noma BG.png`
(1200x2744, RGBA) rather than extracted from the paste, the same route logged
for the wordmark and the 3D icons.

Unlike the previous background this one carried **no alpha noise at all** (0
pixels under 250), so flattening was a formality rather than a repair. Resized
to 850px wide and re-encoded as progressive JPEG q82 — photographic content,
same convention as before.

| File | What it is | Size | Bytes |
|---|---|---|---|
| `first-run-bg.jpg` | The real background, flattened + re-encoded | 850x1944 | 73 KB |

**It now covers nodes 1-5, not just 1-3.** Nodes 4 and 5 (the profile sheet and
the mobile OTP) were built on the flat `--grad` canvas because that is what the
owner asked for at the time; on 2026-08-20 they asked for this image across
1-5. The data URI is declared ONCE, as `--aubg` on `.phone`, and read by both
`.au .bg__img` (nodes 1-3) and `.ovl--bare` (nodes 4-5) — a second copy would
add ~100KB and could drift.

⚠ **Nodes 4-5 carry no scrim, and 1-3 still do.** `.ovl__s` is 42% black; it
exists to make near-black type readable over a busy image, and these two
screens put an opaque sheet over the photo instead. With a background this
bright the scrim on 1-3 now reads much heavier than it did against the darker
house photo — the splash and login sheet render noticeably grey next to the
source image. **That is an owner call, not a bug**, and it is one declaration
to change.

**To replace it again****To replace it again**, drop a file here with one of these names and re-run
the build — first match wins:

    first-run-bg.jpg      (checked first)
    first-run-bg.png
    first-run-bg.webp

```bash
python3 docs/features/first-run/build-auth.py
```

The build embeds it as a data URI so the prototype stays one portable file,
and prints which background it used — the real photo or the drawn fallback.
No code change is needed, and nothing in the layout moves.

**What the image has to do.** The sheet covers the bottom 40–55% depending on
which state is showing, and the wordmark sits about 104pt off the bottom on
the splash. So everything that has to be seen lives in the **top 45%**, and
the lower half has to stay quiet enough for near-black type to sit on it.
Greyscale or near-greyscale: the palette rule (two greens and shades of them,
LAW 6's 10% budget) applies to photography too, and a warm or coloured hero
would be the largest non-palette surface in the product. The current photo's
one warm note — the lit doorway — sits inside the top 45% and stays small
enough not to trip that budget; watch this on any replacement.

**It becomes a video later** (owner, 2026-08-17). Nothing in the layout
depends on the image being still, so a `<video>` swapped in at the same
position needs no other change — but it does need a poster frame, because the
sheet animates in at 480ms and a black first frame would read as a bug.
