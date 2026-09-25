#!/usr/bin/env python3
"""
Build docs/research/refs-print.html  ->  NOMA-first-run-references.pdf

    python3 docs/research/build-refs.py
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
      --no-pdf-header-footer --print-to-pdf=docs/research/NOMA-first-run-references.pdf \
      docs/research/refs-print.html

REFERENCE TILES
---------------
Every competitor tile is a WIREFRAME REDRAWN from a Mobbin capture read on
2026-08-05 — layout, hierarchy and verbatim copy, not the pixels. Mobbin's
bitmaps could not be brought into this repo (see the provenance note in the
document itself). Each tile carries the exact app / flow / screen coordinates so
the original is one click away, and `refs/<slug>.png` is picked up automatically
if a real capture is ever dropped in.
"""
import base64, html, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT  = ROOT / "docs/research/refs-print.html"
REFS = ROOT / "docs/research/refs"
FDIR = ROOT / "src/fonts/google-sans-flex/static"

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = {k: b64(FDIR / v) for k, v in {
    "REG":  "GoogleSansFlex_24pt-Regular.ttf",
    "MED":  "GoogleSansFlex_24pt-Medium.ttf",
    "BOLD": "GoogleSansFlex_24pt-Bold.ttf"}.items()}

E = lambda s: html.escape(str(s), quote=False)
# tile captions are plain text: drop any inline emphasis markup before escaping
import re as _re
TX = lambda s: E(_re.sub(r"</?(b|i|em|strong|code)>", "", str(s)))

# ───────────────────────────────────────────────────────── wireframe tile
W, Hh = 150, 316          # tile viewBox

def wrap(txt, chars, maxlines):
    ls = textwrap.wrap(txt, chars)[:maxlines]
    if len(textwrap.wrap(txt, chars)) > maxlines and ls:
        ls[-1] = ls[-1][:chars - 1] + "…"
    return ls

