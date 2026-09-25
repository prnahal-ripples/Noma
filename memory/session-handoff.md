# Session Handoff — MANDATORY FIRST READ

**Last updated:** 2026-08-21
**Branch:** `main` (Noma-main) — pushed through `ea6f78b`, **plus uncommitted local
changes on top, see below**. `main` (noiseFit mirror) — pushed through `19e0682`.
Both repos are on `main` directly right now, not a feature branch.

---

## Read this first — 2026-08-21 (1)

**Everything the 2026-08-20 (1) entry below describes is now finished and shipped,
and a lot has happened since.** That entry still talks about a "25 nodes" flow with
the key card "assembled while you type" — that build is done and superseded. Read
`memory/changelog.md` entries (1) through (15) under 2026-08-20 for the full
blow-by-blow; this is the orientation summary.

### The key-card creation stage, finished

Five screens, one card that never duplicates itself: node 4 (name + mobile, a real
bottom sheet, fields actually wired — they were silently broken for a while, see
below), node 5 (mobile OTP), 5a (wallet slides open), 5b (colourway picker + the
gyroscopic shimmer), 5c (the dot-matrix celebration). The card travels between all
of them as ONE element (`.khero`), never re-created, and parks in perspective at
the top centre — exactly on the back button's vertical line — between 5c and the
door. Getting the perspective park right took two rounds of transform-order bugs
(perspective must not project pre-translate geometry; rotate must happen at the
already-scaled size, not full size) — both were only findable by measuring the
rendered box against the phone width, not by looking at it.

⚠ **Node 4's form was broken for a real stretch of this session.** The field
binding lived inside a function scoped to the profile CARD, and node 4 stopped
having a card when it became a sheet — so typing did nothing and Proceed could
never enable. Fixed by moving the binding to run per-screen (`wireBinds()`)
instead. Worth remembering: a field's behaviour must never depend on some other
unrelated element being present on the screen.

### The flow was restructured, not just polished — node numbers do NOT renumber

Owner: Bluetooth now comes **before** the box is ever opened. New order: key
card → switch on Bluetooth → the scan (**now the device picker**) → pair → unwrap
the filter → find a socket → light blinking → Wi-Fi → connected → name the room →
name the device → tap the key on the door → home.

- **Node 6 ("choose your purifier") is DELETED**, not hidden. The Bluetooth scan
  answers the same question from what it can actually see, so asking up front
  asked twice. The scan's rows now carry the SKU and the real product renders
  (`.rnd--{sku}`) instead of a generic Bluetooth glyph — verified by clicking a row
  and confirming `.phone` picks up `sku-500`.
- **Nodes 24, 25 (location/geofencing, notifications) and branch 18a (send a
  key) left the happy path.** Demoted to edge states, not hard-deleted — for 18a
  that's exactly what was asked (it's now a secondary "Send a key" button on node
  18 instead of its own page); for 24/25 the instruction was "remove" and
  demoting was my judgment call for the least-destructive version. **Still an
  open owner decision** whether that should become a real deletion.
- Happy path: 30 → 24 screens, 25 → 21 nodes. **The node id list is deliberately
  NOT sorted any more** (10, 11, 7, 8, 9, 13, 12, ...) because the owner still
  calls it "node 7 unwrap the filter" — only the ORDER changed, not the ids.
  There is a build assertion that throws if the list ever comes back sorted,
  because that would mean this resequence got silently undone.
- Cost worth knowing: two identical purifier SKUs used to be a deliberate case
  (a household with a matched pair) and that case is now unrepresented in the
  scan. "Identify" (blink the light on one device) was already flagged as owed
  before this build and is what would fix it.

### Publishing got a real complication: two Vercel entries now exist on purpose

