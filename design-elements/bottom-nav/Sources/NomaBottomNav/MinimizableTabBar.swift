import SwiftUI

// ---------------------------------------------------------------------------
// THE BAR.
//
// Reconstructed from Kavsoft's "Instagram App's Minimizable Tab Bar Using
// SwiftUI" (youtu.be/691o2FUDs-8) by stepping the reference clip frame by frame.
// The tutorial's own source was not available, so this is a rebuild of the
// observed behaviour, not a transcription of his code. Three things were read
// off the reference:
//
//   1. A FLOATING PILL, inset from the screen edges, with content scrolling
//      underneath it — not a full-width bar pinned to the bottom edge.
//
//   2. A SELECTION BLOB that lifts off the bar and travels to the tapped tab.
//      Clearest at 6.0s and 7.5s of the reference, where the capsule is caught
//      mid-flight between the first and second tab, visibly raised and bulging.
//
//   3. SHRINK ON SCROLL-DOWN. The bar narrows and its icons tighten, then it
//      re-expands on scroll-up. Across all 26s of the reference it never
//      collapses to a single icon and never leaves the screen — it is a shrink,
//      not a collapse and not a hide. Handled in NomaTabScaffold.
//
// ⚠ ONE DELIBERATE DIVERGENCE FROM THE REFERENCE. In the video the selected
// pill is a slightly DARKER grey than the bar around it. NOMA's LAW 3 says the
// opposite: white means raised, and selection is expressed by LIFT, not by
// colour — a selected chip is a white raised pill, an unselected one is sunken
// grey. The token file calls a colour-only selection a bug. So the pill here is
// WHITE and raised on a translucent grey bar. Every other aspect of the
// reference is reproduced. If the owner wants literal video fidelity instead,
// that is a C-14 palette decision, not a code change — flip `Surface.raised` to
// a sunken value in ONE place below.
// ---------------------------------------------------------------------------

/// The two geometry states the bar interpolates between.
///
/// Every number here is a reading off the reference clip, not a measurement —
/// the recording zooms during playback, so absolute pixel comparisons between
/// frames are unreliable. The RATIOS are what was preserved: the minimized bar
/// is roughly three-quarters the width of the expanded one, and its glyphs
/// about four-fifths the size.
public struct NomaTabBarMetrics: Equatable, Sendable {

    /// Horizontal slot per tab. Also the tap target width.
    public var itemWidth: CGFloat
    /// Overall bar height.
    public var height: CGFloat
    /// Glyph point size.
    public var iconSize: CGFloat
    /// Padding between the bar's edge and the first/last slot.
    public var innerPadding: CGFloat
    /// Vertical inset of the selection pill inside the bar.
    public var pillInsetY: CGFloat

    /// Apple's HIG minimum tap target. `itemWidth` is clamped to this so a
    /// long tab set can never shrink the touch area below it.
    public static let minimumTapTarget: CGFloat = 44

    public static let expanded = NomaTabBarMetrics(
        itemWidth: 66,
        height: 64,
        iconSize: 25,
        innerPadding: NomaTokens.Space.s2,
        pillInsetY: NomaTokens.Space.s2
    )

    public static let minimized = NomaTabBarMetrics(
        itemWidth: 50,
        height: 52,
        iconSize: 21,
        innerPadding: NomaTokens.Space.s1 + 2,
        pillInsetY: NomaTokens.Space.s1 + 2
    )

    func barWidth(tabCount: Int) -> CGFloat {
        max(itemWidth, Self.minimumTapTarget) * CGFloat(tabCount) + innerPadding * 2
    }

    var slotWidth: CGFloat { max(itemWidth, Self.minimumTapTarget) }
}

public struct MinimizableTabBar: View {

    private let tabs: [NomaTab]
    @Binding private var selection: String
    private let isMinimized: Bool

    /// GATE 2 — the accessibility gate. Read once, threaded through every
    /// animation and every scale effect in this view.
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    /// 0 = pill resting in the bar, 1 = pill lifted for travel.
    @State private var lift: CGFloat = 0
    /// Tab id currently held down, for press feedback.
    @State private var pressedID: String?

    public init(tabs: [NomaTab] = .nomaDefault, selection: Binding<String>, isMinimized: Bool = false) {
        self.tabs = tabs
        self._selection = selection
        self.isMinimized = isMinimized
    }

    private var metrics: NomaTabBarMetrics {
        isMinimized ? .minimized : .expanded
    }

    private var selectedIndex: Int {
        tabs.firstIndex { $0.id == selection } ?? 0
    }

    public var body: some View {
        ZStack {
            selectionPill
            slots
        }
        .frame(
            width: metrics.barWidth(tabCount: tabs.count),
            height: metrics.height
        )
        .background(barGround)
        // The bar is a single tab-bar element to assistive tech, containing the
        // individual tab buttons.
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("noma.bottomNav")
        // No-op on macOS; the real feedback is on device. Left unguarded so the
        // call is covered by the macOS typecheck.
        .sensoryFeedback(.selection, trigger: selection)
    }