def phone(title="", body="", media=0, rows=0, chips=None, btn=None, btn2=None,
          dots=0, dotAt=0, note="", big="", kb=0, pill=0, radios=0, sheet=0,
          check=0, num=""):
    """Return inline SVG for one redrawn reference screen."""
    p, y = [], 26
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{Hh-2}" rx="15" fill="#fff" stroke="#CFCAC1"/>')
    p.append(f'<rect x="12" y="9" width="16" height="3.4" rx="1.7" fill="#C9C3B8"/>')
    p.append(f'<rect x="{W-30}" y="9" width="18" height="3.4" rx="1.7" fill="#C9C3B8"/>')
    if sheet:
        p.append(f'<rect x="1" y="{Hh*0.30:.0f}" width="{W-2}" height="{Hh*0.70:.0f}" rx="15" fill="#FBFAF8" stroke="#E2DED6"/>')
        y = int(Hh * 0.30) + 18
    if media:
        p.append(f'<rect x="12" y="{y}" width="{W-24}" height="{media}" rx="6" fill="#EFEDE7"/>')
        for i, cx in enumerate((0.32, 0.5, 0.68)):
            p.append(f'<circle cx="{12+(W-24)*cx:.0f}" cy="{y+media/2:.0f}" r="{5-i%2}" fill="#D5D0C6"/>')
        y += media + 13
    if num:
        p.append(f'<text x="{W/2}" y="{y+34}" text-anchor="middle" font-size="46" font-weight="700" fill="#4D6747">{E(num)}</text>')
        y += 52
    if big:
        for ln in wrap(big, 15, 3):
            p.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-size="12.5" font-weight="700" fill="#222">{E(ln)}</text>'); y += 15
        y += 4
    if title:
        for ln in wrap(title, 24, 3):
            p.append(f'<text x="12" y="{y}" font-size="9.6" font-weight="700" fill="#222">{E(ln)}</text>'); y += 12
        y += 3
    if body:
        for ln in wrap(body, 33, 5):
            p.append(f'<text x="12" y="{y}" font-size="6.9" fill="#6E6A63">{E(ln)}</text>'); y += 9
        y += 5
    if pill:
        p.append(f'<rect x="12" y="{y}" width="70" height="17" rx="8.5" fill="#fff" stroke="#C9C3B8"/>')
        p.append(f'<circle cx="24" cy="{y+8.5}" r="4.5" fill="#D9D4CA"/>')
        p.append(f'<rect x="32" y="{y+6}" width="40" height="5" rx="2.5" fill="#CFCAC1"/>'); y += 26
    if chips:
        cx = 12
        for c in chips:
            w = 9 + len(c) * 3.5
            if cx + w > W - 12: cx = 12; y += 17
            p.append(f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="14" rx="7" fill="#F3F1EC" stroke="#DFDAD1"/>')
            p.append(f'<text x="{cx+w/2:.0f}" y="{y+9.4}" text-anchor="middle" font-size="5.9" fill="#4A463F">{E(c)}</text>')
            cx += w + 5
        y += 22
    for i in range(rows):
        p.append(f'<rect x="12" y="{y}" width="{W-24}" height="20" rx="5" fill="#F7F5F1"/>')
        p.append(f'<circle cx="24" cy="{y+10}" r="5.5" fill="#DFDAD1"/>')
        p.append(f'<rect x="34" y="{y+6}" width="{58-(i%3)*9}" height="4" rx="2" fill="#CFCAC1"/>')
        p.append(f'<rect x="34" y="{y+12}" width="{40-(i%2)*8}" height="3" rx="1.5" fill="#E1DCD3"/>')
        y += 24
    for i in range(radios):
        p.append(f'<circle cx="19" cy="{y+9}" r="5.2" fill="none" stroke="#B9B3A8" stroke-width="1.3"/>')
        if i == 0 and check: p.append(f'<circle cx="19" cy="{y+9}" r="2.6" fill="#4D6747"/>')
        p.append(f'<rect x="30" y="{y+4}" width="{86-i*12}" height="4" rx="2" fill="#CFCAC1"/>')
        p.append(f'<rect x="30" y="{y+11}" width="{62-i*10}" height="3" rx="1.5" fill="#E1DCD3"/>')
        y += 23
    if note:
        h = 11 + 8 * len(wrap(note, 34, 3))
        p.append(f'<rect x="12" y="{y}" width="2" height="{h}" fill="#4D6747"/>')
        yy = y + 9
        for ln in wrap(note, 34, 3):
            p.append(f'<text x="19" y="{yy}" font-size="6.2" fill="#5C5850">{E(ln)}</text>'); yy += 8
        y += h + 8
    if kb:
        p.append(f'<rect x="1" y="{Hh-92}" width="{W-2}" height="91" fill="#EDEBE6"/>')
        for r in range(3):
            for c in range(10 - r):
                p.append(f'<rect x="{6+c*14+r*6}" y="{Hh-84+r*20}" width="12" height="16" rx="2.5" fill="#fff"/>')
        p.append(f'<rect x="34" y="{Hh-24}" width="{W-68}" height="16" rx="2.5" fill="#fff"/>')
    if dots:
        cx0 = W/2 - (dots-1)*4.5
        for i in range(dots):
            p.append(f'<circle cx="{cx0+i*9:.1f}" cy="{Hh-40}" r="2.6" fill="{"#4D6747" if i==dotAt else "#D9D4CA"}"/>')
    if btn:
        by = Hh - 30 if not kb else Hh - 104
        p.append(f'<rect x="12" y="{by}" width="{W-24}" height="20" rx="10" fill="#4D6747"/>')
        p.append(f'<text x="{W/2}" y="{by+13.4}" text-anchor="middle" font-size="7.4" font-weight="700" fill="#fff">{E(btn)}</text>')
        if btn2:
            p.append(f'<text x="{W/2}" y="{by-7}" text-anchor="middle" font-size="7" fill="#6E6A63">{E(btn2)}</text>')
    elif btn2:
        p.append(f'<text x="{W/2}" y="{Hh-18}" text-anchor="middle" font-size="7" fill="#6E6A63">{E(btn2)}</text>')
    return f'<svg viewBox="0 0 {W} {Hh}" class="ph">' + "".join(p) + '</svg>'


REGISTRY = []

def tile(app, flow, screen, quote, verdict, kind, svg, slug=""):
    real = REFS / f"{slug}.png"
    REGISTRY.append({"slug": slug, "app": app, "flow": flow, "screen": screen,
                     "verdict": kind, "haveCapture": real.exists()})
    is_real = bool(slug) and real.exists()
    art = (f'<img class="ph" src="refs/{slug}.png" alt="">' if is_real else svg)
    mark = '' if is_real else '<p class="t__wf">redrawn wireframe</p>'
    return (f'<figure class="tile tile--{kind}{"" if is_real else " tile--wf"}">{art}{mark}'
            f'<figcaption><p class="t__app">{E(app)}</p>'
            f'<p class="t__flow">{E(flow)} <span>&rsaquo;</span> {E(screen)}</p>'
            f'<p class="t__q">{TX(quote)}</p>'
            f'<p class="t__v">{TX(verdict)}</p></figcaption></figure>')

# ───────────────────────────────────────────────────────── content
T = tile

STAGES = [
{"n":"A","name":"The first screen","fear":"“Is this going to be a whole evening?”",
 "job":"Earn one tap. Nothing else.",
 "noma":["<b>1.1 Welcome</b> — a warm room photograph, not a product shot. The purifier is furniture in the frame, not the subject. One line, one button, terms at the foot.",
         "The only screen in the flow allowed a full-bleed image and no explanation."],
 "rules":["A room, not a device. The product is the calm, not the box.",
          "One button. No secondary path competing with it.",
          "Terms as a footnote, never a modal."],
 "tiles":[
  T("IKEA Home smart","Onboarding","Splash","No headline at all — a lit room, a lamp, the logo.","Take. Sets a domestic register before a single word of UI.","good",
    phone(media=196, big="", body="", btn=None, btn2=""),"ikea-splash"),
  T("Google Home","Onboarding","Welcome home","“Control your content and devices from one place.”","Take the brevity. The illustration is generic; ours should be a room.","ok",
    phone(media=120, big="Welcome home", body="Control your content and devices from one place.", btn="Get started"),"ghome-welcome"),
  T("SmartThings","Onboarding","Control your devices","“View and control all your devices here. You can connect TVs, light bulbs, appliances, and more.”","Avoid — a feature list masquerading as a welcome, and it fires an OS permission dialog on top of itself.","bad",
    phone(big="Control your devices", body="View and control all your devices here. You can connect TVs, light bulbs, appliances, and more.", media=96, dots=4, dotAt=0, btn2="Skip   ·   Next"),"st-slide1"),
  T("Amazon Alexa","Onboarding","Sign in","Account first, before any statement of value.","Avoid. 28 screens follow.","bad",
    phone(title="Sign in", rows=2, btn="Continue", kb=0),"alexa-signin"),
  T("IKEA Home smart","Onboarding","Let’s start with your region","“We’ll provide local Terms & Conditions so you know what to expect from the app.”","Take the pattern, not the question: the very first ask already says why it is being asked.","good",
    phone(title="Let’s start with your region", body="We’ll provide local Terms & Conditions so you know what to expect from the app.", pill=1, btn="Next"),"ikea-region"),
 ]},

{"n":"B","name":"Value slides","fear":"“Just let me get on with it.”",
 "job":"Three claims, skippable, and never a promise we cannot render.",
 "noma":["<b>1.2 Three slides</b> — <i>One app, whole home</i> · <i>It runs itself</i> · <i>Your data stays home</i>. Dots plus a persistent Skip.",
         "<b>Slide 4 is cut.</b> The prototype promises <i>Home Score</i> here, before any device exists, and no zero-device Score state has ever been designed. Design that state or stop promising it.",
         "<i>Your data stays home</i> comes third on purpose — it lands immediately before the consent screens, so consent reads as confirmation rather than ambush."],
 "rules":["Never promise a surface whose empty state does not exist.",
          "Skip is visible on every slide, from the first.",
          "Three, not four. Every app in the set that ran four or more used the extras for features, not for reasons."],
 "tiles":[
  T("SmartThings","Onboarding","Slide 2 of 4","“Add services to your smart life — Do more with your devices and make your life smarter.”","Avoid. “Do more… smarter” says nothing; the slide exists to fill a carousel.","bad",
    phone(big="Add services to your smart life", body="Do more with your devices and make your life smarter.", media=90, dots=4, dotAt=1, btn2="Skip   ·   Next"),"st-slide2"),
  T("Google Home","Creating home","Welcome to the new Google Home","Three benefits, each a heading plus two lines, with an icon rail.","Structure is right, placement is wrong — it is a product-update note shown to someone who has never used the product.","ok",
    phone(media=88, big="Welcome to the new Google Home", rows=3, btn="Next"),"ghome-whatsnew"),
  T("IKEA Home smart","Connecting to a hub","What can a smart home do?","“There’s so much you can do with smart products, from better sleep habits to feeling safe and connected to your home from anywhere in the world.”","Take the register — outcomes (sleep, safety), not capabilities.","good",
    phone(media=104, title="What can a smart home do?", body="There’s so much you can do with smart products, from better sleep habits to feeling safe and connected to your home from anywhere in the world."),"ikea-whatcan"),
  T("IKEA Home smart","Connecting to a hub","A smart home in harmony","“The hub is the heart of the smart home and keeps everything running smoothly.”","Take. Names the one object the whole system depends on, in one sentence.","good",
    phone(media=100, title="A smart home in harmony", body="The hub is the heart of the smart home and keeps everything running smoothly. Remote access, notifications, scenes and more.", btn="Add hub now", btn2="Shop online"),"ikea-harmony"),
  T("SmartThings","Onboarding","Slide 1 + OS permission","The local-network dialog fires over slide 1.","Avoid, emphatically. Three system dialogs land before any value is shown. This is the anti-pattern our 1.x screens exist to avoid.","bad",
    phone(big="Control your devices", body="", media=70, sheet=1, title="“SmartThings” would like to find and connect to devices on your local network", btn2="Don’t Allow   ·   Allow"),"st-perm"),
 ]},

{"n":"C","name":"Account","fear":"“What are you going to do with this?”",
 "job":"Identity with the smallest possible surface.",
 "noma":["<b>1.3 Phone number</b> — “We’ll text you a code. Your number is how you get back in — nothing else.” India default, country selector present.",
         "<b>1.4 OTP</b> — auto-advances on the sixth digit. The resend timer runs from t=0, not from the first failure.",
         "<b>Finding: not one of the five reference apps uses phone + OTP.</b> All five are email-and-password account systems, three of them tied to a platform account (Google, Samsung, Amazon). For an Indian consumer product that is simply the wrong shape — phone-and-OTP is the local default and it removes the password entirely. We are deliberately unlike all five here, so there is no reference to copy: the bar is set by Indian fintech and commerce apps, not by these."],
 "rules":["The number is for sign-in and nothing else — say so on the screen.",
          "Resend visible immediately. A hidden resend turns a delayed SMS into a dead end.",
          "No password anywhere in the flow."],
 "tiles":[
  T("Google Home","Onboarding","Sign in","Google account, in an in-app browser at accounts.google.com.","Platform-account shortcut. Not available to us, and it puts a browser chrome bar in the middle of onboarding.","ok",
    phone(title="Sign in", body="with your Google Account. You’ll also sign in to Google services in your apps & Safari.", rows=1, btn="Next", kb=1),"ghome-signin"),
  T("SmartThings","Creating an account","Create your Samsung account","A wall of consent checkboxes inside account creation: service terms, specific terms, notice of financial incentives, plus three optional opt-ins.","Avoid. Consent bundled into signup is consent nobody reads. See stage D.","bad",
    phone(title="Create your Samsung account", body="Check our Privacy Notice to see how we manage your data.", radios=4, btn="Agree"),"st-account"),
  T("SmartThings","Onboarding","One account. Any device.","“One account. Any device. Just for you. Sign in to get started.”","Copy is good. The flow behind it is thirteen screens.","ok",
    phone(big="One account. Any device. Just for you.", body="Sign in to get started.", rows=1, btn="Sign in"),"st-oneaccount"),
  T("Amazon Alexa","Adding a family member","Welcome, Sam","“Let’s get started. First, agree to the profile terms and conditions below to begin.”","Take for stage O — the new member consents for themselves, on the same handset.","good",
    phone(media=0, big="Welcome  ·  Sam", body="Let’s get started. First, agree to the profile terms and conditions below to begin.", btn="Agree and Continue"),"alexa-welcome-sam"),
  T("Apple Home","Home settings","No account step at all","Home lives inside the Apple ID the phone already has.","The ceiling: zero account screens. We cannot reach it, but it is the direction to push — fewest screens between install and a live reading.","good",
    phone(title="Home Settings", rows=4, body=""),"apple-homesettings"),
 ]},

{"n":"D","name":"Consent","fear":"“Am I signing something?”",
 "job":"Satisfy the DPDP Act 2023 honestly, on its own screens, with nothing pre-ticked.",
 "noma":["<b>1.5 Privacy</b> — scrollable, and <b>Continue stays disabled until the reader reaches the bottom</b>.",
         "It must state the narrowing that <code>memory/architecture/ai-integration.md</code> §10 flags as unresolved: personal and biometric data stays on the device; <i>public ambient data — outdoor AQI and forecast — is fetched from the network</i>. “Your data never leaves home” without that sentence is a compliance exposure, not a tagline.",
         "<b>1.6 Analytics</b> — two options, <b>neither pre-selected</b>, each with a Read more expander. Declining degrades nothing. ⚠ Blocked by C-11: until it closes, ship this screen with the analytics option <i>absent</i>, not defaulted."],
 "rules":["Consent gets its own screen. Never bundled into signup.",
          "Nothing pre-ticked, and refusal costs the user nothing.",
          "Gate Continue on having reached the bottom — it is the only honest way to claim it was read."],
 "tiles":[
  T("IKEA Home smart","Onboarding","Privacy Statement","“Thanks for trusting IKEA of Sweden AB with your personal data.” Then: what is collected, what it is used for, and the seven data rights, in plain sentences.","Take wholesale. Next is greyed until scrolled to the bottom. Best consent screen in the set.","good",
    phone(media=64, title="Privacy Statement", body="Thanks for trusting IKEA of Sweden AB with your personal data. We rely on cookies and other technologies to collect personal data, as detailed in our cookie statement.", btn2="Next (disabled)"),"ikea-privacy"),
  T("IKEA Home smart","Onboarding","Consent for Analytics","“Yes, I consent to IKEA’s usage of cookies and analysis of personal data…” / “No, I don’t consent…”","Take. Two explicit checkboxes, neither pre-ticked, each with a Read more expander. This is the DPDP shape.","good",
    phone(media=60, title="Consent for Analytics", body="We, IKEA of Sweden AB, always strive to improve the System and Application to give you the best possible experience", radios=2, btn2="Next (disabled)"),"ikea-analytics"),
  T("IKEA Home smart","Onboarding","Consent — chosen","Ticking a box enables Next.","Take. The state change is the whole affordance; no dark pattern needed.","good",
    phone(media=60, title="Consent for Analytics", body="We, IKEA of Sweden AB, always strive to improve the System and Application", radios=2, check=1, btn="Next"),"ikea-analytics2"),
  T("SmartThings","Creating an account","Optional opt-ins","“Turn on Customization Service (optional)”, “Get special offers and product news”, “Improve personalised ads”.","Avoid. Three marketing opt-ins wearing the same visual weight as the legal terms.","bad",
    phone(title="Check all the following options", radios=3, btn="Agree"),"st-optins"),
  T("Google Home","Privacy","Removing saved WiFi and home address","A settings screen that lets you withdraw data given during setup.","Take as an obligation, not a nicety — DPDP requires erasure, and we have no surface for it (scope ledger).","good",
    phone(title="Privacy", rows=4, btn2="Remove"),"ghome-privacy"),
 ]},

{"n":"E","name":"Naming the home","fear":"“I don’t know what to call it.”",
 "job":"Get a label without making the user compose one.",
 "noma":["<b>1.7 Name your home</b> — “Give your home a name — so you can tell it apart later.” Chips: <code>Home</code> · <code>My home</code> · <code>Mumbai flat</code> · <code>Mum &amp; Dad’s</code>. 0/25 counter.",
         "The chips are the interface; the text field is the fallback. <code>Mum &amp; Dad’s</code> is there for P1, who is often setting up a home she does not live in.",
         "<b>No address.</b> Google asks for one before any device exists. We have no use for a street address at this point and asking for it spends trust we have not earned."],
 "rules":["Offer names, don’t demand one.",
          "Never ask for anything we cannot immediately justify — especially an address.",
          "A character counter, so a long name fails before it is submitted, not after."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","Give your home a name","Field plus three chips: Home · My home · Our place. 0/25.","Take exactly. Chips remove the blank-page problem in one move.","good",
    phone(title="Give your home a name", chips=["Home","My home","Our place"], rows=0, btn2="Next (disabled)", kb=1),"ikea-name"),
  T("Google Home","Creating home","Name your home","“Choose a nickname for this home to help identify it later.” 0/20.","Take the subtitle — it states the reason. No chips, so the user starts from nothing.","ok",
    phone(title="Name your home", body="Choose a nickname for this home to help identify it later", rows=1, btn2="Next (disabled)"),"ghome-name"),
  T("Google Home","Creating home","Home address","“Your home address will be used for things like directions.” Country, two address lines, town, state, postcode. Skip present.","Reason stated well; ask is wrong this early. Note Skip is the only thing rescuing it.","bad",
    phone(title="Home address", body="Your home address will be used for things like directions.", rows=4, btn="Next", btn2="Skip"),"ghome-address"),
  T("SmartThings","Adding a device","Set the location name and geolocation","“Set where this location is so that you can use more SmartThings features.”","Vague benefit (“more features”) for a precise ask. If we cannot name the feature, we should not ask.","bad",
    phone(media=78, title="Set the location name and geolocation", body="Set where this location is so that you can use more SmartThings features.", rows=2, dots=3, dotAt=1, btn2="Previous   ·   Next"),"st-location"),
  T("Apple Home","Changing Home name","Add Home","Name field, then People, then Home Hubs — home identity and household on one settings sheet.","Useful later, wrong for first run. We keep household entirely out of step 1.","ok",
    phone(title="Add Home", rows=4, btn2="Done"),"apple-addhome"),
 ]},

{"n":"F","name":"Choosing what to set up","fear":"“Will it even recognise my thing?”",
 "job":"Show the four device types we actually support and get out of the way.",
 "noma":["<b>2.1 Which device?</b> — Camera · Lock · Purifier · Vacuum (<code>firstRunDeviceTypes</code>). Purifier is highlighted, not pre-selected: P4 arrives with a camera.",
         "No brand search, no partner directory, no “works with” taxonomy. We make the hardware; a search field here would imply an ecosystem we do not have and cannot support."],
 "rules":["Four types, as tiles. Not a searchable list.",
          "Never show a category we cannot complete.",
          "The empty Devices state must invite, not apologise."],
 "tiles":[
  T("Google Home","Adding a device","Devices — empty","“When any household member adds a device, it appears here.” + Add device.","Take the sentence. It explains the emptiness <i>and</i> hints that the home is shared.","good",
    phone(media=104, title="Devices", body="When any household member adds a device, it appears here", btn="+ Add device"),"ghome-empty"),
  T("Google Home","Adding a device","Choose a device","Three routes: Matter-enabled device · Google Nest or partner device · Works with Google Home.","Avoid for us. Three abstractions the user must self-diagnose before they can start.","bad",
    phone(sheet=1, title="Choose a device", rows=3, body=""),"ghome-choose"),
  T("Amazon Alexa","Adding a device (speaker)","Which device would you like to set up?","Brand shortcuts (echo, ring, blink, matter, kasa) then All Devices by type.","Marketplace shape. Correct for Amazon, wrong for a single-brand product.","ok",
    phone(title="Which device would you like to set up?", rows=4, body=""),"alexa-which"),
  T("Apple Home","Adding an accessory (Bridge)","Add Accessory","“Scan code or hold iPhone near the accessory.” Two how-to rows: Scan a Setup Code · Hold iPhone Near Accessory.","Take the two-route framing — one visual, one proximity — and the fact that both are explained on the same screen.","good",
    phone(sheet=1, title="Add Accessory", body="Scan code or hold iPhone near the accessory.", rows=2),"apple-addacc"),
  T("Apple Home","Home","The + menu","Add Accessory · Add Scene · Add Automation · Add Room · Add People · Add New Home.","Note where Add People sits: a peer of Add Room, in a menu, reached when the user goes looking. Never in first run.","good",
    phone(media=60, title="", rows=5, body=""),"apple-plusmenu"),
 ]},

{"n":"G","name":"Before the first instruction","fear":"“Am I about to get stuck halfway?”",
 "job":"Answer the question nobody asks out loud: do I have everything I need?",
 "noma":["<b>2.2 Here’s what you’ll need</b> — a 2×2 grid of line drawings: <b>Purifier</b> · <b>Power socket</b> · <b>Your Wi-Fi password</b> · <b>About 5 minutes</b>. Then <i>I’ve got these</i>.",
         "This is the single most important screen in the flow, and it is the one most likely to be cut as “an extra tap”. Putting the Wi-Fi password and the five minutes in the same grid as the physical objects is deliberate: those are the two things people discover they do not have three screens too late.",
         "Only IKEA does this. It is the cheapest anxiety reduction available to us."],
 "rules":["Inventory before instruction. Always.",
          "Include the non-physical prerequisites — credentials and time — as items.",
          "The button confirms readiness (“I’ve got these”), it does not just advance."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","Let’s get started!","“Here are the parts you’ll need:” Hub · Cables and plug · Power · Router, as four line drawings. Then Get started.","Take wholesale. The best screen in 130.","good",
    phone(title="Let’s get started!", body="Here are the parts you’ll need:", rows=4, btn="Get started"),"ikea-parts"),
  T("Amazon Alexa","Adding a device (speaker)","Is your Echo Dot plugged in and displaying an orange light?","“Once your Echo Dot is plugged in, the light will turn orange after about a minute.” [No] [Yes]","Take the yes/no state check — it gives the app a reliable branch and tells the user exactly what to look at.","good",
    phone(media=96, title="Is your Echo Dot plugged in and displaying an orange light?", body="Once your Echo Dot is plugged in, the light will turn orange after about a minute.", btn="Yes", btn2="No"),"alexa-orange"),
  T("SmartThings","Adding a device","Add devices to use at this location","An illustrated house, a three-dot stepper, Previous / Next.","Stepper is right; the screen carries no preparation at all. Straight into scanning.","ok",
    phone(media=96, title="Add devices to use at this location.", dots=3, dotAt=0, btn2="Previous   ·   Next"),"st-adddevices"),
  T("SmartThings","Adding a device","Getting everything ready","“Now ready to add your device. 0%”","A progress bar for setup preparation the user cannot influence. Ours names what is happening instead.","ok",
    phone(media=104, big="Getting everything ready", body="Now ready to add your device."),"st-ready"),
  T("IKEA Home smart","Connecting to a hub","Welcome home — empty","Editorial photo card plus “Add a hub now →”.","Take. An empty home that reads as an invitation, not an error.","good",
    phone(media=110, title="Welcome home", body="", btn="Add a hub now"),"ikea-welcomehome"),
 ]},

