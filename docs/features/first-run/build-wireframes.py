#!/usr/bin/env python3
"""
Build docs/features/first-run/first-run-wireframes.html

The same flow as first-run-prototype.html, laid out flat: every screen at once,
grouped by the node it belongs to in the owner's flow diagram (2026-08-06), with
the edge states that hang off each node shown beside it. For print and for review
meetings, where clicking through 36 screens one at a time is not the point.

    python3 docs/features/first-run/build-wireframes.py

GENERATED FROM build-prototype.py — DO NOT REDEFINE SCREENS HERE.
Until 2026-08-06 this file carried its own second copy of every screen in a
different renderer, and the two drifted: the prototype was corrected to the
owner's flow and the board still showed the old ordering. There is now exactly
one screen set. If a screen is wrong, fix it in build-prototype.py and rebuild
both.
"""
import importlib.util, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT  = ROOT / "docs/features/first-run/first-run-wireframes.html"
SRC  = pathlib.Path(__file__).with_name("build-prototype.py")

spec = importlib.util.spec_from_file_location("first_run_screens", SRC)
P = importlib.util.module_from_spec(spec)
sys.modules["first_run_screens"] = P
spec.loader.exec_module(P)          # __name__ != "__main__", so it writes nothing

SC, SEQ, E = P.SC, P.SEQ, P.E
CSS = P.css_out()   # every embedded asset resolved — see build-prototype.py

# ───────────────────────────────────────────── grouping
# One column per diagram node. Edge states are attached to the node whose screen
# they are reachable from — worked out from the data, not hand-maintained: a state
# belongs to the last backbone screen that links to it.
OWNER = {}
for sid in SEQ:
    html_ = SC[sid]["html"]
    for other in SC:
        if SC[other]["kind"] == "state" and f'data-go="{other}"' in html_:
            OWNER.setdefault(other, sid)
# A state reachable only from another state (help pages behind an error) inherits
# that state's node, so nothing falls off the board.
for _ in range(4):
    for sid, s in SC.items():
        if s["kind"] != "state" or sid not in OWNER:
            continue
        for other in SC:
            if SC[other]["kind"] == "state" and other not in OWNER \
               and f'data-go="{other}"' in s["html"]:
                OWNER[other] = OWNER[sid]
orphans = [s for s, v in SC.items() if v["kind"] == "state" and s not in OWNER]

NODES = []
for sid in SEQ:
    n = SC[sid]["node"]
    if not NODES or NODES[-1]["node"] != n:
        NODES.append(dict(node=n, screens=[], states=[]))
    NODES[-1]["screens"].append(sid)
for st, owner in OWNER.items():
    for grp in NODES:
        if owner in grp["screens"]:
            grp["states"].append(st)
            break

TOTAL = len([g for g in NODES if "a" not in str(g["node"])])
BRANCHES = len([g for g in NODES if "a" in str(g["node"])])  # 4a, 5a, 18a

# ───────────────────────────────────────────── render
def phone(sid, state=False):
    s = SC[sid]
    cls = "bd bd--state" if state else "bd"
    tag = ("edge state" if state else
           f'node {s["node"]}' + (" · branch" if "a" in str(s["node"]) else ""))
    return (f'<figure class="{cls}" id="s-{sid}">'
            f'<div class="bd__hd"><span class="bd__id">{E(sid)}</span>'
            f'<span class="bd__t">{E(s["title"])}</span>'
            f'<span class="bd__k">{E(tag)}</span></div>'
            f'<div class="bd__ph"><div class="scr">{s["html"]}</div></div>'
            + (f'<figcaption>{s["note"]}</figcaption>' if s["note"] else "")
            + "</figure>")

groups = []
for g in NODES:
    n = g["node"]
    branch = "a" in str(n)
    head = (f'<div class="nd__hd"><span class="nd__n">{E(n)}</span>'
            f'<span class="nd__t">{E(SC[g["screens"][0]]["sec"])}</span>'
            + ('<span class="nd__b">branch</span>' if branch else
               f'<span class="nd__c">of {TOTAL}</span>')
            + '</div>')
    body = "".join(phone(s) for s in g["screens"])
    states = ("".join(phone(s, True) for s in g["states"]))
    groups.append(f'<section class="nd{" nd--branch" if branch else ""}">{head}'
                  f'<div class="nd__row">{body}'
                  + (f'<div class="nd__st">{states}</div>' if states else "")
                  + '</div></section>')

