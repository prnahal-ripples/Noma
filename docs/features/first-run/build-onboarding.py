#!/usr/bin/env python3
"""
Build docs/features/first-run/onboarding-prototype.html

First run, rebuilt in the 2026-08-11 visual language.

    python3 docs/features/first-run/build-onboarding.py

WHAT THIS IS, AND WHAT IT ISN'T. This is a VISUAL rebuild of the flow's spine —
eleven screens covering every component type the language needs. It is not a
replacement for first-run-prototype.html, which carries all ~40 screens, every
error state, and the node-by-node reasoning. That file remains the flow's
canonical prototype; this one shows what the flow LOOKS like now. Screen ids
below match the PRD's node table exactly, so the two line up.

SCREEN IDS → PRD nodes: A2·2 A3·3 P1·6 P2·7 P3·9 W3·15 W4·16 L1·24 N1·25
R1·17 C1·23.

COPY IS VERBATIM from docs/features/first-run/prd.md and the existing
prototype. Not one line was rewritten for this rebuild — the voice was
re-specified on 2026-08-06 and is not a visual concern. First person singular,
reason always given as the subtitle, privacy as a concrete negative (§8.1).

TOKENS ARE READ, NOT RESTATED. Same node-import approach as build-settings.py:
every colour, radius, shadow and type step below is generated from
src/tokens/design.tokens.js at build time. Re-run after a token change.

THREE COMPONENTS CAME FROM THE OWNER'S FIGMA INSPECTOR (2026-08-11) and are
now recipes in the token module rather than local values here:

  recipes.cardSelect     radius 12, padding 16, gap 20, #FFFFFF fill,
                         1px INSIDE white stroke, drop shadow.
                         Selection is LIFT — the chosen row is raised and the
                         others go flat and muted. No tick, no accent border.
  recipes.illustration   radius 24, linear fill, 8px INSIDE white stroke.
                         The 8pt frame is the whole effect.
  recipes.buttonQuiet    "Not now" — same 56pt height and full radius as the
                         primary CTA, near-white instead of ink.

Adding cardSelect also surfaced a gap in the radius scale: the inspector says
12 and the ramp went 10 → 16. radius.sm is now 12 and the old 10 moved to
radius.xs (progress segments). That is a token change, not a local override.

ILLUSTRATIONS ARE PLACEHOLDERS. The product renders and the 3D house in the
owner's reference are real assets; there are none in this repo, so the plates
below are drawn as SVG in the right shape, palette and framing. They are
composition-correct and art-direction-wrong on purpose — swap in the real
renders and nothing around them has to move.
"""

import json
import subprocess
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _phone_fit import CSS as FIT_CSS, JS as FIT_JS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent / "onboarding-prototype.html"
TOKENS = ROOT / "src" / "tokens" / "design.tokens.js"


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

FONT = "../../../src/fonts/google-sans-flex/GoogleSansFlex-VariableFont_GRAD,ROND,opsz,slnt,wdth,wght.ttf"

# Illustration plates.
#
# ⚠ RETUNED 2026-08-12 to the owner's palette rule: outside white and grey,
# ONLY the two greens and shades of them. The old blue / teal / amber plates
# are gone — they were three unrelated hues doing a job (telling the three
# SKUs apart) that the palette no longer permits. The three SKUs are now
# separated by DEPTH within one hue family — mint at the top of the ramp,
# lime at the bottom, and a near-neutral haze for the third — which is a
# weaker signal than three colours were. Flagged rather than smuggled: if the
# SKUs genuinely need to be distinguishable at a glance, that wants product
# renders, not plate tints.
# The two washes fade to the neutral BY THE HALFWAY POINT, not at the very
# bottom. That is what keeps a 232pt hero plate inside the 10% budget (LAW 6):
# a plate that is green all the way down is ~16% of the screen on its own.
# Green at the top, dissolving into white — "very white with a hint of green".
PLATES = {
    "mint": "linear-gradient(170deg,__MINT__ 0%,__HAZE__ 52%,#FFFFFF 100%)",
    "lime": "linear-gradient(170deg,__LIME__ 0%,__HAZE__ 52%,#FFFFFF 100%)",
    # Full mint→lime. Reserved for the ONE feature surface (LAW 5). Not a plate.
    "ramp": "linear-gradient(165deg,__MINT__ 0%,__LIME__ 100%)",
    "haze": "linear-gradient(170deg,__HAZE__ 0%,#FFFFFF 100%)",
}


# ---------------------------------------------------------------------------
# SVG parts. Drawn, not vendored — see the docstring.
# ---------------------------------------------------------------------------

