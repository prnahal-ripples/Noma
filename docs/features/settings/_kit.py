#!/usr/bin/env python3
"""
docs/features/settings/_kit.py — shared chrome for the two settings surfaces.

NOMA has TWO settings pages and they are not the same thing:

  build-profile-settings.py   →  profile-settings-prototype.html
      The app / home settings. "Ruhaan's Home", who's in it, which rooms and
      devices exist, app-wide preferences, privacy, account. Reached from the
      profile avatar. Scope: the whole home.

  build-device-settings.py    →  device-settings-prototype.html
      One purifier's settings. QSensAI, Silent Mode, filter, firmware, remove
      device. Reached from the gear inside a device. Scope: one device.
      IA transcribed from `PurSettingsBody` in the owner's PM prototype.

They are siblings in the same app, so they must look identical — same rows,
same section labels, same toggles, same danger treatment. That is why the
chrome lives here rather than being copy-pasted into both: two files drifting
apart is exactly how a settings surface starts feeling like two apps.

Neither script restates a token. Both read src/tokens/design.tokens.js through
node at build time. Re-run both after a token change.

✅ THE DESTRUCTIVE ROW HAS ITS COLOUR BACK — 2026-08-13.
This docstring previously argued at length that it did not, and that the loss
was real. That is now history: the owner supplied a negative red, so
`colors.status` is populated and `DANGER` is a red again rather than ink.

The decision that was pending got made in the owner's favour — one red,
scoped to negative meaning only. What matters for anyone reading this file:

  · DANGER is `status.negative.text` = #A03B3B, NOT the supplied anchor
    #F38E8E. The anchor is LIGHT: it measures 2.09:1 as text on canvas and
    5.88:1 under ink. It is a surface colour, not a text colour. Using it for
    the destructive label would be unreadable. Same trap as the greens.
  · Red is scoped to WRONG / LOST / DESTRUCTIVE. It is not a second accent
    and it is not "attention". Do not decorate with it.
  · O-6 is HALF closed. `status.warning` is still null, so "filter at 10%"
    and "firmware out of date" still have no colour — they are nudges, not
    faults, and painting them this red overstates them. That one is still an
    owner decision.
"""

import base64
import json
import pathlib
import subprocess
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _phone_fit import CSS as FIT_CSS, JS as FIT_JS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"
FONT = "../../../src/fonts/google-sans-flex/GoogleSansFlex-VariableFont_GRAD,ROND,opsz,slnt,wdth,wght.ttf"


