#!/usr/bin/env python3
"""
Build docs/features/first-run/auth-prototype.html

FIRST RUN, NODES 1-5 — REBUILT AS A BOTTOM-SHEET FLOW (owner refs, 2026-08-17).

    python3 docs/features/first-run/build-auth.py

WHAT THIS REPLACES. The first five nodes of the first-run spine — A1 get
started, A2 login with phone, A3 verify, A4 profile + email, A5 email verify —
were five full-screen pages. The owner supplied seven frames on 2026-08-17 that
replace all five with ONE surface: a full-bleed image behind a bottom sheet
that stays put and re-lays-out under you. Nothing after node 5 is touched;
`onboarding-prototype.html` and `first-run-prototype.html` still own nodes 6+.

THE FOUR STATES. Owner, 2026-08-17: "the bottom sheet will only be till phone
number verification". The email half moved out of the sheet and became the
Setup Profile page (node 4) in build-prototype.py.

    S0  splash            image + NOMA wordmark, no sheet yet
    A1  login sheet       wordmark, tagline, mobile number, Continue with Apple
    A2  mobile number     +91 prefix, Proceed disabled until 10 digits
    A3  mobile OTP        four boxes, resend countdown, auto-advance

⚠ The A4 (email) and A5 (email OTP) SHEET states were deleted here, not
disabled. Their replacements are full pages and live in build-prototype.py:
node 4 is the profile + master-key card, node 5 is the email code.

COPY IS VERBATIM FROM THE FRAMES, punctuation included ("What's your email"
has no question mark; "What's your mobile number?" does). Three consequences
are flagged in the per-state notes rather than quietly corrected — see NOTES
below and the rail in the built page.

TOKENS ARE READ, NOT RESTATED. Same node-import approach as every other
harness here: colour, radius, shadow, type and now MOTION are generated from
src/tokens/*.tokens.js at build time. Re-run after a token change. There is
not one raw hex, duration or bezier below the token loader.

THE BACKGROUND IS NOW THE REAL PHOTO. `assets/first-run-bg.jpg` (owner-
supplied, 2026-08-17 — an architectural render, foggy sky, lit doorway,
reflecting pool) replaced the drawn placeholder the same day it was built.
`bg_plate()` — an SVG drawing of the reference's composition in the neutral
ramp, composition-correct and art-direction-wrong on purpose, same convention
as the illustration plates in build-onboarding.py — still exists and is still
live code, but only as the FALLBACK if the real file is ever moved or
deleted: `background()` checks disk first and only draws the plate if nothing
is there. See `docs/features/first-run/assets/README.md` for provenance and
how to replace the photo again.
"""

import base64
import json
import mimetypes
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # docs/
from _phone_fit import CSS as FIT_CSS, JS as FIT_JS  # noqa: E402
import _squircle as SQ  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "auth-prototype.html"
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"
MOTION = ROOT / "src" / "tokens" / "motion.tokens.js"

# Real photography goes here. Any of these names, first match wins.
BG_CANDIDATES = ["first-run-bg.jpg", "first-run-bg.png", "first-run-bg.webp"]

# The real wordmark. See design-elements/brand/README.md for provenance,
# crop rationale and how to replace it.
WORDMARK = ROOT / "design-elements" / "brand" / "web" / "noma-wordmark.webp"


