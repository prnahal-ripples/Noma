#!/usr/bin/env python3
"""
Build docs/voice/voice-print.html, then render it to
docs/voice/NOMA-Voice-PRD.pdf with headless Chrome.

    python3 docs/voice/build-voice-pdf.py

Follows the same typesetting system as docs/prd/prd-print.html (A4, Google
Sans Flex, moss/warm palette) so the two PRDs read as one family. Differs in
one respect worth keeping: fonts are embedded as base64 data URIs rather than
a relative path, because the original file's relative font path
(`../../src/noma-fonts/...`) points at a file that does not exist in this repo
— this version cannot silently fall back to a system font.

Content is a direct typeset of docs/voice/voice-prd.md — that
markdown file is canonical; keep them in sync by hand (this repo's PRDs are
short-lived enough that a markdown→HTML pipeline hasn't been worth building).
"""
import base64, pathlib, subprocess, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_HTML = ROOT / "docs/voice/voice-print.html"
OUT_PDF  = ROOT / "docs/voice/NOMA-Voice-PRD.pdf"
FDIR = ROOT / "src/fonts/google-sans-flex/static"
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
FONTS = {
    "REG":  b64(FDIR / "GoogleSansFlex_24pt-Regular.ttf"),
    "MED":  b64(FDIR / "GoogleSansFlex_24pt-Medium.ttf"),
    "SEMI": b64(FDIR / "GoogleSansFlex_24pt-SemiBold.ttf"),
    "BLD":  b64(FDIR / "GoogleSansFlex_24pt-Bold.ttf"),
}
E = lambda s: H.escape(str(s), quote=False)

