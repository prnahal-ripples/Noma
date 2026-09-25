// CANONICAL SOURCE OF TRUTH — design tokens.
// Markdown mirrors in memory/ must defer to this file.
//
// Reference: owner-supplied NOMA screens + Figma component gallery, 2026-08-11.
// Values marked [INSPECTOR] were read directly off the Figma inspector panels
// and are exact. Everything else is measured off the renders and is a best
// reading — those are marked [MEASURED].
//
// THE FIVE LAWS OF THIS SYSTEM. Break these and it stops looking like NOMA.
//
//   1. THE GROUND IS A GRADIENT. White at the top falling to warm sand dust.
//      Never a flat fill. Never grey. See gradients.canvas.
//
//   2. GREEN IS NEVER SOLID. There is no flat green fill in this language —
//      green only ever appears as a ramp, a blur, or a bloom. A flat green
//      hex in UI code is a bug. See the `green` block for the one narrow
//      exception (text glyphs, which cannot be ramped accessibly).
//      COROLLARY, added 2026-08-12 with the new palette: WHITE TEXT NEVER
//      GOES ON GREEN. Both anchors are light — lime measures 1.83:1 against
//      white, mint 1.99:1. Green surfaces carry NEAR-BLACK.
//
//   3. WHITE MEANS RAISED. Cards are white because they are lifted off the
//      ground. Selection is expressed by LIFT, not by colour — a selected
//      chip is a white raised pill, an unselected one is a sunken grey pill.
//
//   4. THE CTA IS INK. Primary action is near-black and fully round.
//      Green is never the button.
//
//   5. THE INSURANCE CARD IS NOT A PATTERN. It is a single bespoke object
//      (full green fill, gyroscope-reactive). It is deliberately NOT
//      generalised into a recipe. Do not build a second one.
//
//   6. THE 10% RULE. Green is budgeted, not sprinkled. On any screen it
//      should be findable in one glance and absent everywhere else —
//      roughly a tenth of the pixels, no more. The product is white, grey
//      and glossy; green is the thing that MOVES on top of that. If a
//      screen looks green, something that should have been neutral got
//      coloured in. This was dropped in an earlier revision and is
//      reinstated 2026-08-12 at the owner's direction.
//
// Typography is UNCHANGED — Google Sans Flex, same family, same scale.
// Two additive styles only (`metric`, `label`), both required by the
// reference components and both absent before.
//
// Units are density-independent points (pt on iOS, dp on Android, px on web).
// Light theme only for now; see ADR-001 for the dark-theme deferral.

/* ------------------------------------------------------------------ *
 * 1. PRIMITIVES — raw ramps. Do not reference these in UI code.
 *    Always go through the semantic layer in section 2.
 * ------------------------------------------------------------------ */

// Neutral ramp. Cool at the light end, warming as it darkens, so it sits
// happily on top of the sand-dust ground without going muddy.
export const neutral = {
  0: "#FFFFFF",
  25: "#FAFAF9",
  50: "#F8F8F8", // [INSPECTOR] icon-button fill
  100: "#F1F1EF",
  150: "#E8E8E5", // unselected chip fill
  200: "#DDDCD8", // effective bottom of the canvas gradient (post-veil)
  300: "#CCCAC4", // [INSPECTOR] canvas gradient dark stop — "warm sand dust"
  400: "#9E9E9C",
  500: "#767674",
  600: "#5A5A58",
  700: "#3A3A38",
  800: "#2E2E2C", // ink — CTA fill, transport controls
  900: "#0E0E0D",
};

/* Brand green — LAW 2: NEVER SOLID.
 *
 * These are GRADIENT STOPS, not fills. Referencing any of them as a flat
 * background is a bug. Green enters the UI only through `gradients.*` —
 * as a ramp (progress), a bloom (status marks, hero glow), or a blurred
 * wash (ambient state).
 *
 * THE ONE EXCEPTION: text and monoline glyphs. A gradient-clipped glyph
 * cannot hold a contrast ratio, so green TEXT uses the flat `onLight`
 * value below, darkened until it clears WCAG AA. Where the surface allows
 * a decorative treatment, prefer gradients.accentText instead.
 *
 * THE PALETTE — owner-supplied 2026-08-12. Two anchors and the neutral they
 * fade into. This replaces the #1D6B27→#3DBE4E ramp entirely.
 *
 * THIS IS AN INK-ON-GREEN SYSTEM. That is the single most important thing to
 * know about it, and it inverts what the previous ramp did. Both anchors are
 * LIGHT — measured with the shared relative-luminance formula:
 *
 *   lime #AECC2A + white  →  1.83:1  ✗✗ unreadable
 *   mint #6CCC7C + white  →  1.99:1  ✗✗ unreadable
 *   lime #AECC2A + ink    →  7.43:1  ✓ AAA
 *   mint #6CCC7C + ink    →  6.85:1  ✓ AA  (AAA at large sizes)
 *
 * So: WHITE TEXT NEVER GOES ON GREEN IN THIS SYSTEM. Not on a fill, not on a
 * ramp, not on the feature card, not anywhere. There is no darkened anchor
 * that rescues it, because darkening these hues far enough to hold white text
 * takes them out of the palette the owner set. Green surfaces carry NEAR-BLACK
 * text, which is also why they read as glossy rather than as flat colour
 * blocks — a light green with ink on it looks lit; a dark green with white on
 * it looks printed.
 *
 * `limeDeep` / `mintDeep` are shades of the two anchors, darkened only as far
 * as green TEXT on a light ground requires (a gradient-clipped glyph cannot
 * hold a ratio, so green type has to be flat):
 *   limeDeep #5E6F0D on canvas  →  5.04:1  ✓ AA
 *   mintDeep #27753A on canvas  →  5.13:1  ✓ AA
 */
export const green = {
  // The two anchors. NON-TEXT-BEARING surfaces, or ink-on-green surfaces.
  lime: "#AECC2A",
  mint: "#6CCC7C",

  // The neutral the washes fade into — the third swatch the owner supplied.
  haze: "#E9E8E5",

  // Shades of the anchors, dark enough to BE text on a light ground.
  limeDeep: "#5E6F0D",
  mintDeep: "#27753A",

  // Bloom source. Always low-alpha, behind or around a mark.
  glow: "rgba(108, 204, 124, 0.55)",
  glowSoft: "rgba(108, 204, 124, 0.20)",
};

/* NEGATIVE RED — owner-supplied 2026-08-13. THIS IS THE FIRST NON-GREEN HUE
 * IN THE PALETTE, and it exists for exactly one job: things that are wrong,
 * lost, or destructive. It is not a second accent. Do not decorate with it.
 *
 * ⚠ IT BEHAVES LIKE THE GREENS, WHICH IS THE THING PEOPLE WILL GET WRONG.
 * The supplied #F38E8E is LIGHT. Measured with the shared relative-luminance
 * formula, not eyeballed:
 *
 *   salmon #F38E8E under white text        →  2.32:1  ✗ FAILS
 *   salmon #F38E8E under NEAR-BLACK text   →  5.88:1  ✓ AA
 *   salmon #F38E8E AS TEXT on canvas       →  2.09:1  ✗ FAILS BADLY
 *
 * So the anchor carries ink, never white — same rule as lime and mint. And it
 * CANNOT be the colour of the words "Offline" or "Remove this home"; that is
 * what `salmonDeep` is for:
 *
 *   salmonDeep #A03B3B AS TEXT on canvas   →  5.95:1  ✓ AA with margin
 *   salmonDeep #A03B3B under white text    →  6.60:1  ✓ AA
 *   mid        #D65151 AS TEXT on canvas   →  3.67:1  ✗ fails AA body,
 *                                              passes AA Large only
 *
 * LAW 2 DOES NOT EXTEND HERE, and that is deliberate. "Green is never solid"
 * is a rule about the BRAND accent — green earns its ramp because it is
 * decoration carrying delight. A fault signal is the opposite: it has to be
 * unambiguous at a glance, and a gradient makes it prettier and weaker. So a
 * flat `salmon` fill is legal. There is intentionally no `negativeRamp`.
 */
export const red = {
  // THE ANCHOR. Owner-supplied. Non-text-bearing surfaces, or ink-on-red.
  salmon: "#F38E8E",

  // The shade dark enough to BE text on a light ground. Use this for every
  // negative label, glyph and destructive row — never `salmon`.
  salmonDeep: "#A03B3B",

  // Waypoint on the same ramp. Safe as a fill or a border; NOT safe as body
  // text (3.67:1). Kept because borders and 2px rules need something between
  // `light` and `salmonDeep`.
  mid: "#D65151",

  // Tints, for row highlights and washes.
  light: "#F8BEBE",
  haze: "#FCE8E8", //  the neutral the negative washes fade into

  // Bloom source. Always low-alpha, behind or around a mark.
  glow: "rgba(243, 142, 142, 0.55)",
  glowSoft: "rgba(243, 142, 142, 0.22)",
};

