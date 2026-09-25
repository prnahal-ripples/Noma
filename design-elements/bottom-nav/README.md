# Bottom Navigation Bar

**Registered** in [`.claude/rules/design-system.md`](../../.claude/rules/design-system.md)
Approved Components, 2026-08-12. Indexed alongside every other approved
component at [`design-elements/README.md`](../README.md).

**Live on the Vercel dashboard** (`noise-design/noiseFit`), same day —
`design/noma/bottom-nav/` there, embedded in NOMA's Design pillar as a real
folder (matching how Bottom Sheets already had one), not a text listing.
⚠ That copy is a **trimmed gallery variant**, not a byte-copy of this
folder's `index.html` — no internal phone chrome (the dashboard supplies
its own), no measurement-readout panel (that context lives in its own
README instead). The two should agree on behaviour, not markup; re-sync
the noiseFit copy by hand if this file's geometry or motion changes, same
discipline as the token mirror.

A rebuild of the tab bar in Kavsoft's
[**Instagram App's Minimizable Tab Bar Using SwiftUI**](https://www.youtube.com/watch?v=691o2FUDs-8)
([demo clip](https://x.com/_kavsoft/status/2081135065908801661)), skinned with
NOMA tokens.

Two implementations, not one, and they are not at the same maturity — see
**Verification status** below before treating them as equivalent:

```
index.html                 static HTML/CSS/JS mobile preview — phone frame,
                            scrollable app content, live measurement readout.
                            Opens directly, no build step. VERIFIED IN-BROWSER.
Package.swift               ── SwiftUI package — BUILDS, NEVER EXECUTED ──
Sources/NomaBottomNav/
  NomaTokens.swift          colour · radius · elevation · spacing (mirror)
  NomaMotion.swift          durations · easings · reduced-motion gate (mirror)
  NomaTab.swift             the tab model — i18n keys, SF Symbol pairs
  MinimizableTabBar.swift   the bar: pill ground, travelling selection blob
  NomaTabScaffold.swift     container, scroll-direction detection, shrink call
  NomaBottomNavDemo.swift   scrollable skeleton per tab
Demo/                       @main entry + #Preview — EXCLUDED from the package
```

Four provisional tabs: Home, Device, Automation, Profile.

⚠ **The geometry described in "How it was derived" and "Deliberate
divergence" below is the SwiftUI package's, from the first pass.** The HTML
preview (`index.html`) was revised twice since — see its own header comment
for the current spec: 16px inset on left/right/bottom (not a content-sized
pill), and a uniform 0.8× shrink floor via `transform: scale()` rather than
per-property width/height animation. **The SwiftUI package has not been
ported to that geometry yet.** Treat `index.html` as the current reference
for how this component should look and behave; this README's prose below
describes the SwiftUI package specifically.

## How it was derived

**The tutorial's source code was not available, and video is not something that
can be read.** What this is built from is the reference clip stepped
frame by frame in a browser — the 26-second demo, sampled at 18 points and
composited into a contact sheet. Three behaviours were legible enough to rebuild:

1. **A floating pill**, inset from the screen edges, with content scrolling
   underneath it — not a full-width bar pinned to the bottom edge.
2. **A selection blob that lifts and travels.** Clearest at 6.0s and 7.5s, where
   the capsule is caught mid-flight between the first and second tab, visibly
   raised and bulging out of the bar.
3. **Shrink on scroll-down**, re-expand on scroll-up.

**One correction to the brief.** The request described this as an "AI-based
navigation bar." It isn't — there is no AI in it. It's the iOS 26/27 Liquid Glass
tab-bar pattern.

**One correction to the pattern's reputation.** Across all 26 seconds the bar
never collapses to a single icon and never leaves the screen. It is a *shrink* —
width contracts, glyphs tighten — not a collapse and not a hide. Apple's native
`.tabBarMinimizeBehavior(.onScrollDown)` does collapse to a single-icon pill, and
is **not** what the reference shows. That is why this is a custom bar rather than
four lines of system modifier, and it is also why it works on iOS 18 rather than
requiring 26.

### What is a reading, not a measurement

The geometry numbers in `NomaTabBarMetrics`. The screen recording zooms during
playback, so absolute pixel comparisons between frames are unreliable. What was
preserved are the **ratios**: the minimized bar is roughly three-quarters the
width of the expanded one, its glyphs about four-fifths the size. Treat the
absolute values as a starting point to tune against a real device, not as spec.

## Deliberate divergence from the reference

**The selected pill is white, not grey.** In the video it is a slightly *darker*
grey than the bar around it. NOMA's LAW 3 says the opposite — white means raised,
and selection is expressed by lift rather than by colour; the token file calls a
colour-only selection a bug. So the pill is white and raised on a translucent
grey bar, and the glyph switches from `Ink.tertiary` to `Ink.primary`.

If literal video fidelity is wanted instead, it is one line —
`selectionPill`'s fill in `MinimizableTabBar.swift`. But that is a C-14 palette
decision, not a code preference.

## Verification status

**Typechecks and builds clean** under Swift 6 language mode with strict
concurrency:

```bash
swift build
```

**That is the whole of what was verified.** There is no Xcode on the machine that
wrote this — only Command Line Tools — so:

| | |
|---|---|
| Compiles, Swift 6 strict concurrency | ✅ verified |
| Builds as a package | ✅ verified |
| Motion gates 1 and 3 (greppable) | ✅ verified |
| Gate 2 in substance (reduced motion) | ✅ every animating file routes through `NomaMotion.resolve` |
| **Runs on a simulator or device** | ❌ **never executed** |
| **Looks like the reference** | ❌ **never rendered — not once** |
| **SF Symbol names resolve** | ❌ asserted from the catalogue, not compiled against an iOS SDK |
| **The shrink feels right** | ❌ needs a thumb on real glass |

`air.purifier` / `air.purifier.fill` need SF Symbols 5 (iOS 17+). A missing
symbol renders as a placeholder rather than crashing, but check all eight glyph
names in Xcode before this goes near a build. `flowchart` for Automation is a
swap-me choice — `sparkles` reads more agent-first but has no filled counterpart,
and the selected state needs one.

## Tokens

Hand-copied from [`src/tokens/design.tokens.js`](../../src/tokens/design.tokens.js)
and [`src/tokens/motion.tokens.js`](../../src/tokens/motion.tokens.js) — a Swift
package has no build step wired to the JS token files, so it cannot import them.
Same arrangement, and the same caveat, as
[`design-elements/bottom-sheets`](../bottom-sheets/README.md): **if tokens drift,
the JS files win**; re-sync `NomaTokens.swift` and `NomaMotion.swift` by hand.

Reflects the rebuilt token file (2026-08-11, five laws). Two laws do real work
here:

- **LAW 1, the ground is a gradient** — the scaffold's canvas is
  `gradients.canvas`, never a flat fill.
- **LAW 3, white means raised** — the whole selection model, as above.

Palette: **light greyscale** (owner's call this session). No green is referenced
anywhere in the package, and under LAW 2 no flat green would have been legal
even if it were.

### Two gaps this component surfaces

Both are pre-existing and tracked elsewhere, not invented here:

- **`colors.status` is still `null`** (ADR-001 O-6). A tab cannot carry a badge,
  a dot, or an attention state, because there is no colour that means
  "something needs you" — and green cannot carry it. The moment Home wants to
  signal a filter due or an alert, this bar has nothing to draw with.
- **No spring-physics token.** `motion.tokens.js` has cubic-beziers only, so the
  pill's travel is a timing curve with ~10% overshoot
  (`easings.spring`, mapped 1:1 onto `Animation.timingCurve`) rather than real
  spring physics. It reads correctly; it is not the same thing. The reference's
  blob looks physically simulated.

## Motion compliance

Per [`.claude/rules/motion.md`](../../.claude/rules/motion.md):

- **Gate 1, tokens only.** Every duration, curve and delay lives in
  `NomaMotion.swift`. View code references animations by name and contains no
  numeric animation literals — verified by grep.
- **Gate 2, reduced motion is mandatory.** Every `withAnimation` in the package
  passes through `NomaMotion.resolve(_:reduceMotion:)`, which returns `nil` when
  the user has asked for reduced motion. Scale effects collapse too, via
  `nomaScaleEffect` — an instant jump to 1.04 is still motion. The tab still
  changes and the bar still shrinks; neither is animated.
- **Gate 3, exits never bounce.** The shrink (`barMinimize`) is `easings.standard`.
  Only the re-expand (`barExpand`) and the tab travel (`tabTravel`) — both
  discrete, user-caused arrivals — get the house spring. `barDismiss` exists
  unused on `easings.exit`, so that anyone adding a hide-on-scroll variant
  reaches for the right token.
- **Gate 4, ambient never springs.** Nothing here is ambient; the bar moves only
  in response to a deliberate scroll or tap.

### ⚠ Gate 2 is not greppable for Swift

The rule says every animating file must contain the literal string
`prefers-reduced-motion`. That is a CSS media query. **No Swift file can satisfy
it**, so the gate as written silently fails to cover this package — and would
silently fail to cover any native code in the repo. The substance is met via
`@Environment(\.accessibilityReduceMotion)`; the gate needs amending to accept
that spelling. Flagged in `memory/decisions.md` rather than worked around here,
because adding a dead CSS string to a Swift comment to satisfy a grep would make
the gate pass while making it meaningless.

### There is no reduced-motion preview

`\.accessibilityReduceMotion` is get-only in `EnvironmentValues`, so it cannot be
forced from a `#Preview`. Verify on a simulator or device with **Settings →
Accessibility → Motion → Reduce Motion** on. Expected: tapping a tab changes it
instantly, no pill travel and no lift; scrolling still shrinks the bar, in one
step rather than as a transition.

## Usage

```swift
@State private var selection = [NomaTab].nomaDefault[0].id

NomaTabScaffold(selection: $selection) { tab in
    MyScreen(for: tab)
}
```

Each scrollable screen opts into driving the shrink:

```swift
ScrollView { … }
    .nomaTracksBottomNav()
```

The scroll signal has to be opt-in because the `ScrollView` belongs to the
screen, not to the scaffold. A tab with nothing scrollable never reports and its
bar stays expanded — that is correct behaviour, not a gap.

The shrink is guarded three ways, all in `NomaScrollShrink`: a 6pt direction
threshold so a resting finger can't flip it, a 12pt top rest zone so the bar
stays open through the rubber-band, and an 80pt overflow minimum so a screen with
barely more than a screenful doesn't flicker. The space reserved for the bar is
constant at the **expanded** height — if it tracked the actual height, every
shrink would reflow the content underneath and turn a calm scroll into a jitter.

## Accessibility

- Bar is one `accessibilityElement(children: .contain)`; each tab is a button
  carrying `.isSelected` when active.
- Labels come from the tab's i18n key. The bar is icon-only, so **that key is the
  tab's only name for a VoiceOver user** — `nav.*.label` in
  [`src/i18n/locales/en/common.json`](../../src/i18n/locales/en/common.json).
  Hindi is deliberately unwritten; see that locale file for why.
- `itemWidth` is clamped to a 44pt minimum tap target, so a longer tab set
  cannot shrink the touch area below the HIG floor. The minimized bar is
  50 × 52pt per slot, comfortably clear.
- Identifiers (`noma.bottomNav`, `noma.bottomNav.<id>`) are set for UI tests.

## Not done

- **Tab count.** Built and checked for four. The layout is content-driven so it
  handles any count, but five tabs at 66pt is 346pt of a 393pt screen — near the
  edge, and worth re-reading against the reference before adding one.
- **Badges.** Blocked on `colors.status` being `null`, above.
- **Analytics.** No events. `memory/analytics/event-taxonomy.md` is empty by
  design (C-11 unresolved), so a tab-switch event has nowhere legitimate to go
  yet. `NomaTab.id` is stable specifically so it can carry one later.
- **Landscape and iPad.** Only portrait phone was reasoned about.
