# Acquisition Status — PILOT-1E

**As of:** 2026-08-11  
**Decision:** `CALIBRATION_PARTIAL`  
**New real cases this sprint:** **0** (no authorized new birth charts supplied)

## Summary

| Metric | Value |
|---|---:|
| Existing provisional cases retained | 7 |
| New cases acquired | 0 |
| New verified cases | 0 |
| Dual-reviewed total | 0 |
| Adjudicated (formal dual disagreement) | 0 |
| Open acquisition targets | 16 |
| DATA_GAP targets | 16 |

## Taxonomy DATA_GAP ledger

| Level | Provisional (single-ref) | Dual-reviewed | Target dual | Gap | Gate |
|---|---:|---:|---:|---:|---|
| VERY_WEAK | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| WEAK | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| SLIGHTLY_WEAK | 3 | 0 | 5 | 5 | NOT_COVERED |
| BALANCED | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| SLIGHTLY_STRONG | 1 | 0 | 5 | 5 | NOT_COVERED |
| STRONG | 2 | 0 | 5 | 5 | NOT_COVERED |
| VERY_STRONG | 1 | 0 | 5 | 5 | NOT_COVERED |

## Boundary DATA_GAP ledger

| Boundary | Dual-reviewed | Target | Gap | Status |
|---|---:|---:|---:|---|
| VERY_WEAK / WEAK | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| WEAK / SLIGHTLY_WEAK | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| SLIGHTLY_WEAK / BALANCED | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| BALANCED / SLIGHTLY_STRONG | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| SLIGHTLY_STRONG / STRONG | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| STRONG / VERY_STRONG | 0 | 2 | 2 | BOUNDARY_DATA_GAP |

Note: CAL-000003/005/006 are provisional boundary-adjacent seeds only (not dual-reviewed).

## Dual-review backlog (EXISTING_PILOT)

| CAL ID | Chart | Expert 1 | Expert 2 | Status |
|---|---|---|---|---|
| CAL-000001 | VERIFIED | recorded (reference) | PENDING — packet READY | See `../expert_review/CASE_0001/` (PILOT-1E-A) |
| CAL-000002 | VERIFIED | recorded (reference) | PENDING | AQ-014 |
| CAL-000003 | VERIFIED | recorded (reference) | PENDING | AQ-014 |
| CAL-000004 | VERIFIED | recorded (reference) | PENDING | AQ-014 |
| CAL-000005 | VERIFIED | recorded (reference) | PENDING | AQ-014 |
| CAL-000006 | VERIFIED_CORRECTED | recorded (reference) | PENDING — packet READY | See `../expert_review/CASE_0006/` (PILOT-1E-A) |
| CAL-000007 | VERIFIED | recorded (reference) | PENDING | AQ-014 |

## Blockers

1. No new authorized real-world charts delivered this sprint.  
2. No second independent expert (EXPERT-B) available to complete dual reviews.  
3. Fabrication forbidden → gaps remain open.

## Next concrete action

Secure EXPERT-B dual reviews for CAL-000001 and CAL-000006 first (P0 conflict/boundary anchors), then acquire ≥5 real charts targeting VERY_WEAK, WEAK, and BALANCED.
