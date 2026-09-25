# F-FIRST-RUN + F-SETUP + F-SHARING · Onboarding and device setup

| | |
|---|---|
| **Status** | draft — **rebuilt 2026-08-06 to the owner's flow diagram, then revised four times same day** |
| **Owner** | TODO(owner) |
| **F-id** | `F-FIRST-RUN` ⚠ **proposed, unassigned** · `F-SETUP` ⚠ **proposed, unassigned** · `F-SHARING` (exists) |
| **Journeys** | `J-ONBOARD-01…07` · `J-PAIR-PUR-01…04` · `J-SHARE-01…06` · `J-WEEK-01` |
| **Source of truth for the flow** | The owner's flow diagram, 2026-08-06, plus four same-day owner revisions. **22 main-line nodes + branch 18a** as built — nodes 19–22 were removed, and the ids no longer ascend. §5 is the spec; the diagram is its origin, not its current state. |
| **Blocked by** | `C-2` (product + assistant name — every string below is provisional) · `C-3` (role model — node 18a is shape-only) · `O-8` (two of the three F-ids do not exist yet) · **open legal question on consent, §5.1** |
| **Research** | `docs/research/2026-08-05-setup-teardown.md` · `docs/research/NOMA-first-run-references.pdf` |
| **Prototype** | `docs/features/first-run/first-run-prototype.html` — tappable, light theme, 32 screens + 13 edge states |
| **Flat board** | `docs/features/first-run/first-run-wireframes.html` — **generated from the prototype's source**, grouped by node, for print and review |
| **Clean export** | `docs/features/first-run/first-run-export.html` — one phone, tappable, no review apparatus. For experiencing the flow, not reviewing it. ⚠ Edge states are hash-only there (`#W2E`); they are not tappable. |

> **Superseded 2026-08-05 → 2026-08-06.** The previous draft specified Arrival → Household →
> Device, chose that ordering out of three candidates, and had no email, no device choice
> and no location ask. The diagram overrides all of it. §5 opens with a table of exactly what
> changed and what each change costs; the open judgement calls are §5.1, §5.2 and §5.6.
>
> **Four owner revisions, same day.** (1) Node 6 narrowed from a four-way device-*type*
> chooser to three purifier *SKUs* — retiring §5.4. (2) **Nodes 19–22 removed entirely**
> (firmware check, install, complete, first reading), along with `R3B`, the household
> disclosure screen. (3) **Nodes 7–12 rewritten** to the updated pairing sequence: filter
> unwrap as its own step, plug-in split from light-check, Bluetooth reframed around the
> radio, device pick as a list, and Wi-Fi auto-fetched rather than hand-picked.
> (4) **Both permission asks moved forward** to run straight after node 16, and node 23 now
> lands directly on Home — see §5.8.
> §5.3 is now an open risk again, not a resolved one — the reveal has no screen at all.

---

## 1. Problem

Somebody has just unboxed a purifier. It is on the floor, not plugged in, and they are
holding a phone. The thing they are most afraid of is not that setup will be long — it is
that it will **fail in a way they cannot fix**, in their own living room, with a box they
have already paid for. Meanwhile the product's entire first-week argument
(`memory/product/journeys.md`, `J-WEEK-01`) depends on getting them to one number —
their room's AQI against the street's — before they lose patience.

Nothing in the material covers this. `J-ONBOARD` and `J-PAIR-PUR` list happy-path screens
with seeded data. There is no not-found state, no wrong-Wi-Fi-band state, no
wrong-password state, no timeout, and no zero-device Home Score — which onboarding slide 4
promises before any device exists.

## 2. Why now

- `J-WEEK-01` ("The Reveal", emotional target: *quiet shock*) is the retention mechanism
  the whole first week hangs off. It cannot fire until a device is paired.
- `memory/product/scope-ledger.md` names "empty, loading, error states" as absent
  throughout, and every setup flow is 80% error handling by weight.
- The teardown found **no purifier app on Mobbin at all** — there is no incumbent to be
  compared against and no established pattern to inherit. This is a place where NOMA can
  simply be better than the category.

## 3. Users

| Persona | What they need differently |
|---|---|
| **P1 · Asha** (primary, buyer, power user) | Is often setting up **her parents' home, remotely or on a visit**. Needs node 18a to work when the other person is not in the room, and needs depth available but never volunteered. |
| **P2 · Ravi & Lakshmi** (residents, low fluency) | Set up their own phone **from an invitation, on their own**, with nobody beside them. Sets the floor: large targets, one instruction per screen, no jargon, no step that requires app fluency to stay safe. |
| **P3 · Household help** | ⚠ **No first-run entry point at all now.** The diagram's household branch is family-only, and per-member scoping and expiry moved out of first run. P3 is enrolled from People, later, still time-boxed by default. |
| **P4 · Priya** (one camera, considering more) | ⚠ **Out of scope, and now genuinely absent.** Node 6 no longer shows a camera option at all (narrowed 2026-08-06 to purifier SKUs only), so this persona has no entry point and no false promise either. Correct until cameras actually ship. |

⚠ Persona set is `C-1`-provisional. No step below carries a persona-conditional branch.

## 4. Scope

**In**
- Cold app open → account (phone **and** email) → paired device → home created → **one
  device reporting a live reading** → Home.
- Every failure state in that path.
- Inviting the first household member, as the branch off node 18.
- The location and notification asks, and the three-slide tour between them.

**Out**
- Multi-home (`S2_HOMES` exists in the data with no flow — out of first run entirely).
- Second and subsequent devices (the same nodes 6–18 machine, entered from Devices, no
  wrapper around it).
- Payment, shop, subscription.
- **Per-member device scoping and expiry.** The 2026-08-05 build had these as first-run
  screens; the diagram does not, and they belong in People. P3 (household help) therefore has
  no first-run entry point, which is correct.
- Any agent proposal. The agent introduces itself on node 23 slide 2 and on Home, and
  proposes nothing until Day 2.

---

## 5. The flow

**Rebuilt 2026-08-06 to the owner's flow diagram, then revised four times the same day.**
The ordering question that dominated the 2026-08-05 draft — Arrival → Household → Device,
chosen over two alternatives — is closed and moot. What follows is the flow **as built**:
22 main-line nodes plus branch 18a. Node ids come from the original diagram and are kept
stable so downstream references still resolve — which means **they no longer run in ascending
order**. The gap at 19–22 is deliberate, and so is the 16 → 24 → 25 → 17 jump.

**The order as built:**

```
1 … 16   account → pairing → network → connected
  24     ask for location (geofencing)   ← moved here 2026-08-06
  25     ask for notifications           ← moved here 2026-08-06
  17     which room is it in? create a home
  18     what should we name the device
 18a       └ invite family members  (branch)
  23     tap your key on the door        ← replaced the 3-slide tour 2026-08-17
  26     home
```

**What changed, and what it cost.** Recorded here so nobody re-derives it:

| | 2026-08-05 build | The diagram | Consequence |
|---|---|---|---|
| Account | Phone + OTP only | Phone + OTP, **then name + email, then email verification** | Two verifications back to back. Five screens before the box is opened. §5.2 |
| Consent | Two dedicated screens, scroll-gated, plus an analytics opt-in | **Neither** | DPDP notice has nowhere to live except node 4. §5.1 — the one open legal question |
| Device choice | One full-width purifier card, no choice | **Three purifier SKUs, one card each, stacked** — `HW-PUR-200`/`500`/`MAX` | One product line, three sizes. Closed 2026-08-06; §5.4 is retired, not open. |
| The home | Created on its own screen, before any device | **Created while naming the room**, node 17 | Better: nothing abstract is named before something real exists |
| Household | 11 screens, before any device existed | **A 2-screen branch off node 18** | Shorter — but the per-invite disclosure (`R3B`) was cut with it, and nothing replaced it |
| The reveal | Its own full screen, node 2.12 | **No screen at all** — node 22 removed 2026-08-06 | Home shows a number with no step that produced it. Now `F-AQI-LIVE`'s problem. §5.3 |
| Feature tour | 3 slides, agent first | 3 slides, **privacy first** | Correct. §5.6 |
| Location | Absent | **Asked, for geofencing** | The only permission in the flow with a concrete payoff. §5.5 |
| Pairing | Instructions → light → BT permission → scan | **Filter unwrap · plug in · light · Bluetooth on · pick from a list** | Rewritten 2026-08-06. The filter step is new and is the highest-value screen in the sequence. |
| Wi-Fi | Pick from a list, type a password | **Auto-fetched from the phone**, list is the fallback | One tap instead of a list plus a keyboard |
| Firmware | Check · install · complete | **Removed entirely** | No update path exists anywhere now. Flagged in §5 and §9. |
| Notifications | Primed after the reveal | Primed at node 25, resolves straight to Home | The old §5.5 dangling promise died with node 19. |

**Prototype:** `first-run-prototype.html` — 32 screens across 22 nodes + one branch, plus
13 edge states. **Flat board:** `first-run-wireframes.html`, generated from the same source.

---

### The nodes, as built

Ids are the screen ids in the prototype. A node with two ids needs two screens to be
honest — an OS dialog sitting over the screen that explains it, a spinner resolving into
an offer — and the node count does not move.

#### Nodes 1–5 · Account — `F-FIRST-RUN`

