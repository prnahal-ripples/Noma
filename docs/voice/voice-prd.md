> # ⚠ SUPERSEDED 2026-08-14
> **The canonical voice document is now `docs/voice/noma-voice-guide.md`**
> (v1.2-draft). Do not write copy against this file.
>
> It is kept because the guide's rule IDs do not map onto this document's
> section numbers, so a commit or review citing the old §-numbers is only
> traceable here. Three things it said are now settled and changed:
>
> - **C-2 is closed.** There is one speaker; the app *is* the agent. Every
>   provisional "I" in this file is now ratified (guide §1, R-01/R-02).
> - **Indoor readings are PM2.5 in µg/m³, never AQI** (W-01). This file
>   predates that and its examples do not obey it.
> - **Em dashes are banned everywhere** (M-03). This file is full of them.
>
> The register survives almost intact. The mechanics are what moved.

# The NOMA Voice

| | |
|---|---|
| **Status** | draft — 2026-08-07, canonical source for `docs/voice/NOMA-Voice-PRD.pdf` |
| **Owner** | TODO(owner) |
| **Scope** | **App-wide.** The register the app speaks in everywhere — onboarding, ongoing surfaces (Home, notifications, agent narration), settings, sharing, errors, everywhere between. Started as an onboarding-only document; generalized 2026-08-07 once the register proved out. Onboarding stays the worked evidence throughout because it's the one surface fully rewritten and shipped — `docs/features/first-run/prd.md` §8. §13 tracks what's rewritten elsewhere and what isn't yet. |
| **Blocked by** | `C-2` (product + assistant name — every "I" in this document is provisional until it's settled who is speaking) |
| **Canonical for** | `memory/voice/tone-matrix.md` (all rows) · `memory/voice/glossary.md` (banned/approved words, §6) |
| **Extends** | `memory/voice/ai-personas.md` — the ongoing-product voice already approved (notifications, Home). This document generalizes that voice into one standard covering the whole app; §13 reconciles the two. |

---

## 1. Why this exists

The first build of onboarding copy was correct and lifeless. Every screen followed the same
shape — a headline stating what to do, a line of body text stating why, a button labelled with
the action. *"What's your number?" / "We'll text you a code." / [Send code]*. Nothing was
wrong with it. Nothing in it sounded like anyone.

The owner's instruction was specific: **stop writing instructions, start writing a
conversation.** The app should talk about the house, refer to itself as "I", and sound like
it's genuinely interested in getting this right for you — not administering a checklist. That
instruction wasn't scoped to onboarding; onboarding is just where the first prototype existed
to rewrite. **This document has since been generalized to the whole app** — the same seven
rules, the same grammar, the same banned words, wherever the app has something to say.

This document is the rule set that came out of that instruction. It is not a copy deck — the
actual onboarding strings live in `docs/features/first-run/prd.md` §8 and in that prototype's
source; other surfaces don't have a rewritten copy deck yet (§13). This is the *why* behind the
rules, written so the next hundred strings — wherever in the app they land — can be judged
against the same standard without re-deriving it.

## 2. What makes a setup flow feel like a conversation

A wizard and a conversation can carry identical information and still feel like opposite
relationships. The difference sits in two structural habits, not in word choice:

**A question and its reason arrive in the same breath.** If a screen asks for something, the
next sentence — not the help text, not a linked policy — says why. *"Where does it live?"*
followed immediately by *"So I can compare your air against the right patch of outdoors."*
Left to be inferred, or deferred to a privacy policy, the same ask reads as a form.

**Nothing is asked before the app has shown it understands the situation.** An ask that lands
cold, with no context, reads as a form filling itself out at you. An ask that follows an
observation about what's actually in front of the user — a device that just connected, a room
that needs naming — reads as something a person would say next, not a step in a sequence.

Neither habit is decorative. Both are trust-sequencing: the app earns the right to ask by
showing it already understands, before it asks.

## 3. The seven rules

Every rule below has a NOMA line already shipped in the prototype — these aren't aspirational,
they're a description of work already done, so they can be checked against the artifact.

### Rule 1 — First person, singular
The app is "I", not "we", not "the app", not a passive voice that names no one. "We'll text
you a code" becomes *"I'll need Bluetooth for a minute."* A team behind a curtain is a company;
a single voice is something you can have a relationship with.

### Rule 2 — Ask, then say why, in the same breath
The reason is never optional, never deferred, and never longer than the ask itself. *"Where
does it live?"* is immediately followed by *"So I can compare your air against the right patch
of outdoors."* If a screen asks for something and the reason isn't in the next sentence, the
screen fails this rule regardless of how warm its adjectives are.

### Rule 3 — Take the anxiety out of the answer
Setup questions are full of tiny stakes that don't need to be there — what if I get this wrong,
what if this matters later. Defuse it explicitly: *"Only really matters once there are two of
them"* about naming a device tells the user the question in front of them carries almost no
weight, so they can answer it without overthinking.

### Rule 4 — "Let's" for shared work
Anything framed as something both parties are doing reads as collaborative; the same content
framed as an instruction reads as administrative. *"Let's get the filter out of its bag"*
is a shared task. *"Remove the filter from its packaging"* is a work order. Same information,
opposite relationship.

### Rule 5 — Privacy as a concrete negative, not a policy
Never "your data is protected" — always the specific thing that does *not* happen, stated
plainly enough to picture. *"I only notice you crossing in and out. I never keep a trail of
where you've been."* A concrete negative is falsifiable and therefore trustworthy; a policy
statement is neither.

### Rule 6 — Warm buttons at warm moments
Buttons are load-bearing tone, not just labels. *"Yes, do that"* and *"It's on"* read as
answers in a conversation. *"Confirm"* and *"Continue"* read as UI chrome. Reserve the
warmest buttons for the moments the user is glad to be there — a permission that clearly
helps them, a success screen — and keep buttons on physical/technical steps a notch more
plain, because those need to be found fast under pressure, not savored.

### Rule 7 — Observation, then offer, then ask — in that order
Never ask for something before demonstrating you understand why it's needed. On Home, this
shows up as *"It's 168 out there. I've already started."* — the observation and the action,
before anything is asked of the user at all. The permission screens (location, notifications)
each lead with what the app noticed or can do, and only then ask.

## 4. Who is speaking — the open question

Every "I" in this app is written as if the product itself is speaking. That is a **product
decision wearing a copy decision's clothes**, and it rides on `C-2`, which is still open.

`memory/voice/ai-personas.md` already established this exact register for the ongoing
product — first person, owns the action, never a bare status — but under a name that was
never settled (`Ding` / `Noise AI Agent` / `Sanctuary Assistant` / an unnamed first person all
appear in the source material). This document runs the same voice everywhere in the app, on
the assumption that the thing greeting you at the door and the thing telling you the filter's
dying are the same speaker.

**If they are not** — if the product is NOMA and the agent is a separately named character
that lives inside it — every "I" in this flow needs re-attribution before it ships. That is
not a global find-and-replace: it changes whether the door, the setup wizard, and the agent's
Day-2 proposals are one relationship or three introductions.

**Resolve `C-2` before any string in this document becomes an i18n key.** Until then, treat
every example here as the register, not the final line.

## 5. Grammar and mechanics

Rules a writer or a reviewer can apply mechanically, independent of judgment calls about warmth:

- **Contractions, always.** "I'll", "it's", "you're" — never "I will", "it is", "you are".
  A voice that doesn't contract reads as formal no matter what it's saying.
- **First person for the app, second person for the user.** "I'll need Bluetooth", "your
  purifier". Never third person for either ("the app requires", "the user's device").
- **Present tense for state, past tense for action taken.** "It's on Sharma_Home" (state);
  "I've already started" (action). Don't blur the two — a user needs to know which one
  they're reading.
- **No exclamation marks.** Calm is the register; enthusiasm punctuation undercuts it. Warmth
  comes from word choice, not punctuation.
- **Sentence-case headlines, never Title Case.** "Which one did you bring home?" not "Which
  One Did You Bring Home?" Title Case reads as a form label; sentence case reads as speech.
- **Numerals, not spelled-out numbers**, except where spelling one out reads more like speech
  than a spec sheet ("about twenty minutes" beats "about 20 minutes" when it's a felt duration
  rather than a measurement; a displayed AQI or a countdown stays numeral).
- **Em dashes for the aside, not the semicolon.** "It's the only way to reach a purifier that
  isn't on Wi-Fi yet — I'll let it go the moment we're done." Conversational rhythm uses
  dashes; semicolons read as written, not said.
- **One idea per sentence.** If a sentence needs a comma to hold two instructions, it's two
  sentences. Read every line out loud — if you'd need to breathe mid-sentence, split it.

## 6. Vocabulary — words in, words out

This table is the canonical source for `memory/voice/glossary.md`'s banned/approved list.

| Banned (wizard voice) | Use instead | Why |
|---|---|---|
| "Please enter your…" | "What's your…" / a direct question | "Please enter" is a form filling itself out at you |
| "Invalid [X]" | Name what's actually wrong, plainly — "That doesn't look like a phone number or an email address to me" | "Invalid" blames the input, not the mismatch |
| "Error" / "Failed" | Say what happened and what still works — "I can't see it yet" | Both words are a verdict with no next step |
| "Please wait…" | Name the wait and its length — "Fifteen seconds or so" | An un-named wait reads as a stall |
| "Continue" (bare, on a plain step) | Fine as-is for physical/technical steps (Rule 6) — reserve warmer verbs for warm moments | Plain is correct for plain steps; the mistake is warming up the wrong buttons, not using "Continue" |
| "Kindly" / "Please note that" | Cut it — say the thing | Both are throat-clearing with no content |
| "In order to" | "To" | Three words doing one word's job |
| "Utilize" | "Use" | — |
| "We are unable to" | "I can't" | First person, direct, no corporate distance |
| "The user" / "the device" (referring to *this* user or device) | "You" / "it" (named, if there's ambiguity) | Third person here is the product talking about the person in front of it as if they'd left the room |
| "Successfully completed" | Say what's true now — "That's the hard part done" | "Successfully completed" is a system log line, not something a person says |

**Two words we lean on, worth naming because they carry real weight:** *"Let's"* (Rule 4) and
*"I'll"* (Rule 1). If a screen has neither a "let's" moment nor an "I'll" statement, check
whether it actually needed a person speaking at all, or whether it's a step that should stay
plain (§8).

## 7. Tone by moment

Not every screen wants the same amount of warmth. This is the register per moment, each with
a real line already in the prototype.

| Moment | Emotional target | Do | Don't |
|---|---|---|---|
| **Arrival** (node 1) | Anticipation, not friction | Speak as the house — *"Let's make your home breathe easier"* | Brand slogan detached from the moment |
| **Asking for something** (phone, email, permissions) | Low-stakes, reason up front | Question + reason in one breath — *"Want the air sorted before you get home?"* | A form label with a tooltip |
| **Waiting** (spinners, progress) | Named, bounded, released | *"Fifteen seconds or so"*, *"I'll notice, and carry on from here"* | A bare spinner, or "Please wait" |
| **Something went wrong** | The device is the subject, never the user; offer the next move | *"I can't see it yet. Usually it just needs a small nudge."* | "Invalid", "Error", or blaming the user's setup |
| **Success** | Warm, specific, closes the loop | *"That's the hard part done"* | "Setup complete." with nothing else |
| **The agent narrating itself** (tour, Home) | First person, evidence over claims | *"It's 168 out there. I've already started."* | Marketing copy about the product in third person |
| **System dialogs** (OS permission sheets) | Not ours to write | Leave Apple's/Google's register alone | A chatty system dialog, which reads as a fake one |

## 8. What stays literal, on purpose

Two categories are deliberately **not** warmed up, and this is a judgment call worth
defending rather than an oversight:

**The instruction inside an instruction screen.** The frame around a physical step can be
warm; the step itself has to stay literal, because getting it slightly wrong costs the user
real time with a purifier in pieces on the floor. *"Let's get the filter out of its bag"* is
warm framing; *"It ships sealed in plastic. Until that comes off it will hum away happily and
clean nothing at all"* is still, underneath the voice, a precise statement of a failure mode.
Unwrapping the filter is the single most common invisible setup failure in the whole flow —
charm is not worth the ambiguity there.

**System dialogs.** iOS and Android own that register. A permission sheet written in NOMA's
voice reads as a spoofed system dialog, which is worse than a cold one — it looks like the app
is trying to sound official rather than being official.

## 9. Errors, specifically

Errors are the hardest case: the app has to stay warm *and* stay unambiguous, and those two
goals fight each other more here than anywhere else in the flow. Four rules, non-negotiable:

1. **The device is the subject, never the user.** *"I can't see it yet"*, not "you didn't hold
   your phone close enough." The user did not cause the failure; do not imply they did.
2. **Every error offers the next move, not just a verdict.** *"Worth another look?"* — never a
   bare restatement of what failed.
3. **Never apologize on behalf of hardware.** "Sorry, something went wrong" is empty. State
   what happened and what still works instead.
4. **The fix stays literal even when the frame is warm.** "That password didn't work. Worth
   another go?" is warm framing around a precise, unambiguous fact.

## 10. Before / after — the actual rewrite

Ten screens from the shipped prototype, shown as they were and as they are now. This is the
concrete evidence the rules above describe.

| Screen | Before | After |
|---|---|---|
| Get started | "Quiet, clean air. One app." / [Get started] | "Let's make your home breathe easier." / slide to enter |
| Phone number | "What's your number?" | "First — how do I reach you?" |
| Profile | "Who are we setting this up for?" | "And who am I looking after?" |
| Email verify | "Check your email" | "Have a look in your inbox" |
| Choose purifier | "Which one is it?" | "Which one did you bring home?" |
| Plug in | "Plug it in and switch it on" | "Now find it a socket" |
| Bluetooth | "Switch on Bluetooth" | "I'll need Bluetooth for a minute" |
| Connected | "Your purifier is set up" | "That's the hard part done" |
| Which room | "Which room is it in?" | "Where does it live?" |
| Not found | "We couldn't find your purifier" | "I can't see it yet" |

## 11. Localization

This voice raises the translation bar. Idiomatic phrases — *"a spare key"*, *"hum away
happily"*, *"already spoken for"* — carry meaning through cultural reference, not through
their literal words. A machine or literal translation of any of them into Hindi will read as
broken, not warm.

**This needs transcreation, not translation.** Budget a native-voice pass that re-derives the
*feeling* of each line in Hindi, rather than translating the English sentence. The seven rules
in §3 should hold in Hindi even where the specific idioms don't survive.

`hi` is required for this flow, not deferred — `memory/voice/ai-personas.md` already flags
that a resident persona with low app fluency is exactly the case an English-only setup fails.
This voice makes that requirement more expensive, not less necessary.

## 12. The checklist

Before a new string ships, run it against these eight questions:

1. Would a person actually say this out loud to someone in their home?
2. Is the reason for the ask in the same sentence or the very next one?
3. If this is an error, is the device the subject — not the user?
4. Does every error offer a next move, not just a verdict?
5. Is there a wait here that isn't named and bounded?
6. Did this sentence need a comma to hold two instructions? If so, split it.
7. Is this a physical/technical instruction dressed in so much warmth that it's gotten
   ambiguous? (§8 — the frame can be warm; the instruction can't blur.)
8. Is this a system dialog? If yes, leave it in the OS's own voice.

A string that fails any of these isn't necessarily wrong, but it needs a reason to survive
the exception, and that reason should be written down next to it — as every deliberate
exception in §8 is here.

## 13. Where this applies beyond onboarding

This document generalized from an onboarding-only PRD to an app-wide one on 2026-08-07,
because the register it describes was never actually specific to setup — a wizard-vs-
conversation problem shows up anywhere the app has to ask something, wait for something, or
report back. The seven rules, the grammar in §5, and the banned words in §6 apply without
modification to every surface below. What changes by surface is *how much warmth a moment can
carry* (§7 already covers this axis) — not the rules themselves.

**Reconciling with `ai-personas.md`.** That document already specified the ongoing-product
voice — first person, owns the action, pairs a number with a consequence, anchors units to
something human, never volunteers alarm — derived independently from PM prototype material
for notifications and Home. It does not conflict with anything here; it's a *superset* for
those two surfaces, with rules specific to what an ambient, always-on voice needs that a
one-time setup flow doesn't (the night-hook/morning-proof pairing, the share-caption
exception where brand voice must disappear entirely). Read both for Home and notifications;
this document alone is sufficient everywhere else.

**Surface by surface — what's rewritten, and what's still owed:**

| Surface | Status | Notes |
|---|---|---|
| Onboarding & device setup | **Rewritten and shipped.** | The worked evidence throughout this document. `docs/features/first-run/prd.md` §8. |
| Home & notifications | **Already this register**, via `ai-personas.md`, written independently but consistent with the rules here. | Extend, don't duplicate — see above. |
| **My Home** (the six-state dashboard prototype) | **Not yet rewritten.** | `docs/features/my-home/build-home.py` has its own copy, written before this voice existed. Next concrete pass. |
| Sharing / People, Automations, Shop, Settings | **No prototype exists yet to rewrite.** | Apply the checklist (§12) at first-draft time rather than retrofitting later — cheaper than a second pass. |
| Errors app-wide | **§9's four rules apply everywhere**, not just onboarding's error states. | The device (or the automation, or the routine) stays the subject; every error still offers a next move. |

⚠ **Do not treat "rewritten elsewhere" as done until it's checked against real strings**, the
same way §10's before/after table checks onboarding. A surface isn't in this voice because
someone believes it is; it's in this voice because a specific line can be pointed at.

## 14. Cross-references

- `memory/voice/ai-personas.md` — the ongoing-product voice for Home and notifications,
  reconciled with this document in §13. Read it first if `C-2` closes and every "I" needs
  re-attribution.
- `memory/voice/tone-matrix.md` — **this document is canonical for all its rows**, not just
  onboarding. The stub should point here rather than duplicate this content.
- `memory/voice/glossary.md` — **this document is canonical for §6's banned/approved words.**
- `docs/features/first-run/prd.md` §8 — the onboarding copy this document explains, screen by
  screen, and the only surface fully checked against §10's before/after standard so far.
- `memory/decisions.md` §C-2 — the open blocker on who "I" is.

---

*Compiled 2026-08-07 from the first-run prototype's shipped copy, then generalized the same
day into the app-wide standard. Every rule here is checked against a real, already-written
line — nothing in this document is aspirational, and §13 tracks exactly how far the rewrite
has actually reached.*
