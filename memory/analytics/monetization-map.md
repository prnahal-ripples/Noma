# Monetization Map

> Extracted from the PM prototype set, 2026-08-04. **Two revenue models appear across
> the docs and they are not reconciled** — see C-6 and C-13.

---

## Three revenue lines

### 1. Hardware
| SKU | Price seen | Where |
|---|---|---|
| Cam 360 2K | ₹2,999 | launch app shop |
| Bell Pro | ₹3,499 | launch app shop |
| Air Pro | **₹4,999** | launch app shop |
| Smart Lock X1 | ₹5,499 | launch app shop |
| Clean Bot R1 | ₹8,999 | launch app shop |
| "NS Air S1" purifier | **₹8,999** | strategy deck |

⚠ **C-6 — the anchor product has two prices**: ₹4,999 in the app, ₹8,999 in the deck
(where it is also positioned as matching Xiaomi's entry price). Nearly 2×. The deck's
entire competitive argument rests on price parity with Xiaomi at ₹8,999, so this is not
a typo to smooth over — one of the two documents is describing a different product.

### 2. Consumables — the recurring line
| Item | Price seen |
|---|---|
| HEPA H13 filter | **₹1,299** *(Week One)* / **₹1,499** *(launch app)* |
| Mop pads ×4 | ₹499 |
| Cam wall mount | ₹299 |

⚠ Filter price also conflicts. This is the highest-frequency purchase in the product.

**Why filter health is the strategic centre.** It is simultaneously the retention
signal, the differentiator, and the consumable trigger. The docs are sharp on the
timing: surfaced too late it becomes *"a 1-star 'it stopped working' review"*; surfaced
predictively it becomes a reorder that *"arrives before it runs out."* Same data, opposite
outcomes, decided by when it is shown.

### 3. Subscription
Only in the strategy deck. **Absent from every app prototype** — no paywall, no upgrade
prompt, no gated feature.

| Tier | Price | Includes |
|---|---|---|
| Free | ₹0 | Live control & room views · real-time AQI · **real filter health score** · current Score · basic automations |
| Plus | ₹699/mo · ₹6,999/yr | AQI-weighted filter tracking · predictive replacement · doorstep filter cleaning (3+ purifiers) · **30-day** event history · pet detection · family awareness |
| Family | ₹1,199/mo · ₹11,999/yr | All Plus · elder monitoring & check-ins · routine intelligence · **365-day** home memory · annual home health report |

⚠ **C-13 — the free/paid line contradicts the product's own positioning.** Free gets
"real filter health score"; Plus gets "AQI-weighted filter tracking". But AQI-weighting
*is* what makes the score real — it is the entire differentiator versus the competitors
the deck names. Selling it as an upsell undercuts the headline claim, and the two tier
descriptions cannot both be honest.

Also unresolved: the annual prices imply "save 2 months" on Plus (₹6,999 vs ₹8,388) but
only ~1.6 months on Family (₹11,999 vs ₹14,388), which is stated as if identical.

---

## Contextual upsell — the designed surfaces

Monetisation is **data-triggered**, never a standalone pop-up. This is the one thing all
docs agree on, and it maps directly to persona **P4 (Priya, the prospective owner)**.

| Surface | Trigger | Ask |
|---|---|---|
| Home air map | Rooms without a purifier show what they still breathe ("Living Rm 94, Kitchen 112") | A second device — *"A Living Room unit would cut it to ~24"* |
| Filter card | Predicted exhaustion (~22 days) | Reorder |
| Shop reorder rail | Device already owned | Matched consumable |
| Week recap | Day 7 | Retention, then Week-2 hook |

**The stated rule:** *"The first upsell has to feel like help, not a pop-up."*

**Design constraint that follows.** Every one of those surfaces wants an accent-coloured
CTA — and the accent budget is 10% of a screen with **one** primary action (ADR-003).
Upsell and primary action are therefore in direct competition for the same budget. On
the air map, the upsell IS the primary action; on the filter card it is not. Not resolved
anywhere; flagged here because it is a token-level consequence of a business decision.

---

## Acquisition, treated as a revenue line

The docs treat sharing as an acquisition channel with real intent:

- *"Every share is a Noise Home billboard on a friend's phone."*
- *"The weekly recap is the cheapest acquisition channel a product ever gets."*
- **Content rule, learned the hard way:** *"Pre-filled brandy captions kill shares;
  emoji + the number travel."* The caption must read as the user's, not the company's.

⚠ Shareable cards depend on neighbourhood comparison, which has an open privacy question
(C-10). The acquisition engine is gated on a compliance answer.

---

## What does not exist

No payment gateway, address book, tax handling, invoice, refund, subscription
management, or order tracking appears in any prototype. **Every number on this page is a
price tag with nothing behind it.**