/* ------------------------------------------------------------------ *
 * 2. SEMANTIC COLOR — the only color tokens UI code may reference.
 * ------------------------------------------------------------------ */

export const colors = {
  surface: {
    // LAW 1: the ground is gradients.canvas. `canvas` is the flat fallback
    // for engines that cannot render one (print, email, some RN paths).
    canvas: "#F4F3F1",
    canvasTop: neutral[0], //     [INSPECTOR] gradient stop 0%
    canvasBottom: neutral[300], //[INSPECTOR] gradient stop 100%

    raised: neutral[0], //        LAW 3 — white == lifted. Cards, selected chips.
    control: neutral[50], //      [INSPECTOR] icon-button fill #F8F8F8
    sunken: neutral[150], //      unselected chips, inert tracks
    muted: "#B8B8B6", //          secondary transport control (stop button)
    inverse: neutral[800], //     LAW 4 — the CTA, dark pills, pause button
    scrim: "rgba(0, 0, 0, 0.48)",
  },

  border: {
    // [INSPECTOR] The icon button carries a 1px INSIDE stroke of pure white
    // over an #F8F8F8 fill. That bevel is what makes controls read as glass
    // rather than as flat discs. It is not decoration — keep it.
    bevel: neutral[0],
    subtle: "rgba(11, 11, 11, 0.05)",
    hairline: "rgba(11, 11, 11, 0.09)",
    strong: neutral[300],
    inverse: neutral[0],
  },

  text: {
    primary: neutral[800], //   headings + body. Near-black, never #000.
    secondary: neutral[500], // supporting copy, section labels
    tertiary: neutral[400], //  placeholders, helper text, unselected chips
    inverse: neutral[0], //     on `surface.inverse` — INK surfaces only
    onMedia: neutral[0],
    accent: green.mintDeep, //  green text — flat by necessity, see `green`
    onAccent: neutral[800], //  text ON a green surface. NEAR-BLACK, never white.
  },

  icon: {
    primary: neutral[800],
    secondary: neutral[500],
    tertiary: neutral[400],
    inverse: neutral[0],
    accent: green.mintDeep, // monoline glyphs (power symbol) — flat, see `green`
  },

  /* ----------------------------------------------------------------
   * ACCENT — the green. There is still no `accent.solid`: LAW 2 means
   * there is nothing for a flat green fill token to point at.
   *
   * THE 10% RULE IS BACK, AND IT IS A BUDGET AGAIN (LAW 6). Green should
   * be reachable in one glance and absent everywhere else. The ground is
   * white and grey; green is the thing that moves on top of it. If more
   * than roughly a tenth of a screen is green, something that should be
   * neutral has been coloured in.
   *
   *   ALLOWED   progress and fill ramps          gradients.accentRamp
   *             status marks with bloom          gradients.accentBloom
   *             ambient "all good" washes        gradients.limeWash / mintWash
   *             hero glow behind a device        gradients.accentHalo
   *             green text / glyphs              colors.text.accent
   *             ONE feature surface per screen   gradients.accentSurface
   *
   *   FORBIDDEN any flat green background, at any size
   *             green as a page or section ground
   *             green headings or green body copy
   *             WHITE TEXT ON GREEN — anywhere, at any size, on any stop
   *             a green primary button (the CTA is ink — LAW 4)
   *             a second full-green card (LAW 5)
   *             more than ~10% of a screen (LAW 6)
   * ---------------------------------------------------------------- */
  accent: {
    ramp: "gradients.accentRamp", //   pointer, not a value — see gradients
    bloom: "gradients.accentBloom",
    wash: "gradients.mintWash",
    onFill: neutral[800], //           NEAR-BLACK on green. Was white; white
    //                                 measures 1.8–2.0:1 on these anchors.
    text: green.mintDeep,
  },

  /* STATUS — partially resolved 2026-08-13. O-6 was open because every
   * reference supplied was happy-path green and green cannot carry "bad".
   * The owner has now supplied a red (see the `red` primitive), so NEGATIVE
   * is real. Warning is still missing and still blocks work — see below.
   *
   * Reach for `negative` when something is wrong, lost or destructive:
   * offline devices, failed pairing, expired filters, and the destructive row
   * at the bottom of a settings surface. Not for "attention" or "due soon" —
   * that is warning, and warning does not exist yet.
   */
  status: {
    negative: {
      // Flat, on purpose — see the LAW 2 note on the `red` primitive.
      fill: red.salmon, //          surfaces, chips, filled marks
      onFill: neutral[800], //      NEAR-BLACK on salmon (5.88:1). Never white.
      text: red.salmonDeep, //      the label/glyph colour (5.95:1 on canvas)
      border: red.mid, //           1–2px rules and outlines
      tint: red.haze, //            row highlight / background wash
      bloom: red.glowSoft, //       halo behind a negative mark
    },

    // TODO(owner): WARNING IS STILL MISSING AND STILL BLOCKS THINGS. "Filter
    // at 10%", "firmware out of date" and "AQI is climbing" are not faults —
    // they are nudges, and rendering them in `negative` red overstates them
    // while rendering them in green says the opposite. Amber/yellow has never
    // been supplied. O-6 is now HALF closed, not closed.
    warning: null,

    // Critical deliberately folds into `negative` rather than being a third
    // step. One red is enough until something needs to outrank it.
    critical: "status.negative",
  },
};

/* ------------------------------------------------------------------ *
 * 2b. GRADIENTS — a first-class layer in this system, not a garnish.
 *     Angles follow CSS convention (0deg = up, 180deg = down).
 *     Every entry carries `.css`; consumers that cannot render a gradient
 *     use the `fallback` noted beside it.
 * ------------------------------------------------------------------ */

