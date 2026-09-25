# NOMA v1 — Product Requirements

| | |
|---|---|
| **Status** | **DRAFT — needs a scope ruling before it can be approved** (see §1) |
| **Version** | 0.1 · 2026-08-04 |
| **Author** | Compiled from all material supplied to date |
| **Canonical sources** | `src/tokens/*`, `src/hardware/*`, `memory/**` |
| **Decision log** | `memory/decisions.md` — ADR-001…005, conflicts C-1…C-13 |
| **Provenance** | Four PM prototypes (`docs/index.md`), the Airbnb visual reference, an owner-supplied typeface, two green revisions, and a motion ruling |

> **How to read this.** Everything here traces to something supplied. Where the
> sources disagree, the disagreement is stated rather than resolved — thirteen
> such conflicts are open, four of them blocking. Nothing in this document was
> invented to fill a gap; gaps are marked **GAP**.

---

## 1. The decision this PRD is waiting on

The supplied material describes **two different products**:

| | **A · Air companion** | **B · Whole-home platform** |
|---|---|---|
| Anchor | One air purifier | Purifier + cameras + locks + vacuums + doorbells |
| Evidence | Deep. A day-by-day retention arc with stated research findings and an articulated agent architecture. | Broad but mostly asserted. ~60 prototype screens, a subscription deck, no research behind the claims. |
| Revenue | Hardware + filters | Hardware + filters + ₹699/₹1,199 subscription |
| Open conflicts | 6 | 13 |

**Recommendation: ship A, architected for B.** The purifier story is the only part
of the material that *argues* rather than asserts — it has research findings, named
behavioural mechanisms, and a chokepoint. The platform story has more screens but
less conviction, and it carries most of the unresolved conflicts (roles, score,
subscription, pricing). Build A's data model as a subset of B's so nothing has to
be thrown away.

**This is the owner's call, and everything below is scoped to A unless marked
`[B]`.** Until it is ruled, teams will build against different assumptions.

---

## 2. Problem and insight

> "You can't see what you breathe."

An air purifier is a box that hums. When it works, nothing visibly happens — and
the material is blunt about the consequence:

> **Invisible protection that runs silently is, to the user, indistinguishable
> from a switched-off box.**

That is the whole problem. In Indian homes it compounds: people switch purifiers
*off* to save electricity, losing the benefit they paid for, because the cost is
visible and the protection is not.

**The insight this product is built on:** *air is invisible, so perceived value is
whatever the app makes visible.* Perceived value is therefore a **design output**,
not a hardware output. That single sentence justifies the entire seven-day arc in §7.

---

## 3. Users

> ⚠ **BLOCKED BY C-1.** Two incompatible persona sets were supplied.
> `src/personas/personas.json` is deliberately empty. The set below (B) is used
> throughout this PRD because the prototypes corroborate it four ways — Ravi and
> Lakshmi appear as named people in the camera feed, and all four product surfaces
> Set B names are built. Set A's names appear nowhere. **Still the owner's ruling.**

| ID | Persona | Tier | What they need | Design consequence |
|---|---|---|---|---|
| **P1** | **Asha**, 32, PM in Bangalore. Manages her parents' separate home remotely. | Primary · buyer · power user | Know her family is safe and breathing clean air without checking six apps | Buyer *and* power user, so she absorbs depth — but she is time-poor, so depth is opt-in, never the default view |
| **P2** | **Ravi & Lakshmi**, early 60s, living in the home Asha manages | Secondary · resident | Things that just work. Large, legible controls. | **Sets a hard floor on type size and touch targets.** Any flow that *requires* app fluency to stay safe is a defect |
| **P3** | **The Household Help** — maid, cook, delivery | Tertiary · time-boxed | Scoped, expiring entry | Access is scoped and expiring *by default*. A permissions requirement, not a UI preference |
| **P4** | **Priya** — owns one device, considering more | Acquisition | To understand what a second device adds | Monetisation is data-triggered, and competes with the primary CTA for the accent budget (§13) |

**P2 is the accessibility constraint that binds the whole design.** A low-fluency
resident who cannot confirm the air is clean is a product failure, not an edge case.

---

## 4. Jobs to be done

Three return-drivers, in the priority the research gives them:

