# Docs Index — feature status & source material

## Engineering

| File | What it is |
|---|---|
| **`docs/engineering/claude-launch-json-conflicts.md`** | **Why `.claude/launch.json` conflicted on every push, and the fix — applies to any repo, nothing NOMA-specific.** It is machine-local state (Claude Code writes session-scoped `/private/tmp` paths into it) that was tracked in git, so it was permanently dirty, conflicted between sessions, and rode into three unrelated commits. Fixed by untracking + gitignoring it and shipping a per-project template beside it. ⚠ The live filename cannot change — the preview tooling reads that exact path. Procedure is tested end to end, including a two-clone reproduction of the conflict. |

## Research

| File | What it is |
|---|---|
| **`docs/research/NOMA-first-run-references.pdf`** | **21-page reference book — the shareable one.** 17 stages of first run, each with five annotated competitor references (app · flow · screen · verbatim copy · take-or-avoid), what NOMA does, and the rules it sets. **69 of the 85 tiles are real Mobbin captures**; 15 are labelled redrawn wireframes; 1 is ours. |
| `docs/research/refs-print.html` | Print source. Regenerate with `python3 docs/research/build-refs.py`, then the headless-Chrome command in that script's docstring. |
| `docs/research/build-refs.py` | Generator. All 85 reference tiles live here as data. A slug with a real file at `refs/<slug>.png` always beats its wireframe. |
| `docs/research/fetch-refs.py` | The capture pipeline: `add` downloads a flow's screens from Mobbin MCP short URLs, `sheet` builds a numbered montage to identify positions, `bind` copies chosen screens to `refs/<slug>.png`, `status` reports coverage. |
| `docs/research/refs-map.json` | All 85 slugs with their source app / flow / screen and whether a real capture is present. Generated — never edit by hand. |
| `docs/research/refs/` | The captures. `refs/_raw/<flow>/` keeps every downloaded screen so re-binding never re-downloads. |
| `docs/research/2026-08-05-setup-teardown.md` | **Competitive teardown of first run, device setup and household invites.** 9 flows / ~130 screens across the five smart-home apps Mobbin carries. Twelve patterns extracted with attribution, plus the anti-patterns. Feeds `docs/features/first-run/prd.md`. |

Captures come from **Mobbin's MCP connector** (`https://api.mobbin.com/mcp`, registered in
`~/.claude.json`, OAuth). Its `search_flows` returns every screen of a flow with a plain short URL
that `curl` can fetch — which is what made the real screenshots possible. The 15 remaining
wireframes sit in flows that search did not return, mostly account-creation and settings screens;
page 2 of the PDF lists them.


## Master PRD

| File | What it is |
|---|---|
| **`docs/prd/NOMA-v1-PRD.pdf`** | **36-page typeset PRD — the shareable one.** Set in Google Sans Flex, with printed colour swatches and the measured contrast table. |
| `docs/prd/noma-v1.md` | The same content as markdown, for diffing and editing |
| `docs/prd/prd-print.html` | Print source. Regenerate the PDF with headless Chrome — see the comment at the top of the file. |

Covers the whole product as supplied to date: problem, personas, the agent
architecture, the Week One arc, journeys, features, hardware, the data model,
permissions, privacy, competitors, monetization, voice, the design system, motion,
metrics, risks, and all thirteen open conflicts. **Read it before any feature PRD.**

It opens with the one decision everything waits on: the material describes two
different products (a purifier companion and a whole-home platform) and nothing says
which ships first.

## Feature PRDs

| File | Covers | Status |
|---|---|---|
| `docs/features/first-run/prd.md` | **The first thirty minutes** — `J-ONBOARD-*`, `J-PAIR-PUR-*`, `J-SHARE-*`, `J-WEEK-01`. Section ordering is an open decision; see the wireframes. | draft, 2026-08-05 |
| **`docs/features/my-home/my-home-prototype.html`** | **The My Home page — six states, two strata, report sheet, notification feed.** Built from `ding-my-home-prd.md`; fixture mirrors that PRD's §7 interfaces. ⚠ Built in the light palette, not the PRD's dark one — see C-14. Regenerate with `python3 docs/features/my-home/build-home.py`. | draft, 2026-08-05 |
| **`docs/features/first-run/first-run-prototype.html`** | **Tappable prototype — light theme, one phone, controller on the left.** The flow as built: **32 screens across 22 nodes + branch 18a**, plus 13 edge states, a jumpable node list and a button to fire each state. Node 6 offers three purifier SKUs; nodes 7–12 are the 2026-08-06 pairing sequence (filter unwrap → plug in → light → Bluetooth → device list → Wi-Fi auto-fetch); node 15 runs a feature carousel over the setup wait. Nodes 19–22 were removed. Open it in a browser; arrow keys work. Regenerate with `python3 docs/features/first-run/build-prototype.py`. | **rebuilt 2026-08-06** |
| **`docs/voice/NOMA-Voice-PRD.pdf`** | **Voice & Tone PRD, app-wide** — how the app talks, everywhere, under explicit owner direction to read as a conversation rather than a wizard. Seven rules, grammar mechanics, a banned/approved vocabulary, tone-by-moment table, the actual onboarding before/after rewrite (its worked evidence), a surface-by-surface status table (§13 — onboarding shipped, My Home and everything else still owed), and an eight-question ship checklist. Canonical for `memory/voice/tone-matrix.md` and `glossary.md`. ⚠ Every "I" in it rides on `C-2` (open). Canonical markdown: `docs/voice/voice-prd.md`. Regenerate: `python3 docs/voice/build-voice-pdf.py`. | **generalized app-wide 2026-08-07** |
| **`docs/features/first-run/first-run-export.html`** | **Clean shareable export — one phone, tappable, nothing else.** No controller rail, no node numbers, no design notes, no simulate buttons. Send this to someone who should *experience* the flow; send the prototype to someone who should review it. Generated from `build-prototype.py`. ⚠ The 13 edge states are unreachable by tapping here (the sim buttons that reached them are stripped) — they remain hash-addressable, e.g. `#W2E`. Regenerate with `python3 docs/features/first-run/build-export.py`. | **new 2026-08-06** |
| `docs/features/first-run/first-run-wireframes.html` | The same flow as a printable board, grouped by diagram node with each node's edge states beside it. **Generated from `build-prototype.py` — it defines no screens of its own**, so the two can no longer disagree. Regenerate with `python3 docs/features/first-run/build-wireframes.py`. | **rebuilt 2026-08-06** |
| **`docs/features/first-run/first-run-mobile.html`** | **The flow on an actual handset — no phone frame, no controller, no scaling.** `.phone` becomes the viewport, so the device you are holding *is* the prototype. Open it on a phone to judge the key card's **gyro shimmer**, which cannot be assessed on a laptop (the desktop pointer fallback only approximates it). ⚠ Opens on a one-tap gate: iOS refuses `DeviceOrientationEvent` unless permission is requested inside a real gesture, and the harness's own prompt does not bind until node 5b — several taps in. The gate is that gesture, and it also holds the flow, since node 1 now auto-advances after 1s. Generated from `build-prototype.py`; sim buttons stripped as in the export, edge states still hash-addressable. Regenerate with `python3 docs/features/first-run/build-mobile.py`. | **new 2026-08-20** |