export const gradients = {
  /* THE GROUND. [INSPECTOR] Two stacked fills in Figma:
   *   layer 1 (back)  linear 180deg  #FFFFFF 0%  →  #CCCAC4 100%
   *   layer 2 (front) #FFFFFF @ 34%
   * `css` below is the composite of both, pre-flattened for consumers that
   * only take one background. `layers` preserves the Figma structure for
   * anyone rebuilding it natively.
   * Fallback: colors.surface.canvas
   */
  canvas: {
    type: "linear",
    angle: 180,
    layers: [
      { fill: `linear-gradient(180deg, ${neutral[0]} 0%, ${neutral[300]} 100%)` },
      { fill: neutral[0], opacity: 0.34 },
    ],
    stops: [
      { color: "#FFFFFF", at: 0 },
      { color: "#FDFDFC", at: 38 },
      { color: neutral[200], at: 100 },
    ],
    css: `linear-gradient(180deg, #FFFFFF 0%, #FDFDFC 38%, ${neutral[200]} 100%)`,
  },

  // Optional brightening spot behind a hero object. Layer OVER canvas.
  canvasSpot: {
    type: "radial",
    css: `radial-gradient(120% 62% at 50% 16%, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0) 72%)`,
  },

  /* THE BOTTOM SHEET GROUND. [INSPECTOR] 2026-08-17, read directly off the
   * Figma layer panel for the sign-in sheet. Two stacked fills:
   *   layer 1 (back)  #F9F9F9 flat, 100%
   *   layer 2 (front) linear 180deg #FFFFFF 0% -> #CCCAC4 100%, at 24%
   * DELIBERATELY LIGHTER AND FLATTER THAN `canvas`. A sheet floating over a
   * photo reads as glass and wants to stay close to white; the page's own
   * ground gradient is tuned for sitting directly on the gradient itself and
   * reads too heavy layered on top of an image. Do not point a bottom sheet
   * at `canvas` after this — that was true before this token existed and is
   * why the sign-in sheet needed its own.
   * `css` is the flattened composite (24%-opacity layer pre-mixed onto the
   * #F9F9F9 base) for consumers that only take one background; `layers`
   * keeps the exact Figma structure for anyone rebuilding it natively. */
  sheet: {
    type: "linear",
    angle: 180,
    base: "#F9F9F9",
    layers: [
      { fill: `linear-gradient(180deg, #FFFFFF 0%, ${neutral[300]} 100%)`, opacity: 0.24 },
    ],
    stops: [
      { color: "#FAFAFA", at: 0 },
      { color: "#F4F4F3", at: 50 },
      { color: "#EEEEEC", at: 100 },
    ],
    css: `linear-gradient(180deg, #FAFAFA 0%, #F4F4F3 50%, #EEEEEC 100%)`,
  },

  // Ink CTA. Barely-there vertical lift so a 56pt pill doesn't read as a slab.
  // Fallback: colors.surface.inverse
  ink: {
    type: "linear",
    angle: 180,
    css: `linear-gradient(180deg, #3A3A38 0%, ${neutral[800]} 100%)`,
  },

  /* GREEN — the only legal way green enters a surface.
   *
   * THE THREE RAMPS the owner supplied on 2026-08-12, verbatim. Every green
   * gradient in the product is one of these three or derived from them.
   * All three run TOP-DOWN in the reference (180deg); the per-use angle is
   * noted where a surface needs a different one.
   *
   *   accentRamp  mint → lime      the signature. Both anchors, no neutral.
   *   limeWash    lime → haze      lime dissolving into the ground.
   *   mintWash    mint → haze      mint dissolving into the ground.
   *
   * The two washes are what makes this system read as glossy rather than
   * flat: a green that fades into the page has depth; a green that stops at
   * an edge is a colour block.
   */

  // THE SIGNATURE RAMP. mint → lime. Progress fills, feature surfaces, marks.
  // Carries NEAR-BLACK text only (colors.accent.onFill).
  accentRamp: {
    type: "linear",
    angle: 180,
    stops: [
      { color: green.mint, at: 0 },
      { color: green.lime, at: 100 },
    ],
    css: `linear-gradient(180deg, ${green.mint} 0%, ${green.lime} 100%)`,
    // Horizontal variant, for progress tracks that fill left-to-right.
    cssX: `linear-gradient(90deg, ${green.mint} 0%, ${green.lime} 100%)`,
  },

  // lime → haze. A lime surface dissolving into the ground.
  limeWash: {
    type: "linear",
    angle: 180,
    css: `linear-gradient(180deg, ${green.lime} 0%, ${green.haze} 100%)`,
  },

  // mint → haze. The quieter of the two washes.
  mintWash: {
    type: "linear",
    angle: 180,
    css: `linear-gradient(180deg, ${green.mint} 0%, ${green.haze} 100%)`,
  },

  // Status marks — a dot is a bloom, not a disc. Lime core, mint falloff.
  accentBloom: {
    type: "radial",
    css: `radial-gradient(circle at 40% 34%, ${green.lime} 0%, ${green.mint} 62%, ${green.mintDeep} 100%)`,
    // Pair with this outer halo on the same mark for the bloom to read.
    halo: `0 0 8px 2px ${green.glowSoft}`,
  },

  // Ambient "all good" wash — a very blurred green bleeding out of a corner.
  // Used behind live readings. Never sharp, never edge-to-edge.
  accentWash: {
    type: "radial",
    css: `radial-gradient(140% 90% at 6% 0%, ${green.glow} 0%, ${green.glowSoft} 34%, rgba(108,204,124,0) 68%)`,
    blur: 32, // pt of blur to apply if the engine supports it
  },

  // Hero halo — the diffuse glow behind a running device.
  accentHalo: {
    type: "radial",
    css: `radial-gradient(closest-side, ${green.glowSoft} 0%, rgba(108,204,124,0) 74%)`,
    blur: 48,
  },

  /* GLOSS — not a colour, a finish. A hairline of white along the top edge of
   * a raised surface. This is most of what separates "glossy" from
   * "editorial": the same card with and without it reads as an object versus
   * a rectangle. Apply as an inset shadow on top of the real elevation. */
  gloss: {
    css: `inset 0 1px 0 rgba(255,255,255,0.9)`,
    onGreen: `inset 0 1px 0 rgba(255,255,255,0.55)`,
  },

  // For background-clip:text on a large numeric readout. DECORATIVE ONLY —
  // never on body copy, and never where the value must be read to be safe.
  // Accessible fallback: colors.text.accent
  // Runs between the two DEEP shades, not the anchors — clipped to a glyph,
  // lime and mint are far too light to read on a white ground.
  accentText: {
    type: "linear",
    angle: 135,
    css: `linear-gradient(135deg, ${green.mintDeep} 0%, ${green.limeDeep} 100%)`,
  },
};

/* ------------------------------------------------------------------ *
 * 3. RADIUS
 * ------------------------------------------------------------------ */

export const radius = {
  none: 0,
  xs: 8, //    chiclets — small selectable chips [INSPECTOR — 8/8/8/8]
  //           ⚠ was 10 (progress segments). The progress track is a full pill
  //           now, so nothing else wants 10 and the step is reused.
  sm: 12, //   selection-list rows, device thumbnails [INSPECTOR — 12/12/12/12]
  md: 16, //   nested blocks inside a card
  lg: 20, //   text inputs [MEASURED]
  xl: 24, //   DEFAULT card radius [INSPECTOR — 24/24/24/24]
  xxl: 28, //  the insurance card
  /* LARGE SURFACES ONLY [OWNER FIGMA 2026-08-19 — inspector read 34/34/34/34].
   * Bottom sheets, permission dialogs, and cards big enough to read as a
   * surface rather than an object. ⚠ It is NOT the next stop on the ramp and
   * nothing small may take it: a 34 corner on a list row eats the row. The
   * boundary is written down once, in `recipes.largeSurface`. */
  xxxl: 34,
  full: 999, // pills, chips, CTA, circular controls, avatars

  /* CORNER SMOOTHING — owner 2026-08-18 "very high, like iOS"; raised to the
   * full iOS value 2026-08-19: "we are gonna go hundred percent corner
   * smoothing to give it a more polished vibe."
   *
   * NO LONGER JUST AN INTENT. Until 2026-08-19 this token was documentation
   * only, because a CSS `border-radius` corner is a circular arc and a
   * smoothed corner is a superellipse. `docs/_squircle.py` now emits Figma's
   * own corner geometry as a 9-slice mask, so the prototypes render the real
   * shape at any element size with no script. Where it must be right:
   *   SwiftUI  RoundedRectangle(cornerRadius: r, style: .continuous)
   *   Figma    corner smoothing 100%
   *   CSS      docs/_squircle.py — mask-border, NOT border-radius
   * ⚠ `border-radius` remains on the same elements, but only so the shadow
   * (which a mask would clip away) has a shape to be cast from. */
  smoothing: 1.0,
};

/* ------------------------------------------------------------------ *
 * 4. ELEVATION — the Figma panels confirm "Drop shadow" on cards and on
 *    icon buttons but do not expose the values, so these are [MEASURED]:
 *    wide, faint, low-contrast. Their whole job is to separate a white
 *    card from a near-white ground, which takes spread, not darkness.
 * ------------------------------------------------------------------ */

const shadow = (layers) => ({
  layers,
  css: layers.length
    ? layers
        .map((l) => `${l.x}px ${l.y}px ${l.blur}px ${l.spread || 0}px ${l.color}`)
        .join(", ")
    : "none",
});

export const elevation = {
  none: shadow([]),

  // Circular icon buttons and small pills. Pair with border.bevel.
  control: shadow([
    { x: 0, y: 1, blur: 3, color: "rgba(0, 0, 0, 0.04)" },
    { x: 0, y: 5, blur: 14, color: "rgba(0, 0, 0, 0.07)" },
  ]),

  // DEFAULT card lift. [INSPECTOR confirms presence, values MEASURED.]
  card: shadow([
    { x: 0, y: 2, blur: 8, color: "rgba(0, 0, 0, 0.03)" },
    { x: 0, y: 12, blur: 32, color: "rgba(0, 0, 0, 0.06)" },
  ]),

  // The bottom-docked CTA — sits above scrolling content, needs to detach.
  dock: shadow([
    { x: 0, y: 4, blur: 12, color: "rgba(0, 0, 0, 0.06)" },
    { x: 0, y: 14, blur: 34, color: "rgba(0, 0, 0, 0.12)" },
  ]),

  floating: shadow([
    { x: 0, y: 4, blur: 12, color: "rgba(0, 0, 0, 0.05)" },
    { x: 0, y: 20, blur: 48, color: "rgba(0, 0, 0, 0.10)" },
  ]),

  // Hero product render on the canvas — a contact shadow, not a card lift.
  object: shadow([{ x: 0, y: 18, blur: 40, color: "rgba(0, 0, 0, 0.10)" }]),

  onMedia: shadow([{ x: 0, y: 2, blur: 6, color: "rgba(0, 0, 0, 0.2)" }]),
};

