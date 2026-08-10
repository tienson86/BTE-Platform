# PILOT-1E-B Summary — Expert Agreement & Adjudication

**Purpose:** Record genuine Expert-B judgments for CAL-000001 and CAL-000006; compute agreement; adjudicate only if required.  
**Scope:** Calibration only. No Taxonomy v2 implementation. No production / Golden / AF-1 changes.

## Results

| Case | Expert-A | Expert-B | Distance | Agreement | Adjudication |
|---|---|---|---:|---|---|
| CAL-000001 | SLIGHTLY_WEAK / MEDIUM | SLIGHTLY_WEAK / MEDIUM | 0 | EXACT_MATCH | NOT_REQUIRED |
| CAL-000006 | SLIGHTLY_WEAK / MEDIUM | SLIGHTLY_WEAK / MEDIUM | 0 | EXACT_MATCH | NOT_REQUIRED |

Expert-B rationale: **not supplied** → stored as `null` (not invented).  
Expert-A records: **preserved unchanged**.

## Model disagreement (separate)

- CAL-000001: experts SLIGHTLY_WEAK vs runtime **strong** (0.87) → MODEL_DISAGREEMENT  
- CAL-000006: experts SLIGHTLY_WEAK vs runtime **balanced** (0.50) → MODEL_DISAGREEMENT (adjacent)

## Hypotheses (CAL-000001)

- Sitting Ngọ fire coverage: **PLAUSIBLE** (unchanged; Expert-B silent on hypothesis)  
- Officer deduplication: **SUPPORTED** as modeling hygiene (no production rule)

## Coverage impact

- TOTAL_DUAL_REVIEWED: **2**  
- Dual SLIGHTLY_WEAK: 2 (still short of ≥5)  
- Overall readiness remains **CALIBRATION_PARTIAL**  
- SCORE_ONLY = NOT_SUFFICIENT (unchanged)  
- T1–T6 not frozen  

## Validation / tests

Adjudication validator `ok: true`. Golden + strength tests expected pass (no production changes).

---

Status:
- CASE_000001_EXPERT_A_PRESERVED: YES
- CASE_000001_EXPERT_B_RECORDED: YES
- CASE_000001_AGREEMENT: EXACT_MATCH
- CASE_000001_ADJUDICATION: NOT_REQUIRED
- CASE_000006_EXPERT_A_PRESERVED: YES
- CASE_000006_EXPERT_B_RECORDED: YES
- CASE_000006_AGREEMENT: EXACT_MATCH
- CASE_000006_ADJUDICATION: NOT_REQUIRED
- TOTAL_DUAL_REVIEWED: 2
- TOTAL_ADJUDICATED: 0
- TAXONOMY_BOUNDARIES_FROZEN: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- AF1_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
CALIBRATION_PARTIAL

Recommendation:
- NEXT_ACTION: Continue acquiring real verified charts and obtain dual expert reviews, prioritizing VERY_WEAK, WEAK, and BALANCED coverage.
