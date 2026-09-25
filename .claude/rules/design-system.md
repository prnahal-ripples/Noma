# RULES — Design System

> Status: STUB — most of this is still to be filled in.
> Gates: tokens only (no raw hex/px), approved components, icon set, file structure. Each gate must be greppable.

TODO(owner): populate the remaining gates (tokens-only enforcement, icon set,
file structure). See CLAUDE.md and memory/index.md for how it fits in.

## Approved components — 2026-08-12, first real entry in this gate

Registered, not just present in `design-elements/`. Full index and how to add
one: [`design-elements/README.md`](../../design-elements/README.md).

| Component | Canonical location |
|---|---|
| Bottom Sheets | `design-elements/bottom-sheets/` |
| Bottom Navigation Bar | `design-elements/bottom-nav/` |

Nothing else in `design-elements/` (or anywhere else) is approved. A folder
existing there is not the gate — a row here is.

## Icon set — 2026-08-14, first content for this gate, still not approved

The gate this file has stubbed since creation. First real content, and it
does not clear the gate yet:

**Two tiers.** Tier 1 is 3D renders for higher-visibility moments; tier 2 is
the flat monoline set already live in `docs/features/settings/_kit.py`'s
`ICONS` dict (22 icons) and its equivalent in `build-onboarding.py`. Neither
tier has a row in Approved Components above. Tier 2 is running code, proven
by every screenshot in this session's prototypes, but was never formally
registered here — an oversight this entry also flags, not just tier 1's gap.

**Tier 1 (`design-elements/3d-icons/`) now has its assets — updated
2026-08-14.** The four icons named here (info, appearance, notifications,
family) were pasted into the folder by the owner, opened, checked, and
re-encoded to 288px WebP under `web/` so a prototype can embed them and stay
a single portable file. All four render as L2 page headers and were verified
in a browser, not assumed.

**Usage rule, set by the owner and enforced here: sparingly.** A tier-1 icon
is a page header, one per screen. An L1 page may carry two or three. It is
never a row icon and never decoration — that is tier 2's job, and putting a
3D render in a list would undo the thing that makes it read as a header.

**Every L2 inner page takes the header, and it renders at 62px.** Owner
calls on 2026-08-14 took it down twice, 96 → 77 → 62, each a 0.8× step: at
96 and again at 77 the render read too heavy against a 29px title.
Structure: icon, title, centred description, then the page's content.

**The size lives once, in `design.tokens.js` as `layout.iconHeaderSize`** —
read by `_kit.py`'s `ICON_PX` (which feeds both the `<img>` attributes and
the `.ph__i` rule) and by the Vercel dashboard's 3D-icons folder. Grep: a
numeric literal near an icon dimension is a bug; that this resize was one
token edit plus documentation is the point of putting it there. As of this
entry all six L2 pages across the two settings prototypes carry the header;
the two L1 roots deliberately do not.

**A page may claim an icon that hasn't been drawn.** `icon3d()` falls back to
a flat, grey, dashed, name-labelled placeholder rather than failing the
build, so an L2 page is never blocked on artwork. One is outstanding —
`filter` (`rooms` shipped 2026-08-14). The placeholder is deliberately not a
plausible icon: the failure mode worth designing against is a stand-in
quietly becoming the design. Each build prints every placeholder it emitted,
and the manifest carries a `PLACEHOLDER` status per icon. Dropping
`<name>.png` into `design-elements/3d-icons/` and re-running that folder's
resize snippet replaces it with no code change.

**Two icons still conflict with the palette rule, and that blocks the row.**
The painter's palette carries blue/red/yellow/brown; the notification badge
is red. Both sit outside the 2026-08-12 two-green rule. Whether that rule
binds a 3D render of a real-world object — as opposed to the product's own
surfaces — is an owner call. Per this gate's standing rule that a folder is
not the gate, a row is, **3D Icons does not get an Approved Components row
until that call is made.** The bar it has now cleared is existence and
verification; the one left is the palette decision.

## Large surfaces — 2026-08-19, and this one IS greppable

The card design, from the owner's Figma inspector. Canonical values:
`recipes.largeSurface` in `src/tokens/design.tokens.js`. Geometry:
`docs/_squircle.py`. Spec page: `docs/design/large-surfaces.html`
(generated — do not hand-edit).

    corner radius   34 (radius.xxxl), all four
    smoothing       100% (radius.smoothing) — a superellipse, not an arc
    fill            #F9F9F9 under a white->neutral300 layer at 24%
    stroke          1px #FFFFFF, INSIDE
    effect          drop shadow (elevation.floating)

