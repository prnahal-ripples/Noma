# Journey Step → Event Trigger Map

> Maps `J-*` steps (`memory/product/journeys.md`) to the telemetry each would need.
>
> ⚠ **Nothing in the right-hand column is registered.** `src/analytics/events.schema.json`
> is empty, and the prototypes contain zero analytics calls. The names below are
> **descriptions, not event names** — deliberately written as prose so nobody greps this
> file and ships them as a taxonomy. Naming is blocked on **C-11**
> (telemetry vs the on-device privacy claim). See `memory/analytics/event-taxonomy.md`.

---

## Onboarding — `J-ONBOARD`

| Step | What must be measurable | Why it matters |
|---|---|---|
| 01–02 | Slide reached, slide skipped | Slide 4 promises Home Score before a device exists |
| 03–04 | Phone submitted, OTP outcome | OTP failure is a hard acquisition leak |
| 05 | Home named | |
| 06 | Notification permission: primed → OS prompt → granted/denied | **The whole Week One arc is push-dependent.** A denial here silently kills J-WEEK-01…07. This is the single most consequential measurement in the product. |
| 07 | First device type chosen | Tells you whether the purifier is really the anchor |

## Pairing — `J-PAIR-PUR`

| Step | What must be measurable | Why |
|---|---|---|
| 01 | BLE discovery started / found / timed out | |
| 02 | Wi-Fi step reached, 2.4 GHz connect succeeded/failed | The 5 GHz-hiding decision claims to remove the most common setup failure. Unmeasured, that claim can't be verified. |
| 03 | Room preset chosen vs custom | Validates C-12 (which preset list is right) |
| 04 | First reading displayed, and the value | Day-0 value moment |

## Week One — `J-WEEK` (the retention spine)

Each day has a stated emotional target and mechanism, so each is a falsifiable claim.

| Day | Must be measurable | The claim being tested |
|---|---|---|
| 01 Reveal | First reading seen; indoor vs outdoor delta | "The first number must land as a gut-punch, not a spec" |
| 02 Proof | Morning card opened from push vs cold open | Narrating the overnight win prevents value evaporating |
| 03 Habit | Routines suggested → accepted (per routine); remote control used | "Better automations" + "remote control" are return-drivers #2 and #3 |
| 04 Neighbourhood | Compare card seen → share initiated → channel picked | Shareability converts a private utility into an acquisition channel |
| 05 Worth | Energy card seen | Bill anxiety is a usage-suppressor |
| 06 Gap | Air map seen → second-device interest; filter card → reorder tapped | The first upsell must feel like help |
| 07 Score | Recap seen → shared; **return on day 8–14** | Day 7 → Week 2 is *the* chokepoint |

**The one metric that matters most:** day-7 recap seen → returned in week 2. Every other
Week One measurement is diagnostic for this one.

## Agent — `J-AGENT`

This is the richest surface, and most of it is **application state that doubles as
telemetry** — the autonomy ladder is literally driven by a consecutive-accept tally.

| Step | Must be measurable |
|---|---|
| 01 | Proposal surfaced, with capability + trigger source |
| 02 | "Why this?" expanded — **the direct measure of whether explanation is load-bearing or ignored** |
| 03 | Rehearsal opened; any step edited |
| 04 | Run / Later / Not tonight — **and expiry, which has no defined behaviour yet** |
| 05 | Undo used, and how long after the action |
| 06 | "Do this always" accepted |
| 07 | Autonomy promotion offered → accepted / declined; later reverted |

Two things worth watching that nobody has asked for yet: **undo rate per autonomy level**
(the honest measure of whether "Act silently" was granted too early), and whether a
single rejection should reset the promotion counter.

## Sharing — `J-SHARE`
Invite sent → accepted; grant scope at creation; revocation; expiry lapse.
⚠ Blocked by C-3 (three role models) — role can't be a property until the model is settled.

## Reorder — `J-REORDER`
Filter surfaced → reorder tapped → **funnel ends there.** `J-REORDER-03` (payment) does
not exist, so the revenue funnel is unmeasurable by construction, not by omission.

---

## Hard constraints on anything built from this

1. **No face, identity, or biometric value may ever be an event property** — not a name,
   not an embedding, not a per-individual known/unknown flag.
2. **Neighbourhood comparison must not be instrumented until C-10 resolves.**
3. Wearable-derived signals (SpO₂, sleep) are health data. Measuring *that an automation
   fired* is not the same as transmitting the reading; keep that line explicit.
4. Every registered event must cite a `J-*` step (`.claude/rules/analytics.md`).
