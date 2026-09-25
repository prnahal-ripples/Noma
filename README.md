# Noma

**Noma** · [noh-mah] · from Japanese **ma** (間, the *intentional* space between things) and **no** (野, nature/openness).

A **smart-home app** for a connected-device ecosystem — air purifiers, cameras, door locks, and wearables — unified into one calm surface. The promise isn't "control your gadgets"; it's **peace of mind about your home and the people in it**, without checking six apps.

> `ma` is a design constraint, not decoration: whitespace is a feature, one idea per screen, calm over informative, warm neutrals over the category's cool blue-grey. See [`memory/product/vision.md`](memory/product/vision.md).

---

## What this repository is

This is **not application code (yet)**. It is the **source of truth** — a structured knowledge base that both humans and AI agents fill in and build the product against. The system in one line:

> **`CLAUDE.md` routes → `memory/` holds → `docs/` plans → `.claude/rules/` enforces → `src/` is canonical machine truth.**

New to the repo? Read [`START-HERE.md`](START-HERE.md) first (written for humans), then [`CLAUDE.md`](CLAUDE.md) (the entry point for agents).

## Layout

| Path | What lives here |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Entry point — **routes** to everything, holds nothing. Non-negotiable rules + a "where to find things" map. |
| [`memory/`](memory/) | The knowledge that holds: product vision, personas, journeys, architecture, motion, voice, analytics. [`memory/index.md`](memory/index.md) is the master map. |
| [`docs/`](docs/) | Plans and source material: feature PRDs, design docs, research (competitive teardowns, reference book), voice guide. [`docs/index.md`](docs/index.md) indexes it. |
| [`src/`](src/) | **Canonical machine-readable truth** — design tokens, motion tokens, hardware specs (`devices.json`, `feature-map.json`), analytics event schema, i18n, persona prompts. Where a `src/` file and a markdown mirror disagree, `src/` wins. |
| [`.claude/rules/`](.claude/rules/) | Enforced gates — greppable rules that are part of the pre-commit checklist. |
| [`templates/`](templates/) | Starting points. Every new event, persona, feature, or motion pattern starts from a file here. |
| [`design-elements/`](design-elements/) | Brand and UI assets: 3D/engraved icons, bottom nav & sheets, illustrations, renders. |
| [`data/`](data/) | Fixtures, evals, and edge cases. |

## Core rules

These are enforced (see [`CLAUDE.md`](CLAUDE.md) and `.claude/rules/`):

1. Read `memory/session-handoff.md` **first** in every session.
2. **One canonical home per fact.** Machine-readable files in `src/` win over markdown mirrors.
3. Cross-reference by **stable IDs** only (`P1`, `J-ONBOARD-03`, `F-*`, `HW-*`, `S-*`, `ADR-###`) — never by prose.
4. **No hardcoded** colors/durations/strings — use tokens and i18n keys.
5. Every new event, persona, feature, or motion pattern **starts from `templates/`**.
6. Flag conflicts in `memory/decisions.md`; never silently pick a winner.
7. Update `memory/changelog.md` and `memory/session-handoff.md` at the **end** of every session.

## Working with this repo

It's designed to be opened with [Claude Code](https://claude.com/claude-code):

```bash
cd Noma-main
claude
```

The agent reads `CLAUDE.md`, follows the routes, and works against the canonical files in `src/`. To orient yourself as a human, start at `START-HERE.md` → `memory/index.md` → `docs/index.md`.

## Status

Early — a knowledge skeleton in active build-out. Several canonical files are still stubs or empty (tracked as open items in `memory/index.md`, e.g. `src/personas/personas.json`, `src/tokens/motion.tokens.js`, PRDs under `docs/features/`). Current state and next steps always live in **`memory/session-handoff.md`**.
