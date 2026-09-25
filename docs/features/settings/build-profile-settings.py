#!/usr/bin/env python3
"""
Build docs/features/settings/profile-settings-prototype.html

THE HOME / APP settings — reached from the profile avatar. Scope: the whole
home and the account behind it. One purifier's own settings are a different
surface entirely; see build-device-settings.py.

    python3 docs/features/settings/build-profile-settings.py

WHY THE TWO ARE SEPARATE, since it is the thing most likely to get merged by
mistake: everything here is true of the HOME (who's in it, what rooms exist,
how the app behaves, what the account is). Everything on the device surface is
true of ONE PURIFIER (its fan mode, its filter, its firmware). The rows that
look like they belong to both — Notifications is the obvious one — are
genuinely different settings: here it is "what does this app send my phone",
there it is "what does this purifier raise alerts about". Merging them makes
one of the two lie.

STRUCTURE — rebuilt 2026-08-12 (2) to the owner's second reference capture,
which is materially different from the first and supersedes it:

    back · Settings · Help
    centred avatar · name + edit · place
    DEVICES        one card per device — thumbnail, state, connection, toggle
    IN THIS HOME   ONE card split in two: the owner | the household
    HOME / APP / PRIVACY & DATA
    (unlabelled)   Help & support · About NOMA
    (unlabelled)   Sign out · Remove this home

The previous version led with an "Ruhaan's Home" `<h1>` and a horizontal
identity card carrying the owner, place, device count and avatars. Both are
gone — the avatar is now the header, and the identity card's two jobs split
into the DEVICES cards and the two-up IN THIS HOME card. Every row below
those was already an exact match and is untouched.

COLOURS vs THE REFERENCE — two of the four gaps closed 2026-08-13, when the
owner supplied a negative red:

    "Offline"            red   → RED ✅        status.negative.text #A03B3B
    "Remove this home"   red   → RED ✅        _kit.DANGER, same token
    device thumbnail     blue  → grey  ⚠      .th--a — blue is still not in
                                               the palette
    owner's crown        gold  → grey  ⚠      .crown — nor is gold

Note both reds render as #A03B3B, NOT the supplied #F38E8E. The anchor is a
light surface colour (2.09:1 as text); the deep shade is the text one. See
the `red` primitive in design.tokens.js for the measurements.

Legal and unchanged: "Online" is green TEXT (`text.accent`, the documented
LAW 2 exception) and the on-toggle is `gradients.accentRamp`, a ramp rather
than a flat green.

Sectioning and the state-on-the-right pattern follow the same competitive
research as the device surface (Google Home's identity header, SmartThings'
inline values).

Chrome, tokens and the danger-red rationale live in _kit.py.

⚠ C-1 is still open — personas are unresolved, so the member names below are
placeholders, not a roster anyone has agreed to. The ROLES are real: owner /
adult / guest, with guests scopeable to single devices, is what the sharing
flow in the PM prototype implements.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _kit as K  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "profile-settings-prototype.html"

HOME = {"name": "Ruhaan's Home", "owner": "Ruhaan", "place": "Gurugram",
        "initials": "RR", "devices": 2, "people": 3}

# ⚠ Roster transcribed from the owner's 2026-08-14 Family reference: THREE
# people, not four. Vikram is renamed Vicky and demoted to Guest; Sunita is
# gone. HOME["people"] follows so the root screen's count agrees with the
# list it links to.
#
# ⚠ `tone` picks the avatar tint, and the reference uses PINK and BLUE. Both
# are outside the 2026-08-12 palette rule (white, grey, the two greens only).
# Rendered as supplied rather than silently greened, because the owner drew
# them that way, but flagged: this is the same palette question the device
# thumbnails and the crown raised, and it is still an owner call.
MEMBERS = [
    {"in": "RR", "n": "Ruhaan", "role": "Owner", "s": "You · full access", "tone": "a"},
    {"in": "AK", "n": "Aarti",  "role": "Adult", "s": "All devices",       "tone": "b"},
    {"in": "VK", "n": "Vicky",  "role": "Guest", "s": "Air purifier only", "tone": "c"},
]

# The two devices as CARDS at the top of the page, which is what the owner's
# 2026-08-12 reference leads with — distinct from the DEVICES list further
# down, which is the by-room drill-down on its own screen.
#
# `tone` picks a thumbnail gradient. ⚠ The reference gives the first device a
# BLUE thumbnail; blue is not in the 2026-08-12 palette (white, grey, and the
# two greens only), so this is grey. Same compromise, same reason, as the
# household avatars below.
DEVICE_CARDS = [
    {"n": "Bedroom Air", "state": "Cleaning", "conn": "Online",  "on": True,  "tone": "a"},
    {"n": "Living room", "state": "Idle",     "conn": "Offline", "on": False, "tone": "b"},
]

# Derived, never restated: this row read "4 people" while the Family screen
# listed three, because the count was typed in two places. M-17 also applies —
# the singular has to exist rather than reading "1 people".
PEOPLE_V = "%d %s" % (len(MEMBERS), "person" if len(MEMBERS) == 1 else "people")

# Section order and every label/value here is transcribed from the owner's
# reference screen. Home / App / Privacy & data matched it already.
SECTIONS = [
    ("Home", [
        {"i": "home",    "t": "Rooms & devices", "v": "2 devices", "go": "devices"},
        {"i": "people",  "t": "Family & access", "v": PEOPLE_V,     "go": "family"},
        {"i": "clock",   "t": "Automations",     "v": "3 active"},
    ]),
    ("App", [
        {"i": "bell",    "t": "Notifications", "v": "On",      "go": "notifications"},
        {"i": "palette", "t": "Appearance",    "v": "Light",   "go": "appearance"},
        {"i": "globe",   "t": "Language",      "v": "English"},
        {"i": "access",  "t": "Accessibility"},
    ]),
    ("Privacy & data", [
        {"i": "shield",  "t": "Privacy controls"},
        {"i": "link",    "t": "Connected services", "v": "2 linked"},
    ]),
]

# ⚠ PARKED, NOT DELETED. "Across your devices" (filter life, air-quality
# alerts, firmware) sat between Home and App until the 2026-08-12 reference,
# which does not have it. Kept here rather than dropped so three real settings
# don't vanish in a layout change — but nothing renders it now, so they are
# currently unreachable from this surface. Either fold them into the device
# cards above, or give them back a section. Owner's call.
PARKED_SECTIONS = [
    ("Across your devices", [
        {"i": "filter",  "t": "Filter life",         "meter": 0.23},
        {"i": "wind",    "t": "Air alerts",  "v": "On"},
        {"i": "chip",    "t": "Firmware",            "v": "Up to date", "dot": True},
    ]),
]

FOOTER = [
    {"i": "help", "t": "Help & support"},
    {"i": "info", "t": "About NOMA", "v": "v1.0.4"},
]

NOTIF_MASTER = {"t": "Allow notifications", "s": "Turn everything off in one place.",
                "kind": "toggle", "on": True}

NOTIF = [
    ("Your devices", [
        {"t": "When the air turns",    "s": "I'll tell you when PM2.5 climbs into the unhealthy range.", "kind": "toggle", "on": True},
        {"t": "Filter needs changing", "s": "At 10% life remaining",      "kind": "toggle", "on": False},
        {"t": "Device goes offline",   "s": "Lost power or Wi-Fi",        "kind": "toggle", "on": False},
    ]),
    ("Security", [
        {"t": "Door unlocked", "s": "Every unlock",     "kind": "toggle", "on": True},
        {"t": "Camera motion", "s": "Can be frequent", "kind": "toggle", "on": True},
    ]),
    ("Household", [
        {"t": "Someone joins", "s": "A new person accepts an invite", "kind": "toggle", "on": True},
        {"t": "Product news",  "s": "Occasional. Never more than monthly.", "kind": "toggle", "on": False},
    ]),
]

DEVICES = [
    ("Living room", [
        {"t": "Air Pro 500", "s": "Online · cleaning", "v": "73 µg/m³", "dot": True},
    ]),
    ("Bedroom", [
        {"t": "Air Pro 200", "s": "Online · idle", "v": "41 µg/m³", "dot": True},
    ]),
]

CROWN = ('<svg width="15" height="11" viewBox="0 0 15 11" fill="currentColor">'
         '<path d="M1 9.6h13L12.7 2.6 9.8 5 7.5 1 5.2 5 2.3 2.6z"/></svg>')

EDIT = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M4.5 19.5h4L19 9a2.5 2.5 0 0 0-3.5-3.5L5 16z"/><path d="M14.5 6.5 17.5 9.5"/>'
        '</svg>')

# A purifier tower, flat. Deliberately not an emoji or a photo — the owner's
# standing instruction on the nav bar was flat icons, and it applies here too.
PURIFIER = ('<svg width="24" height="32" viewBox="0 0 24 32" fill="none">'
            '<rect x="3" y="1.5" width="18" height="29" rx="7" fill="#FFFFFF" opacity=".96"/>'
            '<path d="M8 10.5h8M8 14.5h8M8 18.5h8" stroke="%s" stroke-width="1.6" '
            'stroke-linecap="round"/></svg>') % K.N['300']

EXTRA_CSS = f"""
/* ---------- centred profile header ---------- */
.prof{{display:flex;flex-direction:column;align-items:center;padding:2px 0 6px}}
.prof__av{{width:104px;height:104px;border-radius:{K.R['full']}px;display:grid;
  place-items:center;font-size:29px;font-variation-settings:'wght' 700;
  color:{K.N['400']};background:linear-gradient(158deg,{K.N['500']},{K.N['700']});
  box-shadow:{K.EL['card']['css']}}}