1. **Checking live AQI** — *the #1 stated reason users reopen an air-purifier app*
2. **Controlling it remotely** — a reason to open the app before you're home
3. **Trusting the automations** — carries the away-mode trap (§6)

Everything in v1 serves one of these three. A feature that serves none is out of scope.

---

## 5. Product principles

From `memory/product/vision.md`, derived from the name (*ma* 間 — the intentional
space between things):

- **Whitespace is a feature.** If a screen looks sparse that is likely correct. Density is the failure mode.
- **One idea per screen.** The primary action is findable in one glance.
- **Calm over informative.** Show the state of things, not every metric that produced it. Detail on demand, never volunteered.
- **Never volunteer alarm.** Urgency is earned by real events, not styling.
- **The emotional target is relief, not delight.** A glance that confirms everything is fine.

**Never:** make the accent green the ground · require app fluency for basic safety ·
use a raw metric as a headline · hide a trade-off.

---

## 6. The agent model — v1's core architecture

Full detail: `memory/architecture/ai-integration.md`. This is not a feature bolted
on; it determines what the app *is*. **Home is not a grid of devices — it is a list
of what the agent has decided, is proposing, or has already done.**

### 6.1 Three zones, in this order

| Zone | Contains |
|---|---|
| 1 · Settled now | What is already fine. Per-room readings. |
| 2 · Needs your call | Proposals awaiting a decision, with a count. |
| 3 · Done today | Completed actions, each still undoable. |

Ordering is load-bearing: **reassurance, then the ask, then the receipt.** Someone
opening the app anxious gets "air is clean in 2 rooms" before a decision.

### 6.2 Graduated autonomy — per capability, three levels

| Level | Behaviour |
|---|---|
| **Ask me** | Agent proposes. Nothing runs without a tap. **Default.** |
| **Act & tell me** | Agent acts, then reports. Undo remains. |
| **Act silently** | Agent acts without notifying. |

Granted **one capability at a time**, never globally. Promotion is offered on
evidence: *"You've accepted 7 fan suggestions in a row — ready to let this run
itself?"* — which makes a **per-capability accept/reject tally application state**,
not analytics.

> ⚠ **BLOCKED BY C-8.** Every capability shown is comfort-grade. Nothing prevents
> "Act silently" applying to a **lock**, and `Reorder filters` at that level is an
> **unattended purchase**. v1 must ship a capability **safety class** before any
> autonomy above "Ask me" is enabled.

### 6.3 The explanation contract — four fixed slots

Every proposal exposes "Why this?" with the **same four slots, always in this order**:

| Slot | Job | Example |
|---|---|---|
| **Sensed** | The evidence | "Outdoor AQI 118 and climbing, forecast 182 by 10pm; bedroom holding at 38" |
| **Decided** | The action | "Pre-clean 8:30–9:00 at medium, then hold windows-closed" |
| **Instead of** | The counterfactual | "Reacting at 11pm — which would run loud while you sleep" |
| **Obeys rule** | The constraint respected | "Quiet hours 11pm–7am stays intact" |

**"Instead of" is the differentiating slot.** Naming what the agent chose *not* to
do is what makes a decision read as considered rather than arbitrary; most assistant
UIs ship the first two and stop. **"Obeys rule" is a promise** — ship without it and
standing rules become unverifiable.

### 6.4 Rehearsal before execution

A proposal previews as an **inert, editable timeline**. *Nothing happens until you
tap Run.* Steps derived from a standing rule render **`Locked`, not `Edit`** — a user
cannot casually edit away their own constraint from inside a one-off plan.

### 6.5 Standing rules

Persistent constraints that bound every future plan. Each states its **trade-off**
and anchors its unit to something human:

| Rule | Value | Copy |
|---|---|---|
| Quiet hours | 11pm–7am | referenced by name in "Obeys rule" |
| Noise ceiling asleep | 28 dB | "Lower is quieter but cleans slower. 28 dB is about a whisper." |
| Target overnight PM2.5 | under 12 | "The goal I'll hold the room to, not a one-time action." |

### 6.6 Promotion, reversal, isolation