CSS = r"""
@font-face { font-family:"GSF"; font-weight:400; src:url(data:font/ttf;base64,__REG__) format("truetype"); }
@font-face { font-family:"GSF"; font-weight:500; src:url(data:font/ttf;base64,__MED__) format("truetype"); }
@font-face { font-family:"GSF"; font-weight:600; src:url(data:font/ttf;base64,__SEMI__) format("truetype"); }
@font-face { font-family:"GSF"; font-weight:700; src:url(data:font/ttf;base64,__BLD__) format("truetype"); }

:root {
  --ink:#222222; --sec:#5E5E5E; --ter:#8A8A8A;
  --line:#E4E1DA; --hair:#D3CFC6;
  --warm:#F5F3EF; --warm2:#EFEDE6; --raised:#FFFFFF;
  --moss:#4D6747; --moss-tint:#EEF2ED;
  --neon:#AEC799; --neon-tint:#F2F5F0;
  --crit:#8C2F2F; --crit-bg:#FBF0EF;
  --warn:#8A5A16; --warn-bg:#FBF5EA;
  --ok:#3B5F36; --ok-bg:#F0F5EE;
}

@page { size: A4; margin: 17mm 15mm 16mm; }

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  margin: 0;
  font-family: "GSF", system-ui, sans-serif;
  font-optical-sizing: auto;
  font-size: 9.6pt; line-height: 1.52;
  color: var(--ink);
  background: #fff;
}

h1,h2,h3,h4 { margin: 0; text-wrap: balance; }

/* ---------- cover ---------- */
.cover { height: 262mm; display: flex; flex-direction: column; page-break-after: always; }
.cover-mark { font-size: 8pt; letter-spacing: .28em; text-transform: uppercase; color: var(--sec); }
.cover-rule { height: 3px; background: var(--moss); width: 46mm; margin: 5mm 0 0; }
.cover-title { font-size: 38pt; line-height: 1.04; font-weight:700; letter-spacing: -1.2pt; margin-top: 14mm; }
.cover-sub { font-size: 13pt; line-height: 1.4; color: var(--sec); margin-top: 6mm; max-width: 128mm; font-weight:400; }
.cover-spacer { flex: 1; }
.cover-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm 10mm; border-top: 1px solid var(--hair); padding-top: 6mm; }
.cover-meta div span { display: block; font-size: 7.4pt; letter-spacing: .12em; text-transform: uppercase; color: var(--ter); }
.cover-meta div b { font-size: 10pt; font-weight:600; }
.cover-status {
  margin-top: 8mm; background: var(--warn-bg); border-left: 3px solid var(--warn);
  padding: 4mm 5mm; font-size: 9.4pt; line-height: 1.5;
}
.cover-status b { color: var(--warn); font-weight:700; }

/* ---------- contents ---------- */
.toc { page-break-after: always; }
.toc ol { list-style: none; counter-reset: t; padding: 0; margin: 6mm 0 0; column-count: 2; column-gap: 10mm; }
.toc li { counter-increment: t; font-size: 9.4pt; padding: 1.6mm 0; border-bottom: 1px dotted var(--line); break-inside: avoid; }
.toc li::before { content: counter(t) ". "; color: var(--ter); font-weight:600; }

/* ---------- sections ---------- */
section { page-break-inside: auto; }
h2 {
  font-size: 17pt; line-height: 1.15; font-weight:700;
  letter-spacing: -.4pt; margin-top: 11mm; padding-bottom: 2.4mm;
  border-bottom: 2px solid var(--ink);
  page-break-after: avoid;
}
h2 .num { color: var(--moss); margin-right: 3mm; }
h3 { font-size: 11.4pt; font-weight:700; margin-top: 6.5mm; page-break-after: avoid; }
h4 { font-size: 9.6pt; font-weight:700; margin-top: 4.5mm; page-break-after: avoid; }
p { margin: 2.4mm 0 0; }
.lede { font-size: 11pt; line-height: 1.5; color: var(--sec); margin-top: 3mm; }
ul, ol { margin: 2.4mm 0 0; padding-left: 5.5mm; }
li { margin: 1.1mm 0; }
code { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: .88em; background: var(--warm2); padding: .3mm 1.1mm; border-radius: 1mm; }
strong { font-weight:700; }
em { font-style: italic; }

/* ---------- tables ---------- */
table { width: 100%; border-collapse: collapse; margin-top: 3.5mm; font-size: 8.8pt; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th {
  text-align: left; font-size: 7.4pt; letter-spacing: .1em; text-transform: uppercase;
  color: var(--sec); font-weight:700;
  border-bottom: 1.4px solid var(--ink); padding: 1.8mm 2.2mm 1.8mm 0; vertical-align: bottom;
}
td { padding: 2mm 2.2mm 2mm 0; border-bottom: 1px solid var(--line); vertical-align: top; }
td:last-child, th:last-child { padding-right: 0; }
tbody tr:nth-child(even) { background: #FBFAF8; }
.tight td, .tight th { padding-top: 1.4mm; padding-bottom: 1.4mm; }

/* ---------- callouts ---------- */
.box { margin-top: 4mm; padding: 3.6mm 4.2mm; border-radius: 2mm; page-break-inside: avoid; font-size: 9.2pt; }
.box p:first-child { margin-top: 0; }
.box .bt { font-size: 7.4pt; letter-spacing: .14em; text-transform: uppercase; font-weight:700; display: block; margin-bottom: 1.6mm; }
.box.crit { background: var(--crit-bg); border-left: 3px solid var(--crit); }
.box.crit .bt { color: var(--crit); }
.box.warn { background: var(--warn-bg); border-left: 3px solid var(--warn); }
.box.warn .bt { color: var(--warn); }
.box.ok { background: var(--ok-bg); border-left: 3px solid var(--ok); }
.box.ok .bt { color: var(--ok); }
.box.quiet { background: var(--warm); border-left: 3px solid var(--hair); }
.box.quiet .bt { color: var(--sec); }

blockquote {
  margin: 4mm 0 0; padding: 0 0 0 5mm; border-left: 2px solid var(--moss);
  font-size: 11pt; line-height: 1.44; color: var(--ink); font-weight:500;
}
blockquote cite { display: block; font-style: normal; font-size: 8.4pt; color: var(--ter); margin-top: 1.8mm; }

.chip {
  display: inline-block; font-size: 7.2pt; letter-spacing: .06em; text-transform: uppercase;
  font-weight:700; padding: .5mm 1.6mm; border-radius: 1mm; white-space: nowrap;
}
.chip.ok { background: var(--moss); color: #fff; }
.chip.b { background: var(--warm2); color: var(--sec); }
.chip.h { background: var(--warn); color: #fff; }

.kv { display: grid; grid-template-columns: 38mm 1fr; gap: 1.6mm 4mm; margin-top: 3mm; font-size: 9.2pt; }
.kv dt { color: var(--sec); }
.kv dd { margin: 0; }

.pagebreak { page-break-before: always; }
.avoid { page-break-inside: avoid; }
footer.doc { margin-top: 12mm; padding-top: 4mm; border-top: 1px solid var(--hair); font-size: 8.2pt; color: var(--ter); }

/* rule cards — §3, this document's own pattern (not borrowed from prd-print) */
.rule { margin-top: 5mm; padding: 4mm 4.5mm; background: var(--warm); border-radius: 2.4mm;
  border-left: 3px solid var(--moss); page-break-inside: avoid; }
.rule h3 { margin-top: 0; font-size: 10.6pt; }
.rule h3 .rn { color: var(--moss); font-weight:700; margin-right: 2mm; }
.rule p { font-size: 9.2pt; }

/* print hygiene */
@media print {
  section { orphans: 3; widows: 3; }
  h2, h3, h4 { break-after: avoid-page; }
  table, .box, blockquote { break-inside: auto; }
  tr, .rule { break-inside: avoid; }
}
"""
for k, v in FONTS.items():
    CSS = CSS.replace(f"__{k}__", v)


