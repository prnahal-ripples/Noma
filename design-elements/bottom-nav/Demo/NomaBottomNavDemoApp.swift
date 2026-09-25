import SwiftUI
import NomaBottomNav

// ---------------------------------------------------------------------------
// App entry point — EXCLUDED from the Swift package on purpose (`@main` cannot
// live in a library target). To run the demo:
//
//   1. New Xcode project → iOS App → SwiftUI. Deployment target iOS 18 or later.
//   2. Delete the generated ContentView.swift and App file.
//   3. Add this package: File → Add Package Dependencies → Add Local →
//      design-elements/bottom-nav.
//   4. Add this file to the app target.
//   5. Add src/fonts/google-sans-flex/ to the target and register the family
//      under `UIAppFonts` in Info.plist — without it the demo falls back to the
//      system face and the type will not match NOMA.
//   6. Add nav.* keys to a String Catalog, or the headings render as raw keys.
//      Source of truth: src/i18n/locales/en/common.json.
// ---------------------------------------------------------------------------

@main
struct NomaBottomNavDemoApp: App {
    var body: some Scene {
        WindowGroup {
            NomaBottomNavDemo()
        }
    }
}
