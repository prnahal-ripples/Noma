#!/usr/bin/env python3
"""
Build docs/features/first-run/first-run-prototype.html

Tappable, visual onboarding + device-setup prototype. One phone, driven by a
controller on the left: position, a jumpable node list, and a button for every
edge state.

    python3 docs/features/first-run/build-prototype.py

THE FLOW IS THE OWNER'S DIAGRAM (2026-08-06), FOLLOWED NODE FOR NODE — MINUS FOUR
NODES THE OWNER CUT THE SAME DAY, PLUS TWO BRANCHES ADDED SINCE. Originally 26
main-line nodes plus one branch (18a, invite family); nodes 19–22 (update check,
install, update complete, taking first reading) were removed entirely, and node
14 (manual Wi-Fi password) followed on 2026-08-18 — 21 main-line nodes remain.
2026-08-19 added two more branches on node 4: 4a (verified) and 5a (the "key
card created" success screen) — see that section's own note for why. 21
main-line nodes + branches 4a, 5a, 18a: 24 in total.
Every screen carries the node number it belongs to; where a node needs two screens
to be truthful — an OS permission dialog sits on top of the app screen that
explains it — both screens carry the same node, so the node count never drifts
from what is actually built.

THE ORDER AS BUILT — node ids are stable, so they no longer ascend. Read down:

  1  get started                    24  ask for location (geofencing)
  2  login with phone               25  ask for notifications
  3  verify                         17  which room is it in? create a home
  4  create profile + email         18  what should we name the device
  5  email verify                  18a  invite family members        (branch)
  6  choose your purifier           23  about the app · 3 slides, privacy first
  7  unwrap the filter              26  home
  8  plug in and switch on
  9  wi-fi light blinking     ── REMOVED 2026-08-06: nodes 19–22 ──
 10  switch on bluetooth      (check for update, update device,
 11  scan · select · pair      update complete, taking first reading)
 12  auto-fetch wi-fi
 13  select wi-fi  (fallback)
 14  wi-fi password (fallback)
 15  setting up · carousel
 16  connected

WHAT THIS REPLACED (2026-08-06). The previous build ran Arrival → Household →
Device with a standalone DPDP consent pair, an analytics opt-in, "create your
home" up front, a five-person household counter before any device existed, and no
email, no device-choice and no location ask. All of that was wrong against the
diagram and is gone. Consequences worth knowing:
  · The home is now created at node 17, as a side effect of naming the room.
  · The household shrank from 11 screens to a 2-screen branch off node 18.
  · There is no standalone consent screen. DPDP notice now rides on node 4, the
    point where the first non-phone personal data is collected. See PRD §5.1 —
    this is the one place the diagram and the Act may need a referee.
  · Node 6 is a purifier-only choice — three horizontal cards, stacked, one for
    each SKU in src/hardware/devices.json (`HW-PUR-200`/`500`/`MAX`). A first
    pass at this node offered four device CATEGORIES (purifier, camera, lock,
    vacuum), three of them unbuyable; the owner narrowed it 2026-08-06 to what
    the product actually is — one purifier line, three sizes. Camera, lock and
    vacuum appear nowhere in this flow.

NODES 19–22 REMOVED (owner, 2026-08-06, third pass). The whole firmware-update /
first-reading sequence — check for update, install, update complete, taking a
first reading — is gone. Node 18a's disclosure screen ("what Lakshmi will see")
is also gone; picking a contact now sends the invite directly. Two open questions
this leaves, noted where the old screens used to be: nothing in the flow takes a
first reading anymore (Home just shows a number with no setup step that earned
it), and firmware update has no path at all, in this flow or any other.

PERMISSIONS MOVED FORWARD (owner, 2026-08-06, fourth pass). Nodes 24 (location /
geofencing) and 25 (notifications) now run IMMEDIATELY AFTER node 16 (connected),
before the home is created at 17. And node 23 (the three about-the-app slides)
now lands straight on Home. So the tail is:

    16 connected → 24 location → 25 notifications
       → 17 create home → 18 name device → 18a invite → 23 about ×3 → 26 home

What this buys: both OS prompts fire in one block, at the moment the device has
just visibly worked, instead of being separated by four naming/household screens.
What it costs, and it is worth watching: the two permission asks now sit between
"it connected" and any use of the product, so they arrive before the user has a
named room, a named device, or a reading — node 24's pitch ("start cleaning
before you get home") is being made about a device with no room yet. If either
prompt's grant rate drops, this ordering is the first thing to suspect.

VISUAL DIRECTION (owner, 2026-08-05):
  · Background: gradients.canvas — white falling to warm sand dust (#DDDCD8).
    ⚠ CORRECTED 2026-08-19. This said "radial gradient, #FFFFFF at top right
    falling to #A4A4A4 bottom left" and the `:root` matched it, but the
    previous first run (build-onboarding.py) and build-flow.py's re-skin had
    both been on gradients.canvas for some time — this file was the only one
    still painting the cool radial. Now read from the token, so the three
    renderings of the same screens cannot disagree about the ground again.
  · Cards / fields: near-white, 8%-opacity drop shadow
  · CTA: black, fully rounded (pill)
  · No accent green anywhere in this file

Household follows the Apple Home / Google Home model — an invitation sent to a
contact, accepted on their own device. The hand-the-phone-over step was removed
2026-08-05 and must not come back.
"""
import base64, html, importlib.util, json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT  = ROOT / "docs/features/first-run/first-run-prototype.html"


def _load_builder(name):
    """Import a sibling builder by path — the filenames have hyphens, so they
    are not importable as modules. Does not run its build()."""
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), pathlib.Path(__file__).with_name(name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# NODES 1-5 COME FROM build-auth.py — see the ACCOUNT section below. That file
# owns the sheet's markup, its CSS and its token reads; nothing about the
# sign-in is restated here (CLAUDE.md rule 2). This is also the only part of
# this file that is token-driven: everything else predates that rule and
# carries raw hex in `:root`, which build-flow.py re-skins.
AUTH = _load_builder("build-auth")
FDIR = ROOT / "src/fonts/google-sans-flex/static"
b64  = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = {k: b64(FDIR / v) for k, v in {
    "REG": "GoogleSansFlex_24pt-Regular.ttf",
    "MED": "GoogleSansFlex_24pt-Medium.ttf",
    "BLD": "GoogleSansFlex_24pt-Bold.ttf"}.items()}
E = lambda s: html.escape(str(s), quote=False)
GO = lambda g: f' data-go="{E(g)}"' if g else ''

# ── node 4's master key ─────────────────────────────────────────────────────
# The card artwork is a supplied PNG, used AS THE BASE and written over — the
# frame, bevel, grain, divider and key glyph are all in the image, and nothing
# here redraws them. Only the four live things sit on top: the avatar, the
# serif initial, the name and the email.
#
# Instrument Serif is loaded for ONE glyph, the initial. It is not a second
# body face and must not become one; every other character on the card is
# Google Sans Flex. Licence: SIL OFL, vendored beside the font.
KEYCARD = ROOT / "design-elements/brand/web/key-card.webp"
SERIF   = ROOT / "src/fonts/instrument-serif/InstrumentSerif-Regular.ttf"
KEYCARD_B64 = b64(KEYCARD)

# ── the key card, REBUILT 2026-08-20 on owner artwork ──────────────────────
# Five colourways plus the two wallet-sleeve layers. `Card base.png` is
# byte-identical to `Card 1.png`, so only 1-5 are vendored.
#
# ⚠ FIVE FILES, NOT ONE PLUS A CSS TINT — and that was a measured decision.
# The five colourways are the SAME artwork: their luminance channels differ by
# 0.2/255, i.e. the brushed-metal pattern is pixel-identical and only the
# chroma moves. So a single image under `mix-blend-mode:color` was tried first
# and reproduces each variant to within 2-6/255 per channel. Close, but not the
# owner's file — and this project's pattern is to ship supplied artwork rather
# than an approximation of it. The real files at 528px (2x their 264px render,
# quality 70) cost 253 KB for all five, which is 5x lighter than the naive
# 720px encode and cheap enough not to need the trick.
CARD_B64 = {n: b64(ROOT / f"design-elements/brand/keycard/web/card-{n}.webp")
            for n in range(1, 6)}
SLEEVE_B64 = {k: b64(ROOT / f"design-elements/brand/keycard/web/sleeve-{k}.webp")
              for k in ("back", "front")}

# The card artwork's own geometry, MEASURED off the alpha channel (longest
# contiguous run >= 245) — the PNG is a soft outer glow around a solid face, so
# anything overlaid has to use the FACE, not the file's box. Same discipline as
# recipes.cardShimmer.face, which this supersedes for the new art.
#   card-1.png 1180x1564  face x 96..1082 (987)  y 56..1427 (1372)
CARD_FACE = {"left": 8.14, "right": 8.22, "top": 3.58, "bottom": 8.70,
             "radiusX": 12.87, "radiusY": 9.26}
CARD_AR = "1180/1564"      # the new art is squarer than the old 1384/1907
SERIF_B64   = b64(SERIF)

# The resident's key (node 18a) — owner-supplied artwork, used AS IS: no name,
# no initials, nothing live on it. The master key is personal; this one is
# deliberately generic, which is what makes it sendable.
RESKEY_B64 = b64(ROOT / "design-elements/brand/web/resident-key.webp")

# The three SKU renders (design-elements/renders/) — real product photography
# replacing the CSS-drawn purifier everywhere a purifier is depicted.
RENDERS_B64 = {sku: b64(ROOT / f"design-elements/renders/web/air-pro-{sku}.webp")
               for sku in ("200", "500", "max")}

# Nodes 10-11's Bluetooth scene — owner-supplied iPhone Bluetooth-settings
# mock (2026-08-18), real alpha, bottom fade baked in. Composed per the
# owner's reference: purifier upper-left, this phone lower-right, overlapping.
BTPHONE_B64 = b64(ROOT / "design-elements/renders/web/bt-phone.webp")

# The two large page glyphs (owner-supplied SVG, 2026-08-18). Embedded as
# data URIs rather than inlined markup: both carry Figma filter/gradient ids
# (`filter0_di_…`, `paint0_linear_…`) which would collide the moment two
# screens sat in the DOM together — and with the seamless swap below, they now
# always do during a transition.
GLYPH_B64 = {n: base64.b64encode((ROOT / f"design-elements/engraved-icons/{n}.svg")
                                 .read_bytes()).decode()
             for n in ("bluetooth", "wifi", "check-circle", "notifications-unread")}


# ── the SMALL icon register — Lucide, ISC (owner, 2026-08-19) ───────────────
# "these icons will be used for smaller 24x24 px icons only, only smaller than
# 24 icons. don't change any other larger icons and engraved or 3d icons."
#
# Inlined as markup rather than data-URI'd, unlike GLYPH_B64 above, and the
# difference is deliberate: at this size a glyph has to inherit `color` from
# whatever it sits in — a row, a dark CTA, a disabled control — and a
# background-image cannot. The engraved 77px glyphs have no such need, which is
# why they stay background images.
#
# See design-elements/icons/README.md for the register boundary: what this set
# owns and what it must never touch (brand marks, engraved, 3D, artwork).
def _icons():
    import re
    d = ROOT / "design-elements/icons"
    out = {}
    for f in sorted(d.glob("*.svg")):
        raw = f.read_text(encoding="utf-8")
        inner = re.sub(r"^.*?>", "", raw, count=1, flags=re.S).rsplit("</svg>", 1)[0]
        out[f.stem] = re.sub(r"\s+", " ", inner).strip()
    if not out:
        raise SystemExit("build-prototype.py: design-elements/icons/ is empty — "
                         "the small icon register is vendored, not generated.")
    return out


ICONS = _icons()


def icon(name, px=18, cls="", sw=2):
    """One small icon, at `px`, inheriting `color`.

    ⚠ RAISES on an unknown name. A missing icon that renders an empty box is
    the kind of thing that ships; a build that stops is not. Add the .svg to
    design-elements/icons/ rather than pasting path data here."""
    if name not in ICONS:
        raise SystemExit("build-prototype.py: no icon %r. Have: %s"
                         % (name, ", ".join(sorted(ICONS))))
    return ('<svg class="ic%s" width="%d" height="%d" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '%s</svg>' % ((" " + cls) if cls else "", px, px, sw, ICONS[name]))


# ── node 24's geofencing illustration (owner-supplied SVG, 2026-08-19) ──────
# Replaces a CSS-drawn stand-in. Consumed in TWO pieces, for the same reason
# GLYPH_B64 exists (ids collide) plus one more: the green "you" dot has to
# ANIMATE across the dashed boundary, which a background-image cannot do. So
# the dot is stripped out of the plate and re-drawn as a positioned element.
#
# ⚠ The geometry below is PARSED from the file, never transcribed — the
# overlay dot and the plate therefore cannot drift apart, and a re-export with
# a moved dot moves the animation with it. The strip asserts, so a re-export
# that changes the dot's markup fails the build instead of quietly shipping
# two dots. See design-elements/illustrations/README.md.
def _geofence():
    import re
    src = (ROOT / "design-elements/illustrations/geofencing.svg").read_text(encoding="utf-8")
    box = float(re.search(r'viewBox="0 0 ([\d.]+)', src).group(1))
    dot = re.search(r'<g filter="url\(#filter1_d[^"]*\)">\s*'
                    r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"'
                    r'[^>]*fill="(#[0-9A-Fa-f]{6})"\s*/>\s*</g>', src)
    if not dot:
        raise SystemExit(
            "build-prototype.py: geofencing.svg's green dot no longer matches the "
            "expected markup. It is stripped from the plate and re-drawn as an "
            "animated overlay — fix this parse rather than dropping it, or the "
            "screen will render two dots.")
    cx, cy, r, fill = (float(dot.group(1)), float(dot.group(2)),
                       float(dot.group(3)), dot.group(4))
    ring = re.search(r'<circle cx="[\d.]+" cy="([\d.]+)" r="(80[\d.]*)"', src)
    ccx = ccy = float(ring.group(1))
    plate = src.replace(dot.group(0), "")
    # How far to travel to cross the boundary: from the dot's resting distance
    # to comfortably inside the ring, along the line to the centre. Expressed
    # as a multiple of the dot's OWN size, because `transform:translate(%)`
    # resolves against the element, not its container — which is what lets the
    # whole thing scale with the card.
    import math
    dx, dy = ccx - cx, ccy - cy
    dist = math.hypot(dx, dy)
    travel = dist - float(ring.group(2)) + 22.0      # cross it, then some
    d = 2 * r
    return {
        "plate": base64.b64encode(plate.encode()).decode(),
        "left": 100 * (cx - r) / box, "top": 100 * (cy - r) / box,
        "size": 100 * d / box, "fill": fill,
        "tx": 100 * (dx / dist) * travel / d,
        "ty": 100 * (dy / dist) * travel / d,
    }


GEO = _geofence()

# ───────────────────────────────────────────── chrome
def bar():
    return ('<div class="sbar"><span>9:41</span><span class="sbar__r">'
            '<i class="sig"></i><i class="wf"></i><i class="bt"></i></span></div>')

# THE BACK CHEVRON — one definition, used by the page nav AND the sheet.
# Owner, 2026-08-19: "use the previous button style that we have. We had
# already locked it... refer to the mobile OTP bottom sheet." The sheet's
# button was the locked one, so the page nav now renders the same glyph in the
# same container (see the `.nb` block in the token-driven CSS at the end of
# this file, which reads recipes.buttonIcon). Two back buttons that merely
# looked similar is how they drifted apart in the first place.
BACK_SVG = icon("chevron-left", 19, sw=2)


def nav(back=None, title="", close=None):
    l = (f'<button class="nb"{GO(back)} aria-label="Back">{BACK_SVG}</button>'
         if back else '<span class="nb"></span>')
    r = (f'<button class="nb"{GO(close)}>' + icon("x", 18) + '</button>'
         if close else '<span class="nb"></span>')
    return f'<div class="nav">{l}<span class="nav__t">{E(title)}</span>{r}</div>'

# ───────────────────────────────────────────── visuals (CSS-drawn, monochrome)
def viz(inner, h=250):
    return f'<div class="viz" style="height:{h}px">{inner}</div>'

def v_room(h=430):
    return (f'<div class="hero" style="height:{h}px">'
            '<span class="hero__b b1"></span><span class="hero__b b2"></span>'
            '<span class="hero__b b3"></span></div>')

def v_purifier(h=250, ring="idle"):
    return viz(f'<div class="pur pur--{ring}">'
               '<span class="pur__ring"></span><span class="pur__grill"></span>'
               '<span class="pur__grill"></span><span class="pur__grill"></span></div>', h)

def v_plug(h=230):
    """Node 8 — ANIMATED as of 2026-08-18 (owner): the socket's rocker flips
    on, then the power light blooms awake on the device, on a loop. Socket and
    cord stay drawn; the body is the real render, with the LED glow overlaid
    where the render's own light sits."""
    return viz('<div class="scene scene--pwr"><span class="sock"><i></i><i></i>'
               '<span class="rocker"></span></span>'
               '<span class="cord"></span>'
               '<span class="pwrwrap">' + hero("rnd--sm") +
               '<span class="pwrled"></span></span></div>', h)

def v_ring(h=230, pct=70):
    return viz(f'<div class="ringw"><div class="ringa" style="--p:{pct}"></div>'
               '<span class="ringc"></span></div>', h)

def v_phone_near(h=220):
    """Nodes 10-11 — the real render upper-left, and the phone's Bluetooth
    settings lower-right with the toggle FLIPPING ON, on a loop.

    REDRAWN 2026-08-18: the supplied PNG was a flat screenshot and could not
    animate, and the owner asked to see the switch actually turn on. This is
    the same screen rebuilt in markup so the toggle moves and the rows below
    it arrive once Bluetooth is on. It depicts iOS, so it carries iOS's
    colours (#007AFF, #34C759) rather than NOMA's palette — the same licence
    dialog() already takes for the OS's own prompts. Nothing here is a NOMA
    surface."""
    return viz('<div class="btsc">' + hero("btsc__pur") +
               '<span class="btph">'
               '<span class="btph__nav"><b>Settings</b><em>Bluetooth</em></span>'
               '<span class="btph__row"><span>Bluetooth</span>'
               '<span class="btph__tog"><i></i></span></span>'
               '<span class="btph__cap">Now discoverable as “R’s iPhone”.</span>'
               '<span class="btph__lab">MY DEVICES</span>'
               '<span class="btph__dev"><span>HandsFreeLink</span><em>Not Connected</em></span>'
               '<span class="btph__dev"><span>My Apple Watch</span><em>Connected</em></span>'
               '</span></div>', h)

def v_tick(h=150):
    return viz('<span class="tick"></span>', h)

def v_wifi(h=150):
    return viz('<span class="wifiv"><i></i><i></i><i></i><b></b></span>', h)

def v_bell(h=200):
    """Node 25 — REBUILT 2026-08-18 (owner: a better-looking bell, rings coming
    out of it, and the red dot). The bell is drawn from a dome, a rim and a
    clapper rather than the old rounded-rectangle stand-in; three concentric
    rings pulse outward on a loop, and the badge is `status.negative` — the
    palette's only non-green hue, and a notification count is what it is for."""
    return viz('<span class="bellw">'
               '<i class="bellw__r"></i><i class="bellw__r"></i><i class="bellw__r"></i>'
               '<span class="bell2"><i class="gly gly--bell"></i></span>'
               '</span>', h)


def _v_bell_drawn(h=200):
    """RETIRED 2026-08-18: the hand-drawn bell, replaced by the engraved glyph.
    Kept for one reason — the rings, the swing and the badge geometry were tuned
    against this shape, and if the glyph is ever swapped again this is what they
    were tuned to."""
    return viz('<span class="bellw">'
               '<i class="bellw__r"></i><i class="bellw__r"></i><i class="bellw__r"></i>'
               '<span class="bell2">'
               '<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" '
               'stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">'
               '<circle cx="50" cy="12" r="4.6" fill="#fff"/>'
               '<path d="M50 17c-14 0-23 11-23 25 0 13-3 20-8 25h62c-5-5-8-12-8-25 '
               '0-14-9-25-23-25Z" fill="#fff"/>'
               '<path d="M41 67a9 9 0 0 0 18 0" fill="#fff"/>'
               '</svg>'
               '<i class="bell2__d"></i></span></span>', h)

def v_q(h=180):
    return viz('<div class="scene sceneq">'
               '<div class="pur pur--sm pur--dim"><span class="pur__ring"></span></div>'
               '<span class="qmark">?</span></div>', h)

# v_clock() and v_updating() lived here until 2026-08-06. They were only ever used by
# nodes 19-22 (the firmware-update path and its timeout state), which the owner removed.
# Their CSS (.clock, .pur__arrow) is likewise dead — kept in the stylesheet only because
# it costs nothing and those nodes may come back if firmware update needs a home.

def v_filter(h=210):
    """Node 7 — ANIMATED as of 2026-08-18 (owner): the polybag slides off the
    cartridge and drifts away, on a loop. The bag is its own element now (it
    used to be a dashed ::after on the cartridge) precisely so it can leave.
    The cartridge stays drawn — no filter render exists; the body is the real
    render."""
    return viz('<div class="xfil">'
               '<span class="xfil__wrap">'
               '<span class="filt__f filt__f--out"><i></i><i></i><i></i><i></i></span>'
               '<span class="xbag"></span></span>'
               '<span class="xfil__a"></span>'
               + hero("xfil__pur") +
               '</div>', h)

def v_people(h=180, n=2, pend=0):
    a = "".join('<span class="fav"></span>' for _ in range(n))
    p = "".join('<span class="fav fav--p"></span>' for _ in range(pend))
    return viz(f'<div class="favs">{a}{p}</div>', h)

def v_shield(h=180):
    return viz('<span class="shield"></span>', h)

def v_home_ill(h=200):
    return viz('<span class="hicon"><i></i><i></i></span>', h)

def v_agent(h=200):
    return viz('<span class="orb"><i></i></span>', h)

def v_mail(h=190):
    return viz('<span class="mail"></span>', h)

def v_geo(h=210):
    """Node 24. The house, the dashed boundary and the soft glow are the
    owner's SVG (2026-08-19), painted as one plate; only the "you" dot is a
    separate element, because it has to travel across the boundary. Same
    behaviour the CSS stand-in had — owner: "keep the animation the same of
    the circle going in and out of the line"."""
    return viz('<span class="geo"><u></u></span>', h)

def v_pairing(h=210):
    return viz('<div class="scene"><span class="link"><i></i><i></i><i></i></span>'
               '<div class="pur pur--pulse pur--sm"><span class="pur__ring"></span></div></div>', h)

# ───────────────────────────────────────────── content blocks
# `grad` is the title gradient (tokens.titleGradient) — owner, 2026-08-20:
# every header carries it now, so it lives on the helper rather than on 30
# call sites. `.grad` is paint only; size stays with whatever screen it is on.
t1   = lambda x: f'<h1 class="t1 grad">{E(x)}</h1>'
t2   = lambda x: f'<h2 class="t2">{E(x)}</h2>'
bd   = lambda x: f'<p class="bd">{E(x)}</p>'
lab  = lambda x: f'<p class="lab">{E(x)}</p>'
foot = lambda x: f'<p class="foot">{E(x)}</p>'
gap  = lambda: '<div class="gap"></div>'

def field(ph="", v="", cnt="", state="", pw=False, label="", bind=""):
    """A REAL input as of 2026-08-17 (owner: the flow "needs to be
    interactive"). It used to be a span with a fake caret, which looked right
    and could not be typed into. `bind` names the value for wireProfile, so
    node 4's card can follow what is typed underneath it."""
    l = lab(label) if label else ""
    c = f'<span class="fc">{E(cnt)}</span>' if cnt else ""
    b = f' data-bind="{E(bind)}"' if bind else ""
    return (f'{l}<div class="fld {state}">'
            f'<input class="fi" type="{"password" if pw else "text"}" '
            f'value="{E(v)}" placeholder="{E(ph)}"{b}>{c}</div>')

def mobile_field(mobile="98765 43210", verified=False):
    """Node 4's mobile-number row — new 2026-08-19 (owner), replacing the
    email field the profile page used to have. A +91 prefix like the sheet's
    old phone step, plus an inline action on the right: a "Verify" pill while
    unverified, a plain check once it is.

    ⚠ The pill NAVIGATES rather than opening in place — `data-go="A5"`, the
    same mechanism every other button in this file uses, not a bespoke
    JS overlay-toggle. A5 is a fully separate screen (`profile_page()` plus
    the sheet baked into its HTML, exactly the shape node 5 already had for
    the old email flow) — see the note on S("A5", ...). That keeps this
    screen inside the file's one real convention: every screen is a static
    snapshot reached by `data-go`, not two screens quietly pretending to be
    one DOM the way build-auth.py's own sheet is."""
    action = (
        '<span class="fverify fverify--ok" aria-label="Verified">'
        + icon("check", 17, sw=2.4) +
        '</span>'
        if verified else
        f'<button class="fverify" type="button"{GO("A5")}>Verify</button>'
    )
    return (
        f'{lab("MOBILE NUMBER")}'
        f'<div class="fld fld--verify{" fld--verified" if verified else ""}">'
        '<span class="fld__cc">+91</span>'
        f'<input class="fi" type="tel" inputmode="numeric" maxlength="10" '
        f'value="{E(mobile)}" placeholder="Enter number" data-bind="mobile"'
        f'{" readonly" if verified else ""}>'
        f'{action}</div>')

def otp(filled=0, bad=False):
    return ('<div class="otp' + (' bad' if bad else '') + '">' + "".join(
        f'<span class="otpc">' + ('<i></i>' if i < filled else '') + '</span>'
        for i in range(6)) + '</div>')

def chips(items, sel=(), dim=(), go=None, label=""):
    l = lab(label) if label else ""
    out = []
    for i, it in enumerate(items):
        cls = "chip" + (" on" if i in sel else "") + (" dim" if i in dim else "")
        out.append(f'<button class="{cls}"{GO(go)}>{E(it)}</button>')
    return f'{l}<div class="chips">' + "".join(out) + '</div>'

def rows(items, ctl="none", on=(), go=None, icons=True, label=""):
    l = lab(label) if label else ""
    out = []
    for i, it in enumerate(items):
        t, s = (it if isinstance(it, (list, tuple)) else (it, ""))
        c = {"radio": f'<span class="rad{" on" if i in on else ""}"></span>',
             "check": f'<span class="chk{" on" if i in on else ""}"></span>',
             "toggle": f'<span class="tog{" on" if i in on else ""}"></span>',
             "chev": icon("chevron-right", 17, cls="ic-chev", sw=2)}.get(ctl, "")
        ic = '<span class="ri"></span>' if icons and ctl in ("chev", "toggle", "none") else ""
        sub = f'<span class="rs">{E(s)}</span>' if s else ""
        tag = "button" if go else "div"
        out.append(f'<{tag} class="row"{GO(go)}>{ic}<span class="rt">{E(t)}{sub}</span>{c}</{tag}>')
    return f'{l}<div class="rows">' + "".join(out) + '</div>'

def bullets(items, label=""):
    l = lab(label) if label else ""
    return f'{l}<div class="bl">' + "".join(
        f'<div class="bli"><span class="bln">{i+1}</span><span>{E(x)}</span></div>'
        for i, x in enumerate(items)) + '</div>'

def needs(items):
    return '<div class="needs">' + "".join(
        f'<div class="need"><span class="need__i i{i}"></span><span>{E(x)}</span></div>'
        for i, x in enumerate(items)) + '</div>'

def scanner():
    return ('<div class="scan"><span class="scan__c c1"></span><span class="scan__c c2"></span>'
            '<span class="scan__c c3"></span><span class="scan__c c4"></span>'
            '<span class="scan__qr"><i></i><i></i><i></i></span></div>')

def method(icon, title, body):
    return (f'<div class="mth"><span class="mth__i mth__i--{icon}"></span>'
            f'<span class="mth__t"><b>{E(title)}</b><span>{E(body)}</span></span></div>')

def figures(n, maxn=5):
    out = []
    for i in range(n):
        out.append(f'<span class="fig{" fig--you" if i == 0 else ""}"><i></i><b></b></span>')
    return f'<div class="figs" data-n="{n}">' + "".join(out) + '</div>'

def counter(val=1, mn=1, mx=5, label="People", sub="Everyone gets their own phone"):
    return (f'<div class="cnt" data-cmp="counter" data-min="{mn}" data-max="{mx}" data-val="{val}">'
            f'<div class="cnt__figs">{figures(val, mx)}</div>'
            '<div class="cnt__row">'
            f'<button class="stp" data-step="-1">' + icon("minus", 17) + '</button>'
            f'<span class="cnt__n">{val}</span>'
            f'<button class="stp" data-step="1">' + icon("plus", 17) + '</button>'
            '</div>'
            f'<p class="cnt__l">{E(label)}</p><p class="cnt__s">{E(sub)}</p></div>')

def purcard(name, sub, spec, sel=False, go=None, sku="200"):
    """Node 6 — 'choose device type', narrowed to 'choose your purifier'. One of the
    three src/hardware/devices.json purifier SKUs (HW-PUR-200/500/MAX), as a
    horizontal card matching `devcard`'s shape, stacked vertically rather than in a
    grid — there is one product line, not four device categories.
    Thumbnails are the REAL RENDERS as of 2026-08-17 (owner) — the three SKUs
    are genuinely different shapes now, which is the at-a-glance signal the
    2026-08-12 monochrome rule had cost and the hue tints only approximated."""
    cls = "pcard" + (" on" if sel else "")
    # The chosen tile is where the carry starts — whether you tap a card or
    # just press Continue on the default selection.
    mark = ' data-hero data-carry="pur"' if sel else ''
    return (f'<button class="{cls}"{GO(go)} data-sku="{sku}">'
            f'<span class="pcard__v"><i class="rnd rnd--{sku} pcard__r"{mark}></i></span>'
            f'<span class="pcard__t"><b>{E(name)}</b><span>{E(sub)}</span>'
            f'<em>{E(spec)}</em></span>'
            + icon("chevron-right", 17, cls="ic-chev", sw=2) + '</button>')

def mini(kind):
    """A miniature app screenshot for the node-15 carousel. CSS-drawn, monochrome,
    same visual language as the real screens — all four variants share the status bar,
    greeting and title so they read as four shots of one app rather than four graphics."""
    sb = ('<div class="mn__sb"><b>9:41</b>'
          '<span class="mn__sr"><i></i><i></i><i></i></span></div>')
    hd = ('<p class="mn__g">Good evening, Ruhaan</p>'
          '<div class="mn__h"><b>My Home</b>'
          '<span class="mn__o"></span><span class="mn__o"></span></div>')
    chip = lambda t, on=False: f'<span class="mn__c{" on" if on else ""}">{E(t)}</span>'

    if kind == "rooms":
        body = ('<div class="mn__cs">' + chip("All calm") + chip("6 µg/m³ · clean")
                + chip("24°C inside") + '</div>'
                '<div class="mn__cs">' + chip("All rooms", True) + chip("Living 22")
                + chip("Bedroom 19") + chip("Kitchen") + '</div>'
                '<div class="mn__map">'
                '<span class="mn__tl t1"></span><span class="mn__tl t2"></span>'
                '<span class="mn__tl t3"></span><span class="mn__tl t4"></span>'
                '<span class="mn__pn k p1">22</span><span class="mn__pn p2">19</span>'
                '<span class="mn__pn p3">97</span><span class="mn__pn p4">41</span>'
                '</div>')
    elif kind == "agent":
        body = ('<div class="mn__cs">' + chip("Bedroom") + chip("Auto") + '</div>'
                '<div class="mn__bd">'
                '<div class="mn__big">6<em>µg/m³ · RIGHT NOW</em></div>'
                '<div class="mn__cd"><i></i><i></i></div>'
                '<div class="mn__cd sm"><i></i></div></div>')
    elif kind == "people":
        body = ('<div class="mn__cs">' + chip("Everyone", True) + chip("Invited") + '</div>'
                '<div class="mn__bd"><div class="mn__pp">'
                '<span></span><span></span><span></span></div>'
                '<div class="mn__cd"><i></i><i></i></div>'
                '<div class="mn__cd"><i></i><i></i></div>'
                '<div class="mn__cd sm"><i></i></div></div>')
    else:  # privacy
        body = ('<div class="mn__cs">' + chip("On this device") + chip("Private") + '</div>'
                '<div class="mn__bd"><div class="mn__sh"></div>'
                '<div class="mn__cd"><i></i><i></i></div>'
                '<div class="mn__cd sm"><i></i></div></div>')
    return f'<div class="mn">{sb}{hd}{body}</div>'


def carousel(slides, interval=2200):
    """Node 15 — an auto-advancing feature carousel over the Wi-Fi join wait.
    slides: [(headline, screenshot_html)].

    Crossfade only, `standard` easing: this sits on top of a progress bar on an
    ambient surface, so motion gate 4 applies — no spring, no slide-in bounce.
    Auto-advance is disabled entirely under prefers-reduced-motion (gate 2), and the
    dots are real buttons so the carousel is drivable by hand either way."""
    ss, ds = [], []
    for i, (head, shot) in enumerate(slides):
        on = " on" if i == 0 else ""
        ss.append(f'<div class="car__s{on}" data-i="{i}">'
                  f'<h2 class="car__h">{E(head)}</h2>'
                  f'<div class="car__shot">{shot}</div></div>')
        ds.append(f'<button class="car__d{on}" data-i="{i}" '
                  f'aria-label="Feature {i + 1}"></button>')
    return (f'<div class="car" data-cmp="carousel" data-interval="{interval}">'
            f'<div class="car__w">{"".join(ss)}</div>'
            f'<div class="car__ds">{"".join(ds)}</div></div>')


# ═══════════════════════════════════════════════════════════════════════════
# INTERACTIONS (owner, 2026-08-06). The flow was correct and emotionally flat.
# These are the moments where it should feel like arriving somewhere rather than
# completing a form. All are discrete moments, so spring is not just allowed but
# correct — `.claude/rules/motion.md` opens with "playful and springy on discrete
# moments, still on ambient ones". Every one of them:
#   · works by TAP as well as by drag/hold — the gesture is the delight, never the
#     only way through. A prototype that can only be advanced by dragging is a
#     prototype that excludes switch and keyboard users.
#   · is a <button> where it is the primary action, so Enter/Space work.
#   · collapses to an instant state change under prefers-reduced-motion (gate 2).
# ═══════════════════════════════════════════════════════════════════════════

def doorway(title, sub, go="next"):
    """Node 1 — built to the owner's reference at measured positions.

    THE CORRIDOR IS ONE SHARED-VERTEX SVG. Earlier passes composed it from
    CSS-transformed <span>s; separately rasterised planes cannot be made to meet,
    so the joins showed hairlines and the door read as floating in front of the
    wall. Here every surface is a polygon in one 390x844 viewBox and adjacent
    surfaces share their corner coordinates, so a gap is not expressible:

        aperture   128,158 → 262,394        (the four points every plane meets at)
        ceiling    0,0    390,0    262,158  128,158
        left wall  0,0    128,158  128,394  0,844
        right wall 390,0  262,158  262,394  390,844
        floor      0,844  128,394  262,394  390,844

    The bottom corners belong to the WALLS, not the floor — that is what gives the
    reference its bright central path with grey outer corners.

    LIGHT COMES FROM BEHIND THE DOOR. There is no dark drop shadow anywhere near
    it: a dark shadow says the space beyond is dark, which is the opposite of the
    story. The door is haloed in white with the faintest green cast, the floor
    pools with spill light, and both brighten with --p as the leaf cracks open.

    Positions measured off the reference: door 18.7%→46.7%, wordmark 69.5%, body
    75.9%, slider 85.1%→91.4%, 20px side margins. Copy and slider sit absolutely
    over the scene, because the corridor floor runs behind the text to the bottom."""
    return (f'<div class="en" data-cmp="door" data-go="{E(go)}">'
            '<div class="en__scene"><div class="en__world">'
            '<svg class="en__cor" viewBox="0 0 390 844" preserveAspectRatio="none">'
            '<defs>'
            '<linearGradient id="enL" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#D9D8D5"/><stop offset="1" stop-color="#F2F1EF"/>'
            '</linearGradient>'
            '<linearGradient id="enR" x1="1" y1="0" x2="0" y2="0">'
            '<stop offset="0" stop-color="#D9D8D5"/><stop offset="1" stop-color="#F2F1EF"/>'
            '</linearGradient>'
            '<linearGradient id="enC" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#EBEAE8"/><stop offset="1" stop-color="#F7F6F4"/>'
            '</linearGradient>'
            '<linearGradient id="enF" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#FCFCFB"/>'
            '<stop offset="1" stop-color="#F1F0EE"/></linearGradient>'
            '</defs>'
            '<polygon fill="url(#enC)" points="0,0 390,0 262,158 128,158"/>'
            '<polygon fill="url(#enL)" points="0,0 128,158 128,394 0,844"/>'
            '<polygon fill="url(#enR)" points="390,0 262,158 262,394 390,844"/>'
            '<polygon fill="url(#enF)" points="0,844 128,394 262,394 390,844"/>'
            '<rect x="119" y="149" width="152" height="254" rx="2" fill="#EFEEEC"/>'
            '<rect x="128" y="158" width="134" height="236" fill="#FFFFFF"/>'
            '</svg>'
            # light spilling out of the doorway — white, barely green, never dark
            '<span class="en__pool"></span>'
            '<span class="en__halo"></span>'
            '<div class="en__leaf"><span class="en__panelA"></span>'
            '<span class="en__panelB"></span><span class="en__knob"></span></div>'
            '</div></div>'
            f'<div class="en__copy"><h1 class="en__brand">{E(title)}</h1>'
            f'<p>{E(sub)}</p></div>'
            '<div class="en__slider"><div class="en__track"><span class="en__fill"></span>'
            '<span class="en__label en__label--a">Enter Home</span>'
            '<span class="en__label en__label--b">Entering now&hellip;</span>'
            '<button class="en__pill" aria-label="Slide to enter your home">'
            '<span class="en__arrow"></span></button></div></div>'
            '</div>')


# Six rooms, four pieces of furniture each, in a 2:1 isometric grid. The piece
# COUNT is fixed at four on purpose: morphing needs a slot-for-slot
# correspondence, so bed→sofa→counter is one slot that changes shape rather than
# three objects that appear and disappear. Fields: x/y grid centre, w/d half
# extents, h height in px, t tone 0(light)→1(dark).
ROOMS = [
 ("Bedroom", [
   dict(x=-0.2, y=0.5,  w=1.45, d=0.95, h=17, t=.22),   # bed
   dict(x=-1.5, y=0.5,  w=0.16, d=0.95, h=36, t=.55),   # headboard
   dict(x=-1.4, y=-0.9, w=0.38, d=0.38, h=21, t=.38),   # nightstand
   dict(x=-1.4, y=-0.9, w=0.15, d=0.15, h=46, t=.70)]), # lamp
 ("Living room", [
   dict(x=-0.3, y=1.0,  w=1.55, d=0.52, h=23, t=.22),   # sofa seat
   dict(x=-1.1, y=1.0,  w=0.18, d=0.52, h=41, t=.55),   # sofa back
   dict(x=0.55, y=-0.1, w=0.68, d=0.48, h=13, t=.38),   # coffee table
   dict(x=1.45, y=-0.8, w=0.22, d=1.05, h=31, t=.70)]), # TV unit
 ("Pooja room", [
   dict(x=-1.2, y=0.0,  w=0.48, d=0.95, h=19, t=.22),   # platform
   dict(x=-1.2, y=0.0,  w=0.24, d=0.28, h=45, t=.55),   # idol niche
   dict(x=0.60, y=0.60, w=0.78, d=0.58, h=4,  t=.38),   # mat
   dict(x=0.60, y=-1.0, w=0.13, d=0.13, h=27, t=.70)]), # bell stand
 ("Kitchen", [
   dict(x=-1.2, y=0.2,  w=0.48, d=1.55, h=29, t=.22),   # counter run
   dict(x=-1.2, y=-1.4, w=0.44, d=0.44, h=62, t=.55),   # fridge
   dict(x=-1.2, y=0.85, w=0.34, d=0.38, h=32, t=.38),   # hob
   dict(x=-1.2, y=0.85, w=0.40, d=0.48, h=59, t=.70)]), # hood
 ("Study", [
   dict(x=0.0,  y=-1.0, w=1.35, d=0.48, h=25, t=.22),   # desk
   dict(x=0.35, y=0.10, w=0.12, d=0.40, h=41, t=.55),   # chair back
   dict(x=0.0,  y=0.10, w=0.38, d=0.38, h=21, t=.38),   # chair seat
   dict(x=1.40, y=0.60, w=0.22, d=0.88, h=55, t=.70)]), # shelf
 ("Balcony", [
   dict(x=-0.4, y=0.6,  w=0.44, d=0.44, h=25, t=.22),   # chair
   dict(x=1.60, y=0.0,  w=0.10, d=1.95, h=35, t=.55),   # railing
   dict(x=1.20, y=-1.2, w=0.28, d=0.28, h=23, t=.38),   # planter
   dict(x=1.20, y=-1.2, w=0.17, d=0.17, h=45, t=.70)]), # plant
]


# The isometric projection, in ONE place. `wireRooms()` re-declares the same
# constants in JS because it has to project every frame of the morph; this copy
# exists so the viewBox can be DERIVED from the furniture rather than guessed.
# ⚠ If you change a constant here, change it in wireRooms() too — there is an
# assertion below that the two agree on the resulting box.
RS_PROJ = dict(OX=160, OY=84, IX=26, IY=13, WALL=56, R=2.25)


def _rs_viewbox(rooms, pad=7):
    """The tightest box that contains the shell and EVERY room's furniture.

    ⚠ THIS REPLACED A HARDCODED `9 -25 302 180`, which clipped the tall pieces.
    Measured: the content reaches y=-30.5 (the kitchen hood and fridge, the
    pooja bell stand, the bedroom lamp) while that box started at -25, so the
    top 5.5px of those objects was cut off — which is exactly the "illustrations
    are being cut on top" the owner reported on 2026-09-09. Deriving it means a
    new room with a taller object cannot reintroduce the bug."""
    P = lambda x, y, h: (RS_PROJ["OX"] + (x - y) * RS_PROJ["IX"],
                         RS_PROJ["OY"] + (x + y) * RS_PROJ["IY"] - h)
    R, W = RS_PROJ["R"], RS_PROJ["WALL"]
    pts = [P(-R, -R, 0), P(R, -R, 0), P(R, -R, W), P(-R, -R, W),
           P(-R, R, 0), P(-R, R, W), P(R, R, 0)]
    for _, items in rooms:
        for o in items:
            h = max(0.5, o["h"])
            for sx in (-1, 1):
                for sy in (-1, 1):
                    for hh in (0, h):
                        pts.append(P(o["x"] + sx * o["w"], o["y"] + sy * o["d"], hh))
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    x0, y0 = min(xs) - pad, min(ys) - pad
    return "%g %g %g %g" % (x0, y0, max(xs) - min(xs) + 2 * pad,
                            max(ys) - min(ys) + 2 * pad)


RS_VIEWBOX = _rs_viewbox(ROOMS)


def roomstage(rooms=ROOMS, active=0):
    """Node 17 — the room picker as the centrepiece rather than a row of chips.
    Tapping a room MORPHS the isometric drawing into it: four furniture slots
    interpolate position, footprint, height and tone simultaneously, so the bed
    becomes the sofa becomes the kitchen counter. Nothing pops in or out.

    Why morph and not crossfade: crossfading two drawings says "here is a
    different picture". Morphing says "this is the same room, and you are
    deciding what it is" — which is exactly the decision being made.

    ⚠ REWORKED 2026-09-09 (owner): "it looks very wireframey right now. Use our
    card styles... to kind of add gradients and shadows... make it look more of
    a finished product rather than a Wireframe." The flat `rgba(11,11,11,a)`
    faces are still what carries TONE through the morph — they have to, because
    tone is an interpolated number — but each face now also gets a shared
    gradient overlay and every object gets a contact shadow, so the boxes read
    as lit solids sitting on a floor instead of filled outlines. The gradients
    live in `<defs>` here rather than in JS because they never change; only the
    polygons they fill do.

    ⚠ `xMidYMax` — the drawing is BOTTOM-anchored. The stage grows to fill the
    leftover height (owner: "it needs to be longer and take up more space
    towards the bottom"), and bottom-anchoring means the floor stays put while
    the headroom above it absorbs the slack, rather than the whole room
    drifting up and down as the stage resizes."""
    tabs = "".join(
        f'<button class="rs__t{" on" if i == active else ""}" data-i="{i}">{E(n)}</button>'
        for i, (n, _) in enumerate(rooms))
    # ⚠ The custom-room affordance — owner, 2026-09-09: "there should also be an
    # option to add your own room... your own name of the room." It is a tab
    # rather than a second field, because it is the same decision as the six
    # beside it and belongs in the same row.
    tabs += ('<button class="rs__t rs__t--add" data-add aria-label="Add your own room">'
             + icon("plus", 15, sw=2.2) + '<span>Add a room</span></button>')
    data = json.dumps([items for _, items in rooms])
    return (f'<div class="rs" data-cmp="rooms" data-active="{active}" '
            f"data-rooms='{data}'>"
            f'<div class="rs__bar">{tabs}</div>'
            '<div class="rs__new" data-newwrap hidden>'
            '<input class="fi rs__newin" type="text" data-newin '
            'placeholder="Kids\u2019 room" aria-label="Name your room" '
            'maxlength="24" autocomplete="off">'
            '<button class="rs__newok" data-newok>Add</button>'
            '</div>'
            f'<div class="rs__stage"><svg viewBox="{RS_VIEWBOX}" '
            'preserveAspectRatio="xMidYMax meet">'
            '<defs>'
            # the three face treatments. Shared, so they cost nothing per item.
            '<linearGradient id="rsTop" x1="0" y1="0" x2=".45" y2="1">'
            '<stop offset="0" stop-color="#fff" stop-opacity=".72"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            '</linearGradient>'
            '<linearGradient id="rsL" x1="0" y1="0" x2="1" y2=".3">'
            '<stop offset="0" stop-color="#fff" stop-opacity=".26"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity=".07"/>'
            '</linearGradient>'
            '<linearGradient id="rsR" x1="0" y1="0" x2=".2" y2="1">'
            '<stop offset="0" stop-color="#0B0B0B" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity=".13"/>'
            '</linearGradient>'
            # the room itself: floor catching light from the open corner
            '<linearGradient id="rsFloor" x1=".15" y1="0" x2=".85" y2="1">'
            '<stop offset="0" stop-color="#0B0B0B" stop-opacity=".085"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity=".025"/>'
            '</linearGradient>'
            '<linearGradient id="rsWallA" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#0B0B0B" stop-opacity=".045"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity=".105"/>'
            '</linearGradient>'
            '<linearGradient id="rsWallB" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#0B0B0B" stop-opacity=".14"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity=".06"/>'
            '</linearGradient>'
            # the contact shadow each object sits in
            '<radialGradient id="rsSh" cx=".5" cy=".5" r=".5">'
            '<stop offset="0" stop-color="#0B0B0B" stop-opacity=".30"/>'
            '<stop offset=".55" stop-color="#0B0B0B" stop-opacity=".13"/>'
            '<stop offset="1" stop-color="#0B0B0B" stop-opacity="0"/>'
            '</radialGradient>'
            '</defs>'
            '<g class="rs__shell"></g><g class="rs__items"></g></svg></div>'
            '</div>')


# ── node 23 · the three tour slides, as large animated illustrations ──────
# CSS/SVG keyframes only, deliberately: no JS means no timers to leak and no
# wiring to duplicate in the export. Each one animates the CLAIM the slide makes,
# rather than decorating it.

def il_privacy(h=300):
    """Slide 1. Seven readings drift around inside the house and never cross the
    outline; one thing — outdoor air — comes IN from outside. That is exactly the
    narrowing `ai-integration.md` §10 flags, drawn instead of asserted."""
    dots = "".join(f'<span class="il__d d{i}"></span>' for i in range(1, 8))
    return (f'<div class="il il--priv" style="height:{h}px">'
            '<svg viewBox="0 0 260 226" preserveAspectRatio="xMidYMid meet">'
            '<path class="il__house" d="M130 20 L234 104 L234 194 Q234 206 222 206 '
            'L38 206 Q26 206 26 194 L26 104 Z"/></svg>'
            f'{dots}'
            '<span class="il__seal"></span>'
            '<span class="il__inbound"><i></i></span>'
            '</div>')


def il_agent(h=300):
    """Slide 2. Air is drawn in from the edges, the orb pulses as it works, clean
    rings push back out. The agent's claim is "it runs itself" — so the only thing
    on screen that never gets touched is the thing doing the work."""
    spec = "".join(f'<span class="il__spec s{i}"></span>' for i in range(1, 7))
    return (f'<div class="il il--agent" style="height:{h}px">'
            '<span class="il__rip r1"></span><span class="il__rip r2"></span>'
            '<span class="il__rip r3"></span>'
            f'{spec}'
            '<span class="il__orb"><i></i></span>'
            '<span class="il__tick t1"></span><span class="il__tick t2"></span>'
            '</div>')


def il_home(h=300):
    """Slide 3. One hub, four devices, wires that draw themselves in turn. The
    three that are not the purifier are drawn faint — the same honesty node 6
    now enforces by not offering them at all."""
    return (f'<div class="il il--home" style="height:{h}px">'
            '<svg viewBox="0 0 260 226" preserveAspectRatio="xMidYMid meet">'
            '<path class="il__house" d="M130 20 L234 104 L234 194 Q234 206 222 206 '
            'L38 206 Q26 206 26 194 L26 104 Z"/>'
            '<path class="il__wire w1" d="M130 140 L74 106"/>'
            '<path class="il__wire w2" d="M130 140 L186 106"/>'
            '<path class="il__wire w3" d="M130 140 L70 176"/>'
            '<path class="il__wire w4" d="M130 140 L190 176"/>'
            '</svg>'
            '<span class="il__hub"></span>'
            '<span class="il__nd n1 on"></span><span class="il__nd n2"></span>'
            '<span class="il__nd n3"></span><span class="il__nd n4"></span>'
            '</div>')


def peel(go="next"):
    """Node 7 — drag the tab to strip the polybag off the filter. The one setup
    step whose failure is completely invisible, turned into the one step the user
    physically performs on screen. Tap also works (it plays the peel)."""
    return (f'<div class="pl" data-cmp="peel" data-go="{E(go)}">'
            '<div class="pl__filter"><i></i><i></i><i></i><i></i><i></i></div>'
            '<div class="pl__wrap"><span class="pl__sheen"></span></div>'
            '<button class="pl__tab" aria-label="Peel off the wrapper"></button>'
            '<p class="pl__hint"><span>Drag down to unwrap</span></p>'
            '</div>')


def holdring(label, go="next", ms=1500):
    """Node 11 — press and hold to pair, ring filling as you hold. Replaces a
    fake progress bar with a Next button under it. Holding is the honest gesture
    for 'this takes a moment and you should stay near the device', and letting go
    early drains the ring, which teaches the requirement without an error."""
    return (f'<div class="hr" data-cmp="hold" data-go="{E(go)}" data-ms="{ms}">'
            '<svg class="hr__svg" viewBox="0 0 200 200">'
            '<circle class="hr__bg" cx="100" cy="100" r="86"/>'
            '<circle class="hr__fg" cx="100" cy="100" r="86"/></svg>'
            '<div class="hr__core"><span class="pur pur--pulse pur--sm">'
            '<span class="pur__ring"></span></span></div>'
            f'<button class="hr__btn" aria-label="{E(label)}"><span>{E(label)}</span></button>'
            '</div>')


def countup(n, unit, sub):
    """Node 26 — the first number the user ever sees should arrive, not just be
    there. Counts up from zero on mount, `standard` easing, no spring: this is an
    ambient reading and motion gate 4 caps it."""
    return (f'<div class="rd" data-cmp="countup" data-to="{E(n)}">'
            '<span class="rd__g"></span>'
            f'<span class="rd__n">0</span><span class="rd__u">{E(unit)}</span>'
            f'<span class="rd__s">{E(sub)}</span></div>')


def devcard(name, sub, go=None):
    return (f'<button class="dev"{GO(go)}>'
            '<span class="dev__v"><span class="pur pur--idle"><span class="pur__ring"></span>'
            '<span class="pur__grill"></span><span class="pur__grill"></span></span></span>'
            f'<span class="dev__t"><b>{E(name)}</b><span>{E(sub)}</span></span>'
            + icon("chevron-right", 17, cls="ic-chev", sw=2) + '</button>')

def note(head, body):
    return f'<div class="note"><b>{E(head)}</b><span>{E(body)}</span></div>'

def banner(x, kind="err"):
    return f'<div class="ban {kind}">{E(x)}</div>'

def dots(n, at):
    return '<div class="dots">' + "".join(
        f'<span class="dot{" on" if i == at else ""}"></span>' for i in range(n)) + '</div>'

# prog() removed 2026-08-19 — node 15 was its only caller and now uses
# infloader(). Its `.pb` CSS went with it. A determinate bar is still
# supported by wireLoad() if a future screen genuinely knows its duration
def spin(label="", sub=""):
    return (f'<div class="sw"><span class="sp"></span>'
            f'{f"<b>{E(label)}</b>" if label else ""}{f"<span>{E(sub)}</span>" if sub else ""}</div>')

def reading(n, unit, sub):
    return (f'<div class="rd"><span class="rd__g"></span>'
            f'<span class="rd__n">{E(n)}</span><span class="rd__u">{E(unit)}</span>'
            f'<span class="rd__s">{E(sub)}</span></div>')

def cta(x, go="next", state="on", gate=None):
    """`gate="name,mobile"` renders the button inert but KEEPS its target, so
    the runtime can switch it on once those fields have content.

    ⚠ The plain `state="off"` form deliberately drops `data-go`, which is why
    node 4's Proceed was a dead end: nothing in the harness ever removed that
    state, so the button could not be enabled even in principle. A gate is the
    difference between "off right now" and "off forever"."""
    if gate:
        return (f'<button class="cta off" disabled data-gate="{E(gate)}"'
                f'{GO(go)}>{E(x)}</button>')
    d = "" if state == "on" else " disabled"
    return f'<button class="cta{"" if state=="on" else " off"}"{GO(go) if state=="on" else ""}{d}>{E(x)}</button>'

def cta2(x, go="next"):
    return f'<button class="cta2"{GO(go)}>{E(x)}</button>'

# sim() removed 2026-08-17 (owner: remove all the simulate buttons). Every
# error/edge screen this drove is still reachable from the review rail and
# by hash — see the note on the matching screen for how to reach it now.

def lnk(x, go="next"):
    return f'<button class="lnk"{GO(go)}>{E(x)}</button>'

def two(a, ago, b, bgo):
    return (f'<div class="two"><button class="cta2 f"{GO(ago)}>{E(a)}</button>'
            f'<button class="cta f"{GO(bgo)}>{E(b)}</button></div>')

def dialog(title, body, a, ago, b, bgo):
    """The OS permission alert. Owner 2026-08-19: "you can also apply these
    settings on the pop ups" — so it takes recipes.dialog, the same large
    surface as the sheet, and for the same structural reason it needs the same
    two elements: `.dlg` is the shell that casts the shadow, `.dlg__s` is the
    masked surface. A mask would clip the shadow away if they were one."""
    return (f'<div class="dlgw"><div class="dlg"><i class="dlg__s"></i>'
            f'<div class="dlg__b"><b>{E(title)}</b><span>{E(body)}</span>'
            f'<div class="dlg__r"><button{GO(ago)}>{E(a)}</button>'
            f'<button class="s"{GO(bgo)}>{E(b)}</button></div></div></div></div>')

def sheet(*blocks):
    return f'<div class="shw"><div class="sh">{"".join(blocks)}</div></div>'

def toast(x):
    return f'<div class="toast">{E(x)}</div>'

def kb():
    rws = "".join('<div class="kr">' + "".join(f'<span>{k}</span>' for k in r) + '</div>'
                  for r in ["qwertyuiop", "asdfghjkl", "zxcvbnm"])
    return (f'<div class="kbd">{rws}<div class="kr">'
            '<span class="w">space</span><span class="g">done</span></div></div>')

def tabbar(active=0):
    """The Home mock's tab bar. The four icons were grey placeholder blocks
    until 2026-08-19; they are real glyphs from the small register now."""
    tabs = (("Home", "house"), ("Device", "fan"),
            ("Routines", "repeat"), ("People", "users"))
    return '<div class="tabs">' + "".join(
        f'<span class="tab{" on" if i == active else ""}">'
        + icon(g, 22, sw=1.9) + f'{E(l)}</span>'
        for i, (l, g) in enumerate(tabs)) + '</div>'
# ───────────────────────────────────────────── the page layout (owner, 2026-08-17)
#
# THE STRUCTURE EVERY INSTRUCTIONAL SCREEN NOW USES. Four owner frames set it:
#
#     status bar
#     ( ← )                     circular, floating over the visual
#     ┌──────────────┐
#     │              │          pgt — the visual, taking whatever height is
#     │   VISUAL     │                left over. Full-bleed, centred.
#     └──────────────┘
#     EYEBROW                   pgb — pinned to the bottom, left-aligned
#     A big title
#     supporting copy
#     [      CTA      ]
#     quiet link
#
# WHAT CHANGED FROM THE OLD SCREENS, all four visible in the frames:
#   · an EYEBROW above the title, which did not exist before
#   · content is BOTTOM-ALIGNED; the visual floats in the space above it
#   · the close (×) is gone — the frames carry a back arrow and nothing else
#   · the 4-dot stepper is gone — no frame shows one
# Each is flagged where it costs something; see the section notes below.

def hero(cls=""):
    """A SLOT for the carried purifier — not the purifier itself.

    REBUILT 2026-08-18 (owner: "the device image keeps flickering... just use
    one single image throughout"). Every pairing screen used to render its own
    `.rnd` element and the runtime FLIPped between them. Same data URI, but a
    new element each time, so the browser re-rasterised the background on every
    screen — that is the flicker, and no amount of easing hides it.

    There is now exactly ONE purifier in the document (`.phero`, a sibling of
    the screens, created once at boot). These slots are invisible boxes that
    declare where it should be; the runtime reads the slot and moves the single
    element there with a transform. Nothing is re-rendered, nothing re-decodes,
    and only a compositor property changes."""
    return f'<i class="pslot {cls}" data-pslot></i>'


def v_led(h=250):
    """Node 9 — REBUILT 2026-08-18 (owner): the light is ON THE DEVICE now,
    not a capsule floating on its own. The purifier is the carried hero, at
    its largest here, with the glow pinned to `--ledy` — the real position of
    each SKU's indicator, measured off the render rather than guessed."""
    return ('<div class="ledp">' + hero("ledp__pur") +
            '<span class="ledp__glow"></span><span class="ledp__bar"></span></div>')


def sheetover(*blocks):
    """A bottom sheet over the screen behind it, dimmed. Node 5 (owner,
    2026-08-17): the email code opens ON the Setup profile page rather than
    replacing it, so the card you just filled in stays visible behind the ask.

    It reuses build-auth.py's sheet CSS — the same `.sheet` / `.sheet__c` that
    nodes 1-3 use, already imported into this stylesheet. One sheet, two
    grounds: a photograph in the sign-in, a page here."""
    return ('<div class="ovl"><span class="ovl__s"></span>'
            '<div class="sheet" data-align="left"><i class="sheet__s"></i>'
            '<div class="sheet__c">'
            + "".join(blocks) + '</div></div></div>')


def sheetbare(*blocks, back=None):
    """A bottom sheet on the plain canvas, with nothing behind it to dim.

    Nodes 4 and 5 as of 2026-08-20 (owner): the profile page became a sheet,
    and the owner's frames show it on the app's own light ground rather than
    over a screen. So this is `sheetover()` minus the scrim — same `.sheet`
    machinery, no `.ovl__s`. Kept separate rather than giving sheetover() a
    flag, because "is there something behind this worth seeing" is the whole
    difference between the two and a boolean would hide it."""
    return ('<div class="ovl ovl--bare">'
            + (nav(back=back) if back else '')
            + '<div class="sheet" data-align="left"><i class="sheet__s"></i>'
            '<div class="sheet__c">' + "".join(blocks) + '</div></div></div>')


def sheetback(go):
    """The sheet's own back arrow — inside the sheet, not the page behind it.

    ⚠ NO CALLERS as of 2026-08-20. The owner moved the back button out of the
    sheet and onto the page for nodes 2-5 (`au(back=)` / `sheetbare(back=)`),
    which is every screen that used this. Kept rather than deleted because it is
    a shape a sheet may legitimately need again — a sheet opened OVER a page
    that has its own back button cannot borrow that one. If you reach for it,
    check first that the page-level bar is not the right answer."""
    return f'<button class="iconbtn"{GO(go)} aria-label="Back">{BACK_SVG}</button>'


def otpin(n=4, v=""):
    """A code field you can actually type into — one transparent input laid
    across the boxes, same trick as the sign-in sheet. A per-box input steals
    focus on every keystroke and breaks paste."""
    boxes = "".join(f'<i data-i="{i}">{E(v[i]) if i < len(v) else ""}</i>'
                    for i in range(n))
    return (f'<div class="otpi" data-cmp="otp" data-n="{n}">{boxes}'
            f'<input inputmode="numeric" autocomplete="one-time-code" '
            f'maxlength="{n}" value="{E(v)}" aria-label="Code"></div>')


def keycard(name="Ruhaan Royce", mobile="+91 98765 43210", cls="", tilt=False,
            slot=False):
    """The master key card — REBUILT 2026-08-20 on the owner's new artwork.

    Five colourways (`design-elements/brand/keycard/`), chosen on node 5b and
    then carried by every later appearance. The colour lives on `.phone` as
    `data-kc`, not on the card, for the same reason the purifier's SKU does:
    three cards can be alive at once (this one, the travelling mini, the
    door's) and they must never disagree about which key you made.

    ⚠ THE LAYOUT MOVED WITH THE ART. The old card put NAME and EMAIL in the
    middle with a serif watermark initial top-right; this one is "MASTER KEY"
    engraved at the top, the key mark centred, and the identity block in the
    BOTTOM LEFT. Positions are percentages of the card so the whole thing
    scales as one object.

    Three things on it are live, all driven by node 4's sheet (see
    paintCard): the avatar (initials until a picture is chosen), the name and
    the mobile number. The serif watermark initial is GONE — the new art has
    its own centred key mark and a second watermark fought it."""
    parts = [w for w in name.split() if w]
    inits = "".join(w[0] for w in parts[:2]).upper() or "N"
    # the shimmer — one speckle layer plus the edge catch. Inert until a tilt
    # driver sets --gx/--gy/--gi; `tilt=True` is what asks for that driver.
    fx = ('<i class="kfx" aria-hidden="true">'
          '<i class="kfx__spk"></i><i class="kfx__rim"></i></i>')
    return (
        f'<div class="kcard{" " + cls if cls else ""}" data-cmp="profile"'
        f'{" data-tilt" if tilt else ""}{" data-kslot" if slot else ""}>'
        f'{fx}'
        '<div class="kcard__id">'
        # ⚠ NO AVATAR, NO EDIT GLYPH — owner, 2026-09-09: "remove the profile
        # picture and the profile picture edit button and align the name and the
        # mobile number to the left where it is currently aligned with the
        # profile picture." So `.kcard__id`'s left inset is unchanged and the
        # text simply inherits the position the avatar used to hold.
        # This reverses the 2026-08-19 edit glyph and the avatar with it; the
        # first-run flow now has NO way to set a picture at all, which closes
        # the open question that had been flagged since the avatar lost its
        # field on node 4 rather than leaving it half-built.
        '<div class="kcard__t">'
        f'<span class="kcard__l">NAME</span>'
        f'<b class="kcard__v" data-cname>{E(name)}</b>'
        f'<span class="kcard__l">MOBILE</span>'
        f'<b class="kcard__v kcard__v--m" data-cmob>{E(mobile)}</b>'
        '</div>'
        '</div>'
        '</div>')


# The five colourways, and the swatch colour that stands for each. Sampled
# from the centre of the owner's own files rather than eyeballed, so a swatch
# cannot end up advertising a colour the card does not have:
# ── the five colourways, READ FROM THE TOKENS ───────────────────────────
# ⚠ This file otherwise re-states values raw (see the `.fld` comment) because
# it predates the token loader. The colourways are the exception, and
# deliberately so: they are a NEW canonical fact with no prior home, and a
# mirrored copy of a five-entry list whose ORDER encodes the owner's mapping
# is exactly the kind of thing that drifts silently. One home, read at build
# time — CLAUDE.md rules 2 and 4.
def _tok(expr):
    """Read one expression out of design.tokens.js through node.

    Grew out of _ways(): once a SECOND canonical fact had to come from the
    tokens, a copy of the subprocess boilerplate per fact was the wrong
    shape."""
    script = ("import(%s).then(m=>process.stdout.write(JSON.stringify(%s)))"
              % (json.dumps((ROOT / 'src/tokens/design.tokens.js').as_uri()), expr))
    res = subprocess.run(['node', '--input-type=module', '-e', script],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit('Could not read %s from the tokens.\n%s'
                         % (expr, res.stderr.strip()))
    return json.loads(res.stdout)


def _ways():
    ways = _tok('m.keycard.ways')
    # the artwork has to exist for every id the tokens name, or a swatch
    # would select a card that cannot be drawn
    missing = [w['id'] for w in ways if int(w['id']) not in CARD_B64]
    assert not missing, 'tokens name colourways with no artwork: %s' % missing
    return [(w['id'], w['label'], w['swatch']) for w in ways]

CARDWAYS = _ways()
KCDEFAULT = CARDWAYS[0][0]
TITLEGRAD = _tok('m.titleGradient')


def swatches(active=None):
    """Node 5b's colourway picker. Selection writes `data-kc` on `.phone`, so
    the card, the travelling mini and the door's card all follow one value."""
    active = active or KCDEFAULT
    dots = "".join(
        f'<button class="sw{" on" if k == active else ""}" data-kc="{k}" '
        f'style="--sw:{hexv}" aria-label="{E(label)}"></button>'
        for k, label, hexv in CARDWAYS)
    return f'{lab("CUSTOMIZE")}<div class="sws" data-cmp="ways">{dots}</div>'


def ccol(*head, mid="", tail=(), midattr="", headcls=""):
    """The centred column shared by nodes 5a and 5b — see the `.ccol` CSS.

    `head` is the heading and body, `mid` is the one object the screen is
    about, `tail` is everything pinned beneath it. Split this way because the
    OBJECT is the only part that differs between the two screens, and the owner
    asked for the same structure on both.

    ⚠ `head` goes in a FIXED-HEIGHT band. That is load-bearing, not tidiness:
    the two screens have different copy lengths, and while the head was free to
    size itself the object below it started at a different y on each — which is
    the card jump the owner reported between 5a and 5b."""
    return ('<div class="ccol">'
            + f'<div class="ccol__h{headcls}">' + "".join(head) + '</div>'
            + f'<div class="ccol__w"{midattr}>{mid}</div>'
            + '<div class="ccol__t">' + "".join(tail) + '</div>'
            + '</div>')


def sleeve(inner="", cls=""):
    """The wallet the key arrives in — node 5a. Owner artwork, TWO layers:
    `sleeve-back` sits behind the card and `sleeve-front` in front of it, so
    the card is genuinely enveloped rather than pasted on top. The card slots
    BETWEEN them, which is why this takes `inner` rather than being a backdrop.

    Tapping slides the whole sleeve down and off, leaving the card behind —
    see wireWallet()."""
    return (f'<div class="wal{" " + cls if cls else ""}" data-cmp="wallet">'
            '<i class="wal__back" aria-hidden="true"></i>'
            f'<div class="wal__card">{inner}</div>'
            '<i class="wal__front" aria-hidden="true"></i>'
            '</div>')


def reskey(cls=""):
    """Node 18a's resident's key — owner artwork (2026-08-17), used AS IS.
    Nothing on it is live and nothing is personalised: no name, no initials,
    no avatar. The master key (node 4) is yours; this one is deliberately
    generic, which is what makes it something you can hand out. Replaced
    memberkey(), which composited the member's name onto the master-key
    artwork."""
    return f'<i class="reskey {cls}"></i>'


def glyph(kind):
    """The large page glyph — owner-supplied SVG (2026-08-18), one per pairing
    surface: Bluetooth on node 11, Wi-Fi on nodes 13 and 12."""
    return f'<i class="gly gly--{kind}"></i>'


def sigbars(n=4):
    """Wi-Fi strength as four ascending bars, n of them lit.

    SVG rather than four divs: the harness scales the whole phone with a
    transform, and at that scale CSS gaps between 3px divs fell below a pixel
    and the meter rendered as one solid triangle. SVG geometry survives the
    scale. Material's own icon is nested arcs, which at 13px on a list row is
    a smudge — bars are legible at this size and are what the owner asked for.
    """
    bars = "".join(
        '<rect x="%s" y="%s" width="4" height="%s" rx="1.2" fill="currentColor" '
        'opacity="%s"/>' % (i * 7, 16 - (4 + i * 4), 4 + i * 4,
                            "0.8" if i < n else "0.13")
        for i in range(4))
    # ⚠ Replaced the four hand-drawn bars 2026-08-19. This encodes a VALUE, so
    # it maps strength onto the pack's four Wi-Fi states rather than picking one
    # glyph — wifi-zero/low/high/wifi are the same mark at four fill levels,
    # which is what a meter is.
    # ⚠ CLASS IS `sigm`, NOT `sig`. `.sig` is the STATUS BAR's signal glyph —
    # `.sig{width:17px;height:11px;clip-path:polygon(...)}` — and it was
    # silently winning here: the old row meter also used `class="sig"`, so the
    # status bar's clip-path was what you actually saw, at one fixed shape, and
    # the strength this function computes never rendered at all. Three networks
    # at 4/3/2 bars drew identical icons. Renaming is the fix; the meter now
    # shows the value it is handed.
    return icon(("wifi-zero", "wifi-low", "wifi-high", "wifi")[max(0, min(3, n - 1))],
                17, cls="sigm", sw=2)


def infloader(note=""):
    """An INDETERMINATE loader for node 15 — a plain circular spinner.

    Owner, 2026-08-19, asked for "a Infinity loader because we do not know how
    long it will take", and the honest half of that argument still stands: a
    progress bar claims knowledge of the remaining time, and the old one filled
    over a fixed ten seconds while the real device work takes 15-20, so it lied
    twice — about the duration AND about being measurable at all.

    On 2026-08-20 the owner replaced the literal lemniscate with this: "the
    infinity loader on page 15 can just be regular circular loader than an
    actual infinity symbol." Same claim, ordinary vocabulary — and a circle is
    the shape every platform already uses for "indeterminate", so it needs no
    explaining to the person waiting.

    The arc length is still DERIVED (2*pi*r) rather than guessed, so the gap
    stays a fixed fraction of the ring at any size."""
    import math
    SZ, SW = 24.0, 2.2
    r = (SZ - SW) / 2
    C = 2 * math.pi * r
    arc = C * 0.26                       # the visible sweep; the rest is gap
    return (f'<div class="inf">'
            f'<svg class="inf__s" viewBox="0 0 {SZ:g} {SZ:g}" aria-hidden="true">'
            f'<circle class="inf__t" cx="{SZ/2:g}" cy="{SZ/2:g}" r="{r:.2f}"/>'
            f'<circle class="inf__d" cx="{SZ/2:g}" cy="{SZ/2:g}" r="{r:.2f}" '
            f'style="stroke-dasharray:{arc:.1f} {C - arc:.1f}"/>'
            f'</svg>'
            + (f'<p class="inf__n">{E(note)}</p>' if note else "")
            + '</div>')


def dotmatrix():
    """A DOT MATRIX with a ring travelling outward through it — the
    celebratory backdrop for node 5a (key card created) and node 16
    (connected). Owner, 2026-08-19: "a dot matrix in the back and a circular
    ring only visible in the dot matrix going outwards."

    "Only visible in the dot matrix" is the whole trick, and it is why this is
    two layers rather than a ring drawn on top: `__base` is the resting matrix
    in very light grey, `__ring` is the SAME matrix in a darker grey, masked to
    an annulus that expands. Nothing is ever drawn between the dots, so the
    ring reads as the dots themselves lighting up in sequence.

    ⚠ IT IS A SIBLING OF THE CONTENT, NOT ITS PARENT. It used to wrap what it
    sat behind, and that quietly capped its width: `.scr.in .pgt>*` gives every
    direct child of the visual half a `pgin` transform, a transform CREATES A
    CONTAINING BLOCK for absolutely positioned descendants, and so the backdrop
    could never grow past its wrapper's content box no matter what insets it
    was given. Two passes of padding arithmetic failed against that before it
    was measured. As a sibling it is positioned by `.pgt` itself and is
    full-bleed by construction.

    ⚠ GREYS ONLY. The owner's reference is a dark product shot with colour;
    the instruction was to take the structure and not the palette — "keep the
    theme white... only use colors of gray and white. Don't break the theme."
    """
    return ('<i class="dmx" aria-hidden="true">'
            '<i class="dmx__base"></i><b class="dmx__ring"></b></i>')


def slist(label, rows, go, kind="bt"):
    """A LIVE SCAN LIST — nodes 11 and 13, merged 2026-08-18 (owner).

    Scanning and picking used to be two screens each ("scanning over
    Bluetooth" then "select your device"; "fetching Wi-Fi" then "select
    Wi-Fi"). The owner's reference makes each pair ONE screen: the count
    starts at zero with the spinner turning, and results arrive in place
    underneath it. Rows are in the markup and revealed by wireSlist, so the
    static renderings (board, export) still show what the list contains.
    """
    n = len(rows)
    def row(r):
        # wifi rows carry a SIGNAL STRENGTH in r[1]; bt rows carry a sub-label
        if kind == "wifi":
            right = ('<span class="sr__w">' + icon("lock", 13, cls="sr__lock", sw=2.1)
                     + sigbars(r[1] if len(r) > 1 else 4) + '</span>')
            sub = ""
        else:
            right = icon("chevron-right", 17, cls="ic-chev", sw=2)
            sub = f'<span>{E(r[1])}</span>' if len(r) > 1 and r[1] else ""
        # ⚠ A PLAIN MONOLINE BLUETOOTH MARK, not the engraved render (owner,
        # 2026-08-19: "in the devices found section... they are very small
        # icons. They will be regular maybe material design Bluetooth icons").
        # The engraved glyph is a page-header object; at 30px it reads as a
        # smudge — the same mistake the Wi-Fi lock/meter pair had already been
        # corrected for a day earlier, and this tile was simply missed.
        # Lucide, not the engraved render and not my earlier hand-drawn one:
        # this is the small register (see design-elements/icons/README.md).
        # ⚠ THE RENDER, NOT A BLUETOOTH GLYPH, WHEN THE ROW IS A DEVICE.
        # Owner, 2026-08-20: "we need the render images in the container to show
        # which devices are available." A Bluetooth mark on every row said only
        # "this arrived over Bluetooth", which the screen's own title already
        # says; the render is the thing that tells two rows apart at a glance —
        # and since node 6 was deleted, this list is where the model is chosen,
        # so it has to LOOK like a choice between products.
        # Falls back to the mark when a row carries no SKU (a Wi-Fi list, or a
        # device whose model the scan could not resolve).
        if kind != "bt":
            ic = ""
        elif len(r) > 2 and r[2]:
            ic = (f'<span class="sr__i sr__i--rnd">'
                  f'<i class="rnd rnd--{E(r[2])}"></i></span>')
        else:
            ic = '<span class="sr__i">' + icon("bluetooth", 16, sw=1.9) + '</span>' 
        # ⚠ A THIRD TUPLE FIELD IS THE SKU, and only the Bluetooth scan uses it.
        # Node 6 used to ask which model you owned; since 2026-08-20 this scan is
        # the only place that question gets answered, so the row has to carry the
        # answer forward. `wirePick` reads `data-sku` — the same attribute the
        # deleted picker's cards used, so nothing downstream changed.
        sku = f' data-sku="{E(r[2])}"' if len(r) > 2 and r[2] else ""
        return (f'<button class="sr" data-go="{E(go)}"{sku} hidden>{ic}'
                f'<span class="sr__t"><b>{E(r[0])}</b>{sub}</span>{right}</button>')
    items = "".join(row(r) for r in rows)
    return (f'<div class="slist" data-cmp="slist" data-n="{n}" data-label="{E(label)}">'
            f'<div class="slist__h"><span data-count>(0) {E(label)}</span>'
            '<i class="slist__s"></i></div>'
            f'<div class="slist__l">{items}</div></div>')


# The three household contacts, and their avatar hues. ⚠ HUE-CODED AVATARS
# are back on the owner's 2026-08-18 reference — the 2026-08-12 palette rule
# had stripped them to monochrome and the changelog recorded the loss ("SKU
# thumbnails and household avatars lost their hue coding... and now separate
# only by depth"). Same standing conflict as node 6's SKU tiles: two owner
# instructions, only the owner can retire one. Three CSS rules to revert.
KEY_CONTACTS = [("Ayush Tiwari", "+91 9876543210", "pink"),
                ("Aanya Verma", "+91 9876543210", "blue"),
                ("Karan Singh", "+91 9988776655", "sand")]


def inits(name):
    parts = [w for w in name.split() if w]
    return "".join(w[0] for w in parts[:2]).upper() or "?"


def keyshare():
    """Node 18a — REBUILT 2026-08-18 to the owner's reference.

    Pick people and they become removable pills between the field and the
    list; the list drops whoever is already picked, so the two halves never
    disagree about who is invited. The CTA counts what is selected.

    ⚠ The reference labels Ayush Tiwari's avatar "AK". Initials are computed
    from the name here (AT), because a wrong initial on a screen whose whole
    job is telling people apart is a typo to fix, not a style to copy.
    """
    # ⚠ THE "FROM YOUR CONTACTS" LIST IS GONE — owner, 2026-08-19: "there will
    # be no from your contact section. You can remove and scrap that entire
    # section." Two consequences, neither hidden:
    #   · KEY_CONTACTS is now unused by this screen, and with it the hue-coded
    #     avatars that reversed the 2026-08-12 palette rule. That flag on this
    #     screen is therefore CLOSED by deletion rather than by decision.
    #   · wireKeys' pill-picking path is unreachable: no `.kc` rows means no
    #     pills, so the CTA no longer counts a selection and stays "Share key".
    #     The wiring is left in place (it is harmless and `data-pills` still
    #     exists) because the field is where a recipient comes from now, and a
    #     future contact picker would want exactly that machinery back.
    return ('<div class="ks" data-cmp="keys">'
            + lab("SEND A KEY TO")
            + '<div class="fld"><input class="fi" '
              'placeholder="Name, phone number or email" aria-label="Send a key to"></div>'
            + '<div class="ks__pills" data-pills></div></div>')


def eyb(txt):
    """The uppercase section label above the title. typography.scale.label."""
    return f'<p class="eyb">{E(txt)}</p>'


def pgt(inner):
    """The visual half. Takes the leftover height and centres its content."""
    return f'<div class="pgt">{inner}</div>'


def pgb(*blocks, top=False, enter=False):
    """The content half — pinned to the bottom, left-aligned. Its presence is
    what switches the screen into this layout (`.scr:has(.pgb)`).

    `top=True` pins it to the TOP instead — for any page whose content half
    carries a LIST (owner, 2026-08-19). A bottom-pinned list grows upward:
    every item that arrives makes `.pgb` taller, which shrinks `.pgt`, which
    slides the icon and heading up the screen. Owner: "after every new item
    appears the icon and header body keeps shifting up." Top-aligned, arriving
    items grow DOWNWARD into empty space and nothing above them moves. The CTA
    still sits on the bottom edge — see the `.pgb--top` CSS.

    `enter=True` opts this content half OUT of the generic page-to-page
    transition (`pgin`) and into its own entrance — currently node 4 only,
    where the fields rise from below to meet the card flipping in from above.
    ⚠ It has to be a real class, not a `:has()` sniff: `.scr.in .pgb` is
    (0,3,0) and silently beats anything weaker, which is exactly how the
    first version of this animation came to never run at all."""
    cls = "pgb" + (" pgb--top" if top else "") + (" pgb--enter" if enter else "")
    return f'<div class="{cls}">' + "".join(blocks) + '</div>'


def qlink(x, go="next"):
    """The quiet secondary action under the CTA — "Not blinking?". A text link,
    not a second button: the frames are explicit that only one thing on the
    screen looks pressable."""
    return f'<button class="qlink"{GO(go)}>{E(x)}</button>'


def infoln(txt, link="", go=""):
    """A small (!) note under a list.

    Was written for node 6's "One to start" line; node 6 was deleted on
    2026-08-20 and node 11's troubleshoot entry is the caller now.

    `link`/`go` make the tail of the sentence tappable — the owner's reference
    for node 11 puts the way out of a failed scan directly under the results,
    which is where someone who cannot see their purifier is actually looking.

    ⚠ THE LINK TEXT NAMES THE DESTINATION (W-14). The reference reads "Click
    here to troubleshoot"; "click here" names nothing, which W-14 rules out and
    which a screen reader announces as a list of identical links. The
    destination is the words."""
    inner = E(txt)
    if link:
        inner += f' <button class="infoln__a"{GO(go)}>{E(link)}</button>'
    return (f'<p class="infoln">' + icon("info", 15, cls="ic-i", sw=2)
            + f'<span>{inner}</span></p>')


# ───────────────────────────────────────────── the sign-in sheet (nodes 1-5)
#
# These render build-auth.py's states as STATIC screens, which is what this
# harness is: 45 screens you walk with the arrow keys, every field showing a
# fixed value. auth-prototype.html remains the LIVE one — you type into it and
# the sheet resizes under you. Same states, two jobs, one source.
#
# The sheet still animates in when you land on a sheet screen, because the
# screen's markup is re-inserted on every visit and the entrance animation
# replays. Walking S0 -> A1 with the arrow key plays the real arrival.

def au(inner, splash=False, align="center", back=None):
    """One sheet state as a full-bleed screen: photo, status bar, and either
    the wordmark (splash) or the sheet.

    The photo is an empty div painted by one CSS rule, not an inlined <img>:
    eight screens share it, and inlining put 1.4 MB of duplicate base64 in
    this file. See the CSS join at the bottom.

    ⚠ `splash=True` carries `data-cmp="splash"` — owner, 2026-08-20: "on page 1
    splash screen, after 1 second the bottom sheet pops up automatically."
    `wireSplash()` reads the timing off it. This only fires in the CANONICAL
    harness (this file, hence first-run-flow.html — the one Vercel serves);
    `auth-prototype.html` is a separate standalone tool with its own splash
    timer (`MO.splashHold`, 2.6s) and is unaffected."""
    splash_attrs = ' data-cmp="splash" data-go="A1" data-ms="1000"' if splash else ""
    return (
        f'<div class="au"{splash_attrs}>'
        f'<div class="bg" data-carry="bg"><i class="bg__img"></i></div>'
        f'{bar()}'
        + (nav(back=back) if back else '')
        + (AUTH.wordmark() if splash else
           f'<div class="sheet" data-carry="sheet" data-align="{align}">'
           f'<i class="sheet__s"></i>'
           f'<div class="sheet__c sheet__c--stagger">{inner}</div></div>')
        + '</div>'
    )


def au_state(sid, digits=None, email=None, ready=None, handoff=None):
    """The `inner` build-auth.py already wrote for that state, filled in.

    The live prototype starts every field empty and fills it as you type; this
    harness is a static walkthrough where every field carries a value — the
    same convention the other 38 screens follow, and what the owner's frames
    show. Nothing here rewrites copy; it only supplies the values typing would
    have produced.

    ⚠ `phone=` was dropped 2026-08-19: build-auth.py's A2/A3 verify email now,
    not a phone number (see that file's STATES docstring) — the phone number
    moved to node 4's `mobile_field()`, filled in there instead."""
    s = next(x for x in AUTH.STATES if x["id"] == sid)
    h = s.get("inner", "")
    if digits:
        for i, ch in enumerate(digits):
            h = h.replace(f'<i data-i="{i}"></i>',
                          f'<i data-i="{i}" data-filled>{E(ch)}</i>')
    if email:
        h = h.replace('data-email', f'data-email value="{E(email)}"')
    if ready:
        h = h.replace(' disabled>', '>')
    if handoff:
        # The last sign-in state ends build-auth.py's own flow, so its CTA
        # points at that file's end card. Here it hands over to node 6.
        marker = f'data-go="{AUTH.HANDOFF}"'
        if marker not in h:
            raise SystemExit(
                f"build-prototype.py: {sid} no longer carries {marker}. "
                "build-auth.py's hand-off changed and this repoint is now a "
                "silent no-op — fix it rather than dropping it.")
        h = h.replace(marker, f'data-go="{handoff}"')
    return h


# ───────────────────────────────────────────── screens
# `node` is the box number in the owner's flow diagram (2026-08-06). Screens that
# share a node are two halves of one box — an app screen and the OS dialog that
# sits on top of it, a spinner and the answer it resolves into. Nothing that is
# not in the diagram gets a node; those are the edge states, reachable from the
# controller and from the dashed buttons on the phone.
SC = {}
def S(sid, sec, title, blocks, note_="", kind="core", node=None):
    SC[sid] = dict(id=sid, sec=sec, title=title, html="".join(blocks),
                   note=note_, kind=kind, node=node)

# ══════════════════════════════════════════════════ 1 · ACCOUNT  (nodes 1–5)

# REBUILT 2026-08-17 (owner) AS A BOTTOM-SHEET FLOW. Nodes 1-5 were five
# full-screen pages; they are now one surface — a photograph with a sheet that
# stays put and re-lays-out under you. The states, their copy and their markup
# all come from build-auth.py; this file only places them in the sequence.
#
# ⚠ WHAT THIS REPLACED, so it is not lost by accident:
#   · Node 1 was `doorway()` — the drag-to-open door with light behind it,
#     rebuilt four times over 2026-08-06 (PRD §5.10, §5.10a-c). The function is
#     still defined above and is now UNUSED. Re-instating it is one line; it
#     was replaced on owner instruction, not because it stopped working.
#   · Node 4 collected a display NAME as well as an email. The name is gone
#     from the reference frames entirely, so nothing in first run collects it
#     now, and node 18a (invite family) is downstream of that. PRD §5.11.
#   · Node 5 waited for a LINK so the mail client could be left open; it is a
#     code now, so §5.2's "two verifications" costs two code entries.
#
# ⚠ EMAIL AND PHONE SWAPPED PLACES, 2026-08-19 (owner). The sheet (nodes 1-3)
# used to verify a phone number and node 4 collected an email; now the sheet
# verifies EMAIL and node 4 collects a PHONE NUMBER, verified inline via its
# own "Verify" pill and a sheet-over-page at node 5 — the exact relationship
# node 5 already had, just the other contact method. See build-auth.py's own
# docstring for the sheet side of this swap. Node 4 also gained TWO new
# states this pass: 4a (verified) and 5a (the "key card created" success
# screen, new — nothing in the old flow celebrated finishing this page).

S("S0", "Account", "Splash", [au("", splash=True)],
  "Node 1, first half. The image and the wordmark, no control. AUTO-ADVANCES to the "
  "login sheet (node 1's second half) after 1s (owner, 2026-08-20) — see wireSplash(). "
  "⚠ This replaced the drag-to-open "
  "door — see the note at the top of this section. Walking S0 → A1 with the arrow key "
  "plays the real arrival: a 1s hold, then an 880ms settle with no overshoot "
  "(durations.entrance).", node=1)

S("A1", "Account", "Login sheet", [au(au_state("A1", handoff="A4"))],
  "Node 1, second half — restacked 2026-08-19 (owner). Apple leads as the primary (black) "
  "CTA, Google is secondary (white), email is the tertiary link. Apple and Google both skip "
  "straight to node 4 — a federated sign-in has already verified the person, so there is no "
  "email left to check. Only “Continue with email” walks through nodes 2-3. ⚠ The DPDP "
  "notice still rides on this screen's fine print; PRD §5.1 remains open regardless of which "
  "field moved where.", node=1)

S("A2", "Account", "Email address",
  [au(au_state("A2", email="ruhaanroyce@gmail.com", ready=True), back="A1")],
  "Node 2 — was the mobile-number entry; now the same shape, for email (owner, 2026-08-19). "
  "Proceed is inert until the address looks valid.", node=2)

S("A3", "Account", "Email OTP",
  [au(au_state("A3", digits="2169", ready=True, handoff="A4"), back="A2")],
  "Node 3 — was the mobile OTP; now email. Four digits, countdown visible from t=0. Proceed "
  "hands off to node 4, which now asks for the phone number rather than the email node 4 "
  "used to collect. ⚠ No way back: a mistyped address strands you here, the same gap the "
  "old mobile-OTP state had.", node=3)

S("A3E", "Account", "Code didn’t match", [au(au_state("A3", digits="2169", handoff="A4").replace(
    '<p class="resend">',
    '<p class="err">That code didn’t match. Two attempts left.</p><p class="resend">'))],
  "⚠ EXTRAPOLATED, not from the owner's frames — every supplied frame is happy path. The "
  "error takes the place the countdown sits in and the boxes stay filled, so the correction "
  "is a single digit rather than a re-entry. Uses status.negative, the only non-green hue in "
  "the palette. Needs an owner pass before it means anything.", "state")

# Node 4's page, shared by three screens: the page itself (unverified), node
# 5's sheet-over-it, and 4a's verified snapshot. One definition so none of
# the three can drift from the others. `verified` switches the mobile row
# between the "Verify" pill and the plain check, and gates Continue —
# nothing downstream should be able to reach node 5a without it.
# ── nodes 4-5c · REBUILT 2026-08-20 to the owner's five frames ──────────────
# The profile page became a SHEET, and creating the key became a small
# ceremony: name it, verify it, receive it in a wallet, open the wallet, choose
# its colour, then the celebration.
#
#     4    "Tell us about yourself"   sheet: name + mobile
#     5    mobile OTP                 sheet
#     5a   "Welcome, {name}"          the wallet, with Tap to open
#     5b   "Key created!"             the card revealed + 5 colourways
#     5c   the dot-matrix celebration (was 5a)
#
# ⚠ WHAT THIS REPLACED, so it is not lost by accident:
#   · Node 4 was a full PAGE carrying the card and the two fields together,
#     with an inline "Verify" pill on the mobile row that opened node 5. The
#     pill, the verified snapshot (node 4a) and `mobile_field()` all go with
#     it — the sheet asks for the number and the next sheet verifies it, so
#     there is no half-verified page to be in any more.
#   · The card's serif watermark initial is gone with the old artwork.

def profile_sheet(name="", mobile="", ready=False):
    """Node 4. The owner's frame: eyebrow, title, NAME, MOBILE NUMBER, Proceed.

    ⚠ Values are EMPTY by default, unlike every other screen in this harness.
    The frame shows placeholders, and it is the one screen whose whole job is
    that nothing is filled in yet — pre-filling it would hide the state the
    screen exists for. `paintCard` still drives the card from whatever is
    typed here."""
    return [bar(), sheetbare(
        eyb("Create profile"),
        '<h1 class="h1 grad">A bit about you</h1>',
        lab("NAME"),
        f'<div class="fld"><input class="fi" placeholder="Enter name" '
        f'value="{E(name)}" data-bind="name"></div>',
        lab("MOBILE NUMBER"),
        '<div class="fld fld--verify"><span class="fld__cc">+91</span>'
        f'<input class="fi" type="tel" inputmode="numeric" maxlength="10" '
        f'placeholder="Enter number" value="{E(mobile)}" data-bind="mobile"></div>',
        cta("Proceed", "A5", gate="name,mobile"),
        back="A3")]


S("A4", "Account", "A bit about you", profile_sheet(),
  "Node 4 — REBUILT 2026-08-20 (owner) from a full page into a SHEET on the app's own "
  "ground. It asks two things and gets out of the way: a name and a number. ⚠ THE CARD IS "
  "NOT ON THIS SCREEN any more, and that is the point of the rebuild — the key is now "
  "something you are GIVEN at node 5a rather than something you watch yourself fill in. "
  "⚠ The fields are deliberately EMPTY here, unlike every other screen in this harness: "
  "this is the one screen whose subject is that nothing has been entered yet. INTERACTIVE — "
  "what you type drives the card on every later screen. ⚠ Proceed is inert until both "
  "fields are filled. ⚠ The inline “Verify” pill, the verified page (old node 4a) and "
  "`mobile_field()` are all gone: the next sheet verifies the number, so there is no "
  "half-verified page to be in.", node=4)

S("A5", "Account", "Mobile OTP", [bar(), sheetbare(
      '<h1 class="h1 grad">Enter OTP</h1>',
      '<p class="sub">We’ve sent an OTP to +91 98765 43210</p>',
      '<button class="s-link" data-go="A4">Edit number</button>',
      otpin(4, "2169"),
      '<p class="resend">Resend OTP in <b>15s</b></p>',
      cta("Proceed", "A6"), back="A4")],
  "Node 5. Same sheet, one step on — and it is a sheet on the ground now rather than over "
  "node 4's page, because node 4 is a sheet too. Proceed hands over to node 5a, where the "
  "key is presented. INTERACTIVE — the four boxes take real typing.", node=5)

S("A5E", "Account", "Nothing arrived", [bar(), sheetbare(
      '<h1 class="h1 grad">Nothing yet?</h1>',
      '<p class="sub">It was sent to +91 98765 43210.</p>',
      bullets(["Check you typed the number correctly",
               "Signal can be slow indoors, so give it a minute",
               "Some carriers delay OTP SMS during busy hours."]),
      cta("Send it again", "A5"),
      '<button class="s-link" data-go="A4">Use a different number</button>',
      back="A4")],
  "The mobile “nothing arrived” state — same three-reasons shape, SMS-flavoured causes.",
  "state")

S("A6", "Account", "Welcome — the wallet", [bar(), nav(back="A5"),
  ccol('<h1 class="t1 grad">Welcome, <span data-wname>Ruhaan</span></h1>',
       bd("We made a little something for you, to celebrate your first key to "
          "your home."),
       mid=sleeve(keycard(), cls="wal--enter"),
       tail=['<button class="cta3" data-walopen>Tap to open</button>'],
       headcls=" ccol__h--in")],
  "Node 5a — NEW 2026-08-20 (owner). The key is PRESENTED, not assembled: it arrives in a "
  "wallet with your name on the screen above it. Two owner layers with the card between "
  "them (`sleeve-back` behind, `sleeve-front` in front) so it is genuinely enveloped rather "
  "than pasted on. INTERACTIVE — tap the card or the button and the sleeve slides off the "
  "bottom, then the flow moves to node 5b. ⚠ The greeting uses the name typed on node 4, so "
  "this screen is empty of meaning if you jump straight to it; walk from node 4 to see it "
  "read properly.", node="5a")

S("A7", "Account", "Key created", [bar(), nav(back="A6"),
  ccol('<h1 class="t1 grad">Key created</h1>',
       bd("This is your key to access your home in the NOMA app. You can make "
          "a custom key for your home residents."),
       mid=keycard(tilt=True, slot=True),
       tail=[swatches(), cta("Proceed", "A8")])],
  "Node 5b — NEW 2026-08-20 (owner). The sleeve is off and the key is yours to finish: five "
  "colourways of the owner's artwork, default first. INTERACTIVE — tap a swatch and every "
  "later appearance of the card follows, because the choice lives on `.phone` as `data-kc` "
  "rather than on any one card. ⚠ This is also one of the three screens that keep the gyro "
  "shimmer (owner: “we can still give the rainbowing gyro effect… on the customize "
  "screen”).", node="5b")

S("A8", "Account", "Key card created", [bar(), nav(), dotmatrix(),
  # no tilt: the shimmer belongs to the screens where you are looking AT the
  # card, not to the celebration, where the backdrop is the event
  ccol('<h1 class="t1 grad">Key card created</h1>',
       mid=keycard(),
       midattr=' data-cmp="success" data-go="P4" data-ms="2600"',
       headcls=" ccol__h--in")],
  "Node 5c — REBUILT 2026-08-20 (owner) onto the same column as 5a and 5b, which is the "
  "whole point: \u201cthe card remains in the same place and the animation behind the card "
  "with the dot matrix starts\u201d. It used to be its own layout (`.ksucc`), so the card "
  "changed size and position at the exact moment it was supposed to hold still. Now only the "
  "text and the backdrop change. ⚠ `nav()` with no back button is deliberate and load-"
  "bearing: it reserves the bar's height so the column starts where it does on 5a and 5b — "
  "without it everything above the card shifts up 70px and the card goes with it. "
  "Auto-advances into pairing after 2.6s, handing the card to the corner mini partway "
  "through. Greys only.", node="5c")

# ══════════════════════════════════════════════════ 2 · PAIRING  (nodes 6–12)
#
# REWRITTEN 2026-08-06 (owner) to the updated pairing sequence. Node 6 (choose the
# purifier) is unchanged; everything after it is new. The old flow went
# instructions → light → bluetooth → scan → wifi-list → password; the new one adds
# the filter unwrap as its own step, splits "plug in" from "check the light", makes
# the Bluetooth step about switching the radio on rather than about a permission,
# and replaces the manual Wi-Fi list with an auto-fetch that falls back to manual.
#
# Node numbering: 6-16 are re-mapped to the new stages. 17 onward are untouched, so
# every downstream reference (17, 18, 18a, 23-26) still means what it meant.

# ⚠ NODE 6 — "CHOOSE YOUR PURIFIER" — IS DELETED (owner, 2026-08-20):
# "we don't need to select the device now... the number six page will not exist
# any longer." It asked which model you own before anything had been switched
# on; the Bluetooth scan on node 11 now answers the same question from what it
# can actually see, so asking first was asking twice.
#
# ⚠ WHAT WENT WITH IT, AND WHERE IT LANDED INSTEAD:
#   · `wirePick()` and the SKU carry. `PICK` defaults to '200', so nothing broke
#     when the picker vanished — it simply stopped being chooseable. Node 11's
#     rows carry `data-sku` now, so the scan sets it. Grep `wirePick` if this
#     ever needs the old three-card screen back; the function is untouched.
#   · `CARRY.pur`, which flew the chosen render onto the next screen. The scan
#     rows have no render to fly, so the purifier's first appearance is now node
#     7's unwrap illustration.
#   · The three hue-coded SKU thumbnails, and with them the open conflict they
#     carried against the 2026-08-12 two-green rule. That conflict is CLOSED by
#     deletion rather than by decision — worth knowing if the picker returns.
S("P2", "Pairing", "Unwrap the filter", [bar(), nav(back="P5"),
  pgt(v_filter(300)),
  pgb(eyb("Getting started"),
      t1("Let’s unwrap the filter"),
      bd("It ships sealed in plastic. Until that comes off it will hum away happily and "
         "clean nothing at all."),
      bd("Then slide it back in and close the door until it clicks."),
      cta("Continue", "P2B"))],
  "Node 7 — the single most common cause of “it’s running but the air isn’t changing”, and "
  "the only setup step whose failure is completely invisible. "
  "⚠ RE-LAID-OUT 2026-08-17, AND THE PEEL GESTURE IS GONE. The frame shows a static "
  "exploded view and a plain Continue; the 2026-08-06 build made the polybag something you "
  "physically dragged off, on the reasoning that the instruction most likely to be skimmed "
  "should be the one thing you have to touch (PRD §5.9). That reasoning has not been "
  "answered — it has been overtaken by a frame. `peel()` is still defined and unused. "
  "⚠ The door-click is still the only confirmation; if the hardware can detect a seated "
  "filter this screen should verify rather than ask (`O-9`).", node=7)

S("P2B", "Pairing", "Plug in and switch on", [bar(), nav(back="P2"),
  pgt(v_plug(300)),
  pgb(eyb("Getting started"),
      t1("Now find it a socket"),
      bd("Anywhere near where it’ll live. One press of the power button. You should hear "
         "the fan pick up."),
      cta("Continue", "P3"))],
  "Node 8. Split out from the old combined instruction screen: unwrapping the filter and "
  "powering on are two different physical tasks with two different failure modes, and "
  "collapsing them is how the filter step gets skimmed. Re-laid-out 2026-08-17; the CTA "
  "was “It’s on”, and the frame says “Continue”. ⚠ That is a real loss — “It’s on” is the "
  "user reporting the physical world back, which is the whole pattern of this section "
  "(PRD §8.1 rule 6, warm buttons at warm moments). Followed the frame; flagging it.", node=8)

S("P3", "Pairing", "Wi-Fi light blinking", [bar(), nav(back="P2B"),
  pgt(v_led(250)),
  pgb(eyb("Getting started"),
      t1("Is the light blinking?"),
      bd("A slow blink means it’s ready for me. It can take a moment to get there."),
      cta("Yes, it’s blinking", "W1"),
      qlink("Not blinking?", "P3F"))],
  "Node 9. The user confirms the physical world — never a timer. Re-laid-out 2026-08-17: "
  "the recovery instruction that used to sit on the screen as a bordered note is now the "
  "quiet “Not blinking?” link under the CTA, which is what the frame shows. "
  "⚠ That buries it. The 2026-08-06 reasoning was that needing the hold-to-reset is the "
  "COMMON case on a second setup, not an error, which is why it was on the screen rather "
  "than behind a link. It now routes to P3F, so the content still exists one tap away. "
  "⚠ `O-9`: the blink vocabulary and the 5–6s hold are both unconfirmed hardware "
  "behaviours.", node=9)

S("P3E", "Pairing", "In another home", [bar(), nav(back="P3"),
  pgt(v_q(200)),
  pgb(eyb("Getting started"),
      t1("Already spoken for"),
      bd("It’s set up in another home. Resetting it takes it out of there, and whoever set "
         "it up will be told."),
      rows(["How do I reset it?"], "chev", go="P3E"),
      cta("I’ve reset it", "P3"), qlink("Cancel", "P5"))],
  "Says what resetting costs the other household. SmartThings has this state with nothing "
  "in it. Re-laid-out 2026-08-17 to the owner's page structure.", "state")

S("P3F", "Pairing", "No light at all", [bar(), nav(back="P3"),
  pgt(v_q(200)),
  pgb(eyb("Getting started"),
      t1("No light at all?"),
      bullets(["Check the plug is switched on at the wall",
               "Try a different socket",
               "Press the power button once. The fan should start"]),
      cta("The light is on now", "P3"), qlink("Contact support", "P3F"))],
  "Dead-device triage before pairing triage. Nothing here is an error code. Also where "
  "node 9's “Not blinking?” link now lands, so it carries the hold-to-reset content that "
  "used to sit on node 9 itself.", "state")

S("P4", "Pairing", "Switch on Bluetooth", [bar(), nav(back="A7"),
  pgt(v_phone_near(280)),
  pgb(eyb("Getting started"),
      t1("I’ll need Bluetooth for a minute"),
      bd("It’s the only way to reach a purifier that isn’t on Wi-Fi yet. I’ll let it go the "
         "moment we’re done."),
      cta("Continue", "P4D"))],
  "Node 10. Reframed 2026-08-06: this is about the radio being ON, not only about granting "
  "the app permission — a phone with Bluetooth switched off is the failure this step "
  "actually prevents. The permission dialog still follows immediately, with the reason "
  "visible behind it.", node=10)

S("P4D", "Pairing", "Bluetooth · system prompt", [bar(), nav(),
  pgt(v_phone_near(280)),
  pgb(eyb("Getting started"),
      t1("I’ll need Bluetooth for a minute"),
      bd("It’s the only way to reach a purifier that isn’t on Wi-Fi yet.")),
  dialog("“NOMA” would like to use Bluetooth",
         "This lets NOMA find your purifier during setup.",
         "Don’t Allow", "P4E", "Allow", "P5")],
  "Node 10, second half. The reason stays visible behind the system dialog, which is the "
  "whole point of splitting the node in two.", node=10)

S("P4E", "Pairing", "Bluetooth refused", [bar(), nav(back="P4"),
  pgt(v_phone_near(250)),
  pgb(eyb("Getting started"),
      t1("Bluetooth is still off"),
      bd("There’s no other way to get to a purifier that isn’t on Wi-Fi yet. Turn it back "
         "on in Settings and I’ll pick up where we left off."),
      cta("Open Settings", "P4"), qlink("Not now", "A7"))],
  "A refusal that genuinely blocks has to say so, and has to say how long it costs. Never "
  "re-prompt; send them to Settings.", "state")

S("P5", "Pairing", "Looking for your purifier", [bar(), nav(back="P4"),
  pgt(""),
  pgb(eyb("Connect Bluetooth"),
      t1("Looking for your purifier"),
      bd("Keep your phone near it while I search. This usually takes a few seconds."),
      slist("devices found",
           [("Air Pro 200", "AP-9611 · Signal strong", "200"),
            ("Air Pro 500", "AP-9611 · Signal fair", "500")], "P6B", "bt"),
      # the way out of a failed scan, under the results — owner, 2026-08-20:
      # "below the available devices is the entry point for that flow"
      infoln("Can’t see yours?", "Troubleshoot", "P5E"),
      cta("Refresh", "P5"), top=True)],
  "Node 11 — MERGED 2026-08-18 (owner). Scanning and picking were two screens ("
  "“Scanning over Bluetooth” then “Select your device”); they are one now, with the count "
  "starting at zero and results arriving in place. That is both truer to how a scan behaves "
  "and one screen shorter. "
  "⚠ TWO IDENTICAL SKUs, deliberately: the scan really can surface two of the same purifier "
  "in a household that bought a pair, and the signal line is the only thing telling them "
  "apart. “Identify” — blink the light on one — was the answer to that and it is NOT on this "
  "screen; it needs to come back before build. ⚠ `O-9`: the Bluetooth name format "
  "(`AP-9611`) is an assumed hardware behaviour, not a confirmed one.", node=11)

S("P5E", "Pairing", "Not found", [bar(), nav(back="P5"),
  pgt(v_q(200)),
  pgb(eyb("Getting started"),
      t1("I can’t see it yet"),
      bd("Usually it just needs a small nudge."),
      bullets(["Keep your phone within three metres",
               "Check the Wi-Fi light is blinking, not steady",
               "Hold the Wi-Fi icon for five seconds to restart pairing"]),
      cta("Try again", "P5"), qlink("I need help", "P5F"))],
  "The device is the subject, never the user. Try again is primary, help is secondary, and "
  "Cancel is not offered.", "state")

S("P5F", "Pairing", "Common issues", [bar(), nav(back="P5E"),
  pgt(""),
  pgb(eyb("Getting started"),
      t1("Common issues"),
      rows(["There’s no light on the device at all", "The Wi-Fi light is steady, not blinking",
            "The light stopped blinking part-way", "It was set up in another home"],
           "chev", go="P5F"),
      cta("Back", "P5E"), qlink("Contact support", "P5F"))],
  "Written as the symptoms a person can observe, not as error codes. IKEA’s accordion.",
  "state")

S("P6B", "Pairing", "Pairing", [bar(), nav(),
  pgt('<div class="pair" data-cmp="pairing" data-go="P2">'
      # ⚠ THREE COLUMNS, THE OUTER TWO EQUAL. Owner, 2026-09-09: "make a unit
      # of all three items... and center all these three components to the
      # screen." The purifier is ~94px wide and the phone ~63, so a plain flex
      # row centres its own BOUNDING BOX and leaves the connection sitting
      # right of the screen's centre — and the tick, pinned to the row, sat
      # 15px left of the dots it is supposed to replace. Equal side columns
      # make the middle column dead centre by construction, and the tick lives
      # INSIDE that column, so it and the dots cannot disagree again.
      '<div class="pair__row">'
      '<span class="pair__side"><i class="pslot pair__pur" data-pslot></i></span>'
      '<span class="pair__mid">'
      '<span class="pair__line"><i></i><i></i><i></i><i></i><i></i></span>'
      '<span class="pair__check"></span>'
      '</span>'
      # A real phone, front on, screen off — owner: "make it look like a real
      # phone with a black screen and bezels and buttons on the side... only
      # show, like, a reflection on top of the black screen."
      '<span class="pair__side">'
      '<span class="iph">'
      '<span class="iph__scr"><i class="iph__isl"></i><i class="iph__gl"></i></span>'
      '<i class="iph__b iph__b--mute"></i>'
      '<i class="iph__b iph__b--up"></i>'
      '<i class="iph__b iph__b--dn"></i>'
      '<i class="iph__b iph__b--pwr"></i>'
      '</span>'
      '</span>'
      '</div>'
      '<p class="pair__status" data-status>Connecting…</p>'
      '</div>'),
  pgb(eyb("Getting started"),
      t1("Keep your phone nearby"),
      bd("I’m introducing myself to the purifier. This takes a few seconds."))],
  "Node 11, closing — REBUILT 2026-08-17 evening (owner): hold-to-pair is gone. The owner "
  "supplied a structural reference from the NoiseFit app — device on the left, phone on "
  "the right, a connection animation between them, a check when it lands — and this is "
  "that structure with NOMA's own visuals: the real render, a drawn phone, dots "
  "travelling the line, then the check and “Connected”, and the flow moves on by itself. "
  "⚠ WHAT THE HOLD WAS FOR, so its removal is a decision and not a loss: the 2026-08-06 "
  "build made pairing a press-and-hold because holding is the honest gesture for “stay "
  "near the device”, replacing a fake progress bar you could skip. This screen keeps the "
  "honesty a different way — the wait resolves ITSELF, there is no button to skip it, and "
  "the copy carries the stay-near instruction instead of the gesture. Auto-advances on "
  "completion; reduced motion goes straight to the check.", node=11)

S("P6E", "Pairing", "Pairing failed", [bar(), nav(back="P5"),
  pgt(v_q(200)),
  pgb(eyb("Getting started"),
      t1("That didn’t take"),
      bd("It stopped answering half-way through. Nothing’s half-done. It’s exactly "
         "as it was before we started."),
      cta("Try again", "P5"), qlink("I need help", "P5F"))],
  "Says the state of the world after the failure. A user who thinks the device is now "
  "half-configured will factory-reset it unnecessarily.", "state")

# ══════════════════════════════════════════════════ 3 · NETWORK  (nodes 12–16)

S("P7B", "Network", "Confirm your Wi-Fi", [bar(), nav(back="W1"),
  pgt(""),
  pgb(eyb("Connecting"),
      t1("Sharma_Home"),
      bd("This phone already knows the password, so there’s nothing to type."),
      field("Password", "••••••••••••", label="PASSWORD · FROM THIS PHONE"),
      foot("2.4 GHz and dual-band networks are fine. A 5 GHz-only one won’t work. There’s "
           "no 5 GHz radio inside the purifier."),
      cta("Join this network", "W3"),
      qlink("Wrong password?", "W2E"), top=True)],
  "Node 12, second half — now the CONFIRM step after the list rather than before it "
  "(top-pinned 2026-08-19 to match node 13: owner — \"it should not shift from page to "
  "page. Both are Wi-Fi pages\"). "
  "(owner, 2026-08-18). The credential is still pre-filled from the phone, so the common "
  "case is one tap and no typing. ⚠ 2026-08-18: node 14 (type the password yourself) was "
  "removed on owner instruction, so the escape hatch is now the wrong-password STATE "
  "rather than a screen — if a saved credential is stale there is no longer a normal path to correct it, only an edge state. The band line is stated here rather than buried in an error, "
  "because it is the one property of a home network that decides whether setup can work at "
  "all. ⚠ The source phrasing was “does not work with standalone wifi credential” — read "
  "here as *5 GHz-only networks*. If it actually meant captive-portal or "
  "enterprise/802.1X networks, this copy is wrong and both need their own states.",
  node=12)

S("W1", "Network", "Which network?", [bar(), nav(back="P3"),
  pgt(""),
  pgb(eyb("Connect Wi-Fi"),
      t1("Which network?"),
      bd("It needs one to fetch the outdoor air and run your routines."),
      slist("available networks",
           [("Sharma_Home", 4), ("Airtel_Asha_1224", 3), ("Airtel_Nup_1224", 2)],
           "P7B", "wifi"),
      foot("I’m only showing 2.4 GHz networks. The purifier can’t use 5 GHz."),
      cta("Refresh", "W1"), top=True)],
  "Node 13 — MERGED 2026-08-18 (owner), the same treatment as node 11: the “fetching "
  "Wi-Fi” spinner screen and the “select Wi-Fi” list screen are one page, with networks "
  "arriving under a live count. "
  "⚠ THIS ABSORBS NODE 12's FIRST HALF. Auto-fetch existed to make picking from a list "
  "unnecessary (PRD §5, node 12); the list is now the screen, so that argument is spent — "
  "what survives of node 12 is P7B, where the credential still comes from this phone and "
  "there is nothing to type. Node 12's id therefore lives on the CONFIRM screen and node 13 "
  "on this one, which is why the two no longer ascend. PRD §5.16, §5.17. "
  "⚠ 5 GHz SSIDs are hidden AND the app says so: hiding without explaining is a defect.",
  node=13)

S("W1E", "Network", "Only 5 GHz found", [bar(), nav(back="W1"),
  pgt(""),
  pgb(eyb("Connecting"),
      t1("Only 5 GHz here"),
      bd("The purifier needs 2.4 GHz. Most routers broadcast both, sometimes under a name "
         "ending in ‑2.4G."),
      rows(["Show every network anyway", "How do I find my 2.4 GHz network?"],
           "chev", go="W1E"),
      cta("Try again", "W1"))],
  "Common in Indian metros with ISP-supplied dual-band routers. The real fix is dual-band "
  "hardware — a copy fix on a hardware limit has a ceiling.", "state")

S("W2E", "Network", "Wrong password", [bar(), nav(back="W1"),
  pgt(""),
  pgb(eyb("Connecting"),
      t1("Sharma_Home"),
      field("Password", "", state="bad", label="PASSWORD"),
      banner("That password didn’t work. Worth another go?"),
      cta("Join", "W3"), qlink("Show password", "W2E")), kb()],
  "⚠ RE-BASED 2026-08-18. Node 14 (the manual password screen) was removed on owner "
  "instruction — node 12 hands straight to node 15 now — and this state was the error on "
  "that screen. Rather than delete the only wrong-password path in the flow, it is rebuilt "
  "on the CONFIRM surface: the credential comes from the phone, and a pre-filled credential "
  "can still be stale. It is rail- and hash-reachable only. ⚠ If the confirm screen never "
  "gets an inline error, a wrong saved password is a dead end with no state at all.",
  "state")

S("W3", "Network", "Setting up", [bar(), nav(),
  pgt(carousel([
    ("Set it up once, then forget about it",     mini("rooms")),
    ("I’ll watch the air, so you don’t have to", mini("agent")),
    ("Everyone at home, one app",                mini("people")),
    ("What I learn stays in your home",          mini("privacy"))])),
  pgb('<div data-cmp="load" data-go="W4" data-ms="10000">'
      + infloader("This can take about 15 to 20 seconds")
      + '</div>')],
  "Node 15. The wait is 15–20s of genuine device work, which is what makes it the one "
  "honest place in the flow for a pitch: it fills dead time rather than inserting it. "
  "⚠ 2026-08-19: the progress BAR is gone (owner: \"we do not know how long it will "
  "take\"). It filled over a fixed ten seconds while the work takes 15–20, so it lied "
  "twice — about the duration and about being measurable. An indeterminate lemniscate "
  "loader claims neither, and the 10px line under it gives the honest estimate in words. "
  "⚠ NO CTA as of 2026-08-18 (owner): the bar fills over ten seconds and the screen hands "
  "itself to node 16, with the carousel running throughout. That removes the last instance "
  "of the pattern the 2026-08-06 rebuild called the most dishonest in the prototype — a "
  "visible wait with a button under it that skips it. The wait is now the wait. "
  "⚠ The only screen with no eyebrow and no title — the carousel IS the content, and "
  "adding a heading over it would give the screen two competing voices. "
  "⚠ WCAG 2.2.2 (Pause/Stop/Hide): four slides at 2.2s loops for the length of the setup. "
  "Reduced-motion disables auto-advance and the dots are tappable, but 15–20s is already "
  "past the 5s threshold — this likely needs a real pause control.", node=15)

S("W4", "Network", "Connected", [bar(), nav(),
  pgt(dotmatrix() + glyph("check")),
  pgb(eyb("Connecting"),
      t1("That’s the hard part done"),
      bd("It’s on Sharma_Home, and it’ll find its way back on its own from now on."),
      cta("Next", "R1"))],
  "Node 16. The success state gets a full screen, not a toast — this is where the setup "
  "anxiety ends, and it is the first thing in the flow that has visibly worked. Runs into the "
  "two permission asks (24, 25) before the home is created — reordered 2026-08-06. "
  "2026-08-19: carries the same DOT MATRIX backdrop as node 5a (owner: \"this also needs to "
  "be a little bit celebratory\") — one component, so the two celebratory beats in the flow "
  "cannot drift apart.", node=16)

S("W4E", "Network", "No internet", [bar(), nav(back="P7B"),
  pgt(v_q(200)),
  pgb(eyb("Connecting"),
      t1("It can’t reach me"),
      bd("It’ll keep cleaning regardless. I just can’t show you the outdoor air or run "
         "your routines yet."),
      cta("Try again", "W3"), qlink("Carry on anyway", "R1"))],
  "The device still works; say so. Never strand a working device behind a network error.",
  "state")

# ══════════════════════════════════════════════════ 4 · PLACE & NAME  (nodes 17, 18, 18a)

S("R1", "Place", "Which room · create a home", [bar(), nav(back="W4"),
  pgt(""),
  pgb(eyb("Where it lives"),
      t1("Where does it live?"),
      bd("So I can compare your air against the right patch of outdoors."),
      # ⚠ A LABEL DOES NOT SPEAK (W-14). This read "AND WHAT SHALL I CALL
      # HOME?" — a question set in 12px letter-spaced caps, which is the label
      # register, so the voice came out shouted. It was also a SECOND ask on a
      # screen whose ask is "Where does it live?" (R-09, one ask per message).
      # Plain noun here; the placeholder already shows the shape of the answer
      # (W-11) and the foot takes the stakes out of it (R-05).
      field("Home name", "My Home", label="HOME NAME"),
      roomstage(),
      foot("You can rename any of this later."),
      cta("Continue", "R2"), top=True)],
  "Node 17, and the diagram’s biggest structural change: the home is created HERE, as a "
  "by-product of placing the first device, instead of on a screen of its own before the box "
  "was opened. It is a better trade — nothing abstract is named before something real exists "
  "— but it makes the home name a field most people will never look at. ⚠ C-12: two room "
  "preset lists exist in the material (8 and 11 items); this is the 11-item one, which has "
  "Pooja Room. "
  "⚠ RE-ORDERED 2026-08-18 (owner): title and body, then the home name, then the room "
  "chips, then the drawing last. The picker left the visual half to do it, so this is the "
  "one screen in the flow that does NOT follow the 2026-08-17 structure — the illustration "
  "is the last thing on the page rather than the first. The reading order is better (you "
  "name the home before being asked to place the device in it) and the drawing still morphs "
  "between rooms; PRD §5.9's gesture is unchanged. Flagged because a one-screen exception "
  "to a flow-wide structure is a decision, not a detail.", node=17)

S("R2", "Place", "Name the device", [bar(), nav(back="R1"),
  pgt(""),
  pgb(eyb("Where it lives"),
      t1("What should I call it?"),
      bd("Only really matters once there are two of them."),
      field("Device name", "Bedroom purifier", label="NAME"),
      chips(["Bedroom purifier", "Air Pro", "Upstairs"], (0,), (), go="R2"),
      cta("Continue", "D1"),
      # ⚠ SECONDARY, NOT A STEP. Owner, 2026-08-20: "give send a key as a
      # secondary CTA in page number eighteen... sending a key is a optional
      # flow. We don't want it to be a separate page." So node 18a left the
      # happy path and is reached from here instead.
      cta2("Send a key", "R3"), top=True), kb()],
  "Node 18, pre-filled from the room so the common case is one tap. Nodes 19–22 (update "
  "check, install, first reading) were removed 2026-08-06 — see below. "
  "⚠ 2026-08-18: this screen used to BE the diagram's branch — “Invite the family” against "
  "“Not now, I’ll do that later”. It is one Continue now (owner), so the branch moved onto "
  "node 18a itself, where the skip lives as a tertiary action. The path is the same; the "
  "fork is just one screen later.",
  node=18)

S("R3", "Household", "Send a key", [bar(), nav(back="R2"),
  pgt(reskey("reskey--tilt")),
  pgb(eyb("Your household"),
      t1("Who else needs a key?"),
      bd("Everyone at home gets a resident’s key of their own, on their own phone."),
      keyshare(),
      '<button class="cta" data-keycta>Share key</button>',
      '<button class="cta3" data-go="D1">Not now</button>'),
  '<div class="toast" data-toast>Key shared</div>'],
  "Node 18a — REBUILT 2026-08-18 to the owner's reference. Pick people and they become "
  "removable pills between the field and the list; the list drops whoever is already "
  "picked, so the two halves cannot disagree about who is invited, and the CTA counts the "
  "selection. INTERACTIVE — tap a contact, tap a pill's × to undo. "
  "⚠ THE DISCLOSURE GAP IS NOW UNSPOKEN. The body used to end “and you decide what each key "
  "opens”; the reference drops it. That is arguably better — the promise was never "
  "implementable, since the per-invite disclosure screen was removed on 2026-08-06 and "
  "never replaced — but the GAP is unchanged and is now invisible on the screen. A key that "
  "silently opens everything still needs a node. "
  "⚠ Hue-coded avatars are back, reversing the 2026-08-12 palette rule; see KEY_CONTACTS. "
  "2026-08-18: “Not now” lives here as a tertiary action — no container, no fill — because "
  "node 18 collapsed to a single Continue and the branch had to land somewhere. Skipping the "
  "household is still a first-class path; it just no longer competes with sharing for the "
  "eye.",
  node="18a", kind="state")

S("R3E", "Household", "Not a contact", [bar(), nav(back="R3"),
  pgt(reskey()),
  pgb(eyb("Your household"),
      t1("Who else needs a key?"),
      field("Name, phone number or email", "lakshmi@", state="bad", label="SEND A KEY TO"),
      banner("That doesn’t look like a phone number or an email address to me."),
      cta("Try again", "R3"))],
  "Inline, and it keeps what was typed. The keyboard mock came off with the 2026-08-17 key-card re-layout: the member card owns the visual half now, and there is no room for both.", "state")

# ══════════════════════════════════════════════════ 5 · ABOUT & PERMISSIONS  (nodes 23–26)
#
# ⚠ REMOVED WHOLESALE 2026-08-06 (owner). Nodes 19–22 — check for update / install /
# update complete / taking first reading — no longer exist in this flow. That was
# four screens (five counting the "update timed out" edge state, U2E) covering the
# firmware-update path and the post-tour reading wait. R2's "not now" and R3C's
# "Continue" now go straight into the tour at node 23; N1/N1D now resolve straight
# to Home instead of into a reading screen.
#
# Two things this removal leaves unresolved, worth carrying forward rather than
# quietly losing:
#   · There is no longer ANY screen in the flow that takes a first reading. Node 26
#     (Home) renders "34 · AQI" with no setup step that explains why a number is
#     already there. If the backend genuinely needs ~20s to settle a first reading
#     (as U4's copy said), Home needs its own loading state for that window — this
#     is now Home's problem, not first run's.
#   · Firmware update has no path at all. If a purifier can ship with stale
#     firmware, that has to be handled somewhere — during setup (as it was) or
#     later as a Device-detail nudge. Silently dropping it is a product decision,
#     not just a flow simplification, and it isn't recorded as one anywhere else.

# ⚠ THE TOUR IS GONE — C1 / C2 / C3 REMOVED 2026-08-17 (owner). Three things
# went with it, each of which had exactly one home there and now has none:
#   · The PRIVACY RECEIPT (C1) — "what I learn stays here", the repayment of
#     the promise node 4 makes. §5.6 argued leading the tour with privacy was
#     right; there is now no tour to lead. The promise is made and never
#     repeated.
#   · The AGENT'S INTRODUCTION (C2) — the product's first-person "I" now
#     introduces itself nowhere before Home starts speaking as it.
#   · The ROADMAP LINE (C3) — cameras, locks and the vacuum are now mentioned
#     NOWHERE in first run. That closes the unchecked-claim risk C3's note
#     carried, by removing the claim.
# il_privacy / il_agent / il_home are still defined and unused, same
# convention as doorway() and peel().
#
# ── UNUSED HELPERS, kept deliberately ──────────────────────────────────────
# Six visual helpers now have zero call sites, each retired by an owner
# decision rather than by rot. Kept because every one is a one-line
# reinstatement and the reasoning for its removal lives in the PRD:
#   doorway()     node 1's drag-to-open door        (PRD §5.10-§5.10c, §5.11)
#   peel()        node 7's drag-the-polybag gesture (PRD §5.12)
#   holdring()    node 11's press-and-hold pairing  (PRD §5.9 row, §5.14)
#   il_privacy/il_agent/il_home  the removed tour   (PRD §5.14)
#   v_scan()      the QR-viewfinder scan visual
#   spin()/v_wifi()  the two spinner screens the 2026-08-18 merges absorbed
# If any of these is still unused when the flow is handed to engineering,
# delete it then — an unused helper in a prototype is a parked decision, in
# shipped code it is just dead.

S("D1", "Home", "Tap your key on the door", [bar(),
  '<div class="dk" data-cmp="doorkey" tabindex="0" aria-label="Tap your key card on the '
  'door to enter">'
  '<div class="dk__scene">'
  '<div class="dk__light"></div>'
  '<div class="dk__door">'
  '<span class="dk__panel dk__panel--t"></span><span class="dk__panel dk__panel--b"></span>'
  '<div class="dk__lock"><span class="dk__reader"></span><span class="dk__led"></span>'
  '<span class="dk__lever"></span></div>'
  '</div></div>'
  '<p class="dk__hint">Tap card on door to enter</p>'
  # ⚠ no tilt/shimmer on the door either — nodes 4, 5 and 4a only, and the
  # drag owns `transform` here regardless.
  + '<div class="dk__card" data-kslot>'
  + '<div class="dk__roll">' + keycard() + '</div></div>'
  + '<div class="dk__flood"></div></div>'],
  "The last screen before Home — NEW 2026-08-17 (owner), and it replaces the tour. A "
  "closed door, and the key you made on node 4: drag the card up and tap it on the lock, "
  "and the door opens into your home. A plain tap on the card (or Enter) glides it to the "
  "lock by itself, so the gesture is the delight and never the toll gate; reduced motion "
  "goes straight through. The card carries whatever name and picture you gave it — it is "
  "the SAME card, which is the whole point of the key metaphor. "
  "⚠ There is deliberate symmetry here: node 1's drag-to-open door was removed this "
  "morning, and the door comes back at the end — you now end first run the way the old "
  "build began it, except this time you have the key. "
  "⚠ The lock is drawn beige, as the owner's reference shows. That is a non-palette hue on "
  "a depicted real-world object — the same open question as the 3D icons and the SKU "
  "thumbnails. Same flag, same owner call. "
  "⚠ This screen has no CTA and no skip: the gesture (or a tap, or Enter) is the only way "
  "on. Node 26 (Home) is one interaction away, so the toll is one tap — but if that reads "
  "as a gate rather than a delight in testing, a quiet link is the fix.", node=23)

S("L1", "Permissions", "Location · geofencing", [bar(), nav(back="W4"),
  pgt(v_geo(300)),
  pgb(eyb("Before we finish"),
      t1("Want the air sorted before you get home?"),
      bd("If I know you’re on your way, I’ll start clearing the room about twenty minutes "
         "out, and ease off once everyone’s gone."),
      foot("I only notice you crossing in and out. I never keep a trail of where you’ve "
           "been."),
      cta("Yes, do that", "L1D"), qlink("Not now", "N1"))],
  "Node 24 — NEW, and the flow’s only ask with a concrete payoff attached. This is the Away "
  "Saver trigger in J-WEEK-03 and `feature-map.json` triggerSources. ⚠ It is also the ask "
  "most in tension with “your data stays home”, said one screen earlier — hence the third "
  "line, which has to be true in the implementation, not just in the copy. "
  "⚠ 2026-08-17: “Not now” dropped from a full-size button to a text link. On a PERMISSION "
  "ask that is a bigger change than it looks — the 2026-08-06 build made it a real button "
  "precisely because declining has to stay first-class. Followed the frames' hierarchy; "
  "this is the clearest place to argue for an exception.", node=24, kind="state")

S("L1D", "Permissions", "Location · system prompt", [bar(), nav(),
  pgt(v_geo(300)),
  pgb(eyb("Before we finish"),
      t1("Want the air sorted before you get home?"),
      bd("About twenty minutes before you arrive.")),
  dialog("Allow “NOMA” to use your location?",
         "So your home is clean by the time you get back.",
         "Don’t Allow", "N1", "While Using the App", "N1")],
  "Node 24, second half. “While Using the App” is the honest option to lead with; Always is "
  "what geofencing actually needs, and iOS will ask for it separately once the pattern is "
  "established. Do not ask for Always here.", node=24, kind="state")

S("N1", "Permissions", "Notifications", [bar(), nav(back="L1"),
  pgt(v_bell(300)),
  pgb(eyb("Before we finish"),
      t1("Shall I tell you when the air turns?"),
      bd("Outdoor air spiking, the filter wearing out, anything I did while you were out. "
         "Nothing else."),
      cta("Yes, please", "N1D"), qlink("Not now", "R1"))],
  "Node 25. Primed at the end of the tour, when there is something worth being notified "
  "about. ⚠ Nodes 19–22 (the update/firmware/reading path that used to promise "
  "“we’ll notify you when it’s done”) were removed 2026-08-06 — that dangling promise is "
  "gone along with them. ⚠ Same “Not now” demotion as node 24 — see there.", node=25, kind="state")

S("N1D", "Permissions", "Notifications · system prompt", [bar(), nav(),
  pgt(v_bell(300)),
  pgb(eyb("Before we finish"),
      t1("Shall I tell you when the air turns?"),
      bd("Only the things worth interrupting you for.")),
  dialog("“NOMA” would like to send you notifications",
         "Air alerts, filter reminders and what the agent did.",
         "Don’t Allow", "R1", "Allow", "R1")],
  "Node 25, second half. Resolves straight to Home — nodes 19–22 no longer sit between "
  "this and it.", node=25, kind="state")

S("HOME", "Home", "Home", [bar(), nav(title="My Home", close="restart"),
  countup("34", "µg/m³", "BEDROOM, RIGHT NOW"),
  bd("It’s 168 out there. I’ve already started."),
  note("NOMA", "“I’ll hold the bedroom under 40 tonight. Nothing runs without your say-so.”"),
  rows([["Started cleaning the bedroom", "Just now · Undo"]], "chev", go="HOME",
       label="DONE TODAY"),
  gap(), rows([["Add another device", ""], ["People", ""]], "chev", go="HOME"), tabbar(0)],
  "Node 26, and — as the diagram is drawn — the first place the user ever sees a number. "
  "The three zones from ai-integration.md §2: reassurance first, then the ask, then the "
  "receipt. “Needs your call” is empty on day one and says so rather than hiding.", node=26)

# ───────────────────────────────────────────── the sequence
# One entry per screen, in diagram order. The branch (18a) is walked inline so a
# linear pass sees every box; the phone's own buttons let you skip it, exactly as
# the diagram's branch implies.
# S0 joins A1 on node 1: the splash and the login sheet are two halves of one
# box, the same way a screen and the OS dialog over it are.
# ⚠ 2026-08-19: node 4 gained two branches, 4a (verified) and 5a (success),
# walked inline here for the same reason 18a is — a linear pass should see
# every box. That is what moves the assertion below from 22 to 24.
# ⚠ RESEQUENCED 2026-08-20 (owner). Bluetooth now comes FIRST, before the box is
# ever opened, and the story is: you are given a key, the phone finds the device,
# they pair, and only then do you unwrap anything. Owner's words: "after the key
# card is created, we'll turn on the Bluetooth, and we'll start looking for
# devices that are available... then it will go to the number seven, unwrap your
# filter page."
#
# NODE NUMBERS DO NOT RENUMBER. The owner still refers to "number seven unwrap
# your filter" and "number thirteen" Wi-Fi, so the boxes keep their ids and only
# their ORDER changes. The harness already prints the node id separately from the
# step count for exactly this reason.
#
# Four pages left the happy path:
#   node 6   choose your purifier  — DELETED. The Bluetooth scan is the picker
#                                    now, so choosing a model up front asked the
#                                    same question twice.
#   node 24  location / geofencing — demoted to an edge state (owner: "they are
#   node 25  notifications           breaking the flow"). Kept rather than
#                                    deleted; see the changelog.
#   node 18a send a key           — demoted; reached from node 18's secondary CTA.
SEQ = ["S0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
       "P4", "P4D", "P5", "P6B",
       "P2", "P2B", "P3",
       "W1", "P7B", "W3", "W4",
       "R1", "R2",
       "D1",
       "HOME"]

VERSIONS = [dict(id="v1", label="Owner flow diagram, 2026-08-06", seq=SEQ)]

missing = [s for s in SEQ if s not in SC]
assert not missing, f"sequence references unknown screens: {missing}"
nodeless = [s for s in SEQ if SC[s]["node"] is None]
assert not nodeless, f"sequence screens with no diagram node: {nodeless}"
NODES = []
for s in SEQ:
    n = SC[s]["node"]
    if n not in NODES:
        NODES.append(n)
# ⚠ THE ORDER OF THIS LIST IS ITSELF A CHECK. After the 2026-08-20 resequence the
# nodes deliberately do NOT ascend — Bluetooth (10, 11) runs before the physical
# steps (7, 8, 9), and 13 before 12. If this list ever comes out sorted, the
# resequence has been undone.
assert len(NODES) == 21, (
    f"expected 18 main-line nodes + branches 5a, 5b, 5c. Removed over time: 19-22 "
    f"(2026-08-06), node 14 (2026-08-18, when node 12 began handing straight to 15), "
    f"and on 2026-08-20 node 6 (deleted — the Bluetooth scan is the picker now) plus "
    f"nodes 24, 25 and branch 18a (demoted to edge states). "
    f"got {len(NODES)}: {NODES}")
assert NODES != sorted(NODES, key=str), (
    "the nodes are in ascending order again — the 2026-08-20 resequence that puts "
    "Bluetooth before the unboxing has been lost")

STATES = [s for s in SC.values() if s["kind"] == "state"]
DATA = json.dumps({
  "screens": {k: {"html": v["html"], "sec": v["sec"], "title": v["title"],
                  "note": v["note"], "kind": v["kind"], "node": v["node"]}
              for k, v in SC.items()},
  "versions": [{"id": v["id"], "label": v["label"], "seq": v["seq"]} for v in VERSIONS],
  "nodes": NODES,
}, ensure_ascii=False)

state_btns = "".join(
    f'<button class="sb" data-jump="{s["id"]}">{E(s["title"])}</button>' for s in STATES)

CSS = r"""
@font-face{font-family:GSF;font-weight:400;src:url(data:font/ttf;base64,__REG__) format("truetype")}
@font-face{font-family:GSF;font-weight:600;src:url(data:font/ttf;base64,__MED__) format("truetype")}
@font-face{font-family:GSF;font-weight:700;src:url(data:font/ttf;base64,__BLD__) format("truetype")}
/* Instrument Serif (SIL OFL) — loaded for exactly one glyph, node 4's initial.
   src/fonts/instrument-serif/. Not a second body face. */
@font-face{font-family:ISerif;font-weight:400;src:url(data:font/ttf;base64,__SERIF__) format("truetype")}
:root{
  --kcard:url(data:image/webp;base64,__KCARD__);
  --kc1:url(data:image/webp;base64,__KC1__);
  --kc2:url(data:image/webp;base64,__KC2__);
  --kc3:url(data:image/webp;base64,__KC3__);
  --kc4:url(data:image/webp;base64,__KC4__);
  --kc5:url(data:image/webp;base64,__KC5__);
  --slvb:url(data:image/webp;base64,__SLVB__);
  --slvf:url(data:image/webp;base64,__SLVF__);
  --reskey:url(data:image/webp;base64,__RESKEY__);
  --rnd200:url(data:image/webp;base64,__RND200__);
  --rnd500:url(data:image/webp;base64,__RND500__);
  --rndmax:url(data:image/webp;base64,__RNDMAX__);
  --btphone:url(data:image/webp;base64,__BTPHONE__);
  --glybt:url(data:image/svg+xml;base64,__GLYBT__);
  --glywifi:url(data:image/svg+xml;base64,__GLYWIFI__);
  --glycheck:url(data:image/svg+xml;base64,__GLYCHECK__);
  --glybell:url(data:image/svg+xml;base64,__GLYBELL__);
  --ink:#0B0B0B; --sec:#6B6B6B; --ter:#9B9B9B; --hair:rgba(11,11,11,.10);
  --card:rgba(255,255,255,.76); --cardq:rgba(255,255,255,.44);
  --sh:0 10px 30px rgba(0,0,0,.08);
  --shs:0 4px 14px rgba(0,0,0,.08);
  --err:#8A2F1E; --errbg:rgba(138,47,30,.09);
  /* node 25's notification badge. red.mid from the palette — the token
     file marks it safe as a fill, and a badge is a fill. build-flow.py
     re-skins this from status.negative like everything else. */
  --neg:#D65151;
  --warn:#7A5A16; --warnbg:rgba(122,90,22,.10);
  --page:#EFEFEF; --panel:#FFFFFF;
  /* THE PHONE'S GROUND — gradients.canvas, substituted in css_out().
     ⚠ CORRECTED 2026-08-19 (owner: "you have changed the Bg color all of a
     sudden. Use the old bg color from the previous first run"). This was a
     cool radial falling to #A4A4A4, and it was the ODD ONE OUT: the previous
     first run (build-onboarding.py) has always painted the phone with
     gradients.canvas, and build-flow.py's re-skin already overrode this line
     to canvas too — its own comment reads "was radial → #A4A4A4 grey". Only
     this file was still on the stale value, so the prototype and every other
     rendering of the SAME screens disagreed about the ground.
     Nothing in this pass changed it; node 5a is simply the first screen with
     enough bare ground to make the discrepancy obvious. Reading the token
     means the three renderings cannot drift apart again. */
  --grad:__CANVAS__;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{background:var(--page);color:var(--ink);font-family:GSF,system-ui,sans-serif;font-size:15px;
  line-height:1.5;-webkit-font-smoothing:antialiased;overflow:hidden}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer;text-align:left}

.shell{display:flex;flex-direction:column;height:100vh}
.ctrl{background:var(--panel);border-right:0;border-bottom:1px solid var(--hair);
  flex:0 0 auto;max-height:min(38vh,360px);overflow-y:auto;padding:18px 26px 16px}
.ctrl__inner{max-width:1180px;margin:0 auto}
.ctrl__head{margin-bottom:14px}
.ctrl__grid{display:flex;flex-wrap:wrap;gap:20px 28px;align-items:flex-start}
.panel{flex:1 1 260px;min-width:230px;max-width:360px}
.panel--wide{flex:2 1 420px;max-width:560px}
.stage{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
  gap:18px;padding:26px 20px 40px;overflow-y:auto}

.ctrl h1{font-size:21px;letter-spacing:-.025em;margin:0 0 4px}
.lede{font-size:12.5px;color:var(--sec);margin:0 0 0;line-height:1.45}
.cl{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ter);
  font-family:ui-monospace,Menlo,monospace;margin:0 0 8px;padding-bottom:6px;border-bottom:1px solid var(--hair)}
.cl:first-of-type{margin-top:0}
.vr{display:block;margin-bottom:6px;cursor:pointer}
.vr input{position:absolute;opacity:0}
.vr>span{display:block;padding:10px 12px;border:1px solid var(--hair);border-radius:12px;font-size:12.5px;line-height:1.35}
.vr b{display:block;font-family:ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.08em;color:var(--ter)}
.vr em{float:right;font-style:normal;font-size:9.5px;color:var(--ter);letter-spacing:.06em;
  text-transform:uppercase;margin-top:-13px}
.vr input:checked+span{border-color:var(--ink);background:#F4F4F4}
.vr input:checked+span b{color:var(--ink)}
.vr input:focus-visible+span{outline:2px solid var(--ink);outline-offset:2px}
.pos{display:flex;align-items:center;gap:8px;margin:4px 0 10px}
.posn{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--sec);flex:1}
.nbx{width:34px;height:34px;border:1px solid var(--hair);border-radius:99px;display:grid;place-items:center;font-size:15px}
.nbx:hover{background:#F4F4F4}.nbx[disabled]{opacity:.3;cursor:default}
.track{height:3px;background:#E8E8E8;border-radius:2px;overflow:hidden;margin-bottom:14px}
.track i{display:block;height:100%;background:var(--ink)}
.jump{max-height:168px;overflow-y:auto;border:1px solid var(--hair);border-radius:12px}
.ji{width:100%;padding:7px 10px;font-size:12px;border-bottom:1px solid var(--hair);
  display:flex;gap:7px;align-items:baseline}
.ji:last-child{border-bottom:0}.ji:hover{background:#F6F6F6}
.ji.on{background:#F0F0F0;font-weight:600}
.jin{font-family:ui-monospace,Menlo,monospace;font-size:10px;color:var(--ter);min-width:16px}
.jis{margin-left:auto;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ter)}
.sb{display:block;width:100%;padding:7px 10px;font-size:12px;border:1px solid var(--hair);
  border-radius:9px;margin-bottom:5px;color:var(--err)}
.sb:hover{background:var(--errbg)}
.args{display:none}.args.on{display:block}
.arg{margin-bottom:10px}
.arg p{margin:0 0 5px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  font-family:ui-monospace,Menlo,monospace;color:var(--ter)}
.arg ul{margin:0;padding-left:16px}.arg li{font-size:12px;line-height:1.4;margin-bottom:5px}
.hint{font-size:11px;color:var(--ter);line-height:1.55;margin-top:18px;padding-top:12px;border-top:1px solid var(--hair)}

.phwrap{flex:0 0 auto;display:flex;align-items:center;justify-content:center}
.phone{width:390px;height:844px;flex:none;border-radius:52px;position:relative;overflow:hidden;
  background:var(--grad);
  box-shadow:0 0 0 11px #17171A, 0 0 0 12.5px #34343A, 0 30px 70px rgba(0,0,0,.26);
  transform-origin:center center}
.phone::before{content:"";position:absolute;inset:0;background:rgba(255,255,255,.30);
  pointer-events:none;z-index:0}
.island{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:110px;height:30px;
  background:#0A0A0A;border-radius:20px;z-index:50}
.hbar{position:absolute;bottom:9px;left:50%;transform:translateX(-50%);width:134px;height:5px;
  background:rgba(0,0,0,.22);border-radius:3px;z-index:50}
.scr{position:absolute;inset:0;display:flex;flex-direction:column;padding:0 22px 34px;overflow:hidden;z-index:2}
/* The incoming screen sits on top; the outgoing one fades out beneath it, so
   the swap cross-dissolves instead of blinking through the bare phone. The
   travel is 10px rather than 18 — with a real cross-fade underneath, a big
   slide is the thing that reads as lag. */
/* ⚠ THE SCREEN ROOT NEVER ANIMATES OPACITY — that is the whole fix for both
   the flash and the merging, third attempt and structural this time. Fading a
   whole transparent screen from 0 shows the bare ground for the first frames
   (the flash); overlapping two screens shows both contents blended (the
   merge). Instead the swap is a single paint — old removed and new appended
   in one task — and what animates is the new screen's CONTENT, entering over
   a ground that never changes. Same grammar as the carry screens, which were
   already accepted as seamless; direction survives as a small x-nudge. */
/* ⚠ TWO EXCLUSIONS, both for the same underlying reason: these elements own
   their own `transform`, and this animation would take it from them.

   `.dmx` is a full-bleed BACKDROP. The x-nudge would slide the whole matrix,
   and — because a transform creates a containing block — undo the reason it is
   a sibling of the content rather than its wrapper. See dotmatrix().

   `[data-tilt]` is the key card, which is steered continuously by the gyro.
   ⚠ SPECIFICITY CANNOT FIX THIS ONE: a FILLED animation outranks every normal
   declaration in the cascade, so `pgin`'s `both` fill pins `transform` forever
   and the tilt can never apply, at any weight. Measured — `getAnimations()`
   reported `pgin fill=both` on the card while the tilt rule was live and
   ignored. Exclusion is the only fix.
   It is also the better behaviour: nodes 4, 5 and 4a all show the SAME card,
   so it standing still while the content nudges says "one object" — exactly
   what `carryClass()`'s `holds` already does for the carried purifier. */
/* ⚠ `:not(:has(.pslot))` IS LOAD-BEARING, and its absence was a real bug.
   The exclusion list only skipped a `.pslot` that was a DIRECT child of
   `.pgt`. Node 11's slot is nested inside `.pair`, so `.pair` took the
   animation and dragged the slot with it — and `placeHero()` then read the
   slot's rect through `pgin`'s `translateX(14px)` and pinned the purifier
   render 14px right of where the layout had reserved space. Measured: slot
   left 47.0, render left 58.7, and 14px x the 0.834 phone scale is 11.7.
   This is the same failure the `carryClass()` note warns about ("every rect
   would be read through the slide's translateX"); that guard only fires when
   the purifier is already live, which it is not on the way into node 11. */
.scr.in .pgb,.scr.in .pgt>*:not(.pslot):not(:has(.pslot)):not(.dmx):not([data-tilt]){animation:pgin .28s cubic-bezier(.2,0,0,1) both}
.scr.bk .pgb,.scr.bk .pgt>*:not(.pslot):not(:has(.pslot)):not(.dmx):not([data-tilt]){animation:pgbk .28s cubic-bezier(.2,0,0,1) both}
@keyframes pgin{from{opacity:0;transform:translateX(14px)}}
@keyframes pgbk{from{opacity:0;transform:translateX(-14px)}}
.meta{width:390px;max-width:92vw;font-size:12.5px;color:var(--sec);line-height:1.55;
  text-align:center;flex:0 0 auto}
.meta b{color:var(--ink);display:block;margin-bottom:4px;font-size:13px}
@media (prefers-reduced-motion:reduce){.scr.in .pgb,.scr.in .pgt>*,.scr.bk .pgb,.scr.bk .pgt>*{animation:none}}

.sbar{height:56px;flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;
  font-size:14px;font-weight:600;padding-top:15px}
.sbar__r{display:flex;gap:5px;align-items:center}
.sig,.wf,.bt{display:block;background:var(--ink);opacity:.9}
.sig{width:17px;height:11px;clip-path:polygon(0 68%,20% 68%,20% 100%,0 100%,0 68%,27% 44%,47% 44%,47% 100%,27% 100%,27% 44%,54% 20%,74% 20%,74% 100%,54% 100%,54% 20%,80% 0,100% 0,100% 100%,80% 100%)}
.wf{width:15px;height:11px;clip-path:polygon(50% 100%,0 38%,14% 26%,50% 62%,86% 26%,100% 38%)}
.bt{width:25px;height:12px;border-radius:3.5px}
.nav{min-height:42px;flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:8px}
/* INVERTED 2026-08-18 (owner). The default used to be the dimmer translucent
   fill and hover brightened it, which reads backwards: a raised control is at
   its brightest at rest (LAW 3 — white means raised) and going DOWN under a
   finger should darken it. Default is now the bright fill; hover and press
   darken. */
.nb{width:38px;height:38px;border-radius:99px;display:grid;place-items:center;
  transition:background .16s ease,transform .16s ease}
button.nb{background:var(--panel)}
button.nb:hover{background:#EDECEA}
button.nb:active{background:#E2E1DE;transform:scale(.94)}
.nav__t{font-size:14.5px;font-weight:600;flex:1;text-align:center}
/* ⚠ The border-rotated chevron / x / plus / minus that used to live here are
   gone — all four are real glyphs from the small register now (2026-08-19).
   `.ic` is the shared class icon() emits; only flow and colour belong here,
   because the geometry is in the artwork. */
.ic{display:block;flex:0 0 auto}
.ic-chev{color:var(--ter)}
.gap{flex:1 1 auto;min-height:6px}

.t1{font-size:31px;line-height:1.12;letter-spacing:-.032em;font-weight:700;margin:0 0 9px;white-space:pre-line}
.t2{font-size:23px;line-height:1.18;letter-spacing:-.026em;font-weight:700;margin:0 0 8px}
.bd{font-size:15.5px;line-height:1.45;color:var(--sec);margin:0 0 12px}
.rd+.bd{text-align:center;font-size:16px}
.lab{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--ter);margin:24px 0 8px;font-weight:600}
/* flex columns do not collapse margins, so boundaries must not stack:
   bd already spends the 24; a label after a field tops up 12+12=24. */
.lab:first-child,.pgb .bd+.lab{margin-top:0}
.fld+.lab{margin-top:12px}
.foot{font-size:12px;line-height:1.4;color:var(--sec);margin:0 0 10px}

.viz{flex:0 0 auto;position:relative;display:grid;place-items:center;margin-bottom:14px}
.hero{flex:0 0 auto;border-radius:28px;position:relative;overflow:hidden;margin:0 -2px 16px;
  background:linear-gradient(160deg,#FFF 0%,#F2F2F2 40%,#D6D6D6 100%);box-shadow:var(--sh)}
.hero__b{position:absolute;border-radius:50%;filter:blur(28px)}
.b1{width:220px;height:220px;background:rgba(255,255,255,.95);top:-46px;right:-34px}
.b2{width:180px;height:180px;background:rgba(140,140,140,.34);bottom:24px;left:-36px}
.b3{width:130px;height:130px;background:rgba(255,255,255,.82);bottom:-26px;right:44px}
.pur{width:104px;height:150px;border-radius:34px;position:relative;
  background:linear-gradient(160deg,#FFF,#EDEDED 60%,#DBDBDB);box-shadow:var(--sh);
  display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:16px;gap:7px}
.pur--sm{width:80px;height:116px;border-radius:26px;padding-bottom:12px}
.pur--dim{opacity:.45}
.pur__ring{position:absolute;top:16px;left:50%;transform:translateX(-50%);width:44px;height:44px;
  border-radius:50%;border:2.5px solid rgba(11,11,11,.16)}
.pur--sm .pur__ring{width:34px;height:34px;top:12px}
.pur--pulse .pur__ring{border-color:rgba(11,11,11,.5);animation:pl 1.9s ease-in-out infinite}
@keyframes pl{50%{border-color:rgba(11,11,11,.12);transform:translateX(-50%) scale(1.07)}}
.pur__grill{width:38px;height:3px;border-radius:2px;background:rgba(11,11,11,.09)}
.pur--sm .pur__grill{width:28px}
.pur__arrow{position:absolute;top:74px;left:50%;transform:translateX(-50%);width:0;height:0;
  border-left:8px solid transparent;border-right:8px solid transparent;border-bottom:11px solid rgba(11,11,11,.4);
  animation:up 1.7s ease-in-out infinite}
@keyframes up{50%{transform:translate(-50%,-8px)}}
.scene{position:relative;width:250px;height:100%;display:grid;place-items:center}
.sceneq{width:200px}
.sock{position:absolute;left:8px;top:24px;width:42px;height:54px;border-radius:10px;background:var(--card);
  box-shadow:var(--shs);display:flex;align-items:center;justify-content:center;gap:8px}
.sock i{width:4px;height:13px;border-radius:2px;background:rgba(11,11,11,.26)}
.cord{position:absolute;left:48px;top:70px;width:82px;height:50px;border-bottom:2px solid rgba(11,11,11,.2);
  border-left:2px solid rgba(11,11,11,.2);border-radius:0 0 0 40px}
.ringw{position:relative;width:148px;height:148px;display:grid;place-items:center}
.ringa{position:absolute;inset:0;border-radius:50%;
  background:conic-gradient(from -90deg, rgba(11,11,11,.5) calc(var(--p)*1%), rgba(11,11,11,.09) 0);
  mask:radial-gradient(circle, transparent 59px, #000 60px);
  -webkit-mask:radial-gradient(circle, transparent 59px, #000 60px);
  animation:rot 7s linear infinite}
@keyframes rot{to{transform:rotate(360deg)}}
.ringc{width:96px;height:96px;border-radius:50%;background:var(--card);box-shadow:var(--sh)}
.hand{position:absolute;right:4px;bottom:12px;width:62px;height:104px;border-radius:22px 22px 12px 12px;
  background:var(--card);box-shadow:var(--shs)}
.waves{position:absolute;right:72px;bottom:54px;display:flex;flex-direction:column;gap:6px;align-items:flex-end}
.waves i{width:22px;height:2px;border-radius:2px;background:rgba(11,11,11,.28);animation:wv 1.7s ease-in-out infinite}
.waves i:nth-child(2){width:15px;animation-delay:.2s}.waves i:nth-child(3){width:9px;animation-delay:.4s}
@keyframes wv{50%{opacity:.25}}
.tick{width:90px;height:90px;border-radius:50%;background:var(--ink);position:relative;box-shadow:var(--sh)}
.tick::after{content:"";position:absolute;left:29px;top:36px;width:30px;height:15px;
  border-left:3px solid #fff;border-bottom:3px solid #fff;transform:rotate(-45deg)}
.wifiv{position:relative;width:100px;height:78px;display:grid;place-items:end center}
.wifiv i{position:absolute;border:2.5px solid rgba(11,11,11,.26);border-bottom-color:transparent;
  border-left-color:transparent;border-right-color:transparent;border-radius:50%;left:50%;transform:translateX(-50%)}
.wifiv i:nth-child(1){width:96px;height:96px;bottom:-6px}
.wifiv i:nth-child(2){width:64px;height:64px;bottom:-6px}
.wifiv i:nth-child(3){width:34px;height:34px;bottom:-6px}
.wifiv b{width:10px;height:10px;border-radius:50%;background:var(--ink);margin-bottom:-3px}
.bell{width:78px;height:78px;border-radius:28px 28px 20px 20px;background:var(--card);box-shadow:var(--sh);position:relative}
.bell::before{content:"";position:absolute;left:50%;top:-9px;transform:translateX(-50%);width:13px;height:13px;
  border-radius:50%;background:var(--card)}
.bell::after{content:"";position:absolute;left:50%;bottom:-10px;transform:translateX(-50%);width:24px;height:9px;
  border-radius:0 0 13px 13px;background:var(--ink);opacity:.7}
.qmark{position:absolute;right:6px;top:14px;width:36px;height:36px;border-radius:50%;background:var(--ink);
  color:#fff;display:grid;place-items:center;font-size:20px;font-weight:700;box-shadow:var(--shs)}
.clock{width:90px;height:90px;border-radius:50%;background:var(--card);box-shadow:var(--sh);position:relative}
.clock::before,.clock::after{content:"";position:absolute;left:50%;top:50%;background:var(--ink);border-radius:2px}
.clock::before{width:2.5px;height:27px;transform:translate(-50%,-100%)}
.clock::after{width:21px;height:2.5px;transform:translateY(-50%)}
.clock i{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(11,11,11,.10)}
.favs{display:flex;padding-left:14px}
.fav{width:60px;height:60px;border-radius:50%;background:var(--card);box-shadow:var(--shs);margin-left:-14px;
  border:2.5px solid rgba(255,255,255,.92)}
.fav--p{background:transparent;border:2.5px dashed rgba(11,11,11,.22);box-shadow:none}
.shield{width:84px;height:98px;background:var(--card);box-shadow:var(--sh);position:relative;
  border-radius:14px 14px 44px 44px}
.shield::after{content:"";position:absolute;left:50%;top:38px;transform:translate(-50%,0) rotate(-45deg);
  width:27px;height:14px;border-left:3px solid var(--ink);border-bottom:3px solid var(--ink);opacity:.8}
.hicon{position:relative;width:124px;height:100px}
.hicon i:nth-child(1){position:absolute;inset:28px 0 0;border-radius:18px;background:var(--card);box-shadow:var(--sh)}
.hicon i:nth-child(2){position:absolute;left:50%;top:2px;transform:translateX(-50%) rotate(45deg);
  width:64px;height:64px;border-radius:14px;background:linear-gradient(135deg,#FFF,#E4E4E4);box-shadow:var(--shs)}
.orb{width:106px;height:106px;border-radius:50%;display:grid;place-items:center;
  background:radial-gradient(circle at 32% 28%, #FFF, #DEDEDE 62%, #BDBDBD);box-shadow:var(--sh)}
.orb i{width:34px;height:34px;border-radius:50%;background:var(--ink);opacity:.86;animation:br 3.8s ease-in-out infinite}
@keyframes br{50%{transform:scale(1.15);opacity:.68}}

/* recipes.input (2026-08-18): flat white, r8, 1px hairline, h52, inner
   shadows. Raw values here because this file predates the token loader;
   build-flow.py re-states the same numbers FROM the tokens, so the flow
   rendering is the canonical one. */
.fld{background:#FFF;border-radius:8px;padding:0 16px;min-height:52px;margin-bottom:12px;
  display:flex;align-items:center;position:relative;flex:0 0 auto;
  border:1px solid rgba(0,0,0,.12);
  box-shadow:inset 0 1px 2px rgba(0,0,0,.06),inset 0 2px 6px rgba(0,0,0,.03)}
.fld.bad{border-color:var(--err);border-width:1.5px}
/* the +91 prefix and the field it shares a row with. Restored 2026-08-20:
   this block was collateral from a slice edit and the prefix rendered flush
   against the placeholder ("+91Enter number"). */
.fld__cc{font-size:16.5px;font-weight:600;color:var(--ink);flex:none;margin-right:2px}
.fld--verify{gap:10px}
.fld--verify .fi{flex:1 1 auto}
.fv{font-size:16.5px}.fp{font-size:16.5px;color:var(--ter)}
.fc{position:absolute;right:16px;bottom:8px;font-size:11px;color:var(--ter)}
.caret{width:1.6px;height:21px;background:var(--ink);margin-left:1px;animation:bl 1.05s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
.otp{display:flex;gap:9px;margin-bottom:14px;flex:0 0 auto}
.otpc{flex:1;height:60px;border-radius:16px;background:var(--card);box-shadow:var(--shs);display:grid;place-items:center}
.otpc i{width:9px;height:9px;border-radius:50%;background:var(--ink)}
.otp.bad .otpc{box-shadow:var(--shs),inset 0 0 0 1.6px var(--err)}
.chips{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:14px;flex:0 0 auto}
.chip{font-size:14.5px;padding:11px 17px;border-radius:12px;background:var(--card);box-shadow:var(--shs)}
.chip.dim{background:var(--cardq);color:var(--ter);box-shadow:none}
.chip.on{background:var(--ink);color:#fff;box-shadow:none}
.chip.on:hover{background:#232323}
.chip:hover{background:#fff}
.rows{display:flex;flex-direction:column;gap:8px;margin-bottom:14px;flex:0 0 auto}
.row{display:flex;align-items:center;gap:13px;background:var(--card);border-radius:16px;
  padding:14px 16px;min-height:60px;width:100%;box-shadow:var(--shs)}
button.row:hover{background:#fff}
.ri{width:26px;height:26px;border-radius:8px;background:rgba(11,11,11,.07);flex:0 0 auto}
.rt{flex:1;font-size:15.5px;line-height:1.25;display:flex;flex-direction:column;gap:2px}
.rs{font-size:12.5px;color:var(--ter)}
.rad,.chk{width:22px;height:22px;flex:0 0 auto;border:1.7px solid rgba(11,11,11,.28)}
.rad{border-radius:50%}.chk{border-radius:6px}
.rad.on{border-color:var(--ink);box-shadow:inset 0 0 0 5px var(--ink)}
.chk.on{border-color:var(--ink);background:var(--ink);position:relative}
.chk.on::after{content:"";position:absolute;left:5.5px;top:5px;width:9px;height:5px;
  border-left:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-45deg)}
.tog{width:44px;height:26px;border-radius:99px;background:rgba(11,11,11,.14);flex:0 0 auto;position:relative}
.tog::after{content:"";position:absolute;top:2.5px;left:2.5px;width:21px;height:21px;border-radius:50%;
  background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.22)}
.tog.on{background:var(--ink)}.tog.on::after{left:20.5px}
.bl{display:flex;flex-direction:column;gap:12px;margin-bottom:14px;flex:0 0 auto}
.bli{display:flex;gap:12px;align-items:flex-start;font-size:14.5px;line-height:1.35;color:var(--sec)}
.bln{width:24px;height:24px;border-radius:50%;background:var(--card);box-shadow:var(--shs);flex:0 0 auto;
  display:grid;place-items:center;font-size:12px;font-weight:700;color:var(--ink)}
.needs{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:14px;flex:0 0 auto}
.need{background:var(--card);border-radius:20px;padding:22px 14px;text-align:center;font-size:13.5px;
  color:var(--sec);display:flex;flex-direction:column;align-items:center;gap:13px;line-height:1.25;box-shadow:var(--shs)}
.need__i{width:44px;height:44px;border-radius:13px;background:rgba(11,11,11,.06);position:relative}
.need__i.i0{border-radius:17px}
.need__i.i1::after{content:"";position:absolute;inset:14px 13px;border-left:3px solid rgba(11,11,11,.3);
  border-right:3px solid rgba(11,11,11,.3)}
.need__i.i2::after{content:"";position:absolute;left:12px;top:15px;width:20px;height:14px;
  border:2.5px solid rgba(11,11,11,.3);border-radius:3px}
.need__i.i3::after{content:"";position:absolute;left:21px;top:12px;width:2.5px;height:12px;
  background:rgba(11,11,11,.34);box-shadow:5px 9px 0 -1px rgba(11,11,11,.34)}
.dev{display:flex;align-items:center;gap:18px;background:var(--card);border-radius:26px;padding:22px;
  width:100%;box-shadow:var(--sh);margin-bottom:14px;flex:0 0 auto}
.dev:hover{background:#fff}
.dev__v{flex:0 0 auto}
.dev__v .pur{width:74px;height:104px;border-radius:24px;padding-bottom:11px;gap:6px;box-shadow:none;
  background:linear-gradient(160deg,#FFF,#E6E6E6)}
.dev__v .pur__ring{width:30px;height:30px;top:11px;border-width:2px}
.dev__v .pur__grill{width:30px}
.dev__t{flex:1;display:flex;flex-direction:column;gap:4px}
.dev__t b{font-size:20px;letter-spacing:-.022em}
.dev__t span{font-size:13.5px;color:var(--ter)}
.note{border-left:2.5px solid var(--ink);padding:3px 0 3px 13px;margin-bottom:14px;display:flex;
  flex-direction:column;gap:3px;flex:0 0 auto}
.note b{font-size:13.5px}.note span{font-size:13.5px;line-height:1.4;color:var(--sec)}
.ban{border-radius:12px;padding:12px 14px;font-size:13.5px;line-height:1.35;margin-bottom:14px;flex:0 0 auto}
.ban.err{background:var(--errbg);color:var(--err)}
.ban.warn{background:var(--warnbg);color:var(--warn)}
.ban.ok{background:rgba(11,11,11,.06);color:var(--ink)}
.dots{display:flex;gap:8px;justify-content:center;margin-bottom:14px;flex:0 0 auto}
.dot{width:7px;height:7px;border-radius:50%;background:rgba(11,11,11,.18)}.dot.on{background:var(--ink)}
.pw{display:flex;flex-direction:column;gap:10px;margin-bottom:14px;flex:0 0 auto}
.pw span{font-size:15px;font-weight:600;text-align:center}
.sw{display:flex;flex-direction:column;align-items:center;gap:14px;flex:0 0 auto}
.sw b{font-size:18px;letter-spacing:-.02em}.sw span:not(.sp){font-size:14px;color:var(--sec);text-align:center}
.sp{width:32px;height:32px;border-radius:50%;border:2.5px solid rgba(11,11,11,.14);border-top-color:var(--ink);
  animation:rot 1s linear infinite}
@media (prefers-reduced-motion:reduce){
  .sp,.ringa,.orb i,.waves i,.pur--pulse .pur__ring,.pur__arrow{animation:none}}
.rd{position:relative;display:flex;flex-direction:column;align-items:center;flex:0 0 auto;margin-bottom:8px}
.rd__g{position:absolute;width:260px;height:260px;border-radius:50%;top:-46px;
  background:radial-gradient(circle,rgba(255,255,255,.92),rgba(255,255,255,0) 68%)}
.rd__n{font-size:128px;line-height:.92;font-weight:700;letter-spacing:-.06em;position:relative}
.rd__u{font-size:12px;letter-spacing:.18em;color:var(--ter);font-weight:600;position:relative;margin-top:2px}
.rd__s{font-size:11px;letter-spacing:.15em;color:var(--sec);position:relative;margin-top:12px}
/* redline 2026-08-18: primary 54, quiet 46, 8 apart when stacked. The height
   difference IS the hierarchy — a quiet button at the primary's height reads
   as an equal choice however pale it is. */
.cta,.cta2{border-radius:99px;padding:0;text-align:center;font-size:16.5px;font-weight:600;
  width:100%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;
  height:54px;margin-top:24px}
.cta2{height:46px;margin-top:8px}
.cta+.cta2,.cta2+.cta2{margin-top:8px}
.cta{background:var(--ink);color:#fff}
.cta:hover{background:#232323}
.cta.off{background:rgba(11,11,11,.13);color:rgba(255,255,255,.8);cursor:default}
.cta2{background:var(--card);color:var(--ink);box-shadow:var(--shs)}
.cta2:hover{background:#fff}
.two{display:flex;gap:10px;margin-bottom:10px;flex:0 0 auto}
.two .f{margin:0;width:auto;flex:1 1 0;min-width:0}
.lnk{display:block;width:100%;text-align:center;font-size:14.5px;color:var(--ink);padding:9px 0;
  margin-bottom:8px;flex:0 0 auto;text-decoration:underline;text-underline-offset:3px;
  text-decoration-color:rgba(11,11,11,.26)}
.dlgw{position:absolute;inset:0;background:rgba(0,0,0,.32);display:grid;place-items:center;padding:36px;z-index:40}
/* fill, radius, stroke and shadow are NOT here — see recipes.dialog, applied
   in the token-driven block appended at the end of this stylesheet. */
.dlg{position:relative;width:100%;text-align:center}
.dlg__b{position:relative;z-index:1;padding:20px 18px 0}
.dlg b{font-size:16px;display:block;margin-bottom:7px;line-height:1.3}
.dlg span{font-size:13px;color:var(--sec);display:block;line-height:1.4;margin-bottom:16px}
.dlg__r{display:flex;border-top:1px solid var(--hair);margin:0 -18px}
.dlg__r button{flex:1;padding:14px;text-align:center;font-size:16px}
.dlg__r button+button{border-left:1px solid var(--hair)}
.dlg__r .s{font-weight:700}
.shw{position:absolute;inset:0;background:rgba(0,0,0,.28);display:flex;align-items:flex-end;z-index:40}
.sh{background:#F7F6F5;border-radius:26px 26px 0 0;padding:24px 22px 34px;width:100%}
.toast{position:absolute;left:22px;right:22px;bottom:34px;background:var(--ink);color:#fff;
  border-radius:14px;padding:14px 16px;font-size:14px;text-align:center;z-index:30}
.kbd{margin:auto -22px -34px;background:rgba(255,255,255,.5);backdrop-filter:blur(14px);
  padding:9px 5px 30px;display:flex;flex-direction:column;gap:8px;flex:0 0 auto}
.kr{display:flex;gap:6px;justify-content:center}
.kr span{flex:1;max-width:33px;height:41px;background:#fff;border-radius:7px;display:grid;place-items:center;
  font-size:17px;box-shadow:0 1px 0 rgba(0,0,0,.13)}
.kr span.w{max-width:none;flex:4}
.kr span.g{max-width:none;flex:1.6;background:var(--ink);color:#fff;font-size:13.5px}
.tabs{display:flex;margin:auto -22px -34px;padding:12px 0 28px;border-top:1px solid var(--hair);flex:0 0 auto}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:10.5px;color:var(--ter)}
.tab i{width:24px;height:24px;border-radius:8px;background:rgba(11,11,11,.12);display:block}
.tab.on{color:var(--ink)}.tab.on i{background:var(--ink)}

/* Apple-style pairing entry */
.scan{position:relative;height:190px;border-radius:22px;background:rgba(11,11,11,.045);
  margin-bottom:18px;flex:0 0 auto;display:grid;place-items:center;overflow:hidden}
.scan__c{position:absolute;width:26px;height:26px;border:2.5px solid rgba(11,11,11,.5)}
.scan__c.c1{top:16px;left:16px;border-right:0;border-bottom:0;border-radius:8px 0 0 0}
.scan__c.c2{top:16px;right:16px;border-left:0;border-bottom:0;border-radius:0 8px 0 0}
.scan__c.c3{bottom:16px;left:16px;border-right:0;border-top:0;border-radius:0 0 0 8px}
.scan__c.c4{bottom:16px;right:16px;border-left:0;border-top:0;border-radius:0 0 8px 0}
.scan__qr{width:62px;height:62px;display:grid;grid-template-columns:1fr 1fr;gap:7px;opacity:.32}
.scan__qr i{background:var(--ink);border-radius:4px}
.scan__qr i:nth-child(3){grid-column:1/3;height:14px;align-self:end}
.mth{display:flex;gap:14px;align-items:flex-start;margin-bottom:16px;flex:0 0 auto}
.mth__i{width:30px;height:30px;flex:0 0 auto;position:relative;opacity:.8}
.mth__i--qr{border:2.5px solid var(--ink);border-radius:6px}
.mth__i--qr::after{content:"";position:absolute;inset:6px;border:2.5px solid var(--ink);border-radius:2px}
.mth__i--nfc::before,.mth__i--nfc::after{content:"";position:absolute;border:2.5px solid var(--ink);
  border-radius:50%;border-right-color:transparent;border-top-color:transparent;border-bottom-color:transparent;
  left:8px;top:3px;transform:rotate(-45deg)}
.mth__i--nfc::before{width:14px;height:24px}
.mth__i--nfc::after{width:24px;height:24px;left:2px;opacity:.45}
.mth__t{display:flex;flex-direction:column;gap:3px}
.mth__t b{font-size:15.5px}
.mth__t span{font-size:13.5px;line-height:1.4;color:var(--sec)}

/* the live group + counter — Airbnb's mechanic, our shapes */
.cnt{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;margin-bottom:6px}
.cnt__figs{height:132px;display:flex;align-items:flex-end;justify-content:center;margin-bottom:6px}
.figs{display:flex;align-items:flex-end;justify-content:center;gap:8px}
.fig{width:38px;display:flex;flex-direction:column;align-items:center;gap:5px;
  animation:figin .34s cubic-bezier(.2,.9,.25,1.08) both}
.fig i{width:24px;height:24px;border-radius:50%;background:var(--card);box-shadow:var(--shs)}
.fig b{width:34px;height:52px;border-radius:17px 17px 8px 8px;background:var(--card);box-shadow:var(--shs)}
.fig--you i,.fig--you b{background:var(--ink);box-shadow:none}
.fig.out{animation:figout .2s ease-in both}
@keyframes figin{from{opacity:0;transform:translateY(16px) scale(.7)}to{opacity:1;transform:none}}
@keyframes figout{to{opacity:0;transform:translateY(10px) scale(.7)}}
.cnt__row{display:flex;align-items:center;gap:30px;margin-bottom:4px}
.cnt__n{font-size:66px;line-height:1;font-weight:700;letter-spacing:-.05em;min-width:74px;text-align:center;
  font-variant-numeric:tabular-nums}
.cnt__n.bump{animation:bump .26s cubic-bezier(.2,.9,.25,1.1)}
@keyframes bump{40%{transform:scale(1.14)}}
.stp{width:52px;height:52px;border-radius:50%;background:var(--card);box-shadow:var(--shs);
  display:grid;place-items:center}
.stp:hover{background:#fff}
.stp[disabled]{opacity:.34;cursor:default;box-shadow:none}
/* the border-drawn plus/minus are glyphs now — geometry lives in the artwork */
.cnt__l{font-size:16px;font-weight:600;margin:6px 0 2px}
.cnt__s{font-size:13px;color:var(--ter);margin:0}

/* node 6 — choose your purifier: three SKUs, horizontal cards, stacked vertically.
   Replaces the 2×2 device-type grid (owner, 2026-08-06) — one product line, not four
   device categories. Shares .dev's card anatomy rather than inventing a new one. */
.pcard{display:flex;align-items:center;gap:16px;background:var(--card);border-radius:24px;
  padding:18px 20px;width:100%;box-shadow:var(--shs);margin-bottom:12px;flex:0 0 auto}
.pcard:hover{background:#fff}
.pcard.on{box-shadow:var(--shs),inset 0 0 0 2px var(--ink)}
/* the tile IS the wrapper now — the drawn .pur inside it became a render */
.pcard__v{flex:0 0 auto;width:56px;height:78px;border-radius:18px;
  display:grid;place-items:center;overflow:hidden;
  background:linear-gradient(160deg,#FFF,#E6E6E6)}
/* ⚠ HUE-CODED SKU THUMBNAILS — owner frame, 2026-08-17, and a REVERSAL.
   The 2026-08-12 palette rule ("outside white and grey, only the two greens
   and shades of them") deleted exactly this: three unrelated hues telling the
   three SKUs apart. The changelog for that day records the trade explicitly —
   the SKUs went to depth-within-one-family and it was noted as a WEAKER
   signal. The new frame puts hue back. Drawn as supplied because it is the
   newer instruction; flagged because both are owner instructions and only the
   owner can retire one. If the palette rule wins, delete these three rules
   and nothing else changes. */
.pcard:nth-of-type(1) .pcard__v{background:linear-gradient(160deg,#CFE3F2,#F2F7FB)}
.pcard:nth-of-type(2) .pcard__v{background:linear-gradient(160deg,#CFE6E2,#F2F9F7)}
.pcard:nth-of-type(3) .pcard__v{background:linear-gradient(160deg,#E2E0C6,#F8F7EC)}
.pcard__r{height:60px;width:auto;margin:9px 0}
.pcard__t{flex:1;display:flex;flex-direction:column;gap:2px;min-width:0}
.pcard__t b{font-size:17px;letter-spacing:-.018em}
.pcard__t span{font-size:12.5px;color:var(--sec)}
.pcard__t em{font-style:normal;font-size:11px;color:var(--ter);margin-top:2px}

/* ── node 15 — auto-advancing feature carousel over the Wi-Fi join wait.
   Crossfade at `standard`, never spring: ambient surface, motion gate 4. */
.car{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;margin-bottom:16px}
.car__w{position:relative;width:100%;height:344px}
.car__s{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  opacity:0;pointer-events:none;transition:opacity .55s cubic-bezier(.2,0,0,1)}
.car__s.on{opacity:1;pointer-events:auto}
.car__h{font-size:23.5px;line-height:1.2;letter-spacing:-.028em;font-weight:700;
  text-align:center;margin:0 0 20px;max-width:290px}
.car__shot{flex:1 1 auto;width:100%;min-height:0;display:flex;justify-content:center;
  -webkit-mask-image:linear-gradient(to bottom,#000 54%,rgba(0,0,0,0) 100%);
  mask-image:linear-gradient(to bottom,#000 54%,rgba(0,0,0,0) 100%)}
.car__ds{display:flex;gap:7px;justify-content:center;margin-top:14px}
.car__d{width:6.5px;height:6.5px;border-radius:50%;background:rgba(11,11,11,.20);padding:0;
  flex:0 0 auto;transition:background .3s cubic-bezier(.2,0,0,1)}
.car__d.on{background:var(--ink)}

/* the miniature screenshot inside a slide */
.mn{width:214px;border-radius:17px;background:#FCFCFC;box-shadow:0 8px 26px rgba(0,0,0,.10);
  padding:8px 10px 0;display:flex;flex-direction:column;gap:5px;overflow:hidden;flex:0 0 auto}
.mn__sb{display:flex;justify-content:space-between;align-items:center}
.mn__sb b{font-size:6.5px;font-weight:700}
.mn__sr{display:flex;gap:2px;align-items:center}
.mn__sr i{display:block;background:var(--ink);opacity:.85}
.mn__sr i:nth-child(1){width:7px;height:5px;
  clip-path:polygon(0 60%,22% 60%,22% 100%,0 100%,28% 40%,50% 40%,50% 100%,28% 100%,56% 18%,78% 18%,78% 100%,56% 100%,84% 0,100% 0,100% 100%,84% 100%)}
.mn__sr i:nth-child(2){width:6px;height:5px;clip-path:polygon(50% 100%,0 38%,14% 26%,50% 62%,86% 26%,100% 38%)}
.mn__sr i:nth-child(3){width:10px;height:5px;border-radius:1.5px}
.mn__g{font-size:6px;color:var(--ter);margin:2px 0 0}
.mn__h{display:flex;align-items:center;gap:4px}
.mn__h b{font-size:14px;letter-spacing:-.03em;flex:1}
.mn__o{width:12px;height:12px;border-radius:50%;background:rgba(11,11,11,.08);flex:0 0 auto}
.mn__cs{display:flex;gap:3px;overflow:hidden}
.mn__c{font-size:5.5px;line-height:1;padding:3.5px 5px;border-radius:99px;
  background:rgba(11,11,11,.05);color:var(--sec);white-space:nowrap}
.mn__c.on{background:var(--ink);color:#fff}
.mn__bd{flex:1 1 auto;display:flex;flex-direction:column;gap:5px;padding-top:2px;min-height:0}
/* rooms — the isometric tile map from the reference */
.mn__map{position:relative;flex:1 1 auto;min-height:118px;margin-top:1px;border-radius:11px;
  background:linear-gradient(165deg,#F8F7F4,#EFEEEA)}
.mn__tl{position:absolute;width:44px;height:44px;border-radius:5px;background:#fff;
  box-shadow:0 2px 6px rgba(0,0,0,.08);transform:rotate(45deg) scaleY(.56)}
.mn__tl.t1{left:22px;top:32px}
.mn__tl.t2{left:58px;top:14px}
.mn__tl.t3{left:94px;top:40px}
.mn__tl.t4{left:56px;top:58px}
.mn__pn{position:absolute;min-width:15px;height:15px;padding:0 3px;border-radius:99px;
  background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.14);font-size:6.5px;font-weight:700;
  display:grid;place-items:center}
.mn__pn.k{background:var(--ink);color:#fff}
.mn__pn.p1{left:14px;top:36px}
.mn__pn.p2{left:64px;top:16px}
.mn__pn.p3{left:104px;top:44px}
.mn__pn.p4{left:62px;top:64px}
/* agent / people / privacy bodies */
.mn__big{font-size:38px;line-height:1;font-weight:700;letter-spacing:-.055em;text-align:center;
  padding:8px 0 2px}
.mn__big em{display:block;font-style:normal;font-size:5px;letter-spacing:.16em;
  color:var(--ter);font-weight:600;margin-top:4px}
.mn__cd{background:#fff;border-radius:9px;padding:7px 8px;box-shadow:0 2px 7px rgba(0,0,0,.06);
  display:flex;flex-direction:column;gap:4px;flex:0 0 auto}
.mn__cd i{display:block;height:4px;border-radius:2px;background:rgba(11,11,11,.14)}
.mn__cd i:nth-child(2){width:62%;background:rgba(11,11,11,.08)}
.mn__cd.sm i{width:44%}
.mn__pp{display:flex;padding-left:8px;margin:8px 0 3px}
.mn__pp span{width:26px;height:26px;border-radius:50%;background:#fff;margin-left:-8px;
  border:2px solid #FCFCFC;box-shadow:0 2px 6px rgba(0,0,0,.10)}
.mn__sh{width:38px;height:44px;margin:9px auto 5px;background:#fff;border-radius:7px 7px 20px 20px;
  box-shadow:0 2px 7px rgba(0,0,0,.10);position:relative;flex:0 0 auto}
.mn__sh::after{content:"";position:absolute;left:50%;top:17px;transform:translate(-50%,0) rotate(-45deg);
  width:13px;height:7px;border-left:2px solid var(--ink);border-bottom:2px solid var(--ink);opacity:.75}
@media (prefers-reduced-motion:reduce){.car__s,.car__d{transition:none}}

/* node 7 — the filter, out of the device, still bagged */
.filt{position:relative;width:220px;height:100%;display:flex;align-items:center;
  justify-content:center;gap:26px}
.filt__b{width:82px;height:118px;border-radius:26px;position:relative;flex:0 0 auto;
  background:linear-gradient(160deg,#FFF,#E9E9E9);box-shadow:var(--sh)}
.filt__b::after{content:"";position:absolute;right:-3px;top:26px;width:24px;height:66px;
  border-radius:5px 13px 13px 5px;background:#fff;box-shadow:3px 3px 10px rgba(0,0,0,.12);
  transform-origin:left center;transform:rotate(15deg)}
.filt__f{width:50px;height:88px;border-radius:11px;background:#fff;box-shadow:var(--shs);
  display:flex;flex-direction:column;justify-content:center;gap:7px;padding:0 9px;
  position:relative;flex:0 0 auto}
.filt__f i{display:block;height:3px;border-radius:2px;background:rgba(11,11,11,.15)}
.filt__f::after{content:"";position:absolute;inset:-10px;border-radius:18px;
  border:1.6px dashed rgba(11,11,11,.32)}

/* ═══════════ node 1 — enter the home ═══════════
   Geometry is in the SVG (shared vertices, no seams possible). This file places
   the leaf over the aperture, positions copy/slider at the reference's measured
   percentages, and runs the entry. --p (0→1) comes from the drag and drives the
   leaf, the light behind the door, AND the slider's green state. */
.en{position:absolute;inset:0;margin:0;overflow:hidden;z-index:2;--p:0;background:#F2F1EF}
.en__scene{position:absolute;inset:0;overflow:hidden}
.en__world{position:absolute;inset:0;transform-origin:50% 32.7%;will-change:transform}
/* travel = scale about the aperture centre. At 6× the 134x236 doorway covers the
   whole screen, and nothing can be culled because nothing moves in Z. */
.en.go .en__world{transform:scale(6);
  transition:transform 1.15s cubic-bezier(.62,0,.36,1) .42s}
.en__cor{position:absolute;inset:0;width:100%;height:100%;display:block}

/* ── light from behind the door. NEVER a dark shadow here: dark says the space
   beyond is dark, which is the opposite of what the door is promising. White
   with the faintest green cast, brightening as the leaf cracks. ── */
.en__halo{position:absolute;left:50%;top:32.7%;width:86%;height:70%;
  transform:translate(-50%,-50%);pointer-events:none;
  background:radial-gradient(closest-side,
    rgba(255,255,255,.98) 0%, rgba(244,252,246,.62) 42%,
    rgba(247,253,248,.22) 68%, rgba(255,255,255,0) 100%);
  opacity:calc(.34 + var(--p) * .66)}
.en__pool{position:absolute;left:50%;top:44%;width:135%;height:46%;
  transform:translateX(-50%);pointer-events:none;
  background:radial-gradient(58% 100% at 50% 0%,
    rgba(255,255,255,.95) 0%, rgba(243,252,245,.46) 38%, rgba(255,255,255,0) 100%);
  opacity:calc(.40 + var(--p) * .60)}

/* the leaf, sat exactly in the aperture: 128,158 → 262,394 of 390x844.
   Its outer shadow is WHITE — light escaping past the edge, not a cast shadow. */
.en__leaf{position:absolute;left:32.82%;top:18.72%;width:34.36%;height:27.96%;
  transform-origin:left center;transform:rotateY(calc(var(--p) * -26deg));
  background:linear-gradient(97deg,#F4F3F1 0%,#FBFAF9 42%,#EDECEA 100%);
  box-shadow:inset -8px 0 18px rgba(0,0,0,.04), 0 0 0 1px rgba(11,11,11,.045),
             14px 0 34px rgba(255,255,255,.95);
  backface-visibility:hidden;will-change:transform}
.en.go .en__leaf{transform:rotateY(-105deg);
  transition:transform .75s cubic-bezier(.45,0,.2,1)}
.en__panelA,.en__panelB{position:absolute;left:11%;right:11%;border-radius:2px;
  background:rgba(11,11,11,.026);box-shadow:inset 0 0 0 1px rgba(11,11,11,.042)}
.en__panelA{top:7%;height:39%}
.en__panelB{top:52%;height:39%}
.en__knob{position:absolute;right:7%;top:50%;width:7px;height:24px;margin-top:-12px;
  border-radius:99px;background:#141414;box-shadow:0 2px 6px rgba(0,0,0,.3)}

/* copy + slider over the corridor, at the reference's measured positions */
.en__copy{position:absolute;left:0;right:0;top:67.2%;text-align:center;padding:0 24px}
.en__brand{font-size:39px;line-height:1;letter-spacing:.30em;text-indent:.30em;
  font-weight:700;margin:0 0 22px}
.en__copy p{font-size:16px;line-height:1.4;color:#7C7C79;margin:0}
.en__slider{position:absolute;left:20px;right:20px;top:85.1%;height:53px}
/* both clear to zero before the travel, so the hand-off is white on white */
.en.go .en__copy,.en.go .en__slider{opacity:0;
  transition:opacity .34s cubic-bezier(.3,0,0,1) .14s}

.en__track{position:relative;height:53px;border-radius:99px;overflow:hidden;
  background:linear-gradient(180deg,#FAFAF9,#EFEEEC);
  box-shadow:inset 0 1px 3px rgba(0,0,0,.06), inset 0 0 0 1px rgba(11,11,11,.045)}
/* the green arrives WITH THE THUMB, not after it: at 50% dragged the track is
   half green and both labels are half-way through their cross-fade. ⚠ this green
   is the owner's, and it is the only green in first run — see C-14 */
.en__fill{position:absolute;inset:0;opacity:var(--p);
  background:linear-gradient(90deg,#EAF4EB 0%,#A9CFAC 55%,#6FAE78 100%)}
.en__label{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);
  text-align:center;font-size:15.5px;pointer-events:none}
.en__label--a{color:#A2A29F;opacity:calc(1 - var(--p) * 1.25)}
.en__label--b{color:#fff;opacity:calc(var(--p) * 1.3 - .3)}
/* on a tap --p jumps 0→1, so ease it; during a drag there is no transition and
   the fill tracks the finger exactly */
.en.go .en__fill,.en.go .en__label{transition:opacity .3s cubic-bezier(.3,0,0,1)}
.en__pill{position:absolute;left:2px;top:2px;width:49px;height:49px;border-radius:50%;
  background:#1B2A1E;display:grid;place-items:center;cursor:grab;touch-action:none;
  box-shadow:0 4px 12px rgba(0,0,0,.24);will-change:transform;z-index:2}
.en__pill:active{cursor:grabbing}
.en.snap .en__pill{transition:transform .45s cubic-bezier(.34,1.5,.4,1)}
.en__arrow{display:block;width:15px;height:15px;position:relative}
.en__arrow::before{content:"";position:absolute;left:0;top:6.5px;width:14px;height:2px;
  background:#fff;border-radius:2px}
.en__arrow::after{content:"";position:absolute;right:1px;top:2.5px;width:8.5px;height:8.5px;
  border-top:2px solid #fff;border-right:2px solid #fff;transform:rotate(45deg)}
.en__pill::after{content:"";position:absolute;inset:-5px;border-radius:50%;
  border:1.5px solid rgba(11,11,11,.13);animation:pull 2.3s ease-in-out infinite}
@keyframes pull{50%{transform:translateX(9px);opacity:.25}}
.en.go .en__pill::after,.en.drag .en__pill::after{animation:none;opacity:0}

/* The white we walk into. Lives on .phone, NOT inside .scr — the screen is
   destroyed at the hand-off, so anything inside it dies mid-dissolve. This is
   what makes the next screen emerge FROM the white instead of sliding in under
   it. Sits below the island/home-bar (z 50) so the hardware stays visible. */
.en-veil{position:absolute;inset:0;background:#fff;opacity:0;z-index:45;
  pointer-events:none;transition:opacity .42s ease-in 1.25s}
.en-veil.on{opacity:1}
.en-veil.off{opacity:0;transition:opacity .6s ease-out}
@media (prefers-reduced-motion:reduce){
  .en-veil{transition:none}
  .en.go .en__world,.en.go .en__leaf,.en.go .en__copy,.en.go .en__slider{transition:none}
}

/* ═══════════ node 23 — the three tour illustrations ═══════════
   CSS keyframes only; nothing here needs wiring or teardown. */
.il{position:relative;width:100%;flex:0 0 auto;margin-bottom:16px;display:grid;place-items:center}
.il svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.il__house{fill:rgba(255,255,255,.60);stroke:rgba(11,11,11,.28);stroke-width:2.5;
  stroke-linejoin:round;filter:drop-shadow(0 12px 26px rgba(0,0,0,.10))}

/* — slide 1: readings stay inside, only outdoor air comes in — */
.il--priv .il__d{position:absolute;width:9px;height:9px;border-radius:50%;
  background:rgba(11,11,11,.40);box-shadow:0 2px 6px rgba(0,0,0,.12)}
.il--priv .d1{left:40%;top:52%;animation:dfa 7.5s ease-in-out infinite}
.il--priv .d2{left:56%;top:60%;animation:dfb 8.5s ease-in-out infinite}
.il--priv .d3{left:46%;top:70%;animation:dfc 6.8s ease-in-out infinite}
.il--priv .d4{left:60%;top:47%;animation:dfa 9.2s ease-in-out infinite reverse}
.il--priv .d5{left:37%;top:64%;animation:dfb 7.1s ease-in-out infinite reverse}
.il--priv .d6{left:52%;top:78%;animation:dfc 8.9s ease-in-out infinite}
.il--priv .d7{left:64%;top:70%;animation:dfa 6.4s ease-in-out infinite}
@keyframes dfa{25%{transform:translate(22px,-16px)}50%{transform:translate(6px,20px)}
  75%{transform:translate(-20px,4px)}}
@keyframes dfb{33%{transform:translate(-18px,14px)}66%{transform:translate(16px,-18px)}}
@keyframes dfc{20%{transform:translate(14px,12px)}55%{transform:translate(-16px,-10px)}
  80%{transform:translate(8px,-16px)}}
/* the boundary itself, breathing — the promise being kept */
.il--priv .il__seal{position:absolute;left:50%;top:57%;width:172px;height:120px;
  transform:translate(-50%,-50%);border-radius:16px;
  border:1.5px dashed rgba(11,11,11,.22);animation:seal 4.4s ease-in-out infinite}
@keyframes seal{50%{transform:translate(-50%,-50%) scale(1.045);border-color:rgba(11,11,11,.10)}}
/* one thing crosses, inward: outdoor air */
.il--priv .il__inbound{position:absolute;right:6%;top:12%;width:64px;height:64px}
.il--priv .il__inbound i{position:absolute;width:10px;height:10px;border-radius:50%;
  background:var(--ink);animation:inb 4.2s cubic-bezier(.4,0,.5,1) infinite}
@keyframes inb{0%{transform:translate(46px,-30px);opacity:0}
  22%{opacity:1}70%{transform:translate(-2px,34px);opacity:1}
  100%{transform:translate(-14px,52px);opacity:0}}

/* — slide 2: air in, clean air out, the orb never touched — */
.il--agent .il__orb{position:relative;width:118px;height:118px;border-radius:50%;
  display:grid;place-items:center;z-index:2;
  background:radial-gradient(circle at 32% 28%, #FFF, #E2E0DB 60%, #C2BFB8);
  box-shadow:0 14px 34px rgba(0,0,0,.16)}
.il--agent .il__orb i{width:40px;height:40px;border-radius:50%;background:var(--ink);
  opacity:.86;animation:br 3.6s ease-in-out infinite}
.il--agent .il__rip{position:absolute;left:50%;top:50%;width:118px;height:118px;
  border-radius:50%;border:1.5px solid rgba(11,11,11,.24);
  transform:translate(-50%,-50%);animation:rip 3.9s cubic-bezier(.2,.6,.3,1) infinite}
.il--agent .r2{animation-delay:1.3s}
.il--agent .r3{animation-delay:2.6s}
@keyframes rip{0%{transform:translate(-50%,-50%) scale(1);opacity:.75}
  100%{transform:translate(-50%,-50%) scale(2.35);opacity:0}}
.il--agent .il__spec{position:absolute;width:7px;height:7px;border-radius:50%;
  background:rgba(11,11,11,.34)}
.il--agent .s1{left:6%;top:26%;animation:sk1 3.4s ease-in infinite}
.il--agent .s2{right:8%;top:20%;animation:sk2 3.9s ease-in infinite .5s}
.il--agent .s3{left:12%;bottom:22%;animation:sk3 3.6s ease-in infinite 1.1s}
.il--agent .s4{right:10%;bottom:26%;animation:sk4 4.1s ease-in infinite 1.7s}
.il--agent .s5{left:44%;top:6%;animation:sk5 3.7s ease-in infinite 2.2s}
.il--agent .s6{left:50%;bottom:6%;animation:sk6 4.0s ease-in infinite 2.8s}
@keyframes sk1{0%{opacity:0}20%{opacity:1}100%{transform:translate(112px,64px) scale(.3);opacity:0}}
@keyframes sk2{0%{opacity:0}20%{opacity:1}100%{transform:translate(-104px,74px) scale(.3);opacity:0}}
@keyframes sk3{0%{opacity:0}20%{opacity:1}100%{transform:translate(96px,-58px) scale(.3);opacity:0}}
@keyframes sk4{0%{opacity:0}20%{opacity:1}100%{transform:translate(-92px,-66px) scale(.3);opacity:0}}
@keyframes sk5{0%{opacity:0}20%{opacity:1}100%{transform:translate(6px,104px) scale(.3);opacity:0}}
@keyframes sk6{0%{opacity:0}20%{opacity:1}100%{transform:translate(-4px,-96px) scale(.3);opacity:0}}
/* two small receipts, because the agent reports what it did */
.il--agent .il__tick{position:absolute;width:26px;height:26px;border-radius:50%;
  background:#fff;box-shadow:var(--shs);opacity:0}
.il--agent .il__tick::after{content:"";position:absolute;left:8px;top:9px;width:9px;height:5px;
  border-left:2px solid var(--ink);border-bottom:2px solid var(--ink);transform:rotate(-45deg)}
.il--agent .t1{left:16%;top:16%;animation:pop 5.2s ease-in-out infinite 1.4s}
.il--agent .t2{right:14%;bottom:18%;animation:pop 5.2s ease-in-out infinite 3.6s}
@keyframes pop{0%{opacity:0;transform:scale(.5)}12%{opacity:1;transform:scale(1)}
  40%{opacity:1;transform:scale(1)}55%{opacity:0;transform:scale(.9)}}

/* — slide 3: one hub, four devices, wires drawing in turn — */
.il--home .il__wire{fill:none;stroke:rgba(11,11,11,.34);stroke-width:2;stroke-linecap:round;
  stroke-dasharray:76;stroke-dashoffset:76;animation:wire 6.4s ease-in-out infinite}
.il--home .w2{animation-delay:.5s}
.il--home .w3{animation-delay:1.0s}
.il--home .w4{animation-delay:1.5s}
@keyframes wire{0%{stroke-dashoffset:76}22%{stroke-dashoffset:0}
  76%{stroke-dashoffset:0}100%{stroke-dashoffset:-76}}
.il--home .il__hub{position:absolute;left:50%;top:62%;width:38px;height:38px;border-radius:50%;
  transform:translate(-50%,-50%);background:var(--ink);z-index:2;
  box-shadow:0 6px 18px rgba(0,0,0,.28)}
.il--home .il__hub::after{content:"";position:absolute;inset:-9px;border-radius:50%;
  border:1.5px solid rgba(11,11,11,.2);animation:seal 3.2s ease-in-out infinite}
.il--home .il__nd{position:absolute;width:30px;height:30px;border-radius:11px;background:#fff;
  box-shadow:var(--shs);opacity:.42;animation:lit 6.4s ease-in-out infinite}
.il--home .il__nd.on{opacity:1}
.il--home .n1{left:24%;top:41%}
.il--home .n2{right:24%;top:41%;animation-delay:.5s}
.il--home .n3{left:22%;top:72%;animation-delay:1.0s}
.il--home .n4{right:21%;top:72%;animation-delay:1.5s}
@keyframes lit{0%,18%{transform:scale(1)}26%{transform:scale(1.16)}40%,100%{transform:scale(1)}}

@media (prefers-reduced-motion:reduce){
  .il *,.il__seal,.il__hub::after{animation:none !important}
}

/* ═══════════ node 7 — peel the wrapper ═══════════ */
.pl{position:relative;height:236px;flex:0 0 auto;margin-bottom:14px;display:grid;place-items:center}
.pl__filter,.pl__wrap{position:absolute;width:150px;height:190px;border-radius:16px}
.pl__filter{background:linear-gradient(170deg,#FFF,#F0EFEC);box-shadow:var(--sh);
  display:flex;flex-direction:column;justify-content:center;gap:11px;padding:0 20px}
.pl__filter i{display:block;height:8px;border-radius:3px;background:rgba(11,11,11,.10)}
.pl__wrap{background:linear-gradient(150deg,rgba(214,222,228,.90),rgba(188,199,208,.86));
  box-shadow:0 8px 22px rgba(0,0,0,.14), inset 0 0 0 1px rgba(255,255,255,.55);
  overflow:hidden;touch-action:none;will-change:clip-path}
.pl__sheen{position:absolute;left:-40%;top:-30%;width:70%;height:170%;transform:rotate(18deg);
  background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.75),rgba(255,255,255,0))}
.pl__tab{position:absolute;top:9px;width:70px;height:30px;border-radius:99px;
  background:var(--ink);color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.26);cursor:grab;
  touch-action:none;z-index:3;display:grid;place-items:center}
.pl__tab::after{content:"";width:22px;height:3px;border-radius:2px;background:rgba(255,255,255,.85);
  box-shadow:0 5px 0 rgba(255,255,255,.5)}
.pl__tab:active{cursor:grabbing}
.pl.anim .pl__wrap,.pl.anim .pl__tab{transition:clip-path .5s cubic-bezier(.3,0,0,1),
  transform .5s cubic-bezier(.3,0,0,1),opacity .4s}
.pl.done .pl__wrap{opacity:0;transform:translateY(34px) rotate(6deg)}
.pl.done .pl__tab{opacity:0}
.pl__hint{position:absolute;bottom:2px;left:0;right:0;text-align:center;margin:0;
  font-size:12px;color:var(--ter);pointer-events:none}
.pl__hint span{animation:bob 2.2s ease-in-out infinite;display:inline-block}
@keyframes bob{50%{transform:translateY(5px)}}
.pl.done .pl__hint{opacity:0;transition:opacity .2s}

/* ═══════════ node 11 — hold to pair ═══════════ */
.hr{position:relative;width:210px;height:210px;flex:0 0 auto;margin:2px auto 16px;
  display:grid;place-items:center}
.hr__svg{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg)}
.hr__bg{fill:none;stroke:rgba(11,11,11,.10);stroke-width:7}
.hr__fg{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round;
  stroke-dasharray:540;stroke-dashoffset:540}
.hr__core{position:absolute;display:grid;place-items:center}
.hr__btn{position:absolute;inset:0;border-radius:50%;touch-action:none;cursor:pointer;
  display:grid;place-items:end center;padding-bottom:12px}
.hr__btn span{font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
  color:var(--ter);transition:color .25s}
.hr.on .hr__btn span{color:var(--ink)}
.hr.on .hr__core{transform:scale(1.06);transition:transform .5s cubic-bezier(.34,1.4,.5,1)}
.hr.done .hr__core{transform:scale(1.14)}

/* ═══════════ node 17 — the morphing room ═══════════ */
/* In the content flow now, not the visual half (owner, 2026-08-18), so the
   stage runs shorter — it shares a screen with a field, a chip strip and a
   CTA rather than owning the top half. */
/* `.rs` has to be able to grow for `.rs__stage`'s `flex:1` to mean anything —
   a flex child of a fixed-height parent has nothing to claim. */
.rs{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;margin:4px 0 10px}
/* ⚠ WRAPS, DOES NOT SCROLL — changed 2026-09-09 and for a reason worth
   keeping. This was a horizontally scrolling rail with edge-to-edge negative
   margins. That was fine while every item was a room, but the custom-room tab
   the owner asked for lands LAST, and with six rooms ahead of it it sat off the
   right edge — an option you cannot see is not an option. Wrapping costs one
   extra row of height and makes all seven choices visible at once, which the
   taller stage can easily afford. */
.rs__bar{display:flex;flex-wrap:wrap;gap:7px;padding:3px 0 9px}
.rs__t{flex:0 0 auto;font-size:14px;padding:10px 15px;border-radius:12px;white-space:nowrap;
  background:var(--card);box-shadow:var(--shs);
  transition:background .28s cubic-bezier(.2,0,0,1),color .28s cubic-bezier(.2,0,0,1)}
.rs__t:hover{background:#fff}
.rs__t.on{background:var(--ink);color:#fff;box-shadow:none}
/* ⚠ THE STAGE GROWS; IT NO LONGER HAS A FIXED HEIGHT. Owner, 2026-09-09:
   "there's a ton of empty space... the illustration part can be longer." It was
   168px tall and measured 191px of dead space between it and the CTA. `flex:1`
   hands that space to the drawing instead, and `xMidYMax` in the markup keeps
   the floor anchored to the bottom edge while the extra height becomes headroom
   above the room — so the room does not float as the stage resizes.
   `min-height` is the floor for a short viewport, not the target. */
.rs__stage{flex:1 1 auto;min-height:190px;border-radius:22px;position:relative;
  overflow:hidden;
  background:linear-gradient(168deg,#FBFAF8 0%,#F1F0EC 52%,#E6E4DE 100%);
  box-shadow:var(--shs),inset 0 0 0 1px rgba(255,255,255,.72)}
.rs__stage svg{position:absolute;inset:0;width:100%;height:100%}

/* ═══════════ shared: reduced motion kills every one of these ═══════════ */
@media (prefers-reduced-motion:reduce){
  .dw.anim .dw__panel,.dw.snap .dw__panel,.pl.anim .pl__wrap,.pl.anim .pl__tab,
  .hr.on .hr__core,.rs__t{transition:none}
  .dw__hint span,.pl__hint span{animation:none}
}

/* node 5 — email */
.mail{width:114px;height:80px;border-radius:14px;background:var(--card);box-shadow:var(--sh);
  position:relative;overflow:hidden}
.mail::before,.mail::after{content:"";position:absolute;top:15px;width:68px;height:2.5px;
  border-radius:2px;background:rgba(11,11,11,.30)}
.mail::before{left:7px;transform-origin:left center;transform:rotate(31deg)}
.mail::after{right:7px;transform-origin:right center;transform:rotate(-31deg)}

/* node 24 — geofence */
/* ── node 24 · geofencing ────────────────────────────────────────────────
   The plate is the owner's SVG (design-elements/illustrations/geofencing.svg),
   MINUS its green dot — see _geofence(). SQUARE, because the supplied ring
   spans ~92% of a square viewBox and the old 184x152 card would have clipped
   it top and bottom. The card, its radius and its shadow are unchanged, which
   is the "keep the visuals the same" half of the instruction.
   ⚠ Every number below comes from __GEO*__ placeholders resolved in
   css_out() from the SVG itself. Do not hardcode them back. */
.geo{position:relative;width:190px;height:190px;border-radius:24px;
  background:var(--card) __GEOPLATE__ center/86% auto no-repeat;
  box-shadow:var(--sh);overflow:hidden}
/* the "you" dot — the one piece that moves. It rests OUTSIDE the dashed
   boundary and crosses it, which is the whole point of the illustration.
   The travel is a multiple of the dot's own size, so it scales with the card
   (translate percentages resolve against the element, not the parent). */
.geo u{position:absolute;left:__GEOL__%;top:__GEOT__%;
  width:__GEOSZ__%;aspect-ratio:1;border-radius:50%;background:__GEOFILL__;
  box-shadow:0 0 6px __GEOFILL__;animation:geoDrift 6s ease-in-out infinite}
@keyframes geoDrift{50%{transform:translate(__GEOTX__%,__GEOTY__%)}}

/* node 11 — pairing link */
.link{position:absolute;left:24px;top:50%;transform:translateY(-50%);display:flex;gap:7px}
.link i{width:8px;height:8px;border-radius:50%;background:rgba(11,11,11,.3);
  animation:hop 1.5s ease-in-out infinite}
.link i:nth-child(2){animation-delay:.16s}
.link i:nth-child(3){animation-delay:.32s}
@keyframes hop{50%{transform:translateY(-7px);opacity:.4}}
@media (prefers-reduced-motion:reduce){.geo u,.link i{animation:none}}

/* ── controller: left rail, matching the My Home harness */
.shell{display:grid;grid-template-columns:clamp(238px,30%,400px) minmax(0,1fr);height:100vh}
.ctrl{background:var(--panel);overflow-y:auto;padding:34px 30px 46px;
  border-right:1px solid var(--hair);border-bottom:0;max-height:none;flex:none}
.ctrl__inner{max-width:400px;margin:0}
.ctrl__head{margin-bottom:22px}
.ctrl h1{font-size:26px;line-height:1.1;margin:0 0 9px}
.lede{font-size:13px;margin:0}
.cl{margin:24px 0 9px}
.cl:first-of-type{margin-top:0}
.ctrl__grid{display:block}
.panel,.panel--wide{max-width:none;min-width:0;margin-bottom:0}
.src{border:1px solid var(--hair);border-radius:12px;padding:12px 13px;display:flex;
  flex-direction:column;gap:6px}
.src b{font-size:13px}
.src span{font-size:11.5px;color:var(--ter);line-height:1.45}
.src em{font-style:normal;font-size:11.5px;line-height:1.5;color:var(--sec);
  border-top:1px solid var(--hair);padding-top:8px;margin-top:2px}
.posn{font-size:11.5px}
.jump{max-height:min(38vh,420px)}
.ji{padding:8px 10px}
.jin{min-width:26px;font-size:9.5px}
.ji.sub .jin{visibility:hidden}
.stage{justify-content:center;padding:24px 16px 24px 26px;overflow:hidden}
@media (max-width:1100px){
  .ctrl{padding:24px 20px 34px}
  .ctrl h1{font-size:21px}
  .lede{font-size:12px}
  .meta{display:none}
  .jump{max-height:min(30vh,300px)}
}
/* only collapse when a side-by-side genuinely cannot work */
@media (max-width:560px){
  .shell{grid-template-columns:1fr}
  .ctrl{max-height:44vh}
  .stage{padding:18px 12px}
}

/* ── the page layout, owner frames 2026-08-17 ────────────────────────────
   Visual on top taking the leftover height, content pinned to the bottom.
   `:has(.pgb)` is the switch, so screens that have not been converted keep
   the old top-aligned padding untouched. */
.scr:has(.pgb){padding:0}
.scr:has(.pgb) .sbar{padding:15px 22px 0}
/* The back arrow floats over the visual rather than sitting in a nav row, and
   the empty right-hand slot goes with it — the frames carry a back arrow and
   nothing else, so there is no close (×) to reserve room for. */
.scr:has(.pgb) .nav{position:absolute;top:60px;left:22px;right:22px;z-index:30;
  min-height:0;pointer-events:none}
.scr:has(.pgb) .nav button{pointer-events:auto}
/* The empty right-hand slot keeps its space so a centred nav title stays
   centred, but shows nothing — the frames have a back arrow and no close. */
.scr:has(.pgb) .nav span.nb{visibility:hidden}
.scr:has(.pgb) .nav__t:empty{display:none}
.scr:has(.pgb) .nav__t{font-size:19px;font-weight:700;letter-spacing:-.02em}
/* A column rather than a centring grid: `place-items:center` sizes children to
   their content, which squeezed the node-15 carousel to one word per line and
   clipped the node-17 room picker. Everything centres, and anything that wants
   the full width can have it. */
.pgt{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;position:relative;
  overflow:hidden;padding:8px 22px 0}
/* node 4's card is the tallest thing any visual half holds — give it real
   air top and bottom rather than letting it touch the header and the fields */
/* +24px on 2026-08-17, +20px more on 2026-08-18 (owner: still too high;
   "18 or 24, you make that call") — 70px balances the card between the nav
   title above and the NAME field below. */
/* UNCLIPPED, and the padding rebalanced for the smaller card. 0.9x still does
   not fit the content box, so the card is allowed to overflow rather than be
   cropped — which is what "unclip the image" asks for.
   ⚠ Unclipping is only safe because the flip's travel was shortened to match
   (see `kcardIn`): at the old -104px the entering card would now escape over
   the nav instead of being hidden by this clip. The two are a pair — do not
   change one without the other. */
/* The padding is held in custom properties rather than repeated, because two
   hardcoded copies of these numbers is how that kind of thing drifts.
   (This used to point at `.ksucc .dmx`, which cancelled them exactly. That
   layout was deleted on 2026-08-20 when node 5c moved onto `.ccol`; the
   full-bleed matrix is handled by the `:has(.ccol):has(.dmx)` rules now.) */
.pgt:has(.kcard){--pgtx:22px;--pgty:44px;--pgtb:14px;
  padding:var(--pgty) var(--pgtx) var(--pgtb);overflow:visible}
.pgt > *{max-width:100%}
.pgt .viz{margin-bottom:0}
/* the two visuals that are laid out rather than drawn, and need the width */
.pgt .car,.pgt .rs{width:100%;margin-bottom:0}
.pgt .rs__bar{margin:0;padding-left:0;padding-right:0}
/* Same discipline as the sheet: UA block margins are zeroed so the rhythm
   values are the ONLY vertical spacing.
   ⚠ `:not([class])` matters. The first version was `.pgb p` (0,1,1), which
   OUT-SPECIFIES `.eyb` and `.lab` (0,1,0) and silently zeroed the very
   margins the rhythm sets — the eyebrow ended up touching the heading. The
   reset now only claims elements that have no component rule of their own. */
.pgb p:not([class]),.pgb h1:not([class]),.pgb h2:not([class]){margin:0}
.pgb{flex:0 0 auto;display:flex;flex-direction:column;padding:14px 20px 34px}

/* ── TOP-ALIGNED PAGES (owner, 2026-08-19) ──────────────────────────────
   Any page whose content half carries a LIST. Bottom-pinned, a list grows
   UPWARD — each arriving item makes `.pgb` taller, which shrinks `.pgt`,
   which slides the icon and heading up the screen. Owner: "after every new
   item appears the icon and header body keeps shifting up."

   The fix is to stop `.pgt` absorbing the leftover height and give it to
   `.pgb` instead: the visual half sizes to its own content and stays put,
   and the list grows downward into space that was already empty.

   ⚠ Ordering, not weight: `.pgb--top` is (0,1,0), the same as the `.pgb`
   rule directly above, so it wins by coming after it. Do not "fix" that by
   adding a parent selector, and do not move this block above `.pgb`. The
   `.pgt` override IS higher-specificity and so is order-independent. */
/* ── A REAL TOP NAVIGATION BAR ───────────────────────────────────────────
   Owner, 2026-08-19: "think of the back button being on a top navigation bar.
   So nothing will overlap that. The Bluetooth icon and the connect Bluetooth
   and all those things will come below that."

   On hero pages the nav is ABSOLUTE and floats over the visual half — fine
   there, because that half is always tall. On a top-aligned page it is not
   fine: the content starts at the top, so it slid straight under the nav and
   the eyebrow collided with the back arrow (R1, R2, P1). A previous pass tried
   to buy clearance with `min-height` on `.pgt`; that is a spacer pretending to
   be a bar, and it broke again the moment a page had no visual half.

   The bar is now IN FLOW on these screens and reserves its own height, so
   nothing below it can ever ride up into it — the structural fix rather than
   another measured gap.

   ⚠ `.pgb.pgb--top` (0,4,0) beats `.scr:has(.pgb) .nav` (0,3,0) on WEIGHT.
   Written that way on purpose: at equal specificity this would depend on
   source order, which is how two animations were silenced a pass earlier. */
.scr:has(.pgb.pgb--top) .nav{position:static;z-index:auto;pointer-events:auto;
  min-height:44px;padding:4px 22px 0;margin-bottom:2px}
.scr:has(.pgb.pgb--top) .nav span.nb{visibility:hidden}
/* ── and the same for the centred column (nodes 5a, 5b) ──────────────────
   `.ccol` is top-aligned content too, so gate 6 applies to it verbatim: a
   floating nav let the heading start at the very top of the screen, which
   measured 11.6% against the owner's ~18-20% and read as the title hanging
   off the back button. Reserving the bar's height fixes it STRUCTURALLY —
   the alternative was a `padding-top` on `.ccol`, i.e. buying clearance with
   a measured gap, which is exactly what the note above says not to do.
   `margin-bottom` is larger here than on the `.pgb--top` screens because
   those put a glyph under the bar and these put a 28px heading. */
/* ⚠ NO HORIZONTAL PADDING. Owner, 2026-08-20: "the back button on the top
   left placement keeps changing, use page 6 back button placement". It was
   DOUBLE-INSET here and measured 44px against node 6's 22: `.scr` already
   pays 22px on these screens (`.scr:has(.pgb){padding:0}` never matches a
   `.ccol` screen, so the screen keeps its own padding) and the bar was
   adding another 22 on top. The `.pgb--top` rule above needs its 22 for the
   opposite reason — there `.scr`'s padding IS zeroed. Same visual result,
   two different sums; that is exactly why this drifted. */
.scr:has(.ccol) .nav{position:static;z-index:auto;pointer-events:auto;
  min-height:44px;padding:4px 0 0;margin-bottom:26px}
.scr:has(.ccol) .nav span.nb{visibility:hidden}
.scr:has(.pgb--top) .pgt{flex:0 0 auto;justify-content:flex-start;overflow:visible}
.pgb--top{flex:1 1 auto;min-height:0;justify-content:flex-start}
/* The CTA keeps the bottom edge — only the content above it is top-aligned.
   `margin-top:auto` on the primary eats the slack, and a stacked `.cta2`
   rides along on its own 8px. A `foot()` between the list and the CTA stays
   with the LIST, which is correct: it explains the list, not the button. */
.pgb--top .cta{margin-top:auto}
/* RHYTHM (owner 2026-08-18, tokens: rhythm.textGap/sectionGap = 12/24):
   12 between pieces of one text set, 24 between blocks. Raw numbers here
   because this file predates the loader; the values ARE the tokens. */
/* THE ALL-CAPS -> HEADING PAIR. 12 everywhere, no exceptions (owner
   2026-08-18). An eyebrow is a label FOR the heading under it, so the pair
   has to read as one unit — which is exactly the gap that broke when the
   reset above out-specified this rule. */
.eyb{font-size:12px;letter-spacing:.085em;text-transform:uppercase;font-weight:600;
  color:var(--sec);margin:0 0 12px}
/* The page title runs SMALLER than the sign-in sheet's. Measured off the
   frames rather than assumed: cap height ≈ 17pt against the CTA label's 11pt,
   which puts it at typography.scale.title1 (26) and not `display` (30). It
   reads correctly — the sheet is one big statement on a compact surface,
   these screens carry two paragraphs and a list under the same heading. */
.pgb .t1{font-size:26px;line-height:1.16;letter-spacing:-.024em;margin:0 0 12px}
.pgb .bd{font-size:15px}
/* field() is a real <input> now — strip the UA chrome so it reads as the
   typed value it replaced, not as a form control. */
.fi{width:100%;border:0;background:none;outline:0;font:inherit;font-size:16.5px;
  font-weight:600;letter-spacing:-.005em;color:var(--ink);padding:0;min-width:0}
.fi::placeholder{color:var(--ter);font-weight:400}
.fld:focus-within{border-color:rgba(0,0,0,.34);
  box-shadow:inset 0 1px 2px rgba(0,0,0,.06),inset 0 2px 6px rgba(0,0,0,.03)}
.pgb .bd{margin:0 0 12px}
.pgb .bd:last-of-type{margin-bottom:24px}
.qlink{display:block;width:100%;text-align:center;font-size:15.5px;font-weight:600;
  color:var(--ter);padding:11px 0 0;flex:0 0 auto}
.qlink:hover{color:var(--sec)}
/* the tappable tail of an info line — inherits the line's size and colour so
   it reads as part of the sentence, and only the weight marks it */
.infoln__a{background:none;border:0;padding:0;font:inherit;color:var(--ink);
  font-weight:600;cursor:pointer;text-underline-offset:2px;text-decoration:underline}
.infoln{display:flex;gap:9px;align-items:flex-start;font-size:13px;line-height:1.4;
  color:var(--sec);margin:2px 0 16px}
/* ⚠ No border and no ::before/::after. The Lucide glyph draws its own ring and
   dot; the old CSS drew a ring AROUND it, which would have doubled the circle,
   and its width/height would have overridden the glyph's own size. */
.ic-i{flex:0 0 auto;color:var(--ter);margin-top:1px}

/* ── the key card catches light ──────────────────────────────────────────
   Owner, 2026-08-19 (second pass): the first build was "too much" — a smooth
   rainbow wash over the whole PNG, permanently on. From the reference it is
   "only a shimmer which is kind of a dotted visual pattern", a speckled patch
   that on movement "appears as a slight strip", and it appears ONLY when moved.

   So it is ONE layer now, not five: a rainbow gradient seen through a DOT GRID,
   intersected with a soft patch that the tilt moves. The dots ARE the effect;
   the gradient only colours them.

   ⚠ CLIPPED TO THE ARTWORK'S FACE, NOT THE PNG BOX. key-card.webp is an outer
   TRAY with the real card face inset inside it, so `inset:0` spilled the
   shimmer across the tray and its corner followed nothing. The insets and
   radius below are MEASURED off the alpha channel — see recipes.cardShimmer.

   ⚠ `--gx/--gy/--gi` are set by JS and default to 0, so with no runtime (the
   flat board, the wireframes) the card is simply a clean card — not a
   half-lit one.

   ⚠ `isolation:isolate` is load-bearing: the speckles blend, and without a
   stacking context they would blend with the PAGE, lighting the ground. */
.kcard{--gx:0;--gy:0;--gi:0;isolation:isolate}
/* the tilt. Small — motion.tokens.js `gyro.maxTiltDeg`: past ~10deg a card
   stops reading as a lit surface and starts reading as a 3D toy. */
.kcard[data-tilt]{
  transform:perspective(900px)
    rotateY(calc(var(--gx) * __SHIMTILT__deg))
    rotateX(calc(var(--gy) * -__SHIMTILT__deg));
  will-change:transform}
/* ⚠ No bloom / drop-shadow glow any more: it lit the area OUTSIDE the card,
   which was half of "it's going way out". */

/* the face. Every number measured from the artwork (cardShimmer.face). */
.kfx{position:absolute;z-index:3;pointer-events:none;overflow:hidden;
  left:__FACEL__%;right:__FACER__%;top:__FACET__%;bottom:__FACEB__%;
  border-radius:__FACERX__%/__FACERY__%;
  /* ⚠ opacity is PURELY deflection — no resting shimmer. "Only when moved." */
  opacity:calc(var(--gi) * __SHIMMAX__)}

/* THE SPECKLE. Two masks intersected: a dot grid, and a soft patch the tilt
   drags around. `mask-composite` is what makes it an intersection — without it
   the layers union and the whole face fills with dots. */
.kfx__spk{position:absolute;inset:-14%;mix-blend-mode:__SHIMBLEND__;
  background:conic-gradient(from calc(var(--gx) * 120deg + var(--gy) * 40deg),
             __SHIMHOLO__);
  -webkit-mask-image:
    radial-gradient(circle at 50% 50%, #000 __DOTR__%, transparent calc(__DOTR__% + 6%)),
    radial-gradient(__PATCHW__% __PATCHH__% at
      calc(50% + var(--gx) * 26%) calc(50% + var(--gy) * -26%),
      #000 0%, rgba(0,0,0,.55) 46%, transparent 82%);
  mask-image:
    radial-gradient(circle at 50% 50%, #000 __DOTR__%, transparent calc(__DOTR__% + 6%)),
    radial-gradient(__PATCHW__% __PATCHH__% at
      calc(50% + var(--gx) * 26%) calc(50% + var(--gy) * -26%),
      #000 0%, rgba(0,0,0,.55) 46%, transparent 82%);
  -webkit-mask-size:__DOTPX__px __DOTPX__px, 100% 100%;
  mask-size:__DOTPX__px __DOTPX__px, 100% 100%;
  -webkit-mask-repeat:repeat, no-repeat;
  mask-repeat:repeat, no-repeat;
  -webkit-mask-composite:source-in;
  mask-composite:intersect}

/* the edge catch — the owner asked for corners by name. Deflection-only and
   much quieter than the first pass. */
.kfx__rim{position:absolute;inset:0;border-radius:inherit;
  mix-blend-mode:multiply;
  box-shadow:inset 0 0 0 1px __SHIMRIMT__calc(var(--gi) * __SHIMRIM__));
  background:linear-gradient(calc(90deg + var(--gx) * 70deg),
    __SHIMRIMT__calc(var(--gi) * __SHIMRIM__)) 0%,
    rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%,
    __SHIMRIMT__calc(var(--gi) * __SHIMRIM__ * .7)) 100%)}

/* ⚠ OFF where it does not belong. Owner: the effect lives on nodes 4, 5 and 4a
   and nowhere else — so `data-tilt` is only emitted there. These two rules are
   belt-and-braces for the cards that exist elsewhere: the 0.2x travelling mini
   (invisible, and a blend per frame) and the door's card, whose DRAG owns
   `transform`. */
.khero .kfx{display:none}
.dk__card .kcard[data-tilt]{transform:none}
@media (prefers-reduced-motion:reduce){
  .kcard[data-tilt]{transform:none}
  .kfx{opacity:0}
}

/* ── the master key card — owner artwork, 2026-08-20 ─────────────────────
   Five colourways of ONE piece of art. `data-kc` on `.phone` selects; the card
   itself never carries the choice, so the three cards that can be alive at
   once (node 5b's, the travelling mini, the door's) cannot disagree about
   which key you made. Same reasoning as `.phone.sku-*` for the purifier.
   Every position below is a PERCENTAGE of the card, measured against the new
   art, so the whole thing scales as one object. */
/* ⚠ `container-type:inline-size` IS THE FIX FOR "out of bounds of the card
   scale" (owner, 2026-08-20). Everything on the card used to be sized in
   FIXED px while the card itself is drawn at four different widths — 264 on
   node 5b, 100% of the wallet pocket on 5a, 0.2x as the travelling mini,
   and again at the door. Fixed type against a variable card means the
   identity block fits at exactly one of those sizes and overflows at the
   others. Every dimension on the card is `cqw` now — a percentage of the
   CARD, so the whole thing scales as one object at any width.
   ⚠ Do not put a raw px font-size back on a `.kcard__*` rule. */
/* ⚠ ONE width for the card, and the wallet is DERIVED from it. The sleeve
   holds the card between `left:6.5%` and `right:6.5%`, so a wallet of width
   W shows a card of 0.87W — which is how 5a's card came out 5px narrower
   than 5b's and read as a slight grow between the two screens. Deriving the
   wallet means the two can no longer disagree. */
.kcard{position:relative;width:var(--kcw,264px);aspect-ratio:__CARDAR__;flex:0 0 auto;
  container-type:inline-size;
  background:var(--kc1) center/100% 100% no-repeat}
.phone[data-kc="2"] .kcard{background-image:var(--kc2)}
.phone[data-kc="3"] .kcard{background-image:var(--kc3)}
.phone[data-kc="4"] .kcard{background-image:var(--kc4)}
.phone[data-kc="5"] .kcard{background-image:var(--kc5)}

/* THE IDENTITY BLOCK, bottom-left. The art engraves "MASTER KEY" at the top
   and centres the key mark, so the only free space is the lower band. Inset
   to the artwork's own FACE (measured, see CARD_FACE) plus a little breathing
   room, not to the file's box — the file has a soft glow around it. */
/* 14%/11% — the artwork's printed face starts 8.14% in from the left, so
   11.5% left only 3.4% of clearance and the avatar read as sitting ON the
   card's edge rather than inside it. */
/* ⚠ `text-align:left` is load-bearing, not decoration. Node 5a centres its
   whole column (`.ccol`), and the card inherited it — NAME sat centred
   over RUHAAN ROYCE on the wallet screen and left-aligned on node 5b, the
   same card reading two ways depending on the page around it. */
/* Measured against the face, not the file: the printed face runs 8.14% to
   91.78% across and ends 91.3% down. The block was at bottom:8.5%, which
   put its baseline 0.2% BELOW the face — outside the card by measurement,
   not by eye. 11.5% clears it with room to spare. */
/* [OWNER 2026-08-20] The row is spelled out:
       12px > DP container > 4px > edit icon > 8px > name & number
   In `cqw`, so it holds at every card width (1cqw = 1% of the card):
       12px = 4.55cqw   4px = 1.52cqw   8px = 3.03cqw   at the 264px card
   The 12px is measured from the artwork's printed FACE (8.14%), which is
   the card's visible edge — the file has a soft glow outside it that no one
   would measure to. Hence left = 8.14 + 4.55 = 12.69cqw.
   ⚠ `gap` is 0 on purpose: a single flex gap cannot express 4px then 8px,
   and using one value for both is how the spacing would quietly become
   'whatever looked fine'. The two gaps are margins on the items they
   precede, so each is named where the owner named it. */
/* Two owner passes, both in the card's own units so the offsets hold at every
   card size: +24 right / +24 up on 2026-08-20, then 12 back left and 4 back
   down. Net +12 right, +20 up from where it started.
     left    12.69 + 9.09 - 4.55 = 17.23cqw   (24px then 12px of 264)
     bottom  11.5  + 6.86 - 1.14 = 17.22%     (24px then 4px of 350) */
.kcard__id{position:absolute;left:17.23cqw;right:8.14cqw;bottom:17.22%;
  text-align:left;display:flex;align-items:center;gap:0}
.kcard__t{flex:1;min-width:0;display:flex;flex-direction:column}
/* Letter-spaced caps to sit with the engraved "MASTER KEY" above them —
   the art sets that voice and the live text has to answer it. */
/* [OWNER 2026-08-20, from the Figma inspector] TWO drop shadows, and they
   are a pair: a white highlight up-left and a 12% black down-right. That is
   an ENGRAVED effect — the type reads as stamped into the metal rather than
   printed on it, which is what makes it sit with the artwork's own engraved
   "MASTER KEY". Exact values as given:
     highlight  x -0.5  y -0.5  blur 1  #FFFFFF 100%
     shadow     x  0.5  y  0.5  blur 0  #000000  12%
   ⚠ Kept in px, NOT cqw. These are sub-pixel hairlines; scaling them with
   the card would smear the highlight into a glow on the big card and round
   it away to nothing on the mini. First shadow listed paints on top, in
   both Figma and CSS, so the order below is the panel order.
   Applied to the labels AND the values because the owner's two selections
   were the label+value GROUPS, not the values alone. */
.kcard__l,.kcard__v{text-shadow:-0.5px -0.5px 1px #FFFFFF,
  0.5px 0.5px 0 rgba(0,0,0,.12)}
.kcard__l{font-size:3.03cqw;letter-spacing:.13em;text-transform:uppercase;
  color:rgba(11,11,11,.42);font-weight:600;line-height:1.5}
.kcard__v{font-size:4.16cqw;letter-spacing:.055em;font-weight:600;
  text-transform:uppercase;color:rgba(11,11,11,.82);line-height:1.35;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin:0 0 3px}
.kcard__v--m{margin-bottom:0;letter-spacing:.045em}
/* [OWNER 2026-08-19] Small, 50% opacity, 4px clear of the avatar — expressed
   as a percentage so it survives any card scale. */
/* The edit icon — REINSTATED 2026-08-20 (owner), now IN the identity row
   rather than floating at its top-right corner: "add the edit image icon
   next to the card DP container". 50% opacity as originally specified.
   `flex:0 0 auto` and a cqw width, so it scales with the card like
   everything else on it; no height/clip of its own, so the glyph keeps its
   own geometry (design-system icon gate 4). */
/* `.kcard__av` and `.kcard__ed` are both GONE — owner, 2026-09-09. The
   avatar had already lost its input field on node 4, and the pencil was
   the last thing pretending a picture could be set. Removing both closes
   that half-built state rather than leaving it flagged a fifth time. */

/* HISTORY, so the two reversals stay legible. The edit glyph arrived
   2026-08-19 from the owner's own SVG, was removed on 2026-08-20 ("we don't
   need that"), came back later the same day repositioned beside the avatar,
   and left for good with the avatar on 2026-09-09.
   The consequence flagged through all of that — node 4 has no avatar field, so
   the card was the only place a picture could be set — is now RESOLVED by
   removal: first run does not collect a picture at all. The old note here
   claimed the avatar "still works if you click it", which stopped being true
   the moment the picker was deleted. */

/* the line that explains what the card IS */
.kcard__note{font-size:13px;line-height:1.45;color:var(--sec);margin:2px 0 18px}

/* ── node 5b · the colourway picker ──────────────────────────────────────
   Selection is a RING, not a fill: the swatch has to keep showing the colour
   it stands for, so it cannot be filled with ink the way `.chip.on` is. The
   ring is the same ink the CTA uses (never #0B0B0B — see the CTA block). */
.sws{display:flex;gap:14px;align-items:center;margin:0 0 22px;flex:0 0 auto}
.sw{width:30px;height:30px;border-radius:50%;flex:0 0 auto;background:var(--sw);
  box-shadow:0 1px 3px rgba(0,0,0,.10),inset 0 0 0 1px rgba(255,255,255,.9);
  /* easings.spring from motion.tokens.js — the house spring, ~10% overshoot,
     documented there for "buttons, chips, toggles, cards". Picking a colour is
     a DISCRETE moment, which is what ADR-005 says may spring; the exits gate
     (rules/motion.md 3) governs things LEAVING and does not apply. Raw here
     for the same reason every other value in this file is — build-flow.py is
     the rendering that reads the tokens. */
  transition:transform 160ms cubic-bezier(.34,1.56,.64,1),box-shadow 160ms ease}
.sw:hover{transform:scale(1.06)}
.sw.on{box-shadow:0 1px 3px rgba(0,0,0,.10),inset 0 0 0 1px rgba(255,255,255,.9),
  0 0 0 2px var(--panel),0 0 0 4px #2E2E2C}
@media (prefers-reduced-motion:reduce){.sw{transition:none}}

/* ── node 5a · the wallet the key arrives in ─────────────────────────────
   TWO owner layers with the card BETWEEN them, so it is genuinely enveloped:
   `wal__back` behind, `wal__front` in front. Tapping slides the pair down and
   off — see wireWallet(). The card does not move; the sleeve leaves it. */
/* 300px, up from 270: on node 5a the wallet IS the screen, and the owner's
   frame has it filling most of the width. `max-width` keeps it honest on the
   narrowest phone, and `.ccol__w` caps its height, so it cannot push the
   tap-to-open off the bottom. */
/* aspect from the BACK artwork's own frame (1298x1721), not the rounded
   600/796 this used to carry — free accuracy, and it makes the number
   traceable to a file instead of to a memory of one. */
.wal{position:relative;width:calc(var(--kcw,264px) / .87);max-width:100%;
  aspect-ratio:1298/1721;flex:0 0 auto;--slide:0%}
.wal__back,.wal__front{position:absolute;
  background:center/100% 100% no-repeat;pointer-events:none;
  transform:translateY(var(--slide));
  transition:transform 820ms cubic-bezier(.3,0,.2,1)}
.wal__back{left:0;right:0;top:0;bottom:0;background-image:var(--slvb);z-index:1}
/* ⚠ THE FRONT IS NARROWER THAN THE BACK, AND IT HAS TO BE SET EXPLICITLY.
   Owner, 2026-08-20: "the front sleeve is slightly smaller." It was sharing
   `left:0;right:0` with the back, which stretched its 1227-wide frame across
   the back's 1298 — and since the two PNGs carry almost the same proportion of
   transparent padding (83.78% vs 83.67% opaque), that made the two leather
   panels come out the SAME width. A pocket the size of the sleeve reads as one
   flat shape, which is why the layering never showed.

   Every number below is measured off the two files, not chosen:
     frames    back 1298x1721   front 1227x1407
     opaque    back (106,62)-(1192,1571)   front (99,60)-(1127,1267)
   width   1227/1298 = 94.53%, so 5.47% of margin, centred -> 2.735% a side
   bottom  the front's leather must sit flush with the back's. The back's
           lower padding is 150/1721 = 8.72% of the wal; the front's 140px
           scales to 8.13%; the difference is what the frame is lifted by.
   ⚠ Re-exporting either sleeve at a different crop invalidates all four. */
.wal__front{left:2.735%;right:2.735%;bottom:0.59%;
  aspect-ratio:1227/1407;background-image:var(--slvf);z-index:3}
/* the card sits in the pocket: high enough that the front panel covers its
   lower two-thirds, which is what makes it read as inserted */
.wal__card{position:absolute;left:6.5%;right:6.5%;top:6%;z-index:2;
  transition:transform 820ms cubic-bezier(.3,0,.2,1)}
.wal__card .kcard{width:100%}
/* ⚠ NOT a percentage. The two panels have DIFFERENT heights (the front is
   the pocket, `aspect-ratio:572/656`, the back is the whole sleeve), so one
   percentage travels two distances and the shorter panel was left sitting
   in the bottom of the screen after the slide — measured, not guessed.
   A shared px distance moves both the same way; 560px is the phone's
   content height, so whatever the wallet's resting position, both panels
   end up past the bottom edge. `.scr` clips, so nothing escapes. */
.wal.out .wal__back,.wal.out .wal__front{--slide:560px}
/* ⚠ THE CARD DOES NOT MOVE WHEN THE SLEEVE LEAVES. It used to lift
   `translateY(-4%)` — 14px on the 350px card — and the next screen put it
   straight back, which is the jump the owner kept seeing between 5a and 5b.
   The positions matched to 0.00px by then; the movement was this rule,
   during the slide rather than at the swap, which is why measuring the two
   settled screens did not find it. The sleeve moves. The card is the fixed
   point of the whole sequence. */
@media (prefers-reduced-motion:reduce){
  .wal__back,.wal__front,.wal__card{transition:none}
}

/* ── node 15 · the indeterminate loader ──────────────────────────────────
   A dash travelling a closed lemniscate. `stroke-dasharray` and the travel
   distance are DERIVED from the measured arc length in infloader(), passed in
   as `--infL`, so the dash cannot drift if the size changes. Ink on a faint
   track — no colour, same as everything else on these screens. */
.inf{display:flex;flex-direction:column;align-items:center;gap:10px;
  flex:0 0 auto;padding:6px 0 2px}
.inf__s{width:24px;height:24px;overflow:visible}
.inf__t,.inf__d{fill:none;stroke-linecap:round;stroke-width:2.2}
.inf__t{stroke:rgba(11,11,11,.10)}
/* The ring SPINS now rather than a dash travelling a path: on a circle the
   two are visually identical, and a rotation needs no `--infL` arc-length
   plumbed through from the generator. `transform-box:fill-box` is what makes
   `transform-origin:center` mean the circle's centre and not the SVG's
   user-space origin. */
.inf__d{stroke:var(--ink);transform-box:fill-box;transform-origin:center;
  animation:infSpin 900ms linear infinite}
@keyframes infSpin{to{transform:rotate(360deg)}}
/* 10px, on the owner's instruction — an estimate in words, sized so it reads
   as a footnote to the loader rather than as body copy. */
.inf__n{font-size:10px;line-height:14px;color:var(--ter);margin:0;
  text-align:center;letter-spacing:.01em}
@media (prefers-reduced-motion:reduce){
  .inf__d{animation:none;stroke-dasharray:none;stroke:rgba(11,11,11,.28)}
}

/* Node 5c's own layout (`.ksucc`) is GONE — 2026-08-20. It was a second
   celebration layout that centred its own card, which is precisely why the
   card changed size and position on the one screen where the owner wanted it
   to hold still. 5c is a `.ccol` screen now, registered with 5a and 5b, so
   there is nothing left for these rules to style. Deleted rather than left
   dead: an orphaned layout in this stylesheet is the next reader's wrong
   answer to "which layout does the celebration use". */
/* ⚠ FULL-BLEED BACKDROP — owner, 2026-08-19: "the dot matrix is getting
   clipped from the left and the right."

   It was inset by 44px, from TWO stacked paddings: `.scr`'s own 22px (node 5a
   is the only card screen with no `.pgb`, so `.scr:has(.pgb){padding:0}` never
   applied to it and that padding survived where every neighbour had it
   stripped) plus `.pgt:has(.kcard)`'s 22px.

   The first fix cancelled both with negative `inset` arithmetic. It was 393
   wide and still 14px off-centre, because those insets resolve against
   `.ksucc`, whose own box is not what the matrix should be measured from.
   Chasing that offset would have been a third layer of arithmetic.

   So the arithmetic is GONE instead: `.ksucc` is not a positioned ancestor,
   which makes `.scr` the containing block — the matrix is `inset:0` against
   the SCREEN and is full-bleed by construction. Nothing to keep in sync, and
   no padding anywhere upstream can clip it again.
   ⚠ `inset:0` resolves against the containing block's PADDING box, not its
   border box, so `.scr`'s own side padding still has to come off — that is the
   one line of the old approach worth keeping. The bottom padding stays: it is
   home-indicator clearance.
   `.scr` itself clips, so nothing escapes the phone. */


/* ── the dot matrix itself, and the ring travelling through it ───────────
   TWO LAYERS OF THE SAME GRID. `__base` rests in very light grey; `__ring` is
   an identical grid in a darker grey, masked to an expanding annulus. That is
   what makes the ring read as the DOTS lighting up rather than as a circle
   drawn over them — there is never any ink between the dots.

   `@property` is load-bearing: a bare custom property does not interpolate, so
   animating the mask's radius needs the type registered. `inset:-14%`
   overscans the grid so the ring can leave the frame without its own dots
   thinning out at the edge.

   ⚠ GREY AND WHITE ONLY — the owner's reference was a dark colour shot and the
   instruction was to take its structure, not its palette. */
@property --dmr{syntax:"<percentage>";inherits:false;initial-value:0%}
.dmx{position:absolute;inset:0;overflow:hidden;pointer-events:none;
  display:grid;place-items:center}
.dmx__base,.dmx__ring{position:absolute;inset:-14%;
  background-image:radial-gradient(circle,var(--dc) 1.5px,transparent 2px);
  background-size:15px 15px}
.dmx__base{--dc:rgba(11,11,11,.075)}
.dmx__ring{--dc:rgba(11,11,11,.34);--dmr:0%;
  -webkit-mask-image:radial-gradient(circle at 50% 50%,
    transparent calc(var(--dmr) - 8%),#000 var(--dmr),
    transparent calc(var(--dmr) + 8%));
  -webkit-mask-repeat:no-repeat;
  animation:dmxRing 2800ms cubic-bezier(.25,0,.2,1) infinite}
@keyframes dmxRing{
  0%{--dmr:0%;opacity:0}
  12%{opacity:1}
  72%{opacity:1}
  100%{--dmr:64%;opacity:0}
}
@media (prefers-reduced-motion:reduce){
  .dmx__ring{animation:none;--dmr:38%;opacity:.85}
}

/* The confetti burst that lived here was replaced by the dot matrix above on
   2026-08-19 (owner). Removed rather than commented out — a disabled effect in
   a stylesheet is one `display:block` away from coming back by accident, and
   the reasoning worth keeping (white-on-white needs a shadow to be visible at
   all) is recorded in memory/changelog.md. */


/* ── the centred column · nodes 5a and 5b ────────────────────────────────
   NOT the split visual/content layout. Both of the owner's frames for this
   stage are ONE CENTRED COLUMN — heading, body, the object, then the tail —
   and the first build used `pgt`+`pgb`, which on 5a put the wallet ABOVE the
   greeting and read backwards, and on 5b left-aligned a page the frame centres.
   Owner, 2026-08-20: "look at the structure of this page where the
   customization happens. Use this exact structure. Don't use the left align
   button structure."

   ⚠ ONE class for both screens, deliberately. They are the same layout with a
   different object in the middle, and the previous version of this file grew
   two near-identical stylesheets for the CTA and then let them drift — see the
   `.cta` / `.s-cta` note in rules/design-system.md. Same reason `.ksucc` opts
   out of `.pgb` rather than fighting it.

   No side padding of its own: `.scr` keeps its 22px here, because
   `.scr:has(.pgb){padding:0}` never matches these screens. */
.ccol{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  align-items:center;text-align:center;padding:0 0 6px}
/* ⚠ THE HEAD IS A FIXED BAND, and that is what stops the card jumping.
   Owner, 2026-08-20: "there is jump of the card when it goes from 5a to 5b
   the card jumps a bit. keep the placement the same in both these pages."
   Measured 48px of vertical jump. The cause was NOT the card: it was that
   `.ccol__w` is `flex:1` and the two screens differ both above it (a 2-line
   body on 5a, 3-line on 5b) and below it (one link vs label+swatches+CTA),
   so the leftover box it centres in was a different box on each screen.
   Reserving the head fixes where the middle STARTS; top-aligning the object
   inside it makes the start the only thing that matters, so the tail can
   differ freely without moving the card. A 2-line body simply gets more air
   under it, which is the trade the owner asked for. */
.ccol__h{flex:0 0 auto;min-height:112px;width:100%}
.ccol .t1{font-size:24px;line-height:1.18;font-weight:700;letter-spacing:0;
  text-wrap:normal;margin:0 auto 8px}
/* the three stops and the angle, from tokens.titleGradient — see the note
   there about the mid stop not being one of the two greens */
.grad{--tg1:__TG1__;--tg2:__TG2__;--tg3:__TG3__}
/* ── the stylized title ──────────────────────────────────────────────────
   Owner redline, 2026-08-20, from their Figma inspector: Google Sans Flex Bold
   24px, letter-spacing 0, and a three-stop linear gradient — ink, then a pale
   green at the midpoint, then ink again — run at an angle across the words.
   Applied to the heading on nodes 5a, 5b and 5c only.

   ⚠ `background-clip:text` needs a TRANSPARENT text colour to show through, and
   `-webkit-` is not optional: it is still the only form Safari accepts.
   ⚠ The gradient is on the h1, so it spans the whole heading box rather than
   each line — which is what makes the green land mid-phrase the way the
   reference shows it. On a two-line heading it reads diagonally, by design.
   ⚠ `text-wrap:balance` is off here: a gradient tuned to the midpoint of one
   line length jumps if the browser rebalances the break. */
/* ⚠ `width:fit-content` IS THE WHOLE EFFECT. A block h1 is full-width, so the
   gradient spanned the box and the text — sitting in the middle third of it —
   sampled only the green midpoint and rendered uniformly green, with both ink
   ends off past the edges of the words. Shrinking the box to the text is what
   puts 0% and 100% at the first and last letter. `margin-inline:auto` keeps it
   centred, since a fit-content block no longer fills the column. */
/* ⚠ SPLIT INTO PAINT AND SIZE, 2026-08-20. This started as one class for the
   three key-card screens and carried their 24px and their centring along with
   the gradient. The owner then asked for the gradient on EVERY header, and
   those two extras would have resized and centred the whole flow. So `.grad`
   is now the paint and nothing else, and the key-card screens keep their own
   size in `.ccol .t1` below. */
.grad{width:fit-content;max-width:100%;
  background-image:linear-gradient(__TGA__deg,var(--tg1) __TGP1__%,var(--tg2) __TGP2__%,var(--tg3) __TGP3__%);
  -webkit-background-clip:text;background-clip:text;
  color:transparent;-webkit-text-fill-color:transparent}
/* the greeting's name is inside the h1, so it inherits the clip and must not
   re-declare a colour or it would punch an opaque hole in the gradient */
.grad [data-wname]{color:inherit;-webkit-text-fill-color:inherit}
@supports not ((-webkit-background-clip:text) or (background-clip:text)){
  /* no clip support: plain ink beats invisible text */
  .grad{color:var(--ink);-webkit-text-fill-color:currentColor}
}
.ccol .bd{margin-bottom:0}
/* the object — wallet or card — takes whatever height is left over and stays
   centred in it, so the tail below can never be pushed off the bottom */
/* 29px. The owner asked for 54 down and then 18 back up, which lands at 36 —
   but the stated GOAL was that the card reads centred on 5b "between the top
   elements and the bottom elements", and at 36 the gaps measured 30.6 above
   against 19.4 below. 31 equalises them (measured 24 above, 25 below). Solved from the measurement rather
   than from the delta, because the delta was the owner's estimate OF the goal
   and the goal is the thing that can be checked. On
   `.ccol__w` rather than on the card, so the wallet, the bare card and the
   celebration card all move together and stay registered.
   The brief for the final value is that the card reads CENTRED on 5b between
   the head and the tail — measured below, not eyeballed. */
.ccol__w{flex:1 1 auto;min-height:0;width:100%;display:grid;
  place-items:start center;padding-top:31px}
/* The wallet is taller than the card and holds it 6% down from its own top
   (`.wal__card{top:6%}`), so top-aligning the sleeve would sit the card 6%
   lower than the bare card on 5b. Cancelling that offset here is what makes
   the two land on the same pixel.
   ⚠ `translateY` percentages resolve against the ELEMENT's own height, which
   is the whole reason this can be written once and stay correct — a margin
   percentage would resolve against the width and be wrong by the aspect
   ratio. The slide-out transform lives on `.wal`'s CHILDREN, so it does not
   collide with this. */
.ccol__w .wal{transform:translateY(-6%)}
.ccol__w .wal,.ccol__w .kcard{max-height:100%}
/* the tail: everything pinned under the object. On 5a that is one link, on 5b
   it is the CUSTOMIZE label, the swatches and the CTA. */
.ccol__t{flex:0 0 auto;margin:0;width:100%;display:flex;flex-direction:column;
  align-items:center;gap:0}
.ccol__t .lab{text-align:center}
/* the picker centres here — `.sws` is flex, so `text-align` cannot do it */
.ccol__t .sws{justify-content:center}
.ccol__t .cta{width:100%}

/* ── the sequence's two entrances, node 5a only ──────────────────────────
   Owner, 2026-08-20: "the welcome text appears with dissolve with the name
   user has inputed in the previous page, then the wallet needs to come
   flipping up from the bottom of the screen".

   ⚠ Only 5a carries these classes. 5b and 5c deliberately have NO entrance on
   the object: the card is the fixed point of the sequence and the whole point
   is that it does not re-arrive. Same reasoning as node 4's one-time flip.
   A dissolve is opacity ONLY — no translate. Anything that moves would
   contradict the card standing still beside it. */
.ccol__h--in>*{animation:ccolDis 620ms ease both}
.ccol__h--in>*+*{animation-delay:140ms}
@keyframes ccolDis{from{opacity:0}}

/* ⚠ The `to` keyframe MUST restate `translateY(-6%)`. That is the sleeve's
   resting compensation for the 6% it holds the card at, and a filled animation
   replaces the declaration rather than composing with it — so leaving `to`
   implicit would land the wallet 24px low and take the card with it. */
.wal--enter{animation:walUp 780ms cubic-bezier(.19,.91,.24,1) both}
@keyframes walUp{
  from{opacity:0;transform:perspective(900px) translateY(155%) rotateX(-44deg)}
  55%{opacity:1}
  to{opacity:1;transform:perspective(900px) translateY(-6%) rotateX(0deg)}
}
@media (prefers-reduced-motion:reduce){
  .ccol__h--in>*{animation:none}
  .wal--enter{animation:none}
}

/* ── 5c · the dot matrix runs BEHIND a card that has not moved ───────────
   The celebration used to be its own layout (`.ksucc`), which meant the card
   changed size and position at the exact moment the owner wanted it to hold
   still. It is a `.ccol` screen now like 5a and 5b, so the card is registered
   with the two before it and only the text and the backdrop change.
   ⚠ `.dmx` is `inset:0` against `.scr`'s PADDING box, so the screen's 22px has
   to come off or the matrix is inset and clipped — and the 22px then has to be
   paid one level in, by the nav and the column. Scoped with both `:has()`
   clauses so node 16's matrix, which lives in a `.pgt`, is untouched. */
.scr:has(.ccol):has(.dmx){padding-left:0;padding-right:0}
.scr:has(.ccol):has(.dmx) .nav,
.scr:has(.ccol):has(.dmx) .ccol{padding-left:22px;padding-right:22px}
/* ⚠ AND THE STATUS BAR. Second time this exact bug: zeroing the screen's side
   padding for a full-bleed matrix takes the clock's inset with it and "9:41"
   renders clipped against the phone's rounded corner. The old `.ksucc`
   celebration needed the identical line for the identical reason. */
.scr:has(.ccol):has(.dmx) .sbar{padding:15px 22px 0}
/* above the matrix, below nothing */
.scr:has(.ccol):has(.dmx) .ccol{position:relative;z-index:1}

/* The resident's key — node 18a. Owner artwork used as is; nothing on it is
   live. Sized to sit clear of the floating nav on R3, the tallest content
   half in the flow. */
/* 168px: R3 leaves ~258px for the visual half (measured), and the key at
   its aspect ratio plus nav clearance has to live inside that. */
.reskey{display:block;width:168px;aspect-ratio:666/918;flex:0 0 auto;
  background:var(--reskey) center/contain no-repeat;margin-top:22px}

/* The SKU renders — real product photography, replacing the CSS-drawn
   purifier everywhere a purifier is depicted (owner, 2026-08-17). contain-fit
   so the three different aspect ratios all sit on the same baseline. */
/* THE CARRIED PURIFIER. Every appearance of the chosen device is this one
   element, sized by HEIGHT with the SKU's true aspect ratio — so the image
   exactly fills its box, `--ledy` lands on the real light, and the FLIP
   between screens scales something whose proportions never change.
   --ledy measured off each render (the 200's light sits much lower). */
.rnd{display:block;background:var(--rnd200) center/contain no-repeat;
  aspect-ratio:var(--ar);--ar:801/1200}
.rnd--500{background-image:var(--rnd500);--ar:623/1200}
.rnd--max{background-image:var(--rndmax);--ar:982/1200}

/* ── ONE purifier, moved rather than redrawn ─────────────────────────────
   `.pslot` is an invisible box that only declares geometry; `.phero` is the
   single real render, created once at boot as a sibling of the screens and
   moved to each slot with a transform. Nothing re-rasterises between screens,
   which is what the flicker was.
   It sits BELOW the screens (z-index 1 vs 2) on purpose: node 9's light
   overlay and nodes 10-11's phone have to be in front of the device, and both
   live inside a screen. */
/* ── the travelling key card ─────────────────────────────────────────────
   A sibling of the screens, like `.phero`, so screen swaps never touch it.
   `transform-origin:0 0` is what lets placeKey() express a position and a
   scale as one translate+scale from the phone's top-left, exactly as the
   purifier does. Never interactive: the door's real card owns the drag. */
.khero{position:absolute;left:0;top:0;z-index:45;width:264px;
  transform-origin:0 0;pointer-events:none;opacity:0;
  filter:drop-shadow(0 10px 22px rgba(0,0,0,.16));
  transition:transform 620ms cubic-bezier(.2,0,0,1),opacity 260ms linear}
.khero .kcard{width:100%}
/* ── the parked card carries NOTHING ─────────────────────────────────────
   Owner: "No text will be on it just the card bg colors." Everything live on
   the card fades out as it flies — the identity block and the edit icon. What
   is left is the artwork itself, which is a background image and so cannot be
   stripped; at this size and tilt its engraving is sub-pixel anyway.
   ⚠ Opacity, not `display:none`. The card flies and folds at the same time as
   this fades, and a display change mid-flight would pop the layout — and it
   has to be reversible, because the door puts the real card back.
   The shimmer is already off on this element (`.khero .kfx{display:none}`). */
.khero--bare .kcard__id{opacity:0;
  transition:opacity 260ms linear}
/* a tilted card catches light along its top edge rather than casting the same
   drop shadow a flat one does */
/* ⚠ TOP CENTRE — AND IT STAYS THAT WAY THROUGH THE FLIGHT TO THE SLOT.
   `transform-origin` is not animatable in any useful sense: changing it takes
   effect instantly while the transform interpolates, so the card jumps to a
   new start position on the frame the class comes off. That was the second
   half of the flicker the owner reported. So the class is NOT removed for the
   flight; placeKey() compensates its x arithmetic for this origin instead
   (see the note there). Only `--bare` comes off, which is a pure fade. */
.khero--parked{transform-origin:50% 0;
  filter:drop-shadow(0 6px 14px rgba(0,0,0,.13))}
@media (prefers-reduced-motion:reduce){
  .khero--bare .kcard__id{transition:none}
}
@media (prefers-reduced-motion:reduce){.khero{transition:none}}
/* the door's card waits, invisible, until the mini lands on it */
/* ⚠ GENERIC, not door-specific. Any screen that declares `[data-kslot]` hides
   its own card until the travelling one lands on it, so there is never more
   than one card on screen — owner, 2026-08-20: "only one card is visible at a
   time because it is just a shrunken instance of the card not any new
   object". Both shapes are covered: the slot may BE the card (node 5b) or
   CONTAIN it (the door). */
.kslot--handoff,.kslot--handoff .kcard{opacity:0;transition:none}

.pslot{display:block;visibility:hidden;aspect-ratio:var(--ar)}
.phero{position:absolute;left:0;top:0;z-index:1;height:250px;width:auto;
  aspect-ratio:var(--ar);transform-origin:0 0;opacity:0;pointer-events:none;
  background:var(--rnd200) center/contain no-repeat;
  transition:transform .62s cubic-bezier(.2,0,0,1),opacity .3s ease}
.phone.sku-500 .phero{background-image:var(--rnd500)}
.phone.sku-max .phero{background-image:var(--rndmax)}
/* the aspect ratio and the light position ride the PHONE, so the slot, the
   render and the overlay all read the same numbers */
.phone{--ar:801/1200;--ledy:39.7%}
.phone.sku-500{--ar:623/1200;--ledy:19.2%}
.phone.sku-max{--ar:982/1200;--ledy:19.8%}
@media (prefers-reduced-motion:reduce){.phero{transition:none}}
/* --ledy and --ar ride the PHONE (see below) rather than the screen, because
   `.phero` is a sibling of the screens and a custom property only inherits
   down. Setting them once, high, is what lets the slot, the single render and
   the light overlay agree. */
.rnd--sm{height:170px}

/* The "key shared" toast — node 18a's confirmation, 2026-08-18 (owner: the
   sent screen "can just say key sent as a toast"). It replaces a whole screen
   (R3C), which is the right trade: a confirmation you have to dismiss is a
   screen, a confirmation you just see is a toast. ⚠ What R3C also carried was
   the ROSTER — "You · owner / Lakshmi · key sent, waiting" — and a toast cannot
   hold that. The pending state now has no representation in first run; it
   belongs to People. */
.toast{position:absolute;left:50%;bottom:104px;transform:translate(-50%,14px);
  z-index:50;background:var(--ink);color:#fff;font-size:14px;font-weight:600;
  padding:11px 20px;border-radius:99px;box-shadow:0 10px 26px rgba(0,0,0,.24);
  opacity:0;pointer-events:none;
  transition:opacity .26s ease,transform .32s cubic-bezier(.34,1.56,.64,1)}
.toast.on{opacity:1;transform:translate(-50%,0)}

/* A TERTIARY action: no container, no fill — a text button that sits under
   the CTA. Used where declining has to stay reachable without competing with
   the primary for attention (node 18a's "Not now"). */
.cta3{display:block;width:100%;text-align:center;font-size:15.5px;font-weight:600;
  color:var(--sec);padding:14px 0 2px;flex:0 0 auto;
  transition:color .16s ease}
.cta3:hover{color:var(--ink)}
.cta3:active{color:var(--ink);transform:scale(.985)}

/* ── node 18a · sending a resident's key ─────────────────────────────────
   Owner reference, 2026-08-18. Picked people become removable pills between
   the field and the list, and the list drops whoever is already picked. */
/* 0.8x on 2026-08-18, then 0.8x again the same day: 236 -> 189 -> 151.
   The visual half clips its overflow, which was cutting the tilted card top
   and bottom — a rotated box is taller than its own width. `.pgt` releases
   the clip when it holds a key so the whole card reads. Nothing else on these
   screens overflows, so this is safe rather than a blanket change. */
/* 1.5x on 2026-08-19 (owner: "give the residence key illustration on the top
   a little more space. So you can make it maybe 1.5x and shift everything else
   down"). 151 -> 227. The room came from dropping the contacts list below. */
/* CENTRED, not bled off the right. The old `-8% ... auto` offset was tuned for
   a 151px key; at 227 the same bleed cut the artwork's "HOME" wordmark in half,
   which reads as a mistake rather than as a crop. Centring keeps whatever
   clipping remains on the top and bottom edges — which the owner has already
   accepted for this illustration — instead of through lettering. */
.reskey--tilt{transform:rotate(-20deg);margin:10px auto 0;width:227px}
/* the content half starts lower, so the bigger key has the top of the screen */
.scr:has(.ks) .pgb{padding-top:30px}
.pgt:has(.reskey){overflow:visible}
.ks{flex:0 0 auto;display:flex;flex-direction:column}
.ks .fld{margin-bottom:0}
.ks .lab{margin:16px 0 9px}
.ks .lab:first-child{margin-top:2px}
.ks__pills{display:flex;flex-wrap:wrap;gap:8px;padding:12px 0 0}
.ks__pills:empty{display:none}
.kp{display:flex;align-items:center;gap:7px;background:var(--card);border-radius:99px;
  padding:5px 10px 5px 5px;box-shadow:var(--shs);font-size:13.5px;font-weight:600;
  animation:kpin .26s cubic-bezier(.34,1.56,.64,1) both}
@keyframes kpin{from{opacity:0;transform:scale(.86)}}
.kp__a{width:22px;height:22px;border-radius:99px;display:grid;place-items:center;
  font-size:9px;font-weight:700;color:#fff;flex:0 0 auto;letter-spacing:.02em}
.kp__x{width:15px;height:15px;position:relative;flex:0 0 auto;opacity:.5}
.kp__x::before,.kp__x::after{content:"";position:absolute;left:2px;top:7px;width:11px;
  height:1.6px;border-radius:2px;background:var(--ink)}
.kp__x::before{transform:rotate(45deg)}
.kp__x::after{transform:rotate(-45deg)}
.kp:hover .kp__x{opacity:.85}
/* the contact rows */
.ks__list{display:flex;flex-direction:column}
.kc{display:flex;align-items:center;gap:13px;width:100%;padding:9px 2px;
  text-align:left;flex:0 0 auto}
.kc[hidden]{display:none}
.kc__a{width:34px;height:34px;border-radius:99px;display:grid;place-items:center;
  font-size:11px;font-weight:700;color:#fff;flex:0 0 auto;letter-spacing:.02em}
/* ⚠ the three avatar hues — see KEY_CONTACTS for why they are back */
.kc__a--pink,.kp__a--pink{background:#F0A0B4}
.kc__a--blue,.kp__a--blue{background:#8FB4E8}
.kc__a--sand,.kp__a--sand{background:#EBC98C}
.kc__t{display:flex;flex-direction:column;gap:1px;min-width:0}
.kc__t b{font-size:15.5px;letter-spacing:-.014em}
.kc__t span{font-size:12.5px;color:var(--ter)}

/* ── a sheet over a page ─────────────────────────────────────────────────
   Node 5. The Setup profile page stays behind it, dimmed, so the card you
   just filled in is still there while you confirm the address on it. */
.ovl{position:absolute;inset:0;z-index:40}
/* nodes 4 and 5 have nothing behind the sheet to dim — see sheetbare() */
.ovl--bare{background-image:var(--aubg);background-size:cover;
  background-position:center}
/* ⚠ THE BACK BUTTON LIVES ON THE PAGE, NOT IN THE SHEET — owner, 2026-08-20:
   "shift the back button from inside the bottom sheet and shift it to the top
   left like page 5a, also apply the back button to pages 2-5".
   Both hosts position it absolutely because everything inside `.au` and
   `.ovl--bare` is absolute (the sheet is pinned to the bottom, the status bar
   to the top), so there is no flow for a nav bar to sit in. The numbers match
   node 5a's IN-FLOW bar rather than being chosen: `.sbar` is 56px tall and
   5a's nav adds 4px of padding above the button, so 60px; and 22px is the
   same side inset every screen in the flow uses.
   Grep: a `sheetback()` inside one of these sheets is now a regression.

   ⚠ MISSING ITS COMPANION RULE ON FIRST LANDING, and it shipped to Vercel that
   way — a plain white circle sat in the nav's right slot on nodes 2-5. `nav()`
   always emits BOTH sides; with no `close` handler the right slot is an empty
   `<span class="nb">`, and `.nb`'s own CSS (a white 38px circle) does not know
   the difference between a real button and a placeholder — something else has
   to hide the placeholder. Two existing call sites already carry that
   companion rule (`.scr:has(.pgb.pgb--top) .nav span.nb` and
   `.scr:has(.ccol) .nav span.nb`, both `visibility:hidden`), and this one was
   the third `nav()` host added this session — the one time the twin rule was
   forgotten instead of copied. */
.au>.nav,.ovl--bare>.nav{position:absolute;top:60px;left:22px;right:22px;
  z-index:41;min-height:40px}
.au>.nav span.nb,.ovl--bare>.nav span.nb{visibility:hidden}
/* ⚠ The bare overlay paints the canvas at z-index 40, which covered the
   status bar — the clock and battery vanished on nodes 4 and 5 while every
   scrimmed sheet kept them (a scrim is translucent; this fill is not).
   The sheet is a sheet, not a takeover, so the bar stays on top of it. */
.scr:has(.ovl--bare) .sbar{position:relative;z-index:41}
/* Centred head, left-aligned fields — the owner's frames for nodes 4 and 5.
   Targeted rather than `data-align="center"`, which would drag NAME and
   MOBILE NUMBER into the middle with it. */
.ovl--bare .eyb,.ovl--bare .h1,.ovl--bare .sub{text-align:center}
.ovl__s{position:absolute;inset:0;background:rgba(20,20,20,.42);
  animation:ovlin 320ms cubic-bezier(.2,0,0,1) both}
@keyframes ovlin{from{opacity:0}}
.ovl .sheet{transform:none;animation:auRise 480ms cubic-bezier(.16,1,.3,1) both}
/* Condensed 2026-08-18 (owner), the same pass the sign-in sheets had. The
   single biggest win was the UA's default h1 margin-block-start — 0.67em of
   a 30px title is 20px of dead space nobody wrote. */
.ovl .sheet .iconbtn{margin-bottom:10px}
.ovl .sheet .h1{margin:0 0 8px}
.ovl .sheet .sub{margin:6px 0 8px}
.ovl .sheet .s-link{margin-top:6px}
.ovl .sheet .otpi{margin:10px 0 2px}
.ovl .sheet .otpi i{width:52px;height:46px}
.ovl .sheet .resend{margin:8px 0 8px}
.ovl .sheet .cta{margin-bottom:0}

/* ── D1 · the door, and the key that opens it ────────────────────────────
   The finale (owner reference, 2026-08-17). A closed door fills the screen;
   the master key card sits at the bottom, half off-screen; dragging it to the
   lock (or a plain tap, or Enter) opens the door into Home.
   ⚠ The lock is BEIGE, from the reference — a non-palette hue on a depicted
   real-world object; same open question as the 3D icons. Flagged at the
   screen's note. */
.dk{position:absolute;inset:0;overflow:hidden;background:#E9E8E6;outline:none}
.scr:has(.dk){padding:0}
.scr:has(.dk) .sbar{position:absolute;top:0;left:0;right:0;z-index:30;
  padding:15px 22px 0}
.dk__scene{position:absolute;inset:0;perspective:1200px}
/* the door leaf — hinged on the right, wall showing at the left edge */
.dk__door{position:absolute;left:24%;right:0;top:0;bottom:0;
  background:linear-gradient(200deg,#FDFDFD 0%,#F4F3F1 100%);
  box-shadow:-1px 0 0 rgba(11,11,11,.10),-14px 0 34px rgba(0,0,0,.05);
  transform-origin:100% 50%;
  transition:transform 1.1s cubic-bezier(.4,0,.2,1) .12s}
.dk__panel{position:absolute;left:38%;right:9%;border-radius:3px;
  box-shadow:inset 0 0 0 1.5px rgba(11,11,11,.07),
             inset 3px 3px 7px rgba(11,11,11,.045),
             inset -2px -2px 5px rgba(255,255,255,.9)}
.dk__panel--t{top:9%;height:33%}
.dk__panel--b{top:47%;height:41%}
/* the smart lock — reader strip, LED, lever */
.dk__lock{position:absolute;left:11%;top:27%;width:46px;height:140px;border-radius:11px;
  background:linear-gradient(160deg,#E7DCC0 0%,#CDBE9B 100%);
  box-shadow:0 8px 22px rgba(0,0,0,.16),inset 0 1px 0 rgba(255,255,255,.55)}
.dk__reader{position:absolute;left:12%;right:12%;top:7px;height:11px;border-radius:3px;
  background:#1B1B1A}
.dk__led{position:absolute;left:50%;top:26px;width:5px;height:5px;margin-left:-2.5px;
  border-radius:99px;background:#6CCC7C;box-shadow:0 0 5px 1px rgba(108,204,124,.55);
  animation:bl 2.2s steps(1) infinite}
.dk__lever{position:absolute;left:58%;top:46%;width:80px;height:22px;border-radius:12px;
  background:linear-gradient(180deg,#E2D6BA 0%,#C4B590 100%);
  box-shadow:0 5px 12px rgba(0,0,0,.18);transform-origin:9% 50%;
  transition:transform .5s cubic-bezier(.34,1.56,.64,1) .55s}
.dk__hint{position:absolute;left:0;right:0;top:56%;text-align:center;font-size:15px;
  font-weight:600;color:var(--ink);transition:opacity .3s}
/* the key, half off-screen at the foot. The drag transform rides on the INNER
   card so this positioning wrapper never fights it. */
/* bottom -190 -> -116 -> -92: the owner's 74px lift on node 23, then another
   24 (2026-08-20, two passes). The card is anchored from the BOTTOM here, so
   a lift is a positive move on that offset. */
.dk__card{position:absolute;left:50%;bottom:-92px;margin-left:-150px;z-index:10;
  cursor:grab;touch-action:none}
/* ⚠ THE ROLL IS GONE — owner, 2026-08-20: "the transition of the shrunken card
   to the large card is breaking and flickering... we can remove the rotate
   from the big card so the transition is easier." They were right about the
   cause. The traveller flew to the slot's `getBoundingClientRect()`, which is
   an AXIS-ALIGNED box; a rotated card's AABB is larger than the card, so
   matching the rect meant NOT matching the card, and the handoff swapped one
   for the other at slightly different sizes. Putting the roll on an inner
   wrapper kept the SLOT square but the traveller still had to carry the angle
   itself to look right, and a rotated traveller has the same enlarged AABB.
   Square on both sides is the only version where the two are the same shape.
   The wrapper stays as a plain passthrough so the DOM shape is unchanged. */
.dk__roll{transform:none}
.dk__card .kcard{width:300px}
.dk__card .kcard{transition:transform .45s cubic-bezier(.2,0,0,1),opacity .3s}
.dk.drag .dk__card .kcard{transition:none}
.dk.drag .dk__card{cursor:grabbing}
/* success: LED flares, lever turns, door swings, light floods, card fades */
.dk__light{position:absolute;left:0;top:0;bottom:0;width:60%;
  background:linear-gradient(90deg,rgba(255,252,242,.95),rgba(255,252,242,0));
  opacity:0;transition:opacity .9s ease .25s}
.dk__flood{position:absolute;inset:0;background:#FFFFFF;opacity:0;pointer-events:none;
  transition:opacity .55s ease .95s;z-index:20}
.dk.open .dk__door{transform:rotateY(52deg)}
.dk.open .dk__lever{transform:rotate(34deg)}
.dk.open .dk__led{animation:none;box-shadow:0 0 10px 3px rgba(108,204,124,.9)}
.dk.open .dk__light{opacity:1}
.dk.open .dk__flood{opacity:1}
.dk.open .dk__hint{opacity:0}
.dk.open .dk__card .kcard{opacity:0}
@media (prefers-reduced-motion:reduce){
  .dk__led{animation:none}
  .dk__door,.dk__lever,.dk__flood,.dk__light{transition:none}
}

/* a code field you can type into — see otpin() */
.otpi{position:relative;display:flex;gap:11px;justify-content:center;margin:2px 0 4px;
  flex:0 0 auto}
.otpi i{width:56px;height:54px;border-radius:16px;background:var(--panel);
  box-shadow:var(--shs);display:grid;place-items:center;font-style:normal;
  font-size:22px;font-weight:700}
.otpi input{position:absolute;inset:0;width:100%;opacity:0;border:0;background:none;
  font:inherit;cursor:pointer}
.otpi i.at::after{content:"";width:2px;height:22px;background:var(--ink);
  animation:bl 1.05s steps(1) infinite}

/* nodes 10-11 — the Bluetooth scene, per the owner's reference (2026-08-18):
   the real render upper-left, the real iPhone Bluetooth mock lower-right,
   in front. */
/* No min-height: .pgt clips its overflow, and a taller-than-viz scene put
   the phone's device rows outside the visible box. */
.btsc{position:relative;width:308px;height:100%}
.btsc__pur{position:absolute;left:2px;top:0;height:56%}
/* The phone's Bluetooth settings, drawn so the toggle can actually move.
   iOS colours on purpose — this depicts the OS, not a NOMA surface. The
   whole 5.4s loop: switch flips at ~1.1s, the caption and the device rows
   arrive behind it, everything resets at the end. */
/* Fades to nothing on the way down (owner, 2026-08-18) instead of stopping
   at a hard bordered edge — it should read as an illustration dissolving,
   not as a square pasted on the screen. mask-image rather than a gradient
   overlay, so the bezel and the drop shadow fade with the content; the
   shadow moves onto a wrapper for the same reason. */
.btph{position:absolute;right:0;bottom:0;width:198px;height:84%;
  border-radius:20px 20px 0 0;background:#F2F2F7;overflow:hidden;
  box-shadow:inset 0 0 0 3px #1B1B1D,inset 0 0 0 4.5px #46464A;padding:0 8px;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 46%,rgba(0,0,0,.55) 72%,
    rgba(0,0,0,0) 97%);
  mask-image:linear-gradient(180deg,#000 0%,#000 46%,rgba(0,0,0,.55) 72%,
    rgba(0,0,0,0) 97%)}
.btph__nav{display:flex;align-items:center;gap:6px;height:32px;font-size:8.5px;
  border-bottom:.5px solid rgba(11,11,11,.10);margin:0 -9px 8px;padding:0 9px}
.btph__nav b{color:#007AFF;font-weight:400}
.btph__nav b::before{content:"‹ ";font-weight:600}
.btph__nav em{font-style:normal;font-weight:700;font-size:9.5px;margin-left:auto;
  margin-right:auto;padding-right:22px}
.btph__row{display:flex;align-items:center;justify-content:space-between;
  background:#fff;border-radius:7px;padding:7px 8px;font-size:9px}
.btph__tog{width:26px;height:15px;border-radius:99px;background:#E4E4E6;position:relative;
  animation:btflip 5.4s cubic-bezier(.2,0,0,1) infinite}
.btph__tog i{position:absolute;left:1.5px;top:1.5px;width:12px;height:12px;border-radius:99px;
  background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.28);
  animation:btknob 5.4s cubic-bezier(.34,1.56,.64,1) infinite}
@keyframes btflip{0%,18%{background:#E4E4E6}26%,92%{background:#34C759}100%{background:#E4E4E6}}
@keyframes btknob{0%,18%{transform:none}26%,92%{transform:translateX(11px)}100%{transform:none}}
.btph__cap,.btph__lab,.btph__dev{animation:btfade 5.4s ease infinite}
@keyframes btfade{0%,24%{opacity:0}34%,92%{opacity:1}100%{opacity:0}}
.btph__cap{display:block;font-size:7px;color:var(--sec);padding:5px 8px 8px;line-height:1.3}
.btph__lab{display:block;font-size:6.5px;letter-spacing:.06em;color:var(--ter);
  padding:0 8px 4px}
.btph__dev{display:flex;align-items:center;justify-content:space-between;background:#fff;
  border-radius:7px;padding:6px 8px;font-size:8.5px;margin-bottom:4px}
.btph__dev em{font-style:normal;font-size:7.5px;color:var(--ter)}
.btph__dev+.btph__dev{animation-delay:.1s}
@media (prefers-reduced-motion:reduce){
  .btph__tog,.btph__tog i,.btph__cap,.btph__lab,.btph__dev{animation:none}
  .btph__tog{background:#34C759}
  .btph__tog i{transform:translateX(11px)}
}

/* Node 25's bell. Drawn as ONE SVG silhouette rather than stacked boxes —
   a white dome on a near-white ground with only a soft shadow reads as a
   blob, which is what the first attempt did. Three rings pulse out of it and
   the badge is status.negative (var(--neg)); an unread count is precisely
   what that hue exists for. */
.bellw{position:relative;width:170px;height:170px;display:grid;place-items:center}
.bellw__r{position:absolute;width:82px;height:82px;border-radius:50%;
  border:1.6px solid rgba(11,11,11,.16);animation:bring 3.4s ease-out infinite}
.bellw__r:nth-child(2){animation-delay:1.13s}
.bellw__r:nth-child(3){animation-delay:2.26s}
@keyframes bring{0%{transform:scale(.62);opacity:0}
  22%{opacity:.85}100%{transform:scale(2.05);opacity:0}}
.bell2{position:relative;width:104px;height:104px;display:block;color:var(--ink);
  animation:bswing 3.4s ease-in-out infinite;transform-origin:50% 10%}
@keyframes bswing{0%,70%,100%{transform:rotate(0)}
  77%{transform:rotate(8deg)}84%{transform:rotate(-6deg)}91%{transform:rotate(3deg)}}
.bell2 svg{display:block;width:100%;height:100%;
  filter:drop-shadow(0 10px 18px rgba(0,0,0,.10))}
/* The engraved glyph brings its own unread dot, so the drawn badge is only
   used by the retired bell. The swing and the rings around it are unchanged —
   they were tuned against the old silhouette and still read on this one. */
.bell2 .gly--bell{width:100%;height:100%}
.bell2__d{position:absolute;right:1px;top:3px;width:24px;height:24px;border-radius:50%;
  background:var(--neg);box-shadow:0 2px 8px rgba(160,59,59,.34),0 0 0 3.5px var(--page);
  animation:bdot 3.4s ease infinite}
@keyframes bdot{0%,70%{transform:scale(1)}80%{transform:scale(1.16)}100%{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){
  .bellw__r,.bell2,.bell2__d{animation:none}
  .bellw__r{opacity:.5;transform:scale(1.35)}
}



/* node 7 — the polybag slides off the cartridge, on a loop */
.xfil__wrap{position:relative}
.filt__f--out::after{display:none}   /* the bag is its own element now */
.filt__f--out{animation:cartlift 4s cubic-bezier(.2,0,0,1) infinite}
.xbag{position:absolute;inset:-10px;border-radius:18px;pointer-events:none;
  border:1.6px dashed rgba(11,11,11,.32);
  animation:bagoff 4s cubic-bezier(.2,0,0,1) infinite}
.xbag::after{content:"";position:absolute;left:50%;top:-8px;width:24px;height:8px;
  margin-left:-12px;border-radius:5px 5px 0 0;
  border:1.6px dashed rgba(11,11,11,.32);border-bottom:0}
@keyframes bagoff{0%,16%{transform:none;opacity:1}
  58%,100%{transform:translate(36px,-52px) rotate(11deg);opacity:0}}
@keyframes cartlift{0%,16%{transform:translateY(7px)}52%,100%{transform:none}}

/* node 8 — the rocker flips on, then the power light blooms awake */
.rocker{position:absolute;left:50%;bottom:-22px;width:14px;height:17px;margin-left:-7px;
  border-radius:4px;background:#fff;box-shadow:var(--shs),inset 0 0 0 1.4px rgba(11,11,11,.22);
  transform-origin:50% 100%;animation:rock 3.8s cubic-bezier(.2,0,0,1) infinite}
@keyframes rock{0%,20%{transform:rotate(-16deg)}32%,100%{transform:rotate(0)}}
.pwrwrap{position:relative;display:grid;place-items:center}
.pwrled{position:absolute;left:50%;top:44%;width:4px;height:16px;margin-left:-2px;
  border-radius:99px;background:#6CCC7C;
  box-shadow:0 0 12px 4px rgba(108,204,124,.55);
  animation:pled 3.8s ease infinite}
@keyframes pled{0%,32%{opacity:0}46%,88%{opacity:1}100%{opacity:0}}

/* node 11 — pairing: device left, phone right, dots travelling the line,
   then the check. Structure from the owner's NoiseFit reference; visuals ours. */
.pair{display:flex;flex-direction:column;align-items:center;gap:22px;width:100%}
/* Equal side columns, so the middle one is the screen's centre by
   construction rather than by arithmetic that breaks the moment either object
   changes width. `1fr` on the sides and `auto` in the middle. */
.pair__row{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
  gap:16px;width:100%}
.pair__side{display:grid;place-items:center;min-width:0}
/* the tick and the dots share this box, which is what keeps them concentric */
.pair__mid{position:relative;display:grid;place-items:center;min-height:38px}
.pair__pur{height:168px}

/* ── the phone, front on, screen off ─────────────────────────────────────
   Was a clay rectangle with a grey pill on it. This is a titanium-rail iPhone
   read from the front: a cool metal edge, a black inset screen with the
   island, and four side buttons. Nothing is shown ON the screen except a
   single diagonal sheen — owner: "keep the screen off. don't show anything
   inside the screen. Maybe you can only show, like, a reflection." */
.iph{position:relative;width:78px;height:160px;border-radius:23px;
  background:linear-gradient(147deg,#E8E9EC 0%,#B9BCC4 26%,#8E9299 52%,#C6C9D0 78%,#9DA1A9 100%);
  padding:3px;
  box-shadow:0 10px 22px rgba(11,11,11,.20),0 2px 5px rgba(11,11,11,.14),
             inset 0 0 0 .5px rgba(255,255,255,.55)}
.iph__scr{position:absolute;inset:3px;border-radius:20px;overflow:hidden;
  background:linear-gradient(158deg,#15161A 0%,#0A0B0D 46%,#101114 100%);
  box-shadow:inset 0 0 0 .5px rgba(255,255,255,.10)}
/* the island reads as part of the dark glass, not as a control */
.iph__isl{position:absolute;left:50%;top:7px;width:26px;height:7px;
  margin-left:-13px;border-radius:99px;background:#000;
  box-shadow:inset 0 0 0 .5px rgba(255,255,255,.07)}
/* ⚠ THE ONLY THING ON THE SCREEN. A wide, low-opacity diagonal band — glass
   catching the room. Anything more literal (icons, a clock, a wallpaper) would
   contradict "screen off", which is the point of the whole illustration: the
   phone is idle while the purifier is being introduced to it. */
.iph__gl{position:absolute;left:-32%;top:-14%;width:96%;height:132%;
  transform:rotate(19deg);
  background:linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.085) 42%,
             rgba(255,255,255,.115) 56%,rgba(255,255,255,0) 100%)}
/* the rails. Colour comes from the frame gradient's own mid tones so the
   buttons read as machined out of the same piece. */
.iph__b{position:absolute;border-radius:2px;
  background:linear-gradient(180deg,#B4B7BE,#8C9097)}
.iph__b--mute{left:-1.5px;top:34px;width:2px;height:15px}
.iph__b--up{left:-1.5px;top:56px;width:2px;height:25px}
.iph__b--dn{left:-1.5px;top:87px;width:2px;height:25px}
.iph__b--pwr{right:-1.5px;top:62px;width:2px;height:33px}

.pair__line{display:flex;gap:8px;align-items:center}
.pair__line i{width:5px;height:5px;border-radius:99px;background:var(--ter);
  animation:pairdot 1.15s ease infinite}
.pair__line i:nth-child(2){animation-delay:.12s}
.pair__line i:nth-child(3){animation-delay:.24s}
.pair__line i:nth-child(4){animation-delay:.36s}
.pair__line i:nth-child(5){animation-delay:.48s}
@keyframes pairdot{0%,100%{opacity:.25;transform:none}40%{opacity:1;transform:translateX(3px)}}
.pair__check{position:absolute;left:50%;top:50%;width:38px;height:38px;margin:-19px 0 0 -19px;
  border-radius:99px;background:var(--ink);opacity:0;transform:scale(.4);
  transition:opacity .3s,transform .45s cubic-bezier(.34,1.56,.64,1)}
.pair__check::after{content:"";position:absolute;left:11px;top:12px;width:14px;height:8px;
  border-left:2.5px solid #fff;border-bottom:2.5px solid #fff;transform:rotate(-45deg)}
.pair.ok .pair__check{opacity:1;transform:scale(1)}
.pair.ok .pair__line i{animation:none;opacity:0}
.pair__status{font-size:14.5px;font-weight:600;color:var(--sec)}
.pair.ok .pair__status{color:var(--ink)}
@media (prefers-reduced-motion:reduce){
  .xbag,.filt__f--out,.rocker,.pwrled,.pair__line i{animation:none}
  .xbag{opacity:0}
  .pwrled{opacity:1}
}

/* node 7 — the drawn cartridge lifting out of the real render */
.xfil{display:flex;flex-direction:column;align-items:center;gap:12px}
.filt__f--out{position:static;transform:none}
.xfil__a{width:2px;height:26px;background:var(--ter);position:relative;opacity:.7}
.xfil__a::after{content:"";position:absolute;left:50%;bottom:-1px;width:9px;height:9px;
  border-right:2px solid var(--ter);border-bottom:2px solid var(--ter);
  transform:translateX(-50%) rotate(45deg)}
.xfil__pur{height:196px}

/* ── the large page glyphs, and the live scan list ───────────────────────
   Owner SVGs, 2026-08-18. Embedded as data URIs — see GLYPH_B64 for why. */
/* 0.8x on 2026-08-19 (owner: "you can scale down the big jumbo engraved
   icons... by 0.8x because now they are too big for the new top layout").
   96 -> 77, 104 -> 83. These are PAGE HEADERS and nothing smaller may take
   them — a list row gets a plain monoline mark instead, see slist()'s icon. */
.gly{display:block;background:center/contain no-repeat;flex:0 0 auto}
.gly--bt{width:77px;height:77px;background-image:var(--glybt)}
.gly--wifi{width:83px;height:77px;background-image:var(--glywifi)}
.gly--check{width:77px;height:77px;background-image:var(--glycheck)}
.gly--bell{width:77px;height:77px;background-image:var(--glybell)}

/* the list header: a count that climbs, and a spinner that stops when done.
   ⚠ NOT `.scan` — that class is already the QR-viewfinder component, and
   reusing it silently inherited height:190px/display:grid and collapsed this
   list to nothing. Same class-collision trap as .link/.cta/.otp. */
.slist{flex:0 0 auto;margin:2px 0 16px}
.slist__h{display:flex;align-items:center;justify-content:space-between;
  font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ter);
  font-weight:600;padding:0 2px 10px}
.slist__s{width:15px;height:15px;border-radius:50%;flex:0 0 auto;
  border:1.7px solid rgba(11,11,11,.16);border-top-color:rgba(11,11,11,.42);
  animation:spin 900ms linear infinite}
/* ⚠ `.slist--done`, NOT `.done`: build-auth.py's sheet CSS (imported into
   this stylesheet) uses a bare `.done` for the sign-in end card, at
   position:absolute;display:none — adding `done` to this list made the
   whole thing vanish. Third collision of this kind; state classes get a
   component prefix from here on. */
.slist--done .slist__s{animation:none;border-top-color:rgba(11,11,11,.16)}
@keyframes spin{to{transform:rotate(360deg)}}
.slist__l{display:flex;flex-direction:column;gap:10px}
/* a result row. Arrives rather than appears — it is a thing that was found. */
.sr{display:flex;align-items:center;gap:12px;width:100%;background:var(--panel);
  border-radius:14px;padding:11px 13px;box-shadow:var(--shs);flex:0 0 auto;
  animation:srin .34s cubic-bezier(.2,0,0,1) both}
@keyframes srin{from{opacity:0;transform:translateY(7px)}}
.sr[hidden]{display:none}
.sr__i{width:30px;height:30px;border-radius:9px;flex:0 0 auto;
  background:linear-gradient(165deg,#F4F4F4,#E4E4E6);position:relative;
  display:grid;place-items:center;color:var(--sec)}
.sr__i svg{width:16px;height:16px}
/* the render tile: same 30px slot, but the render needs room to breathe and
   keeps its own aspect (`.rnd` sets `--ar` per SKU), so height leads and
   width follows. `overflow:hidden` because the 500 is the tallest and would
   otherwise poke out of the rounded corners. */
.sr__i--rnd{overflow:hidden;padding:3px 0;
  background:linear-gradient(160deg,#FFF,#E9E9EB)}
.sr__i--rnd .rnd{height:100%;width:auto}
.sr__t{flex:1;display:flex;flex-direction:column;gap:1px;min-width:0;text-align:left}
.sr__t b{font-size:14.5px;letter-spacing:-.012em}
.sr__t span{font-size:11.5px;color:var(--ter)}
.sr__w{display:flex;align-items:center;gap:9px;flex:0 0 auto}
/* A padlock and a signal meter, drawn at list-row size. The previous pair
   reused the big Wi-Fi glyph shrunk to 15px, which read as a smudge. */
.sr__lock{flex:0 0 auto;opacity:.62;color:var(--ink)}
.sr__lock::after{content:"";position:absolute;left:0;bottom:0;width:11px;height:8px;
  border-radius:2px;background:var(--ink)}
.sr__lock::before{content:"";position:absolute;left:2px;top:.5px;width:7px;height:7px;
  box-sizing:border-box;border:1.7px solid var(--ink);border-bottom:0;
  border-radius:4px 4px 0 0}
/* the Wi-Fi row's strength meter. Renamed off `.sig` 2026-08-19 — see
   sigbars() for why that collision hid the value it was drawing. */
.sigm{display:block;flex:0 0 auto;color:var(--ink);opacity:.72}

/* Node 9 — the light ON the device. The purifier is the carried hero at its
   largest; the glow and the bar are pinned to --ledy, each SKU's real
   indicator position. LAW 2: the green is a bloom, never a flat disc. */
/* fit-content, so .ledp is EXACTLY the purifier's box: the overlays are
   absolutely positioned and contribute nothing to grid sizing, which
   makes top:var(--ledy) a percentage of the DEVICE rather than of the
   visual half. That mismatch is what put the light off the device. */
.ledp{position:relative;display:grid;place-items:center;
  width:fit-content;height:fit-content;margin:auto}
.ledp__pur{height:250px}
.ledp__glow,.ledp__bar{position:absolute;left:50%;top:var(--ledy);
  transform:translate(-50%,-50%);pointer-events:none;
  animation:ledbl 2.6s ease-in-out infinite}
.ledp__glow{width:190px;height:190px;border-radius:99px;
  background:radial-gradient(circle,rgba(108,204,124,.34) 0%,rgba(108,204,124,.11) 40%,
    rgba(108,204,124,0) 70%)}
.ledp__bar{width:5px;height:26px;border-radius:99px;
  background:linear-gradient(180deg,#8FDC9C,#4FC266);
  box-shadow:0 0 14px 4px rgba(108,204,124,.75)}
@keyframes ledbl{0%,100%{opacity:1}50%{opacity:.32}}

/* THE CARRY. When one pairing screen hands the purifier to the next, the
   screen itself must not slide — a translating parent would drag the hero
   with it and the FLIP would fight the transition. So a carried screen has
   no slide at all: the purifier flies, and everything else fades in behind
   it. */
.scr.carry{animation:none}
/* everything that is NOT the carried object fades in behind it */
.scr.carry .pgb,.scr.carry .pgt>*:not([data-carry]),
.scr.carry .sheet__c,.scr.carry .mark{animation:carryin .42s ease .1s both}
@keyframes carryin{from{opacity:0;transform:translateY(6px)}}
/* A carried sheet GROWS to its new height; it must not replay its arrival.
   Not carried (the splash hand-off) and auRise still plays, which is the one
   place that motion is wanted. */
.au .sheet[data-carried]{animation:none}
.scr.carry .sheet__c--stagger>*{animation:none}

/* decoded once at boot rather than mid-transition — see warmAssets() */
.pre{position:absolute;left:0;top:0;width:1px;height:1px;opacity:.01;
  pointer-events:none;z-index:-1;
  background-image:var(--rnd200),var(--rnd500),var(--rndmax),var(--btphone),
    var(--reskey),var(--kcard),var(--glybt),var(--glywifi)}

@media (prefers-reduced-motion:reduce){
  .ledp__glow,.ledp__bar{animation:none}
  .scr.carry .pgb,.scr.carry .pgt>*:not([data-carry]){animation:none}
}
"""

# ── the sign-in sheet, nodes 1-5 ────────────────────────────────────────────
# Appended rather than written here: build-auth.py owns every value in it and
# reads them from the token files, so this is the one part of this stylesheet
# that is not raw hex. build-flow.py's re-skin does not need to touch it — it
# is already the new language, which is the point of the merge.
#
# `.sheet`-scoped selectors in that file are what keep its .cta / .field /
# .otp / .iconbtn from colliding with this one's.
CSS += AUTH.CSS_BG + AUTH.CSS_SHEET + """
/* the photograph, painted once for all eight sheet screens — see au() */
/* ⚠ ONE declaration of the photo, read by BOTH the node 1-3 sheets and the
   node 4-5 ones. Owner, 2026-08-20: "a bg image that needs to be the bg from
   1-5 page". Nodes 4 and 5 were on the flat `--grad` canvas because that is
   what the owner asked for when those sheets were built; putting the photo
   behind them too is the change. Held in a custom property rather than
   repeating the data URI: the second copy would add ~100KB and could drift.
   ⚠ NO SCRIM on 4-5. The `.ovl__s` that nodes 1-3 carry is 42%% black, and
   this photograph is near-white — the scrim is what makes near-black type
   readable over a busy image, and these two screens put an opaque sheet over
   it instead. Flagged for the owner: with a photo this bright, 1-3's scrim
   may now be heavier than it needs to be. */
.phone{--aubg:%s}
.au .bg__img{background-image:var(--aubg);background-size:cover;background-position:center}
""" % AUTH.background_css() + r"""
/* the join: a sheet screen is full-bleed, so it drops this harness's padding,
   and its status bar sits over the photograph rather than in the flow */
.scr:has(.au){padding:0}

/* ── centred sheet titles ─────────────────────────────────────────────────
   Owner, 2026-08-20: "for the bottom sheets make the title headers centered,
   also center the otp 'edit number'."

   ⚠ A fit-content BLOCK IGNORES THE PARENT'S text-align — a regression I
   introduced earlier today. `.grad` shrinks a heading to its own text so the
   gradient's ends land on the first and last letter, which is necessary, and it
   silently un-centred every sheet heading the moment the gradient went
   flow-wide. `text-align:center` was still doing its job — centring the text
   inside a box that now hugged it. Auto margins are what centre a shrunk block.

   ⚠ AND IT HAS TO LIVE HERE, AFTER `AUTH.CSS_SHEET`. Written 40 lines earlier
   in this file it lost to build-auth's `.sheet__c p,.sheet__c h1{margin:0}` —
   not on specificity (`.sheet .h1` is (0,2,0) and beats (0,1,1)) but because
   the auth stylesheet is injected AFTER that region, so the shorthand reset a
   longhand set by an earlier, more specific rule. Proven by setting the margin
   inline, which centred it immediately: a layout that works under an inline
   style and not under a rule is a cascade problem, never a geometry one. */
.sheet .h1{margin-left:auto;margin-right:auto}
/* ⚠ And once more for the OVERLAY sheets (nodes 4, 5). `.ovl .sheet .h1` is
   (0,3,0) and already set `margin:0 0 8px`, so the rule above — (0,2,0) — lost
   to it and only the auth sheets centred. Matching the specificity and keeping
   its bottom margin is the fix; the two rules are a pair and the second is not
   redundant. */
.ovl .sheet .h1{margin:0 auto 8px}
/* the OTP's "Edit number" — `align-self:flex-start` in the auth sheet */
.sheet .s-link{align-self:center}
.au{position:absolute;inset:0}
.au .sbar{position:absolute;top:0;left:0;right:0;z-index:20;padding:15px 22px 0}
""" + """
/* There is no sheet controller in this harness — no `data-sheet` is ever set,
   so the sheet is simply in place and plays its arrival as an animation. The
   screen's markup is re-inserted on every visit, so walking S0 -> A1 with the
   arrow key replays the real 880ms settle rather than merely describing it. */
.au .sheet{transform:none;animation:auRise %(dur)sms %(ease)s both}
@keyframes auRise{from{transform:translateY(calc(100%% + %(inset)spx))}}
""" % {"dur": AUTH.D["entrance"], "ease": AUTH.E["entrance"],
       "inset": AUTH.SHEET_INSET}

# ── the permission alert, recipes.dialog ────────────────────────────────────
# The same large-surface treatment as the sheet: 34 corners at 100% smoothing,
# the #F9F9F9 + 24% fill, a 1px white inside stroke, a drop shadow. Kept here
# rather than in the raw block above because every value is read from the
# token file, and mixing the two is how raw hex creeps back in.
CSS += """
.dlg{border-radius:%(r)spx;box-shadow:%(shadow)s}
.dlg__s{position:absolute;inset:0;z-index:0;background:%(fill)s;%(surface)s}
/* The CONTENT layer takes the same mask, without the stroke. The button row
   runs full-bleed to the dialog's edge, so its divider — and any pressed
   fill added later — has to be cut by the SAME superellipse as the surface.
   Clipping it with `border-radius` instead would be a circular arc inside a
   superellipse, and the mismatch shows first at exactly the corner everyone
   looks at. */
.dlg__b{%(mask)s}

/* ── CONTROL LABELS, flow-wide ───────────────────────────────────────────
   The owner's 2026-08-19 redline sizes the sheet's three CTAs at 14 / 12 / 12.
   These are the SAME controls on a full page, so they take the same register:
   without this, the label jumps 14 -> 16.5 at every sheet-to-page hand-off
   (A3 -> A4 most visibly), which is the kind of seam the flow has been getting
   redlined for. Sizes come from recipes.buttonPrimary / buttonQuiet.

   ⚠ Appended deliberately. The base rule above is `.cta,.cta2` at the same
   specificity (0,1,0), so this wins on order, not weight — do not "fix" it by
   adding a parent selector here, and do not move it above that rule. */
.cta{font-size:%(pri)spx;font-weight:%(priw)s}
.cta2{font-size:%(sec)spx;font-weight:%(secw)s}
.qlink{font-size:%(sec)spx;font-weight:%(secw)s}

/* ══ THE THREE CTAs, AND THE ONE BLACK ═══════════════════════════════════
   Owner, 2026-08-19: "Go to the first login sheet page. Look at the primary
   black one. The secondary, the white one, and the tertiary, the one without
   the container. These are the three correct CTAs. Follow these CTAs
   throughout... All of a sudden, on the number five OTP page, the CTA changes
   to a solid black. We cannot be doing those silly mistakes."

   They were right, and the cause was structural rather than careless. THIS
   FILE predates the token loader and declared its own buttons in raw hex:
   `.cta` was `background:var(--ink)` — #0B0B0B, FLAT, no shadow. The sheet's
   `.s-cta` reads recipes.buttonPrimary — the ink GRADIENT (#3A3A38 -> #2E2E2C)
   with a real drop shadow. Two stylesheets, two buttons, and node 5's OTP
   sheet pulled the page one because `sheetover()` calls `cta()`. Pointing
   both at the same recipe is the only fix that stays fixed; matching them by
   eye is what produced the drift.

   ⚠ #0B0B0B IS NOT A FILL. Owner: "do not use any other black. Don't use the
   absolute black color." `--ink` is the TEXT colour and stays that. Every
   dark SURFACE — CTA, selected chip, toggle track — takes the ink gradient. */
.cta{background:%(priBg)s;color:%(priFg)s;border-radius:%(pillR)spx;
  height:%(priH)spx;box-shadow:%(priEl)s}
.cta:hover{background:%(priBg)s}
.cta.off{background:%(offBg)s;color:%(offFg)s;box-shadow:none;cursor:default}
.cta2{background:%(secBg)s;color:%(secFg)s;border-radius:%(pillR)spx;
  height:%(secH)spx;box-shadow:%(secEl)s,inset 0 0 0 %(bevelW)spx %(bevel)s}
.cta2:hover{background:%(secBg)s}
/* tertiary: no container at all, and never a shadow — that IS the hierarchy */
.qlink{background:none;box-shadow:none;color:%(terFg)s}

/* ══ THE BACK BUTTON — recipes.buttonIcon, the locked one ════════════════
   Owner: "You are not using the correct back button... It has a stroke. It was
   kind of a 3D with drop shadow. You have completely removed and ruined that.
   Use the previous button style that we have. We had already locked it. Do not
   change it. You can refer to the mobile OTP bottom sheet."

   The sheet's `.iconbtn` was the locked one. `.nb` had drifted to a flat
   `var(--panel)` fill with neither the 1px white INSIDE stroke (the thing that
   makes it read as glass) nor the shadow. Both now read recipes.buttonIcon, so
   there is exactly ONE back button in the product and `nav()` renders the same
   chevron the sheet does — see BACK_SVG. */
.nav button.nb{width:%(icoSz)spx;height:%(icoSz)spx;background:%(icoBg)s;
  color:%(icoFg)s;border-radius:%(pillR)spx;
  box-shadow:%(icoEl)s,inset 0 0 0 %(bevelW)spx %(bevel)s}
/* pressing DARKENS a raised control; it never brightens it (LAW 3) */
.nav button.nb:hover{background:%(n100)s}
.nav button.nb:active{background:%(n150)s;transform:scale(%(press)s)}

/* ══ CHIPS AND THE TOGGLE ════════════════════════════════════════════════
   Owner: "the bedroom, living room, selected chips are not the correct color
   and do not have the inner shadow like our final CTA... toggle styles also
   are not 3D and are very dark."

   Both were `background:var(--ink)` — the absolute black again, flat. A
   selected chip is a small dark surface, so it takes the SAME black and the
   same shadow as the primary CTA; the gradient's lighter top edge is the
   inner-shadow read. Unselected chips get the raised-white treatment with the
   white inside stroke, so the pair reads as lifted rather than as outlined.
   ⚠ recipes.chipSelected says a selected chip should be WHITE-lift, not a
   dark fill — that disagrees with this instruction and is logged as C-15 in
   memory/decisions.md rather than silently resolved either way. */
.chip{background:%(secBg)s;color:%(secFg)s;
  box-shadow:%(secEl)s,inset 0 0 0 %(bevelW)spx %(bevel)s}
.chip:hover{background:%(secBg)s}
.chip.on,.chip.on:hover{background:%(priBg)s;color:%(priFg)s;box-shadow:%(priEl)s}
.chip.dim{background:%(offBg)s;color:%(terFg)s;box-shadow:none}
.tog{background:%(togOff)s;box-shadow:inset 0 1px 2px rgba(0,0,0,.10)}
.tog.on{background:%(priBg)s;box-shadow:%(secEl)s}
.tog::after{box-shadow:%(knobEl)s}

/* ⚠ THE ROOM PICKER IS A THIRD SELECTION COMPONENT, and it had its own copy of
   the same absolute-black fill. `.chip.on`, `.tog.on` and `.rs__t.on` were
   three independent declarations of "selected", which is exactly how a design
   system rots: the owner named the room chips ("the bedroom, living room,
   selected chips"), and fixing only `.chip.on` would have left this one wrong
   while looking fixed. Same values as the chips above, deliberately — a room
   tab IS a chip, it just lives inside the picker.
   Checkboxes are included for the same reason: `.chk.on` was the ink too. */
.rs__t{background:%(secBg)s;color:%(secFg)s;
  box-shadow:%(secEl)s,inset 0 0 0 %(bevelW)spx %(bevel)s}
.rs__t:hover{background:%(secBg)s}
.rs__t.on,.rs__t.on:hover{background:%(priBg)s;color:%(priFg)s;box-shadow:%(priEl)s}
/* ── the custom room ────────────────────────────────────────────────────
   Reads as one of the tabs, not as a form control, because it is the same
   decision as the six beside it. Dashed edge is the one place in this flow
   that borrows the placeholder idiom deliberately: it marks a slot the person
   fills rather than a choice already drawn. */
.rs__t--add{display:inline-flex;align-items:center;gap:6px;color:var(--sec);
  background:transparent;box-shadow:none;
  border:1px dashed rgba(11,11,11,.22)}
.rs__t--add:hover{background:rgba(255,255,255,.6)}
.rs__t--add svg{width:15px;height:15px;flex:0 0 auto}
.rs__new{display:flex;gap:8px;align-items:center;margin:0 0 10px}
.rs__new[hidden]{display:none}
.rs__newin{flex:1 1 auto;min-width:0}
.rs__newok{flex:0 0 auto;height:42px;padding:0 16px;border-radius:12px;
  font-size:14px;font-weight:600;background:%(priBg)s;color:%(priFg)s;
  box-shadow:%(priEl)s}
.rs__newok[disabled]{background:%(offBg)s;color:%(offFg)s;box-shadow:none}
.chk.on{border-color:transparent;background:%(priBg)s;box-shadow:%(secEl)s}
.rad.on{border-color:%(radOn)s;box-shadow:inset 0 0 0 5px %(radOn)s}

/* ══ THE SELECTED DEVICE CARD ════════════════════════════════════════════
   `.pcard.on` drew a 2px ABSOLUTE-BLACK outline. build-flow.py has re-skinned
   it to LIFT since 2026-08-18 — its own note calls that "the single biggest
   visual change in the file" — so the prototype and the flow rendering have
   been showing the same screen two different ways, the same split the phone's
   ground had. Brought in line here: raised white with the white inside stroke.

   ⚠ A card LIFTS, a chip FILLS, and that is now an unresolved inconsistency
   rather than a decision — LAW 3 says selection is "never an outline and never
   a fill", but the owner's 2026-08-19 instruction is explicitly that a selected
   chip takes the CTA's black fill. Logged as C-15 in memory/decisions.md; I
   have followed the owner for chips and LAW 3 for cards, which is the
   least-wrong reading of both, not a resolution of them. */
/* The lift has to be LEGIBLE, or "selection is lift" just means "selection is
   invisible". Unselected cards drop to `card` and the selected one rises to
   `floating` — two steps of the elevation scale apart, which is what makes the
   difference read at a glance without an outline. First attempt used `control`
   for both and the selected card was indistinguishable. */
.pcard{box-shadow:%(cardEl)s}
.pcard.on{background:%(secBg)s;
  box-shadow:%(liftEl)s,inset 0 0 0 %(bevelW)spx %(bevel)s}
.pcard:not(.on){background:%(cardBg)s}
""" % {"r": AUTH.RC["dialog"]["borderRadius"],
       "shadow": AUTH.EL["floating"]["css"],
       "fill": AUTH.RC["dialog"]["background"],
       # the three CTAs, the back button, chips and the toggle — all read from
       # the same recipes the sign-in sheet uses. See the CSS comments above.
       "priBg": AUTH.RC["buttonPrimary"]["background"],
       "priFg": AUTH.RC["buttonPrimary"]["color"],
       "priH": AUTH.RC["buttonPrimary"]["height"],
       "priEl": AUTH.RC["buttonPrimary"]["elevation"]["css"],
       "secBg": AUTH.RC["buttonQuiet"]["background"],
       "secFg": AUTH.RC["buttonQuiet"]["color"],
       "secH": AUTH.RC["buttonQuiet"]["height"],
       "secEl": AUTH.RC["buttonQuiet"]["elevation"]["css"],
       "terFg": AUTH.C["text"]["tertiary"],
       "offBg": AUTH.C["surface"]["muted"],
       "offFg": AUTH.C["text"]["inverse"],
       "pillR": AUTH.R["full"],
       "bevel": AUTH.C["border"]["bevel"],
       "bevelW": AUTH.LAY["bevelWidth"],
       "icoSz": AUTH.RC["buttonIcon"]["size"],
       "icoBg": AUTH.RC["buttonIcon"]["background"],
       "icoFg": AUTH.RC["buttonIcon"]["color"],
       "icoEl": AUTH.RC["buttonIcon"]["elevation"]["css"],
       "n100": AUTH.N["100"], "n150": AUTH.N["150"],
       "press": AUTH.SCL["press"],
       "cardEl": AUTH.EL["card"]["css"],
       "liftEl": AUTH.EL["floating"]["css"],
       "cardBg": AUTH.C["surface"]["sunken"],
       "radOn": AUTH.C["surface"]["inverse"],
       "togOff": AUTH.RC["toggle"]["trackOff"],
       "knobEl": AUTH.RC["toggle"]["knobElevation"],
       "pri": AUTH.TX[AUTH.RC["buttonPrimary"]["textStyle"]]["size"],
       "priw": AUTH.TX[AUTH.RC["buttonPrimary"]["textStyle"]]["weight"],
       "sec": AUTH.TX[AUTH.RC["buttonQuiet"]["textStyle"]]["size"],
       "secw": AUTH.TX[AUTH.RC["buttonQuiet"]["textStyle"]]["weight"],
       "mask": AUTH.SQ.surface_css(
           AUTH.RC["dialog"]["borderRadius"], AUTH.RC["dialog"]["smoothing"]),
       "surface": AUTH.SQ.surface_css(
           AUTH.RC["dialog"]["borderRadius"], AUTH.RC["dialog"]["smoothing"],
           stroke=AUTH.RC["dialog"]["strokeColor"],
           stroke_width=AUTH.RC["dialog"]["strokeWidth"])}


# ═══════════════════════════════════════════════════════════════════════════
# RUNTIME_JS — the interaction layer, shared verbatim by build-prototype.py and
# build-export.py. It lives here as a plain string (single braces) rather than
# inside the f-string BODY, because the export needs the identical code and a
# second hand-maintained copy is exactly how the flat board drifted from the
# prototype on 2026-08-06. Both embed this; neither reimplements it.
#
# Contract: the host page must define `go(target)`. Everything else is self
# contained. Every wirer degrades to an instant, tappable state change under
# prefers-reduced-motion.
# ═══════════════════════════════════════════════════════════════════════════
# ── one component-dispatch list for every rendering ─────────────────────────
# build-flow.py, build-export.py and this file each mount screens their own
# way, and each used to carry its OWN copy of the wiring calls. Adding node 4's
# profile card wired it in one of the three and silently not the others, which
# reads as "the JS is broken" rather than as a missing line. One list now; the
# three mount functions interpolate it.
WIRE_JS = """
  el.querySelectorAll('.pcard[data-sku]').forEach(wirePick);
  el.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => go(b.dataset.go)));
  el.querySelectorAll('[data-cmp=counter]').forEach(wireCounter);
  el.querySelectorAll('[data-cmp=carousel]').forEach(wireCarousel);
  el.querySelectorAll('[data-cmp=door]').forEach(wireDoor);
  el.querySelectorAll('[data-cmp=peel]').forEach(wirePeel);
  el.querySelectorAll('[data-cmp=hold]').forEach(wireHold);
  el.querySelectorAll('[data-cmp=rooms]').forEach(wireRooms);
  el.querySelectorAll('[data-cmp=countup]').forEach(wireCountup);
  /* the old screen's cards are gone, and any loop still driving them is
     superseded — see tiltFrame()'s generation check */
  TILT.cards = []; TILT.gen++;
  el.querySelectorAll('[data-cmp=profile]').forEach(wireProfile);
  el.querySelectorAll('.kcard[data-tilt]').forEach(wireCardTilt);
  el.querySelectorAll('[data-cmp=otp]').forEach(wireOtp);
  el.querySelectorAll('[data-cmp=doorkey]').forEach(wireDoorKey);
  el.querySelectorAll('[data-cmp=pairing]').forEach(wirePairing);
  el.querySelectorAll('[data-cmp=load]').forEach(wireLoad);
  el.querySelectorAll('[data-cmp=slist]').forEach(wireSlist);
  /* the scan is the SKU picker since node 6 was deleted — see slist() */
  el.querySelectorAll('.sr[data-sku]').forEach(wirePick);
  el.querySelectorAll('[data-cmp=keys]').forEach(wireKeys);
  el.querySelectorAll('[data-cmp=success]').forEach(wireSuccess);
  el.querySelectorAll('[data-cmp=splash]').forEach(wireSplash);
  el.querySelectorAll('[data-cmp=wallet]').forEach(wireWallet);
  el.querySelectorAll('[data-cmp=ways]').forEach(wireWays);
  wireBinds(el);
  wireSheet(el);
  placeHero(el);
  placeKey(el);
  wireCarry(el);
"""


PROFILE_JS = r"""
/* ── node 4 · the master key, and the two fields that drive it ──────────────
   The card is not a picture of a card: everything on it is bound to what is
   typed underneath. Kept in PROFILE so it survives leaving the screen and
   coming back — the harness rebuilds a screen's markup on every visit, and a
   key that forgot your name the moment you walked away would be a poor key.

   ⚠ `email` was here through 2026-08-18; the card's second field is the
   mobile number as of 2026-08-19 (email moved to nodes 2-3's sheet — see
   build-auth.py). `mobile`/`mobileVerified` are new; the merged flow's
   nodes 4/4a/5 are still static snapshots (au_state()'s own convention), so
   nothing here actually flips `mobileVerified` yet — it exists for whichever
   screen next makes node 4 genuinely interactive rather than a snapshot per
   state, and defaults to the SAME value 4a's snapshot already renders by hand. */
/* `typed` tracks which fields the user has actually entered. The values above
   are DEMO defaults so that jumping straight to node 5b shows a realistic
   card rather than scaffolding — but node 4's inputs must not be pre-filled
   from them, because that screen's whole subject is that nothing has been
   entered yet. `typed` is what tells those two intentions apart. */
const PROFILE = {name: 'Ruhaan Royce', mobile: '9876543210', mobileVerified: false,
                 img: '', typed: {}};

/* THE CARD'S ENTRANCE IS ONCE PER RUN. Owner, 2026-08-19: it "will only be a
   one time thing... It is only gonna come in once on the number four page.
   Then it is gonna be static until the key card is created."
   Why it replayed: this harness rebuilds a screen from its stored HTML on
   every visit, so `kcard--enter` arrives fresh each time — including on the
   walk back from node 5's OTP sheet and on node 4a. The flag is checked in
   wireProfile, which runs in the SAME task as the appendChild, so the class is
   gone before the first paint and the animation never starts rather than being
   cut off mid-flight. Reset by `reset()` so replaying the flow replays it. */
let cardEntered = false;

function wireProfile(card){
  const scr   = card.closest('.scr');
  /* see `cardEntered` — the flip is once per run, not once per visit.
     ⚠ BOTH HALVES, together. The card flipping down from the top and the
     fields rising from the bottom are ONE entrance ("meanwhile, the text and
     everything comes in from the bottom half"), so they have to be gated by
     the same flag. Stripping only the card's class left the content replaying
     `pgbIn` on every return to node 4 while the card sat still — half an
     animation, which reads worse than either whole. */
  if (card.classList.contains('kcard--enter')){
    if (cardEntered){
      card.classList.remove('kcard--enter');
      if (scr) scr.querySelectorAll('.pgb--enter')
                  .forEach(el => el.classList.remove('pgb--enter'));
    } else {
      cardEntered = true;
    }
  }
  /* ⚠ `scr` is null for the TRAVELLING card (`KH`), which lives outside the
     screens — so every screen-scoped step below is guarded. Painting is shared
     with it through paintCard(), so the mini card in the corner shows the same
     name you typed rather than the placeholder. */
  /* ⚠ THE FIELD BINDING IS NOT HERE ANY MORE — see wireBinds(). It used to
     live in this function, which only runs for a `[data-cmp=profile]` CARD, and
     node 4 stopped having a card in the 2026-08-20 rebuild. The inputs were
     therefore never wired at all: typing did nothing and Proceed could not be
     enabled. Binding form fields to the presence of an unrelated element was
     the bug; wireBinds() runs per SCREEN and does not care what else is on it. */
  /* ⚠ THE AVATAR PICKER IS GONE TOO (owner, 2026-09-09). A FileReader-backed
     picture picker lived here; the card has no avatar to put one in any more,
     so `PROFILE.img` is now written by nothing and read by nothing. Left in
     PROFILE rather than ripped out, because the field is harmless and a
     re-introduced avatar would want it back. */

  paintCard(card);
}

/* ── node 5a · the wallet opens ────────────────────────────────────────────
   Owner, 2026-08-20: "when the user presses tap to open... the sleeve is going
   to slide out of the bottom". The CARD DOES NOT MOVE — the sleeve leaves it.
   That is the whole read of the gesture: you are drawing the wallet away, not
   pulling the card out, so what you are left looking at is the key.

   Tapping the card counts as well as tapping the button. The house rule is
   that the gesture is the delight and never the toll gate (see wireDoorKey),
   so Enter works too and reduced motion goes straight through. */
function wireWallet(el){
  const scr = el.closest('.scr');
  const btn = scr && scr.querySelector('[data-walopen]');
  let opened = false;
  function open(){
    if (opened) return;
    opened = true;
    if (btn) btn.disabled = true;
    if (REDUCE()){ go('A7'); return; }
    el.classList.add('out');
    /* 820ms is the sleeve's own transition; the extra beat lets it clear the
       frame before the screen changes under it. */
    touts.push(setTimeout(() => go('A7'), 980));
  }
  el.addEventListener('click', open);
  if (btn) btn.addEventListener('click', open);
  if (scr){
    scr.setAttribute('tabindex', '0');
    scr.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') open();
    });
  }
}

/* ── node 5b · which key did you make ─────────────────────────────────────
   The choice lives on `.phone` as `data-kc`, never on a card. Three cards can
   be alive at once — this screen's, the travelling mini and the door's — and a
   per-card value would let them disagree about which key you made. Same
   reasoning as `PICK` for the purifier's SKU, and it survives navigation for
   the same reason: the element that holds it is not a screen. */
let WAY = '__KCDEF__';
function wireWays(el){
  const phone = document.querySelector('.phone');
  const dots = [...el.querySelectorAll('.sw')];
  const apply = (k) => {
    WAY = k;
    if (phone) phone.dataset.kc = k;
    dots.forEach(d => d.classList.toggle('on', d.dataset.kc === k));
    if (KH) paintCard(KH);        /* the corner card is the same key */
  };
  dots.forEach(d => d.addEventListener('click', () => apply(d.dataset.kc)));
  apply(WAY);                      /* re-entering the screen shows your choice */
}

/* ── MO-GYRO · the key card catches light ──────────────────────────────────
   Owner, 2026-08-19: gyroscope on a phone, and "just for desktop, just for
   our reference" the same thing on hover so the effect can be judged on a
   laptop. Both drive the SAME three custom properties, so there is one visual
   path and the desktop preview cannot drift from the real thing:

       --gx / --gy   deflection, -1..1
       --gi          |deflection|, 0..1 — how hard it is catching light

   ⚠ NEVER SPRINGS. rules/motion.md gate 4: ambient motion uses `standard` at
   most. This is steered continuously by the hand holding the phone, so
   overshoot would feel loose rather than playful. `gyro.follow` is a per-frame
   approach to the target — damping for sensor jitter, not an easing.

   ⚠ ONE rAF LOOP FOR ALL CARDS, and it only runs while a card is on screen.
   A per-card loop would multiply with the travelling card and the door's card
   both alive; and the loop is registered on `rafs`, so leaving a screen stops
   it rather than animating a detached node forever. */
const GY = __GYRO__;
/* `gen` supersedes loops instead of a boolean. ⚠ THE FIRST VERSION USED
   `on:true` AS A GUARD AND THE LOOP DIED AFTER ONE NAVIGATION: `clearTimers()`
   cancels every handle in `rafs` on each screen change, but the guard then
   refused to restart it — so the shimmer worked on the first card screen only
   and silently never again. It also pushed a handle every frame, growing
   `rafs` at 60/sec. Bumping a generation kills the old loop and starts one
   clean loop per screen, with nothing to leak. */
let TILT = {x: 0, y: 0, tx: 0, ty: 0, bound: false, gen: 0, cards: []};

function tiltFrame(gen){
  if (gen !== TILT.gen) return;              /* superseded, or stopped */
  TILT.x += (TILT.tx - TILT.x) * GY.follow;
  TILT.y += (TILT.ty - TILT.y) * GY.follow;
  const gi = Math.min(1, Math.hypot(TILT.x, TILT.y));
  for (const c of TILT.cards){
    c.style.setProperty('--gx', TILT.x.toFixed(3));
    c.style.setProperty('--gy', TILT.y.toFixed(3));
    c.style.setProperty('--gi', gi.toFixed(3));
  }
  requestAnimationFrame(() => tiltFrame(gen));
}

/* The sensor. `beta`/`gamma` are absolute, and nobody holds a phone at zero —
   so the FIRST reading becomes the neutral and everything after it is a delta.
   Assuming a posture (a fixed 45deg, say) makes the card sit permanently
   deflected for anyone lying down. */
let GNEUTRAL = null;
function onOrient(e){
  if (e.beta == null || e.gamma == null) return;
  if (!GNEUTRAL) GNEUTRAL = {b: e.beta, g: e.gamma};
  const dz = GY.deadzoneDeg, span = 22;
  const db = e.beta - GNEUTRAL.b, dg = e.gamma - GNEUTRAL.g;
  const nz = (v) => Math.abs(v) < dz ? 0 : Math.max(-1, Math.min(1, v / span));
  TILT.tx = nz(dg);
  TILT.ty = nz(db);
}

/* iOS 13+ will not deliver orientation without an explicit grant, and the
   request has to come from a real gesture — so it is asked for on the first
   tap anywhere in the phone, once, and never re-prompted. */
let GASKED = false;
function askGyro(){
  if (GASKED) return;
  GASKED = true;
  const D = window.DeviceOrientationEvent;
  if (!D) return;
  if (typeof D.requestPermission === 'function'){
    D.requestPermission().then(r => {
      if (r === 'granted') addEventListener('deviceorientation', onOrient);
    }).catch(() => {});
  } else {
    addEventListener('deviceorientation', onOrient);
  }
}

function wireCardTilt(card){
  if (REDUCE()) return;
  /* The entrance animation owns `transform` while it plays — and with `both`
     fill it keeps owning it forever. So the tilt cannot take over until the
     class is gone; stripping it on animationend is what hands `transform` over.
     (A card with no entrance is free immediately.) */
  if (card.classList.contains('kcard--enter')){
    card.addEventListener('animationend', () => card.classList.remove('kcard--enter'),
                          {once: true});
  }
  TILT.cards.push(card);
  if (TILT.cards.length > 1) return;   /* one loop and one binding per screen */
  tiltFrame(TILT.gen);

  /* DESKTOP PREVIEW ONLY. Pointer position across the phone stands in for
     turning the device, so the same three properties get driven and the
     effect can be reviewed without a handset. Deliberately the phone's box
     and not the card's: you are pretending to tilt the DEVICE. */
  /* the listeners are attached ONCE for the document's life — the loop is
     what restarts per screen, not the bindings */
  const phone = document.getElementById('phone');
  if (phone && !TILT.bound){
    TILT.bound = true;
    phone.addEventListener('pointermove', e => {
      if (e.pointerType === 'touch') return;      /* real touch uses the sensor */
      const r = phone.getBoundingClientRect();
      TILT.tx = Math.max(-1, Math.min(1, ((e.clientX - r.left) / r.width - .5) * 2));
      TILT.ty = Math.max(-1, Math.min(1, ((e.clientY - r.top) / r.height - .5) * -2));
    });
    phone.addEventListener('pointerleave', () => { TILT.tx = 0; TILT.ty = 0; });
    phone.addEventListener('pointerdown', askGyro, {once: true});
  }
  askGyro();
}

/* Everything live on a key card, for ANY key card — the one on node 4, the one
   on the door, and the travelling mini in the corner. Extracted from
   wireProfile so the three cannot show different names. */
/* ── the sheet MORPHS between pages, it does not snap ─────────────────────
   Owner, 2026-08-20: "either the bottom sheet enlarges and shrinks then the
   content appears rather than size of the bottomsheet suddenly snapping to the
   different size on the next page... page 1 content will dissolve and the
   bottom sheet will shorten in height and then the page 2 content will dissolve
   appear."

   ⚠ THIS IS DONE ENTIRELY ON THE ARRIVING SCREEN, and that is not a shortcut —
   it is forced. render() removes the outgoing screen in the SAME frame it
   appends the new one (deliberately, to kill a white flash), so there is no
   outgoing sheet left to animate. What the eye gets instead is the same
   sequence: the new sheet opens at the OLD height with its content already
   hidden, so the frame you see is the sheet you were just looking at minus its
   contents; it resizes; then the new content dissolves in. Two sheets that look
   identical make the substitution invisible.

   `offsetHeight`, not `getBoundingClientRect()`: the harness scales the whole
   phone, and the height being written back is a CSS px value.

   A screen with no sheet clears the chain, so arriving at a sheet from a
   non-sheet page plays no morph — there is nothing to morph FROM. */
let SHEETH = null;
function wireSheet(el){
  const sheet = el.querySelector('.sheet');
  if (!sheet){ SHEETH = null; return; }
  const c = sheet.querySelector('.sheet__c');
  const target = sheet.offsetHeight;
  const from = SHEETH;
  SHEETH = target;
  /* the first sheet of a run has nothing to morph FROM and plays its own
     arrival instead */
  if (from == null) return;
  if (REDUCE()){ return; }

  /* ⚠ THE DISSOLVE IS UNCONDITIONAL, THE RESIZE IS NOT. Owner, 2026-08-20:
     the effect was missing on nodes 4 and 5 — and the reason was that node 4's
     sheet and node 5's are BOTH 359 tall, by coincidence of their content. The
     old early-return bailed on equal heights and took the content fade with it,
     so those two pages swapped their contents instantly while every other pair
     dissolved. Height and content are two separate promises: only one of them
     is about the box changing size. */
  const grows = Math.abs(from - target) >= 2;
  const GROW = grows ? 380 : 0, FADE = 240;
  if (c){ c.style.transition = 'none'; c.style.opacity = '0'; }
  if (grows){
    sheet.style.transition = 'none';
    sheet.style.height = from + 'px';
  }
  sheet.getBoundingClientRect();          /* commit before animating */
  if (grows){
    sheet.style.transition = 'height ' + GROW + 'ms cubic-bezier(.4,0,.2,1)';
    sheet.style.height = target + 'px';
  }
  touts.push(setTimeout(() => {
    /* hand the height back to the content — a sheet pinned to a px value would
       stop responding to anything that changes inside it */
    sheet.style.transition = '';
    sheet.style.height = '';
    if (c){
      c.style.transition = 'opacity ' + FADE + 'ms linear';
      c.style.opacity = '1';
    }
  }, GROW));
}

/* ── the profile fields, and everything downstream of them ────────────────
   Owner, 2026-08-20: "the text fields are not working on the 4 number page.
   make the page 4 working and whatever the user types will appear on the
   keycard and further pages."

   ⚠ THIS RUNS PER SCREEN, deliberately. The binding used to live in
   wireProfile(), which runs per CARD — so when node 4 became a sheet with no
   card, the inputs silently stopped being wired. A form field's behaviour must
   not depend on whether some other element happens to be on the screen.

   Everything the typing feeds is repainted from one place: any card on this
   screen, the travelling corner card, node 5a's greeting, and any gated CTA. */
function wireBinds(el){
  const gates = [...el.querySelectorAll('[data-gate]')];
  const inputs = [...el.querySelectorAll('[data-bind]')];
  /* ⚠ Gates read the INPUTS, not PROFILE. PROFILE carries demo defaults, so
     gating on it would enable node 4's Proceed while its fields sat visibly
     empty — the button and the form disagreeing about the same question. */
  const filled = (k) => {
    const inp = el.querySelector('[data-bind="' + k + '"]');
    return inp ? !!inp.value.trim() : !!(PROFILE[k] || '').trim();
  };
  const repaint = () => {
    el.querySelectorAll('.kcard').forEach(paintCard);
    if (KH) paintCard(KH);
    /* node 5a greets you by first name only — "Welcome, Ruhaan Royce" reads
       like a form receipt. No name yet falls back to a greeting rather than to
       a placeholder, so jumping straight in never shows scaffolding. */
    el.querySelectorAll('[data-wname]').forEach(n => {
      const f = (PROFILE.name || '').trim().split(/\s+/)[0];
      n.textContent = f || 'there';
    });
    gates.forEach(b => {
      const ok = b.dataset.gate.split(',').every(k => filled(k.trim()));
      b.disabled = !ok;
      b.classList.toggle('off', !ok);
    });
  };
  inputs.forEach(inp => {
    const k = inp.dataset.bind;
    if (PROFILE.typed[k]) inp.value = PROFILE[k];   /* come back to what you typed */
    inp.addEventListener('input', () => {
      PROFILE[k] = inp.value;
      PROFILE.typed[k] = true;
      repaint();
    });
  });
  repaint();
}

function paintCard(card){
  if (!card) return;
  const n = PROFILE.name.trim();
  const words = n.split(/\s+/).filter(Boolean);
  const set = (sel, txt) => { const el = card.querySelector(sel); if (el) el.textContent = txt; };
  /* Initials from the first two words; the big serif one is the first letter
     of the name, which is what the reference shows. */
  /* `[data-inits]` / `[data-ini]` were the avatar's initials and the serif
     watermark; both are gone. `set()` is a no-op on a missing target, so this
     is removed rather than left to silently match nothing. */
  set('[data-cname]', n || 'Your name');
  set('[data-cmob]', PROFILE.mobile.trim() ? '+91 ' + PROFILE.mobile.trim() : 'Enter number');
}


/* ── D1 · drag the key to the lock ─────────────────────────────────────────
   Three ways through, per the house rule that the gesture is the delight and
   never the toll gate: drag the card onto the lock, tap the card (it glides
   up by itself), or press Enter. Reduced motion goes straight through. */
function wireDoorKey(el){
  const wrap = el.querySelector('.dk__card');
  const card = wrap.querySelector('.kcard');
  const lock = el.querySelector('.dk__lock');
  let done = false, dragging = false, x0 = 0, y0 = 0, moved = 0;
  /* The harness scales the whole phone to fit the viewport, so pointer deltas
     arrive in SCREEN space while transforms apply in the card's LOCAL space.
     Without this the card moves at half the finger's speed on a fitted phone
     and the glide stops short of the lock. */
  const phoneScale = () => {
    const ph = el.closest('.phone');
    return ph ? ph.getBoundingClientRect().width / ph.offsetWidth : 1;
  };

  function unlock(){
    if (done) return;
    done = true;
    el.classList.remove('drag');
    if (REDUCE()) { go('HOME'); return; }
    el.classList.add('open');
    touts.push(setTimeout(() => go('HOME'), 1650));
  }
  function nearLock(){
    const c = card.getBoundingClientRect(), l = lock.getBoundingClientRect();
    return !(c.right < l.left - 12 || c.left > l.right + 12 ||
             c.top > l.bottom + 12 || c.bottom < l.top - 12);
  }
  /* tap / Enter: the card glides to the lock on its own */
  function glide(){
    if (done) return;
    if (REDUCE()) { unlock(); return; }
    const k = phoneScale();
    const c = card.getBoundingClientRect(), l = lock.getBoundingClientRect();
    const dx = ((l.left + l.width / 2) - (c.left + c.width / 2)) / k;
    const dy = ((l.top + l.height / 2) - (c.top + 40 * k)) / k;
    card.style.transform = `translate(${dx}px,${dy}px) rotate(-4deg) scale(.9)`;
    touts.push(setTimeout(unlock, 430));
  }

  wrap.addEventListener('pointerdown', e => {
    if (done) return;
    dragging = true; moved = 0; x0 = e.clientX; y0 = e.clientY;
    /* the drag class kills the card's settle transition BEFORE the first
       move; capture last and guarded, because it throws on synthetic
       pointers and must never take the state with it */
    el.classList.add('drag');
    try { wrap.setPointerCapture(e.pointerId); } catch (_) {}
  });
  wrap.addEventListener('pointermove', e => {
    if (!dragging || done) return;
    const k = phoneScale();
    const dx = (e.clientX - x0) / k, dy = (e.clientY - y0) / k;
    moved = Math.max(moved, Math.abs(dx) + Math.abs(dy));
    card.style.transform = `translate(${dx}px,${Math.min(40, dy)}px) rotate(${dx * .015}deg)`;
    if (nearLock()) { dragging = false; unlock(); }
  });
  const drop = () => {
    if (done) return;
    el.classList.remove('drag');
    if (dragging && moved < 8) { dragging = false; glide(); return; }
    dragging = false;
    card.style.transform = '';                    /* spring back */
  };
  wrap.addEventListener('pointerup', drop);
  wrap.addEventListener('pointercancel', drop);
  el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') glide(); });
}




/* ── nodes 11 and 13 · the live scan ──────────────────────────────────────
   The count starts at zero with the spinner turning and results arrive in
   place. Rows ship in the markup (so the board and the export still show what
   the list contains) and are revealed here. Timeouts ride `touts`, so leaving
   the screen cancels the scan instead of firing into a detached DOM. */
function wireSlist(el){
  const rows = [...el.querySelectorAll('.sr')];
  const out = el.querySelector('[data-count]');
  const label = el.dataset.label || '';
  let n = 0;
  const show = () => { out.textContent = '(' + n + ') ' + label.toUpperCase(); };
  show();
  if (REDUCE()) {
    rows.forEach(r => r.hidden = false);
    n = rows.length; show(); el.classList.add('slist--done');
    return;
  }
  rows.forEach((r, i) => touts.push(setTimeout(() => {
    r.hidden = false; n++; show();
    if (n === rows.length) el.classList.add('slist--done');
  }, 900 + i * 620)));
}


/* ── node 18a · picking who gets a key ────────────────────────────────────
   One list, two views of it: a contact is either a row or a pill, never both.
   The CTA counts the selection, and its label pluralises rather than reading
   "Share keys (1)". */
function wireKeys(el){
  const scr = el.closest('.scr');
  const pills = el.querySelector('[data-pills]');
  const cta = scr && scr.querySelector('[data-keycta]');
  const rows = [...el.querySelectorAll('.kc')];

  const toast = scr && scr.querySelector('[data-toast]');
  let sent = false;

  function label(){
    if (!cta || sent) return;
    const n = pills.children.length;
    cta.textContent = n === 0 ? 'Share key'
                   : n === 1 ? 'Share key (1)'
                   : 'Share keys (' + n + ')';
  }
  /* Sharing raises the toast and then moves on by itself (owner, 2026-08-18:
     "no need for the user to press continue again"). A confirmation you have
     to acknowledge is a screen wearing a toast's clothes; this one is seen,
     not dismissed. The wait is long enough to read three words and no longer. */
  if (cta) cta.addEventListener('click', () => {
    if (sent) return;
    sent = true;
    cta.disabled = true;
    if (toast) toast.classList.add('on');
    touts.push(setTimeout(() => go('D1'), REDUCE() ? 600 : 1400));
  });
  function add(row){
    row.hidden = true;
    const hue = row.dataset.hue;
    const pill = document.createElement('button');
    pill.className = 'kp';
    pill.innerHTML = '<span class="kp__a kp__a--' + hue + '">'
      + row.querySelector('.kc__a').textContent + '</span>'
      + '<span>' + row.dataset.name + '</span><i class="kp__x"></i>';
    pill.addEventListener('click', () => { pill.remove(); row.hidden = false; label(); });
    pills.appendChild(pill);
    label();
  }
  rows.forEach(r => r.addEventListener('click', () => add(r)));
  label();
}

/* ── THE CARRY ─────────────────────────────────────────────────────────────
   Two mechanisms, for two different problems.

   ONE PURIFIER, MOVED. `.phero` is a single render created once at boot and
   parked outside the screens. Pairing screens carry invisible `.pslot` boxes
   that declare where it should be; `placeHero` reads the slot and moves the
   one element there with a transform. Nothing is recreated, so nothing
   re-rasterises — which is what the flicker was. Only a compositor property
   changes between screens.

   FLIP, for the sign-in. `data-carry="<key>"` still FLIPs an element from the
   matching element on the previous screen. `bg` keeps the photograph from
   re-rendering across nodes 1-3; `sheet` makes the sheet grow between states
   instead of replaying its arrival.

   ⚠ BOTH DECISIONS ARE MADE BEFORE THE SCREEN IS APPENDED. Measuring forces a
   style recalc, so if the incoming screen still carried `.scr.in` every rect
   would be read through the slide's translateX and every animation would start
   offset and snap. That was the "jerk between pages". `carryClass()` reads the
   markup first. */
const CARRY = {};
let PICK = '200';
let PH = null;                       /* the one purifier */

/* ── THE KEY CARD'S JOURNEY ────────────────────────────────────────────────
   Owner, 2026-08-19: "right now the card seems very disjointed... The card
   shrinks to the top right and it stays there till the tap your key card to
   the door page... This is to basically create a story of the card."

   Same idea as `.phero` above and for the same reason — ONE element, moved by
   transform, never re-created — but with a difference that matters: the
   purifier only exists where a screen declares a slot for it, whereas this card
   has to persist across SIX screens that say nothing about it at all. So it
   has a third state the purifier does not: PARKED.

       hidden   before node 5a. The card has not been made yet.
       parked   docked top-right at 0.2x, from node 5a's celebration through
                pairing, Wi-Fi, the permissions and the household. The screens
                in between do not mention it; it simply stays put while they
                change underneath.
       slotted  node 18/D1 declares `[data-kslot]`, so it flies there full-size
                and HANDS OFF to the door's own card.

   ⚠ IT HANDS OFF RATHER THAN BECOMING the door's card. `wireDoorKey` drags a
   real element and hit-tests it against the lock; making that element the
   travelling card would put the drag physics on a node living outside the
   screen. So the mini flies to the real card's rect, the real card fades up
   underneath it, and the mini goes away — the seam is covered by both being
   the same artwork in the same place. */
let KH = null;                       /* the one key card */
/* ⚠ WHERE IN THE FLOW THE KEY CAME INTO EXISTENCE. Owner, 2026-08-20: "the
   behavior for when the card goes to top right will only happen on the 5c
   card and if user goes to previous steps the card will not be on the top
   right."
   `KH.dataset.live` alone could not express that: once the celebration armed
   it, it stayed armed, so stepping BACK to 5b or node 4 still parked a key
   card in the corner — on screens where the user has not been given a key
   yet. Recorded as a sequence POSITION rather than a screen id so it stays
   correct if 5c moves, and compared against `idx` rather than `cur()` so an
   off-sequence edge state inherits the position of the node it branches off
   instead of matching nothing. */
let KEYAT = null;
/* ⚠ REWRITTEN 2026-08-20 (owner): the card no longer shrinks to the top RIGHT.
   "rather than the card shrinking to the right, the contents disappear and the
   card turn in perspective... it will shrink to the top center in a
   perspective view. No text will be on it just the card bg colors."
   So: centred horizontally, laid back on its X axis so it foreshortens into a
   thin form, and stripped of every live element — see `.khero--parked`.
   `tilt` is a rotation in degrees, not a duration. The three numbers were
   solved against the owner's reference frame, in which the parked card measures
   roughly 93 x 33 at the top centre: 0.28 and 75 deg render 95 x 33 once the
   perspective's ~1.28x magnification is accounted for.
   `top` is 64 because the owner asked for the parked card to sit ON THE BACK
   BUTTON'S LINE: that button's centre is at 80 on every screen that has one
   (`.sbar` 56 + 4 padding + half of 40), the folded card measures 31.9 tall,
   so 80 - 31.9/2 = 64. Measured, because the rendered height of a
   perspective-folded card is not a number worth deriving by hand. */
const KPARK = {scale: 0.28, top: 64, tilt: 75};

function carryClass(html, dir){
  const keys = (html.match(/data-carry="[\w-]+"/g) || [])
                 .map(m => m.slice(12, -1));
  const flip = keys.some(k => CARRY[k]);
  /* a screen that hands the purifier on must not slide either, or the phone
     would move under an element that is deliberately standing still */
  const holds = /data-pslot/.test(html) && PH && PH.dataset.live === '1';
  return (flip || holds) ? 'carry' : (dir === 'back' ? 'bk' : 'in');
}

function wirePick(card){
  card.addEventListener('click', () => {
    PICK = card.dataset.sku || '200';
    const ph = document.querySelector('.phone');
    if (ph) {
      ph.classList.remove('sku-200', 'sku-500', 'sku-max');
      ph.classList.add('sku-' + PICK);
    }
    const thumb = card.querySelector('.pcard__r');
    if (thumb) CARRY.pur = thumb.getBoundingClientRect();   /* fly from here */
    card.parentNode.querySelectorAll('.pcard').forEach(c => c.classList.remove('on'));
    card.classList.add('on');
  }, true);      /* capture: must beat the [data-go] handler that navigates */
}

/* Move the one render onto this screen's slot. Geometry is converted out of
   screen space into the phone's own space, because the harness scales the whole
   phone to fit and a transform applies in the untransformed box. */
function placeHero(el){
  if (!PH) return;
  const slot = el.querySelector('[data-pslot]');
  /* Leaving the pairing world: fade on the screen's own clock, so the device
     does not blink out from under a screen that is still arriving. */
  if (!slot){ PH.style.opacity = '0'; PH.dataset.live = '0'; return; }

  const phone = document.querySelector('.phone');
  const pr = phone.getBoundingClientRect();
  const k = pr.width / phone.offsetWidth || 1;
  const rectToLocal = (r) => ({
    x: (r.left - pr.left) / k, y: (r.top - pr.top) / k, h: r.height / k });
  const put = (t, animate) => {
    PH.style.transition = animate ? '' : 'none';
    PH.style.transform =
      `translate(${t.x}px,${t.y}px) scale(${t.h / PH.offsetHeight})`;
    if (!animate) PH.getBoundingClientRect();   /* commit before re-enabling */
  };

  const to = rectToLocal(slot.getBoundingClientRect());
  if (PH.dataset.live !== '1'){
    /* first appearance — start on node 6's tile, then fly to the slot */
    put(rectToLocal(CARRY.pur || slot.getBoundingClientRect()), false);
    PH.style.opacity = '1';
    PH.dataset.live = '1';
    requestAnimationFrame(() => put(to, true));
  } else {
    put(to, true);
  }
}

/* Where the travelling card should be for THIS screen. Geometry is converted
   out of screen space into the phone's own space for the same reason
   placeHero() does it: the harness scales the whole phone, and a transform
   applies in the untransformed box. */
function placeKey(el){
  if (!KH) return;
  const phone = document.querySelector('.phone');
  if (!phone) return;
  const pr = phone.getBoundingClientRect();
  const k = pr.width / phone.offsetWidth || 1;
  const slot = el.querySelector('[data-kslot]');

  /* ⚠ A SLOT WINS OVER THE "BEFORE THE KEY EXISTED" CHECK, and the order here is
     the whole of the owner's request: "when the user goes back from anywhere
     before page 6, user will be taken to page 5b and the card will expand again
     to the center." Node 5b sits BEFORE the screen that created the key, so the
     retire branch below would have blinked the card out of existence on arrival.
     Declaring 5b a slot makes it RECEIVE the card instead — the same flight the
     door already used, run backwards — and because the slot hides its own card
     until the traveller lands, there is only ever one card on screen. */
  if (KH.dataset.live === '1' && slot){
    const r = slot.getBoundingClientRect();
    const x = (r.left - pr.left) / k, y = (r.top - pr.top) / k;
    /* full size again, flat, with its contents fading back. `--parked` STAYS on
       (see its CSS note): the origin must not change mid-flight.
       ⚠ WITH `transform-origin:50% 0`, A SCALE NO LONGER PUTS THE LEFT EDGE AT
       `x`. The box [0,W] maps to [W(1-s)/2, W(1+s)/2], so landing the visible
       left edge on the slot means x = slotLeft - W(1-s)/2. The top needs no
       correction: the origin's y is 0, so scaling leaves it where it is. */
    KH.classList.remove('khero--bare');
    const sc = (r.height / k) / KH.offsetHeight;
    putKey(x - KH.offsetWidth * (1 - sc) / 2, y, sc, true, 0, SLOTROLL(slot));
    slot.classList.add('kslot--handoff');
    touts.push(setTimeout(() => {
      slot.classList.remove('kslot--handoff');
      KH.style.opacity = '0';
      KH.dataset.live = '2';           /* spent: the screen has it now */
      /* handed over BEFORE the key's origin, so the next walk forward through
         5c has to arm it again from scratch */
      if (KEYAT !== null && idx < KEYAT) KEYAT = null;
    }, REDUCE() ? 0 : 620));
    return;
  }

  /* before the key existed, there is no key to show — see KEYAT */
  if (KEYAT !== null && idx < KEYAT){
    KH.style.opacity = '0';
    KH.dataset.live = '0';
    KEYAT = null;      /* going forward through 5c re-arms it from scratch */
    return;
  }
  if (KH.dataset.live !== '1') return;
  park(true);
}

/* A slot may ask for the card to land slightly off-square. Read from the DOM
   rather than passed down a call chain, so the value lives next to the screen
   it belongs to instead of inside the travelling card's code. */
function SLOTROLL(slot){ return +(slot.dataset.kroll || 0); }

function putKey(x, y, sc, animate, tilt, roll){
  KH.style.transition = animate ? '' : 'none';
  /* ⚠ THE TRANSLATE GOES OUTSIDE THE PERSPECTIVE. Written the other way round
     first — `perspective(460px) translate(...) scale(...) rotateX(...)` — and the
     card rendered 608px wide inside a 390px phone. The reason: the list applies
     right-to-left, so putting `perspective()` leftmost makes it project the
     TRANSLATED geometry, and a point 150px from the perspective origin is
     magnified by its distance. With the translate first, the perspective only
     ever sees the scale and the rotation, which is all it should. */
  /* ⚠ AND THE ROTATE GOES LEFT OF THE SCALE. Right-to-left again: with
     `scale() rotateX()` the card rotates at FULL size first, so its bottom edge
     swings 350*sin(64) = 314px toward a 460px camera and the projection
     magnifies everything 3.2x — measured 284px wide inside a 390px phone.
     Rotating the ALREADY-SHRUNK card moves it ~100px in Z instead of ~314, and
     the magnification drops to about 1.3. */
  const t = tilt ? ` perspective(460px) rotateX(${tilt}deg) scale(${sc})`
                 : ` scale(${sc})`;
  const z = roll ? ` rotate(${roll}deg)` : '';
  KH.style.transform = `translate(${x}px,${y}px)${t}${z}`;
  if (!animate) KH.getBoundingClientRect();      /* commit before re-enabling */
}

function park(animate){
  const phone = document.querySelector('.phone');
  if (!phone || !KH) return;
  /* ⚠ The parked state moves `transform-origin` to TOP CENTRE (see the CSS), so
     the card folds symmetrically about its own top edge instead of skewing away
     from a top-left pivot. With that origin the scale no longer moves the
     horizontal centre, which makes the centring arithmetic independent of the
     scale: the visible centre is always `x + offsetWidth/2`. */
  KH.classList.add('khero--parked');
  KH.classList.add('khero--bare');
  putKey((phone.offsetWidth - KH.offsetWidth) / 2, KPARK.top,
         KPARK.scale, animate, KPARK.tilt);
}

/* Node 5a hands the card over: the celebration card is measured, the mini is
   dropped exactly on top of it, the real one fades, and then the mini shrinks
   away to the corner. Called by wireSuccess() partway through that screen so
   the shrink is SEEN rather than happening between screens. */
function launchKey(fromCard){
  if (!KH || !fromCard) return;
  const phone = document.querySelector('.phone');
  if (!phone) return;
  const pr = phone.getBoundingClientRect();
  const k = pr.width / phone.offsetWidth || 1;
  const r = fromCard.getBoundingClientRect();
  paintCard(KH);
  putKey((r.left - pr.left) / k, (r.top - pr.top) / k,
         (r.height / k) / KH.offsetHeight, false);
  KH.style.opacity = '1';
  KH.dataset.live = '1';
  KEYAT = idx;                     /* this screen is where the key begins */
  fromCard.style.transition = 'opacity 160ms linear';
  fromCard.style.opacity = '0';
  if (REDUCE()){ park(false); return; }
  rafs.push(requestAnimationFrame(() => park(true)));
}

function wireCarry(el){
  const seen = {};
  el.querySelectorAll('[data-carry]').forEach(n => {
    const k = n.dataset.carry;
    const from = CARRY[k];
    const to = n.getBoundingClientRect();
    seen[k] = to;
    if (!from || !from.width || !to.width) return;
    /* marked even when it does not move: [data-carried] is what tells the
       sheet not to replay its arrival */
    n.setAttribute('data-carried', '');
    if (REDUCE()) return;
    const dx = (from.left + from.width / 2) - (to.left + to.width / 2);
    const dy = (from.top + from.height / 2) - (to.top + to.height / 2);
    const sx = from.width / to.width, sy = from.height / to.height;
    if (Math.abs(dx) < .5 && Math.abs(dy) < .5 &&
        Math.abs(sx - 1) < .004 && Math.abs(sy - 1) < .004) return;
    n.animate([{transform: `translate(${dx}px,${dy}px) scale(${sx},${sy})`},
               {transform: 'none'}],
              {duration: 620, easing: 'cubic-bezier(.2,0,0,1)'});
  });
  /* only keys the screen we just left actually had may carry onward */
  for (const kk in CARRY) if (kk !== 'pur') delete CARRY[kk];
  Object.assign(CARRY, seen);
}

/* Create the one purifier, and warm the heavy data-URI backgrounds, once at
   boot — they decode on first use otherwise, and that decode landed in the
   middle of a transition. */
(function boot(){
  const host = document.getElementById('phone');
  if (!host) return;
  PH = document.createElement('i');
  PH.className = 'phero';
  PH.dataset.live = '0';
  PH.setAttribute('aria-hidden', 'true');
  host.appendChild(PH);

  /* the travelling key card — one element, created once, never re-rendered */
  KH = document.createElement('div');
  KH.className = 'khero';
  KH.dataset.live = '0';
  KH.setAttribute('aria-hidden', 'true');
  KH.innerHTML = __KEYCARD_HTML__;
  host.appendChild(KH);
  const pre = document.createElement('div');
  pre.className = 'pre';
  pre.setAttribute('aria-hidden', 'true');
  host.appendChild(pre);
})();


/* ── node 15 · the bar fills, then the screen hands itself on ──────────────
   No CTA: the wait is the wait. Timeouts and the rAF ride the harness's
   cancel lists, so leaving the screen stops it rather than advancing out of a
   detached DOM. */
function wireLoad(el){
  const ms = +el.dataset.ms || 10000;
  const to = el.dataset.go;
  /* ⚠ THE ADVANCE IS UNCONDITIONAL. This used to open with
     `const bar = …; if (!bar) return;` — the timed hand-off was INSIDE the
     bar's branch, so the moment node 15 swapped its progress bar for the
     indeterminate loader (2026-08-19) the screen would have become a dead end
     with no bar, no button and no way forward. The wait is the contract here;
     whatever is drawn during it is decoration. */
  touts.push(setTimeout(() => go(to), REDUCE() ? 600 : ms + 260));

  /* A determinate bar, if this particular screen still has one. */
  const bar = el.querySelector('.pb i');
  if (!bar) return;
  if (REDUCE()){ bar.style.width = '100%'; return; }
  /* One CSS transition rather than a per-frame JS loop: the compositor owns
     the fill, so it cannot stutter against the carousel running beside it. */
  bar.style.width = '0%';
  touts.push(setTimeout(() => {
    bar.style.transition = 'width ' + ms + 'ms linear';
    bar.style.width = '100%';
  }, 30));
}

/* ── node 1 · the splash hands itself on ──────────────────────────────────
   Owner, 2026-08-20: "on page 1 splash screen, after 1 second the bottom
   sheet pops up automatically." Same data-ms/data-go contract as wireLoad and
   wireSuccess — the timing lives on the markup (see `au()`), not here, so the
   number is never duplicated between the builder and the runtime.
   REDUCE() is not special-cased: an unconditional 1s wait before the sheet
   arrives is already still, not a skip that motion.md's reduced-motion gate
   needs to shorten. */
function wireSplash(el){
  const to = el.dataset.go, ms = +el.dataset.ms || 1000;
  touts.push(setTimeout(() => go(to), ms));
}

/* ── node 5a · key card created ─────────────────────────────────────────
   Same data-ms/data-go auto-advance contract as wireLoad above, minus the
   progress bar: the card and caption animate on CSS alone (see the
   .ksucc/.kcard--enter rules), this only has to generate the confetti and
   then hand off. Reduced motion (LAW 2, no exceptions) skips the confetti
   and the card/caption keyframes entirely and just holds the plain result
   for a beat before advancing — a celebration is exactly the kind of
   discrete moment rules/motion.md allows spring on, but the accessibility
   gate still wins over the fun. */
function wireSuccess(el){
  /* The backdrop is pure CSS now — an expanding mask on a dot grid, see
     `.dmx__ring`. The confetti generator that used to live here (34 elements
     with per-piece vectors) went with the confetti on 2026-08-19; all this
     has left to do is hand the screen on.
     Reduced motion still advances faster: the ring is frozen mid-travel
     rather than animating, so there is no cycle to wait for. */
  const to = el.dataset.go, ms = +el.dataset.ms || 2600;
  /* Partway through the celebration the card stops being this screen's and
     becomes the journey's: it shrinks to the corner and stays there until the
     door. Timed so the shrink finishes before the screen advances. */
  const card = el.querySelector('.kcard');
  touts.push(setTimeout(() => launchKey(card), REDUCE() ? 200 : Math.max(0, ms - 900)));
  touts.push(setTimeout(() => go(to), REDUCE() ? 900 : ms));
}

/* ── node 11 · pairing resolves itself ─────────────────────────────────────
   Dots travel the line, the check lands, and the flow moves on. No button —
   the wait resolves itself, which is the honest version of what hold-to-pair
   was for. Timeouts ride `touts`, so leaving the screen cancels them. */
function wirePairing(el){
  const done = () => {
    el.classList.add('ok');
    const st = el.querySelector('[data-status]');
    if (st) st.textContent = 'Connected';
  };
  if (REDUCE()){ done(); touts.push(setTimeout(() => go(el.dataset.go), 900)); return; }
  touts.push(setTimeout(done, 2300));
  touts.push(setTimeout(() => go(el.dataset.go), 3400));
}

/* ── a code field you can type into ───────────────────────────────────────── */
function wireOtp(el){
  const n = +el.dataset.n, boxes = [...el.querySelectorAll('i')];
  const inp = el.querySelector('input');
  function paint(){
    const v = inp.value;
    boxes.forEach((b, i) => {
      b.textContent = v[i] || '';
      b.classList.toggle('at', i === v.length && v.length < n);
    });
  }
  inp.addEventListener('input', () => {
    inp.value = inp.value.replace(/\D/g, '').slice(0, n);
    paint();
  });
  el.addEventListener('click', () => inp.focus());
  paint();
}
"""


def css_out():
    """CSS with every embedded asset resolved. build-flow.py, build-export.py
    and build-wireframes.py all import this rather than repeating the
    substitutions — forgetting one used to be a silent missing-font bug."""
    SH, GY = AUTH.RC["cardShimmer"], AUTH.M["gyro"]
    FC = SH["face"]
    return (CSS.replace("__CANVAS__", AUTH.G["canvas"]["css"])
               # the shimmer. Face geometry is MEASURED off key-card.webp's
               # alpha — see recipes.cardShimmer. Re-exporting that artwork
               # invalidates these five numbers.
               .replace("__FACEL__", str(FC["left"]))
               .replace("__FACER__", str(FC["right"]))
               .replace("__FACET__", str(FC["top"]))
               .replace("__FACEB__", str(FC["bottom"]))
               .replace("__FACERX__", str(FC["radiusX"]))
               .replace("__FACERY__", str(FC["radiusY"]))
               .replace("__SHIMTILT__", str(GY["maxTiltDeg"]))
               .replace("__SHIMHOLO__", ",".join(SH["holo"]))
               .replace("__SHIMBLEND__", SH["blend"])
               .replace("__DOTPX__", str(SH["dotSize"]))
               .replace("__DOTR__", str(SH["dotRadius"]))
               .replace("__PATCHW__", str(SH["patchW"]))
               .replace("__PATCHH__", str(SH["patchH"]))
               .replace("__SHIMMAX__", str(SH["maxOpacity"]))
               .replace("__SHIMRIM__", str(SH["rimMax"]))
               .replace("__SHIMRIMT__", SH["rimTint"])
               .replace("__GEOPLATE__", "url(data:image/svg+xml;base64,%s)" % GEO["plate"])
               .replace("__GEOL__", "%.3f" % GEO["left"])
               .replace("__GEOT__", "%.3f" % GEO["top"])
               .replace("__GEOSZ__", "%.3f" % GEO["size"])
               .replace("__GEOTX__", "%.2f" % GEO["tx"])
               .replace("__GEOTY__", "%.2f" % GEO["ty"])
               .replace("__GEOFILL__", GEO["fill"])
               .replace("__REG__", FONTS["REG"])
               .replace("__MED__", FONTS["MED"])
               .replace("__BLD__", FONTS["BLD"])
               .replace("__SERIF__", SERIF_B64)
               .replace("__KCARD__", KEYCARD_B64)
               .replace("__KC1__", CARD_B64[1]).replace("__KC2__", CARD_B64[2])
               .replace("__KC3__", CARD_B64[3]).replace("__KC4__", CARD_B64[4])
               .replace("__KC5__", CARD_B64[5])
               .replace("__SLVB__", SLEEVE_B64["back"])
               .replace("__SLVF__", SLEEVE_B64["front"])
               .replace("__CARDAR__", CARD_AR)
               .replace("__TGA__", str(TITLEGRAD["angle"]))
               .replace("__TG1__", TITLEGRAD["stops"][0]["color"])
               .replace("__TG2__", TITLEGRAD["stops"][1]["color"])
               .replace("__TG3__", TITLEGRAD["stops"][2]["color"])
               .replace("__TGP1__", str(TITLEGRAD["stops"][0]["at"]))
               .replace("__TGP2__", str(TITLEGRAD["stops"][1]["at"]))
               .replace("__TGP3__", str(TITLEGRAD["stops"][2]["at"]))
               .replace("__CFL__", str(CARD_FACE["left"]))
               .replace("__CFR__", str(CARD_FACE["right"]))
               .replace("__CFT__", str(CARD_FACE["top"]))
               .replace("__CFB__", str(CARD_FACE["bottom"]))
               .replace("__CFRX__", str(CARD_FACE["radiusX"]))
               .replace("__CFRY__", str(CARD_FACE["radiusY"]))
               .replace("__RESKEY__", RESKEY_B64)
               .replace("__RND200__", RENDERS_B64["200"])
               .replace("__RND500__", RENDERS_B64["500"])
               .replace("__RNDMAX__", RENDERS_B64["max"])
               .replace("__BTPHONE__", BTPHONE_B64)
               .replace("__GLYBT__", GLYPH_B64["bluetooth"])
               .replace("__GLYWIFI__", GLYPH_B64["wifi"])
               .replace("__GLYCHECK__", GLYPH_B64["check-circle"])
               .replace("__GLYBELL__", GLYPH_B64["notifications-unread"]))


RUNTIME_JS = PROFILE_JS + r"""
let timers = [], touts = [], rafs = [];
function clearTimers(){
  timers.forEach(clearInterval); timers = [];
  touts.forEach(clearTimeout);   touts  = [];
  rafs.forEach(cancelAnimationFrame); rafs = [];
}
const REDUCE = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── node 1 · the door ─────────────────────────────────────────────────── */
function wireDoor(el){
  const pill  = el.querySelector('.en__pill');
  const track = el.querySelector('.en__track');
  let dragging = false, x0 = 0, p = 0, moved = 0, done = false;
  const span = () => track.clientWidth - pill.offsetWidth - 4;
  function set(v){
    p = Math.max(0, Math.min(1, v));
    el.style.setProperty('--p', p);          // drives leaf, door light AND slider green
    pill.style.transform = 'translateX(' + (p * span()) + 'px)';
  }
  function enter(){
    if (done) return;
    done = true;
    el.classList.remove('snap', 'drag');
    if (REDUCE()) { go(el.dataset.go); return; }
    set(1);
    el.classList.add('go');
    // The veil goes on .phone, not in this screen: render() destroys .scr at the
    // hand-off, so a white layer inside it would vanish exactly when it is doing
    // its job. On .phone it survives, and the next screen emerges out of it.
    const phone = el.closest('.phone');
    let veil = null;
    if (phone) {
      // never stack veils — a stranded one is a white sheet over the whole app
      phone.querySelectorAll('.en-veil').forEach(v => v.remove());
      veil = document.createElement('div');
      veil.className = 'en-veil';
      phone.appendChild(veil);
      // Force the initial style to be computed before flipping the class. Without
      // this the browser coalesces append+class into one style pass, no transition
      // runs, and the veil snaps to white instantly — hiding the entire door
      // sequence behind a white sheet from frame one. A rAF is NOT enough here.
      void veil.offsetHeight;
      veil.classList.add('on');
      // Hard backstop, scheduled NOW and deliberately untracked: whatever happens
      // downstream — an interrupted hand-off, a jump from the controller, a
      // throttled frame — this node comes out of the DOM. A veil that survives is
      // an opaque white page with no way back.
      setTimeout(() => { if (veil.parentNode) veil.remove(); }, 4200);
    }
    // 1700ms: copy+slider long gone, the doorway owns the viewport, veil is white
    touts.push(setTimeout(() => {
      go(el.dataset.go);
      if (!veil) return;
      // plain timeout, not rAF: this runs immediately after a synchronous
      // re-render and a dropped frame here would strand the veil at full white
      setTimeout(() => {
        veil.classList.add('off');
        setTimeout(() => { if (veil.parentNode) veil.remove(); }, 800);
      }, 30);
    }, 1700));
  }
  pill.addEventListener('pointerdown', e => {
    if (done) return;
    dragging = true; moved = 0; x0 = e.clientX;
    el.classList.remove('snap'); el.classList.add('drag');
    pill.setPointerCapture(e.pointerId);
  });
  pill.addEventListener('pointermove', e => {
    if (!dragging) return;
    const dx = e.clientX - x0;
    moved = Math.max(moved, Math.abs(dx));
    set(dx / span());
  });
  function release(){
    if (!dragging) return;
    dragging = false;
    if (moved < 7) return enter();          // a tap counts as a full slide
    if (p > 0.62)  return enter();          // past halfway commits
    el.classList.add('snap'); el.classList.remove('drag'); set(0);
  }
  pill.addEventListener('pointerup', release);
  pill.addEventListener('pointercancel', release);
  pill.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); enter(); }
  });
  set(0);
}

/* ── node 7 · peel the wrapper ─────────────────────────────────────────── */
function wirePeel(el){
  const wrap = el.querySelector('.pl__wrap'), tab = el.querySelector('.pl__tab');
  const H = 190;
  let dragging = false, y0 = 0, p = 0, moved = 0, base = 0;
  function set(v){
    p = Math.max(0, Math.min(1, v));
    wrap.style.clipPath = 'inset(' + (p * 100) + '% 0 0 0)';
    tab.style.transform = 'translateY(' + (p * H) + 'px)';
  }
  set(0);
  function finish(){
    el.classList.add('anim'); set(1); el.classList.add('done');
    touts.push(setTimeout(() => go(el.dataset.go), REDUCE() ? 0 : 540));
  }
  tab.addEventListener('pointerdown', e => {
    dragging = true; moved = 0; y0 = e.clientY; base = p;
    el.classList.remove('anim');
    tab.setPointerCapture(e.pointerId);
  });
  tab.addEventListener('pointermove', e => {
    if (!dragging) return;
    const dy = e.clientY - y0;
    moved = Math.max(moved, Math.abs(dy));
    set(base + dy / H);
  });
  function release(){
    if (!dragging) return;
    dragging = false;
    if (moved < 7)  return finish();          // tap plays the whole peel
    if (p > 0.55)   return finish();
    el.classList.add('anim'); set(0);
  }
  tab.addEventListener('pointerup', release);
  tab.addEventListener('pointercancel', release);
  tab.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); finish(); }
  });
}

/* ── node 11 · hold to pair ────────────────────────────────────────────── */
function wireHold(el){
  const fg = el.querySelector('.hr__fg'), btn = el.querySelector('.hr__btn');
  const ms = +el.dataset.ms || 1500, LEN = 540;
  let val = 0, holding = false, done = false, last = 0, raf = null, downAt = 0;
  const set = v => {
    val = Math.max(0, Math.min(1, v));
    fg.style.strokeDashoffset = LEN * (1 - val);
  };
  function finish(){
    if (done) return;
    done = true; set(1); el.classList.add('done');
    touts.push(setTimeout(() => go(el.dataset.go), REDUCE() ? 0 : 280));
  }
  function frame(now){
    if (done) return;
    if (!last) last = now;
    const dt = now - last; last = now;
    set(val + (holding ? dt / ms : -dt / (ms * 0.5)));
    if (val >= 1) return finish();
    if (val <= 0 && !holding) { last = 0; return; }
    raf = requestAnimationFrame(frame); rafs.push(raf);
  }
  btn.addEventListener('pointerdown', e => {
    if (done) return;
    downAt = performance.now();
    if (REDUCE()) return finish();
    holding = true; el.classList.add('on'); last = 0;
    btn.setPointerCapture(e.pointerId);
    raf = requestAnimationFrame(frame); rafs.push(raf);
  });
  function release(){
    if (done) return;
    // a quick tap completes it — the hold is the delight, not the toll gate
    if (performance.now() - downAt < 180) return finish();
    holding = false; el.classList.remove('on');
    if (!raf) { last = 0; raf = requestAnimationFrame(frame); rafs.push(raf); }
  }
  btn.addEventListener('pointerup', release);
  btn.addEventListener('pointercancel', release);
  btn.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); finish(); }
  });
}

/* ── node 17 · the morphing room ───────────────────────────────────────── */
function wireRooms(el){
  const rooms = JSON.parse(el.dataset.rooms);
  const items = el.querySelector('.rs__items');
  const shell = el.querySelector('.rs__shell');
  const tabs  = Array.from(el.querySelectorAll('.rs__t'));
  const NS = 'http://www.w3.org/2000/svg';
  const OX = 160, OY = 84, IX = 26, IY = 13, WALL = 56, R = 2.25;
  const P = (x, y, h) => [OX + (x - y) * IX, OY + (x + y) * IY - h];
  /* The stage's own ground, as a flat triple — the midpoint of the
     `.rs__stage` gradient (#FBFAF8 -> #E6E4DE). Compositing against one
     representative value rather than sampling the real gradient per polygon is
     a deliberate simplification: the error at the extremes is a couple of
     levels of grey and invisible, and the alternative is reading pixels back
     out of a live gradient every frame. */
  const GROUND = [241, 240, 235];
  const solid = (a) => {
    const m = 1 - a;
    return 'rgb(' + Math.round(GROUND[0] * m + 11 * a) + ','
                  + Math.round(GROUND[1] * m + 11 * a) + ','
                  + Math.round(GROUND[2] * m + 11 * a) + ')';
  };

  function poly(pts, fill){
    const n = document.createElementNS(NS, 'polygon');
    n.setAttribute('points', pts.map(q => q[0].toFixed(1) + ',' + q[1].toFixed(1)).join(' '));
    n.setAttribute('fill', fill);
    return n;
  }
  // floor + the two back walls, drawn once and never morphed. Gradient-filled
  // as of 2026-09-09 so the room reads as lit from the open corner rather than
  // as three flat greys — see roomstage()'s <defs>.
  shell.appendChild(poly([P(-R,-R,0), P(R,-R,0), P(R,-R,WALL), P(-R,-R,WALL)], 'url(#rsWallA)'));
  shell.appendChild(poly([P(-R,-R,0), P(-R,R,0), P(-R,R,WALL), P(-R,-R,WALL)], 'url(#rsWallB)'));
  shell.appendChild(poly([P(-R,-R,0), P(R,-R,0), P(R,R,0), P(-R,R,0)], 'url(#rsFloor)'));
  // where the two walls meet — a single hairline, which is what stops the room
  // reading as two disconnected planes
  const seam = document.createElementNS(NS, 'line');
  const s0 = P(-R,-R,0), s1 = P(-R,-R,WALL);
  seam.setAttribute('x1', s0[0]); seam.setAttribute('y1', s0[1]);
  seam.setAttribute('x2', s1[0]); seam.setAttribute('y2', s1[1]);
  seam.setAttribute('stroke', 'rgba(255,255,255,.5)');
  seam.setAttribute('stroke-width', '1');
  shell.appendChild(seam);

  let cur = rooms[+el.dataset.active].map(o => Object.assign({}, o));
  let raf = null;

  function draw(){
    while (items.firstChild) items.removeChild(items.firstChild);
    // painter's algorithm: far corner first, recomputed every frame because the
    // pieces genuinely swap depth order mid-morph
    cur.map((o, i) => i)
       .sort((a, b) => (cur[a].x + cur[a].y) - (cur[b].x + cur[b].y))
       .forEach(i => {
      const o = cur[i], h = Math.max(0.5, o.h);
      const A = [o.x - o.w, o.y - o.d], B = [o.x + o.w, o.y - o.d];
      const C = [o.x + o.w, o.y + o.d], Dp = [o.x - o.w, o.y + o.d];
      const g = document.createElementNS(NS, 'g');

      /* ⚠ THE CONTACT SHADOW GOES DOWN FIRST, and it is what stops the object
         looking pasted onto the floor. An ellipse on the floor plane, sized to
         the footprint and squashed by the isometric ratio, offset a little
         along the light direction. Skipped for anything essentially flat (a
         mat, a rug) — a 4px-high object casting a pool of shade reads wrong. */
      if (h > 7){
        const c0 = P(o.x, o.y, 0);
        const sh = document.createElementNS(NS, 'ellipse');
        sh.setAttribute('cx', (c0[0] + 2.5).toFixed(1));
        sh.setAttribute('cy', (c0[1] + 1.5).toFixed(1));
        sh.setAttribute('rx', ((o.w + o.d) * IX * 0.62).toFixed(1));
        sh.setAttribute('ry', ((o.w + o.d) * IY * 0.72).toFixed(1));
        sh.setAttribute('fill', 'url(#rsSh)');
        g.appendChild(sh);
      }

      /* Each face is TWO polygons: an OPAQUE tone underneath, which is what
         the morph interpolates, and a shared gradient over it, which is what
         makes it look lit. Keeping the tone a flat single colour is deliberate
         — a per-item gradient would mean building a <linearGradient> per object
         per frame.

         ⚠ OPAQUE IS THE WHOLE DIFFERENCE, AND IT WAS THE ACTUAL BUG. These
         faces were `rgba(11,11,11,a)`, so nothing occluded anything: you could
         see the back wall and the lamp straight through the bed, and every
         overlap darkened where the two translucent shapes crossed. That
         see-through look is what read as "wireframey" — no amount of gradient
         on top fixes it, because the problem is that the solid is not solid.
         `solid()` composites the same tone against the stage's own ground once,
         at full opacity, so the painter's-algorithm sort actually hides what is
         behind. Same greys as before; they just stop being transparent. */
      const face = (pts, tone, grad) => {
        g.appendChild(poly(pts, solid(tone)));
        g.appendChild(poly(pts, grad));
      };
      const fL = [P(Dp[0],Dp[1],0), P(C[0],C[1],0), P(C[0],C[1],h), P(Dp[0],Dp[1],h)];
      const fR = [P(B[0],B[1],0), P(C[0],C[1],0), P(C[0],C[1],h), P(B[0],B[1],h)];
      const fT = [P(A[0],A[1],h), P(B[0],B[1],h), P(C[0],C[1],h), P(Dp[0],Dp[1],h)];
      face(fL, 0.20 + o.t * 0.30, 'url(#rsL)');
      face(fR, 0.14 + o.t * 0.22, 'url(#rsR)');
      face(fT, 0.07 + o.t * 0.15, 'url(#rsTop)');

      /* The lit edge along the top face — the same idea as the large-surface
         recipe's 1px inside stroke, which is what reads as a finished material
         rather than a filled outline. */
      const lip = document.createElementNS(NS, 'polyline');
      lip.setAttribute('points', [fT[3], fT[0], fT[1]]
        .map(q => q[0].toFixed(1) + ',' + q[1].toFixed(1)).join(' '));
      lip.setAttribute('fill', 'none');
      lip.setAttribute('stroke', 'rgba(255,255,255,.55)');
      lip.setAttribute('stroke-width', '1');
      lip.setAttribute('stroke-linejoin', 'round');
      g.appendChild(lip);

      items.appendChild(g);
    });
  }

  // easeOutBack — a little overshoot, because choosing a room is a discrete
  // moment and the house style is springy there (motion rules, opening line)
  const ease = p => { const c1 = 1.02, c3 = c1 + 1;
    return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };

  function morph(to){
    if (raf) cancelAnimationFrame(raf);
    if (REDUCE()) { cur = to.map(o => Object.assign({}, o)); draw(); return; }
    const from = cur.map(o => Object.assign({}, o)), ms = 620, t0 = performance.now();
    (function step(now){
      const p = Math.min(1, (now - t0) / ms), e = ease(p);
      cur = from.map((o, i) => {
        const q = to[i], r = {};
        ['x','y','w','d','h','t'].forEach(k => { r[k] = o[k] + (q[k] - o[k]) * e; });
        return r;
      });
      draw();
      if (p < 1) { raf = requestAnimationFrame(step); rafs.push(raf); }
    })(t0);
  }

  /* `tabs` grows when a custom room is added, so selection is bound per-tab as
     tabs are created rather than over a snapshot of the list. */
  const bar = el.querySelector('.rs__bar');
  const addBtn = el.querySelector('[data-add]');
  function select(b, i){
    el.querySelectorAll('.rs__t').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    el.dataset.active = i;
    morph(rooms[i]);
    b.scrollIntoView({block: 'nearest', inline: 'nearest'});
  }
  function bind(b, i){ b.addEventListener('click', () => select(b, i)); }
  tabs.filter(b => b !== addBtn).forEach(bind);

  /* ── a room the person names themselves ─────────────────────────────────
     Owner, 2026-09-09: "there should also be an option to add your own room...
     your own name of the room."

     ⚠ WHAT THE DRAWING SHOWS FOR IT, AND WHY. The stage illustrates a room
     TYPE — the bed becomes the sofa becomes the counter — and a name we have
     never seen tells us nothing about what is in it.

     Tried first: an EMPTY room, all four slots sunk into the floor. It is the
     most honest picture and it animates beautifully, but at this stage size it
     just reads as a large pale box, i.e. exactly the unfinished look this pass
     was meant to remove. So a custom room gets a GENERIC arrangement instead —
     a seat, a back, a side table, something tall — which is deliberately not
     any of the six: it reads as "furniture" without claiming to know which.
     The alternative, inheriting whichever room was selected before, would have
     actively asserted a wrong answer. */
  const wrap = el.querySelector('[data-newwrap]');
  const input = el.querySelector('[data-newin]');
  const ok = el.querySelector('[data-newok]');
  const GENERIC = [{x:-0.30, y: 0.60, w:1.10, d:0.50, h:20, t:.22},   // seat
                   {x:-1.10, y: 0.60, w:0.16, d:0.50, h:34, t:.55},   // its back
                   {x: 0.70, y:-0.20, w:0.40, d:0.40, h:15, t:.38},   // side table
                   {x: 1.30, y:-0.90, w:0.14, d:0.14, h:40, t:.70}];  // tall thing
  function sync(){ if (ok) ok.disabled = !input.value.trim(); }
  if (addBtn && wrap && input && ok){
    sync();
    addBtn.addEventListener('click', () => {
      wrap.hidden = false;
      /* no focus on touch — a keyboard springing up over the illustration is
         the opposite of helpful when the illustration is the thing being
         chosen. Same test `focus()` uses elsewhere in this file. */
      if (!matchMedia('(hover: none)').matches) input.focus();
    });
    input.addEventListener('input', sync);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') commit(); });
    ok.addEventListener('click', commit);
  }
  function commit(){
    const name = input.value.trim();
    if (!name) return;
    rooms.push(GENERIC.map(o => Object.assign({}, o)));
    const i = rooms.length - 1;
    const b = document.createElement('button');
    b.className = 'rs__t';
    b.dataset.i = i;
    b.textContent = name;
    bar.insertBefore(b, addBtn);      /* the add tab stays last */
    bind(b, i);
    input.value = ''; sync(); wrap.hidden = true;
    select(b, i);
  }
  draw();
}

/* ── node 26 · the number arrives ──────────────────────────────────────── */
function wireCountup(el){
  const n = el.querySelector('.rd__n'), to = +el.dataset.to;
  if (REDUCE()) { n.textContent = to; return; }
  const ms = 1100, t0 = performance.now();
  (function step(now){
    const p = Math.min(1, (now - t0) / ms);
    n.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));  // standard, no spring
    if (p < 1) rafs.push(requestAnimationFrame(step));
  })(t0);
}

function wireCarousel(c){
  const slides = Array.from(c.querySelectorAll('.car__s'));
  const dots   = Array.from(c.querySelectorAll('.car__d'));
  const iv     = +c.dataset.interval || 2200;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 0, t = null;
  function show(n){
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    dots.forEach((d, k) => d.classList.toggle('on', k === i));
  }
  function start(){
    if (reduce) return;                       // motion gate 2: no auto-advance
    if (t) clearInterval(t);
    t = setInterval(() => show(i + 1), iv);
    timers.push(t);
  }
  dots.forEach(d => d.addEventListener('click', () => { show(+d.dataset.i); start(); }));
  show(0);
  start();
}
function wireCounter(c){
  const mn = +c.dataset.min, mx = +c.dataset.max;
  let v = +c.dataset.val;
  const row = c.querySelector('.figs'), num = c.querySelector('.cnt__n');
  const btns = c.querySelectorAll('.stp');
  function figure(i){
    const f = document.createElement('span');
    f.className = 'fig' + (i === 0 ? ' fig--you' : '');
    f.innerHTML = '<i></i><b></b>';
    return f;
  }
  function sync(){
    num.textContent = v;
    num.classList.remove('bump'); void num.offsetWidth; num.classList.add('bump');
    btns[0].disabled = v <= mn;
    btns[1].disabled = v >= mx;
    c.dataset.val = v;
  }
  btns.forEach(b => b.addEventListener('click', () => {
    const d = +b.dataset.step, nv = Math.min(mx, Math.max(mn, v + d));
    if (nv === v) return;
    if (d > 0) { row.appendChild(figure(row.children.length)); }
    else {
      const last = row.lastElementChild;
      if (last) { last.classList.add('out'); setTimeout(() => last.remove(), 200); }
    }
    v = nv; sync();
  }));
  sync();
}
"""

# The travelling card's markup, injected once. It is the SAME keycard() the
# screens use — not a second, simplified copy — so the mini in the corner and
# the card it flew off cannot drift apart. JSON-encoded because it goes into a
# JS string literal.
RUNTIME_JS = (RUNTIME_JS
    .replace("__KEYCARD_HTML__", json.dumps(keycard()))
    # MO-GYRO's numbers, from motion.tokens.js — never restated in JS
    .replace("__GYRO__", json.dumps(AUTH.M["gyro"]))
    # the default colourway, from the tokens — see _ways()
    .replace("__KCDEF__", KCDEFAULT))

BODY = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOMA — onboarding &amp; device setup</title>
<style>{css_out()}</style>
</head><body>
<div class="shell">
  <aside class="ctrl">
    <div class="ctrl__inner">
      <div class="ctrl__head">
        <h1>Onboarding &amp;<br>device setup</h1>
        <p class="lede">Tap anything in the phone, or drive it from here. Arrow keys work too.</p>
      </div>

      <div class="ctrl__grid">
        <div class="panel">
          <p class="cl">Flow</p>
          <div class="src"><b>Owner flow diagram &middot; 2026-08-06</b>
            <span>21 main-line boxes plus three branches (4a and 5a on the setup-profile page,
              18a invite family), followed node for node &mdash; nodes 19&ndash;22 were cut the
              same day, see below.</span>
            <em>Where a box needs two screens to be honest &mdash; an OS dialog over the screen that
              explains it &mdash; both carry the same node number, so the count never drifts from
              what is actually built.</em></div>
          <p class="hint"><b>Changed from the 2026-08-05 build.</b> Email account creation is new
            (nodes 4&ndash;5), node 6 is now a choice of purifier &mdash; three SKUs, not four device
            categories &mdash; the home is now created while naming the room (node 17), the household
            is a 2-screen branch off node 18, and the location / geofencing ask is new (node 24).
            Gone: the standalone consent pair, the analytics opt-in, the separate reveal screen, and
            &mdash; cut 2026-08-06, third pass &mdash; <b>nodes 19&ndash;22 entirely</b> (update check,
            install, update complete, taking the first reading) and the &ldquo;what she&rsquo;ll
            see&rdquo; household disclosure. Two open questions that removal leaves: nothing left in
            the flow takes a first reading, and firmware update has no path at all.<br><br>
            Copy is provisional (C-2). Roles are shape-only (C-3). Room presets (C-12).<br>
            Spec: docs/features/first-run/prd.md</p>
        </div>

        <div class="panel panel--wide">
          <p class="cl">Position</p>
          <div class="pos">
            <button class="nbx" id="prev">&lsaquo;</button>
            <span class="posn" id="posn">1 / 1</span>
            <button class="nbx" id="next">&rsaquo;</button>
            <button class="nbx" id="reset" title="Start over">&#8635;</button>
          </div>
          <div class="track"><i id="tr"></i></div>
          <div class="jump" id="jump"></div>
        </div>

        <div class="panel">
          <p class="cl">Fire an edge state</p>
          {state_btns}
        </div>
      </div>
    </div>
  </aside>

  <main class="stage">
    <div class="phwrap">
      <div class="phone" id="phone"><div class="island"></div><div class="hbar"></div></div>
    </div>
    <div class="meta"><b id="mt"></b><span id="mn"></span></div>
  </main>
</div>
<script>
const D = {DATA};
let vi = 0, idx = 0, off = null, hist = [];
{RUNTIME_JS}
// Screens are destroyed and rebuilt on every navigation, so any interval a screen
// started has to die with it — otherwise the node-15 carousel keeps ticking against
// detached DOM for the rest of the session.
const V = () => D.versions[vi];
const cur = () => off || V().seq[idx];

function render(dir){{
  const id = cur(), s = D.screens[id], ph = document.getElementById('phone');
  clearTimers();
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
  el.innerHTML = s.html;
  el.className = 'scr ' + carryClass(s.html, dir);
  ph.appendChild(el);
  outgoing.forEach(o => o.remove());
{WIRE_JS}
  document.getElementById('mt').textContent = s.sec + ' · ' + s.title + (s.kind === 'state' ? '  (edge state)' : '');
  document.getElementById('mn').textContent = s.note || '';
  const n = V().seq.length;
  // Node ids are stable across reorderings, so they no longer run in ascending
  // order — "node 24 of 22" would be nonsense. Show the node id and, separately,
  // where that node actually falls in the built flow.
  const mains = D.nodes.filter(x => String(x).indexOf('a') < 0);
  const step  = mains.indexOf(s.node) + 1;   // count over the main line only
  document.getElementById('posn').textContent = off
    ? (s.title + ' — off the flow')
    : ('Node ' + s.node + (String(s.node).indexOf('a') > -1
        ? ' · branch' : '  ·  step ' + step + '/' + mains.length)
       + '   ·   screen ' + (idx + 1) + '/' + n);
  document.getElementById('tr').style.width = (off ? 0 : (idx + 1) / n * 100) + '%';
  document.getElementById('prev').disabled = (!off && idx === 0 && !hist.length);
  document.getElementById('next').disabled = (!!off || idx >= n - 1);
  document.querySelectorAll('.ji').forEach(j => j.classList.toggle('on', !off && +j.dataset.i === idx));
  const a = document.querySelector('.ji.on'); if (a) a.scrollIntoView({{block:'nearest'}});
  if (typeof fit === 'function') fit();
}}
function jumpTo(pred){{ const i = V().seq.findIndex(pred);
  if (i > -1) {{ off = null; hist = []; idx = i; render(); return true; }} return false; }}
function go(t){{
  if (t === 'next')    return advance();
  if (t === 'back')    return backward();
  if (t === 'restart') return reset();
  if (t === 'skip-invite') return jumpTo(x => x === 'D1') || advance();
  if (t === 'skip-tour')   return jumpTo(x => x === 'HOME') || advance();
  const at = V().seq.indexOf(t);
  if (at > -1) {{ if (off) hist = []; off = null; idx = at; }}
  else {{ hist.push(cur()); off = t; }}
  render();
}}
function advance(){{ if (off) {{ off = null; hist = []; }} else if (idx < V().seq.length - 1) idx++; render(); }}
function backward(){{
  if (off) {{ const p = hist.pop(); off = (p && !V().seq.includes(p)) ? p : null;
              if (p && V().seq.includes(p)) idx = V().seq.indexOf(p); }}
  else if (idx > 0) idx--;
  render('back');
}}
function reset(){{ off = null; hist = []; idx = 0;
  /* the key has not been created in the new run either */
  if (typeof KEYAT !== 'undefined') KEYAT = null;
  if (KH) {{ KH.style.opacity = '0'; KH.dataset.live = '0'; }}
  /* the key card's one-time entrance is part of "the run" — see cardEntered */
  if (typeof cardEntered !== 'undefined') cardEntered = false;
  render(); }}
function buildJump(){{
  const j = document.getElementById('jump');
  let last = null;
  j.innerHTML = V().seq.map((id, i) => {{
    const s = D.screens[id], same = (s.node === last); last = s.node;
    return '<button class="ji' + (same ? ' sub' : '') + '" data-i="' + i + '">' +
      '<span class="jin">' + s.node + '</span>' +
      s.title + '<span class="jis">' + s.sec + '</span></button>';
  }}).join('');
  j.querySelectorAll('.ji').forEach(b => b.addEventListener('click', () => {{
    off = null; hist = []; idx = +b.dataset.i; render(); }}));
}}
function setVer(id){{
  vi = D.versions.findIndex(v => v.id === id);
  document.querySelectorAll('.args').forEach(a => a.classList.toggle('on', a.dataset.for === id));
  buildJump(); reset();
}}
document.getElementById('prev').addEventListener('click', backward);
document.getElementById('next').addEventListener('click', advance);
document.getElementById('reset').addEventListener('click', reset);
document.querySelectorAll('.sb').forEach(b => b.addEventListener('click', () => go(b.dataset.jump)));
addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') advance();
  if (e.key === 'ArrowLeft') backward();
}});
function fit(){{
  const p = document.getElementById('phone');
  const stage = document.querySelector('.stage');
  const meta = document.querySelector('.meta');
  const cs = getComputedStyle(stage);
  const padV = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
  const contentH = stage.clientHeight - padV;
  const reserve = meta.offsetHeight + 18;
  const avail = Math.max(320, contentH - reserve);
  const sc = Math.min(1, avail / 872);
  p.style.transform = 'scale(' + sc + ')';
  p.parentElement.style.height = (872 * sc) + 'px';
  p.parentElement.style.width  = (414 * sc) + 'px';
}}
addEventListener('resize', fit);
function fromHash(){{
  const h = decodeURIComponent(location.hash.replace('#','')).trim();
  if (!h) return false;
  const parts = h.split('/');
  let sid = parts[parts.length - 1];
  if (D.screens[sid]) {{ go(sid); return true; }}
  return false;
}}
setVer('v1');
fromHash();
addEventListener('hashchange', fromHash);
fit();
</script>
</body></html>
"""

# Guarded so build-wireframes.py can import SC / SEQ / CSS / FONTS from here and
# render the same screens flat. One screen set, two layouts — the 2026-08-06 flow
# correction had to be made twice because these two files each owned a copy.
if __name__ == "__main__":
    # ⚠ NOTHING SHIPS WITH A LIVE PLACEHOLDER. This file substitutes ~40
    # `__NAME__` tokens across three separate chains (CSS, the runtime JS,
    # the body), and putting a `.replace()` on the wrong chain fails SILENTLY:
    # the placeholder ships as literal text and whatever it configured just
    # stops working. `__KCDEF__` did exactly that on 2026-08-20 — it went on
    # the CSS chain, and the runtime read the colourway default as the string
    # "__KCDEF__". Cheap to check, invisible without it.
    _left = sorted(set(re.findall(r"__[A-Z][A-Z0-9_]*__", BODY)))
    assert not _left, "unsubstituted placeholders in the output: %s" % _left
    OUT.write_text(BODY)
    print(f"wrote {OUT.relative_to(ROOT)}  screens={len(SC)}  "
          f"seq={{{', '.join(v['id'] + ':' + str(len(v['seq'])) for v in VERSIONS)}}}  "
          f"{len(BODY)/1024/1024:.2f} MB")
