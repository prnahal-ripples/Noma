# Competitive teardown — first run, household members, device setup

**Date:** 2026-08-05 · **Source:** Mobbin (iOS), owner's account
**Apps examined:** Google Home · Apple Home · SmartThings · IKEA Home smart · Amazon Alexa
**Flows read screen-by-screen:** 9 flows, ~130 screens

> Mobbin carries **no** air-purifier or air-quality app (searched: Dyson, Levoit,
> Molekule, Airthings, purifier, air). It carries no Aqara, Ring, Nest, Wyze, Eufy,
> Tuya or Hue either. The five apps above are the entire smart-home set available.
> So the purifier-specific setup problem — *a box with a filter in it, on your floor,
> that has to join 2.4 GHz Wi-Fi* — has **no direct competitor reference here**. The
> closest analogue is IKEA's DIRIGERA hub, which is also a physical object you plug in
> and watch a light on. It is by some distance the best reference in the set.

---

## 1. What every app agrees on

**Device before people. Five out of five.** Not one app asks you to add a household
member during first run. Members always live in Settings, reached later, deliberately.

| App | Order |
|---|---|
| Google Home | sign in → create home (name → address, *skippable*) → choose home → what's new → pick favourites → **devices empty state** → add device. *People: Settings → Invite person.* |
| Apple Home | a Home already exists → `+` menu → Add Accessory → room. *People: same `+` menu, no first-run prompt.* |
| SmartThings | 4 value slides → Samsung account → **location name + geolocation** → scan → pair. *No member flow captured at all.* |
| IKEA Home smart | region → privacy statement → analytics consent → editorial welcome → **hub setup** → name home. *No invite flow. Guests **request** access from a host.* |
| Amazon Alexa | account → **device setup** → Wi-Fi. *Family member: Profile → Add Someone Else, much later.* |

The reason is structural, not fashion: **an invitation to a home with nothing in it is an
invitation to nothing.** There is no permission worth granting, no device worth scoping,
and no way for the invitee to tell whether accepting did anything.

The second thing they agree on: **one question per screen.** No app in the set puts two
decisions on one setup screen. Google Home splits home-name and home-address across two.
IKEA splits three cable instructions across three.

---

## 2. The twelve patterns worth taking

Ordered by how much anxiety each one removes.

### 2.1 Parts checklist before the first instruction — IKEA

> **Let's get started!**
> Here are the parts you'll need:
> `[Hub]` `[Cables and plug]` `[Power]` `[Router]`
> **[Get started]**

Four line-drawings in a 2×2 grid, before a single instruction. This is the strongest
anti-anxiety move in the whole set. The fear at the start of a hardware setup is not
"will this be hard" — it is **"am I about to get three screens in and discover I need
something I don't have?"** The checklist answers that before it is asked.

Nobody else does this. Every other app starts issuing instructions immediately.

### 2.2 Every ask states its reason — Google, IKEA

- Google: *"Home address — Your home address will be used for things like directions."*
- Google: *"Name your home — Choose a nickname for this home to help identify it later."*
- IKEA: *"Let's start with your region — We'll provide local Terms & Conditions so you know what to expect from the app."*

