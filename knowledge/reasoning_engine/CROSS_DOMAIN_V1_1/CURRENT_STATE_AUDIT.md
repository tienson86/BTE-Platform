# CURRENT_STATE_AUDIT — Pre-CDR Cross-Domain Logic

Audit completed before CDR-001 implementation. No fixes in this document.

## Components audited

| Component | Path | Finding |
|-----------|------|---------|
| CrossDomainIntegrator | `interpretation/integrator.py` | Dedupes themes; does not scope-compare Strength vs Pattern |
| conflict_control | `interpretation/conflict_control.py` | Narrow pairs; misses balanced ↔ Tòng Nhi |
| theme_keys | `interpretation/theme_keys.py` | Generic vocabulary; reusable across charts |
| ExecutiveConsultingComposer | `interpretation/executive_composer.py` | `_insight` hard-preferred ENDURANCE+OUTPUT_RELEASE → CASE-0001 leakage |
| Identity / Career | product docs only | Not wired into production orchestrator |
| CASE-0001 | golden | Commercial reference OK; themes overfitted into generic stitch |
| CASE-0002 | validation | Strength↔Pattern tension with empty conflicts; executive “gánh thêm” insight |

## Failure modes identified

1. **Generic theme inheritance** — themes from claim theme_ids reused without chart-specific derivation.
2. **CASE-0001 domination** — endurance/output stitch applied when both theme keys present, including false positives.
3. **Conflicts detected but not resolved** — and often not detected across BODY_STRENGTH vs STRUCTURAL_PATTERN.
4. **Single-domain authority** — domain conclusion pasted as executive WHO/INSIGHT without relation classification.

## Design constraint for fix

Do not redesign platform. Do not author new BaZi doctrine. Do not modify calculation engines to make CASE-0002 look better.
