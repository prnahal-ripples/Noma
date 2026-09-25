import SwiftUI

// ---------------------------------------------------------------------------
// THE TAB MODEL.
//
// CLAUDE.md rule 4 — no hardcoded strings. A tab carries an i18n KEY, never
// display copy. Keys follow strings.schema.json's `<screen-or-domain>.<element>`
// format and are registered in src/i18n/locales/en/common.json.
//
// ⚠ PROVISIONAL SET. The owner's instruction was "keep them as home, device,
// automation and profile" pending a real information architecture. These are
// placeholders with stable ids, not a decided navigation model — `NomaTab` takes
// any array, and the bar lays out whatever it is given.
// ---------------------------------------------------------------------------

public struct NomaTab: Identifiable, Hashable, Sendable {

    /// Stable id. Analytics will need this to survive a label change, so it is
    /// deliberately not derived from the title.
    public let id: String

    /// i18n key — resolved by the app's string catalogue, never shown raw.
    /// Carries the accessibility label; the bar is icon-only, so for VoiceOver
    /// users this key IS the tab's name.
    ///
    /// Held as a `String` rather than a `LocalizedStringKey` for two reasons:
    /// `LocalizedStringKey` is not `Sendable`, and analytics and UI tests both
    /// want the raw key. Use `label` to render it.
    public let labelKey: String

    /// The key resolved for display. Everything user-facing goes through here.
    public var label: LocalizedStringKey { LocalizedStringKey(labelKey) }

    /// SF Symbol shown when the tab is not selected — outline weight.
    public let symbol: String

    /// SF Symbol shown when the tab is selected — filled weight. The reference
    /// video switches glyph weight on selection as well as lifting the pill.
    public let selectedSymbol: String

    public init(id: String, labelKey: String, symbol: String, selectedSymbol: String) {
        self.id = id
        self.labelKey = labelKey
        self.symbol = symbol
        self.selectedSymbol = selectedSymbol
    }

    // Hashable/Equatable on `id` alone. A tab that gets a new label, a new
    // glyph, or both is still the same tab — identity is the thing analytics
    // and selection state hang off, so it must not drift with presentation.
    public static func == (lhs: NomaTab, rhs: NomaTab) -> Bool { lhs.id == rhs.id }
    public func hash(into hasher: inout Hasher) { hasher.combine(id) }
}

// Declared on the array rather than on `NomaTab` so that it is reachable as a
// leading-dot default argument (`tabs: [NomaTab] = .nomaDefault`). One canonical
// home — there is no `NomaTab.nomaDefault` mirroring this.
public extension Array where Element == NomaTab {

    /// The provisional NOMA set.
    ///
    /// ⚠ SYMBOL AVAILABILITY, UNVERIFIED HERE: `air.purifier` is SF Symbols 5
    /// (iOS 17+). This package could not be compiled against an iOS SDK on the
    /// machine that wrote it, so the symbol names are asserted from the SF
    /// Symbols catalogue rather than resolved by the compiler. A missing symbol
    /// renders as a placeholder rather than crashing, but check them in Xcode
    /// before this goes anywhere real. `flowchart` for Automation is a
    /// deliberate swap-me choice — `sparkles` reads more agent-first but has no
    /// filled counterpart, and the selected state needs one.
    static var nomaDefault: [NomaTab] { [
        NomaTab(
            id: "home",
            labelKey: "nav.home.label",
            symbol: "house",
            selectedSymbol: "house.fill"
        ),
        NomaTab(
            id: "device",
            labelKey: "nav.device.label",
            symbol: "air.purifier",
            selectedSymbol: "air.purifier.fill"
        ),
        NomaTab(
            id: "automation",
            labelKey: "nav.automation.label",
            symbol: "flowchart",
            selectedSymbol: "flowchart.fill"
        ),
        NomaTab(
            id: "profile",
            labelKey: "nav.profile.label",
            symbol: "person.crop.circle",
            selectedSymbol: "person.crop.circle.fill"
        ),
    ] }
}
