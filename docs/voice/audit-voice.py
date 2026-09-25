#!/usr/bin/env python3
"""
docs/voice/audit-voice.py — the machine gate from the Voice Guide §12.

    python3 docs/voice/audit-voice.py                 # audit every prototype
    python3 docs/voice/audit-voice.py path/to.html    # audit specific files
    python3 docs/voice/audit-voice.py --list          # what it audits

Implements the ⚙ items of the shipping checklist (Voice Guide §12, items 1-6).
Exits non-zero on any violation, so it can sit in CI. D-4 is explicit about why
this exists rather than a one-time rewrite:

    "the onboarding round of Aug 2026 found live em dashes, two clefts, an
     unbounded wait, and a line the corrections bank had already fixed, all in
     a surface believed shipped. This is the argument for running the gate in
     CI rather than trusting a one-time rewrite. No surface is done from
     belief."

WHAT COUNTS AS COPY, AND WHY IT MATTERS HERE. This audits only text the PERSON
reads: everything inside the `.phone` frame of a prototype. It deliberately
does NOT audit the review rails (`.rail`, `.ctrl`), the design notes beside the
phone, Python docstrings, comments, or CSS. Those are writing ABOUT the product
for the team, not the product speaking, and they are full of em dashes on
purpose. Auditing them would bury the real findings in noise, which is the
fastest way to get a gate switched off.

WHAT THIS CANNOT DO, stated plainly because §0.1 rule 5 forbids claiming a
string "passes the voice" from an audit alone:

  · It cannot hear tone. Every finding here is mechanical. The read-aloud
    test (§0) is a human gate and always outranks this script.
  · M-18 (character limits) is NOT implemented, because D-7 has not landed.
    The rule is written, the numbers are not published, and inventing limits
    would violate R-17 in the very tool meant to enforce it.
  · Cleft detection (M-04) is a heuristic on the commonest English forms. It
    will miss some and can flag an innocent one. Treat a cleft hit as "read
    this line", not as a verdict.
  · Sentence case (M-06) is only checked on short strings that are clearly
    titles or buttons, and skips scripts without letter case (Devanagari and
    others are explicitly out of scope per M-06).
"""

import html.parser
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Prototypes carrying product copy. Add a surface here when it gains copy.
TARGETS = [
    "docs/features/settings/profile-settings-prototype.html",
    "docs/features/settings/device-settings-prototype.html",
    "docs/features/first-run/onboarding-prototype.html",
    "docs/features/first-run/auth-prototype.html",
    "docs/features/first-run/first-run-flow.html",
    "docs/features/my-home/my-home-prototype.html",
]


# ---------------------------------------------------------------------------
# Copy extraction — only what is inside the phone.
# ---------------------------------------------------------------------------

class CopyExtractor(html.parser.HTMLParser):
    """Pulls visible text plus aria-labels and placeholders from inside
    `.phone`, skipping <script>/<style> and any review chrome.

    `require_phone=False` parses a bare fragment (used for screen HTML that
    lives inside an embedded JSON blob, where the .phone wrapper is added at
    runtime rather than being in the file)."""

    SKIP_TAGS = {"script", "style", "svg", "title"}

    def __init__(self, require_phone=True):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.in_phone = not require_phone
        self.require_phone = require_phone
        self.skip_depth = 0
        self.out = []             # (text, kind)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.require_phone and not self.in_phone:
            if "phone" in a.get("class", "").split():
                self.in_phone = True
                self.depth = 0
            return
        if self.in_phone:
            self.depth += 1
            if tag in self.SKIP_TAGS:
                self.skip_depth += 1
            # attribute-borne copy — a11y strings are copy (M-19)
            for attr in ("aria-label", "placeholder"):
                if a.get(attr):
                    self.out.append((a[attr], attr))

    def handle_endtag(self, tag):
        if self.in_phone:
            if tag in self.SKIP_TAGS and self.skip_depth:
                self.skip_depth -= 1
            self.depth -= 1
            if self.require_phone and self.depth < 0:
                self.in_phone = False

    def handle_data(self, data):
        if self.in_phone and not self.skip_depth:
            t = data.strip()
            if t:
                self.out.append((t, "text"))