{"n":"H","name":"The physical steps","fear":"“I’m going to do this wrong.”",
 "job":"One instruction per screen, and let the user set the pace.",
 "noma":["<b>2.3 Plug it in</b> — “Plug the purifier in and switch it on.”",
         "<b>2.4 Wait for the light</b> — “The ring on top will pulse slowly when it’s ready to pair. It can take up to a minute.” Then <b>[The light is pulsing]</b> — the user confirms, never a timer.",
         "With an inline note on 2.4 and nowhere else: <b>“Already set up by someone else?”</b> — “If the ring is steady instead of pulsing, it’s already paired to another home.”",
         "A persistent four-dot stepper runs across the connect phase, and <b>there is only one stepper</b>. SmartThings resets its progress indicator twice inside one flow, which makes progress unreadable."],
 "rules":["One instruction, one illustration, at most two lines of body.",
          "The user confirms the physical world. A timer that advances on its own is a guess.",
          "One progress indicator per flow, never re-based.",
          "Divergent situations get one inline note, on the screen where they diverge."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","Connect the ethernet cable to the hub and your router","“The router will connect the hub to your home internet network.”","Take. Instruction, then the reason, then a drawing that shows exactly which ports.","good",
    phone(media=96, title="Connect the ethernet cable to the hub and your router", body="The router will connect the hub to your home internet network.", dots=3, dotAt=0, btn="→"),"ikea-ethernet"),
  T("IKEA Home smart","Connecting to a hub","Connect the power cable to the hub and plug it in","“The hub will start up as soon as the ethernet cable and power cable are connected.”","Take. Sets the expectation for what happens next before it happens.","good",
    phone(media=96, title="Connect the power cable to the hub and plug it in", body="The hub will start up as soon as the ethernet cable and power cable are connected.", dots=3, dotAt=1, btn="→"),"ikea-power"),
  T("IKEA Home smart","Connecting to a hub","Wait for the ring light to make a full circle","“It may take a few minutes for the ring light to completely fill.” Inline note: “Are you joining someone’s hub? If the hub is already set up, you will see a solid centre light instead of the ring.”","Take both — the named wait and the one inline note for the other situation. This is our 2.4 almost verbatim.","good",
    phone(media=80, title="Wait for the ring light to make a full circle", body="It may take a few minutes for the ring light to completely fill.", note="Are you joining someone’s hub? If the hub is already set up, you will see a solid centre light instead of the ring.", dots=3, dotAt=2, btn="Next"),"ikea-ring"),
  T("IKEA Home smart","Connecting to a hub","The ring light will pulse when the hub is ready","Button: “My hub is ready”.","Take. The user decides when to proceed. Our 2.4 button is this button.","good",
    phone(media=90, title="The ring light will pulse when the hub is ready", body="You will see a solid centre light instead of a ring if the hub was already up and running.", btn="My hub is ready"),"ikea-pulse"),
  T("IKEA Home smart","Connecting to a hub","Time to confirm your hub!","“Press the Action button on the back of the hub to confirm it as part of your smart home system.”","Take as a model for proof-of-possession — a physical press proves the person is in the room with the device.","good",
    phone(media=90, title="Time to confirm your hub!", body="Press the Action button on the back of the hub to confirm it as part of your smart home system."),"ikea-confirm"),
 ]},

