import SwiftUI

// ---------------------------------------------------------------------------
// MOTION TOKEN MIRROR — hand-copied from src/tokens/motion.tokens.js (ADR-005).
// That file wins; re-sync by hand.
//
// This file is the ONLY place in the package that may contain a duration or a
// bezier. `.claude/rules/motion.md` gate 1 says UI code never writes a raw
// millisecond value or curve — so every animation the views use is named here
// and referenced by name there.
//
// HOW THE GATES LAND ON THIS COMPONENT:
//
//   Gate 2  reduced motion is mandatory     → `resolve(_:reduceMotion:)`. Every
//           (accessibility, no exceptions)    withAnimation in this package
//                                             goes through it. Nothing animates
//                                             when the user has asked it not to.
//
//   Gate 3  EXITS NEVER BOUNCE               → `barMinimize` is `standard`, not
//                                             `spring`. The bar shrinking away
//                                             is a layout shift, so it settles
//                                             without personality. Only the
//                                             re-expand (`barExpand`) and the
//                                             tab travel (`tabTravel`) — both
//                                             discrete, user-caused moments —
//                                             are allowed the house spring.
//
//   Gate 4  ambient never springs            → nothing here is ambient. The bar
//                                             only moves in response to a
//                                             deliberate scroll or a tap.
// ---------------------------------------------------------------------------

public enum NomaMotion {

    // MARK: - Primitives (`durations`, in seconds — the JS file is in ms)

    private enum Duration {
        static let fast = 0.140 // taps, toggles, chips, segment thumbs
        static let base = 0.240 // card state changes, tab content swap
        static let gentle = 0.360 // expanders, list entrances, meters filling
    }

    // MARK: - Primitives (`easings`)
    //
    // cubic-bezier(x1, y1, x2, y2) maps 1:1 onto Animation.timingCurve. The
    // house spring's y1 of 1.56 is what produces the ~10% overshoot; SwiftUI
    // honours control points above 1, so the curve is preserved exactly rather
    // than approximated with `.spring()`.

    private enum Curve {
        /// settle without personality — ambient + layout shifts
        static func standard(_ d: TimeInterval) -> Animation {
            .timingCurve(0.2, 0, 0, 1, duration: d)
        }
        /// leave fast, no bounce — every exit uses this
        static func exit(_ d: TimeInterval) -> Animation {
            .timingCurve(0.4, 0, 1, 1, duration: d)
        }
        /// THE house spring — ~10% overshoot. Buttons, chips, toggles, cards.
        static func spring(_ d: TimeInterval) -> Animation {
            .timingCurve(0.34, 1.56, 0.64, 1, duration: d)
        }
    }

    // MARK: - `scale`

    public enum Scale {
        /// `scale.press` — active/pressed state.
        public static let press: CGFloat = 0.96
        /// `scale.pop` — the moment of arrival, before settling to 1.
        /// Drives the selection pill's lift as it leaves for a new tab.
        public static let pop: CGFloat = 1.04
    }

    // MARK: - Named component animations
    //
    // Views reference these by name and never build their own.

    /// The selection pill travelling to a newly tapped tab. A discrete,
    /// user-caused moment, so it gets the house spring (gate 3 permits bounce
    /// on arrival — it forbids it on exit).
    public static let tabTravel = Curve.spring(Duration.base)

    /// The pill's lift on departure — scales to `Scale.pop` and gains shadow.
    /// Fast, because it must be fully lifted before the travel is underway.
    public static let liftOut = Curve.standard(Duration.fast)

    /// Settling back down at the destination.
    public static let liftIn = Curve.standard(Duration.base)

    /// How long the pill stays lifted before it starts settling. Matched to
    /// `liftOut` so the descent begins the instant the rise completes. Named
    /// here rather than written inline at the call site — gate 1 covers delays
    /// as much as it covers durations.
    public static let liftSettleDelay: TimeInterval = Duration.fast

    /// Icon glyph crossfade between the outline and filled variants.
    public static let iconSwap = Curve.standard(Duration.fast)

    /// The bar SHRINKING on scroll-down. GATE 3 — this is a layout shift on the
    /// way out, so it settles flat. Never `spring` here.
    public static let barMinimize = Curve.standard(Duration.base)

    /// The bar RE-EXPANDING on scroll-up. An arrival, so the house spring is
    /// legal — but at `gentle` rather than `base`, because a nav bar that
    /// overshoots briskly on every upward flick reads as twitchy.
    public static let barExpand = Curve.spring(Duration.gentle)

    /// Tap-down feedback on a tab.
    public static let press = Curve.spring(Duration.fast)

    /// Reserved for a bar that leaves the screen entirely (not used by the
    /// scroll-shrink behaviour, which never fully hides). Kept so that anyone
    /// adding a hide-on-scroll variant reaches for `exit` and not `spring`.
    public static let barDismiss = Curve.exit(Duration.fast)

    // MARK: - Gate 2 — reduced motion

    /// GATE 2, the accessibility gate: every `withAnimation` in this package
    /// passes through here. Returns `nil` when the user has asked for reduced
    /// motion, which makes SwiftUI apply the state change instantly — the tab
    /// still changes, the bar still shrinks, neither is animated.
    /// - Parameter delay: seconds to hold before the animation starts. Under
    ///   reduced motion the delay is dropped along with the animation — a
    ///   delayed instant change is still a change the user did not ask to see
    ///   staged.
    public static func resolve(
        _ animation: Animation,
        reduceMotion: Bool,
        delay: TimeInterval = 0
    ) -> Animation? {
        guard !reduceMotion else { return nil }
        return delay > 0 ? animation.delay(delay) : animation
    }
}

extension View {
    /// Scale/lift effects must also collapse under reduced motion, not just the
    /// animations that drive them — an instant jump to 1.04 is still motion.
    func nomaScaleEffect(_ scale: CGFloat, reduceMotion: Bool, anchor: UnitPoint = .center) -> some View {
        scaleEffect(reduceMotion ? 1 : scale, anchor: anchor)
    }
}
