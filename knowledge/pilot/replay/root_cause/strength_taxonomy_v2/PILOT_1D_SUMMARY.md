# PILOT-1D Summary

**Sprint:** Expert Calibration & Golden Dataset Expansion  
**Predecessor:** PILOT-1C → CALIBRATION_READY  
**Outcome:** Calibration structure executed; coverage incomplete → **CALIBRATION_PARTIAL**

## What was done

1. Projected CASE-0001…0007 → `CAL-000001`…`CAL-000007` with explicit provenance `EXISTING_PILOT`.  
2. CASE-0006 uses corrected **Mậu Ngọ** projection; historical replay fixture untouched.  
3. Recorded single expert-reference reviews; left `expert_review_2` as PENDING (not fabricated).  
4. Built coverage, boundary, conflict, distribution, and validation artifacts.  
5. Created `CASE_ACQUISITION_QUEUE.md` for missing taxonomy levels / dual reviews.  
6. Focused CASE-0001 hypothesis review (`CASE_0001_EXPERT_CALIBRATION.md`).  
7. Recorded CASE-0006 corrected projection (`CASE_0006_CALIBRATION_RECORD.md`).  
8. Documented Golden vs Calibration separation and readiness gates.  
9. Ran `tests/golden_dataset` + `tests/score/test_strength.py` (pass).  

## What was not done (correctly refused)

- No fabricated birth charts or expert labels  
- No T1–T6 freeze  
- No production Strength / package / Expected / AF-1 changes  
- No Golden Dataset promotion  

## Coverage vs target (≥5 per level)

| Level | Achieved | Gap |
|---|---:|---:|
| VERY_WEAK | 0 | 5 |
| WEAK | 0 | 5 |
| SLIGHTLY_WEAK | 3 | 2 |
| BALANCED | 0 | 5 |
| SLIGHTLY_STRONG | 1 | 4 |
| STRONG | 2 | 3 |
| VERY_STRONG | 1 | 4 |

Total provisional verified: **7** (target 40–50).  
Dual-reviewed: **0**.

## Score-only sufficiency

**NO** — CAL-000003 and CAL-000005 share score **0.66** with different expert levels.

## Threshold freeze

**TAXONOMY_BOUNDARIES_FROZEN: NO** — all T1–T6 remain INSUFFICIENT_DATA / symbolic.

---

Status:  
EXISTING_CASES_REVIEWED: 7  
NEW_VERIFIED_CASES: 0  
TOTAL_VERIFIED_CASES: 7  
VERY_WEAK_COVERAGE: 0  
WEAK_COVERAGE: 0  
SLIGHTLY_WEAK_COVERAGE: 3  
BALANCED_COVERAGE: 0  
SLIGHTLY_STRONG_COVERAGE: 1  
STRONG_COVERAGE: 2  
VERY_STRONG_COVERAGE: 1  
BOUNDARY_CASES: 3  
CONFLICT_CASES: 3  
LOW_CONFIDENCE_CASES: 7  
EXPERT_DUAL_REVIEWED: 0  
TAXONOMY_BOUNDARIES_FROZEN: NO  
PRODUCTION_CODE_CHANGED: NO  
STRENGTH_ENGINE_CHANGED: NO  
KNOWLEDGE_PACKAGES_CHANGED: NO  
GOLDEN_EXPECTED_CHANGED: NO  
AF1_CHANGED: NO  
TEST_REGRESSION: NO  

Final Decision:  
CALIBRATION_PARTIAL  

Recommendation:  
NEXT_ACTION: Acquire real verified charts and dual expert reviews per CASE_ACQUISITION_QUEUE.md until each taxonomy level reaches ≥5 dual-reviewed cases; do not implement Taxonomy v2 until then.