- **"Do this always"** promotes an accepted one-off into a standing automation — and appears on *completed* items too, because the moment someone appreciates what it did is the moment to offer the upgrade.
- **Undo** stays on completed actions, including autonomous ones.
- The **chat thread is deliberately context-free**: *"this thread does not carry over anything from Home."* Ambient agent and conversational agent are separate sessions. Anyone reversing this must say why.

---

## 7. The Week One retention arc

The most specified thing in the material. Each day states an emotional target, the
research finding, and the screen that delivers it. **Day 7 → Week 2 is the named
retention chokepoint.**

| Day | Beat | Target emotion | Mechanism |
|---|---|---|---|
| 1 | The Reveal | Quiet shock | First reading is *your* room vs the street, already cleaning. **No feature tour.** |
| 2 | The Proof | Reassured | Morning "Air Defended" card: outdoor 187 → indoor 22, plus wearable SpO₂ `[B]` |
| 3 | The Habit | Hands-off | Three routines from observed use, one-tap accept + remote control + geofence |
| 4 | The Neighbourhood | A little proud | "Cleaner than 82% of your street" + one-tap share ⚠ C-10 |
| 5 | The Worth | Anxiety resolved | ₹164 saved vs always-Turbo, then "trees' worth of clean air" |
| 6 | The Gap | Curious | Home air map shows unprotected rooms; filter health + reorder |
| 7 | The Score | Sealed in | Air Score /100, shareable, Week-2 hook (pollen / Diwali) ⚠ C-5 |

**The night-hook → morning-proof pair (D1→D2) is the single most important
structure in the product.** It converts a silent box into something worth checking.
**Never ship one without the other.**

> ⚠ **The entire arc is push-dependent.** A notification-permission denial at
> `J-ONBOARD-06` silently kills days 1–7 with no other signal changing. This is the
> highest-leverage thing to measure (§14).

---

## 8. Scope

### In — v1
| F-id | Feature | Notes |
|---|---|---|
| `F-AQI-LIVE` | Live air quality, per room | The #1 return-driver. Everything sits on it. |
| `F-AGENT-PROPOSE` | Agent proposals + graduated autonomy | §6. Ship at "Ask me" only until C-8 is ruled. |
| `F-FILTER-HEALTH` | AQI-weighted filter health | Differentiator *and* revenue. ⚠ C-7 — no formula exists. |
| `F-AUTOMATIONS` | Routines, agent- and user-created | Templates: clean before wake, boost when cooking, pause when out |
| `F-WEEK-RECAP` | Air Week recap + share card | Bridges the D7→W2 chokepoint |
| `F-ENERGY` | Running cost, reframed as saving | Answers the bill anxiety that suppresses usage |
| `F-AIR-MAP` | Home air map | ⚠ C-9 — shows AQI for rooms with no sensor |
| `F-SHOP` | Filter reorder | ⚠ No payment flow exists anywhere |

### Out — v1
Cameras, locks, vacuums, doorbells, lights, music `[B]` · Faces You Trust `[B]` ·
Home Score `[B]`, ⚠ C-5 · household sharing `[B]`, ⚠ C-3 · subscription `[B]`,
⚠ C-13 · neighbourhood comparison ⚠ C-10 · wearable bridge ⚠ C-8 ·
third-party ecosystems (Alexa/Google/HomeKit/Matter — **absent from all four
documents; confirm this is a decision, not an oversight**)

### GAP — designed nowhere, required for v1
Payment & order flow · offline / device-unreachable · filter fully exhausted ·
declined-consent state · zero-device Home Score · proposal expiry · account
deletion & data export (a DPDP obligation) · **empty, loading and error states
throughout** — every prototype is a happy path with seeded data.

---

## 9. Hardware and sensing

Canonical: `src/hardware/devices.json`. **All specs are `prototype-only` — nothing
checked against a datasheet or BOM.**

| HW-id | Model | Coverage | CADR | Filtration |
|---|---|---|---|---|
| `HW-PUR-200` | Air Pro 200 | up to 280 ft² | 240 m³/hr | HEPA H13 |
| `HW-PUR-500` | Air Pro 500 | up to 550 ft² | 400 m³/hr | HEPA H13 + carbon |
| `HW-PUR-MAX` | Air Pro Max | up to 900 ft² | 600 m³/hr | Dual HEPA H13 |

