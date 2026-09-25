#!/usr/bin/env python3
"""
Build docs/design/scenarios.html — every adjacency, as a live specimen.

    python3 docs/design/build-scenarios-dashboard.py

THE COMPANION TO sizing-and-rhythm.html. That page states the grammar; this
one answers the question a designer actually has at 2am — "what goes between
THESE two things?" — for every pair that occurs in the product.

Generated from src/tokens/design.tokens.js, so no number here is transcribed.
"""

import base64
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))  # docs/
import _squircle as SQ  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).with_name("scenarios.html")
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"
FONTS = ROOT / "src" / "fonts" / "google-sans-flex" / "static"


def load(names):
    script = ("import(%s).then(m=>{const {%s}=m;"
              "process.stdout.write(JSON.stringify({%s}));})"
              % (json.dumps(TOKENS.as_uri()), ",".join(names), ",".join(names)))
    r = subprocess.run(["node", "--input-type=module", "-e", script],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr.strip())
    return json.loads(r.stdout)


T = load(["colors", "elevation", "layout", "neutral", "radius", "rhythm",
          "spacing", "typography", "recipes"])
C, N, R = T["colors"], T["neutral"], T["radius"]
LAY, RH, RC = T["layout"], T["rhythm"], T["recipes"]

b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
FACE = {w: b64(FONTS / f"GoogleSansFlex_24pt-{n}.ttf")
        for w, n in ((400, "Regular"), (500, "Medium"), (700, "Bold"))}

E = RH["textGap"]; SEC = RH["sectionGap"]; CTRL = RH["controlGap"]; TTL = RH["titleGap"]


def gapmark(px):
    return f'<span class="g" style="height:{px}px"><i></i><b>{px}</b></span>'


def case(n, when, gap, why, demo, token):
    return f"""<article class="case">
  <div class="chead"><span class="cn">{n}</span>
    <h3>{when}</h3><span class="val">{gap}</span></div>
  <div class="cbody">
    <div class="demo">{demo}</div>
    <div class="why"><p>{why}</p><code>{token}</code></div>
  </div>
</article>"""


