# Changelog

> What changed, when, why, and what was verified. Newest entries on top.

---

## 2026-09-10 — `.claude/launch.json` is no longer tracked, in either repo

**A file the tooling rewrites every session was under version control.** It is the
preview-server registry, and every session that starts a preview writes an entry into it
carrying an absolute, session-scoped `/private/tmp` path. Two real examples found on the same
day: this repo pointing at its own session scratchpad, and noiseFit pointing at a scratch
workspace from a *different* session on 8 Sep. So its content is guaranteed to differ between
any two checkouts — the definition of a file that must not be tracked.

Three symptoms, one cause: `git status` was permanently dirty, pushes and pulls conflicted on
it, and it kept riding into unrelated commits. It had to be pulled back out of **three**
commits during the first-run work and had still been committed four times here with different
contents. The tell was frequency — the fourth time is not an accident, it is a file in the
wrong category.

Untracked and gitignored in both repos. The shared baseline moved to a per-project template
(`.claude/launch.Noma.json`, `.claude/launch.Noisefit.json`) so a fresh clone still gets the
known servers.

⚠ **The live filename cannot change.** `.claude/launch.json` is the exact path the preview
tooling reads; renaming it stops previews resolving. Only the template is named per project —
which is the point, since both repos previously had a file called `launch.example.json`,
indistinguishable side by side. Verified by starting a registered server after the rename.

⚠ **Only `launch.json` was untracked.** Everything else under `.claude/` is real shared
content and stays in git — the rules files here, the `animate-text` skill in noiseFit. A
`git rm -r --cached .claude` would have thrown those away.

⚠ **Nothing local was discarded.** noiseFit's shared `noisefit-dashboard` entry had already
been clobbered by that 8 Sep session; the fix put it back *alongside* the newer entry rather
than choosing between them.

**Written up for the org** as `docs/engineering/claude-launch-json-conflicts.md` — the
symptom, the cause, a copy-paste procedure for any repo, the four verification checks, and the
traps (`git rm --cached` not `git rm`; do not untrack the whole `.claude` directory; a
`/private/tmp` path existing today proves nothing).

The procedure was **tested rather than just written**: run end to end in a throwaway repo
(clean status, only the template tracked, live file ignored but present, shared rules
untouched, scratch entry stripped while the team entry survived), and the conflict itself
reproduced and confirmed gone — two clones of a bare repo, each with its own `launch.json` and
its own `/private/tmp` path, both `pull --rebase` and `push` succeeding with no conflict and
each keeping its own config.

---

## 2026-09-09 — Engraved glyphs out, avatar out, a real phone, and the room stage finished

Six owner changes, and three of them turned up bugs that were not what was reported.

**The engraved glyph leaves the Bluetooth and Wi-Fi pages** — five screens (the BT scan and
the four Wi-Fi ones). `glyph()` and the engraved register stay; node 16's check mark is
untouched.

**The avatar and its edit glyph leave the key card.** The name and mobile now sit where the
avatar was, which is what the owner asked for and needed no repositioning — `.kcard__id`'s
left inset was already the avatar's, so removing the avatar and its `margin-left` was enough.
This closes a question that had been flagged since 2026-08-20: node 4 had no avatar field, so
the card was the only place a picture could be set, and the pencil was the last thing
pretending that worked. First run now collects no picture at all. Also removed: the
FileReader picker, the initials setter, and a comment that still claimed the avatar "still
works if you click it".

**Node 11's phone is a real phone.** A titanium-rail iPhone, front on, black screen, island,
four side buttons, and a single diagonal sheen as the only thing on the glass — owner: "keep
the screen off. don't show anything inside the screen."

⚠ **The reported "phone is shifted to the right" was two separate bugs, neither of them the
phone.**
- The tick sat **15px left of the dots** it replaces. It was absolutely positioned against
  `.pair__row`, and since the purifier (94px) and the phone (65px) are different widths, the
  row's centre is not the connection's centre. The row is a 3-column grid now with equal
  `1fr` sides, and the tick lives INSIDE the middle column with the dots, so they cannot
  disagree again. Measured after: connection 0.0px off the screen centre, tick 0.0px off the
  dots.
- The purifier **render was 14px right of its own slot**. `.scr.in .pgt>*` excluded a
  `.pslot` from the entrance animation, but only as a DIRECT child — node 11's slot is nested
  inside `.pair`, so `.pair` took the animation and `placeHero()` read the slot's rect
  through `pgin`'s `translateX(14px)`. That is the exact failure `carryClass()`'s note warns
  about, and its guard only fires when the purifier is already live, which it is not on the
  way in. Fixed with `:not(:has(.pslot))`, which generalises to any future wrapper holding a
  hero slot. Measured after: render offset 0.0px.

⚠ Worth recording separately: my first measurement of this screen was taken headlessly and
reported the whole row 14px off-centre. That number was the same `pgin` transform, frozen
because **headless Chrome does not tick animations** — the row is and was centred. The real
bugs only showed up when measured in a live browser. Third time this trap has cost time.