{"n":"I","name":"Discovery and the permission","fear":"“Why does it want that?”",
 "job":"Ask for Bluetooth at the exact moment it is used, with the reason visible behind the dialog.",
 "noma":["<b>2.5 Looking for your purifier</b> — “Hold your phone close — this takes a moment.”",
         "<b>The Bluetooth prompt fires here and nowhere earlier</b>, one beat before the search, with the reason on screen behind it. Notification priming moves to 2.11, where there is something to be notified about.",
         "<b>2.6 Found it</b> — “Is this the one?” with <b>Identify</b> alongside, which blinks the ring. This matters the moment a household owns two purifiers. ⚠ O-9: no document confirms the hardware can do this."],
 "rules":["Permission at the point of use, never in a fixed onboarding slot.",
          "The reason stays visible behind the system dialog.",
          "Confirm identity before naming. Identify, then name."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","Looking for nearby hubs…","The OS local-network dialog fires over this screen.","Take the timing exactly. The user has just been told what is being looked for, so the dialog is self-explaining.","good",
    phone(sheet=1, big="Looking for nearby hubs…", title="“Home smart” would like to find and connect to devices on your local network", btn2="Don’t Allow   ·   Allow"),"ikea-looking"),
  T("Amazon Alexa","Adding a device (speaker)","Searching for device…","“Make sure your device is nearby, plugged in, and in pairing mode.”","Take — the wait screen restates the three preconditions, so a failure is already half-diagnosed.","good",
    phone(media=64, big="Searching for device…", body="Make sure your device is nearby, plugged in, and in pairing mode."),"alexa-searching"),
  T("Apple Home","Adding an accessory (Bridge)","Bridge — found","Device name, then “Add to ‘Apple Home’”.","Minimal and good. But no way to confirm <i>which</i> device — see the next tile.","ok",
    phone(media=96, big="Bridge", btn="Add to “Apple Home”"),"apple-bridge"),
  T("Apple Home","Adding an accessory (Bridge)","Bridge Location + Identify","A room picker wheel of suggestions, Continue, and a secondary action: <b>Identify</b>.","Take Identify. One word that removes an entire class of “did I just name the wrong one” doubt.","good",
    phone(sheet=1, title="Bridge Location", rows=3, btn="Continue", btn2="Identify"),"apple-identify"),
  T("SmartThings","Adding a device","Connecting to device","A four-dot stage indicator, illustrated device, “Make sure your phone or tablet is near your Screen so they can connect.”","Stage indicator is good. But this is the <i>second</i> stepper in the same flow — the three-dot one preceded it — so progress becomes unreadable.","bad",
    phone(media=96, big="Connecting to device", body="Make sure your phone or tablet is near your Screen so they can connect.", dots=4, dotAt=0),"st-connecting"),
 ]},

{"n":"J","name":"Wi-Fi","fear":"“This is where it always breaks.”",
 "job":"Remove the single most common smart-home setup failure before it happens.",
 "noma":["<b>2.7 Pick your Wi-Fi</b> — “Live air data and automations need a connection.” <b>5 GHz SSIDs are hidden, and the app says so</b>: a line under the list reads “Only 2.4 GHz networks are shown. Your purifier can’t use 5 GHz.”",
         "Hiding without explaining is a defect, not a simplification — a user who cannot find their network name needs to know why.",
         "<b>2.8 Password</b> — show/hide toggle. <b>No “save my password to the cloud” checkbox.</b> That is Alexa’s pattern and it contradicts the privacy posture."],
 "rules":["Hide what the hardware cannot join, and say that you did.",
          "Never offer to store a Wi-Fi password off-device.",
          "A wrong password is an inline error that keeps the SSID and the focus — never a full-screen failure."],
 "tiles":[
  T("Amazon Alexa","Setting up Wi-Fi","Select your wifi network","List of SSIDs with a “Refresh networks” action.","Take Refresh — a network that was not broadcasting a second ago is the most common recoverable case.","good",
    phone(title="Select your wifi network", body="Refresh networks", rows=4),"alexa-wifi"),
  T("Amazon Alexa","Setting up Wi-Fi","Enter wifi password","Checkbox: “Save your password to Amazon and allow eligible devices to use it during setup…” plus a Password Tips link.","<b>Avoid the checkbox.</b> Take Password Tips — the one place a hint belongs.","bad",
    phone(title="Enter wifi password", rows=1, radios=1, btn="Connect", kb=0),"alexa-wifipass"),
  T("Amazon Alexa","Setting up Wi-Fi","Connecting to wifi → Connected","Two states, one icon, no ambiguity.","Take. The success state is a full screen, not a toast, because it is the moment the anxiety ends.","good",
    phone(media=0, num="", big="Connected to wifi", body=""),"alexa-wificonn"),
  T("SmartThings","Adding a device","Verify your device — PIN","“Check the PIN shown on your Screen, then enter it below.”","Correct for a TV with a display. Our purifier has a ring light and no screen, so proof-of-possession is a button press (stage H), not a code.","ok",
    phone(media=80, title="Verify your device", body="Check the PIN shown on your Screen, then enter it below.", rows=1, dots=4, dotAt=1, kb=0),"st-pin"),
  T("Google Home","Privacy","Saved WiFi","Setup Wi-Fi credentials are stored and listed, with removal.","Take as an obligation: whatever we keep must be visible and removable. We keep the password on the device only.","good",
    phone(title="Saved networks", rows=3, btn2="Remove"),"ghome-savedwifi"),
 ]},

