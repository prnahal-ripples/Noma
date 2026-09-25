#!/usr/bin/env python3
"""
Build docs/features/my-home/my-home-prototype.html

The "My Home" page from ding-my-home-prd.md, as a tappable prototype.
Six states, two strata, the report sheet and the notification feed.

    python3 docs/features/my-home/build-home.py

DATA-DRIVEN. The fixture below mirrors the PRD's §7 TypeScript interfaces
one-for-one, and the runtime renders from it — no screen is hard-coded.
Porting to React means replacing the renderers, not the data.

THREE DEVIATIONS FROM THE PRD, ALL DELIBERATE (2026-08-05):

  1. Palette. PRD §11 specifies a dark language (#0c0e12 page, aqua/amber/
     coral accents). This uses the light greyscale direction the owner set
     for the first-run flow — radial gradient, 8% card shadows, black pill
     CTAs. Reason: the user reaches Home straight off the first-run reveal;
     two palettes in one session is a product defect. Flip by swapping the
     token block if the PRD wins.

  2. Band colour. The greyscale system has no semantic colour and
     src/tokens/design.tokens.js still has `colors.status: null` (O-6).
     An air-quality product cannot signal "bad" in grey, and PRD §11
     mandates a band mapping. Four MUTED band colours are introduced here,
     used only on the AQI badge, band dots and meter fills — never on
     chrome, buttons or type. Always paired with a text label (PRD §11
     accessibility). This is the O-6 gap, filled narrowly.

  3. Stack. PRD §11 asks for React + Tailwind. This repo has no app
     scaffold, and every other artefact here is a self-contained HTML
     prototype. Same pattern, but rendered from the typed fixture so the
     React port is mechanical.

ALSO UNRESOLVED: the PRD calls the product "Ding". Everything else in this
repo calls it NOMA. That is C-2 (five competing names), still open. This
file uses NOMA for consistency with the first-run prototype and logs the
PRD's usage as one more data point.
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT  = ROOT / "docs/features/my-home/my-home-prototype.html"
FDIR = ROOT / "src/fonts/google-sans-flex/static"
b64  = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = {k: b64(FDIR / v) for k, v in {
    "REG": "GoogleSansFlex_24pt-Regular.ttf",
    "MED": "GoogleSansFlex_24pt-Medium.ttf",
    "BLD": "GoogleSansFlex_24pt-Bold.ttf"}.items()}

# ─────────────────────────────────────────────────────────── fixture
# Mirrors PRD §7. Every DetectorClass in §4.2 and every CardKind in §4.1
# appears at least once. dayOne omits `humidity` to exercise renormalisation.

def contributors(*rows):
    """rows: (key, label, rawValue, band, weight, subScore)"""
    return [dict(key=k, label=l, rawValue=r, band=b, weight=w, subScore=s)
            for k, l, r, b, w, s in rows]

STATES = {

"dayOne": dict(
  key="dayOne", accent="amber", clock="9:41", deviceCount=1,
  outdoor=dict(aqi=168, category="Unhealthy", ageMinutes=38, stale=False),
  weather=dict(temp="31°", condition="Haze"),
  room=dict(aqi=42, tone="amber", label="Bedroom"),
  score=dict(value=71, confidence="soft", confidenceReason="less than a day of history",
    # NOTE: humidity deliberately absent → weights renormalise, report shows 'unavailable'
    contributors=contributors(
      ("pm25","Particulates","12 µg/m³","good",0.40,0.78),
      ("voc","VOCs","0.41 ppm · slightly high","moderate",0.20,0.58),
      ("noise","Noise","Quiet · 32 dB","good",0.20,0.90),
      ("filter","Filter","New · 100%","good",0.20,1.00))),
  hero=dict(mode="narrative",
    headline="Your purifier is running.", dim="First reading is in.",
    narrative="It's pulling the bedroom down to 42 while the street sits at 168. "
              "Give me one night with the door shut and I'll know this room properly."),
  roomExtras=[],
  agentCards=[
    dict(id="d1-sleep", kind="proposal", detector="onboarding", zone="needsYourCall",
      stratum="agent", statusTag="One question", source="setup",
      title="When do you usually sleep?",
      body="I'll seal the room and run quiet during those hours, and ease back up before you wake. "
           "You can change it any time.",
      actions=[
        dict(id="a1", label="11 pm – 7 am", variant="primary",
             effect=dict(type="toast", message="Sleep window set · 11 pm – 7 am")),
        dict(id="a2", label="Pick different hours", variant="default",
             effect=dict(type="toast", message="Hour picker would open here")),
      ]),
    dict(id="d1-guide", kind="guide", detector="none", zone="worthKnowing",
      stratum="agent", statusTag="2 min read",
      title="Why the first night matters",
      body="A closed door is the only time this room is genuinely mine to measure. "
           "Everything I learn about your air starts there.",
      actions=[dict(id="a3", label="Read", variant="ghost",
                    effect=dict(type="toast", message="Guide would open here"))]),
  ],
  emptySlots=[dict(zone="doneToday",
    copy="Nothing yet. I've only just met this room.")],
  unseenNotifications=1),

"morningRecap": dict(
  key="morningRecap", accent="aqua", clock="7:14", deviceCount=1,
  outdoor=dict(aqi=187, category="Unhealthy", ageMinutes=12, stale=False),
  weather=dict(temp="24°", condition="Smog"),
  room=dict(aqi=22, tone="aqua", label="Bedroom"),
  score=dict(value=91, confidence="full", confidenceReason="sealed overnight",
    contributors=contributors(
      ("pm25","Particulates","6 µg/m³","good",0.35,0.92),
      ("voc","VOCs","0.28 ppm","good",0.15,0.85),
      ("humidity","Humidity","38% · a little dry","moderate",0.20,0.60),
      ("noise","Noise","Quiet · 28 dB","good",0.15,0.95),
      ("filter","Filter","94%","good",0.15,0.94))),
  hero=dict(mode="narrative",
    headline="While you slept, Delhi hit 187.", dim="Your bedroom never went past 24.",
    narrative="Sealed at 11:04 pm. Held under 30 for seven hours and eleven minutes."),
  roomExtras=[
    dict(id="mr-defended", kind="receipt", detector="none", zone="doneToday",
      stratum="room", statusTag="Overnight",
      title="Air defended", body="Outside peaked at <b>187</b>. The room held at <b>24</b>.",
      meta=dict(sparkline="night", outsidePeak="187", roomHeld="24"),
      actions=[dict(id="b1", label="See the night", variant="ghost",
                    effect=dict(type="openReportSegment", segment="night"))]),
    dict(id="mr-streak", kind="receipt", detector="none", zone="doneToday",
      stratum="room", statusTag="Streak",
      title="11 nights under 50 µg/m³", body="Longest run since you set this up."),
    dict(id="mr-rail", kind="receipt", detector="none", zone="doneToday",
      stratum="room", statusTag="Next up",
      title="Coming up", body="",
      meta=dict(rail="1"),
      items=[dict(text="Sleep mode", sub="Tonight, 11 pm", done=False),
             dict(text="Filter check", sub="Friday", done=False),
             dict(text="Pollen season", sub="About 3 weeks", done=False)]),
  ],
  agentCards=[
    dict(id="mr-quiet", kind="receipt", detector="recurringPattern", zone="doneToday",
      stratum="agent", statusTag="Done", source="21 nights",
      title="Ran quiet all night",
      body="Fan capped at 28 dB from 11:04 pm. You didn't hear it, and the room still held.",
      actions=[
        dict(id="c1", label="Do this always", variant="warm",
             effect=dict(type="toAutomation", message="Added to Automation · created by your agent")),
        dict(id="c2", label="Undo", variant="ghost",
             effect=dict(type="toast", message="Reverted · tonight will ask first")),
      ]),
    dict(id="mr-facts", kind="learnedFacts", detector="recurringPattern", zone="learned",
      stratum="agent", statusTag="What I've learned", source="3 weeks in this room",
      title="About this room", body="",
      facts=[
        dict(text="You seal the door around 11 pm", sub="21 of the last 24 nights"),
        dict(text="Mornings spike when the kitchen window opens", sub="Most weekdays, 7–8 am"),
        dict(text="This room recovers in about 18 minutes", sub="From 100 back under 50 µg/m³"),
      ]),
  ],
  emptySlots=[dict(zone="needsYourCall",
    copy="Nothing needs you this morning. I'm watching the 6 pm forecast. "
         "if it turns, I'll ask before dinner.")],
  unseenNotifications=2),

"calmDay": dict(
  key="calmDay", accent="aqua", clock="2:18", deviceCount=1,
  outdoor=dict(aqi=96, category="Moderate", ageMinutes=22, stale=False),
  weather=dict(temp="33°", condition="Hazy sun"),
  room=dict(aqi=31, tone="aqua", label="Bedroom"),
  score=dict(value=84, confidence="soft", confidenceReason="door open since noon",
    contributors=contributors(
      ("pm25","Particulates","8 µg/m³","good",0.35,0.88),
      ("voc","VOCs","0.31 ppm","good",0.15,0.82),
      ("humidity","Humidity","38% · dry","moderate",0.20,0.55),
      ("noise","Noise","Low · 34 dB","good",0.15,0.88),
      ("filter","Filter","62% used","moderate",0.15,0.62))),
  hero=dict(mode="watchlist",
    headline="Nothing needs you.", dim="Here's what I'm watching.",
    watch=[
      dict(when="2:40 pm", text="Outdoor climbing slowly. 96 and rising"),
      dict(when="4:00 pm", text="Cooking usually starts around now"),
      dict(when="6:00 pm", text="Forecast turns. I'll propose a pre-clean if it holds"),
    ]),
  roomExtras=[
    dict(id="cd-blind", kind="blindSpot", detector="none", zone="beyondRoom",
      stratum="room", statusTag="Worth knowing",
      title="I only sense the bedroom",
      body="The rest of the flat is a guess. On fourteen of the last twenty evenings "
           "the bedroom spiked <b>after</b> the kitchen did. I was reacting, not preventing.",
      actions=[dict(id="e1", label="What a second sensor would change", variant="ghost",
                    effect=dict(type="toast", message="Second-sensor case would open here"))]),
  ],
  agentCards=[
    dict(id="cd-power", kind="proposal", detector="energy", zone="needsYourCall",
      stratum="agent", statusTag="From your history", source="14 afternoons",
      title="Your afternoons run clean on their own",
      body="Fourteen afternoons in a row this room stayed under 40 with the fan barely working. "
           "Drop to power saver between 12 and 5: about <b>₹90 a month</b>, and the filter lasts longer.",
      actions=[
        dict(id="f1", label="Do that", variant="primary",
             effect=dict(type="toast", message="Power saver set · 12–5 pm daily")),
        dict(id="f2", label="Show data", variant="default",
             effect=dict(type="openReportSegment", segment="energy")),
        dict(id="f3", label="Not now", variant="ghost", effect=dict(type="dismissCard")),
      ]),
    dict(id="cd-humid", kind="proposal", detector="comfort", zone="comfort",
      stratum="agent", statusTag="Advisory", source="live",
      title="The air's dry today",
      body="38%, below the 40–60 band. I can't add moisture, but I've capped the fan "
           "so it doesn't dry the room further.",
      meta=dict(band="humidity", value="38", low="40", high="60"),
      actions=[
        dict(id="g1", label="Understood", variant="default",
             effect=dict(type="dismissCard")),
        dict(id="g2", label="Why this?", variant="ghost",
             effect=dict(type="openReport")),
      ]),
    dict(id="cd-guide", kind="guide", detector="none", zone="worthKnowing",
      stratum="agent", statusTag="3 min read",
      title="What the outdoor AQI actually measures",
      body="It's a scale, not a quantity, and it hides which pollutant is driving it. "
           "Here's how to read yours.",
      actions=[dict(id="h1", label="Read", variant="ghost",
                    effect=dict(type="toast", message="Guide would open here"))]),
  ],
  emptySlots=[dict(zone="doneToday",
    copy="Nothing done yet today. Power saver hasn't run. You haven't said yes to it.")],
  unseenNotifications=2),

"eveningPlan": dict(
  key="eveningPlan", accent="aqua", clock="6:42", deviceCount=1,
  outdoor=dict(aqi=142, category="Unhealthy", ageMinutes=8, stale=False),
  weather=dict(temp="27°", condition="Smog"),
  room=dict(aqi=28, tone="aqua", label="Bedroom"),
  score=dict(value=88, confidence="full", confidenceReason="sealing at 11 pm",
    contributors=contributors(
      ("pm25","Particulates","7 µg/m³","good",0.35,0.90),
      ("voc","VOCs","0.29 ppm","good",0.15,0.84),
      ("humidity","Humidity","44% · in band","good",0.20,0.92),
      ("noise","Noise","Low · 33 dB","good",0.15,0.89),
      ("filter","Filter","62% used","moderate",0.15,0.62))),
  hero=dict(mode="watchlist",
    headline="Tonight's plan.", dim="Nothing runs without your say-so.",
    watch=[
      dict(when="8:30 pm", text="Pre-clean. Bedroom only, medium, about 30 minutes"),
      dict(when="11:00 pm", text="Seal and drop to quiet · fan capped at 28 dB"),
      dict(when="7:00 am", text="Ease back up before you wake"),
    ]),
  roomExtras=[],
  agentCards=[
    dict(id="ep-preclean", kind="proposal", detector="externalForecast", zone="needsYourCall",
      stratum="agent", statusTag="Proposed", source="forecast + 21 nights",
      title="Outside hits 180 by 10 pm",
      body="I'd rather clean early than run loud while you sleep. Pre-clean <b>8:30–9:00</b> "
           "at medium, then hold windows-closed. Quiet hours stay intact.",
      actions=[
        dict(id="i1", label="Run it", variant="primary",
             effect=dict(type="toast", message="Pre-clean scheduled · 8:30 pm, bedroom, medium")),
        dict(id="i2", label="Why this?", variant="default",
             effect=dict(type="openReport")),
        dict(id="i3", label="Not tonight", variant="ghost", effect=dict(type="dismissCard")),
      ]),
    dict(id="ep-saver", kind="receipt", detector="energy", zone="doneToday",
      stratum="agent", statusTag="Done", source="power saver",
      title="Power saver ran today",
      body="12–5 pm at low. <b>₹3 saved</b>, and the room never went above 38.",
      actions=[
        dict(id="j1", label="Do this always", variant="warm",
             effect=dict(type="toAutomation", message="Added to Automation · created by your agent")),
        dict(id="j2", label="See the numbers", variant="ghost",
             effect=dict(type="openReportSegment", segment="energy")),
      ]),
  ],
  emptySlots=[],
  unseenNotifications=1),

"liveEvent": dict(
  key="liveEvent", accent="coral", clock="7:19", deviceCount=1,
  outdoor=dict(aqi=96, category="Moderate", ageMinutes=14, stale=False),
  weather=dict(temp="26°", condition="Haze"),
  room=dict(aqi=148, tone="coral", label="Bedroom"),
  score=dict(value=52, confidence="full", confidenceReason="responding now",
    contributors=contributors(
      ("pm25","Particulates","54 µg/m³","bad",0.35,0.18),
      ("voc","VOCs","0.88 ppm · high","bad",0.15,0.25),
      ("humidity","Humidity","46% · in band","good",0.20,0.90),
      ("noise","Noise","Turbo · 52 dB","moderate",0.15,0.40),
      ("filter","Filter","62% used","moderate",0.15,0.62))),
  hero=dict(mode="narrative",
    headline="Something's burning.", dim="PM2.5 jumped to 148 in four minutes.",
    narrative="Kitchen smoke reaching the bedroom. I've gone to turbo and I'll hold it "
              "until the room is back under 50."),
  roomExtras=[],   # PRD §3.1.4 — a live event suppresses decorative slots
  agentCards=[
    dict(id="le-live", kind="liveAction", detector="recurringPattern", zone="liveNow",
      stratum="agent", statusTag="Running", source="acting now", progress=0.62,
      title="Turbo, running now",
      body="Four minutes in. Down from <b>148</b> to <b>96</b>. This is reversible. "
           "stop it any time.",
      actions=[
        dict(id="k1", label="Stop it", variant="default",
             effect=dict(type="toast", message="Stopped · back to auto")),
        dict(id="k2", label="Why this?", variant="ghost",
             effect=dict(type="openReport")),
      ]),
    dict(id="le-pattern", kind="proposal", detector="recurringPattern", zone="needsYourCall",
      stratum="agent", statusTag="From your history", source="9 of the last 14 days",
      title="This happens most evenings",
      body="Nine of the last fourteen days, around 7:15 pm. I could start the fan "
           "<b>five minutes early</b> instead of chasing it, you'd never see 148.",
      actions=[
        dict(id="l1", label="Do this daily", variant="primary",
             effect=dict(type="toAutomation", message="Added to Automation · 7:10 pm, weekdays")),
        dict(id="l2", label="Show data", variant="default",
             effect=dict(type="openReport")),
        dict(id="l3", label="Not now", variant="ghost", effect=dict(type="dismissCard")),
      ]),
  ],
  emptySlots=[],
  unseenNotifications=3),

"seasonPrep": dict(
  key="seasonPrep", accent="amber", clock="11:06", deviceCount=1,
  outdoor=dict(aqi=118, category="Unhealthy for sensitive", ageMinutes=30, stale=False),
  weather=dict(temp="29°", condition="Dusty"),
  room=dict(aqi=34, tone="amber", label="Bedroom"),
  score=dict(value=86, confidence="full", confidenceReason="door shut, 4 hours",
    contributors=contributors(
      ("pm25","Particulates","9 µg/m³","good",0.35,0.86),
      ("voc","VOCs","0.33 ppm","good",0.15,0.80),
      ("humidity","Humidity","47% · in band","good",0.20,0.93),
      ("noise","Noise","Low · 31 dB","good",0.15,0.91),
      ("filter","Filter","62% used","moderate",0.15,0.62))),
  hero=dict(mode="narrative",
    headline="Pollen season starts in about three weeks.", dim="Last year it caught you out.",
    narrative="Grass pollen climbs from mid-March here. Your filter is at 62%. "
              "on current use it won't make it through."),
  roomExtras=[],
  agentCards=[
    dict(id="sp-filter", kind="proposal", detector="predictiveMaintenance", zone="needsYourCall",
      stratum="agent", statusTag="Proposed", source="62% used · season-adjusted",
      title="Order a filter before the season",
      body="At this rate you hit 20% around <b>8 March</b>, right as pollen peaks. "
           "Order now and it arrives before it runs out.",
      actions=[
        dict(id="m1", label="Order · ₹1,490", variant="primary",
             effect=dict(type="toast", message="Filter ordered · arrives 2–4 March")),
        dict(id="m2", label="Show data", variant="default",
             effect=dict(type="openReport")),
        dict(id="m3", label="Remind me later", variant="ghost", effect=dict(type="dismissCard")),
      ]),
    dict(id="sp-goal", kind="proposal", detector="standingGoal", zone="needsYourCall",
      stratum="agent", statusTag="Standing goal", source="a season, not a night",
      title="Give me the season instead of the question",
      body="Rather than asking every night, I could hold the bedroom <b>under 40</b> "
           "from March to May and just tell you what I did. You can revoke it any time.",
      actions=[
        dict(id="n1", label="Set the goal", variant="primary",
             effect=dict(type="toAutomation", message="Standing goal set · under 40, Mar–May")),
        dict(id="n2", label="Why this?", variant="ghost",
             effect=dict(type="openReport")),
      ]),
    dict(id="sp-list", kind="checklist", detector="predictiveMaintenance", zone="checklist",
      stratum="agent", statusTag="Playbook", source="4 steps",
      title="Pollen playbook", body="",
      items=[
        dict(text="Order the replacement filter", sub="Before 1 March", done=False),
        dict(text="Seal the bedroom window gap", sub="The draught on the east side", done=True),
        dict(text="Move sleep mode 30 min earlier", sub="Pollen peaks at dawn", done=False),
        dict(text="Wash bedding weekly through April", sub="Not something I can do", done=False),
      ]),
  ],
  emptySlots=[dict(zone="doneToday",
    copy="Nothing today. The season hasn't started. This is all preparation.")],
  unseenNotifications=2),
}

# ─────────────────────────────────────────────────────────── report + feed
def series(*vals): return list(vals)

REPORT = dict(
  day="Today · Tue 5 Aug", live=True,
  score=84, confidence="soft", confidenceReason="door open since noon",
  narrative="A steady day. One dip when the door was open through the afternoon, "
            "and the fan barely had to work.",
  metrics=dict(
    pm25=dict(label="PM2.5", unit="µg/m³", peak=58, series=series(
      22,20,19,18,18,19,24,38,52,44,33,29,31,34,36,33,30,28,31,58,46,34,27,24)),
    voc=dict(label="VOC", unit="ppm", peak=0.9, series=series(
      28,26,25,24,24,26,31,38,42,36,32,30,31,33,35,33,31,29,33,52,44,36,30,28)),
    temp=dict(label="Temp", unit="°C", peak=34, series=series(
      24,24,23,23,23,24,25,27,29,31,32,33,34,34,33,32,31,30,29,28,27,26,25,24)),
    noise=dict(label="Noise", unit="dB", peak=52, series=series(
      28,28,28,28,28,28,30,34,36,33,31,30,30,31,32,31,30,30,33,52,44,36,31,29)),
  ),
  bands=[dict(kind="night", label="Sealed window", fromH=0, toH=7),
         dict(kind="saver", label="Power saver", fromH=12, toH=17)],
  peak=dict(hour=19, label="Cooking spike · 58 µg/m³"),
  night=dict(label="Last night · the sealed window", detail="11:04 pm – 7:02 am",
    outsidePeak=187, roomHeld=24, held="7h 11m under 30 µg/m³",
    series=series(24,22,21,20,19,19,20,22)),
  energy=dict(caption="Fan effort against what the air actually needed. "
                      "The gap is electricity you didn't have to spend.",
    effort=series(30,30,32,44,58,52,40,34,32,34,36,38,40,42,44,42,38,36,42,68,58,44,36,32),
    need=series(28,26,25,24,24,26,32,42,50,44,34,30,31,33,35,33,30,29,33,60,48,36,29,27),
    saved="₹3 today · about ₹90 a month"),
)

NOTIFICATIONS = [
  dict(id="n1", day="Today", kind="proposal", title="Your afternoons run clean on their own",
       timestamp="2:12 pm", typeLabel="Proposal", unseen=True,
       effect=dict(type="openReportSegment", segment="energy")),
  dict(id="n2", day="Today", kind="alert", title="PM2.5 spike. Turbo running",
       timestamp="7:18 pm", typeLabel="Live alert", unseen=True,
       effect=dict(type="openReport")),
  dict(id="n3", day="Yesterday", kind="done", title="Ran quiet all night",
       timestamp="7:02 am", typeLabel="Done", unseen=False,
       effect=dict(type="openReportSegment", segment="night")),
  dict(id="n4", day="Yesterday", kind="proposal", title="Pre-clean before 10 pm",
       timestamp="6:30 pm", typeLabel="Accepted", unseen=False,
       effect=dict(type="openReport")),
  dict(id="n5", day="Sunday", kind="digest", title="Your week in air",
       timestamp="9:00 am", typeLabel="Weekly summary", unseen=False,
       effect=dict(type="toast", message="Weekly summary archives into report history")),
]

FIXTURE = dict(activeState="morningRecap", states=STATES,
               report=REPORT, notifications=NOTIFICATIONS)

ORDER = ["dayOne","morningRecap","calmDay","eveningPlan","liveEvent","seasonPrep"]
LABELS = {"dayOne":"Day one","morningRecap":"Morning recap","calmDay":"Calm day",
          "eveningPlan":"Evening plan","liveEvent":"Live event","seasonPrep":"Season prep"}
JOBS = {
 "dayOne":"Prove the device works; ask the one onboarding question.",
 "morningRecap":"Report the sealed night; celebrate the streak.",
 "calmDay":"Name what it's watching; surface the best available proposal.",
 "eveningPlan":"Show tonight's plan.",
 "liveEvent":"Show the live response to a spike. Decorative slots suppressed.",
 "seasonPrep":"Frame a coming seasonal change; run the playbook.",
}

CIRCLED = ["\u2460","\u2461","\u2462","\u2463","\u2464","\u2465"]
GROUPS = [("New & early", ["dayOne"]),
          ("Steady state", ["morningRecap","calmDay","eveningPlan"]),
          ("Events & seasons", ["liveEvent","seasonPrep"])]
def group_html(title, keys):
    btns = "".join(
      f'<button class="sbtn" data-state="{k}"><b>{CIRCLED[ORDER.index(k)]}</b>{LABELS[k]}</button>'
      for k in keys)
    return f'<p class="cl">{title}</p><div class="sbtns">{btns}</div>'
state_btns = "".join(group_html(t, ks) for t, ks in GROUPS)

CSS = r"""
@font-face{font-family:GSF;font-weight:400;src:url(data:font/ttf;base64,__REG__) format("truetype")}
@font-face{font-family:GSF;font-weight:600;src:url(data:font/ttf;base64,__MED__) format("truetype")}
@font-face{font-family:GSF;font-weight:700;src:url(data:font/ttf;base64,__BLD__) format("truetype")}
:root{
  --ink:#2E2E2C; --sec:#767674; --ter:#9E9E9C; --hair:rgba(11, 11, 11, 0.09);
  --card:#FFFFFF; --cardq:#E8E8E5;
  --sh:0px 2px 8px 0px rgba(0, 0, 0, 0.03), 0px 12px 32px 0px rgba(0, 0, 0, 0.06); --shs:0px 1px 3px 0px rgba(0, 0, 0, 0.04), 0px 5px 14px 0px rgba(0, 0, 0, 0.07);
  --page:#E8E8E5; --panel:#FFFFFF;
  --grad:linear-gradient(180deg, #FFFFFF 0%, #FDFDFC 38%, #DDDCD8 100%);
  /* PALETTE 2026-08-12 — read from src/tokens/design.tokens.js, not invented
     here. lime/mint replace the sage moss/neon pair entirely.
     ⚠ INK ON GREEN: both anchors are light (lime+white 1.83:1), so anything
     sitting ON green uses --ink, never white. LAW 6, the 10%% rule, is back:
     green marks one thing per screen and is absent everywhere else. */
  --lime:#AECC2A; --mint:#6CCC7C; --haze:#E9E8E5;
  --limeDeep:#5E6F0D; --mintDeep:#27753A;
  --gGrad:linear-gradient(180deg, #6CCC7C 0%, #AECC2A 100%);
  --gWash:linear-gradient(150deg,rgba(108,204,124,.34) 0%,rgba(108,204,124,0) 62%);
  /* ⚠⚠ BAND COLOURS ARE THE STRONGEST OPEN CASE FOR O-6 IN THE PRODUCT.
     The 2026-08-12 palette rule says only greens, whites and greys. An AIR
     QUALITY app cannot obey that here: "severe" has to be legible as bad, and
     neither green nor grey can carry it. These four amber/orange/red values
     are therefore KEPT, knowingly outside the palette, because stripping them
     would make the product unable to say the one thing it exists to say.
     This is the same open decision as the destructive row and the 13 first-run
     error states — but it is the case where monochrome costs the most.
     "good" now uses the new mint→lime ramp; the other three are untouched. */
  --good:#27753A; --moderate:#8A6A2F; --poor:#A2632F; --bad:#96402F;
  --goodGrad:linear-gradient(180deg, #6CCC7C 0%, #AECC2A 100%);
  --moderateGrad:linear-gradient(135deg,#C4AC7A 0%,#8A6A2F 100%);
  --poorGrad:linear-gradient(135deg,#D09A6E 0%,#A2632F 100%);
  --badGrad:linear-gradient(135deg,#C97A63 0%,#96402F 100%);
  --goodWash:linear-gradient(150deg,rgba(108,204,124,.34) 0%,rgba(108,204,124,0) 62%);
  --moderateWash:linear-gradient(150deg,rgba(196,172,122,.40) 0%,rgba(196,172,122,0) 62%);
  --poorWash:linear-gradient(150deg,rgba(208,154,110,.42) 0%,rgba(208,154,110,0) 62%);
  --badWash:linear-gradient(150deg,rgba(201,122,99,.46) 0%,rgba(201,122,99,0) 62%);
  --goodbg:rgba(108,204,124,.16); --moderatebg:rgba(138,106,47,.13);
  --poorbg:rgba(162,99,47,.13); --badbg:rgba(150,64,47,.13);
  --cream:#FAF7F2; --creamLine:rgba(90,74,52,.14); --creamLabel:#9A7F55;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{background:var(--page);color:var(--ink);font-family:GSF,system-ui,sans-serif;font-size:15px;
  line-height:1.5;-webkit-font-smoothing:antialiased;overflow:hidden}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer;text-align:left}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:6px}

.shell{display:grid;grid-template-columns:clamp(230px,32%,430px) minmax(0,1fr);height:100vh}
.ctrl{background:var(--cream);overflow-y:auto;padding:44px 40px 56px;
  border-right:1px solid var(--creamLine)}
.ctrl__in{max-width:430px}
.ctrl h1{font-size:31px;line-height:1.1;letter-spacing:-.03em;margin:0 0 12px}
.lede{font-size:14.5px;color:#6E6154;margin:0 0 30px;line-height:1.55}
.cl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--creamLabel);
  font-weight:600;margin:30px 0 12px}
.cl:first-of-type{margin-top:0}
.sbtns{display:flex;flex-direction:column;gap:9px}
.sbtn{width:100%;padding:16px 18px;border:1px solid var(--creamLine);border-radius:15px;
  font-size:15.5px;display:flex;gap:14px;align-items:center;background:#fff}
.sbtn b{font-family:GSF,serif;font-size:15px;font-weight:400;color:#A99C8B;flex:0 0 auto}
.sbtn:hover{border-color:rgba(90,74,52,.3)}
.sbtn.on{border:2px solid var(--ink);padding:15px 17px}
.sbtn.on b{color:var(--ink)}
/* the one place green marks state in the harness — 10% rule */
.sbtn.on::after{content:"";width:7px;height:7px;border-radius:50%;background:var(--gGrad);
  margin-left:auto;flex:0 0 auto}
.job{font-size:13.5px;color:#8B7E6E;line-height:1.5;margin:14px 2px 0;padding:0 0 0 13px;
  border-left:2px solid var(--neon)}
.dev{display:flex;flex-direction:column;gap:9px}
.dev button{padding:14px 18px;border:1px solid var(--creamLine);border-radius:15px;
  font-size:14.5px;background:#fff}
.dev button:hover{border-color:rgba(90,74,52,.3)}
.note{font-size:12px;color:#8B7E6E;line-height:1.6;margin:0}
.note b{color:#5E5245}

.stage{display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:14px;padding:26px 10px 26px 30px;overflow:hidden;position:relative}
.phwrap{flex:0 0 auto;display:flex;align-items:center;justify-content:center}
.phone{width:390px;height:844px;flex:none;border-radius:52px;position:relative;overflow:hidden;
  background:var(--grad);transform-origin:center center;
  box-shadow:0 0 0 11px #17171A,0 0 0 12.5px #34343A,0 30px 70px rgba(0,0,0,.26)}
.phone::before{content:"";position:absolute;inset:0;background:rgba(240,238,233,.74);
  pointer-events:none;z-index:0}
.island{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:110px;height:30px;
  background:#0A0A0A;border-radius:20px;z-index:60}
.hbar{position:absolute;bottom:9px;left:50%;transform:translateX(-50%);width:134px;height:5px;
  background:rgba(0,0,0,.22);border-radius:3px;z-index:60}
.meta{width:390px;max-width:92%;font-size:12.5px;color:var(--sec);line-height:1.5;text-align:center;flex:0 0 auto}
.meta b{color:var(--ink);display:block;margin-bottom:3px;font-size:13px}

/* the scrolling app surface */
.app{position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;overflow:hidden}
.appscroll{flex:1 1 auto;overflow-y:auto;padding:0 20px 16px;scrollbar-width:none}
.appscroll::-webkit-scrollbar{display:none}
.fade-in{animation:fi .34s cubic-bezier(.2,0,0,1)}
@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

.sbar{height:56px;flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;
  font-size:14px;font-weight:600;padding:15px 20px 0}
.sbar i{display:block;background:var(--ink);opacity:.9}
.sbar .r{display:flex;gap:5px;align-items:center}
.sig{width:17px;height:11px;clip-path:polygon(0 68%,20% 68%,20% 100%,0 100%,0 68%,27% 44%,47% 44%,47% 100%,27% 100%,27% 44%,54% 20%,74% 20%,74% 100%,54% 100%,54% 20%,80% 0,100% 0,100% 100%,80% 100%)}
.wf{width:15px;height:11px;clip-path:polygon(50% 100%,0 38%,14% 26%,50% 62%,86% 26%,100% 38%)}
.bt{width:25px;height:12px;border-radius:3.5px}

/* header */
.hdr{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:6px 0 14px}
.hdr__l{min-width:0}
.hdr__room{font-size:15px;font-weight:700;letter-spacing:-.01em;margin:0 0 3px}
.hdr__out{font-size:12.5px;color:var(--sec);margin:0;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}
.hdr__out b{font-weight:600;color:var(--ink)}
.age{font-size:11px;color:var(--ter)}
.hdr__r{display:flex;gap:8px;align-items:center;flex:0 0 auto}
.wpill{background:var(--card);box-shadow:var(--shs);border-radius:99px;padding:7px 12px;font-size:12.5px;
  display:flex;gap:6px;align-items:center;white-space:nowrap}
.bell{width:40px;height:40px;border-radius:50%;background:var(--card);box-shadow:var(--shs);
  display:grid;place-items:center;position:relative;flex:0 0 auto}
.bell:hover{background:#fff}
.bell__i{width:15px;height:16px;border-radius:7px 7px 3px 3px;border:2px solid var(--ink);position:relative}
.bell__i::after{content:"";position:absolute;left:50%;bottom:-5px;transform:translateX(-50%);
  width:7px;height:3px;border-radius:0 0 4px 4px;background:var(--ink)}
.bell__n{position:absolute;top:-1px;right:-1px;min-width:17px;height:17px;border-radius:99px;
  background:var(--ink);color:#fff;font-size:10px;font-weight:700;display:grid;place-items:center;padding:0 4px}

/* ── ROOM STRATUM ─────────────────────────────────────────── */
.hero{width:100%;text-align:left;display:block;box-shadow:var(--sh);position:relative;
  border-radius:26px;padding:18px 18px 16px;margin-bottom:12px;overflow:hidden;
  background:var(--card)}
.hero::before{content:"";position:absolute;inset:0;background:var(--w,var(--gWash));pointer-events:none}
.hero > *{position:relative}
.hero:hover{background:rgba(255,255,255,.9)}
.hero__top{display:flex;gap:14px;align-items:flex-start;margin-bottom:14px}
.iso{width:150px;height:126px;flex:0 0 auto;position:relative}
.iso svg{width:100%;height:100%;display:block}
.badge{position:absolute;right:2px;top:6px;min-width:44px;height:30px;border-radius:99px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 9px;
  background:var(--card);box-shadow:var(--shs);line-height:1}
.badge b{font-size:14px;font-weight:700;letter-spacing:-.02em}
.badge span{font-size:7px;letter-spacing:.12em;color:var(--ter);margin-top:1px}
.scoreb{flex:1;min-width:0;padding-top:2px}
.kick{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ter);
  display:flex;align-items:center;gap:6px;margin:0 0 2px}
.livedot{width:6px;height:6px;border-radius:50%;background:var(--gGrad);animation:br 2.4s ease-in-out infinite}
@keyframes br{50%{opacity:.35;transform:scale(.8)}}
.scoren{font-size:60px;line-height:.95;font-weight:700;letter-spacing:-.05em;margin:0}
.scoren.g{background:var(--ng,var(--gGrad));-webkit-background-clip:text;background-clip:text;
  color:transparent}
.scoresub{font-size:12px;color:var(--sec);margin:2px 0 0}
.hero__head{font-size:20px;line-height:1.22;letter-spacing:-.024em;font-weight:700;margin:0 0 8px}
.hero__head span{color:var(--ter);font-weight:400}
.hero__nar{font-size:14px;line-height:1.45;color:var(--sec);margin:0}
.watch{display:flex;flex-direction:column;gap:9px;margin:0}
.watch div{display:flex;gap:11px;align-items:baseline;font-size:13.5px;line-height:1.35;color:var(--sec)}
.watch b{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:var(--ter);
  min-width:52px;flex:0 0 auto;letter-spacing:.02em}
.hero__foot{display:flex;align-items:center;justify-content:space-between;gap:10px;
  border-top:1px solid var(--hair);padding-top:12px;margin-top:14px}
.conf{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--sec)}
.conf i{width:7px;height:7px;border-radius:50%;flex:0 0 auto}
.cue{font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:4px}

.rcard{background:var(--card);box-shadow:var(--shs);border-radius:20px;padding:15px 16px;margin-bottom:10px}
.rcard__tag{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ter);margin:0 0 6px}
.rcard__t{font-size:15.5px;font-weight:700;letter-spacing:-.015em;margin:0 0 4px}
.rcard__b{font-size:13.5px;line-height:1.45;color:var(--sec);margin:0}
.rcard__b b{color:var(--ink);font-weight:700}
.defend{display:flex;gap:14px;align-items:center;margin-top:10px}
.defend__n{flex:0 0 auto}
.defend__n b{display:block;font-size:22px;font-weight:700;letter-spacing:-.03em;line-height:1}
.defend__n span{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ter)}
.spark{flex:1;height:38px}
.spark svg{width:100%;height:100%;display:block}
.rail{display:flex;gap:8px;margin-top:10px;overflow-x:auto;scrollbar-width:none}
.rail::-webkit-scrollbar{display:none}
.rail div{flex:0 0 auto;background:rgba(11,11,11,.05);border-radius:12px;padding:9px 12px}
.rail b{display:block;font-size:12.5px;font-weight:600}
.rail span{font-size:11px;color:var(--ter)}

/* ── DIVIDER ──────────────────────────────────────────────── */
.divider{display:flex;align-items:center;gap:12px;margin:18px 0 14px}
.divider i{flex:1;height:1px;background:var(--hair)}
.divider span{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ter);
  display:flex;align-items:center;gap:7px}
.divider em{font-style:normal;font-size:11px}

/* ── AGENT STRATUM ────────────────────────────────────────── */
.zone{margin-bottom:16px}
.zone__t{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ter);margin:0 0 9px}
.acard{background:var(--card);box-shadow:var(--sh);border-radius:20px;padding:16px 16px 14px;
  margin-bottom:10px;border-left:2.5px solid var(--ink);position:relative}
.acard--live{border-left-color:var(--bad)}
.acard__top{display:flex;gap:8px;align-items:baseline;margin-bottom:7px;flex-wrap:wrap}
.tag{font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ter);
  background:rgba(11,11,11,.05);border-radius:99px;padding:3px 8px}
.src{font-size:11px;color:var(--ter)}
.acard__t{font-size:16.5px;line-height:1.25;font-weight:700;letter-spacing:-.02em;margin:0 0 6px}
.acard__b{font-size:13.5px;line-height:1.5;color:var(--sec);margin:0 0 12px}
.acard__b b{color:var(--ink);font-weight:700}
.acts{display:flex;flex-wrap:wrap;gap:8px}
.act{border-radius:99px;padding:11px 16px;font-size:13.5px;font-weight:600;flex:0 0 auto}
.act--primary{background:var(--ink);color:#fff}
.act--primary:hover{background:#232323}
.act--warm{background:rgba(11,11,11,.07)}
.act--warm:hover{background:rgba(11,11,11,.12)}
.act--default{background:transparent;border:1px solid var(--hair)}
.act--default:hover{background:rgba(11,11,11,.04)}
.act--ghost{background:transparent;color:var(--sec);padding:11px 6px;text-decoration:underline;
  text-underline-offset:3px;text-decoration-color:rgba(11,11,11,.25)}
.act--ghost:hover{color:var(--ink)}
.prog{height:5px;border-radius:99px;background:rgba(11,11,11,.10);overflow:hidden;margin:0 0 12px}
.prog i{display:block;height:100%;background:var(--bad);transition:width .5s}
.facts{display:flex;flex-direction:column;gap:9px;margin-bottom:12px}
.fact{display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
.fact__t{flex:1;min-width:0}
.fact__t b{display:block;font-size:13.5px;font-weight:600;line-height:1.3}
.fact__t span{font-size:11.5px;color:var(--ter)}
.fact__a{display:flex;gap:5px;flex:0 0 auto}
.mini{font-size:11.5px;padding:6px 11px;border-radius:99px;border:1px solid var(--hair)}
.mini:hover{background:rgba(11,11,11,.05)}
.checks{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
.chk{display:flex;gap:11px;align-items:flex-start;width:100%;text-align:left}
.chk__b{width:21px;height:21px;border-radius:6px;border:1.7px solid rgba(11,11,11,.28);flex:0 0 auto;
  margin-top:1px;position:relative}
.chk.done .chk__b{background:var(--ink);border-color:var(--ink)}
.chk.done .chk__b::after{content:"";position:absolute;left:5.5px;top:5px;width:8px;height:4px;
  border-left:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-45deg)}
.chk__t b{display:block;font-size:13.5px;font-weight:600;line-height:1.3}
.chk.done .chk__t b{color:var(--ter);text-decoration:line-through}
.chk__t span{font-size:11.5px;color:var(--ter)}
.hband{margin:0 0 12px}
.hband__bar{height:8px;border-radius:99px;background:rgba(11,11,11,.08);position:relative}
.hband__in{position:absolute;top:0;bottom:0;background:var(--goodbg);border-radius:99px}
.hband__pin{position:absolute;top:-3px;width:3px;height:14px;border-radius:2px;background:var(--moderate)}
.hband__l{display:flex;justify-content:space-between;font-size:10.5px;color:var(--ter);margin-top:6px}
.empty{background:rgba(255,255,255,.4);border:1px dashed rgba(11,11,11,.14);border-radius:18px;
  padding:15px 16px;font-size:13.5px;line-height:1.5;color:var(--sec);margin-bottom:10px}

/* tabbar */
.tabs{display:flex;padding:10px 20px 26px;border-top:1px solid var(--hair);flex:0 0 auto;
  background:rgba(255,255,255,.5);backdrop-filter:blur(14px)}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px;font-size:10px;color:var(--ter)}
.tab i{width:22px;height:22px;border-radius:7px;background:rgba(11,11,11,.13);display:block}
.tab.on{color:var(--ink)}.tab.on i{background:var(--ink)}

/* sheets */
.sheet{position:absolute;inset:0;z-index:70;background:rgba(0,0,0,.32);display:none;
  align-items:flex-end}
.sheet.on{display:flex;animation:fade .2s}
@keyframes fade{from{opacity:0}to{opacity:1}}
.sheet__c{background:#F4F3F1;width:100%;max-height:92%;border-radius:26px 26px 52px 52px;
  display:flex;flex-direction:column;animation:up .34s cubic-bezier(.2,.9,.3,1)}
@keyframes up{from{transform:translateY(50px)}to{transform:none}}
.sheet__h{display:flex;align-items:center;justify-content:space-between;gap:10px;
  padding:16px 20px 12px;border-bottom:1px solid var(--hair);flex:0 0 auto}
.sheet__h b{font-size:17px;letter-spacing:-.02em}
.xb{width:34px;height:34px;border-radius:50%;background:rgba(11,11,11,.06);display:grid;place-items:center;
  flex:0 0 auto;position:relative}
.xb::before,.xb::after{content:"";position:absolute;width:13px;height:1.8px;background:var(--ink)}
.xb::before{transform:rotate(45deg)}.xb::after{transform:rotate(-45deg)}
.sheet__b{overflow-y:auto;padding:16px 20px 34px;scrollbar-width:none}
.sheet__b::-webkit-scrollbar{display:none}

/* report */
.pager{display:flex;align-items:center;justify-content:space-between;gap:8px;
  background:var(--card);box-shadow:var(--shs);border-radius:99px;padding:7px 8px;margin-bottom:14px}
.pager button{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;font-size:16px}
.pager button:hover{background:rgba(11,11,11,.06)}
.pager span{font-size:13px;font-weight:600}
.rhead{display:flex;gap:16px;align-items:center;margin-bottom:14px}
.ring{width:98px;height:98px;flex:0 0 auto;position:relative}
.ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.ring b{position:absolute;inset:0;display:grid;place-items:center;font-size:30px;font-weight:700;
  letter-spacing:-.03em}
.rhead__t{flex:1;min-width:0}
.rhead__t p{margin:0;font-size:13.5px;line-height:1.45;color:var(--sec)}
.chips{display:flex;gap:7px;margin-bottom:12px;overflow-x:auto;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.mchip{flex:0 0 auto;padding:8px 14px;border-radius:99px;background:var(--card);box-shadow:var(--shs);
  font-size:13px;font-weight:600}
.mchip.on{background:var(--ink);color:#fff}
.chart{background:var(--card);box-shadow:var(--shs);border-radius:18px;padding:14px;margin-bottom:12px}
.chart__t{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ter);margin:0 0 10px;
  display:flex;justify-content:space-between}
.chart svg{width:100%;display:block}
.chart__k{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:11px;color:var(--ter)}
.chart__k span{display:flex;align-items:center;gap:5px}
.chart__k i{width:14px;height:3px;border-radius:2px;display:block}
.nightseg{background:rgba(124,138,224,.10);border-left:2.5px solid #6E7BC8;border-radius:14px;
  padding:14px 15px;margin-bottom:12px}
.nightseg b{font-size:14.5px;display:block;margin-bottom:3px}
.nightseg p{margin:0 0 10px;font-size:12.5px;color:var(--sec)}
.contrib{background:var(--card);box-shadow:var(--shs);border-radius:18px;padding:6px 15px;margin-bottom:12px}
.crow{display:flex;gap:12px;align-items:center;padding:13px 0;border-bottom:1px solid var(--hair)}
.crow:last-child{border-bottom:0}
.crow__l{flex:1;min-width:0}
.crow__l b{display:block;font-size:13.5px;font-weight:600}
.crow__l span{font-size:11.5px;color:var(--ter)}
.crow__r{flex:0 0 auto;text-align:right;width:104px}
.blabel{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-bottom:5px;
  display:block}
.meter{height:5px;border-radius:99px;background:rgba(11,11,11,.09);overflow:hidden}
.meter i{display:block;height:100%;border-radius:99px}
.unav{opacity:.62}
.rnote{font-size:12px;line-height:1.55;color:var(--ter);margin:14px 0 0;padding-top:12px;
  border-top:1px solid var(--hair)}

/* feed */
.fday{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ter);margin:16px 0 8px}
.fday:first-child{margin-top:0}
.frow{display:flex;gap:12px;align-items:flex-start;width:100%;background:var(--card);box-shadow:var(--shs);
  border-radius:16px;padding:13px 15px;margin-bottom:8px;text-align:left}
.frow:hover{background:#fff}
.fi{width:30px;height:30px;border-radius:9px;background:rgba(11,11,11,.06);display:grid;place-items:center;
  font-size:13px;flex:0 0 auto}
.frow__t{flex:1;min-width:0}
.frow__t b{display:block;font-size:13.5px;font-weight:600;line-height:1.3;margin-bottom:2px}
.frow__t span{font-size:11.5px;color:var(--ter);font-family:ui-monospace,Menlo,monospace}
.udot{width:8px;height:8px;border-radius:50%;background:var(--ink);flex:0 0 auto;margin-top:6px}

.toast{position:absolute;left:20px;right:20px;bottom:96px;background:var(--ink);color:#fff;
  border-radius:14px;padding:14px 16px;font-size:13.5px;text-align:center;z-index:80;
  animation:up .28s cubic-bezier(.2,.9,.3,1)}

@media (prefers-reduced-motion:reduce){
  *{animation:none !important;transition:none !important}}
@media (max-width:1150px){
  .ctrl{padding:30px 24px 40px}
  .ctrl h1{font-size:25px}
  .lede{font-size:13.5px;margin-bottom:24px}
  .sbtn{padding:13px 15px;font-size:14.5px;gap:11px}
  .sbtn.on{padding:12px 14px}
  .dev button{padding:12px 15px;font-size:13.5px}
  .meta{display:none}
}
@media (max-width:820px){
  .ctrl{padding:22px 18px 32px}
  .ctrl h1{font-size:21px;margin-bottom:8px}
  .lede{font-size:12.5px;margin-bottom:20px;line-height:1.45}
  .cl{font-size:10px;margin:22px 0 9px}
  .sbtn{padding:11px 13px;font-size:13.5px;border-radius:13px}
  .sbtn.on{padding:10px 12px}
  .job{font-size:12.5px}
  .note{font-size:11px}
}
/* only collapse when a side-by-side genuinely cannot work */
@media (max-width:520px){.shell{grid-template-columns:1fr}.ctrl{max-height:46vh}}
"""

BODY = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOMA — My Home</title>
<style>{CSS.replace("__REG__",FONTS["REG"]).replace("__MED__",FONTS["MED"]).replace("__BLD__",FONTS["BLD"])}</style>
</head><body>
<div class="shell">
  <aside class="ctrl"><div class="ctrl__in">
    <h1>My Home &mdash; state harness</h1>
    <p class="lede">Pick a state. The hero changes job, and the agent slots fill or empty with
      it. Tap the hero for the report, the bell for the feed. Keys 1&ndash;6 switch, Esc closes.</p>
    {state_btns}
    <p class="job" id="job"></p>

    <p class="cl">Open directly</p>
    <div class="dev">
      <button id="oR">Report sheet</button>
      <button id="oN">Notification feed</button>
      <button id="oE">Report &rarr; energy chart</button>
      <button id="oS">Report &rarr; last night</button>
    </div>

    <p class="cl">Deviations from the PRD</p>
    <p class="note"><b>Palette.</b> PRD &sect;11 specifies dark (#0c0e12, aqua/coral). This uses
      the light direction set for first-run, so Home matches the reveal the user just came from.
      See C-14.<br><br>
      <b>Green.</b> Back as accent only, under the 10% rule &mdash; the good band, the score ring,
      the fertile-equivalent gradients. Never a ground, never body copy, never two per screen.
      Canonical moss/neon from <code>design.tokens.js</code>.<br><br>
      <b>Stack.</b> PRD asks React+Tailwind; no scaffold in this repo. Rendered from a fixture
      matching the &sect;7 interfaces, so the port is mechanical.<br><br>
      <b>Name.</b> The PRD says &ldquo;Ding&rdquo;. Everything else here says NOMA &mdash; C-2.</p>
  </div></aside>

  <main class="stage">
    <div class="phwrap">
      <div class="phone" id="phone">
        <div class="island"></div><div class="hbar"></div>
        <div class="app">
          <div class="sbar"><span id="clock">9:41</span>
            <span class="r"><i class="sig"></i><i class="wf"></i><i class="bt"></i></span></div>
          <div class="appscroll" id="scroll"></div>
          <div class="tabs">
            <span class="tab on"><i></i>My home</span>
            <span class="tab"><i></i>Device</span>
            <span class="tab"><i></i>Automation</span>
            <span class="tab"><i></i>Shop</span>
          </div>
        </div>
        <div class="sheet" id="report"><div class="sheet__c">
          <div class="sheet__h"><b>Today's report</b><button class="xb" data-close="report" aria-label="Close"></button></div>
          <div class="sheet__b" id="reportBody"></div></div></div>
        <div class="sheet" id="feed"><div class="sheet__c">
          <div class="sheet__h"><b>Notifications</b><button class="xb" data-close="feed" aria-label="Close"></button></div>
          <div class="sheet__b" id="feedBody"></div></div></div>
      </div>
    </div>
    <div class="meta"><b id="mt"></b><span id="mn"></span></div>
  </main>
</div>
<script>
const F = {json.dumps(FIXTURE, ensure_ascii=False)};
const JOBS = {json.dumps(JOBS, ensure_ascii=False)};
const LABELS = {json.dumps(LABELS, ensure_ascii=False)};
const ORDER = {json.dumps(ORDER)};
let key = F.activeState;
let metric = 'pm25';
let dismissed = new Set();
let checks = {{}};

const bandOf = a => a <= 50 ? 'good' : a <= 100 ? 'moderate' : a <= 150 ? 'poor' : 'bad';
const bandWord = b => ({{good:'Good', moderate:'Moderate', poor:'Poor', bad:'Unhealthy',
  unavailable:'Unavailable'}})[b] || b;
const bandVar = b => ({{good:'--good', moderate:'--moderate', poor:'--poor', bad:'--bad',
  unavailable:'--ter'}})[b] || '--ter';
const esc = s => String(s).replace(/[<>&]/g, c => ({{'<':'&lt;','>':'&gt;','&':'&amp;'}})[c]);
// body copy allows <b> and <i> only (PRD §7: "supports simple <b>/<i> emphasis")
const rich = s => esc(s).replace(/&lt;(\\/?[bi])&gt;/g, '<$1>');

function toast(msg){{
  const old = document.querySelector('.toast'); if (old) old.remove();
  const t = document.createElement('div');
  t.className = 'toast'; t.setAttribute('role','status'); t.textContent = msg;
  document.getElementById('phone').appendChild(t);
  setTimeout(() => t.remove(), 2600);
}}
function runEffect(e, cardId){{
  if (!e) return;
  if (e.type === 'toast')  toast(e.message);
  if (e.type === 'toAutomation') toast(e.message);
  if (e.type === 'openReport') openReport();
  if (e.type === 'openReportSegment') openReport(e.segment);
  if (e.type === 'dismissCard'){{ dismissed.add(cardId); toast('Dismissed · I won\\u2019t ask again today'); render(); }}
}}

/* ── isometric room ───────────────────────────────────────── */
function isoRoom(aqi, tone){{
  const b = bandOf(aqi);
  // The ripple is always a gradient, but never the wrong colour: green only when
  // the air is actually good, and the band's own red/amber when it is not.
  const stops = {{good:['#6CCC7C','#AECC2A'], moderate:['#C4AC7A','#8A6A2F'],
    poor:['#D09A6E','#A2632F'], bad:['#C97A63','#96402F']}}[b] || ['#C4C4C4','#8B8B8B'];
  const c = 'url(#rip)';
  const cText = `var(${{bandVar(b)}})`;
  return `<div class="iso">
    <svg viewBox="0 0 150 126" role="img" aria-label="Bedroom, air quality index ${{aqi}}, ${{bandWord(b)}}">
      <defs><linearGradient id="fl" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#fff" stop-opacity=".95"/>
        <stop offset="1" stop-color="#d8d8d8" stop-opacity=".85"/></linearGradient>
        <radialGradient id="rip"><stop offset="0" stop-color="${{stops[0]}}"/>
        <stop offset="1" stop-color="${{stops[1]}}"/></radialGradient></defs>
      <path d="M75 96 L18 66 L75 36 L132 66 Z" fill="url(#fl)"/>
      <path d="M18 66 L18 34 L75 4 L75 36 Z" fill="#fff" opacity=".55"/>
      <path d="M132 66 L132 34 L75 4 L75 36 Z" fill="#e6e6e6" opacity=".6"/>
      <ellipse cx="86" cy="74" rx="30" ry="15" fill="${{c}}" opacity=".46">
        <animate attributeName="rx" values="26;34;26" dur="4s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values=".46;.18;.46" dur="4s" repeatCount="indefinite"/></ellipse>
      <ellipse cx="86" cy="74" rx="18" ry="9" fill="${{c}}" opacity=".62">
        <animate attributeName="rx" values="15;22;15" dur="4s" repeatCount="indefinite"/></ellipse>
      <path d="M52 70 L52 50 L64 44 L64 64 Z" fill="#fff" opacity=".9"/>
      <path d="M64 64 L64 44 L76 50 L76 70 Z" fill="#ededed"/>
      <rect x="80" y="52" width="15" height="26" rx="7" fill="#fff" stroke="rgba(11,11,11,.10)"/>
      <circle cx="87.5" cy="60" r="4" fill="none" stroke="${{cText}}" stroke-width="1.6"/>
    </svg>
    <div class="badge" style="background:var(${{bandVar(b)}}bg)">
      <b style="color:${{cText}}">${{aqi}}</b><span>µg/m³</span></div></div>`;
}}

/* ── room stratum ─────────────────────────────────────────── */
function heroHTML(s){{
  const b = bandOf(s.room.aqi);
  const body = s.hero.mode === 'narrative'
    ? `<p class="hero__nar">${{rich(s.hero.narrative)}}</p>`
    : `<div class="watch">${{s.hero.watch.map(w =>
        `<div><b>${{esc(w.when)}}</b><span>${{esc(w.text)}}</span></div>`).join('')}}</div>`;
  return `<button class="hero" id="hero" style="--w:var(${{bandVar(b)}}Wash)" aria-label="Room quality ${{s.score.value}} out of 100. Open today's report.">
    <div class="hero__top">
      ${{isoRoom(s.room.aqi, s.room.tone)}}
      <div class="scoreb">
        <p class="kick"><span class="livedot"></span>Room quality</p>
        <p class="scoren g" style="--ng:var(${{bandVar(b)}}Grad)">${{s.score.value}}</p>
        <p class="scoresub">${{esc(s.score.confidenceReason)}}</p>
      </div>
    </div>
    <h2 class="hero__head">${{esc(s.hero.headline)}} <span>${{esc(s.hero.dim || '')}}</span></h2>
    ${{body}}
    <div class="hero__foot">
      <span class="conf"><i style="background:${{s.score.confidence === 'full' ? 'var(--gGrad)' : 'var(--moderate)'}}"></i>
        ${{s.score.confidence === 'full' ? 'Full confidence' : 'Soft — inferring'}}</span>
      <span class="cue">Today's report &rsaquo;</span>
    </div></button>`;
}}

function sparkSVG(pts, stroke){{
  const w = 100, h = 30, mx = Math.max(...pts), mn = Math.min(...pts), r = (mx - mn) || 1;
  const d = pts.map((v,i) => `${{(i/(pts.length-1))*w}},${{h - ((v-mn)/r)*h*0.82 - 3}}`).join(' ');
  return `<svg viewBox="0 0 ${{w}} ${{h}}" preserveAspectRatio="none">
    <polyline points="${{d}}" fill="none" stroke="${{stroke}}" stroke-width="1.8"
      stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>`;
}}

function roomExtraHTML(c){{
  let inner = `<p class="rcard__tag">${{esc(c.statusTag||'')}}</p>
    <p class="rcard__t">${{esc(c.title)}}</p>`;
  if (c.body) inner += `<p class="rcard__b">${{rich(c.body)}}</p>`;
  if (c.meta && c.meta.sparkline){{
    inner += `<div class="defend">
      <div class="defend__n"><b>${{c.meta.outsidePeak}}</b><span>outside</span></div>
      <div class="spark">${{sparkSVG(F.report.night.series, 'var(--good)')}}</div>
      <div class="defend__n"><b>${{c.meta.roomHeld}}</b><span>in here</span></div></div>`;
  }}
  if (c.meta && c.meta.rail){{
    inner += `<div class="rail">${{c.items.map(i =>
      `<div><b>${{esc(i.text)}}</b><span>${{esc(i.sub)}}</span></div>`).join('')}}</div>`;
  }}
  if (c.actions) inner += `<div class="acts" style="margin-top:10px">${{c.actions.map(a =>
    `<button class="act act--${{a.variant}}" data-act="${{a.id}}" data-card="${{c.id}}">${{esc(a.label)}}</button>`
  ).join('')}}</div>`;
  return `<div class="rcard">${{inner}}</div>`;
}}

/* ── agent stratum ────────────────────────────────────────── */
const ZONE_TITLES = {{needsYourCall:'Needs your call', liveNow:'Happening now',
  doneToday:'Done today', comfort:'Comfort', learned:'What I\\u2019ve learned',
  checklist:'Playbook', worthKnowing:'Worth knowing', beyondRoom:'Beyond this room'}};

function agentCardHTML(c){{
  let inner = `<div class="acard__top">
      ${{c.statusTag ? `<span class="tag">${{esc(c.statusTag)}}</span>` : ''}}
      ${{c.source ? `<span class="src">${{esc(c.source)}}</span>` : ''}}</div>
    <h3 class="acard__t">${{esc(c.title)}}</h3>`;
  if (c.kind === 'liveAction' && typeof c.progress === 'number')
    inner += `<div class="prog"><i style="width:${{c.progress*100}}%"></i></div>`;
  if (c.body) inner += `<p class="acard__b">${{rich(c.body)}}</p>`;
  if (c.meta && c.meta.band === 'humidity'){{
    const v = +c.meta.value, lo = +c.meta.low, hi = +c.meta.high;
    inner += `<div class="hband"><div class="hband__bar">
      <span class="hband__in" style="left:${{lo}}%;right:${{100-hi}}%"></span>
      <span class="hband__pin" style="left:${{v}}%"></span></div>
      <div class="hband__l"><span>0%</span><span>In band ${{lo}}\\u2013${{hi}}%</span><span>100%</span></div></div>`;
  }}
  if (c.facts) inner += `<div class="facts">${{c.facts.map((f,i) =>
    `<div class="fact"><span class="fact__t"><b>${{esc(f.text)}}</b><span>${{esc(f.sub)}}</span></span>
      <span class="fact__a">
        <button class="mini" data-fact="right">Right</button>
        <button class="mini" data-fact="fix">Fix</button></span></div>`).join('')}}</div>`;
  if (c.items && c.kind === 'checklist'){{
    inner += `<div class="checks">${{c.items.map((it,i) => {{
      const done = (c.id+':'+i) in checks ? checks[c.id+':'+i] : it.done;
      return `<button class="chk${{done?' done':''}}" data-check="${{c.id}}:${{i}}">
        <span class="chk__b"></span><span class="chk__t"><b>${{esc(it.text)}}</b>
        <span>${{esc(it.sub)}}</span></span></button>`;
    }}).join('')}}</div>`;
    const n = c.items.filter((it,i) => (c.id+':'+i) in checks ? checks[c.id+':'+i] : it.done).length;
    inner += `<p class="src" style="margin:0 0 12px">${{n}} of ${{c.items.length}} done</p>`;
  }}
  if (c.actions) inner += `<div class="acts">${{c.actions.map(a =>
    `<button class="act act--${{a.variant}}" data-act="${{a.id}}" data-card="${{c.id}}">${{esc(a.label)}}</button>`
  ).join('')}}</div>`;
  return `<div class="acard${{c.kind==='liveAction'?' acard--live':''}}">${{inner}}</div>`;
}}

/* ── page ─────────────────────────────────────────────────── */
function render(){{
  const s = F.states[key];
  document.getElementById('clock').textContent = s.clock;
  const out = s.outdoor;
  let h = `<div class="hdr">
    <div class="hdr__l">
      <p class="hdr__room">${{esc(s.room.label)}} Air &middot; Gurugram</p>
      <p class="hdr__out"><b>${{out.aqi}}</b> outside &middot; ${{esc(out.category)}}
        <span class="age">&middot; ${{out.ageMinutes}} min ago</span></p>
    </div>
    <div class="hdr__r">
      <span class="wpill">${{esc(s.weather.temp)}} &middot; ${{esc(s.weather.condition)}}</span>
      <button class="bell" id="bell" aria-label="Notifications, ${{s.unseenNotifications}} unseen">
        <span class="bell__i"></span>
        ${{s.unseenNotifications ? `<span class="bell__n">${{s.unseenNotifications}}</span>` : ''}}
      </button>
    </div></div>`;

  h += heroHTML(s);
  (s.roomExtras || []).filter(c => !dismissed.has(c.id)).forEach(c => h += roomExtraHTML(c));

  h += `<div class="divider"><i></i><span>&#10022; <em>your agent</em></span><i></i></div>`;

  // group agent cards by zone, in fixture order; then any empty-slot copy
  const zones = [];
  (s.agentCards || []).filter(c => !dismissed.has(c.id)).forEach(c => {{
    let z = zones.find(x => x.zone === c.zone);
    if (!z) {{ z = {{zone: c.zone, cards: []}}; zones.push(z); }}
    z.cards.push(c);
  }});
  (s.emptySlots || []).forEach(e => {{
    if (!zones.find(x => x.zone === e.zone)) zones.push({{zone: e.zone, empty: e.copy}});
  }});
  zones.forEach(z => {{
    h += `<div class="zone"><p class="zone__t">${{esc(ZONE_TITLES[z.zone] || z.zone)}}</p>`;
    h += z.empty ? `<div class="empty">${{esc(z.empty)}}</div>`
                 : z.cards.map(agentCardHTML).join('');
    h += `</div>`;
  }});

  const sc = document.getElementById('scroll');
  sc.innerHTML = h; sc.scrollTop = 0;
  sc.querySelector('.hero').classList.add('fade-in');

  document.getElementById('hero').addEventListener('click', () => openReport());
  document.getElementById('bell').addEventListener('click', openFeed);
  sc.querySelectorAll('[data-act]').forEach(b => b.addEventListener('click', ev => {{
    ev.stopPropagation();
    const card = [...(s.agentCards||[]), ...(s.roomExtras||[])].find(c => c.id === b.dataset.card);
    const a = card && card.actions.find(x => x.id === b.dataset.act);
    runEffect(a && a.effect, b.dataset.card);
  }}));
  sc.querySelectorAll('[data-fact]').forEach(b => b.addEventListener('click', () =>
    toast(b.dataset.fact === 'right' ? 'Thanks \\u2014 I\\u2019ll keep relying on that'
                                     : 'Tell me what\\u2019s wrong and I\\u2019ll relearn it')));
  sc.querySelectorAll('[data-check]').forEach(b => b.addEventListener('click', () => {{
    const k = b.dataset.check;
    const [cid, i] = k.split(':');
    const card = s.agentCards.find(c => c.id === cid);
    checks[k] = !((k in checks) ? checks[k] : card.items[+i].done);
    render();
  }}));

  document.querySelectorAll('.sbtn').forEach(b => b.classList.toggle('on', b.dataset.state === key));
  document.getElementById('job').textContent = JOBS[key];
  document.getElementById('mt').textContent = 'State ' + (ORDER.indexOf(key)+1) + ' \\u00B7 ' + LABELS[key];
  document.getElementById('mn').textContent = JOBS[key];
}}

/* ── report ───────────────────────────────────────────────── */
function lineChart(pts, opts){{
  const w = 300, h = 96, mx = Math.max(...pts) * 1.12, mn = 0, r = (mx - mn) || 1;
  const xy = i => [(i/(pts.length-1))*w, h - ((pts[i]-mn)/r)*h];
  const d = pts.map((_,i) => xy(i).join(',')).join(' ');
  let bands = '';
  (opts.bands || []).forEach(b => {{
    const x1 = (b.fromH/23)*w, x2 = (b.toH/23)*w;
    const fill = b.kind === 'night' ? 'rgba(110,123,200,.13)' : 'rgba(11,11,11,.055)';
    bands += `<rect x="${{x1}}" y="0" width="${{x2-x1}}" height="${{h}}" fill="${{fill}}"/>`;
  }});
  let peak = '';
  if (opts.peak){{
    const [px, py] = xy(opts.peak.hour);
    peak = `<line x1="${{px}}" y1="0" x2="${{px}}" y2="${{h}}" stroke="var(--bad)" stroke-width="1"
      stroke-dasharray="3 3" opacity=".55"/><circle cx="${{px}}" cy="${{py}}" r="3.4" fill="var(--bad)"/>`;
  }}
  return `<svg viewBox="0 0 ${{w}} ${{h}}" preserveAspectRatio="none" style="height:96px">
    ${{bands}}<polyline points="${{d}}" fill="none" stroke="var(--ink)" stroke-width="1.8"
      stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>${{peak}}</svg>`;
}}
function twoLine(a, b){{
  const w = 300, h = 96, mx = Math.max(...a, ...b) * 1.12;
  const p = s => s.map((v,i) => `${{(i/(s.length-1))*w}},${{h - (v/mx)*h}}`).join(' ');
  const area = `${{p(a)}} ${{w}},${{h}} 0,${{h}}`;
  return `<svg viewBox="0 0 ${{w}} ${{h}}" preserveAspectRatio="none" style="height:96px">
    <polygon points="${{area}}" fill="rgba(11,11,11,.06)"/>
    <polyline points="${{p(b)}}" fill="none" stroke="var(--good)" stroke-width="1.8"
      stroke-dasharray="4 3" vector-effect="non-scaling-stroke"/>
    <polyline points="${{p(a)}}" fill="none" stroke="var(--ink)" stroke-width="1.8"
      vector-effect="non-scaling-stroke"/></svg>`;
}}
function openReport(segment){{
  const s = F.states[key], R = F.report;
  const m = R.metrics[metric];
  const circ = 2 * Math.PI * 42;
  let h = `<div class="pager"><button aria-label="Previous day">&lsaquo;</button>
      <span>${{esc(R.day)}}</span><button aria-label="Next day" disabled style="opacity:.3">&rsaquo;</button></div>
    <div class="rhead">
      <div class="ring"><svg viewBox="0 0 98 98">
        <circle cx="49" cy="49" r="42" fill="none" stroke="rgba(11,11,11,.10)" stroke-width="7"/>
        <defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#6CCC7C"/><stop offset="1" stop-color="#AECC2A"/></linearGradient></defs>
        <circle cx="49" cy="49" r="42" fill="none" stroke="url(#rg)" stroke-width="7"
          stroke-linecap="round" stroke-dasharray="${{circ}}"
          stroke-dashoffset="${{circ*(1 - s.score.value/100)}}"/></svg>
        <b>${{s.score.value}}</b></div>
      <div class="rhead__t"><p>${{esc(R.narrative)}}</p>
        <p style="margin-top:8px"><span class="conf"><i style="background:var(${{s.score.confidence==='full'?'--good':'--moderate'}})"></i>
        ${{s.score.confidence === 'full' ? 'Full confidence' : 'Soft'}} &middot; ${{esc(s.score.confidenceReason)}}</span></p></div>
    </div>
    <div class="chips">${{Object.keys(R.metrics).map(k =>
      `<button class="mchip${{k===metric?' on':''}}" data-metric="${{k}}">${{esc(R.metrics[k].label)}}</button>`).join('')}}</div>
    <div class="chart"><p class="chart__t"><span>${{esc(m.label)}} &middot; today</span><span>peak ${{m.peak}} ${{esc(m.unit)}}</span></p>
      ${{lineChart(m.series, {{bands: R.bands, peak: R.peak}})}}
      <div class="chart__k">
        <span><i style="background:rgba(110,123,200,.5)"></i>Sealed window</span>
        <span><i style="background:rgba(11,11,11,.2)"></i>Power saver</span>
        <span><i style="background:var(--bad)"></i>${{esc(R.peak.label)}}</span></div></div>
    <div class="nightseg" id="segNight"><b>${{esc(R.night.label)}}</b>
      <p>${{esc(R.night.detail)}} &middot; outside peaked ${{R.night.outsidePeak}}, the room held ${{R.night.roomHeld}}. ${{esc(R.night.held)}}.</p>
      ${{sparkSVG(R.night.series, '#6E7BC8')}}</div>
    <p class="cl" style="margin-top:18px">What made the score</p>
    <div class="contrib">${{contribRows(s.score.contributors)}}</div>
    <p class="cl">From your history</p>
    <div class="chart" id="segEnergy"><p class="chart__t"><span>Fan effort vs. air need</span><span>${{esc(R.energy.saved)}}</span></p>
      ${{twoLine(R.energy.effort, R.energy.need)}}
      <div class="chart__k"><span><i style="background:var(--ink)"></i>Fan effort</span>
        <span><i style="background:var(--good)"></i>What the air needed</span></div>
      <p style="font-size:12.5px;line-height:1.5;color:var(--sec);margin:10px 0 0">${{esc(R.energy.caption)}}</p></div>
    <p class="rnote">Your weekly summary lands here too, and archives into report history.
      As you add rooms, each gets its own report with a home roll-up above it &mdash; same layout,
      one more level.</p>`;
  const body = document.getElementById('reportBody');
  body.innerHTML = h;
  body.querySelectorAll('[data-metric]').forEach(b => b.addEventListener('click', () => {{
    metric = b.dataset.metric; openReport();
  }}));
  document.getElementById('report').classList.add('on');
  if (segment === 'night')  document.getElementById('segNight').scrollIntoView({{block:'center'}});
  if (segment === 'energy') document.getElementById('segEnergy').scrollIntoView({{block:'center'}});
}}
function contribRows(cs){{
  const ALL = ['pm25','voc','humidity','noise','filter'];
  const NAMES = {{pm25:'Particulates', voc:'VOCs', humidity:'Humidity', noise:'Noise', filter:'Filter'}};
  const present = new Set(cs.map(c => c.key));
  let rows = cs.map(c => `<div class="crow">
      <span class="crow__l"><b>${{esc(c.label)}}</b><span>${{esc(c.rawValue)}} &middot; weight ${{Math.round(c.weight*100)}}%</span></span>
      <span class="crow__r"><span class="blabel" style="color:var(${{bandVar(c.band)}})">${{bandWord(c.band)}}</span>
        <span class="meter"><i style="width:${{Math.round(c.subScore*100)}}%;background:${{c.band === 'good' ? 'var(--gGrad)' : `var(${{bandVar(c.band)}})`}}"></i></span></span>
    </div>`).join('');
  // PRD §2.1 — a missing contributor renders 'unavailable', it does not score zero
  ALL.filter(k => !present.has(k)).forEach(k => {{
    rows += `<div class="crow unav">
      <span class="crow__l"><b>${{NAMES[k]}}</b><span>No reading &middot; weight redistributed</span></span>
      <span class="crow__r"><span class="blabel" style="color:var(--ter)">Unavailable</span>
        <span class="meter"></span></span></div>`;
  }});
  return rows;
}}

/* ── feed ─────────────────────────────────────────────────── */
function openFeed(){{
  const ICON = {{proposal:'\\u2726', done:'\\u2713', alert:'!', digest:'\\u25F7'}};
  let h = '', day = '';
  F.notifications.forEach(n => {{
    if (n.day !== day) {{ day = n.day; h += `<p class="fday">${{esc(day)}}</p>`; }}
    h += `<button class="frow" data-notif="${{n.id}}">
      <span class="fi">${{ICON[n.kind] || '\\u2022'}}</span>
      <span class="frow__t"><b>${{esc(n.title)}}</b>
        <span>${{esc(n.timestamp)}} &middot; ${{esc(n.typeLabel)}}</span></span>
      ${{n.unseen ? '<span class="udot"></span>' : ''}}</button>`;
  }});
  h += `<p class="rnote">Quiet hours follow the sleep window you set. Notifications are kept
    for 90 days. Per-category toggles live in Settings.</p>`;
  const body = document.getElementById('feedBody');
  body.innerHTML = h;
  body.querySelectorAll('[data-notif]').forEach(b => b.addEventListener('click', () => {{
    const n = F.notifications.find(x => x.id === b.dataset.notif);
    document.getElementById('feed').classList.remove('on');
    runEffect(n.effect, null);
  }}));
  document.getElementById('feed').classList.add('on');
}}

/* ── wiring ───────────────────────────────────────────────── */
document.querySelectorAll('.sbtn').forEach(b => b.addEventListener('click', () => {{
  key = b.dataset.state; dismissed = new Set(); checks = {{}}; render();
}}));
document.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', () =>
  document.getElementById(b.dataset.close).classList.remove('on')));
document.querySelectorAll('.sheet').forEach(s => s.addEventListener('click', ev => {{
  if (ev.target === s) s.classList.remove('on');
}}));
document.getElementById('oR').addEventListener('click', () => openReport());
document.getElementById('oN').addEventListener('click', openFeed);
document.getElementById('oE').addEventListener('click', () => openReport('energy'));
document.getElementById('oS').addEventListener('click', () => openReport('night'));
addEventListener('keydown', e => {{
  if (e.key === 'Escape') document.querySelectorAll('.sheet.on').forEach(s => s.classList.remove('on'));
  const n = parseInt(e.key, 10);
  if (n >= 1 && n <= 6) {{ key = ORDER[n-1]; dismissed = new Set(); checks = {{}}; render(); }}
}});
function fit(){{
  const p = document.getElementById('phone'), stage = document.querySelector('.stage');
  const meta = document.querySelector('.meta'), cs = getComputedStyle(stage);
  const padV = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
  const avail = Math.max(320, stage.clientHeight - padV - meta.offsetHeight - 14);
  const byW = (stage.clientWidth - 40) / 414;
  const sc = Math.min(1.05, avail / 872, byW);
  p.style.transform = 'scale(' + sc + ')';
  p.parentElement.style.height = (872 * sc) + 'px';
  p.parentElement.style.width  = (414 * sc) + 'px';
}}
addEventListener('resize', fit);
render(); fit();
</script>
</body></html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(BODY)
print(f"wrote {OUT.relative_to(ROOT)}  states={len(STATES)}  "
      f"cards={sum(len(s['agentCards'])+len(s.get('roomExtras',[])) for s in STATES.values())}  "
      f"{len(BODY)/1024/1024:.2f} MB")