**REBUILT 2026-08-17 (owner) as a bottom-sheet flow, and now merged into the canonical
screen set.** All five nodes were full-screen pages; they are now one full-bleed image with
a sheet that stays put and re-lays-out under you. What each node must do is unchanged
except where marked; the *surface* is what changed. See §5.11.

**Where it lives:** `build-auth.py` owns the states and their markup. `build-prototype.py`
imports them, so **all four renderings carry the new sign-in** — the tappable prototype, the
45-screen flow (the one published at `#noma/userflows/first-run`), the flat board and the
clean export. `auth-prototype.html` remains the *live* one, where you type and the sheet
resizes; the four flow renderings are static walkthroughs with every field pre-filled, which
is the convention the other 38 screens already follow.

**The sheet stops at node 3.** Owner, 2026-08-17: *"the bottom sheet will only be till phone
number verification."* Nodes 1-3 are the sheet; nodes 4 and 5 are full pages.

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 1 | `S0` | **Splash** *(sheet)* | Image (video later) with the wordmark at the foot. No control. The sheet arrives on its own. |
| 1 | `A1` | **Login sheet** *(sheet)* | Wordmark, one-line promise, mobile number or Apple. No third path. **Carries the T&C and, for now, the DPDP notice** — see §5.1. |
| 2 | `A2` | Login with phone *(sheet)* | ⚠ **+91 hardcoded; the country selector is gone.** **No password anywhere in this flow** — the number is the account. |
| 3 | `A3` | Verify *(sheet)* | ⚠ **Four digits, not six.** Resend countdown visible from t=0. Hands over to node 4. |
| 4 | `A4` | **Setup profile · the master key** | Name + email, and the card that IS the key to the home. **The display name is back.** See §5.13. |
| 5 | `A5` | **Email verify** *(sheet over node 4)* | A code, not a link. Opens **on** the Setup profile page, dimmed behind, so the card stays visible while you confirm the address on it. |

**States:** wrong OTP (`A3E`) · email already in use (`A4E`) · nothing arrived (`A5E`).
⚠ **All three are EXTRAPOLATED, not from the owner's frames** — every supplied frame is
happy path. They are drawn in the sheet language using `status.negative`, so the flow does
not fall back to the old full-screen language mid-run, but they have not had an owner pass.
`A4E` lost something real in the port: the old version offered *"sign in with that one
instead"* as a second button, which is the useful action. A second CTA changes the sheet's
whole button hierarchy, so it is flagged rather than guessed.

#### Nodes 6–11 · Pairing — `F-SETUP`

**Rewritten 2026-08-06 (owner) to the updated pairing sequence.** Node 6 is unchanged;
everything after it is new. The old flow ran instructions → light → Bluetooth permission →
scan; the new one gives the filter unwrap its own screen, splits "plug in" from "check the
light", reframes the Bluetooth step around switching the *radio* on rather than granting a
permission, and turns the device pick into a list rather than a single confirm card.

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 6 | `P1` | **Choose your purifier** | Three SKUs — `HW-PUR-200` / `HW-PUR-500` / `HW-PUR-MAX` — one horizontal card each, stacked vertically. No device-type chooser, no camera/lock/vacuum. One product line, three sizes. |
| 7 | `P2` | **Unwrap the filter** | ⚠ **NEW, and the highest-value screen in the sequence.** Open the door, remove the polybag, reseat, close until it clicks. This is the only setup failure that is *completely invisible* — a bagged purifier behaves normally in every respect except cleaning. |
| 8 | `P2B` | **Plug in and switch on** | Split out from node 7. Any socket; press power once; the fan should start. Two physical tasks with two failure modes should not share a screen. |
| 9 | `P3` | **Wi-Fi light blinking** | **User-paced, never a timer.** The recovery — *hold the Wi-Fi icon 5–6s until it blinks* — is on the screen, not behind a help link: on a re-setup it is the common path, not an error. ⚠ `O-9` |
| 10 | `P4` `P4D` | **Switch on Bluetooth** | Reframed: about the radio being **on**, not only about app permission. A phone with Bluetooth off is the failure this prevents. System dialog follows immediately, reason visible behind it. |
| 11 | `P5` `P6B` | **Scan and select, then pair** | ⚠ **MERGED 2026-08-18** — scanning and picking are one screen: the count starts at zero and results arrive in place. Still a **list**, not a single confirm card. ⚠ **Identify** (blink the light) was the only way to tell two identical SKUs apart and is NOT on the merged screen — it has to come back. `O-9` |

**States:** already in another home (`P3E`) · no light at all (`P3F`) · Bluetooth refused
(`P4E`, sends to Settings, never re-prompts) · not found (`P5E`) → common issues (`P5F`) ·
pairing failed (`P6E`, states the world after the failure so nobody factory-resets
unnecessarily).

#### Nodes 12–16 · Network

**The Wi-Fi step is now auto-fetch first, manual second.** The phone already knows which
network it is on; making the user re-pick it from a list was work the app could do itself.
Nodes 13–14 still exist, as the fallback.

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 13 | `W1` | **Which network should it join?** | ⚠ **MERGED 2026-08-18** and moved BEFORE the confirm — the fetch spinner and the network list are one screen, networks arriving under a live count. **5 GHz SSIDs hidden AND the app says so.** Hiding without explaining is a defect. |
| 12 | `P7B` | **Confirm the network** | The credential still comes from this phone, so there is nothing to type; the band rule is stated here — **2.4 GHz and dual-band work; 5 GHz-only will not.** Escape hatch to `W2`, type it yourself. ⚠ Node 12's fetch half was absorbed by node 13, which is why 13 now precedes 12. §5.17 |
| 14 | `W2` | Wi-Fi password *(fallback)* | Show/hide. **No "save my password to the cloud" checkbox** — Alexa's pattern, and it contradicts the promise made at node 4. |
| 15 | `W3` | **Setting up** | 15–20s of real device work. Four-slide feature carousel above a named progress bar. **Re-spaced 2026-08-06:** CTA pinned to the bottom, progress block just above it, and the duplicate 4-dot stepper removed — the carousel has its own dots, and two indicators on one screen read as two different progress meanings. See §5.7. |
| 16 | `W4` | Connected | **A full screen, not a toast.** This is where the setup anxiety ends and the first thing in the flow visibly works. |

**States:** only 5 GHz found (`W1E`) · wrong password (`W2E`, inline, keeps the SSID) ·
joined but no internet (`W4E`, the device still works — say so).

> ⚠ **One phrase in the source spec is unresolved.** The brief said the device
> *"does not work with standalone wifi credential"*. Node 12 reads that as **5 GHz-only
> networks**, which fits the accompanying "works on 2.4 GHz / dual-band". If it actually
> meant **captive-portal or enterprise/802.1X networks**, node 12's copy is wrong and both
> cases need their own error states — neither exists today. Worth thirty seconds of
> confirmation before this ships.

#### Nodes 17, 18, 18a · Place, name, household — `F-SHARING`

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 17 | `R1` | **Which room + create the home** | Room presets incl. **Pooja Room** (⚠ `C-12`), free text, and the home name in the same screen. The `Home` record is created here. |
| 18 | `R2` | Name the device | Pre-filled from the room. Two buttons: the branch, or straight on. |
| 18a | `R3` | Invite family members | Contact suggestions. **The invitation goes to them; the phone never changes hands.** Picking a contact sends directly. |
| 18a | `R3C` | Invite sent | Pending appears in the roster immediately. Resend and revoke on the row. Rejoins the main line at node 23. |

**States:** not a valid contact (`R3E`).

> ⚠ **Removed 2026-08-06 (owner): `R3B`, "What Lakshmi will see".** It sat between the two
> screens above and was Google's "What's shared", adapted — a three-line grant summary
> (devices / other members / all activity). It was the one screen that disclosed to the
> owner what an invitee actually gets, and it carried the camera/audio wording flagged
> elsewhere in this PRD as needing to return the day a camera ships. **That disclosure now
> has no home in first run.** If any per-invite disclosure is still required — and for a
> product whose pitch is "your data stays on your devices", inviting someone into all of it
> silently is a hard thing to defend — it needs a new node, not a quiet re-insertion here.

> **Still true, still load-bearing — the hand-the-phone-over step stays removed.** An earlier
> draft borrowed Alexa's *"Hand your phone to Sam"*, with the new member accepting terms on
> the owner's handset. Three reasons it is gone: it assumes the two people are in the same
> room, which is exactly what P1 is not; the invitee gets no independent record of what they
> agreed to; and it has the owner physically present while someone else grants a
> data-processing consent. An invitation accepted on their own device solves all three.

⚠ **`C-3` still open.** Nothing in 18a assigns a role name. Per-device scoping and expiry —
which the 2026-08-05 build had as screens `H6`/`H7` — are **not in the diagram** and are not
in this flow. They belong in People, post-setup. P3 (household help) has no first-run entry
point at all now, which is correct: nobody enrols a maid in the first ten minutes.

#### ~~Nodes 19–22 · Update and first reading~~ — REMOVED 2026-08-06

The whole firmware sequence and the reading wait are gone: **check for update** (`U1`/`U1B`),
**update device** (`U2`), **update complete** (`U3`), **taking first reading** (`U4`), and the
**update-timed-out** state (`U2E`). Node 18 and node 18a now run straight into the tour at
node 23; node 25's dialogs resolve straight to Home.

