import SwiftUI

// ---------------------------------------------------------------------------
// DEMO HARNESS — a scrollable skeleton per tab, enough to exercise the shrink.
//
// Deliberately copy-free: the only text is each tab's own i18n key resolved as a
// heading. Everything else is shapes, so the harness cannot become a back door
// for hardcoded strings (CLAUDE.md rule 4) or a second place where product copy
// lives.
//
// This is a View, not an App, so it typechecks inside the library target and
// works in Xcode Previews. The `@main` entry point lives in Demo/ and is
// excluded from the package.
// ---------------------------------------------------------------------------

public struct NomaBottomNavDemo: View {

    @State private var selection: String = [NomaTab].nomaDefault[0].id

    public init() {}

    public var body: some View {
        NomaTabScaffold(selection: $selection) { tab in
            DemoTabScreen(tab: tab)
        }
    }
}

private struct DemoTabScreen: View {

    let tab: NomaTab

    /// Varied heights so the skeleton reads as content rather than as a grid,
    /// and so there is comfortably more than a screenful to scroll.
    private let cardHeights: [CGFloat] = [148, 96, 210, 132, 96, 178, 120, 240, 104, 160]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: NomaTokens.Space.s5) {
                Text(tab.label)
                    .font(NomaTokens.Typeface.micro())
                    .tracking(NomaTokens.Typeface.microTracking)
                    .textCase(.uppercase)
                    .foregroundStyle(NomaTokens.Ink.secondary)
                    .padding(.top, NomaTokens.Space.s4)

                ForEach(Array(cardHeights.enumerated()), id: \.offset) { _, height in
                    RoundedRectangle(cornerRadius: NomaTokens.Radius.xl, style: .continuous)
                        .fill(NomaTokens.Surface.raised)
                        .frame(height: height)
                        .nomaShadow(NomaTokens.Elevation.card)
                }
            }
            .padding(.horizontal, NomaTokens.Layout.screenPaddingX)
        }
        // Opt this screen into driving the shrink.
        .nomaTracksBottomNav()
        // The bar is glass; content must be visible through it rather than
        // clipped behind an opaque edge.
        .scrollIndicators(.hidden)
    }
}
