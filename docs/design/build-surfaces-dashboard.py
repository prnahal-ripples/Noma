#!/usr/bin/env python3
"""
Build docs/design/large-surfaces.html — the card design, at true size.

    python3 docs/design/build-surfaces-dashboard.py

THE THIRD PAGE IN THE SET. `sizing-and-rhythm` states the vertical grammar,
`scenarios` answers "what goes between THESE two things", and this one answers
"what is this surface MADE of, and is my surface even allowed to be one".

Owner's Figma inspector, 2026-08-19 — four properties and one hard boundary:

    corner radius   34, all four, at 100% corner smoothing
    fill            #F9F9F9 with a white -> neutral300 layer at 24%
    stroke          1px #FFFFFF, INSIDE
    effect          drop shadow

    "this card design will only apply on larger cards, like bottom sheets or
     maybe bigger cards. It won't apply on smaller cards."

That last line is why section 3 exists. Every value is read from
src/tokens/design.tokens.js at build time; nothing here is transcribed.
"""

import base64
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))  # docs/
import _squircle as SQ  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).with_name("large-surfaces.html")
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"
FONTS = ROOT / "src" / "fonts" / "google-sans-flex" / "static"
MARK = ROOT / "design-elements" / "brand" / "web" / "noma-wordmark.webp"


def load(names):
    script = ("import(%s).then(m=>{const {%s}=m;"
              "process.stdout.write(JSON.stringify({%s}));})"
              % (json.dumps(TOKENS.as_uri()), ",".join(names), ",".join(names)))
    r = subprocess.run(["node", "--input-type=module", "-e", script],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr.strip())
    return json.loads(r.stdout)


T = load(["colors", "elevation", "gradients", "layout", "neutral", "radius",
          "rhythm", "spacing", "typography", "recipes"])
C, N, R, S = T["colors"], T["neutral"], T["radius"], T["spacing"]
LAY, RH, RC, EL = T["layout"], T["rhythm"], T["recipes"], T["elevation"]
TX = T["typography"]["scale"]
LS = RC["largeSurface"]

b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
FACE = {w: b64(FONTS / f"GoogleSansFlex_24pt-{n}.ttf")
        for w, n in ((400, "Regular"), (500, "Medium"), (700, "Bold"))}
WORDMARK = b64(MARK) if MARK.exists() else None

# The recipe, as the declarations an element actually takes. Everything on the
# page that claims to BE a large surface is built from this string, so a
# specimen cannot quietly disagree with the spec printed beside it.
SURFACE = SQ.surface_css(LS["borderRadius"], LS["smoothing"],
                         stroke=LS["strokeColor"], stroke_width=LS["strokeWidth"])
SLICE = SQ.slice_px(LS["borderRadius"], LS["smoothing"])
MINSZ = SQ.min_size(LS["borderRadius"], LS["smoothing"])   # 136 at r34 / 100%


def ty(name):
    t = TX[name]
    return ("font-size:%spx;line-height:%spx;letter-spacing:%.3gpx;font-weight:%s;"
            % (t["size"], t["lineHeight"], t["tracking"], t["weight"]))


def sect(num, title, val, why, demo, tok, wide=False):
    return f"""<section class="case">
  <header class="chead"><span class="cn">{num}</span><h3>{title}</h3>
    <span class="val">{val}</span></header>
  <div class="cbody{' cbody--wide' if wide else ''}"><div class="demo">{demo}</div>
    <div class="why">{why}<p><code>{tok}</code></p></div></div>
</section>"""


def surface(inner, w=None, extra=""):
    """A real large surface — shell casts the shadow, child carries the mask."""
    wd = f"width:{w}px;" if w else ""
    return (f'<div class="ls" style="{wd}{extra}">'
            f'<i class="ls__s"></i><div class="ls__c">{inner}</div></div>')


