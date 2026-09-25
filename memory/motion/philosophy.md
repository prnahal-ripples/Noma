# Motion Philosophy

> Canonical values: `src/tokens/motion.tokens.js` — this file explains, that file wins.
> Decision record: ADR-005, which resolves O-7.

## The one-sentence rule

**Bounce means "something happened"; stillness means "everything is fine."**

NOMA is playful — springy, bouncy, a little quirky, the Airbnb register — but only
at *discrete* moments: the user tapped, something arrived, something confirmed.
Ambient surfaces (live AQI, monitoring, charts) are almost perfectly still. This
split is how owner-stated playfulness and the `ma` philosophy stop fighting:
the calm is the ground, the bounce is the event.

## Where the spring lives

| Moment | Treatment |
|---|---|
| Button/chip press | `scale.press` (0.96) at `fast`, release springs back |
| Card / list item arrives | rise `travel.rise` + `scale.pop`, `spring`, staggered `stagger.list` |
| Bottom sheet / AI overlay opens | rise from off-screen, `springBold` at `sheet` |
| Toggle, segment thumb | `spring` at `fast` — the knob genuinely bounces |
| Toast | pops up with `springBold`, leaves with `exit` |
| Count/badge change | brief `scale.pop` pulse |

## Where it never lives

- **Exits.** Everything leaves fast and straight (`exit`). Overshoot on the way
  out reads as broken, not playful.
- **Ambient.** Breathing ripples run at `ambient` (4s) with scale ≤ `breathe`
  (1.02). A live number never bounces because it changed.
- **Alarm.** If something is wrong, motion gets out of the way entirely.

## Accessibility

`prefers-reduced-motion` support is mandatory on every animation — the gate in
`.claude/rules/motion.md` is unconditional. Reduced mode collapses durations to
near-zero; state changes remain visible, choreography disappears.