def tint(svg):
    """Single swap point for the plates' green. They carry __MINT__ / __LIME__
    placeholders rather than a literal hex, so a palette change lands here too
    (CLAUDE.md rule 4 — no hardcoded colours)."""
    return (svg.replace("__MINT__", T["green"]["mint"])
               .replace("__LIME__", T["green"]["lime"])
               .replace("__DEEP__", T["green"]["mintDeep"])
               .replace("__HAZE__", T["green"]["haze"]))


def _lerp_hex(a, b, t):
    """Linear-interpolate two hex colours — sweeps filled progress bars from
    green.mint to green.lime by position."""
    a, b = a.lstrip("#"), b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        av, bv = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append("%02X" % round(av + (bv - av) * t))
    return "#" + "".join(out)


def prog_bars(frac, total=20):
    """recipes.progressTrack — INDIVIDUAL RECTANGLES, 2px corners, 4px gap.
    ⚠ Replaces a repeating-gradient MASK over one continuous bar — that
    produced a squashed-capsule look, not discrete shapes (owner correction).
    """
    RC_ = RC["progressTrack"]
    filled = round(total * frac)
    bars = []
    for i in range(total):
        if i < filled:
            t = i / max(filled - 1, 1)
            color = _lerp_hex(RC_["fillFrom"], RC_["fillTo"], t)
            bars.append('<i style="background:%s"></i>' % color)
        else:
            bars.append('<i class="prog__off"></i>')
    return '<span class="prog">%s</span>' % "".join(bars)


def purifier(w=44, dark_top=True):
    """The Air Pro silhouette: white cylinder, dark control panel, green LED."""
    h = int(w * 1.42)
    return tint(f"""<svg width="{w}" height="{h}" viewBox="0 0 44 62" fill="none">
      <ellipse cx="22" cy="57.5" rx="17" ry="3.2" fill="rgba(0,0,0,.13)"/>
      <path d="M5 14c0-1.6 1.2-2.6 2.7-2.9C11.6 10.4 16.4 10 22 10s10.4.4 14.3 1.1
        C37.8 11.4 39 12.4 39 14v40c0 2.2-1.4 3.4-3.4 3.7-3.7.6-8.2.9-13.6.9s-9.9-.3-13.6-.9
        C6.4 57.4 5 56.2 5 54z" fill="#fff"/>
      <path d="M5 14c0-1.6 1.2-2.6 2.7-2.9C11.6 10.4 16.4 10 22 10s10.4.4 14.3 1.1
        C37.8 11.4 39 12.4 39 14v3.4c0 1.5-1.2 2.4-2.7 2.7-3.9.7-8.7 1.1-14.3 1.1
        s-10.4-.4-14.3-1.1C6.2 19.8 5 18.9 5 17.4z" fill="{'#3C3C3A' if dark_top else '#E8E8E5'}"/>
      <ellipse cx="22" cy="13.6" rx="17" ry="3.4" fill="{'#4A4A47' if dark_top else '#F2F2F0'}"/>
      <rect x="21.2" y="33" width="1.6" height="9" rx=".8" fill="__MINT__"/>
      <path d="M7.6 26h4M7.6 30h4M7.6 34h4M32.4 26h4M32.4 30h4M32.4 34h4"
        stroke="rgba(0,0,0,.10)" stroke-width="1.1" stroke-linecap="round"/>
    </svg>""")


def house_geo():
    """Node 24's plate: the home, a geofence ring, and you crossing it."""
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <circle cx="100" cy="104" r="66" fill="#fff" opacity=".34"/>
      <circle cx="100" cy="104" r="66" stroke="#2E2E2C" stroke-width="2"
        stroke-dasharray="5 7" stroke-linecap="round" opacity=".62"/>
      <ellipse cx="100" cy="146" rx="46" ry="7" fill="rgba(0,0,0,.10)"/>
      <path d="M62 104 100 74l38 30v40H62z" fill="#fff"/>
      <path d="M100 74 62 104h12l26-20 26 20h12z" fill="#EDEDEA"/>
      <rect x="94" y="119" width="13" height="25" rx="1.6" fill="#D6D6D2"/>
      <rect x="72" y="112" width="14" height="12" rx="1.6" fill="#E4E4E0"/>
      <rect x="116" y="112" width="14" height="12" rx="1.6" fill="#E4E4E0"/>
      <rect x="120" y="80" width="9" height="16" rx="1.6" fill="#EDEDEA"/>
      <circle cx="46" cy="52" r="9" fill="__MINT__"/>
      <circle cx="46" cy="52" r="15" fill="__MINT__" opacity=".22"/>
    </svg>""")


def bell_plate():
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <circle cx="100" cy="100" r="58" fill="#fff" opacity=".42"/>
      <ellipse cx="100" cy="150" rx="40" ry="6.5" fill="rgba(0,0,0,.10)"/>
      <path d="M68 116c0-3 4-6 4-20a28 28 0 0 1 56 0c0 14 4 17 4 20z" fill="#fff"/>
      <path d="M64 116h72a5 5 0 0 1 0 10H64a5 5 0 0 1 0-10z" fill="#EDEDEA"/>
      <path d="M90 132a10.5 10.5 0 0 0 20 0z" fill="#fff"/>
      <circle cx="128" cy="70" r="10" fill="__MINT__"/>
      <circle cx="128" cy="70" r="16" fill="__MINT__" opacity=".22"/>
    </svg>""")