# M-06 does not govern these. Identifiers (SSIDs, timezones), dates, and the
# OS's own dialog strings, which §1.2 case 2 says are not ours to rewrite.
M06_EXEMPT = re.compile(
    r"_|/|"                                              # SSIDs, Asia/Kolkata
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    r"|January|February|March|April|June|July|August|September"
    r"|October|November|December"
    r"|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b|"                   # dates
    r"\b(Don.t Allow|While Using the App|Open Settings|Allow Once"
    # iOS Settings > Bluetooth, depicted verbatim on nodes 10-11. Same case as
    # the dialog strings above: §1.2 case 2 — the OS's own words are not ours
    # to sentence-case.
    r"|Not Connected|My Apple Watch|Now discoverable)\b"  # iOS
)

LOOKS_LIKE_HTML = re.compile(r"<[a-zA-Z/][^>]*>")
# Interpolation and token noise that is code, not copy.
CODE_NOISE = re.compile(r"^\s*(\$\{|\}|[\w.]+\(|//|/\*)")

# Variables holding REVIEW CHROME, not product copy. Verified by reading each
# one: JOBS is the my-home rail's per-state description, LABELS its button
# text. Excluding them is the difference between a gate people trust and one
# they switch off, because every hit from these is a false positive.
HARNESS_VARS = {"JOBS", "LABELS", "ORDER"}
# Same, at key level: build-flow.py packs its rail's design notes and jump-list
# titles into the same JSON blob as the screens themselves.
# `note` (singular) is auth-prototype.html's per-state rail note — the same
# thing build-flow.py spells `notes`. Its sibling key `inner` carries that
# file's actual product copy and is deliberately NOT excluded.
HARNESS_KEYS = {"notes", "titles", "note"}


def _json_blobs(script_text):
    """Every `const X = {...}` / `= [...]` in a script that parses as JSON,
    returned as (varname, blob).

    Bracket-matches while respecting string literals, so a brace inside a
    copy string doesn't end the blob early."""
    blobs = []
    for m in re.finditer(r"(?:const|let|var)\s+(\w+)\s*=\s*", script_text):
        i = m.end()
        if i >= len(script_text) or script_text[i] not in "{[":
            continue
        depth, in_str, esc = 0, None, False
        for j in range(i, len(script_text)):
            ch = script_text[j]
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if in_str:
                if ch == in_str:
                    in_str = None
                continue
            if ch in "\"'":
                in_str = ch
                continue
            if ch in "{[":
                depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    try:
                        blobs.append((m.group(1), json.loads(script_text[i:j + 1])))
                    except Exception:
                        pass
                    break
    return blobs


def _walk_strings(node, out):
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            # keys that are ids/classes/config, not copy
            if k in ("id", "seq", "node", "kind", "sec", "class") or k in HARNESS_KEYS:
                continue
            _walk_strings(v, out)
    elif isinstance(node, list):
        for v in node:
            _walk_strings(v, out)


def extract_copy(path):
    """Static copy inside .phone, PLUS copy inside embedded JSON.

    ⚠ The second half matters: first-run-flow.html and my-home-prototype.html
    render every screen from a JSON fixture at runtime, so a .phone-only pass
    reports them clean while they carry the most copy in the product. A gate
    that silently passes the biggest surfaces is worse than no gate."""
    raw = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")

    p = CopyExtractor(require_phone=True)
    p.feed(raw)
    found = list(p.out)

    for script in re.findall(r"<script[^>]*>(.*?)</script>", raw, re.S):
        for varname, blob in _json_blobs(script):
            if varname in HARNESS_VARS:
                continue
            strings = []
            _walk_strings(blob, strings)
            for s in strings:
                if not s.strip() or CODE_NOISE.match(s):
                    continue
                if LOOKS_LIKE_HTML.search(s):
                    fp = CopyExtractor(require_phone=False)
                    fp.feed(s)
                    found.extend(fp.out)
                else:
                    found.append((s.strip(), "text"))

    seen, uniq = set(), []
    for text, kind in found:
        # drop interpolation fragments and bare template plumbing
        if CODE_NOISE.match(text) or text in ("${", "}"):
            continue
        key = (text, kind)
        if key not in seen:
            seen.add(key)
            uniq.append((text, kind))
    return uniq


# ---------------------------------------------------------------------------
# The checks. Each returns a reason string, or None.
# ---------------------------------------------------------------------------

