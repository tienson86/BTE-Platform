# PILOT-1C Summary

**Sprint:** Strength Taxonomy v2 Design & Expert Calibration  
**Date:** 2026-08-11  
**Production code / Strength engine / packages / Expected / AF-1:** unchanged  

## Why this sprint

PILOT-1B confirmed taxonomy limitation without proving polarity/arithmetic bugs.  
Score-only classification fails for expert granularity — especially CASE-0003 and CASE-0005 both at **0.66** with different expert labels.

## Delivered design

1. Canonical Strength Evidence Model (direct / derived / contextual / interaction)  
2. Strength Profile independent of final label  
3. Taxonomy v2 candidate (7 levels) with **symbolic thresholds T1–T6** (numeric edges provisional)  
4. Boundary model (no hard-threshold-only classification)  
5. Confidence model (HIGH/MEDIUM/LOW/VERY_LOW/UNRESOLVED)  
6. Expert calibration protocol (multi-expert, adjudication)  
7. Golden Dataset expansion plan  
8. Backward compatibility v1↔v2 mapping (conceptual)  
9. CASE-0001 structured weight review (calibration only)  
10. Per-case calibration notes CASE-0002…0007  

## Score distribution reminder (do not freeze thresholds)

```text
0006: 0.50
0003: 0.66  ─┐ identical score
0005: 0.66  ─┘ different expert labels → score-only taxonomy impossible
0007: 0.76
0004: 0.84
0001: 0.87  (expert: slightly weak — model/expert dispute)
0002: 0.89
```

## Readiness

| Gate | Status |
|---|---|
| Taxonomy semantics | Designed (candidate) |
| Evidence / Profile / Boundary / Confidence | Designed |
| Expert protocol | Designed |
| Case count for implementation | **Insufficient (n=7)** |
| Implementation | **Not ready** |

---

Status:  
TAXONOMY_V2_DESIGNED: YES  
EVIDENCE_MODEL_DESIGNED: YES  
PROFILE_MODEL_DESIGNED: YES  
BOUNDARY_MODEL_DESIGNED: YES  
CONFIDENCE_MODEL_DESIGNED: YES  
EXPERT_PROTOCOL_DESIGNED: YES  
GOLDEN_EXPANSION_DEFINED: YES  
BACKWARD_COMPATIBILITY_DEFINED: YES  
PRODUCTION_CODE_CHANGED: NO  
STRENGTH_ENGINE_CHANGED: NO  
KNOWLEDGE_PACKAGES_CHANGED: NO  
GOLDEN_EXPECTED_CHANGED: NO  
AF1_CHANGED: NO  
TEST_REGRESSION: NO  

Final Decision:  
CALIBRATION_READY  

Recommendation:  
NEXT_ACTION: Execute EXPERT_CALIBRATION_PROTOCOL on an expanded Golden set (≥5 charts per taxonomy level + boundary/low-confidence cohorts) before any Strength Taxonomy v2 implementation.
