# ROUND_3_QUEUE

**Sprint:** PILOT-1L  
**As of:** 2026-08-11  
**New charts received:** 0  
**Next free CAL ID:** `CAL-000008` (create only after authorized intake + calendar verification; do not reserve empty CAL records)

## Priority acquisition slots (ACQ IDs — not CAL IDs)

| acq_id | candidate_target | priority | status | remaining_needed | notes |
|---|---|---|---|---:|---|
| ACQ-R3-001 | very_weak | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-002 | weak | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-003 | balanced | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-004 | slightly_strong | P1 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-005 | strong | P1 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-006 | very_strong | P2 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-007 | slightly_weak | P1 | source_pending | 3 | fill to gate=5; existing dual=2 |

candidate_target is **ACQUISITION_TARGET_ONLY**. It is not an expert label.

## Immediate ask

Deliver ≥3 authorized real charts for P0 targets (VERY_WEAK, WEAK, BALANCED) with consent, then calendar-verify and run Expert-A / blinded Expert-B.

## Coverage matrix

| level | dual_reviewed_count | expert_a_count | expert_b_count | verified_real_count | data_gap | priority | minimum_target | remaining_needed | status |
|---|---:|---:|---:|---:|---|---|---:|---:|---|
| very_weak | 0 | 0 | 0 | 0 | YES | P0 | 5 | 5 | data_gap |
| weak | 0 | 0 | 0 | 0 | YES | P0 | 5 | 5 | data_gap |
| slightly_weak | 2 | 2 | 2 | 2 | YES | P1 | 5 | 3 | partial_not_covered |
| balanced | 0 | 0 | 0 | 0 | YES | P0 | 5 | 5 | data_gap |
| slightly_strong | 0 | 0 | 0 | 0 | YES | P1 | 5 | 5 | data_gap |
| strong | 0 | 0 | 0 | 0 | YES | P1 | 5 | 5 | data_gap |
| very_strong | 0 | 0 | 0 | 0 | YES | P2 | 5 | 5 | data_gap |