**Sensing.** On-device **QSensAI laser particle sensor** — PM2.5 (headline), PM10,
NO₂, O₃, plus VOC (qualitative), humidity, temperature. Outdoor values blended from
the **nearest CPCB station**. ⚠ The blend algorithm is specified nowhere, and every
indoor-vs-outdoor number — the product's core emotional beat — depends on it.

**Connectivity.** BLE pairing, **Wi-Fi 2.4 GHz only**. Setup **hides the 5 GHz SSIDs
the device cannot join** rather than listing them and failing — this removes the
single most common smart-home setup failure and must be preserved.

**Modes.** ⚠ **BLOCKED BY C-4** — three incompatible vocabularies exist
(`Auto/Turbo/Silent/Eco` · `Auto/Sleep/Turbo/Manual` · `Quiet/Standard/Turbo/Max`).
**"Turbo" is the only value present in all three.** No mode UI or mode-naming copy
can be finalised until this is ruled.

---

## 10. The differentiator — and its missing spec

**AQI-weighted filter life, not clock-counted hours.** Competitors count runtime, so
three months in Delhi's winter and three months in Mumbai's monsoon return the same
score. NOMA weights every hour by the particulate actually absorbed.

| Same filter, same hours | Real AQI | Competitor says | NOMA says |
|---|---|---|---|
| Delhi NCR, winter | 287 | 72% | **38%** |
| Mumbai, monsoon | 94 | 72% | **64%** |

Identical hardware, identical runtime, **26 points apart**. That gap is the product.

> 🔴 **BLOCKED BY C-7 — the most serious gap in this PRD.** There is a worked
> example and a stated effect ("3–5× more particulate above AQI 200") but **no
> formula, no coefficients, and no validation data.** This is a marketing claim
> awaiting an engineering model. It gates `F-FILTER-HEALTH`, which is simultaneously
> the differentiator *and* the recurring-revenue lever. **Nothing else in v1 is
> worth as much as closing this.**

---

## 11. Privacy and compliance

Stated repeatedly and specifically: **on-device AI · DPDP Act 2023 compliant · your
data never leaves home.** Face data (if `F-FACES` ever ships) is on-device only,
gated by explicit consent citing the Act by name.

> 🔴 **BLOCKED BY C-11.** Three features cannot work locally: CPCB outdoor blending,
> forecast-driven pre-clean, and neighbourhood comparison. **"Never leaves home" and
> "uses tomorrow's forecast" cannot both be literally true.**
>
> The claim probably means *personal and biometric data stays local; ambient public
> data is fetched* — defensible, and still a strong position. **It must be narrowed
> to that before it reaches store copy or a privacy policy.** As written it is a
> compliance exposure, and it also blocks the analytics taxonomy (§14), because an
> analytics SDK is by definition exfiltration.

Also required and unaddressed: **consent is per-feature, not per-app** — declining
face recognition must leave a working camera, and no declined state is designed.

---

## 12. Monetization

| Line | v1 |
|---|---|
| Hardware | Purifier ⚠ **C-6 — priced ₹4,999 in the app and ₹8,999 in the deck** |
| Consumables | HEPA H13 filter ⚠ **C-6 — ₹1,299 or ₹1,499** |
| Subscription | `[B]` — deck only, no paywall in any prototype ⚠ C-13 |

**Filter health is the strategic centre.** Same data, opposite outcomes, decided by
*when* it is shown: surfaced late it becomes *"a 1-star 'it stopped working' review"*;
surfaced predictively it becomes a reorder that *"arrives before it runs out."*

**Upsell is data-triggered, never a pop-up** — *"the first upsell has to feel like
help."* Surfaces: air map (a second device), filter card (reorder), Week recap.

⚠ **C-13 is a positioning contradiction, not a pricing detail.** The free tier
promises "real filter health score" while Plus sells "AQI-weighted filter tracking" —
but AQI-weighting *is* what makes the score real. Both tier descriptions cannot be
honest.

⚠ **No payment gateway, address book, tax, invoice, refund or order tracking exists
in any prototype.** Every price is a tag with nothing behind it.

---

## 13. Design system — settled

This is the one area with no open conflicts. Canonical: `src/tokens/`.

