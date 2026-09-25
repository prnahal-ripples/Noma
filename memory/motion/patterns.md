# Motion Patterns — registry

> Tokens: `src/tokens/motion.tokens.js`. Philosophy: `memory/motion/philosophy.md`.
> New patterns start from `templates/motion-pattern.md` (CLAUDE.md rule 5).

| ID | Pattern | Recipe (tokens only) | Used on |
|---|---|---|---|
| MO-PRESS | Press & release | scale → `press` over `fast`/`standard`; release back with `spring` | every tappable |
| MO-POP | Arrival pop | opacity 0→1, translateY `rise`→0, scale 0.97→`pop`→1, `spring` at `gentle` | cards, receipts, chat bubbles |
| MO-STAGGER | List entrance | MO-POP per child, delay = index × `stagger.list` | room tiles, automations, chat |
| MO-SHEET | Sheet rise | translateY `sheet`→0 with `springBold` at `sheet`; scrim opacity at `base`; exit with `exit` at `base` | rehearse, create, settings, AI overlay |
| MO-KNOB | Toggle/segment thumb | position/scale with `spring` at `fast` | switches, autonomy segments, mode picker |
| MO-TOAST | Toast | rise + `springBold` in, `exit` out after hold | confirmations |
| MO-PULSE | Count change | scale 1→`pop`→1 at `fast` | badges (Needs your call · 1) |
| MO-BREATHE | Ambient breathing | scale 1→`breathe`→1, opacity ±0.15, `ambient` loop, `standard` | purifier ripples only |
| MO-GYRO | Surface catches light | rotateX/Y to `gyro.maxTiltDeg`, damped by `gyro.follow` per frame; iridescent speckle patch tracks the deflection; **no easing, no spring; nothing at rest** | the key card — first run nodes 4, 5, 4a ONLY |

Every pattern collapses under `prefers-reduced-motion` — MO-BREATHE stops entirely,
and MO-GYRO drops to a still surface (no tilt, no bloom, foil held at `restOpacity`).

---

## MO-GYRO — a surface that catches light

**Added 2026-08-19** on owner instruction: the key card should move with the
phone's gyroscope and carry a glittery, refractive, rainbowing, blooming foil
that catches light at different angles and at the corner edges.

**Tokens.** `motion.tokens.js` → `gyro` (maxTiltDeg 9, follow 0.14, sheenTravel
0.42, glitterTravel 0.4, deadzoneDeg 1.5). Visual layers:
`design.tokens.js` → `recipes.cardShimmer`.

**⚠ IT NEVER SPRINGS, and that is this file's rule 4 rather than a preference.**
Ambient motion uses `standard` at most. A gyro response is steered continuously
by the hand holding the device, so overshoot would read as looseness, not as
play. `gyro.follow` is a per-frame approach to the target — damping for sensor
jitter — not an easing curve.

**Two drivers, one visual path.** The phone uses `deviceorientation`; desktop
uses pointer position across the phone, added purely so the effect can be
reviewed on a laptop. Both write the same three custom properties
(`--gx`, `--gy`, `--gi`), so the desktop preview cannot drift from the real
thing.

**The first reading is the neutral.** `beta`/`gamma` are absolute and nobody
holds a phone at zero, so the first sample is captured as the rest pose and
everything after is a delta. Assuming a posture leaves the card permanently
deflected for anyone lying down.

**iOS needs a grant, from a gesture.** `DeviceOrientationEvent.requestPermission()`
is asked once on the first tap inside the phone, and never re-prompted.

**⚠ Do not give the surface a competing `transform`.** A filled CSS animation
outranks every normal declaration, so the page transition's `pgin` (`fill:both`)
pinned the card's transform and the tilt silently never applied at any
specificity. Elements running MO-GYRO are excluded from `pgin` — which is also
the truer behaviour, since the same card appears on four consecutive screens and
should stand still while the content around it moves.

**⚠ Blend modes are measured, not chosen.** On a near-white surface every
light-adding mode (screen, color-dodge, overlay, hard-light, soft-light) is a
no-op — verified side by side against the real artwork. Only `multiply` tints
white. On a dark surface this inverts.

**⚠ REVISED 2026-08-19, same day, after the owner saw it.** The first build was
rejected as "too much": a smooth rainbow wash over the whole PNG, permanently
on, glowing outside the card. Four things were wrong and all four are worth
keeping written down:

1. **It is a SPECKLE, not a wash.** From the reference: *"only a shimmer which
   is kind of a dotted visual pattern"* — a rainbow gradient seen through a dot
   grid, intersected with a soft patch the tilt drags. The dots are the effect;
   the gradient only colours them. Saturated hues are fine here precisely
   because they are only visible through ~12% of the area; the same colours as
   a flat wash read as a sticker.
2. **Nothing at rest.** Opacity is purely a function of deflection, from zero.
   The first build held it at 0.22 permanently, which is exactly what "it is
   static" meant.
3. **Clipped to the artwork's FACE, not its box.** `key-card.webp` is an outer
   translucent TRAY with the real card face inset inside it. `inset:0` spilled
   the shimmer across the tray and its corner followed nothing. The face
   geometry in `recipes.cardShimmer.face` is measured off the alpha channel.
4. **No outer bloom.** A `drop-shadow` glow lit the area *outside* the card,
   which was the other half of "it's going way out".

**⚠ Nodes 4, 5 and 4a only.** Not the celebration screen, not the door. The
owner named the screens; `data-tilt` is only emitted there.

**⚠ The rAF loop is generation-counted, not boolean-guarded.** The first version
used `on:true` and died after ONE navigation: `clearTimers()` cancels every
handle in `rafs` on each screen change, and the guard then refused to restart
it — so the shimmer worked on the first card screen and silently never again.
It also pushed a handle every frame, growing `rafs` at 60/sec. One clean loop
per screen, superseded by bumping `TILT.gen`.