# ---------------------------------------------------------------------------
# 1. THE ANATOMY
# ---------------------------------------------------------------------------
ANATOMY = surface(
    '<span class="anno" style="--d:0">corner radius %d, smoothing %d%%</span>'
    '<span class="anno" style="--d:1">fill %s + 24%% gradient layer</span>'
    '<span class="anno" style="--d:2">stroke %dpx %s, inside</span>'
    '<span class="anno" style="--d:3">drop shadow</span>'
    % (LS["borderRadius"], int(LS["smoothing"] * 100), LS["backgroundFallback"],
       LS["strokeWidth"], LS["strokeColor"]), w=330)

# ---------------------------------------------------------------------------
# 2. THE CORNER — the same radius drawn three ways, at true size
# ---------------------------------------------------------------------------
def corner_demo():
    out = []
    for label, sm in (("border-radius", None), ("smoothing 60%", 0.6),
                      ("smoothing 100%", LS["smoothing"])):
        if sm is None:
            st = f"border-radius:{LS['borderRadius']}px"
        else:
            st = SQ.surface_css(LS["borderRadius"], sm, stroke=LS["strokeColor"])
        out.append(f'<figure class="cnr"><span class="cnr__b" style="{st}"></span>'
                   f'<figcaption>{label}</figcaption></figure>')
    return '<div class="cnrs">' + "".join(out) + "</div>"


# Specimens are drawn at MINSZ, the smallest box this corner fits on — which is
# both the honest size to compare at and, in section 3, the point being made.


# ---------------------------------------------------------------------------
# 3. THE BOUNDARY — the rule that gets broken
# ---------------------------------------------------------------------------
SMALL_R = RC["card"]["borderRadius"]
ROW_H = 56   # a real list-row height, and deliberately far below MINSZ
SQ_BAD = ('<i class="sml__s" style="%s"></i>'
          % SQ.surface_css(LS["borderRadius"], LS["smoothing"], stroke=LS["strokeColor"]))
BOUNDARY = f"""<div class="cmp">
  <div class="cmp__col">
    <span class="cmp__t cmp__t--ok">Takes it &mdash; a ground</span>
    {surface('<b>Bottom sheet</b><span>A surface other things sit on. Tall enough that the '
             'corner has edge to ease into.</span>', extra=f'min-height:{MINSZ}px')}
    {surface('<b>Permission dialog</b><span>Floats over a dimmed screen.</span>',
             extra=f'min-height:{MINSZ}px')}
  </div>
  <div class="cmp__col">
    <span class="cmp__t cmp__t--no">Never &mdash; an object</span>
    <div class="sml" style="border-radius:{SMALL_R}px">
      <b>Device row</b><span>Radius {SMALL_R}, no stroke. Sits ON a ground.</span></div>
    <div class="sml sml--bad">{SQ_BAD}
      <b>The same row, wrongly</b>
      <span>The 34 corner needs {SLICE} of edge and has {ROW_H // 2}. It bulges.</span></div>
  </div>
</div>"""

# ---------------------------------------------------------------------------
# 4. THE SHEET'S TYPE RAMP — the inspector read, as a live sheet
# ---------------------------------------------------------------------------
mark = (f'<img class="wm" src="data:image/webp;base64,{WORDMARK}" alt="NOMA" '
        f'style="width:{LAY["wordmarkSheet"]}px;opacity:{LAY["wordmarkSheetOpacity"]}">'
        if WORDMARK else '<span class="wm wm--t">NOMA</span>')
RAMP = surface(
    f'<div class="sheet">{mark}'
    f'<h4 class="sh1">A calmer kind of smart home.</h4>'
    f'<button class="sc sc--pri">Use mobile number</button>'
    f'<button class="sc sc--qui">Continue with Apple</button>'
    f'<button class="sc sc--bare">Continue with email</button>'
    f'<p class="slegal">By continuing, you agree to our<br>'
    f'<b>Terms of Service</b> and <b>Privacy Policy</b></p></div>', w=330)