def rows(items):
    return "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in items
    )


VOCAB_ROWS = rows([
  ["\u201cPlease enter your\u2026\u201d", "\u201cWhat\u2019s your\u2026\u201d \u2014 a direct question", "\u201cPlease enter\u201d is a form filling itself out at you"],
  ["\u201cInvalid [X]\u201d", "Name what\u2019s actually wrong, plainly", "\u201cInvalid\u201d blames the input, not the mismatch"],
  ["\u201cError\u201d / \u201cFailed\u201d", "Say what happened and what still works", "Both are a verdict with no next step"],
  ["\u201cPlease wait\u2026\u201d", "Name the wait and its length", "An un-named wait reads as a stall"],
  ["\u201cContinue\u201d on a warm moment", "A warmer verb \u2014 reserve \u201cContinue\u201d for plain steps", "The mistake is warming the wrong buttons, not using \u201cContinue\u201d at all"],
  ["\u201cKindly\u201d / \u201cPlease note that\u201d", "Cut it \u2014 say the thing", "Both are throat-clearing with no content"],
  ["\u201cIn order to\u201d", "\u201cTo\u201d", "Three words doing one word\u2019s job"],
  ["\u201cUtilize\u201d", "\u201cUse\u201d", "&mdash;"],
  ["\u201cWe are unable to\u201d", "\u201cI can\u2019t\u201d", "First person, direct, no corporate distance"],
  ["\u201cThe user\u201d / \u201cthe device\u201d", "\u201cYou\u201d / \u201cit\u201d (named if ambiguous)", "Third person here is the product discussing the person as if they\u2019d left the room"],
  ["\u201cSuccessfully completed\u201d", "Say what\u2019s true now", "\u201cSuccessfully completed\u201d is a system log line, not something a person says"],
])

TONE_ROWS = rows([
  ["Arrival", "Anticipation, not friction", "\u201cLet\u2019s make your home breathe easier\u201d", "A brand slogan detached from the moment"],
  ["Asking for something", "Low-stakes, reason up front", "\u201cWant the air sorted before you get home?\u201d", "A form label with a tooltip"],
  ["Waiting", "Named, bounded, released", "\u201cFifteen seconds or so\u201d", "A bare spinner, or \u201cPlease wait\u201d"],
  ["Something went wrong", "Device is the subject; offer the next move", "\u201cI can\u2019t see it yet. Usually it just needs a small nudge.\u201d", "\u201cInvalid\u201d, \u201cError\u201d, or blaming the user"],
  ["Success", "Warm, specific, closes the loop", "\u201cThat\u2019s the hard part done\u201d", "\u201cSetup complete.\u201d with nothing else"],
  ["Agent narrating itself", "First person, evidence over claims", "\u201cIt\u2019s 168 out there. I\u2019ve already started.\u201d", "Marketing copy about the product in third person"],
  ["System dialogs", "Not ours to write", "Leave the OS\u2019s register alone", "A chatty system dialog \u2014 reads as a fake one"],
])