.prof__n{{display:flex;align-items:center;gap:6px;margin-top:15px;font-size:26px;
  font-variation-settings:'opsz' 26,'wght' 700;letter-spacing:-.5px}}
.prof__edit{{border:0;background:none;padding:1px;margin:0;line-height:0;cursor:pointer;
  color:{K.C['icon']['tertiary']}}}
.prof__edit:active{{transform:scale(.9)}}
.prof__p{{font-size:14px;color:{K.C['text']['secondary']};margin-top:3px}}

/* ---------- device cards ---------- */
.dev{{display:flex;align-items:center;gap:12px;
  background:{K.C['surface']['raised']};border-radius:{K.R['xl']}px;
  box-shadow:{K.EL['card']['css']};padding:13px {K.LAY['cardPaddingX']}px}}
.dev + .dev{{margin-top:10px}}
/* The tappable region — everything but the toggle. See device_card(). */
.dev__hit{{display:flex;align-items:center;gap:14px;flex:1;min-width:0;border:0;
  background:none;font:inherit;text-align:left;cursor:pointer;padding:0}}
.dev__hit:active{{opacity:.6}}
.dev__th{{width:58px;height:58px;border-radius:16px;flex:none;display:grid;
  place-items:center;box-shadow:inset 0 0 0 1px rgba(255,255,255,.6)}}