/* ------------------------------------------------------------------ *
 * 4b. SHAPE DYNAMICS — the finish, 2026-08-12 [INSPECTOR].
 *
 * This is the thing that makes the small shapes in this product feel
 * moulded rather than drawn, and it is THREE layers that only work
 * together:
 *
 *   1. a white stroke on the INSIDE edge   — the lit top edge
 *   2. a soft drop shadow underneath       — lifts it off the ground
 *   3. an inner shadow along the bottom    — gives it thickness
 *
 * Drop shadow alone reads flat and printed. Inner shadow alone reads
 * pressed-in. Stroke alone reads like an outline. All three is the
 * house style — every chip, chiclet, pill and small control gets it.
 *
 * ⚠ This is the single most copy-pasted thing in the system, so it lives
 * here as one string rather than being retyped per component. If a shape
 * looks flat next to its neighbours, it is missing `.css`.
 * ------------------------------------------------------------------ */

export const effects = {
  // Small selectable shapes: room chiclets, theme chips, text-size chips.
  // [INSPECTOR: fill #F8F8F8, stroke #FFFFFF inside 1, drop + inner shadow]
  chiclet: {
    strokeWidth: 1,
    strokeColor: neutral[0],
    fill: neutral[50], //  #F8F8F8
    css: [
      "0 1px 2px rgba(0,0,0,0.05)",
      "0 4px 10px rgba(0,0,0,0.055)",
      "inset 0 0 0 1px rgba(255,255,255,0.95)",
      "inset 0 -1.5px 2px rgba(0,0,0,0.05)",
      "inset 0 1.5px 1px rgba(255,255,255,0.9)",
    ].join(", "),
  },

  // The chosen chiclet — same finish, lifted further (LAW 3: selection is
  // lift, so the difference is shadow depth, never colour).
  chicletSelected: {
    strokeWidth: 1,
    strokeColor: neutral[0],
    fill: neutral[0],
    css: [
      "0 2px 4px rgba(0,0,0,0.05)",
      "0 8px 20px rgba(0,0,0,0.08)",
      "inset 0 0 0 1px rgba(255,255,255,1)",
      "inset 0 1.5px 1px rgba(255,255,255,1)",
    ].join(", "),
  },

  /* Tinted pill — the "Help" affordance.
   * [INSPECTOR: fill #8BCC6D @ 24%, stroke #FFFFFF inside 1.53,
   *  drop shadow + inner shadow]
   *
   * #8BCC6D sits between the two anchors (hue ~100°, lime is ~73°, mint
   * ~134°), so it is a legal shade of the family rather than a fourth
   * colour. At 24% it is a tint, not a fill — which is why the near-black
   * text rule does not bite: the label sits on what is effectively a very
   * pale green, and uses `green.mintDeep`. */
  tintPill: {
    strokeWidth: 1.53,
    strokeColor: neutral[0],
    tint: "#8BCC6D",
    tintOpacity: 0.24,
    fill: "rgba(139, 204, 109, 0.24)",
    css: [
      "0 1px 2px rgba(0,0,0,0.04)",
      "0 5px 14px rgba(0,0,0,0.07)",
      "inset 0 0 0 1.53px rgba(255,255,255,0.92)",
      "inset 0 -1.5px 2px rgba(0,0,0,0.04)",
    ].join(", "),
  },
};

/* ------------------------------------------------------------------ *
 * 5. SPACING — 4pt base, 8pt rhythm. Ramp unchanged.
 * ------------------------------------------------------------------ */

export const spacing = {
  s0: 0,
  s1: 4,
  s2: 8,
  s3: 12,
  s4: 16,
  s5: 20,
  s6: 24,
  s7: 32,
  s8: 40,
  s9: 48,
  s10: 64,
};

/* ---------------------------------------------------------------------------
 * RHYTHM — the vertical spacing grammar (owner, 2026-08-18).
 *
 * Two numbers do almost all of the work, and they are deliberately the s3/s6
 * stops of the existing 4pt ramp rather than new values:
 *
 *   textGap    12  between two pieces of the SAME text block —
 *                  eyebrow -> title, title -> body
 *   sectionGap 24  between BLOCKS — text block -> field, field -> next field
 *                  group, content -> CTA
 *   controlGap 12  between sibling controls in one group — field -> field,
 *                  chip row -> field
 *
 * Grounded, not guessed: Airbnb's login runs title->body at ~8-12 and
 * body->field / field->CTA at ~24-32; CRED's onboarding runs its caps
 * eyebrow -> title at ~12 and text band -> field zone at ~24-32 (Mobbin,
 * 2026-08-18). Anything tighter than 12 reads as one line wrapping; anything
 * between 12 and 24 reads as indecision. If a screen needs a third value it
 * is usually two sections pretending to be one.
 * ------------------------------------------------------------------------ */
export const rhythm = {
  textGap: spacing.s3, //     12 — eyebrow -> title [OWNER REDLINE]
  titleGap: 18, //            18 — title -> the first control under it.
  //                          ⚠ NOT a ramp stop. It is the one measured value
  //                          the 4pt ramp does not contain, and the redline is
  //                          explicit about it: 16 lets the title crowd the
  //                          button, 20 opens a gap the eye reads as a section
  //                          break. Kept as measured rather than rounded.
  sectionGap: spacing.s6, //  24 — block -> block, and the sheet's own padding
  controlGap: spacing.s2, //   8 — STACKED CONTROLS [OWNER REDLINE]. Was 12.
  //                          Two buttons 8 apart read as one group of choices;
  //                          at 12 they read as two unrelated things.
};


export const layout = {
  screenPaddingX: spacing.s5, //  20 [MEASURED — CTA and cards inset 20]
  cardPaddingX: spacing.s6, //    24 [INSPECTOR]
  cardPaddingY: spacing.s4, //    16 [INSPECTOR]
  cardGap: spacing.s5, //         20 [INSPECTOR — auto-layout gap]
  stackGap: spacing.s4, //        16 between sibling cards
  sectionGap: spacing.s7, //      32
  hairlineWidth: 1,
  bevelWidth: 1, //               [INSPECTOR] inside stroke on controls

  controlSize: 40, //             circular icon button [MEASURED]
  transportSize: 40, //           pause / stop discs [MEASURED]
  ctaHeight: 54, //               [OWNER REDLINE 2026-08-18] was 56
  ctaQuietHeight: 46, //          [OWNER REDLINE] a secondary/ghost button is
  //                              SHORTER than the primary, not merely paler —
  //                              the size difference is half the hierarchy.
  inputHeight: 52, //             [OWNER FIGMA 2026-08-18] was 56. Matches the
  //                              inspector: "333 Fill × 52". CRED and Airbnb
  //                              fields sit at 52-56; ours at the tight end.
  sheetPadX: 20, //               [OWNER REDLINE] the sheet's horizontal inset
  sheetPadY: 24, //               [OWNER REDLINE] top and bottom, = sectionGap
  otpBox: [56, 52], //            [OWNER REDLINE] w x h
  chipHeight: 40, //              [MEASURED]
  pillHeight: 34, //              status / "Read more" pill [MEASURED]

  // Tier-1 (3D) icon in an L2 page header. [OWNER 2026-08-14]
  // Taken down twice on the same day, both owner calls: 96 -> 77 -> 62,
  // each a 0.8x step. At 96 and again at 77 the render read as too heavy
  // against a 29px title. Assets stay 288px, so even at 62 this is well
  // over 3x and loses no sharpness.
  // Canonical: _kit.py and the Vercel dashboard both read this, neither
  // restates it.
  iconHeaderSize: 62,

  // Brand wordmark display width. [OWNER 2026-08-17] Two contexts, two
  // sizes: the splash (spacious, full-bleed image) sits larger than the
  // sheet header (compact, directly above the tagline). Height is never a
  // token — it follows from the asset's own aspect ratio
  // (design-elements/brand/manifest.json), so sizing the mark anywhere only
  // ever sets width. Canonical consumer: build-auth.py.
  wordmarkSplash: 116,
  /* [OWNER FIGMA 2026-08-19 — inspector: W 56, H 16, opacity 50%.] Was 84 at
   * full strength. The mark is a signature on the sheet, not its headline;
   * at 84 it competed with the 28 title directly under it. */
  wordmarkSheet: 56,
  wordmarkSheetOpacity: 0.5,
};

/* ------------------------------------------------------------------ *
 * 6. TYPOGRAPHY — Google Sans Flex (SIL OFL), ADR-001 O-2. Family, weights
 *    and existing scale are UNCHANGED. Assets: src/fonts/google-sans-flex/.
 *
 *    Two ADDITIONS, both required by the reference components and neither
 *    previously expressible: `metric` (the large AQI readout) and `label`
 *    (the uppercase "HOME NAME" / "STARTER ROOMS" section labels).
 *
 *    Variable axes: opsz (6-144), wght (1-1000), wdth, slnt, GRAD, ROND.
 *    Noma uses opsz + wght only. Prefer `font-optical-sizing: auto` on web;
 *    the `opsz` values below are the fallback for RN / Skia.
 *
 *    COVERAGE GAP: no Devanagari glyphs. Cannot be the sole family for the
 *    `hi` locale. Open as ADR-001 O-5.
 * ------------------------------------------------------------------ */

