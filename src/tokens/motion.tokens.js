// CANONICAL SOURCE OF TRUTH — motion tokens (durations, easings, stagger).
// memory/motion/philosophy.md is the human-readable mirror; this file wins.
//
// ADR-005 (2026-08-04) resolved O-7: NOMA's motion is PLAYFUL — springy,
// bouncy, Airbnb-like — but only on DISCRETE moments: something the user did,
// something that arrived, something that confirmed. Ambient surfaces (live
// AQI, charts, monitoring) stay almost perfectly still. Bounce means
// "something happened"; stillness means "everything is fine". That split is
// what lets playfulness coexist with the `ma` philosophy in vision.md.
//
// Hard rules (greppable gates in .claude/rules/motion.md):
//   - UI code never writes a raw millisecond value or bezier — tokens only.
//   - Exits NEVER bounce. Overshoot on the way out reads as broken.
//   - Alarm or critical surfaces never bounce.
//   - prefers-reduced-motion support is mandatory on every animation.

export const durations = {
  instant: 80, //   opacity-only: hovers, focus rings
  fast: 140, //     taps, toggles, chips, segment thumbs
  base: 240, //     card state changes, tab content swap
  gentle: 360, //   expanders, list entrances, meters filling
  sheet: 480, //    bottom sheets, full-screen overlays
  // THE FIRST IMPRESSION. Added 2026-08-17 (owner: the sign-in sheet "is too
  // fast… make it slower and more premium"). This is NOT a second `sheet`
  // value to reach for when a sheet feels quick — it is for the once-per-
  // install arrival that sets the tone for everything after it, and today
  // exactly one surface uses it (first run, splash -> login sheet). A routine
  // sheet opening at 880ms is sluggish, not premium; the difference is that
  // this one is the app introducing itself and the user has nothing else to
  // do yet. Pair with `easings.entrance`, never with springBold.
  entrance: 880,
  ambient: 4000, // breathing ripples and idle pulses — the ONLY long value
};

export const easings = {
  // settle without personality — ambient + layout shifts
  standard: "cubic-bezier(0.2, 0, 0, 1)",
  // leave fast, no bounce — every exit uses this
  exit: "cubic-bezier(0.4, 0, 1, 1)",
  // THE house spring — ~10% overshoot. Buttons, chips, toggles, cards.
  spring: "cubic-bezier(0.34, 1.56, 0.64, 1)",
  // bigger overshoot for hero arrivals — sheets, the AI overlay, toasts
  springBold: "cubic-bezier(0.22, 1.8, 0.36, 1)",

  /* THE FIRST IMPRESSION. Added 2026-08-17 alongside `durations.entrance`.
   * Near-instant departure, then a long decelerating tail and NO overshoot —
   * the thing arrives already slowing down, and settles rather than lands.
   *
   * ⚠ THIS IS THE ONE PLACE THE PRODUCT IS NOT SPRINGY, and that is a real
   * tension with ADR-005, which resolved O-7 in favour of playful overshoot
   * on discrete moments. Flagged, not smuggled: overshoot reads as *fun*, and
   * scaled up to an 880ms hero arrival it reads as *cheap* — a bounce that
   * big and that slow is a cartoon, not a welcome. ADR-005's rule still holds
   * everywhere it was written for (taps, toggles, chips, routine sheets); the
   * once-per-install opening is the exception it never considered.
   * TODO(owner): confirm, or send it back to springBold at 480ms. */
  entrance: "cubic-bezier(0.16, 1, 0.3, 1)",
};

/* ------------------------------------------------------------------ *
 * GYRO — a surface that catches light as the device turns.
 *
 * ⚠ CONTINUOUS, SO IT NEVER SPRINGS. rules/motion.md gate 4: anything
 * ambient uses `standard` at most. A gyro response is driven by the hand
 * holding the phone, not by a discrete event, so a spring would add
 * overshoot to a value the user is directly steering — it would feel loose
 * rather than playful. `follow` is a smoothing factor, not an easing: each
 * frame moves this fraction of the way to the target, which damps sensor
 * jitter without adding lag you can feel.
 *
 * `maxTiltDeg` is small on purpose. A card is a flat object lying on the
 * screen; past ~10 degrees it stops reading as light catching a surface and
 * starts reading as a 3D toy.
 *
 * See MO-GYRO in memory/motion/patterns.md.
 * ------------------------------------------------------------------ */
export const gyro = {
  maxTiltDeg: 9, //     rotation at full deflection, both axes
  follow: 0.14, //      per-frame approach to target. 1 = instant (jittery)
  sheenTravel: 0.42, // how far the specular band slides, as a fraction of the
  //                    surface. Larger than the tilt because a highlight moves
  //                    much further than the object when the object turns.
  glitterTravel: 0.4, //the sparkle field's parallax against the sheen
  deadzoneDeg: 1.5, //  ignore below this, or a resting phone shimmers forever
};

export const stagger = {
  list: 45, // ms between siblings entering a list
  grid: 60, // ms between tiles entering a grid
};

export const scale = {
  press: 0.96, //   active/pressed state
  pop: 1.04, //     the moment of arrival, before settling to 1
  breathe: 1.02, // ambient maximum — anything larger stops being calm
};

export const travel = {
  rise: 16, //      px — cards/chips enter from this far below
  sheet: "100%", // sheets enter from fully off-screen
};
