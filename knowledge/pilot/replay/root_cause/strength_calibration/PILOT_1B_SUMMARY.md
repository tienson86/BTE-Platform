# PILOT-1B Summary

**Sprint:** Strength Calibration & Taxonomy  
**Date:** 2026-08-11  
**Production code changed:** No  
**Knowledge packages / Golden Expected / AF-1 / API / UI / pipelines changed:** No  

## What was done

1. Re-ran `tests/golden_dataset` and `tests/score/test_strength` (both passed).  
2. Extracted full Strength evidence for CASE-0001…0007 via live engines.  
3. Applied PILOT-1A corrected chart for CASE-0006 (month **Mậu Ngọ**).  
4. Separated score correctness from taxonomy/label correctness.  
5. Built polarity ledger for CASE-0001 (highest priority).  
6. Audited confidence and proposed (not implemented) 7-level taxonomy.

## Score distribution (normalized)

| Case | Expert reference | Raw Σ | Norm | Band | Label | Conf |
|---|---|---:|---:|---|---|---:|
| 0001 | balanced / slightly weak | 37 | 0.87 | strong | Thân vượng | 1.0 |
| 0002 | very strong | 39 | 0.89 | strong | Thân vượng | 1.0 |
| 0003 | slightly weak (boundary) | 16 | 0.66 | strong | Thân vượng | 1.0 |
| 0004 | strong | 34 | 0.84 | strong | Thân vượng | 1.0 |
| 0005 | balanced / slightly strong | 16 | 0.66 | strong | Thân vượng | 1.0 |
| 0006 | balanced / slightly weak | 0 | 0.50 | balanced | Trung hòa | 1.0 |
| 0007 | strong | 26 | 0.76 | strong | Thân vượng | 1.0 |

Normalization: `(raw_total + 50) / 100` clamped to `[0,1]`.  
Bands: `strong ≥ 0.65`, `weak ≤ 0.35`, else `balanced`.

## Key conclusions

### Polarity (CASE-0001)

- **No inverted-sign implementation defect found.**  
- Season `Tướng` for Canh Kim in Sửu (Thổ sinh Kim) is classically consistent.  
- Rule signs match group intent (season+/root+/support+/control−/special+).  
- Expert “slightly weak” vs runtime `0.87 strong` is a **model plausibility / evidence-coverage / weighting** dispute, not a broken `+`/`−` operator.

### Score vs taxonomy

- Arithmetic and threshold application are internally consistent.  
- 3-band taxonomy **cannot** express: very strong, slightly weak, slightly strong, thiên nhược/vượng.  
- Cases 0002 / 0005 / 0006 (post-calendar) are primarily **taxonomy** issues.  
- Cases 0004 / 0007 agree with expert under the coarse band.

### CASE-0006

- Calendar issue closed (PILOT-1A).  
- Strength on corrected Ngọ chart: `balanced / 0.50` — coarse mid band; expert thiên nhược remains a taxonomy gap → **TAXONOMY_LIMITATION** (not Calendar).

### Confidence

- Always `1.0` for these cases (`min(1, n/5) + 0.2`).  
- Does not reflect threshold proximity (0003/0005 at 0.66) → confidence calibration needed (recommend only).

## Final Decision

**B. STRENGTH_TAXONOMY_LIMITATION_CONFIRMED**

Score math is broadly algorithmically valid; current taxonomy cannot represent expert granularity.  
CASE-0001 remains a **modeling research** item (weights / sitting-branch evidence), **not** a proven P0 calculation bug.

---

Status:  
CASES_ANALYZED: 7  
POLARITY_ISSUE: NO  
SCORE_ISSUE: UNRESOLVED  
TAXONOMY_LIMITATION: YES  
CONFIDENCE_ISSUE: YES  
CASE_0006_CALENDAR_ISSUE: NO  
PRODUCTION_CODE_CHANGED: NO  
KNOWLEDGE_PACKAGES_CHANGED: NO  
GOLDEN_EXPECTED_CHANGED: NO  
AF1_CHANGED: NO  
TEST_REGRESSION: NO  

Final Decision:  
STRENGTH_TAXONOMY_LIMITATION_CONFIRMED  

Recommendation:  
NEXT_ACTION: Freeze a versioned Strength taxonomy proposal (7-level or tilt-extended 3-band) for a future contract sprint; schedule CASE-0001 expert weight/evidence-coverage review before any Strength rule CSV or scorer change.
