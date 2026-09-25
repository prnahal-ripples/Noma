#!/usr/bin/env python3
"""
Build docs/features/first-run/first-run-mobile.html

THE FLOW ON AN ACTUAL PHONE. No phone frame, no controller, no scaling — the app
fills the device screen, so the thing you are holding IS the prototype.

    python3 docs/features/first-run/build-mobile.py

GENERATED FROM build-prototype.py — DO NOT REDEFINE SCREENS HERE.
Fifth rendering of one screen set (harness, flat board, export, wireframes, this).
A flow change is made once, in build-prototype.py, and all five rebuild from it.

WHY THIS EXISTS, AND WHY IT IS NOT build-export.html
  The export still draws a 390x844 phone with a bezel and scales it to fit the
  window. That is right for sending to someone at a desk and wrong for holding:
  on a handset you get a small picture of a phone inside a phone, and the key
  card's gyro shimmer — the one thing that CANNOT be judged on a laptop — reads
  at half size behind a fake bezel.

  So this build keeps every screen byte-identical and changes only the shell:
    · `.phone` becomes the viewport (fixed, inset 0, no radius, no bezel shadow)
    · the drawn island and home bar are hidden — the real device has its own
    · the fake status bar's GLYPHS are hidden but its 56px is KEPT, because the
      layout above the fold is measured against it; the real status bar then sits
      in that reserved band instead of on top of content
    · no `fitPhone()` at all: `fit` is a no-op, so nothing is transformed
  ⚠ That last point is load-bearing for more than layout. placeKey()/placeHero()
  divide by the phone's own scale (`pr.width / phone.offsetWidth`) to convert
  screen space into phone space. With no transform that ratio is exactly 1, so
  the travelling key card lands where it should with no special-casing.

⚠ THE GYRO NEEDS AN EXPLICIT GATE, AND THAT IS AN iOS RULE, NOT A CHOICE.
  iOS 13+ refuses `DeviceOrientationEvent` unless `requestPermission()` is called
  from inside a real user gesture. The harness asks on the first tap on the phone,
  but that binding is only attached once a tilt card exists (wireCardTilt), which
  first happens on node 5b — several taps in. On a handset that reads as "the
  shimmer is broken". So this build opens on a tap gate whose only job is to be a
  genuine gesture, calls the harness's own `askGyro()` from it, and only then
  starts the flow. Same function, asked at a moment when the answer can arrive.

  It also HOLDS the flow until tapped, deliberately: node 1 now auto-advances
  after 1s, so a gate that merely overlaid a running flow would have the splash
  gone before it was dismissed.

CONTROLS: tap. Every screen's own affordances work; there is nothing else. Any
screen is still deep-linkable by hash for demoing a specific state.
"""
import base64, importlib.util, pathlib, re, sys, json

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT  = ROOT / "docs/features/first-run/first-run-mobile.html"
SRC  = pathlib.Path(__file__).with_name("build-prototype.py")

spec = importlib.util.spec_from_file_location("first_run_screens", SRC)
P = importlib.util.module_from_spec(spec)
sys.modules["first_run_screens"] = P
spec.loader.exec_module(P)          # __name__ != "__main__", so it writes nothing

SC, SEQ, RUNTIME_JS = P.SC, P.SEQ, P.RUNTIME_JS
CSS = P.css_out()   # every embedded asset resolved — see build-prototype.py

# Same strip as the export: the dashed "simulate" affordances are review
# apparatus. Edge states stay in the file and stay hash-addressable.
SIM = re.compile(r'<button class="sim"[^>]*>.*?</button>', re.S)
strip = lambda h: SIM.sub("", h)

DATA = json.dumps({
    "screens": {k: strip(v["html"]) for k, v in SC.items()},
    "seq": SEQ,
}, ensure_ascii=False)

# The gate's mark. Read straight from the same file build-auth.py uses rather
# than borrowing its `wordmark()` helper: that helper emits the `.mark` class,
# which is absolutely positioned against the splash's bottom edge and would not
# sit in a centred gate. Missing file degrades to the text mark, same as there.
_WM = ROOT / "design-elements/brand/web/noma-wordmark.webp"
GATE_MARK = (
    '<img class="mgate__w" alt="NOMA" src="data:image/webp;base64,%s">'
    % base64.b64encode(_WM.read_bytes()).decode()
) if _WM.exists() else '<p class="mgate__w mgate__w--text">NOMA</p>'

