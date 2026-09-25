# PRD — Ding · "My Home" Page

**Scope of this document:** the build spec for the **My Home** tab only. It is written for an engineering agent (Claude Code) to implement as a **faithful front-end** of the approved prototype, in **React + Tailwind**, with **all data mocked via typed fixtures**. The backend, score engine, and detector pipeline are out of scope for this build — but every data contract they will eventually satisfy is defined here so the UI is wired correctly from day one.

**Reference artifact:** `ding-home-states.html` (S3 prototype). Where this document and the prototype disagree, this document wins. Where this document is silent, match the prototype.

**Status:** approved for build.
**North star this page serves:** WAAH — Weekly Active Automated Homes. Every surface either produces an automation, proves one paid off, or builds the trust/habit that makes the next one land.

---

## 1. Product context (why this page is shaped this way)

Ding is an **agent-first** smart-home app launching with a single white-label air purifier. The agent **observes, proposes, explains, and learns — it does not act autonomously** in v1 (proposal-only, with a narrow "act & tell me" exception for reversible safety responses). The differentiator is the software layer, not the hardware.

Four principles constrain every decision below:

1. **Glass-box, always.** Every number is tappable to its evidence; every proposal shows what was sensed, what was decided, and what rule it obeys.
2. **Goals, not rules.** The agent proposes outcomes ("keep the room under AQI 50 overnight"), not device macros.
3. **Scarcity protects trust.** At most **one** proposal is visible in the primary proposal slot at a time. Accept-rate is a tracked OKR (≥80% action-accept, <5% reversal); flooding the page with asks destroys it.
4. **The room is the product — until it isn't.** v1 is one purifier in one bedroom that seals shut at night. The page is built for that reality and **mode-switches** when a second device appears.

### The two-strata model (the spine of this page)

The page is divided by a labeled divider into two strata, and **this division is load-bearing** — it is not decoration:

- **Room stratum (above the divider):** the room as a *place*. The isometric render, the live indoor AQI pinned to it, the large Room Quality Score, and the room's own observations. **Nothing in this stratum asks the user for anything** — no action buttons. It is a state of the world.
- **Agent stratum (below the divider):** the agent as a *voice*. Proposals, receipts, learned facts, checklists, guides. **Every card here carries a left "spine" accent** so the stratum stays legible when the divider has scrolled off-screen. This is where all interaction lives.

Implementation must preserve this separation structurally (two distinct container regions), not merely visually.

---

## 2. Two numbers, on purpose (read this before building the hero)

The hero shows **two different numbers that will frequently disagree**, and the disagreement is the point. Do not "fix" it by making them match.

| | Live indoor AQI (the badge) | Room Quality Score (the numeral) |
|---|---|---|
| **What it is** | A single **measurement** — particulate AQI right now | A **composite judgment**, 0–100 |
| **Where** | Small circular badge pinned to the room render | Large numeral beside the render |
| **Composed of** | PM2.5 only | Weighted contributors: PM2.5, VOC, humidity-in-band, noise (from fan level), filter health |
| **Example** | 22 | 86 — because humidity dipped out of band |
| **Purpose** | Instant, familiar, glanceable | The reason to tap through to the report |

At **n=1 (single device), the Room Quality Score *is* the Home Score.** There is no separate home-level number to reconcile. That equivalence is a core concept, not a placeholder.

### 2.1 Score calculation contract (the one thing to pin precisely)

The engine is out of scope, but the **contract the fixture must honor and the UI must render** is fixed:

- Score is **0–100**, integer.
- It is a **weighted sum of contributors**, each of which has: a `key`, a raw value + unit, a **banded status** (`good | moderate | bad` → drives the colored label and meter fill), a `weight`, and a normalized 0–1 sub-score.
- **A missing contributor rebalances the remaining weights — it does not tank the score.** (If the humidity sensor drops out, the score is computed from the remaining contributors renormalized to sum to 1, and the missing row renders as `unavailable`, not as zero.) The fixture must include at least one scenario exercising a missing contributor so this path is built.
- The score carries a **confidence** value: `full` when the room is sealed (night, door shut) or the sensor otherwise owns the air; `soft` when the agent is inferring (door open, daytime, or <72h of history on a new room). Confidence is displayed, never hidden.
- The **drill-in (report) always shows the full contributor breakdown** — the score is never a black box.