EXTRA = r"""
body{overflow:auto;background:#F2F1EF}
.wrap{max-width:1680px;margin:0 auto;padding:52px 40px 90px}
.top{margin-bottom:46px;max-width:760px}
.top h1{font-size:38px;line-height:1.06;letter-spacing:-.032em;margin:0 0 14px}
.top p{font-size:15px;line-height:1.6;color:var(--sec);margin:0 0 12px}
.top .k{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;letter-spacing:.06em;
  color:var(--ter);text-transform:uppercase}
.top ul{margin:0;padding-left:18px;font-size:14px;line-height:1.6;color:var(--sec)}
.top li{margin-bottom:5px}
.top b{color:var(--ink)}

.nd{margin-bottom:34px;padding-bottom:30px;border-bottom:1px solid rgba(11,11,11,.10)}
.nd--branch{background:rgba(11,11,11,.035);border-radius:22px;padding:22px 22px 20px;
  border-bottom:0;margin-bottom:38px}
.nd__hd{display:flex;align-items:baseline;gap:14px;margin-bottom:18px}
.nd__n{font-size:30px;font-weight:700;letter-spacing:-.04em;min-width:52px}
.nd__t{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--ter);font-weight:600}
.nd__c,.nd__b{margin-left:auto;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ter)}
.nd__b{color:var(--ink);border:1px solid var(--hair);border-radius:99px;padding:4px 11px}
.nd__row{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
.nd__st{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;padding-left:20px;
  border-left:1px dashed rgba(11,11,11,.22)}

.bd{margin:0;width:300px;flex:0 0 auto}
.bd__hd{display:flex;align-items:baseline;gap:8px;margin-bottom:9px;padding-bottom:7px;
  border-bottom:1px solid rgba(11,11,11,.12)}
.bd__id{font-family:ui-monospace,Menlo,monospace;font-size:10px;color:var(--ter)}
.bd__t{font-size:13.5px;font-weight:600;letter-spacing:-.01em}
.bd__k{margin-left:auto;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ter)}
.bd--state .bd__k{color:var(--err)}
.bd--state .bd__hd{border-bottom-color:rgba(138,47,30,.34)}
.bd__ph{width:300px;height:649px;border-radius:40px;overflow:hidden;position:relative;
  background:var(--grad);box-shadow:0 0 0 7px #17171A,0 14px 34px rgba(0,0,0,.16)}
.bd__ph::before{content:"";position:absolute;inset:0;background:rgba(255,255,255,.30);z-index:0}
.bd__ph .scr{position:absolute;top:0;left:0;width:390px;height:844px;
  transform:scale(.769);transform-origin:top left;padding:0 22px 34px;
  display:flex;flex-direction:column;overflow:hidden;z-index:1;animation:none}
.bd figcaption{font-size:12px;line-height:1.5;color:var(--sec);margin-top:11px}

@media print{
  body{background:#fff}
  .wrap{max-width:none;padding:0}
  .nd{break-inside:avoid;page-break-inside:avoid}
  .bd__ph{box-shadow:0 0 0 1px rgba(0,0,0,.3)}
}
"""

BODY = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOMA — onboarding &amp; device setup, flat board</title>
<style>{CSS}{EXTRA}</style>
</head><body>
<div class="wrap">
  <header class="top">
    <p class="k">Generated from build-prototype.py &middot; {len(SEQ)} screens &middot;
      {TOTAL} nodes + {BRANCHES} branch{"" if BRANCHES == 1 else "es"}</p>
    <h1>Onboarding &amp; device setup</h1>
    <p>Every screen of the owner&rsquo;s flow diagram (2026-08-06), in order, one block per box.
      Screens sharing a number are two halves of one box &mdash; an OS dialog over the screen that
      explains it, a spinner that resolves into an offer. The dashed column to the right of a block
      holds the edge states reachable from it.</p>
    <p><b>Changed from the 2026-08-05 build:</b></p>
    <ul>
      <li>Email account creation is new &mdash; nodes 4 and 5.</li>
      <li>The device-type chooser is back &mdash; node 6.</li>
      <li>The home is created while naming the room &mdash; node 17 &mdash; not on a screen of its
        own before the box is opened.</li>
      <li>The household is a 3-screen branch off node 18, down from eleven screens ahead of the
        device.</li>
      <li>The location / geofencing ask is new &mdash; node 24.</li>
      <li>Gone: the standalone consent pair, the analytics opt-in, and the separate reveal screen.</li>
    </ul>
  </header>
  {"".join(groups)}
</div>
</body></html>
"""

OUT.write_text(BODY)
print(f"wrote {OUT.relative_to(ROOT)}  nodes={len(NODES)}  screens={len(SEQ)}  "
      f"states={len(OWNER)}  orphan-states={orphans}  {len(BODY)/1024/1024:.2f} MB")
