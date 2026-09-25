# Scope Ledger

> What is in, what is out, and what was found missing. Derived from the PM prototype set,
> 2026-08-04. Feature IDs: `src/hardware/feature-map.json`.

---

## In scope — built as prototypes

Every item below exists as a working screen in at least one prototype. **"Prototyped" is
not "specified"**: zero PRDs exist, and `docs/features/` is empty.

| F-* | Feature | Confidence |
|---|---|---|
| F-AQI-LIVE | Live air quality | high — appears in all four docs |
| F-FILTER-HEALTH | AQI-weighted filter health | high on intent, **zero on method** (C-7) |
| F-AGENT-PROPOSE | Agent proposals + graduated autonomy | high — most developed idea in the set |
| F-AUTOMATIONS | Automations and routines | high |
| F-FACES | Faces You Trust | medium — consent flow designed, declined state not |
| F-HOME-SCORE | Home Score | **blocked** — four incompatible definitions (C-5) |
| F-SHARING | Household sharing | **blocked** — three role models (C-3) |
| F-SHOP | In-app shop and reorder | catalogue only; no transaction |
| F-WEEK-RECAP | Air Week recap + share | high |
| F-NEIGHBOURHOOD | Neighbourhood comparison | **blocked** — privacy (C-10) |
| F-ENERGY | Energy and running cost | medium — depends on an unstated tariff |
| F-AIR-MAP | Home air map | medium — sensorless rooms unexplained (C-9) |
| F-WEARABLE-BRIDGE | Wearable bridge | **blocked** — health-adjacent (C-8) |

## Explicitly on the roadmap, not now

From the strategy deck's "more coming": smart lights (circadian, presence-aware), music
system (multi-room, routine-aware), water sensors, door sensors, smoke detectors.

Also mentioned but unscoped: elder monitoring and check-ins, routine-intelligence alerts,
annual home health report, doorstep filter cleaning (all top-tier subscription features).

## Out of scope — deliberately not designed

Third-party ecosystems (Alexa/Google/HomeKit/Matter) are **absent from every document**.
For a 2026 connected-home product this is a conspicuous silence rather than an obvious
exclusion — worth confirming it is a decision, not an oversight.

---

## Found missing — real gaps, not nitpicks

Ordered by how much they block shipping.

| Gap | Consequence |
|---|---|
| **Payment / order flow** | `F-SHOP` is the recurring-revenue path and stops at a price tag |
| **Analytics** | A named seven-day retention strategy with no way to measure it |
| **Offline / device-unreachable** | No degraded state, though a notification says "camera went offline briefly" |
| **Filter fully exhausted** | Predictive path designed; failure path not |
| **Declined-consent state** | Face recognition is declinable; nothing shows what a declined camera does |
| **Zero-device Home Score** | Promised in onboarding slide 4, before any device is paired |
| **Account deletion / data export** | A DPDP obligation with no surface |
| **Proposal expiry** | "Later" and "Not tonight" exist; what happens if ignored does not |
| **Agent safety classes** | Nothing stops "Act silently" from applying to a lock or a purchase (C-8) |
| **Multi-home** | Data structure exists, no flow — and persona P1 is defined by managing a second home |
| **Empty, loading, error states** | Absent throughout. Every prototype shows the happy path with seeded data. |

---

## Scope risk worth naming

The material spans **two different products**: a focused air-purifier companion (Week One,
Air Agent) and a whole-home platform with cameras, locks, vacuums, lights, music and a
subscription (strategy deck, launch app).

The purifier story is deep and evidence-backed. The platform story is broad and mostly
asserted. They are not incompatible — one-device-to-ecosystem is the stated funnel — but
they imply very different first releases, and **nothing in the material says which one
ships first.** That is the largest open product question here, and it is upstream of most
of the conflicts in `memory/decisions.md`.
