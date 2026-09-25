# Tone Matrix

> **Canonical: `docs/voice/noma-voice-guide.md`** (v1.2-draft, 14 Aug 2026).
> This file is a pointer, not a copy. If the two disagree, the guide wins.

The guide replaced the old `docs/voice/voice-prd.md` on 2026-08-14. It carries
**two dials**, not one, which is the substantive change from what this stub
used to describe:

- **§7.1 the severity dial** — Safety (T-01) · Urgent (T-02) · Friction (T-03)
  · Everyday (T-04). Warmth *drops* as severity climbs, and **severity always
  wins** over the moment dial. At T-01 the voice steps back entirely: no "I",
  no warmth, imperative only.
- **§7.2 the moment dial** — arrival, asking, waiting, acting live, reporting,
  success, broken streak, something wrong, selling, system dialogs.

⚠ **Persona × context is still unfilled here, and is no longer the blocker it
was.** The guide sets the register by *reader* in §2 (Asha, Ravi & Lakshmi, the
household help, Priya) with the instruction "when in doubt, write for Ravi".
That is not the same as a persona × moment grid, which nobody has needed yet.
C-1 (personas unresolved) still blocks naming the readers in the product.

Machine-checkable rules run in CI: `python3 docs/voice/audit-voice.py`.