def load_tokens():
    script = (
        "import(%s).then(m=>{"
        "const {colors,effects,elevation,gradients,green,layout,neutral,radius,spacing,typography,recipes}=m;"
        "process.stdout.write(JSON.stringify("
        "{colors,effects,elevation,gradients,green,layout,neutral,radius,spacing,typography,recipes}"
        "));})" % json.dumps(TOKENS.as_uri())
    )
    res = subprocess.run(["node", "--input-type=module", "-e", script],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit("Could not read %s through node.\n%s" % (TOKENS, res.stderr.strip()))
    return json.loads(res.stdout)


T = load_tokens()
C, G, N, R, S = T["colors"], T["gradients"], T["neutral"], T["radius"], T["spacing"]
EL, LAY, RC = T["elevation"], T["layout"], T["recipes"]
FX = T["effects"]

# RESOLVED 2026-08-13. The owner supplied a negative red, so `colors.status`
# is no longer null and the destructive row gets its colour back. This is
# `status.negative.text` (#A03B3B), NOT the supplied anchor #F38E8E — the
# anchor measures 2.09:1 as text on canvas and would be unreadable. See the
# `red` primitive in design.tokens.js for the full measurement table.
DANGER = C["status"]["negative"]["text"]
NEGATIVE = C["status"]["negative"]

ICONS = {
    "back":    '<path d="M14.5 5.5 8 12l6.5 6.5"/>',
    "chev":    '<path d="M9.5 5.5 16 12l-6.5 6.5"/>',
    "restart": '<polyline points="21.5 4 21.5 9.5 16 9.5"/>'
               '<path d="M19.6 14.2A8.2 8.2 0 1 1 17.7 5.7l3.8 3.8"/>',
    "trash":   '<path d="M4.8 7h14.4"/><path d="M9.4 7V4.8h5.2V7"/>'
               '<path d="M6.6 7.2 7.5 20h9l.9-12.8"/>',
    "signout": '<path d="M14 4.5H6.5v15H14"/><path d="M11 12h9.5M17.4 8.6l3.4 3.4-3.4 3.4"/>',
    "home":    '<path d="M3 10.5 12 3l9 7.5"/><path d="M5.5 9.5V20h13V9.5"/>',
    "people":  '<circle cx="9" cy="8" r="3.2"/><path d="M2.8 19.5c.6-3.3 3.2-5 6.2-5s5.6 1.7 6.2 5"/>'
               '<path d="M16.5 5.6a3.2 3.2 0 0 1 0 6.3"/><path d="M18 14.8c2.1.5 3.5 2.1 3.9 4.7"/>',
    "clock":   '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.2 2"/>',
    "filter":  '<path d="M4 5.5h16l-6.2 7.2V20l-3.6-2.2v-5.1z"/>',
    "wind":    '<path d="M3 8.5h9.5a3 3 0 1 0-3-3"/><path d="M3 13h13a3 3 0 1 1-3 3"/><path d="M3 17.5h6"/>',
    "chip":    '<rect x="6.5" y="6.5" width="11" height="11" rx="2.4"/>'
               '<path d="M9.5 3v3M14.5 3v3M9.5 18v3M14.5 18v3M3 9.5h3M3 14.5h3M18 9.5h3M18 14.5h3"/>',
    "bell":    '<path d="M6.5 10a5.5 5.5 0 0 1 11 0c0 4 1.5 5.4 1.5 5.4H5S6.5 14 6.5 10z"/>'
               '<path d="M10.2 18.6a2 2 0 0 0 3.6 0"/>',
    "palette": '<path d="M12 3.4c-4.8 0-8.6 3.7-8.6 8.4 0 4.8 3.6 8.2 8 8.2 1.6 0 2.5-.9 2.5-2 '
               '0-1.4-1.2-1.7-1.2-2.8 0-.9.7-1.5 1.8-1.5h1.6c2.6 0 4.5-1.7 4.5-4.3 0-3.5-3.5-6-8.6-6z"/>'
               '<circle cx="8" cy="10.5" r="1.1" fill="currentColor" stroke="none"/>'
               '<circle cx="12" cy="7.8" r="1.1" fill="currentColor" stroke="none"/>'
               '<circle cx="16" cy="10.2" r="1.1" fill="currentColor" stroke="none"/>',
    "globe":   '<circle cx="12" cy="12" r="8.6"/><path d="M3.6 12h16.8"/>'
               '<path d="M12 3.4c2.2 2.4 3.3 5.4 3.3 8.6s-1.1 6.2-3.3 8.6c-2.2-2.4-3.3-5.4-3.3-8.6S9.8 5.8 12 3.4z"/>',
    "access":  '<circle cx="12" cy="4.6" r="1.9"/><path d="M4.6 8.4h14.8"/><path d="M12 8.4v5.3"/>'
               '<path d="m8.6 20.4 3.4-6.7 3.4 6.7"/>',
    "shield":  '<path d="M12 3.2 5 6v6c0 4.2 2.9 7.4 7 8.8 4.1-1.4 7-4.6 7-8.8V6z"/>'
               '<path d="m9.2 12 2 2 3.6-3.8"/>',
    "link":    '<path d="M10.2 13.8a3.6 3.6 0 0 0 5.1 0l2.6-2.6a3.6 3.6 0 1 0-5.1-5.1l-1.3 1.3"/>'
               '<path d="M13.8 10.2a3.6 3.6 0 0 0-5.1 0l-2.6 2.6a3.6 3.6 0 1 0 5.1 5.1l1.3-1.3"/>',
    "help":    '<circle cx="12" cy="12" r="8.6"/><path d="M9.6 9.4a2.5 2.5 0 0 1 4.8.8c0 1.7-2.4 2-2.4 3.5"/>'
               '<circle cx="12" cy="17" r=".9" fill="currentColor" stroke="none"/>',
    "info":    '<circle cx="12" cy="12" r="8.6"/><path d="M12 11v5.4"/>'
               '<circle cx="12" cy="7.9" r="1" fill="currentColor" stroke="none"/>',
    "plus":    '<path d="M12 5.5v13M5.5 12h13"/>',
    "check":   '<path d="m5.5 12.5 4.2 4.2 8.8-9.4"/>',
    "devices": '<rect x="3" y="5" width="12" height="9" rx="1.8"/><path d="M6 18h6"/>'
               '<rect x="17" y="9" width="4" height="10" rx="1.4"/>',
}


def ico(name, size=20, sw=1.7):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (size, size, sw, ICONS[name]))