{"n":"K","name":"Where it lives","fear":"none — this is the easy one, don’t make it hard",
 "job":"One tap, with India-appropriate options.",
 "noma":["<b>2.9 Where is it?</b> — room presets including <b>Pooja Room</b>, with free text below the chips. “Naming the room lets us compare against the right outdoor sensor.”",
         "⚠ <b>C-12 is open</b>: two room-preset lists exist in the prototypes — 8 items and 11 items. The 11-item list is the India-appropriate one; the 8-item list omits Pooja Room. This screen cannot be finalised until that closes."],
 "rules":["Presets first, free text second.",
          "The list must be written for Indian homes, not translated into them.",
          "State why the room matters — ours actually changes the data."],
 "tiles":[
  T("Apple Home","Adding an accessory (Bridge)","Bridge Location","A wheel of suggested rooms: Bedroom (Suggested) · Living Room (Suggested) · Dining Room · Kitchen · Entrance · Bathroom · Hallway · Garage.","Take “(Suggested)” — it marks the list as a shortcut rather than a fixed taxonomy. Note the list is entirely Western.","good",
    phone(sheet=1, title="Bridge Location", rows=4, btn="Continue", btn2="Identify"),"apple-room"),
  T("Google Home","Adding new devices to room","Devices, groups and rooms","Rooms as a settings list with device counts.","Structure for later, not a setup step. Ours is a chip grid inside the flow.","ok",
    phone(title="Devices, groups & rooms", rows=4, body=""),"ghome-rooms"),
  T("IKEA Home smart","Creating a room","Create a room","Name plus an icon picker.","Icon picking during first-device setup is a decision too many. Defer it.","bad",
    phone(title="Create a room", rows=2, chips=["Kitchen","Bedroom","Hall"], btn="Next"),"ikea-room"),
  T("Apple Home","Adding a new scene (custom)","Choose Icon","A full grid of icons and twelve colours.","Deliberate counter-example: this is what stage K must not become.","bad",
    phone(title="Choose Icon", media=56, rows=3, btn2="Cancel   ·   Done"),"apple-icon"),
  T("Google Home","Creating home","Choose a home","“You’ll be able to control the devices and services in this home.”","Relevant to multi-home, which we have data for and no flow (scope ledger). Out of first run.","ok",
    phone(title="Choose a home", body="You’ll be able to control the devices and services in this home.", rows=2, btn="Next"),"ghome-choosehome"),
 ]},

{"n":"L","name":"Waiting, and the update","fear":"“Is it frozen? Can I put the phone down?”",
 "job":"Name the wait, bound it, and release the user from it.",
 "noma":["<b>2.10 Connecting</b> — progress with named stages: <code>Joining your Wi-Fi</code> → <code>Taking a first reading</code> → <code>Almost there</code>. Never a bare spinner.",
         "<b>2.11 Updating</b> (conditional) — “This takes a few minutes — please leave the purifier plugged in. <b>You’re welcome to close the app while it finishes; we’ll notify you when it’s done.</b>”",
         "That last sentence is where notification permission earns itself, which is why priming moved here from <code>J-ONBOARD-06</code>."],
 "rules":["A spinner with no label is a bug.",
          "State the duration before the wait, not during it.",
          "Release the user. If they can leave, tell them they can leave."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","We found your hub!","“Let’s update to the latest software. Please don’t unplug your hub. <b>You are welcome to close the app while waiting.</b>”","Take the whole screen, and especially that last line. The most humane sentence in 130 screens.","good",
    phone(media=90, title="We found your hub!", body="Let’s update to the latest software. Please don’t unplug your hub. You are welcome to close the app while waiting.", btn2="Downloading  0%"),"ikea-found"),
  T("IKEA Home smart","Connecting to a hub","Rebooting","“A few minutes remaining.”","Take. A named phase plus a bounded estimate, so a two-minute silence is not a failure.","good",
    phone(media=90, big="Rebooting", body="A few minutes remaining."),"ikea-reboot"),
  T("IKEA Home smart","Connecting to a hub","Update complete","“Your DIRIGERA hub has the latest software and is ready to use.”","Take. Closes the loop explicitly rather than just moving on.","good",
    phone(media=90, title="Update complete", body="Your DIRIGERA hub has the latest software and is ready to use.", btn="Next"),"ikea-updated"),
  T("SmartThings","Adding a device","Registering your device","“Your Screen is being registered to your Samsung account.”","Honest about what is happening, but it is an account operation surfaced to someone who wanted a working TV.","ok",
    phone(media=90, big="Registering your device", body="Your Screen is being registered to your Samsung account.", dots=4, dotAt=2),"st-registering"),
  T("SmartThings","Adding a device","Processing…","A grey “Processing…” chip over an illustration, repeated across four consecutive screens.","Avoid. Four near-identical waits with no named stage is how a flow starts to feel broken.","bad",
    phone(media=96, title="Add devices to use at this location.", body="Processing…", dots=3, dotAt=1),"st-processing"),
 ]},

{"n":"M","name":"The reveal","fear":"gone — this is the payoff",
 "job":"Deliver J-WEEK-01. One number, the street’s number, one sentence.",
 "noma":["<b>2.12 First reading</b> — <b>no confetti, no “Setup complete!”, no feature tour.</b> “Your bedroom is at 34. Outside, it’s 168. It’s already cleaning.” Then the agent’s first and only Day-1 line, and nothing else.",
         "Motion: the card arrives on <code>MO-POP</code>, the dial settles with <code>standard</code> — <b>never <code>spring</code></b>, because it is an ambient reading (<code>.claude/rules/motion.md</code> gate 4) — and <code>MO-BREATHE</code> starts only after the number has settled.",
         "<b>No competitor has an equivalent screen.</b> All five end setup with a device tile in a list. That is the whole opportunity: air is invisible, so the first reading is the product’s only chance at a visceral moment."],
 "rules":["End on evidence, not on congratulations.",
          "The number is the hero. Nothing else on the screen competes.",
          "Ambient data never bounces."],
 "tiles":[
  T("Google Home","Creating home","Choose your favourites","“Favourites are personal and only appear in your app.” A checklist, then Home.","Avoid as an ending. Setup finishes on a configuration chore.","bad",
    phone(title="Choose your favourites", body="Favourites are personal and only appear in your app", rows=2, btn2="Cancel   ·   Save"),"ghome-favs"),
  T("Apple Home","Home","My Home — after adding","A device tile appears in a grid over a wallpaper.","The category default: setup ends and you are looking at a switch. Nothing has been revealed.","ok",
    phone(media=70, title="My Home", rows=2),"apple-home"),
  T("IKEA Home smart","Connecting to a hub","Welcome home — hub added","The hub appears; the app returns to Home.","Same shape. Excellent journey, flat ending.","ok",
    phone(media=100, title="Welcome home", rows=1),"ikea-added"),
  T("SmartThings","Adding a device","Favorites — where setup begins and ends","A QR-code prompt and an empty grid. Setup starts here and returns here.","Same again, five for five: the arc closes on a grid of controls. Nothing about the home has been revealed.","ok",
    phone(title="Favorites", rows=3, media=0),"st-added"),
  T("NOMA — proposed","F-SETUP · 2.12","First reading","“Your bedroom is at 34. Outside, it’s 168. It’s already cleaning.”","Ours. The one screen in this document with no reference behind it, because nobody in the category has anything to reveal.","noma",
    phone(num="34", body="Outside, it’s 168. It’s already cleaning.", media=0),"noma-reveal"),
 ]},

{"n":"N","name":"When it breaks","fear":"“I’ve bought a brick.”",
 "job":"Eight designed failures. The device is always the subject of the sentence.",
 "noma":["Absent from all four NOMA prototypes and from the scope ledger’s own admission. <b>A setup flow without a not-found state is not a setup flow.</b>",
         "The eight: <b>not found</b> · <b>ring never pulses</b> · <b>already paired elsewhere</b> · <b>only 5 GHz found</b> · <b>wrong password</b> · <b>on Wi-Fi but no internet</b> · <b>timeout</b> · <b>Bluetooth declined</b>.",
         "Full copy for each is in <code>docs/features/first-run/prd.md</code> §2e. Two structural rules from the references: the primary action is always <i>Try again</i>, and the secondary is always <i>help</i> — never <i>Cancel</i>, which strands the user with an unpaired device.",
         "⚠ <b>O-6</b>: <code>colors.status</code> is <code>null</code> and green cannot carry “bad”, so these screens ship neutral until a warning token exists."],
 "rules":["Name the device, never blame the user.",
          "Numbered tips, ordered by likelihood.",
          "Try again is primary; help is secondary; Cancel is not an option.",
          "Every failure has a route forward that is not “start over”."],
 "tiles":[
  T("IKEA Home smart","Connecting to a hub","We didn’t find any hubs","“Sometimes the hub needs a little nudge to get going. You can get help from common issues and solutions or try to search again.” [I need help] [Try again]","Take wholesale — including “the hub needs a nudge”, which puts the fault on the object.","good",
    phone(media=90, title="We didn’t find any hubs", body="Sometimes the hub needs a little nudge to get going. You can get help from common issues and solutions or try to search again.", btn="Try again", btn2="I need help"),"ikea-notfound"),
  T("IKEA Home smart","View help","Common issues and solutions","An accordion: “There are no lights on my hub” · “The ring light stopped filling” · “The hub only has a small centre light.”","Take. Written as the symptoms a person can actually observe, not as error codes.","good",
    phone(title="Common issues and solutions", rows=4, body=""),"ikea-issues"),
  T("Amazon Alexa","Adding a device (speaker)","Device not discovered","“Here are a few tips: 1. Make sure you stay within 10ft of your Echo device. 2. Check that your device is plugged in. 3. If you don’t see an orange light, learn how to enter setup mode.” [Try Again]","Take the numbered, concrete tips — a distance in feet beats “move closer”.","good",
    phone(title="Device not discovered", body="Here are a few tips:", rows=3, btn="Try Again"),"alexa-notfound"),
  T("Amazon Alexa","Adding a device (speaker)","No orange light? Try this","Two reset procedures, by button type, with hold durations. Plus “Need more help?”.","Take. This is the <i>No</i> branch of the stage-G state check, designed rather than dead-ended.","good",
    phone(media=80, title="No orange light? Try this:", body="If your device has a round action button, press and hold it for approximately 15 seconds.", btn="Continue", btn2="Need more help?"),"alexa-noorange"),
  T("SmartThings","Adding a device","Device already registered","A title, a help icon, and nothing else.","<b>Right state, no content.</b> The one “already claimed” screen in the set, and it tells the user nothing about how to release the device. Ours must explain that resetting removes it from the other home.","bad",
    phone(title="Device already registered", body="", dots=4, dotAt=0),"st-already"),
 ]},