def filter_plate():
    """Node 7 — the polybag coming off. The one invisible setup failure."""
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <ellipse cx="100" cy="156" rx="44" ry="7" fill="rgba(0,0,0,.10)"/>
      <rect x="62" y="58" width="76" height="94" rx="8" fill="#fff"/>
      <path d="M70 74h60M70 88h60M70 102h60M70 116h60M70 130h60"
        stroke="#D8D8D4" stroke-width="3.4" stroke-linecap="round"/>
      <path d="M58 52c26-9 58-9 84 0 7 2.4 9 7 6 12-4 6-14 4-22 2-20-5-32-5-52 0
        -8 2-18 4-22-2-3-5-1-9.6 6-12z" fill="#fff" opacity=".62"/>
      <path d="M58 52c26-9 58-9 84 0" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      <circle cx="150" cy="44" r="9" fill="__MINT__"/>
      <path d="m146 44 3 3 5.5-6" stroke="#fff" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round"/>
    </svg>""")


def light_plate():
    """Node 9 — the Wi-Fi light blinking. User-paced, never a timer."""
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <ellipse cx="100" cy="158" rx="42" ry="6.5" fill="rgba(0,0,0,.10)"/>
      <rect x="66" y="44" width="68" height="112" rx="12" fill="#fff"/>
      <rect x="66" y="44" width="68" height="26" rx="12" fill="#3C3C3A"/>
      <path d="M84 118h32M84 128h32M84 138h32" stroke="#E4E4E0" stroke-width="3"
        stroke-linecap="round"/>
      <g class="blink">
        <circle cx="100" cy="92" r="7" fill="__MINT__"/>
        <circle cx="100" cy="92" r="15" fill="__MINT__" opacity=".26"/>
        <circle cx="100" cy="92" r="24" fill="__MINT__" opacity=".12"/>
      </g>
    </svg>""")


def wifi_plate():
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <circle cx="100" cy="104" r="60" fill="#fff" opacity=".38"/>
      <g stroke="#fff" stroke-width="11" stroke-linecap="round" fill="none">
        <path d="M56 92a64 64 0 0 1 88 0"/>
        <path d="M72 112a40 40 0 0 1 56 0"/>
      </g>
      <circle cx="100" cy="134" r="8.5" fill="#fff"/>
    </svg>""")
    # No success tick here on purpose: W3 is the 38%-complete screen. A green
    # check on a screen that says "Getting everything talking" tells the user
    # the opposite of the progress bar directly beneath it. The tick belongs
    # to W4, which is the screen that actually earned it.


def shield_plate():
    return tint("""<svg viewBox="0 0 200 200" fill="none" width="100%" height="100%">
      <ellipse cx="100" cy="160" rx="38" ry="6" fill="rgba(0,0,0,.10)"/>
      <path d="M100 42 58 58v44c0 30 20 52 42 60 22-8 42-30 42-60V58z" fill="#fff"/>
      <path d="M100 42 58 58v44c0 30 20 52 42 60z" fill="#F4F4F2"/>
      <path d="m84 100 12 12 22-25" stroke="__MINT__" stroke-width="7"
        stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""")


# ---------------------------------------------------------------------------
# Chrome
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


def nav(back=None):
    b = ('<button class="iconbtn" data-go="%s">'
         '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M14.5 5.5 8 12l6.5 6.5"/></svg></button>' % back) if back else "<span></span>"
    return '<div class="nav">%s</div>' % b


def t1(txt):
    return '<h1 class="t1">%s</h1>' % txt


def bd(txt):
    return '<p class="bd">%s</p>' % txt


def foot(txt):
    return '<p class="foot">%s</p>' % txt


def plate(inner, tone="mint", size=None):
    """recipes.illustration — gradient plate, 8pt white frame, tilted."""
    sz = size or RC["illustration"]["size"]
    return ('<div class="plate" style="width:%dpx;height:%dpx;background:%s">%s</div>'
            % (sz, sz, tint(PLATES[tone]), inner))


def cta(label, go=None):
    return '<button class="cta"%s>%s</button>' % (
        ' data-go="%s"' % go if go else "", label)


def quiet(label, go=None):
    return '<button class="quiet"%s>%s</button>' % (
        ' data-go="%s"' % go if go else "", label)


def dots(n, at):
    return '<div class="dots">%s</div>' % "".join(
        '<i%s></i>' % (' class="on"' if i == at else "") for i in range(n))


def dock(inner):
    """CTA docked to the bottom edge. Everything above it scrolls."""
    return '<div class="dock">%s</div>' % inner


def selcard(name, sub, spec, tone, sel=False, go=None):
    """recipes.cardSelect / cardSelectIdle. LAW 3 — selection is lift."""
    chev = ('<svg class="sel__c" width="17" height="17" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.9" stroke-linecap="round" '
            'stroke-linejoin="round"><path d="M9.5 5.5 16 12l-6.5 6.5"/></svg>') if sel else ""
    return (
        '<button class="sel%s"%s>'
        '<span class="sel__th" style="background:%s">%s</span>'
        '<span class="sel__c1"><span class="sel__n">%s</span>'
        '<span class="sel__s">%s</span><span class="sel__sp">%s</span></span>'
        '%s</button>'
        % (" sel--on" if sel else "", ' data-go="%s"' % go if go else "",
           tint(PLATES[tone]), purifier(38, dark_top=sel), name, sub, spec, chev)
    )


# ---------------------------------------------------------------------------
# Screens. Ids match the PRD node table.
# ---------------------------------------------------------------------------

SCREENS = []


def SC(sid, node, label, body, note):
    SCREENS.append({"id": sid, "node": node, "label": label, "body": body, "note": note})


SC("A2", 2, "Login", f"""
  {nav()}
  {t1("First, how do I reach you?")}
  {bd("A code by text, and that’s it. No password to remember: your number is how you get back in.")}
  <div class="field">
    <span class="field__cc">🇮🇳 +91<svg width="14" height="14" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="m6 9.5 6 6 6-6"/></svg></span>
    <span class="field__div"></span>
    <span class="field__v">98765 43210</span><span class="caret"></span>
  </div>
  {foot("By continuing you agree to the Terms and the Privacy Policy.")}
