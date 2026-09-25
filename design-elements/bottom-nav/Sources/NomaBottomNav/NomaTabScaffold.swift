import SwiftUI

// ---------------------------------------------------------------------------
// THE CONTAINER — owns selection, owns the minimized state, and decides when to
// shrink.
//
// The scroll signal cannot come from here: the ScrollView belongs to whatever
// the app puts in a tab. So the scaffold publishes a reporting closure through
// the environment, and each scrollable screen opts in with
// `.nomaTracksBottomNav()`. A tab with nothing scrollable simply never reports,
// and its bar stays expanded — which is the correct behaviour, not a gap.
// ---------------------------------------------------------------------------

/// What the bar needs to know about a scroll view, per geometry change.
///
/// Carries the content and container heights as well as the offset, because
/// "did the user scroll down" is not answerable from the offset alone — a short
/// screen that rubber-bands must not be allowed to shrink the bar.
public struct NomaScrollProbe: Equatable, Sendable {
    public var offsetY: CGFloat
    public var contentHeight: CGFloat
    public var containerHeight: CGFloat
}

/// Distance thresholds for the shrink decision. Points, not durations — the
/// motion tokens have no vocabulary for these, so they live with the component
/// that reads them.
public enum NomaScrollShrink {
    /// Minimum movement before a direction is believed. Below this, a finger
    /// resting on the glass or a one-pixel layout settle would flip the bar.
    public static let directionThreshold: CGFloat = 6

    /// Offset below which the bar always expands, regardless of direction. Keeps
    /// the bar open at the top of a list and through the rubber-band above it.
    public static let topRestZone: CGFloat = 12

    /// How much taller than its container the content must be before shrinking
    /// is allowed at all. A screen with barely more than a screenful has nothing
    /// to gain from a smaller bar and would just flicker.
    public static let minimumScrollableOverflow: CGFloat = 80
}

// MARK: - Environment plumbing

private struct NomaScrollReportKey: EnvironmentKey {
    static let defaultValue: @MainActor (NomaScrollProbe, NomaScrollProbe) -> Void = { _, _ in }
}

extension EnvironmentValues {
    var nomaScrollReport: @MainActor (NomaScrollProbe, NomaScrollProbe) -> Void {
        get { self[NomaScrollReportKey.self] }
        set { self[NomaScrollReportKey.self] = newValue }
    }
}

private struct NomaScrollTracker: ViewModifier {
    @Environment(\.nomaScrollReport) private var report

    func body(content: Content) -> some View {
        content.onScrollGeometryChange(for: NomaScrollProbe.self) { geometry in
            NomaScrollProbe(
                // Normalised so that "resting at the top" is 0 regardless of
                // how much safe-area inset the scroll view was given.
                offsetY: geometry.contentOffset.y + geometry.contentInsets.top,
                contentHeight: geometry.contentSize.height,
                containerHeight: geometry.containerSize.height
            )
        } action: { old, new in
            report(old, new)
        }
    }
}

public extension View {
    /// Opt a scroll view into driving the bottom bar's shrink. Apply to the
    /// `ScrollView` (or `List`) inside a tab, not to the tab's root.
    func nomaTracksBottomNav() -> some View {
        modifier(NomaScrollTracker())
    }
}

// MARK: - Scaffold

public struct NomaTabScaffold<Content: View>: View {

    private let tabs: [NomaTab]
    @Binding private var selection: String
    private let content: (NomaTab) -> Content

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var isMinimized = false

    public init(
        tabs: [NomaTab] = .nomaDefault,
        selection: Binding<String>,
        @ViewBuilder content: @escaping (NomaTab) -> Content
    ) {
        self.tabs = tabs
        self._selection = selection
        self.content = content
    }

    private var selectedTab: NomaTab {
        tabs.first { $0.id == selection } ?? tabs[0]
    }

    /// Constant — deliberately the EXPANDED height even while minimized. If the
    /// reserved space tracked the bar's actual height, every shrink would reflow
    /// the content underneath it, which turns a calm scroll into a jitter.
    ///
    /// Includes `s3` of clearance so the bar floats above the home indicator
    /// rather than sitting on it. Paired with `.bottom` alignment and a matching
    /// bottom padding below, which together pin the bar's BOTTOM edge: it shrinks
    /// upward from a fixed baseline instead of drifting down the screen.
    private var reservedHeight: CGFloat {
        NomaTabBarMetrics.expanded.height + NomaTokens.Space.s3
    }

    public var body: some View {
        ZStack {
            // LAW 1 — the ground is a gradient, never a flat fill.
            NomaTokens.Gradient.canvas
                .ignoresSafeArea()

            content(selectedTab)
                .environment(\.nomaScrollReport, handleScroll)
        }
        // A fixed-height inset holding the bar: reserves room at rest, and lets
        // scroll content pass underneath the bar in motion.
        .safeAreaInset(edge: .bottom, spacing: 0) {
            MinimizableTabBar(
                tabs: tabs,
                selection: $selection,
                isMinimized: isMinimized
            )
            .padding(.bottom, NomaTokens.Space.s3)
            .frame(height: reservedHeight, alignment: .bottom)
        }
    }

    // MARK: - The shrink decision

    private func handleScroll(_ old: NomaScrollProbe, _ new: NomaScrollProbe) {
        // Nothing meaningful to scroll — stay open.
        guard new.contentHeight > new.containerHeight + NomaScrollShrink.minimumScrollableOverflow else {
            setMinimized(false)
            return
        }

        // At or above the top of the content — always open. Also catches the
        // rubber-band, where the delta briefly reads as a downward scroll.
        guard new.offsetY > NomaScrollShrink.topRestZone else {
            setMinimized(false)
            return
        }

        let delta = new.offsetY - old.offsetY
        guard abs(delta) > NomaScrollShrink.directionThreshold else { return }

        // Scrolling down (content moving up) minimizes; scrolling up expands.
        setMinimized(delta > 0)
    }

    private func setMinimized(_ value: Bool) {
        guard value != isMinimized else { return }

        // GATE 3 — the shrink settles flat, only the re-expand may spring.
        let curve = value ? NomaMotion.barMinimize : NomaMotion.barExpand

        withAnimation(NomaMotion.resolve(curve, reduceMotion: reduceMotion)) {
            isMinimized = value
        }
    }
}
