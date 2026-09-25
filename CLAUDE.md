# CLAUDE.md — Entry Point (routes, never contains)

One-line product description: TODO(owner): describe the app in one sentence.

## Non-negotiable rules
1. Read `memory/session-handoff.md` FIRST in every session.
2. One canonical home per fact. Machine-readable files in `src/` win over markdown mirrors.
3. Cross-reference by stable IDs only (P1, J-ONBOARD-03, F-*, HW-*, S-*, ADR-###) — never by prose.
4. No hardcoded colors/durations/strings — use tokens and i18n keys.
5. Every new event, persona, feature, or motion pattern starts from a file in `templates/`.
6. Flag conflicts in `memory/decisions.md`; never silently pick a winner.
7. Update `memory/changelog.md` and `memory/session-handoff.md` at the end of every session.

## Where to find things
| Question | File |
|---|---|
| What is the current state / what's next? | memory/session-handoff.md |
| Master map of all knowledge | memory/index.md |
| Who are the users? | memory/product/personas.md (canonical: src/personas/personas.json) |
| User journeys & step IDs | memory/product/journeys.md |
| What's out of scope? | memory/product/scope-ledger.md |
| **How the product speaks (canonical)** | **docs/voice/noma-voice-guide.md** — run `docs/voice/audit-voice.py` before shipping copy |
| Tone & voice per persona | memory/voice/tone-matrix.md (pointer) |
| AI persona prompts | src/personas/prompts/ (docs: memory/voice/ai-personas.md) |
| Approved terminology per language | memory/voice/glossary.md |
| Design tokens | src/tokens/design.tokens.js |
| Motion philosophy & tokens | memory/motion/philosophy.md (canonical: src/tokens/motion.tokens.js) |
| Analytics events | src/analytics/events.schema.json (docs: memory/analytics/event-taxonomy.md) |
| Journey → event trigger map | memory/analytics/trigger-map.md |
| Monetization surfaces | memory/analytics/monetization-map.md |
| System architecture | memory/architecture/system.md |
| Why was X decided? | memory/decisions.md |
| Feature status & PRDs | docs/index.md, docs/features/<feature>/prd.md |

## Enforced gates
See `.claude/rules/` — every rule there is greppable and part of the pre-commit checklist.