    // MARK: - Ground
    //
    // Glass, not a flat fill: `.ultraThinMaterial` for the real blur, tinted
    // toward `Surface.sunken` so the bar reads as the sunken ground the white
    // pill is lifted OFF of (LAW 3), plus the bevel stroke that the inspector
    // notes make controls read as glass rather than as flat discs.

    private var barGround: some View {
        Capsule()
            .fill(.ultraThinMaterial)
            .overlay {
                Capsule().fill(NomaTokens.Surface.sunken.opacity(0.55))
            }
            .overlay {
                Capsule().strokeBorder(
                    NomaTokens.Stroke.bevel.opacity(0.6),
                    lineWidth: NomaTokens.Layout.bevelWidth
                )
            }
            .nomaShadow(NomaTokens.Elevation.floating)
    }

    // MARK: - Selection pill
    //
    // LAW 3 — white == lifted. This is the one line to change if the owner
    // wants the reference video's darker-than-the-bar pill instead.

    private var selectionPill: some View {
        Capsule()
            .fill(NomaTokens.Surface.raised)
            .overlay {
                Capsule().strokeBorder(
                    NomaTokens.Stroke.bevel,
                    lineWidth: NomaTokens.Layout.bevelWidth
                )
            }
            .nomaShadow(NomaTokens.Elevation.control)
            .frame(
                width: metrics.slotWidth - NomaTokens.Space.s2,
                height: metrics.height - metrics.pillInsetY * 2
            )
            // The lift: bulges as it leaves, settles back to rest on arrival.
            .nomaScaleEffect(1 + (NomaMotion.Scale.pop - 1) * lift, reduceMotion: reduceMotion)
            .offset(x: pillOffsetX)
            // Decorative — the selected state is announced on the button itself.
            .accessibilityHidden(true)
    }

    /// Distance from the bar's centre to the centre of the selected slot.
    private var pillOffsetX: CGFloat {
        guard !tabs.isEmpty else { return 0 }
        let centreIndex = CGFloat(tabs.count - 1) / 2
        return (CGFloat(selectedIndex) - centreIndex) * metrics.slotWidth
    }

    // MARK: - Slots

    private var slots: some View {
        HStack(spacing: 0) {
            ForEach(tabs) { tab in
                slot(for: tab)
            }
        }
    }

    private func slot(for tab: NomaTab) -> some View {
        let isSelected = tab.id == selection
        let isPressed = pressedID == tab.id

        return Button {
            select(tab)
        } label: {
            // Rendered at the expanded size and scaled down, because SwiftUI
            // snaps between font sizes rather than interpolating them — a
            // scaleEffect is what makes the shrink continuous.
            Image(systemName: isSelected ? tab.selectedSymbol : tab.symbol)
                .font(.system(size: NomaTabBarMetrics.expanded.iconSize, weight: .regular))
                .scaleEffect(metrics.iconSize / NomaTabBarMetrics.expanded.iconSize)
                .foregroundStyle(isSelected ? NomaTokens.Ink.primary : NomaTokens.Ink.tertiary)
                .frame(width: metrics.slotWidth, height: metrics.height)
                // Whole slot is tappable, not just the glyph.
                .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .nomaScaleEffect(isPressed ? NomaMotion.Scale.press : 1, reduceMotion: reduceMotion)
        .animation(NomaMotion.resolve(NomaMotion.press, reduceMotion: reduceMotion), value: isPressed)
        .animation(NomaMotion.resolve(NomaMotion.iconSwap, reduceMotion: reduceMotion), value: isSelected)
        .onLongPressGesture(minimumDuration: 0, pressing: { pressing in
            pressedID = pressing ? tab.id : nil
        }, perform: {})
        .accessibilityLabel(tab.label)
        .accessibilityAddTraits(isSelected ? [.isButton, .isSelected] : [.isButton])
        .accessibilityIdentifier("noma.bottomNav.\(tab.id)")
    }

    // MARK: - Selection

    /// Lift, travel, settle — three animations on named tokens.
    ///
    /// Note this runs on TAP only. A selection changed from outside (deep link,
    /// programmatic navigation) moves the pill without the lift, because there
    /// is no gesture to have caused it.
    private func select(_ tab: NomaTab) {
        guard tab.id != selection else { return }

        withAnimation(NomaMotion.resolve(NomaMotion.liftOut, reduceMotion: reduceMotion)) {
            lift = 1
        }
        withAnimation(NomaMotion.resolve(NomaMotion.tabTravel, reduceMotion: reduceMotion)) {
            selection = tab.id
        }
        withAnimation(
            NomaMotion.resolve(
                NomaMotion.liftIn,
                reduceMotion: reduceMotion,
                delay: NomaMotion.liftSettleDelay
            )
        ) {
            lift = 0
        }
    }
}
