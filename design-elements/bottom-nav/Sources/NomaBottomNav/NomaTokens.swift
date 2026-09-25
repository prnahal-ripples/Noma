import SwiftUI

// ---------------------------------------------------------------------------
// TOKEN MIRROR — hand-copied from the canonical JS token files.
//
//   src/tokens/design.tokens.js   (colour, radius, elevation, spacing, layout)
//   src/tokens/motion.tokens.js   (durations, easings, scale)  → NomaMotion.swift
//
// This is a Swift Package with no build step wired to those JS files, so it
// cannot import them. Same arrangement — and same caveat — as
// design-elements/bottom-sheets/. IF TOKENS DRIFT, THE JS FILES WIN; re-sync
// this file by hand.
//
// Reflects the token file as rebuilt 2026-08-11 (the five laws). Two of those
// laws do real work in this component and are called out where they land:
//
//   LAW 1  the ground is a gradient        → NomaTokens.Gradient.canvas
//   LAW 3  white means raised; selection   → the selected tab is a WHITE
//          is expressed by LIFT, not         RAISED pill, the bar under it is
//          by colour                         translucent grey. See the note in
//                                            MinimizableTabBar.swift — this is
//                                            the one place the component
//                                            deliberately diverges from the
//                                            reference video.
//
// Palette direction: light greyscale (C-14 unresolved — greens are NOT
// referenced here, and no flat green would be legal anyway under LAW 2).
// ---------------------------------------------------------------------------

public enum NomaTokens {

    // MARK: - Primitives
    //
    // Neutral ramp. Do not reference these from view code — go through
    // `Surface` / `Ink` / `Stroke` below, exactly as the JS file requires.

    fileprivate enum Neutral {
        static let n0 = Color(nomaHex: 0xFFFFFF)
        static let n50 = Color(nomaHex: 0xF8F8F8) // [INSPECTOR] icon-button fill
        static let n150 = Color(nomaHex: 0xE8E8E5) // unselected chip fill
        static let n200 = Color(nomaHex: 0xDDDCD8) // canvas gradient, post-veil
        static let n400 = Color(nomaHex: 0x9E9E9C)
        static let n500 = Color(nomaHex: 0x767674)
        static let n800 = Color(nomaHex: 0x2E2E2C) // ink
    }

    // MARK: - Semantic colour

    /// `colors.surface.*`
    public enum Surface {
        /// LAW 3 — white == lifted. The selected tab pill.
        public static let raised = Neutral.n0
        /// [INSPECTOR] icon-button fill #F8F8F8.
        public static let control = Neutral.n50
        /// Unselected chips, inert tracks. The bar's own ground.
        public static let sunken = Neutral.n150
        /// Flat fallback for engines that cannot render `Gradient.canvas`.
        public static let canvas = Color(nomaHex: 0xF4F3F1)
    }

    /// `colors.icon.*`
    public enum Ink {
        public static let primary = Neutral.n800
        public static let secondary = Neutral.n500
        public static let tertiary = Neutral.n400
    }

    /// `colors.border.*`
    public enum Stroke {
        /// [INSPECTOR] 1pt INSIDE stroke of pure white over an #F8F8F8 fill.
        /// That bevel is what makes controls read as glass rather than as flat
        /// discs. It is not decoration — keep it.
        public static let bevel = Neutral.n0
        public static let hairline = Color(nomaHex: 0x0B0B0B, alpha: 0.09)
        public static let subtle = Color(nomaHex: 0x0B0B0B, alpha: 0.05)
    }

    // MARK: - Gradients

    public enum Gradient {
        /// LAW 1 — THE GROUND IS A GRADIENT. White at the top falling to warm
        /// sand dust. Never a flat fill, never grey.
        /// `gradients.canvas.css`, pre-flattened composite of both Figma layers.
        public static let canvas = LinearGradient(
            stops: [
                .init(color: Color(nomaHex: 0xFFFFFF), location: 0.00),
                .init(color: Color(nomaHex: 0xFDFDFC), location: 0.38),
                .init(color: Neutral.n200, location: 1.00),
            ],
            startPoint: .top,
            endPoint: .bottom
        )
    }

    // MARK: - Radius

