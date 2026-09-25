import SwiftUI
import NomaBottomNav

// ---------------------------------------------------------------------------
// Previews live here rather than beside the sources for one reason: `#Preview`
// expands through a compiler plugin that ships with Xcode, and the library
// target is verified with the Command Line Tools toolchain, which has no plugin
// to load. Keeping previews in the excluded Demo/ folder means the whole library
// typechecks cleanly. Add this file to an Xcode target to use them.
//
// ⚠ THERE IS NO REDUCED-MOTION PREVIEW, and that is a limitation, not an
// oversight: `\.accessibilityReduceMotion` is get-only in EnvironmentValues, so
// it cannot be forced from a preview. Verify the gate-2 behaviour on a simulator
// or device with Settings → Accessibility → Motion → Reduce Motion turned ON.
// Expected: tapping a tab changes it instantly with no pill travel and no lift;
// scrolling still shrinks the bar, but in one step rather than as a transition.
// ---------------------------------------------------------------------------

#Preview("Bottom nav — demo") {
    NomaBottomNavDemo()
}