REWRITE_ROWS = rows([
  ["Get started", "\u201cQuiet, clean air. One app.\u201d / [Get started]", "\u201cLet\u2019s make your home breathe easier.\u201d / slide to enter"],
  ["Phone number", "\u201cWhat\u2019s your number?\u201d", "\u201cFirst \u2014 how do I reach you?\u201d"],
  ["Profile", "\u201cWho are we setting this up for?\u201d", "\u201cAnd who am I looking after?\u201d"],
  ["Email verify", "\u201cCheck your email\u201d", "\u201cHave a look in your inbox\u201d"],
  ["Choose purifier", "\u201cWhich one is it?\u201d", "\u201cWhich one did you bring home?\u201d"],
  ["Plug in", "\u201cPlug it in and switch it on\u201d", "\u201cNow find it a socket\u201d"],
  ["Bluetooth", "\u201cSwitch on Bluetooth\u201d", "\u201cI\u2019ll need Bluetooth for a minute\u201d"],
  ["Connected", "\u201cYour purifier is set up\u201d", "\u201cThat\u2019s the hard part done\u201d"],
  ["Which room", "\u201cWhich room is it in?\u201d", "\u201cWhere does it live?\u201d"],
  ["Not found", "\u201cWe couldn\u2019t find your purifier\u201d", "\u201cI can\u2019t see it yet\u201d"],
])

BODY = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The NOMA Voice</title>
<style>{CSS}</style>
</head>
<body>

<!-- ============================ COVER ============================ -->
<div class="cover">
  <div class="cover-mark">NOMA · Voice &amp; Tone</div>
  <div class="cover-rule"></div>
  <h1 class="cover-title">The NOMA Voice</h1>
  <p class="cover-sub">How the app talks, everywhere — and why. A voice for a home that's
  looking after you, rather than a wizard processing you.</p>

  <div class="cover-status">
    <b>Status: draft — the register is settled app-wide, the speaker is not.</b><br>
    Every "I" in this document rides on <code>C-2</code>, still open: whether the product and
    the assistant are the same character. Treat every example as the register to hit, not the
    final shipped string.
  </div>

  <div class="cover-spacer"></div>

  <div class="cover-meta">
    <div><span>Version</span><b>0.1 · 2026-08-07</b></div>
    <div><span>Scope</span><b>App-wide</b></div>
    <div><span>Canonical for</span><b>tone-matrix.md · glossary.md</b></div>
    <div><span>Extends</span><b>ai-personas.md</b></div>
    <div><span>Blocked by</span><b>C-2 — the name</b></div>
    <div><span>Worked evidence</span><b>first-run/prd.md §8</b></div>
  </div>
</div>

<!-- ============================ CONTENTS ============================ -->
<div class="toc">
  <h2 style="margin-top:0"><span class="num">§</span>Contents</h2>
  <ol>
    <li>Why this exists</li>
    <li>What makes a setup flow feel like a conversation</li>
    <li>The seven rules</li>
    <li>Who is speaking — the open question</li>
    <li>Grammar and mechanics</li>
    <li>Vocabulary — words in, words out</li>
    <li>Tone by moment</li>
    <li>What stays literal, on purpose</li>
    <li>Errors, specifically</li>
    <li>Before / after — the actual rewrite</li>
    <li>Localization</li>
    <li>The checklist</li>
    <li>Where this applies beyond onboarding</li>
    <li>Cross-references</li>
  </ol>
</div>

<!-- ============================ 1 ============================ -->
<section>
<h2><span class="num">1</span>Why this exists</h2>
<p class="lede">The first build of onboarding copy was correct and lifeless. Every screen
followed the same shape — a headline stating what to do, a line of body text stating why, a
button labelled with the action. Nothing was wrong with it. Nothing in it sounded like anyone.</p>

<p>The owner's instruction was specific: <strong>stop writing instructions, start writing a
conversation.</strong> The app should talk about the house, refer to itself as "I", and sound
like it's genuinely interested in getting this right for you — not administering a checklist.</p>

<p>This document is the rule set that came out of that instruction. It is not a copy deck —
the actual strings live in <code>docs/features/first-run/prd.md</code> §8 and in the
prototype's source. This is the <em>why</em> behind them, written so the next hundred strings
can be judged against the same standard without re-deriving it.</p>
</section>

<!-- ============================ 2 ============================ -->
<section>
<h2><span class="num">2</span>What makes a setup flow feel like a conversation</h2>
<p class="lede">A wizard and a conversation can carry identical information and still feel
like opposite relationships. The difference sits in two structural habits, not in word
choice.</p>

