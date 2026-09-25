# AI Integration — the agent model

> Source: `air-agent-app.html` ("Air Agent — agent-first sample UI, C2"), corroborated
> by the agent surfaces in the launch-app prototype. Extracted 2026-08-04.
> Feature ID: `F-AGENT-PROPOSE` in `src/hardware/feature-map.json`.

**This is the architectural spine of the product, not a feature bolted onto it.**
The prototypes are explicit: the home screen is not a grid of devices, it is a list
of things the agent has decided, is proposing, or has already done. Read this before
designing any screen involving the agent — the trust mechanics below constrain
layout, copy, and motion.

---

## 1. The problem it solves

Air is invisible, and so is protection. From the Week One doc, stated plainly:

> Invisible protection that runs silently is, to the user, indistinguishable from a
> switched-off box.

This is the **away-mode trap**: a perfectly-working automation that never narrates
itself destroys the reason to open the app, and eventually the reason to keep the
device plugged in. So the agent's job is not only to act — it is to *account for
itself*. Narration is a retention mechanism, not chrome.

---

## 2. Home is three zones, in this order

| Zone | Contains | Prototype label |
|---|---|---|
| 1 · Settled | What is already fine. Per-room readings. | "Settled now" |
| 2 · Needs your call | Proposals awaiting a decision. Badged with a count. | "Needs your call · 1" |
| 3 · Done today | Completed actions, each still undoable. | "Done today · 2" |

The ordering is deliberate and worth preserving: **reassurance first, then the ask,
then the receipt.** Someone opening the app anxious gets "air is clean in 2 rooms"
before they are handed a decision.

---

## 3. Graduated autonomy — per capability, three levels

The single most important mechanic. Autonomy is **not global** and **not binary**. It
is granted one capability at a time, and starts at the bottom.

| Level | Behaviour |
|---|---|
| **Ask me** | Agent proposes. Nothing runs without a tap. **Default.** |
| **Act & tell me** | Agent acts, then reports. Undo remains. |
| **Act silently** | Agent acts without notifying. |

Capabilities in the prototype, each with an independent level:
`Adjust fan speed` · `Pre-clean before forecasts` · `Reorder filters`

Verbatim:

> Right now, I only ever propose. Nothing runs without your tap. As you approve
> things, you can let me act on my own — one capability at a time.

**Trust is earned with evidence, and the app says so out loud:**

> You've accepted 7 fan suggestions in a row — ready to let this run itself?

That is the promotion prompt: a count of consecutive accepts, offered back as the
reason. It means the system must keep a **per-capability accept/reject tally** — a
real data requirement falling out of a trust decision.

⚠ **Unanswered and safety-critical.** Every capability shown is comfort-grade (fan,
pre-clean, reorder). Whether the agent may ever act on a **lock**, or on anything
with a physical-security or health consequence, is never addressed. And
`Reorder filters` at "Act silently" means **spending money without asking**. There
is no safety classification for capabilities. See C-8.

---

## 4. The explanation contract — four fixed slots

Every proposal exposes a "Why this?" disclosure with the **same four slots, always in
the same order**. A contract, not a copy template:

| Slot | Job | Example from the prototype |
|---|---|---|
| **Sensed** | The evidence | "Outdoor AQI at 118 and climbing, forecast 182 by 10pm; bedroom holding at AQI 38 (PM2.5 9 µg/m³)" |
| **Decided** | The action | "Pre-clean 8:30–9:00 at medium, then hold windows-closed mode" |
| **Instead of** | The counterfactual | "Reacting at 11pm — which would run loud while you sleep" |
| **Obeys rule** | The constraint respected | "Quiet hours 11pm–7am stays intact" |

**"Instead of" is the unusual slot and the most valuable.** Explaining what the agent
chose *not* to do is what makes a decision feel considered rather than arbitrary.
Most assistant UIs ship the first two slots and stop.

**"Obeys rule" is a promise.** Naming the constraint it respected is how the agent
proves it is bounded. Ship the disclosure without this slot and standing rules become
unverifiable — the user has no way to know their rule held.

---

## 5. Rehearsal before execution

A proposal can be previewed as a **step-by-step timeline before it runs**, each step
individually editable:

```
8:30pm   start pre-clean        Bedroom only · medium · ~30 min       [Edit]
9:00pm   windows-closed mode    Recirculate · hold until AQI drops    [Edit]
11:00pm  respect quiet hours    Fan capped at 28 dB · standing rule   [Locked]
```

Two things to preserve:

