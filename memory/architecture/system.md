# System Architecture

> Reconstructed from the PM prototype set on 2026-08-04. **These are design prototypes,
> not an engineering design** — everything here is the shape the product implies, not a
> ratified architecture. Nothing has been reviewed by an engineer.
> Canonical hardware facts: `src/hardware/devices.json`.

---

## The shape the product implies

```
                    ┌─────────────────────────────┐
   CPCB nearest ───▶│  outdoor AQI + forecast     │──┐   (network — see §4)
   station          └─────────────────────────────┘  │
                                                     ▼
   QSensAI      ┌──────────────┐            ┌──────────────────┐
   laser    ───▶│  device      │───telemetry▶│   agent          │
   sensor       │  (purifier)  │◀──commands──│   - rules engine │
                └──────────────┘            │   - autonomy tiers│
                                            │   - audit log     │
   camera ─────▶ on-device face model ─┐    └──────────────────┘
                 (never uploaded)      │              │
                                       ▼              ▼
                              ┌────────────────────────────┐
                              │  app  (three home zones)   │
                              └────────────────────────────┘
```

## 1. Client

Static React, no build step in the prototypes (in-browser JSX). Tab structure:

- **My home** — the three agent zones (Settled / Needs your call / Done today)
- **Device** — device-first control and settings
- **Automation** — split `Created by your agent` vs `Created by you`
- **Shop** — catalogue and reorder
- **Me** — account, members, homes
- Floating bubble → **agent chat**, a deliberately separate session

Two later prototypes add `MultiViewTab` and `SpatialHomeTab` (a room-scene view). Both
are exploratory; neither is referenced by the others.

## 2. Device layer

| Concern | Detail |
|---|---|
| Pairing | Bluetooth LE, phone held close to a powered device |
| Network | Wi-Fi **2.4 GHz only**; setup hides 5 GHz SSIDs it cannot join |
| Firmware | OTA, version surfaced in device settings |
| Local controls | LED brightness, child lock — must work independent of cloud |

## 3. The agent

The spine. Full detail in `memory/architecture/ai-integration.md`. Architecturally it
needs four things the prototypes assume but never specify:

1. **A rules engine** that can prove which standing rule a plan obeyed (the "Obeys rule"
   slot is a promise the system has to keep)
2. **A per-capability autonomy store** with an accept/reject tally driving promotion
3. **An audit log** — every completed action stays undoable, including autonomous ones
4. **A planner** that emits an *editable, inert* step list before execution

## 4. Data sources and the privacy tension

| Data | Source | Locality |
|---|---|---|
| Indoor particulates | QSensAI on-device laser sensor | local |
| Outdoor AQI | nearest CPCB station, blended with local reading | **network** |
| Forecast | unstated provider | **network** |
| Faces | on-device model | local, never uploaded |
| Wearable signals | companion ring / watch | phone-mediated |
| Neighbourhood comparison | aggregated peer devices | **server-side by definition** |

⚠ **The unresolved core tension.** The product claims "on-device AI, your data never
leaves home" while shipping three features that cannot work without a server: outdoor
AQI blending, forecast-driven pre-clean, and neighbourhood comparison. Both statements
are in the same prototype.

The claim probably *means* "personal and biometric data stays local; ambient public data
is fetched" — which is defensible and still a strong position. But it has to be narrowed
before it appears in store copy or a privacy policy. As written it is a compliance
exposure under DPDP. Tracked as **C-11**.

## 5. What has no architecture at all

- **Payments** — no gateway, no order state machine, no refunds. `F-SHOP` is the revenue path.
- **Identity** — phone + OTP shown; no session model, no multi-device login, no account recovery
- **Multi-home** — `S2_HOMES` exists in the data with no flow
- **Offline** — no degraded mode, despite an "went offline briefly" notification
- **Per-room AQI without a per-room sensor** — the air map shows numbers for rooms with no device (see C-9)
- **Analytics** — nothing. See `memory/analytics/event-taxonomy.md`.
- **Data export / deletion** — a DPDP obligation with no surface