""", "Node 2. India default, country selector present. No password anywhere in this flow — "
     "the number is the account.")

SC("A3", 3, "Verify", f"""
  {nav("A2")}
  {t1("Just sent you a code")}
  {bd("To +91 98765 43210. It should land in a few seconds.")}
  <div class="otp">{"".join('<i%s>%s</i>' % (" f" if i < 4 else "", "471 9"[i] if i < 4 else "")
                            for i in range(6))}</div>
  <button class="lnk">Resend in 0:24</button>
""", "Node 3. Auto-advance on the sixth digit. The resend timer is visible from t=0, not "
     "after the first failure.")

SC("P1", 6, "Choose your purifier", f"""
  {nav("A3")}
  {t1("Which one did you bring home?")}
  {bd("One to start. You can add the rest whenever you like.")}
  <div class="sels">
    {selcard("Air Pro 200", "Bedrooms and small rooms", "Up to 280 ft² · CADR 240 m³/hr", "mint", True, "P2")}
    {selcard("Air Pro 500", "Living rooms and mid-size homes", "Up to 550 ft² · CADR 400 m³/hr", "lime")}
    {selcard("Air Pro Max", "Whole-floor coverage", "Up to 900 ft² · CADR 600 m³/hr", "haze")}
  </div>
""", "Node 6. Three SKUs from src/hardware/devices.json — one product line, three sizes, no "
     "device-type chooser. recipes.cardSelect: the chosen row is lifted and the other two go "
     "flat and muted. No tick, no accent border — selection is elevation (LAW 3).")

SC("P2", 7, "Unwrap the filter", f"""
  {nav("P1")}
  {plate(filter_plate(), "lime")}
  {t1("Let’s get the filter out of its bag")}
  {bd("It ships sealed in plastic. Until that comes off it will hum away happily and clean nothing at all.")}
  {foot("Then slide it back in and close the door until it clicks.")}
""", "Node 7 — the highest-value screen in the sequence. The only setup failure that is "
     "completely invisible: a bagged purifier behaves normally in every respect except "
     "cleaning. The frame stays warm; the instruction itself stays literal (§8.1).")

SC("P3", 9, "Wi-Fi light", f"""
  {nav("P2")}
  {plate(light_plate(), "mint")}
  {t1("Is the little light blinking?")}
  {bd("A slow blink means it’s ready for me. It can take a moment to get there.")}
  {foot("Not blinking? Hold the Wi-Fi icon for five or six seconds until it starts.")}