EMOJI = re.compile(
    "[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F000-\U0001F2FF"
    "\U0000FE00-\U0000FE0F" "\U00002190-\U000021FF" "]"
)

# §5.2, matched as families. Form voice is matched as PHRASES, never the bare
# word "please" — §12 gate item 2 is explicit, because "Yes, please" is a
# correct answer the PERSON gives.
BANNED_PHRASES = [
    # Form voice
    ("please enter", "§5.2 form voice"), ("please wait", "§5.2 form voice"),
    ("please note", "§5.2 form voice"), ("kindly", "§5.2 form voice"),
    ("invalid", "§5.2 form voice"), ("successfully completed", "§5.2 form voice"),
    # Corporate distance
    ("we are unable", "§5.2 corporate distance"), ("the user", "§5.2 corporate distance"),
    ("utilize", "§5.2 corporate distance"), ("in order to", "§5.2 corporate distance"),
    # Narrator
    ("data shows", "§5.2 narrator"), ("score updated", "§5.2 narrator"),
    # Hype
    ("amazing", "§5.2 hype"), ("awesome", "§5.2 hype"), ("great job", "§5.2 hype"),
    ("crush it", "§5.2 hype"), ("smash it", "§5.2 hype"), ("oops", "§5.2 hype"),
    ("uh-oh", "§5.2 hype"),
    # Shame
    ("you failed", "§5.2 shame"), ("you missed", "§5.2 shame"),
    ("you're behind", "§5.2 shame"), ("you broke", "§5.2 shame"),
    # Alarm
    ("urgent", "§5.2 alarm"), ("act now", "§5.2 alarm"), ("toxic", "§5.2 alarm"),
    ("hazardous", "§5.2 alarm"),
    # Insider
    ("baseline", "§5.2 insider"), ("in range", "§5.2 insider"),
    ("on target", "§5.2 insider"), ("threshold", "§5.2 insider"),
    ("telemetry", "§5.2 insider"), ("parameters", "§5.2 insider"),
    # Slang / hustle
    ("legit", "§5.2 slang"), ("lowkey", "§5.2 slang"), ("beast mode", "§5.2 slang"),
    ("crushing it", "§5.2 slang"),
    # Health overclaim (R-14)
    ("your lungs", "R-14 health overclaim"), ("doctor-recommended", "R-14 health overclaim"),
]

# M-09: a push title arrives with no screen behind it.
COLD_TITLE_BANNED = ["came in", "reads", "logged", "registered", "data shows", "detected"]

# M-04 cleft heuristics, commonest English forms only.
CLEFTS = [
    re.compile(r"\bis what\b", re.I),
    re.compile(r"\bis where\b(?!\s+(it|they|the device|the purifier)\s+lives)", re.I),
    re.compile(r"\bit is\s+\w+\s+that\b", re.I),
    re.compile(r"\bwhat .{3,40} is that\b", re.I),
]

# W-01: AQI is only legal quoting the OUTDOOR index, with its source.
OUTDOOR_CONTEXT = re.compile(r"outside|outdoor|cpcb|forecast", re.I)


def has_case(s):
    """M-06 only governs scripts that have letter case."""
    return any(unicodedata.category(ch) in ("Lu", "Ll") for ch in s)