{"n":"O","name":"Offering the household","fear":"“Am I about to give someone control of my house?”",
 "job":"Offer it at the moment of pride, never as a gate. Then handle both the person in the room and the person who isn’t.",
 "noma":["<b>3.0 The offer</b> — a dismissible card on Home, after the reveal: “Who else lives here? Add the people at home so they can see the air and control the purifier — <i>without your phone</i>.” <b>[Add someone]</b> · <i>Later</i>.",
         "Framed as the other person’s convenience, not as an admin task. For P2 (Ravi &amp; Lakshmi) this is the point of the product: they should not have to ask Asha to turn the fan down.",
         "<b>3.1 Are they here right now?</b> — <b>[They’re with me]</b> → hand-the-phone path · <b>[Send them a link]</b> → remote path. P1 is in Bangalore; P2 is in the room. Both, on one screen.",
         "<b>3.7</b> On the co-present path the new member <b>accepts their own terms and sets their own sign-in on the same handset</b>. Their consent is theirs; the owner cannot give it for them."],
 "rules":["Never a gate. Dismissible, and it does not return in the same session.",
          "Two enrolment paths, co-present first.",
          "The member consents for themselves, always."],
 "tiles":[
  T("Amazon Alexa","Adding a family member","Hand your phone to Sam","“Alexa will help get them started by learning to recognize their voice. If they are not with you at the moment, you can share these instructions with them.” SHARE INSTRUCTIONS · [Continue]","Take wholesale. Co-present and remote on one screen, co-present as the default. Our 3.1 is this idea, moved earlier.","good",
    phone(media=64, big="Hand your phone to Sam", body="Alexa will help get them started by learning to recognize their voice. If they are not with you at the moment, you can share these instructions with them.", btn="Continue", btn2="Share instructions"),"alexa-handphone"),
  T("Google Home","Inviting a person","Invite person","“Type a name or email address”, with a Suggestions list from contacts.","Contact suggestions are fine. But there is no “are they here?” question — the flow assumes the other person is elsewhere.","ok",
    phone(title="Invite person", body="Type a name or email address", rows=4),"ghome-invite"),
  T("Apple Home","Home settings","People — Invite People…","“All members in the shared home can control and see updates from accessories. People invited to your home will need to be on the latest software to accept invitations.”","Take the disclosure sentence placed <i>next to</i> the invite control, before it is tapped.","good",
    phone(title="Home Settings", body="People", rows=3, btn2="Invite People…"),"apple-people"),
  T("Amazon Alexa","Adding a family member","Your Family + Add Someone Else","Household as a roster on the profile screen.","Take the shape for 3.8 — everyone visible in one list, reachable in two taps.","good",
    phone(title="Your Profile", body="Your Family", rows=3, btn2="+ Add Someone Else"),"alexa-family"),
  T("IKEA Home smart","Requesting for Control Anywhere","Guest requests access from a host","IKEA has <b>no invite flow at all</b>. A second person installs the app and <i>requests</i> access; the host approves by verifying an email.","Notable inversion — pull rather than push. Lower risk of accidental over-granting, but it needs the guest to act first, which P2 will not do.","ok",
    phone(title="Requesting access", body="The host will need to verify their email before you can control this home.", rows=2, btn="Send request"),"ikea-request"),
 ]},

{"n":"P","name":"Saying what will be shared","fear":"“What can they actually see?”",
 "job":"The missing step. Disclose the real consequence before the invite is sent.",
 "noma":["<b>3.5 What they’ll be able to see</b> — three plain cards, <b>generated from the grants actually chosen</b> in 3.3/3.4, not static marketing copy: <b>① The devices</b> · <b>② The people here</b> · <b>③ Camera and activity</b>.",
         "Card ③ must name <b>video and audio</b> explicitly, and must appear whenever a camera is in scope. A disclosure that does not match the scope is a defect.",
         "<b>3.2 Who is it?</b> — each role reads as a consequence, not a title: “Sees everything, changes everything” beats “Admin”. ⚠ <b>C-3</b>: three incompatible role models exist and the prototype rebuilt this flow three times, so the options stay as data until it closes.",
         "<b>3.4 For how long</b> — household help defaults to <b>time-boxed and expiring</b>. That is a permissions requirement (P3), not a preference."],
 "rules":["Disclose before send, in the user's words, generated from the actual grants.",
          "Name cameras, video and audio explicitly. Never “activity”.",
          "A role is a sentence about consequences.",
          "Scoped and expiring by default for anyone who is not family."],
 "tiles":[
  T("Google Home","Inviting a person","What’s shared — 1 of 3","“Full control of devices and services — This member can access all devices, services and settings, including devices and services that are added later. They can also change all home settings, add and remove devices and services, and add and remove people.”","Take wholesale. Note “including devices added later” — the one clause people never think about.","good",
    phone(media=104, title="Full control of devices and services", body="This member can access all devices, services and settings, including devices and services that are added later.", btn="Next", btn2="Cancel"),"ghome-shared1"),
  T("Google Home","Inviting a person","What’s shared — 2 of 3","“Contact information and home address — This member can see the names and emails of other people in this home. They can also see and change the address.” + View household","Take. Discloses that inviting one person exposes everyone else already in the home.","good",
    phone(media=104, title="Contact information and home address", body="This member can see the names and emails of other people in this home. They can also see and change the address.", btn="Next", btn2="Cancel"),"ghome-shared2"),
  T("Google Home","Inviting a person","What’s shared — 3 of 3","“Home activity — This member will be able to see activity and events from all devices and services, like Nest Aware. This includes all events with video and audio data captured on cameras and other devices.”","<b>Take, and make it unmissable.</b> The only screen in the set that says the words video and audio. Our card ③.","good",
    phone(media=104, title="Home activity", body="This member will be able to see activity and events from all devices and services. This includes all events with video and audio data captured on cameras.", btn="Next", btn2="Cancel"),"ghome-shared3"),
  T("Amazon Alexa","Adding a family member","Who is this profile for?","“Adult — Controls their own experience” / “Kid — Includes parental controls”.","Take the form exactly: two options, each one line, each an outcome rather than a rank.","good",
    phone(title="Who is this profile for?", body="For a child-friendly experience, add a child profile, or enable Amazon Kids in devices settings.", radios=2, check=1, btn="Add Sam"),"alexa-role"),
  T("Amazon Alexa","Adding a family member","Here’s some things you share as part of the family","Amazon Shopping and Alexa Calendar, each with one line of consequence.","Take the placement — a closing summary of what is now shared, after enrolment, not buried in a settings screen.","good",
    phone(title="Here’s some things you share as part of the family", rows=2, btn="Done"),"alexa-shares"),
 ]},

{"n":"Q","name":"Send, and afterwards","fear":"“Can I undo this?”",
 "job":"A review that tells the truth, and a roster that stays reachable forever.",
 "noma":["<b>3.6 Review and send</b> — name, scope summary, expiry, and “<i>Everyone at home will be told when you add someone.</i>” Then <b>[Send invite]</b>.",
         "<b>3.8 Everyone at home</b> — each person, their scope, their expiry, and <b>Remove</b>. Reachable in two taps from Home for the life of the account.",
         "States required: invite pending (with resend and revoke) · expired · declined · member removed · last-remaining-owner (cannot be removed) · offline (queue it, and say so)."],
 "rules":["The review screen states the side effects, including who else gets told.",
          "Every grant is revocable from one list, forever.",
          "Removal is a first-class action, not buried in a detail sheet."],
 "tiles":[
  T("Google Home","Inviting a person","Send an invite to “Home”?","“Review this person’s access before inviting them.” Person, Device access ›, and “<b>Everyone in this home will be notified when you send this invitation.</b>”","Take wholesale, especially the last line — it tells the user the invite is not private from the household.","good",
    phone(title="Send an invite to “Home”?", body="Review this person’s access before inviting them.", rows=2, note="Everyone in this home will be notified when you send this invitation.", btn="Send", btn2="Cancel"),"ghome-review"),
  T("Google Home","Inviting a person","Invite sent","A toast, and the pending member appears in the household avatar row immediately.","Take. The invite is acknowledged in place rather than on a success screen, and the roster updates before the person has accepted.","good",
    phone(title="Device access", rows=4, btn2="All devices"),"ghome-access"),
  T("Apple Home","Home settings","People roster","Household members listed under People, with the owner marked.","Take. Owner clearly marked; ours must also refuse to remove the last one.","good",
    phone(title="Home Settings", body="People", rows=3),"apple-roster"),
  T("Amazon Alexa","Adding a family member","Your Family — after","“Sam”, “Jane Smith (Kid)” listed on the profile screen.","Take. Roles visible in the roster, so scope is legible at a glance without opening anything.","good",
    phone(title="Your Profile", body="Your Family", rows=3),"alexa-roster"),
  T("Google Home","Support","Deleting Home","A destructive action, confirmed, in settings.","Relevant to a DPDP obligation we have no surface for: account deletion and data export (scope ledger).","ok",
    phone(title="Delete Home", body="This will remove the home and all its devices for everyone.", btn2="Cancel   ·   Delete"),"ghome-delete"),
 ]},
]

