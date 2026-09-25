# User Journeys — J-* step IDs

> Extracted from the PM prototype set on 2026-08-04. Every step below corresponds to a
> screen that EXISTS in a prototype — none is invented. Step IDs are stable; do not
> renumber, retire instead.
>
> ⚠ **Journeys are not yet persona-conditional.** C-1 (two incompatible persona sets)
> is open, so no step carries a persona ID. Do not add one until C-1 closes.

---

## J-ONBOARD — account and first device

| ID | Step | Screen | Notes |
|---|---|---|---|
| J-ONBOARD-01 | Welcome | `WelcomeScreen` | "By continuing you agree to our Terms & Privacy Policy" |
| J-ONBOARD-02 | Value slides (4) | `OnboardingScreen` | One App Whole Home · Privacy First · Smart Automations · Home Score |
| J-ONBOARD-03 | Phone number | `PhoneScreen` | Country selector present; India default |
| J-ONBOARD-04 | OTP verify | `OTPScreen` | |
| J-ONBOARD-05 | Name the home | `HomeBootstrapScreen` | |
| J-ONBOARD-06 | Notification priming | `NotifPrimeScreen` | Pre-permission screen, shown before the OS prompt |
| J-ONBOARD-07 | Pick first device type | `AddDeviceIntroScreen` | Camera · Lock · Purifier · Vacuum only |

**Observation.** The value slides promise "Home Score" before any device exists, so the
Score must have a legible zero-device state. None is designed.

---

## J-PAIR-PUR — add a purifier

The most carefully-designed flow in the material. Three steps, each removing a known
failure.

| ID | Step | What it does |
|---|---|---|
| J-PAIR-PUR-01 | Bluetooth discovery | "Power on the purifier. Hold your phone close — this takes a moment." Sets an expectation of delay instead of appearing stuck. |
| J-PAIR-PUR-02 | Wi-Fi (2.4 GHz) | **Hides 5 GHz SSIDs the device cannot join.** Removes the single most common smart-home setup failure. Says why: "Live air data and automations need a connection." |
| J-PAIR-PUR-03 | Name + room | India-context presets incl. **Pooja Room**. Names the reason: "Naming the room lets us compare against the right outdoor sensor." |
| J-PAIR-PUR-04 | First reading | The gut-punch. See J-WEEK-01. |

Every step states its *purpose*, not just its instruction. Worth preserving as a rule.

---

## J-WEEK — the first seven days

A deliberate day-by-day retention arc, each day with a stated emotional target and the
research reason behind it. This is the closest thing to a product spec in the material.

| ID | Day | Beat | Emotional target | Mechanism |
|---|---|---|---|---|
| J-WEEK-01 | 1 | The Reveal | "Quiet shock" | First reading is about *your* room vs the street, colour-coded, already cleaning. No feature tour. |
| J-WEEK-02 | 2 | The Proof | Reassured | Morning "Air Defended" card quantifies the night (outdoor 187 → indoor 22) + wearable SpO₂ tie-in |
| J-WEEK-03 | 3 | The Habit | Hands-off | Three suggested routines from observed use, one-tap accept + remote control + geofenced away mode |
| J-WEEK-04 | 4 | The Neighbourhood | "A little proud" | "Cleaner than 82% of your street" + one-tap share card |
| J-WEEK-05 | 5 | The Worth | Anxiety resolved | Energy card reframes cost as saving (₹164 vs always-Turbo) then as "trees' worth of clean air" |
| J-WEEK-06 | 6 | The Gap | Curious | Home air map shows unprotected rooms; filter health surfaces with reorder |
| J-WEEK-07 | 7 | The Score | "Sealed in" | Air Score /100, shareable, with a Week-2 cliffhanger (pollen / Diwali) |

**The three JTBD return-drivers** everything above is built on, in stated priority:

1. **Checking live AQI** — the #1 stated reason users reopen an air-purifier app
2. **Controlling it remotely**
3. **Trusting the automations**

**Retention chokepoint:** Day 7 → Week 2 is named as the canonical drop-off. J-WEEK-07
exists specifically to bridge it.

---

## J-AGENT — the proposal loop

The core repeating loop. Full mechanics in `memory/architecture/ai-integration.md`.

| ID | Step |
|---|---|
| J-AGENT-01 | Agent surfaces a proposal in "Needs your call" |
| J-AGENT-02 | User expands "Why this?" — Sensed / Decided / Instead of / Obeys rule |
| J-AGENT-03 | User rehearses the plan as an editable timeline |
| J-AGENT-04 | User runs, defers ("Later"), or declines ("Not tonight") |
| J-AGENT-05 | Agent reports back; item moves to "Done today" with Undo |
| J-AGENT-06 | User promotes it via "Do this always" → appears in Automation tab |
| J-AGENT-07 | After repeated accepts, agent offers a capability autonomy upgrade |

⚠ J-AGENT-04's defer paths have **no expiry behaviour defined**.

---

## J-SHARE — invite a household member

| ID | Step |
|---|---|
| J-SHARE-01 | Pick role |
| J-SHARE-02 | Select devices to grant |
| J-SHARE-03 | Select per-device features |
| J-SHARE-04 | Set time window / expiry (role-dependent) |
| J-SHARE-05 | Send invite |
| J-SHARE-06 | Review in member list / audit |

⚠ **Blocked by C-3** — three incompatible role models exist. The flow was rebuilt three
times in the prototype (`SharingFlow`, `V2`, `V3`), which is itself the evidence that
this is unsettled.

---

## J-REORDER — consumable reorder

| ID | Step |
|---|---|
| J-REORDER-01 | Filter health surfaces proactively (not at failure) |
| J-REORDER-02 | Reorder CTA with arrival framing: "Arrives before it runs out" |
| J-REORDER-03 | *(missing)* payment, address, confirmation, tracking |

⚠ J-REORDER-03 **does not exist in any prototype.** The shop is a catalogue and a price
with nothing behind it. This is the revenue path.

---

## Flows referenced but never designed

Honest gaps, each a real flow with no screen anywhere in the material:

- **Offline / device-unreachable** — no state, despite a notification reading "Camera went offline briefly"
- **Filter fully exhausted** — the predictive path is designed; the failure path is not
- **Declined consent** — face recognition can be declined; nothing shows what a declined camera does
- **Agent proposal expiry** — see J-AGENT-04
- **Zero-device Home Score** — promised in onboarding before any device is paired
- **Multi-home** — `S2_HOMES` exists in the data with no flow attached
- **Account deletion / data export** — a DPDP obligation with no surface