NOMA already does this in `J-PAIR-PUR` ("Naming the room lets us compare against the right
outdoor sensor", "Live air data and automations need a connection"). The teardown confirms
it as best-in-class and it should be promoted from a habit to a **gate**: no setup screen
ships without a stated reason.

### 2.3 The physical world is confirmed by the user, not by a timer — IKEA, Alexa

- IKEA: *"The ring light will pulse when the hub is ready"* → **[My hub is ready]**
- Alexa: *"Is your Echo Dot plugged in and displaying an orange light?"* → **[No] [Yes]**

Neither app guesses. The user looks at the object and says so. This costs one tap and buys
two things: the user knows what to look at, and the app gets a reliable branch point.

Alexa's `No` branch is designed: *"No orange light? Try this:"* with two reset procedures
and a **Need more help?** link.

### 2.4 The failure state is designed, not an afterthought — IKEA, Alexa

IKEA:
> **We didn't find any hubs**
> Sometimes the hub needs a little nudge to get going. You can get help from common issues
> and solutions or try to search again.
> **[I need help]** (secondary) **[Try again]** (primary)

…leading to a **Common issues and solutions** accordion: *"There are no lights on my hub" ·
"The ring light stopped filling" · "The hub only has a small centre light."*

Alexa:
> **Device not discovered** — Here are a few tips:
> 1. Make sure you stay within 10ft of your Echo device.
> 2. Check that your device is plugged in.
> 3. If you don't see an orange light, [learn how to enter setup mode].
> **[Try Again]**

Note the tone in both: the *device* needs a nudge. Never the user's fault.

**This is the single biggest gap in NOMA's material.** `memory/product/scope-ledger.md`
records "empty, loading, error states — absent throughout." A setup flow without a
not-found state is not a setup flow.

### 2.5 Permission is asked at the moment of need — IKEA (and SmartThings shows the anti-pattern)

IKEA fires the OS local-network prompt **immediately before** the screen that says
*"Looking for nearby hubs…"* — the reason is on screen behind the dialog.

SmartThings fires the same prompt **on onboarding slide 1**, before the user has done
anything or been given a reason. It then fires the Bluetooth prompt on slide 3 and the
microphone prompt during device add. Three system dialogs before any value.

NOMA's `J-ONBOARD-06` (a pre-permission priming screen shown before the OS prompt) is the
right instinct. The teardown says: keep the priming, but **move the prompt to the moment
it is needed**, not to a fixed step in onboarding.

### 2.6 Waiting is named, bounded, and released — IKEA

> **We found your hub!**
> Let's update to the latest software. Please don't unplug your hub.
> **You are welcome to close the app while waiting.**
> `Downloading 0%` → `Rebooting — A few minutes remaining`

*"You are welcome to close the app while waiting"* is the most humane sentence in 130
screens. It converts a hostage situation into an errand. Also: *"It may take a few minutes
for the ring light to completely fill"* sets the expectation **before** the wait, which is
exactly what `J-PAIR-PUR-01` already does ("this takes a moment").

### 2.7 Naming is offered, not demanded — IKEA

> **Give your home a name**
> `[________]` 0/25
> `Home` `My home` `Our place`

Suggestion chips under the field. A blank text input is a small exam; three chips make it
a choice. NOMA's `J-PAIR-PUR-03` already uses room presets including **Pooja Room** —
extend the same treatment to the home name with India-context chips.

### 2.8 A single inline "…but what if my situation is different?" note — IKEA

Under *"Wait for the ring light to make a full circle"*, a left-bordered inline note:

> **Are you joining someone's hub?**
> If the hub is already set up, you will see a solid centre light instead of the ring.

One note, on the one screen where the two situations diverge. Not a FAQ, not a modal — a
sentence placed exactly where the confusion happens.

### 2.9 Disclose what an invitee will see — *before* you send — Google Home

The best member flow in the set, by a distance. After picking a person, a three-page
carousel titled **"What's shared"**, one full-bleed illustration per page:

| Page | Heading | Body |
|---|---|---|
| 1 | Full control of devices and services | "This member can access all devices, services and settings, including devices and services that are added later. They can also change all home settings, add and remove devices and services, and add and remove people." |
| 2 | Contact information and home address | "This member can see the names and emails of other people in this home. They can also see and change the address." + `View household` |
| 3 | Home activity | "This member will be able to see activity and events from all devices and services, like Nest Aware. This includes all events with video and audio data captured on cameras and other devices." |

Then a review screen:

> **Send an invite to "Home"?**
> Review this person's access before inviting them.
> `Sam · samlee.mobbin@gmail.com`
> `Device access — All devices ›`
> *Everyone in this home will be notified when you send this invitation.*
> **[Send]**

Two things to keep: page 3 names **cameras, video and audio** explicitly, and the review
screen tells you the invite is **not private** from the rest of the household.

### 2.10 A member has two enrolment paths — Alexa

> **Hand your phone to Sam**
> Alexa will help get them started by learning to recognize their voice. If they are not
> with you at the moment, you can share these instructions with them.
> **SHARE INSTRUCTIONS** · **[Continue]**

Co-present and remote, on one screen, with the co-present path as the default. This maps
directly onto NOMA's two situations: **P2 (Ravi & Lakshmi)** are in the room and will
literally be handed the phone; **P1 (Asha)** is setting up her parents' home from
Bangalore.

Alexa then runs the *member's own* mini-onboarding on the same handset — their own T&C
acceptance, their own voice enrolment, and a closing screen listing what they now share.

### 2.11 A role is a consequence, not a title — Alexa

> **Who is this profile for?**
> `First name` `[Sam]`
> ○ **Adult** — Controls their own experience
> ○ **Kid** — Includes parental controls

Two options, each one line, each describing an *outcome*. Compare with the three
incompatible role models NOMA is currently carrying (`C-3`): whichever wins, the labels
must read as consequences, not as job titles.

### 2.12 "Identify" — Apple Home

On the room picker for a newly-found accessory, a secondary action: **Identify**. Makes
the physical device blink so you can be sure which one you are naming. One word, removes
an entire class of "did I just name the wrong purifier" doubt in a two-device home.

---

## 3. Anti-patterns observed

| App | What it does | Why it hurts |
|---|---|---|
| SmartThings | **22 screens** to add one TV. Wizard with a 3-dot stepper, then a *second* 4-dot stepper, then a PIN entry, then a registration screen. | The stepper resets twice, so progress is unreadable. Long is survivable; *unmeasurable* is not. |
| SmartThings | Local-network, Bluetooth and microphone prompts before any value is shown | Three refusals before the first reading |
| Amazon Alexa | 28-screen onboarding | — |
| Google Home | Asks for **home address** before a single device exists | High-friction, high-sensitivity ask with no earned trust behind it. It is skippable, which is the only thing saving it. |
| Google Home | Home creation ends in a *"Welcome to the new Google Home"* marketing interstitial | A product-update note delivered to someone who has never used the product |
| SmartThings / Alexa | Consent as a wall of checkboxes inside account creation | IKEA's separate, scroll-gated consent screen is the better pattern (see below) |

**IKEA's consent handling is the counter-example worth copying** and is directly relevant
to NOMA's **DPDP Act 2023** obligation:

- Privacy Statement on its own screen. **[Next] stays disabled until the user scrolls to
  the bottom.**
- Analytics consent on a *separate* screen, with **two explicit radio options** —
  *"Yes, I consent…"* / *"No, I don't consent…"* — neither pre-selected, both with
  **Read more** expanders.

Nothing is pre-ticked and nothing is bundled. For a product whose store copy will say
*"Your data never leaves home,"* this is the standard to meet.

---

## 4. What this changes for NOMA

| Finding | Consequence |
|---|---|
| Device before members, 5/5 | Members must be **step three**, offered after the first reading — not before it. See §5 of the spec. |
| No competitor reference exists for purifier setup | IKEA's hub flow is the template. Adapt it; do not look for a purifier app that does it better, there isn't one on Mobbin. |
| Failure states are designed everywhere except NOMA | `F-SETUP` cannot ship without: device-not-found, wrong-Wi-Fi-band, wrong-password, timeout, already-registered. |
| Google's "What's shared" | `J-SHARE` needs a disclosure step **between** role selection and send. It does not currently have one. |
| Alexa's dual enrolment | `J-SHARE` needs a hand-the-phone-over path, because P2 is defined by low app fluency. |
| IKEA's consent gating | The DPDP consent surface is a *separate screen with unticked options*, not a line of small print under a Continue button. |

---

## 5. Registry gap found while doing this

`src/hardware/feature-map.json` registers thirteen features. **None of them is
"get a new customer to a working first device."** Onboarding and pairing exist as journeys
(`J-ONBOARD-*`, `J-PAIR-PUR-*`) with no `F-*` id, so they have no PRD slot, no owner and
no place in the scope ledger.

Two ids are **proposed, not assigned** (per CLAUDE.md rule 6 — the owner assigns ids):

- `F-FIRST-RUN` — arrival, account, home creation
- `F-SETUP` — physical device pairing

Logged as **O-8** in `memory/decisions.md`.
