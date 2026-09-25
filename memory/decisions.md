# Decision Records (ADR log)

> Why X was chosen over Y. Format: ADR-### | date | decision | alternatives | rationale.
> Also holds OPEN CONFLICTS flagged by agents.

---

## ADR-001 | 2026-08-04 | Adopt an Airbnb-derived warm-neutral foundation

**Decision.** Noma's visual foundation is a warm-neutral system derived from
Airbnb iOS: near-neutral greys for text and structure, a warm beige/sand family
for surfaces, generous corner radii, and soft two-layer shadows. Canonical
values live in `src/tokens/design.tokens.js`.

**Source.** Airbnb iOS screens observed via Mobbin on 2026-08-04 (Home,
Checkout, Host profile, Search sheet), captured at 393×852pt.

**What we took**
- Neutral ramp `#FFFFFF → #F7F7F7 → #EBEBEB → #DDDDDD → #717171 → #222222 → #000000`
- Warm surface family, anchored on the observed sheet background `#F0EEE9`
- Radius scale: `12` default, `20` for elevated cards and sheets, `999` for pills
- Elevation: soft, low-opacity, **two layers** (tight contact + wide ambient)
- Two distinct card anatomies (see below)
- 24pt screen margin, 4pt spacing base

**What we explicitly rejected**
- Airbnb's Rausch red (`#FF5A5F`) and all brand hues. Owner's direction: keep
  the blacks / whites / beiges / greys and the overall vibe, not the red.
- Pure `#000000` for text. Airbnb uses `#222222`; pure black reads harsh on warm
  surfaces. `#000000` is reserved for system chrome and icons only.

**Two card styles — both are canonical, they are not alternatives**
| | `recipes.cardElevated` | `recipes.cardOutlined` |
|---|---|---|
| Sits on | warm surface (`sand.200`) | white canvas |
| Radius | 20 | 12 |
| Definition | soft shadow (`elevation.card`) | 1pt `border.hairline` |
| Use for | hero / featured / identity | dense, structured content (forms, checkout) |

Rule: **never combine a hairline border with a shadow** on the same card, and
never place an elevated white card directly on white — it needs the warm ground
to read as lifted.

**Alternatives considered**
- *Cool-grey neutral system (Linear/Stripe-like).* Rejected — owner specifically
  wanted the warmer tone.
- *Warm tint applied across the whole ramp, text included.* Rejected — tinting
  text greys makes contrast ratios drift and muddies photography. Warmth is
  carried by surfaces only; text greys stay near-neutral.

---

## ADR-002 | 2026-08-04 | Typeface: Google Sans Flex

**Decision.** Noma adopts **Google Sans Flex** (variable, SIL OFL) as the
primary typeface, closing O-2. Owner supplied the specimen and the font
package directly. Assets live in `src/fonts/google-sans-flex/`:
the full variable TTF (`opsz`, `wght`, `wdth`, `slnt`, `GRAD`, `ROND` axes),
its `OFL.txt`, and a handful of 24pt/9pt static cuts for tooling that can't
consume a variable font. A Latin-only subset variable WOFF2 (~118KB) was cut
for web/artifact use — see `memory/decisions.md` O-4 lineage; same
optical-accuracy caveat applies to anything web-rendered.

`typography.family.sans` and the `opsz`-aware type scale in
`src/tokens/design.tokens.js` are canonical. Prefer `font-optical-sizing: auto`
on web so `opsz` tracks rendered size automatically; the per-style `opsz`
value in the scale is the fallback for engines that don't support it (React
Native / Skia).

**Alternatives considered.** None — owner specified this typeface directly
rather than asking for options, unlike the colour system which was derived
from a reference app.

**Consequence — new gap opened.** Google Sans Flex's cmap has no Devanagari
block. See O-5 below.

---

## ADR-003 | 2026-08-04 | Accent: two brand greens, budgeted at 10%