""", "Node 9. User-paced, never a timer. The recovery is ON the screen rather than behind a "
     "help link — on a re-setup it is the common path, not an error. ⚠ O-9.")

SC("W3", 15, "Setting up", f"""
  {nav()}
  {plate(wifi_plate(), "mint")}
  {t1("Getting everything talking")}
  {bd("Fifteen seconds or so.")}
  {prog_bars(0.38)}
  <p class="prog__l">Joining Sharma_Home<span>38%</span></p>
""", "Node 15. 15–20s of real device work. The wait is named before it starts and the user is "
     "released from it (§8.2 rule 3). CTA pinned to the bottom, progress just above it, and "
     "only ONE progress indicator on the screen.")

SC("W4", 16, "Connected", f"""
  {nav()}
  {plate(shield_plate(), "lime")}
  {t1("That’s the hard part done")}
  {bd("It’s on Sharma_Home, and it’ll find its way back on its own from now on.")}
""", "Node 16. A full screen, not a toast — this is where the setup anxiety ends and the "
     "first thing in the flow visibly works.")

SC("L1", 24, "Location", f"""
  {nav("W4")}
  {plate(house_geo(), "mint")}
  {t1("Want the air sorted before you get home?")}
  {bd("If I know you’re on your way, I’ll start clearing the room about twenty minutes out, and ease off once everyone’s gone.")}
  {foot("I only notice you crossing in and out. I never keep a trail of where you’ve been.")}
""", "Node 24 — the flow's only ask with a concrete payoff attached. Ask for While-Using, "
     "never Always. ⚠ It is also the ask most in tension with “what I learn stays here”, said "
     "one screen earlier — hence the third line, which has to be true in the implementation, "
     "not just in the copy.")

SC("N1", 25, "Notifications", f"""
  {nav("L1")}
  {plate(bell_plate(), "haze")}
  {t1("Shall I tell you when something changes?")}
  {bd("Outdoor air spiking, the filter wearing out, anything I did while you were out.")}
  {foot("Never marketing. You can turn any of it off later.")}
""", "Node 25. Declining goes on to node 17 exactly as accepting does — which is why “Not now” "
     "is a full-size button (recipes.buttonQuiet), not a text link.")

SC("R1", 17, "Room & home", f"""
  {nav("N1")}
  {t1("Where does it live?")}
  {bd("So I can compare your air against the right patch of outdoors.")}
  <div class="lbl">Room</div>
  <div class="chips">
    <button class="chip chip--on">Living room</button>
    <button class="chip chip--off">Bedroom</button>
    <button class="chip chip--off">Kitchen</button>
    <button class="chip chip--off">Pooja room</button>
    <button class="chip chip--off">Study</button>
  </div>
  <div class="lbl">Home name</div>
  <div class="field field--plain"><span class="field__v">Ruhaan’s Home</span><span class="caret"></span></div>
  {foot("You can rename any of this later.")}
""", "Node 17. The Home record is created here. ⚠ C-12 — “Pooja Room” is in the preset list; "
     "it is correct for the Indian market and has no equivalent in the reference apps this "
     "language borrowed from. Chips use LAW 3 again: the chosen one is lifted, not coloured.")

SC("C1", 23, "Privacy", f"""
  {nav()}
  {plate(shield_plate(), "lime")}
  {t1("What I learn stays here")}
  {bd("Your readings and your habits live on your devices. The only thing I go and fetch is the outdoor air for your area.")}
""", "Node 23, slide 1. The receipt for the promise made at node 4 — and the screen that "
     "node 24 immediately spends credibility against.")


# Per-screen footer controls.
FOOTERS = {
    "A2": dock(cta("Send code", "A3")),
    "A3": dock(cta("Continue", "P1")),
    "P1": dock(cta("Continue", "P2")),
    "P2": dock(dots(4, 0) + cta("It’s back in", "P3")),
    "P3": dock(dots(4, 1) + cta("Yes, it’s blinking", "W3")),
    "W3": dock(cta("Next", "W4")),
    "W4": dock(dots(4, 3) + cta("Next", "L1")),
    "L1": dock(cta("Yes, do that", "N1") + quiet("Not now", "N1")),
    "N1": dock(cta("Yes, please", "R1") + quiet("Not now", "R1")),
    "R1": dock(cta("Continue", "C1")),
    "C1": dock(dots(3, 0) + cta("Next", "A2")),
}


# Split into CHROME + SCREENS so build-first-run.py can take the screen CSS
# without also taking a second copy of the harness, phone and status bar it
# shares with build-auth.py. `CSS` below concatenates them, so this file's own
# output is unchanged — verified byte-identical when the split was made.
CSS_CHROME = f"""
@font-face {{ font-family:'Google Sans Flex'; src:url('{FONT}') format('truetype');
  font-weight:1 1000; font-display:swap; }}