def status_bar():
    return ('<div class="sbar"><span class="sbar__t">9:41</span><span class="sbar__r">'
            '<svg width="17" height="11" viewBox="0 0 17 11" fill="currentColor">'
            '<rect x="0" y="7.5" width="2.6" height="3.5" rx="1"/>'
            '<rect x="4.2" y="5.2" width="2.6" height="5.8" rx="1"/>'
            '<rect x="8.4" y="2.6" width="2.6" height="8.4" rx="1"/>'
            '<rect x="12.6" y="0" width="2.6" height="11" rx="1"/></svg>'
            '<svg width="16" height="11" viewBox="0 0 16 11" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round"><path d="M1 4.1a10 10 0 0 1 14 0"/>'
            '<path d="M3.6 6.7a6.4 6.4 0 0 1 8.8 0"/>'
            '<circle cx="8" cy="9.6" r=".9" fill="currentColor" stroke="none"/></svg>'
            '<span class="bat"><i></i></span></span></div>')


def top_bar(title="", back=True, help_link=False):
    left = ('<button class="iconbtn" data-back>%s</button>' % ico("back", 18)
            if back else '<span class="sp"></span>')
    right = ('<button class="link">Help</button>' if help_link
             else '<span class="sp"></span>')
    mid = '<span class="topbar__t">%s</span>' % title
    return '<div class="topbar">%s%s%s</div>' % (left, mid, right)


ICON_DIR = ROOT / "design-elements" / "3d-icons" / "web"
_ICON_CACHE = {}

# Rendered size of a tier-1 icon in a page header. Read from the token file,
# never restated here (CLAUDE.md rule 2) — the Vercel dashboard reads the same
# export, so the two surfaces cannot disagree about how big these are.
ICON_PX = LAY["iconHeaderSize"]

# Every L2 header that has asked for an icon which does not exist on disk.
# Populated as a side effect of icon3d() and reported by page(), so a
# placeholder can never ship silently.
MISSING_ICONS = []


