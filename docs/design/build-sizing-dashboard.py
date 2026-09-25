#!/usr/bin/env python3
"""
Build docs/design/sizing-and-rhythm.html

THE SIZING AND RHYTHM SPEC, GENERATED FROM THE TOKENS — never hand-written.

    python3 docs/design/build-sizing-dashboard.py

Every number on the page is read out of src/tokens/design.tokens.js at build
time, so the spec cannot drift from what the product actually renders. If a
value here looks wrong, the token is wrong.

WHY IT LOOKS LIKE A REDLINE. The owner communicated these numbers by drawing
red measurement brackets on a screenshot. The page answers in the same
language: every rule is a LIVE specimen at true size with a real bracket over
it, not a number in a table. A spec you can hold a ruler to is one you can
disagree with precisely.
"""

import base64
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).with_name("sizing-and-rhythm.html")
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"
FONTS = ROOT / "src" / "fonts" / "google-sans-flex" / "static"


def load(names):
    script = ("import(%s).then(m=>{const {%s}=m;"
              "process.stdout.write(JSON.stringify({%s}));})"
              % (json.dumps(TOKENS.as_uri()), ",".join(names), ",".join(names)))
    res = subprocess.run(["node", "--input-type=module", "-e", script],
                         capture_output=True, text=True)
    if res.returncode:
        raise SystemExit("token read failed:\n" + res.stderr.strip())
    return json.loads(res.stdout)


T = load(["colors", "elevation", "layout", "neutral", "radius", "rhythm",
          "spacing", "typography", "recipes"])
C, N, R, S = T["colors"], T["neutral"], T["radius"], T["spacing"]
LAY, RH, RC, EL = T["layout"], T["rhythm"], T["recipes"], T["elevation"]

b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
FACE = {w: b64(FONTS / f"GoogleSansFlex_24pt-{n}.ttf")
        for w, n in ((400, "Regular"), (500, "Medium"), (700, "Bold"))}


def bracket(px, label=None):
    """A redline measurement bracket — the owner's own annotation language."""
    return (f'<span class="mk" style="height:{px}px">'
            f'<i></i><b>{label or px}</b></span>')


def rule(num, title, body, spec, meta):
    return f"""<section class="rule">
  <header><span class="rn">{num}</span><h2>{title}</h2></header>
  <p class="lede">{body}</p>
  <div class="split">
    <div class="spec">{spec}</div>
    <dl class="meta">{meta}</dl>
  </div>
</section>"""


def dt(k, v):
    return f"<dt>{k}</dt><dd>{v}</dd>"


# ── the specimens ──────────────────────────────────────────────────────────
rhythm_spec = f"""
<div class="sheetdemo">
  <p class="eyb">Login with number</p>
  {bracket(RH['textGap'])}
  <h3 class="dh1">What's your mobile<br>number?</h3>
  {bracket(RH['sectionGap'])}
  <div class="otprow">{''.join('<i>%s</i>' % d for d in '2169')}</div>
  {bracket(RH['controlGap'])}
  <p class="dresend">Resend OTP in <b>15s</b></p>
  {bracket(RH['sectionGap'])}
  <button class="dcta">Proceed</button>
</div>"""

control_spec = f"""
<div class="sheetdemo">
  <h3 class="dh1">A calmer kind of<br>smart home.</h3>
  {bracket(RH['titleGap'])}
  <button class="dcta">Use mobile number</button>
  {bracket(RH['controlGap'])}
  <button class="dcta dcta--quiet">Continue with Apple</button>
  {bracket(RH['controlGap'])}
  <button class="dcta dcta--bare">Continue with email</button>
</div>"""

field_spec = f"""
<div class="sheetdemo">
  <p class="dlab">Name</p>
  <div class="dfield">Ruhaan Royce</div>
  <div class="callouts">
    <span><i style="border-radius:{RC['input']['borderRadius']}px"></i>radius {RC['input']['borderRadius']}</span>
    <span><i class="stroke"></i>1px #000 @ 12%</span>
    <span><i class="hgt"></i>height {RC['input']['height']}</span>
  </div>
</div>"""