<h3>A question and its reason arrive in the same breath</h3>
<p>If a screen asks for something, the next sentence — not the help text, not a linked policy
— says why. <em>"Where does it live?"</em> followed immediately by <em>"So I can compare your
air against the right patch of outdoors."</em> Left to be inferred, or deferred to a privacy
policy, the same ask reads as a form.</p>

<h3>Nothing is asked before the app has shown it understands the situation</h3>
<p>An ask that lands cold, with no context, reads as a form filling itself out at you. An ask
that follows an observation about what's actually in front of the user — a device that just
connected, a room that needs naming — reads as something a person would say next, not a step
in a sequence.</p>

<p>Neither habit is decorative. Both are trust-sequencing: the app earns the right to ask by
showing it already understands, before it asks.</p>
</section>

<!-- ============================ 3 ============================ -->
<section class="pagebreak">
<h2><span class="num">3</span>The seven rules</h2>
<p class="lede">Every rule below has a NOMA line already shipped in the prototype — these
aren't aspirational, they're a description of work already done, so they can be checked
against the artifact.</p>

<div class="rule"><h3><span class="rn">1</span>First person, singular</h3>
<p>The app is "I", not "we", not "the app". <em>"We'll text you a code"</em> becomes
<strong>"I'll need Bluetooth for a minute."</strong> A team behind a curtain is a company;
a single voice is something you can have a relationship with.</p></div>

<div class="rule"><h3><span class="rn">2</span>Ask, then say why, in the same breath</h3>
<p>The reason is never optional, never deferred, never longer than the ask.
<strong>"Where does it live?" → "So I can compare your air against the right patch of
outdoors."</strong> If the reason isn't in the next sentence, the screen fails this rule
regardless of its adjectives.</p></div>

<div class="rule"><h3><span class="rn">3</span>Take the anxiety out of the answer</h3>
<p>Setup questions carry tiny stakes that don't need to be there. <strong>"Only really matters
once there are two of them"</strong> about naming a device tells the user the question in
front of them carries almost no weight, so they can answer without overthinking.</p></div>

<div class="rule"><h3><span class="rn">4</span>"Let's" for shared work</h3>
<p>Anything framed as something both parties are doing reads as collaborative.
<strong>"Let's get the filter out of its bag"</strong> is a shared task; "remove the filter
from its packaging" is a work order. Same information, opposite relationship.</p></div>

<div class="rule"><h3><span class="rn">5</span>Privacy as a concrete negative, not a policy</h3>
<p>Never "your data is protected" — always the specific thing that does not happen, stated
plainly enough to picture. <strong>"I only notice you crossing in and out. I never keep a
trail of where you've been."</strong> A concrete negative is falsifiable, and therefore
trustworthy.</p></div>

<div class="rule"><h3><span class="rn">6</span>Warm buttons at warm moments</h3>
<p><strong>"Yes, do that"</strong> reads as an answer in a conversation. "Confirm" reads as UI
chrome. Reserve the warmest buttons for moments the user is glad to be there; keep
physical/technical steps a notch more plain, because those need to be found fast, not
savored.</p></div>

<div class="rule"><h3><span class="rn">7</span>Observation, then offer, then ask</h3>
<p>Never ask before demonstrating understanding. On Home: <strong>"It's 168 out there. I've
already started."</strong> — the observation and the action, before anything is asked at
all.</p></div>
</section>

<!-- ============================ 4 ============================ -->
<section class="pagebreak">
<h2><span class="num">4</span>Who is speaking — the open question</h2>
<p class="lede">Every "I" in this app is written as if the product itself is speaking. That
is a <strong>product decision wearing a copy decision's clothes</strong>, and it rides on
<code>C-2</code>, which is still open.</p>

<p><code>memory/voice/ai-personas.md</code> already established this exact register for the
ongoing product — first person, owns the action, never a bare status — but under a name that
was never settled (four different names for the assistant appear across the source material).
This document runs the same voice everywhere in the app, on the assumption that the thing
greeting you at the door and the thing telling you the filter's dying are the same
speaker.</p>

<div class="box crit">
<span class="bt">If they are not the same speaker</span>
If the product is NOMA and the agent is a separately named character that lives inside it,
every "I" in this flow needs re-attribution before it ships. That is not a global
find-and-replace: it changes whether the door, the setup wizard, and the agent's Day-2
proposals are one relationship or three introductions.
</div>