export const typography = {
  family: {
    sans: "'Google Sans Flex', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
    // TODO(owner): pick a Devanagari-covering pairing for the `hi` locale.
  },
  // Four weights, matching the dashboard's own "Only four weights are in the
  // token set" note. `black` (900) was listed here but used nowhere in
  // `scale` below — dead weight, and inconsistent with that documentation.
  // Semibold (600) is the heaviest named weight the token set actually uses.
  weight: { regular: 400, medium: 500, semibold: 600, bold: 700 },
  scale: {
    // NEW — the big numeric readout. Never wraps, never used as a heading.
    metric: { size: 72, lineHeight: 72, weight: 700, tracking: -2.4, opsz: 72 },

    /* [OWNER FIGMA 2026-08-19] 28 SemiBold, was 30 Bold. The inspector reads
     * SemiBold on the sheet's "A calmer kind of smart home." — dropping the
     * weight with the size is what keeps it from thickening as it shrinks. */
    display: { size: 28, lineHeight: 34, weight: 600, tracking: -0.6, opsz: 28 },
    title1: { size: 26, lineHeight: 31, weight: 700, tracking: -0.3, opsz: 26 },
    title2: { size: 22, lineHeight: 27, weight: 600, tracking: -0.2, opsz: 22 },
    title3: { size: 18, lineHeight: 23, weight: 600, tracking: -0.1, opsz: 18 },
    body: { size: 16, lineHeight: 22, weight: 400, tracking: 0, opsz: 16 },
    bodyStrong: { size: 16, lineHeight: 22, weight: 600, tracking: 0, opsz: 16 },
    caption: { size: 14, lineHeight: 19, weight: 400, tracking: 0, opsz: 14 },

    // NEW — uppercase section label. Always colors.text.secondary.
    label: {
      size: 12,
      lineHeight: 16,
      weight: 600,
      tracking: 0.96, // 0.08em
      opsz: 12,
      transform: "uppercase",
    },

    /* CONTROL LABELS [OWNER FIGMA 2026-08-19]. Button text is its own register
     * and is SMALLER than body: the control's height and fill already carry
     * the emphasis, so a 16 label inside a 54 pill reads shouty. The 14/12
     * split is the primary/secondary hierarchy said a second way, after
     * height and fill. */
    action: { size: 14, lineHeight: 18, weight: 600, tracking: 0, opsz: 14 },
    actionSmall: { size: 12, lineHeight: 16, weight: 600, tracking: 0, opsz: 12 },

    /* Terms and privacy under the CTA stack. "Mixed 10" in the inspector —
     * one 10pt run at regular weight with the two links at semibold, which is
     * why this carries a `linkWeight` rather than a second style. */
    legal: { size: 10, lineHeight: 15, weight: 400, tracking: 0, opsz: 10, linkWeight: 600 },

    micro: { size: 12, lineHeight: 16, weight: 500, tracking: 0.1, opsz: 12 },
  },
};

/* ------------------------------------------------------------------ *
 * 7. COMPONENT RECIPES — built from the supplied gallery. Composed from
 *    tokens above; no raw values.
 * ------------------------------------------------------------------ */

