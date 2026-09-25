# Event Taxonomy

> Canonical schema: `src/analytics/events.schema.json` — **still empty, deliberately.**

---

## The honest finding

**The PM prototypes contain zero analytics instrumentation.** Searched all four files
for `track(`, `logEvent(`, `analytics`, `gtag`, `amplitude`, `mixpanel` — no matches.
Not one event is fired anywhere.

This is worth stating plainly rather than papering over: the product has a fully
articulated seven-day retention strategy (`J-WEEK-01`…`07`) with named chokepoints and
stated behavioural mechanisms — **and no way to measure any of it.**

`src/analytics/events.schema.json` stays empty. Inventing an event taxonomy here would
create a machine-readable file that looks authoritative and was guessed, which is worse
than an empty one (CLAUDE.md rules 2 and 6).

---

## What the strategy already commits to measuring

The docs make measurable claims. These are the events the taxonomy *will* need — listed
as **requirements, not as a registry**, and deliberately unnamed so nobody greps this
file and ships them.

**Retention spine.** The Week One arc is a funnel with an explicit chokepoint at
Day 7 → Week 2. Measuring it needs: first-reading viewed, morning-card opened,
routine accepted, share initiated, energy card viewed, air-map viewed, recap viewed.
Each maps 1:1 to a `J-WEEK-*` step.

**The three JTBD return-drivers** are ranked in the source, so the ranking is a
falsifiable hypothesis. Needs: app-open attributed to a reason (AQI check vs remote
control vs automation trust).

**Agent trust — the richest and most novel surface.** The autonomy ladder is driven by
a *consecutive-accept tally*, so proposal accept / defer / decline / undo are not
optional analytics, they are **application state** that also happens to be the single
best measure of whether the agent is trusted. Also needed: autonomy promotion offered,
accepted, declined; and per-capability reversion.

**Revenue.** Filter-health surfaced → reorder tapped → *nothing*. `J-REORDER-03` does
not exist, so the funnel cannot be closed today.

**Sharing.** Invite sent → accepted → grant revoked → expiry lapsed.

---

## Constraints the taxonomy must respect

1. **On-device and DPDP.** The product claims data never leaves home. An analytics SDK
   is by definition exfiltration. Whether telemetry is exempt, consented separately, or
   aggregated on-device before sending is an **architecture decision that has to be made
   before the first event is named** — not after. See C-11.
2. **Face and identity data can never be an event property.** Not a name, not an
   embedding, not a "known/unknown" flag tied to an individual.
3. **Neighbourhood comparison** already has a privacy question open (C-10); do not
   instrument it until that resolves.
4. Every event must map to a `J-*` step (`.claude/rules/analytics.md` gate).

---

## Status

| | |
|---|---|
| Events defined | **0** |
| Events implied by strategy | ~20 |
| Blocking decision | C-11 — telemetry vs the on-device privacy claim |
| Next step | Rule C-11, then draft the schema against `J-*` IDs from `memory/product/journeys.md` |