The UI never computes the score. It receives it, with its contributor array and confidence, from the data layer (fixture now, API later).

---

## 3. The state machine (the hero "changes job" so the page is never empty)

The single most important structural idea: **My Home is a state machine, not a static list.** A continuous score plus a rotating hero job means the page always has something true and useful to show, solving the "empty between events" problem that kills smart-home apps.

Six states ship in v1. **Exactly one is active** at render, selected by the data layer (for this build: selectable via a dev control + the fixture's `activeState` field). Each state defines the hero's job and which agent-stratum slots are filled.

| # | State key | Hero's job | Trigger (real system, for reference) | Confidence |
|---|---|---|---|---|
| 01 | `dayOne` | Prove the device works; ask the one onboarding question | First session, <24h history | soft (low) |
| 02 | `morningRecap` | Report the sealed night; celebrate the streak | First open after a sleep window ends | full |
| 03 | `calmDay` | Name what it's watching; surface the best available proposal | Default daytime, nothing acute | soft (door/day) |
| 04 | `eveningPlan` | Show tonight's plan | Evening, pre-sleep window | full (sealing) |
| 05 | `liveEvent` | Show the live response to a spike | Indoor AQI crosses threshold, rising fast | full (responding) |
| 06 | `seasonPrep` | Frame a coming seasonal change; run the playbook | Forecast/calendar signals season shift | full |

Each state has an **accent color** that flows through the hero glow, the score kick-label dot, and the live dot:
`dayOne` amber · `morningRecap` aqua · `calmDay` aqua · `eveningPlan` aqua · `liveEvent` coral · `seasonPrep` amber.

### 3.1 Composition rules (how slots fill and empty)

These rules are enforced by the state definition, but the component must respect them:

1. **The hero (room stratum) is always filled.** There is no empty hero.
2. **The primary proposal slot shows at most one proposal.** If a state has multiple proposals (e.g. `seasonPrep`), they stack in the "Needs your call" zone but this is the deliberate exception for the seasonal register; the *steady-state* rule is one.
3. **Empty states are written, never blank.** When a slot has nothing, it renders explanatory copy naming what the agent is watching ("Nothing needs you this morning. I'm watching the 6 pm forecast…"), never a void or a spinner. Every empty slot in the fixture ships with this copy.
4. **A live event suppresses decorative slots.** In `liveEvent`, trends/streak/rotating/guide slots are hidden — the page narrows to the event and its prevention proposal.
5. **Slot content is data-driven.** The component reads a `slots` structure per state; it does not hard-code which cards appear.

---

## 4. Detector → Proposal → Card (the pipeline behind agent-stratum content)

Every agent-stratum card is the visible end of a **detector → proposal → card** pipeline. The detectors are out of scope; the **card contract and the proposal taxonomy** are in scope because the UI must render each type correctly and the fixtures must cover them.

### 4.1 Proposal / card taxonomy

The fixture and the components must support these card `kind`s:

| kind | Meaning | Primary action | Notes |
|---|---|---|---|
| `proposal` | An ask awaiting the user's call | Accept (primary) · "Why this?"/"Show data" · Skip/dismiss | The atomic unit. Undoable once accepted. |
| `receipt` | Something already done (agent acted, or a past accept ran) | "Do this always" (→ Automation) · Undo | The glass-box audit made friendly. |
| `liveAction` | An autonomous reversible response happening now | Stop it · "Why this?" | Only appears in `liveEvent`. Shows progress. |
| `learnedFacts` | The agent's memory of this room | per-fact: Right / Fix | The moat. Each fact is confirmable/correctable. |
| `checklist` | A seasonal/onboarding playbook | per-item: toggle complete | State persists across sessions. |
| `guide` | An evergreen micro-article | Opens guide | India-specific content library. |
| `blindSpot` | Honesty about sensing limits | (tap → second-sensor upsell) | Only at n=1. Evidence-based, not promotional. |

### 4.2 Detector classes the fixtures must exercise

The PRD's card content spans these detector families. **The build must include at least one fixture card per class** so every rendering path exists:

1. **External-forecast** — pre-clean before a bad-air window (`eveningPlan`).
2. **Own-history / recurring-pattern** — the cook-spike → daily automation offer (`liveEvent`). *This is the engine of WAAH.*
3. **Own-history / energy** — **the power-saver proposal** (`calmDay`): "your afternoons run clean on their own → power saver 12–5 pm → ~₹90/month + filter life." This class is new and important: **an agent that sometimes tells you to run *less* earns the trust to tell you to run *more*.** It comes with three touchpoints that must all be built:
   - the **proposal card** in `calmDay`;
   - a **receipt** in `eveningPlan` ("power saver ran, ₹3 saved today");
   - a **fan-effort-vs-air-need chart** in the report (see §6), whose gap between the two lines is the evidence.
4. **Predictive maintenance** — season-adjusted filter reorder (`seasonPrep`), feeding the ≥40%-reorder OKR.
5. **Comfort** — humidity advisory with in-band visualization (`calmDay`); the purifier can't fix RH, so the card advises + compensates (caps fan).
6. **Standing-goal** — trade a nightly question for a season-long mandate (`seasonPrep`); the bridge toward the autonomy ladder.

### 4.3 Card interaction behavior (front-end, mocked)

Since the backend is stubbed, actions resolve locally with optimistic UI:

- **Accept a proposal** → toast confirming what was scheduled/created; card transitions to a receipt-like acknowledged state or dismisses (per fixture). No network.
- **"Do this always"** on a receipt → toast "Added to Automation · created by your agent". (Automation tab itself is out of scope for this page.)
- **Undo / Stop it** → toast confirming reversal.
- **Right / Fix** on a learned fact → toast; `Fix` opens a stub input affordance (can be a toast for this build).
- **Checklist toggle** → updates completion count, persists in local component state for the session.
- **"Why this?" / "Show data"** → opens the **Report sheet** (§6), which is the universal evidence surface.

All toasts, transitions, and the local-state model are part of this build. The **contract** (what a real accept would POST) is documented in §7 but not called.

---

## 5. Room stratum — detailed spec

### 5.1 Header (above the hero, not part of either stratum's content)

- **Left:** room label ("Bedroom Air · Gurugram") + **outdoor** reading: value, "outside", and a **freshness stamp** ("· 38 min ago"). Outdoor numbers are periodic and **must always display their age**; never present a stale outdoor number as live.
- **Right:** a weather pill (temp + condition) and the **notification bell** (§8) with an unseen-count badge.

### 5.2 The hero

- **Isometric room render** (inline SVG in the prototype; keep as a component that accepts `tone` + `aqi`). Recolors per state accent — aqua ripples on calm days, full coral tint with the badge reading the spike value during `liveEvent`.
- **AQI badge** pinned to the room: small, subordinate to the score. (Sizing already tuned in S3 — do not enlarge it back to overpowering the score.)
- **Large Room Quality Score numeral** in the reserved left column, with a kick-label ("Room quality"), a live dot, and a short sub-label ("sealed night", "live · 2:18 pm").
- **Hero headline + body**, which vary by state: either a **narrative sentence** (recap/event/season) or a **"what I'm watching" list** of timed rows (calm/evening). The state defines which.
- **Score footer:** a **confidence chip** (`full`/`soft`, colored dot) on the left, a **"Today's report ›" cue** on the right. The entire hero is tappable → opens the Report sheet.

The ring is **not** on Home in S3 — it survives only inside the report. Keep it out of the hero.

### 5.3 Room-stratum extras (state-dependent, still "about the room")

Content that describes the room's own history/status lives above the divider even though it's card-like:

- **Overnight "air defended" card** (`morningRecap`): outside-peak vs room-held, a sparkline, deep-links into the night segment of the report.
- **Streak** (`morningRecap`): "11 nights under AQI 50."
- **Next-up rail** (`morningRecap`): upcoming moments (tonight's sleep mode, filter check, season start).
- **Blind-spot strip** (`calmDay`): "I only sense the bedroom…" → the evidence-based second-sensor case. **n=1 only.**

---

## 6. The Report (drill-in) — spec

The Report is a **drill-in, never a tab.** It is **one component, windowed** — the same screen renders today (live), a past day (paged), and holds the night as a segment.

### 6.1 Two entry points, one screen

1. **Tap the Room Quality Score / hero on Home** → contextual "why is it this?"
2. **A standing "Today's report" row on the Device tab** → habitual "just show me the numbers." *(The Device tab is out of scope for this build, but the Report component must be built so a second entry point can open it with no changes — i.e. it is a self-contained sheet, not coupled to Home.)*

Both open the identical live screen. Decision locked: the Device entry reads **"Today's report"** (live), matching the Home score-tap, so there's never a "which report did I get?" ambiguity.

### 6.2 Windowing (the night is a chapter of the day, not a rival)

- Default view: **Today**, live, midnight → now.
- **"Last night · the sealed window"** is a **labeled violet segment inside today's report** — simultaneously reachable directly from the overnight card on Home. It is not a separate night-vs-day toggle.
- A **date-pager** ("‹ Today · Tue 5 Aug ›") walks backward through history; a past day renders the same layout, closed instead of live.

### 6.3 Report contents (dense — this is where the reference-app density lives)

- **Score + narrative summary** for the windowed day (ring reappears here).
- **Metric-chip selector:** PM2.5 · VOC · Temp · Noise — switches the timeline's series.
- **Live day timeline** with a night band, a **power-saver band**, and a **peak marker**.
- **Last-night segment** (violet) with its own mini-timeline.
- **Contributor breakdown:** one row per contributor — name, banded status label, raw value + unit, and a meter. This is the visible form of the §2.1 contract, including filter health. **Raw numbers live here, not on Home.**
- **Energy / from-your-history block:** the **fan-effort-vs-air-need chart** — two lines (effort vs. need), the gap = wasted electricity, explicitly captioned as the basis for the power-saver proposal.
- A closing note that the weekly summary (§9) also lands here, and that as rooms are added each gets its own report with a Home roll-up (same layout, one more level).

---

## 7. Data model & contracts (build to these types; fill with fixtures)

Define these as TypeScript types/interfaces in the front-end. The fixture is the single source of screen data; swapping to a real API later means replacing the fixture loader, nothing else.

```ts
type Band = 'good' | 'moderate' | 'bad' | 'unavailable';
type Confidence = 'full' | 'soft';
type StateKey = 'dayOne' | 'morningRecap' | 'calmDay' | 'eveningPlan' | 'liveEvent' | 'seasonPrep';
type Accent = 'aqua' | 'amber' | 'coral' | 'violet';

interface Contributor {
  key: 'pm25' | 'voc' | 'humidity' | 'noise' | 'filter';
  label: string;
  rawValue: string;      // pre-formatted, e.g. "AQI 34 · 9 µg/m³"
  band: Band;
  weight: number;        // 0..1, weights of present contributors sum to 1
  subScore: number;      // 0..1
}

interface RoomQualityScore {
  value: number;         // 0..100
  confidence: Confidence;
  confidenceReason: string; // "sealed overnight" | "door open since noon" | ...
  contributors: Contributor[]; // may omit a contributor → renormalized; UI shows 'unavailable' row in report
}

interface OutdoorReading {
  aqi: number;
  category: string;      // "Moderate" | "Unhealthy" | ...
  ageMinutes: number;    // drives the freshness stamp; UI must render this
  stale: boolean;        // if true (e.g. >3h), UI degrades per copy
}

interface RoomRender {
  aqi: number;           // live indoor AQI shown on the badge
  tone: Accent;          // recolors the render
}

type CardKind =
  | 'proposal' | 'receipt' | 'liveAction'
  | 'learnedFacts' | 'checklist' | 'guide' | 'blindSpot';

type DetectorClass =
  | 'externalForecast' | 'recurringPattern' | 'energy'
  | 'predictiveMaintenance' | 'comfort' | 'standingGoal' | 'onboarding' | 'none';

interface Action {
  id: string;
  label: string;
  variant: 'primary' | 'warm' | 'default' | 'ghost';
  effect:                     // resolved locally in this build
    | { type: 'toast'; message: string }
    | { type: 'openReport' }
    | { type: 'openReportSegment'; segment: 'night' | 'energy' }
    | { type: 'dismissCard' }
    | { type: 'toAutomation'; message: string };
}

interface Card {
  id: string;
  kind: CardKind;
  detector: DetectorClass;
  zone: 'needsYourCall' | 'liveNow' | 'doneToday' | 'comfort' | 'learned' | 'checklist' | 'worthKnowing' | 'beyondRoom';
  stratum: 'room' | 'agent';  // enforce the split
  statusTag?: string;         // "Proposed" | "From your history" | "Running" | "Done" | ...
  source?: string;            // provenance line, e.g. "14 afternoons", "forecast + 21 nights"
  title: string;
  body: string;               // supports simple <b>/<i> emphasis
  actions?: Action[];
  // kind-specific payloads:
  facts?: { text: string; sub: string }[];       // learnedFacts
  items?: { text: string; sub: string; done: boolean }[]; // checklist
  progress?: number;          // liveAction, 0..1
  meta?: Record<string, string | number>;        // sparkline data refs, band positions, etc.
}

interface EmptySlot {
  zone: Card['zone'];
  copy: string;               // written, never blank
}

interface HomeState {
  key: StateKey;
  accent: Accent;
  clock: string;              // status-bar time in the mock
  outdoor: OutdoorReading;
  weather: { temp: string; condition: string };
  room: RoomRender;
  score: RoomQualityScore;
  hero: {
    headline: string;
    dim?: string;             // the muted continuation of the headline
    mode: 'narrative' | 'watchlist';
    narrative?: string;
    watch?: { when: string; text: string }[];
  };
  roomExtras?: Card[];        // overnight card, streak, rail, blindSpot (stratum: 'room')
  agentCards: Card[];         // stratum: 'agent'
  emptySlots?: EmptySlot[];
  unseenNotifications: number;
}

interface HomeFixture {
  activeState: StateKey;      // which state renders; dev control can override
  states: Record<StateKey, HomeState>;
  report: ReportFixture;      // §6 data
  notifications: NotificationFixture; // §8 data
}
```

**Fixture requirements:**

- All six `states` populated, matching the S3 prototype's copy and numbers.
- At least one state whose `score.contributors` **omits** a contributor, to exercise the renormalization + `unavailable` report row.
- Every `DetectorClass` in §4.2 represented by at least one card.
- Every `EmptySlot` carries real written copy.
- The `report` fixture includes today's timeline series for all four metric chips (can be simple point arrays), the night segment, the contributor breakdown, and the two-line energy series.

---

## 8. Notification bell & feed

The bell (header, room stratum) opens a **day-grouped historical feed**. **A notification is not a new object type** — it is a **delivery channel that replays existing objects** (proposals, receipts, live alerts, weekly digests), each **deep-linking back to its card/report**. This doubles as the agent's audit log — glass-box for free.

- **Feed rows** are grouped by day (Today / Yesterday / Sunday / …), each with an icon by type (proposal ✦ · done ✓ · alert ! · digest ◷), title, timestamp + type label, and an unseen dot.
- **Deep links:** tapping a row invokes the object's effect (open report, open the relevant proposal, etc.) — same `Action.effect` vocabulary as §7.
- **Unseen badge** count on the bell mirrors `unseenNotifications`.
- **Copy to include** (non-functional, but render it): quiet hours follow the learned sleep window; 90-day retention; per-category toggles exist in settings (settings screen out of scope).

`NotificationFixture`: an ordered list of `{ id, day, kind, title, timestamp, unseen, effect }`.

---

## 9. Weekly summary (render the touchpoints, generation out of scope)

The weekly summary is a **separate generated, pushed object** (contrast with the pulled daily report). For this build, it appears as:

- a **feed row** in the bell ("Your week in air…", Sunday), and
- a note in the Report that it archives into report history.

The full Sunday-hero variant and its generation are **not** in this build; do not create a seventh state. Just ensure the two touchpoints above render from fixture data.

---

## 10. Multi-device mode (build the seam, not the second mode)

The layout has **two modes**, switched at **2+ devices**: single-room (this build) → multi-room (tile grid, room comparisons, whole-home roll-up). **Only single-room ships now.** But structure the code so mode is a branch, not a rewrite:

- Gate the **blind-spot strip** and all single-room-only copy behind a `deviceCount === 1` check.
- Keep the score component agnostic to whether it's showing a room score or a home roll-up (at n=1 they're identical).
- Do not hard-code "Bedroom" as the only possible subject; the room label is data.

No multi-room UI is required in this build — just the seam.

---

## 11. Visual system

- **Stack:** React + Tailwind (matches the prototype). Single-page; no router required for this page (the sheets are in-component overlays).
- **Type:** Fraunces (display/headlines/score numeral), Inter (body/UI), JetBrains Mono (labels, numbers, timestamps).
- **Palette (dark "Air Agent" language):** page `#0c0e12`, card `#11151d`, ink `#eef1f0`, sub `#8b93a0`, faint `#565e6c`; accents aqua `#7ee0c8`, amber `#f2a03d`, orange `#e2872f`, coral `#e8684a`, violet `#7c8ae0`. Accent is state-driven via a CSS variable.
- **AQI color mapping:** good → aqua, moderate → amber, USG → orange, unhealthy → coral. Apply consistently to badge, score numeral, and report values.
- **Agent-stratum spine:** each agent card has a left accent border (aqua; coral for live) so the stratum reads mid-scroll.
- **Motion:** state transitions fade; the live dot breathes; **respect `prefers-reduced-motion`** (disable the breathing + fades). Already handled in the prototype — preserve it.
- **Phone frame** and the desktop "slot map" side panel from the prototype are a **demo harness, not product** — the shipped app is the phone screen. Keep the slot map only behind a dev flag if convenient; it is not required.

### Accessibility (carry over from prototype, non-negotiable)

- The hero and every actionable card are keyboard-focusable with visible focus rings and Enter/Space activation.
- Sheets close on Esc.
- The room render carries an `aria-label` including the live AQI.
- Color is never the only carrier of the band status — always pair with a text label ("Good", "Dry", "62% used").

---

## 12. Component inventory (suggested decomposition)

```
<MyHomePage>                     // owns active-state selection + fixture load
  <StatusBar/>
  <Header>                        // room label, outdoor+freshness, weather, <Bell/>
  <RoomStratum>
    <Hero>                        // <IsoRoom tone aqi/> + <ScoreBlock/> + headline + (Narrative | WatchList) + <ScoreFooter/>
    <RoomExtras>                  // OvernightCard | Streak | NextUpRail | BlindSpot (state-driven)
  <StratumDivider/>              // the ✦ "your agent" line
  <AgentStratum>
    <Zone>*                       // renders Cards (or EmptySlot copy) by zone, in fixture order
      <ProposalCard/> <ReceiptCard/> <LiveActionCard/>
      <LearnedFactsCard/> <ChecklistCard/> <GuideCard/>
  <TabBar/> + <AIBubble/>        // My home active; Device/Automation inert stubs
  <ReportSheet/>                  // §6, self-contained, opens from hero OR external caller
  <NotificationSheet/>           // §8
  <Toast/>
  <DevStateSwitcher/>            // dev-only: pick activeState (mirrors prototype's chips + keys 1–6)
```

`DevStateSwitcher` replaces the prototype's masthead/switcher for testing all six states; it must be trivially removable/flag-gated for a production build.

---

## 13. Acceptance criteria

The build is done when:

1. All **six states** render faithfully from the fixture, switchable via the dev control (and keys 1–6), each matching the S3 prototype's layout, copy, numbers, and accent.
2. The **two-strata split** is structural: room content and agent content live in distinct regions; agent cards show the spine; **no action buttons appear in the room stratum**.
3. The **hero** shows the isometric room, the subordinate AQI badge, and the large score with correct confidence chip; tapping anywhere on the hero opens the Report.
4. The **Report sheet** opens from the hero and from a simulated external caller; renders today's live timeline with night + power-saver bands and peak marker, the violet night segment, the full contributor breakdown (including a `filter` row), the metric-chip selector, and the two-line energy chart; the date-pager is present.
5. The **contributor renormalization path** is visibly exercised by at least one state (a missing contributor → `unavailable` row, score still sane).
6. **All six detector classes** from §4.2 appear as cards, including the **power-saver proposal + its receipt + its report chart**.
7. The **bell** shows the unseen count, opens the day-grouped feed, and rows deep-link via the `Action.effect` vocabulary (report/proposal/etc.).
8. **Empty slots render written copy**, never blanks or spinners.
9. All **card actions resolve locally** (toasts / transitions / Automation toast) with no network calls; the POST-shape contract is documented in types but uncalled.
10. **Single-device gating** is in place (blind-spot strip behind `deviceCount === 1`); the room subject is data-driven, not hard-coded.
11. **Accessibility**: keyboard focus + activation on hero and cards, Esc closes sheets, reduced-motion respected, band status always has a text label.
12. **No `localStorage`/`sessionStorage`** or other browser-storage dependency; all state is in-memory React state for the session.

---

## 14. Explicitly out of scope for this build

- The score engine, detector pipeline, outdoor-AQI ingestion/cache, forecast pulls, fact store persistence — all mocked.
- The Device and Automation tabs (only inert tab stubs here) and the AI assistant behind the floating bubble.
- The multi-room (2+ device) layout mode (only the seam).
- The Sunday weekly-summary hero variant and its generation (only the two touchpoints).
- Settings screens (notification toggles, autonomy ladder, quiet-hours config) — referenced in copy only.
- Real authentication, real device pairing, real commerce/checkout for filter reorder.

---

## 15. Non-functional notes carried for the future backend (context, not this build)

Recorded so the front-end's contracts aren't accidentally designed against them:

- **Outdoor data is slow-moving and shared.** It will be fetched **server-side once per station/geohash and cached** (~hourly), never polled per client; forecasts pulled ~2×/day. The UI's `ageMinutes`/`stale` fields exist to honor this. **Indoor telemetry is genuinely live** (own MQTT, minute-level). The visible rule — "live indoors, periodic outdoors" — must survive into production; do not build the UI to imply live outdoor data.
- **Detectors run on schedules/events, not render.** The front-end must never assume a card implies a fresh computation happened at page load.
- The **energy detector** needs a fan-effort-vs-air-need history per device and a tariff/rate assumption for the ₹ figure; the report chart is the surface for both.

---

*End of PRD. Source of visual truth: `ding-home-states.html` (S3). Source of behavioral truth: this document.*