RAMP_TABLE = "".join(
    f'<tr><td>{n}</td><td class="n">{TX[k]["size"]}</td>'
    f'<td class="n">{TX[k]["weight"]}</td><td><code>{k}</code></td></tr>'
    for n, k in (("Sheet heading", "display"), ("Primary CTA label", "action"),
                 ("Quiet CTA label", "actionSmall"), ("Legal", "legal")))

CASES = [
    sect("01", "The anatomy", f"radius {LS['borderRadius']}",
         "<p>Four properties, read straight off the owner's Figma inspector. They travel "
         "together &mdash; a surface with the radius but not the stroke reads flat, and the "
         "stroke without the shadow reads like an outline rather than a lit edge.</p>"
         "<p>The fill is <b>not</b> a flat grey. It is "
         f"<code>{LS['backgroundFallback']}</code> with a white-to-neutral gradient over it at "
         "<b>24% opacity</b>, which is what gives the top of a sheet its slight lift.</p>",
         ANATOMY, "recipes.largeSurface"),

    sect("02", "The corner", f"{int(LS['smoothing'] * 100)}% smoothing",
         "<p>All three squares below have the same radius. Only the corner differs, and the "
         "difference is where each one <b>stops being straight</b>: a circular corner turns "
         "abruptly at a tangent point, a smoothed one eases in long before it.</p>"
         "<p><b>These prototypes render the real shape.</b> CSS <code>border-radius</code> "
         "cannot &mdash; it only draws a circular arc &mdash; so <code>docs/_squircle.py</code> "
         "emits Figma's own corner geometry as a 9-slice mask that restretches at any element "
         "size, with no script. Native takes "
         "<code>RoundedRectangle(style: .continuous)</code>.</p>",
         corner_demo(), "radius.smoothing", wide=True),

    sect("03", "What may take it", "grounds only",
         "<p>The owner's boundary, and the rule most likely to be broken by someone applying "
         "the treatment because it looks nice:</p>"
         "<p class=\"quote\">&ldquo;this card design will only apply on larger cards, like "
         "bottom sheets or maybe bigger cards. It won't apply on smaller cards.&rdquo;</p>"
         "<p>The test is not width, it is <b>role</b>. A surface is large when it is a "
         "<b>ground that other things sit on</b>. A row, chip, thumbnail or device tile is an "
         f"<b>object sitting on</b> a ground: it keeps <code>card</code> (radius {SMALL_R}) and "
         "never takes the 34 corner or the white stroke.</p>"
         "<p><b>The rule has arithmetic behind it, not just taste.</b> A smoothed corner needs "
         f"{SLICE}px of edge to ease into, so two of them need <b>{MINSZ}px</b> between them. "
         f"Below {MINSZ} in either direction the corners meet before the edge does and the shape "
         "goes bulbous &mdash; see the last specimen. A 56-tall list row cannot physically hold "
         "this corner, which is why the boundary is where the owner drew it.</p>",
         BOUNDARY, "recipes.largeSurface.appliesTo"),

    sect("04", "The sheet's type ramp", f"{TX['display']['size']} / "
         f"{TX['action']['size']} / {TX['actionSmall']['size']} / {TX['legal']['size']}",
         "<p>The inspector's sizes for the sign-in sheet, live at true size. Two things here "
         "are easy to get wrong.</p>"
         "<p><b>The wordmark is a signature, not a headline</b> &mdash; "
         f"{LAY['wordmarkSheet']}px wide at {int(LAY['wordmarkSheetOpacity'] * 100)}% opacity. "
         "It was 84 at full strength and competed with the heading directly under it.</p>"
         "<p><b>Control labels are smaller than body text.</b> A button's height and fill "
         "already carry its emphasis, so a 16 label inside a 54 pill reads shouty. The 14/12 "
         "split says the primary/secondary hierarchy a second time, after height and fill.</p>"
         f"<table class=\"tbl\"><tr><th>Role</th><th>Size</th><th>Weight</th><th>Token</th></tr>"
         f"{RAMP_TABLE}</table>",
         RAMP, "typography.scale · layout.wordmarkSheet"),

    sect("05", "Why it is two elements", "implementation",
         "<p>A mask clips <b>everything an element paints</b>, and an outer shadow is painted. "
         "So a masked surface cannot cast one, and the recipe needs two nodes:</p>"
         "<p><b>The shell</b> holds the shadow, the position and the transform. Its "
         "<code>border-radius</code> exists only to give the shadow a shape &mdash; under a 48px "
         "blur nothing can tell an arc from a superellipse.</p>"
         "<p><b>The surface</b> is <code>inset:0</code> inside it and carries the fill and the "
         f"hairline, clipped by the 9-slice. Its <code>border:{SLICE}px</code> is the slice's "
         "canvas for the hairline, <b>not padding</b> &mdash; real padding goes on a third, "
         "content layer, which is why the surface must not be the layout parent.</p>"
         "<p>Where a surface has full-bleed content that reaches its edge (a dialog's button "
         "row), the <b>content layer takes the same mask</b> without the stroke. Clipping it "
         "with <code>border-radius</code> instead puts a circular arc inside a superellipse, "
         "and the mismatch shows first at exactly the corner everyone looks at.</p>",
         '<pre class="code">.shell {   /* shadow + border-radius */\n'
         '  box-shadow: …;\n'
         f'  border-radius: {LS["borderRadius"]}px;\n'
         '}\n.shell > .surface {   /* fill + hairline, masked */\n'
         '  position: absolute; inset: 0;\n'
         '  background: …;\n'
         '  -webkit-mask-box-image: …;\n'
         '}\n.shell > .content {   /* padding lives here */\n'
         '  position: relative; z-index: 1;\n}</pre>',
         "docs/_squircle.py"),
]

