#!/usr/bin/env python3
"""
Build docs/features/first-run/first-run-flow.html

The COMPLETE first-run flow — all 45 screens, 32 on the happy path and 13 edge
states — in the 2026-08-11 visual language. Controller rail on the left, phone
on the right.

    python3 docs/features/first-run/build-flow.py

GENERATED FROM build-prototype.py — NO SCREEN IS REDEFINED HERE.
This is the fourth rendering of the one screen set, and it follows the same rule
build-export.py and build-wireframes.py already follow: a flow change is made
once, in build-prototype.py, and every rendering rebuilds from it. What this file
adds is a SKIN, not content. If a screen's copy looks wrong, fix it upstream.

HOW THE RE-SKIN WORKS. build-prototype.py declares its palette in a `:root`
block of CSS custom properties, so most of the language swaps by overriding
those eleven variables with values read from src/tokens/design.tokens.js. The
rest is a targeted override layer for the places where the NEW system disagrees
with the old one structurally rather than chromatically:

  .row / .rows        radius 16 → 12, gap 8 → 20, translucent → solid white
                      (recipes.cardSelect — the inspector values)
  .pcard.on           was a 2px INK BORDER around the selected card. The new
  .chip.on            language says selection is LIFT, never an outline and
  .row.on             never a fill, so all three become raised-white instead.
                      This is the single biggest visual change in the file.
  .tog.on             ink fill → gradients.accentRamp (LAW 2: green is never
                      flat, and a toggle's on-state is exactly "system is
                      doing something")
  .cta / .cta2        → recipes.buttonPrimary / recipes.buttonQuiet, both 56pt
  --grad              the phone's ground was a radial falling to #A4A4A4 grey.
                      Now gradients.canvas — white to warm sand dust.

KNOWN GAP, DELIBERATELY NOT FAKED: the `.viz` illustrations are the old
outline-SVG drawings. The new language's hero is a gradient plate inside an 8pt
white frame (recipes.illustration), and you cannot turn line art into that with
a stylesheet. They are left as-is and read as the one un-migrated element in the
file. onboarding-prototype.html shows what the framed treatment looks like on
the screens that have it. Re-arting them is a real task, not a CSS one.

CONTROLLER: every screen, grouped by section, edge states marked. Click to jump,
or ← / → to walk the happy path. Any screen is deep-linkable by hash.
"""

import importlib.util
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _phone_fit import JS as FIT_JS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/features/first-run/first-run-flow.html"
SRC = pathlib.Path(__file__).with_name("build-prototype.py")
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"

# ---- 1. the one screen set -------------------------------------------------
spec = importlib.util.spec_from_file_location("first_run_screens", SRC)
P = importlib.util.module_from_spec(spec)
sys.modules["first_run_screens"] = P
spec.loader.exec_module(P)  # __name__ != "__main__", so it writes nothing

SC, SEQ, RUNTIME_JS = P.SC, P.SEQ, P.RUNTIME_JS
BASE_CSS = P.css_out()   # every embedded asset resolved — see build-prototype.py