def _placeholder_icon(name):
    """A visibly-unfinished stand-in for a tier-1 icon that doesn't exist yet.

    Deliberately NOT a plausible icon. It is flat, grey, dashed and labelled,
    so nobody can mistake it for the real render in a screenshot or a review —
    the failure mode to avoid is a placeholder quietly becoming the design.

    An SVG data URI rather than a file, because a file in `web/` is
    indistinguishable from a real asset and would need its own cleanup step.
    Drop `<name>.png` into design-elements/3d-icons/, run the resize snippet
    in that folder's README, and the real icon takes over on the next build
    with no code change — icon3d() checks disk first."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">'
        '<rect x="4" y="4" width="88" height="88" rx="22" fill="#E4E3DF"/>'
        '<rect x="4.75" y="4.75" width="86.5" height="86.5" rx="21.25"'
        ' fill="none" stroke="#B4B2AB" stroke-width="1.5"'
        ' stroke-dasharray="6 5"/>'
        '<g fill="none" stroke="#96948C" stroke-width="2.4"'
        ' stroke-linejoin="round" stroke-linecap="round">'
        '<path d="M48 26 66 36v20L48 66 30 56V36z"/>'
        '<path d="M30 36l18 10 18-10M48 46v20"/></g>'
        '<text x="48" y="83" text-anchor="middle" fill="#96948C"'
        ' font-family="ui-sans-serif,system-ui,sans-serif" font-size="9.5"'
        ' font-weight="600" letter-spacing=".6">%s</text></svg>'
        % name[:11].upper())
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg)


def icon3d(name):
    """A tier-1 3D icon as a base64 data URI.

    Embedded rather than linked so a prototype stays a single portable file —
    the same reason the fonts are embedded. These are viewed from disk, from a
    local server, and from the Vercel dashboard at three different relative
    depths; a linked path would have to be right in all three and silently
    404s when it isn't.

    Source of truth is the 800x1000 PNG beside `web/`. The embedded copy is a
    288px WebP derivative (~11-22KB each, about a tenth of the PNG) built by
    the snippet in the folder README. Re-run it if an icon is replaced.

    A name with no file behind it yields a labelled placeholder rather than an
    error, so an L2 page can be built before its icon has been drawn. The name
    is recorded in MISSING_ICONS and printed by the build."""
    if name not in _ICON_CACHE:
        p = ICON_DIR / ("%s.webp" % name)
        if not p.exists():
            if name not in MISSING_ICONS:
                MISSING_ICONS.append(name)
            _ICON_CACHE[name] = ("raw", _placeholder_icon(name))
        else:
            _ICON_CACHE[name] = (
                "webp", base64.b64encode(p.read_bytes()).decode("ascii"))
    kind, payload = _ICON_CACHE[name]
    return payload if kind == "raw" else "data:image/webp;base64," + payload


def page_header(icon, title, sub, title_lead=None):
    """The L2 inner-page header: 3D icon, big title, centred description.

    Owner's 2026-08-14 reference set, and the standard structure for EVERY L2
    inner page — not just the four the references covered. The 3D icons are
    used SPARINGLY and almost always here: one per page, at the top, as the
    page's identity. They are not row icons and not decoration; tier 2 (flat
    monoline) still owns everything inside a list.

    `title_lead` renders a bold lead-in with the rest regular, for the
    "**3 people** here" shape in the Family reference. Where the lead is a
    count, derive it from the data it counts — a hardcoded one drifted once
    already (root said "4 people", Family listed 3)."""
    h1 = ('<span class="ph__lead">%s</span><span class="ph__rest"> %s</span>'
          % (title_lead, title) if title_lead else title)
    return ('<div class="ph">'
            '<img class="ph__i" src="%s" alt="" width="%d" height="%d">'
            '<h1 class="ph__t">%s</h1>'
            '<p class="ph__s">%s</p></div>'
            % (icon3d(icon), ICON_PX, ICON_PX, h1, sub))


def toggle(on, name):
    return ('<button class="tg%s" role="switch" aria-checked="%s" aria-label="%s">'
            '<i></i></button>' % (" tg--on" if on else "", str(on).lower(), name))


def segmented(opts, at, name):
    return '<span class="seg" role="group" aria-label="%s">%s</span>' % (
        name, "".join('<button class="seg__o%s">%s</button>'
                      % (" seg__o--on" if o == at else "", o) for o in opts))


def _lerp_hex(a, b, t):
    """Linear-interpolate two hex colours. Used to sweep filled bars from
    green.mint to green.lime by position, rather than one flat fill."""
    a = a.lstrip("#")
    b = b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        av, bv = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append("%02X" % round(av + (bv - av) * t))
    return "#" + "".join(out)


def meter(frac, total=10, size="sm"):
    """recipes.progressTrack — INDIVIDUAL RECTANGLES, 2px corners, 4px gap.

    ⚠ Replaces a previous version that faked segments with a repeating-
    gradient mask over one continuous bar, wrapped in a pill container — a
    squashed capsule, not discrete shapes. This is the owner's correction:
    real elements, no wrapping pill, no mask.
    """
    filled = round(total * frac)
    RC_ = RC["progressTrack"]
    bars = []
    for i in range(total):
        if i < filled:
            t = i / max(filled - 1, 1)
            color = _lerp_hex(RC_["fillFrom"], RC_["fillTo"], t)
            bars.append('<i style="background:%s"></i>' % color)
        else:
            bars.append('<i class="meter__off"></i>')
    return '<span class="meter meter--%s">%s</span>' % (size, "".join(bars))


def row(r):
    """One settings row.
    kind: chev | toggle | seg | danger | restart | value | plain
    """
    kind = r.get("kind", "chev")
    tail, cls, attr = "", "", ""
    if kind == "toggle":
        tail, cls = toggle(r["on"], r["t"]), " row--static"
    elif kind == "seg":
        tail, cls = segmented(r["opts"], r["at"], r["t"]), " row--static"
    elif kind == "value":
        tail, cls = '<span class="row__v">%s</span>' % r["v"], " row--static"
    elif kind == "restart":
        tail = '<span class="row__ic">%s</span>' % ico("restart", 17)
    elif kind == "danger":
        # Only add the trailing trash when the row has no leading icon — the
        # profile surface puts icons on the left, so both would render and you
        # get the same bin twice on one row.
        tail = "" if r.get("i") else '<span class="row__ic">%s</span>' % ico("trash", 17)
        cls = " row--danger"
    elif kind == "plain":
        cls = " row--plain"
    else:
        if r.get("dot"):
            tail += '<span class="dot"></span>'
        if r.get("meter") is not None:
            tail += ('<span class="rowmeter">%s<span class="rowmeter__n">%d%%</span></span>'
                     % (meter(r["meter"]), round(r["meter"] * 100)))
        if r.get("v"):
            tail += '<span class="row__v row__v--q">%s</span>' % r["v"]
        tail += '<span class="row__ic">%s</span>' % ico("chev", 16)
    if r.get("go"):
        attr = ' data-go="%s"' % r["go"]
    icon = '<span class="row__i">%s</span>' % ico(r["i"]) if r.get("i") else ""
    sub = '<span class="row__s">%s</span>' % r["s"] if r.get("s") else ""
    tag = "div" if kind in ("toggle", "seg", "value") else "button"
    return ('<%s class="row%s"%s>%s<span class="row__c">'
            '<span class="row__t">%s</span>%s</span>%s</%s>'
            % (tag, cls, attr, icon, r["t"], sub, tail, tag))


def section(label, rows):
    lbl = '<div class="lbl">%s</div>' % label if label else ""
    return '%s<div class="card">%s</div>' % (lbl, "".join(row(r) for r in rows))


def note(txt):
    return '<p class="note">%s</p>' % txt


CSS = f"""
@font-face {{ font-family:'Google Sans Flex'; src:url('{FONT}') format('truetype');
  font-weight:1 1000; font-display:swap; }}
