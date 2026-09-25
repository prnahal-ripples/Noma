# RULES — Motion

> Canonical values: `src/tokens/motion.tokens.js`. Decision: ADR-005 (resolves O-7).
> NOMA's motion is playful and springy on discrete moments, still on ambient ones.

## Gates (all greppable)

1. **Tokens only.** UI code never contains a raw duration or bezier.
   Grep: `cubic-bezier(` and `[0-9]ms` must only match `src/tokens/motion.tokens.js`
   (or the CSS custom properties generated from it).
2. **Reduced motion is mandatory.** Every file that animates must contain
   `prefers-reduced-motion`. No exceptions — this is an accessibility gate.
3. **Exits never bounce.** Anything leaving the screen uses `easings.exit`.
   Grep: no `spring` easing on a `close|dismiss|exit|leave` transition.
4. **Ambient never springs.** Live readings, charts, monitoring surfaces use
   `standard` at most, scale capped at `scale.breathe` (1.02).
5. **Alarm never bounces.** If a surface signals something wrong, it does not play.
6. **Every new pattern starts from `templates/motion-pattern.md`** and is
   registered in `memory/motion/patterns.md` (CLAUDE.md rule 5).