*{{box-sizing:border-box;margin:0;padding:0}}
/* height, not min-height: the phone is scaled to fit the space available,
   so the page must not grow past the viewport and scroll instead. */
body{{font-family:'Google Sans Flex',system-ui,sans-serif;font-optical-sizing:auto;
  background:{N['150']};color:{C['text']['primary']};display:flex;gap:32px;
  padding:32px;height:100vh;overflow:hidden;-webkit-font-smoothing:antialiased}}
{FIT_CSS}

/* review chrome — not part of the product */
.rail{{width:230px;flex:none;align-self:stretch;
  overflow-y:auto;scrollbar-width:none}}
.rail::-webkit-scrollbar{{display:none}}
.rail__b{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:{C['text']['tertiary']};font-weight:600;margin-bottom:13px}}
.rail__i{{display:flex;align-items:baseline;gap:9px;width:100%;text-align:left;
  background:{N['0']};border:0;border-radius:{R['sm']}px;padding:10px 12px;margin-bottom:6px;
  font:inherit;font-size:13.5px;cursor:pointer;color:{C['text']['secondary']};
  box-shadow:{EL['control']['css']};transition:transform .16s}}
.rail__i:hover{{transform:translateX(2px)}}
.rail__i[aria-current="true"]{{color:{C['text']['primary']};font-weight:600;
  box-shadow:{EL['card']['css']},inset 0 0 0 1px {C['border']['bevel']}}}
.rail__n{{font-size:10.5px;color:{C['text']['tertiary']};font-family:ui-monospace,Menlo,monospace}}
.note{{font-size:11.5px;line-height:1.65;color:{C['text']['tertiary']};margin-top:16px}}
.note b{{color:{C['text']['secondary']}}}

/* phone */
.phone{{width:390px;height:844px;flex:none;border-radius:52px;position:relative;
  overflow:hidden;background:{G['canvas']['css']};box-shadow:0 40px 90px rgba(0,0,0,.16)}}
.notch{{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:122px;height:33px;
  background:{N['900']};border-radius:20px;z-index:60}}
.hbar{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:138px;height:5px;
  background:rgba(0,0,0,.2);border-radius:3px;z-index:60}}
.scr{{position:absolute;inset:0;display:none;flex-direction:column}}
.scr[data-on]{{display:flex;animation:in .36s cubic-bezier(.22,1,.36,1)}}
@keyframes in{{from{{opacity:0;transform:translateX(16px)}}}}

.sbar{{height:54px;flex:none;display:flex;align-items:center;justify-content:space-between;
  padding:14px {LAY['screenPaddingX']}px 0}}
.sbar__t{{font-size:15px;font-variation-settings:'wght' 600;letter-spacing:-.2px}}
.sbar__r{{display:flex;align-items:center;gap:5px}}
.bat{{width:25px;height:12px;border-radius:3.5px;border:1.3px solid currentColor;padding:1.4px;display:block}}
.bat i{{display:block;height:100%;width:88%;background:currentColor;border-radius:1.4px}}
"""

CSS_SCREENS = f"""
.body{{flex:1;overflow-y:auto;padding:0 {LAY['screenPaddingX']}px;scrollbar-width:none;
  display:flex;flex-direction:column}}
.body::-webkit-scrollbar{{display:none}}
.nav{{padding:6px 0 18px}}
.iconbtn{{width:{LAY['controlSize']}px;height:{LAY['controlSize']}px;border-radius:{R['full']}px;
  background:{C['surface']['control']};border:0;display:grid;place-items:center;cursor:pointer;
  color:{C['icon']['primary']};
  box-shadow:{EL['control']['css']},inset 0 0 0 {LAY['bevelWidth']}px {C['border']['bevel']}}}
.iconbtn:active{{transform:scale(.94)}}

.t1{{font-size:30px;line-height:36px;letter-spacing:-.7px;
  font-variation-settings:'opsz' 30,'wght' 700;margin-bottom:10px}}
.bd{{font-size:16.5px;line-height:23px;color:{C['text']['secondary']};margin-bottom:6px}}
.foot{{font-size:12.5px;line-height:18px;color:{C['text']['tertiary']};margin-top:12px}}
.lbl{{font-size:12px;letter-spacing:.96px;text-transform:uppercase;
  font-variation-settings:'wght' 600;color:{C['text']['secondary']};margin:22px 0 10px 2px}}

/* recipes.illustration — 8pt white frame IS the effect */
.plate{{border-radius:{RC['illustration']['borderRadius']}px;
  border:{RC['illustration']['frameWidth']}px solid {RC['illustration']['frameColor']};
  box-shadow:{EL['floating']['css']};margin:8px auto 30px;flex:none;
  transform:rotate({RC['illustration']['tiltDeg']}deg);overflow:hidden;
  display:grid;place-items:center}}
