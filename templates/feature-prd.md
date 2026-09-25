# TEMPLATE — Feature PRD

> Copy to `docs/features/<feature>/prd.md`. One PRD per `F-*` id.
> Master product PRD lives at `docs/prd/noma-v1.md` — read it first for context.

---

# F-XXX · <Feature name>

| | |
|---|---|
| **Status** | draft · in review · approved · built |
| **Owner** | TODO |
| **F-id** | `F-XXX` (must exist in `src/hardware/feature-map.json`) |
| **Journeys** | `J-*` steps this feature serves |
| **Blocked by** | `C-#` / `O-#` or "nothing" |

## 1. Problem
What is broken or missing for the user. One paragraph, user-side language.

## 2. Why now
Evidence. Link the source (research, prototype, conflict). No unsourced claims.

## 3. Users
Which `P*` personas, and what each needs differently.

## 4. Scope
**In.** Bulleted, testable.
**Out.** Explicit — what this feature deliberately does not do.

## 5. Behaviour
The rules. Include every state: empty, loading, error, offline, declined-permission.
A PRD without an error state is not finished.

## 6. Acceptance criteria
Numbered, each independently verifiable.

## 7. Design
Token references only (`radius.md`, `elevation.card`, `accent.solid`…). Never hexes.
Motion: name the `MO-*` pattern from `memory/motion/patterns.md`.

## 8. Copy
Every user-facing string, as an i18n key + English value. Flag anything needing `hi`.

## 9. Risks
What could go wrong, and the mitigation.

---

## Declares
> Mandatory. This block is what makes the PRD machine-checkable.

**Data** — entities and fields created or changed (see `memory/architecture/data-models.md`).
**Events** — analytics events fired, each mapped to a `J-*` step. Write `none` if none.
**Hardware** — `HW-*` ids touched, and any capability required from `feature-map.json`.
