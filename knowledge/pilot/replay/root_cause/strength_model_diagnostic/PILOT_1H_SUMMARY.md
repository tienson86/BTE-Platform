# PILOT_1H_SUMMARY — Strength Model Diagnostic & Taxonomy Boundary Analysis

**Purpose:** Diagnose what the current Strength score measures, where information is lost, and what is required before Taxonomy v2 — without changing production behavior.

## Populations analyzed

- REAL_CALIBRATION dual-reviewed: CAL-000001, CAL-000006 (n=2)
- SYNTHETIC_STRESS: SYN-STR-000001..000021 (n=21)
- RUNTIME_REFERENCE: existing engine outputs (observation only)

## Headline conclusions

- Score is a useful net index of season/root/support/drain/control/special rules.
- Score is **not** sufficient for seven-level taxonomy.
- Published score **saturates** at 1.000 for raw>=50 (STRONG vs VERY_STRONG lost).
- Taxonomy projection collapse is a **separate** problem from score clamp.
- Profile layer is **required** before implementation.
- Real dual-reviewed coverage remains a **DATA_GAP** outside SLIGHTLY_WEAK.

## No-patch gate

Only paths under `knowledge/pilot/replay/root_cause/strength_model_diagnostic/` are in scope for this sprint.

---

Status:
- REAL_DUAL_REVIEWED_CASES: 2
- SYNTHETIC_CASES_ANALYZED: 21
- SCORE_TRACE_COMPLETED: YES
- SCORE_SATURATION_ANALYZED: YES
- VERY_WEAK_BOUNDARY_ANALYZED: YES
- BALANCED_PROFILE_ANALYZED: YES
- SCORE_COLLISION_ANALYZED: YES
- SUPPORT_PRESSURE_ANALYZED: YES
- SEASONAL_WEIGHTING_ANALYZED: YES
- ROOTING_ANALYZED: YES
- PROFILE_REQUIREMENTS_DEFINED: YES
- TAXONOMY_BOUNDARIES_FROZEN: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- AF1_CHANGED: NO
- CALIBRATION_DATA_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
DIAGNOSTIC_COMPLETE

Recommendation:
- NEXT_ACTION: Continue real expert case acquisition while preserving the current Strength Engine and keeping Taxonomy v2 unimplemented.