SHOTLIST = [
 ("Google Home","Onboarding · Creating home · Inviting a person · Adding a device","4 flows"),
 ("Apple Home","Home · Adding an accessory (Bridge) · Adding a room · Adding people · Home settings","5 flows"),
 ("SmartThings","Onboarding · Creating an account · Adding a device","3 flows"),
 ("IKEA Home smart","Onboarding · Connecting to a hub · View help · Creating a room","4 flows"),
 ("Amazon Alexa","Onboarding · Adding a device (speaker) · Setting up Wi-Fi · Adding a family member","4 flows"),
]

# ───────────────────────────────────────────────────────── html
def stage_html(s):
    tiles = "".join(s["tiles"])
    noma  = "".join(f"<p>{p}</p>" for p in s["noma"])
    rules = "".join(f"<li>{E(r)}</li>" for r in s["rules"])
    return f"""
<section class="stage">
  <header class="sh">
    <p class="sh__n">{E(s['n'])}</p>
    <div>
      <h2>{E(s['name'])}</h2>
      <p class="sh__job">{E(s['job'])}</p>
      <p class="sh__fear"><span>At this moment the user is thinking</span> {E(s['fear'])}</p>
    </div>
  </header>
  <div class="strip">{tiles}</div>
  <div class="cols">
    <div class="col col--noma"><p class="ct">What NOMA does</p>{noma}</div>
    <div class="col col--rules"><p class="ct">Rules this sets</p><ul>{rules}</ul></div>
  </div>
</section>"""

CSS = r"""
@page { size: A4; margin: 15mm 14mm 16mm; }
@font-face{font-family:"GSF";font-weight:400;src:url(data:font/ttf;base64,__REG__) format("truetype")}
@font-face{font-family:"GSF";font-weight:600;src:url(data:font/ttf;base64,__MED__) format("truetype")}
@font-face{font-family:"GSF";font-weight:700;src:url(data:font/ttf;base64,__BOLD__) format("truetype")}
:root{
  --ink:#222; --sec:#5E5E5E; --ter:#8A8A8A; --line:#E4E1DA; --hair:#D3CFC6;
  --warm:#F5F3EF; --warm2:#EFEDE6; --moss:#4D6747; --neon:#AEC799;
  --good:#4D6747; --bad:#8C4A2F; --okc:#7A7266;
}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact}
body{margin:0;font-family:"GSF",system-ui,sans-serif;color:var(--ink);font-size:8.6pt;line-height:1.5}
h1,h2,h3{margin:0;text-wrap:balance}
p{margin:0 0 .42em}
code{font-family:ui-monospace,Menlo,monospace;font-size:.9em;background:var(--warm2);padding:.5pt 2pt;border-radius:2pt}
.mono{font-family:ui-monospace,Menlo,monospace;font-size:6.6pt;letter-spacing:.07em;text-transform:uppercase;color:var(--ter)}

/* cover */
.cover{height:262mm;display:flex;flex-direction:column;page-break-after:always}
.cover__top{flex:1}
.cover h1{font-size:41pt;line-height:.98;letter-spacing:-.025em;font-weight:700;max-width:17ch;margin:14mm 0 6mm}
.cover__sub{font-size:11.5pt;line-height:1.45;color:var(--sec);max-width:52ch}
.cover__rule{height:2pt;background:var(--ink);margin:8mm 0 4mm}
.cover__meta{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.cover__meta p{margin:0}
.cover__meta b{display:block;font-size:15pt;font-weight:700;letter-spacing:-.02em}

/* provenance */
.prov{background:var(--warm);border-radius:4mm;padding:6mm 7mm;margin:0 0 8mm}
.prov h3{font-size:11pt;margin-bottom:2mm}
.prov p{max-width:none;color:var(--sec)}
.prov strong{color:var(--ink)}

.tally{width:100%;border-collapse:collapse;margin:3mm 0 0;font-size:7.8pt}
.tally th,.tally td{text-align:left;padding:2mm 2.5mm;border-bottom:.5pt solid var(--line);vertical-align:top}
.tally th{font-size:6.6pt;letter-spacing:.07em;text-transform:uppercase;color:var(--ter);font-weight:600}
.tally td:first-child{font-weight:600;white-space:nowrap}

/* stage */
.stage{page-break-before:always;page-break-inside:avoid}
.sh{display:grid;grid-template-columns:16mm 1fr;gap:0 4mm;align-items:start;
    border-bottom:1.6pt solid var(--ink);padding-bottom:3mm;margin-bottom:4mm}
.sh__n{font-size:30pt;line-height:.8;font-weight:700;color:var(--moss);margin:0}
.sh h2{font-size:19pt;line-height:1.08;letter-spacing:-.022em;font-weight:700;margin-bottom:1.4mm}
.sh__job{color:var(--sec);font-size:9.4pt;margin-bottom:1mm}
.sh__fear{margin:0;font-size:8.2pt;color:var(--moss);font-weight:600}
.sh__fear span{color:var(--ter);font-weight:400}

.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-bottom:4.5mm}
.tile{margin:0;display:flex;flex-direction:column;border-radius:2.6mm;overflow:hidden;
      background:#fff;border:.5pt solid var(--line)}
.tile svg.ph,.tile img.ph{display:block;width:100%;height:auto;background:var(--warm2)}
.tile figcaption{padding:2.2mm 2.4mm 2.6mm;border-top:.5pt solid var(--line);flex:1;display:flex;flex-direction:column}
.t__app{font-size:7.4pt;font-weight:700;margin:0 0 .6mm}
.t__flow{font-size:6.2pt;color:var(--ter);margin:0 0 1.4mm;line-height:1.3}
.t__flow span{color:var(--hair)}
.t__q{font-size:6.5pt;line-height:1.34;color:var(--sec);margin:0 0 1.6mm}
.t__v{font-size:6.5pt;line-height:1.34;margin:auto 0 0;padding-top:1.4mm;border-top:.5pt dotted var(--line)}
.tile--good .t__v{color:var(--good)}
.tile--bad  .t__v{color:var(--bad)}
.tile--ok   .t__v{color:var(--okc)}
.tile--noma{border-color:var(--moss);border-width:1pt}
.tile--noma .t__app{color:var(--moss)}
.tile--noma .t__v{color:var(--moss);font-weight:600}
.t__wf{margin:0;padding:1.1mm 2.4mm 0;font-family:ui-monospace,Menlo,monospace;
  font-size:5.6pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ter)}
.tile--wf svg.ph{background:#FCFBF9}

.cols{display:grid;grid-template-columns:1.42fr 1fr;gap:5mm}
.ct{font-size:6.6pt;letter-spacing:.07em;text-transform:uppercase;color:var(--ter);font-weight:600;
    margin:0 0 1.8mm;padding-bottom:1.2mm;border-bottom:.5pt solid var(--line)}
.col p{font-size:8.1pt;line-height:1.46;margin:0 0 1.6mm}
.col--rules ul{margin:0;padding-left:4mm}
.col--rules li{font-size:8.1pt;line-height:1.42;margin-bottom:1.4mm}
.col--rules{background:var(--warm);border-radius:2.6mm;padding:4mm 4.4mm}
.col--rules .ct{border-color:var(--hair)}

/* appendix */
.apx{page-break-before:always}
.apx h2{font-size:19pt;letter-spacing:-.022em;font-weight:700;margin-bottom:2mm}
.apx > p{color:var(--sec);max-width:78ch;margin-bottom:5mm}
.apx h3{font-size:10.5pt;margin:6mm 0 2mm}
.dl{display:grid;grid-template-columns:auto 1fr;gap:2.2mm 5mm;font-size:8.2pt;align-items:baseline}
.dl dt{font-family:ui-monospace,Menlo,monospace;font-size:7.4pt;color:var(--moss);font-weight:700}
.dl dd{margin:0;color:var(--sec)}
.dl dd b{color:var(--ink)}
.foot{margin-top:8mm;padding-top:3mm;border-top:.5pt solid var(--line);color:var(--ter);font-size:7.2pt}
"""