.dev__c{{display:flex;flex-direction:column;flex:1;min-width:0}}
.dev__n{{font-size:17px;font-variation-settings:'wght' 700;letter-spacing:-.2px}}
.dev__s{{font-size:13.5px;color:{K.C['text']['secondary']};margin-top:2px}}
/* Green TEXT is the one documented exception to LAW 2 — a gradient-clipped
   glyph cannot hold a contrast ratio, so `text.accent` is a flat value. */
.dev__on{{color:{K.C['text']['accent']};font-variation-settings:'wght' 600}}
/* Offline is red again as of 2026-08-13 — the owner supplied a negative red,
   so `colors.status` is populated. This is `status.negative.text` (#A03B3B),
   not the #F38E8E anchor: the anchor measures 2.09:1 as text and would be
   unreadable. A device that has dropped off the network is genuinely a fault,
   so `negative` is the right family rather than a muted grey. */
.dev__off{{color:{K.NEGATIVE['text']};font-variation-settings:'wght' 600}}
.th--a{{background:linear-gradient(150deg,{K.N['100']},{K.N['300']})}}
.th--b{{background:linear-gradient(150deg,{K.T['green']['haze']},{K.T['green']['mint']}88)}}

/* ---------- "in this home": one card, two halves ---------- */
.home2{{display:flex;align-items:stretch;background:{K.C['surface']['raised']};
  border-radius:{K.R['xl']}px;box-shadow:{K.EL['card']['css']}}}
