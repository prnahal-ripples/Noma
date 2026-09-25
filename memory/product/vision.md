# Product Vision & Principles

## The name

**Noma** · [noh-mah] · noun

From two Japanese roots:
- **ma** (間) — the *intentional* space between things
- **no** (野) — nature, openness

> A philosophy of creating homes where thoughtful spaces and everyday rituals
> come together.

## What it is

A **smart-home app** for a connected-device ecosystem — air purifiers, cameras,
door locks, and wearables — unified into one calm surface. The product promise is
not "control your gadgets"; it is **peace of mind about your home and the people
in it**, without checking six apps.

Device brand seen in strategy material: **Ding** (cameras). Hardware truth is
canonical in `src/hardware/devices.json`.

## Why the name is a design constraint, not decoration

`ma` is the load-bearing idea. It means the empty space is *doing work* — it is
composed, not left over. This translates directly and testably:

- **Whitespace is a feature.** If a screen looks sparse, that is likely correct.
  Resist the urge to fill. Density is a failure mode here, not a virtue.
- **One idea per screen.** The primary action should be findable in one glance.
  Same instinct as the 10% accent rule — scarcity creates focus.
- **Calm over informative.** Show the state of things, not every metric that
  produced it. Detail is available on demand, never volunteered.
- **`no` (nature/openness)** is why the palette is warm neutrals and green
  rather than the cool blue-grey default of the smart-home category. Noma should
  feel like a well-lit room with a plant in it, not a control panel.

## Considerations (owner-supplied)

| Axis | Direction |
|---|---|
| **Visual language** | Friendly & approachable — soft, rounded forms make technology feel warm and inviting. |
| **Typography** | Minimal & neutral — clean sans-serif, complementing playful iconography. |
| **Motion** | Playful micro-interactions — gentle scale, bounce, and hover animations add personality. |

The first two are already satisfied by the foundation: generous radii
(`radius.md` 12 / `radius.xl` 20) give the soft rounded forms, and Google Sans
Flex (ADR-002) is deliberately neutral so the iconography carries personality.

**Resolved — ADR-005.** "Playful bounce" and `ma`-driven calm split by surface:
spring on discrete moments (taps, arrivals, confirmations), stillness on ambient
monitoring. Canonical values: `src/tokens/motion.tokens.js`.

## What the app should feel like

Warm, quiet, and certain. The emotional target is **relief**, not delight — a
glance that confirms everything is fine. Personality lives in small moments
(icons, transitions, a status dot going green), never in the chrome.

Deliberately *not*: dashboard-dense, blue-lit, alarm-forward, or gamified.

## What the app will never do

- Never make the accent green the ground. It marks one action; it is not decor.
- Never volunteer alarm. Urgency is earned by real events, not by styling.
- Never require app fluency for basic safety (a resident persona has low
  fluency — see `memory/product/personas.md`).

## Positioning reference

Airbnb iOS is the **visual** reference for surface, radius, and elevation
(ADR-001) — not a product or IA reference. Its warmth was taken; its density
and its red were not.