CASES = "".join([
    case("01", "All-caps label → heading", E,
         "An eyebrow is a label <em>for</em> the heading beneath it, so the two have to "
         "read as one unit. This is the pair that is easiest to get wrong in code — a "
         "margin reset that out-specifies the component rule closes it to zero and the "
         "label looks stuck to the title.",
         f'<p class="eyb">Before we finish</p>{gapmark(E)}<h4 class="h1">Shall I tell you when something changes?</h4>',
         "rhythm.textGap"),

    case("02", "Heading → body", E,
         "Same set, same gap. The body is the heading finishing its sentence, not a new "
         "thought — opening this to 24 makes the screen read as two unrelated statements.",
         f'<h4 class="h1">Where does it live?</h4>{gapmark(E)}<p class="bd">So I can compare your air against the right patch of outdoors.</p>',
         "rhythm.textGap"),

    case("03", "Body → the next block", SEC,
         "The text set has ended. Whatever comes next — a field, a list, a picker — is a "
         "new block and takes the section gap. This is the boundary the eye uses to "
         "decide how many things are on the screen.",
         f'<p class="bd">It needs one to fetch the outdoor air.</p>{gapmark(SEC)}<p class="lab">Password</p><div class="fld">••••••••••</div>',
         "rhythm.sectionGap"),

    case("04", "Field label → field", 8,
         "Tighter than a text pair on purpose: a label and its input are one control, and "
         "8 is close enough that no one has to work out which label belongs to which box "
         "on a screen with two of them.",
         f'<p class="lab">Home name</p>{gapmark(8)}<div class="fld">My Home</div>',
         "recipes.input.labelGap"),

    case("05", "Field → field", 12,
         "Two fields in one group. Far enough apart to be separate answers, close enough "
         "to still be one form.",
         f'<p class="lab">Name</p><div class="fld">Ruhaan Royce</div>{gapmark(12)}<p class="lab">Email</p><div class="fld">ruhaanroyce@gmail.com</div>',
         "rhythm.controlGap × 1.5"),

    case("06", "Heading → the control under it", TTL,
         "The one measured value that is not a stop on the 4pt ramp, and it is kept "
         "measured rather than rounded: at 16 the title crowds the button, at 20 the eye "
         "reads a section break that is not there.",
         f'<h4 class="h1">A calmer kind of smart home.</h4>{gapmark(TTL)}<button class="cta">Use mobile number</button>',
         "rhythm.titleGap"),

    case("07", "Stacked buttons", CTRL,
         "Eight binds them into one group of choices. At 12 they read as unrelated "
         "controls that happen to sit near each other — which is the wrong story when "
         "they are three ways of doing the same thing.",
         f'<button class="cta">Use mobile number</button>{gapmark(CTRL)}<button class="cta cta--quiet">Continue with Apple</button>{gapmark(CTRL)}<button class="cta cta--bare">Continue with email</button>',
         "rhythm.controlGap"),

    case("08", "Content → the primary CTA", SEC,
         "The CTA is always its own block, whatever precedes it. It is the only thing on "
         "the screen that leaves it.",
         f'<p class="dresend">Resend OTP in <b>15s</b></p>{gapmark(SEC)}<button class="cta">Proceed</button>',
         "rhythm.sectionGap"),

    case("09", "Three button weights", "54 / 46 / —",
         "Height carries the hierarchy before colour does. The primary is ink and tallest; "
         "the quiet one is a raised surface and shorter; the tertiary has no container at "
         "all. A quiet button at the primary's height reads as an equal choice however "
         "pale you make it.",
         '<button class="cta">Share key</button>'
         f'{gapmark(CTRL)}<button class="cta cta--quiet">Invite someone else</button>'
         f'{gapmark(CTRL)}<button class="cta cta--bare">Not now</button>',
         "recipes.buttonPrimary / buttonQuiet"),

    case("10", "Grey has three jobs", "—",
         "Primary ink is what you read. Secondary is supporting copy and eyebrows — "
         "present, not competing. Tertiary is metadata you only look at when you go "
         "looking: placeholders, timestamps, field labels. A grey doing the wrong job is "
         "the fastest way to make a clean screen feel muddy.",
         '<p class="sw ink">Sharma_Home</p>'
         '<p class="sw sec">This phone already knows the password.</p>'
         '<p class="sw ter">2.4 GHz and dual-band networks are fine.</p>',
         "colors.text.primary / secondary / tertiary"),

    case("11", "The sheet's own padding", f"{LAY['sheetPadY']} / {LAY['sheetPadX']}",
         "Twenty-four top and bottom — the section gap again, because the sheet edge is "
         "the outermost block boundary there is. Twenty at the sides, which is the screen "
         "margin the whole product uses.",
         f'<div class="sheetbox"><span class="pad">{LAY["sheetPadY"]}</span>'
         f'<p class="eyb">Login with number</p><h4 class="h1">What’s your mobile number?</h4>'
         f'<button class="cta">Proceed</button><span class="pad">{LAY["sheetPadY"]}</span></div>',
         "layout.sheetPadX / sheetPadY"),

    case("12", "Corner smoothing", "100%",
         "Corners are smoothed the way iOS smooths them — a superellipse, not a circular "
         "arc — and that is a large part of why the shapes read as premium rather than "
         "merely rounded. Owner, 2026-08-19: <b>100%, the full iOS value</b>. "
         "The two squares on the right are the same size and the same radius; only the "
         "corner differs. Look at where each one stops being straight — the smoothed one "
         "starts turning much earlier and never has a hard tangent point. "
         "<b>These prototypes now render it.</b> <code>border-radius</code> can only draw a "
         "circular arc, so <code>docs/_squircle.py</code> emits Figma\u2019s own corner "
         "geometry as a 9-slice mask that restretches at any element size. Native takes "
         "<code>.continuous</code>.",
         f'<div class="smoo"><span class="sq"></span><b>border-radius \u00b7 circular</b></div>'
         f'<div class="smoo"><span class="sq sq--ios"></span><b>squircle \u00b7 100%</b></div>',
         "radius.smoothing"),
])