export const recipes = {
  /* --- ground ---------------------------------------------------- */

  // Every screen. LAW 1.
  screen: {
    background: gradients.canvas.css,
    backgroundFallback: colors.surface.canvas,
    paddingX: layout.screenPaddingX,
  },

  // The "Create your home" pattern: gradient ground, scrolling body,
  // CTA docked to the bottom edge with the same 20pt side inset.
  sheet: {
    background: gradients.canvas.css,
    backgroundFallback: colors.surface.canvas,
    paddingX: layout.screenPaddingX,
    borderTopRadius: radius.xxl,
    elevation: elevation.floating,
    ctaDock: {
      paddingX: layout.screenPaddingX,
      paddingBottom: spacing.s5,
      background: "transparent", // the CTA floats on the ground, no bar
    },
  },

  /* --- cards ----------------------------------------------------- */

  // THE card. [INSPECTOR] radius 24, #FFFFFF, padding 24/16, gap 20, no stroke.
  card: {
    background: colors.surface.raised,
    borderRadius: radius.xl,
    elevation: elevation.card,
    paddingX: layout.cardPaddingX,
    paddingY: layout.cardPaddingY,
    gap: layout.cardGap,
    borderWidth: 0,
  },

  // Same card with a live-state wash bleeding out of the top-left corner.
  // The wash is the ONLY green on a white card, and it is always blurred.
  cardLive: {
    background: colors.surface.raised,
    overlay: gradients.accentWash.css,
    overlayBlur: gradients.accentWash.blur,
    borderRadius: radius.xl,
    elevation: elevation.card,
    paddingX: layout.cardPaddingX,
    paddingY: layout.cardPaddingY,
    gap: layout.cardGap,
  },

  // Card whose lower half is a bleeding image ("Discover Clean Air").
  // Media is inset-clipped to the card radius; no inner radius of its own.
  cardMedia: {
    background: colors.surface.raised,
    borderRadius: radius.xl,
    elevation: elevation.card,
    paddingX: layout.cardPaddingX,
    paddingY: layout.cardPaddingY,
    clipContent: true,
    mediaBleed: "bottom",
  },

  // Dense/structured content (forms, checkout) — hairline instead of shadow.
  cardOutlined: {
    background: colors.surface.raised,
    borderRadius: radius.xl,
    borderWidth: layout.hairlineWidth,
    borderColor: colors.border.hairline,
    elevation: elevation.none,
    paddingX: layout.cardPaddingX,
    paddingY: layout.cardPaddingY,
  },

  /* Selection row — the "which one did you bring home?" pattern.
   * [INSPECTOR: radius 12, padding 16, gap 20, fill #FFFFFF, 1px INSIDE
   * white stroke, drop shadow.]
   *
   * The radius is tighter than a content card on purpose: a stack of these
   * is ONE single-choice control, and at 24 they stop reading as a list and
   * start reading as three unrelated surfaces.
   *
   * LAW 3, and this is the clearest case of it in the product: the chosen
   * row is LIFTED (white, bevel, shadow, chevron) and the others are flat
   * and muted. No accent colour, no tick, no coloured border — selection is
   * elevation. The chevron belongs only to the selected row, because it is
   * the only one that leads anywhere.
   */
  cardSelect: {
    background: colors.surface.raised,
    color: colors.text.primary,
    borderRadius: radius.sm, //  12 [INSPECTOR]
    padding: spacing.s4, //      16 [INSPECTOR]
    gap: spacing.s5, //          20 [INSPECTOR] — between rows in the stack
    borderWidth: layout.bevelWidth,
    borderColor: colors.border.bevel,
    elevation: elevation.card,
    thumbSize: 68,
    thumbRadius: radius.sm,
  },

  cardSelectIdle: {
    background: "transparent",
    color: colors.text.tertiary,
    borderRadius: radius.sm,
    padding: spacing.s4,
    borderWidth: layout.hairlineWidth,
    borderColor: colors.border.subtle,
    elevation: elevation.none,
  },

  /* Framed illustration — the onboarding hero.
   * [INSPECTOR: radius 24, linear-gradient fill, 8px INSIDE white stroke,
   * drop shadow.]
   *
   * The 8pt white frame IS the effect. At 1pt this is just a coloured
   * square; at 8 it reads as a printed tile resting on the ground, which is
   * what lets it carry a soft gradient without competing with the page.
   * Tilt it a couple of degrees for the same reason — square-on reads as a
   * banner, slightly turned reads as an object.
   */
  illustration: {
    size: 232,
    borderRadius: radius.xl, //  24 [INSPECTOR]
    frameWidth: 8, //            [INSPECTOR] inside stroke, white
    frameColor: neutral[0],
    elevation: elevation.floating,
    tiltDeg: -2,
  },

  /* --- buttons --------------------------------------------------- */

  // PRIMARY CTA. LAW 4 — ink, full radius, full width, docked.
  /* ⚠ HEIGHTS ARE THE HIERARCHY, not just colour (owner redline 2026-08-18):
   * primary 54, quiet 46, stacked 8 apart. A quiet button that matches the
   * primary's height reads as an equal choice no matter how pale it is. */
  buttonPrimary: {
    background: gradients.ink.css,
    backgroundFallback: colors.surface.inverse,
    color: colors.text.inverse,
    borderRadius: radius.full,
    height: layout.ctaHeight, // 54 [OWNER REDLINE]
    paddingX: spacing.s6,
    textStyle: "action", // 14/600 [OWNER FIGMA 2026-08-19] — was bodyStrong (16)
    elevation: elevation.dock,
    stackGap: rhythm.controlGap, // 8 when buttons stack
  },

  buttonSecondary: {
    background: colors.surface.raised,
    color: colors.text.primary,
    borderRadius: radius.full,
    borderWidth: layout.bevelWidth,
    borderColor: colors.border.bevel,
    height: layout.chipHeight,
    paddingX: spacing.s5,
    elevation: elevation.control,
  },

  /* "Not now" — the CTA's twin, stacked directly under it. SAME height and
   * radius so the pair reads as one control group; near-white instead of ink
   * so there is never a question which is the main path. Declining is a
   * first-class option in this product (every permission ask can be refused
   * and the flow continues), so it gets a real button, not a text link.
   */
  buttonQuiet: {
    background: colors.surface.raised,
    color: colors.text.primary,
    borderRadius: radius.full,
    height: layout.ctaQuietHeight, // 46 [OWNER REDLINE] — SHORTER than primary on purpose
    paddingX: spacing.s6,
    textStyle: "actionSmall", // 12/600 [OWNER FIGMA 2026-08-19]
    elevation: elevation.control,
  },

  // Circular icon button — back, settings.
  // [INSPECTOR] fill #F8F8F8 + 1px INSIDE stroke #FFFFFF + drop shadow.
  // The white inside stroke is what makes it read as glass. Keep it.
  buttonIcon: {
    background: colors.surface.control,
    color: colors.icon.primary,
    borderRadius: radius.full,
    size: layout.controlSize, // 40
    borderWidth: layout.bevelWidth,
    borderColor: colors.border.bevel,
    borderPosition: "inside",
    elevation: elevation.control,
  },

  // Transport controls. Pause is ink, stop is muted grey — a deliberate
  // hierarchy, not two peers.
  buttonTransport: {
    background: colors.surface.inverse,
    color: colors.icon.inverse,
    borderRadius: radius.full,
    size: layout.transportSize,
  },
  buttonTransportMuted: {
    background: colors.surface.muted,
    color: colors.icon.inverse,
    borderRadius: radius.full,
    size: layout.transportSize,
  },

  /* --- input ----------------------------------------------------- */

  // Typing bar. White raised field on the gradient ground, uppercase label
  // above it in `label` / text.secondary.
  /* REBUILT 2026-08-18 from the owner's Figma inspector: fill #FFFFFF, corner
   * radius 8, stroke #000000 at 12% inside at 1px, height 52, two inner
   * shadows. A text field is now a QUIETER shape than a card — less rounded,
   * hairline-bounded, sitting IN the surface rather than floating on it. The
   * CTA keeps its pill; the contrast between the two is the point.
   * Cross-checked against Airbnb (hairline ~r8-10 fields) and CRED (1px
   * stroke, near-square fields) via Mobbin, 2026-08-18. */
  input: {
    background: neutral[0], // #FFFFFF flat — no gradient on a field
    color: colors.text.primary,
    placeholderColor: colors.text.tertiary,
    borderRadius: radius.xs, // 8 [OWNER FIGMA] was radius.lg (20)
    height: layout.inputHeight, // 52
    paddingX: spacing.s4,
    borderWidth: 1, // [OWNER FIGMA] was 0 — the field is drawn, not lifted
    borderColor: "rgba(0, 0, 0, 0.12)", // stroke #000 @ 12%, inside
    // the two inner shadows from the inspector: a tight top press and a soft
    // lower wash, so the well reads as sunken without a visible drop shadow
    innerShadow:
      "inset 0 1px 2px rgba(0, 0, 0, 0.06), inset 0 2px 6px rgba(0, 0, 0, 0.03)",
    elevation: null, // was elevation.control — a sunken well casts nothing
    labelStyle: "label",
    labelColor: colors.text.secondary,
    labelGap: spacing.s2,
    focusBorderWidth: 1.5,
    focusBorderColor: colors.border.strong,
  },

  /* --- chips ----------------------------------------------------- */

  /* LAW 3. Selection here is LIFT, not colour. A selected chip is a white
   * raised pill with a bevel and a shadow; an unselected one is a flat
   * sunken grey pill with muted text and NO shadow. There is no green chip
   * and no dark chip in this pattern. Getting this backwards inverts the
   * whole screen's read. */
  /* Chiclets — room presets, theme, text size. Any small selectable shape.
   *
   * ⚠ RADIUS 8, NOT A PILL [INSPECTOR]. This is the correction the owner's
   * shape-dynamics sheet is most explicit about: these were fully rounded and
   * should not be. A pill reads as a filter or a tag — something you toggle
   * off again; a soft 8pt rectangle reads as a tile you are picking from a
   * set. Bigger shapes get rounder, small ones get tighter, which is the
   * opposite of what a single "make everything rounder" instruction would
   * produce and is why the two radii are specified separately.
   *
   * Both states carry the shape-dynamics finish (effects.chiclet). Selection
   * is still LIFT — the chosen one goes white and gains shadow depth; nothing
   * changes hue. */
  chipSelected: {
    background: effects.chicletSelected.fill,
    color: colors.text.primary,
    borderRadius: radius.xs, // 8 [INSPECTOR]
    height: layout.chipHeight, // 40
    paddingX: spacing.s4,
    effect: effects.chicletSelected.css,
    textStyle: "caption",
  },

  chipUnselected: {
    background: effects.chiclet.fill,
    color: colors.text.tertiary,
    borderRadius: radius.xs, // 8 [INSPECTOR]
    height: layout.chipHeight,
    paddingX: spacing.s4,
    effect: effects.chiclet.css,
    textStyle: "caption",
  },

  /* The "Help" affordance — a tinted pill, not bare green text.
   * [INSPECTOR: #8BCC6D @ 24%, white inside stroke 1.53, drop + inner shadow]
   * Bare coloured text has no touch target and no affordance; this gives it
   * both without spending a button on it. */
  buttonTint: {
    background: effects.tintPill.fill,
    color: green.mintDeep,
    borderRadius: radius.full,
    height: 38,
    paddingX: spacing.s4,
    effect: effects.tintPill.css,
    textStyle: "bodyStrong",
  },

  /* Toggle — chunkier and rounder than the platform default, per the
   * shape-dynamics sheet. The knob nearly fills the track height, which is
   * what makes it read as a moulded object rather than a switch graphic. */
  /* Retuned 2026-08-13 to the owner's Figma spec. [INSPECTOR: W 56, H 24,
   * corner radius 100, fill Linear.] Slimmer and proportionally wider than
   * before — 58×34 (1.7:1) became 56×24 (2.3:1).
   *
   * ⚠ BREAKING SHAPE CHANGE: `knob` (one number, implying a circle) is gone,
   * replaced by `knobW`/`knobH`. THE KNOB IS A PILL, NOT A SPHERE — that was
   * the explicit correction, and the owner's reference marks the circular
   * version with a red X. A knob whose width equals its height reads as a
   * platform default; a wider-than-tall knob is what makes this one ours.
   * Only docs/features/settings/_kit.py consumes these.
   */
  toggle: {
    width: 56, //     [INSPECTOR]
    height: 24, //    [INSPECTOR]
    knobW: 30, //     PILL — wider than tall. Not a circle.
    knobH: 18,
    knobInset: 3, //  (24 - 18) / 2 — so the knob is optically centred
    trackOff: colors.surface.sunken,
    trackOn: "gradients.accentRamp", // pointer — LAW 2, never a flat green
    knobColor: neutral[0],
    knobElevation: "0 2px 6px rgba(0,0,0,0.18)",
    radius: radius.full, // 999 on both track and knob — [INSPECTOR: 100]
  },

  /* Segmented control — a small set of mutually exclusive values sitting
   * inline on a settings row (Off / Low / High, °C / °F). A sunken track
   * with a raised white pill riding in it.
   *
   * LAW 3 again, and worth stating because the owner's source prototype does
   * the opposite: it fills the selected segment with ink and puts white text
   * on it. Ink is this system's ACTION colour — filling a segment with it
   * reads as "tapping this does something", when the control is only
   * reporting which value is current. Lift says "this is the one" without
   * implying a button.
   */
  segmented: {
    track: colors.surface.sunken,
    trackRadius: radius.full,
    trackPadding: 3,
    height: 32,
    optionRadius: radius.full,
    optionPaddingX: spacing.s3,
    color: colors.text.tertiary,
    selectedBackground: colors.surface.raised,
    selectedColor: colors.text.primary,
    selectedElevation: elevation.control,
  },

  chipGroup: {
    gap: spacing.s2,
    labelStyle: "label",
    labelColor: colors.text.secondary,
    labelGap: spacing.s3,
    helperStyle: "micro",
    helperColor: colors.text.tertiary,
    helperGap: spacing.s3,
  },

  /* --- pills & marks --------------------------------------------- */

  // Dark status pill — "Improving", "Read more". Ink fill, white label.
  // Its dot is a bloom (recipes.statusDot), never a flat disc.
  pillStatus: {
    background: colors.surface.inverse,
    color: colors.text.inverse,
    borderRadius: radius.full,
    height: layout.pillHeight, // 34
    paddingX: spacing.s3,
    gap: spacing.s2,
    textStyle: "micro",
  },

  pill: {
    background: colors.surface.raised,
    color: colors.text.primary,
    borderRadius: radius.full,
    height: layout.pillHeight,
    paddingX: spacing.s3,
    elevation: elevation.control,
  },

  // LAW 2 — even at 8pt, green is a bloom with a halo, not a solid dot.
  statusDot: {
    background: gradients.accentBloom.css,
    shadow: gradients.accentBloom.halo,
    size: 8,
    borderRadius: radius.full,
  },

  /* --- progress -------------------------------------------------- */

  // Segmented live progress. Discrete ticks; filled ticks carry the ramp
  // as ONE continuous gradient across the whole track, not per-segment.
  /* Segmented progress / filter life.
   *
   * ⚠ CORRECTED 2026-08-12 (owner). The previous revision wrapped this in a
   * white pill container and faked the segments with a repeating-gradient
   * MASK punched through one continuous bar — visually a squashed capsule
   * with rounded ends, not discrete shapes. That is exactly the "weird
   * shape pill" the owner's reference rules out.
   *
   * This is now what the reference actually shows: real INDIVIDUAL
   * rectangles, 2px corner radius, 4px gap between each one — no wrapping
   * pill, no mask trick. Each filled bar is its own element so it can carry
   * its own point on the mint→lime ramp; unfilled bars are flat
   * `trackEmpty`. Do not reintroduce a container radius here — the shape IS
   * the row of rectangles.
   */
  progressTrack: {
    segmentWidth: 4, //  [OWNER REFERENCE]
    segmentGap: 4, //    [OWNER REFERENCE] — "4px interdistance between each point"
    segmentRadius: 2, // [OWNER REFERENCE] — "2px rounded corners"
    heightSm: 14, //     inline, next to a row label
    heightLg: 20, //     standalone, in its own card

    fillFrom: green.mint, // filled bars interpolate mint → lime by position
    fillTo: green.lime,
    trackEmpty: colors.surface.sunken,

    endLabelStyle: "micro",
    endLabelColor: colors.text.secondary,
  },

  /* --- sheets ---------------------------------------------------- */

  // [INSPECTOR] 2026-08-17 — see gradients.sheet for the Figma source and why
  // this is lighter than the page's own `canvas` ground.
  /* ================================================================
   * LARGE SURFACES — the card design, from the owner's Figma inspector
   * on 2026-08-19. Four properties, one shape:
   *
   *     corner radius   34, all four, at 100% smoothing
   *     fill            #F9F9F9 with a white->neutral300 layer at 24%
   *     stroke          1px #FFFFFF, INSIDE
   *     effect          drop shadow (elevation.floating)
   *
   * ⚠ THE SCOPE IS THE POINT, and it is the owner's own line:
   *
   *     "this card design will only apply on larger cards, like bottom
   *      sheets or maybe bigger cards. It won't apply on smaller cards."
   *
   * A surface is LARGE when it is a ground that other things sit on — a
   * bottom sheet, a permission dialog, a card that fills most of the
   * width. Those take this recipe. A row, a chip, a thumbnail, a device
   * tile is an OBJECT sitting on a ground: it keeps `card` (radius 24) or
   * `cardSelect`, and it never takes the 34 corner or the white stroke.
   * Applied downward the treatment stops reading as glass and starts
   * reading as a mistake — 34 on a 56-tall row leaves no straight edge at
   * all.
   *
   * `stroke` is INSIDE, which is not the CSS default. See docs/_squircle.py:
   * the hairline is drawn on the smoothed path at double width and the
   * outer half is masked off, which is exactly what Figma's "Inside" does.
   * ================================================================ */
  largeSurface: {
    background: gradients.sheet.css,
    backgroundFallback: gradients.sheet.base,
    layers: gradients.sheet.layers, // the un-flattened Figma stack, for native
    borderRadius: radius.xxxl, // 34, ALL FOUR CORNERS
    smoothing: radius.smoothing, // 1.0 — a superellipse, not an arc
    strokeWidth: 1,
    strokeColor: "#FFFFFF",
    strokePosition: "inside",
    elevation: elevation.floating,
    // What may take it. Anything not on this list is a small card.
    appliesTo: ["bottomSheet", "dialog", "largeCard"],
  },

  /* ================================================================
   * CARD SHIMMER — iridescent speckle, inside the artwork's own face.
   *
   * Owner, 2026-08-19, second pass: the first build was "too much" — a smooth
   * rainbow wash over the whole PNG box, permanently on. What was actually
   * asked for, from the reference: *"only a shimmer which is kind of a dotted
   * visual pattern"*, a speckled/circular patch that "on hover only appears as
   * a slight strip", and only WHEN MOVED.
   *
   * So this is now ONE effect, not five layers: a rainbow gradient seen
   * through a DOT GRID, intersected with a soft moving patch. The dots are
   * the effect; the gradient only colours them.
   *
   * ⚠ THE FACE GEOMETRY IS MEASURED FROM THE ARTWORK, not guessed. key-card
   * .webp is not a plain rounded rect — it is an outer TRAY (translucent fill,
   * crisp border) with the real card FACE inset inside it. The first build
   * clipped the shimmer to the whole PNG box, so it spilled across the tray
   * and its corner did not follow the card at all. Measured off the alpha
   * channel (longest contiguous run of alpha >= 245, at 640x882):
   *
   *     face   x 95..544 (450 wide)   y 88..763 (676 tall)
   *     inset  L/R 14.84%   T 9.98%   B 13.38%
   *     corner 42px = 9.33% of face width, 6.21% of face height
   *
   * At the card's current 264px render that corner is 17.3 css px. ⚠ The owner
   * asked for 34px; 34 is `radius.xxxl`, the design system's large-surface
   * radius, but it is NOT what this artwork is drawn with. These numbers make
   * the shimmer follow the CARD exactly, which is the visible intent. Making
   * the card itself a true 34 needs the PNG re-exported (or rendered ~2418px
   * wide) — an artwork change, flagged rather than faked.
   *
   * ⚠ RE-EXPORTING key-card.webp INVALIDATES THESE FIVE NUMBERS. They are
   * measured, not derived at build time, because decoding webp in the build
   * would need a native dependency (`sips`, macOS-only) and this repo builds
   * with nothing but python + node.
   *
   * Motion lives in motion.tokens.js `gyro`; MO-GYRO in
   * memory/motion/patterns.md is the registered pattern.
   * ================================================================ */
  cardShimmer: {
    /* the artwork's own card face, as percentages of the PNG box */
    face: { left: 14.84, right: 14.84, top: 9.98, bottom: 13.38,
            radiusX: 9.33, radiusY: 6.21 },

    /* the hue wheel the speckles are coloured from. Saturated is fine here
     * BECAUSE it is only ever seen through ~12% of the area (the dots) — the
     * same colours as a flat wash read as a sticker, which is what the first
     * pass looked like. */
    holo: ["#FF4D7E", "#FFB03A", "#5BE08A", "#3FB8FF", "#A86BFF", "#FF4D7E"],

    /* ⚠ MULTIPLY, AND THIS WAS MEASURED. The card is near-white foil, and on
     * white every light-ADDING mode is a no-op — screen, color-dodge, overlay,
     * hard-light and soft-light were rendered side by side against the real
     * artwork and all five left the face unchanged. Only multiply tints white.
     * On a DARK card this inverts. */
    blend: "multiply",

    dotSize: 5, //      px grid pitch of the speckle field
    dotRadius: 32, //   % of the cell that is ink — small, so it reads as dust
    patchW: 62, //      % of the face the lit patch spans, wide and shallow so
    patchH: 40, //      it reads as a "strip" rather than a spotlight

    /* ⚠ NO RESTING SHIMMER. Owner: "only when moved, there will be a slight
     * rainbow effect". The first build held it at 0.22 permanently, which is
     * exactly the "it is static" complaint. Opacity is now purely a function
     * of deflection, from zero. */
    maxOpacity: 0.55, // at full deflection. "slight", per the brief.

    /* the edge catch, also deflection-only. Kept because the owner asked for
     * corners by name, but far quieter than the first pass. */
    rimMax: 0.3,
    rimTint: "rgba(150,120,190,",
  },

  bottomSheet: {
    background: gradients.sheet.css,
    backgroundFallback: gradients.sheet.base,
    borderRadius: radius.xxxl, // 34 [OWNER FIGMA 2026-08-19] — was 28, top-only
    smoothing: radius.smoothing,
    strokeWidth: 1,
    strokeColor: "#FFFFFF",
    strokePosition: "inside",
    elevation: elevation.floating,
    // ⚠ `paddingX` was declared TWICE here — screenPaddingX first, then
    // sheetPadX. Same value today (20), so it never showed, but the first
    // was dead and a later edit to either would have diverged silently.
    paddingX: layout.sheetPadX, // 20 [OWNER REDLINE]
    paddingY: layout.sheetPadY, // 24 [OWNER REDLINE]
  },

  /* The OS-style permission alert — "NOMA would like to send you
   * notifications". Owner 2026-08-19: "you can also apply these settings on
   * the pop ups". It is the one surface here that is not literally large,
   * and it takes the recipe anyway because it is a ground floating over a
   * dimmed screen, which is what the treatment is for.
   *
   * TODO(owner): this now reads as a NOMA surface rather than an iOS one.
   * The flow's own docstring argues these screens are truthful because the
   * dialog is the system's, not the app's. Branding it trades that accuracy
   * for consistency — worth a look on screen before it is settled. */
  dialog: {
    background: gradients.sheet.css,
    backgroundFallback: gradients.sheet.base,
    borderRadius: radius.xxxl,
    smoothing: radius.smoothing,
    strokeWidth: 1,
    strokeColor: "#FFFFFF",
    strokePosition: "inside",
    elevation: elevation.floating,
    paddingX: layout.sheetPadX,
    paddingY: layout.sheetPadY,
  },
};

