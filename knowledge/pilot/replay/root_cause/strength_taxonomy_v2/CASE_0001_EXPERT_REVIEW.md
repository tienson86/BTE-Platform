# CASE-0001 Expert Weight Review (Calibration Only)

**Case:** Nguyễn Tiến Sơn — 1987-01-21 04:30 — Canh Ngọ  
**Pillars:** Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần  
**Expert reference:** balanced / slightly weak  
**Runtime:** score 0.87 → strong / Thân vượng  
**No weights changed in production.**

## Context

PILOT-1B: polarity signs consistent; arithmetic OK; day-branch Ngọ fire under-represented as weakener; expert disagrees with strong label.

## Evidence weight table

| Evidence | Runtime Direction | Expert Direction (ref) | Runtime Weight | Proposed Weight | Confidence | Rationale | Status |
|---|---|---|---:|---|---|---|---|
| Season Tướng (Thổ→Kim via Sửu) | strengthen | strengthen (mild) | +25 | +15 to +20 | medium | Classical 相 OK; magnitude may overpower mid charts | **PLAUSIBLE** |
| Month branch Sửu / Chính Ấn main qi | strengthen | strengthen | via season + spc | keep separate seal term | medium | Seal support real | **SUPPORTED** |
| Month hidden stems (Kỷ/Quý/Tân) | mixed | mixed | in root/support | explicit ledger | medium | Xin companion in branch | **PLAUSIBLE** |
| Day branch Ngọ (Hỏa sitting) | **under-weighted / missing as control** | weaken | ~0 explicit | add sitting-branch weaken (−8 to −15 candidate) | medium | Day sits fire vs Kim — major classical weaken | **SUPPORTED** (coverage gap) |
| Hour branch Dần | mixed | mixed | partial via stems | keep | low | Wood/fire hidden | **UNCERTAIN** |
| Year branch Dần + stem Bính Thất Sát | weaken | weaken | −10 + −8 | collapse double-count to single officer event (−10 to −12) | high | Same officer family twice | **SUPPORTED** |
| Visible Tân Kiếp Tài | strengthen | mild strengthen | +8 | +5 to +8 | medium | Peer support OK | **PLAUSIBLE** |
| Visible Mậu Thiên Ấn | strengthen | strengthen | via resource list / spc | avoid stack with season | medium | Seal stacking with Tướng | **PLAUSIBLE** |
| Root 1 chi | strengthen | mild | +12 | +8 to +12 | medium | Real but limited | **PLAUSIBLE** |
| Temperature (context cold vs engine hot) | conflicting | needs climate net | not in score | unify source before weight | low | Do not weight until SSOT | **REJECTED** (as scorer input now) |
| Combinations / clashes | none exposed | possible | 0 | 0 until producer | high | No fake interactions | **SUPPORTED** (leave 0) |
| spc_004 Ấn mùa lạnh | strengthen | mild | +10 | +0 to +5 if season already Tướng | medium | Double-counts seal/season theme | **PLAUSIBLE** |

## Proposed weight adjustments — summary

| Adjustment | Class |
|---|---|
| Add day-branch sitting weaken evidence | **SUPPORTED** |
| Deduplicate officer ctl_001+ctl_006 | **SUPPORTED** |
| Reduce sea_002 magnitude | **PLAUSIBLE** |
| Reduce spc_004 when season already seal-aligned | **PLAUSIBLE** |
| Use TemperatureEngine in Strength score immediately | **REJECTED** (until source policy) |
| Case-specific CASE-0001 multiplier | **REJECTED** |

## Outcome

- Does **not** prove production bug requiring immediate patch.  
- Establishes calibration hypotheses for a future evidence-policy sprint.  
- Even after coverage fixes, taxonomy v2 still needed for expert lexicon.