**Node 17's room stage is finished rather than wireframed**, and the "wireframey" look had a
concrete cause: **the faces were `rgba(11,11,11,a)`**, so nothing occluded anything — you
could see the back wall and the lamp straight through the bed, and every overlap darkened
where two translucent shapes crossed. No amount of gradient fixes that, because the problem
is that the solid is not solid. Faces are composited against the stage's own ground once and
drawn **opaque** now, so the painter's-algorithm sort actually hides what is behind. On top of
that: a shared gradient per face type, a contact-shadow ellipse under anything over 7px tall,
a lit lip along each top face (the same idea as the large-surface recipe's inside stroke), and
gradient walls plus a hairline seam where they meet.

**The stage grew from 168px to 320px** and the dead space below it fell from **191px to 37px**
(owner: "there's a ton of empty space... the illustration part can be longer"). It flexes now
rather than carrying a fixed height, and `xMidYMax` bottom-anchors the drawing so the floor
stays put as the stage resizes.

⚠ **The viewBox is DERIVED from the furniture now, not hardcoded.** It was `9 -25 302 180`
while the content reaches y=-30.5 — the kitchen hood and fridge, the pooja bell stand, the
bedroom lamp — so the top 5.5px of the tallest objects was cut off, which is exactly the "being
cut on top" the owner reported. `_rs_viewbox()` computes the tightest box over the shell and
every room at build time, so a new room with a taller object cannot reintroduce it. Verified
per room in a live browser: all four clearances positive on the kitchen, the worst case.

**A custom room can be named** — a dashed "Add a room" tab opens an inline field, and the
typed name becomes a selected tab with the add button staying last.

⚠ Two judgement calls inside that. First, **the tab row now wraps instead of scrolling**: the
add tab lands last, and behind six rooms it sat off the right edge of a horizontally scrolling
rail — an option you cannot see is not an option. Wrapping costs one row of height, which the
taller stage can afford. Second, **what the drawing shows for a custom room**. An empty room
(all four slots sunk into the floor) is the most honest picture and animates beautifully, but
at this stage size it just reads as a large pale box — the exact unfinished look this pass
existed to remove. So it gets a deliberately generic arrangement instead: a seat, a back, a
side table, something tall, matching none of the six. Inheriting whichever room was selected
before would have actively asserted a wrong answer.

Verified: all six renderings build, voice gate clean, no unresolved link targets across 41
screens, no `icon()` above the 24px ceiling, the room morph still short-circuits under reduced
motion, and the full 24-screen path walks end to end in a live browser.

---

## 2026-08-20 (15) — Centred sheet titles, device renders in the scan

**Centring the sheet titles was fixing my own regression, not adding a feature.** `.grad`
gives a heading `width:fit-content` so the gradient's ends land on the first and last letter
— necessary — and a fit-content BLOCK ignores its parent's `text-align`. So the moment the
gradient went flow-wide, every sheet heading silently went left, including the ones whose
sheet already declared `data-align="center"`: `text-align` was still doing its job, centring
the text inside a box that now hugged it. Auto margins are what centre a shrunk block.

⚠ **It took two placements and two specificities to actually land, and both failures were
cascade, not layout.** Proven up front by setting the margin inline, which centred it
immediately — a layout that works inline and not from a rule is never a geometry problem.

- First attempt sat ~40 lines too early in the file and lost to build-auth's
  `.sheet__c p,.sheet__c h1{margin:0}`. Not on specificity — `.sheet .h1` is (0,2,0) and
  beats (0,1,1) — but because `AUTH.CSS_SHEET` is injected AFTER that region, so a shorthand
  reset a longhand set by an earlier, more specific rule. Moved below the injection.
- That fixed the auth sheets (nodes 1-3) and not the overlay ones (4, 5), because
  `.ovl .sheet .h1` already set `margin:0 0 8px` at (0,3,0). Matched with
  `.ovl .sheet .h1{margin:0 auto 8px}`. The two rules are a pair; the second is not redundant.

Measured after: all seven sheet screens centred to under 2px, and "Edit number" centred too
(it was `align-self:flex-start`, inherited from the auth sheet).

**The scan rows carry device renders now.** Owner: "we need the render images in the container
to show which devices are available." A Bluetooth mark on every row only said "this arrived
over Bluetooth", which the screen's title already says. The render is what tells two rows
apart at a glance — and since node 6 was deleted, this list is where the model is chosen, so
it has to look like a choice between products. Reuses `.rnd--{sku}`, the same real renders the
deleted picker used. Falls back to the Bluetooth mark for a row with no SKU (a Wi-Fi list, or
a device whose model the scan could not resolve).

⚠ `purcard()` is now dead code — one definition, no callers, since node 6 went. Left in place
deliberately: it is the shape to come back to if the picker is ever restored, and its
docstring carries why the renders replaced the hue tints. Grep before assuming it is live.

---

## 2026-08-20 (14) — Bluetooth moves before the unboxing; four pages leave the path

The biggest structural change since 2026-08-06. Owner: "after the key card is created, we'll
turn on the Bluetooth, and we'll start looking for devices that are available... then it will
go to the number seven, unwrap your filter page." The story is now: you are given a key, the
phone finds the device, they pair, and only then do you open anything.

**Happy path 30 → 24 screens, 25 → 21 nodes.** New order:

    1  S0 A1     splash, login          5c A8    key card created
    2  A2        email                  10 P4    switch on Bluetooth
    3  A3        email OTP              10 P4D   Bluetooth prompt
    4  A4        a bit about you        11 P5    the scan  ← device chosen here
    5  A5        mobile OTP             11 P6B   pairing
    5a A6        the wallet             7  P2    unwrap the filter
    5b A7        key created            8  P2B   find it a socket
                                        9  P3    light blinking
    13 W1  which network                17 R1    which room
    12 P7B confirm Wi-Fi                18 R2    name it  (+ optional key share)
    15 W3  setting up                   23 D1    tap the key
    16 W4  that's the hard part done     26 HOME

⚠ **NODE NUMBERS DELIBERATELY DO NOT RENUMBER.** The owner still refers to "number seven
unwrap your filter" and "number thirteen", so the boxes keep their ids and only their order
changes. The nodes therefore run 10, 11, 7, 8, 9, 13, 12 — and there is now an assertion that
this list is NOT sorted, because the day it comes out ascending, this resequence has been
silently undone.

**Node 6 (choose your purifier) is DELETED,** not demoted: the scan answers the same question
from what it can actually see, so asking first asked twice. What went with it, and where each
piece landed, is recorded in the source where the screen used to be:

- `wirePick()` survives and is now wired to the scan's rows. `slist()` rows take a third
  tuple field, the SKU, and emit the same `data-sku` the deleted cards used — so everything
  downstream of the choice is untouched. The scan lists **Air Pro 200 and Air Pro 500** now,
  where it used to list two identical 200s; it has to offer a model choice because it is the
  only place one is made. Verified: picking the 500 row sets `sku-500` on `.phone`.
- ⚠ That change costs something the old note guarded. Two identical SKUs were deliberate —
  a household that bought a pair really does see two, and the signal line was the only thing
  telling them apart. That case is now unrepresented, and "Identify" (blink the light on one),
  already flagged as owed before build, is the thing that would answer it.
- `CARRY.pur` had nothing left to fly from, so the purifier's first appearance is node 7's
  unwrap illustration.
- The hue-coded SKU thumbnails went too, and with them the open conflict they carried against
  the two-green rule. That conflict is closed **by deletion rather than by decision** — worth
  knowing if the picker ever returns.

**Nodes 24 (location/geofencing), 25 (notifications) and branch 18a (send a key) left the
path.** ⚠ I demoted all five screens to edge states rather than deleting them. For 18a that is
exactly what was asked ("keep that as a edge state below"). For 24 and 25 the instruction was
"remove", and demoting is my reading of the least destructive way to do it: they are reachable,
off the happy path, and recoverable, and geofencing has a whole owner-supplied illustration
behind it. **Say the word and I will delete them properly.**

Node 18 gained a **secondary CTA** ("Send a key" → node 18a) so the share is optional, per
"sending a key is a optional flow. We don't want it to be a separate page."

**The scan gained the way out of a failed scan**, under the results where someone who cannot
see their purifier is actually looking. ⚠ The reference reads "Click here to troubleshoot";
the link says **"Troubleshoot"** instead, because W-14 requires a label to name its
destination and "click here" names nothing (and a screen reader announces a page of them as
identical). `infoln()` takes an optional link now; its docstring pointed at node 6, which no
longer exists.

Rewired and checked: A8 → P4, pairing → P2, blinking light → W1, connected → R1, node 18 →
D1. Two edge states pointed at the deleted picker ("Cancel" on *Already spoken for* now
returns to the scan; "Not now" on a hard Bluetooth refusal returns to the key card, since
without Bluetooth the scan is unreachable). **Zero unresolved link targets across 41 screens,
and zero remaining references to P1.** Walked all 24 screens forward in a real browser and
recorded the header on each — the order matches the brief exactly.

---

## 2026-08-20 (13) — New sleeve artwork; every header shortened and gradient-painted

**The front sleeve is narrower than the back now, and it never was before.** Owner: "the front
sleeve is slightly smaller." It was sharing `left:0;right:0` with the back, which stretched
its 1227-wide frame across the back's 1298 — and because the two PNGs carry almost the same
proportion of transparent padding (83.78% vs 83.67% opaque), that made the two leather panels
come out the SAME width. A pocket the size of its sleeve reads as one flat shape, which is why
the layering never showed. Every number is now measured off the files:

    frames   back 1298x1721   front 1227x1407
    opaque   back (106,62)-(1192,1571)   front (99,60)-(1127,1267)
    width    1227/1298 = 94.53%, so 2.735% a side, centred
    bottom   0.59% — what lifts the front's leather flush with the back's

⚠ New artwork, IDENTICAL geometry. The replacement PNGs measure the same frames and the same
opaque boxes as the old ones (mean per-channel difference ~9, a texture and tone change). So
the visible fix was entirely in the CSS, not the assets — worth knowing before hunting for it
in the files. `sleeve-reference.png` is vendored alongside them as the compositing reference.
`.wal`'s aspect also moved from the rounded 600/796 to the frame's own 1298/1721.

**Every header is shorter, and every header now carries the gradient.**

⚠ **SIX HEADERS WERE LEFT ALONE ON PURPOSE.** The voice guide's corrections bank (§10.1) and
its rules quote these as the APPROVED fix for an earlier failure, so shortening them would
have regressed a documented decision: "Now find it a socket" (the fix for "Plug it in and
switch it on"), "I'll need Bluetooth for a minute" (for "Switch on Bluetooth"), "That's the
hard part done", "I can't see it yet" (for "We couldn't find your purifier"), "Where does it
live?" (quoted in R-04), and "Want the air sorted before you get home?" (quoted in W-04).

⚠ **ONE CHANGE IS NOT A SHORTENING AT ALL — the flow was shipping copy the guide already
marks as broken.** §10.2 lists "Shall I tell you when something changes?" as a FAILURE under
M-04 · M-09 and prescribes "Shall I tell you when the air turns?". Both permission screens
carried the "before" column. Fixed to the prescribed version.

Two more were voice fixes as much as length ones: "Tell us about yourself" → **"A bit about
you"** (that "us" is the corporate we §5.2 bans) and "No light on the device?" → **"No light
at all?"** (§5.2 bans "the device" once a thing has a name). Also `Connect wifi` →
**`Connect Wi-Fi`**, the spelling the rest of the flow already uses.

The rest: "Which one did you bring home?" → "Which one's yours?", "Let's get the filter out of
its bag" → "Let's unwrap the filter", "Is the little light blinking?" → "Is the light
blinking?", "This one's already spoken for" → "Already spoken for", "I can't reach it without
Bluetooth" → "Bluetooth is still off", "Which network should it join?" → "Which network?", "I
can only see 5 GHz networks" → "Only 5 GHz here", "It's on Wi-Fi, but it can't reach me" → "It
can't reach me", "Enter the OTP sent to your email" → "Enter the OTP", "Enter OTP to verify
your mobile number" → "Enter OTP", "What's your email address?" → "What's your email?". Screen
titles were aligned with their headers so the flow doc and the product agree.

⚠ **The gradient class had to be SPLIT before it could be reused.** `.t1--grad` was written for
the three key-card screens and carried their 24px and their centring along with the paint.
Applying it to every header would have resized and centred the whole flow. `.grad` is the paint
alone now; the key-card screens keep their size in `.ccol .t1`. Applied on the `t1()` helper
rather than at 30 call sites.

**All-caps audit (§5.4, W-14).** One real failure: `field(label="AND WHAT SHALL I CALL HOME?")`
on node 17 — a question set in 12px letter-spaced caps, so the voice came out shouted, and a
SECOND ask on a screen whose ask is "Where does it live?" (R-09). Now "HOME NAME"; the
placeholder already shows the shape of the answer (W-11) and the foot takes the stakes out
(R-05). Everything else checked clean as signposts: "GETTING STARTED", "CONNECT BLUETOOTH",
"WHERE IT LIVES", "YOUR HOUSEHOLD", "BEFORE WE FINISH", "PICK YOUR DEVICE", "CREATE PROFILE",
"NAME", "MOBILE NUMBER", "SEND A KEY TO", "CUSTOMIZE", "DONE TODAY", "BEDROOM, RIGHT NOW", and
"PASSWORD · FROM THIS PHONE" (provenance stated plainly, §5.1).

⚠ Still unresolved and now more visible with shorter copy: nodes 5b and 5c read "Key created"
then "Key card created" back to back. Flagged four times; it needs an owner call, not another
guess.

---

## 2026-08-20 (12) — A mobile rendering, so the gyro can actually be judged

Owner: "give a running mobile view html to check gyro and actual app flow... remove the
controller for the app html for mobile version just keep the full screen experience."

`build-mobile.py` — the FIFTH rendering of the one screen set (harness, flat board, export,
wireframes, this). Defines no screens of its own; a flow change is still made once, in
build-prototype.py.

**Why not just use the export.** `first-run-export.html` already has no controller, but it
still draws a 390x844 handset with a bezel and scales it to fit the window. On a phone that
gives you a small picture of a phone inside a phone — and the gyro shimmer, the one thing
that cannot be judged on a laptop, renders at half size behind a fake bezel. So this build
keeps every screen byte-identical and changes only the shell: `.phone` becomes the viewport,
the drawn island and home bar go (the real device has its own), and `fit` is a no-op so
nothing is transformed.

⚠ **That no-op matters beyond layout.** `placeKey()`/`placeHero()` divide by the phone's own
scale (`pr.width / phone.offsetWidth`) to convert screen space into phone space. With no
transform that ratio is exactly 1, so the travelling key card lands correctly with no
special-casing — verified, the card measures its full 264px here.

⚠ **The status bar keeps its 56px and loses only its contents.** Every screen's top spacing
is measured against that band; removing the bar would pull the whole flow up under the real
clock. `max(56px, env(safe-area-inset-top))` gives taller notches their room while keeping
the number the layout was designed on.

⚠ **The gyro needs an explicit gate, and that is an iOS rule rather than a choice.** iOS 13+
refuses `DeviceOrientationEvent` unless `requestPermission()` is called inside a real user
gesture. The harness asks on the first tap on the phone — but that binding is only attached
once a tilt card exists (`wireCardTilt`), which first happens on node 5b, several taps in. On
a handset that reads as "the shimmer is broken". So this build opens on a tap gate whose only
job is to be a genuine gesture, calls the harness's own `askGyro()` from it, and only then
starts the flow. It also HOLDS the flow deliberately: node 1 auto-advances after 1s, so a
gate that merely overlaid a running flow would have the splash gone before it cleared.

Verified at a 375x812 viewport: `.phone` measures exactly 375x812 at the origin with no
transform and no radius, the gate covers to both edges and hands over, the splash
auto-advances to the login sheet, island/home-bar compute to `display:none`, the status bar
is 56px and `visibility:hidden`. **The gyro was proven end to end** by driving `onOrient()`
with a real orientation delta rather than trusting the binding: a 16-degree gamma change
resolves to `--gx: 0.727` / `--gi: 0.727` on the card, and the shimmer is visible in the
capture.

⚠ Also fixed while writing it: the gate's mark was written as `var(--wordmark)`, which does
not exist — the wordmark is an inline `<img>`, not a custom property. Caught by grepping the
built output for the variable rather than by looking at the render, where a missing
background is easy to read as intentional whitespace.

---

## 2026-08-20 (11) — A ghost back button on nodes 2-5, caught on the live Vercel deploy

Owner spotted a plain white circle sitting in the nav's right slot on the deployed site —
not something either of us had looked for, because it renders far enough from the real back
button that it reads as a second, purposeless control.

**Cause:** `nav()` always emits BOTH slots. With no `close` handler, the right slot is an
empty `<span class="nb">`, and `.nb`'s own CSS — a white 38px circle, correct for a real
button — cannot tell a placeholder from a control. Something else has to hide the
placeholder, and this codebase already carries that companion rule at its two existing
`nav()` call sites (`.scr:has(.pgb.pgb--top) .nav span.nb` and `.scr:has(.ccol) .nav
span.nb`, both `visibility:hidden`). The `.au`/`.ovl--bare` host added earlier today for the
nodes 2-5 back button was the THIRD site, and it got the positioning rule but not the twin
visibility rule — the one time the pattern was forgotten instead of copied.

Fixed: `.au>.nav span.nb,.ovl--bare>.nav span.nb{visibility:hidden}` alongside the existing
positioning rule. Verified on all four screens: the placeholder measures `visibility:hidden`
at 38px (present in the DOM, invisible) while the real `button.nb` stays. This is a
GREPPABLE pattern now worth naming for the next `nav()` host: a positioning rule with no
adjacent placeholder-hiding rule is the bug.

---

## 2026-08-20 (10) — The splash auto-advances after 1s

Owner: "on page 1 splash screen, after 1 second the bottom sheet pops up automatically."

`au(splash=True)` now emits `data-cmp="splash" data-go="A1" data-ms="1000"` on the splash's
outer `.au`, wired by a new `wireSplash()` — the same data-ms/data-go contract `wireLoad()`
and `wireSuccess()` already use, so the timing lives on the markup rather than a second copy
in the runtime. Scoped to `splash=True` only: `au()` backs eight screens, and the seven login
sheets must not inherit a timer meant for one of them.

⚠ **This only reaches the canonical harness** (`build-prototype.py`, hence
`first-run-flow.html` — the file Vercel serves). `auth-prototype.html` is a separate
standalone tool with its own splash timer (`MO.splashHold`, 2.6s) and was not touched.

The S0 docstring previously claimed the sheet "arrives on its own after a beat, or on a tap"
at a 2.6s hold — neither half of that was ever wired (confirmed: no click handler existed on
`.au`, and no timer at all in this harness). Corrected to describe what is actually built
rather than repeating the old claim at a new number.

Verified in a real browser, frame-sampled rather than spot-checked, after the first attempt's
reading was contaminated by leftover timers from unrelated tests earlier in the same long-lived
tab: still on the splash at 776ms, advanced by 1177ms. Manual navigation away from the splash
during the wait (`clearTimers()`, called by every `render()`) correctly cancels the pending
advance — confirmed by navigating to node 4 mid-wait and finding it still there 2s later.

---

## 2026-08-20 (9) — The dissolve is unconditional; a plain spinner; an exact card handoff

**The sheet effect was missing on nodes 4-5 for a reason worth recording:** their two sheets
are BOTH 359 tall, by coincidence of their content. The old early-return bailed on equal
heights and took the content fade out with it, so those two pages swapped instantly while
every other pair dissolved. Height and content are two separate promises and only one of them
is about the box changing size — the dissolve is unconditional now, the resize is not.
Verified on 4 -> 5: opacity 1 -> 0.45 -> 1 with the height untouched.

**Node 15's loader is a plain circular spinner.** The honest half of the original argument
survives (an indeterminate wait must not be drawn as a progress bar) but the literal
lemniscate is gone — a circle is what every platform already uses for "indeterminate", so it
needs no explaining to the person waiting. The arc is still DERIVED (2*pi*r) rather than
guessed. The dash-travel animation became a rotation, which also drops the `--infL`
arc-length that had to be plumbed through from the generator; `transform-box:fill-box` is what
makes `transform-origin:center` mean the circle's centre rather than the SVG's origin.

**The shrunken-to-large handoff was flickering for TWO reasons, and the owner had already
diagnosed the first.**

- The roll. The traveller flies to the slot's `getBoundingClientRect()`, which is an
  AXIS-ALIGNED box, and a rotated card's AABB is larger than the card — so matching the rect
  meant not matching the card. Moving the roll to an inner wrapper kept the slot square, but
  the traveller still had to carry the angle to look right, and a rotated traveller has the
  same enlarged AABB. Square on both sides is the only version where the two are the same
  shape. Removed, as asked.
- ⚠ `transform-origin`. The parked state sets `50% 0` and the old code removed that class for
  the flight, so the origin changed INSTANTLY while the transform interpolated — the card
  jumped to a new start position on that frame. The class now stays on through the flight and
  `placeKey()` compensates its x arithmetic instead: with origin `50% 0` a scale maps [0,W] to
  [W(1-s)/2, W(1+s)/2], so landing the left edge on the slot needs
  `x = slotLeft - W(1-s)/2`. The y needs no correction because the origin's y is 0.
  Only `--bare` (a pure fade of the card's contents) comes off now.

Measured after: the traveller lands within 0.3-0.8px of the target box on all four edges, and
exactly one card is visible once it settles. Door card also lifted another 24px (bottom -116
-> -92).

---

## 2026-08-20 (8) — The sheet morphs between pages; new background; slimmer gradient

**The bottom sheet resizes instead of snapping.** Owner: "either the bottom sheet enlarges and
shrinks then the content appears rather than size of the bottomsheet suddenly snapping."

⚠ **Done entirely on the ARRIVING screen, and that is forced rather than lazy.** `render()`
removes the outgoing screen in the same frame it appends the new one — deliberately, to kill a
white flash reported on 2026-08-18 — so there is no outgoing sheet left to animate. The
arriving sheet instead opens at the OLD height with its content already hidden, so the frame
you see is the sheet you were just looking at minus its contents; it resizes; then the new
content dissolves in. Two sheets that look identical make the substitution invisible.
`offsetHeight`, not `getBoundingClientRect()`, because the harness scales the whole phone and
the value is written back as CSS px. A screen with no sheet clears the chain.

Verified frame by frame: node 1 -> 2 runs 379, 377, 371, 357, 338, 323, 313, 307 -> 298 with
content at 0 throughout, then fades in; node 2 -> 4 GROWS 298 -> 346 -> 359; node 4 -> 5 has
identical heights and correctly plays nothing.

⚠ **I spent several probes debugging a stale page.** `wireSheet` was reported undefined and
the height never animated — because the tab was still running the document from before the
build. The copy-to-preview step is not a reload. Check `typeof <newFunction>` first when a new
function appears to do nothing.

**New background** (nodes 1-5): the owner's arch-and-stairs interior, 0 alpha noise, 850px
wide progressive JPEG q82 — 26 KB, down from 73. Same drop-in path, no code change.

**Gradient retuned** to the owner's second redline: stops pulled in to 24/50/74 and the green
darkened to `#8EAE7D`. The point is the ramp length — ink now holds the first and last quarter
flat, so the green reads as a slim streak through the middle of the word rather than as the
word's colour. ⚠ The second redline moved the green FURTHER from `green.neon` (#AEC799), not
closer, so it is a deliberate darker green rather than eyedropper drift. Still flagged: three
greens in the product unless the owner snaps it.

---

## 2026-08-20 (7) — The parked card lands on the back button's line, and 5b takes it back

**Parked card centred on the back button.** `KPARK.top` 34 -> 64: that button's centre is 80
on every screen that has one (`.sbar` 56 + 4 padding + half of 40) and the folded card
measures 31.9 tall. Measured rather than derived — the rendered height of a
perspective-folded card is not a number worth computing by hand. Verified: hero centre 80,
back-button centre 80.

**Stepping back from node 6 now lands on 5b and the card expands into it.** Owner: "when the
user goes back from anywhere before page 6, user will be taken to page 5b and the card will
expand again to the center... only one card is visible at a time because it is just a shrunken
instance of the card not any new object."

The mechanism already existed for the door, so 5b's card just declares `[data-kslot]` and
`placeKey()` was reordered: **a slot now wins over the "before the key existed" retire
branch**, which would otherwise have blinked the card away on arrival since 5b sits before the
screen that created the key. The handoff class moved off `.dk` onto the slot itself, so it is
generic and covers both shapes — the slot may BE the card (5b) or contain it (the door).
Verified across the transition: parked at 80, mid-flight expanding with 5b's own card hidden
(0 visible), landed with the hero spent and exactly 1 card visible. Node 6's back also
retargeted A5 -> A7, which is what makes the step land on 5b at all.

**Node 23's card sits 74px higher and rolls -4 degrees.** ⚠ The roll is on an INNER wrapper,
not on `[data-kslot]`. A rotated element reports an enlarged axis-aligned bounding box, and
the traveller flies to that rect — rotating the slot itself would have landed it at the wrong
scale. The slot stays square, the rotation lives inside it, and `data-kroll` tells the
traveller to match the angle so the handoff is invisible.

**A stylized gradient title** on the three key-creation headings: Google Sans Flex Bold 24,
letter-spacing 0, three stops at 0/51/100 run at 100deg. Canonical in
`src/tokens/design.tokens.js` as `titleGradient`, read at build time through a new generic
`_tok()` (grown out of `_ways()` — a second canonical fact meant the subprocess boilerplate
wanted one home).

⚠ **`width:fit-content` is the whole effect.** A block `h1` is full-width, so the gradient
spanned the box while the text sat in the middle third of it — sampling only the green
midpoint and rendering uniformly green, with both ink ends off past the edges of the words.
Shrinking the box to the text is what puts 0% and 100% on the first and last letter.

⚠ **THE MID STOP IS NOT ONE OF THE TWO GREENS.** The owner picked `#AECF9B`; `green.neon` is
`#AEC799` — two hex digits apart, which reads as an eyedropper of it rather than a new
decision. Recorded as given and flagged in the token, because inventing agreement between a
redline and a token is worse than naming the gap. Owner call: snap it and LAW 6 holds with no
visible change, or keep it and the product has three greens.

⚠ Process note: several readings this session were corrupted by stray timers firing between
separate tool calls while the page kept living. Wrapping `go()` to log its callers proved only
ONE navigation was happening. Multi-step behavioural checks in this harness have to run inside
a SINGLE evaluation.

---

## 2026-08-20 (6) — The card parks in perspective; the back button leaves the sheet

**The corner park is gone; the card now folds away at the top centre.** Owner: "rather than
the card shrinking to the right, the contents disappear and the card turn in perspective...
it will shrink to the top center in a perspective view. No text will be on it just the card
bg colors." So `.khero--parked` strips the identity block and the edit icon (opacity, not
`display`, because it flies and fades at once and the door has to put them back), moves the
transform origin to top centre so the fold is symmetric, and lays the card back 75 degrees.

⚠ **Two transform-order bugs, both found by measuring the rendered box against the phone.**
CSS transform lists apply right-to-left, and both mistakes came from reading them left-to-right:

- `perspective() translate() scale() rotateX()` put the perspective LEFTMOST, so it projected
  the *translated* geometry — a point 150px from the perspective origin is magnified by its
  distance, and the card rendered **608px wide inside a 390px phone**. The translate has to
  sit outside the perspective.
- Then `scale() rotateX()` rotated the card at FULL size, swinging its bottom edge
  350*sin(64) = 314px toward a 460px camera: a 3.2x magnification, measured at 284px wide.
  The rotate belongs LEFT of the scale so the already-shrunk card is what moves in Z, which
  drops the magnification to about 1.28.

Final geometry solved against the owner's reference frame, where the parked card measures
roughly 93x33 at the top centre: scale 0.28, tilt 75 deg, top 34 renders 95x33, centred to
0.0px. Verified in a real browser after walking through 5c, not by deep-link.

**The back button moved out of the sheet and onto the page, for nodes 2-5.** Owner: "shift the
back button from inside the bottom sheet and shift it to the top left like page 5a, also apply
the back button to pages 2-5". `au(back=)` and `sheetbare(back=)` both emit the standard
`nav()`. Positioned absolutely in both hosts because everything inside `.au` and `.ovl--bare`
is absolute — the sheet is pinned to the bottom, the status bar to the top, so there is no
flow for a bar to sit in. The numbers are node 5a's, not new ones: 60px down (`.sbar`'s 56 plus
5a's 4px of nav padding) and the same 22px side inset the whole flow uses.

`sheetback()` now has **no callers**. Kept with a warning rather than deleted: a sheet opened
over a page that has its own back button cannot borrow that one, so the shape may be needed
again — but the page-level bar is the right answer first.

**Identity block: 12px left and 4px down**, netting +12 right / +20 up from where it started
this morning. Still in the card's own units (17.23cqw / 17.22%).

---

## 2026-08-20 (5) — Node 4 actually works; the new background; the card recentred

**Node 4's fields were never wired, and its Proceed could not be enabled even in principle.**
Two independent faults from the same rebuild:

- The `[data-bind]` binding lived inside `wireProfile()`, which runs per **card**
  (`[data-cmp=profile]`). Node 4 stopped having a card when it became a sheet, so the inputs
  were never wired: typing did nothing. Binding a form field's behaviour to the presence of
  an unrelated element was the mistake; it is `wireBinds()` now, which runs per SCREEN.
- Proceed was emitted `state="off"`, and that form deliberately drops `data-go`. Nothing in
  the harness ever removes it, so the button was not "off until valid" — it was off forever.
  `cta(gate="name,mobile")` keeps the target and lets the runtime switch it on.

⚠ Gates read the INPUTS, not `PROFILE`. `PROFILE` carries demo defaults so that jumping
straight to 5b shows a realistic card instead of scaffolding — gating on it would have
enabled Proceed while the fields sat visibly empty, the button and the form disagreeing about
the same question. `PROFILE.typed` is what separates "the demo default" from "what the user
entered", so node 4 starts empty but returning to it shows what you typed.

Verified live end to end: fields empty and Proceed inert on mount; a name alone leaves it
inert; both filled enables it; 5a/5b/5c then show the typed name and number, 5a greets by
first name, and returning to node 4 restores both.

**The new background covers nodes 1-5.** Owner artwork, no alpha noise this time (0 pixels
under 250), 850px wide progressive JPEG q82, 73 KB. Declared once as `--aubg` on `.phone` and
read by both `.au .bg__img` (1-3) and `.ovl--bare` (4-5); a second copy of the data URI would
add ~100KB and could drift. ⚠ **Flagged for the owner:** 1-3 still carry the 42% `.ovl__s`
scrim and 4-5 carry none, and against a photo this bright the scrim now reads much heavier
than it did against the darker house — the splash and login sheet render noticeably grey next
to the source image. One declaration to change, but it is a design call.

**The card rose and the block moved inboard.** The owner asked for 18px up (54 -> 36) and
also that the card read centred on 5b between head and tail. At 36 the gaps measured 30.6
above against 19.4 below, so the stated delta did not achieve the stated goal; 31px does (24
above, 25 below). Solved from the measurement, because the delta was the owner's estimate OF
the goal and the goal is the part that can be checked. Card top identical on all three
screens (221.4) — the sequence stays registered.

Identity block +24px right and +24px up, in the card's own units (9.09cqw and 6.86%) so the
offset holds at every card size. Verified it still sits inside the printed face (right edge
91.69% against the face's 91.78%) and that the number does not truncate.

---

## 2026-08-20 (4) — 5a/5b/5c become one continuous beat around a card that never moves

Owner: "use one image throughout the 3 pages... this will make it a seamless experience not
a refresh at every page and the card jumping around."

**The jump was `.wal.out .wal__card{transform:translateY(-4%)}`** — the card lifted 14px
while the sleeve slid away, and the next screen put it straight back. The two screens'
settled positions already measured 0.00px apart, which is exactly why measuring them did not
find it: the movement happened DURING the slide, not at the swap. The sleeve moves now; the
card is the fixed point of the sequence.

**Node 5c had its own layout and that was the second half of the problem.** `.ksucc` centred
its own card, so the card changed size and position on the one screen where the owner wanted
it to hold still. 5c is a `.ccol` screen now, registered with 5a and 5b — only the text and
the backdrop change. Measured across all three: x/w/h identical, y within 0.01 scaled px
(sub-pixel rounding from the sleeve's -6%, against a 0.5px threshold the FLIP code already
treats as "did not move"). Layout confirmed separately with `offsetWidth`/`offsetHeight`:
264x350 on all three.

⚠ A live `getBoundingClientRect()` read said 5b's card was 2.4px wider. It is not: 5b is the
screen that keeps the gyro shimmer, and `data-tilt`'s `matrix3d` expands the RENDERED box
while leaving layout untouched. Measure `offsetWidth` when the question is layout.

**The sequence the owner described, built:** the welcome dissolves in carrying the first name
typed on node 4 (`[data-wname]`, first word only — "Welcome, Aditi Sharma" reads like a form
receipt); the wallet flips up off the bottom of the screen; tap pulls the sleeve down; the
head and tail swap to "Key created" + the colour block; Proceed swaps to "Key card created"
and starts the dot matrix behind a card that has not moved. Verified end to end in a real
browser with a typed name, not headless.

⚠ The `walUp` keyframes MUST restate `translateY(-6%)` in `to`. That is the sleeve's resting
compensation for the 6% it holds the card at, and a filled animation replaces the declaration
rather than composing with it — an implicit `to` lands the wallet 24px low and takes the card
with it.

**Card pushed down 54px** as asked, on `.ccol__w` rather than the card, so the wallet, the
bare card and the celebration card all move together. Card top 238 -> 292.

**`.ksucc` deleted, not left dead** — 0 markup uses against 4 rule groups. An orphaned second
celebration layout is the next reader's wrong answer to "which layout does 5c use". The
removed-selector audit was run properly this time, against the CSS selector text rather than
the whole file, which is what made it lie earlier today; every live selector survived. Also
fixed a comment that still pointed readers at `.ksucc .dmx` for the full-bleed reasoning.

⚠ Second occurrence of the same status-bar bug: zeroing a screen's side padding for a
full-bleed matrix takes the clock's inset with it and "9:41" renders clipped. The rule the
old celebration needed is now needed by `:has(.ccol):has(.dmx)`, for the identical reason.

**Not literally one DOM element.** The card is still three elements with identical geometry,
because it stays in the screen markup — build-flow, build-export and build-wireframes render
these screens statically and would show an empty column if the card only existed as a
runtime hero. A true single element means the hero pattern (`.phero`/`.khero`) plus a slot
that the static renderings can draw into. Flagged for the owner; the visible result is
already continuous.

---

## 2026-08-20 (3) — The corner card is scoped to 5c; 5a and 5b share one card position

Four owner notes, all four measured before and after.

**The travelling corner card is now scoped to where the key was created.** It was armed by
the celebration and then stayed armed, so stepping BACK to 5b, 5a or node 4 still parked a
key card in the corner — on screens where you have not been given a key yet. `dataset.live`
could not express this, so `KEYAT` records the sequence POSITION the key came from and
`placeKey()` retires the mini whenever the current position is earlier. Recorded as a
position rather than a screen id so it survives 5c moving, and compared against `idx` rather
than `cur()` so an off-sequence edge state inherits the position of the node it branches off.
Verified in a real browser: corner card present on node 6, absent stepping back to 5b / 5a /
node 4 / node 2, and it re-arms walking forward through 5c again.

**The 48px card jump between 5a and 5b is gone — and it was never the card.** `.ccol__w` is
`flex:1`, and the two screens differ both above it (2-line body vs 3-line) and below it (one
link vs label+swatches+CTA), so the leftover box it centred in was a different box on each.
The head is a fixed band now and the object is top-aligned in the middle, so the tail can
differ freely without moving the card; the sleeve gets `translateY(-6%)` to cancel the 6%
inset it holds the card at. The card was also 5px narrower inside the wallet, because the
sleeve shows `0.87 x` its own width — the wallet is DERIVED from `--kcw` now, so the two
cannot disagree. Measured after: dx, dy, dw, dh all exactly 0.00.

**The back button was double-inset.** 44px against node 6's 22, because `.scr` keeps its own
22px on `.ccol` screens (`.scr:has(.pgb){padding:0}` never matches one) and the nav was
adding another 22 on top. The `.pgb--top` rule needs its 22 for the opposite reason — there
`.scr`'s padding IS zeroed. Same visual result from two different sums, which is exactly how
this drifted. Now 22px on 5a, 5b and node 6 alike.

**The edit icon is back, in the identity row**, to the owner's spacing: 12px > DP > 4px >
edit > 8px > name & number. In `cqw` so it holds at every card width; the 12px is measured
from the artwork's printed face, the card's visible edge. `gap` is 0 and the two gaps are
margins on the items they precede — one flex gap cannot express 4 then 8, and using one
value for both is how spacing becomes "whatever looked fine". Measured: 12.0 / 3.9 / 8.0.

⚠ A headless measurement said the retired corner card was still visible (inline opacity 0,
computed 1). It was a **measurement artifact**: `getAnimations()` showed the 260ms opacity
CSSTransition still "running" after 1400ms, because headless does not tick the animation
clock. The real browser reports 0. Worth recording — the same trick that caught a genuine
filled-animation bug earlier in this session produced a false positive here.

---

## 2026-08-20 (2) — The card's content scales with the card; node 5b takes the frame's structure

Owner redline on node 5b, four changes.

**"Going out of bounds of the card scale" was literal, and the cause was fixed px.**
Everything on the card was sized in px while the card itself is drawn at four widths — 264
on node 5b, the wallet pocket's width on 5a, 0.2× as the travelling mini, and again at the
door. Fixed type against a variable card fits at exactly one of those. `.kcard` is now
`container-type:inline-size` and every dimension on it is `cqw`. Proven: the identity block
measures the SAME percentage box (13.5…88, bottom 88.5) on both 5a and 5b while the font
resolves to 10.77px and 10.98px respectively. Measured, too, that the block really was
outside before: its bottom sat at 91.5% against a face that ends at 91.3%.

**The edit pencil is gone** (owner). Added 2026-08-19 from their own SVG, so this is a
reversal. ⚠ Flagged: node 4 is a sheet with no avatar field, so this was the last way to set
a picture. `.kcard__av` still works if clicked but nothing says so — owner call.

**The engraved text**, from the Figma inspector: a white highlight at −0.5/−0.5 blur 1 and a
12% black at 0.5/0.5 blur 0. Kept in px deliberately, not `cqw` — sub-pixel hairlines would
smear into a glow on the big card and vanish on the mini. Applied to the labels as well as
the values, because the owner's two selections were the label+value groups.

**Node 5b takes the frame's structure** — centred, not the left-aligned `pgb`. Nodes 5a and
5b now share ONE class (`.ccol`) rather than two near-identical ones, since they are the same
layout with a different object in the middle; `ccol()` takes head / mid / tail. Measured
against the owner's frame: card top 31.0% (frame 31.4), CUSTOMIZE 77.0 (76.3), swatches 79.9
(80.6), Proceed 88.9 (90.0), card height 41.5% (40.4).

The heading sat at 11.6% against the frame's ~18% because the nav floated. Fixed
structurally by giving `.ccol` a real nav bar that reserves its height — design-system gate
6, the same rule the `.pgb--top` screens already follow — rather than buying the gap with a
`padding-top`, which is what that gate exists to prevent.

**Verified live, not just statically.** Served the prototype and drove it: all five swatches
change the card's background image, exactly one ring lights each time, zero edit buttons
remain, and tap-to-open applies `.out` and hands over to 5b. (`python3 -m http.server`
cannot run in this sandbox at all — argparse evaluates `os.getcwd()` as the `--directory`
default — and the server also cannot read the project directory, so the single-file
prototype is served from a copy in the scratchpad.)

---

## 2026-08-20 — Key-card creation rebuilt as five screens; colourways get a token home

Owner brief: make the key-card stage "more grand, more amazing, more interactive". The old
node 4 was one page where you watched a card fill itself in as you typed. It is now five
screens where the key is **given** to you.

**The shape.** Node 4 is a sheet ("Tell us about yourself", name + number) on the app's own
ground. Node 5 verifies the number in a second sheet. Node 5a presents the key in the
owner's wallet — **two** sleeve layers with the card between them, so it is genuinely
enveloped rather than pasted on — and "Tap to open" slides the sleeve off the bottom. Node
5b is "Key created" with five colourways. Node 5c is the existing dot-matrix celebration.
Node count 24 → 25. The inline "Verify" pill, the old half-verified page and
`mobile_field()` are gone: a sheet that verifies the number leaves no half-verified state
to be in.

**The five colourways now live in `src/tokens/design.tokens.js` as `keycard.ways`** and
build-prototype.py reads them through node at build time. This file otherwise re-states
values raw by design, and the exception is deliberate: the array's ORDER encodes the
owner's mapping ("pink → card two, yellow → card three, blue → card four, green → card
five"), and a mirrored copy of an order-significant list drifts silently. One home
(CLAUDE.md rules 2 and 4). `_ways()` also asserts that artwork exists for every id the
tokens name, so a swatch can never select a card that cannot be drawn.

**Verified by measurement, not by looking.** The colourway path was proven with a
controlled kc1-vs-kc4 image diff: 55,798 px change on node 5b, and the travelling corner
card follows the choice into pairing, which proves the value survives navigation. Two
earlier "verifications" of the same thing were **wrong** and worth recording: patching
`data-kc` into the built HTML proves nothing, because `wireWays()` calls `apply(WAY)` on
mount and overwrites it; and sampling one card against another at different points of a
radial gradient measures the gradient, not the colourway.

**Four bugs the rebuild exposed, all found by forcing end states rather than by reading:**

- The sleeve's two panels have different heights (the front is the pocket,
  `aspect-ratio:572/656`), so one `translateY(118%)` travelled two distances and the
  shorter panel sat in the bottom of the screen after the slide. Now a shared px distance.
  Verified: zero sleeve-green pixels remain below the fold.
- `.kcard__id` inherited `text-align:center` from node 5a's centred column, so the same
  card read centred on one screen and left-aligned on the next. A card's internals must not
  depend on the page around it — `text-align:left` is load-bearing there.
- `.ovl--bare` paints the canvas at z-index 40 and covered the status bar. A scrim is
  translucent and this fill is not, which is why no earlier sheet had the problem.
- `__KCDEF__` was substituted on the CSS chain and the runtime read its colourway default as
  the literal string `"__KCDEF__"`. **This file has ~40 placeholders across three separate
  chains and putting a `.replace()` on the wrong one fails silently.** There is now a build
  assertion that no `__NAME__` survives into the output, proven by deliberately breaking it.

**A slice edit destroyed four CSS blocks again** — the infinity loader, both dot-matrix
layers, the celebration caption and the mobile field's `+91` prefix. The prefix was the
visible symptom (`+91Enter number`, no gap); the rest builds perfectly while silently doing
nothing. Restored from HEAD by **anchored insertion**. Worse, the removed-selector audit
reported them "present" because it grepped the whole file and matched generated markup — the
audit has to look at the CSS text specifically. Index-slice replacement remains banned in
this file; that is now three occurrences.

Gates: voice machine gate clean (it caught "Key created!" — the exclamation was mine, not
the owner's copy, and is gone). No new hex outside the tokens. No absolute black. The one
springy curve is `easings.spring` on swatch selection — a discrete moment, which ADR-005
allows, and not an exit. Reduced motion covered on every new animating selector. 42 screens,
30 on the happy path, 25 nodes across all four renderings.

**Owner calls still open:** nodes 5b and 5c read "Key created" then "Key card created" back
to back. Node 4's sheet has no avatar field and the owner's frames show no edit affordance
on the card, so the pencil on node 5b is currently the only way to set a picture — keep it
or drop the avatar from first run. C-15 (chips FILL vs cards LIFT) is still unresolved.

---

## 2026-08-19 (11) — The shimmer, rebuilt from the reference

Owner, having now supplied an image reference: the rainbowing was *"too much"*,
it was *"going way out"* past the PNG, the corner radius was wrong, and *"the
rainbow effect is not working currently. It is static."* What it should be:
*"only a shimmer which is kind of a dotted visual pattern"*, appearing *"only
when moved"*, as *"a slight strip"*, on nodes **4, 5 and 4a only**.

Five things were wrong. All five are now written into the recipe and MO-GYRO.

**1. It is a SPECKLE, not a wash.** The reference is a field of iridescent dots
in a soft patch. So it is one layer now, not five: a rainbow gradient seen
through a **dot grid**, intersected with a patch the tilt drags around. The dots
are the effect; the gradient only colours them. `mask-composite:intersect` is
what makes it an intersection — without it the masks union and the whole face
fills. Saturated hues are fine *because* they are seen through ~12% of the area;
the same colours as a flat wash are what read as a sticker.

**2. Nothing at rest.** Opacity is purely a function of deflection, from zero.
The old build held 0.22 permanently — precisely the "it is static" complaint.

**3. ⚠ CLIPPED TO THE ARTWORK'S FACE, AND THE FACE IS NOT THE PNG BOX.** This
was the "going way out". `key-card.webp` is an outer translucent **tray** with
the real card face inset inside it, so `inset:0` spilled the shimmer over the
tray and its corner followed nothing at all. Measured off the alpha channel
(longest contiguous run ≥245, at 640×882): face **x 95..544, y 88..763**, i.e.
insets **L/R 14.84%, T 9.98%, B 13.38%**, corner **42px = 9.33% of face width**.
Verified in the browser after: the shimmer box insets 32.5px on a 218.9px card
box — 14.84% exactly.

⚠ **On the 34px request:** the owner asked for a 34px corner. 34 is
`radius.xxxl`, the design system's large-surface radius, but it is **not what
this artwork is drawn with** — measured, the face's own corner is 17.3 css px at
the card's current size. The clip now follows the CARD exactly, which is the
visible intent. Making the card itself a true 34 needs the PNG re-exported (or
rendered ~2418px wide) — an artwork change, so it is flagged rather than faked.

**4. No outer bloom.** The `drop-shadow` glow lit the area *outside* the card —
the other half of "going way out". Removed.

**5. Nodes 4, 5, 4a only.** `data-tilt` is no longer emitted on the celebration
screen or the door.

**⚠ AND A BUG THAT MADE IT LOOK BROKEN: the rAF loop died after one
navigation.** It was guarded with `on:true`, but `clearTimers()` cancels every
handle in `rafs` on each screen change — so the guard then refused to restart
it. The shimmer worked on the first card screen and silently never again, which
is part of why it read as "not working". It also pushed a handle every frame,
growing `rafs` at 60/sec. Now generation-counted: one clean loop per screen,
superseded by bumping `TILT.gen`, nothing leaked. Found by measuring —
`TILT.tx` was updating from the hover while `TILT.x` sat at 0.000.

⚠ **The reference image helped; the video still could not be seen** (X returns
402 without auth). The speckle is built from the still.

Verified: opacity **0** at rest and no bloom; the clip sits inside the card at
the measured inset with `border-radius:9.33%/6.21%`; `mask-composite:intersect`
on both mask layers; hover drives it live and the patch tracks the pointer;
reduced motion holds it at zero. All four renderings rebuild, voice gate clean,
zero dangling targets.

---

## 2026-08-19 (10) — MO-GYRO: the key card catches light

Owner: the card should move with the phone's gyroscope, with the same thing on
hover *"just for desktop, just for our reference"*, and carry a glittery,
refractive, rainbowing, blooming foil that catches light at different angles and
**at the corner edges**.

⚠ **I could not see the reference.** The X link returns 402 without auth; all I
recovered was the post text and that it quotes a 19-second 3D piece titled
"glitter". Everything below is built from the written description, not from the
video — worth knowing if the intent was something more specific.

**Registered as MO-GYRO** in `memory/motion/patterns.md` (CLAUDE.md rule 5),
with tokens split correctly: motion in `motion.tokens.js.gyro`, the five visual
layers in `recipes.cardShimmer`. ⚠ Deliberately NOT reusing
`insuranceCard.gyro` — that object is marked `__exception: true, do not
generalise`, so borrowing it would have quietly generalised an explicit
exception.

**It never springs**, and that is `rules/motion.md` gate 4 rather than taste:
ambient motion uses `standard` at most. This is steered continuously by the hand
holding the phone, so overshoot would read as looseness. `gyro.follow` damps
sensor jitter per frame; it is not an easing.

**Two drivers, one visual path** — `deviceorientation` on a phone, pointer
position across the phone on desktop. Both write the same `--gx/--gy/--gi`, so
the desktop preview cannot drift from the real thing. The first sensor reading
becomes the neutral, because `beta`/`gamma` are absolute and nobody holds a
phone at zero — assuming a posture leaves the card permanently deflected for
anyone lying down. iOS's permission is asked once, on a real gesture.

**⚠ BLEND MODES ARE MEASURED, NOT CHOSEN — and the first build was invisible.**
I shipped the refraction on `color-dodge` and the shimmer could not be seen.
The card is near-white foil, and on white every light-ADDING mode is a no-op. I
rendered screen, color-dodge, multiply, overlay, hard-light, color, hue and
soft-light side by side against the real artwork: **only `multiply` produces
iridescence**, because white × colour = colour. The refraction, sheen, glitter
and edge catch are all multiply now; a single `screen` pass remains for the
card's DARK features (avatar, serif initial, divider, key glyph), which are the
only parts a white highlight can brighten. On a dark card this inverts, and the
recipe says so.

**⚠ A second bug the same shape as before: `pgin` pinned the transform.** The
page transition has `fill:both`, and **a filled animation outranks every normal
declaration** — so no specificity could let the tilt apply. Measured:
`getAnimations()` reported `pgin fill=both` while the tilt rule was live and
ignored. Elements running MO-GYRO are excluded from `pgin`, which is also truer
behaviour: the same card appears on four consecutive screens and should stand
still while the content moves — the argument `carryClass()`'s `holds` already
makes for the carried purifier.

**A third: the highlight was travelling off the card.** The layers are 1.9× the
card so a gradient can move without its own edge entering frame — but
`translate(%)` resolves against the ELEMENT, so `sheenTravel: 0.42` actually
moved the band 0.8 of the card and pushed the highlight clean off at full
deflection. The build divides by `cardShimmer.layerScale` now.

**Where it runs:** nodes 4, 4a, 5 (the hero card), 5a (the celebration), and 18
— shimmer only on the door, because the DRAG owns `transform` there. Off on the
0.2× travelling mini, where it would be invisible and cost a blend per frame.
One rAF loop for all cards, registered on `rafs` so leaving a screen stops it.

⚠ **This is the one place colour is allowed in first run.** That file's visual
direction says no accent green anywhere and the palette rule is two greens; a
rainbow is neither, it is a physical property of a metallic surface. The owner
asked for it explicitly. Flagged in `recipes.cardShimmer` with the note that
this is the block to cut if it ever reads as decoration rather than material.
`holoOpacity` is the single dial for the whole effect's strength.

Verified: hover drives correctly in all four directions, ignores real touch
(which uses the sensor) and resets on leave; the tilt renders a real `matrix3d`
with the bloom active; reduced motion holds a still flat foil with no tilt, no
bloom and no loop — checked with Chrome's own `--force-prefers-reduced-motion`,
not just a `matchMedia` shim, because the shim cannot fake a CSS media query.
All four renderings rebuild, voice gate clean, zero dangling targets, no CSS
lost.

---

## 2026-08-19 (9) — A small-icon register: Lucide, and only below 24px

Owner, after being told morphicons ships no icons: *"these icons will be used
for smaller 24x24 px icons only, only smaller than 24 icons. don't change any
other larger icons and engraved or 3d icons."*

**Lucide adopted** (ISC, vendored with its LICENSE and a manifest in
`design-elements/icons/`) — 18 icons, only the ones actually used, on a 24
grid at `currentColor`. There are now **four** icon registers, not the "two
tiers" the gate still claimed: small UI (this), engraved 77px, 3D renders,
illustrations. The boundary is written into
`.claude/rules/design-system.md` with the size ceiling as a greppable gate.

**Inlined, not data-URI'd** — deliberately unlike the engraved glyphs. At this
size a glyph has to inherit `color` from a row, a dark CTA or a disabled
control, and a background-image cannot.

**Converted** (all previously hand-drawn by me or faked in CSS): the shared back
chevron, the verified check, the Bluetooth mark in a scan row, the mail icon,
the padlock, the row disclosure chevron, close, plus/minus, the inline info
circle, the Wi-Fi strength meter, and the Home mock's tab bar — which had four
grey placeholder blocks and now has real glyphs.

**Untouched, and verified untouched:** engraved icons (still 77px), 3D renders,
illustrations, product artwork, the wordmark, Apple and Google (owner-supplied
brand marks — Lucide carries no brand logos by policy, and substituting a
lookalike for a trademark is a legal question, not a style one), the key card's
owner-supplied edit glyph, the phone's status-bar chrome (it imitates iOS, not
NOMA), and form controls (`.rad`/`.chk`/`.tog` have states, so they stay CSS).

**⚠ FOUND A REAL BUG THE SWAP EXPOSED: Wi-Fi signal strength never rendered.**
The row meter used `class="sig"` — and `.sig` is the STATUS BAR's signal glyph,
carrying `width:17px;height:11px;clip-path:polygon(…)`. The status bar's
clip-path was what you actually saw: one fixed shape, at one fixed size. So
`sigbars()` computed a strength per network and it was thrown away — three
networks at 4/3/2 bars drew identical icons. The meter is `.sigm` now and the
list finally shows the values it is handed. This had been latent since the
meter was written; the icons only made it visible because the new glyph got
clipped into the old polygon.

**Two more class collisions caught before they shipped**, both the same shape
as that one: `.ic-i` drew its own ring with `border` + `::before/::after`, which
would have doubled the Lucide info glyph's circle; `.sr__lock` set
`width`/`height`, which would have overridden the padlock's size. Both reduced
to colour and flow only. There is now an **audit** for this — every class passed
to `icon()` is grepped for `width`/`height`/`clip-path`/`border`/`border-radius`
before the build is trusted, and it reports ALL CLEAR.

⚠ **One placeholder knowingly left.** `.ri`, the leading square on generic
`rows()`, is still a grey block. Filling it would mean *inventing* a glyph per
row rather than converting an existing one, and most of those rows (help,
troubleshooting) arguably want no icon. Flagged in the rules for an owner call
rather than guessed at.

Verified: `icon()` raises on an unknown name (a missing icon fails the build
rather than rendering an empty box); every call site is 13–19px, none above the
24 ceiling; the engraved/3D/brand/renders folders are byte-identical; 59 icons
inlined across the flow; no markup still references the retired CSS-drawn
glyphs; voice gate clean; zero dangling targets.

---

## 2026-08-19 (8) — The key card travels the whole journey

Owner: *"right now the card seems very disjointed... The card shrinks to the top
right and it stays there till the tap your key card to the door page... This is
to basically create a story of the card."*

**Built on the `.phero` pattern, with one state the purifier never needed.**
Same principle — ONE element, created at boot outside the screens, moved by
transform, never re-created — but the purifier only exists where a screen
declares a slot for it. This card has to persist across six screens that say
nothing about it, so it has a third state:

    hidden   before node 5a. The card does not exist yet.
    parked   docked top-right at 0.2x, from the celebration through pairing,
             Wi-Fi, the two permission asks and the household. Screens change
             underneath it; it stays put.
    slotted  D1 declares `[data-kslot]`, so it flies there full-size.

**The shrink is SEEN, not done between screens.** `wireSuccess` calls
`launchKey()` 900ms before node 5a advances: the celebration card is measured,
the travelling card is dropped exactly on top of it, the real one fades, and
the mini shrinks away to the corner — so the eye follows one object.

**⚠ It HANDS OFF at the door rather than becoming the door's card.**
`wireDoorKey` drags a real element and hit-tests it against the lock; making
that element the travelling card would put the drag physics on a node living
outside the screen. So the mini flies to the real card's rect, the real card
fades up underneath it, and the mini retires (`live="2"`). The seam is covered
by both being the same artwork in the same place — and the drag, the glide, the
Enter key and the reduced-motion path all keep working untouched.

**`paintCard()` extracted from `wireProfile`.** There are now three key cards
that can be on screen — node 4's, the door's, and the travelling mini — and
they must never show different names. One paint function, called for the mini
on every keystroke too. `wireProfile` is now null-safe on `scr`, because the
travelling card has no screen to belong to.

The mini's markup is `keycard()` itself, injected once into the runtime as JSON
— not a second simplified copy — so it cannot drift from the card it flew off.

Verified by walking the flow and measuring in design px: hidden at boot and on
node 4; launches at 280px on node 5a; parks at **x=323 y=50 w=53** and holds
that exact position across nodes 6, 13, 17 and 18a; on D1 the target resolves
to `translate(45px, 620.6px) scale(1.136)`, matching the door slot's measured
rect to the pixel; after the hand-off the mini is spent and transparent while
the door's own card is at opacity 1, 300px, and draggable. No console errors in
the flow or export renderings, no CSS lost, voice gate clean, zero dangling
targets.

---

## 2026-08-19 (7) — The card's flip belongs to node 4, and it is a real hinge

Owner: the entrance is node 4's alone — *"only on the number four page. Do not
touch any other page... in the mobile OTP section and the setup profile
verified section, it will remain static"* — and it should read as a genuine
rotation in 3D, flipping in from the top half while the fields rise from the
bottom.

**It was playing on four screens, not one.** `profile_page()` is shared by node
4, node 5's sheet-over-it, node 5's "nothing arrived" state and node 4a, and it
passed the entrance classes unconditionally. So opening `#A5` or `#A4V`
directly played the flip on a screen it does not belong to. `enter` is now a
parameter, passed only by node 4.

⚠ **That is a SECOND guard, not a replacement for the first.** `cardEntered`
answers *"again?"* — a return visit to node 4. `enter` answers *"here?"* — the
wrong screen entirely. Both are needed and they are independent; the once-per-
run flag never would have caught a direct load of `#A5`.

**Both halves are now gated together.** Stripping only the card's class left the
content still replaying `pgbIn` on every return to node 4 while the card sat
still — half an animation, which reads worse than either whole. The card
flipping down and the fields rising are one entrance, so `wireProfile` removes
`pgb--enter` alongside `kcard--enter`.

**The flip is a hinge now, not a tilt.** `transform-origin:50% 0%` with
`rotateX(-95deg)` stands the card up off the page toward the viewer, edge-on and
effectively invisible, and it lays down onto its own footprint as the angle
closes — past 90 by a few degrees so it swings *through* vertical rather than
easing out of a lean. `translateZ(70px)` releasing to 0 is what reads as depth
rather than a 2D squash. Measured through the arc: rotateX 95° at 0ms with a
projected height of **10px**, 35° at 120ms, 5° at 300ms, settled at 302px —
with the hinge confirmed at `132px 0px`, exactly the top-centre of the 264px
card. Travel stays short (-30px) because `.pgt` no longer clips, so a long one
would fly the card over the nav.

Verified by walking the flow: `kcardIn` + `pgbIn` on the first visit to node 4;
plain `pgin` on node 5, node 4a, node 5's error state, every return to node 4,
and on a fresh run that lands on `#A5` first; and the entrance restored after
`reset()`. No CSS was lost this time — checked with the removed-selector diff
the previous entry introduced, and every animation still sits inside a
`prefers-reduced-motion` block.

---

## 2026-08-19 (6) — Owner edit glyph; the flip is once; the matrix is a sibling

**The edit affordance on the key card is the owner's SVG**
(`edit-svgrepo-com.svg`), replacing a hand-drawn single-stroke pencil. Small,
50% opacity, 4px clear of the avatar — and every value is a PERCENTAGE OF THE
CARD so it survives the 0.9× scale and any future resize; the 4px is converted
once, against the card's own 264px width. Measured after: gap **3.96px**,
14×14, opacity 0.5, vertical centres matching to 0.1px.

**The card's entrance is once per run, not once per visit.** It replayed
because this harness rebuilds a screen from its stored HTML on every
navigation, so `kcard--enter` arrived fresh each time — including walking back
from node 5's OTP sheet and onto node 4a. A `cardEntered` flag now strips the
class after the first play; it is checked in `wireProfile`, which runs in the
SAME task as the `appendChild`, so the class is gone before the first paint and
the animation never starts rather than being cut off mid-flight. `reset()`
clears it, so replaying the flow replays it. Verified across six navigations:
`kcardIn` on the first visit to node 4, nothing on the OTP sheet, nothing back
on node 4, nothing on 4a, nothing later — and node 5a still runs its own
`ksuccCard`.

**⚠ THE DOT MATRIX WAS CLIPPED FOR A REASON TWO PASSES OF PADDING MATH COULD
NOT FIX.** `.scr.in .pgt>*` gives every direct child of the visual half a
`pgin` transform — and **a transform creates a containing block for absolutely
positioned descendants**. The backdrop was a child of that wrapper, so it could
never grow past the wrapper's content box no matter what insets it was given.
The first fix cancelled one padding (still 349 wide), the second cancelled both
(393 wide but 14px off-centre — the transform's own translateX, caught
mid-animation). Only measuring the parent chain showed it.

Fixed structurally: `dotmatrix()` now emits a **sibling** backdrop rather than
wrapping the content, and `.dmx` is excluded from `pgin` so nothing gives it a
transform again. Positioned by `.pgt`, it is full-bleed by construction — 390
wide, 0.0px each side on both node 5a and node 16, with nothing to keep in
sync. Removing the screen's side padding also clipped the status-bar clock to
":41", so `.sbar` got its 22px back explicitly.

**⚠ I DELETED THREE CSS BLOCKS BY ACCIDENT AND CAUGHT IT WITH A GATE, NOT BY
EYE.** Two edits used `s[s.index(a):s.index(b)]` slice replacement, and both
swallowed rules that happened to sit between the anchors: the first took the
base `.dmx` / `.dmx__base` / `.dmx__ring` / `@keyframes dmxRing` group, the
second took the whole `.inf*` loader block, `@keyframes infSpin`, its
reduced-motion rule, `.ksucc .kcard`'s settle and `.ksucc__cap` with both their
keyframes. The reduced-motion audit flagged `.inf__d` as uncovered, which is
what exposed it. All restored, then verified by diffing every removed selector
against the current file — only `.dmx__c` is intentionally gone.

**Lesson worth keeping: index-slice replacement is not a safe edit.** It
deletes whatever is between two anchors, including code you never read. Use
anchored exact-string replaces, and after any structural CSS edit, diff the
removed selectors against the file rather than trusting the build to fail —
missing CSS builds perfectly.

Verified: all four renderings rebuild; voice gate clean; zero dangling
`data-go`; all four animations (`geoDrift`, `dmxRing`, `infSpin`, `kcardIn`)
confirmed inside `prefers-reduced-motion` blocks.

---

## 2026-08-19 (5) — Owner artwork in; confetti out; a progress bar that lied

Seven owner changes across the pairing and account halves.

**Node 24's geofencing illustration is now the owner's SVG.** Consumed in two
pieces: the house, boundary and glow are one base64 plate, and the green "you"
dot is stripped out and re-drawn as a positioned element so it can still travel
across the dashed line — the behaviour the CSS stand-in had, which the owner
asked to keep. **The dot's geometry is PARSED from the file, never
transcribed**, so a re-export moves the animation with it, and the stripper
asserts, so a changed dot fails the build rather than silently shipping two.
Verified by measurement: the dot rests **84px** from the ring centre (ring
r=62) and reaches **52px** mid-cycle — it genuinely crosses the boundary.
⚠ The dot is `#7CF280`, the only colour in first run's illustrations, and this
file's own visual direction says it has no accent green. Owner-supplied
artwork, so it stands — flagged in
`design-elements/illustrations/README.md` rather than quietly recoloured.

**The key card was cropped because it never fit.** Measured: 404 tall in a 304
content box, losing ~20px off the bottom to `.pgt`'s clip. Now 0.9× (293→264)
AND unclipped, with the padding rebalanced. ⚠ Unclipping is only safe because
the flip's travel was shortened from -104px to -44px in the same pass —
otherwise the entering card escapes over the nav instead of being hidden by
the clip. The two are a pair. The name/mobile block moved 41.5%→35% so the
number clears the divider printed in the artwork.

**Confetti replaced by a dot matrix with a ring travelling through it.** The
trick, and the reason it is two layers rather than a ring drawn on top: one
grid rests in very light grey, an identical grid in darker grey is masked to an
expanding annulus, so the ring reads as *the dots lighting up* and no ink is
ever drawn between them. `@property` is load-bearing — a bare custom property
does not interpolate, so the mask radius needs its type registered. Verified:
`--dmr` travels 0% → 25.7% → 51.6% → 63.3%. Greys and white only; the
reference was a dark colour shot and only its structure was taken. Node 16
(connected) takes the same component, so the flow's two celebratory beats
cannot drift apart. The old confetti CSS was **deleted, not commented out** — a
disabled effect is one `display:block` from returning by accident.

**⚠ A BUG I INTRODUCED AND CAUGHT: node 15 would have become a dead end.**
Swapping the progress bar for the indeterminate loader removed `.pb` from that
screen — and `wireLoad()` opened with `const bar = …; if (!bar) return;` with
the timed hand-off *inside* the bar's branch. No bar, no advance, and node 15
has no button: the flow would have stopped there permanently. The advance is
now unconditional and the bar is optional decoration. Proven both ways: a
bar-less holder arms **1** timeout (it armed 0 before), one with a bar arms 2.

**The progress bar deserved to go.** It filled over a fixed ten seconds while
the real work takes 15–20 — a bar that lied twice, about the duration and
about being measurable at all. Replaced by a lemniscate loader whose path is
generated and *measured*, so `stroke-dasharray` derives from real arc length
rather than a guess, plus a 10px line giving the estimate in words.
`prog()` and `.pb` are removed; a determinate bar is still supported by
`wireLoad()` if a screen ever genuinely knows its duration.

**Node 12 top-pinned** to match node 13 — owner: *"it should not shift from
page to page. Both are Wi-Fi pages."*

**Node 18a lost the contacts list.** Two consequences worth naming rather than
discovering later: `KEY_CONTACTS` and its hue-coded avatars are unused by this
screen, so the flag about them reversing the 2026-08-12 palette rule is
**closed by deletion, not by decision**; and `wireKeys`' pill-picking path is
now unreachable, so the CTA no longer counts a selection. The wiring is left in
place because the field is where a recipient comes from now and a future
picker would want it back. The resident's key went 1.5× (151→227) and is
**centred** rather than bled off the right — at the new size the old `-8%`
offset cut the artwork's "NOMA" wordmark in half, which reads as a mistake
rather than a crop.

Verified: all four renderings rebuild; voice gate clean; zero dangling
`data-go`; and every one of the four new animations (`geoDrift`, `dmxRing`,
`infSpin`, `kcardIn`) confirmed present in a `prefers-reduced-motion` block —
checked by parsing those blocks, not by eye.

---

## 2026-08-19 (4) — One design system: three CTAs, one black, one back button

Owner, with justified irritation: the back button had lost its locked style,
the OTP page's CTA was a different black from the login sheet's, chips and
toggles were flat and too dark, engraved icons were too big for the new top
layout, list rows were using those same big icons shrunk, and the back button
was overlapping content on three pages. *"We cannot keep changing everything...
a design system needs to be followed."*

**The cause was structural, not carelessness, and worth naming.**
`build-prototype.py` predates the token loader and declares its own components
in raw hex; `build-auth.py` reads the recipes. So the product had TWO
stylesheets describing the same controls, and they drifted:
`.cta` was `background:var(--ink)` — **#0B0B0B, flat, no shadow** — while the
sheet's `.s-cta` was the ink **gradient** (#3A3A38 → #2E2E2C) with a real drop
shadow. Node 5's OTP sheet looked wrong because `sheetover()` calls `cta()` and
so pulled the page button. Matching them by eye is what produced the drift;
pointing both at the same recipe is the only fix that stays fixed.

Everything below now reads `recipes.*` in that file's token-driven append
block: `.cta`, `.cta2`, `.qlink`, `.nb`, `.chip`, `.rs__t`, `.tog`, `.chk`,
`.rad`, `.pcard`. Measured after: the selected room chip and the primary CTA
both compute to `linear-gradient(rgb(58,58,56), rgb(46,46,44))` — byte-identical
— and the back button to `#F8F8F8` with its shadow.

**#0B0B0B is no longer a fill anywhere it acts as a surface.** Owner: *"do not
use any other black. Don't use the absolute black color."* `--ink` stays the
TEXT colour. I grepped every `background:var(--ink)` rather than fixing the
reported ones: **three separate selection components** had their own copy of
the absolute-black fill — `.chip.on`, `.tog.on` and `.rs__t.on`. The owner
named the room chips; had I fixed only `.chip.on` it would have looked handled
while `.rs__t.on` (the actual component on node 17) stayed wrong. Small dark
*marks* — signal bars, carets, dots, clock hands — are left as ink, which is
correct; the rule is about surfaces.

**The back button is the locked one again**, and there is now exactly one.
`recipes.buttonIcon`: 40px, #F8F8F8, **1px #FFFFFF inside stroke** (the thing
that makes it read as glass, and the thing that had been dropped), two-layer
shadow. `nav()` and `sheetback()` share a single `BACK_SVG` chevron — two
buttons that merely looked alike is how they came apart. Verified by zooming
both the page nav and the sheet's: identical.

**A real top navigation bar.** On top-aligned pages the nav is now
`position:static` and reserves its own height, so nothing can ride up under it.
A previous pass had bought clearance with a `min-height` spacer on `.pgt` —
a spacer pretending to be a bar, which broke the moment a page had no visual
half. R1/R2/P1 no longer collide.

**Engraved glyphs 0.8×** (96→77, 104→83) and demoted to page headers only. The
Bluetooth list row was drawing the engraved render at `background-size:150%`
inside a 30px tile; it now gets a plain monoline mark. Notably the same mistake
had already been fixed for the Wi-Fi lock/meter pair a day earlier — *"the
previous pair reused the big Wi-Fi glyph shrunk to 15px, which read as a
smudge"* — and this tile was simply missed.

**`.pcard.on` stopped drawing a 2px absolute-black outline.** build-flow.py has
re-skinned it to LIFT since 2026-08-18, calling that *"the single biggest
visual change in the file"*, so the prototype and the flow rendering had been
showing the same screen two different ways — the same split the phone's ground
had. Now aligned. First attempt used `control` elevation for both selected and
idle and the selected card was indistinguishable; it lifts `card → floating`,
two steps apart, so the difference actually reads.

⚠ **C-15 opened in memory/decisions.md, not resolved.** LAW 3 and
`recipes.chipSelected` say selection is LIFT and *"never an outline and never a
fill"*; the owner's instruction is that a selected chip takes the CTA's dark
fill. Both are now built — chips FILL, cards LIFT — which is defensible but is
an accident of two instructions arriving separately rather than a stated rule.
Flagged for one owner call rather than silently picking a winner (CLAUDE.md
rule 6).

Six greppable gates added to `.claude/rules/design-system.md` so this cannot
drift again quietly.

---

## 2026-08-19 (3) — A specificity collision had silenced BOTH node-4 animations

Owner: no confetti, no card flip, the background changed, and list pages shift
as items arrive. Four reports, three of them the same root cause as things
this file has been bitten by before.

**⚠ THE ENTRANCE ANIMATIONS NEVER RENDERED A SINGLE FRAME.** Not "looked
wrong" — never ran. The generic page-to-page transition is
`.scr.in .pgb, .scr.in .pgt>*:not(.pslot)` at **(0,3,0)**; I had written
node 4's entrance as a bare `.kcard--enter` **(0,1,0)** and
`.pgb:has(.fld--verify)` **(0,2,0)**. `pgin` won on both, so the card sat flat
and the fields never rose. Found by measurement, not by eye:
`getAnimations()` on the card reported `pgin 280ms`, not `kcardIn`.

Fixed with `.kcard.kcard--enter` / `.pgb.pgb--enter` under
`:is(.scr.in,.scr.bk)` — **(0,5,0)**, so they win on WEIGHT rather than on
source order. A tie would have "worked" only until somebody moved the block.
Also replaced the `:has(.fld--verify)` sniff with a real `pgb(enter=True)`
flag: explicit, greppable, and it cannot be out-specified by accident.
**Third time this file has been bitten by an unnoticed higher-specificity
rule** (`.pgb p`, `.flow-thumb-frame`, now `pgin`) — the arithmetic is written
into the CSS comment this time.

**The confetti had two independent reasons to be invisible**, and the fix for
each is now documented where it lives:
- it carried a 1px hairline ring instead of a shadow, and a 1px ring vanishes
  at 7px against a ground that starts at #FFFFFF. White-on-white needs the
  drop shadow to exist at all — which is exactly what the owner asked for.
- it sat at `z-index:0`, *behind* the card, so the card's own artwork hid most
  of it. Now `z-index:1`, over the card.
Rebuilt as a **burst** rather than a fall: pieces start stacked at the card's
centre and fly outward on evenly-distributed angles with jitter (pure
`Math.random()` clumps, and a clumped burst reads as a bug), 34 pieces, a mix
of squares and short ribbons, +38px downward bias so it arcs instead of
expanding as a perfect ring. White only, one 2px shadow at 18%.

**The card flip is a real flip now** — `rotateX` about the card's own top edge
under a 1100px perspective, so it tumbles forward and lands flat instead of
sliding in at an angle. Verified by pinning `currentTime`: −74° at 0ms, −10.7°
at 200ms, flat at 640ms, with the fields travelling 72px→0 over the same 640ms
and the same easing, so the two visibly converge.

**THE BACKGROUND: the owner was right, and this file was the odd one out.**
`:root` painted the phone with a cool radial falling to **#A4A4A4**. The
previous first run (`build-onboarding.py`) has always used
`gradients.canvas`, and `build-flow.py`'s re-skin already overrode this line
to canvas — its own comment reads *"was radial → #A4A4A4 grey"*. So the SAME
screens had two different grounds depending on which rendering you opened, and
the prototype held the stale one. Nothing in this pass changed it; node 5a is
simply the first screen with enough bare ground to make it obvious. Now read
from the token via a `__CANVAS__` substitution in `css_out()`, so the three
renderings cannot drift apart again. Measured: `#f3f3f3/#e5e5e5/#c5c5c5` →
`#fefefe/#f9f9f8/#e9e8e6`. The docstring's stale "VISUAL DIRECTION" claim
(which had matched the wrong value) is corrected rather than left to mislead.

**List pages are top-aligned** (`pgb(top=True)`): P1, P5, W1, R1, R2. A
bottom-pinned list grows UPWARD — each arriving item makes `.pgb` taller,
shrinks `.pgt`, and slides the icon and heading up. A/B measured on W1: the
heading sat at **486 with a short list and 361 with a full one, a 125px jump**;
top-aligned it holds at **214** either way. The CTA keeps the bottom edge via
`margin-top:auto`, and a `foot()` between list and CTA deliberately stays with
the LIST, which is what it explains.

⚠ One thing that only showed up on screen: R1 and R2 have an **empty** `.pgt`,
so top-aligning slid their content under the floating nav and the eyebrow
overlapped the back arrow. The nav is absolute and floats over the visual half
by design — safe when that half is tall, wrong when it is empty. Measured nav
at 50–82, eyebrow landing at 65; `.pgt` now reserves `min-height:46px` on
top-aligned screens only.

Verified: all four renderings rebuild (41 screens, 24 nodes); voice gate
clean; zero dangling `data-go`; both animations confirmed by
`getAnimations()` name-and-transform probe rather than by screenshot, after a
first screenshot pass wrongly suggested the flip was fine (headless had shown
the settled end state).

---

## 2026-08-19 (2) — Email and phone swap places; a "key card created" moment

Owner: the login sheet should lead with Apple/Google, phone verification moves
to the setup-profile page, and that page "looks way too static."

**The account section's five screens (S0-A5) keep their PRD node numbers but
trade what they verify.** The sheet (nodes 1-3) used to collect and verify a
phone number; now it does email. Node 4's page used to collect an email next
to the name; now it collects the phone number, verified inline via a "Verify"
pill that opens node 5 — the exact same sheet-over-page relationship node 5
already had, just the other contact method. Apple and Google both skip
straight to node 4: a federated sign-in has already verified the person, so
there is no email left to check — only "Continue with email" walks through
nodes 2-3.

**Two new icons**, owner-supplied, replacing a hand-approximated Apple glyph
and adding Google for the first time: `apple-173-svgrepo-com.svg` and
`google-icon-logo-svgrepo-com.svg`. Google's mark stays its real four colours
on purpose — brand guidelines specify it, and it is the one icon in the file
that does NOT take `currentColor`. Baked the source SVG's nested `<g
transform>` offsets into the path data so both drop in as flat
`<path fill="currentColor">`/multicolour paths matching every other icon here.
⚠ The source Google SVG carried literal `width="800px" height="800px"` on a
262-unit viewBox — CSS sizing overrides it, but it was one accidental
unscaled paste from a giant icon; stripped.

**Two new branch states**, 4a and 5a — node 4 never had either before. 4a is
node 4's page with the phone marked verified (checkmark, Continue live); 5a
is new outright: "Key card created," all-white confetti (no colour, on the
owner's instruction), the card settling to the screen's centre as the fields
it came from disappear, auto-advancing into pairing after 1.8s. Node count:
21 main-line + branches 4a/5a/18a = 24, up from 22.

**"Meet in the middle."** Node 4's card now drops in from above with a slight
rotation while the fields rise from below, both the same duration and easing
so they visibly converge rather than one waiting on the other. Scoped
deliberately: `keycard()` gained a `cls=""` parameter (only node 4/4a pass
`kcard--enter`) rather than animating every card, since the same function
also draws the door finale's key; the fields' entrance is scoped via
`.pgb:has(.fld--verify)` rather than touching `pgb()`'s signature, since that
helper is the generic content-half every other screen in the flow uses.

**No green was introduced for the "Verify" pill.** This file has never had an
accent colour — no `--acc` custom property, unlike build-auth.py/
build-flow.py which already read the token file — and the two-green palette
question is still an open owner call in `.claude/rules/design-system.md`.
The pill and the checkmark are both ink, which keeps this change out of that
decision rather than presuming an answer.

**Caught by the voice/link gates, not by eye, twice:**
- A1's `au_state()` call was missing `handoff="A4"`, so in the merged flow
  (not the standalone deck) Apple and Google's buttons still carried the
  literal `data-go="DONE"` marker — a real dangling link the automated check
  caught, not a cosmetic one.
- Two new notes used `<b>` tags for emphasis. Every note panel in this file
  renders via `.textContent`, not `.innerHTML` — the ONLY two `<b>` tags in
  ~40 note strings across the whole file, both mine, both would have shown
  as literal `<b>` in the UI. No markup in a note string, ever; the file's
  own convention is plain text with real punctuation for emphasis.

Also fixed while touching this section: `au_state()`'s dead `phone=`
parameter, `code={A3:'', A5:''}` and a `data-phone` wiring block in
build-auth.py's own JS that were only ever going to be read by content this
rewrite removed; a stale `FIRST` dict that was defined but never read at all
(not embedded into JS, not referenced anywhere) — dropped rather than carried
forward as false signal, since this exact section was already being
rewritten. build-wireframes.py's branch count was hardcoded to "1 branch";
now computed, so it will not go stale again the next time a branch is added.

Verified: all four renderings rebuild clean (41 screens, was 40); voice gate
clean; zero dangling `data-go` targets; the standalone `auth-prototype.html`
walkthrough tested live — typed an email, watched Proceed enable, clicked
Apple and confirmed it lands on the shared `DONE` hand-off exactly like the
old mobile flow did; reduced-motion path checked by forcing `matchMedia`
before the page's own script ran, confirming the confetti is skipped and the
advance uses the faster 900ms timeout rather than 1800ms.

---

## 2026-08-19 — The card design; corner smoothing is real now

Owner sent a Figma inspector frame of the sign-in sheet plus a corner-smoothing
panel at 100%, and three instructions: the design-system pages show nothing on
Vercel, apply the inspector's values, and the card treatment is for **large**
surfaces only.

**The Vercel pages were a class collision, the fourth this project has had.**
`renderNomaSizing` / `renderNomaScenarios` embedded their iframes with
`.flow-thumb-wrap` / `.flow-thumb-frame` — the THUMBNAIL classes. Inline
width/height overrode two of their properties and left the rest: the frame kept
`position:absolute`, `transform:scale(.29)` and `pointer-events:none`, so the
page rendered a 205x209 unclickable thumbnail instead of a document. Measured
before/after against the real stylesheet: 205x209 absolute+scaled → 706x558
static, no transform. Now on `.flow-stage` / `.flow-frame`, the pattern the
Flows pages already proved, plus an "Open full page" link.

Same lesson as `.link` / `.cta` / `.scan` / `.done` and the `.pgb p` reset:
**reusing a class inherits every property you did not think about.**

**CORNER SMOOTHING IS NO LONGER AN INTENT.** `radius.smoothing` was 0.6 and
documentation-only, on the reasoning that CSS cannot draw a superellipse. It
still cannot — but `docs/_squircle.py` now ports Figma's own corner geometry
and emits it as a **9-slice mask** (`mask-border` / `-webkit-mask-box-image`),
which restretches at any element size with no script and no ResizeObserver.
That last part is what makes it viable: a sheet changes height on every state,
so a fixed `clip-path` was never going to hold. Raised to 1.0, the full iOS
value, per the owner.

Three bugs found by measuring rather than looking, all worth remembering:
- the data URI was **quoted**, which ends an inline `style="…"` attribute the
  moment it lands in one. Silently masks the element to nothing. Now unquoted —
  percent-encoding leaves nothing that needs delimiting.
- the stroke colour was escaped twice (`%2523`), so the hairline never loaded.
- headless Chrome needs `--virtual-time-budget` for the mask image to decode
  before the screenshot. Add it to the list beside "headless does not tick
  animations".

**A masked surface cannot cast a shadow** — a mask clips everything an element
paints, outer shadow included. So a large surface is two nodes: a shell with
the shadow and a `border-radius` that exists only to shape it, and a masked
child with the fill and hairline. Under a 48px blur nothing can tell an arc
from a superellipse, which is what makes the split free.

**From the inspector**, all now in tokens: `radius.xxxl` 34 (large surfaces
only); sheet wordmark 84 → **56 at 50% opacity** (a signature, not a headline);
`display` 30/700 → **28/600**; new `action` 14/600, `actionSmall` 12/600 and
`legal` 10/400 with a `linkWeight`, wired through `buttonPrimary` /
`buttonQuiet`. The page-level `.cta` was still 16.5 — extended to the same
register, or the label would jump 14 → 16.5 at every sheet-to-page hand-off.
Also removed a **duplicate `paddingX`** in `recipes.bottomSheet` (dead, same
value, would have diverged silently on the next edit).

**The scope rule has arithmetic behind it, and that was worth finding.** The
owner drew the boundary by feel — sheets and dialogs yes, small cards no. It
turns out the shape enforces it: a smoothed corner needs 68px of edge to ease
into, so two need **136px** between them. Below that the 9-slice corners
overlap and the surface goes bulbous. A 56-tall list row *physically cannot*
hold this corner. `SQ.min_size()` returns it and `.claude/rules/design-system.md`
gates on it.

Applied to the sign-in sheet, the OTP sheet over the profile page, and the
permission dialogs. ⚠ TODO(owner) recorded in `recipes.dialog`: the flow's own
docstring argues those alerts read as truthful *because* they are the system's,
not the app's — branding them trades that accuracy for consistency.

**New:** `docs/design/large-surfaces.html`, the third generated spec page
(anatomy, the corner at three smoothings, the scope boundary with the bad case
shown rather than described, the sheet's type ramp, and why it is two
elements). Mirrored to Vercel as its own folder. Also fixed: scenarios case 12
still claimed "these prototypes do not render it", and all three pages lacked
`<meta charset>` — invisible on Vercel, which sends the header, but mojibake
locally.

---

## 2026-08-18 (10) — A specificity bug closed the eyebrow gap; scenarios documented

⚠ **I broke the eyebrow→heading gap in the previous pass and the owner caught
it.** The UA margin reset was written `.pgb p` — specificity (0,1,1) — which
OUT-SPECIFIES `.eyb` and `.lab` at (0,1,0) and silently zeroed the very rhythm
margins it was meant to protect. Measured: eyebrow margin-bottom 0 where the
rule said 12, and the label's 24/8 gone entirely. Now
`.pgb p:not([class])`, so the reset only claims elements with no component
rule of their own. Verified back at 12.

Worth keeping: **a margin reset is a cascade weapon**. Scoping it to unclassed
elements is the fix; raising every component's specificity to out-shout it is
the trap.

**`radius.smoothing` 0.6** — owner: corners are smoothed like iOS, "very high,
to give a premium feel". ⚠ Recorded as an INTENT, not something the prototypes
render: CSS `border-radius` only draws a circular arc, and a smoothed corner is
a superellipse. The token exists so the native build reaches for SwiftUI's
`.continuous` rather than inheriting a circular corner and quietly losing the
thing that makes the shapes read as premium.

**A second generated spec: `scenarios.html`** (`build-scenarios-dashboard.py`).
Twelve adjacencies — all-caps→heading, heading→body, body→block, label→field,
field→field, title→control, stacked buttons, content→CTA, the three button
weights, the three greys, the sheet's own padding, and corner smoothing — each
as a live specimen at true product size with the gap marked and the reason
given. Published as an artifact and added to the Vercel design system as its
own folder alongside Sizing & rhythm.

---

## 2026-08-18 (9) — The owner redline: sizing tokens, and a generated spec

**The sheet was over-spaced for a reason no one could see.** The `<h1>` and the
`<p>`s inside it carried their UA block margins (0.67em / 1em), which stacked
on top of every rhythm value — the title alone added ~20 to the gaps either
side of it, and the countdown added ~19 under itself. Zeroed at the component
root, so the rhythm tokens are now the ONLY vertical spacing there. Measured
after: node 1's sheet reads mark→title 12, title→CTA 18, CTA→Apple 8 — the
redline exactly. Sheet content 329 against the redline's ~324.

**New sizing tokens, all from the owner's annotated frames:**
- `rhythm.titleGap` 18 — title → first control. ⚠ NOT a ramp stop, and kept
  measured rather than rounded: 16 crowds, 20 reads as a section break.
- `rhythm.controlGap` 12 → **8** — stacked controls. Two buttons 8 apart read
  as one group of choices; at 12 they read as unrelated.
- `layout.ctaHeight` 56 → **54**; new `layout.ctaQuietHeight` **46**. The
  height difference IS the hierarchy — a quiet button at the primary's height
  reads as an equal choice however pale it is.
- `layout.sheetPadX/Y` **20 / 24** — the sheet's own padding goes back to
  sectionGap. The "condense the sheets" pass had squeezed it to 12/12; the
  height now comes out of the gaps BETWEEN things instead.
- `layout.otpBox` **[56, 52]**.

**⚠ THE REDLINE ADDS A THIRD SIGN-IN ROUTE.** "Continue with email" is drawn on
node 1, which directly reverses that screen's founding rule ("two ways in and
no third — no email/password") and reopens a closed question: an email route
skips phone verification, so nodes 2 and 3 leave the universal path, and node 4
already collects an email of its own. Built as drawn, routed to node 4, flagged
in the screen note — where it truly rejoins is an owner call.

**A generated spec page.** `docs/design/build-sizing-dashboard.py` →
`sizing-and-rhythm.html`, read from the token file at build time so it cannot
drift; published as an artifact and mirrored into the Vercel design system as
its own folder. It answers in the owner's own notation — live specimens at true
size with red measurement brackets — so a value can be checked with a ruler
rather than taken on trust. The Vercel folder deliberately frames the page
rather than restating its numbers; restating them is the drift the generator
exists to prevent.

---

## 2026-08-18 (8) — The merge fixed structurally; rhythm and input tokens

**The cross-dissolve is gone because there is no longer anything to dissolve.**
Third attempt, structural this time: fading a whole transparent screen from 0
shows the bare ground for the first frames (the flash), and overlapping two
screens shows both contents blended (the merge) — those were the SAME bug in
two costumes. The swap is now a single paint (old removed and new appended in
one task, so the browser never paints between them) and what animates is the
new screen's CONTENT, entering over a ground that never changes — the grammar
the carry screens already used. Verified: exactly ONE `.scr` in the DOM at
every sampled instant, including three navigations in one tick.

**Two token additions, grounded on Mobbin (Airbnb login, CRED onboarding)
rather than guessed:**
- `rhythm` — `textGap` 12 (within one text set: eyebrow→title→body),
  `sectionGap` 24 (between blocks: text→field, field→CTA), `controlGap` 12
  (siblings in a group). The s3/s6 stops of the existing ramp, promoted to a
  named grammar. Airbnb runs ~8-12/24-32, CRED ~12/24-32; the owner's own
  instinct was 12/24.
- `recipes.input` — REBUILT from the owner's Figma inspector: flat #FFF,
  radius 8 (was 20), 1px #000@12% stroke inside (was borderless), height 52
  (was 56), two inner shadows, no drop elevation. A field is a sunken well
  now, not a floating card; the CTA keeps its pill, and the contrast between
  the two is the point. `layout.inputHeight` 56→52.

Applied across the sheet fields, the page fields (`.fld`) and build-flow's
re-skin (which reads the recipe verbatim); rhythm applied to the sheet
(eyebrow/title/otp/resend/cta) and the page structure (eyb/t1/bd/lab/fld).
⚠ Flex columns do not collapse margins, so block boundaries must not stack —
`.pgb .bd+.lab` and `.fld+.lab` carry explicit corrections.

NOT PUSHED — owner asked to see the tokens first.

---

## 2026-08-18 (7) — The transition flash, R1's order, and the key page's tail

**The A3→A4 and P4D→P5 flash was both layers fading at once.** The incoming
screen faded in *while* the outgoing one faded out, so mid-transition each was
semi-transparent and the phone's bare ground showed through BOTH. It is worst
exactly where it was reported — leaving a full-bleed photo for a light page,
and losing the purifier. The outgoing screen now stays opaque and is simply
covered.

Two latent bugs came out of testing that, and both are real:
- The outgoing screen **kept its `in` class with the fade still mid-flight**, so
  a FAST tap left it stuck part-way and the flash came back. It is now stripped
  of its arrival classes and pinned opaque. Verified at a 100ms tap interval.
- Its removal timeout rode `touts`, which `clearTimers()` empties at the top of
  every render — so the dead screen lingered under the live one until the next
  sweep caught it. Untracked now.

**R1 is reordered** (owner): title and body, then the home name, then the room
chips, then the drawing last. The picker left the visual half to do it. ⚠ That
makes node 17 the one screen in the flow that does not follow the 2026-08-17
structure — illustration last rather than first. The reading order is better
(you name the home before placing a device in it) and §5.9's morph gesture is
untouched, but a one-screen exception to a flow-wide structure is a decision.

**Node 18 collapsed to a single Continue** (owner), so the diagram's branch —
invite the family vs. not now — moved onto node 18a, where "Not now" is a new
tertiary action: no container, no fill, under the CTA. Skipping the household is
still first-class; it just no longer competes with sharing for the eye.

**Node 18a's key card is 0.8× again** (189 → 151) and the visual half releases
its clip when it holds one — a rotated box is taller than its own width, which
is what was cutting the card top and bottom.

**The toast advances by itself** (owner: "no need for the user to press continue
again"). A confirmation you have to acknowledge is a screen wearing a toast's
clothes.

---

## 2026-08-18 (6) — One purifier moved instead of five cross-faded; engraved icons

1. **The flicker was a repaint, and the owner's diagnosis was right.** Every
   pairing screen rendered its own `.rnd` element and the runtime FLIPped
   between them — same data URI, new element, so the browser re-rasterised the
   background on every screen. There is now exactly ONE purifier in the
   document (`.phero`, built at boot, parked outside the screens); pairing
   screens carry invisible `.pslot` boxes that declare geometry, and the runtime
   moves the single element with a transform. Verified: one `.phero`, **zero
   `.rnd` elements**, same node throughout pairing. It sits below the screens on
   purpose — node 9's light and nodes 10-11's phone must be in front.
2. **The 1px-stroke buttons had their states inverted.** Default was the dim
   translucent fill and hover brightened it; a raised control is brightest at
   rest (LAW 3) and pressing should darken. Fixed in all three places that
   style them.
3. **Node 14 removed** — node 12 hands straight to node 15. ⚠ It was the only
   screen for typing a Wi-Fi password, so a stale saved credential now has no
   normal correction path, only the `W2E` edge state. `NODES` is 22 and the
   assertion states the reason.
4. **Node 15 has no CTA**: the bar fills over ten seconds and the screen hands
   itself on, carousel running. That kills the last instance of the pattern the
   2026-08-06 rebuild called the most dishonest here — a visible wait with a
   skip button under it. One CSS transition, not a per-frame loop.
5. **Engraved icons are a third register** —
   `design-elements/engraved-icons/` with manifest + README, mirrored to the
   Vercel design system as its own folder (`renderNomaEngraved`). Node 16's
   drawn tick and node 25's drawn bell are replaced; the bell keeps its rings
   and swing, now animating the glyph.
6. **Node 18a**: key card 0.8×, R3C deleted, sharing raises a "Key shared"
   toast and the CTA becomes Continue — without that the flow dead-ends, since
   R3C was the way onward.

⚠ **Three losses worth naming.** The icon gate's "two tiers" is now wrong as
written and a folder does not get to fix a rule by existing. The notifications
glyph carries `#FF4444`, outside the palette, where `red.mid` is the token for
exactly this. And R3C carried the ROSTER — pending invites now have no
representation in first run at all.

**A verification note.** `wireLoad` first used `requestAnimationFrame`, and
headless Chrome never fires it — the bar read 0% forever and looked broken.
Rewritten as a single CSS transition, which is both testable and smoother.

---

## 2026-08-18 (5) — The jerk between pages, and node 18a becomes a real picker

**The "jerk and lag" was a corrupted measurement, not a performance problem.**
The carry decision was made inside the wiring, after the incoming screen was
already in the DOM with `.scr.in` applied. Measuring forces a style recalc, so
every rect was read while the slide's `translateX(10px)` was still on the
parent: every FLIP began 10px out and snapped at the end. `carryClass()` now
reads the markup BEFORE the element exists, so a carrying screen never gets a
transform. Nothing was slow — the geometry was wrong.

**The carry is generic now**, keyed by `data-carry`: `pur` (the purifier
through pairing), `bg` (the sign-in photo, so nodes 1-3 stop re-rendering it),
and `sheet` — which is the other half of the reported jerk. The sign-in sheet
was replaying its 880ms arrival on EVERY step; it now rises once out of the
splash and changes height in place after that. `[data-carried]` suppresses the
replay, so the one place the rise is wanted still has it. Heavy data-URI
backgrounds are decoded at boot (`warmAssets`) instead of mid-transition.

Verified: S0→A1 carries `bg`, A2/A3 carry `bg`+`sheet`, P1→P2→P2B→P3→P4 all
carry `pur` with the class `carry` (no slide), and the FLIP out of node 6
starts at scale 0.3061 on BOTH axes — proof the aspect-true sizing means the
artwork never distorts.

**Node 13's list gained a lock and a signal meter** — a drawn padlock and four
ascending bars, lit per network (4/3/2). SVG, not divs: the harness scales the
phone and at that scale CSS gaps between 3px divs fell under a pixel and the
meter rendered as one solid triangle. ⚠ Still tight at review scale; it reads
at 1×, which is what ships, and that is the honest claim.

**Node 18a is a real picker** (owner reference): contacts become removable
pills, the list drops whoever is picked so the two halves cannot disagree, and
the CTA counts — "Share key" → "Share key (1)" → "Share keys (2)". The key
card is tilted and bleeds off the right.

⚠ **The body dropped "you decide what each key opens."** Better, in that the
promise was never implementable — the per-invite disclosure was removed
2026-08-06 and never replaced — but the GAP is unchanged and now invisible on
the screen.
⚠ **Hue-coded avatars are back**, reversing the 2026-08-12 palette rule exactly
as node 6's tiles did. Three CSS rules to revert.
⚠ The reference labels Ayush Tiwari "AK"; initials are computed (AT). A wrong
initial on a screen for telling people apart is a typo, not a style.

Three fixture surnames joined the M-06 proper-noun allowlist.

---

## 2026-08-18 (4) — Scan pages merged, and the white flash between screens is gone

1. **Scanning and picking are one screen each** (owner reference). Node 11 was
   "scanning over Bluetooth" + "select your device"; node 13 was "fetching
   Wi-Fi" + "select Wi-Fi". Each pair is now a single page: a large owner-
   supplied glyph, the ask, then a live list where the count climbs from `(0)`
   and results arrive in place. Two screens shorter — 44 → 42, 31 → 29 on the
   happy path, still all 23 nodes. Rows ship in the markup and are revealed by
   the runtime, so the board and the export still show the list contents.
2. **The white flash between screens is fixed.** The harness removed the
   outgoing screen BEFORE appending the incoming one, so for at least one frame
   the phone held no screen and its bare ground showed through. The new screen
   is appended first and the old one fades out beneath it — never a frame
   without content. Patched in all three mount functions (prototype, flow,
   export) and verified structurally: mid-transition the DOM holds two screens,
   one marked `.out`, and settles back to one.
3. **The two glyphs are vendored** at `design-elements/glyphs/` as data URIs
   rather than inlined markup — both carry Figma `filter0_di_…` /
   `paint0_linear_…` ids that would collide the moment two screens shared the
   DOM, which after (2) is every transition.
4. **Node 12/13 order and ids.** The merge took node 12's fetch half into node
   13's screen, so the sequence now runs 13 → 12 and what survives as node 12
   is the confirm step. With §5.16 this is the second change to weaken
   auto-fetch; PRD §5.17 says so plainly rather than re-arguing it.

⚠ **Node 11 lost Identify.** The reference deliberately shows two
identically-named purifiers — the day-one case for a household that bought a
pair — and "make this one blink" was the only thing that distinguished them.
Signal strength is not enough. Flagged in the screen note and PRD §5.17.

**A third class collision, and the lesson is now written down.** The scan list
was invisible in every render while the JS reported it working. Two causes,
stacked: `.scan` is already the QR-viewfinder component (inheriting
`height:190px; display:grid`), and the completion state `.done` is
build-auth.py's sign-in end card at `position:absolute; display:none` — so
finishing the scan deleted it. Renamed to `.slist` / `.slist--done`. Found by
enumerating `document.styleSheets` for every `display:none` rule the element
matched, rather than by reading CSS. **State classes get a component prefix
from here on.**

**Six helpers are now unused** (`doorway`, `peel`, `holdring`, the three tour
illustrations, `v_scan`, `spin`, `v_wifi`), each retired by an owner decision
with its reasoning in a §5 entry. Inventoried in build-prototype.py beside the
sequence, to be deleted at hand-off.

---

## 2026-08-18 (3) — The chosen purifier is carried through pairing

1. **Pick a SKU on node 6 and it travels.** Not five pictures of a purifier —
   ONE element FLIPped between per-screen geometries (measure where it was,
   measure where it landed, start at the old rect, fly to the new). Node 6's
   tile → node 7's filter scene → node 8's socket → node 9 at its largest →
   nodes 10-11 smaller as the phone arrives. `PICK` survives navigation, so a
   500 stays a 500 with its own silhouette and its own light position.
   ⚠ Carrying screens get NO screen-level slide (`.scr.carry`): a translating
   parent would drag the hero and fight the FLIP. The purifier flies;
   everything else fades in behind it.
   ⚠ Renders are now sized by HEIGHT with their true `aspect-ratio`. Each SKU
   has different proportions, so a fixed box letterboxed differently per SKU
   and the carried size jumped between screens.
2. **Node 9's light is on the device.** Each SKU's indicator position was
   measured off its render rather than guessed (`--ledy`: the 200 at 39.7% of
   its height, the 500 at 19.2%, the MAX at 19.8%) and the glow is pinned to
   it. Verified per SKU: MAX lands at 20%, the 200 at 40%.
3. **Node 10-11's phone dissolves downward** via `mask-image` instead of
   ending in a hard bordered edge — the bezel and shadow fade with the
   content rather than outliving it.
4. **W1 moved before P7B** (owner). Order is now P7 → W1 → P7B → W2: fetch,
   pick, confirm the pre-filled password, with typing it yourself as the
   escape. ⚠ This weakens node 12's own argument — it existed to make picking
   from a list unnecessary, and the list is now on the happy path. Its copy no
   longer claims to have saved the trouble; PRD §5.16 records the tension and
   the shape that would restore it.

**Two bugs found by measuring rather than looking, both invisible in a
screenshot.** `--ledy` was declared on the render, but the glow and the bar are
its SIBLINGS and custom properties only inherit downward — the light was
landing off the device (-10% for the MAX). And `.ledp` was full-height, so
`top: 19.8%` was a percentage of the visual half rather than of the purifier;
`width/height: fit-content` makes the container exactly the device's box,
because absolutely-positioned children contribute nothing to grid sizing.

**A verification note that keeps biting.** Headless Chrome does not tick
animations, so a running FLIP freezes the hero at its START rect — the first
measurement pass reported every screen's hero one screen behind and looked like
a real bug. `getAnimations().forEach(a => a.finish())` before measuring resting
geometry, and `a.pause(); a.currentTime = t` to screenshot a live keyframe.

---

## 2026-08-18 (2) — A5 condensed, the Bluetooth screen redrawn to animate, a real bell

1. **Node 5's sheet is condensed** — 453px (54% of the screen) down to 389px
   (46%). The single biggest win was the UA's own default `h1`
   margin-block-start: 0.67em of a 30px title is 20px of dead space nobody
   wrote and nobody could see in the source.
2. **Nodes 10-11's Bluetooth screen is REDRAWN, not embedded.** The supplied
   PNG was a flat screenshot and could not animate; the owner asked to see the
   switch actually turn on. It is markup now, so the toggle flips grey → green,
   the knob slides, and the caption plus the device rows arrive once Bluetooth
   is on, on a 5.4s loop. It depicts iOS and carries iOS's colours (#007AFF,
   #34C759) — the same licence `dialog()` already takes for the OS's own
   prompts. `bt-phone.png` stays vendored but is now unused by the flow.
3. **Node 25's bell is rebuilt as one SVG silhouette** with three rings pulsing
   out of it, a swing on the loop, and a `status.negative` badge. The first
   attempt stacked white boxes on a near-white ground and read as a blob —
   drawn silhouettes read, soft-shadowed white rectangles do not.
4. **`--neg` is now a real token path.** build-prototype.py gained a `--neg`
   var (red.mid, which the token file marks safe as a fill) and build-flow.py
   drives it from `status.negative`. ⚠ While wiring it I found a **stale
   comment in build-flow.py's re-skin claiming "the 2026-08-12 palette has no
   red"** — untrue since 2026-08-13, when the owner supplied one. The 13 edge
   screens were rendering their error colour as ink for that reason; they now
   carry `status.negative` properly. Warning stays ink: O-6 is still half-open
   and a "filter at 10%" nudge is not a fault.

**Two verification notes worth keeping.** Headless Chrome does not tick CSS
animations — `getAnimations()[0].currentTime` sits at 0 while the document
timeline advances — so screenshots taken under `--virtual-time-budget` show
frame zero and silently look "broken". Every animation above was instead
verified by pinning `currentTime` through the Web Animations API and shooting
real keyframes. And the phone mock's device rows were genuinely missing at
first: the scene had a `min-height` taller than its container, and `.pgt`
clips overflow, so the rows were laid out correctly and cut off.

`audit-voice.py` gained three iOS Settings strings ("Not Connected", "My Apple
Watch", "Now discoverable") to the M-06 exemption — the OS's own words, the
same case §1.2 already grants the permission dialogs.

---

## 2026-08-18 — Fine-tweaks: Bluetooth scene, condensed sheets, pairing animations, hold-to-pair removed

Four owner notes, all verified in headless Chrome rather than by eye:

1. **Nodes 10-11's Bluetooth scene is real** — owner-supplied iPhone
   Bluetooth-settings mock (`design-elements/renders/bt-phone.png` + web
   webp), composed per the owner's reference: render upper-left, phone
   lower-right in front. Nothing drawn remains in that scene.
2. **Node 4's card sits 20px lower** (owner: "18 or 24, you make that call")
   — 70px total top inset, balancing the card between the nav title and the
   NAME field.
3. **The sign-in sheets are condensed** — every vertical gap stepped one to
   two stops down the spacing ramp, OTP boxes 56×52 → 52×46, the Apple text
   button 56 → 44. Measured after: A1 342px (41% of the screen), A2 308px
   (37%), A3 343px (41%) — roughly 0.85× their previous height. ⚠ The owner
   asked for ~0.6-0.7×; the remaining distance is the 56pt CTA and the 30pt
   display title, both tokens. Shrinking those is an owner call, not a trim.
4. **Nodes 7 and 8 animate.** The polybag slides off the cartridge and drifts
   away on a loop — the bag became its own element precisely so it can leave —
   and the socket's rocker flips before the power light blooms on over the
   render's own LED. Both loop gently; both collapse under reduced motion.
5. **Hold-to-pair is gone.** Node 11's closer is a pairing page built on the
   owner's NoiseFit structural reference — device left, phone right, dots
   travelling the line, then the check and "Connected", then it advances by
   itself. The 2026-08-06 honesty argument (holding = staying near) survives
   in a different form: the wait resolves ITSELF, there is no button to skip
   it, and the stay-near instruction moved into the copy. PRD §5.9's gesture
   row is struck through with the reasoning; `holdring()` joins `doorway()`
   and `peel()` as defined-but-unused.

⚠ **A bad scripted edit briefly nested this changelog inside itself** (a
replace expression that evaluated to the whole file). Caught by the
double-header count and repaired by reconstructing the original from the
duplicated halves — noted because the repair touched every line of this file
in the diff, and that should not read as a rewrite.

---

## 2026-08-17 — First run nodes 1–5 rebuilt as a bottom-sheet flow

Owner supplied seven frames and asked for the first five steps to be replaced
with a bottom-sheet sign-in. Built `docs/features/first-run/build-auth.py` →
`auth-prototype.html`: six states (splash · login sheet · mobile number ·
mobile OTP · email · email OTP) on one full-bleed image, with a floating sheet
that changes height and contents rather than five pages replacing each other.

**What it is.** A working prototype, not a board — you type a real number,
real digits auto-render into the boxes, Proceed enables on ten digits and on
four digits and on an address that parses, the resend countdown actually runs
and turns into a Resend button, and the address you type is echoed on node 5
and editable in place. Every state is addressable (`#A3`), which is how the
screenshots were taken and how a reviewer links one.

**Generated from tokens, like every other harness here.** Colour, radius,
shadow, type and — new for this file — motion all come from
`src/tokens/*.tokens.js` through the same node import. Not one raw hex,
duration or bezier in the source; the only `ms` literal is the `.01ms` inside
the mandatory `prefers-reduced-motion` block, which is that gate's own
spelling. Motion gates 1, 2 and 3 checked by grep: the sheet arrives on
`springBold`, content leaves on `exit` and enters on `spring`, the wordmark
fades out on `exit`.

**Two measurements the frames settle that the token set did not.** The sheet
floats 16pt off all four edges rather than docking to the bottom, and its
inner padding is 12, not `layout.screenPaddingX` — a sheet inset from the
screen cannot also carry the screen's padding or everything creeps inward.
Both are noted at the top of the CSS block.

**The background is a drawn placeholder and says so.** `bg_plate()` draws the
reference photograph's composition — arch, stair flight, two soft foreground
crops — out of the neutral ramp. The build prints which background it used,
and dropping `docs/features/first-run/assets/first-run-bg.jpg` replaces it with
no code change. Same convention as the illustration plates in
`build-onboarding.py`: composition-correct, art-direction-wrong on purpose.

**Four spec changes came in with the frames, all flagged in PRD §5.11 rather
than absorbed quietly.** Node 4 stopped collecting a display name (so nothing
in first run collects one, and invite-family is downstream of it); the DPDP
notice moved to the login sheet's fine print, which moves where §5.1's answer
has to land; the country selector is gone and +91 is hardcoded; and node 5
verifies with a code instead of waiting for a link. Two smaller things were
reproduced exactly rather than corrected, per the instruction: the mobile OTP
state still carries the *"What's your mobile number?"* heading over a code
field, and nothing between nodes 2 and 4 has a way back.

**Two deliberate divergences from the frames**, both flagged:
`Edit email` is `colors.text.accent` (mintDeep) rather than the frames'
brighter green, which is outside the 2026-08-12 palette and would not clear AA
as text; and the *"We've sent an OTP to …"* line wraps to two lines where the
frames show one, because Google Sans Flex sets that string wider than the mock
did. Shrinking real copy below the type scale to make one fixture address fit
would have been the worse trade.

**Follow-up, same day — the sheet ground is now its own token.** Owner supplied
the exact Figma layer stack for the sign-in sheet (`#F9F9F9` flat base, a
linear white→`neutral.300` overlay at 24%) and asked for it on "the
bottomsheet." That is a new `gradients.sheet` entry, not a hand-edit of
`build-auth.py` — CLAUDE.md rule 4 — and `recipes.bottomSheet.background` now
points at it instead of `gradients.canvas`, which it had been borrowing.
**Deliberately not the same value as `canvas`:** a sheet floating over a photo
wants to stay close to white; the page's own ground gradient is tuned for
sitting directly under content and reads too heavy layered on top of an image.
`recipes.bottomSheet` had exactly one consumer (`build-auth.py`) at the time of
this change, so nothing else needed re-checking. Verified live: the sheet
recomputed to `linear-gradient(#FAFAFA 0%, #F4F4F3 50%, #EEEEEC 100%)` after
the token edit with no change to the build script.

**Follow-up, same day — the real wordmark replaced the CSS text stand-in.**
Owner supplied the actual NOMA logo. New folder,
[`design-elements/brand/`](../design-elements/brand/), following the exact
convention `3d-icons/` set: a source PNG (transparent, cropped tight to
content with air around it), a `web/*.webp` derivative for embedding, a
`manifest.json`, and a README with provenance and a replace-it recipe.
`recipes.layout` gained `wordmarkSplash`/`wordmarkSheet` (116 / 84) so the
display width is a token, same reasoning as `iconHeaderSize`. `build-auth.py`
now embeds the real mark at both call sites (splash, login sheet) and falls
back to the old letter-spaced text if the asset is ever missing — a missing
asset degrades, it does not fail the build, same convention as `icon3d()`'s
placeholder.

⚠ **Provenance note, because the image never reached disk as a normal
attachment.** The owner pasted the logo into chat; as with the 3D icons on
2026-08-14, no available tool extracts a pasted image's raw bytes to
the filesystem. It was located instead at a file already saved locally,
`~/Downloads/Noma/Noma Logo 2.png` (1500×1500, transparent) — verified
pixel-identical to what was pasted before use. A second, larger export sat
alongside it (`~/Downloads/Noma Logo.png`, 14000×8000, flattened to white, no
alpha) and was deliberately not used — same mark, wrong format for a UI asset.

⚠ **Not swapped everywhere the word "NOMA" appears.** The older 45-screen
flow's node-1 door screen (`build-prototype.py` → `first-run-prototype.html`
/ `first-run-flow.html`) still renders the mark as heavily-tuned CSS text —
left alone on purpose, flagged in the folder README as an owner call rather
than done silently, since that screen's choreography was tuned over several
passes documented earlier in this file and swapping in an image there is a
real edit to it, not a drop-in.

**Follow-up, same day — the drawn placeholder background was replaced with
the real photo.** Owner supplied an architectural render (pitched-roof house,
foggy sky, lit doorway, reflecting pool) for the sign-in splash and login
screens. Same provenance situation as the wordmark: pasted into chat, located
instead at `~/Downloads/Noma/BG.png` and verified pixel-identical before use.
Flattened onto white (the source's ~0.4% of non-opaque pixels read as export
noise, not intentional transparency) and re-encoded as JPEG at
`docs/features/first-run/assets/first-run-bg.jpg` (126 KB) — the exact swap
point `build-auth.py` already had wired up from when it built the drawn
placeholder, so **no code change was needed**, only the file drop and a
rebuild. `bg_plate()` (the drawn composition) stays in the file as the
fallback if the real asset ever goes missing, same convention as `icon3d()`'s
placeholder. Verified across all six states in-browser; re-generated
`auth-flow-sheet.png`. `docs/features/first-run/assets/README.md` carries the
full provenance and the replace-it recipe.

**Follow-up, same day — the arrival was slowed, and the two halves of first
run were merged into one walkable file.** Two owner notes: the login sheet
"is too fast… make it slower and more premium", and merge the sign-in with
the rest of onboarding.

**The arrival is now a sequence rather than a slide.** Four changes, all
token-driven: the splash holds 1600 -> 2600ms; the background settles out of
`scale.breathe` over `durations.ambient` so the extra beat is not an empty
one; the wordmark fades up on `entrance`; and the sheet rises over 880ms with
a decelerating curve instead of 480ms with an 80% overshoot, its contents
staggering in behind it at `stagger.list`. Only the FIRST arrival is slow —
every later state change keeps the quick fast/base swap, because staggering a
form step reads as sluggish rather than considered. Measured in-browser rather
than eyeballed: the sheet travels y=357 -> 153 -> 60 -> 25 -> 9 -> 3 -> 1 -> 0
over ~800ms and never crosses zero, which is the no-overshoot settle the curve
promises.

⚠ **This added two motion tokens and one of them breaks an ADR.**
`durations.entrance` (880) and `easings.entrance` (a no-overshoot expo-out).
**ADR-005 resolved O-7 in favour of playful overshoot on discrete moments, and
this is the one place the product is now not springy** — flagged in the token
file with a TODO(owner), not smuggled: an 80% overshoot scaled up to an 880ms
hero arrival reads as a cartoon, not a welcome. ADR-005's rule still holds
everywhere it was written for. Send it back to springBold/480 if that call
goes the other way; it is a two-value edit.

**Follow-up, same day — real renders in the flow, and the resident's key.**
Two owner drops, both vendored and wired:

1. **The household key is the RESIDENT'S KEY artwork, used as is.** No name,
   no initials, no avatar — the owner is explicit that it is not personalised.
   `design-elements/brand/resident-key.png` (+ web webp), replacing the
   composited member card on nodes 18a. The master key stays personal; this
   one is generic, which is what makes it sendable. Copy follows: "a
   resident's key of their own".
2. **The three SKU renders replace the drawn purifier** —
   `design-elements/renders/` (new folder, README + provenance), embedded as
   CSS variables so all four flow renderings inherit them. Node 6's chooser
   thumbnails now carry the real 200/500/MAX (three genuinely different
   shapes, which is the at-a-glance signal the 2026-08-12 monochrome rule had
   cost); node 7 shows the drawn cartridge lifting out of the real render;
   nodes 8 and 10-11 swap the drawn body for the render inside their existing
   scenes. Node 9's Wi-Fi light stays drawn — owner: fine as is. Sources are
   5-32 MB originals; the repo keeps 1200px working copies.

**One silent override found and removed:** `build-flow.py`'s re-skin layer was
re-tinting node 6's tiles into the 2026-08-12 two-green depth ramp, overriding
the hue-coded tiles the owner's node-6 frame specifies — so the published flow
had never actually shown the frame's tints. The re-skin now passes the base
tints through, and the palette conflict lives in exactly one flag (the
screen's note) instead of a hidden reversal.

Simulate buttons were also removed this session (owner: "remove all the
simulate buttons") — all 10 calls plus the helper and its CSS. The edge
states stay reachable from the review rail and by hash; A3E, A4E, A5E, P6E,
W4E and R3E are now rail/hash-only, which the wireframes builder reports as
orphans. That is the tool being accurate.

**Follow-up, same day — the key travels: keys for the household, and a door to
finish.** Three owner directions in one message, all built and verified:

1. **Node 4's card sits 24px lower** — at 1.2x it was clipping the floating
   "Setup profile" title.
2. **Node 18a sends key cards, not invites.** The blank member card (same
   artwork, smaller, static — theirs to fill in on their own phone) sits in the
   visual half; the sent state shows it carrying Lakshmi's name. Copy moved to
   the key register ("Who else needs a key?"). ⚠ The per-invite disclosure gap
   from 2026-08-06 gets louder under this metaphor: "you decide what each key
   opens" is now said on the screen and decidable nowhere. R3's keyboard mock
   came off — the card owns the visual half.
3. **The tour is gone and the flow ends at a door.** C1/C2/C3 removed (44
   screens, 31 on the happy path, still 23 nodes — D1 carries node 23). What
   went with them is itemised in PRD §5.14: the privacy receipt, the agent's
   introduction, and the only roadmap mention. `D1` is a closed door, the
   beige lock from the owner's reference, and the key card made on node 4 —
   drag it to the lock, tap it (it glides itself), or press Enter; the LED
   flares, the lever turns, the door swings on light, and Home is behind it.
   Reduced motion goes straight through. The card carries the name and picture
   typed on node 4 — verified, not assumed. Deliberate symmetry: node 1's
   drag-to-open door was removed the same morning; it returns at the end, and
   this time you hold the key.

**One real bug found by testing the drag rather than watching it:** the
harness scales the phone to fit the viewport, so pointer deltas arrive in
screen space while the card's transform applies in local space — the card
moved at half the finger's speed and the tap-glide stopped short of the lock.
`wireDoorKey` now divides by the live phone scale. Also `setPointerCapture`
throws on synthetic pointers; it is now guarded and ordered so a throw cannot
strand the drag state.

⚠ `A4E` / `A5E` are now orphan states (rail- and hash-reachable only) — the
direct consequence of the owner removing the simulate buttons from nodes 4
and 5. The wireframes builder reports it; that is the tool being accurate.

**Follow-up, same day — the sheet stops at phone verification, and node 4 is
the master key.** Owner direction plus two frames: the bottom sheet now covers
nodes 1-3 only; node 4 became a full page, *Setup profile*, built around a card
that is the profile AND the key to the home. Node 5 followed it out of the
sheet and is a page in the standard structure.

**Everything on the card is bound to the two fields under it** — name, email,
the avatar's initials, and a serif initial top right — and what is typed
survives leaving the screen and coming back. The avatar takes a real picture
off disk (FileReader; nothing leaves the page). The artwork is the owner's PNG
used as the base and written over: the bevel, grain, rule and key glyph are all
in the image and nothing redraws them. Positions are percentages of the card,
measured off the frame, so it scales as one object.

**The flow harness is genuinely interactive now.** `field()` rendered a span
with a fake caret — it looked right and could not be typed into. It is a real
input across all four renderings, and node 5's code boxes take real digits.
Verified by driving a copy in headless Chrome rather than by eye: typing a name
updates the card, initials go AS/A for "Asha Sharma" and P/P for "Priya", an
empty name degrades to a placeholder instead of throwing, a round trip through
another screen preserves everything, and the Wi-Fi password field accepts text.

**Refined the same day, four owner notes:** the harness's simulate buttons
came off nodes 4 and 5 (they are review affordances and the card is the
subject); the card grew 1.2x with its content inset a further 1.1x from the
edges; the "this is your key" line was sitting straight on top of the CTA and
now has real space under it; and **node 5 became a sheet OVER node 4** rather
than a page of its own — the profile page stays behind it, dimmed, so the card
you have just filled in is still there while you confirm the address written on
it. Verified: the name typed on node 4 is still on the card behind the scrim.

⚠ **THE DISPLAY NAME IS BACK**, closing the hole this session opened in the
morning: PRD §5.11 had recorded that nothing in first run collected the name
the household sees, with invite-family downstream of it. Node 4 collects it.

⚠ **Instrument Serif is vendored for exactly one glyph** (SIL OFL, licence
beside it). Not a second body face; a second serif use is an ADR-001 decision.

**Two real bugs found by checking rather than by eye.** The component-dispatch
list was duplicated in three renderings, so wiring node 4's card in one of them
silently did nothing in the other two — that is now one exported `WIRE_JS` the
three mount functions interpolate. And `.link` / `.cta` / `.otp` collided with
build-prototype.py components: scoping raised specificity only for the
properties the new rules DECLARE, so "Edit email" was inheriting
`position:absolute; left:24px; top:50%` from an unrelated pairing component.
Namespaced to `.s-link` / `.s-cta` / `.s-otp`, then re-checked until clean.

**`build-first-run.py` and `first-run-complete.html` are deleted.** They merged
the sheet with the 11-screen spine — the wrong flow, corrected earlier the same
day — and once the sheet lost A4/A5 that builder silently produced a flow that
skipped the profile page entirely. The canonical merge lives in
build-prototype.py and reaches all four renderings; a third variant would only
drift. Removed from the voice-gate targets with it.

**One copy deviation from the frame:** it reads "Setup Profile"; built as
"Setup profile", because M-06 is sentence case and machine-checked. `Royce` was
added to the audit's proper-noun allowlist — it is the fixture user's surname,
a false positive rather than a loosened gate.

**Follow-up, same day — the whole flow was re-laid-out to a bottom-aligned page
structure.** Four more owner frames (nodes 6-9) set it, with the instruction to
apply it to the rest of first run: a circular back arrow floating over a visual
that takes the leftover height, then eyebrow / title / body / CTA pinned to the
bottom. All 46 screens now share it, driven by three new primitives in
`build-prototype.py` (`pgt`, `pgb`, `eyb`) and a `.scr:has(.pgb)` switch, so
converting a screen is a local edit and an unconverted one keeps the old
padding untouched.

Node 9's Wi-Fi indicator is drawn properly rather than stood in for — a
blinking capsule inside its own bloom, which is the one frame visual that is a
light rather than a product render. The rest still use the existing CSS
drawings; re-arting them remains the known gap.

⚠ **Four deliberate losses, each flagged in PRD §5.12 rather than absorbed:**
the close (×) is gone from every pairing screen, taking the exit-setup hatch
with it; the 4-dot setup stepper is gone; **node 7's peel gesture is gone**
(the 2026-08-06 build made the polybag something you physically dragged off,
precisely because that instruction gets skimmed — `peel()` is still defined and
unused); and node 9's hold-to-reset recovery moved from a note on the screen to
a *"Not blinking?"* link, which routes to P3F so the content survives one tap
away.

⚠ **Secondary actions dropped from full-size buttons to text links**, and on
the two permission asks that is the change worth arguing about. "Not now" was a
`recipes.buttonQuiet` button on nodes 24 and 25 *because* declining has to stay
first-class; it is a grey link now. The flow continues identically either way —
it just no longer looks like a real choice.

⚠ **The frames reintroduce hue-coded SKU thumbnails** (blue / teal / olive),
which the 2026-08-12 palette rule had deleted in favour of depth within one
green family. Built as supplied because it is the newer instruction, flagged
because both are owner instructions. Reverting is three CSS rules.

**One copy deviation from a frame, and it was the gate's call:** node 6 reads
"Mid Sized homes"; built as "Mid-sized homes". M-06 (sentence case) is
machine-checked and the capital S failed it, while both sibling rows are
sentence case — so the frame is a typo rather than a style call. The frame's
shortening was kept; only the casing moved.

⚠ **CORRECTION, same day — the first merge went into the wrong flow.**
`first-run-complete.html` (below) joined the sheet to `onboarding-prototype.html`, the
**11-screen visual spine**. The owner meant the **45-screen flow** published at
`noise-apps.vercel.app/#noma/userflows/first-run`, which is a mirror of
`first-run-flow.html` — a different artefact with different screens, edge
states and a different harness. Verified by reading the dashboard's own
route table (`dashboard/dashboard.js`, `FLOWS_BY_APP.noma.exploration`)
rather than by guessing, since the Vercel host is blocked from the browser
tool here; the served file is byte-identical to this repo's copy.

**The real merge: `build-prototype.py` now imports nodes 1-5 from
`build-auth.py`.** That file is the canonical screen set behind ALL FOUR
renderings — the tappable prototype, the 45-screen flow, the flat board and
the clean export — so the new sign-in lands in every one of them from a single
edit, which is what rule 2 asks for. 45 → 46 screens, 32 → 33 on the happy
path; the node count is still 23, because the splash and the login sheet are
two halves of node 1 the way a screen and the OS dialog over it are. The
Vercel mirror and the dashboard's own screen-count metadata were re-synced.

⚠ **The drag-to-open door is gone.** Node 1 was `doorway()`, rebuilt four
times on 2026-08-06 and documented across PRD §5.10 and §5.10a-c — the door
you pulled open on warm light. Replaced on owner instruction, not because it
failed. The function is still defined and now unused, so putting it back is
one line; the four PRD sections are kept for the reasoning but no longer
describe what is built.

⚠ **Three edge states are EXTRAPOLATED.** `A3E` / `A4E` / `A5E` had no owner
frame — every supplied frame is happy path — but leaving them would have
dropped the flow back into the old full-screen language mid-run. They are
drawn in the sheet using `status.negative` and marked as extrapolated in
their own notes and in the PRD. `A4E` lost something real: the old version
offered "sign in with that one instead", which is the useful action, and a
second CTA changes the sheet's button hierarchy — flagged, not guessed.

**Two class collisions were found by checking rather than by eye**, and both
were live bugs. `.link`, `.cta` and `.otp` already exist in
`build-prototype.py` as unrelated components; scoping build-auth.py's rules
under `.sheet` raised specificity for the properties they *declare* but left
the old rules' other properties applying — "Edit email" was inheriting
`position:absolute; left:24px; top:50%` from a pairing component and sitting
7px out. Fixed by namespacing the three to `.s-link` / `.s-cta` / `.s-otp`,
then re-running the check until it reported none. Whack-a-mole resets would
have hidden it rather than fixed it.

**`first-run-complete.html` is the whole flow in one file** — six sheet states
(nodes 1-5) into nine setup screens (nodes 6-23), fifteen states, one rail,
built by `build-first-run.py`. **It defines no screens of its own.** Both
source builders were split into named CSS and JS parts so the merged one
composes them live: onboarding's chrome + auth's background + auth's sheet +
onboarding's screens, and auth's runtime with a new `route()` hook for the
ids it does not own. Editing either source builder updates the merged flow.
The alternative — copying ~100 lines of proven OTP/countdown/input logic into
a third file — is exactly the drift `_phone_fit.py`'s docstring exists to warn
about. Auth's component CSS is now scoped under `.sheet` so `.cta`, `.field`,
`.otp` and `.iconbtn` cannot collide with the screens' versions; both source
prototypes were re-verified after the split, and `onboarding-prototype.html`
is byte-identical apart from whitespace at the split points.

Three rewires, held as data in the merged builder and asserted at build time
(a rewire whose target string vanishes fails the build rather than silently
becoming a no-op): A5's CTA `DONE -> P1`, P1's back arrow `A3 -> A5`, and C1's
CTA `A2 -> END`. That middle one mattered: P1's back pointed at `A3`, which
still resolves — to the NEW sheet OTP — so it would have looked fine while
sending the user two nodes too far back.

⚠ **The merge makes an old conflict concrete for the first time: C-14.**
Walking it end to end, nodes 1-5 are photographic, greyscale and warm; nodes
6-23 are white with green-gradient illustration plates. They do not read as
one product, and the seam is exactly at P1. Nothing was changed to hide it —
this is the clearest evidence yet for the palette decision that has been open
since 2026-08-12, and it is worth looking at the strip in
`first-run-complete-sheet.png` before deciding.

**The voice gate now covers this surface, and two of its rules were touched.**
`audit-voice.py` gained the new file as a target; `note` was added to
`HARNESS_KEYS` (it is the rail's review chrome, the same thing `build-flow.py`
spells `notes` — its sibling key `inner`, which carries the product copy, is
deliberately still audited); and `Apple`, `Service`, `Policy` were added to
the M-06 proper-noun allowlist. Apple's HIG specifies *"Continue with Apple"*
verbatim, and the other two are titles of documents rather than descriptions
of them. One real M-03 violation was found and fixed — an em dash in the
hand-off screen, which is copy this repo wrote, not copy from the frames. All
six surfaces are machine-clean; the human read-aloud gate is still owed.

---

## 2026-08-14 (2) — 3D icon set scaffolded: info, appearance, notifications, family

Owner supplied four 3D-rendered icons (info, appearance, notifications,
family) and asked for a `design-elements/3d-icons/` folder registered in the
design system. Built the folder, `manifest.json`, and README following the
bottom-sheets/bottom-nav convention — but **the four image files are not in
it.**

⚠ **The images arrived pasted directly into chat, not as file paths.** No
available tool extracts a pasted image's raw bytes to the filesystem — it
can be viewed, not saved. So this is a scaffold: manifest, README, and index
entries exist and name the four icons precisely, but the folder holds zero
image files. `design-elements/3d-icons/README.md` has the "how to finish
this" instructions (drop the four PNGs in with the exact filenames the
manifest already specifies).

**This also names a real two-tier icon system** for the first time in a
committed file, following the "Level 1 3D / Level 2 flat" split raised in
conversation on 2026-08-13:

  · Tier 1 (3D) — this folder. Higher-visibility, higher-importance moments.
  · Tier 2 (flat) — already running code: the 22-icon `ICONS` dict in
    `docs/features/settings/_kit.py` and its twin in `build-onboarding.py`.
    Never formally registered in the design-system gate before this entry,
    which the new "Icon set" section in `design-system.md` also flags.

⚠ **The owner's four names override an earlier draft split, on purpose, not
by mistake.** `notifications` and `appearance` were tentatively tier-2 flat
in the 2026-08-13 conversation (`bell` and `palette` already exist as flat
icons for those exact rows). The 2026-08-14 direction promotes both to tier
1. Where a flat and a 3D icon now both exist for the same settings row,
which one actually ships is an open call, tracked in `manifest.json`'s
`conflict` fields — not decided here.

**One more open question, not resolved:** `appearance.png` (a painted
palette) and `notifications.png` (a red badge) carry real-world colours
outside the 2026-08-12 product palette rule (white, grey, the two greens
only — LAW 2). Whether that rule constrains a photographic/3D icon
rendering a real object, versus governing only the product's own drawn
surfaces, is an owner call flagged in the folder README rather than assumed
either way.

**Gate discipline held rather than being waived for convenience:**
`design-elements/README.md`'s own rule is "a folder existing here is not the
gate, a row [in design-system.md's Approved Components] is." 3D Icons got an
index row (for visibility — the gap is tracked, not silent) but explicitly
NOT an Approved Components row, because there is nothing yet to open and
check. That's a different kind of incomplete than the SwiftUI bottom-nav
package (which builds but has never run) — this folder has no asset to even
attempt opening.

**Not verified, because there is nothing to verify yet.** No image opened,
no dimension checked, no format decided. All three are named as immediate
next steps once the files exist.

## 2026-08-14 — Voice Guide v1.2 installed, machine gate built, every surface swept

Owner supplied `noma-voice-guide.md` v1.2-draft. Installed at the canonical path
the document names for itself, `docs/voice/noma-voice-guide.md`, and applied.

**The gate is the deliverable, not the sweep.** §12 marks seven rules ⚙ for CI,
and D-4 argues explicitly for a gate over a one-time rewrite, citing an
onboarding round that found live em dashes in "a surface believed shipped".
`docs/voice/audit-voice.py` implements §12 items 1-6 and exits non-zero, so it
can run in CI. It audits ONLY what the person reads: text inside the `.phone`
frame. Review rails, design notes, docstrings and CSS are writing *about* the
product and are deliberately out of scope.

⚠ **The first version of the gate reported the two biggest surfaces clean, and
was wrong.** `first-run-flow.html` (45 screens) and `my-home-prototype.html`
render every screen from an embedded JSON fixture at runtime, so a static
`.phone` pass saw an empty frame. Extended to walk embedded JSON too. A gate
that silently passes the largest surfaces is worse than no gate.

**Then the opposite failure.** With JSON walking on, it reported 180 violations,
68 of which were review chrome: my-home's `JOBS`/`LABELS` (the rail's own state
descriptions) and build-flow's `notes`/`titles` keys. Excluded by name after
reading each one. False positives are how a gate gets switched off.

**Findings and fixes, 85 real violations to zero:**

| Rule | Count | What it was |
|---|---|---|
| M-03 em dash | 41 | Banned everywhere. Split to full stops per the §10.2 pattern. |
| M-06 sentence case | 19 | Preset values mostly: "Living Room" → "Living room", "Pooja Room" → "Pooja room", "Silent Mode", "Light Intensity", "City / Town". The corrections bank lists this row verbatim. |
| W-01 AQI indoors | 18 | The substantive one. See below. |
| §5.2 / M-04 / M-11 | 7 | "urgent" in the alarm family, two clefts, one semicolon. |

**W-01 deserves its own note, because it is the one place this risked inventing
data (R-17).** Indoor readings must be PM2.5 in µg/m³, never AQI. Where the
fixture already carried both ("AQI 22 · 6 µg/m³") the AQI half was simply
dropped. Where only an AQI number existed, converting it to PM2.5 would have
been fabricating a reading, so instead:

  · `pm25=dict(label="PM2.5", unit="AQI")` was an outright contradiction in the
    my-home fixture and became `unit="µg/m³"`.
  · Unpaired indoor numbers were RELABELLED, not converted, and only where the
    result stays internally consistent: the room holds 24 and its series runs
    19-24, so "7h 11m under AQI 30" → "under 30 µg/m³" agrees with its own data.
  · "What AQI actually measures" is a legal use of AQI (the public outdoor
    index, W-01) but did not say so, and became "What the outdoor AQI actually
    measures".
  · The device rows' "73 AQI"/"41 AQI" were relabelled to µg/m³. ⚠ These are
    PROTOTYPE FIXTURE values, not sensor output. Real values must come from the
    device; nothing here should be read as a measurement.

**Gold-standard lines taken verbatim from the guide** rather than paraphrased:
§11.3's removal note, §10.1's "First, how do I reach you?", §11.5's "It's back
in" button, and §11.3's "When the air turns / I'll tell you when PM2.5 climbs
into the unhealthy range" replacing "Air quality drops / When AQI crosses into
Poor". "Air quality alerts" → "Air alerts", which §11.3 calls out as an honesty
fix rather than a warmth one.

**M-17 caught one real bug on the way past:** the household count rendered
`{people} People`, which reads "1 people" on a one-person home. Now generates
singular and plural.

**Repository wiring:** CLAUDE.md routes to the guide and to the gate.
`memory/voice/tone-matrix.md` and `glossary.md` are now pointers, not copies,
and say what actually changed (two dials not one; families not words).
`docs/voice/voice-prd.md` carries a SUPERSEDED banner naming the three things
that moved, and is kept because the old §-numbers appear in commit history and
the new R-/M-/W- IDs do not map onto them.

⚠ **This is NOT "the surfaces pass the voice", and the gate says so in its own
output.** §0.1 rule 5 forbids that claim from an audit alone. The machine gate
is clean. The human gate (§12 items 8-19, read aloud) has not been run, and
Sahil and Kaustubh are the arbiters. Nothing here was read aloud by a person.

**Not implemented, deliberately:** M-18 (character limits) needs D-7's published
per-surface numbers. Inventing limits would violate R-17 inside the tool built
to enforce it.

**Verified:** all five surfaces machine-clean, all prototypes rebuilt, my-home
renders its six states with no console errors, no superseded hexes or copy left.

## 2026-08-12 (6) — New green palette, the 10% rule back, and shape dynamics

Three owner directions in one session, each superseding part of the last. Newest first
inside the entry, because the later ones changed the earlier ones.

**The palette (owner image, three swatches + three ramps).** `lime #AECC2A`,
`mint #6CCC7C`, `haze #E9E8E5`, and the rule that outside white and grey **only these two
greens and shades of them** are used. This replaces the `#1D6B27→#3DBE4E` ramp from
entry (3) entirely — that ramp was four days old and is now gone.

⚠ **The finding that changed a rule: this is an INK-ON-GREEN system.** Measured, both
anchors are far too light to carry white text — lime + white = **1.83:1**, mint + white =
**1.99:1**. Against near-black they are excellent (7.43 and 6.85). So LAW 2 gained a
corollary — *white text never goes on green, anywhere, at any size* — and
`colors.accent.onFill` flipped from white to near-black. The Insurance Card flipped with
it, which **simplified** it: the old card needed its gradient locked to one angle so white
text stayed over the dark end, and `textSafeZone` is gone because ink is legible anywhere
on it.

The three supplied ramps are in verbatim: `gradients.accentRamp` (mint→lime, the
signature), `limeWash` and `mintWash` (each fading to haze). Added `gradients.gloss` — a
white hairline along the top edge of raised surfaces; that one line is most of what
separates "glossy" from "editorial".

**LAW 6 — the 10% rule — reinstated** at owner request, after entry (3) had replaced it
with "green means the system is doing something". It immediately caught a real breach: the
onboarding hero plate was ~16% solid green. The supplied washes fade to the neutral for
exactly this reason, so plates now go green at the top and white by halfway.

**Shape dynamics (owner sheet, X/O pairs + two Figma inspectors).** The through-line is a
three-layer finish — white INSIDE stroke, drop shadow, and an **inner** shadow — now a
single `effects` export (`chiclet` / `chicletSelected` / `tintPill`) rather than a habit
retyped per component. Any one layer alone reads wrong: drop shadow is flat, inner shadow
is pressed-in, stroke is an outline.
  · **Chiclets are radius 8, not pills** [INSPECTOR]. Bigger shapes got rounder and small
    ones got *tighter* — the opposite of a blanket "make it rounder", which is why the two
    radii are specified apart. A pill reads as a filter you switch off; a soft rectangle
    reads as a tile you pick from a set.
  · **"Help" is a tinted pill** — `#8BCC6D @ 24%`, white inside stroke 1.53, drop + inner
    shadow. `#8BCC6D` sits at hue ~100°, between lime (~73°) and mint (~134°), so it is a
    legal shade of the family and not a fourth colour.
  · **Toggle** 51×31 → 58×34, knob 26 → 28. **Meter** segments 4×14 → 5×20 with a 4pt gap,
    inside a white pill — at the old size they read as texture, at this size as counted
    units, which is the point of a segmented meter.
  · `radius.xs` 10 → **8**; the old 10 was only the progress track, now a full pill.

**Earlier in the same session, still standing:** `radius.sm` 12 [INSPECTOR] and new recipes
`cardSelect` / `cardSelectIdle` (radius 12, padding 16, gap 20 — selection is LIFT, never a
tick or a coloured border), `illustration` (radius 24, **8pt** white frame — the frame is
the whole effect), `buttonQuiet` ("Not now" at the CTA's exact height), `segmented`
(lift, not an ink fill — ink is this system's action colour and a filled segment reads as
a button when it is only reporting state).

**New prototypes**, all generated from the token module through node, none restating a
value: `docs/features/settings/` split into **two surfaces that must not be merged** —
`profile-settings` (home-scoped) and `device-settings` (one purifier, IA transcribed from
`PurSettingsBody` in the PM prototype), sharing `_kit.py` so they cannot drift;
`docs/features/first-run/onboarding-prototype.html` (11-screen visual spine); and
`first-run-flow.html` — **all 45 screens**, controller rail left, phone right, generated
from `build-prototype.py` per that file's own "one screen set, many renderings" rule.

⚠ **TWO OPEN DECISIONS THE PALETTE CREATED, both flagged in code, neither resolved:**
1. **There is no red any more.** Destructive rows ("Remove this home" / "Remove device")
   and all **13 edge screens** in the flow lost `--err`/`--warn` and now read in ink.
   That is a real degradation on every failure state in the product. Either allow one
   non-palette red for destructive only (what the owner's own PM prototype does with
   `#FF3B30`), or put destructive behind a confirm sheet so the second tap carries the
   weight instead of the colour. This also makes **O-6 harder, not easier** — the same
   argument now blocks warning and critical too.
2. **Two places lost a signal to the monochrome rule.** The three SKU thumbnails were
   blue/teal/amber to separate the sizes at a glance, and the household avatars were four
   hues; both are now depth within one hue, which is weaker. Probably wants real product
   renders and photos rather than tints.

**Still un-migrated, deliberately not faked:** the 45-screen harness's `.viz` illustrations
are the old outline SVGs. The new hero is a gradient plate in an 8pt white frame, and line
art cannot be turned into that with a stylesheet. Checked for a CSS hook — `.scene` covers
only 9 pairing screens and not L1 — so re-arting is a real design task.

**Verified:** all 45 flow screens render with zero console errors; every generated
prototype audited programmatically for off-palette hue (none survive); token module
re-imported through node after every change.

## 2026-08-12 (5) — Bottom Navigation Bar is live on the Vercel dashboard

Owner: "do whatever it takes to get the navigation bar on Vercel." Full detail lives in
`noise-design/noiseFit`'s own `memory/changelog.md` (per rule 2, not duplicated here) —
this entry exists so this repo's history shows the component didn't stop at registration.

**What actually happened there:** while working, discovered that repo's `main` had moved
independently — Bottom Sheets had already graduated to a real, embedded dashboard folder
(iframe, phone-framed, live). This component got the exact same treatment:
`design/noma/bottom-nav/` (index.html, preview.html, README), wired into NOMA's Design
pillar as an 8th folder, matching the `phone-stage`/`X_BASE`/`renderNomaX` pattern the
sheets folder set. The "Approved, not yet embedded" text-registry that a concurrent
change had briefly added there is now gone — once its one entry graduated, an empty list
wasn't worth keeping.

**This repo's own README updated to match** — `design-elements/bottom-nav/README.md` now
says plainly that the noiseFit copy is a **trimmed gallery variant**, not a byte-copy: no
internal phone chrome, no measurement panel, both stripped to match the convention Bottom
Sheets already established there. The two should agree on behaviour, not markup.

**Verified as far as the login gate allows, no further** — same constraint as the last
pass. The dashboard's own SPA shell is still behind a password the coding agent correctly
won't enter. What *was* verified: the new files are static, reachable directly under
`/design/`, with no login involved — navigated there directly and confirmed in-browser
that scroll-shrink, tap-to-select, and the pill travel all work exactly as built, no
console errors.

---

## 2026-08-12 (4) — Tokens fix synced onward to noiseFit/Vercel

Continuation of the fix below (this same day) — see 2026-08-12 (3) for the fix itself.
Owner asked to bring the Vercel-deployed dashboard (`noise-design/noiseFit`) up to date too.

Re-synced `src/noma/noma.tokens.js` there from commit `bb61642` (below) and added a
Components folder to NOMA's Design pillar — Bottom Sheets + Bottom Navigation Bar,
mirroring the Approved Components gate populated in 2026-08-12 (2). Full detail lives in
**that repo's own** `memory/changelog.md` and `memory/session-handoff.md` — not duplicated
here, per rule 2 (one canonical home per fact); this entry exists so anyone reading this
repo's history knows the fix didn't stop at this commit.

Pushed to `noise-design/noiseFit` branch `noma/sync-tokens-and-components`, not merged.
**One thing that repo's own handoff flags and this one should too:** the new Components
folder was never checked visually — its login gate correctly blocked password entry at the
tool-permission level, cosmetic or not. Someone with the password needs to look at it once
before that branch merges.

Also added a `noisefit-dashboard` entry to `.claude/launch.json` here, pointing at
`localhost:4175` — used to import-check the synced module in-browser without needing that
login. Same "attach to a URL you start yourself" pattern the two existing entries already use.

---

## 2026-08-12 (3) — Design tokens: fix green.deep accessibility failure, add missing recipes

Closes drift between this file and its two mirrors (noiseFit dashboard, `memory/` markdown)
rather than adding new design direction — surfaced by the noiseFit sync above, fixed here,
upstream, first.

`green.deep` corrected `#1E8A2E` → `#1D6B27`. The original measured only 4.44:1 contrast
under white text (fails WCAG AA) despite looking like the safest, darkest stop on the
ramp — hue and lightness don't move together linearly, so "looks darker" isn't a substitute
for computing it. Re-verified with the shared relative-luminance formula; `deep` now clears
AA with real margin (6.59:1). noiseFit's mirror already carried this fixed value from an
earlier, undocumented hand-patch; this commit is what makes that value legitimately
canonical instead of the mirror being ahead of its own source of truth.

Also adds four recipes that existed nowhere in committed history: `cardSelect` /
`cardSelectIdle` (the "which one did you bring home?" selection row — LAW 3, lift not
colour, chevron only on the selected row), the framed onboarding illustration (8px inside
white stroke, tilted -2°), `buttonQuiet` (the CTA's declined-path twin, same height/radius so
the pair reads as one group), and `segmented` (a sunken-track control with a raised pill,
corrected against the owner's source prototype which fills the selected segment with ink —
ink is this system's ACTION colour, so filling it implies a tap where the control only
reports current state). Also splits `radius.xs` (10, small inline marks) from `radius.sm`
(12, selection rows/thumbnails) — these had been one value; the selection row above needs 12
specifically.

Verified: `node --check` on the file and on noiseFit's re-synced mirror both pass; the mirror
imports cleanly in-browser with every new field resolving, and `dashboard.js` has no
reference to any of the changed field names, so nothing there could throw against the new
shape.

---

## 2026-08-12 (2) — Design system: Approved Components gate populated for the first time

Owner asked to "push this into the design system as Bottom Navigation Bar." That gate —
`.claude/rules/design-system.md`'s "approved components" line — had **never actually been
populated**, for either component that already exists here: Bottom Sheets went straight into
`design-elements/` on 2026-08-11 with no entry anywhere else, and the Bottom Navigation Bar
(below) landed the same way earlier today. `memory/index.md`'s Design table had no row for
components at all. So this wasn't "register one thing" — it was the first real use of a rule
that had sat as a stub since the rules file was created, and leaving Bottom Sheets out of a
now-populated registry would have made the registry itself misleading on day one.

**Four things now exist that didn't this morning:**

1. `design-elements/README.md` — top-level index, both components, explicit about the two
   *not* being at the same maturity (Bottom Sheets and the nav bar's HTML preview are
   browser-verified; the nav bar's SwiftUI package builds but has never run — the index says
   so rather than presenting one checkmark for both).
2. `.claude/rules/design-system.md` — an "Approved Components" table, the gate's first real
   content. Everything else in that file is still a stub; only this one gate moved.
3. `memory/index.md` — new Design-table row pointing at the gate and the index.
4. `design-elements/bottom-nav/README.md` retitled from "Bottom navigation — minimizable
   floating tab bar (SwiftUI)" to **Bottom Navigation Bar**, the owner's formal name, with a
   registered-in banner and a corrected file tree — it never mentioned `index.html`, which by
   this point was the component's more-verified half.

**One thing surfaced while touching the README that had nothing to do with registration:** its
"How it was derived" / "Deliberate divergence" sections describe the SwiftUI package's
original geometry (66pt tabs, content-sized pill). `index.html` was revised twice since (16px
inset left/right/bottom, uniform 0.8× scale floor) and the SwiftUI package was never ported to
match. The README now says explicitly which half it's describing rather than letting the two
implementations silently disagree under one document. **The SwiftUI package still needs that
port** — noted here so it isn't lost, not done as part of this pass since it wasn't asked for.

**Not done, on purpose:** no `git commit`/`push` — "push into the design system" read as
"register/integrate," not a literal git operation, and commits happen only when asked. No new
`templates/component-registration.md` — `design-elements/README.md` flags the gap (rule 5
covers events/personas/features/motion patterns, not components) but doesn't resolve it; that
precedent was already set by Bottom Sheets having no template either, so this doesn't newly
break anything, it just makes the existing gap visible at the moment it matters.

---

## 2026-08-12 (1) — Bottom navigation: minimizable floating tab bar (SwiftUI)

`design-elements/bottom-nav/` — a rebuild of the tab bar from Kavsoft's
[Instagram App's Minimizable Tab Bar Using SwiftUI](https://www.youtube.com/watch?v=691o2FUDs-8),
skinned with NOMA tokens. Owner supplied the video and a demo clip and asked for an exact
recreation. **This is the repo's first native code** — everything before it was markdown,
tokens, or static-HTML prototypes.

**Two corrections to the brief, both recorded because they change what was built:**

1. **It is not an "AI-based navigation bar."** There is no AI in it. It is the iOS 26/27
   Liquid Glass tab-bar pattern.
2. **It does not collapse.** Across all 26s of the reference the bar never reduces to a
   single icon and never leaves the screen — width contracts and glyphs tighten, nothing
   more. Apple's native `.tabBarMinimizeBehavior(.onScrollDown)` *does* collapse to a
   single-icon pill and is **not** what the reference shows. That is why this is a custom
   bar rather than four lines of system modifier, and why it targets iOS 18 rather than 26.

**How it was derived.** The tutorial's source was not available and video cannot be read
directly, so the reference clip was stepped frame by frame in a browser — 26 seconds sampled
at 18 points and composited into a contact sheet. Three behaviours were legible enough to
rebuild: the floating pill inset from the screen edges with content scrolling underneath; a
selection blob that lifts off the bar and travels to the tapped tab (caught mid-flight at
6.0s and 7.5s); and shrink-on-scroll-down / expand-on-scroll-up. **The geometry numbers are
a reading, not a measurement** — the recording zooms during playback, so only the ratios
were preserved (minimized ≈ ¾ the width, glyphs ≈ ⅘ the size). Tune against a device.

**Deliberate divergence, one.** In the video the selected pill is a slightly *darker* grey
than the bar. LAW 3 says the opposite — white means raised, selection is lift not colour,
and the token file calls a colour-only selection a bug. So the pill is white and raised on a
translucent grey bar. Reverting to literal video fidelity is one line, but it is a C-14
palette decision rather than a code preference.

**Palette:** light greyscale, owner's call this session against the three live C-14
directions. No green is referenced anywhere in the package; under LAW 2 none would have been
legal anyway.

**Tabs are provisional** — home / device / automation / profile, per owner instruction,
pending a real IA. Ids are stable so they can carry analytics later. Four `nav.*.label` keys
added to `src/i18n/locales/en/common.json` (the bar is icon-only, so those keys are the only
name a VoiceOver user gets). **Hindi deliberately left unwritten** — `hi/common.json` now
says why: the conversational rewrite raised the transcreation bar, and ADR-001 O-5 means
Google Sans Flex cannot render Devanagari even once written. Four guessed transliterations
would have looked like the work was done.

**Verified:** `swift build` clean under Swift 6 language mode with strict concurrency; motion
gates 1 and 3 by grep; gate 2 in substance (every animating file routes through
`NomaMotion.resolve`). **Not verified, and the README says so in a table:** never executed,
never rendered once, SF Symbol names asserted from the catalogue rather than compiled against
an iOS SDK. There is no Xcode on this machine, only Command Line Tools — which is also why
`Demo/` holds the `@main` entry and the `#Preview` blocks (the preview macro needs an
Xcode-only compiler plugin).

**One new open item, O-10 — an accessibility gate that silently does not fire.** Motion gate
2 requires every animating file to contain `prefers-reduced-motion`, which is a CSS media
query no Swift file can hold; the grep therefore reports clean exactly where it has no
coverage. Not worked around — a dead CSS string in a Swift comment would make the gate pass
while making it meaningless. Gate 1 has the same shape of hole. Needs an owner because it
edits an enforced rule.

Two pre-existing gaps this component runs into, both already tracked: **`colors.status` is
`null`** (O-6), so a tab cannot carry a badge or attention state — the moment Home wants to
signal a filter due, this bar has nothing to draw with; and **there is no spring-physics
token**, so the pill's travel is a cubic-bezier with ~10% overshoot rather than simulated
physics. It reads correctly; the reference's blob looks genuinely simulated.

---

## 2026-08-07 (2) — Voice PRD generalized app-wide; renamed off "onboarding"

Owner direction: the conversational register shouldn't be onboarding-only — the whole app
should ask questions, talk about the house, and read as a housemate rather than a wizard
anywhere it has something to say. Two changes:

**Removed every mention of the app the tonality work had been benchmarked against**, per a
separate owner request — swept all `.md`/`.py`/`.html` files in the repo, not just the PDF,
and rewrote §1–§2's reasoning as our own design logic rather than an extraction from a named
source. Rebuilt and re-verified: zero mentions remain anywhere, same eleven pages, same
substance.

**Generalized the PRD's scope from onboarding to the whole app.** Renamed
`onboarding-voice-{prd.md,PRD.pdf,print.html}` → `voice-prd.md` / `NOMA-Voice-PRD.pdf` /
`voice-print.html` — cheap to do while the document is a day old, expensive to leave
misnamed once other surfaces depend on it. Updated every cross-reference across
`changelog.md`, `session-handoff.md`, `tone-matrix.md`, `glossary.md`, `ai-personas.md`,
`docs/index.md` and `first-run/prd.md`.

Added new §13, "Where this applies beyond onboarding" (old §13 Cross-references is now §14):
reconciles this document with `ai-personas.md` (that one's a superset for Home/notifications
specifically — night-hook/morning-proof, the share-caption exception — this one is
sufficient everywhere else), and a live surface-by-surface status table. As of today:
onboarding rewritten and shipped; Home/notifications already in-register via
`ai-personas.md`; **My Home not yet touched** — `docs/features/my-home/build-home.py`'s copy
predates this voice; Sharing/Automations/Shop/Settings have no prototype yet to rewrite.

⚠ **The table is a status check, not a todo list someone else owns.** Explicit note in the
doc: a surface isn't in this voice because someone believes it is, it's in this voice because
a specific shipped line can be pointed at — same standard §10 already holds onboarding to.

Verified: PDF rebuilds to 11 pages (one more table, same page count), all renamed paths
resolve, zero dangling references to the old filenames repo-wide.

---

## 2026-08-07 (1) — Voice & Tone PRD, typeset and PDF'd

Owner asked for the voice work formalized as a document: a PRD on tonality that says what the
app should and shouldn't say. Built as a matched pair —
`docs/voice/voice-prd.md` (canonical markdown) and
`docs/voice/NOMA-Voice-PRD.pdf` (typeset, 11 pages) — using the same design system as
`docs/prd/NOMA-v1-PRD.pdf` (A4, Google Sans Flex, moss/warm palette), rendered the same way
(headless Chrome `--print-to-pdf`). One difference worth keeping: fonts are embedded as
base64 data URIs rather than the original's relative path, which points at a file
(`src/noma-fonts/google-sans-flex-subset.woff2`) that does not exist in this repo — that PDF
may have silently fallen back to a system font. This one cannot.

Thirteen sections: why this exists, what makes a setup flow feel like a conversation rather
than a wizard, the seven rules (each checked against an already-shipped NOMA line, not
aspirational), who's speaking (flags `C-2` formally — every "I" is a product
decision, not a copy one), grammar mechanics, a banned/approved vocabulary table (now
canonical for `glossary.md`), tone by moment (now canonical for `tone-matrix.md`), what stays
deliberately literal (physical instructions, system dialogs), error rules, the actual
before/after rewrite (ten real screens), localization (flags the Hindi transcreation cost),
and an eight-question ship checklist.

**Both prior stubs now point here rather than staying empty**, per CLAUDE.md rule 2 (one
canonical home per fact): `memory/voice/tone-matrix.md`'s onboarding row and
`memory/voice/glossary.md`'s banned-words list are both this document now, with a note on
what's still unfilled (persona-by-persona variation in the matrix; language-by-term
translation in the glossary — both separate axes this PRD doesn't cover). Also cross-linked
from `memory/voice/ai-personas.md`, the existing ongoing-product voice doc this one extends
backward into onboarding.

Verified: PDF renders 11 pages, cover/TOC/sections/tables/callouts all match the sibling
PRD's visual system, fonts render correctly (embedded, not linked).

---

## 2026-08-06 (12) — The voice: rewritten from wizard to housemate

Owner brief: the copy read like instructions, and should read like a conversation about your
home. Distilled seven rules, now written into PRD §8.1 each with a shipped NOMA line as
evidence:

first person singular · ask-then-say-why in the subtitle · take the anxiety out of the answer
· "let's" for shared work · privacy as a concrete negative · warm buttons at warm moments ·
observation → offer → ask.

The observation → offer → ask sequence is the load-bearing structural idea: name what you
noticed, offer to help with the specific thing noticed, and only then ask for what's needed —
in first person, using the person's name if you have it.

**Every screen rewritten**, 50 strings across all 32 path screens and 13 edge states. The
register is now a housemate rather than a setup wizard: *"Which one did you bring home?"*,
*"Now find it a socket"*, *"Anywhere near where it'll live"*, *"That's the hard part done"*,
*"What I learn stays here"*. The email is *"a spare key"*.

**Two things deliberately left literal**, and this is the judgement worth recording:
- **The instruction inside an instruction screen.** The frame is warm, the step is not. Node 7
  (unwrap the filter) and node 9 (blinking light) are physical and success-critical — node 7
  in particular is the one failure that is completely invisible. Charm there costs
  comprehension.
- **System dialogs** keep Apple's register. A chatty permission sheet reads as a fake one.

⚠ **Adopting "I" is a product decision, not a copy decision.** The app now speaks in first
person from screen one, before the agent has been introduced. That matches
`ai-integration.md`, which already specifies a first-person agent — but **`C-2` is open**, so
whether "I" is the product or a separately-named assistant is undecided. If they are different
characters, every "I" here needs re-attribution. Resolve C-2 before these become i18n keys.

⚠ **The translation bar went up.** "A spare key", "hum away happily", "already spoken for" are
idioms; literal Hindi will read as broken. This needs transcreation, not translation — noted
in §8.

Also caught and fixed in passing: node 10's two halves had drifted apart (the system-prompt
screen still carried the old headline while the priming screen had the new one).

Verified: no screen overflows after the rewrite; all 32 path screens dumped and read end to
end; builds clean in all three renderings.

---

## 2026-08-06 (11) — Node 1: light behind the door, progressive slider, white dissolve restored

Three owner corrections.

**No dark shadow may exist near the door.** It had a dark drop shadow and a dark contact
shadow, which read as *the space beyond is dark* — the opposite of the story the door tells.
Replaced with a white halo carrying the faintest green cast, plus light pooling on the floor
in front of the doorway; the leaf's outer shadow is now white. Both halo and pool **brighten
with the drag**, so more light escapes as the leaf cracks. The only dark values left on the
door are an `inset` face shading (what makes it a panel and not a rectangle) and a 1px edge.

**The green arrives with the thumb.** Track fill and both labels are driven straight off
`--p`: at 50% dragged the track is 50% green and "Enter Home"/"Entering Now…" are mid
cross-fade. Measured 0/.25/.5/.75/1 → 0/.25/.5/.75/1. Before, the green state was binary and
fired only on commit — the drag itself had no feedback until it was already over.

**The white dissolve is back, and now it cannot be lost.** It disappeared last pass because
the white layer lived *inside* `.scr`, which `render()` destroys at the hand-off — the layer
vanished at precisely the moment it was doing its job. It now lives on **`.phone`**, so it
survives the swap and the next screen emerges out of the white instead of sliding in under
it. Measured: copy/slider at zero by ~560ms, doorway owns the viewport ~1400ms, pure white
~1680ms, hand-off 1700ms, dissolve done ~2500ms.

Two things that cost real debugging and are worth carrying:
- The veil needs a **forced reflow** (`void veil.offsetHeight`) between append and class
  flip. A rAF is not enough: the browser coalesces both into one style pass, no transition
  runs, and the veil snaps to white on frame one — hiding the entire door sequence. Caught by
  sampling opacity every 300ms and seeing it pinned at 1 from t=300.
- Removal is scheduled **at creation, untracked, as a hard backstop**, and any pre-existing
  veil is cleared before a new one is made. A stranded veil is an opaque white page with no
  way back — which is exactly what the first attempt produced when the hand-off was
  interrupted. Verified against a deliberately interrupted entry: 0 veils, 0 leaks.

---

## 2026-08-06 (10) — Node 1: corridor rebuilt as one SVG; placement measured to the reference

Two owner corrections, both structural rather than cosmetic.

**"The door is floating, the walls are not connected."** The corridor was five
CSS-transformed `<span>`s (rotateY walls, rotateX ceiling/floor). Separately rasterised
planes cannot be made to meet — the joins showed hairlines and the doorway read as pasted in
front of the wall rather than set into it. It is now **one SVG in a 390×844 viewBox where
adjacent surfaces share corner coordinates**, so a gap is not expressible. The aperture's
four points (`128,158 → 262,394`) are the same four points every plane terminates on. Added
a contact shadow at the door base. The bottom corners belong to the **walls**, not the floor
— that is what gives the reference its bright central path with grey outer corners.

**"The placement is very low."** Measured off the reference and matched to within 0.1%:
door 18.7→46.7%, NOMA centre 69.5%, body centre 75.9%, slider 85.1→91.4%, 20px side margins.
Copy and slider now sit absolutely positioned *over* the scene rather than stacked under it,
because in the reference the floor runs behind the text to the bottom of the screen.

**Exit is white-on-white**, as asked. Sampled every 220ms: copy and slider hit zero opacity
by ~500ms — before the travel is really moving — the scaled aperture owns the viewport by
~1540ms, flash completes ~1760ms, handover at 1700ms. Nothing of screen one is visible when
screen two arrives.

Also switched the travel from `translateZ` to `scale` about the aperture centre. Same
apparent motion, and it sidesteps the perspective-culling trap recorded in entry (9)
entirely — nothing moves in Z, so nothing can cross the camera.

Verified: every screen still fits; the full pointer drag enters and lands on A2 with the
label reading "Entering Now…"; tap and Enter still complete; reduced motion goes instantly;
zero leaked timers; identical in prototype and export.

---

## 2026-08-06 (9) — Node 1, third pass: the owner's mock, followed rather than interpreted

The owner supplied a four-frame mock and the correction "we are not going inside the door."
Both taken literally this time:

**To the mock:** rectangular white door with a black pill handle (the arch is gone),
straight-walled corridor in the mock's neutrals, **NOMA** wordmark letterspaced over
"A calmer kind of smart home.", full-width slide track labelled **Enter Home** with a dark
round knob — and while entering, the label becomes **Entering Now…** over a green fill.

**The walk-through, staged:** ① leaf swings fully open (~0.8s) → ② the camera travels
THROUGH the frame, the pure-white interior growing until it swallows the viewport (1.25s,
overlapping) → ③ only then does the flash finish and the next screen arrive out of the same
white. The previous version whited out before the travel read as travel — that was the
complaint, and the staging is the fix.

**One rendering bug worth remembering:** the first cut travelled to z=1150px against a 640px
perspective. Past the perspective distance the browser culls the plane — the scene vanished
and the beige page background blinked through for ~0.2s before the flash. Caught by running
the sequence at 1/20th speed and screenshotting mid-travel. Fix: cap the travel at z=600px,
just under the camera; measured at rest the interior still overshoots every phone edge by
~900px. If this ever gets ported, that constraint (travel < perspective) is the one
non-obvious thing to carry.

⚠ **The green entering-state is from the owner's mock** and contradicts the standing
"no green in this file" direction (2026-08-05). Used as supplied; folded into C-14 rather
than resolved silently. It is currently the only green in first run.

Verified: no overflow anywhere; the full pointer-drag enters (label reads "Entering Now…",
lands on A2); tap and Enter still work; reduced motion goes instantly; zero leaked timers;
same checks pass in prototype and export.

---

## 2026-08-06 (8) — Node 1 rebuilt as a threshold; room recentred; tour slides animated

Second pass on the interaction work, against the owner's reference (the Finvu "unlock
wealth" portico sequence) and two specific defects.

**Node 1 is now a threshold you cross.** Structure taken from the reference, subject ours:
scene on the top ~60%, headline + one line of body, and a **slide-to-unlock track** at the
foot. The slider scrubs the approach — drag and the camera creeps toward the door, the leaf
cracks, the light behind widens. Complete it and the frame rushes past the viewer, the leaf
swings wide, the room whites out, and we are inside.

Why this beats the first attempt: a handle only reads as a handle once you have noticed it.
A track with a knob and an arrow is the most legible "do this" affordance on a phone, and it
leaves room for the headline and body. **Commit threshold set to 62%, not 82%** — caught in
testing: a drag that ran out of track at 81% snapped back, which would read as the app
refusing a gesture the user completed.

**Node 17's drawing was framed by nothing.** The viewBox was `0 0 320 210` — a box picked
before the art existed — so the room sat high and the kitchen fridge, the tallest object and
on the far grid corner, clipped off the top. Recomputed from actual content bounds
(x 43…277, y −12…142.5) to `9 -25 302 180`. Verified across all six rooms *after the morph
settles*: every one now clears the stage top and bottom. Kitchen is tightest at 2px, which is
correct — the fridge is supposed to be the thing that nearly touches.

**Node 23's three slides animate the claim instead of illustrating it.** Were static CSS
shapes at 250px; now 298px of pure CSS/SVG keyframes — no JS, so nothing to wire in two
builders and nothing to leak:
- *Your data stays home* — seven readings drift inside the house outline and never cross it,
  the boundary breathes, and exactly one thing comes **in**: the outdoor air that
  `ai-integration.md` §10 names as the sole exception. The narrowing is drawn, not asserted.
- *It runs itself* — specks drawn in from every edge, orb pulsing, clean rings pushed back
  out, two receipts ticking. The only thing never touched is the thing doing the work.
- *One app, whole home* — one hub, four devices, wires drawing in turn; the three that are
  not the purifier are faint, matching the honesty node 6 now enforces by omission.

Verified: no screen in any of the three renderings overflows; no dangling links; the slide
completes and enters in both prototype and export; all six room morphs clear the stage; the
privacy slide renders 7 drifting dots, the agent slide 6 specks, the home slide 4 wires; zero
leaked timers, timeouts or rAF handles after navigating away.

⚠ Unchanged reservation: **this is prototype code.** The timings and the feel are the
deliverable. Port the behaviour, not the CSS.

---

## 2026-08-06 (7) — The interaction layer: five nodes stop being forms

Owner verdict on the flow so far: *"too boring, too mundane… this is going to be our main
attraction point."* Correct. Every node was a headline, a graphic and a pill button —
structurally right and completely inert. Five nodes now carry a real gesture:

| Node | Gesture |
|---|---|
| 1 · Get started | **Drag the handle; the door swings open on warm light.** It is a *home* app — you do not tap "Get started" to enter a house. |
| 7 · Unwrap the filter | **Drag the tab; the polybag peels off.** The one setup failure that is completely invisible became the only thing on screen you must touch. |
| 11 · Pair | **Press and hold; the ring fills.** Replaces a fake progress bar with a Next button under it — the most dishonest pattern in any prototype. Releasing early drains the ring, teaching the requirement with no error state. |
| 17 · Which room | **Tap a room; the isometric drawing morphs into it.** The centrepiece. |
| 26 · Home | **The AQI counts up from zero.** The first number should arrive, not merely be present. |

**Node 17 is the one that matters.** Six rooms on a horizontal selector, one isometric
drawing below that morphs — four furniture slots interpolating position, footprint, height
and tone simultaneously, so bed → sofa → kitchen counter. Slot count fixed at four so
nothing ever pops in or out; depth order recomputed every frame because pieces genuinely
swap front-to-back mid-morph. Crossfading would say "here is a different picture"; morphing
says "this is the same room and you are deciding what it is" — which is the actual decision.

**Three rules held throughout, and they are not negotiable:**
1. **The gesture is the delight, never the toll gate.** Every one also completes on a plain
   tap and on Enter/Space (all are `<button>`s). Node 11 treats a sub-180ms press as
   tap-to-complete. A flow advanceable only by dragging excludes switch and keyboard users.
2. **`prefers-reduced-motion` collapses each to an instant state change** (motion gate 2).
3. **Spring only where the rules allow it.** Room morph uses easeOutBack — choosing a room
   is a discrete moment, and the motion rules open by asking for playful there. The Home
   count-up is an ambient reading, so `standard`, no overshoot (gate 4).

**Structural fix, same lesson as the flat board.** The interaction JS is now `RUNTIME_JS`, a
single shared string in `build-prototype.py` embedded verbatim by both the prototype and the
export. The export previously carried a hand-copied `wireCarousel`/`wireCounter`; had that
stood, node 1's door would have been dead on arrival in the export — an unopenable door on
the first screen of the file we send to stakeholders. One runtime, two hosts; the only
contract is that the host defines `go(target)`.

⚠ **Still flat:** nodes 2–5 (the account run) are four consecutive form screens with no
moment in them, and node 8 is a static illustration of a physical act. If the
"main attraction" bar applies to the whole flow, the account run is furthest from meeting it.

⚠ **Do not port this JavaScript.** The gestures are proven to feel right; the code is
CSS/SVG/rAF written to survive a review, not a design-system contribution. Port the
behaviour, with real tokens.

Verified: all 45 screens fit with no overflow; no dangling links; a synthesized pointer drag
opens the door and advances; the peel tracks 47%→95% and completes; hold fills 540→325 over
600ms and drains on early release; a sub-180ms tap on hold completes and advances; the room
morph redraws 12 polygons per frame and the selector auto-scrolls; count-up reaches 34;
zero leaked intervals, timeouts or rAF handles after navigating away from every interactive
screen; the same checks pass in the export.

---

## 2026-08-06 (6) — Clean prototype export

New artefact: `docs/features/first-run/first-run-export.html`, built by
`build-export.py`. One phone, centred, tappable, and nothing else — no controller rail, no
node numbers, no per-screen design notes, no simulate buttons. The file to hand to someone
who should *experience* the flow; the harness stays the file for reviewing it.

Generated from `build-prototype.py` like the flat board is, so there are now **three
renderings of one screen set** and a flow change still only happens in one place.

⚠ **One honest limitation, stated in the file's own docstring.** Stripping the `sim` buttons
removed the only path to most edge states, so in the export the 13 error states are
unreachable by tapping. They are still in the file and still addressable by hash
(`…#W2E`), so they can be demoed deliberately — but nobody clicking through will see them.
Do not treat this file as evidence the error states exist; that is the harness's job.

Verified: all 32 path screens render and fit; zero harness residue in the DOM (`.sim`,
`.ctrl`, `.meta`, `.jump` all absent); the carousel still runs and its timer clears on
navigation; a tap-only walk reaches Home (correctly skipping the Wi-Fi fallback screens,
since auto-fetch succeeds); hash deep-link to `W2E` lands on the right screen.

---

## 2026-08-06 (5) — Permissions moved to just after connect; tour lands on Home

Owner reorder. The tail is now:

    16 connected → 24 location → 25 notifications
       → 17 create home → 18 name device → 18a invite → 23 about ×3 → 26 home

Both OS prompts previously sat at the very end, separated from the device working by four
naming and household screens. They now fire as one block at the flow's strongest moment —
"connected" is the only unambiguous win in the whole sequence, so asking there is asking
from strength. It also stops a modal landing in the middle of the naming/household run,
which is one coherent task. And node 23 (the three about-the-app slides) now lands straight
on Home rather than routing through the permissions.

**Node ids are unchanged and therefore no longer ascend.** 16 → 24 → 25 → 17 is deliberate,
as is the 19–22 gap. Keeping the ids stable is what lets every earlier note, PRD reference
and conversation ("node 15", "node 6") still resolve. The harness readout was changed to
match: it now prints `Node 24 · step 17/22` rather than the nonsensical "Node 24 of 22".

⚠ **The cost, recorded in PRD §5.8 rather than assumed away.** The asks now arrive before
the product has any shape — no named room, no named device, no reading. Node 24's pitch
("start cleaning about twenty minutes before you get back") is being made about a device
with no room, in a home that does not exist yet. That is a weaker frame than the same
sentence after node 17. **The tell is grant rate on node 24**; if it drops, moving node 24
alone back behind node 17 — keeping 25 where it is — recovers most of it. Also flagged:
node 24 and 25 copy still speaks as though a device is placed, and needs a reread against
the new position before ship.

Verified: walk reads `1…16, 24, 24, 25, 25, 17, 18, 18a, 18a, 23, 23, 23, 26`; primary-CTA
path from Connected runs W4 → L1 → L1D → N1 → N1D → R1 → R2; readout reads step 22/22 on
Home; no overflow, no dangling links.

---

## 2026-08-06 (4) — Pairing sequence rewritten; nodes 19–22 and `R3B` removed

Two owner changes, one additive and one subtractive.

**Removed: nodes 19–22 and the household disclosure.** The whole firmware sequence — check
for update (`U1`/`U1B`), install (`U2`), complete (`U3`), plus the timeout state (`U2E`) —
and the first-reading wait (`U4`) are gone. So is `R3B`, "What Lakshmi will see". Node 18
and node 18a now run straight into the tour at node 23; node 25's dialogs resolve straight
to Home. `v_clock()` and `v_updating()` went with them.

This kills the §5.5 dangling promise (node 19 said *"we'll notify you when it's done"* six
screens before notification permission was asked) and removes a multi-minute blocking wait
from setup. It also leaves **three things genuinely unhandled**, recorded in PRD §5 and §9
rather than lost with the screens:
  · Nothing in the flow takes a first reading. Home shows `34 · AQI` with no step that
    produced it, so `J-WEEK-01` now rests entirely on Home's first paint — which needs a
    real loading state for the ~20s before a reading exists. Reopens §5.3.
  · Firmware update has no path anywhere, in this spec or any other.
  · Inviting someone now grants access to everything with no screen disclosing it. For a
    product whose pitch is "your data stays on your devices", that is hard to defend.

**Rewritten: nodes 7–12, the pairing sequence.** Node 6 (choose the purifier) is unchanged.
After it:
  · **7 — Unwrap the filter** (NEW). Open the door, remove the polybag, reseat, close till
    it clicks. The only setup failure that is completely invisible: a bagged purifier
    behaves normally in every respect except cleaning. Own screen, not a bullet.
  · **8 — Plug in and switch on**, split out from the old combined instruction screen.
  · **9 — Wi-Fi light blinking**, with the hold-Wi-Fi-icon-5–6s recovery on the screen
    itself rather than behind a help link — on a re-setup it is the common path.
  · **10 — Switch on Bluetooth**, reframed around the radio being on rather than only the
    app permission. Dialog still follows with the reason visible behind it.
  · **11 — Scan → select from a list → pair.** A list, not a single confirm card: the scan
    genuinely can surface two, and a household with two purifiers hits that on day one.
  · **12 — Auto-fetch Wi-Fi credentials** (NEW). Read the network the phone is already on
    and pre-fill the password; nodes 13–14 (manual list + password) survive as the fallback.
    States the band rule where it matters rather than in an error.

**Node 15 re-spaced** per the same request: CTA pinned to the bottom, progress block just
above it, and the duplicate 4-dot stepper removed — the carousel has its own dots, and two
indicators on one screen read as two different progress meanings.

⚠ **One phrase in the brief is unresolved.** "Does not work with standalone wifi credential"
is built as *5 GHz-only networks*, which fits the accompanying "works on 2.4 GHz / dual
band". If it meant captive-portal or enterprise/802.1X, node 12's copy is wrong and both
need error states that do not exist. Flagged in PRD §5.

Verified: build asserts 22 main-line nodes + branch 18a; DOM pass confirms all 45 screens
fit the viewport, no `data-go` dangles, and the walk reads 1-18a then 23-26 with the 19-22
gap intact.

---

## 2026-08-06 (3) — Feature carousel on the Wi-Fi join wait (node 15)

Node 15 (`W3`, "joining Wi-Fi") now carries a **four-slide auto-advancing feature carousel**
above the progress bar: headline, a miniature app screenshot masked to zero opacity at its
lower edge, four dots, crossfading every 2.2s. Owner-specified shape.

The argument for putting marketing here, recorded in PRD §5.7: node 15 is the **only screen
in the flow with dead time the user cannot shorten**. It fills a wait rather than inserting
one — unlike node 23, which is an inserted wait and survives only because it runs after the
device already worked.

The four miniatures share status bar, greeting and title, and differ only in body, so they
read as four shots of one app rather than four unrelated graphics. All four are CSS-drawn;
no raster assets were added.

Three constraints held: crossfade at `standard` and never spring (gate 4 — it sits on a
progress bar on an ambient surface); auto-advance fully suppressed under
`prefers-reduced-motion` (gate 2), with the dots left as real buttons so it stays
hand-drivable; and screens now clear their intervals on navigation, so a destroyed carousel
cannot keep ticking against detached DOM.

⚠ **Left open, flagged in §5.7:** WCAG 2.2.2 (Pause/Stop/Hide). Four slides at 2.2s is an
8.8s loop repeating for the length of the join. Tapping a dot resets the timer, which is not
the same as pausing. If real joins routinely exceed ~10s this needs an explicit pause
control — a call to make from join telemetry, not taste.

Verified: 4 slides / 4 dots render, no screen in the file overflows its viewport, no
`data-go` dangles, the timer starts on node 15 and reaches zero on navigating away, and a
simulated `prefers-reduced-motion` produces zero timers while still showing a slide.

---

## 2026-08-06 (2) — Two owner corrections to the flow diagram rebuild

Same day as the rebuild below, two fixes on top of it:

**Node 22 moved.** "Taking first reading" sat right after node 21 (update complete), ahead
of the privacy tour and both permission asks — that is where the diagram's row layout placed
it, and it meant the first number the user actually sees still landed on Home four screens
later, behind three slides and two permission prompts. It now runs immediately before node
26, after nodes 23–25, so nothing sits between the wait and the number. This resolves the
open item recorded as PRD §5.3. `N1`/`N1D` (notifications) now resolve into `U4` (the
reading) rather than straight to Home; `U3` (update complete) now runs straight into the
tour at `C1`.

**Node 6 narrowed to purifier SKUs.** The first pass at node 6 offered four device
*categories* — purifier, camera, lock, vacuum, from `firstRunDeviceTypes` — with three of
them unbuyable and routed to a "not shipping yet" edge state (`P1B`). The owner corrected
this: node 6 is a choice of **purifier**, full stop — three SKUs (`HW-PUR-200` /
`HW-PUR-500` / `HW-PUR-MAX`, all three already in `src/hardware/devices.json`) as horizontal
cards stacked vertically, matching the confirm-card shape used at node 11 rather than a grid.
Camera, lock and vacuum no longer appear anywhere in this flow. `P1B` is removed (edge-state
count: 15 → 14). This retires PRD §5.4 outright rather than leaving it open. Node 23 slide 3
("One app, whole home") is now the only remaining place in the flow that names a future
device category — flagged in the PRD as the one unchecked roadmap claim left.

Verified: build still asserts 26 nodes + branch 18a; a DOM pass confirms all 50 screens fit
the viewport, no `data-go` target dangles, and the full-sequence walk now reads
`…21, 23, 23, 23, 24, 24, 25, 25, 22, 26` — node 22 immediately precedes Home.

---

## 2026-08-06 (1) — First run rebuilt to the owner's flow diagram

The 2026-08-05 first-run flow was **wrong against the owner's intent** and has been replaced.
The owner supplied a flow diagram — 26 main-line boxes plus one branch — and both artefacts
now follow it node for node.

**What the diagram changed.** Email account creation is new (nodes 4–5: name + email, then a
verification link). The device-type chooser is back (node 6: purifier, camera, lock, vacuum
from `firstRunDeviceTypes`), reversing the 2026-08-05 "purifier only" instruction. The home is
created while naming the room (node 17) rather than on its own screen before the box is
opened. The household shrank from eleven screens ahead of the device to a three-screen branch
off node 18. The location/geofencing ask is new (node 24). Gone: the standalone DPDP consent
pair, the analytics opt-in, and the dedicated reveal screen.

**Six things the diagram leaves open**, all argued in `docs/features/first-run/prd.md` §5.1–5.6
rather than silently decided: (1) there is no consent screen, so the DPDP notice rides on node
4 — a legal question, not a design one; (2) two verifications run back to back before the box
is opened; (3) **the reveal is no longer a screen** — the first number appears on Home, four
screens after the reading is taken, which is the largest behavioural risk in the rebuild;
(4) node 6 shows three device types nobody can buy; (5) node 19 promises a notification six
screens before the permission is asked, and geofencing must request While-Using, never Always;
(6) leading the tour with privacy is right, and costs saying it twice.

**Structural fix.** `build-wireframes.py` used to carry a second, independent copy of every
screen in its own renderer — which is exactly how the prototype and the flat board came to
disagree. It now **imports the screen set from `build-prototype.py`** and only lays it out,
grouping by node with each node's edge states in a dashed column beside it. One screen set,
two layouts; a flow correction can no longer be made in one file and missed in the other.

Verified: build asserts the sequence resolves to 26 nodes + branch 18a; a DOM pass confirms
all 51 screens fit the viewport without clipping and no `data-go` target dangles.

**Superseded:** the V1/V2/V3 ordering comparison, and the decision recorded on 2026-08-05 that
chose V1. The diagram answers the ordering question differently and is now the spec.

---

## 2026-08-05 (9) — Luna-style harness; green returns as accent under the 10% rule

**Harness.** The My Home preview now follows the owner-supplied Luna Cycle reference:
controller on the left in a warm cream column, phone large on the right. Scenarios are
grouped and numbered (New & early / Steady state / Events & seasons) rather than sitting in
a flat row, with the selected row taking a 2px black border. This replaces the stacked
top-bar layout from entry (5).

**Green is back, as accent only.** Uses the canonical `moss #4D6747` / `neon #AEC799` from
`src/tokens/design.tokens.js` rather than the muted band greens invented in entry (8), so
the prototype and the tokens now agree on at least the accent. Applied as slight gradients
in five places: the room-quality numeral, the report ring stroke, the good-band contributor
meters, the iso-room ripples, and one soft wash across the hero. Chrome, CTAs and body copy
stay monochrome.

**Measured, not asserted.** Green covers **~3.1% of the phone surface** on good-air states —
comfortably inside the 10% budget the tokens define. And it behaves semantically rather than
decoratively: on `liveEvent`, where the air is bad, **green drops to 0%** — the score numeral
falls back to ink and the badge takes the band colour. Green is earned by good air, which is
the correct reading of "green cannot carry bad" (`colors.status`, O-6).

One judgement call worth recording: the *confidence* dot stays green even on a bad-air
screen. It signals that the reading is trustworthy, not that the air is fine — a different
axis. Roughly 50px², and defensible, but flag it if it reads wrong.

⚠ Still unresolved: this is the prototype agreeing with the tokens on the accent only. The
grounds still differ (light greyscale here, ADR-001 warm sand in the tokens), and the My Home
PRD still specifies dark. **C-14 is unchanged and still the top visual decision.**

---

## 2026-08-05 (8) — "My Home" page built from the supplied PRD

`docs/features/my-home/my-home-prototype.html`, generated by `build-home.py`.
All six states from the PRD's state machine, the two-strata split, the report sheet and
the notification feed. Rendered from a fixture that mirrors the PRD §7 TypeScript
interfaces one-for-one, so nothing is hard-coded per screen and the React port is a
re-render rather than a redesign.

**Verified against the PRD's own acceptance criteria (§13):** six states render from the
fixture and switch on keys 1–6 · the two-strata split is structural, with **zero
non-ghost action buttons in the room stratum** · the hero opens the report, and the
report also opens from a simulated external caller · the contributor renormalisation path
is exercised (`dayOne` omits humidity; the four present weights sum to exactly 1.0 and the
report shows an `unavailable` row) · all seven detector classes appear as cards, including
the power-saver proposal, its receipt and its fan-effort-vs-air-need chart · the bell shows
an unseen count and its rows deep-link through the `Action.effect` vocabulary · empty slots
carry written copy · every action resolves locally with a toast · `liveEvent` suppresses
decorative slots · Esc closes sheets, the room render carries an `aria-label` with the live
AQI, band status always pairs colour with a text label · no `localStorage`/`sessionStorage`
anywhere.

**Three deliberate deviations, all logged in the file header and in decisions.md:**

1. **Palette — built light, PRD says dark.** See C-14. The user reaches this page straight
   off the first-run reveal; shipping two palettes in one session is a defect. The PRD is
   newer and says "approved for build", so this is the owner's call to make.
2. **Band colour introduced.** Four muted colours, narrowly scoped. This is O-6 filled
   provisionally in a prototype, not in the tokens — see the O-6 note.
3. **Stack.** PRD asks React + Tailwind; this repo has no app scaffold and every other
   artefact is a self-contained HTML prototype. Same pattern, fixture-driven.

**Not supplied:** `ding-home-states.html` (the S3 prototype the PRD names as visual truth).
Everything visual here is derived from the PRD text plus the established first-run language.

---

## 2026-08-05 (7) — Ordering locked to V1; Airbnb counter for the household; Apple structure for pairing

Four owner changes, all applied to `docs/features/first-run/first-run-prototype.html`.

**1. Background lifted.** A `#FFFFFF` layer at 30% now sits over the radial gradient. It was too dark
at the bottom-left corner where body copy and the T&C line land.

**2. The ordering decision is closed: V1.** Home → Household → Device. V2 and V3 are removed from
the prototype and the version picker is gone; the controller states the chosen order instead.
⚠ **This is the ordering I recommended against**, and the cost is now visible rather than argued:
because the household runs before any device exists, the “what she’ll see” disclosure cannot name a
device and has to describe an empty home. Screen H3’s copy was rewritten to “Whatever you add” and
its note points at exactly this. The decision is the owner’s; the consequence is recorded so nobody
rediscovers it later.

**3. The parts checklist is gone**, replaced with Apple Home’s Add Accessory structure: a viewfinder,
then each route named with one line of explanation — *Scan the setup code* / *Hold your phone close* —
plus *More options*. ⚠ The 2×2 checklist was the single screen the teardown rated highest, on the
grounds that it answers “am I about to get stuck?” before it is asked. The owner found it odd and it
is out. The prerequisites it carried were redistributed rather than dropped: the time estimate sits on
D1’s device card, and the Wi‑Fi password requirement sits on D14 where it is actually needed.

**4. Household add/remove rebuilt on the Airbnb guest counter.** Read the reference video frame by
frame (16 frames over 5.7s) and took the mechanic, not the art: a live figure group that grows and
shrinks, one very large number, `−` / `+` that dim at the bounds, and a secondary pill for the second
class of member. It is genuinely interactive in the prototype — the figures animate in and out and the
count clamps.

Two adaptations worth recording:

- **“Add children” became “Add household help.”** Airbnb’s second counter exists because children
  follow different rules. Ours has exactly the same shape: helpers get one device and an expiry date
  by default, family gets neither restriction. That is P3’s permissions requirement expressed as an
  interface rather than a settings screen.
- **A counter alone cannot carry names or scope**, which Airbnb does not need and we do. So the
  counter sets *how many*, and the following screen collects *who* — one field per person the counter
  added, with contact suggestions beneath. The invitation still goes to each person and is still
  accepted on their own device.

---

## 2026-08-05 (6) — Prototype restyled and restructured on owner direction

**Visual.** The accent green is gone from the prototype entirely — zero references to `moss`,
`#4D6747` or `#AEC799`. Replaced with the owner's reference treatment: a radial gradient running
`#FFFFFF` at the top right to `#A4A4A4` at the bottom left (a true diagonal falloff, `circle
farthest-corner at 100% 0%`), near-white cards carrying an 8%-opacity drop shadow, and a black
fully-rounded pill CTA. Every visual is CSS-drawn and monochrome, so the prototype now reads as a
designed product rather than a wireframe.

⚠ **This is prototype-local and does NOT change `src/tokens/design.tokens.js`.** The canonical
tokens still carry the greens from ADR-003/004. Either the tokens follow this direction and those
ADRs get superseded, or the prototype is a one-off exploration. That needs deciding before anything
is built — the two cannot both be true.

**Two structural changes, both owner calls:**

1. **The feature showcase moved after device setup**, in all three orderings — between the reveal
   and notification priming. A tour before the product has proved anything is a pitch; after the
   reveal it answers the question the user actually has. Cost: the privacy line is said twice, once
   as a promise before consent and once as a receipt afterwards. That is an acceptable trade.
2. **Purifier only.** Camera, lock and vacuum are out of every flow. The device step is now one
   large full-width card instead of a four-tile grid, so the single option reads as the intended
   one rather than a menu with three things missing.

**Two consequences worth flagging, both recorded in the PRD:**

- **Persona P4 (Priya, the camera owner) now has no entry point.** She was defined by arriving with
  a device that is not the purifier. She is out of scope until cameras return.
- **The strongest disclosure screen in the whole reference set had to be weakened.** Household
  step 3-of-3 said *"including the video and the audio recorded on them"* — the only screen in five
  apps that names video and audio. With cameras out of scope it would describe something that does
  not exist, so it now covers activity and history. **The camera wording must come back the moment a
  camera ships.**

Also added: hash deep-links (`#A12`, `#v3/D23`) so any screen can be linked directly for review.

---

## 2026-08-05 (5) — Tappable first-run prototype

`docs/features/first-run/first-run-prototype.html` — the flow as a working prototype rather than a
board. Light theme, one 390×844 phone, controller on the left: version (V1/V2/V3), position with
prev/next/reset, a jumpable step list, and a button to fire each of the eleven edge states directly.
Arrow keys drive it. Every button in the phone is live; error branches are reachable both from the
controller and from "simulate" buttons on the screen that owns them.

58 screens. Verified programmatically rather than by eye: no screen overflows the 844px frame, every
`data-go` target resolves, no screen is a dead end, and all three sequences walk start to finish.

The wireframe board (`first-run-wireframes.html`) stays — it is the better artefact for a review
meeting where everyone needs to see the whole flow at once. The prototype is the one to click.

One bug worth remembering: the generator had been entity-escaping all non-ASCII so the HTML would
survive any charset, but JS `textContent` does not decode entities, so every apostrophe and dash in
the screen titles and notes rendered literally as `&#8217;`. Fixed by emitting a proper standalone
document with `<meta charset="utf-8">` and dropping the escaping entirely. The reference-book
generator still needs the escaping, because it is wrapped by the Artifact runtime rather than
serving its own `<head>`.

---

## 2026-08-05 (4) — First-run wireframes, three orderings; hand-the-phone pattern removed

`docs/features/first-run/first-run-wireframes.html` — 57 screens at wireframe fidelity, every
state including all eight setup failures and every Wi-Fi sub-state (finding, picking, 5-GHz-only,
password, wrong password, joining, joined, on-network-no-internet). Three orderings switchable from
the left panel, plus a toggle to hide the edge states and read the happy path alone. Generated by
`build-wireframes.py`, so screens are data.

**The hand-the-phone-over step is gone.** An earlier draft borrowed Alexa's *"Hand your phone to
Sam"*, with a co-present path where the new member accepted terms on the owner's handset. The owner
rejected it and it does not come back. Three reasons, recorded in the PRD so the pattern stays dead:
it assumes both people are in the same room, which is exactly what P1 is not; it makes the owner's
phone the enrolment device, so the invitee keeps no independent record of what they agreed to; and it
has the owner physically present while someone else grants a data-processing consent, which is not a
consent worth having to defend.

**Household now follows Apple Home / Google Home**: type a contact, disclose exactly what they will
be able to reach (three pages, camera video and audio named explicitly), review, send. The invitee
accepts on their own device. Pending appears in the roster immediately; acceptance resolves it in
place.

**The ordering question is now framed rather than assumed.** V1 puts the household with the home
(~27 screens to the reveal), V2 after the device (~14), V3 after the reveal with the account last
(~9). Each carries its own argument for and against.

**V3 is the interesting one and it fails on law, not taste.** Pairing over BLE genuinely needs no
account, so the reveal could come ninth. But the DPDP Act requires notice and consent *before*
processing personal data, and an air reading tied to a room in someone's home is personal data — so
the privacy screen moves back in front of the device and most of the advantage evaporates. Worth
keeping in the document as a closed question rather than an untried idea.

**Recommendation stands at V2** — the only ordering with both the reference evidence and the
consent sequencing on its side.

---

## 2026-08-05 (3) — Real Mobbin screenshots in the reference book

The owner connected **Mobbin's MCP server** (`https://api.mobbin.com/mcp`, OAuth via Supabase),
which solved the extraction problem the previous entry describes. **69 of the 85 reference tiles
are now the actual Mobbin capture**; 15 remain labelled redrawn wireframes; 1 is ours.

**Why the MCP worked where the browser did not.** `search_flows` returns *every* screen of a flow
with a plain `https://mobbin.com/api/mcp/short/<id>` URL — no query string, no auth — so `curl`
fetches it straight into the repo. Nothing had to cross the browser boundary.

**The pipeline is reusable** — `docs/research/fetch-refs.py`: `add` downloads a flow, `sheet` builds
a numbered montage so all 22 screens of a flow can be identified in one look, `bind` copies the
chosen ones to `refs/<slug>.png`, `status` reports coverage. `refs/_raw/` keeps every download, so
re-binding never re-fetches.

**Three captions were corrected once the real screens arrived**, and the note lost every time:

1. IKEA's analytics consent uses **checkboxes**, not radio buttons.
2. Google Home has **no standalone Device access screen** — stage Q now shows the *Invite sent*
   state, where the pending member appears in the household row before accepting.
3. SmartThings has **no device-added screen** — stage M now shows the Favorites grid that setup both
   starts and ends in, which makes the "no reveal" point better than the original note did.

Also confirmed against real captures: SmartThings runs **five** intro slides with the local-network
and Bluetooth prompts landing on slides 1–2, and Alexa's device flow has a *"Which room is your Echo
Pop in?"* step we had not recorded.

---

## 2026-08-05 (2) — First-run reference book, typeset as a 21-page PDF

`docs/research/NOMA-first-run-references.pdf`. Seventeen stages from cold install to a populated
household. Each stage is one page: **five annotated competitor references** (app · flow · screen ·
verbatim copy · a take-or-avoid verdict), then what NOMA does, then the rules that stage sets.
85 reference tiles in total. Generated by `docs/research/build-refs.py`, so the whole book is
regenerable and every tile is editable as data.

**The reference tiles are hand-drawn wireframes, not Mobbin's bitmaps.** They carry the real
layout, hierarchy and verbatim copy plus exact app/flow/screen coordinates, but not the pixels.
Every route for getting Mobbin's images into this repo turned out to be closed: signed CDN URLs
are redacted in transit, the image canvas is cross-origin-tainted, a page-to-localhost upload is
blocked as mixed content, the clipboard is isolated, programmatic downloads never fire, and long
strings are truncated. Mobbin's own **“Download all screens”** button *does* work — fired on IKEA's
Onboarding flow, it reported *16 screens downloaded* — but the files land on the browser's
filesystem, which is not the one this repo lives on. The generator picks up
`docs/research/refs/<slug>.png` automatically if real captures are ever dropped in, so swapping
them is a file copy and a re-run, not a rewrite.

Three findings that only surfaced while laying the stages out side by side:

1. **Not one of the five reference apps uses phone + OTP.** All five are email-and-password
   systems, three tied to a platform account. For an Indian consumer product that is the wrong
   shape, so stage C is deliberately unlike all five and has no reference to copy.
2. **All five end setup with a device tile in a list.** Nobody has a reveal. Since air is
   invisible, that final screen is the entire opportunity — stage M is the one page in the book
   with no competitor reference behind it.
3. **SmartThings is the cautionary tale**: 22 screens to add one TV, and the progress indicator
   re-bases twice inside a single flow, so progress becomes unreadable. Long is survivable;
   unmeasurable is not.

---

## 2026-08-05 (1) — First-run flow: Mobbin teardown + the first feature PRD

**Research.** Read 9 flows / ~130 screens across the five smart-home apps Mobbin
carries (Google Home, Apple Home, SmartThings, IKEA Home smart, Amazon Alexa) —
onboarding, home creation, device pairing and household invites in each.
`docs/research/2026-08-05-setup-teardown.md`.

Two findings shaped the spec:

1. **Device before people, five out of five.** Not one reference app asks for a
   household member during first run; members always live in Settings, reached later.
   So the brief's suggested order (members → device) is inverted in the spec, with
   the reasoning stated: an invitation to a home with no devices scopes nothing, and
   the invite lands far better *after* `J-WEEK-01`'s reveal than ninety seconds
   before it.
2. **Mobbin has no purifier or air-quality app at all** (also no Aqara, Ring, Nest,
   Wyze, Eufy, Tuya, Hue). There is no incumbent to copy. IKEA's DIRIGERA hub flow —
   a physical object you plug in and watch a light on — is the closest analogue and
   is the best flow in the set by a distance.

Twelve patterns extracted with attribution. The three that most change our design:
IKEA's **parts checklist before the first instruction** ("Here's what you'll need"),
Google's **"What's shared" disclosure before an invite is sent**, and Alexa's
**dual enrolment** (hand-the-phone-over vs. send-a-link), which maps exactly onto
P1-remote and P2-in-the-room.

**Spec.** `docs/features/first-run/prd.md` — the first feature PRD in the repo.
Three steps (Arrival → Device → Household), screen-by-screen, from
`templates/feature-prd.md`. Includes the eight setup failure states that the
scope ledger records as missing everywhere, and the DPDP consent screens as a
scroll-gated privacy statement plus an unticked analytics choice.

Deliberate calls made in the spec, each argued rather than assumed:
- **Value slide 4 (Home Score) cut** — it promises a surface whose zero-device state
  has never been designed.
- **No OS permission dialog before screen 2.5** — priming stays, the prompt moves to
  the moment of need. SmartThings fires three before showing any value.
- **Members offered as a dismissible card, never a gate.**
- **The privacy statement must name the narrowing** that `ai-integration.md` §10
  flags: personal and biometric data stays local, ambient public data is fetched.

**Two new open items** — `O-8` (onboarding and setup have no `F-*` id; the PRD is
written against two *proposed, unassigned* ids rather than inventing registry
entries) and `O-9` (`identify` and the ring-LED state vocabulary are hardware
behaviours no document confirms exist).

Nothing was reconciled. `C-2` still blocks every string, `C-3` leaves Step 3
shape-only, `C-11` means the flow ships unmeasurable.

---

## 2026-08-04 (6) — PRD expanded and typeset as a 36-page PDF

The v0.1 PRD compressed too much out. v0.2 restores the detail: 36 pages, ~9,100
words, every figure and quote from the source material rather than a summary of it.

**New in v0.2** — full seven-day arc with each day's research finding, target emotion
and actual numbers (168 first reading, 187→22 overnight, ₹164 saved, ₹0.40/hour, 34%
filter / ~22 days, Air Score 84, 148 hours, 61M particles) · the complete competitor
teardown with each brand's own stated filter method and high-AQI sensor behaviour ·
all three subscription tiers with full feature lists · the whole device catalogue and
consumables · six wearable trigger signals with IDs · the per-device-type permission
grants (camera 7 / lock 2 / purifier 2 / vacuum 2) and why the asymmetry is correct ·
all ten data-model entities with fields · every pollutant with example values ·
the full voice-characteristics table with evidence · nine India-context specifics ·
the complete design-system section with printed swatches, the type scale, elevation
and the measured contrast trap · all motion tokens and MO-* patterns · nine missing
flows · thirteen conflicts with what each blocks.

**Typeset rather than dumped.** Cover, contents, numbered sections, severity-coded
callouts, printed colour swatches at true values, tabular figures. Set in the actual
Google Sans Flex — verified embedded and rendering, not falling back.

Delivered as `docs/prd/NOMA-v1-PRD.pdf` with the print source vendored alongside
(`prd-print.html`, font externalised) so the PDF is reproducible with one headless
Chrome command.

Verified: 36 pages · 9,137 words extractable · 20 spot-checked key facts all present
in the extracted text · swatches print at true hex · superscripts render (µg/m³, not
tofu boxes).

---

## 2026-08-04 (5) — Master PRD written

`docs/prd/noma-v1.md` — the whole product as supplied to date, compiled from the four
PM prototypes, the Airbnb visual reference, the owner-supplied typeface, both green
revisions and the motion ruling. ~4,000 words. `templates/feature-prd.md` populated
alongside it (it now mandates a `declares` block and explicit error/empty/offline
states, since their absence was the most systematic gap in the source material).

**It opens with the decision everything else waits on.** The material describes two
products — a purifier companion with real research behind it, and a whole-home
platform that is broader but mostly asserted. The PRD recommends shipping the
companion architected as a subset of the platform, and marks every platform-only
item `[B]` so the split is legible. That recommendation is explicitly the owner's to
accept or reject.

**Four blockers are called out as critical rather than listed flatly:**
- **C-7** — the differentiator (AQI-weighted filter life) has a worked example and no
  formula. It gates the feature that is simultaneously the differentiator and the
  recurring-revenue lever, so nothing else in v1 is worth as much as closing it.
- **C-11** — "data never leaves home" cannot coexist literally with CPCB blending,
  forecast pre-clean and neighbour comparison. Also blocks the analytics taxonomy.
- **C-8** — no safety class for autonomy; "Act silently" could reach a lock or an
  unattended purchase. v1 ships "Ask me" only until ruled.
- **C-2** — five product/assistant names; all copy and i18n is downstream.

Also recorded: the accessibility floor derives from persona P2 (low-fluency
residents) — 16pt body minimum, 44pt targets, no safety state by colour alone; and
the seven-day arc is entirely push-dependent, so a notification denial at
J-ONBOARD-06 kills days 1–7 with no other signal changing. That is named as the
single highest-leverage thing to measure.

Design is the one section with no open conflicts — ADR-001…005 are all settled.

---

## 2026-08-04 (4) — Motion tokens: ADR-005 resolves O-7

Owner ruled the playful-vs-`ma` tension: NOMA's motion is **playful — springy,
bouncy, Airbnb-register — on discrete moments, and still on ambient ones**.
`src/tokens/motion.tokens.js` is populated (two springs, five duration tiers plus
a 4s ambient tier, stagger, press/pop/breathe scales); `.claude/rules/motion.md`
now carries six greppable gates (tokens only, reduced-motion mandatory, exits
never bounce, ambient never springs, alarm never bounces, patterns start from the
template). `memory/motion/philosophy.md` and `patterns.md` (MO-* registry) are
populated. `vision.md`'s tension note now points at the resolution.

Provenance caveat recorded in the ADR: the owner referenced a bouncy style from an
earlier session unavailable to this one; values are a fresh codification of the
stated direction, and any recovered earlier values reconcile via ADR revision.

---

## 2026-08-04 (3) — PM prototype set ingested; six pillars populated

**What changed.** Four PM-supplied HTML prototypes were read and extracted into the
knowledge base. This is the first real product substance the repo has held — before this,
everything outside the design foundation was a `TODO(owner)` stub.

Populated: `src/hardware/devices.json` · `src/hardware/feature-map.json` ·
`memory/product/journeys.md` · `memory/product/scope-ledger.md` ·
`memory/architecture/{system,data-models,ai-integration}.md` ·
`memory/analytics/{event-taxonomy,monetization-map,trigger-map}.md` ·
`memory/voice/ai-personas.md` · `memory/index.md` · `docs/index.md`.

**No design-pillar values were touched.** Tokens, fonts and ADR-001…004 are untouched.

**The most valuable finding** is the agent model in `air-agent-app.html`, now written up
in `memory/architecture/ai-integration.md`:

- **Graduated autonomy, per capability, three levels** (Ask me → Act & tell me → Act
  silently). Not global, not binary, defaults to proposal-only.
- **A four-slot explanation contract**: Sensed / Decided / **Instead of** / Obeys rule.
  "Instead of" — naming the counterfactual — is the unusual one and the reason a decision
  reads as considered rather than arbitrary. "Obeys rule" is a promise the rules engine
  has to be able to keep.
- **Inert, editable rehearsal** before execution, where rule-derived steps render
  `Locked` rather than `Edit` so a user cannot casually edit away their own constraint.
- Trust is promoted on **evidence**: "You've accepted 7 fan suggestions in a row."

That is an architectural position, not a UI pattern, and it should be read before any
agent surface is designed.

**Second finding — C-1 now has evidence.** The prototypes independently corroborate
persona Set B: **Ravi** and **Lakshmi** appear as real named people in the camera event
feed, all four surfaces Set B names exist as built screens (Home Score, Faces You Trust,
Shop, AQI), and P3's "household help" maps exactly onto the `staff` role. Set A's names
appear nowhere in any of the four documents. **C-1 is not closed** — that is the owner's
call, and the prototypes could have been built from a superseded brief — but four for four
is worth knowing.

**Twelve new conflicts opened (C-2…C-13).** The four documents disagree with each other on
nearly every naming decision. Nothing was reconciled; both readings are recorded with
evidence. Highest-leverage first:

| ID | Conflict |
|---|---|
| **C-2** | Product and assistant have **five names** between them (NOMA / Ding / Noise Home / Noise Air / Noise Sanctuary; assistant: Ding / Noise AI Agent / Sanctuary Assistant). Blocks all copy and i18n. |
| **C-7** | The core differentiator — AQI-weighted filter life — has a worked example and **no formula**. A marketing claim awaiting an engineering model. |
| **C-11** | "Data never leaves home" vs three features that cannot work locally (CPCB outdoor blend, forecast pre-clean, neighbourhood compare). Also blocks the analytics taxonomy. |
| **C-8** | No safety class for agent autonomy. Nothing stops "Act silently" applying to a **lock** or to **spending money**; SpO₂ → Turbo is health-adjacent with no medical position. |
| C-3 | Three role models for sharing (the flow was rebuilt three times) |
| C-4 | Three fan-mode vocabularies; "Turbo" is the only shared value |
| C-5 | Four definitions of the Score |
| C-6 | Anchor purifier is ₹4,999 or ₹8,999; filter ₹1,299 or ₹1,499 |
| C-9 | The air map shows AQI for rooms with no sensor — and uses it to sell hardware |
| C-10 | "Anonymised" neighbour comparison shows a surname and a floor number |
| C-12 | Two room-preset lists; only one has Pooja Room |
| C-13 | The subscription sells AQI-weighted filtering, which *is* the free tier's claim |

**Deliberately left as stubs**, because they are blocked rather than unwritten:
`voice/tone-matrix.md` and `voice/glossary.md` (blocked by C-1 and C-2),
`motion/*` (O-7), `architecture/api-contracts.md` (none exist),
`analytics/{funnels,metrics-dictionary}.md` (blocked by C-11),
`src/analytics/events.schema.json` and `src/personas/personas.json`
(**intentionally empty** — a guessed machine-readable file is worse than an empty one).

**Verified:** both JSON files parse; ID prefixes (`J-*`, `F-*`, `HW-*`, `C-#`) are
consistent across the new files and indexed in `memory/index.md`.

**Honest limits of this work.** These are design prototypes, not specs: seeded data, happy
paths only, no empty/error/loading states anywhere, and zero PRDs. Device specs (CADR,
coverage) are marked `prototype-only` and have not been checked against a datasheet. The
source files still live in the owner's `~/Downloads` — the provenance of this entire
knowledge base is currently a local folder, and they should be vendored.

---

## 2026-08-04 (2) — Accent greens retuned (ADR-004)

`neon #A6CD86 → #AEC799`; deep anchor `sage #2C5146 → moss #4D6747`, renamed to match the
owner's naming. Derived states recomputed in-hue.

Two measured consequences: the primary CTA **lost AAA** (8.85:1 → 6.27:1 on white — still
comfortably AA and correct for a 16px/600 button label, but no longer AAA); and the pair is
now **one hue family**, 16° apart instead of 69°, so ADR-003's ban on interpolating between
them was relaxed and the "muddy olive" warning corrected rather than left to mislead.

---

## 2026-08-04 (1) — Visual foundation established (ADR-001…003)

Warm-neutral surface language derived from Airbnb iOS: `neutral` carries text and
structure, `sand` carries the warmth, so text contrast stays predictable instead of
drifting with a tint. Airbnb's red explicitly rejected. Two card anatomies
(elevated-on-warm, outlined-on-white) that are not interchangeable.

Google Sans Flex adopted (ADR-002) — variable, six axes, of which Noma drives `wght` and
`opsz`. Green accent adopted and budgeted at 10% (ADR-003).

Opened O-3 (light theme only), O-4 (hexes read optically — cross-origin sampling was
blocked), O-5 (no Devanagari coverage despite an `hi` locale), O-6 (no status colours —
green cannot carry "bad"), O-7 ("playful bounce" vs `ma` calm).