    public enum Radius {
        public static let sm: CGFloat = 12
        public static let xl: CGFloat = 24 // default card radius [INSPECTOR]
        /// Pills, chips, CTA, circular controls. The bar and its pill both
        /// use Capsule() rather than this value — same intent, cleaner result.
        public static let full: CGFloat = 999
    }

    // MARK: - Elevation
    //
    // CSS blur → SwiftUI shadow radius is blur ÷ 2. SwiftUI's `radius` is a
    // standard deviation, CSS `blur` is roughly twice that. The comments carry
    // the original CSS values so this stays checkable against the JS file.

    public struct ShadowLayer: Sendable {
        public let color: Color
        public let radius: CGFloat
        public let x: CGFloat
        public let y: CGFloat
    }

    public enum Elevation {
        /// `elevation.control` — circular icon buttons and small pills.
        /// Pair with `Stroke.bevel`. CSS: 0 1 3 4%, 0 5 14 7%.
        public static let control: [ShadowLayer] = [
            .init(color: .black.opacity(0.04), radius: 1.5, x: 0, y: 1),
            .init(color: .black.opacity(0.07), radius: 7, x: 0, y: 5),
        ]

        /// `elevation.card` — the default card lift. CSS: 0 2 8 3%, 0 12 32 6%.
        public static let card: [ShadowLayer] = [
            .init(color: .black.opacity(0.03), radius: 4, x: 0, y: 2),
            .init(color: .black.opacity(0.06), radius: 16, x: 0, y: 12),
        ]

        /// `elevation.floating` — CSS: 0 4 12 5%, 0 20 48 10%.
        /// The tab bar's own lift. Wide, faint, low-contrast: its whole job is
        /// to separate a near-white bar from a near-white ground, which takes
        /// spread, not darkness.
        public static let floating: [ShadowLayer] = [
            .init(color: .black.opacity(0.05), radius: 6, x: 0, y: 4),
            .init(color: .black.opacity(0.10), radius: 24, x: 0, y: 20),
        ]
    }

    // MARK: - Spacing & layout

    public enum Space {
        public static let s1: CGFloat = 4
        public static let s2: CGFloat = 8
        public static let s3: CGFloat = 12
        public static let s4: CGFloat = 16
        public static let s5: CGFloat = 20
        public static let s6: CGFloat = 24
    }

    public enum Layout {
        /// `layout.screenPaddingX` — 20 [MEASURED].
        public static let screenPaddingX = Space.s5
        /// `layout.bevelWidth` — 1 [INSPECTOR].
        public static let bevelWidth: CGFloat = 1
        public static let hairlineWidth: CGFloat = 1
    }

    // MARK: - Typography

    public enum Typeface {
        /// Google Sans Flex (SIL OFL), ADR-001 O-2. Assets live at
        /// src/fonts/google-sans-flex/ and must be added to the app target's
        /// Info.plist (`UIAppFonts`) for this name to resolve.
        ///
        /// ⚠ COVERAGE GAP: no Devanagari glyphs, so this cannot be the sole
        /// family for the `hi` locale (ADR-001 O-5, still open). Falls back to
        /// the system face automatically when unavailable.
        public static let family = "Google Sans Flex"

        /// `typography.scale.micro` — 12/16, weight 500, tracking 0.1.
        /// The only text style this component uses (the optional tab caption).
        public static func micro() -> Font {
            .custom(family, size: 12).weight(.medium)
        }
        public static let microTracking: CGFloat = 0.1
        public static let microLineHeight: CGFloat = 16
    }
}

// MARK: - Hex helper

extension Color {
    /// Token-file hex literals only. View code must never call this — it exists
    /// so `NomaTokens` can transcribe the JS values verbatim and stay diffable
    /// against them.
    fileprivate init(nomaHex hex: UInt32, alpha: Double = 1) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: alpha
        )
    }
}

// MARK: - Shadow application

extension View {
    /// Applies a multi-layer elevation token in order, back layer first.
    func nomaShadow(_ layers: [NomaTokens.ShadowLayer]) -> some View {
        layers.reduce(AnyView(self)) { view, layer in
            AnyView(view.shadow(color: layer.color, radius: layer.radius, x: layer.x, y: layer.y))
        }
    }
}