| | Decision | ADR |
|---|---|---|
| Surfaces | Warm-neutral. `neutral` ramp carries text and structure; `sand` carries warmth. Splitting them keeps text contrast predictable. | ADR-001 |
| Cards | **Two anatomies, not alternatives** — elevated (r20, soft shadow, on warm) and outlined (r12, hairline, on white). Never combine border + shadow; never put an elevated white card on white. | ADR-001 |
| Type | **Google Sans Flex** (SIL OFL), variable. NOMA drives `wght` + `opsz`; scale is opsz-aware. | ADR-002 |
| Accent | **Moss `#4D6747`** (primary CTA) + **neon `#AEC799`** (status). **Budgeted at ~10% of any screen.** | ADR-003/004 |
| Motion | **Playful spring on discrete moments, still on ambient ones.** Bounce means "something happened"; stillness means "everything is fine". Exits never bounce; alarm never bounces; `prefers-reduced-motion` mandatory. | ADR-005 |
| Layout | 24pt screen gutter, 32pt section gap, 16pt card padding, 4pt base | tokens |

**Contrast, measured — one pairing is a trap:**

| Pairing | Ratio | |
|---|---|---|
| moss + white | 6.27:1 | AA (not AAA) |
| neon + `#222222` | 8.66:1 | AAA |
| **neon + white** | **1.84:1** | **FAILS — never ship** |

Neon looks like it should carry white text and doesn't. Always pair a green with the
`on*` token beside it.

**Accessibility floor (from P2):** minimum body 16pt, touch targets ≥44pt, and no
safety-critical state conveyed by colour alone.

**Open design items:** O-3 light theme only · O-5 **Google Sans Flex has no
Devanagari** despite an `hi` locale and Indian primary personas · O-6 **no semantic
status colours — green cannot carry "bad"**, which blocks real device-status UI ·
a hero-numeral type step is used on Device but is not in `typography.scale`.

---

## 14. Success metrics

> 🔴 **There are zero analytics events.** All four prototypes were searched for
> `track(`, `logEvent(`, `analytics`, `gtag`, `amplitude`, `mixpanel` — no matches.
> The product has a fully articulated seven-day retention strategy **and no way to
> measure any of it.** `src/analytics/events.schema.json` stays empty deliberately:
> a guessed machine-readable taxonomy is worse than an empty one.
>
> **Blocked by C-11** — the on-device privacy claim must be reconciled with
> telemetry *before the first event is named*.

Once unblocked, in priority order:

| # | Metric | Why |
|---|---|---|
| 1 | **Notification permission granted / denied** at `J-ONBOARD-06` | The whole Week One arc is push-dependent. A denial kills D1–D7 invisibly. |
| 2 | **D7 recap seen → returned in week 2** | *The* retention number. Every other Week One measure is diagnostic for this one. |
| 3 | Agent **accept / defer / decline / undo** per proposal | Application state that doubles as the best measure of whether the agent is trusted |
| 4 | **Undo rate per autonomy level** | The honest signal that "Act silently" was granted too early. Nobody has asked for this yet. |
| 5 | "Why this?" expansion rate | Whether explanation is load-bearing or ignored |
| 6 | Filter surfaced → reorder tapped → **purchased** | Revenue funnel. Cannot close today — no payment flow. |
| 7 | 2.4 GHz connect success at `J-PAIR-PUR-02` | Validates the 5 GHz-hiding decision |

**Hard constraints:** no face, identity or biometric value may ever be an event
property · wearable SpO₂/sleep are health data · every event must cite a `J-*` step.

---