<p><strong>Resolve <code>C-2</code> before any string in this document becomes an i18n
key.</strong> Until then, treat every example here as the register, not the final line.</p>
</section>

<!-- ============================ 5 ============================ -->
<section>
<h2><span class="num">5</span>Grammar and mechanics</h2>
<p class="lede">Rules a writer or a reviewer can apply mechanically, independent of judgment
calls about warmth.</p>
<ul>
<li><strong>Contractions, always.</strong> "I'll", "it's", "you're" — never "I will", "it is".
A voice that doesn't contract reads as formal no matter what it's saying.</li>
<li><strong>First person for the app, second person for the user.</strong> "I'll need
Bluetooth", "your purifier". Never third person for either.</li>
<li><strong>Present tense for state, past tense for action taken.</strong> "It's on
Sharma_Home" (state); "I've already started" (action). Don't blur the two.</li>
<li><strong>No exclamation marks.</strong> Calm is the register; enthusiasm punctuation
undercuts it. Warmth comes from word choice, not punctuation.</li>
<li><strong>Sentence-case headlines, never Title Case.</strong> "Which one did you bring
home?" not "Which One Did You Bring Home?" — Title Case reads as a form label.</li>
<li><strong>Numerals, not spelled-out numbers</strong> — except a felt duration read aloud
("about twenty minutes") beats a measurement ("about 20 minutes"); a displayed number stays
numeral.</li>
<li><strong>Em dashes for the aside, not the semicolon.</strong> Conversational rhythm uses
dashes; semicolons read as written, not said.</li>
<li><strong>One idea per sentence.</strong> If a sentence needs a comma to hold two
instructions, it's two sentences. Read every line aloud — if you'd need to breathe
mid-sentence, split it.</li>
</ul>
</section>

<!-- ============================ 6 ============================ -->
<section class="pagebreak">
<h2><span class="num">6</span>Vocabulary — words in, words out</h2>
<p class="lede">Canonical source for <code>memory/voice/glossary.md</code>'s banned/approved
list.</p>
<table>
<thead><tr><th style="width:38mm">Banned (wizard voice)</th><th style="width:52mm">Use instead</th><th>Why</th></tr></thead>
<tbody>
{VOCAB_ROWS}
</tbody>
</table>

<div class="box quiet">
<span class="bt">Two words worth naming</span>
<strong>"Let's"</strong> (Rule 4) and <strong>"I'll"</strong> (Rule 1) carry real weight. If a
screen has neither a "let's" moment nor an "I'll" statement, check whether it needed a person
speaking at all, or whether it should stay plain (§8).
</div>
</section>

<!-- ============================ 7 ============================ -->
<section class="pagebreak">
<h2><span class="num">7</span>Tone by moment</h2>
<p class="lede">Not every screen wants the same amount of warmth. Each row is the register for
one moment, with a real line already in the prototype.</p>
<table>
<thead><tr><th style="width:30mm">Moment</th><th style="width:26mm">Target</th><th style="width:44mm">Do</th><th>Don't</th></tr></thead>
<tbody>
{TONE_ROWS}
</tbody>
</table>
</section>

<!-- ============================ 8 ============================ -->
<section>
<h2><span class="num">8</span>What stays literal, on purpose</h2>
<p class="lede">Two categories are deliberately not warmed up — a judgment call worth defending,
not an oversight.</p>

<h3>The instruction inside an instruction screen</h3>
<p>The frame around a physical step can be warm; the step itself has to stay literal, because
getting it slightly wrong costs the user real time with a purifier in pieces on the floor.
"Let's get the filter out of its bag" is warm framing; underneath it is still a precise
statement of a failure mode. Unwrapping the filter is the single most common invisible setup
failure in the whole flow — charm is not worth the ambiguity there.</p>

<h3>System dialogs</h3>
<p>iOS and Android own that register. A permission sheet written in NOMA's voice reads as a
spoofed system dialog, which is worse than a cold one — it looks like the app is trying to
sound official rather than being official.</p>
</section>