- **"Nothing happens until you tap Run."** The rehearsal is inert.
- **Steps derived from a standing rule render `Locked`, not `Edit`.** A user cannot
  casually edit away their own constraint from inside a one-off plan. Rules change
  where rules live, deliberately.

---

## 6. Standing rules — goals, not one-time actions

Persistent constraints that bound every future plan. The prototype distinguishes them
from actions explicitly:

| Rule | Value | UI note |
|---|---|---|
| Quiet hours | 11pm–7am | Referenced by name in "Obeys rule" |
| Noise ceiling while asleep | 28 dB | "Lower is quieter but cleans slower. 28 dB is about a whisper." |
| Target overnight PM2.5 | under 12 | "The goal I'll hold the room to, not a one-time action." |

Note the copy discipline: each rule states its **trade-off** (quieter = slower) and
anchors its unit to something human ("about a whisper").

---

## 7. Promotion and reversal

- **"Do this always"** turns an accepted one-off into a standing automation. It
  appears on *completed* items too — the moment someone appreciates what it did is
  the moment to offer the upgrade. The Automation tab then separates
  `Created by your agent` from `Created by you`.
- **Undo** stays available on completed actions, including ones the agent took alone.
- Recurrence is offered contextually: *"Smog nights repeat this season — do this
  automatically."*

---

## 8. The chat thread is deliberately context-free

> Starting fresh — this thread does not carry over anything from Home.

An unusual and defensible call: the ambient agent (Home) and the conversational agent
(thread) are **separate sessions**. It keeps the thread predictable and stops home
state from silently steering a conversation. Anyone "improving" this by sharing
context should know it was a decision, and should say why they are reversing it.

Chat is **card-and-chip led**, not a bare text box. Chips seen:
`What happened at 7:12pm?` · `Handle cooking automatically` · `Prep for tomorrow's pollen`

The launch-app prototype shows the agent reasoning **across devices** in one turn —
rescheduling the vacuum because yesterday's camera footage showed construction
workers arriving at 8am. That cross-device inference is the most ambitious behaviour
in any of the material, and it is the hardest to deliver on-device (§10).

---

## 9. What the agent's voice does

First person, owns its actions, always ties a number to a consequence:

> "Tonight the AQI outside hits 200+. I'm on Auto in your bedroom — wake up and see
> what I held off."

> "Heading out? I'll stop wasting power. Geofence saw you leave. Dropping to Away
> Saver (Eco) — and I'll boost the bedroom back to clean 20 minutes before you return."

> "Good morning. While you slept, Delhi hit 187. Your bedroom never went past 22."

Pattern: **what I observed → what I did → what it means for you.** Never a bare
status. Full voice rules live in `memory/voice/ai-personas.md`.

⚠ The assistant is named inconsistently across sources — "Ding", "Noise AI Agent",
"Sanctuary Assistant". See C-2.

---

## 10. Privacy posture — a hard constraint

Stated repeatedly and specifically:

- **On-device AI.** "DPDP compliant. Your data never leaves home."
- Face data is stored **"only on your device. It is never uploaded to any server."**
- Face tagging is gated by an explicit consent sheet (Decline / Allow & Continue)
  citing the **DPDP Act 2023** by name.
- The camera event view is badged **"No cloud · DPDP compliant."**

This is India's Digital Personal Data Protection Act, 2023 — a legal obligation, not
a marketing line. Three consequences the prototypes do not resolve:

1. **"Never leaves home" and "uses tomorrow's forecast" cannot both be literally
   true.** A forecast-driven pre-clean requires an outdoor forecast, which is a
   network call. So is the CPCB outdoor blend. The claim needs narrowing to what it
   actually means (personal and biometric data stays local; ambient public data is
   fetched) before it appears in store copy, or it is a compliance exposure.
2. **On-device inference bounds model size and latency**, and therefore how clever
   the agent can be — including the cross-device reasoning in §8.
3. **Consent is per-feature, not per-app.** Declining face recognition must leave a
   working camera. No declined-state is designed anywhere.

---

## 11. Open questions this document raises

| ID | Question |
|---|---|
| C-8 | May the agent act on a lock, or spend money, at "Act silently"? No safety class for capabilities exists. |
| — | Where does the accept/reject tally live, and does one rejection reset the promotion counter? |
| — | What happens when a proposal's window passes un-actioned? "Later" and "Not tonight" exist; expiry does not. |
| — | Can two proposals conflict, and who arbitrates? |
| — | Is there a declined-consent state for face recognition? |
| — | How is a forecast obtained under "your data never leaves home"? |