> ⚠ **VALUES SUPERSEDED BY ADR-004.** Every hex and contrast figure below is
> historical. The structure — two anchors, the 10% budget, near-black for
> non-primary emphasis, pair-each-green-with-its-`on*`-token — still stands.
> For current values see ADR-004 or `src/tokens/design.tokens.js`.

**Decision.** Noma's accent is green, supplied by owner as two anchors. This
closes O-1.

| Token | Hex | Role |
|---|---|---|
| `green.neon` | `#A6CD86` | light — status dots, badges, chips, highlights |
| `green.sage` | `#2C5146` | deep — **the** primary CTA fill |

Green occupies **~10% of any screen, never more**. Primary surface stays white,
text stays near-black `#222222`. The accent marks the one thing that matters on
a screen; it is never the ground. The allowed/forbidden list is inline on
`colors.accent` in `src/tokens/design.tokens.js` so it stays greppable.

Consequence: what used to be `recipes.buttonPrimary` (near-black) is renamed
`recipes.buttonNeutral` and keeps its job — emphasis that is *not* the screen's
primary action. This is what protects the 10% budget; without it every emphatic
button would reach for green.

**Two anchors, not one ramp.** `neon` is ~93° hue (yellow-green), `sage` is ~162°
(blue-green). They are 69° apart. Interpolating between them passes through muddy
olive, so **never** build a gradient or continuous scale from one to the other.
Tints and pressed states are derived per-anchor, in-hue.

**Measured contrast — the reason there are two `on*` tokens:**

| Pair | Ratio | |
|---|---|---|
| `sage #2C5146` + white `#FFFFFF` | 8.85:1 | ✓ AAA |
| `neon #A6CD86` + ink `#222222` | 8.86:1 | ✓ AAA |
| `neon #A6CD86` + white `#FFFFFF` | **1.80:1** | ✗ fails — never ship this |

White-on-neon is the trap: neon is light enough to *look* like a coloured button
that should carry white text, and it fails badly. Always pair a green with the
`on*` token sitting beside it in the token file.

**Alternatives considered.** None on hue — owner specified green directly. The
*budget* (10%, near-black retained for non-primary emphasis) is our addition,
derived from the owner's "use it very sparingly" and from `ma` (see
`memory/product/vision.md`): scarcity is what makes the accent legible as
meaning rather than decoration.

**Noted, not acted on.** The Set B persona deck is styled in orange
(`#D95E2B`-ish), not green. Read as deck styling rather than product intent, but
if that orange is load-bearing brand, ADR-003 needs revisiting.

---

## ADR-004 | 2026-08-04 | Accent greens retuned — supersedes ADR-003's values

**Decision.** The owner supplied a revised green pair. ADR-003's *structure*
(two anchors, 10% budget, near-black for non-primary emphasis, pair-with-the-
`on*`-token rule) stands unchanged. Only the hex values move.

| | Was (ADR-003) | Now | |
|---|---|---|---|
| light | `neon` `#A6CD86` | `neon` `#AEC799` | |
| deep | `sage` `#2C5146` | `moss` `#4D6747` | **renamed** |

The deep anchor is renamed `sage` → `moss` to match the owner's own naming.
Derived states were recomputed in-hue rather than carried over:
`mossPressed #3B4F36`, `mossSoft #C2D0BE`, `mossTint #EFF2EE`,
`neonPressed #91B375`, `neonSoft #D0DDC5`, `neonTint #F2F5F0`.

**Consequence 1 — the primary CTA loses AAA.**

| Pairing | Was | Now | |
|---|---|---|---|
| deep + white | 8.85:1 AAA | **6.27:1 AA** | −2.58 |
| neon + `#222222` | 8.86:1 AAA | 8.66:1 AAA | −0.20 |
| neon + white | 1.80:1 FAIL | 1.84:1 FAIL | trap persists |

6.27:1 clears AA (4.5:1) comfortably and is correct for a 16px/600 button
label, so nothing is broken. But it is no longer AAA, and that is a real
reduction worth knowing before someone specs the accent for dense or small
text. Where AAA is genuinely required, use `surface.inverse` (near-black),
which is what `recipes.buttonNeutral` already exists for. **Do not darken moss
ad hoc to chase the ratio** — `mossPressed` is a state, not a second brand
colour.

