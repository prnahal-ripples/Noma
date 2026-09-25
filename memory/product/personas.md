# Personas

> Canonical registry: `src/personas/personas.json` — if they disagree, the JSON wins.
> **The JSON is intentionally still unpopulated.** See the conflict below.

---

## ⚠ CONFLICT C-1 — two incompatible persona sets supplied

Two different persona sets arrived in the same handoff (2026-08-04). They are not
reconcilable by merging: different names, ages, counts, and framing. Per CLAUDE.md
rule 6 this is flagged, **not silently resolved**. Both are recorded below with
provisional IDs. `src/personas/personas.json` stays empty until the owner picks.

**Do not build persona-conditional logic, tone routing, or journey IDs against
either set until C-1 is closed** — `memory/voice/tone-matrix.md` and
`src/personas/prompts/` both depend on the outcome.

| | Set A | Set B |
|---|---|---|
| Count | 2 | 4 |
| Framing | demographic archetypes | role + priority tier + jobs-to-be-done |
| Depth | traits only | JTBD, tiering, named product features |
| Names | Kartik, Siddharth | Asha, Ravi & Lakshmi, Household Help, Priya |
| Deck accent | — | orange (`#D95E2B`-ish), not green |

**Assessment (owner decides, not us):** Set B is materially more developed — it
carries priority tiers, jobs-to-be-done, and references live product surfaces
(*Faces You Trust*, *Home Score*, in-app *Shop*, AQI thresholds). Set A reads as
earlier or from a different deck. Set B also covers a case Set A misses entirely:
**a low-fluency resident user**, which has real accessibility consequences for
type size and control targets.

### ⚠ 2026-08-04 — the PM prototypes corroborate Set B

Reading the four supplied prototypes (`docs/index.md`) produced independent evidence.
This does **not** close C-1 — the prototypes could have been built from a superseded
brief — but anyone waiting on the decision should know which set the product was
actually built against.

| Evidence | Where |
|---|---|
| **Ravi** and **Lakshmi** appear as real named people in the camera event feed — "Person recognised: Lakshmi", "Ravi arrived home" | launch app, `FACE_EVENTS` |
| **Faces You Trust** exists as a built feature with Known / Verified / Review badges and a DPDP consent gate | `FaceTagSheet`, `CameraLiveView` |
| **Home Score** exists as a weighted five-dimension model | `SCORE_DIMS`, `ScoreDetailScreen` |
| **Shop** exists with contextual, AQI-triggered upsell | `ShopTab`, home air map |
| **AQI thresholds** drive real UI ("AQI hit 187") | throughout |
| P3's *household help* maps exactly onto the `staff` role — "Maid, driver, caretaker — time-limited, assigned devices" | `ROLES` |
| Low-fluency residents are designed for — the deck's room views are built around kids and grandparents | strategy deck |
| **Set A's names (Kartik, Siddharth) appear nowhere in any of the four documents** | — |

Every product surface Set B names turned out to be real and built. That is four for four.

One caution: the prototypes also introduce **more** names — *Kaustubh* (homeowner),
*Arjun* (child), *Maa* (elder, in agent dialogue). These are consistent with Set B's
role-based household framing but are a third naming set. If Set B is ratified, its names
should be reconciled with the prototypes' rather than assumed identical.

---

## Set B — role-based (4) · provisional IDs P1–P4

### P1 · Asha — The Remote Guardian
`PRIMARY · BUYER · POWER USER`

32, product manager in Bangalore. Her parents live in a separate home that she
manages remotely. AQI-anxious, security-conscious, time-poor. Comfortable with
tech and willing to pay for peace of mind.

**Jobs to be done.** Know her family and homes are safe and breathing clean air
without checking six apps; act instantly when something's wrong.

> Design consequence: she is the buyer *and* the power user, so she absorbs
> depth — but she is time-poor, so depth must be opt-in, never the default view.

### P2 · Ravi & Lakshmi — Parents at Home
`SECONDARY · RESIDENT USERS`

Early 60s, living in the home Asha manages. Lower app fluency. Want things to
"just work" — door locks itself, air stays clean — with minimal interaction and
**large, legible controls**.

> Design consequence: this persona sets a hard floor on type size and touch
> targets. A calm, sparse layout (per `ma`) serves them directly. Any flow that
> *requires* app fluency to stay safe is a defect.

### P3 · The Household Help
`TERTIARY · TIME-BOXED ACCESS`

Maid, cook, or delivery agent needing scoped, temporary entry. Should be
recognised (*Faces You Trust*) or granted limited access — **never full account
control**.

> Design consequence: access is scoped and expiring by default. This is a
> permissions-model requirement, not a UI preference.

### P4 · Priya — The Prospective Owner
`ACQUISITION · IN-APP SHOPPER`

Owns one Ding camera, considering more. Browses the in-app Shop, sees contextual
upsell ("add a purifier — your AQI hit 187"). The funnel from one device to an
ecosystem.

**Jobs to be done.** Understand what each device adds to her Home Score; buy
confidently within the app she already trusts.

> Design consequence: monetisation is contextual and data-triggered. Ties to
> `memory/analytics/monetization-map.md`. Upsell must not compromise the calm —
> and must not consume the 10% accent budget that the primary CTA needs.

---

## Set A — demographic archetypes (2) · provisional IDs A1–A2

### A1 · Kartik — The Independent Professional
Age 26. Tech-savvy · early adopter · future-ready · automation-friendly ·
appreciates clean design.

### A2 · Siddharth — The Family Provider
Age 35. Practical · security-minded · family-first · trust-focused ·
long-term thinker.

---

## Product surfaces named in persona material

Captured here because they are the first concrete feature signal received. Not
yet specified anywhere — each needs a PRD in `docs/features/`.

| Surface | Evidence | Belongs to |
|---|---|---|
| **Home Score** | P4 — "what each device adds to her Home Score" | needs `F-*` ID |
| **Faces You Trust** | P3 — recognition-based scoped entry | needs `F-*` ID |
| **Shop** (in-app) | P4 — contextual, AQI-triggered upsell | monetization-map |
| **AQI monitoring** | P1, P4 — "AQI hit 187" | devices.json |
| Door locks, cameras (Ding), purifiers, wearables | P1–P4 | devices.json |