/* ------------------------------------------------------------------ *
 * 8. THE INSURANCE CARD — LAW 5.
 *
 * This is NOT in `recipes`, and that placement is the point. It is one
 * bespoke object, not a pattern: a fully green-filled card, gyroscope-
 * reactive, appearing exactly once in the product. Nothing else in the UI
 * is a green card, and nothing should inherit from this.
 *
 * It is also the single place a near-full green surface is permitted, which
 * is why it lives outside the accent rules rather than bending them.
 *
 * Motion is owned by src/tokens/motion.tokens.js — the gyroscope response
 * (tilt-driven sheen + parallax on the shield pattern) belongs there, not
 * here. TODO(owner): register that pattern from templates/motion-pattern.md
 * per CLAUDE.md rule 5; it does not exist in memory/motion/patterns.md yet.
 * ------------------------------------------------------------------ */

export const insuranceCard = {
  __exception: true,
  __note: "Bespoke single-instance object. Do not generalise. See LAW 5.",

  /* Legal green: a ramp, never a flat fill — the signature mint→lime ramp,
   * run diagonally so the product render at top-right sits on the lighter end.
   *
   * ⚠ THE TEXT ON THIS CARD IS NEAR-BLACK, NOT WHITE. It was white when the
   * green family was dark; both current anchors measure under 2:1 against
   * white, so there is no orientation of this gradient that rescues it. The
   * old `textSafeZone` constraint is gone with it — ink clears 6.8:1 on mint
   * and 7.4:1 on lime, so type is legible anywhere on the card and the
   * gradient can run whichever way looks best. That is a real simplification,
   * not a workaround. */
  background: gradients.accentRamp.css,
  backgroundAngle: 215,
  borderRadius: radius.xxl, // 28
  elevation: elevation.card,
  gloss: gradients.gloss.onGreen,
  padding: spacing.s5,

  color: colors.text.onAccent, //  NEAR-BLACK. Never white — see above.
  subduedColor: "rgba(46, 46, 44, 0.66)",

  // Tiled shield watermark, and the sheen the gyroscope drives across it.
  patternOpacity: 0.10,
  sheen: `linear-gradient(115deg, rgba(255,255,255,0) 34%, rgba(255,255,255,0.34) 50%, rgba(255,255,255,0) 66%)`,
  gyro: {
    maxTiltDeg: 6, //      card rotation ceiling
    sheenTravel: 1.4, //   multiples of card width the sheen sweeps
    parallaxPt: 6, //      watermark offset at full tilt
    // prefers-reduced-motion: disable gyro entirely, keep the static sheen.
  },
};