That removes two real problems — the §5.5 dangling promise (node 19 said *"we'll notify you
when it's done"* six screens before notification permission was asked) and a multi-minute
blocking wait in the middle of setup. It also leaves **two things genuinely unhandled**, which
belong on someone's list rather than in a deleted screen:

1. **Nothing in the flow takes a first reading any more.** Node 26 renders `34 · AQI` with no
   step that earned it. If the sensor really needs ~20s to settle — which is what `U4`'s copy
   claimed — **Home needs its own loading state for that window.** This is now Home's problem
   (`F-AQI-LIVE`), not first run's, and it is not written down anywhere else.
2. **Firmware update has no path at all**, here or in any other spec. If a purifier can ship
   with stale firmware, that has to land somewhere — a Device-detail nudge, a background
   update, something. Dropping it from setup is a reasonable call; dropping it entirely is a
   product decision that nobody has recorded as one.

#### Nodes 24, 25 · Permissions — **run straight after node 16**, before the home exists

Moved here 2026-08-06 (owner). Both OS prompts now fire in one block, at the moment the
device has visibly worked, instead of being separated by four naming and household screens.
See §5.8 for what that buys and what it costs.

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 24 | `L1` `L1D` | **Location · geofencing** | Priming with the concrete payoff, then the dialog. **Ask for While-Using, never Always.** §5.5 |
| 25 | `N1` `N1D` | Notifications | Priming, then the dialog. Declining either goes on to node 17 exactly as accepting does. |

#### Nodes 23, 26 · About the app, then home

| Node | Id | Screen | What it must do |
|---|---|---|---|
| 23 | `D1` | **The door** *(replaces the tour, 2026-08-17)* | A closed door and the key made on node 4. Drag the card to the lock, or tap it, and the door opens into Home. C1/C2/C3 are **removed** — see §5.14 for what went with them. |
| 26 | `HOME` | Home | Three zones from `ai-integration.md` §2: reassurance, then the ask, then the receipt. **The first and only number the user sees** — and, since node 22 was removed, the first screen to show one with no setup step that produced it. §5.3 |

---

### The things worth arguing about

**§5.28 — The transition flash was both layers fading at once, 2026-08-18.**
The incoming screen faded in while the outgoing one faded out, so for the
overlap each was semi-transparent and the phone's bare ground showed through
**both**. Worst exactly where it was reported: leaving a full-bleed photo for a
light page (A3→A4) and losing the purifier (P4D→P5). The outgoing screen now
stays opaque and is covered rather than dissolved.

Two latent bugs surfaced fixing it. The outgoing screen kept its arrival class
with the fade still running, so a **fast tap** left it part-way faded and the
flash returned — it is stripped and pinned opaque now, verified at a 100ms tap
interval. And its removal timeout rode the harness's cancel list, which is
emptied at the top of every render, so dead screens lingered under live ones.

**§5.29 — Node 17 is the one screen that does not follow the page structure.**
Owner: title and body, then the home name, then the room chips, then the drawing
**last**. The picker left the visual half to do it, so the illustration is the
final thing on the page rather than the first. The reading order is better — you
name the home before being asked to place a device in it — and §5.9's morph
gesture is unchanged. ⚠ Flagged because a one-screen exception to a flow-wide
structure is a decision, not a detail: either node 17 is right and the structure
needs an escape clause, or the structure is right and node 17 owes an argument.

**§5.30 — The branch moved from node 18 to node 18a.**
Node 18 is a single *Continue* now, so the diagram's fork — invite the family
against not now — lives on node 18a, where **"Not now" is a tertiary action**:
no container, no fill, sitting under the CTA (`.cta3`). Declining the household
stays a first-class path and stops competing with sharing for the eye. The key
card is 0.8× (151px) and the visual half releases its clip when it holds one,
because a rotated box is taller than its own width and was being cut top and
bottom. Sharing now advances on its own.



**§5.23 — One purifier, moved. Not five, cross-faded, 2026-08-18.**
Owner: *"the device image keeps flickering… just use one single image throughout."* Correct
diagnosis. Every pairing screen rendered its own element, and the runtime FLIPped between
them — same data URI, but a **new element each time**, so the browser re-rasterised the
background on every screen. That is a repaint, and no easing hides a repaint.

There is now exactly one purifier in the document (`.phero`, created at boot, parked outside
the screens). Pairing screens carry invisible `.pslot` boxes that only declare geometry; the
runtime reads the slot and moves the single element there with a transform. Nothing is
recreated, nothing re-decodes, and only a compositor property changes. Verified: **one
`.phero` and zero `.rnd` elements in the document**, the same node throughout pairing.

It sits *below* the screens (z-index 1 vs 2) deliberately — node 9's light overlay and nodes
10-11's phone have to be in front of the device, and both live inside a screen.

**§5.24 — The 1px-stroke buttons had their states backwards.**
Default was the dimmer translucent fill and hover *brightened* it. A raised control is at its
brightest at rest (LAW 3 — white means raised), and going down under a finger should darken.
Default is now the bright fill; hover and press darken, with a press scale.

**§5.25 — Node 14 is gone; node 15 has no CTA.**
Node 12 hands straight to node 15. ⚠ **Node 14 was the only place to type a Wi-Fi password**,
so if a saved credential is stale there is now no normal path to correct it — only the
`W2E` edge state, which is rail- and hash-reachable. `NODES` is 22 now, and the assertion
says why rather than being loosened silently.

Node 15's bar fills over ten seconds and the screen hands itself to node 16, carousel
running throughout. **That removes the last instance of the pattern the 2026-08-06 rebuild
called the most dishonest in the prototype** — a visible wait with a button under it that
skips it. The wait is now the wait. The fill is one CSS transition rather than a per-frame
loop, so it cannot stutter against the carousel.

**§5.26 — Engraved icons are a third register.**
`design-elements/engraved-icons/` — Bluetooth, Wi-Fi, check and notifications. Node 16's
drawn ink tick and node 25's hand-drawn bell are replaced; the bell keeps its concentric
rings and its swing, which now animate the glyph. ⚠ **This makes the icon gate's "two
tiers" wrong as written**, and a folder does not get to fix a rule by existing — an owner
call. ⚠ The notifications glyph carries `#FF4444`, a red that is not in the palette;
`red.mid` is the token for exactly this and is what the drawn bell used. Left as supplied
so it gets decided rather than inherited.

**§5.27 — Node 18a confirms with a toast, and R3C is gone.**
The key card is 0.8×. Sharing raises a "Key shared" toast and the CTA becomes *Continue* —
without that the flow would dead-end on a confirmation, since R3C used to be the way onward.
⚠ **R3C also carried the roster** ("You · owner / Lakshmi · key sent, waiting") and a toast
cannot hold that. The pending-invite state now has no representation anywhere in first run;
it belongs to People.



**§5.19 — The jerk between pages was a corrupted measurement, not a lag.**
The carry decision used to be made *inside* the wiring, after the incoming screen was
already in the DOM carrying `.scr.in`. Measuring an element forces a style recalc — so
every rect was read while the slide's `translateX(10px)` was still applied, every FLIP
started 10px out, and every one snapped at the end. That snap is what read as "a slight
jerk and a lag, then the next page opens". Nothing was slow; the geometry was wrong.

`carryClass()` now reads the markup **before** the element is created, so a carrying screen
never gets a transform at all. Three things carry:

| key | what | why |
|---|---|---|
| `pur` | the chosen purifier | nodes 6 → 7 → 8 → 9 → 10/11 |
| `bg` | the sign-in photograph | so nodes 1-3 never re-render it |
| `sheet` | the sign-in sheet | so it **grows** between states instead of re-rising |

The sheet one matters as much as the purifier: the sheet used to replay its 880ms arrival on
every sign-in step, which is the jerk between the splash and the login sheet. It now rises
once, on the hand-off from the splash, and thereafter changes height in place —
`[data-carried]` is what suppresses the replay, so the one place the rise is wanted still
gets it.

Heavy data-URI backgrounds are also decoded once at boot (`warmAssets`) rather than on first
use, which is to say mid-transition.

**§5.20 — The scale choreography through pairing.**
Node 6's tile → node 7 at 196px → node 8 at 170 (slightly down) → node 9 at 250 (up, its
largest, with the light on it) → nodes 10-11 at ~150 **and shifted left** as the Bluetooth
phone comes in. Because every render is sized by height with its own aspect ratio, the FLIP
between them is a uniform scale — measured at 0.3061 on both axes out of node 6, so the
artwork never distorts.

**§5.21 — Node 13's list gained a lock and a signal meter.**
Both drawn: a padlock, and four ascending bars with the lit count set per network
(Sharma_Home 4, Airtel_Asha 3, Airtel_Nup 2). The meter is SVG rather than four divs
because the review harness scales the whole phone, and at that scale CSS gaps between 3px
divs fell below one pixel and the meter rendered as a solid triangle. ⚠ Even as SVG it is
tight at review scale — it reads correctly at 1×, which is what ships, and that is the
honest description rather than a claim that it looks great in the board.

**§5.22 — Node 18a is a real picker now.**
Owner reference: contacts become removable pills between the field and the list, the list
drops whoever is already picked so the two halves cannot disagree, and the CTA counts the
selection (`Share key` → `Share key (1)` → `Share keys (2)`). The card is tilted and bleeds
off the right edge.