⚠ That PRD is written against **two proposed, unassigned ids** (`F-FIRST-RUN`, `F-SETUP`)
because the registry has no feature for "get a new customer to a working first device".
See `O-8` in `memory/decisions.md`.

Twelve of the thirteen registered features in `src/hardware/feature-map.json` still have
`prdStatus: none`. Start from `templates/feature-prd.md` (populated — it requires a
`declares` block and explicit error/empty/offline states).

Highest-leverage first, by what they unblock:

| F-* | Why first |
|---|---|
| `F-AQI-LIVE` | The #1 stated return-driver. Everything else sits on it. |
| `F-FILTER-HEALTH` | The differentiator *and* the recurring revenue. Blocked by C-7. |
| `F-AGENT-PROPOSE` | Determines what the app *is*. Architecture already written up. |
| `F-SHOP` | The only path to recurring revenue; currently has no transaction. |

---

## PM prototype set — the source material

Four HTML prototypes supplied 2026-08-04. **These are the origin of nearly everything in
`memory/` and `src/hardware/`.** They are design prototypes, not specifications: seeded
data, happy paths only, no empty/error/loading states, and no PRD behind any of them.

Original files live outside the repo (owner's `~/Downloads`). ⚠ **They should be vendored
into `docs/prototypes/` or archived somewhere durable** — right now the provenance of the
entire knowledge base is a local Downloads folder.

| File | Title | What it is | Pillars it fed |
|---|---|---|---|
| `air-agent-app.html` | *Air Agent — agent-first sample UI (C2)* | **The most valuable document.** The graduated-autonomy agent model: three home zones, per-capability autonomy tiers, the four-slot explanation contract, inert editable rehearsal, standing rules. | Tech, User flows, Content |
| `Ding_Air_Purifier_Week_One.html` | *Ding Air Pro · Air Week One* | A day-by-day first-week retention arc. Each day states its emotional target, the research finding behind it, and the screen that delivers it. The closest thing to a product spec received. | Product, User flows, Content, Analytics |
| `Ding App - White & Blue Launch V2...html` | *Ding — Smart Home App (V2)* | The broadest build: ~60 screens across onboarding, purifier, vacuum, camera, sharing, shop, score, wearable bridge. 13MB, all content inside 739KB of JSX. | Hardware, Database, Product, Tech |
| `noise_sanctuary_final (1).html` | *Noise Sanctuary — India's most trustworthy purifier* | Positioning and commercial strategy: the AQI-weighted filter argument, a five-way competitor teardown, three subscription tiers, the whole-home ecosystem pitch. | Product, Monetization, Hardware |

### Reading order for someone new

1. `Ding_Air_Purifier_Week_One.html` — **why** the product exists, and the behavioural
   reasoning. Start here; it is the only document that argues rather than asserts.
2. `air-agent-app.html` — **what** the app fundamentally is.
3. `noise_sanctuary_final (1).html` — the commercial case and competitors.
4. The launch app — the widest surface inventory. Treat its naming as unreliable; it is
   the source of most of C-2…C-13.

### Health warning

The four documents **disagree with each other on nearly every naming decision** — product
name, assistant name, fan modes, roles, prices, score dimensions, room presets. Twelve
conflicts (`C-2`…`C-13`) are logged in `memory/decisions.md`. Do not treat any single
prototype as canonical; check the conflict log before building against a name or a number.

They also split across **two different products**: a focused purifier companion and a
whole-home platform. Which ships first is unstated — see `memory/product/scope-ledger.md`.
