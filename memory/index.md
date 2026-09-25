# Memory Index — Master Map

> Question → file. Update whenever a memory file is added.
> **Rule 2:** machine-readable files in `src/` beat markdown mirrors. Where both exist,
> the `src/` file wins and the markdown says so.

---

## Start here

| Question | File |
|---|---|
| What's the current state / what's next? | `memory/session-handoff.md` |
| Why was X decided? What's unresolved? | `memory/decisions.md` |
| What source material do we actually have? | `docs/index.md` |

## Product

| Question | Canonical | Mirror |
|---|---|---|
| What is Noma, and what must it feel like? | — | `memory/product/vision.md` |
| Who are the users? | `src/personas/personas.json` ⚠ *empty — C-1* | `memory/product/personas.md` |
| What are the user journeys and step IDs? | — | `memory/product/journeys.md` |
| What's in and out of scope? What's missing? | — | `memory/product/scope-ledger.md` |
| Which features exist, and what do they need? | `src/hardware/feature-map.json` | — |
| Feature status & PRDs | `docs/index.md` ⚠ *zero PRDs* | — |

## Design

| Question | Canonical | Mirror |
|---|---|---|
| Colour, type, radius, elevation, spacing | `src/tokens/design.tokens.js` | — |
| Motion durations & easings | `src/tokens/motion.tokens.js` ⚠ *empty — O-7* | `memory/motion/philosophy.md` |
| Motion patterns | — | `memory/motion/patterns.md` |
| Fonts | `src/fonts/google-sans-flex/` | ADR-002 |
| Approved, running components | `.claude/rules/design-system.md` Approved Components | `design-elements/README.md` |

## Architecture

| Question | File |
|---|---|
| **How does the agent work?** *(read before any agent surface)* | `memory/architecture/ai-integration.md` |
| How is the system put together? | `memory/architecture/system.md` |
| What are the entities and their fields? | `memory/architecture/data-models.md` |
| API contracts | `memory/architecture/api-contracts.md` ⚠ *stub — none exist* |

## Hardware

| Question | Canonical |
|---|---|
| Which devices, models, specs, consumables? | `src/hardware/devices.json` |
| Sensors, connectivity, modes | `src/hardware/devices.json` |
| Wearable signals | `src/hardware/devices.json` → `wearables.triggers` |
| Feature → device support matrix | `src/hardware/feature-map.json` |

## Voice & content

| Question | Canonical | Mirror |
|---|---|---|
| How does the assistant speak? | `src/personas/prompts/` ⚠ *empty — C-2* | `memory/voice/ai-personas.md` |
| Tone per persona | — | `memory/voice/tone-matrix.md` ⚠ *stub — blocked by C-1* |
| Approved terminology | — | `memory/voice/glossary.md` ⚠ *stub — blocked by C-2* |
| User-facing strings | `src/i18n/locales/` ⚠ *stubs; `hi` blocked by O-5* | — |

## Analytics & money

| Question | Canonical | Mirror |
|---|---|---|
| Which events exist? | `src/analytics/events.schema.json` ⚠ **empty — zero events** | `memory/analytics/event-taxonomy.md` |
| Funnels | `src/analytics/funnels.json` ⚠ *stub* | `memory/analytics/funnels.md` |
| Journey step → event map | — | `memory/analytics/trigger-map.md` |
| Metric definitions | — | `memory/analytics/metrics-dictionary.md` ⚠ *stub* |
| Pricing, plans, upsell surfaces | — | `memory/analytics/monetization-map.md` |

## ID prefixes

| Prefix | Means | Lives in |
|---|---|---|
| `P1`–`P4` / `A1`–`A2` | Personas (provisional — C-1) | `memory/product/personas.md` |
| `J-*` | Journey step | `memory/product/journeys.md` |
| `F-*` | Feature | `src/hardware/feature-map.json` |
| `HW-*` | Device / consumable | `src/hardware/devices.json` |
| `ADR-###` | Decision record | `memory/decisions.md` |
| `C-#` | Open conflict — never silently resolve | `memory/decisions.md` |
| `O-#` | Open question | `memory/decisions.md` |

## Where the biggest holes are

1. **`C-2`** — the product and assistant have five names. Blocks all copy and i18n.
2. **Zero analytics events** — a named 7-day retention strategy with no measurement.
3. **`C-7`** — the core differentiator (AQI-weighted filter life) has no formula.
4. **No payment flow** — the recurring-revenue path stops at a price tag.
5. **Zero PRDs** — thirteen `F-*` features, none specified.