.blink{{animation:bl 1.9s ease-in-out infinite}}
@keyframes bl{{0%,100%{{opacity:1}}50%{{opacity:.28}}}}

/* recipes.cardSelect — LAW 3, selection is lift */
.sels{{display:flex;flex-direction:column;gap:{RC['cardSelect']['gap']}px;margin-top:22px}}
.sel{{display:flex;align-items:center;gap:14px;width:100%;text-align:left;font:inherit;
  cursor:pointer;padding:{RC['cardSelect']['padding']}px;
  border-radius:{RC['cardSelect']['borderRadius']}px;
  background:{RC['cardSelectIdle']['background']};
  border:{LAY['hairlineWidth']}px solid {C['border']['subtle']};
  transition:transform .2s cubic-bezier(.22,1,.36,1)}}
.sel--on{{background:{RC['cardSelect']['background']};
  border-color:{RC['cardSelect']['borderColor']};box-shadow:{EL['card']['css']}}}
.sel:active{{transform:scale(.99)}}
.sel__th{{width:{RC['cardSelect']['thumbSize']}px;height:{RC['cardSelect']['thumbSize']}px;
  border-radius:{RC['cardSelect']['thumbRadius']}px;display:grid;place-items:center;flex:none}}
.sel:not(.sel--on) .sel__th{{filter:saturate(.42) opacity(.6)}}
.sel__c1{{display:flex;flex-direction:column;flex:1;min-width:0}}
.sel__n{{font-size:16px;font-variation-settings:'wght' 700;letter-spacing:-.2px;
  color:{C['text']['primary']}}}
.sel:not(.sel--on) .sel__n{{color:{C['text']['secondary']}}}
.sel__s{{font-size:14px;color:{C['text']['secondary']};margin-top:2px}}
.sel__sp{{font-size:12.5px;color:{C['text']['tertiary']};margin-top:3px}}
.sel:not(.sel--on) .sel__s,.sel:not(.sel--on) .sel__sp{{color:{C['text']['tertiary']}}}
.sel__c{{color:{C['icon']['primary']};flex:none}}

/* input */
.field{{display:flex;align-items:center;gap:12px;height:{LAY['inputHeight']}px;
  border-radius:{R['lg']}px;background:{C['surface']['raised']};padding:0 16px;
  box-shadow:{EL['control']['css']};margin-top:22px}}
.field--plain{{margin-top:0}}
.field__cc{{display:flex;align-items:center;gap:5px;font-size:16px;
  font-variation-settings:'wght' 600;color:{C['text']['primary']}}}
.field__div{{width:1px;height:22px;background:{C['border']['hairline']}}}
.field__v{{font-size:16.5px;letter-spacing:.2px}}
.caret{{width:2px;height:21px;background:{C['text']['accent']};
  animation:cr 1.1s step-end infinite;margin-left:1px}}
@keyframes cr{{0%,100%{{opacity:1}}50%{{opacity:0}}}}

.otp{{display:flex;gap:9px;margin-top:24px}}
.otp i{{flex:1;height:58px;border-radius:{R['md']}px;background:{C['surface']['raised']};
  box-shadow:{EL['control']['css']};display:grid;place-items:center;font-style:normal;
  font-size:22px;font-variation-settings:'wght' 700}}
.otp i.f{{box-shadow:{EL['control']['css']},inset 0 0 0 1.5px {C['border']['strong']}}}
.lnk{{background:none;border:0;font:inherit;font-size:14.5px;
  font-variation-settings:'wght' 600;color:{C['text']['accent']};cursor:pointer;
  margin-top:18px;align-self:flex-start}}

/* recipes.progressTrack — INDIVIDUAL RECTANGLES, no wrapping pill, no mask.
   [OWNER REFERENCE] 2px corner radius, 4px gap. Replaces a repeating-gradient
   mask over one continuous bar, which read as a squashed capsule. */
.prog{{display:flex;align-items:center;gap:{RC['progressTrack']['segmentGap']}px;
  margin-top:26px;width:100%}}
.prog i{{flex:1;height:{RC['progressTrack']['heightLg']}px;
  border-radius:{RC['progressTrack']['segmentRadius']}px}}
.prog__off{{background:{RC['progressTrack']['trackEmpty']}}}
.prog__l{{display:flex;justify-content:space-between;font-size:13px;
  color:{C['text']['secondary']};margin-top:9px}}
.prog__l span{{font-variation-settings:'wght' 700;color:{C['text']['primary']}}}