⚠ **The body no longer says "you decide what each key opens."** The reference drops it.
That is arguably an improvement — the promise was never implementable, because the
per-invite disclosure screen was removed on 2026-08-06 and never replaced — but **the gap
is unchanged and is now invisible on the screen**. A key that silently opens everything
still needs a node.

⚠ **Hue-coded avatars are back** (pink / blue / sand), reversing the 2026-08-12 palette
rule the same way node 6's SKU tiles did. Two owner instructions in conflict; three CSS
rules to revert.

⚠ The reference labels Ayush Tiwari's avatar **"AK"**. Initials are computed from the name
here (**AT**) — a wrong initial on a screen whose whole job is telling people apart is a
typo to fix, not a style to copy.



**§5.17 — Scanning and picking are one screen each, 2026-08-18.**
Two pairs collapsed on the owner's reference: *scanning over Bluetooth* + *select your
device* became one node-11 screen, and *fetching Wi-Fi* + *select Wi-Fi* became one node-13
screen. Each shows a large glyph, the ask, and a live list underneath: the count starts at
`(0)`, a spinner turns, and results arrive in place. Two screens shorter, and truer to what
a scan actually is — a thing that fills up, not a thing that finishes and then hands you a
page.

Rows ship in the markup and are revealed by the runtime, so the flat board and the clean
export still show what each list contains rather than an empty state.

⚠ **Node 11 lost Identify, and that matters.** The old select screen had *"make this one
blink"* — and the whole reason the reference shows **two identically-named purifiers** is
that a household buying a pair hits that on day one. Signal strength is now the only thing
telling them apart, which is not enough. It has to come back before build.

⚠ **Node 12 and node 13 now run 13 → 12**, because the merge took node 12's fetch half into
node 13's screen. What survives as node 12 is the confirm step, where the credential still
comes from the phone. Combined with §5.16 this is the second change to weaken auto-fetch;
after both, the honest description of node 12 is "confirm and join", not "auto-fetch".

**Six visual helpers are now defined and unused** — `doorway()`, `peel()`, `holdring()`,
the three tour illustrations, `v_scan()`, `spin()` and `v_wifi()`. Each was retired by an
owner decision, each is a one-line reinstatement, and each has its reasoning in a §5 entry.
Listed in `build-prototype.py` beside the sequence. They should be deleted at hand-off: a
parked decision in a prototype is dead code in shipped software.

**§5.18 — The white flash between screens is gone.**
The harness removed the outgoing screen *before* appending the incoming one, so for at
least one frame the phone contained no screen at all and its bare ground showed through —
which reads as a flash, and at the top of a page load reads as a stall. The new screen is
now appended first and the outgoing one fades out beneath it, so there is never a frame
without content. Fixed in all three renderings that mount screens.



**§5.15 — The chosen purifier is carried through pairing, 2026-08-18.**
Pick a SKU on node 6 and *that device* travels the rest of the pairing run. It is not five
pictures of a purifier: it is **one element, FLIPped** between per-screen geometries —
measure where it was, measure where it landed, start it at the old rect and let it fly.
Node 6's tile hands it to node 7's filter scene, then node 8's socket, then node 9 at its
largest, then node 10-11 smaller as the phone comes in.

Three things this forced, each worth knowing:

- **A carried screen does not slide.** The harness's normal `.scr` slide-in would drag the
  hero with it and fight the FLIP, so a carrying screen has no screen-level animation at
  all: the purifier flies and everything else fades in behind it (`.scr.carry`).
- **The renders are sized by height with their true aspect ratio.** Each SKU has different
  proportions (the 500 is much narrower than the MAX), so a fixed box would letterbox
  differently per SKU and the carried size would jump. Height-only sizing with
  `aspect-ratio` keeps the artwork filling its box exactly, which also makes percentage
  overlays land on the real product.
- **The choice persists.** `PICK` survives navigation, so a 500 stays a 500 all the way to
  node 11 — its own silhouette and its own light position.

**Node 9's light is on the device now**, not a capsule floating beside it. Each SKU's
indicator position was measured off its render (`--ledy`: the 200's light sits at 40% of
its height, the 500 and MAX at ~19%) rather than guessed, and the glow is pinned to it.
⚠ That variable rides the **screen**, not the render: the glow and the bar are the render's
siblings, and a custom property only inherits downward — the first attempt put it on the
render and the light landed off the device entirely.

**Node 10-11's phone dissolves downward** instead of ending in a hard bordered edge, via a
`mask-image` so the bezel and the shadow fade with the content rather than surviving it.

