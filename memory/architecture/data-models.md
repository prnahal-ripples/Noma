# Data Models

> Entities inferred from the PM prototype set, 2026-08-04. Field names are the
> prototypes' own where they exist. Canonical hardware: `src/hardware/devices.json`.
> **Inferred, not ratified** — no schema, migration, or validation exists.

---

## Home
```
Home
  id, name
  rooms[]        → Room
  members[]      → Member
  devices[]      → Device
  score          → Score        (see C-5 — definition unsettled)
  scene          'home' | 'away' | 'night'
```
Multi-home is implied by `S2_HOMES` but has no flow. Whether members, rules and
autonomy grants are per-home or per-account is **undefined** — and it matters, because
persona P1 explicitly manages a second household remotely.

## Room
```
Room
  id, name, icon
  devices[]      → Device
  aqi                        ← may exist with NO sensor present (C-9)
```
Two different preset lists appear (**C-12**):

| Source | Presets |
|---|---|
| Launch app (8) | Living Room, Bedroom, Hallway, Kitchen, Office, Study, Balcony, Kids Room |
| Templates (11) | + Bathroom, **Pooja Room**, Front Door, Garage |

The 11-item list includes Pooja Room and is the India-appropriate one. `MAX_ROOMS` is
enforced but its value is not stated as a product rule.

## Device
```Device
  id, model, type            'purifier'|'camera'|'lock'|'vacuum'|'doorbell'
  room                       → Room
  name                       user-editable, INDEPENDENT of room
  online, firmware
  ── purifier ──
  mode                       (C-4 — three vocabularies)
  fanSpeed, pm25, voc, humidity, temp
  filterPercentUsed, filterDaysRemaining
  ── vacuum ──
  cleanMode, suction, consumables[]
```
**Device name and room are independent fields.** The prototype contains a device named
"Living Room Purifier" assigned to room "Bedroom" — probably a mock artifact, but it
proves the fields are decoupled, and any UI showing one while implying the other will
mislead.

## Member and access — the most developed model
```
Member
  id, name, contact
  role                       (C-3 — three models)
  grants[]      → { deviceId, featureIds[] }
  schedule?                  weekly window, e.g. 09:00–10:00 daily
  expiresAt?                 default 24h for guests
```
Grants are **per device type**, and the granularity is real:

| Type | Grants |
|---|---|
| Camera (7) | Live view · Basic functions (PTZ, two-way audio, privacy mode) · Events · Cloud recordings view · Cloud management (delete) · Local (SD) recordings · Device management |
| Lock (2) | Unlock · View access log |
| Purifier (2) | Control (power, fan, modes) · Schedules |
| Vacuum (2) | Control (start, dock, spot) · Schedules |

Note that **camera splits *viewing* cloud clips from *deleting* them**, and lock splits
*unlocking* from *seeing who unlocked*. That asymmetry is correct and deliberate — a
guest may need entry without seeing the household's movements.

⚠ **C-3 — three role models coexist:**

| Source | Roles |
|---|---|
| `ROLES` | family · staff (time-window) · guest (date-range) |
| `ROLES3` | family · guest (staff folded in) |
| `SHARE_ROLE_BADGE` | owner · family · guest |

`ROLES3` looks newest (2-role, simplified) but `ROLES` is the only one with an explicit
**staff** role — which is persona P3, the household help. Collapsing staff into guest
loses the recurring-weekly-window case that P3 is defined by. **Do not resolve by
picking the newest file.**

## Automation
```
Automation
  id, name
  origin        'agent' | 'user'          ← surfaced in the UI, so it is a real field
  trigger       schedule | aqi-threshold | geofence | wearable-signal | forecast | device-event
  actions[]
  enabled
```

## Proposal — the agent's unit of work
```
Proposal
  id, capability
  sensed, decided, insteadOf, obeysRule    ← all four required (see ai-integration.md §4)
  plan[]        → { time, label, detail, locked }
  state         proposed | rehearsing | scheduled | done | deferred | declined
  undoable
```
`locked` on a plan step marks it as rule-derived and therefore not editable inline.

## StandingRule
```
StandingRule
  id, label, value, unit
  tradeoffNote                ← copy is part of the model: "quieter but cleans slower"
```

## AutonomyGrant
```
AutonomyGrant
  capability                  'fan-speed' | 'pre-clean' | 'reorder-filters'
  level                       'ask' | 'act-and-tell' | 'act-silently'
  consecutiveAccepts          ← drives the promotion prompt
```
No `safetyClass` field exists, which is exactly the gap in C-8.

## Event (camera / security)
```
Event
  id, type       motion | person | doorbell | system
  time, location
  identity?      → Face
  badge          'Known' | 'Verified' | 'Review'
  clipAvailable
  unread
```

## Face
```
Face
  id, label
  embedding      ON-DEVICE ONLY — never uploaded (DPDP Act 2023)
  consentGranted ← explicit, per-feature, revocable
```

## Retention tiers
Event history is a **paid axis**: 30 days on the mid tier, 365 days on the top tier.
So retention is a billing entitlement, not a storage default — see
`memory/analytics/monetization-map.md`.