# ---- 2. the canonical tokens ----------------------------------------------
def load_tokens():
    script = (
        "import(%s).then(m=>{"
        "const {colors,effects,elevation,gradients,green,layout,neutral,radius,spacing,recipes}=m;"
        "process.stdout.write(JSON.stringify("
        "{colors,effects,elevation,gradients,green,layout,neutral,radius,spacing,recipes}"
        "));})" % json.dumps(TOKENS.as_uri())
    )
    res = subprocess.run(["node", "--input-type=module", "-e", script],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit("Could not read %s through node.\n%s" % (TOKENS, res.stderr.strip()))
    return json.loads(res.stdout)


T = load_tokens()
green = T["green"]
C, G, N, R, S = T["colors"], T["gradients"], T["neutral"], T["radius"], T["spacing"]
EL, LAY, RC = T["elevation"], T["layout"], T["recipes"]
FX = T["effects"]

# ---- 3. the skin -----------------------------------------------------------
SKIN = f"""
/* ══════════════════════════════════════════════════════════════════
   SKIN — 2026-08-11 visual language, generated from
   src/tokens/design.tokens.js. Everything above this comment is
   build-prototype.py's own stylesheet, untouched.
   ══════════════════════════════════════════════════════════════════ */

:root{{
  --ink:{C['text']['primary']};
  --sec:{C['text']['secondary']};
  --ter:{C['text']['tertiary']};
  --hair:{C['border']['hairline']};
  --card:{C['surface']['raised']};          /* was translucent; cards are solid now */
  --cardq:{C['surface']['sunken']};
  --sh:{EL['card']['css']};
  --shs:{EL['control']['css']};
  --page:{N['150']};
  --panel:{N['0']};
  --grad:{G['canvas']['css']};              /* was radial → #A4A4A4 grey */
  /* ⚠ CORRECTED 2026-08-18: this block used to say "the palette has no red",
     which stopped being true on 2026-08-13 when the owner supplied one. The
     13 edge screens now carry status.negative properly. WARNING is still
     missing (O-6 is half-closed), so --warn remains ink — "filter at 10%" is
     a nudge, not a fault, and rendering it red would overstate it. */
  --err:{C['status']['negative']['text']}; --errbg:{C['status']['negative']['tint']};
  --neg:{C['status']['negative']['border']};
  --warn:{C['text']['secondary']}; --warnbg:{N['150']};
}}

body{{font-family:'Google Sans Flex',GSF,system-ui,sans-serif;font-optical-sizing:auto}}

/* ---- ground & frame ---- */
.phone{{background:{G['canvas']['css']};box-shadow:0 40px 90px rgba(0,0,0,.16)}}
.phone::before{{display:none}}                /* the old white veil over the ground */
.scr{{padding:0 {LAY['screenPaddingX']}px 30px}}

/* ---- type ---- */
.t1{{font-size:30px;line-height:36px;letter-spacing:-.7px;
  font-variation-settings:'opsz' 30,'wght' 700}}
.bd{{font-size:16.5px;line-height:23px;color:var(--sec)}}
.foot{{font-size:12.5px;line-height:18px;color:{C['text']['tertiary']}}}
.lab{{font-size:12px;letter-spacing:.96px;color:var(--sec);
  font-variation-settings:'wght' 600}}

/* ---- nav / icon buttons ---- */
.nb{{width:{LAY['controlSize']}px;height:{LAY['controlSize']}px;
  background:{C['surface']['control']};
  box-shadow:{EL['control']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']}}}
/* default is the bright raised state; hover and press darken — see the base
   rule in build-prototype.py for why this was inverted. */
.nb{{background:{N['0']}}}
.nb:hover{{background:{N['100']}}}
.nb:active{{background:{N['150']}}}

/* ---- recipes.cardSelect — inspector: radius 12, padding 16, gap 20 ---- */
.rows{{gap:{RC['cardSelect']['gap']}px}}
.row{{border-radius:{RC['cardSelect']['borderRadius']}px;
  padding:{RC['cardSelect']['padding']}px;background:transparent;
  box-shadow:none;border:{LAY['hairlineWidth']}px solid {C['border']['subtle']}}}
button.row:hover{{background:rgba(255,255,255,.5)}}
.row.on,.pcard.on{{background:{RC['cardSelect']['background']};
  border-color:{RC['cardSelect']['borderColor']};
  box-shadow:{EL['card']['css']}}}
.ri{{border-radius:{R['sm']}px;background:{C['surface']['sunken']}}}
.rs{{color:{C['text']['tertiary']}}}

/* LAW 3 — selection is LIFT. The old system drew a 2px ink outline around the
   chosen card and left every other card solid white, so all three read as
   chosen. Now the unselected ones go flat and muted and only the picked one
   is raised. An outline and a fill both read as "coloured", which is the
   thing this language does not do. */
.pcard{{border-radius:{RC['cardSelect']['borderRadius']}px;
  padding:{RC['cardSelect']['padding']}px;background:transparent;box-shadow:none;
  border:{LAY['hairlineWidth']}px solid {C['border']['subtle']}}}
.pcard:hover{{background:rgba(255,255,255,.5)}}
.pcard.on{{background:{RC['cardSelect']['background']};
  box-shadow:{EL['card']['css']},
  inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']}}}
.pcard:not(.on) .pcard__t b{{color:{C['text']['secondary']}}}
.pcard:not(.on) .ic-chev{{opacity:0}}   /* only the chosen row leads anywhere */

/* Device thumbnail as a gradient plate, per the owner's reference.
   ⚠ nth-of-type is doing real work here: the three SKU cards are identical
   markup, so the tone can only come from position. It holds because the
   pcards are the first three <button>s inside .scr — if that ever stops being
   true these tints land on the wrong SKU. The real fix is per-SKU renders. */
.pcard__v{{width:{RC['cardSelect']['thumbSize']}px;height:{RC['cardSelect']['thumbSize']}px;
  border-radius:{RC['cardSelect']['thumbRadius']}px;display:grid;place-items:center;
  overflow:hidden}}
/* ⚠ SUPERSEDED OVERRIDE REMOVED 2026-08-17. This layer used to re-tint the
   three SKU tiles into the two-green depth ramp (the 2026-08-12 palette rule),
   silently overriding the hue-coded tiles the owner's node-6 frame specifies.
   The frame is the newer owner instruction, the thumbs are real renders now,
   and the palette conflict is flagged at the screen's note in
   build-prototype.py — one flag, not a hidden reversal. Base tints pass
   through untouched. */
.pcard:not(.on) .pcard__v{{filter:saturate(.38) opacity(.62)}}
/* Chiclets — radius 8, NOT pills [INSPECTOR 2026-08-12]. */
.chip{{border-radius:{R['xs']}px;background:{RC['chipUnselected']['background']};
  color:{C['text']['tertiary']};box-shadow:{FX['chiclet']['css']}}}
.chip.on{{background:{RC['chipSelected']['background']};color:{C['text']['primary']};
  font-variation-settings:'wght' 600;box-shadow:{FX['chicletSelected']['css']}}}
.chip.on:hover{{background:{N['0']}}}

/* radio / checkbox — ink, not accent: these are choices, not state */
.rad.on{{border-color:var(--ink);box-shadow:inset 0 0 0 5px var(--ink)}}

/* LAW 2 — a toggle's on-state is "the system is doing something", and green
   is never a flat fill. */
.tog.on{{background:{G['accentRamp']['css']}}}

/* ---- fields — recipes.input, rebuilt 2026-08-18 from the owner's Figma:
   flat white, r8, 1px #000@12% stroke, h52, two inner shadows. A field is a
   sunken well now, not a floating card; the CTA keeps the pill and the
   contrast between the two is the point. ---- */
.fld{{border-radius:{RC['input']['borderRadius']}px;background:{RC['input']['background']};
  border:{RC['input']['borderWidth']}px solid {RC['input']['borderColor']};
  box-shadow:{RC['input']['innerShadow']};
  min-height:{RC['input']['height']}px;padding-top:0;padding-bottom:0}}
.fld:focus-within{{box-shadow:{RC['input']['innerShadow']},
  inset 0 0 0 1px {C['border']['strong']}}}
.otpc{{border-radius:{R['md']}px;background:{C['surface']['raised']};
  box-shadow:{EL['control']['css']};height:58px}}
.kr span{{border-radius:{R['sm']}px}}
.kr span.g{{background:var(--ink)}}

/* ---- buttons: recipes.buttonPrimary / buttonQuiet ---- */
.cta,.cta2{{border-radius:{R['full']}px;padding:0;height:{LAY['ctaHeight']}px;
  display:grid;place-items:center;font-size:16.5px;
  font-variation-settings:'wght' 600}}
.cta{{background:{G['ink']['css']};color:{C['text']['inverse']};
  box-shadow:{EL['dock']['css']}}}
.cta:hover{{background:{N['700']}}}
.cta.off{{background:{C['surface']['sunken']};color:{C['text']['tertiary']};
  box-shadow:none;cursor:default}}
.cta2{{background:{RC['buttonQuiet']['background']};color:{RC['buttonQuiet']['color']};
  box-shadow:{EL['control']['css']}}}
.cta2:hover{{background:{N['0']}}}
.lnk{{color:{C['text']['accent']};font-variation-settings:'wght' 600}}

/* ---- progress / dots ---- */
.dot{{background:{C['border']['hairline']}}}
.dot.on{{background:var(--ink);width:18px;border-radius:99px}}

/* ---- status dot: a bloom, not a disc (LAW 2) ---- */
.bli,.pur__ring{{}}
"""

# ---- 4. the harness shell --------------------------------------------------
SHELL = f"""
html,body{{overflow:hidden}}
body{{background:{N['150']};display:flex;height:100vh}}

/* The rail is a fixed column: header, a list that scrolls, and a note pinned
   at the bottom. The note used to be position:sticky inside the scroller,
   which let the list run underneath it. */
.ctrl{{width:264px;flex:none;background:{N['0']};border-right:1px solid {C['border']['subtle']};
  display:flex;flex-direction:column;min-height:0}}
.ctrl__top{{padding:22px 18px 0}}
.ctrl__list{{flex:1;overflow-y:auto;padding:0 18px 18px;scrollbar-width:thin;min-height:0}}
.ctrl__h{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:{C['text']['tertiary']};font-variation-settings:'wght' 600;margin-bottom:4px}}
.ctrl__s{{font-size:12px;color:{C['text']['tertiary']};line-height:1.5;margin-bottom:18px}}
.grp{{margin-bottom:16px}}
.grp__t{{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:{C['text']['tertiary']};font-variation-settings:'wght' 700;
  margin:0 0 7px 6px;display:flex;justify-content:space-between;align-items:baseline}}
.grp__n{{font-family:ui-monospace,Menlo,monospace;letter-spacing:0;opacity:.7}}
.ji{{display:flex;align-items:baseline;gap:8px;width:100%;border:0;background:none;
  border-radius:{R['sm']}px;padding:7px 9px;margin-bottom:2px;cursor:pointer;
  font:inherit;font-size:13px;color:{C['text']['secondary']};text-align:left}}
.ji:hover{{background:{N['100']}}}
.ji.on{{background:{N['0']};color:{C['text']['primary']};
  font-variation-settings:'wght' 600;
  box-shadow:{EL['control']['css']},inset 0 0 0 1px {C['border']['bevel']}}}
.ji__id{{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;
  color:{C['text']['tertiary']};flex:none;width:32px}}
.ji__t{{flex:1;line-height:1.3}}
.ji--edge .ji__id{{color:{C['text']['primary']};font-weight:700}}

.stage{{flex:1;display:flex;align-items:center;justify-content:center;padding:24px;
  position:relative;min-width:0}}
.phone{{transform-origin:center center}}

/* The per-screen design note lives in the RAIL, not over the stage. It is
   review apparatus, and floating it across the phone made it unreadable
   against the screen behind it. */
.ctrl__note{{flex:none;max-height:34vh;overflow-y:auto;padding:14px 18px 18px;
  border-top:1px solid {C['border']['subtle']};background:{N['0']};
  font-size:11.5px;line-height:1.62;color:{C['text']['tertiary']}}}
.ctrl__note code{{font-family:ui-monospace,Menlo,monospace;font-size:10.5px}}
.hud__k{{position:absolute;right:24px;bottom:18px;font-family:ui-monospace,Menlo,monospace;
  font-size:11px;color:{C['text']['tertiary']};white-space:nowrap;pointer-events:none}}
"""

# ---- 5. controller groups --------------------------------------------------
# Grouped by the section build-prototype.py already assigns each screen, in
# happy-path order, with that section's edge states appended to it.
GROUPS = []
seen = set()
for sid in SEQ:
    sec = SC[sid].get("sec") or "Flow"
    if not GROUPS or GROUPS[-1][0] != sec:
        GROUPS.append((sec, []))
    GROUPS[-1][1].append(sid)
    seen.add(sid)
EDGE = [k for k in SC if k not in seen]
if EDGE:
    GROUPS.append(("Edge states", EDGE))


def ctrl_html():
    out = []
    for sec, ids in GROUPS:
        items = "".join(
            '<button class="ji%s" data-to="%s"><span class="ji__id">%s</span>'
            '<span class="ji__t">%s</span></button>'
            % (" ji--edge" if i in EDGE else "", i, i,
               (SC[i].get("title") or i).replace("&", "&amp;"))
            for i in ids
        )
        out.append('<div class="grp"><div class="grp__t"><span>%s</span>'
                   '<span class="grp__n">%d</span></div>%s</div>'
                   % (sec.replace("&", "&amp;"), len(ids), items))
    return "".join(out)


DATA = json.dumps({
    "screens": {k: v["html"] for k, v in SC.items()},
    "seq": SEQ,
    "notes": {k: (v.get("note") or "") for k, v in SC.items()},
    "titles": {k: (v.get("title") or k) for k, v in SC.items()},
    "nodes": {k: v.get("node") for k, v in SC.items()},
}, ensure_ascii=False)

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOMA — first run, full flow</title>
<style>{BASE_CSS}{SKIN}{SHELL}</style>
</head><body>
<div class="ctrl">
  <div class="ctrl__top">
    <div class="ctrl__h">NOMA · First run</div>
    <div class="ctrl__s">{len(SC)} screens · {len(SEQ)} on the happy path ·
      {len(EDGE)} edge states. ← / → walks the path.</div>
  </div>
  <div class="ctrl__list">{ctrl_html()}</div>
  <div class="ctrl__note" id="note"></div>
</div>
<div class="stage">
  <div class="phone" id="phone"><div class="island"></div><div class="hbar"></div></div>
  <div class="hud__k" id="kbd"></div>
</div>
<script>
const S = {DATA};
let idx = 0, off = null, hist = [];
{RUNTIME_JS}
const cur = () => off || S.seq[idx];

function paint(){{
  const id = cur();
  document.querySelectorAll('.ji').forEach(b =>
    b.classList.toggle('on', b.dataset.to === id));
  const active = document.querySelector('.ji.on');
  if (active) active.scrollIntoView({{block:'nearest'}});
  document.getElementById('note').innerHTML = S.notes[id] || '';
  const n = S.nodes[id];
  document.getElementById('kbd').textContent =
    id + (n ? '  ·  node ' + n : '') + '  ·  ' + (S.seq.indexOf(id) > -1
      ? (S.seq.indexOf(id) + 1) + '/' + S.seq.length : 'edge state');
  if (location.hash.replace('#','') !== id) history.replaceState(null,'','#'+id);
}}

function render(dir){{
  clearTimers();
  const ph = document.getElementById('phone');
  /* SEAMLESS SWAP (owner, 2026-08-18: "a slight white screen flashes"). The
     old screen used to be removed BEFORE the new one was appended, so for at
     least one frame the phone had no screen in it at all and the bare ground
     showed through — read as a white flash. Now the new screen goes on top
     first and the outgoing one fades out underneath, so there is never a
     frame without content. Stale `.out` screens are swept first so a fast
     tap cannot leave a stack of dead screens behind. */
  ph.querySelectorAll('.scr.out').forEach(n => n.remove());
  const outgoing = [...ph.querySelectorAll('.scr')];
  const el = document.createElement('div');
  el.innerHTML = S.screens[cur()];
  el.className = 'scr ' + carryClass(S.screens[cur()], dir);
  ph.appendChild(el);
  outgoing.forEach(o => o.remove());
{P.WIRE_JS}
  fit(); paint();
}}
function jumpTo(id){{ const i = S.seq.indexOf(id);
  if (i > -1) {{ off = null; hist = []; idx = i; render(); return true; }} return false; }}
function go(t){{
  if (t === 'next')        return advance();
  if (t === 'back')        return backward();
  if (t === 'restart')     return reset();
  if (t === 'skip-invite') return jumpTo('C1') || advance();
  if (t === 'skip-tour')   return jumpTo('HOME') || advance();
  const at = S.seq.indexOf(t);
  if (at > -1) {{ if (off) hist = []; off = null; idx = at; }}
  else {{ hist.push(cur()); off = t; }}
  render();
}}
function advance(){{ if (off) {{ off = null; hist = []; }}
  else if (idx < S.seq.length - 1) idx++; render(); }}
function backward(){{
  if (off) {{ const p = hist.pop(); off = (p && !S.seq.includes(p)) ? p : null;
              if (p && S.seq.includes(p)) idx = S.seq.indexOf(p); }}
  else if (idx > 0) idx--;
  render('back');
}}
function reset(){{ off = null; hist = []; idx = 0; render(); }}
{FIT_JS}
/* Kept as `fit` so the render loop's existing call sites are untouched; the
   measurement itself lives in docs/features/_phone_fit.py now. */
function fit(){{ fitPhone({{stage: '.stage', padY: 96, padX: 48}}); }}
watchPhoneFit({{stage: '.stage', padY: 96, padX: 48}});
addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') advance();
  if (e.key === 'ArrowLeft')  backward();
}});
document.querySelectorAll('.ji').forEach(b =>
  b.addEventListener('click', () => go(b.dataset.to)));
function fromHash(){{
  const h = decodeURIComponent(location.hash.replace('#','')).trim();
  if (h && S.screens[h]) {{ go(h); return true; }}
  return false;
}}
addEventListener('hashchange', fromHash);
if (!fromHash()) render();
fit();
</script>
</body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote %s  screens=%d  path=%d  edge=%d  %.2f MB"
      % (OUT.relative_to(ROOT), len(SC), len(SEQ), len(EDGE), len(HTML) / 1024 / 1024))