<!-- ============================ 9 ============================ -->
<section>
<h2><span class="num">9</span>Errors, specifically</h2>
<p class="lede">Errors are the hardest case: the app has to stay warm and stay unambiguous, and
those two goals fight harder here than anywhere else in the flow. Four rules, non-negotiable.</p>
<ol>
<li><strong>The device is the subject, never the user.</strong> "I can't see it yet", not "you
didn't hold your phone close enough." The user did not cause the failure; do not imply they
did.</li>
<li><strong>Every error offers the next move, not just a verdict.</strong> "Worth another
look?" — never a bare restatement of what failed.</li>
<li><strong>Never apologize on behalf of hardware.</strong> "Sorry, something went wrong" is
empty. State what happened and what still works instead.</li>
<li><strong>The fix stays literal even when the frame is warm.</strong> "That password didn't
work. Worth another go?" is warm framing around a precise, unambiguous fact.</li>
</ol>
</section>

<!-- ============================ 10 ============================ -->
<section class="pagebreak">
<h2><span class="num">10</span>Before / after — the actual rewrite</h2>
<p class="lede">Ten screens from the shipped prototype, as they were and as they are now. This
is the concrete evidence the rules above describe.</p>
<table class="tight">
<thead><tr><th style="width:32mm">Screen</th><th style="width:56mm">Before</th><th>After</th></tr></thead>
<tbody>
{REWRITE_ROWS}
</tbody>
</table>
</section>

<!-- ============================ 11 ============================ -->
<section>
<h2><span class="num">11</span>Localization</h2>
<p class="lede">This voice raises the translation bar. Idiomatic phrases &mdash; &ldquo;a
spare key&rdquo;, &ldquo;hum away happily&rdquo;, &ldquo;already spoken for&rdquo; &mdash;
carry meaning through cultural reference, not through their literal words. A machine or
literal translation of any of them into Hindi will read as broken, not warm.</p>

<div class="box warn">
<span class="bt">This needs transcreation, not translation</span>
Budget a native-voice pass that re-derives the <em>feeling</em> of each line in Hindi, rather
than translating the English sentence. The seven rules in §3 should hold in Hindi even where
the specific idioms don't survive.
</div>

<p><code>hi</code> is required for this flow, not deferred &mdash;
<code>memory/voice/ai-personas.md</code> already flags that a resident persona with low app
fluency is exactly the case an English-only setup fails. This voice makes that requirement
more expensive, not less necessary.</p>
</section>

<!-- ============================ 12 ============================ -->
<section class="pagebreak">
<h2><span class="num">12</span>The checklist</h2>
<p class="lede">Before a new string ships, run it against these eight questions.</p>
<ol>
<li>Would a person actually say this out loud to someone in their home?</li>
<li>Is the reason for the ask in the same sentence or the very next one?</li>
<li>If this is an error, is the device the subject &mdash; not the user?</li>
<li>Does every error offer a next move, not just a verdict?</li>
<li>Is there a wait here that isn&rsquo;t named and bounded?</li>
<li>Did this sentence need a comma to hold two instructions? If so, split it.</li>
<li>Is this a physical/technical instruction dressed in so much warmth that it&rsquo;s gotten
ambiguous? (&sect;8 &mdash; the frame can be warm; the instruction can&rsquo;t blur.)</li>
<li>Is this a system dialog? If yes, leave it in the OS&rsquo;s own voice.</li>
</ol>
<p>A string that fails any of these isn&rsquo;t necessarily wrong, but it needs a reason to
survive the exception, and that reason should be written down next to it &mdash; as every
deliberate exception in §8 is here.</p>
</section>

<!-- ============================ 13 ============================ -->
<section class="pagebreak">
<h2><span class="num">13</span>Where this applies beyond onboarding</h2>
<p class="lede">This document generalized from an onboarding-only PRD to an app-wide one on
2026-08-07, because the register it describes was never actually specific to setup &mdash; a
wizard-vs-conversation problem shows up anywhere the app has to ask something, wait for
something, or report back. The seven rules, the grammar in §5, and the banned words in §6
apply without modification to every surface below. What changes by surface is <em>how much
warmth a moment can carry</em> (§7 already covers this axis) &mdash; not the rules
themselves.</p>