def load(path, names):
    """Read named exports out of an ES module through node, so the token files
    stay the single source and nothing is transcribed into this script."""
    script = (
        "import(%s).then(m=>{const {%s}=m;"
        "process.stdout.write(JSON.stringify({%s}));})"
        % (json.dumps(path.as_uri()), ",".join(names), ",".join(names))
    )
    res = subprocess.run(["node", "--input-type=module", "-e", script],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit("Could not read %s through node.\n%s" % (path, res.stderr.strip()))
    return json.loads(res.stdout)


T = load(TOKENS, ["colors", "effects", "elevation", "gradients", "green", "layout",
                  "neutral", "radius", "rhythm", "spacing", "typography", "recipes"])
# `gyro` is read for build-prototype.py's key-card shimmer (MO-GYRO), which
# reaches the motion tokens through this module — see AUTH.M there.
M = load(MOTION, ["durations", "easings", "scale", "stagger", "travel", "gyro"])

C, G, N, R, S = T["colors"], T["gradients"], T["neutral"], T["radius"], T["spacing"]
EL, LAY, RC = T["elevation"], T["layout"], T["recipes"]
FX, TY = T["effects"], T["typography"]
RH = T["rhythm"]
D, E, SCL = M["durations"], M["easings"], M["scale"]

FONT = "../../../src/fonts/google-sans-flex/GoogleSansFlex-VariableFont_GRAD,ROND,opsz,slnt,wdth,wght.ttf"

TX = TY["scale"]


def ty(name, extra=""):
    """One type step as CSS. Reads the scale rather than restating sizes."""
    t = TX[name]
    css = ("font-size:%spx;line-height:%spx;letter-spacing:%.3gpx;"
           "font-variation-settings:'opsz' %s,'wght' %s;"
           % (t["size"], t["lineHeight"], t["tracking"], t["opsz"], t["weight"]))
    if t.get("transform"):
        css += "text-transform:%s;" % t["transform"]
    return css + extra


# ---------------------------------------------------------------------------
# The background plate.
#
# The reference is a photograph: a white plaster interior, an arched opening
# with light behind it, a stair flight running up to it, and soft curved
# foreground forms cropping the top and bottom. This draws that composition out
# of the neutral ramp so the sheet has something real to sit on and the
# greyscale reads correctly. It is a stand-in and looks like one up close.
# ---------------------------------------------------------------------------

def bg_plate():
    """The reference photograph's composition, drawn out of the neutral ramp:
    a plaster interior, an arch with light behind it, a stair flight running up
    to it between two stepped balustrades, and soft curved forms cropping the
    top and the bottom. Everything below the arch is deliberately quiet — the
    sheet covers the lower 40-55% and nothing important may live there."""
    return f"""<svg class="bg__svg" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"
  xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="wall" x1="0" y1="0" x2=".3" y2="1">
      <stop offset="0" stop-color="{N['200']}"/><stop offset="1" stop-color="{N['150']}"/>
    </linearGradient>
    <linearGradient id="riser" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{N['0']}"/><stop offset="1" stop-color="{N['100']}"/>
    </linearGradient>
    <linearGradient id="tread" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{N['50']}"/><stop offset=".55" stop-color="{N['0']}"/>
      <stop offset="1" stop-color="{N['100']}"/>
    </linearGradient>
    <linearGradient id="jamb" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{N['100']}"/><stop offset="1" stop-color="{N['25']}"/>
    </linearGradient>
    <linearGradient id="fore" x1=".2" y1="0" x2=".6" y2="1">
      <stop offset="0" stop-color="{N['0']}"/><stop offset="1" stop-color="{N['150']}"/>
    </linearGradient>
    <linearGradient id="mound" x1=".1" y1="0" x2=".7" y2="1">
      <stop offset="0" stop-color="{N['0']}"/><stop offset="1" stop-color="{N['200']}"/>
    </linearGradient>
    <radialGradient id="spill" cx=".5" cy=".34" r=".46">
      <stop offset="0" stop-color="{N['0']}" stop-opacity=".92"/>
      <stop offset="1" stop-color="{N['0']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="floor" x1=".1" y1="0" x2=".8" y2="1">
      <stop offset="0" stop-color="{N['0']}"/><stop offset="1" stop-color="{N['100']}"/>
    </linearGradient>
    <linearGradient id="thru" x1="0" y1="1" x2=".2" y2="0">
      <stop offset="0" stop-color="{N['0']}"/><stop offset=".6" stop-color="{N['25']}"/>
      <stop offset="1" stop-color="{N['100']}"/>
    </linearGradient>
  </defs>

  <rect width="390" height="844" fill="url(#wall)"/>
  <rect x="20" y="150" width="350" height="420" fill="url(#spill)"/>

  <!-- The arch. Measured off the frame: ~130pt wide, ~150pt tall, base at
       just under half the screen — squat, not a tall slab. Everything below
       y=400 is progressively covered by the sheet, so the arch has to carry
       the whole image on its own. -->
  <path d="M150 400 V310 a60 60 0 0 1 120 0 V400 Z" fill="url(#jamb)"/>
  <path d="M162 400 V312 a48 48 0 0 1 96 0 V400 Z" fill="url(#thru)"/>
  <path d="M162 400 V312 a48 48 0 0 1 96 0" fill="none"
        stroke="{N['300']}" stroke-opacity=".3" stroke-width="1.2"/>

  <!-- The flight, widening as it comes toward the viewer. Tread and riser are
       separate shapes so the steps read as solid rather than as lines. -->
  <g>
    <path d="M170 400 h80 v10 h-80 Z" fill="url(#tread)"/>
    <path d="M170 410 h80 v11 h-80 Z" fill="url(#riser)"/>
    <path d="M161 421 h98 v11 h-98 Z" fill="url(#tread)"/>
    <path d="M161 432 h98 v12 h-98 Z" fill="url(#riser)"/>
    <path d="M151 444 h118 v12 h-118 Z" fill="url(#tread)"/>
    <path d="M151 456 h118 v13 h-118 Z" fill="url(#riser)"/>
    <path d="M140 469 h140 v13 h-140 Z" fill="url(#tread)"/>
    <path d="M140 482 h140 v14 h-140 Z" fill="url(#riser)"/>
    <path d="M128 496 h164 v14 h-164 Z" fill="url(#tread)"/>
    <path d="M128 510 h164 v15 h-164 Z" fill="url(#riser)"/>
    <path d="M115 525 h190 v15 h-190 Z" fill="url(#tread)"/>
    <path d="M115 540 h190 v16 h-190 Z" fill="url(#riser)"/>
  </g>

  <!-- The two side walls, stepping down and outward with the flight. The left
       catches the light and the right falls away — that asymmetry is most of
       what makes it read as depth rather than as a diagram. -->
  <path d="M170 400 V410 H161 V432 H151 V456 H140 V482 H128 V510 H115 V844 H0 V400 Z"
        fill="url(#fore)"/>
  <path d="M250 400 V410 H259 V432 H269 V456 H280 V482 H292 V510 H305 V844 H390 V400 Z"
        fill="url(#mound)"/>
  <!-- The floor the flight lands on. A trapezoid, not a rectangle: it has to
       widen toward the viewer or it reads as a white column standing on the
       stairs. Nothing below the steps may read as a flat band of wall. -->
  <path d="M115 556 H305 L390 844 H30 Z" fill="url(#floor)"/>

  <!-- Foreground crops. The top one is the only thing that survives on every
       state; the bottom one lives entirely behind the sheet except on splash. -->
  <path d="M0 0 H390 V78 c-58 40 -112 -8 -190 14 C118 110 62 84 0 116 Z" fill="url(#fore)"/>
  <path d="M0 116 C62 84 118 110 200 92 c78 -22 132 26 190 -14" fill="none"
        stroke="{N['0']}" stroke-opacity=".6" stroke-width="1.5"/>
  <path d="M0 700 c96 -60 156 24 246 -12 c56 -22 98 8 144 -12 V844 H0 Z" fill="url(#mound)"/>
  <path d="M0 700 c96 -60 156 24 246 -12 c56 -22 98 8 144 -12" fill="none"
        stroke="{N['0']}" stroke-opacity=".75" stroke-width="2"/>
</svg>"""


def background_css():
    """The same background as a CSS `url(...)` value, for consumers that show
    it on more than one screen. build-prototype.py renders eight sheet screens
    from one photo; inlining the <img> into each of them put 1.4 MB of
    duplicate base64 in that file, so it takes this and paints it once.

    Both branches return a url() so the caller never has to care which it got.
    """
    for name in BG_CANDIDATES:
        p = HERE / "assets" / name
        if p.exists():
            mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
            return "url(data:%s;base64,%s)" % (
                mime, base64.b64encode(p.read_bytes()).decode())
    svg = base64.b64encode(bg_plate().encode()).decode()
    return "url(data:image/svg+xml;base64,%s)" % svg


def background():
    """Real photograph if one has been dropped in; the drawn plate otherwise."""
    for name in BG_CANDIDATES:
        p = HERE / "assets" / name
        if p.exists():
            mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
            b64 = base64.b64encode(p.read_bytes()).decode()
            print("background: assets/%s (%d KB)" % (name, len(b64) // 1400))
            return ('<img class="bg__img" src="data:%s;base64,%s" alt="">' % (mime, b64)), name
    print("background: drawn placeholder — drop assets/%s to replace it"
          % BG_CANDIDATES[0])
    return bg_plate(), None


# ---------------------------------------------------------------------------
# Chrome + parts
# ---------------------------------------------------------------------------

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


ICON_MAIL = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/>'
    '<path d="m3.5 7 8.5 6 8.5-6"/></svg>')

# Owner-supplied 2026-08-19, replacing the earlier hand-approximated glyph
# (docs/features/settings/_kit.py's ICONS convention: a supplied asset wins
# over a redrawn one). Source: apple-173-svgrepo-com.svg. The two nested
# <g transform> offsets in that file are baked into these coordinates so the
# icon is a flat <path fill="currentColor">, matching every other icon here —
# it tints white on the black CTA and stays black on the white one for free.
ICON_APPLE = (
    '<svg width="16" height="19" viewBox="-1.5 0 20 20" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    f'<path d="M11.57,3.19 C12.30,2.35 12.79,1.17 12.66,0.00 C11.61,0.04 10.34,0.67 9.58,1.51 C8.91,2.26 8.31,3.46 8.47,4.61 C9.65,4.70 10.84,4.04 11.57,3.19 M14.20,10.62 C14.23,13.65 16.97,14.66 17.00,14.67 C16.98,14.74 16.56,16.11 15.56,17.52 C14.69,18.73 13.78,19.95 12.36,19.97 C10.96,20.00 10.51,19.18 8.91,19.18 C7.32,19.18 6.82,19.95 5.49,20.00 C4.12,20.05 3.07,18.68 2.20,17.47 C0.40,14.98 -0.97,10.45 0.87,7.39 C1.79,5.87 3.42,4.91 5.19,4.88 C6.54,4.86 7.82,5.75 8.64,5.75 C9.46,5.75 11.01,4.68 12.64,4.84 C13.32,4.86 15.23,5.10 16.45,6.82 C16.36,6.88 14.17,8.09 14.20,10.62" fill="currentColor"/></svg>')

# Owner-supplied 2026-08-19. Source: google-icon-logo-svgrepo-com.svg — the
# official multicolour "G", NOT recoloured to currentColor. Google's own
# brand guidelines specify the four-colour mark on a white/near-white
# surface; it is the one icon in this file that does not inherit the
# button's ink, because the button it sits on (the white "Continue with
# Google") is exactly the surface that mark is drawn for.
# ⚠ The source file carried width="800px" height="800px" — real pixel
# attributes on a 262-unit viewBox. A CSS `width` on the element overrides
# them visually, but leaving them in is one accidental unscaled paste away
# from a giant icon; stripped here so only the CSS size can ever apply.
ICON_GOOGLE = (
    '<svg width="17" height="17" viewBox="-3 0 262 262" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M255.878 133.451c0-10.734-.871-18.567-2.756-26.69H130.55v48.448h71.947'
    'c-1.45 12.04-9.283 30.172-26.69 42.356l-.244 1.622 38.755 30.023 2.685.268'
    'c24.659-22.774 38.875-56.282 38.875-96.027" fill="#4285F4"/>'
    '<path d="M130.55 261.1c35.248 0 64.839-11.605 86.453-31.622l-41.196-31.913'
    'c-11.024 7.688-25.82 13.055-45.257 13.055-34.523 0-63.824-22.773-74.269-54.25'
    'l-1.531.13-40.298 31.187-.527 1.465C35.393 231.798 79.49 261.1 130.55 261.1" '
    'fill="#34A853"/>'
    '<path d="M56.281 156.37c-2.756-8.123-4.351-16.827-4.351-25.82 0-8.994 1.595-17.697 '
    '4.206-25.82l-.073-1.73L15.26 71.312l-1.335.635C5.077 89.644 0 109.517 0 130.55'
    's5.077 40.905 13.925 58.602l42.356-32.782" fill="#FBBC05"/>'
    '<path d="M130.55 50.479c24.514 0 41.05 10.589 50.479 19.438l36.844-35.974'
    'C195.245 12.91 165.798 0 130.55 0 79.49 0 35.393 29.301 13.925 71.947'
    'l42.211 32.783c10.59-31.477 39.891-54.251 74.414-54.251" fill="#EB4335"/></svg>')


def sheet_state(sid, inner, align="center"):
    return {"id": sid, "align": align, "inner": inner}


# Cached once — the same base64 payload is reused at both call sites (splash
# and sheet header) rather than re-reading and re-encoding the file twice.
_WORDMARK_B64 = None


def wordmark(cls="mark"):
    """The real mark (design-elements/brand/) at the width layout.wordmarkSplash
    / layout.wordmarkSheet specifies for this context. Falls back to the old
    letter-spaced text if the asset is ever missing, same convention as
    icon3d()'s placeholder in _kit.py — a missing asset degrades, it never
    fails the build."""
    global _WORDMARK_B64
    width = LAY["wordmarkSplash"] if cls == "mark" else LAY["wordmarkSheet"]

    if _WORDMARK_B64 is None:
        if WORDMARK.exists():
            _WORDMARK_B64 = base64.b64encode(WORDMARK.read_bytes()).decode()
            print("wordmark: %s (%d KB)" % (WORDMARK.relative_to(ROOT),
                                             len(_WORDMARK_B64) // 1400))
        else:
            _WORDMARK_B64 = False
            print("wordmark: %s not found — falling back to CSS text"
                  % WORDMARK.relative_to(ROOT))

    if not _WORDMARK_B64:
        return '<div class="%s %s--text">NOMA</div>' % (cls, cls)

    return ('<div class="%s"><img src="data:image/webp;base64,%s" '
            'alt="NOMA" width="%d" style="width:%dpx"></div>'
            % (cls, _WORDMARK_B64, width, width))


def eyebrow(txt):
    return '<p class="eyebrow">%s</p>' % txt


def h1(txt):
    """The sheet heading. Carries `grad` so the canonical flow paints it with
    the title gradient (tokens.titleGradient, defined in build-prototype.py's
    CSS, which is appended after this file's and therefore wins).

    ⚠ In THIS file's standalone `auth-prototype.html` the class is inert —
    the rule lives with the prototype. That is deliberate and it fails safe:
    an unmatched class renders ordinary ink, whereas a `color:transparent`
    with no gradient behind it would render nothing at all."""
    return '<h1 class="h1 grad">%s</h1>' % txt


def sub(txt):
    return '<p class="sub">%s</p>' % txt


def otp_row(step):
    """Four boxes with ONE input laid transparently across them. A per-box
    input steals focus on every keystroke and breaks paste; this way the OS
    one-time-code autofill still targets a single field."""
    boxes = "".join('<i data-i="%d"></i>' % i for i in range(4))
    return ('<div class="s-otp" data-otp="%s">%s'
            '<input class="s-otp__in" inputmode="numeric" autocomplete="one-time-code" '
            'maxlength="4" aria-label="One-time code"></div>' % (step, boxes))


def resend():
    return ('<p class="resend"><span data-resend>Resend OTP in <b>15s</b></span>'
            '<button class="resend__b" data-resendbtn hidden>Resend OTP</button></p>')


def cta(label, go, ready=False):
    return ('<button class="s-cta" data-go="%s"%s>%s</button>'
            % (go, "" if ready else " disabled", label))


# ---------------------------------------------------------------------------
# The six states. Ids map onto the PRD node table: S0/A1 are node 1, A2 node 2,
# A3 node 3, A4 node 4, A5 node 5.
# ---------------------------------------------------------------------------

STATES = [
    {
        "id": "S0", "node": "1", "label": "Splash", "sheet": None,
        "note": "<b>Node 1, first half.</b> Image and wordmark only — the sheet has not "
                "arrived yet. It rises on its own after a beat, or on a tap. The image is the "
                "<b>real background</b> (assets/first-run-bg.jpg, owner-supplied) — see "
                "assets/README.md for provenance and how to replace it again. Owner note: this "
                "becomes a video later, which is why nothing in the layout depends on the image "
                "being still.",
    },
    {
        "id": "A1", "node": "1", "label": "Login sheet", "align": "center",
        "inner": f"""
      {wordmark("mark--sheet")}
      {h1("A calmer kind of<br>smart home.")}
      <button class="s-cta s-cta--icon" data-go="DONE">{ICON_APPLE}<span>Continue with Apple</span></button>
      <button class="ghost" data-go="DONE">{ICON_GOOGLE}<span>Continue with Google</span></button>
      <button class="ghost ghost--bare" data-go="A2">{ICON_MAIL}<span>Continue with email</span></button>
      <p class="fine">By continuing, you agree to our<br>
        <b>Terms of Service</b> and <b>Privacy Policy</b></p>
""",
        "note": "<b>Node 1, second half — restacked 2026-08-19 (owner).</b> Apple is now the "
                "primary (black) CTA, Google the secondary (white), email the tertiary link — "
                "still three ways in, but federated identity leads rather than the phone "
                "number, which has moved to node 4. <b>Apple and Google both skip straight to "
                "node 4</b>, same DONE hand-off A3's Proceed uses below: a provider that has "
                "already authenticated the person has no email left to verify. Only email "
                "walks through A2/A3. <b>⚠ The DPDP notice still rides on this screen's fine "
                "print</b> rather than on node 4 — PRD §5.1 is unresolved regardless of which "
                "field moved where.",
    },
    {
        "id": "A2", "node": "2", "label": "Email address", "align": "center",
        "inner": f"""
      {eyebrow("Login with email")}
      {h1("What’s your email?")}
      <div class="field">
        <input class="field__in" data-email type="email" inputmode="email"
               placeholder="you@example.com" aria-label="Email address">
      </div>
      {cta("Proceed", "A3")}
""",
        "note": "<b>Node 2 — was the mobile-number entry; now the same shape, for email "
                "(owner, 2026-08-19).</b> Proceed is inert until the address looks valid. "
                "No “Continue with email” variant collects this on the login sheet itself — "
                "it is always its own step, which is what makes A3's “we’ve sent a code to "
                "___” legible.",
    },
    {
        "id": "A3", "node": "3", "label": "Email OTP", "align": "center",
        "inner": f"""
      {eyebrow("Login with email")}
      {h1("Enter the OTP")}
      {otp_row("A3")}
      {resend()}
      {cta("Proceed", "DONE")}
""",
        "note": "<b>Node 3 — was the mobile OTP; now email (owner, 2026-08-19).</b> Four "
                "digits, resend countdown visible from t=0. Proceed hands off to node 4, "
                "which now asks for the phone number instead of the email node 4 used to "
                "collect — see build-prototype.py's <code>mobile_field()</code>. "
                "<b>⚠ No way back</b>: a mistyped address strands you here, same gap the old "
                "mobile-OTP state had.",
    },
]

# HANDOFF was `dead FIRST = {...}` dict removed here 2026-08-19 — defined but
# never read (not embedded into JS, not referenced by any function); a stale
# leftover from an earlier structure, dropped while this section was already
# being rewritten rather than carried forward as false signal.

# The state whose CTA leaves this flow. build-prototype.py repoints it at the
# Setup Profile page (node 4), which is where the sheet hands over. Both A1's
# Apple/Google buttons AND A3's Proceed carry this same literal marker in
# their own `inner` string — au_state() replaces it independently per state,
# so both paths can converge on node 4 with no extra mechanism.
HANDOFF = "DONE"


# ---------------------------------------------------------------------------
# CSS. Every value below resolves to a token.
# ---------------------------------------------------------------------------

# Measured off the frames at 2x: the sheet's own edge sits 15pt in from the
# screen, and the CTA 29pt — so 16 + 12 off the ramp, not the usual
# layout.screenPaddingX of 20. The sheet is inset from the screen, so its
# content cannot also carry the screen's padding or everything creeps inward.
SHEET_INSET = S["s4"]   # 16 — the sheet floats, it is not edge-anchored
SHEET_PAD_X = LAY["sheetPadX"]   # 20 [OWNER REDLINE 2026-08-18]
# Condensed 2026-08-18 (owner: "the bottom sheet is too tall... condense the
# spacing, the wasted space"). Every vertical gap in the sheet stepped down
# one to two stops on the spacing ramp; the type scale and the 56pt CTA are
# tokens and were left alone — going further than spacing means shrinking
# those, which is an owner call, not a trim.
# [OWNER REDLINE 2026-08-18] 24 top and bottom. The 12/12 squeeze that came
# out of the "condense the sheets" pass went too far — the redline puts the
# sheet's own padding back on sectionGap, and buys the height back from the
# gaps BETWEEN things instead (title->control 18, stacked buttons 8).
SHEET_PAD_T = LAY["sheetPadY"]   # 24
SHEET_PAD_B = LAY["sheetPadY"]   # 24

# A caret blink. `durations.ambient` is the only long value in the token set
# and is four times too slow for one; quartering it keeps this derived from a
# token rather than becoming the file's one raw millisecond value.
CARET_MS = M["durations"]["ambient"] // 4

# Per-child delays for the first-arrival stagger. Built here rather than
# inline in the CSS f-string: a generator holding a brace-bearing format
# string inside an f-string does not get the usual {{ }} escaping, which
# silently emits doubled braces and a dead rule.
#
# The first child starts at ~45% of the sheet's travel — late enough that the
# sheet reads as arriving first and carrying its contents with it, early
# enough that the two feel like one move rather than two.
STAGGER_LEAD = round(D["entrance"] * 0.45)
STAGGER_CSS = "".join(
    ".sheet__c--stagger > *:nth-child(%d){animation-delay:%dms}"
    % (i + 1, STAGGER_LEAD + i * M["stagger"]["list"])
    for i in range(8)
)

# CSS is split into three exported parts so build-first-run.py can compose it
# with build-onboarding.py's screen CSS without either one's chrome winning by
# accident. Standalone, this file just concatenates all three (see CSS below).
#
#   CSS_CHROME   harness + phone + status bar + background. Shared shape with
#                build-onboarding.py's own chrome; the merged builder picks
#                ONE of the two rather than letting source order decide.
#   CSS_SHEET    the sheet and everything inside it. Every component selector
#                in here is scoped under `.sheet`, which is both accurate and
#                what keeps `.cta` / `.field` / `.otp` / `.iconbtn` from
#                colliding with the onboarding screens' versions.
#   CSS_REDUCE   motion gate 2. Emitted exactly once per document.

CSS_CHROME = f"""
@font-face {{ font-family:'Google Sans Flex'; src:url('{FONT}') format('truetype');
  font-weight:1 1000; font-display:swap; }}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{TY['family']['sans']};font-optical-sizing:auto;
  background:{N['150']};color:{C['text']['primary']};display:flex;gap:{S['s7']}px;
  padding:{S['s7']}px;height:100vh;overflow:hidden;-webkit-font-smoothing:antialiased}}
{FIT_CSS}

/* ---- review chrome — not part of the product ------------------------- */
.rail{{width:236px;flex:none;align-self:stretch;overflow-y:auto;scrollbar-width:none}}
.rail::-webkit-scrollbar{{display:none}}
.rail__b{{{ty('label')}color:{C['text']['tertiary']};margin-bottom:13px}}
.rail__i{{display:flex;align-items:baseline;gap:9px;width:100%;text-align:left;
  background:{N['0']};border:0;border-radius:{R['sm']}px;padding:10px 12px;margin-bottom:6px;
  font:inherit;font-size:13.5px;cursor:pointer;color:{C['text']['secondary']};
  box-shadow:{EL['control']['css']};
  transition:transform {D['fast']}ms {E['spring']}}}
.rail__i:hover{{transform:translateX(2px)}}
.rail__i[aria-current="true"]{{color:{C['text']['primary']};font-variation-settings:'wght' 600;
  box-shadow:{EL['card']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']}}}
.rail__n{{font-size:10.5px;color:{C['text']['tertiary']};font-family:ui-monospace,Menlo,monospace}}
.note{{font-size:11.5px;line-height:1.68;color:{C['text']['tertiary']};margin-top:{S['s4']}px}}
.note b{{color:{C['text']['secondary']};font-variation-settings:'wght' 600}}

/* ---- phone ----------------------------------------------------------- */
.phone{{width:390px;height:844px;flex:none;border-radius:52px;position:relative;
  overflow:hidden;background:{C['surface']['canvas']};box-shadow:0 40px 90px rgba(0,0,0,.16)}}
.notch{{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:122px;height:33px;
  background:{N['900']};border-radius:20px;z-index:60}}
.hbar{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:138px;height:5px;
  background:rgba(0,0,0,.2);border-radius:3px;z-index:60}}

.sbar{{position:absolute;top:0;left:0;right:0;height:54px;z-index:20;
  display:flex;align-items:center;justify-content:space-between;
  padding:14px {LAY['screenPaddingX']}px 0;color:{C['text']['primary']}}}
.sbar__t{{font-size:15px;font-variation-settings:'wght' 600;letter-spacing:-.2px}}
.sbar__r{{display:flex;align-items:center;gap:5px}}
.bat{{width:25px;height:12px;border-radius:3.5px;border:1.3px solid currentColor;
  padding:1.4px;display:block}}
.bat i{{display:block;height:100%;width:88%;background:currentColor;border-radius:1.4px}}
"""

# The background layer, exported on its own: the merged flow takes THIS plus
# CSS_SHEET but uses build-onboarding.py's chrome, because that harness's
# status bar sits in the flow of each screen while this one's is absolute over
# the photo. Two chromes, one document — the merged builder picks explicitly
# rather than letting source order decide.
CSS_BG = f"""
/* the image sits behind everything and never moves — the sheet moves on it */
.bg{{position:absolute;inset:0;overflow:hidden}}
/* A very slow settle out of a slight over-scale. At ambient (4s) over a
   ~1.5% move this is below the threshold of "an animation" and reads as the
   image being alive — which is the point: it holds the splash for the extra
   beat without the beat feeling empty. It also rehearses the video this
   becomes later. scale.breathe is the ceiling for ambient movement. */
.bg__svg,.bg__img{{position:absolute;inset:0;width:100%;height:100%;
  object-fit:cover;display:block;
  animation:bgSettle {D['ambient']}ms {E['standard']} both}}
@keyframes bgSettle{{from{{transform:scale({SCL['breathe']})}}
  to{{transform:scale(1)}}}}
"""

CSS_SHEET = f"""
/* ---- the wordmark on the splash -------------------------------------- */
/* design-elements/brand/ — the real mark, sized by layout.wordmarkSplash /
   wordmarkSheet. `.mark img` carries no colour of its own: the source PNG is
   already ink-on-transparent, which is why it survives on the photo, the
   sheet's own gradient AND (via the --text fallback below) a plain ground. */
.mark{{position:absolute;left:0;right:0;bottom:{S['s10'] + S['s8']}px;
  text-align:center;z-index:15;
  transition:opacity {D['base']}ms {E['exit']},transform {D['base']}ms {E['exit']}}}
/* The entrance lives on the IMG, the exit on its parent — an `animation` with
   `both` fill would otherwise pin the properties the exit transition needs. */
.mark img{{display:inline-block;height:auto;
  animation:markIn {D['entrance']}ms {E['entrance']} both}}
@keyframes markIn{{from{{opacity:0;transform:translateY({M['travel']['rise']}px)}}}}
.phone[data-sheet] .mark{{opacity:0;transform:translateY(-{M['travel']['rise']}px)}}
/* Fallback only — see wordmark()'s docstring. Reproduces the pre-2026-08-17
   letter-spaced text so a missing asset degrades instead of breaking. */
.mark--text,.mark--sheet--text{{{ty('display')}letter-spacing:.3em;text-indent:.3em;
  font-variation-settings:'opsz' {TX['display']['opsz']},'wght' {TY['weight']['semibold']};
  color:{C['text']['primary']}}}
.mark--sheet--text{{{ty('bodyStrong')}margin-bottom:{S['s3']}px}}

/* ---- the sheet ------------------------------------------------------- */
/* recipes.bottomSheet, floated off all four edges rather than docked to the
   bottom — that inset is what the reference frames show, and it is what makes
   the image read as continuing behind it. */
/* THE ARRIVAL — durations.entrance / easings.entrance, not the usual
   sheet+springBold pair. See the token comments: this is the once-per-install
   opening, so it settles rather than lands, and it is deliberately the one
   un-springy motion in the product. Subsequent state changes (A1->A2 and on)
   still use the quick fast/base swap below — only the FIRST arrival is slow,
   because only the first arrival is an introduction. */
/* THE CARD DESIGN — recipes.largeSurface, straight off the owner's Figma
   inspector 2026-08-19: radius 34 on all four corners at 100% corner
   smoothing, the #F9F9F9 + 24% gradient fill, a 1px WHITE INSIDE stroke, and
   a drop shadow.

   ⚠ TWO ELEMENTS, and it has to be two. A mask clips everything an element
   paints — its outer shadow included — so a masked sheet cannot cast one.
   `.sheet` is therefore the shell: it holds the shadow, the position and the
   transform, and its `border-radius` exists ONLY to give that shadow a shape.
   `.sheet__s` is the surface: the fill and the hairline, clipped to the real
   superellipse by docs/_squircle.py's 9-slice mask. The arc-vs-superellipse
   difference is invisible under a 48px blur, which is why the shadow can stay
   on a plain rounded rect without anyone being able to tell. */
.sheet{{position:absolute;left:{SHEET_INSET}px;right:{SHEET_INSET}px;bottom:{SHEET_INSET}px;
  z-index:30;border-radius:{R['xxxl']}px;
  box-shadow:{EL['floating']['css']};
  transform:translateY(calc(100% + {SHEET_INSET}px));
  transition:transform {D['entrance']}ms {E['entrance']},
             height {D['base']}ms {E['standard']}}}
.phone[data-sheet] .sheet{{transform:translateY(0)}}
/* the surface. `inset:0` so it tracks the shell at every height the sheet
   animates through — no script, no ResizeObserver, the 9-slice restretches. */
.sheet__s{{position:absolute;inset:0;overflow:hidden;
  background:{RC['bottomSheet']['background']};
  {SQ.surface_css(R['xxxl'], R['smoothing'],
                  stroke=RC['bottomSheet']['strokeColor'],
                  stroke_width=RC['bottomSheet']['strokeWidth'])}}}
/* ⚠ `border:{SQ.slice_px(R['xxxl'], R['smoothing'])}px` above is the 9-slice's
   canvas for the hairline, NOT padding — the sheet's real padding is on
   `.sheet__c`, which is why the surface must not be the layout parent. */
/* Every <p> in the sheet starts at margin 0 — the UA's 1em block margins
   were stacking on top of the rhythm values (the countdown alone added
   ~19 to its gap under the CTA). The rhythm tokens are the only vertical
   spacing in this component; nothing inherits leftovers. */
.sheet__c p,.sheet__c h1{{margin:0}}
.sheet__c{{position:relative;z-index:1;
  padding:{SHEET_PAD_T}px {SHEET_PAD_X}px {SHEET_PAD_B}px;
  display:flex;flex-direction:column;align-items:stretch;text-align:center}}
.sheet[data-align="left"] .sheet__c{{text-align:left}}
/* content swap — out on exit easing (LAW: exits never bounce), in on spring */
.sheet__c{{transition:opacity {D['fast']}ms {E['exit']},transform {D['fast']}ms {E['exit']}}}
.sheet__c[data-out]{{opacity:0;transform:translateY(-6px)}}
.sheet__c[data-in]{{animation:cin {D['base']}ms {E['spring']} both}}
@keyframes cin{{from{{opacity:0;transform:translateY({M['travel']['rise']}px)}}}}

/* First arrival only: the sheet's contents come up one after another as it
   settles, instead of the whole block appearing at once. Applied by JS on the
   splash -> A1 hand-off and never again — staggering every form step would
   make the flow feel slow rather than considered. */
.sheet__c--stagger > *{{animation:cin {D['gentle']}ms {E['entrance']} both}}
{STAGGER_CSS}

/* ---- type ------------------------------------------------------------ */
/* [OWNER FIGMA 2026-08-19] W56 at 50% opacity. A signature, not a headline —
   see layout.wordmarkSheet / wordmarkSheetOpacity. */
.mark--sheet{{margin-bottom:{RH['textGap']}px;opacity:{LAY['wordmarkSheetOpacity']}}}
.mark--sheet img{{display:inline-block;height:auto}}
/* rhythm (owner 2026-08-18): 12 within a text set, 24 between blocks —
   grounded against Airbnb and CRED sign-in flows on Mobbin. */
.sheet .eyebrow{{{ty('label')}color:{C['text']['secondary']};margin-bottom:{RH['textGap']}px}}
/* margin:0 — the UA gives an h1 0.67em top AND bottom (20px at this size),
   which silently added ~20 to every gap around the title and is why the
   sheet read as over-spaced. The rhythm tokens are now the ONLY vertical
   spacing here. */
.sheet .h1{{{ty('display')}color:{C['text']['primary']};margin:0}}
.sheet .sub{{{ty('body')}color:{C['text']['secondary']};margin:{RH['textGap']}px 0 0}}
/* [OWNER FIGMA 2026-08-19] "Mixed 10" — one 10pt run, links at semibold. */
.sheet .fine{{{ty('legal')}color:{C['text']['tertiary']};margin-top:{RH['titleGap']}px}}
.sheet .fine b{{color:{C['text']['secondary']};
  font-variation-settings:'opsz' {TX['legal']['opsz']},'wght' {TX['legal']['linkWeight']}}}
.sheet .s-link{{background:none;border:0;font:inherit;{ty('bodyStrong')}
  color:{C['text']['accent']};cursor:pointer;padding:0;margin-top:{S['s2']}px;
  align-self:flex-start}}

/* ---- buttons --------------------------------------------------------- */
/* recipes.buttonPrimary — LAW 4, the CTA is ink and fully round. */
.sheet .s-cta{{height:{LAY['ctaHeight']}px;width:100%;border:0;border-radius:{R['full']}px;
  background:{G['ink']['css']};color:{C['text']['inverse']};font:inherit;
  {ty(RC['buttonPrimary']['textStyle'])}cursor:pointer;box-shadow:{EL['dock']['css']};
  margin-top:{RH['sectionGap']}px;display:flex;align-items:center;justify-content:center;
  gap:{S['s2']}px;
  transition:transform {D['fast']}ms {E['spring']},background {D['base']}ms {E['standard']},
             box-shadow {D['base']}ms {E['standard']}}}
.sheet .s-cta:active{{transform:scale({SCL['press']})}}
.sheet .s-cta[disabled]{{background:{C['surface']['muted']};box-shadow:none;cursor:default}}
.sheet .s-cta[disabled]:active{{transform:none}}
/* follows the title directly, so titleGap (18) not sectionGap */
.sheet .s-cta--icon{{margin-top:{RH['titleGap']}px}}
/* recipes.buttonQuiet — 46 tall, SHORTER than the 54 primary on purpose, and
   8 from whatever it stacks under. The height difference is half the
   hierarchy; matching the primary would make them read as equal choices. */
.sheet .ghost{{height:{LAY['ctaQuietHeight']}px;width:100%;border:0;font:inherit;
  background:{C['surface']['raised']};border-radius:{R['full']}px;
  box-shadow:{EL['control']['css']};
  {ty(RC['buttonQuiet']['textStyle'])}color:{C['text']['primary']};cursor:pointer;
  margin-top:{RH['controlGap']}px;
  display:flex;align-items:center;justify-content:center;gap:{S['s2']}px;
  transition:transform {D['fast']}ms {E['spring']},background {D['base']}ms {E['standard']}}}
.sheet .ghost--bare{{background:none;box-shadow:none}}
.sheet .ghost:active{{transform:scale({SCL['press']})}}
/* recipes.buttonIcon — the white inside stroke is what makes it read as glass */
.sheet .iconbtn{{width:{LAY['controlSize']}px;height:{LAY['controlSize']}px;border-radius:{R['full']}px;
  background:{C['surface']['control']};border:0;display:grid;place-items:center;cursor:pointer;
  color:{C['icon']['primary']};align-self:flex-start;margin-bottom:{S['s5']}px;
  box-shadow:{EL['control']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']};
  transition:transform {D['fast']}ms {E['spring']}}}
/* pressing DARKENS a raised control; it does not brighten it */
.sheet .iconbtn:hover{{background:{N['100']}}}
.sheet .iconbtn:active{{transform:scale({SCL['press']});background:{N['150']}}}

/* ---- input ----------------------------------------------------------- */
/* recipes.input — white raised field on the ground, radius 20, height 56. */
/* recipes.input, 2026-08-18: sunken well, not floating card — see the recipe
   comment in the token file. Section rhythm: 24 above (a field is a new
   block, not part of the title's text set). */
.sheet .field{{display:flex;align-items:center;gap:{S['s3']}px;height:{RC['input']['height']}px;
  border-radius:{RC['input']['borderRadius']}px;background:{RC['input']['background']};
  padding:0 {RC['input']['paddingX']}px;
  border:{RC['input']['borderWidth']}px solid {RC['input']['borderColor']};
  box-shadow:{RC['input']['innerShadow']};margin-top:{RH['sectionGap']}px;
  transition:border-color {D['base']}ms {E['standard']}}}
.sheet .field:focus-within{{border-color:{C['border']['strong']}}}
.sheet .field__cc{{{ty('bodyStrong')}color:{C['text']['primary']};flex:none}}
.sheet .field__in{{flex:1;min-width:0;border:0;background:none;font:inherit;{ty('body')}
  color:{C['text']['primary']};outline:0;caret-color:{C['text']['accent']}}}
.sheet .field__in::placeholder{{color:{C['text']['tertiary']}}}

/* ---- OTP ------------------------------------------------------------- */
.sheet .s-otp{{position:relative;display:flex;gap:{S['s3']}px;justify-content:center;
  margin-top:{RH['sectionGap']}px}}
.sheet .s-otp i{{width:{LAY['otpBox'][0]}px;height:{LAY['otpBox'][1]}px;border-radius:{R['md']}px;background:{C['surface']['raised']};
  box-shadow:{EL['control']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']};
  display:grid;place-items:center;font-style:normal;
  {ty('title2')}font-variation-settings:'opsz' {TX['title2']['opsz']},'wght' {TY['weight']['bold']};
  color:{C['text']['primary']}}}
.sheet .s-otp i[data-filled]{{animation:pop {D['fast']}ms {E['spring']}}}
@keyframes pop{{from{{transform:scale({SCL['pop']})}}}}
/* the caret lives in the active empty box */
.sheet .s-otp i[data-at]::after{{content:'';width:2px;height:22px;background:{C['text']['primary']};
  animation:caret {CARET_MS}ms step-end infinite}}
@keyframes caret{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
/* one transparent input across the whole row — see otp_row() */
.sheet .s-otp__in{{position:absolute;inset:0;width:100%;opacity:0;border:0;background:none;
  font:inherit;cursor:pointer}}
/* Error line. status.negative is the palette's only non-green hue and exists
   for exactly this: something that is wrong. `salmonDeep` because a label has
   to BE readable text on a light ground — the `salmon` anchor measures 2.09:1
   there and fails badly. Nothing in the owner's frames uses this; the three
   edge states in build-prototype.py that do are marked EXTRAPOLATED. */
.sheet .err{{{ty('caption')}color:{C['status']['negative']['text']};
  text-align:center;margin-top:{S['s2']}px}}
.sheet[data-align="left"] .err{{text-align:left}}
.sheet .resend{{{ty('caption')}color:{C['text']['secondary']};text-align:center;
  margin-top:{RH['controlGap']}px}}
.sheet .resend b{{color:{C['text']['primary']};font-variation-settings:'wght' 600}}
.sheet .resend__b{{background:none;border:0;font:inherit;{ty('caption')}
  font-variation-settings:'wght' 600;color:{C['text']['accent']};cursor:pointer}}

/* ---- the hand-off ---------------------------------------------------- */
.done{{position:absolute;inset:0;z-index:40;display:none;place-items:center;
  background:{G['canvas']['css']};text-align:center;padding:0 {LAY['screenPaddingX']}px}}
.phone[data-done] .done{{display:grid;animation:cin {D['gentle']}ms {E['spring']} both}}
.done h2{{{ty('title1')}margin-bottom:{S['s3']}px}}
.done p{{{ty('body')}color:{C['text']['secondary']}}}
.done button{{margin-top:{S['s6']}px;height:{LAY['chipHeight']}px;padding:0 {S['s5']}px;
  border:0;border-radius:{R['full']}px;background:{C['surface']['raised']};font:inherit;
  {ty('caption')}color:{C['text']['primary']};cursor:pointer;
  box-shadow:{EL['control']['css']}}}
"""

# Motion gate 2 — mandatory, and it is the reason this block is never optional
# in a file that animates. Exported separately so a document composing several
# of these CSS blocks emits it once rather than three times.
CSS_REDUCE = """
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.01ms !important;animation-iteration-count:1 !important;
    transition-duration:.01ms !important}
}
"""

CSS = CSS_CHROME + CSS_BG + CSS_SHEET + CSS_REDUCE

# ---------------------------------------------------------------------------
# Runtime. Durations come from the motion tokens, injected as MO — no raw ms.
# ---------------------------------------------------------------------------

# The runtime is split the same way the CSS is, and for the same reason:
# build-first-run.py drives this exact sheet from a different controller, and
# a second copy of ~100 lines of proven input/OTP/countdown logic is precisely
# the drift _phone_fit.py's docstring exists to warn about.
#
#   JS_PRELUDE  constants, shared state, stamp/railMark
#   JS_SHEET    paint + wire + focus + render + countdown, and the shared
#               `go()`. Id-agnostic: it knows about sheet states and nothing
#               else, and defers anything it does not recognise to `route()`.
#   JS_CTRL     this file's own controller — the `route()` hook, the splash,
#               the listeners, the hash boot.
#
# `route(id)` is the extension point. It returns true if the controller fully
# handled that id (an onboarding screen, an end card) and false to let the
# sheet logic run. That one hook is the whole difference between the standalone
# sign-in prototype and the merged flow.

JS_PRELUDE = """
const MO = __MOTION__;
const STATES = __STATES__;
const RESEND_S = 15;

const phone = document.querySelector('.phone');
const sheet = document.querySelector('.sheet');
const body  = document.querySelector('.sheet__c');
const noteEl= document.getElementById('note');
const rail  = [...document.querySelectorAll('.rail__i')];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

let current = null, timer = null, mail = 'ruhaanroyce@gmail.com';
// Keyed by state id, one entry per OTP screen this file owns. `A5` was here
// for the email-OTP-over-profile state deleted 2026-08-17 and was already
// unread; dropped 2026-08-19 while this file's STATES were rewritten anyway.
const code = {A3: ''};

/* Every state is addressable: #A3 opens on the mobile OTP, #S0 holds the
   splash instead of letting it advance. Reviewers need to link a single state,
   and a splash that always runs away is unscreenshottable. */
function stamp(id){
  if (location.hash.slice(1) !== id) history.replaceState(null, '', '#' + id);
}

function railMark(id){
  rail.forEach(b => b.setAttribute('aria-current', String(b.dataset.to === id)));
  const s = STATES.find(x => x.id === id);
  if (s && s.note) noteEl.innerHTML = s.note;
}
"""

JS_SHEET = """
/* Height is animated rather than left to reflow: the sheet is one surface that
   RESIZES between states, not five sheets that replace each other. */
function paint(id, stagger){
  const s = STATES.find(x => x.id === id);
  if (!s || !s.inner) return;
  sheet.dataset.align = s.align;
  body.innerHTML = s.inner;
  body.removeAttribute('data-out');
  /* First arrival staggers its children; every later swap animates the block
     as one. Setting both would double-animate each child. */
  body.classList.toggle('sheet__c--stagger', !!stagger);
  if (!stagger) body.setAttribute('data-in','');
  const mailEl = body.querySelector('[data-mail]');
  if (mailEl) mailEl.textContent = mail;
  sheet.style.height = body.offsetHeight + 'px';
  wire(s);
}

function go(id){
  if (id === current) return;
  if (timer) { clearInterval(timer); timer = null; }
  stamp(id);

  /* The controller's chance to claim this id — an onboarding screen, an end
     card, anything that is not a sheet state. See JS_CTRL. */
  if (typeof route === 'function' && route(id)) return;
  railMark(id);

  if (id === 'S0'){
    current = 'S0';
    phone.removeAttribute('data-sheet');
    sheet.style.height = '';
    body.innerHTML = '';
    return;
  }

  const first = !phone.hasAttribute('data-sheet');
  const prev = current;
  current = id;

  if (first){                                   /* the sheet's arrival */
    paint(id, !reduce);
    requestAnimationFrame(() => phone.setAttribute('data-sheet',''));
    return;
  }
  if (prev === null || reduce){ paint(id); return; }

  sheet.style.height = body.offsetHeight + 'px';  /* pin before swapping */
  body.setAttribute('data-out','');
  setTimeout(() => paint(id), MO.fast);
}

/* --- per-state wiring ------------------------------------------------- */
function wire(s){
  const cta = body.querySelector('.s-cta[data-go]');

  // `data-phone` wiring lived here through 2026-08-18; node 2/3 verified a
  // phone number then. As of 2026-08-19 they verify email (see STATES above)
  // and the phone number moved to node 4 — build-prototype.py's own
  // `mobile_field()` / a dedicated verify sheet, a different component.
  const mailIn = body.querySelector('[data-email]');
  if (mailIn){
    mailIn.value = mail === 'ruhaanroyce@gmail.com' ? '' : mail;
    mailIn.addEventListener('input', () => {
      const ok = /^[^@\\s]+@[^@\\s.]+\\.[^@\\s]{2,}$/.test(mailIn.value.trim());
      cta.disabled = !ok;
      if (ok) mail = mailIn.value.trim();
    });
    cta.disabled = true;
    focus(mailIn);
  }

  const otp = body.querySelector('[data-otp]');
  if (otp){
    const step = otp.dataset.otp, input = otp.querySelector('.s-otp__in');
    input.value = code[step] || '';
    render(otp, input.value);
    cta.disabled = input.value.length !== 4;
    input.addEventListener('input', () => {
      input.value = input.value.replace(/\\D/g,'').slice(0,4);
      code[step] = input.value;
      render(otp, input.value);
      cta.disabled = input.value.length !== 4;
    });
    otp.addEventListener('click', () => input.focus());
    focus(input);
    countdown(otp);
  }

  body.querySelectorAll('[data-go]').forEach(b => {
    b.addEventListener('click', () => { if (!b.disabled) go(b.dataset.go); });
  });
}

function focus(el){ if (!matchMedia('(hover: none)').matches) setTimeout(() => el.focus(), MO.base); }

function render(otp, val){
  [...otp.querySelectorAll('i')].forEach((box, i) => {
    const ch = val[i] || '';
    if (box.textContent !== ch){
      box.textContent = ch;
      if (ch) { box.setAttribute('data-filled',''); }
      else box.removeAttribute('data-filled');
    }
    box.toggleAttribute('data-at', i === val.length && val.length < 4);
  });
}

/* The countdown is real, and it is visible from t=0 rather than after a
   failure — that was true of the old build and is kept. */
function countdown(scope){
  const lab = scope.parentNode.querySelector('[data-resend]');
  const btn = scope.parentNode.querySelector('[data-resendbtn]');
  if (!lab) return;
  let left = RESEND_S;
  const tick = () => {
    left -= 1;
    if (left <= 0){
      clearInterval(timer); timer = null;
      lab.hidden = true; btn.hidden = false;
      return;
    }
    lab.innerHTML = 'Resend OTP in <b>' + left + 's</b>';
  };
  lab.innerHTML = 'Resend OTP in <b>' + left + 's</b>';
  lab.hidden = false; btn.hidden = true;
  if (timer) clearInterval(timer);
  timer = setInterval(tick, 1000);
  btn.addEventListener('click', () => { left = RESEND_S + 1; lab.hidden = false;
    btn.hidden = true; if (timer) clearInterval(timer); timer = setInterval(tick, 1000); tick(); });
}

"""

JS_CTRL = """
/* This file's controller. The merged flow (build-first-run.py) replaces
   everything below with its own `route()` and boot, and reuses everything
   above unchanged. */

/* Only one id here is not a sheet state: the end card. */
function route(id){
  if (id === 'DONE'){
    phone.setAttribute('data-done','');
    railMark('A3'); current = 'DONE';
    return true;
  }
  phone.removeAttribute('data-done');
  return false;
}

/* --- splash ----------------------------------------------------------- */
let splashTimer = null;
function splash(hold){
  go('S0');
  clearTimeout(splashTimer);
  if (hold) return;                       /* #S0 — held open for review */
  splashTimer = setTimeout(() => { if (current === 'S0') go('A1'); }, MO.splashHold);
}
phone.addEventListener('click', e => {
  if (current === 'S0' && !e.target.closest('.sheet')) { clearTimeout(splashTimer); go('A1'); }
});

rail.forEach(b => b.addEventListener('click', () => {
  clearTimeout(splashTimer);
  b.dataset.to === 'S0' ? splash() : go(b.dataset.to);
}));
document.querySelector('[data-restart]').addEventListener('click', splash);

addEventListener('resize', () => { if (current && current !== 'S0') sheet.style.height = body.offsetHeight + 'px'; });

const at = location.hash.slice(1).toUpperCase();
if (at === 'S0') splash(true);
else if (STATES.some(s => s.id === at)) go(at);
else splash();
"""

JS = JS_PRELUDE + JS_SHEET + JS_CTRL


def build():
    bg, real = background()

    rail = "".join(
        '<button class="rail__i" data-to="%s"><span class="rail__n">%s</span>%s</button>'
        % (s["id"], s["id"], s["label"]) for s in STATES
    )

    js_states = json.dumps([
        {"id": s["id"], "align": s.get("align", "center"),
         "inner": s.get("inner"), "note": s["note"]} for s in STATES
    ])
    js_motion = json.dumps({
        "fast": D["fast"], "base": D["base"], "sheet": D["sheet"],
        # The splash hold is not a motion token — it is a DWELL, not a
        # transition, and the token file is deliberate about `ambient` being
        # its only long value. Named here so it is greppable rather than
        # inline. Raised 1600 -> 2600 on 2026-08-17 with the slower arrival:
        # the sheet was landing while the image was still being read, which is
        # most of what made the old opening feel rushed. 2600 is roughly the
        # bgSettle animation's useful half — long enough to notice the room,
        # short enough that a returning user is not waiting on it.
        "splashHold": 2600,
    })
    js = (JS.replace("__MOTION__", js_motion)
            .replace("__STATES__", js_states))

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>NOMA — First run · nodes 1-5</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style></head><body>
  <div class="rail">
    <div class="rail__b">NOMA · Sign in</div>
    {rail}
    <button class="rail__i" data-restart><span class="rail__n">↺</span>Replay from splash</button>
    <p class="note" id="note"></p>
  </div>
  <div class="stage">
    <div class="phone">
      <div class="notch"></div>
      <div class="bg">{bg}</div>
      {status_bar()}
      {wordmark()}
      <div class="sheet"><i class="sheet__s"></i><div class="sheet__c"></div></div>
      <div class="done">
        <div>
          <h2>Signed in</h2>
          <p>Node 5 hands over to node 6, “Which one did you bring home?”, in
             onboarding-prototype.html. Nothing past here changed.</p>
          <button data-restart>Replay from the splash</button>
        </div>
      </div>
      <div class="hbar"></div>
    </div>
  </div>
<script>{js}</script>
<script>{FIT_JS}
watchPhoneFit({{padY: 16, padX: 16}});</script></body></html>"""

    OUT.write_text(html, encoding="utf-8")
    print("wrote %s (%d states, %d KB)%s"
          % (OUT.relative_to(ROOT), len(STATES), len(html) // 1024,
             "" if real else "  [placeholder background]"))


if __name__ == "__main__":
    build()