/* ── THE MASTER KEY CARD ─────────────────────────────────────────────────
 * Owner artwork, 2026-08-20. Five colourways of ONE piece of art, chosen on
 * first-run node 5b and then carried by every later appearance of the key.
 *
 * ⚠ THE ORDER IS THE OWNER'S SENTENCE, verbatim: "as default it will be card
 * one. If the person selects pink, it will be card two. If the person selects
 * yellow, card three. Blue, card four. Green, card five." So `id` is the
 * artwork filename (`card-<id>.webp`) and the array order is the swatch order
 * on screen — the two are deliberately the same thing, because a mismatch
 * between them is the one bug in here a reader could not see.
 *
 * `swatch` is the picker dot, MEASURED off each render rather than invented,
 * so the dot and the card it selects cannot drift apart. It is not the card's
 * fill: the art is a brushed-metal radial and has no single colour.
 *
 * ⚠ These are the only five. This is not a palette to pick from — LAW 5, the
 * same reasoning as `insuranceCard` above: a bespoke single-instance object,
 * not a colour family for general use. Nothing outside the key card may use a
 * `swatch` value, and the two-green rule is untouched by it.
 */
export const keycard = {
  __exception: true,
  __note: "Bespoke single-instance object. Do not generalise. See LAW 5.",
  ways: [
    { id: "1", label: "Silver", swatch: "#d6d5d6", default: true },
    { id: "2", label: "Pink",   swatch: "#e6cfd2" },
    { id: "3", label: "Sand",   swatch: "#e0d8c8" },
    { id: "4", label: "Sky",    swatch: "#cbd9e2" },
    { id: "5", label: "Mint",   swatch: "#cadcd3" },
  ],
  /* The printed face sits inset inside the artwork's outer tray — measured by
   * scanning the PNG's alpha, not eyeballed. The shimmer and the identity
   * block are both positioned against THIS box, not the image's bounds, which
   * is what stopped the shimmer spilling outside the card. */
  face: { left: 8.14, right: 8.22, top: 3.58, bottom: 8.70,
          radiusX: 12.87, radiusY: 9.26 },
  aspect: "1180/1564",
};

/* ── THE STYLIZED TITLE ──────────────────────────────────────────────────
 * Owner redline, 2026-08-20, straight from their Figma inspector: Google Sans
 * Flex Bold 24, letter-spacing 0, and a three-stop linear gradient run at an
 * angle across the words — ink, a pale green at the midpoint, ink again.
 *
 * Used on the first-run key-creation headings only (nodes 5a, 5b, 5c). It is a
 * DISPLAY treatment, not a text colour: the mid stop is legible only because
 * the two ends are ink, so nothing here may be lifted out and used as a fill.
 *
 * ⚠ THE MID STOP IS NOT ONE OF THE TWO GREENS. Now `#8EAE7D` (was `#AECF9B`
 * in the first pass); `green.neon` is `#AEC799`. The second redline moved it
 * further away rather than closer, so this is a deliberate darker green, not an
 * eyedropper drift. Recorded as given, because
 * inventing agreement between a redline and a token is worse than flagging the
 * gap, but this wants an owner call: snap it to `green.neon` and the palette
 * rule (LAW 6, two greens and shades of them) stays intact with no visible
 * change; keep it and there are three greens in the product.
 */
export const titleGradient = {
  __exception: true,
  __note: "Bespoke display treatment. Not a colour family. See LAW 5.",
  font: "Google Sans Flex",
  weight: 700,
  size: 24,
  letterSpacing: 0,
  angle: 100,          // css deg; the owner's handle runs slightly downhill
  /* Retuned 2026-08-20 (second owner redline): the stops pulled IN to 24/50/74
   * and the green darkened. The point of the change is the ramp length — ink now
   * holds the first quarter and last quarter flat, so the green reads as a slim
   * streak through the middle of the word rather than as the word's colour.
   * Owner: "more of the black color and a slimmer streak of the new green". */
  stops: [
    { at: 24, color: "#171717" },
    { at: 50, color: "#8EAE7D" },   // ⚠ see the note above — still not green.neon
    { at: 74, color: "#171717" },
  ],
};