### Gates

1. **`radius.xxxl` is for grounds only.** Owner: *"this card design will only
   apply on larger cards, like bottom sheets or maybe bigger cards. It won't
   apply on smaller cards."* The test is role, not width — a surface is large
   when it is a **ground other things sit on** (sheet, permission dialog,
   full-width card). A row, chip, thumbnail or device tile is an **object on**
   a ground and keeps `recipes.card` (24).
   Grep: `radius.xxxl` / `borderRadius: 34` outside `recipes.largeSurface`,
   `recipes.bottomSheet` and `recipes.dialog` is a bug.

2. **A large surface is never one element.** A mask clips everything an
   element paints, outer shadow included, so the shadow lives on a shell and
   the masked fill on a child. Grep: a `-webkit-mask-box-image` and a
   `box-shadow` on the same selector is a bug — the shadow will not render.

3. **Corner smoothing is rendered, not described.** As of 2026-08-19 the
   prototypes draw the real superellipse. Grep: a large surface whose only
   corner treatment is `border-radius` is a bug; it must also carry the
   9-slice from `docs/_squircle.py`. `border-radius` stays on the shell, but
   ONLY to give the shadow a shape.

4. **Nothing under 136px takes it.** Not taste — arithmetic. The corner needs
   68px of edge to ease into (`SQ.min_size()`), so below 2×68 in either
   direction the corner regions overlap and the shape goes bulbous. This is
   gate 1's boundary expressed in pixels, and it is why a 56-tall list row
   cannot hold this corner at all.

### Still not an Approved Components row

Per this file's standing rule — a folder is not the gate, a row is — large
surfaces is a **recipe**, not a component, so it takes no row in the table
above. The palette question that blocks 3D Icons does not apply here: this
treatment is neutral-only.

## The three CTAs, and the one black — 2026-08-19

Canonical values: `recipes.buttonPrimary` / `buttonQuiet` / `buttonIcon` in
`src/tokens/design.tokens.js`. The reference surface is the **sign-in sheet**
(node 1): owner, 2026-08-19 — *"Look at the primary black one. The secondary,
the white one, and the tertiary, the one without the container. These are the
three correct CTAs. Follow these CTAs throughout."*

| Tier | Fill | Height | Elevation | Class |
|---|---|---|---|---|
| Primary | ink gradient `#3A3A38 → #2E2E2C` | 54 | `dock` | `.cta` / `.s-cta` |
| Secondary | `#FFFFFF` + 1px white inside stroke | 46 | `control` | `.cta2` / `.ghost` |
| Tertiary | none | 46 | none | `.qlink` / `.ghost--bare` |

### Gates