/* Two halves inside ~353px means each gets ~176px. The padding is TIGHTER
   than cardPaddingX (24) on purpose: at 24 the right half ran out of room and
   "4 People" wrapped onto two lines. 14 + a tighter avatar overlap buys back
   the ~30px that costs. */
.home2__h{{flex:1;display:flex;align-items:center;gap:9px;min-width:0;border:0;
  background:none;font:inherit;text-align:left;cursor:pointer;padding:15px 14px}}
.home2__h:active{{opacity:.6}}
.home2__d{{width:1px;flex:none;background:{K.C['border']['subtle']};margin:15px 0}}
.home2__c{{display:flex;flex-direction:column;min-width:0}}
.home2__n{{font-size:15px;font-variation-settings:'wght' 700;letter-spacing:-.1px;
  white-space:nowrap}}
.home2__s{{font-size:12.5px;color:{K.C['text']['secondary']};margin-top:3px;
  white-space:nowrap}}
.home2__chev{{margin-left:auto;flex:none;color:{K.C['icon']['tertiary']}}}
/* Decorative discs, no initials. At 20px an initial is not legible, and the
   "4 People" beside them already carries the count — so they read as a
   cluster of people rather than pretending to be identifiable. Matches the
   reference, which uses silhouettes here, not letters. */
.home2__avs{{display:flex;flex:none}}
.home2__avs .av{{width:20px;height:20px;margin-right:-7px;
  box-shadow:0 0 0 2px {K.N['0']}}}
.home2__avs .av:last-child{{margin-right:0}}
.avwrap{{position:relative;flex:none;line-height:0}}
/* ⚠ The reference's crown is gold. Gold is not in the palette either, so it
   is grey — and the "Owner" pill beside it is now carrying the meaning. */
.crown{{position:absolute;top:-6px;left:50%;transform:translateX(-50%);
  color:{K.C['icon']['tertiary']};line-height:0}}
.ident{{display:flex;align-items:center;gap:14px;width:100%;border:0;text-align:left;
  font:inherit;cursor:pointer;margin-top:14px;position:relative;
  background:{K.C['surface']['raised']};border-radius:{K.R['xl']}px;
  box-shadow:{K.EL['card']['css']};padding:20px {K.LAY['cardPaddingX']}px}}
.ident__who{{display:flex;flex-direction:column}}
.ident__n{{font-size:17px;font-variation-settings:'wght' 700;letter-spacing:-.2px}}
.ident__p{{font-size:13.5px;color:{K.C['text']['secondary']};margin-top:1px}}
.ident__div{{width:1px;align-self:stretch;background:{K.C['border']['subtle']};
  margin:2px 4px 2px auto}}
.ident__stat{{display:flex;flex-direction:column;align-items:flex-start;gap:1px;width:104px}}
.ident__big{{font-size:20px;font-variation-settings:'wght' 700;line-height:1.1}}
.ident__cap{{font-size:11.5px;color:{K.C['text']['secondary']}}}
.ident__avs{{display:flex;margin:7px 0 3px}}
.ident__avs .av{{margin-right:-8px;box-shadow:0 0 0 2px {K.N['0']}}}
.ident__chev{{position:absolute;right:14px;top:16px;color:{K.C['icon']['tertiary']}}}
.av{{width:46px;height:46px;border-radius:{K.R['full']}px;flex:none;display:grid;
  place-items:center;font-size:15px;font-variation-settings:'wght' 700;
  color:{K.C['text']['secondary']};background:{K.N['150']}}}
