# Calibration Coverage Matrix (PILOT-1E-B)

**Coverage rule:** A level is covered only with ≥5 verified **and** ≥5 dual-reviewed cases.

## Taxonomy levels

| Level | Verified (provisional) | Dual Reviewed | Adjudicated | Target | Gap | Gate |
|---|---:|---:|---:|---:|---:|---|
| VERY_WEAK | 0 | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| WEAK | 0 | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| SLIGHTLY_WEAK | 3 | 2 | 0 | 5 | 3 dual | NOT_COVERED |
| BALANCED | 0 | 0 | 0 | 5 | 5 | NOT_COVERED / DATA_GAP |
| SLIGHTLY_STRONG | 1 | 0 | 0 | 5 | 5 | NOT_COVERED |
| STRONG | 2 | 0 | 0 | 5 | 5 | NOT_COVERED |
| VERY_STRONG | 1 | 0 | 0 | 5 | 5 | NOT_COVERED |

Dual-reviewed IDs: CAL-000001, CAL-000006 (both SLIGHTLY_WEAK, EXACT_MATCH, adjudication NOT_REQUIRED).

## Boundaries

| Boundary | Dual Reviewed | Target | Gap | Status |
|---|---:|---:|---:|---|
| VERY_WEAK / WEAK | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| WEAK / SLIGHTLY_WEAK | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| SLIGHTLY_WEAK / BALANCED | 1 candidate (CAL-000006) | 2 | ≥1 | BOUNDARY_DATA_GAP |
| BALANCED / SLIGHTLY_STRONG | 0 | 2 | 2 | BOUNDARY_DATA_GAP |
| SLIGHTLY_STRONG / STRONG | 0 dual | 2 | 2 | BOUNDARY_DATA_GAP |
| STRONG / VERY_STRONG | 0 | 2 | 2 | BOUNDARY_DATA_GAP |

## Special cohorts

| Special Cohort | Dual Reviewed | Target | Gap |
|---|---:|---:|---:|
| Conflicting-evidence | 1 (CAL-000001) | 5 | 4 |
| Low-confidence (expert LOW) | 0 | 5 | 5 |
| Expert-disagreement (dual) | 0 | — | — |