def check_string(s, kind):
    """Returns a list of (rule, detail) for one string."""
    hits = []
    low = s.lower()

    if "—" in s:
        hits.append(("M-03", "em dash"))
    if "!" in s:
        hits.append(("M-01", "exclamation mark"))
    # M-02 explicitly exempts "a glyph doing an icon's job inside a control
    # (a country flag in a dialling-code picker)". Regional indicators are
    # that case, so they are chrome and not audited.
    if EMOJI.search(s) and not re.fullmatch(r"[\U0001F1E6-\U0001F1FF\s+\d]+", s):
        hits.append(("M-02", "emoji in copy"))
    if ";" in s:
        hits.append(("M-11", "semicolon in copy"))

    for phrase, family in BANNED_PHRASES:
        if re.search(r"\b" + re.escape(phrase) + r"\b", low):
            hits.append(("§5.2", '"%s" (%s)' % (phrase, family)))

    for rx in CLEFTS:
        if rx.search(s):
            hits.append(("M-04", "reads as a cleft, check by ear"))
            break

    # W-01 — AQI is indoor-illegal. Legal only quoting the outdoor index.
    if re.search(r"\bAQI\b", s) and not OUTDOOR_CONTEXT.search(s):
        hits.append(("W-01", "AQI without outdoor context; indoor readings are PM2.5 µg/m³"))

    # M-17 — a bare token glued to a fixed plural noun.
    if re.search(r"\{\w+\}\s+(nights|devices|people|rooms|days|weeks|minutes)\b", s):
        hits.append(("M-17", "token glued to a plural noun; needs a singular form"))

    # M-06 — Title Case, on short strings only, and only where case exists.
    if kind in ("title", "button") and has_case(s) and not M06_EXEMPT.search(s):
        # Split on whitespace so a contraction stays one word: the old
        # character-class split turned "I've" into "I" + "ve" and flagged
        # every contraction in the product as Title Case.
        # Keep separators in the token list: a capital right after "·" is a
        # new clause, so dropping the "·" first made every such word look like
        # Title Case ("Online · Living room").
        raw = s.split()
        words = [w.strip(".,:()/") for w in raw]
        if len(words) >= 2:
            # A word right after a "·" separator starts a new clause, so its
            # capital is sentence case, not Title Case.
            caps = []
            for idx, w in enumerate(words[1:], start=1):
                if not w or not re.match(r"[A-Za-z]", w) or not w[:1].isupper():
                    continue
                prev = words[idx - 1]
                if prev.endswith("·") or prev == "·" or prev.endswith(("-", "—")):
                    continue
                caps.append(w)
            # allow acronyms and known proper nouns
            caps = [w for w in caps
                    if not w.isupper() and w not in
                    ("Noma", "Auto", "Turbo", "Night", "Away", "Home", "Wi", "Fi",
                     "Alexa", "Google", "Assistant", "Bluetooth", "PM",
                     # product line + device names the person set (W-05)
                     "Air", "Pro", "Max", "GHz", "AQI", "Undo",
                     # people
                     "Ruhaan", "Royce", "Asha", "Aarti", "Vikram", "Sunita", "Sharma",
                     # node 18a's contact fixtures
                     "Ayush", "Tiwari", "Aanya", "Verma", "Karan", "Singh",
                     # Wi-Fi is a proper noun; Automation is a destination name
                     "Wi-Fi", "Automation", "QSensAI",
                     # Named documents and a platform button whose wording is
                     # not ours to sentence-case: Apple's HIG specifies
                     # "Continue with Apple" verbatim, and the two policies are
                     # titles of documents, not descriptions of them.
                     "Apple", "Service", "Policy")
                    # contractions of "I" are not Title Case
                    and not w.startswith(("I'", "I’"))]
            if caps:
                hits.append(("M-06", "Title Case: %s" % ", ".join(caps)))

    if kind == "title":
        for w in COLD_TITLE_BANNED:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                hits.append(("M-09", 'narrator word "%s" in a title' % w))
    return hits


def audit(path):
    findings = []
    for text, kind in extract_copy(path):
        # Short strings that look like titles/buttons get the case + cold-title
        # checks; long prose does not.
        k = "title" if (kind == "text" and len(text) < 42 and "." not in text) else kind
        for rule, detail in check_string(text, k):
            findings.append((rule, detail, text))
    return findings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--list" in sys.argv:
        for t in TARGETS:
            print(t)
        return 0

    targets = args or TARGETS
    total = 0
    for t in targets:
        p = ROOT / t if not pathlib.Path(t).is_absolute() else pathlib.Path(t)
        if not p.exists():
            print("  MISSING  %s" % t)
            total += 1
            continue
        findings = audit(p)
        rel = p.relative_to(ROOT) if str(p).startswith(str(ROOT)) else p
        if not findings:
            print("  clean    %s" % rel)
            continue
        print("  %-3d      %s" % (len(findings), rel))
        for rule, detail, text in findings:
            snippet = text if len(text) <= 88 else text[:85] + "..."
            print("      %-6s %s" % (rule, detail))
            print("             %s" % snippet)
        total += len(findings)

    print()
    if total:
        print("%d machine-gate violations. Voice Guide §12 items 1-6." % total)
        print("Human gate (read aloud, §12 items 8-19) is separate and still owed.")
    else:
        print("Machine gate clean. This is NOT 'passes the voice' (§0.1 rule 5):")
        print("the read-aloud test is a human gate and has not been run here.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