.av--sm{{width:22px;height:22px;font-size:8.5px}}
/* ⚠ AVATAR TINTS ARE BACK TO REAL HUES, per the owner's 2026-08-14 Family
   reference: dark grey for the owner, PINK, BLUE. An earlier pass had greened
   these to obey the palette rule (white, grey, the two greens only) and noted
   at the time that it was a weaker signal, because hue is how every app tells
   people apart at a glance. The reference overrides that.
   Still the open palette question, now with a third instance behind it (the
   device thumbnail and the owner's crown were the first two). Not resolved
   here: rendered as drawn, flagged as a standing owner call. */
.av--a{{background:linear-gradient(150deg,#6E6E6C,#4A4A48);color:{K.N['0']}}}
.av--b{{background:linear-gradient(150deg,#F79FC4,#EE7FAE);color:{K.N['0']}}}
.av--c{{background:linear-gradient(150deg,#8FB4F5,#6E93E8);color:{K.N['0']}}}
.row--mem{{gap:13px}}
.row--mem + .row--mem::before{{left:72px}}

/* ---- Family: owner raised out of a sunken group ------------------------
   The reference floats the owner's row as a white card inside a grey
   container holding everyone else. That is LAW 3 doing real work: the owner
   is distinguished by lift, not by a label or a colour. */
.fam{{background:{K.C['surface']['sunken']};border-radius:{K.R['xl']}px;
  padding:6px;margin-top:2px}}
.fam__own{{background:{K.C['surface']['raised']};border-radius:{K.R['lg']}px;
  box-shadow:{K.EL['card']['css']},{K.G['gloss']['css']};margin-bottom:6px}}
.fam__own .row--mem::before{{display:none}}
.fam > .row--mem:first-of-type::before{{display:none}}
.mem__n{{font-size:15px;font-variation-settings:'wght' 600;display:flex;
  align-items:center;gap:8px}}
.badge{{font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;
  font-variation-settings:'wght' 700;color:{K.C['text']['tertiary']};
  background:{K.N['150']};border-radius:{K.R['full']}px;padding:3px 8px}}
.badge--own{{color:{K.C['text']['inverse']};background:{K.C['surface']['inverse']}}}
.roles__r{{display:flex;flex-direction:column;padding:9px 0}}
.roles__r + .roles__r{{border-top:1px solid {K.C['border']['subtle']}}}
.roles__r b{{font-size:14px;font-variation-settings:'wght' 700}}
.roles__r span{{font-size:13px;line-height:18px;color:{K.C['text']['secondary']};margin-top:2px}}
.pv__k{{display:flex;align-items:center;gap:7px;font-size:12px;letter-spacing:.06em;
  text-transform:uppercase;font-variation-settings:'wght' 600;color:{K.C['text']['secondary']}}}
.pv__h{{font-size:20px;font-variation-settings:'opsz' 20,'wght' 600;letter-spacing:-.2px;
  margin-top:10px}}
.pv__s{{font-size:13.5px;color:{K.C['text']['secondary']};margin-top:5px}}
"""


def device_card(d):
    """A device card: thumbnail, name, state · connection, toggle.

    The card is a DIV, not a button, and the tappable area is an inner button.
    A <button> cannot contain another <button> — the toggle gets hoisted out of
    it by the parser and lands outside the card. `_kit.row` dodges the same
    trap by switching its tag to a div whenever it carries a control; this
    follows that.
    """
    conn_cls = "dev__on" if d["conn"] == "Online" else "dev__off"
    return f"""
        <div class="dev">
          <button class="dev__hit">
            <span class="dev__th th--{d['tone']}">{PURIFIER}</span>
            <span class="dev__c">
              <span class="dev__n">{d['n']}</span>
              <span class="dev__s">{d['state']} &nbsp;·&nbsp;
                <span class="{conn_cls}">{d['conn']}</span></span>
            </span>
          </button>
          {K.toggle(d['on'], d['n'])}
        </div>"""


def screen_root():
    """The owner's 2026-08-12 reference structure, top to bottom:

      back · Settings · Help
      centred avatar, name + edit, place
      DEVICES        — one card per device: thumbnail, state, connection, toggle
      IN THIS HOME   — ONE card split in two: the owner | the household
      HOME / APP / PRIVACY & DATA
      (unlabelled)   — Help & support, About NOMA
      (unlabelled)   — Sign out, Remove this home

    Replaces the previous "Ruhaan's Home" heading + horizontal identity card.
    Same rows underneath; the header and the top two groups are new.
    """
    # Decorative — see .home2__avs. Empty and aria-hidden so a screen reader
    # gets "Family, 4 People" rather than four unlabelled blobs.
    fam_avatars = "".join('<span class="av av--%s" aria-hidden="true"></span>' % m["tone"]
                          for m in MEMBERS)
    owner = MEMBERS[0]
    body = "".join(K.section(l, r) for l, r in SECTIONS)
    devices = "".join(device_card(d) for d in DEVICE_CARDS)

    return f"""
    <div class="scr" data-scr="root">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Settings", back=True, help_link=True)}

        <div class="prof">
          <span class="prof__av">{HOME['initials']}</span>
          <span class="prof__n">{HOME['owner']}
            <button class="prof__edit" aria-label="Edit name">{EDIT}</button></span>
          <span class="prof__p">{HOME['place']}</span>
        </div>

        <div class="lbl">Devices</div>
        {devices}

        <div class="lbl">In this home</div>
        <div class="home2">
          <button class="home2__h" data-go="family">
            <span class="avwrap">
              <span class="crown">{CROWN}</span>
              <span class="av av--{owner['tone']}">{owner['in']}</span>
            </span>
            <span class="home2__c">
              <span class="home2__n">{owner['n']}</span>
              <span class="badge badge--own">{owner['role']}</span>
            </span>
          </button>
          <span class="home2__d"></span>
          <button class="home2__h" data-go="family">
            <span class="home2__avs">{fam_avatars}</span>
            <span class="home2__c">
              <span class="home2__n">Family</span>
              <span class="home2__s">{HOME['people']} {'person' if HOME['people'] == 1 else 'people'}</span>
            </span>
            <span class="home2__chev">{K.ico("chev", 16)}</span>
          </button>
        </div>

        {body}
        <div class="lbl">&nbsp;</div>
        <div class="card">{"".join(K.row(r) for r in FOOTER)}</div>
        <div class="card">
          {K.row({"i": "signout", "t": "Sign out", "kind": "plain"})}
          {K.row({"i": "trash", "t": "Remove this home", "kind": "danger"})}
        </div>
        {K.note("Removing a home unpairs every device in it and deletes its history for "
                "everyone. The devices keep working. They just stop being yours.")}
        <div class="pad"></div>
      </div>
    </div>"""


def screen_family():
    """⚠ The reference drops the "What each role can do" explainer card and the
    8-people note that used to sit under the CTA. Both are gone here to match
    it. That is a real loss on a screen whose rows carry Owner/Adult/Guest
    badges and now explain them nowhere, so it is flagged rather than quietly
    accepted: if the roles need explaining, they want a disclosure on the
    member detail screen rather than a permanent block on this one."""
    def mem(m):
        badge = '<span class="badge%s">%s</span>' % (
            " badge--own" if m["role"] == "Owner" else "", m["role"])
        return ('<button class="row row--mem"><span class="av av--%s">%s</span>'
                '<span class="row__c"><span class="mem__n">%s%s</span>'
                '<span class="row__s">%s</span></span>'
                '<span class="row__ic">%s</span></button>'
                % (m["tone"], m["in"], m["n"], badge, m["s"], K.ico("chev", 16)))

    owner, rest = MEMBERS[0], MEMBERS[1:]
    return f"""
    <div class="scr" data-scr="family">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Family")}
        {K.page_header("family", "here",
                       "Everyone here can see and control the devices they've been "
                       "given. Only the owner can add or remove people.",
                       title_lead="%d people" % len(MEMBERS))}
        <div class="fam">
          <div class="fam__own">{mem(owner)}</div>
          {"".join(mem(m) for m in rest)}
        </div>
        <button class="cta">Invite someone</button>
        <div class="pad"></div>
      </div>
    </div>"""


def screen_devices():
    body = "".join(K.section(l, r) for l, r in DEVICES)
    n_dev = sum(len(r) for _, r in DEVICES)
    return f"""
    <div class="scr" data-scr="devices">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Rooms & devices")}
        {K.page_header("rooms", "in %d rooms" % len(DEVICES),
                       "Tap a device to open its own settings. Fan mode, filter, "
                       "firmware and the rest live there, not here.",
                       title_lead="%d device%s" % (n_dev, "" if n_dev == 1 else "s"))}
        {body}
        <button class="cta">{K.ico("plus", 18)}<span>Add a device</span></button>
        {K.note("Rooms are just labels. Moving a device between them changes nothing "
                "except where it appears and which outdoor reading it compares against.")}
        <div class="pad"></div>
      </div>
    </div>"""


def screen_notifications():
    body = "".join(K.section(l, r) for l, r in NOTIF)
    return f"""
    <div class="scr" data-scr="notifications">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Notifications")}
        {K.page_header("notifications", "App notifications",
                       "The app sends these to your phone. What each purifier "
                       "raises an alert about lives in that device's own settings.")}
        <div class="card">{K.row(NOTIF_MASTER)}</div>
        {body}
        <div class="lbl">Quiet hours</div>
        <div class="card">
          {K.row({"t": "Hold the quieter alerts", "s": "Security alerts still come through.",
                  "kind": "toggle", "on": True})}
          {K.row({"t": "Between", "v": "10:00 PM – 7:00 AM"})}
        </div>
        <div class="pad"></div>
      </div>
    </div>"""


def screen_appearance():
    themes = [("Light", True, False), ("Dark", False, True), ("Automatic", False, True)]
    chips = "".join(
        '<button class="chip %s"%s>%s%s</button>'
        % ("chip--on" if on else "chip--off", ' disabled title="Not built yet"' if off else "",
           K.ico("check", 15) if on else "", t)
        for t, on, off in themes)
    # Reference's four steps, replacing Small/Default/Large/Larger.
    sizes = "".join('<button class="chip %s">%s%s</button>'
                    % ("chip--on" if s == "Default" else "chip--off",
                       K.ico("check", 15) if s == "Default" else "", s)
                    for s in ["Small", "Default", "Medium", "Large"])
    return f"""
    <div class="scr" data-scr="appearance">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Appearance")}
        {K.page_header("appearance", "Appearance",
                       "Change the theme and text size of the app. This does not "
                       "affect your phone's own settings, just this one.")}
        <div class="lbl">Theme</div>
        <div class="chips">{chips}</div>
        <div class="lbl">Text size</div>
        <div class="chips">{sizes}</div>
        <div class="lbl">Preview</div>
        <div class="card card--pad">
          <div class="pv__h">Everything looks fine at home</div>
          <div class="pv__s">Air quality good · 2 devices online</div>
        </div>
        {K.note("Text size follows your phone's setting by default. Changing it here "
                "affects this app only. Dark and Automatic can't be picked yet: no dark "
                "values exist, so offering them would be a lie. Tracked as O-3.")}
        <div class="pad"></div>
      </div>
    </div>"""


def build():
    html = K.page(
        "NOMA — Profile settings", "NOMA · Home settings",
        [("root", "Ruhaan's Home"), ("family", "Family & access"),
         ("devices", "Rooms & devices"), ("notifications", "Notifications"),
         ("appearance", "Appearance")],
        [screen_root(), screen_family(), screen_devices(),
         screen_notifications(), screen_appearance()],
        extra_css=EXTRA_CSS,
        note_html="The whole home and the account. Reached from the profile avatar.",
    )
    OUT.write_text(html, encoding="utf-8")
    n = sum(len(r) for _, r in SECTIONS) + len(FOOTER) + 2
    print("wrote %s (5 screens, %d root rows, %d KB)"
          % (OUT.relative_to(K.ROOT), n, len(html) // 1024))


if __name__ == "__main__":
    build()