/* Chiclets — radius 8, NOT pills [INSPECTOR]. LAW 3: selection is depth. */
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chip{{height:{LAY['chipHeight']}px;border-radius:{R['xs']}px;border:0;padding:0 16px;
  font:inherit;font-size:14px;cursor:pointer;transition:box-shadow .18s,transform .18s}}
.chip--on{{background:{RC['chipSelected']['background']};color:{C['text']['primary']};
  font-variation-settings:'wght' 600;box-shadow:{FX['chicletSelected']['css']}}}
.chip--off{{background:{RC['chipUnselected']['background']};color:{C['text']['tertiary']};
  box-shadow:{FX['chiclet']['css']}}}
.chip:active{{transform:scale(.97)}}

/* dock */
.dock{{flex:none;padding:14px {LAY['screenPaddingX']}px 30px;display:flex;
  flex-direction:column;gap:10px}}
.cta{{height:{LAY['ctaHeight']}px;border:0;border-radius:{R['full']}px;
  background:{G['ink']['css']};color:{C['text']['inverse']};font:inherit;font-size:16.5px;
  font-variation-settings:'wght' 600;cursor:pointer;box-shadow:{EL['dock']['css']}}}
.cta:active{{transform:scale(.985)}}
.quiet{{height:{RC['buttonQuiet']['height']}px;border:0;border-radius:{R['full']}px;
  background:{RC['buttonQuiet']['background']};color:{RC['buttonQuiet']['color']};
  font:inherit;font-size:16.5px;font-variation-settings:'wght' 600;cursor:pointer;
  box-shadow:{EL['control']['css']}}}
.quiet:active{{transform:scale(.985)}}
.dots{{display:flex;gap:6px;justify-content:center;margin-bottom:6px}}
.dots i{{width:6px;height:6px;border-radius:99px;background:{C['border']['hairline']}}}
.dots i.on{{background:{C['text']['primary']};width:18px}}

"""

# Motion gate 2. Exported separately so a document composing this file's CSS
# with another's emits the block once.
CSS_REDUCE = """
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.01ms !important;transition-duration:.01ms !important}
}
"""

CSS = CSS_CHROME + CSS_SCREENS + CSS_REDUCE

JS = """
const scrs=[...document.querySelectorAll('.scr')], rail=[...document.querySelectorAll('.rail__i')];
const noteEl=document.getElementById('note');
function show(id){
  scrs.forEach(s=>s.toggleAttribute('data-on', s.dataset.scr===id));
  rail.forEach(b=>b.setAttribute('aria-current', String(b.dataset.to===id)));
  const s=scrs.find(x=>x.dataset.scr===id);
  if(s){ s.querySelector('.body').scrollTop=0; noteEl.innerHTML=s.dataset.note; }
}
document.addEventListener('click',e=>{
  const g=e.target.closest('[data-go]'); if(g){ show(g.dataset.go); return; }
  const j=e.target.closest('.rail__i'); if(j){ show(j.dataset.to); return; }
  const c=e.target.closest('.sel'); if(c && !c.dataset.go){
    c.parentNode.querySelectorAll('.sel').forEach(x=>x.classList.remove('sel--on'));
    c.classList.add('sel--on'); }
  const ch=e.target.closest('.chip'); if(ch){
    ch.parentNode.querySelectorAll('.chip').forEach(x=>{
      x.classList.remove('chip--on'); x.classList.add('chip--off'); });
    ch.classList.remove('chip--off'); ch.classList.add('chip--on'); }
});
show('A2');
"""


def build():
    rail = "".join(
        '<button class="rail__i" data-to="%s"><span class="rail__n">%s</span>%s</button>'
        % (s["id"], s["id"], s["label"]) for s in SCREENS
    )
    body = "".join(
        '<div class="scr" data-scr="%s" data-note="%s">%s<div class="body">%s</div>%s</div>'
        % (s["id"], s["note"].replace('"', "&quot;"), status_bar(), s["body"],
           FOOTERS.get(s["id"], ""))
        for s in SCREENS
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>NOMA — Onboarding</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style></head><body>
  <div class="rail">
    <div class="rail__b">NOMA · First run</div>
    {rail}
    <p class="note" id="note"></p>
  </div>
  <div class="stage">
    <div class="phone"><div class="notch"></div>{body}<div class="hbar"></div></div>
  </div>
<script>{JS}</script>
<script>{FIT_JS}
/* body already carries 32px of padding, so the stage is the usable box. */
watchPhoneFit({{padY: 16, padX: 16}});</script></body></html>"""
    OUT.write_text(html, encoding="utf-8")
    print("wrote %s (%d screens, %d KB)"
          % (OUT.relative_to(ROOT), len(SCREENS), len(html) // 1024))


if __name__ == "__main__":
    build()