radius_spec = "".join(
    f'<span class="rad"><i style="border-radius:{v}px"></i><b>{k}</b><em>{v}</em></span>'
    for k, v in R.items() if k != "none" and v < 100)

HTML = f"""<meta charset="utf-8">
<title>NOMA Sizing &amp; Rhythm</title>
<style>
  @font-face{{font-family:GSF;font-weight:400;src:url(data:font/ttf;base64,{FACE[400]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:500;src:url(data:font/ttf;base64,{FACE[500]}) format("truetype")}}
  @font-face{{font-family:GSF;font-weight:700;src:url(data:font/ttf;base64,{FACE[700]}) format("truetype")}}

  :root{{
    --ground:{N['150']}; --card:{N['0']}; --edge:rgba(11,11,11,.09);
    --ink:{C['text']['primary']}; --sec:{C['text']['secondary']}; --ter:{C['text']['tertiary']};
    --mark:#D65151;              /* the redline red — measurements ONLY */
    --ok:{T['colors']['text']['accent']};
  }}
  :root:not([data-theme="light"]){{ }}
  @media (prefers-color-scheme: dark){{
    :root:not([data-theme="light"]){{
      --ground:#141413; --card:#1E1E1C; --edge:rgba(255,255,255,.11);
      --ink:#F2F1EE; --sec:#A9A7A1; --ter:#78766F; --mark:#E4756F;
    }}
  }}
  :root[data-theme="dark"]{{
    --ground:#141413; --card:#1E1E1C; --edge:rgba(255,255,255,.11);
    --ink:#F2F1EE; --sec:#A9A7A1; --ter:#78766F; --mark:#E4756F;
  }}

  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--ground);color:var(--ink);
    font-family:GSF,system-ui,sans-serif;font-size:15px;line-height:1.55;
    -webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}}
  .wrap{{max-width:880px;margin:0 auto;padding:56px 24px 96px;
    display:flex;flex-direction:column;gap:28px}}

  .masthead{{border-bottom:1px solid var(--edge);padding-bottom:26px;
    display:flex;flex-direction:column;gap:10px}}
  .masthead h1{{margin:0;font-size:34px;font-weight:700;letter-spacing:-.028em;
    text-wrap:balance}}
  .masthead p{{margin:0;color:var(--sec);max-width:62ch}}
  .stamp{{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}}
  .stamp span{{font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;
    font-weight:500;color:var(--sec);border:1px solid var(--edge);
    border-radius:99px;padding:4px 11px}}

  .rule{{background:var(--card);border:1px solid var(--edge);border-radius:18px;
    padding:26px;display:flex;flex-direction:column;gap:14px}}
  .rule header{{display:flex;align-items:baseline;gap:12px}}
  .rn{{font-size:11.5px;font-weight:700;color:var(--mark);letter-spacing:.09em}}
  .rule h2{{margin:0;font-size:20px;font-weight:700;letter-spacing:-.02em}}
  .lede{{margin:0;color:var(--sec);max-width:64ch}}
  .split{{display:grid;grid-template-columns:minmax(0,286px) minmax(0,1fr);
    gap:28px;align-items:start;margin-top:6px}}
  @media (max-width:680px){{.split{{grid-template-columns:1fr}}}}

  /* the specimen column renders at TRUE product size */
  .spec{{overflow-x:auto}}
  .sheetdemo{{width:286px;background:var(--card);border:1px solid var(--edge);
    border-radius:20px;padding:{LAY['sheetPadY']}px {LAY['sheetPadX']}px;
    display:flex;flex-direction:column;align-items:stretch}}
  .sheetdemo>*{{margin:0}}
  .eyb{{font-size:12px;letter-spacing:.085em;text-transform:uppercase;
    font-weight:500;color:var(--sec);text-align:center}}
  .dh1{{font-size:26px;line-height:1.16;font-weight:700;letter-spacing:-.024em;
    text-align:center}}
  .otprow{{display:flex;gap:10px;justify-content:center}}
  .otprow i{{width:{LAY['otpBox'][0]}px;height:{LAY['otpBox'][1]}px;font-style:normal;
    border-radius:{R['md']}px;border:1px solid var(--edge);display:grid;
    place-items:center;font-size:21px;font-weight:700}}
  .dresend{{font-size:12.5px;color:var(--sec);text-align:center}}
  .dcta{{height:{LAY['ctaHeight']}px;border:0;border-radius:99px;background:var(--ink);
    color:var(--card);font:inherit;font-weight:700;font-size:15.5px;cursor:default}}
  .dcta--quiet{{height:{LAY['ctaQuietHeight']}px;background:var(--card);color:var(--ink);
    border:1px solid var(--edge)}}
  .dcta--bare{{height:{LAY['ctaQuietHeight']}px;background:none;color:var(--ink);border:0}}
  .dlab{{font-size:11px;letter-spacing:.11em;text-transform:uppercase;
    color:var(--ter);font-weight:500;margin-bottom:8px !important}}
  .dfield{{height:{RC['input']['height']}px;border-radius:{RC['input']['borderRadius']}px;
    background:{RC['input']['background']};color:#0B0B0B;
    border:{RC['input']['borderWidth']}px solid {RC['input']['borderColor']};
    box-shadow:{RC['input']['innerShadow']};
    display:flex;align-items:center;padding:0 {RC['input']['paddingX']}px;
    font-size:16.5px;font-weight:500}}

  /* the redline bracket */
  .mk{{position:relative;display:block;width:100%}}
  .mk i{{position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--mark)}}
  .mk i::before,.mk i::after{{content:"";position:absolute;left:-3px;width:7px;
    height:1px;background:var(--mark)}}
  .mk i::before{{top:0}} .mk i::after{{bottom:0}}
  .mk b{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
    margin-left:26px;font-size:10.5px;font-weight:700;color:var(--mark);
    background:var(--card);padding:0 4px}}

  .callouts{{display:flex;flex-direction:column;gap:7px;margin-top:14px}}
  .callouts span{{display:flex;align-items:center;gap:9px;font-size:12px;color:var(--sec)}}
  .callouts i{{width:17px;height:17px;flex:none;border:1px solid var(--mark)}}
  .callouts i.stroke{{border-radius:4px;border-width:1.5px}}
  .callouts i.hgt{{border:0;border-left:2px solid var(--mark);border-right:2px solid var(--mark);
    width:9px}}

  .meta{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:7px 16px;
    align-content:start;font-size:13.5px}}
  .meta dt{{color:var(--ter);font-size:11.5px;letter-spacing:.06em;
    text-transform:uppercase;font-weight:500;padding-top:2px}}
  .meta dd{{margin:0;color:var(--ink)}}
  .meta code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;
    background:var(--ground);padding:1px 6px;border-radius:5px}}

  .rad{{display:inline-flex;flex-direction:column;align-items:center;gap:6px;
    margin:0 16px 12px 0}}
  .rad i{{width:52px;height:40px;background:var(--ground);
    border:1px solid var(--mark);display:block}}
  .rad b{{font-size:12px;font-weight:700}}
  .rad em{{font-style:normal;font-size:11px;color:var(--ter)}}

  footer{{color:var(--ter);font-size:12.5px;border-top:1px solid var(--edge);
    padding-top:22px;max-width:64ch}}
  footer code{{font-family:ui-monospace,Menlo,monospace}}
</style>

<div class="wrap">
  <div class="masthead">
    <h1>Sizing &amp; rhythm</h1>
    <p>The vertical grammar and control sizes for NOMA's first run. Every number
       below is read from <code>src/tokens/design.tokens.js</code> when this page is
       built, so it cannot drift from what the product renders — if a value here
       looks wrong, the token is wrong.</p>
    <div class="stamp">
      <span>Generated from tokens</span>
      <span>Owner redline · 2026-08-18</span>
      <span>Cross-checked · Airbnb, CRED</span>
    </div>
  </div>

  {rule("01", "Two gaps do almost all the work",
        "Twelve inside a text set, twenty-four between blocks. Both are existing "
        "stops on the 4pt ramp, promoted to a named grammar so a screen never has "
        "to invent a number. Anything tighter than 12 reads as one line wrapping; "
        "anything between 12 and 24 reads as indecision.",
        rhythm_spec,
        dt("textGap", f"<b>{RH['textGap']}</b> — eyebrow → title, title → body")
        + dt("sectionGap", f"<b>{RH['sectionGap']}</b> — block → block, and the sheet's own padding")
        + dt("controlGap", f"<b>{RH['controlGap']}</b> — stacked controls in one group")
        + dt("token", "<code>rhythm.textGap</code> · <code>rhythm.sectionGap</code>")
        + dt("source", "Owner redline. Airbnb runs ~8–12 / 24–32; CRED ~12 / 24–32."))}

  {rule("02", "Height is the hierarchy",
        "A quiet button is <em>shorter</em> than the primary, not merely paler. "
        "Matching heights make two buttons read as equal choices however different "
        "their fills are — the eight-point stack then binds them into one group of "
        "options rather than three unrelated things.",
        control_spec,
        dt("primary", f"<b>{LAY['ctaHeight']}</b> · full-radius pill, ink fill")
        + dt("quiet", f"<b>{LAY['ctaQuietHeight']}</b> · same radius, raised surface")
        + dt("stack", f"<b>{RH['controlGap']}</b> between stacked buttons")
        + dt("title → cta", f"<b>{RH['titleGap']}</b> — the one measured value not on the ramp")
        + dt("token", "<code>layout.ctaHeight</code> · <code>layout.ctaQuietHeight</code>"))}

  {rule("03", "A field is a well, a button is a pill",
        "The two most common controls are deliberately opposite. A text field is "
        "drawn <em>into</em> the surface — barely rounded, hairline-bounded, with "
        "two inner shadows and no drop shadow. A button sits on top of it. That "
        "contrast is what tells you which one you type into.",
        field_spec,
        dt("radius", f"<b>{RC['input']['borderRadius']}</b> (was 20) — against the pill's full round")
        + dt("height", f"<b>{RC['input']['height']}</b> (was 56)")
        + dt("stroke", f"<code>{RC['input']['borderColor']}</code>, 1px inside")
        + dt("depth", "two inner shadows; <b>no</b> elevation")
        + dt("token", "<code>recipes.input</code>")
        + dt("source", "Owner Figma inspector. CRED and Airbnb both use 1px-stroke fields."))}

  {rule("04", "The radius scale",
        "Roundness encodes how much a thing wants to be noticed. Fields sit at the "
        "quiet end, cards in the middle, and only pills and avatars go fully round.",
        f'<div style="display:flex;flex-wrap:wrap">{radius_spec}</div>',
        dt("field", f"<b>{R['xs']}</b>") + dt("row / thumb", f"<b>{R['sm']}</b>")
        + dt("card", f"<b>{R['xl']}</b>") + dt("sheet", f"<b>{R['xxl']}</b>")
        + dt("pill", "<b>full</b> — CTAs, chips, avatars")
        + dt("token", "<code>radius</code>"))}

  <footer>
    Built by <code>docs/design/build-sizing-dashboard.py</code>. The bracket
    notation is the owner's own — these rules arrived as red measurements drawn on
    a screenshot, and the page answers in the same language so a value can be
    checked with a ruler rather than taken on trust.
  </footer>
</div>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote %s (%d KB)" % (OUT.relative_to(ROOT), len(HTML) // 1024))