EXTRA = r"""
/* ── the shell: the device IS the phone ──────────────────────────────────
   Everything here overrides the harness's drawn handset. Nothing below this
   comment touches a screen's own layout. */
/* The ground behind the app. Nothing should ever reveal it — `.phone` is fixed
   and full-bleed and `overscroll-behavior` kills rubber-banding — so this is
   purely the graceful-degradation colour, matched to the `theme-color` meta so
   the browser chrome and any sliver agree instead of flashing black. */
html,body{margin:0;padding:0;height:100%;overflow:hidden;background:#EDECEA;
  overscroll-behavior:none;-webkit-text-size-adjust:100%}
/* a tap must never be interpreted as a double-tap zoom or a text selection —
   both make a prototype feel broken in a way that has nothing to do with it */
body{touch-action:manipulation;-webkit-user-select:none;user-select:none;
  -webkit-tap-highlight-color:transparent}

/* `.phone` loses its bezel, its radius and its fixed size, and becomes the
   viewport. `position:fixed` rather than `100vh`: on mobile Safari `vh` counts
   the URL bar, so a fixed inset is the only version that does not leave a strip
   of black at the bottom when the bar retracts. */
.phone{position:fixed;inset:0;width:auto;height:auto;flex:none;
  border-radius:0;box-shadow:none;transform:none;overflow:hidden}
/* the real device draws these itself */
.island,.hbar{display:none}
/* ⚠ THE STATUS BAR KEEPS ITS HEIGHT AND LOSES ITS CONTENTS. The 56px is what
   every screen's top spacing is measured against, so removing the bar would
   pull the whole flow up under the real clock. Hiding only what it paints
   leaves an empty band for the real status bar to sit in.
   `env()` with a 56px floor: taller notches get their space, and a device that
   reports nothing still gets the number the layout was designed on. */
.sbar{height:max(56px, env(safe-area-inset-top));visibility:hidden}
/* the home-indicator area — the harness's 34px bottom padding already
   approximates it; this tops it up on devices that need more */
.scr{padding-bottom:max(34px, calc(env(safe-area-inset-bottom) + 18px))}

/* ── the gate ────────────────────────────────────────────────────────────
   Its only job is to be a real gesture (see the module docstring). Styled as
   part of the product rather than as scaffolding, because it is the first thing
   anyone testing this will see. */
.mgate{position:fixed;inset:0;z-index:200;display:grid;place-items:center;
  background:var(--grad);padding:32px;text-align:center;
  transition:opacity 320ms ease}
.mgate.off{opacity:0;pointer-events:none}
.mgate__w{display:block;width:96px;height:auto;margin:0 auto 26px;opacity:.5}
.mgate__w--text{font-size:20px;font-weight:700;letter-spacing:.22em;
  color:var(--ink)}
.mgate__t{margin:0 0 10px;font-size:22px;font-weight:700;letter-spacing:-.016em;
  color:var(--ink)}
.mgate__n{margin:0;font-size:13px;line-height:1.5;color:var(--sec);max-width:22em}
.mgate__b{margin-top:30px;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ter)}
@media (prefers-reduced-motion:reduce){.mgate{transition:none}}
"""

BODY = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#EDECEA">
<title>NOMA — first run (mobile)</title>
<style>{CSS}{EXTRA}</style>
</head><body>
<div class="phone" id="phone"><div class="island"></div><div class="hbar"></div></div>

<div class="mgate" id="mgate">
  <div>
    {GATE_MARK}
    <p class="mgate__t">First run</p>
    <p class="mgate__n">Tilt the phone on the key card screens — the card catches
      the light as you move.</p>
    <p class="mgate__b">Tap to begin</p>
  </div>
</div>

<script>
const S = {DATA};
let idx = 0, off = null, hist = [];
{RUNTIME_JS}
const cur = () => off || S.seq[idx];

/* ⚠ A NO-OP ON PURPOSE. The harness calls `fit()` after each render to rescale
   its drawn handset; here the handset is the viewport and must not be
   transformed at all — see the module docstring on why placeKey() depends on
   that. The call site is guarded (`typeof fit === 'function'`), so this could be
   omitted entirely; it is defined so the absence is explicit rather than
   looking like something that was forgotten. */
function fit(){{}}

function render(dir){{
  clearTimers();
  const ph = document.getElementById('phone');
  /* same seamless swap as the harness: the incoming screen goes on top before
     the outgoing one is removed, so there is never a frame with no content */
  ph.querySelectorAll('.scr.out').forEach(n => n.remove());
  const outgoing = [...ph.querySelectorAll('.scr')];
  const el = document.createElement('div');
  el.innerHTML = S.screens[cur()];
  el.className = 'scr ' + carryClass(S.screens[cur()], dir);
  ph.appendChild(el);
  outgoing.forEach(o => o.remove());
{P.WIRE_JS}
}}
function jumpTo(id){{ const i = S.seq.indexOf(id);
  if (i > -1) {{ off = null; hist = []; idx = i; render(); return true; }} return false; }}
function go(t){{
  if (t === 'next')        return advance();
  if (t === 'back')        return backward();
  if (t === 'restart')     return reset();
  if (t === 'skip-invite') return jumpTo('D1') || advance();
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

function fromHash(){{
  const h = decodeURIComponent(location.hash.replace('#', '')).trim();
  if (h && S.screens[h]) {{ go(h); return true; }}
  return false;
}}
addEventListener('hashchange', fromHash);

/* ── the gate hands over ─────────────────────────────────────────────────
   `askGyro()` is the harness's own function; calling it from inside this
   listener is the whole point — it is a real gesture, so iOS will actually show
   the permission sheet. The flow does not start until this runs, because node 1
   auto-advances after 1s and would otherwise be gone before the gate cleared. */
const gate = document.getElementById('mgate');
function begin(){{
  gate.removeEventListener('click', begin);
  if (typeof askGyro === 'function') askGyro();
  gate.classList.add('off');
  if (!fromHash()) render();
}}
gate.addEventListener('click', begin);
</script>
</body></html>
"""

OUT.write_text(BODY)
print(f"wrote {OUT.relative_to(ROOT)}  screens={len(SC)}  path={len(SEQ)}  "
      f"{len(BODY)/1024/1024:.2f} MB")
