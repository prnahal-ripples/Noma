#!/usr/bin/env python3
"""
Build docs/features/settings/device-settings-prototype.html

ONE PURIFIER'S settings — reached from the gear inside a device. Scope: this
device only. The app/home settings are a different surface entirely; see
build-profile-settings.py.

    python3 docs/features/settings/build-device-settings.py

THE IA IS NOT MINE. Every section, row, sub-label and default state is
transcribed from `PurSettingsBody` in the owner's PM prototype —
"Ding App - White & Blue Launch V2 (Fixed, Standalone).html", one of the four
sources credited in src/hardware/devices.json. Six sections, seventeen rows,
in that order. Do not reorder or reword without the source.

DELIBERATELY NOT HERE: family sharing, home name, rooms, app appearance,
account. Those are home-scoped, they live on the profile settings surface, and
the source prototype keeps them separate too.

Chrome, tokens and the danger-red rationale live in _kit.py.

TWO VISUAL DEVIATIONS FROM THE SOURCE, BOTH FLAGGED IN _kit.py OR BELOW:
  · segmented controls LIFT rather than filling with ink (LAW 3)
  · toggles use gradients.accentRamp rather than a flat fill (LAW 2)

The source resolves every chevron row to a toast. Two are built out as real
screens — Filter management and Device info — because they are the two that
obviously own content, and a settings page with no reachable child cannot
show whether the pattern scales.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _kit as K  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "device-settings-prototype.html"

DEVICE = "Air Pro 500"
FIRMWARE = "FW 2.4.1"
FILTER_PCT = 23  # header lead and meter fill both read this, so they can't drift

SECTIONS = [
    ("Performance", [
        {"t": "QSensAI", "s": "AI auto-tunes fan to live air quality",
         "kind": "toggle", "on": True},
        {"t": "Auto mode", "s": "Adjusts fan to live air quality"},
        {"t": "Silent mode", "s": "Mutes all device sounds",
         "kind": "toggle", "on": False},
        {"t": "Light intensity", "s": "Display &amp; ring brightness",
         "kind": "seg", "opts": ["Off", "Low", "High"], "at": "High"},
    ]),
    ("Maintenance &amp; monitoring", [
        {"t": "Filter management", "s": "View remaining filter life or reset it",
         "go": "filter"},
        {"t": "Continuous monitoring", "s": "Monitor air quality when machine is off",
         "kind": "toggle", "on": True},
        {"t": "Temperature unit", "kind": "seg", "opts": ["°C", "°F"], "at": "°C"},
    ]),
    ("Alerts", [
        {"t": "Notifications", "s": "Air spikes, filter &amp; reminders",
         "kind": "toggle", "on": True},
        {"t": "Monthly report", "s": "Emailed on the 1st"},
    ]),
    ("Connection", [
        {"t": "Change Wi-Fi network", "s": "Asha_Home_5G · Strong"},
        {"t": "Voice control", "s": "Alexa, Google Assistant"},
        {"t": "Works with Alexa", "s": "Enabled", "kind": "toggle", "on": True},
        {"t": "Firmware update", "s": "%s · Up to date" % FIRMWARE, "dot": True},
    ]),
    ("Location", [
        {"t": "Time zone", "s": "Asia/Kolkata (UTC+05:30)"},
        {"t": "City / town", "s": "Bengaluru"},
    ]),
    ("Device", [
        {"t": "Device info", "s": "%s · %s" % (DEVICE, FIRMWARE), "go": "info"},
        {"t": "Restart device", "s": "Power-cycle the purifier", "kind": "restart"},
        {"t": "Remove device", "kind": "danger"},
    ]),
]

EXTRA_CSS = f"""
.hero{{display:flex;align-items:center;gap:14px;background:{K.C['surface']['raised']};
  border-radius:{K.R['xl']}px;box-shadow:{K.EL['card']['css']};
  padding:16px {K.LAY['cardPaddingX']}px;margin-bottom:4px}}
