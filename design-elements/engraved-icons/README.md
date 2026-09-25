# Engraved icons

Owner-supplied SVG, 2026-08-18. Canonical registry:
[`manifest.json`](./manifest.json).

## What this register is, and why it is not one of the other two

`.claude/rules/design-system.md` describes exactly **two** icon tiers: tier 1
is 3D renders for page headers, tier 2 is the flat monoline set for rows. These
are neither. They are large **engraved glyphs** — a soft grey vertical gradient
with a drop shadow and an inner shadow, so the shape reads as pressed *into* the
surface rather than drawn on it. They carry a page the way a 3D render does,
without being a photograph of an object.

⚠ **That makes the icon gate's "two tiers" wrong as written**, and this folder
does not get to fix a rule by existing. An owner call: either the gate becomes
three registers, or these are folded into tier 1 as its non-photographic half.

| Icon | File | Used on |
|---|---|---|
| Bluetooth | `bluetooth.svg` | node 11 · looking for your purifier |
| Wi-Fi | `wifi.svg` | nodes 13 and 12 · choose and confirm the network |
| Check | `check-circle.svg` | node 16 · connected |
| Notifications | `notifications-unread.svg` | node 25 · the notification ask |

**Usage: one per page, in the visual half, at 96–104px. Never a row icon** —
at row scale the gradient and the two shadows collapse into a grey smudge,
which is the whole reason tier 2 exists.

**Embedded as base64 data URIs, not inlined markup.** Every file carries
Figma-generated filter and gradient ids (`filter0_di_…`, `paint0_linear_…`), and
two screens share the DOM during a transition — inlining would collide them.

⚠ **`notifications-unread.svg` carries a non-palette red.** Its unread dot is
`#FF4444` at 54%; the palette's token for exactly this is `red.mid` (#D65151),
which is what the drawn bell it replaced used. Left as supplied — recolouring
the owner's artwork silently would hide the divergence rather than settle it.

## Adding one

Drop the SVG here, add a row to `manifest.json`, and reference it from
`build-prototype.py`'s `GLYPH_B64` dict — the builder embeds every entry
automatically. Then mirror the file into the Vercel dashboard at
`design/noma/engraved-icons/` and add it to `NOMA_ENGRAVED` in
`dashboard/dashboard.js`, which is how that folder lists them.