HTML = f"""<meta charset="utf-8">
<title>NOMA Large Surfaces</title>
<style>
  @font-face{{font-family:GSF;font-weight:400;src:url(data:font/ttf;base64,{FACE[400]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:500;src:url(data:font/ttf;base64,{FACE[500]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:700;src:url(data:font/ttf;base64,{FACE[700]}) format("truetype")}}
  :root{{
    --ground:{N['150']}; --card:{N['0']}; --edge:rgba(11,11,11,.09);
    --ink:{C['text']['primary']}; --sec:{C['text']['secondary']}; --ter:{C['text']['tertiary']};
    --mark:#D65151; --ok:#3F7D4E; --stage:{N['200']};
  }}
  @media (prefers-color-scheme:dark){{
    :root:not([data-theme="light"]){{--ground:#141413;--card:#1E1E1C;
      --edge:rgba(255,255,255,.11);--ink:#F2F1EE;--sec:#A9A7A1;--ter:#78766F;
      --mark:#E4756F;--ok:#8CC79A;--stage:#2A2A27}}
  }}
  :root[data-theme="dark"]{{--ground:#141413;--card:#1E1E1C;--edge:rgba(255,255,255,.11);
    --ink:#F2F1EE;--sec:#A9A7A1;--ter:#78766F;--mark:#E4756F;--ok:#8CC79A;--stage:#2A2A27}}

  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--ground);color:var(--ink);font-family:GSF,system-ui,sans-serif;
    font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}}
  .wrap{{max-width:920px;margin:0 auto;padding:56px 24px 96px;display:flex;
    flex-direction:column;gap:24px}}
  .masthead{{border-bottom:1px solid var(--edge);padding-bottom:24px;display:flex;
    flex-direction:column;gap:10px}}
  .masthead h1{{margin:0;font-size:34px;font-weight:700;letter-spacing:-.028em;text-wrap:balance}}
  .masthead p{{margin:0;color:var(--sec);max-width:64ch}}

  .case{{background:var(--card);border:1px solid var(--edge);border-radius:18px;overflow:hidden}}
  .chead{{display:flex;align-items:baseline;gap:12px;padding:18px 22px;
    border-bottom:1px solid var(--edge)}}
  .cn{{font-size:11.5px;font-weight:700;color:var(--mark);letter-spacing:.09em}}
  .chead h3{{margin:0;font-size:17px;font-weight:700;letter-spacing:-.018em;flex:1}}
  .val{{font-size:13px;font-weight:700;color:var(--mark);
    background:color-mix(in srgb,var(--mark) 12%,transparent);border-radius:99px;padding:3px 11px}}
  .cbody{{display:grid;grid-template-columns:minmax(0,398px) minmax(0,1fr);gap:26px;padding:22px;
    align-items:start}}
  @media (max-width:820px){{.cbody{{grid-template-columns:1fr}}}}
  .cbody--wide{{grid-template-columns:1fr}}
  .demo{{min-width:0;background:var(--stage);border-radius:14px;padding:22px;
    display:flex;flex-direction:column;align-items:center;gap:16px;overflow-x:auto}}
  .why p{{margin:0 0 11px;color:var(--sec)}}
  .why p:last-child{{margin-bottom:0}}
  .why code{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ter);
    background:var(--ground);padding:2px 7px;border-radius:5px}}
  .why b{{color:var(--ink);font-weight:700}}
  .quote{{border-left:2px solid var(--mark);padding-left:14px;font-style:italic}}

  /* ---- a real large surface, built from recipes.largeSurface -------------- */
  /* max-width, not width — the specimens declare a TRUE pixel width so they
     read at product scale, and must shrink rather than overflow on a phone. */
  .ls{{position:relative;border-radius:{LS['borderRadius']}px;box-shadow:{EL['floating']['css']};
    width:100%;max-width:100%}}
  .ls__s{{position:absolute;inset:0;background:{LS['background']};{SURFACE}}}
  .ls__c{{position:relative;z-index:1;padding:{LAY['sheetPadY']}px {LAY['sheetPadX']}px;
    color:#0B0B0B}}

  .anno{{display:block;font-size:11.5px;font-weight:700;color:#0B0B0B;opacity:.62;
    padding-left:16px;position:relative;line-height:26px;white-space:nowrap}}
  .anno::before{{content:"";position:absolute;left:0;top:12px;width:8px;height:2px;
    background:var(--mark)}}

  .cnrs{{display:flex;gap:18px;flex-wrap:wrap;justify-content:center}}
  /* fixed width — otherwise each figure is as wide as its CAPTION and the
     three specimens wrap, which reads as three sizes rather than three corners. */
  .cnr{{margin:0;width:{MINSZ}px;display:flex;flex-direction:column;align-items:center;gap:10px}}
  /* {MINSZ}px, the smallest box this corner fits on — see SQ.min_size(). Any
     smaller and the two corners overlap, which would make the comparison lie. */
  .cnr__b{{display:block;width:{MINSZ}px;height:{MINSZ}px;background:{LS['background']};
    box-shadow:{EL['floating']['css']}}}
  .cnr figcaption{{font-size:10.5px;font-weight:700;color:var(--sec);text-align:center;
    line-height:1.25}}

  /* STACKED, not side by side. Two columns inside the demo well leaves each
     specimen ~150px, and a card that narrow stops demonstrating anything. */
  .cmp{{display:flex;flex-direction:column;gap:20px;width:100%}}
  .cmp__col{{display:flex;flex-direction:column;gap:10px;min-width:0}}
  .cmp__t{{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
  .cmp__t--ok{{color:var(--ok)}} .cmp__t--no{{color:var(--mark)}}
  .ls__c b,.sml b{{display:block;font-size:13px;font-weight:700;margin-bottom:2px}}
  .ls__c span,.sml span{{display:block;font-size:11.5px;color:#6B6963;line-height:1.35}}
  .sml{{position:relative;background:{N['0']};border:1px solid rgba(0,0,0,.08);
    padding:13px 15px;color:#0B0B0B;box-shadow:{EL['control']['css']};
    min-height:{ROW_H}px;display:flex;flex-direction:column;justify-content:center}}
  /* the wrong one gets the REAL treatment at row height, so the bulge on show
     is the actual failure and not a drawing of it */
  .sml--bad{{background:none;border:0;box-shadow:{EL['floating']['css']};
    border-radius:{LS['borderRadius']}px;outline:1px dashed var(--mark);outline-offset:5px}}
  .sml__s{{position:absolute;inset:0;z-index:0;background:{LS['background']};}}
  .sml--bad b,.sml--bad span{{position:relative;z-index:1}}

  /* ---- the sheet specimen, at true size ---------------------------------- */
  .sheet{{display:flex;flex-direction:column;align-items:stretch;text-align:center}}
  .wm{{display:block;margin:0 auto {RH['textGap']}px}}
  .wm--t{{{ty('label')}color:#0B0B0B;opacity:{LAY['wordmarkSheetOpacity']};
    letter-spacing:.3em;margin-bottom:{RH['textGap']}px}}
  .sh1{{{ty('display')}margin:0;color:#0B0B0B}}
  .sc{{border:0;font-family:inherit;width:100%;border-radius:99px;cursor:default;
    display:flex;align-items:center;justify-content:center}}
  .sc--pri{{{ty('action')}height:{LAY['ctaHeight']}px;background:#2E2E2C;color:#fff;
    margin-top:{RH['titleGap']}px;box-shadow:{EL['dock']['css']}}}
  .sc--qui{{{ty('actionSmall')}height:{LAY['ctaQuietHeight']}px;background:#fff;color:#0B0B0B;
    margin-top:{RH['controlGap']}px;box-shadow:{EL['control']['css']}}}
  .sc--bare{{{ty('actionSmall')}height:{LAY['ctaQuietHeight']}px;background:none;color:#0B0B0B;
    margin-top:{RH['controlGap']}px}}
  .slegal{{{ty('legal')}color:#8A8880;margin:{RH['titleGap']}px 0 0}}
  .slegal b{{color:#6B6963;font-weight:{TX['legal']['linkWeight']};display:inline;font-size:inherit}}

  .tbl{{width:100%;border-collapse:collapse;margin-top:14px;font-size:13px}}
  .tbl th{{text-align:left;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
    color:var(--ter);font-weight:700;padding:0 10px 7px 0;border-bottom:1px solid var(--edge)}}
  .tbl td{{padding:7px 10px 7px 0;border-bottom:1px solid var(--edge);color:var(--sec)}}
  .tbl td.n{{font-weight:700;color:var(--ink)}}
  .code{{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;line-height:1.7;margin:0;
    color:#0B0B0B;white-space:pre;overflow-x:auto;width:100%}}
  footer{{color:var(--ter);font-size:12.5px;border-top:1px solid var(--edge);padding-top:20px;
    max-width:64ch}}
  footer code{{font-family:ui-monospace,Menlo,monospace}}
</style>
<div class="wrap">
  <header class="masthead">
    <h1>Large surfaces</h1>
    <p>The card design &mdash; radius {LS['borderRadius']} at
      {int(LS['smoothing'] * 100)}% corner smoothing, a {LS['backgroundFallback']} fill under a
      24% gradient, a {LS['strokeWidth']}px white inside stroke, and a drop shadow. Owner's
      Figma inspector, 2026-08-19. It belongs to grounds only.</p>
  </header>
  {"".join(CASES)}
  <footer>Generated from <code>src/tokens/design.tokens.js</code> by
    <code>docs/design/build-surfaces-dashboard.py</code>. Corner geometry from
    <code>docs/_squircle.py</code>. Every specimen on this page is built from the same
    declarations the product uses, so it cannot disagree with the spec beside it &mdash; if a
    value looks wrong, the token is wrong.</footer>
</div>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote %s (%d KB)" % (OUT.relative_to(ROOT), len(HTML) // 1024))