**Consequence 2 — the pair is now one hue family, which is an improvement.**
The old pair sat 69° apart (neon 93°, sage 162° — sage was really a blue-green
teal). The new pair sits **16° apart** (neon 93°, moss 109°). They now read as
one green, light and dark, rather than as two unrelated greens. ADR-003's
outright ban on interpolating between them is relaxed accordingly: at 16° a
blend no longer passes through muddy olive. Solid fills remain the house style
regardless — a gradient CTA is not part of this system.

**Consequence 3 — the white-on-neon trap survives the change.** Neon is still
light enough to look like a coloured button that should carry white text, and
1.84:1 is still unreadable. The rule is unchanged and still needs stating.

---

## ADR-005 | 2026-08-04 | Motion: playful spring on discrete moments — resolves O-7

**Decision.** Owner ruled the O-7 tension: NOMA's motion personality is **playful —
springy, bouncy, quirky, the Airbnb register**. Canonical values now live in
`src/tokens/motion.tokens.js`; gates in `.claude/rules/motion.md`.

**How it coexists with `ma`.** The split flagged as the likely resolution is now the
actual rule: **bounce marks discrete moments** (a tap, an arrival, a confirmation);
**ambient surfaces stay still** (live readings, monitoring, charts — `standard`
easing, scale capped at 1.02, 4s breathing at most). Calm is the ground, bounce is
the event. Exits never bounce; alarm never bounces; reduced-motion is mandatory.

**Values.** Two springs — `spring` (0.34, 1.56, 0.64, 1), ~10% overshoot, for
everyday controls; `springBold` (0.22, 1.8, 0.36, 1) for hero arrivals (sheets,
overlays, toasts). Durations 80/140/240/360/480ms + a 4000ms ambient tier.
Stagger 45ms lists / 60ms grids. Press 0.96, pop 1.04, breathe 1.02.

**Provenance caveat.** The owner referenced a bouncy style defined in an earlier
session that is not available to this one; these values are a fresh codification
from the owner's stated direction (playful / fun / quirky / bouncy / Airbnb-like).
If the earlier session's exact values surface, reconcile by revising this ADR —
not by editing UI code.

---

## 2026-08-04 · PM prototype set ingested — C-2…C-13 opened

Four HTML prototypes were supplied and read (see `docs/index.md`). They are the first
real product substance received. Extracting them populated six pillars — and surfaced
**twelve new conflicts**, because the four documents disagree with each other on nearly
every naming decision.

Nothing was reconciled. Where documents disagree, both readings are recorded below with
the evidence, per rule 6. **No design pillar values were touched.**

What was populated: `src/hardware/devices.json`, `src/hardware/feature-map.json`,
`memory/product/journeys.md`, `memory/product/scope-ledger.md`,
`memory/architecture/{system,data-models,ai-integration}.md`,
`memory/analytics/{event-taxonomy,monetization-map}.md`, `memory/voice/ai-personas.md`.

**The single most valuable thing in the set** is the agent model in `air-agent-app.html`:
graduated per-capability autonomy, a four-slot explanation contract
(Sensed / Decided / **Instead of** / Obeys rule), and inert editable rehearsal before
execution. That is a genuine architectural position, not a UI pattern. It is written up
in `memory/architecture/ai-integration.md` and should be read before any agent surface is
designed.

---

## OPEN — carried forward, do not silently resolve

### C-15 · "Selection is LIFT" vs a dark selected chip — NEW 2026-08-19

**Two live directives contradict each other, and I have followed both in
different places rather than resolving either. This needs one owner call.**

**LAW 3 / `recipes.chipSelected` / `build-flow.py`'s re-skin** say selection is
**LIFT** — a raised white surface — and explicitly *"never an outline and never
a fill"*. build-flow.py's own comment calls converting `.chip.on` / `.row.on` /
`.pcard.on` to lift *"the single biggest visual change in the file"*.