1. **`--ink` (#0B0B0B) IS NEVER A FILL.** Owner: *"do not use any other black.
   Don't use the absolute black color."* It is the TEXT colour. Every dark
   *surface* — CTA, selected chip, toggle track, checkbox — takes the ink
   gradient.
   Grep: `background:var(--ink)` on a control or selection state is a bug.
   Small dark *marks* (signal bars, carets, dots, clock hands) are fine — the
   rule is about surfaces.

2. **One back button.** `recipes.buttonIcon`: 40px, `#F8F8F8`, **1px `#FFFFFF`
   INSIDE stroke**, two-layer drop shadow, and the shared `BACK_SVG` chevron.
   The inside stroke is what makes it read as glass — it is not optional.
   Grep: a nav button with no `inset 0 0 0 1px` is a bug. There must be exactly
   one back-button glyph definition; `nav()` and `sheetback()` share `BACK_SVG`.

3. **A page-level control never redeclares a button.** `build-prototype.py`
   predates the token loader, and that is exactly how `.cta` drifted to a flat
   #0B0B0B while the sheet's `.s-cta` had the gradient — two stylesheets, two
   buttons, and node 5's OTP sheet silently pulled the wrong one. All of
   `.cta` / `.cta2` / `.qlink` / `.nb` / `.chip` / `.rs__t` / `.tog` / `.chk` /
   `.pcard` now read the recipes in that file's token-driven append block.
   Grep: a new raw `background:` on any of those selectors is a regression.

4. **Selection is legible or it is not selection.** `.pcard.on` lifts from
   `card` to `floating` — two steps of the elevation scale. A one-step
   difference is invisible; the first attempt at this used `control` for both
   and the selected card could not be picked out.

5. **Engraved glyphs are PAGE HEADERS ONLY, at 0.8×** (77px; Wi-Fi 83×77).
   Nothing smaller may take one: a list row gets a plain monoline mark. Grep:
   `var(--gly` inside a row/tile rule is a bug — the engraved render at 30px
   reads as a smudge.

6. **A top-aligned page gets a REAL nav bar.** `.scr:has(.pgb.pgb--top) .nav`
   is `position:static` and reserves its own height, so nothing can ride up
   under the back button. Do not buy clearance with a `min-height` spacer on
   `.pgt` — that was tried, and it broke the moment a page had no visual half.

⚠ **C-15 is open** (`memory/decisions.md`): a selected chip FILLS but a
selected card LIFTS, and LAW 3 forbids the fill. Both are built as described
above; the inconsistency is flagged, not resolved.

## Icons — the register boundary, 2026-08-19

The icon gate above had "two tiers" and that was already wrong; there are
**four registers**, and the newest one has a hard size ceiling. Canonical set
and provenance: `design-elements/icons/` (Lucide, ISC, vendored with its
LICENSE and a manifest).

| Register | Size | Source | Consumed by |
|---|---|---|---|
| **Small UI** | **≤ 24px** | **Lucide** | `icon(name, px)` |
| Engraved | 77px (0.8×) | `design-elements/engraved-icons/` | `glyph(kind)` |
| 3D renders | `layout.iconHeaderSize` | `design-elements/3d-icons/` | `icon3d()` |
| Illustration | a screen's visual half | `design-elements/illustrations/` | per screen |

### Gates

1. **The ceiling is the rule.** Owner: *"these icons will be used for smaller
   24x24 px icons only, only smaller than 24 icons. don't change any other
   larger icons and engraved or 3d icons."* Grep: `icon(` with a `px` above 24
   is a bug — that size belongs to another register.

2. **Small icons are INLINED, not data-URI'd.** They must inherit `color` from
   whatever they sit in (a row, a dark CTA, a disabled control), and a
   background-image cannot. The engraved glyphs stay background images because
   they have no such need. Grep: a `≤24px` icon referenced through `var(--gly…)`
   is in the wrong register.

3. **`icon()` raises on an unknown name.** Add the `.svg` to
   `design-elements/icons/` — never paste path data into a builder. A missing
   icon that renders an empty box is the kind of thing that ships.

4. **⚠ NEVER hand `icon()` a class that already carries geometry.** This bit
   twice on the day the set landed: `.ic-i` drew its own ring with `border` +
   `::before/::after` (which would have doubled the glyph's circle), and
   `.sr__lock` set `width`/`height` (which would have overridden the glyph's
   size). Both were reduced to colour and flow only.
   Grep the class you are about to pass for `width:`, `height:`, `clip-path:`,
   `border:` or `border-radius:` first.

5. **⚠ `.sig` IS THE STATUS BAR, NOT A SIGNAL METER.** The Wi-Fi row's strength
   meter used `class="sig"` and so inherited
   `.sig{width:17px;height:11px;clip-path:polygon(…)}` from the phone's own
   chrome. The clip-path was what you actually saw — one fixed shape — and the
   strength `sigbars()` computes never rendered at all: three networks at 4/3/2
   bars drew identical icons. The meter is `.sigm` now. The status bar's own
   glyphs are **out of the register entirely**: they imitate iOS, not NOMA.

### Deliberately not Lucide

Brand marks (Apple, Google, the wordmark), the key card's owner-supplied edit
glyph, product artwork, and form **controls** (`.rad` / `.chk` / `.tog` — a
radio, checkbox and switch have states, so they stay CSS). Lucide carries no
brand logos by policy, and substituting a lookalike for a trademark is a legal
question rather than a style one.

⚠ **One placeholder is knowingly left.** `.ri`, the leading square on generic
`rows()`, is still a grey block. Filling it would mean *inventing* a glyph per
row rather than converting an existing one, and most of those rows (help,
troubleshooting) arguably want no icon at all. Owner call.