*{{box-sizing:border-box;margin:0;padding:0}}
/* height, not min-height: the phone is scaled to the space available, so the
   page must not be allowed to grow past the viewport and scroll instead. */
body{{font-family:'Google Sans Flex',system-ui,sans-serif;font-optical-sizing:auto;
  background:{N['150']};color:{C['text']['primary']};display:flex;gap:34px;
  padding:34px;height:100vh;overflow:hidden;-webkit-font-smoothing:antialiased}}

.rail{{width:224px;flex:none;align-self:stretch;overflow-y:auto;
  scrollbar-width:none}}
.rail::-webkit-scrollbar{{display:none}}
{FIT_CSS}
.rail__b{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:{C['text']['tertiary']};font-weight:600;margin-bottom:4px}}
.rail__k{{font-size:12px;color:{C['text']['tertiary']};margin-bottom:14px;line-height:1.5}}
.rail__i{{display:block;width:100%;text-align:left;background:{N['0']};border:0;
  border-radius:{R['sm']}px;padding:11px 13px;margin-bottom:6px;font:inherit;
  font-size:13.5px;cursor:pointer;color:{C['text']['secondary']};
  box-shadow:{EL['control']['css']}}}
.rail__i[aria-current="true"]{{color:{C['text']['primary']};font-weight:600;
  box-shadow:{EL['card']['css']},inset 0 0 0 1px {C['border']['bevel']}}}
.rail__n{{font-size:11.5px;line-height:1.6;color:{C['text']['tertiary']};margin-top:16px}}
.rail__n code{{font-family:ui-monospace,Menlo,monospace;font-size:10.5px}}

.phone{{width:390px;height:844px;flex:none;border-radius:52px;position:relative;
  overflow:hidden;background:{G['canvas']['css']};box-shadow:0 40px 90px rgba(0,0,0,.16)}}
.notch{{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:122px;
  height:33px;background:{N['900']};border-radius:20px;z-index:60}}
.hbar{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:138px;
  height:5px;background:rgba(0,0,0,.2);border-radius:3px;z-index:60}}
.scr{{position:absolute;inset:0;display:none;flex-direction:column}}
.scr[data-on]{{display:flex;animation:in .32s cubic-bezier(.22,1,.36,1)}}
@keyframes in{{from{{opacity:0;transform:translateX(14px)}}}}

.sbar{{height:54px;flex:none;display:flex;align-items:center;justify-content:space-between;
  padding:14px {LAY['screenPaddingX']}px 0}}
.sbar__t{{font-size:15px;font-variation-settings:'wght' 600;letter-spacing:-.2px}}
.sbar__r{{display:flex;align-items:center;gap:5px}}
.bat{{width:25px;height:12px;border-radius:3.5px;border:1.3px solid currentColor;
  padding:1.4px;display:block}}
.bat i{{display:block;height:100%;width:88%;background:currentColor;border-radius:1.4px}}

.body{{flex:1;overflow-y:auto;padding:0 {LAY['screenPaddingX']}px;scrollbar-width:none}}
.body::-webkit-scrollbar{{display:none}}
.pad{{height:36px}}

