#!/usr/bin/env python3
"""
Build docs/features/first-run/first-run-export.html

A CLEAN, SHAREABLE export of the first-run prototype: one phone, centred, tappable,
and nothing else. No controller rail, no node numbers, no design notes, no
"simulate" buttons. This is the file to send to someone who should experience the
flow rather than review it.

    python3 docs/features/first-run/build-export.py

GENERATED FROM build-prototype.py — DO NOT REDEFINE SCREENS HERE.
Same rule as build-wireframes.py: one screen set, three renderings (harness, flat
board, export). A flow change is made once, in build-prototype.py, and all three
rebuild from it.

WHAT IS STRIPPED, AND WHY IT MATTERS:
  · The controller rail, the jump list, the per-screen design notes — review
    apparatus, not product.
  · Every `sim` button (the dashed "Simulate: wrong password" affordances). These
    were the ONLY way to reach most edge states, so in this export the 13 edge
    states are unreachable by tapping. They are still in the file and still
    addressable by URL hash (e.g. `…first-run-export.html#W2E`) so they can be
    demoed deliberately — but a stakeholder clicking through will only ever see
    the happy path. That is the intent; just do not mistake this file for evidence
    that the error states exist. The harness is where those get reviewed.

CONTROLS: tap anything, or use ← / →. Any screen is deep-linkable by hash.
"""
import importlib.util, pathlib, re, sys, json

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _phone_fit import JS as FIT_JS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT  = ROOT / "docs/features/first-run/first-run-export.html"
SRC  = pathlib.Path(__file__).with_name("build-prototype.py")

spec = importlib.util.spec_from_file_location("first_run_screens", SRC)
P = importlib.util.module_from_spec(spec)
sys.modules["first_run_screens"] = P
spec.loader.exec_module(P)          # __name__ != "__main__", so it writes nothing

SC, SEQ, RUNTIME_JS = P.SC, P.SEQ, P.RUNTIME_JS
CSS = P.css_out()   # every embedded asset resolved — see build-prototype.py

SIM = re.compile(r'<button class="sim"[^>]*>.*?</button>', re.S)
strip = lambda h: SIM.sub("", h)

DATA = json.dumps({
    "screens": {k: strip(v["html"]) for k, v in SC.items()},
    "seq": SEQ,
}, ensure_ascii=False)

EXTRA = r"""
/* the export shell: one phone, centred, nothing competing with it */
body{background:#EDECEA}
.stagex{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
  padding:20px}
.phone{flex:none;transform-origin:center center}
@media (prefers-reduced-motion:reduce){.scr.in,.scr.bk{animation:none}}
"""

BODY = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOMA — onboarding &amp; device setup</title>
<style>{CSS}{EXTRA}</style>
</head><body>
<div class="stagex">
  <div class="phone" id="phone"><div class="island"></div><div class="hbar"></div></div>
</div>
<script>
const S = {DATA};
let idx = 0, off = null, hist = [];
{RUNTIME_JS}
const cur = () => off || S.seq[idx];

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
  fit();
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
/* Kept as `fit` so the existing call sites are untouched; the measurement
   lives in docs/features/_phone_fit.py now. */
function fit(){{ fitPhone({{stage: '.stagex', padY: 40, padX: 40}}); }}
watchPhoneFit({{stage: '.stagex', padY: 40, padX: 40}});
addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') advance();
  if (e.key === 'ArrowLeft')  backward();
}});
function fromHash(){{
  const h = decodeURIComponent(location.hash.replace('#', '')).trim();
  if (h && S.screens[h]) {{ go(h); return true; }}
  return false;
}}
addEventListener('hashchange', fromHash);
if (!fromHash()) render();
fit();
</script>
</body></html>
"""

OUT.write_text(BODY)
stripped = sum(len(SIM.findall(v["html"])) for v in SC.values())
print(f"wrote {OUT.relative_to(ROOT)}  screens={len(SC)}  path={len(SEQ)}  "
      f"sim-buttons-stripped={stripped}  {len(BODY)/1024/1024:.2f} MB")