body = f"""<title>NOMA — First Run Reference Book</title>
<style>{CSS.replace("__REG__",FONTS["REG"]).replace("__MED__",FONTS["MED"]).replace("__BOLD__",FONTS["BOLD"])}</style>

<section class="cover">
  <div class="cover__top">
    <p class="mono">NOMA · design research · 2026-08-05</p>
    <h1>First run: the reference book</h1>
    <p class="cover__sub">Every stage of getting somebody from a sealed box to a live air reading,
      and then to a household — with what five smart-home apps do at each stage, what to take from
      each, and what to refuse. Read alongside <code>docs/features/first-run/prd.md</code>.</p>
  </div>
  <div class="cover__rule"></div>
  <div class="cover__meta mono">
    <p><b>5</b>apps read</p>
    <p><b>17</b>stages</p>
    <p><b>85</b>reference screens</p>
    <p><b>~130</b>screens reviewed</p>
  </div>
</section>

<section class="apx" style="page-break-before:auto">
  <h2>Before you read this</h2>
  <div class="prov">
    <h3>About the reference tiles</h3>
    <p><strong>84 of the 85 tiles reference a real competitor screen. 69 of them are the actual
      Mobbin capture</strong>, pulled through Mobbin's own MCP connector and saved into
      <code>docs/research/refs/</code>. The remaining 15 are <strong>hand-drawn wireframes</strong>,
      labelled as such under the image: they carry the real layout, hierarchy and verbatim copy, but
      the screen was not reachable through the connector's search. The 85th tile is ours — stage M
      has no competitor equivalent.</p>
    <p><strong>Every tile names its app, flow and screen</strong>, so any of them can be opened on
      Mobbin directly. To replace a remaining wireframe, save the capture as
      <code>docs/research/refs/&lt;slug&gt;.png</code> and re-run
      <code>python3 docs/research/build-refs.py</code> — a slug with a real file present always wins.
      <code>docs/research/refs-map.json</code> lists all 85 slugs with their source and current state,
      and <code>fetch-refs.py</code> is the pipeline that fetched them.</p>
    <p><strong>What is still redrawn, and why.</strong> These fifteen sit in flows the MCP search did
      not return — mostly account-creation and settings screens, which are less well indexed than
      setup flows:</p>
    <table class="tally">
      <tr><th>Stage</th><th>App</th><th>Screen</th></tr>
      <tr><td>A, C</td><td>Google Home, Amazon Alexa</td><td>Welcome home &middot; Sign in (both apps' account screens)</td></tr>
      <tr><td>C, D</td><td>SmartThings</td><td>Create your Samsung account &middot; Optional opt-ins &middot; One account. Any device.</td></tr>
      <tr><td>D, J</td><td>Google Home</td><td>Removing saved WiFi and home address &middot; Saved WiFi</td></tr>
      <tr><td>F, K</td><td>Google Home</td><td>Choose a device &middot; Devices, groups and rooms</td></tr>
      <tr><td>K</td><td>IKEA Home smart, Apple Home</td><td>Create a room &middot; Choose Icon</td></tr>
      <tr><td>N, O</td><td>IKEA Home smart</td><td>Common issues and solutions &middot; Guest requests access from a host</td></tr>
      <tr><td>Q</td><td>Google Home</td><td>Deleting Home</td></tr>
    </table>
    <p style="margin-top:3mm"><strong>Three captions were corrected</strong> once the real screens
      arrived: IKEA's analytics consent uses <em>checkboxes</em>, not radio buttons; Google Home has no
      standalone Device access screen, so stage Q now shows the <em>Invite sent</em> state instead; and
      SmartThings' device-added screen does not exist as such — stage M now shows the Favorites grid
      that setup both starts and ends in. Where a real capture contradicted a note, the note lost.</p>
  </div>

  <h3>The one decision in here</h3>
  <p>The brief suggested the household before the device. Every reference app does the opposite, and so
     does this book. <b>Five out of five put device before people.</b> Not one asks for a household
     member during first run; members always live in Settings, reached later, deliberately.</p>
  <p>The reason is structural rather than fashionable. <b>An invitation to a home with nothing in it is
     an invitation to nothing</b> — no device to scope, no permission worth granting, and no way for the
     invitee to tell whether accepting did anything. And the ask lands completely differently once the
     reveal has happened: somebody who has just seen <em>“your bedroom is 34, the street is 168”</em> has
     a reason to add their family. The same screen, ninety seconds earlier, is a chore.</p>
  <table class="tally">
    <tr><th>App</th><th>Order it actually ships</th><th>Where members live</th></tr>
    <tr><td>Google Home</td><td>Sign in → create home (name, address skippable) → choose home → what’s new → favourites → devices empty state → add device</td><td>Settings → Invite person</td></tr>
    <tr><td>Apple Home</td><td>A Home already exists → <code>+</code> → Add Accessory → room</td><td>Same <code>+</code> menu, never prompted</td></tr>
    <tr><td>SmartThings</td><td>4 value slides (3 OS prompts) → Samsung account (13 screens) → location name + geolocation → scan → pair (22 screens)</td><td>No member flow captured at all</td></tr>
    <tr><td>IKEA Home smart</td><td>Region → privacy → analytics consent → editorial welcome → hub setup (22 screens) → name home</td><td>No invite flow — guests <em>request</em> access from a host</td></tr>
    <tr><td>Amazon Alexa</td><td>Account → device setup → Wi-Fi (28-screen onboarding)</td><td>Profile → Add Someone Else, much later</td></tr>
  </table>
  <p style="margin-top:4mm"><b>One more thing the set agrees on:</b> one question per screen. No app in
     the five puts two decisions on one setup screen.</p>
  <p><b>And one gap none of them fills.</b> All five end setup with a device tile in a list. Nobody has
     a reveal. Air is invisible, so that final screen is the whole opportunity — see stage M.</p>
</section>

{"".join(stage_html(s) for s in STAGES)}

<section class="apx">
  <h2>What is still holding this up</h2>
  <p>Nothing in this book is blocked on research. It is blocked on decisions, listed in
     <code>memory/decisions.md</code>.</p>
  <dl class="dl">
    <dt>C-2</dt><dd><b>Five names are in circulation</b> for the product and the assistant. Every headline in stage A and the agent’s line in stage M contains one, so no string here is final. The interaction design does not wait on it; the copy does.</dd>
    <dt>C-3</dt><dd><b>Three incompatible role models.</b> Stages P and Q are built shape-only. 3.1, 3.5, 3.6 and the roster are role-agnostic and can be built now; 3.2’s options stay as data.</dd>
    <dt>C-11</dt><dd><b>No analytics can exist yet.</b> On-device privacy versus any SDK is unresolved, so this flow ships unmeasurable — and per-screen drop-off is the only way to know whether any of it works. That is the real cost of leaving C-11 open.</dd>
    <dt>C-12</dt><dd><b>Two room-preset lists.</b> 8 items vs 11. The 11-item list is the India-appropriate one; the 8-item list omits Pooja Room. Stage K cannot be finalised until this closes.</dd>
    <dt>O-6</dt><dd><b>No status colours.</b> <code>colors.status</code> is <code>null</code> and green cannot carry “bad”, so the eight failure screens in stage N ship neutral. Flagged rather than invented.</dd>
    <dt>O-8</dt><dd><b>Two of the three feature ids do not exist.</b> The registry has thirteen features and none is “get a new customer to a working first device”. <code>F-FIRST-RUN</code> and <code>F-SETUP</code> are proposed, not assigned.</dd>
    <dt>O-9</dt><dd><b>Identify and the ring-LED vocabulary are unconfirmed.</b> Stages H and I depend on hardware behaviour no document says the purifier has: a remote blink, and a ring state that distinguishes pairing from already-paired from error.</dd>
  </dl>

  <h3>Sources</h3>
  <p style="margin-top:1mm">Mobbin (iOS), read 2026-08-05 on the owner’s account: Google Home (35 flows) ·
     Apple Home (34) · SmartThings (44) · IKEA Home smart (59) · Amazon Alexa (76). Nine flows read
     screen by screen, about 130 screens.</p>
  <p><b>Mobbin carries no air-purifier or air-quality app at all</b> — no Dyson, Levoit, Molekule or
     Airthings — and no Aqara, Ring, Nest, Wyze, Eufy, Tuya or Philips Hue either. The five above are
     the entire smart-home set available. There is no incumbent to be measured against. IKEA’s DIRIGERA
     hub, also a physical object you plug in and watch a light on, is the closest analogue and the best
     flow in the set by a distance.</p>

  <p class="foot">Companion documents: <code>docs/research/2026-08-05-setup-teardown.md</code> (the teardown)
     · <code>docs/features/first-run/prd.md</code> (the specification, with full copy and all eight failure
     states). Regenerate this book with <code>python3 docs/research/build-refs.py</code>.
     Set in Google Sans Flex; palette from <code>src/tokens/design.tokens.js</code>.</p>
</section>
"""

# ── emit refs-map.json: slug -> where each capture comes from
import json as _json
_stage_of = {}
for _st in STAGES:
    for _t in _st["tiles"]:
        _stage_of[_t] = (_st["n"], _st["name"])
_order = []
for _st in STAGES:
    for _t in _st["tiles"]:
        _order.append((_st["n"], _st["name"]))
for _r, (_n, _nm) in zip(REGISTRY, _order):
    _r["stage"] = _n
    _r["stageName"] = _nm
MAP = ROOT / "docs/research/refs-map.json"
MAP.write_text(_json.dumps({"$comment": [
  "Where each reference tile's capture comes from.",
  "To use real Mobbin captures: save each as docs/research/refs/<slug>.png and re-run",
  "build-refs.py. Any slug with a real file present replaces its wireframe automatically.",
  "Generated from the tile definitions, so it cannot drift from the document."],
  "have": sum(1 for r in REGISTRY if r["haveCapture"]),
  "total": len(REGISTRY),
  "refs": REGISTRY}, indent=1, ensure_ascii=False) + "\n")

body = "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in body)
OUT.write_text(body)
n = sum(len(s["tiles"]) for s in STAGES)
print(f"wrote {OUT.relative_to(ROOT)}  stages={len(STAGES)} tiles={n}  {len(body)/1024/1024:.2f} MB")