The owner asked to push the resequenced flow as **"First Run NEW"** while
**explicitly not changing the older onboarding entry**. But an earlier sync in
this same session had already overwritten that older entry with the resequence.
So the fix was to actually split them: `first-run-flow.html` /
`first-run-mobile.html` in the noiseFit mirror were rolled back to their
pre-resequence commit and re-published as the frozen old entry (dashboard counts
restored to 42/30/12); the resequenced build was published as brand-new files —
`first-run-new.html` / `first-run-new-mobile.html` — registered as their own
dashboard rows ("First Run NEW", "First Run NEW — on a phone"). Verified live on
`noise-apps.vercel.app` that the two are genuinely different builds (the frozen
one still contains "Choose your purifier"; the new one doesn't).

**Open question:** the frozen old entry is now stale relative to later fixes
(centred sheet titles, device renders in the scan) that only landed in the new
build. Does it stay frozen as a snapshot, or get retired from the dashboard
entirely?

### A new rendering exists: the flow on an actual phone

`build-mobile.py` → `first-run-mobile.html` (and its "-new" twin). No phone
frame, no controller — `.phone` becomes the real viewport, specifically so the
gyroscopic card shimmer can be judged on a handset instead of approximated with
a mouse on a laptop. Opens on a one-tap gate whose only job is to be a real user
gesture, because iOS refuses `DeviceOrientationEvent` permission outside one, and
the flow's own gyro-permission prompt doesn't fire until several taps in
otherwise. Proven end to end by driving `onOrient()` with a fake sensor reading
and confirming the card's `--gx` custom property actually moves.

### Voice and visual polish across the whole flow

- **Every header shortened**, except six the voice guide's own corrections bank
  (`docs/voice/noma-voice-guide.md` §10.1/§10.2) quotes as the *approved fix* for
  an earlier failure — those six were deliberately left alone. One header
  ("Shall I tell you when something changes?") wasn't shortened at all, it was
  corrected to a fix the guide already prescribes; the flow had been shipping
  the "before" column of that entry.
- **A title gradient (ink → green → ink) is now on every header**, not just the
  key-card screens. Retuned once already: stops moved to 24/50/74 and the green
  darkened to `#8EAE7D` so it reads as a slim streak rather than a wash. ⚠ That
  colour is NOT `green.neon` (`#AEC799`) — recorded as given in
  `src/tokens/design.tokens.js` and flagged rather than silently snapped. Still
  an open call.
- **Bottom sheets resize+dissolve between pages** instead of snapping — but the
  dissolve was silently skipping on any two consecutive sheets that happened to
  be the same height (nodes 4→5), because the original code treated "no resize
  needed" as "no transition needed" and they are two separate promises. Fixed.
- **Sheet titles and "Edit number" are centred** — this was fixing a regression
  the gradient itself caused (a `width:fit-content` heading ignores its parent's
  `text-align`), not a new feature. Took two placements and two specificity
  levels to actually stick; both failures were cascade-order bugs, not layout
  bugs, and both were proven by testing an inline style first.
- **A ghost white circle was showing in the nav's right slot on nodes 2-5 on
  the live Vercel deploy** — caught by the owner, not by me. Cause: the nav's
  empty placeholder span needs an explicit `visibility:hidden` companion rule
  at every host that uses it, and the newest host (the page-level back button
  added this session) never got that companion rule copied over. Fixed and
  verified against the live deploy directly, not just locally.
- **The wallet sleeve now matches the reference proportions** — the front
  pocket render was being stretched to the same width as the back layer instead
  of rendering narrower, which is why the "envelope" effect never read
  correctly. Geometry only; both PNGs were re-supplied with identical framing.

### Uncommitted right now — the newest background swap

The most recent turns swapped the sign-in background image (nodes 1–5) **twice**,
live in the local preview only. Current on-disk state:
`docs/features/first-run/assets/first-run-bg.jpg` and all five rebuilt renderings
reflect the SECOND swap (a white plastered staircase/arch/succulents render).
**None of this is committed, pushed, or synced to the noiseFit mirror or
Vercel** — the owner has only asked for local previews so far. `git status`
shows exactly these 7 files plus `.claude/launch.json` dirty.

⚠ **`.claude/launch.json` has a local-only preview-server entry pointing at a
session-scoped `/private/tmp/...` path.** This must NEVER be committed — it has
already leaked into a commit and had to be reverted TWICE earlier this session.
Check `git diff .claude/launch.json` before every commit from now on.

⚠ **The new background was measured against the project's own palette rule**
(LAW 6, a 10% budget on solid green in a surface) because the asset's own README
flags this as something to re-check on any replacement. It measures **~13–14%
green overall and ~23–26% in the top 45% of the frame** — the band that stays
visible above the sheet on every one of these five screens. Flagged twice now
(once per swap), never resolved. Not blocking, just unresolved.

### Open owner decisions, consolidated (ask about these, don't guess)

1. Nodes 5b/5c read "Key created" then "Key card created" back to back —
   flagged 4+ times across this session, needs an actual copy decision.
2. The new background's green content is over the documented 10% budget in the
   visible band. Ship as-is, crop tighter, or desaturate the foliage?
3. The title gradient's green (`#8EAE7D`) is not one of the two brand greens.
   Snap it to `green.neon` (no visible change, palette rule holds cleanly), or
   keep it as a deliberate third green?
4. Nodes 24/25 (location, notifications) and the send-a-key page — demoted to
   edge states this session. Should they become real deletions instead?
5. The frozen "First Run" Vercel entry vs the new "First Run NEW" entry — keep
   both indefinitely, or retire the old one?
6. C-15 (chips FILL vs cards LIFT) — open since well before this session,
   `memory/decisions.md`.
7. Node 4 has no avatar field; the pencil icon on the card (5b) is the only way
   to set a picture, and nothing signals it's tappable. Keep, add an
   affordance, or drop the avatar from first run?
8. The Bluetooth scan can no longer represent "two identical purifiers found"
   (a matched-pair household) now that node 6 is gone — "Identify" (blink the
   light on one) was already owed before this build and is the real fix.

### Workflow, mechanics, and mistakes worth not repeating

- **The screen set lives in exactly one place: `build-prototype.py`.** Five
  renderings regenerate from it — `build-flow.py`, `build-export.py`,
  `build-wireframes.py`, `build-auth.py` (a separate standalone tool, not
  generated from the main file), and `build-mobile.py`. Never hand-edit the
  `.html` outputs; they get overwritten on the next build.
- **After any change: rebuild all five, then run `docs/voice/audit-voice.py`,
  then commit.** The voice gate is a machine gate only — it does not replace
  reading the copy aloud, and it says so on every run.
- **Two repos, two pushes.** `Noma-main` is the source of truth. The site
  actually served at `noise-apps.vercel.app` is a SEPARATE local clone,
  `~/Desktop/noiseFit`, at `flows/noma/exploration/onboarding/`. After pushing
  Noma-main, copy the rebuilt `.html` into noiseFit, update the screen/path/edge
  counts in `noiseFit/dashboard/dashboard.js`, then commit and push noiseFit
  too. A push to Noma-main alone does not update what the owner sees live.
- **Measure in a real browser, not headless.** Headless Chrome does not tick CSS
  animations, so any check involving a running transition or animation state has
  to happen against the actual Browser-pane preview — a headless capture gave at
  least one confirmed false positive this session (a retired element read as
  "still visible" purely because the animation clock never advanced).
- **Local preview mechanism**: `python3 -m http.server` cannot run in this
  sandbox — `argparse` evaluates `os.getcwd()` for its default `--directory`,
  which the sandbox blocks. The workaround is a small custom server
  (`serve.py`) staged in the session scratchpad, serving a copy of the built
  HTML from a `preview/` subfolder there, registered as a `first-run` entry in
  `.claude/launch.json` for the duration of the session. That registration is
  ephemeral and must not be committed (see above).
- **Asset vendoring convention**, documented in
  `docs/features/first-run/assets/README.md` and
  `design-elements/brand/keycard/README.md`: flatten any alpha onto white,
  resize to the target width, encode photographic backgrounds as progressive
  JPEG q82 and artwork/product renders as WEBP q70 via PIL (`sips` can read but
  not write webp on this machine). Always check alpha noise (`getchannel('A')`,
  count pixels below ~250) before flattening — some source exports carry none,
  some carry a few percent of stray edge alpha.
- **Prefer measuring over eyeballing, always.** Repeated pattern all session:
  pixel-scanning geometry, `getBoundingClientRect()`/`getComputedStyle()` in a
  live page, and `getAnimations()` to see which rule actually won a cascade
  fight — screenshots alone missed real bugs (a mis-specified centring rule, a
  transform-order bug that inflated a card 3x, a ghost element invisible in a
  static capture but present in the DOM).

### Canonical references for a fresh session

- `CLAUDE.md` — routes to everything else; rule 1 is "read this handoff file
  first," rule 7 is "update it at the end of every session."
- `memory/changelog.md` — full chronological detail behind every summary above.
- `docs/voice/noma-voice-guide.md` — the voice rules, the corrections bank
  (§10), and the vocabulary tables (§5) referenced throughout this entry.
- `memory/decisions.md` — open conflicts including C-15.
- `.claude/rules/design-system.md` — the three-CTA rule, the icon-register
  boundaries, the large-surface corner-smoothing gates.

---

## Read this first — 2026-08-20 (1)

**The key-card stage is five screens now.** Node 4 sheet (name + number) → node 5
sheet (mobile OTP) → **5a** the wallet → **5b** colourways → **5c** the existing
dot-matrix celebration. 25 nodes. The card is no longer assembled while you
type; it is handed to you in a sleeve.

**⚠ THE COLOURWAY LIVES ON `.phone` AS `data-kc`, AND ONLY `wireWays()` WRITES
IT.** Two consequences that already cost time:

- **Patching `data-kc` into the built HTML proves nothing.** `wireWays()` runs
  `apply(WAY)` on mount and overwrites whatever you set. To test a colourway,
  seed `let WAY = '<n>'` instead — that is the real entry point.
- Deep-linking to node 5a or 5c and seeing no colour change is **not a bug**.
  `data-kc` is only written once the picker has mounted, so the attribute does
  not exist until you have been to 5b. Walk the flow; don't jump.

Colour differences must be measured with an **image diff of the same pixels**,
not by sampling two cards. The art is a brushed-metal radial — sampling
different points measures the gradient. (Proven path: 55,798 px change on 5b
between kc1 and kc4, and the corner mini follows into pairing.)

**⚠ ~40 `__PLACEHOLDER__` SUBSTITUTIONS RUN ACROSS THREE SEPARATE CHAINS** in
build-prototype.py — the CSS chain, `RUNTIME_JS`, and the body. Putting a
`.replace()` on the wrong chain **fails silently**: the placeholder ships as
literal text and whatever it configured stops working. There is now a build
assertion that no `__NAME__` survives into the output. It bites; it was proven
by breaking it on purpose. If you add a placeholder, know which chain owns it.

**The five colourways are tokens, not literals** — `keycard.ways` in
`src/tokens/design.tokens.js`, read through node by `_ways()`. The array ORDER
is the owner's mapping (pink→2, yellow→3, blue→4, green→5), which is exactly why
it must not be mirrored. `_ways()` asserts artwork exists for every id.

**⚠ SLICE EDITS KEEP DESTROYING CSS — THIRD OCCURRENCE.** This session lost the
infinity loader, both dot-matrix layers, the celebration caption and the mobile
field's `+91` prefix to one `s[s.index(a):s.index(b)]` replacement. **Missing CSS
builds perfectly and fails silently.** Use anchored insertion
(`s.replace(anchor, block + anchor, 1)`), never index slicing. And the
removed-selector audit **lied**: it grepped the whole file and matched generated
markup, so it reported deleted CSS as "present". Check the CSS text specifically.

**A card's internals must not inherit page alignment.** `.kcard__id` picked up
`text-align:center` from node 5a's centred column and the same card read two ways
on consecutive screens. `text-align:left` there is load-bearing.

**Open owner calls from this session** — flagged, not decided:
- Nodes 5b/5c read "Key created" then "Key card created" back to back.
- Node 4's sheet has no avatar field, and the owner's frames show no edit
  affordance on the card. The pencil on 5b is now the only way to set a picture:
  keep it, or drop the avatar from first run entirely.
- C-15 (chips FILL vs cards LIFT) still unresolved.

---

## Read this first — 2026-08-19 (11)

**The card shimmer is a SPECKLE, on movement only, on nodes 4/5/4a only.**
A rainbow gradient seen through a dot grid, intersected with a patch the tilt
drags (`mask-composite:intersect` — without it the masks union and the whole
face fills). Opacity is purely deflection, from **zero**: no resting shimmer.

**⚠ `key-card.webp` IS NOT A PLAIN ROUNDED RECT.** It is an outer translucent
**tray** with the real card **face** inset inside it. Anything overlaid on the
card must clip to the FACE or it spills across the tray and its corner follows
nothing. Measured (640×882): insets **L/R 14.84%, T 9.98%, B 13.38%**, corner
**9.33% of face width**. These live in `recipes.cardShimmer.face`.
⚠ **Re-exporting that artwork invalidates those five numbers** — they are
measured, not derived at build time (decoding webp would need `sips`, macOS
only). Re-measure from the alpha channel: longest contiguous run ≥ 245.

⚠ The owner asked for a **34px** corner. That is `radius.xxxl`, not what this
artwork is drawn with — the face's own corner is 17.3 css px at the current
render. A true 34 needs the PNG re-exported. Flagged, not faked.

**⚠ rAF LOOPS MUST NOT BE BOOLEAN-GUARDED IN THIS HARNESS.** `clearTimers()`
cancels every handle in `rafs` on each screen change, so an `if (running)
return` guard means the loop dies after ONE navigation and never restarts. Use a
generation counter (`TILT.gen`) and start a fresh loop per screen. This is what
made the shimmer look "not working" — the hover target updated while the damped
value sat at 0.

---

## Read this first — 2026-08-19 (10)

**MO-GYRO is registered** (`memory/motion/patterns.md`): the key card tilts with
the gyroscope and carries a holographic foil. Tokens: `motion.tokens.js.gyro`
(motion) + `recipes.cardShimmer` (the five layers). It **never springs** —
rules/motion.md gate 4; `gyro.follow` is per-frame damping, not an easing.

**⚠ ON A NEAR-WHITE SURFACE, ONLY `multiply` TINTS.** Measured side by side
against the real artwork: screen, color-dodge, overlay, hard-light and
soft-light are all no-ops on white. My first build used color-dodge and the
shimmer was invisible. One `screen` pass survives, for the card's DARK features
only. If you ever put this on a dark surface, it inverts.

**⚠ A FILLED ANIMATION OUTRANKS EVERY DECLARATION.** `pgin` has `fill:both`, so
it pinned the card's `transform` and the tilt could never apply *at any
specificity*. Anything that owns its own transform must be EXCLUDED from `pgin`
(`.dmx` and `[data-tilt]` both are). Specificity is not the fix here — this is
the cascade's animation origin, which sits above normal author declarations.

**⚠ `translate(%)` resolves against the ELEMENT, not its parent.** The shimmer
layers are 1.9× the card, so a 42% travel moved the highlight 80% of the card
and off the edge. Divide by `cardShimmer.layerScale`.

**Colour exception:** the rainbow is the only colour in first run. Flagged in
`recipes.cardShimmer`; `holoOpacity` is the single strength dial.

⚠ **The reference video was never seen** — X returns 402 without auth. The
effect is built from the owner's written description; if it is wrong, that is
why.

---

## Read this first — 2026-08-19 (9)

**FOUR icon registers, and the small one has a hard ceiling.** Small UI is
**Lucide, ≤24px only** (`design-elements/icons/`, ISC), consumed by
`icon(name, px)`. Engraved 77px, 3D renders and illustrations are separate and
**must not** be touched by it — owner's explicit boundary. Full table and gates
in `.claude/rules/design-system.md`.

**⚠ NEVER pass `icon()` a class that already carries geometry.** Grep the class
for `width:` / `height:` / `clip-path:` / `border:` / `border-radius:` first.
This bit twice on day one: `.ic-i` drew its own ring (would have doubled the
glyph's circle) and `.sr__lock` set a size (would have overridden the glyph's).

**⚠ `.sig` IS THE PHONE'S STATUS BAR, NOT A SIGNAL METER.** The Wi-Fi row meter
used that class and inherited `clip-path:polygon(…)` from the device chrome —
so the clip-path was what rendered, at one fixed shape, and the per-network
strength was silently discarded. The meter is `.sigm`. Status-bar glyphs are
outside the icon register entirely; they imitate iOS, not NOMA.

**Small icons are INLINED so they inherit `color`.** Engraved glyphs stay
background-images because they don't need to. Don't cross those.

**Not Lucide, on purpose:** brand marks (Apple/Google/wordmark — Lucide has no
brand logos and a lookalike trademark is a legal question), the key card's
owner-supplied edit glyph, artwork, and form controls (`.rad`/`.chk`/`.tog`
have states → stay CSS).

⚠ `.ri` (the leading square on generic `rows()`) is still a grey placeholder.
Filling it means inventing a glyph per row, not converting one — owner call.

---

## Read this first — 2026-08-19 (8)

**THE KEY CARD IS A PERSISTENT ELEMENT (`KH`, class `.khero`).** Created once at
boot beside `.phero`, moved by transform, never re-created. Three states:
`hidden` before node 5a, `parked` top-right at 0.2× from node 5a to D1, and
`slotted` where a screen declares `[data-kslot]` (only D1 does). `placeKey()`
runs from WIRE_JS on every screen change; a screen with no slot means "stay
parked", not "hide" — that is the difference from `placeHero`.

**It HANDS OFF at the door, it does not become the door's card.**
`wireDoorKey` drags a real element and hit-tests it against the lock, so that
must stay a normal node inside the screen. The mini flies to its rect, the real
card fades up under it, the mini retires (`live="2"`). If you touch either,
keep the hand-off: putting drag physics on `KH` would break the lock test.

**Three key cards can exist at once** — node 4's, the door's, and the mini.
`paintCard(card)` is the single paint for all of them; call it for `KH` too on
any PROFILE change or the corner card shows a stale name. `wireProfile` is
null-safe on `scr` because `KH` has no screen.

**`KH`'s markup is `keycard()` injected as JSON into RUNTIME_JS** — not a
simplified copy. Don't fork it.

⚠ **morphicons (github.com/guillermolg00/morphicons) is NOT an icon pack** —
checked 2026-08-19: it ships THREE SVGs, all its own logo, and zero icon path
data. It is a morphing engine for icons you supply from Lucide/Tabler/
Heroicons/Iconoir. Nothing was installed; the owner was told and asked which
direction they actually want.

---

## Read this first — 2026-08-19 (7)

**The key card's entrance belongs to NODE 4 ONLY, and it takes TWO guards.**
`profile_page()` is shared by node 4, node 5, node 5's error state and node 4a,
so it takes an `enter` flag that only node 4 passes — that answers *"here?"*.
`cardEntered` in PROFILE_JS answers *"again?"* for a return visit. They are
independent: the once-per-run flag alone still played the flip if you loaded
`#A5` directly. Don't collapse them into one.

**Gate BOTH halves together.** The card flipping down and the fields rising are
one entrance, so `wireProfile` strips `pgb--enter` alongside `kcard--enter`.
Stripping only one leaves half an animation replaying, which looks worse than
either whole.

**The flip is a hinge, not a tilt:** `transform-origin:50% 0%` +
`rotateX(-95deg)` + a releasing `translateZ`, so the card stands edge-on and
lays down onto its own footprint. Keep the translate short — `.pgt` does not
clip on card screens, so a long travel flies the card over the nav.

---

## Read this first — 2026-08-19 (6)

**⚠ NEVER EDIT THIS FILE WITH `s[s.index(a):s.index(b)]` SLICE REPLACEMENT.**
It deletes everything between the anchors, including rules you never looked at.
Twice in one session this silently removed working CSS — the base `.dmx` group
once, and the entire `.inf` loader block plus `.ksucc`'s card-settle and caption
keyframes the second time. **Missing CSS builds perfectly**, so the build tells
you nothing. Use anchored exact-string replaces, and after any structural CSS
edit run:
`git diff HEAD -- <file> | grep '^-'` and check every removed selector still
exists somewhere. That audit is what caught it, via the reduced-motion gate
flagging `.inf__d` as uncovered.

**⚠ A TRANSFORM CREATES A CONTAINING BLOCK.** `.scr.in .pgt>*:not(.pslot)`
gives every direct child of the visual half a `pgin` transform, which means an
absolutely positioned descendant of one of those children **cannot escape it**,
whatever insets you give it. That is why node 5a's dot matrix stayed clipped
through two passes of padding arithmetic. The fix was structural: `dotmatrix()`
emits a SIBLING backdrop, not a wrapper, and `.dmx` is excluded from `pgin`.
If a full-bleed layer ever looks stuck inside a box, walk the parent chain and
check for transforms before touching padding.

**The key card's entrance is once per RUN** (`cardEntered` in PROFILE_JS).
Screens are rebuilt from stored HTML on every visit, so any "play once" class
arrives fresh each time and must be stripped — done in `wireProfile`, which
runs in the same task as the appendChild, so the animation never starts rather
than being cut off. `reset()` clears the flag.

**The edit glyph and everything else on the key card is a PERCENTAGE of the
card**, never px — that is what survives the 0.9× scale. The owner's 4px gap is
converted once against the card's 264px width (4/264 = 1.515%).

**`inset:0` resolves against the containing block's PADDING box**, not its
border box — which is why node 5a also needs `.scr:has(.ksucc)` to zero the
screen's side padding, and why `.sbar` then needs its 22px back explicitly or
the clock clips to ":41".

---

## Read this first — 2026-08-19 (5)

**⚠ `wireLoad()`'s ADVANCE IS UNCONDITIONAL — KEEP IT THAT WAY.** It used to
open `const bar = …; if (!bar) return;` with the timed hand-off inside the bar's
branch. Node 15 has no button, so the moment its progress bar was swapped for
the indeterminate loader that screen became a permanent dead end. The wait is
the contract; whatever is drawn during it is decoration. Proven: a bar-less
holder arms 1 timeout, one with a bar arms 2.

**Node 15 has NO progress bar.** `prog()` and `.pb` are deleted. A bar claims
knowledge of the remaining time, and that one filled in 10s while the work
takes 15–20. `infloader()` generates a lemniscate and *measures* it, so the
dash derives from real arc length. Don't reintroduce a determinate bar unless a
screen genuinely knows its duration (`wireLoad` still supports one).

**The dot matrix (`dotmatrix()`) is one component on nodes 5a and 16.** Two
copies of the same grid — light at rest, darker masked to an expanding annulus
— so the ring reads as the dots lighting up. `@property --dmr` is load-bearing:
a bare custom property will not interpolate. Greys and white only.

**Node 24's illustration is owner SVG, parsed not transcribed.** `_geofence()`
strips the green dot from the plate so it can animate, and reads its geometry
from the file. It ASSERTS — a re-export with different dot markup fails the
build rather than shipping two dots. Fix the parse, don't delete it.

**The key card's 0.9× scale and the flip's -44px travel are a PAIR.** `.pgt` no
longer clips on card screens (the card is allowed to overflow rather than be
cropped), so a longer flip travel would send the entering card over the nav.
Changing either without the other breaks it.

**Node 18a has no contacts list.** So `KEY_CONTACTS`' hue-coded avatars are
unused there — that palette flag is closed by deletion, not decision — and
`wireKeys`' pill path is unreachable, so the CTA no longer counts. Wiring kept
deliberately for a future picker.

Every new animation is in a `prefers-reduced-motion` block; verify by parsing
those blocks, not by reading.

---

## Read this first — 2026-08-19 (4)

**⚠ NEVER DECLARE A BUTTON IN `build-prototype.py`. READ THE RECIPE.**
That file predates the token loader and carries raw hex; `build-auth.py` reads
`recipes.*`. Two stylesheets describing the same controls is how `.cta` came to
be a flat **#0B0B0B** while the sheet's `.s-cta` was the ink **gradient** with a
drop shadow — and why node 5's OTP CTA looked like a different button. All of
`.cta` / `.cta2` / `.qlink` / `.nb` / `.chip` / `.rs__t` / `.tog` / `.chk` /
`.rad` / `.pcard` now read the recipes in that file's token-driven append block
(at the very end, after the dialog rules). Add new controls there, not inline.

**THE THREE CTAs** are the sign-in sheet's, and they are the reference:
primary = ink gradient `#3A3A38 → #2E2E2C` h54 `dock`; secondary = `#FFFFFF` +
1px white inside stroke h46 `control`; tertiary = no container, no shadow.

**`--ink` (#0B0B0B) IS NEVER A FILL** — owner's explicit rule. It is the text
colour. Dark surfaces take the ink gradient. ⚠ When you fix one, **grep
`background:var(--ink)` and fix the set**: three separate components had their
own copy of that fill (`.chip.on`, `.tog.on`, `.rs__t.on`) and the owner had
named only one of them. Small dark marks (signal bars, carets, dots) stay ink.

**ONE BACK BUTTON.** `recipes.buttonIcon` — 40px, `#F8F8F8`, **1px `#FFFFFF`
inside stroke**, two-layer shadow — and one glyph, `BACK_SVG`, shared by `nav()`
and `sheetback()`. The inside stroke is what makes it read as glass; dropping it
is what "ruined" it. The owner has said this style is **locked**. Do not restyle
it.

**Top-aligned pages get a REAL nav bar** (`position:static`, reserves its own
height). Do not buy clearance with a `min-height` spacer on `.pgt` — that was
tried and broke on pages with no visual half.

**Engraved glyphs are PAGE HEADERS ONLY, at 0.8×** (77px; Wi-Fi 83×77). A list
row gets a plain monoline mark — the engraved render at 30px reads as a smudge.

**⚠ C-15 IS OPEN** (`memory/decisions.md`): a selected chip FILLS (owner's
instruction) but a selected card LIFTS (LAW 3, which forbids the fill). Both are
built. Needs one owner call — do not "tidy" it in either direction without one.

---

## Read this first — 2026-08-19 (3)

**⚠ IF YOU ADD AN ANIMATION TO `.pgb` OR TO A `.pgt` CHILD, READ THIS FIRST.**
The generic page transition is `.scr.in .pgb, .scr.in .pgt>*:not(.pslot)` —
**(0,3,0)**. Anything weaker is silently overridden and **never renders a
single frame**. That is what happened to node 4's card flip and field rise
this session: they were (0,1,0) and (0,2,0), so `pgin` won and both looked
like they simply "weren't there". `getAnimations()` reported `pgin`, not
`kcardIn`. They are now `.kcard.kcard--enter` / `.pgb.pgb--enter` under
`:is(.scr.in,.scr.bk)` = (0,5,0), winning on weight rather than source order.

**This is the THIRD such collision in this file** — `.pgb p` (the eyebrow
reset), `.flow-thumb-frame` (the blank Vercel embeds), now `pgin`. When
something new "doesn't show up", measure the cascade before touching the
code: `el.getAnimations()` for animations, and enumerate `document.styleSheets`
for a matching rule, exactly as with the `.done`/`display:none` bug.

**Screenshots are not proof for animations.** A first pass here wrongly
suggested the flip was fine because headless had rendered the settled end
state. Pin `currentTime` via the Web Animations API and read the computed
transform.

**The prototype's ground was the stale one.** `:root --grad` painted a cool
radial to `#A4A4A4`; `build-onboarding.py` (the previous first run) and
`build-flow.py`'s re-skin were both already on `gradients.canvas`. Same
screens, two grounds, depending on which rendering you opened. Now read from
the token via `__CANVAS__` in `css_out()`. If you touch `:root`, keep it
token-driven.

**List pages are top-aligned now** — `pgb(top=True)` on P1, P5, W1, R1, R2.
Bottom-pinned, a growing list pushes the icon and heading up (measured 125px
on W1). Any new list page should pass `top=True`.
⚠ SUPERSEDED BY (4): the `min-height:46px` spacer described here was replaced
by a real in-flow nav bar the same day — see the entry above.

**Confetti (node 5a) is a burst**, white only, and needs its drop shadow to
exist at all — the ground starts at `#FFFFFF`, so white-on-white is invisible
without it. It also has to sit ABOVE the card (`z-index:1`); behind it, the
card's artwork hid most of the pieces.

---

## Read this first — 2026-08-19 (2)

**Email and phone swapped roles in the account section (nodes 1-5), and node
4 gained two new branch states.** Owner: login should lead with Apple/Google,
phone verification moves to the setup-profile page inline, and that page
needed "some fun things."

- **A1** (node 1): Apple (black CTA) / Google (white CTA) / email (tertiary
  link) — real icons this time, not hand-approximated. Apple/Google skip
  straight to node 4 (`handoff="A4"` — a federated login has already
  verified the person). Only email walks A2 → A3.
- **A2/A3** (nodes 2/3): same shapes as the old mobile-number/mobile-OTP
  steps, now for email — build-auth.py's docstring explains the swap in
  full.
- **A4** (node 4): still the master-key page, but the second field is now
  **mobile number**, not email, with an inline "Verify" pill that opens
  **A5** (node 5, a sheet-over-A4 — same relationship node 5 always had,
  different contact method). Continue is disabled until verified.
- **A4V** (branch 4a, NEW): the verified snapshot — checkmark, Continue live.
- **A6** (branch 5a, NEW): "Key card created" — all-white confetti (owner:
  no colour), card settles to centre, auto-advances into pairing at 1.8s.
  Reduced motion skips the confetti and uses a 900ms timeout instead.
- Node 4's entrance is new too: the card drops in rotated from above while
  the fields rise from below, same duration/easing so they visibly converge
  ("meet in the middle"). Scoped via a new `cls=""` param on `keycard()` and
  `.pgb:has(.fld--verify)` — neither touches the two shared helpers' default
  behaviour for every other screen that calls them.

⚠ **No green accent was introduced** for the Verify pill/checkmark — this
file has never had one, and the two-green palette question in
`.claude/rules/design-system.md` is still open. Ink only, on purpose.

⚠ **Caught by the gates, not by eye:** A1's `au_state()` call was missing
`handoff="A4"`, leaving a real dangling `data-go="DONE"` in the merged flow
that the automated link check caught. Two new notes used `<b>` tags — the
note panel renders via `.textContent` everywhere in this file, so those
would have shown as literal `<b>` text; fixed to plain text, matching the
file's one actual convention.

Node count: 21 main-line + branches 4a/5a/18a = 24 (was 22). Screens: 41
(was 40). All four renderings rebuild clean; voice gate clean; zero dangling
targets.

---

## Read this first — 2026-08-19 (1)

**2026-08-19 — the card design, and corner smoothing is now REAL.**
⚠ **Supersedes the 2026-08-18 note below**: `radius.smoothing` is no longer an
intent. It is **1.0** (the owner's 100%), and the prototypes render the true
superellipse via `docs/_squircle.py`, which ports Figma's own corner geometry
and emits it as a **9-slice mask** — it restretches at any element size, which
is why it works on a sheet whose height changes every state.

**`recipes.largeSurface` is the new card design** (Figma inspector): radius
**34** (`radius.xxxl`), 100% smoothing, #F9F9F9 under a 24% gradient, **1px
#FFFFFF INSIDE stroke**, drop shadow. Applied to the sign-in sheet, the OTP
sheet and the permission dialogs.

**Three things to know before touching it:**
1. **A large surface is TWO elements.** A mask clips everything an element
   paints, shadow included — so the shell carries the shadow (its
   `border-radius` exists only to shape it) and a masked child carries the fill
   and hairline. One element loses the shadow entirely.
2. **Nothing under 136px may take it.** The corner needs 68px of edge, so two
   need 136 between them; below that they overlap and the shape bulges.
   `SQ.min_size()`. This is the arithmetic behind the owner's "not on smaller
   cards" rule.
3. **Data URIs in this codebase go UNQUOTED.** A quoted one ends an inline
   `style="…"` attribute and silently masks the element to nothing.

**Type, from the same inspector:** sheet wordmark **56 @ 50%** (was 84 full),
`display` **28/600** (was 30/700), new `action` 14/600 · `actionSmall` 12/600 ·
`legal` 10/400. Page-level `.cta` was extended to the same register so the
label does not jump at sheet→page hand-offs.

**Vercel pages were blank** because the two spec embeds reused the THUMBNAIL
classes — `position:absolute` + `scale(.29)` + `pointer-events:none` survived
the inline overrides. Now `.flow-stage` / `.flow-frame`. Third generated spec
added: **Large surfaces** (`docs/design/large-surfaces.html`), mirrored to the
design system alongside Sizing & rhythm and Spacing scenarios.

⚠ **Open owner call**, recorded in `recipes.dialog`: the permission alerts now
read as NOMA surfaces. The flow's docstring argues they are truthful *because*
they are the system's dialogs — branding them trades accuracy for consistency.

---

## 2026-08-18

**2026-08-18 (10) — ⚠ a specificity bug had closed the eyebrow→heading gap.**
The UA margin reset was `.pgb p` (0,1,1), which out-specifies `.eyb`/`.lab`
(0,1,0) and zeroed the rhythm margins it was meant to protect. Now
`.pgb p:not([class])`. **A margin reset is a cascade weapon — scope it to
unclassed elements; do not raise every component to out-shout it.**
New: `radius.smoothing` 0.6 (iOS-style, ⚠ an INTENT — CSS cannot render a
superellipse corner; it exists so the native build uses `.continuous`), and a
second generated spec `docs/design/scenarios.html` covering twelve adjacencies,
mirrored to the Vercel design system as **Spacing scenarios**.

**2026-08-18 (9) — owner redline applied; sizing tokens + a generated spec.**
The sheets were over-spaced because `<h1>`/`<p>` UA margins stacked on the
rhythm values (~20 around the title, ~19 under the countdown). Zeroed at the
component root. New tokens: `rhythm.titleGap` 18, `rhythm.controlGap` 8 (was
12), `layout.ctaHeight` 54, `ctaQuietHeight` 46, `sheetPadX/Y` 20/24,
`otpBox` [56,52]. Node 1 now measures 12/18/8 exactly.
⚠ **The redline adds "Continue with email"** — a THIRD sign-in route, reversing
that screen's own "two ways in and no third" and letting a user skip phone
verification entirely. Built as drawn, routed to node 4; where it rejoins needs
an owner call.
**Spec page:** `docs/design/build-sizing-dashboard.py` generates
`sizing-and-rhythm.html` FROM the tokens (so it cannot drift) — published as an
artifact and mirrored to the Vercel design system under Sizing & rhythm.

**2026-08-18 (8) — merge fixed structurally; rhythm + input tokens. ⚠ NOT
PUSHED yet (owner reviews tokens first).** The swap is one paint — old removed
and new appended in the same task — and only the new screen's CONTENT animates;
one `.scr` in the DOM at every instant. New tokens: `rhythm` (textGap 12 /
sectionGap 24 / controlGap 12, grounded on Airbnb+CRED via Mobbin) and a rebuilt
`recipes.input` (flat white, r8, 1px #000@12%, h52, inner shadows — from the
owner's Figma inspector). `layout.inputHeight` 56→52. Applied to sheet + pages +
flow re-skin. ⚠ Flex columns don't collapse margins — boundary corrections on
`.bd+.lab` and `.fld+.lab`.

**2026-08-18 (7) — the transition flash is gone.** Both layers were fading at
once, so mid-transition you could see the phone's ground THROUGH both. The
outgoing screen stays opaque now and is simply covered. Two real bugs found
while testing it: the outgoing screen kept its `in` class with the fade
mid-flight (so a FAST tap brought the flash back — verified at 100ms), and its
removal timeout rode `touts`, which `clearTimers()` empties every render, so
dead screens lingered. Both fixed.

**R1 reordered** (title/body → home name → room chips → drawing last). ⚠ Node 17
is now the ONE screen that does not follow the flow-wide structure —
illustration last, not first. **Node 18 is one Continue**, so the invite-vs-skip
branch moved to node 18a, where "Not now" is a new tertiary style (`.cta3`, no
container). Key card 0.8× (151px) with the visual half's clip released so the
tilted card is not cut. The key toast auto-advances.

**2026-08-18 (6) — ONE purifier, moved.** The pairing flicker was a repaint:
each screen built its own render element and the runtime FLIPped between them.
There is now a single `.phero` created at boot and parked outside the screens;
pairing screens carry invisible `.pslot` boxes and the runtime moves the one
element by transform. One `.phero`, zero `.rnd` in the document. It sits BELOW
the screens (z-index 1 vs 2) because node 9's light and node 10's phone must be
in front. **40 screens, 27 happy path, 22 nodes.**

Also: the 1px-stroke buttons had default/hover inverted (bright at rest now,
darken on press); **node 14 is gone** (⚠ the only Wi-Fi password screen — a
stale credential now has only the W2E edge state); **node 15 has no CTA** and
auto-advances after a 10s CSS-driven bar; **engraved icons** are a third
register in `design-elements/engraved-icons/`, mirrored to the Vercel design
system, replacing node 16's tick and node 25's bell; node 18a's key is 0.8× and
**R3C is deleted** in favour of a toast.

⚠ The icon gate's "two tiers" is now wrong as written. ⚠ The notifications glyph
carries a non-palette `#FF4444`. ⚠ R3C carried the roster — pending invites have
no representation in first run now.

**2026-08-18 (5) — the page-to-page jerk is fixed, and node 18a is a picker.**
The jerk was **not a lag**: the carry decision happened after the screen was in
the DOM with `.scr.in` applied, and measuring forces a recalc — so every FLIP
was read through the slide's `translateX(10px)`, started 10px out and snapped.
`carryClass()` decides from the markup before the element exists. The carry is
generic now (`data-carry`): `pur`, `bg`, and `sheet` — the sign-in sheet used to
replay its 880ms rise on every step, which was the splash→login jerk; it now
rises once and grows in place. Assets are decoded at boot, not mid-transition.

Node 13's list has a real padlock and a 4-bar signal meter (4/3/2 per network),
as SVG — CSS div gaps fell sub-pixel under the harness's phone scale. ⚠ Tight at
review scale, correct at 1×.

Node 18a: removable pills, the list drops picked contacts, CTA counts
("Share key" → "Share keys (2)"). ⚠ Body dropped "you decide what each key
opens" — the disclosure gap is now unspoken as well as unbuilt. ⚠ Hue-coded
avatars are back (palette reversal, same as the SKU tiles).

**2026-08-18 (4) — scan pages merged; the white flash is gone.** Nodes 11 and
13 each absorbed their spinner screen: one page, large owner glyph, and a live
list where the count climbs from (0) as results arrive. **42 screens, 29 happy
path, still 23 nodes.** The inter-screen white flash is fixed at its root — the
harness used to remove the old screen before appending the new one, leaving a
frame with no screen at all; it now appends first and cross-fades. Patched in
all three mount functions.

⚠ **Node 11 lost "Identify"** (blink the light). The reference shows two
identically-named purifiers on purpose — the pair-buying household — and signal
strength alone cannot tell them apart. Must come back before build. PRD §5.17.
⚠ **Node 13 now precedes node 12** (the merge took 12's fetch half), and
auto-fetch's original argument is spent. PRD §5.16, §5.17.
⚠ **THIRD class collision this week.** `.scan` (QR viewfinder) and `.done`
(sign-in end card, `display:none`) both silently swallowed the new scan list.
**State classes get a component prefix now** — `.slist--done`, not `.done`.
Diagnose by enumerating `document.styleSheets` for matching `display:none`
rules, not by reading CSS.

**2026-08-18 (3) — the chosen purifier is CARRIED through pairing.** Pick a SKU
on node 6 and that device flies from the tile through nodes 7, 8, 9 and 10-11
as one FLIPped element; `PICK` persists, so a 500 keeps its own silhouette and
its own light position throughout. Node 9's light is now ON the device, pinned
to `--ledy` (measured per SKU: 200 at 39.7%, 500 at 19.2%, MAX at 19.8%). Node
10-11's phone dissolves downward via mask-image instead of a hard edge.
**W1 now precedes P7B** (P7 → W1 → P7B → W2) — ⚠ which weakens node 12's own
reason for existing, since it was built to make the list unnecessary; see PRD
§5.16 for the tension and the shape that would restore it.

⚠ **Carrying screens must not slide** — `.scr.carry` removes the screen
animation, or a translating parent drags the hero and fights the FLIP.
⚠ **Custom properties only inherit downward** — `--ledy` belongs on the screen,
not the render, because the glow is the render's sibling.

**2026-08-18 (2).** Node 5's sheet condensed 54% → 46%. **Nodes 10-11's
Bluetooth screen is redrawn in markup** so the toggle actually flips on (the
supplied PNG couldn't animate); it depicts iOS and carries iOS colours. Node
25's bell is a real SVG bell with rings and a red badge. ⚠ Found and fixed a
**stale claim in build-flow.py that the palette has no red** — untrue since
2026-08-13, and it was why all 13 edge screens rendered their error colour as
ink. They carry `status.negative` now; warning stays ink (O-6 half-open).
⚠ **Headless Chrome does not tick CSS animations** — pin `currentTime` via the
Web Animations API to screenshot keyframes, or everything looks frame-zero.

**2026-08-18 — fine-tweaks.** Bluetooth scene on nodes 10-11 is the owner's
real iPhone mock over the render (`design-elements/renders/bt-phone.png`);
node 4's card sits 20px lower; the sign-in sheets are condensed (~0.85× —
the 56pt CTA and 30pt title tokens are the floor to go further; owner call);
nodes 7 and 8 have looping animations (bag slides off / rocker flips, light
blooms); **hold-to-pair is REMOVED** — node 11 closes with a device-left /
phone-right connection animation that resolves itself and auto-advances
(structure from the owner's NoiseFit reference, visuals ours). All simulate
buttons are gone from every page (previous session, same day-cluster).

## Previously — 2026-08-17

**First run's first five nodes are a bottom sheet now.** Owner supplied seven
frames; `docs/features/first-run/auth-prototype.html` (built by
`build-auth.py`) replaces the five full-screen account pages with six states
on one surface: splash · login sheet · mobile number · mobile OTP · email ·
email OTP. It is interactive, not a board — type a number, type digits, watch
the countdown run out. Every state is addressable by hash (`…#A3`), which is
how to screenshot or link one. **Nothing from node 6 onward changed**;
`onboarding-prototype.html` and `first-run-prototype.html` still own the rest.

⚠ **The background image is a drawn placeholder.** Drop a real file at
`docs/features/first-run/assets/first-run-bg.jpg` and re-run the build; it gets
embedded with no code change and the build prints which one it used. Owner
says this becomes a video later, so nothing in the layout depends on it being
still.

⚠ **Four spec changes arrived with the frames. One needs an owner today:**

1. **Node 4 no longer collects a display name.** It is an email field and
   nothing else. *Nothing anywhere in first run now collects the name the
   household sees next to a member* — and node 18a, invite family, is
   downstream of it. This is a product hole, not a layout question.
2. **The DPDP notice moved to the login sheet's fine print.** §5.1 was already
   open and unanswered; this changes where its answer has to land.
3. **The country selector is gone**, +91 hardcoded.
4. **Node 5 verifies with a code, not a link** — so §5.2's "two verifications
   before the box is opened" now costs two code entries, not one plus a tap.

Two things in the frames were reproduced exactly rather than corrected,
because the instruction was to follow them exactly, and both should be the
first things fixed: **the mobile OTP state still carries the "What's your
mobile number?" heading** over a code field, and **nothing between nodes 2 and
4 has a way back** — a mistyped number strands you, though node 5 has both a
back arrow and "Edit email". Full argument: PRD §5.11.

Two deliberate divergences, both flagged in the build: `Edit email` uses
`colors.text.accent` rather than the frames' brighter green (outside the
palette, and it would not clear AA as text), and the *"We've sent an OTP
to …"* line wraps to two where the frames show one, because Google Sans Flex
sets it wider than the mock's face did.

**`audit-voice.py` covers the new surface and all six are machine-clean.** It
gained three proper nouns (`Apple`, `Service`, `Policy`) and one harness key
(`note`) — see `memory/changelog.md` for why each is a false positive rather
than a loosened gate.

**Same day, follow-up — the real wordmark is in.** `design-elements/brand/`
holds the owner-supplied NOMA logo (source PNG + WebP derivative + manifest,
same shape as `3d-icons/`), and `auth-prototype.html` now embeds it at both
placements instead of letter-spaced CSS text. Display width is a new token
pair, `layout.wordmarkSplash`/`wordmarkSheet`. ⚠ **The older 45-screen flow's
node-1 door screen still uses the CSS-text mark** — left alone on purpose,
since that screen's animation was tuned over several owner passes and an
image swap there is a real edit, not a drop-in. Flagged in
`design-elements/brand/README.md` for an owner call.

**Same day, eighth follow-up — real renders + the resident's key, and the
simulate buttons are gone.** `design-elements/renders/` holds the three SKU
renders (1200px working copies; owner keeps the 5-32 MB masters). Node 6's
thumbs are the real 200/500/MAX; nodes 7, 8 and 10-11 compose the render into
their scenes; node 9 stays drawn (owner call). Node 18a's key is now the
generic RESIDENT'S KEY artwork (`design-elements/brand/resident-key.png`),
used as is — nothing personalised on it. ⚠ `build-flow.py`'s re-skin had been
silently re-tinting node 6's tiles green over the owner's hue-coded frame;
that override is removed and the conflict lives in one flag. All simulate
buttons removed (10 calls + helper + CSS); six edge states are now rail/hash
reachable only.

**Same day, seventh follow-up — keys for the household, and the flow ends at a
door.** Node 18a sends KEY CARDS now, not invites (blank member card on R3, the
sent card carries the name on R3C). **C1/C2/C3 are REMOVED** — 44 screens, 31
happy path, still 23 nodes; what died with the tour (privacy receipt, agent
intro, the only roadmap mention) is in **PRD §5.14**. The finale is `D1`: a
closed door and the node-4 key card — drag it to the lock, tap it, or Enter;
the door opens into Home. Node 4's card also sits 24px lower, clear of its
title.

⚠ `D1`'s lock is beige from the owner's reference (non-palette hue on a
depicted object — same open call as the 3D icons), and the screen has no CTA:
one tap is the toll. ⚠ `A4E`/`A5E` are orphan states now that nodes 4 and 5
lost their simulate buttons — rail/hash reachable only.

**Same day, sixth follow-up — the sheet stops at phone verification; node 4 is
the MASTER KEY page.** Nodes 1-3 are the sheet. Node 4 is *Setup profile*: name
+ email, and a card that is the profile and the key to the home. Node 5 left
the sheet too and is a normal page. Full argument: **PRD §5.13**.

**Node 5 is a sheet OVER node 4** — the profile page stays behind it, dimmed,
so the card is still visible while you confirm the address on it. Same `.sheet`
component as nodes 1-3; one sheet, two grounds.

**The flow is interactive now.** `field()` is a real input across all four
renderings (it was a span with a fake caret), node 5's code boxes take digits,
and node 4's card is fully bound — name, email, avatar initials, serif initial,
plus a real picture off disk. State survives leaving the screen and returning.

⚠ **The display name is back**, closing the hole §5.11 opened this morning:
nothing in first run collected the name the household sees, and invite-family
is downstream of it.

⚠ **Instrument Serif is vendored for ONE glyph** (`src/fonts/instrument-serif/`,
SIL OFL). The card's initial. Not a second body face.

⚠ **`build-first-run.py` and `first-run-complete.html` are deleted** — the
wrong-flow merge, and after the sheet lost A4/A5 it silently built a flow that
skipped the profile page. `first-run-flow.html` is the one that ships.

⚠ **Two duplication bugs fixed and worth remembering:** the component-dispatch
list existed in three renderings (wiring a new component in one did nothing in
the others — now one `WIRE_JS`), and CSS class names collide across the two
builders, where scoping alone does NOT protect you: an unscoped rule's other
properties still apply. Namespace, then re-check.

**Same day, fifth follow-up — EVERY first-run screen is bottom-aligned now.**
Four more owner frames (nodes 6-9) set a page structure and the instruction was
to apply it flow-wide: circular back arrow floating over a visual that takes
the leftover height, then eyebrow / title / body / CTA pinned to the bottom.
All 46 screens converted, via `pgt()` / `pgb()` / `eyb()` in
`build-prototype.py` and a `.scr:has(.pgb)` switch. Titles run at 26px here,
not the sheet's 30 — measured off the frames. Full argument: **PRD §5.12**.

⚠ **Things that were deliberately lost, and are worth a look before build:**
the close (×) and with it the exit-setup hatch; the 4-dot stepper; **node 7's
peel gesture** (`peel()` still defined, now unused); and node 9's hold-to-reset
recovery, demoted from an on-screen note to a "Not blinking?" link into P3F.

⚠ **"Not now" is a text link now, not a button** — including on both permission
asks (nodes 24, 25), where it was a full-size `buttonQuiet` *because* declining
has to stay first-class. Flow behaviour is unchanged; the hierarchy is not.

⚠ **Hue-coded SKU thumbnails are back** (node 6, blue/teal/olive), reversing
the 2026-08-12 palette rule. Built as the frame shows; three CSS rules to
revert. Two owner instructions in conflict — needs the owner.

**Same day, fourth follow-up — nodes 1-5 are now in the CANONICAL screen set,
which is what the Vercel flow serves.** `build-prototype.py` imports the sheet
states from `build-auth.py`, so all four renderings carry the new sign-in from
one edit: `first-run-prototype.html`, **`first-run-flow.html` (the file behind
`noise-apps.vercel.app/#noma/userflows/first-run`)**, the flat board and the
export. 45 → 46 screens, 32 → 33 on the happy path, still 23 nodes. The Vercel
mirror at `~/Desktop/noiseFit/flows/noma/exploration/onboarding/` and that
dashboard's screen-count metadata were both re-synced.

⚠ **The drag-to-open door is gone** — node 1's `doorway()`, rebuilt four times
on 2026-08-06 (PRD §5.10, §5.10a-c). Owner instruction, not a failure. The
function is still defined and unused; putting it back is one line.

⚠ **A3E / A4E / A5E are EXTRAPOLATED** — no owner frame covers an error. Drawn
in the sheet language so the flow does not fall back to the old full-screen
one mid-run, but they need an owner pass. `A4E` dropped the old "sign in with
that one instead" button, which was the useful action.

⚠ **`first-run-complete.html` merged the WRONG flow** (the 11-screen spine, not
the 45-screen one). It still builds and is still a useful single-file walk of
sheet-plus-spine, but **`first-run-flow.html` is the one that ships.**

**Same day, third follow-up — the whole first run is one file now, and the
sheet's arrival was slowed.** `docs/features/first-run/first-run-complete.html`
(`build-first-run.py`) walks all fifteen states, nodes 1 to 23, from splash to
the end of setup. It **defines no screens** — both source builders were split
into named CSS/JS parts and it composes them live, so editing `build-auth.py`
or `build-onboarding.py` updates the merged flow. `route()` in auth's runtime
is the hook that lets a different controller claim ids the sheet does not own.

⚠ **Two new motion tokens, and one breaks ADR-005.** `durations.entrance`
(880) and `easings.entrance` (no overshoot) drive the slower, premium opening.
**This is the only un-springy motion in the product**, against ADR-005's
resolution of O-7 — flagged with a TODO(owner) in `motion.tokens.js`. Reverting
is a two-value edit.

⚠ **The merge makes C-14 concrete.** Nodes 1-5 are photographic and greyscale;
nodes 6-23 are white with green illustration plates. Walked end to end they do
not read as one product, and the seam sits exactly at P1. Nothing was changed
to hide it. `first-run-complete-sheet.png` is the strip to look at — this is
the strongest evidence yet for a palette decision open since 2026-08-12.

**Same day, second follow-up — the background is the real photo now, not the
drawn placeholder.** `docs/features/first-run/assets/first-run-bg.jpg`
(architectural render — pitched roof, foggy sky, lit doorway, reflecting
pool) replaced `bg_plate()`'s SVG drawing across all six states, through the
swap point that was already built — no code change, just the file and a
rebuild. `bg_plate()` remains as the fallback if the file is ever removed.
Provenance and replace-it steps: `docs/features/first-run/assets/README.md`.

## Previously — 2026-08-14 (2)

**`design-elements/3d-icons/` exists and is EMPTY of images.** It has a
manifest and README naming four tier-1 icons (info, appearance,
notifications, family), but zero actual image files. They were pasted into
chat and no available tool can write a pasted image's bytes to disk — that
is not a task left undone, it is a real tool gap. **Save the four PNGs into
that folder** with the filenames the manifest already specifies
(`info.png`, `appearance.png`, `notifications.png`, `family.png`), then the
registration pass (index row → verify → Approved Components row) can
finish.

This also puts a name on a real two-tier icon system for the first time:
tier 1 is 3D, reserved for high-visibility moments; tier 2 is the flat
22-icon set already running in `_kit.py`, which turns out to have never
been registered in `design-system.md`'s gate either — fixed alongside this.

⚠ Two open calls, both flagged in the folder README rather than decided:
whether `appearance`/`notifications`'s real-world colours are exempt from
the product's own two-green palette rule, and whether the new 3D icons
*replace* the existing flat `bell`/`palette` icons on the same settings rows
or sit beside them.

## Previously — 2026-08-14

**The voice has a canonical document and a CI gate.** `docs/voice/noma-voice-guide.md`
(v1.2-draft) is now the single source of truth for every string the product
speaks. It supersedes `docs/voice/voice-prd.md`, which is kept only so old
§-number citations stay traceable.

**Run this before shipping any copy:**

    python3 docs/voice/audit-voice.py

It implements the ⚙ machine-checkable rules from §12 and exits non-zero. All
five prototype surfaces are currently clean.

**Three things it will catch that the old register did not:**

- **M-03, em dashes are banned everywhere.** This was the single biggest source
  of violations (41 of 85).
- **W-01, indoor readings are PM2.5 in µg/m³, never AQI.** AQI is legal only
  when quoting the *outdoor* public index, with its source and age.
- **M-06, sentence case**, including preset values: "Living room", not
  "Living Room".

⚠ **Machine-clean is not "passes the voice", and the gate prints that itself.**
§0.1 rule 5 forbids the claim from an audit alone. The human gate (§12 items
8-19, read aloud, standing in the room) has NOT been run on any surface. Sahil
Dhingra and Kaustubh Khade are the arbiters. **No surface is done from belief.**

⚠ **Prototype numbers are fixtures, not readings.** The AQI-to-PM2.5 sweep
relabelled unpaired indoor numbers rather than converting them, because
converting would have invented data (R-17). The device rows now read "73 µg/m³"
where they read "73 AQI". Real values must come from the sensor.

**Still owed, and each blocks something specific:** D-1 (Hindi tum/aap, a launch
blocker), D-3 (freeze token names before the first localized string), D-7
(per-surface character limits, which is why M-18 is not in the gate), D-8
(legally mandated wording per language), D-9 (what one person may see about
another).

## Previously — 2026-08-12

**LATEST OF ALL — the green palette was replaced, the 10% rule is back, and every small
shape has a new finish.** Three owner directions in one session; full detail in
`memory/changelog.md` (6). The short version:

- **`green` is now `lime #AECC2A` / `mint #6CCC7C` / `haze #E9E8E5`.** Everything from the
  `#1D6B27→#3DBE4E` ramp is gone. Outside white and grey, **only these greens and shades
  of them** appear anywhere in the product.
- ⚠ **This is an INK-ON-GREEN system.** Both anchors measure under 2:1 against white, so
  **white text never goes on green** — LAW 2 has a corollary saying so, `accent.onFill` is
  near-black, and the Insurance Card flipped with it. If you find white-on-green anywhere,
  it is a bug, not a variant.
- **LAW 6, the 10% rule, is reinstated** after being dropped four entries ago.
- **Shape dynamics**: a new `effects` export — white inside stroke + drop shadow + inner
  shadow, all three together. Chiclets are **radius 8, not pills**; "Help" is a tinted
  pill; toggles and the segmented meter got chunkier.

**Two decisions are waiting on the owner, and both are visible in the product right now:**

1. **There is no red left.** Destructive rows and all **13 edge screens** in the first-run
   flow lost their error colour and read in ink. Every failure state in the product is
   worse than it was. Pick one: allow a single non-palette red for destructive only (the
   owner's own PM prototype uses `#FF3B30`), or move destructive behind a confirm sheet.
   **This also makes O-6 harder** — the same argument now blocks warning and critical.
2. **SKU thumbnails and household avatars lost their hue coding** to the monochrome rule
   and now separate only by depth. Likely wants real renders/photos.

**Four prototypes now exist, all generated from the token module** (none restate a value;
re-run their build scripts after any token change):
`docs/features/settings/profile-settings-prototype.html` and
`device-settings-prototype.html` — **two different surfaces, do not merge them**; the
rows that look shared (Notifications) mean different things on each. They share `_kit.py`.
`docs/features/first-run/onboarding-prototype.html` (11-screen spine) and
`first-run-flow.html` (**all 45 screens**, controller left, phone right).

⚠ **Known un-migrated:** the 45-screen harness still uses the old outline-SVG
illustrations. There is no CSS route from line art to the framed-gradient hero; re-arting
is a real design task, not a styling one.

## Previously — 2026-08-12

**Latest of all, same day — the Bottom Navigation Bar is live on Vercel, embedded, not
listed.** Owner: "do whatever it takes to get the navigation bar on Vercel." It now has
its own real folder in noiseFit's dashboard (`design/noma/bottom-nav/`), matching Bottom
Sheets' treatment exactly — phone-framed iframe, not a paragraph. The "Components" folder
mentioned three paragraphs down is **gone**; that whole block is now a historical record
of a state that lasted about one merge. Full detail: `memory/changelog.md` (5). Verified
the same way as everything else that's had to work around the login gate: the new files
are static and reachable directly, no login involved, and were opened and exercised
in-browser — scroll-shrink, tap-travel, no console errors. **The dashboard's own SPA
shell, behind the login, still was not** — someone with the password should look once.

**Same day, earlier — a real accessibility bug in the tokens file is fixed, and merged.**
`green.deep` was `#1E8A2E`, which the token file's own comments say fails WCAG AA
(4.44:1 under white); the working tree had the correct `#1D6B27` (6.59:1) sitting
uncommitted for some time. That fix is now committed and merged, along with four
recipes and a `radius.xs`/`sm` split that existed nowhere in git history before
today — `cardSelect`, `cardSelectIdle`, `illustration`, `buttonQuiet`, `segmented`.
No new design direction; this closed drift between what was written and what was
actually committed. Full detail: `memory/changelog.md`.

**Synced onward to the Vercel dashboard**, `noise-design/noiseFit` — that repo's
mirror had been hand-patched with the correct green value ahead of this repo's own
history, which was exactly backwards for a "canonical wins" mirror; it now
legitimately defers to this repo instead of being ahead of it. ⚠ **Historical note,
superseded by the block above:** this merge originally also added a text-only
"Components" folder listing Bottom Sheets and the Bottom Navigation Bar. That folder
no longer exists — Bottom Sheets already had its own real folder by the time this
landed, and the Bottom Navigation Bar has one now too (see the top of this section).
Left here only so the sequence of events still reads correctly, not because any of
it is still true.

**Addendum, earlier the same day — the Bottom Navigation Bar is now a registered
design-system component, and the story below is partly stale.** Three things
changed after the block below was written:

1. **It's registered.** `.claude/rules/design-system.md`'s Approved Components
   gate had never actually been populated — not for this, not for Bottom
   Sheets either. Both are in it now, and `design-elements/README.md` is the
   index. Detail: `memory/changelog.md`, "Approved Components gate populated
   for the first time."
2. **The HTML half is no longer just "built" — it's verified.** Point 1 below
   was true when written; it no longer describes the whole component. Its
   `index.html` was rebuilt twice since (owner feedback: no snap, centred
   pill, no jiggle, flat icons at `#343434`, then a phone-frame mobile
   preview with 16px insets and a 0.8× shrink floor) and was checked in the
   Browser pane with actual frame-by-frame measurement each time, not by eye.
   **The SwiftUI package below was not touched in that process and does not
   have the 16px/0.8× geometry — it still describes the first pass.**
3. **`#343434` for icons is owner-specified and is still not a NOMA token.**
   Sits between `neutral[700]` and `neutral[800]`. Flagged in the component's
   own README as drift to reconcile; nobody has reconciled it.

**The repo now contains native code.** `design-elements/bottom-nav/` is a SwiftUI package —
a minimizable floating tab bar rebuilt from a Kavsoft tutorial the owner supplied. Everything
before this was markdown, tokens, or static-HTML prototypes, so the line in *Current state*
saying "there is **no application code**" is now wrong for this one folder. Full detail in
`memory/changelog.md`; the README carries the derivation and the caveats.

**Three things to know before touching it:**

1. **It compiles and it has never run.** `swift build` is clean under Swift 6 strict
   concurrency, motion gates 1 and 3 pass by grep, and that is the entire extent of
   verification. There is no Xcode on the machine that wrote it — only Command Line Tools —
   so it has **never been executed and never been rendered once**. The SF Symbol names
   (`air.purifier`, `flowchart`, …) are asserted from the catalogue, not resolved by a
   compiler. The README has a table separating verified from unverified; trust that table
   over the fact that it builds.

2. **The tabs are placeholders, not an IA.** home / device / automation / profile, per owner
   instruction pending real information architecture. `NomaTab.id` is stable so analytics can
   attach later. Four `nav.*.label` keys are now live in `src/i18n/locales/en/common.json` —
   the first real strings in that file. **Hindi is deliberately empty** and the locale file
   explains why rather than carrying four guessed transliterations.

3. **It diverges from the reference video in exactly one way, on purpose.** The video's
   selected pill is darker than the bar; LAW 3 says white means raised and selection is lift,
   not colour. So the pill is white. Reverting is one line but it is a C-14 decision.

⚠ **NEW OPEN ITEM O-10 — an accessibility gate that silently does not fire.** Motion gate 2
demands every animating file contain `prefers-reduced-motion`. That is a CSS media query, so
no Swift/Kotlin/RN file can ever satisfy it — **the grep reports clean precisely where it has
no coverage.** Gate 1 has the same hole (`cubic-bezier(` and `[0-9]ms` are CSS spellings; an
inline `.timingCurve(…, duration: 0.24)` in Swift violates the intent and matches neither
pattern). Deliberately not worked around: a dead CSS string in a Swift comment would make the
gate pass while making it meaningless. **This needs the owner, because it edits an enforced
rule** — and it will keep getting worse as more native code lands.

Two pre-existing gaps this component walked straight into, both already tracked and neither
invented here: **`colors.status` is `null` (O-6)** — a tab cannot carry a badge, a dot, or any
attention state, so the moment Home wants to signal "filter due" this bar has nothing to draw
with; and **there is no spring-physics token** — the pill's travel is a cubic-bezier with ~10%
overshoot, which reads correctly but is not the simulated physics the reference shows.

**C-14 moved one notch, in practice rather than in principle.** The owner chose **light
greyscale** for this component, making it the third artefact to ship in that direction
(first-run, bottom-sheets, now bottom-nav). The conflict is still formally open and the green
tokens are still canonical, but the evidence is now three-for-three against them.

---

## Read this first — 2026-08-06

**First run was rebuilt to the owner's flow diagram, then revised four times the same day.**
The 2026-08-05 ordering (Arrival → Household → Device, chosen out of three candidates) is
superseded, along with the V1/V2/V3 comparison. The spec is `docs/features/first-run/prd.md`
§5 — **not the diagram**, which is now its origin rather than its current state.

**As built: 22 main-line nodes + branch 18a**, in this order:

```
1 … 16   account → pairing → network → connected
  24     location (geofencing)      ← moved here
  25     notifications              ← moved here
  17     which room? create the home
  18     name the device
 18a       └ invite family  (branch)
  23     about the app · 3 slides
  26     home
```

**Node ids are stable and therefore no longer ascend** — that is deliberate, and it is what
lets every earlier reference ("node 15", "node 6") still resolve. The 19–22 gap and the
16 → 24 → 25 → 17 jump are both intentional.

Same-day revisions, in order:
1. **Node 6** narrowed from a four-way device-type chooser to three purifier SKUs.
2. **Nodes 19–22 removed entirely** (firmware check / install / complete / first reading),
   plus `R3B`, the household disclosure screen.
3. **Nodes 7–12 rewritten** to the updated pairing sequence: filter unwrap as its own step,
   plug-in split from light-check, Bluetooth reframed around the radio, device pick as a
   list, Wi-Fi auto-fetched with the manual list as fallback. Node 15 re-spaced.
4. **Both permission asks moved forward** to run straight after node 16 (connected), and
   node 23 now lands directly on Home. PRD §5.8.

**Three things those removals left genuinely unhandled** — these need owners, not screens:
- **Nothing takes a first reading.** Home shows a number with no step that produced it, so
  `J-WEEK-01` rests entirely on Home's first paint. It needs a loading state for the ~20s
  before a reading exists. Reopens PRD §5.3; belongs to `F-AQI-LIVE`.
- **Firmware update has no path anywhere**, in this spec or any other.
- **Per-invite disclosure is gone.** Inviting someone grants access to everything with no
  screen saying so.

**Watch item from the reorder (PRD §5.8):** the permission asks now arrive before the
product has any shape — no named room, no named device, no reading. Node 24's pitch is made
about a device with no room, in a home that does not exist yet. **The tell is grant rate on
node 24**; if it drops, move node 24 alone back behind node 17 and keep 25 where it is. Node
24/25 copy also still speaks as though a device is placed — reread before ship.

Still open from the original rebuild: **PRD §5.1 — there is no consent screen.** The DPDP
notice rides on node 4 because the flow has nowhere else to put it. Legal question, not a
design preference; get a referee before build.

⚠ Also unresolved: the brief's phrase *"does not work with standalone wifi credential"* is
built as **5 GHz-only networks**. If it meant captive-portal or enterprise/802.1X, node 12's
copy is wrong and neither case has an error state.

**Node 1 is built to the owner's four-frame mock** (third pass): rectangular white door,
NOMA wordmark, "Enter Home" slide track → "Entering Now…" over a green fill, and a staged
walk-through — leaf opens fully, the camera travels through the frame until the white
interior swallows the viewport, then the next screen arrives out of that white. ⚠ The green
entering-state is from the mock and is the only green in first run — see C-14. The corridor is **one shared-vertex SVG**, not CSS-transformed
planes — that is what makes the walls and door seamless, and it is the thing to preserve if
this is rebuilt. Placement is measured to the reference within 0.1%. The travel is a `scale`
about the aperture centre (not `translateZ`), which avoids perspective culling altogether.
**Light comes from behind the door — no dark shadow may go near it.** The white you walk
into lives on `.phone`, not inside `.scr`, because the screen is destroyed at the hand-off;
it needs a forced reflow to animate and an untracked removal backstop so it can never strand
as an opaque white page. The slider greens **proportionally with the drag**, not on commit.
**Node 23's three slides animate their own claim** (readings that never leave the house;
air drawn in and pushed back clean; wires drawing device by device).

**The voice is now a formal, app-wide PRD, typeset as a PDF (2026-08-07)** —
`docs/voice/NOMA-Voice-PRD.pdf`, canonical markdown at `docs/voice/voice-prd.md`. Started
onboarding-only, generalized the same day once the register proved out: same seven rules,
same grammar, same banned words, everywhere the app has something to say — not just setup.
Both `tone-matrix.md` and `glossary.md` now point at it instead of staying stubs. Read this
before writing any new string anywhere in the app.

**§13 of that PRD is a live status table — check it before assuming a surface is covered.**
Onboarding is rewritten and shipped (the worked evidence throughout). Home and notifications
already match via `ai-personas.md`, written independently but reconciled in §13. **My Home
(`docs/features/my-home/build-home.py`) is the next concrete pass — its copy predates this
voice and has not been touched.** Sharing/People, Automations, Shop and Settings have no
prototype yet; apply the checklist (§12) at first-draft time there instead of retrofitting.

**The copy was rewritten to a conversational voice (2026-08-06)** — first person, talking
about the house as somewhere it looks after. Seven rules in PRD §8.1, each with a shipped
NOMA example. ⚠ Two open consequences: **"I" commits the product to a first-person agent from screen one and
C-2 is still open** (if the product and the assistant are different characters, every "I" needs
re-attribution), and **the Hindi bar went up** — the new copy is idiomatic and needs
transcreation, not translation.

**Node 1, 7, 11, 17 and 26 all carry real gestures** (2026-08-06, owner: the flow "looks
too boring… this is going to be our main attraction point"). Door you drag open, filter wrap
you peel, hold-to-pair, a room drawing that morphs between six rooms, an AQI that counts up.
Every one also works on a plain tap and on Enter, and collapses under reduced motion — the
gesture is the delight, never the toll gate. Detail: PRD §5.9. **Still flat and named as
such: nodes 2–5, the account run.**

Also note **`build-wireframes.py` and `build-export.py` no longer define screens or
interaction JS** — both import `SC`/`SEQ`/`RUNTIME_JS` from `build-prototype.py`. One screen
set, one runtime, three renderings.

---

## Current state

Two things exist: a **complete design foundation**, and a **freshly-populated knowledge
base** extracted from four PM prototypes. This repo is knowledge, tokens and assets —
plus, as of 2026-08-12, **one native component**: `design-elements/bottom-nav/` (SwiftUI,
builds, never run). There is still no application, no Xcode project and no shell to host it.

| Area | State |
|---|---|
| Design foundation | ⚠ **Done, but now contested three ways.** Palette, typeface, radius, elevation, spacing, card recipes — ADR-001…004, canonical in `src/tokens/design.tokens.js`. **But the 2026-08-05 prototype uses a different direction on owner instruction**: greyscale, a radial gradient (`#FFFFFF` top right → `#A4A4A4` bottom left), 8% card shadows, black pill CTAs, **no accent green at all**. The tokens still carry the ADR-003/004 greens. **And the My Home PRD specifies a third — a dark "Air Agent" language.** Three palettes, one product. See C-14; this is the highest-priority visual decision. |
| Product / Tech / Hardware / Content / Analytics knowledge | **Populated 2026-08-04** from the PM prototype set. See `memory/index.md`. |
| Motion tokens | **Populated — ADR-005.** Playful spring on discrete moments, still on ambient. Gates live in `.claude/rules/motion.md`. |
| Personas registry | **Empty on purpose** — C-1 unresolved. |
| Event schema | **Empty on purpose** — zero events exist; blocked by C-11. |
| i18n strings | Stubs. Blocked by C-2 (no agreed product/assistant name). |
| PRDs | **Two feature PRDs now.** `docs/features/my-home/` built from the owner-supplied `ding-my-home-prd.md`. **Master PRD written** — `docs/prd/noma-v1.md`. **First-run PRD rebuilt 2026-08-06** to the owner's flow diagram, then revised five times same day — `docs/features/first-run/prd.md`, plus a **tappable prototype** (`first-run-prototype.html`, 32 screens across 22 nodes + branch 18a, 13 edge states, five gestural nodes), a **flat board** and a **clean export**, all three generated from one source. 12 features still have none. |
| Competitive research | **Started 2026-08-05.** `docs/research/2026-08-05-setup-teardown.md` — 9 flows / ~130 screens across the five smart-home apps Mobbin carries. Typeset as a 21-page reference book: `docs/research/NOMA-first-run-references.pdf` (17 stages × 5 annotated references, **69 of 85 tiles are real Mobbin captures** via the Mobbin MCP connector). |

**What the product is.** An agent-first connected-home app for Indian homes, anchored on an
air purifier and extending to cameras, locks, vacuums and doorbells. The core insight is
that air is invisible, so *perceived value is whatever the app makes visible*. Full picture:
`memory/product/vision.md` → `memory/product/journeys.md` →
`memory/architecture/ai-integration.md`.

**Read `memory/architecture/ai-integration.md` before designing any agent surface.** The
graduated-autonomy model, the four-slot explanation contract, and rehearsal-before-execution
are architectural commitments, not UI suggestions.

---

## What was just done

**2026-08-06 — first run rebuilt to the owner's flow diagram, then revised five times.**
The 2026-08-05 flow had the wrong steps. `build-wireframes.py` was rewritten to import its
screens from `build-prototype.py` instead of keeping a second copy, which is how the two
drifted apart in the first place. Then four owner revisions landed the same day: node 6
narrowed to three purifier SKUs; nodes 19–22 and `R3B` removed outright; nodes 7–12
rewritten to the new pairing sequence (filter unwrap, plug-in, light, Bluetooth radio,
device list, Wi-Fi auto-fetch); and both permission asks moved to run straight after node
16, with the about-slides landing directly on Home. Finally, **five nodes were given real
gestures** (door, peel, hold-to-pair, morphing room, counting number) after the flow was
judged too inert. As built: 22 main-line nodes + branch 18a. Detail and the open items:
`memory/changelog.md`, PRD §5 and §5.9.

**2026-08-05 — the first run.** Read 9 flows / ~130 screens on Mobbin across Google Home,
Apple Home, SmartThings, IKEA Home smart and Amazon Alexa, wrote the repo's first feature
PRD (`docs/features/first-run/prd.md`), and typeset the research as a 21-page reference book
with 69 real Mobbin captures. The flow drawn that day has since been replaced.

**Decisions:**

1. ~~Where the household belongs — V1, Home → Household → Device.~~ **SUPERSEDED 2026-08-06
   by the owner's flow diagram**, which puts the household after the device as a branch off
   node 18. The V1/V2/V3 comparison is closed and no longer worth reopening.
2. ~~Purifier only; camera, lock and vacuum out of every flow.~~ Reversed briefly, then
   **RE-CLOSED 2026-08-06 the same day**: node 6 is three purifier SKUs —
   `HW-PUR-200`/`500`/`MAX`. Camera, lock and vacuum are out of first run. PRD §5.4 retired.
4. **Firmware update removed from setup 2026-08-06** and not respecced anywhere. If devices
   can ship with stale firmware, this needs an owner — it is a product decision nobody has
   recorded as one.
3. **The hand-the-phone-over step is removed** (owner's call, 2026-08-05) and survives the
   rebuild. Household follows Apple Home / Google Home: an invitation sent to a contact,
   accepted on their own device. The reasoning is recorded in the PRD so it does not creep
   back.

Also worth carrying forward:

- **Device before members, five out of five.** No reference app asks for a household
  member during first run. The diagram now agrees with that evidence — the household runs
  after the device, which is what the 2026-08-05 recommendation had argued for.
- **Mobbin carries no purifier or air-quality app** — and no Aqara, Ring, Nest, Wyze,
  Eufy, Tuya or Hue either. There is no incumbent to benchmark against. IKEA's DIRIGERA
  hub flow is the closest analogue and the best in the set; the spec adapts it.

Two new open items: **O-8** (onboarding and setup have no `F-*` id — the PRD runs on two
*proposed, unassigned* ids) and **O-9** (`identify` and the ring-LED vocabulary are
unconfirmed hardware behaviours the flow depends on).

**2026-08-04.** Ingested four PM-supplied HTML prototypes (inventoried in
`docs/index.md`) and extracted them into six pillars. Design pillar untouched. Detail in
`memory/changelog.md`.

Two findings worth carrying forward:

1. **The agent model is the product's real architecture** — per-capability graduated
   autonomy, a fixed four-slot explanation (Sensed / Decided / **Instead of** / Obeys rule),
   and inert editable rehearsal where rule-derived steps are `Locked`. Trust is promoted on
   evidence ("you've accepted 7 in a row"), which means a per-capability accept tally is
   application state, not just analytics.

2. **C-1 now has evidence for Set B** — Ravi and Lakshmi appear as named people in the
   prototype's camera feed; all four surfaces Set B names are built; Set A's names appear
   nowhere. Not closed — still the owner's call.

**Twelve conflicts opened (C-2…C-13)** because the four documents disagree with each other
on nearly every name and number. Nothing was reconciled.

---

## What's next

00. **Answer PRD §5.1, §5.2, §5.5 — three calls the flow diagram still leaves open**
   (§5.3 and §5.4 were resolved 2026-08-06, same day as the rebuild). In severity order:
   §5.1 (no consent screen; DPDP notice rides on node 4 — needs a legal referee, not a
   designer), §5.5 (node 19 promises a notification six screens before the permission is
   asked; geofencing must request While-Using, never Always), §5.2 (two verifications before
   the box is opened). §5.6 is settled — privacy-first tour is right. Everything here is
   cheap to change now and expensive after build.

0. **Rule C-14 — three palettes are now in play.** The canonical green tokens
   (ADR-003/004), the light greyscale direction the owner set for first-run, and the dark
   "Air Agent" language the My Home PRD specifies. Two prototypes now ship in the light
   one. Nothing visual can be trusted until this is settled, and it is cheap to settle.

1. **Rule C-2 — the product and assistant have six names.** The My Home PRD adds "Ding". Highest leverage on the list:
   all copy, every i18n key, all persona prompts, the glossary, the tone matrix and every
   SKU string in `src/hardware/devices.json` are downstream of it. Nothing user-facing can
   ship first.

2. **Rule C-1** (personas). Set B has four-for-four prototype corroboration. Closing it
   unblocks `src/personas/personas.json`, tone routing, and persona IDs on `J-*` steps.

3. **Get an engineering answer to C-7** — AQI-weighted filter life is *the* product claim
   and has no formula, no coefficients and no validation data. It gates `F-FILTER-HEALTH`,
   which is simultaneously the differentiator and the recurring-revenue lever.

4. **Rule C-11 before naming a single analytics event.** "Data never leaves home" vs
   outdoor-AQI blending, forecast pre-clean and neighbourhood comparison. An analytics SDK
   is by definition exfiltration, so the taxonomy cannot start until this is settled. Today
   there is a named seven-day retention strategy with **no way to measure it**.

5. **Rule C-8** — give agent capabilities a safety class. Nothing currently prevents
   "Act silently" applying to a lock or to an unattended purchase.

6. **Vendor the prototypes.** They live in the owner's `~/Downloads`; the provenance of this
   whole knowledge base is a local folder. Copy into `docs/prototypes/`.

7. **Write the next PRDs** from `templates/feature-prd.md`. `docs/features/first-run/prd.md`
   is done; `F-AQI-LIVE`, `F-FILTER-HEALTH`, `F-AGENT-PROPOSE` next. Note `F-AQI-LIVE` now
   owns the reveal outright — the first-run diagram has no reveal screen, so the first number
   the user ever sees is rendered by Home (first-run node 26). See PRD §5.3.

7b. **Rule O-8** — assign real `F-*` ids for onboarding and setup, or fold them into an
   existing feature. Until then the first PRD points at ids that do not exist in the
   registry.

8. **Decide which product ships first.** The material spans a focused purifier companion
   *and* a whole-home platform. Nothing says which. Upstream of most other conflicts — see
   `memory/product/scope-ledger.md`.

---

## Open questions for the owner

- **`.claude/rules/` are all stubs.** CLAUDE.md calls them enforced, greppable, pre-commit
  gates. Nothing is actually enforced.
- **CLAUDE.md line 3** still reads `TODO(owner): describe the app in one sentence.` There is
  now enough material to write it — blocked only on C-2 for the name.
- **No payment flow anywhere.** `F-SHOP` is the recurring-revenue path and stops at a price
  tag.
- **No empty, loading, error or offline states** in any prototype. Every screen is a happy
  path with seeded data.
- **Third-party ecosystems** (Alexa / Google / HomeKit / Matter) are absent from all four
  documents. For 2026 that is a conspicuous silence — is it a decision?
- Device specs (CADR, coverage, prices) are marked `prototype-only`. None has been checked
  against a datasheet or BOM.

---

## Related repo

This design system is mirrored into the **NOMA** app of the master dashboard at
`noise-design/noiseFit` (deployed on Vercel). Its `src/noma/noma.tokens.js` is a **synced
copy** of `src/tokens/design.tokens.js` from here — **this repo is canonical**; re-sync
there, never edit it. Re-sync after any token change.