HTML = f"""<meta charset="utf-8">
<title>NOMA Spacing Scenarios</title>
<style>
  @font-face{{font-family:GSF;font-weight:400;src:url(data:font/ttf;base64,{FACE[400]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:500;src:url(data:font/ttf;base64,{FACE[500]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:700;src:url(data:font/ttf;base64,{FACE[700]}) format("truetype")}}
  :root{{
    --ground:{N['150']}; --card:{N['0']}; --edge:rgba(11,11,11,.09);
    --ink:{C['text']['primary']}; --sec:{C['text']['secondary']}; --ter:{C['text']['tertiary']};
    --mark:#D65151;
  }}
  @media (prefers-color-scheme:dark){{
    :root:not([data-theme="light"]){{--ground:#141413;--card:#1E1E1C;
      --edge:rgba(255,255,255,.11);--ink:#F2F1EE;--sec:#A9A7A1;--ter:#78766F;--mark:#E4756F}}
  }}
  :root[data-theme="dark"]{{--ground:#141413;--card:#1E1E1C;--edge:rgba(255,255,255,.11);
    --ink:#F2F1EE;--sec:#A9A7A1;--ter:#78766F;--mark:#E4756F}}

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
    background:color-mix(in srgb,var(--mark) 12%,transparent);
    border-radius:99px;padding:3px 11px}}
  .cbody{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:26px;padding:22px}}
  @media (max-width:700px){{.cbody{{grid-template-columns:1fr}}}}
  .demo{{display:flex;flex-direction:column;align-items:stretch;min-width:0}}
  .demo>*{{margin:0}}
  .why p{{margin:0 0 10px;color:var(--sec)}}
  .why code{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ter);
    background:var(--ground);padding:2px 7px;border-radius:5px}}

  .g{{position:relative;display:block;width:100%}}
  .g i{{position:absolute;left:14px;top:0;bottom:0;width:1px;background:var(--mark)}}
  .g i::before,.g i::after{{content:"";position:absolute;left:-3px;width:7px;height:1px;background:var(--mark)}}
  .g i::before{{top:0}} .g i::after{{bottom:0}}
  .g b{{position:absolute;left:26px;top:50%;transform:translateY(-50%);font-size:10.5px;
    font-weight:700;color:var(--mark)}}

  .eyb{{font-size:12px;letter-spacing:.085em;text-transform:uppercase;font-weight:500;color:var(--sec)}}
  .h1{{font-size:24px;line-height:1.16;font-weight:700;letter-spacing:-.022em}}
  .bd{{font-size:15px;color:var(--sec)}}
  .lab{{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--ter);font-weight:500}}
  .fld{{height:{RC['input']['height']}px;border-radius:{RC['input']['borderRadius']}px;
    background:{RC['input']['background']};color:#0B0B0B;
    border:1px solid {RC['input']['borderColor']};box-shadow:{RC['input']['innerShadow']};
    display:flex;align-items:center;padding:0 {RC['input']['paddingX']}px;font-size:16px;font-weight:500}}
  .cta{{height:{LAY['ctaHeight']}px;border:0;border-radius:99px;background:var(--ink);
    color:var(--card);font:inherit;font-weight:700;font-size:15px;cursor:default}}
  .cta--quiet{{height:{LAY['ctaQuietHeight']}px;background:var(--card);color:var(--ink);
    border:1px solid var(--edge)}}
  .cta--bare{{height:{LAY['ctaQuietHeight']}px;background:none;color:var(--sec);border:0}}
  .dresend{{font-size:12.5px;color:var(--sec);text-align:center}}
  .sw{{font-size:15px;padding:3px 0}}
  .sw.ink{{font-weight:700;font-size:19px}} .sw.sec{{color:var(--sec)}}
  .sw.ter{{color:var(--ter);font-size:12.5px}}
  .sheetbox{{border:1px dashed var(--mark);border-radius:16px;padding:0 {LAY['sheetPadX']}px;
    display:flex;flex-direction:column;gap:12px}}
  .pad{{display:block;height:{LAY['sheetPadY']}px;font-size:10px;color:var(--mark);
    font-weight:700;line-height:{LAY['sheetPadY']}px}}
  .smoo{{display:flex;align-items:center;gap:12px;margin-bottom:12px}}
  .smoo b{{font-size:12px;font-weight:500;color:var(--sec)}}
  .sq{{width:58px;height:58px;background:var(--ink);border-radius:18px;display:block}}
  .sq--ios{{border-radius:0;{SQ.surface_css(18, R['smoothing'])}}}
  footer{{color:var(--ter);font-size:12.5px;border-top:1px solid var(--edge);padding-top:20px;max-width:64ch}}
  footer code{{font-family:ui-monospace,Menlo,monospace}}
</style>
<div class="wrap">
  <div class="masthead">
    <h1>Spacing scenarios</h1>
    <p>Every adjacency that occurs in the product, with the gap it takes and why.
       The companion to <b>Sizing &amp; rhythm</b>: that page states the grammar,
       this one answers “what goes between <em>these two</em> things?”. Generated
       from the token file, so nothing here is transcribed.</p>
  </div>
  {CASES}
  <footer>Built by <code>docs/design/build-scenarios-dashboard.py</code>.
    Specimens render at true product size.</footer>
</div>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote %s (%d KB)" % (OUT.relative_to(ROOT), len(HTML) // 1024))