.hero__th{{width:52px;height:52px;border-radius:{K.R['sm']}px;flex:none;
  background:{K.G['accentRamp']['css']}}}
.hero__c{{display:flex;flex-direction:column}}
.hero__n{{font-size:17px;font-variation-settings:'wght' 700;letter-spacing:-.2px}}
.hero__s{{font-size:13px;color:{K.C['text']['secondary']};margin-top:3px;
  display:flex;align-items:center;gap:7px}}
/* The big "23%" that used to live here is now the page header's title lead,
   so the card is just the meter and its two captions. */
.fm__row{{display:flex;justify-content:space-between;font-size:12.5px;
  color:{K.C['text']['secondary']};margin-top:10px}}
"""


def screen_root():
    body = "".join(K.section(l, r) for l, r in SECTIONS)
    return f"""
    <div class="scr" data-scr="root">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Settings", back=True)}
        <div class="hero">
          <span class="hero__th"></span>
          <span class="hero__c"><span class="hero__n">{DEVICE}</span>
            <span class="hero__s"><span class="dot"></span>Online · Living room</span></span>
        </div>
        {body}
        {K.note("Removing a device unpairs it from this home and deletes its history "
                "for everyone. The purifier keeps working on its own controls. It just "
                "stops being part of your home.")}
        <div class="pad"></div>
      </div>
    </div>"""


def screen_filter():
    return f"""
    <div class="scr" data-scr="filter">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Filter management")}
        {K.page_header("filter", "life left",
                       "Life is estimated from run hours and the air this purifier "
                       "has actually moved, not from a calendar.",
                       title_lead="%d%%" % FILTER_PCT)}
        <div class="card card--pad">
          <div style="margin:2px 0 0">{K.meter(FILTER_PCT / 100, total=20, size="lg")}</div>
          <div class="fm__row"><span>HEPA H13 + carbon</span><span>≈ 6 weeks left</span></div>
        </div>
        {K.section("Filter", [
            {"t": "Order a replacement", "s": "Ships in 2–3 days"},
            {"t": "Reset filter life", "s": "Do this only after fitting a new one"},
            {"t": "How to change it", "s": "90-second walkthrough"},
        ])}
        {K.note("A filter in Delhi in November will not last as long as the same "
                "filter in June.")}
        <div class="pad"></div>
      </div>
    </div>"""


def screen_info():
    rows = [("Model", DEVICE), ("Firmware", FIRMWARE), ("Serial", "DP5-24-0099183"),
            ("MAC address", "A4:C1:38:9F:22:0E"), ("Wi-Fi", "Asha_Home_5G · 2.4 GHz"),
            ("Paired", "11 Aug 2026"), ("Room", "Living room")]
    return f"""
    <div class="scr" data-scr="info">
      {K.status_bar()}
      <div class="body">
        {K.top_bar("Device info")}
        {K.page_header("info", "Device info",
                       "Useful when something needs support. Nothing here leaves "
                       "the device unless you send it.")}
        <div class="card">
          {"".join(K.row({"t": k, "v": v, "kind": "value"}) for k, v in rows)}
        </div>
        <div class="pad"></div>
      </div>
    </div>"""


def build():
    html = K.page(
        "NOMA — Device settings", "NOMA · Device settings",
        [("root", "Settings"), ("filter", "Filter management"), ("info", "Device info")],
        [screen_root(), screen_filter(), screen_info()],
        extra_css=EXTRA_CSS,
        note_html="One purifier. Reached from the gear inside a device.",
    )
    OUT.write_text(html, encoding="utf-8")
    n = sum(len(r) for _, r in SECTIONS)
    print("wrote %s (%d sections, %d rows, %d KB)"
          % (OUT.relative_to(K.ROOT), len(SECTIONS), n, len(html) // 1024))


if __name__ == "__main__":
    build()