<p><strong>Reconciling with <code>ai-personas.md</code>.</strong> That document already
specified the ongoing-product voice &mdash; first person, owns the action, pairs a number
with a consequence, anchors units to something human, never volunteers alarm &mdash; derived
independently from PM prototype material for notifications and Home. It does not conflict
with anything here; it's a <em>superset</em> for those two surfaces, with rules specific to
what an ambient, always-on voice needs that a one-time setup flow doesn't (the
night-hook/morning-proof pairing, the share-caption exception where brand voice must
disappear entirely). Read both for Home and notifications; this document alone is sufficient
everywhere else.</p>

<h3>Surface by surface — what's rewritten, and what's still owed</h3>
<table class="tight">
<thead><tr><th style="width:38mm">Surface</th><th style="width:34mm">Status</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Onboarding &amp; device setup</td><td><strong>Rewritten and shipped.</strong></td><td>The worked evidence throughout this document. <code>first-run/prd.md</code> §8.</td></tr>
<tr><td>Home &amp; notifications</td><td><strong>Already this register</strong>, via <code>ai-personas.md</code></td><td>Written independently but consistent with the rules here. Extend, don&rsquo;t duplicate.</td></tr>
<tr><td><strong>My Home</strong> (six-state dashboard prototype)</td><td><strong>Not yet rewritten.</strong></td><td><code>docs/features/my-home/build-home.py</code> has its own copy, written before this voice existed. Next concrete pass.</td></tr>
<tr><td>Sharing / People, Automations, Shop, Settings</td><td><strong>No prototype exists yet.</strong></td><td>Apply the checklist (§12) at first-draft time rather than retrofitting later &mdash; cheaper than a second pass.</td></tr>
<tr><td>Errors app-wide</td><td><strong>§9&rsquo;s four rules apply everywhere</strong>, not just onboarding&rsquo;s error states.</td><td>The device (or the automation, or the routine) stays the subject; every error still offers a next move.</td></tr>
</tbody>
</table>

<div class="box warn">
<span class="bt">Do not mark a surface done from belief</span>
A surface isn't in this voice because someone believes it is; it's in this voice because a
specific line can be pointed at, the same way §10's before/after table checks onboarding.
</div>
</section>

<!-- ============================ 14 ============================ -->
<section>
<h2><span class="num">14</span>Cross-references</h2>
<div class="kv">
<dt><code>ai-personas.md</code></dt><dd>The ongoing-product voice for Home and notifications, reconciled with this document in §13. Read it first if <code>C-2</code> closes and every &ldquo;I&rdquo; needs re-attribution.</dd>
<dt><code>tone-matrix.md</code></dt><dd><strong>This document is canonical for all its rows</strong>, not just onboarding. The stub should point here rather than duplicate this content.</dd>
<dt><code>glossary.md</code></dt><dd><strong>This document is canonical for §6&rsquo;s banned/approved words.</strong></dd>
<dt><code>first-run/prd.md</code> §8</dt><dd>The onboarding copy this document explains, screen by screen &mdash; the only surface fully checked against §10&rsquo;s before/after standard so far.</dd>
<dt><code>decisions.md</code> C-2</dt><dd>The open blocker on who &ldquo;I&rdquo; is.</dd>
</div>

<footer class="doc">
The NOMA Voice · v0.1 · 2026-08-07 · generalized app-wide the same day it was compiled from
the first-run prototype's shipped copy. Every rule here is checked against a real,
already-written line, and §13 tracks exactly how far the rewrite has actually reached.
Canonical markdown: <code>docs/voice/voice-prd.md</code>.
</footer>
</section>

</body>
</html>
"""

OUT_HTML.write_text(BODY)
print(f"wrote {OUT_HTML.relative_to(ROOT)}  {len(BODY)/1024:.0f} KB")

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
chrome = next((c for c in CHROME_CANDIDATES if pathlib.Path(c).exists()), None)
if not chrome:
    print("No Chrome/Chromium found — render the PDF manually:")
    print(f'  <path-to-chrome> --headless --no-pdf-header-footer --print-to-pdf="{OUT_PDF}" "{OUT_HTML}"')
    sys.exit(0)

cmd = [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
       f"--print-to-pdf={OUT_PDF}", f"file://{OUT_HTML}"]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if r.returncode != 0 or not OUT_PDF.exists():
    print("PDF render failed:", r.returncode, r.stderr[-2000:])
    sys.exit(1)
print(f"wrote {OUT_PDF.relative_to(ROOT)}  {OUT_PDF.stat().st_size/1024:.0f} KB")