.topbar{{display:flex;align-items:center;justify-content:space-between;padding:6px 0 18px}}
.topbar__t{{font-size:17px;font-variation-settings:'wght' 600;letter-spacing:-.2px}}
.sp{{width:{LAY['controlSize']}px}}
.iconbtn{{width:{LAY['controlSize']}px;height:{LAY['controlSize']}px;
  border-radius:{R['full']}px;background:{C['surface']['control']};border:0;
  display:grid;place-items:center;cursor:pointer;color:{C['icon']['primary']};
  box-shadow:{EL['control']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']}}}
.iconbtn:active{{transform:scale(.94)}}
/* recipes.buttonTint — bare coloured text has no touch target and no
   affordance; the tinted pill gives it both without spending a button. */
.link{{border:0;font:inherit;font-size:15px;font-variation-settings:'wght' 600;
  color:{RC['buttonTint']['color']};cursor:pointer;
  background:{RC['buttonTint']['background']};
  height:{RC['buttonTint']['height']}px;padding:0 {RC['buttonTint']['paddingX']}px;
  border-radius:{R['full']}px;box-shadow:{FX['tintPill']['css']}}}
.link:active{{transform:scale(.97)}}

.h1{{font-size:30px;line-height:36px;letter-spacing:-.6px;
  font-variation-settings:'opsz' 30,'wght' 400;margin-bottom:6px}}
.h1 b{{font-variation-settings:'opsz' 30,'wght' 700}}
.sub{{font-size:15px;line-height:21px;color:{C['text']['secondary']};margin-bottom:10px}}

/* ---- L2 page header: 3D icon, big title, centred description -----------
   Owner's 2026-08-14 reference set. The tier-1 3D icon appears HERE and
   essentially nowhere else: one per page, at the top, as the page's
   identity. Rows keep the flat tier-2 glyphs. */
.ph{{display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:8px 4px 6px}}
.ph__i{{width:{ICON_PX}px;height:{ICON_PX}px;object-fit:contain;display:block;
  margin-bottom:14px;
  /* the render carries its own lighting; a soft contact shadow sits it on
     the page rather than leaving it floating */
  filter:drop-shadow(0 10px 14px rgba(0,0,0,.10))}}
.ph__t{{font-size:29px;line-height:35px;letter-spacing:-.6px;
  font-variation-settings:'opsz' 29,'wght' 700;margin-bottom:8px}}
.ph__lead{{font-variation-settings:'opsz' 29,'wght' 700}}
.ph__rest{{font-variation-settings:'opsz' 29,'wght' 400}}
.ph__s{{font-size:15.5px;line-height:22px;color:{C['text']['tertiary']};
  max-width:31ch;margin:0 auto 20px}}

.lbl{{font-size:12px;line-height:16px;letter-spacing:.96px;text-transform:uppercase;
  font-variation-settings:'wght' 600;color:{C['text']['secondary']};margin:24px 0 9px 4px}}
.card{{background:{C['surface']['raised']};border-radius:{R['xl']}px;
  box-shadow:{EL['card']['css']},{G['gloss']['css']};overflow:hidden;padding:2px 0}}
.card--pad{{padding:{LAY['cardPaddingY']}px {LAY['cardPaddingX']}px}}
.card + .card{{margin-top:{LAY['stackGap']}px}}
.lbl + .card{{margin-top:0}}

.row{{display:flex;align-items:center;gap:12px;width:100%;border:0;background:none;
  font:inherit;text-align:left;cursor:pointer;color:{C['text']['primary']};
  padding:13px {LAY['cardPaddingX']}px;position:relative}}
.row--static{{cursor:default}}
.row + .row::before{{content:"";position:absolute;top:0;left:{LAY['cardPaddingX']}px;
  right:0;height:1px;background:{C['border']['subtle']}}}
.row__i + .row__c{{}}
.row:has(.row__i) + .row::before{{left:58px}}
button.row:active{{background:{N['50']}}}
.row__i{{color:{C['icon']['secondary']};display:grid;place-items:center;flex:none}}
.row__c{{display:flex;flex-direction:column;flex:1;min-width:0;padding-right:10px}}
.row__t{{font-size:15px;font-variation-settings:'wght' 600;letter-spacing:-.1px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.row__s{{font-size:12px;line-height:16px;color:{C['text']['secondary']};margin-top:3px}}
.row__v{{font-size:13.5px;color:{C['text']['secondary']};white-space:nowrap;
  font-family:ui-monospace,Menlo,monospace}}
.row__v--q{{font-family:inherit;font-size:14px}}
.row__ic{{color:{C['icon']['tertiary']};display:grid;place-items:center;flex:none}}
.row--plain .row__t,.row--plain .row__i{{color:{C['text']['secondary']}}}
.row--danger .row__t,.row--danger .row__ic,.row--danger .row__i{{color:{DANGER}}}

/* LAW 2 — the on-track is a ramp, never a flat green */
/* recipes.toggle, retuned 2026-08-13 to the owner's Figma spec: 56x24, so
   slimmer and proportionally wider than the 58x34 it replaces.

   ⚠ THE KNOB IS A PILL, NOT A SPHERE. It is 30x18 — wider than it is tall —
   with a full radius, which on a non-square box gives a stadium, not a
   circle. The owner's reference marks the circular version with a red X: a
   knob whose width equals its height reads as the platform default. Driven
   off knobW/knobH; `recipes.toggle.knob` no longer exists. */
.tg{{width:{RC['toggle']['width']}px;height:{RC['toggle']['height']}px;
  border-radius:{R['full']}px;border:0;flex:none;
  background:{RC['toggle']['trackOff']};position:relative;cursor:pointer;
  box-shadow:inset 0 1px 2px rgba(0,0,0,.06);
  transition:background .22s cubic-bezier(.22,1,.36,1)}}
.tg i{{position:absolute;top:{RC['toggle']['knobInset']}px;left:{RC['toggle']['knobInset']}px;
  width:{RC['toggle']['knobW']}px;height:{RC['toggle']['knobH']}px;
  border-radius:{R['full']}px;background:{RC['toggle']['knobColor']};
  box-shadow:{RC['toggle']['knobElevation']};
  transition:transform .22s cubic-bezier(.22,1,.36,1)}}
.tg--on{{background:{G['accentRamp']['cssX']};box-shadow:none}}
.tg--on i{{transform:translateX({RC['toggle']['width'] - RC['toggle']['knobW'] - 2*RC['toggle']['knobInset']}px)}}

/* LAW 3 — segmented selection LIFTS, it does not fill with ink */
.seg{{display:inline-flex;gap:2px;flex:none;background:{RC['segmented']['track']};
  border-radius:{RC['segmented']['trackRadius']}px;padding:{RC['segmented']['trackPadding']}px}}
.seg__o{{border:0;background:none;font:inherit;font-size:12.5px;cursor:pointer;
  height:{RC['segmented']['height'] - 2 * RC['segmented']['trackPadding']}px;
  padding:0 {RC['segmented']['optionPaddingX']}px;
  border-radius:{RC['segmented']['optionRadius']}px;color:{RC['segmented']['color']}}}
.seg__o--on{{background:{RC['segmented']['selectedBackground']};
  color:{RC['segmented']['selectedColor']};font-variation-settings:'wght' 600;
  box-shadow:{EL['control']['css']}}}

/* LAW 2 — a bloom with a halo, not a disc */
.dot{{width:8px;height:8px;border-radius:{R['full']}px;flex:none;
  background:{G['accentBloom']['css']};box-shadow:{G['accentBloom']['halo']}}}

/* recipes.progressTrack — INDIVIDUAL RECTANGLES, no wrapping pill, no mask.
   [OWNER REFERENCE] 2px corner radius, 4px gap between bars. Filled bars
   carry their own inline colour (mint -> lime by position, from meter() in
   Python); unfilled bars are flat trackEmpty. */
.meter{{display:inline-flex;align-items:center;
  gap:{RC['progressTrack']['segmentGap']}px}}
.meter i{{border-radius:{RC['progressTrack']['segmentRadius']}px}}
/* --sm: compact, inline next to a row label — bars are a fixed width. */
.meter--sm i{{width:{RC['progressTrack']['segmentWidth']}px;flex:none;
  height:{RC['progressTrack']['heightSm']}px}}
/* --lg: standalone in its own card — bars STRETCH to fill the card, matching
   the owner's reference, which shows the bars spanning the full frame. */
.meter--lg{{display:flex;width:100%}}
.meter--lg i{{flex:1;height:{RC['progressTrack']['heightLg']}px}}
.meter__off{{background:{RC['progressTrack']['trackEmpty']}}}
.rowmeter{{display:flex;align-items:center;gap:8px}}
.rowmeter__n{{font-size:13px;font-variation-settings:'wght' 700}}

.cta{{display:flex;align-items:center;justify-content:center;gap:9px;width:100%;
  height:{LAY['ctaHeight']}px;border:0;border-radius:{R['full']}px;
  background:{G['ink']['css']};color:{C['text']['inverse']};font:inherit;font-size:16px;
  font-variation-settings:'wght' 600;cursor:pointer;box-shadow:{EL['dock']['css']};
  margin-top:18px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
/* ⚠ Chiclets are radius 8, NOT pills [INSPECTOR]. A pill reads as a filter
   you switch off again; a soft rectangle reads as a tile you pick from a set.
   Both states carry effects.chiclet — selection is depth, never hue. */
.chip{{height:{LAY['chipHeight']}px;border-radius:{R['xs']}px;border:0;padding:0 13px;
  font:inherit;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;
  transition:box-shadow .18s,transform .18s}}
.chip--on{{background:{RC['chipSelected']['background']};color:{C['text']['primary']};
  font-variation-settings:'wght' 600;box-shadow:{FX['chicletSelected']['css']}}}
.chip--off{{background:{RC['chipUnselected']['background']};color:{C['text']['tertiary']};
  box-shadow:{FX['chiclet']['css']}}}
.chip:not([disabled]):active{{transform:scale(.97)}}
.chip[disabled]{{cursor:not-allowed;opacity:.72}}

.note{{font-size:12.5px;line-height:18px;color:{C['text']['tertiary']};margin:12px 4px 0}}

@media (prefers-reduced-motion:reduce){{
  *{{animation-duration:.01ms !important;transition-duration:.01ms !important}}
}}
"""

JS = """
const scrs=[...document.querySelectorAll('.scr')],rail=[...document.querySelectorAll('.rail__i')];
let stack=['root'];
function show(id){
  scrs.forEach(s=>s.toggleAttribute('data-on',s.dataset.scr===id));
  rail.forEach(b=>b.setAttribute('aria-current',String(b.dataset.to===id)));
  const s=scrs.find(x=>x.dataset.scr===id); if(s) s.querySelector('.body').scrollTop=0;
}
document.addEventListener('click',e=>{
  const g=e.target.closest('[data-go]');
  if(g){stack.push(g.dataset.go);show(g.dataset.go);return;}
  const b=e.target.closest('[data-back]');
  if(b){if(stack.length>1)stack.pop();show(stack[stack.length-1]);return;}
  const j=e.target.closest('.rail__i');
  if(j){stack=j.dataset.to==='root'?['root']:['root',j.dataset.to];show(j.dataset.to);return;}
  const t=e.target.closest('.tg');
  if(t){const on=t.classList.toggle('tg--on');t.setAttribute('aria-checked',String(on));}
  const o=e.target.closest('.seg__o');
  if(o){[...o.parentNode.children].forEach(x=>x.classList.remove('seg__o--on'));
    o.classList.add('seg__o--on');}
  const c=e.target.closest('.chip:not([disabled])');
  if(c){[...c.parentNode.children].forEach(x=>{x.classList.remove('chip--on');
    x.classList.add('chip--off');});c.classList.remove('chip--off');c.classList.add('chip--on');}
});
show('root');
""" + FIT_JS + """
/* body already carries 34px of padding, so the stage IS the usable box —
   only a little breathing room is taken off here. */
watchPhoneFit({padY: 16, padX: 16});
"""


def page(title, kicker, rail_items, screens, extra_css="", note_html=""):
    # Every screen has rendered by now, so icon3d() has seen every name this
    # prototype asks for. Say so out loud: a placeholder that ships unnoticed
    # is worse than one that never got drawn.
    if MISSING_ICONS:
        print("  ⚠ placeholder icons (no asset on disk): %s"
              % ", ".join(sorted(MISSING_ICONS)))
        print("    drop <name>.png in design-elements/3d-icons/ and run that "
              "folder's resize snippet; no code change needed.")
    rail = "".join('<button class="rail__i" data-to="%s">%s</button>' % (i, n)
                   for i, n in rail_items)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}{extra_css}</style></head><body>
  <div class="rail">
    <div class="rail__b">{kicker}</div>
    <div class="rail__k">{note_html}</div>
    {rail}
    <p class="rail__n">Colours, radii and shadows are generated from
      <code>src/tokens/design.tokens.js</code> at build time. Chrome is shared with the
      other settings surface via <code>_kit.py</code> so the two cannot drift apart.</p>
  </div>
  <div class="stage">
    <div class="phone">
      <div class="notch"></div>
      {"".join(screens)}
      <div class="hbar"></div>
    </div>
  </div>
<script>{JS}</script>
</body></html>"""
