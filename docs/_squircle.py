"""
SQUIRCLE CORNERS — Figma "corner smoothing", as CSS that survives any size.

WHY THIS FILE EXISTS. `border-radius` draws a CIRCULAR arc. iOS (and Figma at
100% corner smoothing) draws a SUPERELLIPSE: the curvature ramps in from the
straight edge instead of starting abruptly, which is the whole reason an iOS
card reads as "soft" and a CSS card reads as "rounded". There is no CSS
property for it, so the shape has to be supplied as artwork.

    Owner, 2026-08-19: "the corner smoothing is very high like iOS to give a
    premium feel. I do not see that here."

THE TRICK, AND WHY IT IS NOT `clip-path`. A bottom sheet changes height on
every state, so a fixed `clip-path: path()` would need JS and a ResizeObserver
and would break mid-transition. Instead the corner is emitted as a 9-SLICE
image: the four corners are painted at their natural size and the edges are
stretched between them. `mask-border` (Chrome: `-webkit-mask-box-image`)
clips the element's own gradient to that shape at ANY width and height, with
no script and nothing to keep in sync.

THREE LAYERS, ONE ELEMENT — see `surface_css()`:
    fill    the element's own CSS background (a real gradient, undistorted —
            the mask only clips, it never stretches what it clips)
    stroke  a second 9-slice via `border-image`, drawn INSIDE the same path,
            so the hairline follows the squircle and not a rounded rect
    shadow  stays on the PARENT. A mask clips everything the element paints,
            outer shadow included, so a masked element cannot cast one.

THE MATH is Figma's own, ported from the `figma-squircle` library so the
corner matches what the owner drew rather than approximating it with a
hand-tuned superellipse exponent. Smoothing is read from
`radius.smoothing` in the token file — this module never hardcodes it.
"""

import math
from urllib.parse import quote


def _corner(r, smoothing, budget):
    """Figma's per-corner parameters. `budget` caps the corner's reach so two
    corners on a short edge cannot overrun each other (half the shorter side).

    Returns the four bezier offsets (a, b, c, d), the arc chord, and `p` —
    how far the corner's influence extends along each edge. `p` is what the
    9-slice has to be sliced at: anything less would cut the curve."""
    p = min((1 + smoothing) * r, budget)
    arc = 90 * (1 - smoothing)                      # degrees still drawn as a true arc
    chord = math.sin(math.radians(arc / 2)) * r * math.sqrt(2)
    alpha = (90 - arc) / 2
    beta = 45 * smoothing
    d_ = r * math.tan(math.radians(beta / 2))
    c = d_ * math.cos(math.radians(alpha))
    d = c * math.tan(math.radians(alpha))
    b = (p - chord - c - d) / 3
    a = 2 * b
    return a, b, c, d, p, chord


def path(w, h, r, smoothing):
    """The closed squircle outline for a w x h box, as SVG path data."""
    a, b, c, d, p, chord = _corner(r, smoothing, min(w, h) / 2)
    f = lambda *v: " ".join(("%.4f" % x).rstrip("0").rstrip(".") or "0" for x in v)
    return (
        f"M {f(w - p)} 0 "
        f"c {f(a, 0, a + b, 0, a + b + c, d)} "
        f"a {f(r, r)} 0 0 1 {f(chord, chord)} "
        f"c {f(d, c, d, b + c, d, a + b + c)} "
        f"L {f(w)} {f(h - p)} "
        f"c {f(0, a, 0, a + b, -d, a + b + c)} "
        f"a {f(r, r)} 0 0 1 {f(-chord, chord)} "
        f"c {f(-c, d, -(b + c), d, -(a + b + c), d)} "
        f"L {f(p)} {f(h)} "
        f"c {f(-a, 0, -(a + b), 0, -(a + b + c), -d)} "
        f"a {f(r, r)} 0 0 1 {f(-chord, -chord)} "
        f"c {f(-d, -c, -d, -(b + c), -d, -(a + b + c))} "
        f"L 0 {f(p)} "
        f"c {f(0, -a, 0, -(a + b), d, -(a + b + c))} "
        f"a {f(r, r)} 0 0 1 {f(chord, -chord)} "
        f"c {f(c, -d, b + c, -d, a + b + c, -d)} Z")


def slice_px(r, smoothing):
    """The 9-slice inset — the corner's full reach, `p` in Figma's terms."""
    return math.ceil((1 + smoothing) * r)


def min_size(r, smoothing):
    """The smallest box this corner can be drawn on, both axes.

    ⚠ A REAL CONSTRAINT, not a rounding guard. The corner needs `p` of edge to
    ease into, so two corners need 2p between them; below that the 9-slice's
    corner regions overlap and the shape goes bulbous — adjacent specimens look
    like they are merging into each other.

    At r=34 / smoothing=1 that is 136px, which is also the arithmetic behind
    the owner's rule that the large-surface treatment belongs to grounds and
    not to rows: a 56-tall list row cannot hold this corner at all."""
    return 2 * slice_px(r, smoothing)


def _uri(svg):
    """Data URI. Kept as readable UTF-8 rather than base64 so the shape stays
    greppable in the built HTML — and so a wrong corner is debuggable.

    UNQUOTED on purpose. `quote(safe="")` leaves no whitespace, parentheses or
    quote marks in the payload, so `url()` needs no delimiters — and a quoted
    URI would end the attribute the moment this lands in an inline `style="…"`,
    silently masking the element down to nothing instead of erroring."""
    return "url(data:image/svg+xml,%s)" % quote(svg, safe="")


def _svg(r, smoothing, paint):
    """One 9-slice tile: a square just big enough for two corner reaches plus
    a 2px middle for the stretched edges to be sampled from."""
    s = slice_px(r, smoothing)
    box = 2 * s + 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d"><path d="%s" %s/></svg>'
            % (box, box, box, box, path(box, box, r, smoothing), paint))


def mask_uri(r, smoothing):
    return _uri(_svg(r, smoothing, 'fill="#fff"'))


def stroke_uri(r, smoothing, color, width=1):
    """Stroked ON the path with double width: SVG centres a stroke on its
    outline, so half falls outside the shape and is then clipped away by the
    mask — which is exactly Figma's "Inside" stroke position."""
    # NB: the colour goes in RAW. `_uri` percent-encodes the whole document,
    # so pre-escaping the "#" here would ship "%2523" and silently kill the
    # hairline — the border-image would fail to load and fall back to the
    # transparent border underneath it.
    return _uri(_svg(r, smoothing, 'fill="none" stroke="%s" stroke-width="%s"'
                     % (color, width * 2)))


def surface_css(r, smoothing, stroke=None, stroke_width=1):
    """The declarations that turn an element into a smoothed surface.

    Apply to the element that carries the FILL. Its parent keeps the shadow
    and a plain `border-radius` of the same r — a blurred shadow cannot show
    the difference between an arc and a superellipse, and putting it on the
    parent is what lets the fill be masked at all."""
    s = slice_px(r, smoothing)
    out = [
        "-webkit-mask-box-image:%s %d stretch" % (mask_uri(r, smoothing), s),
        "mask-border:%s %d stretch" % (mask_uri(r, smoothing), s),
    ]
    if stroke:
        out += [
            # the border area only carries the hairline artwork; it must not
            # push the content in, so the box is border-box and the padding
            # is set by whoever uses this.
            "border:%dpx solid transparent" % s,
            "border-image:%s %d stretch" % (stroke_uri(r, smoothing, stroke, stroke_width), s),
            "background-origin:border-box",
            "box-sizing:border-box",
        ]
    return ";".join(out)