**The owner, 2026-08-19**, looking at node 17's room chips: *"the bedroom,
living room, selected chips are not the correct color and do not have the inner
shadow like our final CTA. Our final CTA gray and the styles that it has, like
the drop shadow, the inner shadow and everything, that is our black."* That is
a dark **fill**, which LAW 3 forbids.

**What is built right now, so nobody has to guess:**
| Component | State | Treatment | Follows |
|---|---|---|---|
| `.chip.on`, `.rs__t.on` | selected | ink-gradient FILL + dock shadow | the owner |
| `.pcard.on` | selected | raised white LIFT + bevel | LAW 3 |

The split is defensible — small controls read as segmented (fill), large cards
read as lifted — and plenty of systems do exactly that. But it is currently an
accident of two instructions arriving separately, not a stated rule, and it
means "selected" looks like two different things in one flow.

**What resolving it looks like:** either (a) LAW 3 gets an explicit exemption
for small controls, written into `.claude/rules/design-system.md` and
`recipes.chipSelected` amended to match, or (b) the room/name chips go back to
lift and the owner's instruction is recorded as superseded. Not my call.

⚠ Related and NOT the same question: the owner also ruled that
`--ink` (#0B0B0B) is never a FILL — every dark surface takes the ink gradient
(#3A3A38 → #2E2E2C). That part is unambiguous and is now applied throughout
`build-prototype.py`; it is not part of this conflict.

---

### C-1 · Two incompatible persona sets — NOW WITH PROTOTYPE EVIDENCE

**Update, not a resolution.** The prototypes independently corroborate **Set B**:

- **Ravi** and **Lakshmi** appear as real named people in the camera event feed
  ("Person recognised: Lakshmi", "Ravi arrived home") — Set B's P2 is literally rendered.
- All four of Set B's named surfaces exist as built screens: **Home Score**
  (`ScoreDetailScreen`), **Faces You Trust** (`FaceTagSheet` + event badges), **Shop**
  (`ShopTab`), **AQI monitoring** (`PurAQIScreen`).
- Set B's **P3 household help** maps exactly onto the `staff` role — "Maid, driver,
  caretaker — time-limited, assigned devices".
- The strategy deck's room views are built around **kids and grandparents**, matching
  Set B's household framing.
- **Set A's names (Kartik, Siddharth) appear nowhere in any prototype.**

This is strong evidence, and it is still the owner's call — the prototypes could equally
have been built from a superseded brief. But anyone waiting on C-1 should know Set B is
the one the product was actually built against.

*(Original C-1 detail follows below.)*

### C-2 · The product and the assistant have five names between them

| Thing | Names seen |
|---|---|
| Product | **NOMA** (current) · Ding · Noise Home · Noise Air · Noise Sanctuary |
| Purifier SKU | Ding Air Pro · Ding Air Pro 200/500/Max · NS Air S1 |
| Assistant | Ding · Noise AI Agent · Sanctuary Assistant · *(unnamed first person)* |
| Score | Home Score · Sanctuary Score · Air Score |
| Subscription | Sanctuary Plus / Sanctuary Family |

Blocks: every user-facing string, all of `src/i18n/`, persona prompts, and every SKU in
`src/hardware/devices.json`. **This is the highest-leverage decision on the list** — most
other content work is downstream of it.

### C-3 · Three role models for household sharing
`family/staff/guest` vs `family/guest` vs `owner/family/guest`. The sharing flow was
rebuilt three times in the prototype (`SharingFlow`, `V2`, `V3`), which is itself the
evidence that it is unsettled. **Do not resolve by picking the newest** — only the 3-role
version has an explicit `staff` role, which is persona P3, and collapsing it into `guest`
loses the recurring weekly-window case P3 is defined by. Detail:
`memory/architecture/data-models.md`.

### C-4 · Three fan-mode vocabularies
`Auto/Turbo/Silent/Eco` vs `Auto/Sleep/Turbo/Manual` vs `Quiet/Standard/Turbo/Max`.
**"Turbo" is the only value present in all three.** Distinct from whole-home scenes
(Home/Away/Night), which are consistent. Blocks mode UI, automation actions, and voice
copy that names a mode.

### C-5 · Four definitions of the Score
| Source | Dimensions |
|---|---|
| Onboarding slide | air, security, energy, cleanliness (4) |
| `SCORE_DIMS` | Air 25 · Security 25 · Cleanliness 20 · Filter Health 15 · Energy 15 (weighted, sums to 100) |
| Strategy deck | Air, Safety, Comfort, Care, Family (5, unweighted) |
| Week One | "Air Score" /100 — purifier-only, weekly |

`SCORE_DIMS` is the only one with weights and is the most implementable. But the deck's
version is the only one with a **Family** dimension, which is the deck's whole
differentiation claim. And the Week One "Air Score" may be a *different feature* — a
weekly recap rather than a live home score. Blocks `F-HOME-SCORE`.

### C-6 · Prices disagree
Anchor purifier **₹4,999** (app) vs **₹8,999** (deck). HEPA filter **₹1,299** (Week One)
vs **₹1,499** (app). Not roundable: the deck's entire competitive argument rests on price
parity with Xiaomi at ₹8,999, so one document is describing a different product.

### C-7 · The core differentiator has no specification
AQI-weighted filter life is *the* product claim, with a worked example (Delhi 38% vs
Mumbai 64% for identical hours) and a stated effect ("3–5× more particulate above AQI
200"). **No formula, no coefficients, no validation data.** It is a marketing claim
awaiting an engineering model, and it gates `F-FILTER-HEALTH` and half the value story.

### C-8 · No safety classification for agent autonomy
"Act silently" is offered per capability, but every example is comfort-grade (fan,
pre-clean, reorder). Nothing prevents it applying to a **lock** or to **spending money** —
`Reorder filters` at "Act silently" is an unattended purchase. Separately, the
SpO₂-below-94% → purifier-Turbo trigger is a **health-adjacent inference** presented as an
ordinary automation, with no medical or legal position. Needs a capability safety class
before any autonomy ships.

### C-9 · The air map shows AQI for rooms with no sensor
The home air map reports Living Room 94, Kitchen 112 — rooms with no purifier and
therefore no sensor. Inference, interpolation, or invention is unstated. It is
**load-bearing for an upsell** ("a Living Room unit would cut it to ~24"), so a guessed
number is being used to sell hardware. Also: CO₂ appears in Score factors with no stated
SKU carrying a CO₂ sensor.

### C-10 · Neighbourhood comparison may not actually be anonymous
Shows *"Mehta (2F) 54"* — a surname plus a floor — while claiming "anonymised, your
address is never shown." In a small building that identifies a household. Needs a DPDP
privacy review. Gates the share/acquisition engine, which the docs call "the cheapest
acquisition channel a product ever gets."

### C-11 · "Data never leaves home" vs three networked features
The product claims on-device AI and DPDP compliance, then ships outdoor-AQI blending
(CPCB), forecast-driven pre-clean, and neighbourhood comparison — none of which can work
locally. The claim probably means *personal and biometric data stays local; ambient public
data is fetched*, which is defensible and still strong. As literally written it is a
compliance exposure, and it also **blocks the analytics taxonomy** — an analytics SDK is
by definition exfiltration.

### C-12 · Two room-preset lists
8 presets (Living Room, Bedroom, Hallway, Kitchen, Office, Study, Balcony, Kids Room) vs
11 (adds Bathroom, **Pooja Room**, Front Door, Garage). The 11-item list is the
India-appropriate one; the 8-item list omits Pooja Room.

### C-13 · The subscription contradicts the positioning
Free tier gets "real filter health score"; Plus (₹699/mo) gets "AQI-weighted filter
tracking". But AQI-weighting *is* what makes the score real — it is the entire
differentiator versus the named competitors. Selling it as an upsell undercuts the
headline claim. Also: no paywall or upgrade prompt exists in any app prototype, so the
subscription is deck-only.

---

### C-1 (original detail) · Two incompatible persona sets

Full detail in `memory/product/personas.md`. `src/personas/personas.json` stays empty
until resolved. Blocks tone routing (`memory/voice/tone-matrix.md`),
`src/personas/prompts/`, and every `J-*` journey ID. See the prototype-evidence update
under C-1 above.

---

---

## 2026-08-05 · "My Home" PRD ingested — C-14 opened

Source: `ding-my-home-prd.md` (owner-supplied, marked *approved for build*).
Built as `docs/features/my-home/my-home-prototype.html`.

### C-14 · Two visual languages, both owner-approved

The My Home PRD §11 specifies a **dark** system — page `#0c0e12`, card `#11151d`,
accents aqua `#7ee0c8` / amber / coral / violet, described as the "Air Agent" language,
with `ding-home-states.html` (S3) as visual truth. That file was not supplied.

The owner separately directed, on the same day, a **light** system for the first-run
flow — radial gradient `#FFFFFF` → `#A4A4A4`, 8% card shadows, black pill CTAs, and
explicitly *no* accent green.

**These cannot both ship.** A user reaches My Home directly off the first-run reveal;
two palettes inside one session is a defect, not a preference. The prototype was built
**light** for exactly that reason — continuity with the flow the owner has been iterating
on — but the PRD is the newer document and says "approved for build", so this is the
owner's call, not mine.

Note this is a *third* palette in play: `src/tokens/design.tokens.js` remains canonical
and still carries the ADR-003/004 greens, which neither the PRD nor the first-run
direction uses. All three need reconciling into one.

### C-2 gains another data point

The PRD calls the product **"Ding"** throughout, and names the purifier a white-label
device. Everything else in this repo says NOMA. That is a sixth name for the same thing.
The prototype uses NOMA for consistency with first-run.

### Reconciliation, not conflict — the home zone model

`memory/architecture/ai-integration.md` §2 describes Home as three zones: *Settled now /
Needs your call / Done today*. The PRD supersedes this with a **two-strata** model (room
above a labelled divider, agent below) and a wider zone vocabulary. They are compatible:
the agent stratum contains the old three zones, and the room stratum is what "Settled now"
was reaching for. Treat the PRD as the evolution, and update `ai-integration.md` when the
page is built for real.

---

### Design-foundation items (ADR-001…004)

- **O-1 · Accent colour.** ~~`colors.accent` is deliberately `null`.~~
  **RESOLVED by ADR-003, values revised by ADR-004** — moss `#4D6747` + neon
  `#AEC799`, budgeted at 10%.
- **O-2 · Typeface.** ~~Airbnb ships proprietary *Cereal*; unavailable to
  us.~~ **RESOLVED by ADR-002** — Google Sans Flex.
- **O-3 · Dark theme.** Light-only for now. The token structure is
  semantic (`surface.*`, `text.*`) so a dark map can be added without touching
  UI code, but no dark values exist yet.
- **O-4 · Radius measurements are optical.** Mobbin serves cross-origin images,
  so pixel/canvas sampling was blocked; hex values and radii were read visually
  from zoomed captures and reconciled against Airbnb's documented ramp. They are
  close but not byte-exact. Re-verify against a real device or Figma file before
  locking a 1.0 design system.
- **O-5 · No Devanagari coverage.** Google Sans Flex (ADR-002) is Latin-only —
  confirmed by inspecting its `cmap`, zero codepoints in U+0900–097F. Noma ships
  an `hi` locale (`src/i18n/locales/hi/`). Any surface rendering Hindi strings
  needs a second family in the fallback chain with real Devanagari glyphs, not
  just the browser/OS default — pick one that pairs visually with Google Sans
  Flex's weight and proportions before `hi` ships, not after. Raised in priority
  by C-1: the primary personas are Indian (Bangalore), so `hi` is likely a real
  shipping locale rather than a nice-to-have.
- **O-6 · No semantic status colours.** ⚠ **Provisionally filled in the My Home prototype
  (2026-08-05), not in the tokens.** That prototype introduces four muted band colours —
  good `#3F6E60`, moderate `#8A6A2F`, poor `#A2632F`, bad `#96402F` — used only on the AQI
  badge, band dots and contributor meters, never on chrome, buttons or type, and always
  paired with a text label. An air-quality product cannot signal "bad" in greyscale, and
  the My Home PRD §11 mandates a band mapping. Either promote these into
  `src/tokens/design.tokens.js` as the status ramp, or replace them with the real one.
  Original note follows. `colors.status` is `null`. Noma reports
  air quality, lock state, and device health — it needs warning / critical /
  offline, and **green cannot carry "bad"**. Deliberately not invented: the owner
  asked for restraint and adding unapproved hues would breach the 10% intent.
  This blocks any real device-status UI. Needs: a warning, a critical, and a
  neutral-offline, all legible on both white and `sand.200`.
- **O-7 · "Playful bounce" vs `ma` calm.** ~~Both owner-stated, pulling
  apart.~~ **RESOLVED by ADR-005** — playful spring on discrete moments, stillness
  on ambient surfaces. `src/tokens/motion.tokens.js` is populated.

- **O-8 · Onboarding and device setup have no `F-*` id.**
  `src/hardware/feature-map.json` registers thirteen features. None of them is
  "get a new customer to a working first device" — the flow every other feature
  depends on. `J-ONBOARD-*` and `J-PAIR-PUR-*` exist as journeys with no feature
  id, so they have no PRD slot, no owner, and no row in the scope ledger.
  `docs/features/first-run/prd.md` (2026-08-05) is written against two
  **proposed, unassigned** ids — `F-FIRST-RUN` and `F-SETUP`. Ids are the
  owner's to assign (rule 6), so nothing was written into the registry.
  Raised by the Mobbin teardown, `docs/research/2026-08-05-setup-teardown.md`.

- **O-9 · `identify` and the LED state vocabulary are unconfirmed hardware behaviour.**
  The setup flow depends on two things no document confirms the purifier can do:
  a **remote identify** (blink the ring on command, so a two-purifier household
  can tell which one it is naming — Apple Home's pattern) and a **distinguishable
  ring state** for pairing vs. already-paired vs. error. Neither appears in
  `src/hardware/feature-map.json`. If the hardware cannot do them, screens 2.4
  and 2.6 of `docs/features/first-run/prd.md` need redesigning, not rewording.

- **O-10 · Motion gate 2 is unenforceable outside CSS.** ⚠ **An accessibility gate
  that silently does not fire.** `.claude/rules/motion.md` gate 2 reads: "Every file
  that animates must contain `prefers-reduced-motion`. No exceptions — this is an
  accessibility gate." That string is a **CSS media query**. No Swift, Kotlin, or
  React Native file can contain it, so the grep passes those files by finding
  nothing to check — it reports clean precisely where it has no coverage. Surfaced
  by `design-elements/bottom-nav/` (2026-08-12), the repo's first native component:
  it satisfies the gate's *substance* via
  `@Environment(\.accessibilityReduceMotion)` routed through
  `NomaMotion.resolve(_:reduceMotion:)`, and fails the gate as *written*.
  **Not worked around** — adding a dead CSS string to a Swift comment would make
  the grep pass while making the gate meaningless. The rule needs amending to
  accept the platform spellings (`accessibilityReduceMotion` on Apple platforms,
  `Settings.Global.TRANSITION_ANIMATION_SCALE` / `isReduceMotionEnabled` on
  Android/RN). Owner's call, because it edits an enforced rule.

  Worth noting the same shape of hole applies to gate 1: `cubic-bezier(` and
  `[0-9]ms` are both CSS spellings, and a Swift file writing
  `.timingCurve(0.34, 1.56, 0.64, 1, duration: 0.24)` inline would violate the
  rule's intent while matching neither pattern. Gate 1 was met here by
  convention, not by enforcement.