## 15. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| **C-7** — the differentiator has no engineering model | 🔴 Critical | Get a filter-decay spec before building `F-FILTER-HEALTH`. Do not ship the claim without it. |
| **C-11** — privacy claim vs three networked features | 🔴 Critical | Narrow the claim to personal/biometric data before any store copy or policy. Unblocks analytics. |
| **C-8** — no safety class for autonomy | 🔴 Critical | Ship "Ask me" only. Classify capabilities before enabling silent action or unattended purchase. |
| **C-2** — five product/assistant names | 🟠 High | Rule the name. All copy, i18n, prompts and SKUs are downstream. |
| Push denial kills the retention arc | 🟠 High | Measure it first; design a no-push fallback for D1–D7 |
| No payment flow | 🟠 High | Recurring revenue is unreachable until this exists |
| Zero error/offline states | 🟠 High | Specify them per feature; the PRD template now requires it |
| **O-6** — green cannot signal "bad" | 🟠 High | Add semantic status colours before device-status UI |
| **O-5** — no Devanagari for the `hi` locale | 🟡 Medium | Pair a Devanagari face before `hi` ships |
| Prototype specs unverified | 🟡 Medium | Confirm CADR/coverage/pricing against a datasheet |
| Sources live in `~/Downloads` | 🟡 Medium | Vendor the prototypes into `docs/prototypes/` |

---

## 16. Open conflicts — nothing here is resolved

Full detail in `memory/decisions.md`.

| ID | Conflict | Blocks | Severity |
|---|---|---|---|
| C-1 | Two persona sets (prototypes corroborate Set B 4/4) | personas.json, tone routing, persona IDs on journeys | 🟠 |
| C-2 | Product + assistant have **five names** | all copy, i18n, prompts, SKUs | 🔴 |
| C-3 | Three role models for sharing | `F-SHARING` `[B]` | 🟠 |
| C-4 | Three fan-mode vocabularies | mode UI, automation actions, copy | 🟡 |
| C-5 | Four definitions of the Score | `F-HOME-SCORE` `[B]` | 🟠 |
| C-6 | Purifier ₹4,999 vs ₹8,999; filter ₹1,299 vs ₹1,499 | all pricing | 🟠 |
| C-7 | Differentiator has no formula | `F-FILTER-HEALTH` | 🔴 |
| C-8 | No safety class for autonomy | all autonomy above "Ask me" | 🔴 |
| C-9 | Air map shows AQI for sensorless rooms — and sells hardware on it | `F-AIR-MAP` credibility | 🟠 |
| C-10 | "Anonymised" comparison shows a surname + floor | `F-NEIGHBOURHOOD`, sharing, acquisition | 🟠 |
| C-11 | "Data never leaves home" vs three networked features | analytics taxonomy, store copy | 🔴 |
| C-12 | Two room-preset lists; only one has Pooja Room | onboarding, room creation | 🟡 |
| C-13 | Subscription sells the free tier's own claim | pricing page, tier copy | 🟠 |

---

## 17. Sequencing

**Before any build.** Rule the §1 scope question · C-2 (name) · C-7 (filter model) ·
C-11 (privacy vs telemetry) · C-8 (autonomy safety class).

**Then.** `F-AQI-LIVE` → `F-AGENT-PROPOSE` at "Ask me" → `F-FILTER-HEALTH` →
`F-AUTOMATIONS` → the D1/D2 push pair → `F-WEEK-RECAP` → `F-SHOP` with a real
payment flow.

**In parallel.** Per-feature PRDs from `templates/feature-prd.md` · the analytics
taxonomy once C-11 clears · empty/error/offline states · O-6 status colours ·
vendor the source prototypes.

---

## Declares

**Data** — `Home`, `Room`, `Device`, `Automation`, `Proposal`, `StandingRule`,
`AutonomyGrant`. New in v1: `AutonomyGrant.safetyClass` (required by C-8) and
`Proposal.expiresAt` (currently undefined behaviour). Detail:
`memory/architecture/data-models.md`.

**Events** — **none defined.** Blocked by C-11. Seven required metrics specified in
§14, deliberately unnamed so nobody ships them as a taxonomy. Canonical home when
unblocked: `src/analytics/events.schema.json`, each event citing a `J-*` step.

**Hardware** — `HW-PUR-200`, `HW-PUR-500`, `HW-PUR-MAX`, `HW-CONS-HEPA`.
Capabilities required: `indoor-particle-sensor`, `outdoor-aqi-feed`, `forecast-feed`,
`standing-rules-engine`, `audit-log`, `scheduler`, `payments` (does not exist).
Deferred to `[B]`: `HW-CAM-360`, `HW-BELL-PRO`, `HW-LOCK-X1/X2`, `HW-VAC-R1/R1P`,
`HW-WEAR-RING2`, `HW-WEAR-WATCH`.