⚠ **§5.16 — W1 now comes before P7B, and that weakens node 12's own argument.**
Owner, 2026-08-18: *"W1 will be before confirming wifi."* The order is now
`P7 → W1 → P7B → W2`: fetch, pick from the list, confirm the pre-filled password, with
typing it yourself as the escape hatch. **Node 12 was introduced specifically to make
picking from a list unnecessary** (PRD §5, node 12: "asking the user to re-select it from a
list is work the app can do itself"), and the list is now on the happy path. Its copy no
longer claims to have saved anyone the trouble, and W2 moved from "the manual half of the
fallback" to "the escape hatch off the confirm screen". If auto-fetch is meant to keep its
point, the honest shape is `P7 → P7B` with W1 as the escape — which is what it was. Flagged
rather than quietly re-argued.



**§5.14 — The key travels: the household sends key cards, and the flow ends at a door,
2026-08-17.**

Three owner directions, one metaphor. Node 4 made the profile a key; now node 18a *sends*
keys, and the flow ends by *using* one.

**Node 18a is reframed from invites to keys.** The blank member card (same artwork,
smaller, static) sits in the visual half; picking a contact sends them their key, and the
sent state shows the card carrying their name. Mechanics unchanged: the key travels to
their phone, the phone never changes hands. ⚠ The missing per-invite disclosure (removed
2026-08-06) gets LOUDER under this metaphor, not quieter — *"you decide what each key
opens"* is now said on the screen, and nothing anywhere lets you decide it.

**The tour (C1/C2/C3) is removed.** Three things went with it, each of which had exactly
one home there and now has none:
- **The privacy receipt** (C1) — the repayment of node 4's promise. §5.6 argued leading
  the tour with privacy was right; there is no tour to lead. The promise is now made once
  and never repeated.
- **The agent's introduction** (C2) — the product's first-person "I" introduces itself
  nowhere before Home starts speaking as it.
- **The roadmap line** (C3) — cameras, locks and the vacuum are now mentioned nowhere in
  first run. That closes C3's unchecked-claim risk by removing the claim.

**The flow ends at a door (`D1`, node 23).** A closed door, the lock, and the key card
made on node 4 — carrying whatever name and picture were typed there. Drag the card to
the lock, or tap it (it glides up by itself), or press Enter; the LED flares, the lever
turns, the door swings on light, and Home is on the other side. Reduced motion goes
straight through. **There is deliberate symmetry here:** node 1's drag-to-open door was
removed on the morning of the same day; the door comes back at the end, and this time you
hold the key.

⚠ Two flags on `D1`: the lock is drawn **beige**, from the owner's reference — a
non-palette hue on a depicted real-world object, same open call as the 3D icons and the
SKU thumbnails. And the screen has **no CTA and no skip** — the gesture (or tap, or
Enter) is the only way on. The toll is one tap, but if it tests as a gate rather than a
delight, a quiet link is the fix.

⚠ Removing the simulate buttons from nodes 4 and 5 (owner, same day) leaves `A4E` and
`A5E` with **no on-screen entry point** — they are reachable from the review rail and by
hash only. The wireframes builder now reports them as orphan states, which is accurate
rather than a bug.



**§5.13 — Node 4 is the master key, 2026-08-17.**
The sheet now stops at phone verification. Node 4 became a full page, *Setup profile*, built
around a card that is the profile **and** the key: the owner's framing is that without it
there is no way into the home. Node 5 followed it out of the sheet and is a page in the
standard bottom-aligned structure.

**Everything on the card is live.** The artwork is supplied and used as the base — bevel,
grain, rule and key glyph are all in the image, and nothing in code redraws them. Four
things sit on top and every one is bound to the two fields underneath:

| On the card | Comes from |
|---|---|
| Avatar | initials of the first two words of the name, or a real picture off disk |
| Serif initial, top right | first letter of the name, in Instrument Serif |
| Name | the NAME field |
| Email | the EMAIL field |

What is typed survives leaving the screen and coming back — a key that forgot your name the
moment you walked away would be a poor key.

**⚠ THE DISPLAY NAME IS BACK, and this closes a hole this PRD opened the same morning.**
§5.11 recorded that the sheet frames had no name field, so nothing in first run collected
the name the household sees, with node 18a (invite family) downstream of that gap. Node 4
collects it again.

**⚠ Instrument Serif is loaded for exactly one character.** It is not a second body face.
A second serif use is a type-system decision and belongs in ADR-001, not in a screen.

**⚠ §5.2 is now unavoidable.** Two codes to enter — phone then email — before the box is
opened. Node 4 adds a profile step between them. Deferring the *email* verification past
the reveal is still the one-node move §5.2 argues for, and it is now the clearest win
available in this section.

**Node 5 opens ON node 4, not instead of it** (owner, 2026-08-17). The email code is a
bottom sheet over the Setup profile page, which stays visible behind a scrim. That is the
right relationship: the code is a check on this page's work, not a new subject, and the
address being confirmed is still on screen behind the ask. It reuses the same `.sheet` that
nodes 1-3 use — one sheet component, two grounds, a photograph in the sign-in and a page
here.

**The flow harness is interactive as of this change.** `field()` used to render a span with
a fake caret: it looked right and could not be typed into. It is a real input now, so every
form screen in all four renderings accepts typing, and node 5's code boxes take real digits.

⚠ **One copy deviation from the frame:** it reads *"Setup Profile"*; built as *"Setup
profile"*. M-06 is sentence case and machine-checked, and the owner's own description calls
it "the setup profile page".

**§5.12 — Every screen is bottom-aligned now, 2026-08-17.**
Four owner frames (nodes 6, 7, 8, 9) set a structure, and the instruction was to apply it
to the rest of first run. All 46 screens now share it:

```
status bar
( ← )                  circular, floating over the visual
┌────────────┐
│  VISUAL    │         takes whatever height is left over
└────────────┘
EYEBROW                pinned to the bottom, left-aligned
A big title
supporting copy
[     CTA     ]
quiet link
```

Four things changed, and each costs something worth naming:

1. **An eyebrow above every title.** New; it did not exist before. It gives the section a
   name ("Getting started", "Connecting", "Before we finish") without spending a nav bar
   on it.
2. **The close (×) is gone.** The frames carry a back arrow and nothing else. That removes
   the *exit setup* escape hatch from every pairing screen — it survives only where a
   branch genuinely needs it (the tour's *skip*, the invite's *skip*).
3. **The 4-dot setup stepper is gone.** No frame shows one. The 3-dot stepper on the tour
   (nodes 23a-c) stays, because it counts slides in a carousel rather than steps in a
   flow — a different job.
4. **Secondary actions dropped from full-size buttons to text links.** ⚠ **This is the one
   to argue about.** "Not now" on nodes 24 and 25 was deliberately a full-size button
   (`recipes.buttonQuiet`) because declining a permission has to stay first-class. It is a
   grey text link now, per the frames' hierarchy. The flow still continues identically
   either way; it just no longer *looks* like a real choice. Same change hits node 18's
   "Not now, I'll do that later".

**The title runs at 26, not 30.** Measured off the frames rather than assumed — cap height
≈ 17pt against the CTA label's 11pt. The sign-in sheet keeps `display` (30); these screens
use `title1`. That reads correctly: the sheet is one statement on a compact surface, these
carry two paragraphs and sometimes a list.

⚠ **The frames reintroduce hue-coded SKU thumbnails** (blue / teal / olive on node 6). The
2026-08-12 palette rule deleted exactly that, moving the three SKUs to depth within one
green family and recording it as a knowingly weaker signal. Built as supplied, because it
is the newer instruction — but both are owner instructions and only the owner can retire
one. If the palette rule wins, three CSS rules come out and nothing else moves.

⚠ **Node 7 lost its peel gesture.** The frame shows a static exploded view and a plain
*Continue*; the 2026-08-06 build made the polybag something you physically dragged off, on
the reasoning that the instruction most likely to be skimmed should be the one thing you
have to touch (§5.9). That reasoning has not been answered — it has been overtaken.
`peel()` is still defined and unused.

⚠ **Node 9's recovery is now behind a link.** *"Not blinking?"* used to be a bordered note
on the screen, because needing the hold-to-reset is the common case on a re-setup, not an
error. It routes to `P3F`, so the content is one tap away rather than gone.

**§5.11 — Nodes 1–5 rebuilt as one bottom sheet, 2026-08-17, and merged into the canonical
screen set.**
Seven owner frames replace five full-screen pages with a single surface: a full-bleed image
(video later) with a floating sheet that changes height and contents under you. Six states:
splash, login sheet, mobile number, mobile OTP, email, email OTP. Built as
`auth-prototype.html` (`build-auth.py`), every state addressable by URL hash for review.

**The merge, same day.** `build-prototype.py` — the canonical screen set behind all four
renderings, including the 45-screen flow published at `#noma/userflows/first-run` — now
imports these states rather than declaring its own account screens. One source, four
renderings, unchanged rule. The count moved 45 → 46 screens and 32 → 33 on the happy path,
because the splash and the login sheet are two halves of node 1 the way a screen and the OS
dialog over it are; the node count is still 23.

⚠ **The drag-to-open door is gone.** Node 1 was `doorway()` — the door you pulled open on
warm light, rebuilt four times across 2026-08-06 and documented in §5.10, §5.10a, §5.10b and
§5.10c. It was replaced on owner instruction, not because it stopped working. The function
is still defined in `build-prototype.py` and is now unused, so re-instating it is one line.
Those four sections are kept for the reasoning, but they no longer describe what is built.

The frames were followed exactly, which means four things changed that are worth an argument
rather than a shrug:

1. **Node 4 stopped being "create profile".** It collects an address and nothing else. The
   display name — *what the household sees next to a member* — now has no screen anywhere in
   first run, and node 18a (invite family) is downstream of it. This is the biggest of the
   four and it needs an owner, not a designer.
2. **The DPDP notice moved to node 1.** It rides on the login sheet's fine print, because
   node 4 is no longer the first collection of anything beyond a number. §5.1 was already
   open; this changes where the answer has to land, and makes it more urgent, not less.
3. **The country selector is gone** and +91 is hardcoded. Defensible for an India-first
   launch, invisible to reverse later.
4. **Node 5 verifies with a code, not a link.** The old design deliberately waited for a link
   so the mail client could be left open. A code is a real mechanism change, and it means
   §5.2 — two verifications before the box is opened — now costs *two* code entries.

Two smaller things, both reproduced from the frames rather than corrected, because the
instruction was to follow them exactly:

- **The mobile OTP state still says "What's your mobile number?"** over a code field. The
  email half of the run gets its own heading ("Enter OTP to verify your email"), so this is
  almost certainly a leftover frame rather than a decision. First thing to fix.
- **Nothing between node 2 and node 4 has a way back.** A mistyped number strands you on
  node 3: no back arrow, no "Edit number", though node 5 has both equivalents for the
  address. Node 5 is the model the other four should be measured against.

**§5.1 — There is no consent screen, and the DPDP Act probably wants one.**
The 2026-08-05 build had a scroll-gated privacy screen plus an analytics opt-in. The diagram
has neither. Under the DPDP Act 2023 an itemised notice must precede processing, and a
room-linked air reading in a named home is personal data. The prototype puts a notice block
plus a *Read the privacy notice* link on node 4 — the first collection of anything beyond a
phone number — which is the most defensible place available inside this flow. **That is
weaker than what the Act asks for, and it is a legal question, not a design preference.**
Get a referee. If the answer is that a standalone screen is required, it goes between nodes
3 and 4 and the node count becomes 27.

Consequence of dropping the analytics opt-in: `C-11` is no longer *blocking* first run — it
is simply unasked. The flow ships with no consented telemetry at all, which means the funnel
below cannot be measured. That was already the state of the world; it is now also invisible.

**§5.2 — Two verifications back to back is the longest unrewarded stretch in the flow.**
Nodes 2–5 are OTP, then name, then email, then wait-for-a-link — five screens, four of them
admin, before the box is even opened, and the email round-trip leaves the app entirely.
Every reference app in the teardown gets to *something* before asking twice.
**Recommendation:** collect the email at node 4 and defer the *verification* to after the
reveal, or to first use of a recovery flow. The account is already usable — the phone number
is the credential. **The diagram says verify here, so the prototype verifies here.**

**§5.3 — The reveal has no screen at all now, and that is the open risk.**
`J-WEEK-01` — emotional target *quiet shock* — was screen 2.12 in the original spec and is
the mechanism the entire first week hangs off. It has been reduced twice: first to node 22
(a wait that resolved into Home), then, on 2026-08-06, **removed entirely along with nodes
19–22.**

As built, first run ends: notifications dialog → Home, with `34 · AQI` already on screen. No
step takes a reading, and nothing marks the moment. The number is just *there*.

That may well be fine — arguably better than a ceremony — but it is now **entirely Home's
job to land it**, and Home was specced assuming the reveal had already happened elsewhere.
Two things to settle, both in `F-AQI-LIVE` rather than here:

1. **The empty window.** If the sensor needs ~20s to produce a first reading, Home's first
   paint has nothing to show. It needs a real loading state, not a zero or a skeleton that
   looks like a reading.
2. **Whether the standard card carries the weight.** The reading card in §7 was designed for
   day 40, not minute 12. If first-week retention depends on this moment, a first-run variant
   of the card is cheap insurance.

**§5.4 — RETIRED 2026-08-06.** Previously: node 6 offered four device *categories* (purifier,
camera, lock, vacuum) sourced from `firstRunDeviceTypes`, three of which could not be bought.
**Closed by the owner:** node 6 is not a device-type chooser at all. It offers the three
purifier SKUs that exist — `HW-PUR-200` / `HW-PUR-500` / `HW-PUR-MAX` — as three horizontal
cards, stacked vertically, matching the confirm-card shape used at node 11. Camera, lock and
vacuum do not appear at node 6 or anywhere else in this flow. The only remaining trace of the
old four-category framing is node 23 slide 3 ("One app, whole home"), which is now the single
place in the flow that names a future device category — see the node 23 row in §5, and cut
the line if that roadmap claim isn't real.

**§5.5 — Two permission problems.**
*One:* node 19 says *"we'll notify you when it's done, you're welcome to close the app"* —
the best sentence in the reference set — six screens before notification permission is asked
at node 25. Either move the ask to node 19, where it earns itself, or stop promising it.
*Two:* geofencing at node 24 needs `Always` location to work; the dialog must still ask for
**While Using the App**. iOS will escalate on its own once the pattern is established, and an
app that asks for Always during setup gets denied. The screen also promises *"we never keep a
trail of where you've been"* — that has to be true in the implementation, not just the copy,
and it sits one screen after the privacy slide.

**§5.6 — Leading the tour with privacy is right.**
Unusual, and correct here: it is said once as a promise at node 4 and repeated at node 23 as
a receipt, after the device has already worked. The cost is saying it twice; the gain is that
the second time it is verifiable. The other two slides restate things the flow has already
demonstrated, which is the right register for a tour that runs *after* the product works —
the previous build's argument for moving it here survives the rebuild intact.

**§5.7 — The node 15 carousel, and why it is the only place a pitch belongs.**
Added 2026-08-06 (owner). Node 15 is the one screen in the flow with **dead time the user
cannot shorten** — the join takes as long as it takes, and there is nothing to tap. That
makes it the only honest place to put feature marketing: it fills a wait rather than
inserting one. (Contrast node 23, which *is* an inserted wait, and survives only because it
runs after the device already worked.)

Shape: a headline, a miniature app screenshot **masked to zero opacity at its lower edge**,
and four dots. Four slides, crossfading every **2.2 s**. The screenshots are four shots of
*the same app* — shared status bar, greeting and title, only the body changes — so it reads
as a product, not as four pieces of art.

Three constraints on it:

- **Crossfade at `standard`, never spring.** This sits directly on top of a progress bar on
  an ambient surface: `.claude/rules/motion.md` gate 4.
- **Auto-advance is disabled entirely under `prefers-reduced-motion`** (gate 2). The dots
  remain real buttons, so the carousel is hand-drivable either way.
- ⚠ **WCAG 2.2.2 (Pause/Stop/Hide).** Auto-advancing content that runs more than five seconds
  needs a pause affordance. Four slides at 2.2 s is an 8.8 s loop that repeats for as long as
  the join takes. Tapping a dot resets the timer, which is *not* the same as pausing. **If
  real-world joins routinely exceed ~10 s, this needs an explicit pause control** — decide
  from join telemetry, not from taste.

The copy on all four slides is provisional (`C-2`), and slide 3 ("One app for everyone at
home") plus node 23 slide 3 are now the only two places in first run that promise anything
beyond a purifier.

**§5.8 — Both permissions now fire right after the device connects.**
Moved 2026-08-06 (owner). Nodes 24 and 25 used to sit at the end, after the home was named
and the household invited; they now run immediately after node 16, and node 23 lands straight
on Home. The tail is `16 → 24 → 25 → 17 → 18 → 18a → 23 → 26`.

**What it buys.** Both OS prompts fire as one block at the flow's strongest moment — the
device has just visibly worked, and "connected" is the only unambiguous win in the whole
sequence. Asking there is asking from strength. It also stops the prompts from interrupting
the naming-and-household run, which is a single coherent task the user is now allowed to
finish without an OS modal landing mid-way.

**What it costs, and this is worth watching.** The asks now arrive *before the product has
any shape*: no named room, no named device, no reading. Node 24's pitch is
*"start cleaning about twenty minutes before you get back"* — made about a device that has
no room yet, in a home that does not exist yet. That is a weaker frame than the same sentence
would have after node 17, when there is a Bedroom to talk about.

**How to tell if this was wrong:** grant rate on node 24. If it drops, the cause is almost
certainly that the ask now precedes the context that made it make sense, and moving node 24
alone back behind node 17 — keeping node 25 where it is — recovers most of it. Do not
re-litigate this from taste; it is a measurable question and cheap to instrument the moment
`C-11` clears.

⚠ **Not yet reflected in copy.** Node 24 and node 25 still speak as though a device is set up
and placed. Their strings should be reread against the new position before anything ships —
"your purifier" is fine, "your bedroom" would not be.

**§5.9 — The interaction layer.**
Added 2026-08-06 (owner), after the verdict that the flow "looks too boring, too mundane…
this is going to be our main attraction point." That was correct: every node was a headline,
a graphic and a pill button. Correct, and inert. Five nodes now carry a real gesture:

| Node | Gesture | Why there |
|---|---|---|
| 1 · Get started | **Slide to enter; the camera moves through the doorway** | It is a *home* app. You do not tap "Get started" to enter a house. This screen sets the expectation for how everything after it behaves, which is the whole reason it stopped being a button. Rebuilt again 2026-08-06 — see §5.10. |
| 7 · Unwrap the filter | **Drag the tab; the polybag peels off** | The one setup failure that is completely invisible — a bagged filter behaves normally in every other respect. The instruction most likely to be skimmed became the only thing on screen you have to touch. |
| 11 · Pair | ~~Press and hold; the ring fills~~ **REMOVED 2026-08-17 evening (owner)** | Now a device-left / phone-right connection animation that resolves itself — no button, no skip, auto-advances on the check. The honesty argument survives in a different form: the wait resolves itself and the stay-near instruction moved into the copy. |
| 17 · Which room | **Tap a room; the isometric drawing morphs into it** | See below — the centrepiece. |
| 26 · Home | **The AQI number counts up from zero** | The first number the user ever sees should arrive, not merely be present. |

**Node 17 is the one that matters.** Six rooms across a horizontal selector; below it a
single isometric drawing that *morphs* — four furniture slots interpolating position,
footprint, height and tone at once, so the bed becomes the sofa becomes the kitchen counter.
The piece count is fixed at four on purpose: morphing needs slot-for-slot correspondence, so
nothing ever pops into or out of existence. Depth order is recomputed every frame because
pieces genuinely swap front-to-back mid-morph.

Crossfading two drawings would say *"here is a different picture."* Morphing says *"this is
the same room, and you are deciding what it is"* — which is precisely the decision the screen
is asking for. That is the difference between decoration and interaction design, and it is
why this is worth the code.

**Three rules every one of these follows, without exception:**

1. **The gesture is the delight, never the toll gate.** Every one also completes on a plain
   tap, and on Enter/Space, because it is a `<button>`. A prototype advanceable only by
   dragging excludes switch and keyboard users, and a *product* built that way would be
   indefensible. Node 11 explicitly treats a sub-180ms press as "tap → complete".
2. **`prefers-reduced-motion` collapses each to an instant state change** (motion gate 2).
   Verified: the door, peel, hold, morph and count-up all resolve with no animation.
3. **Spring is correct here, and only here.** `.claude/rules/motion.md` opens with "playful
   and springy on discrete moments, still on ambient ones". Choosing a room, opening a door
   and peeling a wrapper are discrete moments — the room morph uses easeOutBack. The Home
   count-up is an *ambient reading*, so it uses `standard` with no overshoot (gate 4).

⚠ **Still flat, and candidates for the same treatment:** nodes 2–5 (the account run) are four
consecutive form screens with no moment in them, and node 8 (plug in and switch on) is a
static illustration of a physical act. If the "main attraction" bar applies to the whole
flow, the account run is where it is furthest from being met.

⚠ **This is a prototype, not a spec for production motion.** The gestures are proven to feel
right; the implementations are CSS/SVG/rAF written to survive a review, not a design-system
contribution. Do not port this JavaScript. Port the *behaviour*, with real tokens.

**§5.10c — Node 1: light from behind the door, progressive slider, white dissolve.**
Three owner corrections, 2026-08-06.

**The light is behind the door, so nothing near it may be dark.** The door had a dark drop
shadow and a dark contact shadow — which reads as *the space beyond is dark*, the exact
opposite of what the door is promising. Both are gone. The door is now haloed in white with
the faintest green cast, light pools on the floor in front of it, and the leaf's outer shadow
is white (`rgba(255,255,255,.95)`), not black. Both the halo and the pool **brighten with the
drag** — as the leaf cracks, more light escapes. The only remaining dark values on the door
are an `inset` shading on the leaf face, which is what makes it read as a panel rather than a
flat rectangle, and a 1px hairline edge.

**The green arrives with the thumb, not after it.** The track's fill and both labels are
driven straight off `--p`, so at 50% dragged the track is 50% green and "Enter Home" /
"Entering Now…" are mid-crossfade. Measured: `p` 0 / .25 / .5 / .75 / 1 → green 0 / .25 / .5
/ .75 / 1. Previously the whole green state was binary and only fired on commit, which meant
the drag had no feedback at all until it was already over.

**Entering the white, and dissolving out of it.** The white now lives on **`.phone`, not
inside the screen** — `render()` destroys `.scr` at the hand-off, so a white layer inside it
vanishes at exactly the moment it is doing its job, which is why the effect disappeared in
the previous pass. On `.phone` it survives the swap, so the next screen genuinely emerges
*out of* the white rather than sliding in under it. Measured: copy and slider at zero by
~560 ms, the doorway owns the viewport by ~1400 ms, pure white at ~1680 ms, hand-off at
1700 ms, dissolve complete by ~2500 ms.

Two implementation notes worth keeping if this is rebuilt:
- The veil needs a **forced reflow** (`void veil.offsetHeight`) between append and adding the
  class. A `requestAnimationFrame` is not enough — the browser coalesces the two into one
  style pass, no transition runs, and the veil snaps to white from frame one, hiding the
  whole sequence.
- Its removal is scheduled **at creation, untracked, as a hard backstop**. A veil that
  survives an interrupted hand-off is an opaque white page with no way out. Verified against
  a deliberately interrupted entry.

**§5.10b — Node 1, fourth pass: measured to the reference, and made seamless.**
Two defects the owner named, both real:

**"The door is floating, the walls aren't connected."** Correct, and it was structural rather
than cosmetic. The corridor was five CSS-transformed `<span>`s — `rotateY` walls, `rotateX`
ceiling and floor. Separately rasterised planes cannot be made to meet: the joins showed
hairlines and the doorway read as pasted in front of the wall instead of set into it. It is
now **one SVG in a 390×844 viewBox where adjacent surfaces share their corner coordinates**,
so a gap is not expressible. The aperture's four points — `128,158 → 262,394` — are the same
four points the ceiling, both walls and the floor terminate on. A contact shadow at the door
base grounds it on the floor. Note the bottom corners belong to the **walls**, not the floor:
that is what produces the reference's bright central path with grey outer corners.

**"The placement is very low."** Measured off the reference and matched to within 0.1%:

| | reference | built |
|---|---|---|
| Door aperture | 18.7% → 46.7% | 18.7% → 46.7% |
| NOMA centre | 69.5% | 69.5% |
| Body centre | 75.9% | 75.8% |
| Slider | 85.1% → 91.4% | 85.1% → 91.4% |

Copy and slider are absolutely positioned **over** the scene rather than stacked beneath it,
because in the reference the corridor floor runs behind the text to the bottom of the screen.

**The exit is now white-on-white.** Measured: copy and slider reach zero opacity by ~500 ms —
before the travel is meaningfully under way — the scaled aperture owns the viewport by
~1540 ms, the flash completes at ~1760 ms, and the handover fires at 1700 ms. Nothing of the
first screen is visible when the second arrives.

**§5.10a — Node 1, third pass: built to the owner's mock, and the walk-through fixed.**
The second pass interpreted; this one follows. Rectangular white door (not the arch), black
pill handle, straight-walled corridor in the mock's neutrals, **NOMA** wordmark letterspaced
over "A calmer kind of smart home.", and a full-width slide track reading **Enter Home** —
switching to **Entering Now…** over a green fill while the sequence plays.

The walk-through is now staged, which is what the previous pass got wrong (it whited out
before the travel read as travel): ① the leaf swings fully open (~0.8s) → ② the camera
travels *through* the frame, the white interior growing until it swallows the viewport
(1.25s, overlapping) → ③ only then does the flash finish and the next screen arrive out of
the same white. One rendering subtlety worth keeping: the travel is capped at **z=600px,
deliberately under the 640px perspective** — measured at rest the interior overshoots every
phone edge by ~900px, but push past the perspective distance and the browser culls the plane,
blinking the page background through for a beat. Caught on a slowed-down run.

⚠ **The green entering-state comes from the owner's mock** and contradicts the 2026-08-05
"no accent green in this file" direction. Used as supplied. That makes it the only green in
first run — fold it into C-14 rather than resolving it silently here.

**§5.10 — Node 1 rebuilt (second pass), and the two tour slides that were still flat.**
Second pass on the interaction work, 2026-08-06, against the owner's reference (the Finvu
"unlock wealth" portico sequence). Three changes:

**Node 1 is now a threshold you cross, not a door that opens.** The structure is taken from
the reference and the subject is ours: scene on the top ~60%, then headline and one line of
body, then a **slide-to-unlock track** at the foot. The slider *scrubs the approach* — drag
and the camera creeps toward the door, the leaf cracks, the warm light behind it widens.
Complete it and the sequence plays: the frame rushes past the viewer, the leaf swings wide,
the room whites out, and we are inside.

The change from the first attempt matters. A handle only reads as a handle once you have
noticed it; a track with a knob and an arrow is the most legible "do this" affordance on a
phone, and it leaves room for the headline and body. **Commit threshold is 62%**, not 82% —
a thumb that runs out of track at 80% must not feel refused. Tap and Enter still complete it.

**Node 17's drawing was framed by nothing.** The SVG viewBox was `0 0 320 210` — a box chosen
before the art existed — so the room sat high and the kitchen fridge (the tallest object, on
the far grid corner) clipped off the top. Reframed to `9 -25 302 180`, computed from the
actual content bounds: x 43…277, y −12…142.5. Verified across all six rooms after the morph
settles; every one now sits inside the stage with clearance top and bottom.

**Node 23's three slides now animate the claim rather than illustrate it.** They were static
CSS shapes at 250px. Now 298px, pure CSS/SVG keyframes — no JS, so nothing to wire and
nothing to leak:

- **Your data stays home** — seven readings drift inside the house outline and never cross
  it; the boundary breathes; exactly one thing comes *in* from outside, which is the outdoor
  air `ai-integration.md` §10 flags as the sole exception. The narrowing is drawn, not
  asserted.
- **It runs itself** — specks are drawn in from every edge, the orb pulses as it works, clean
  rings push back out, and two receipts tick in. The only thing never touched is the thing
  doing the work.
- **One app, whole home** — one hub, four devices, wires that draw themselves in turn. The
  three that are not the purifier are drawn faint, matching the honesty node 6 now enforces
  by not offering them at all.

⚠ All three still restate the same reservation as before: **this is prototype code.** The
timings and the feel are the deliverable; the CSS is not a design-system contribution.

---

### Rules that survive any ordering

1. **State the reason.** Every instruction screen, no exceptions.
2. **The device is the subject of every failure sentence, never the user.** "We couldn't find
   your purifier", not "You didn't hold your phone close enough."
3. **Name the wait before it starts, and release the user from it** — *"about a minute"*,
   *"you're welcome to close the app."*
4. **Errors are inline and keep what was typed.** Never a full-screen error for a wrong
   password or a wrong code.
5. **A working device is never stranded behind a network error.** Say what still works.
6. **No OS dialog fires without the screen behind it explaining why.**

---

## 6. Acceptance criteria

1. **The built flow matches §5 node for node.** 22 main-line nodes plus branch 18a, in that
   order, nothing inserted and nothing dropped. The prototype asserts this at build time; the
   shipped app needs the same check in a test.
2. Cold install to Home is **≤ 22 minutes** and, on a working 2.4 GHz network with no
   firmware update pending, **≤ 30 screens**.
3. **No OS permission dialog appears before node 9**, and every dialog has the screen that
   explains it rendered behind it. Grep for the dialog-trigger call sites.
4. **The location dialog requests While-Using, never Always** (§5.5). Grep for the
   authorization constant.
5. **Every** setup screen carries a stated reason. A screen with an instruction and no *why*
   fails review.
6. All 15 edge states listed in §5 are implemented and reachable in QA via a forced-failure
   build flag.
7. The Wi-Fi list hides 5 GHz SSIDs **and** renders the explanatory line. Hiding without
   explaining is a defect, not a simplification.
8. `prefers-reduced-motion` is honoured on every screen in the flow
   (`.claude/rules/motion.md` gate 2).
9. The AQI reading on Home animates with `standard`, never `spring` (gate 4). **And Home has
   a real first-paint loading state** for the window before a first reading exists — see §5.3.
10. Branch 18a is skippable at every point and never blocks reaching Home. **No step in it
    requires the invitee to be physically present, or uses the owner's handset to capture
    their consent.**
11. `R3B` is generated from the home's actual devices and members. A static disclosure that
    does not match what the invitee will really see is a defect.
12. **A `ConsentRecord` is written at node 4** with purpose, version and timestamp — whatever
    §5.1 resolves to. A flow that collects a name and an email and records no consent is not
    shippable in India.
13. Every string in this document exists as an i18n key with an `en` and a `hi` value.
    Zero hardcoded copy (`.claude/rules/voice-and-language.md`).
14. Minimum touch target 48×48pt and minimum body size across the whole flow — P2 sets the
    floor, and this flow is the one place low-fluency users cannot route around.

## 7. Design

- Surfaces: `surface.canvas` for instruction screens, `surface.warm` for the sheet-like
  confirm screens, `surface.raised` + `elevation.card` for device cards.
- Radius: `radius.md` on buttons and outlined cards, `radius.xl` on the elevated reading
  card, `radius.full` on suggestion chips.
- Accent: **one** `accent.solid` CTA per screen. The 4-dot stepper across nodes 7–17 has an
  `accent.bright` active dot and `border.hairline` inactive dots. The stepper does **not** get
  a green fill bar — that would spend the accent budget on chrome. **One stepper only**, the
  SmartThings mistake.
- Node 6, narrowed 2026-08-06: three horizontal cards, one per purifier SKU, stacked
  vertically — the same anatomy as the device-confirm card at node 11, not a grid. One card
  carries the selected treatment; there is no "coming soon" state, because every option shown
  can actually be bought.
- Error surfaces use `surface.warm` and near-black type. ⚠ **`colors.status` is `null`** —
  there is no warning or critical token, and green cannot carry "bad". Error screens
  therefore ship neutral until `O-6` closes. Flagged, not invented.
- Illustration: single-weight line drawings on `surface.sunken` tiles. Consistent with
  "friendly and approachable, soft rounded forms". Never a photorealistic product render
  in an instruction step — it competes with the instruction.

**Motion** — existing patterns only, no new ones:

| Moment | Pattern |
|---|---|
| Every tap | `MO-PRESS` |
| Screen-to-screen | slide with `standard` at `base`. **No spring on forward navigation** — a wizard that bounces feels unstable. |
| Device-type grid, node 6 | `MO-STAGGER`, `stagger.grid` |
| Found-device card, node 11 | `MO-POP` |
| Failure screen entering | `MO-POP` with the spring **removed** — `standard` at `base`. Gate 5: if a surface signals something wrong, it does not play. |
| Progress labels, nodes 15 / 20 / 22 | crossfade at `base` |
| Home's reading, first paint | `MO-POP` for the card, `standard` for the number, then `MO-BREATHE` |
| Carousel, node 23 | slide at `base`. Dots do not spring. |
| Feature carousel, node 15 | **crossfade only**, `standard`, ~550ms. No slide, no spring — it sits on a progress bar (gate 4). Auto-advance suppressed under reduced motion (gate 2). §5.7 |
| Invite sent, node 18a | `MO-TOAST` |

## 8. Copy

Not written as keys yet — **blocked by `C-2`.** Five different names for the product and
the assistant are in circulation, and the node 1 headline, both permission dialogs, node 23
slide 2 and the agent's line on Home all contain one. Keys land under
`src/i18n/locales/{en,hi}/onboarding.json` (currently a stub) once `C-2` closes.

### 8.1 · The voice — rewritten 2026-08-06 to converse rather than instruct

Owner direction: the flow should read as a conversation, not a set of instructions. Full
rule set, grammar mechanics and a banned/approved vocabulary now live in their own document —
`docs/voice/voice-prd.md` (typeset: `docs/voice/NOMA-Voice-PRD.pdf`) — this
section is the summary as it applies to this flow specifically. Seven rules:

| | Rule | NOMA |
|---|---|---|
| 1 | **First person, singular.** The app speaks as itself | *"I'll need Bluetooth for a minute."* |
| 2 | **Ask, then say why, plainly** — the reason is the subtitle, never omitted | *"Where does it live?" / "So I can compare your air against the right patch of outdoors."* |
| 3 | **Take the anxiety out of the answer** | *"Only really matters once there are two of them."* |
| 4 | **"Let's" for shared work** — collaborative, never imperative | *"Let's get the filter out of its bag."* |
| 5 | **Privacy as a concrete negative**, not a policy | *"I only notice you crossing in and out. I never keep a trail of where you've been."* |
| 6 | **Warm buttons at warm moments** | *"Yes, do that" · "It's on" · "Done — it's back in"* |
| 7 | **Observation → offer → ask**, in that order | *"It's 168 out there. I've already started."* |

**The home register.** The copy talks about the house as a place the app looks after:
*"Which one did you bring home?"*, *"Now find it a socket"*, *"Anywhere near where it'll
live"*, *"What I learn stays here"*, *"That's the hard part done"*. The email is *"a spare
key"*. This is the difference the owner asked for — the app is a housemate, not a setup
wizard.

**Two things deliberately NOT made conversational:**

1. **The instruction inside an instruction screen.** The frame is warm; the step itself stays
   literal. *"One press of the power button — you should hear the fan pick up"* is friendly
   and still unambiguous. Node 7 (unwrap the filter) and node 9 (the blinking light) are
   success-critical and physical: charm there costs comprehension, and P2 sets the floor for
   the whole product's actual effectiveness.
2. **System dialogs.** The iOS permission sheets keep Apple's register. They are not ours to
   write, and a chatty system dialog reads as a fake one.

⚠ **What adopting "I" commits us to.** The app now has a first-person voice from screen one —
before the agent has been introduced or done anything. That is consistent with
`ai-integration.md`, which already specifies a first-person agent, and it is exactly what
makes this register work. But it is a product decision, not a copy decision: **`C-2` is still
open, so whether "I" is the product or a separately-named assistant is undecided.** If they
turn out to be different characters, every "I" in this flow has to be re-attributed. Resolve
`C-2` before these strings become i18n keys.

### 8.2 · Rules that survive whatever the name turns out to be

1. **State the reason.** Every instruction screen, no exceptions.
2. **The device is the subject of every failure sentence.** Never the user — and now never
   "we" either: it is *"I can't see it yet"*, *"It's on Wi-Fi, but it can't reach me."*
3. **Name the wait before it starts, and release the user from it** — *"Fifteen seconds or
   so."*, *"Open it anywhere — I'll notice."*
4. **An error offers the next move, not a verdict** — *"Worth another look?"*, *"Usually it
   just needs a small nudge."*

`hi` is required for the whole flow, not deferred. A resident persona with low app fluency
in an Indian home is exactly the case where an English-only setup fails. ⚠ **This voice raises
the translation bar considerably** — *"a spare key"*, *"hum away happily"* and *"already
spoken for"* are idioms, and a literal Hindi rendering of any of them will read as broken.
Budget for transcreation, not translation.

## 9. Risks

| Risk | Mitigation |
|---|---|
| **No consent screen; DPDP notice rides on node 4** (§5.1) | Legal question, not a design one. Get a referee before build. If a standalone screen is required it goes between nodes 3 and 4. |
| **Two verifications before the box is opened** (§5.2) | Measure drop-off at node 5 first. The fix — defer email verification past the reveal — is a one-node move, not a redesign. |
| **The reveal has no screen at all** (§5.3) | Reopened 2026-08-06 when nodes 19–22 were cut. `J-WEEK-01` now depends entirely on Home's first paint. Needs a loading state and possibly a first-run card variant — both in `F-AQI-LIVE`. |
| ~~Node 6 shows three devices nobody can buy~~ (§5.4) | **Retired 2026-08-06.** Node 6 is three purifier SKUs now; no device-type chooser exists. Node 23 slide 3 is the only remaining roadmap claim — cut it if untrue. |
| ~~Node 19 promises a notification before permission is asked~~ (§5.5) | **Moot 2026-08-06** — node 19 was removed. The location half of §5.5 (While-Using, never Always) still stands. |
| **Firmware update has no path anywhere** | Removed from setup 2026-08-06 and not respecced elsewhere. If devices can ship with stale firmware this needs an owner. |
| **Per-invite disclosure removed with `R3B`** | Inviting someone now grants access to everything with no screen saying so. Hard to defend for a privacy-led product; needs a decision, not a silent gap. |
| `C-2` unresolved → the flow cannot be written in final copy | Ship the structure; treat every string as provisional. Do not let copy block the interaction design. |
| `C-3` unresolved → node 18a is shape-only | Build `R3`, `R3B`, `R3C` and the member list, which are role-agnostic. Leave role options as data. |
| `C-11` unresolved → cannot measure any of this | The diagram drops the analytics opt-in entirely, so there is now no consented telemetry and no screen where it could be asked. **The flow ships blind, and the fact that it is blind is now itself invisible.** |
| 5 GHz-only routers are common in Indian metros | Node 13 covers it, but the true fix is dual-band hardware. Raise with hardware; a copy fix on a hardware limitation has a ceiling. |
| Someone "simplifies" the two-screen nodes into one | Nodes 9, 11, 19, 24 and 25 each split for a reason stated in §5. Splitting an OS dialog from its explanation is the difference between a permission that gets granted and one that does not. |

---

## Declares

**Data** — `Person` (id, phone, **displayName**, **email**, **emailVerifiedAt**) — the last
three are new, and node 4 is where they are collected · `Home` (id, name, createdAt, ownerId)
— **created at node 17, not before** · `Membership` (homeId, personId, role, deviceGrants[],
expiresAt, invitedBy, state: pending/active/expired/declined/revoked) · `Device` (id, HW-*,
homeId, roomId, displayName, pairedAt, firmwareVersion) · `ConsentRecord` (personId, purpose,
granted, version, timestamp) — **required by DPDP, absent from
`memory/architecture/data-models.md`, and now written at node 4 with no screen of its own.
See §5.1.**

**Permissions** — `bluetooth` (node 9, required, blocks pairing if refused) ·
`location.whenInUse` (node 24, optional, gates the geofence trigger in `F-AUTOMATIONS`) ·
`notifications` (node 25, optional).

**Events** — **`none`.** Zero events exist and the taxonomy cannot start:
`.claude/rules/analytics.md` requires every event to map to a `J-*` step, and `C-11`
(on-device privacy vs. any analytics SDK) is unresolved. When it closes, this flow is the
**first** thing to instrument — funnel drop-off per screen and per failure state is the
only way to know whether any of the above works.

**Hardware** — `HW-PUR-200`, `HW-PUR-500`, `HW-PUR-MAX` — all three purifier SKUs, chosen at
node 6. `firstRunDeviceTypes` (camera, lock, purifier, vacuum) is no longer consulted by this
flow; node 6 offers purifier sizes, not device categories. Capabilities required: BLE
provisioning, 2.4 GHz Wi-Fi join, factory reset via physical control, ring-LED
pair/steady/error states, remote identify (blink), OTA firmware.
⚠ **`identify` and the LED state vocabulary are not in `src/hardware/feature-map.json`** —
nodes 8 and 11 depend on hardware behaviour nobody has confirmed exists (`O-9`), and four
screens plus two edge states are written against it.
