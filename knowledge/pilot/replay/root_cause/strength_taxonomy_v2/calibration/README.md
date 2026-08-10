# Calibration Dataset (PILOT-1D)

**Dataset type:** `CALIBRATION_DATASET` (separate from released Golden Dataset)  
**Production / Golden Expected:** unchanged  
**Sprint:** PILOT-1E

## Principle

A smaller verified set beats fabricated balance. Dual expert reviews were **not invented**.

## Contents

| Path | Content |
|---|---|
| `dataset_index.json` | Index + coverage |
| `cases/CAL-*.json` | Case records |
| `evidence/` | Evidence snapshots |
| `reviews/` | Expert review 1 + pending review 2 stubs |
| `adjudications/` | Provisional single-reference |
| `distributions/` | Score distribution / coverage matrix |
| `boundaries/` | Boundary cohort |
| `conflicts/` | Conflict cohort |
| `provenance/` | Provenance cards |
| `acquisition/` | Pointer to operational `../acquisition/` |
| `validation/VALIDATION.json` | Quality gates |

## Current population

- **7** provisional verified projections (`CAL-000001`…`CAL-000007`) from `EXISTING_PILOT`
- **0** new real-world acquisitions (PILOT-1E)
- **0** dual-reviewed cases (EXPERT-B PENDING)
- Operational queue: `../acquisition/ACQUISITION_QUEUE.md`

## Parent reports

- `../PILOT_1E_SUMMARY.md`
- `../CALIBRATION_READINESS.md`
- `../CALIBRATION_COVERAGE_MATRIX.md`
- `../CASE_0001_DUAL_REVIEW.md`
- `../CASE_0006_DUAL_REVIEW.md`
- `../GOLDEN_DATASET_SEPARATION.md`
- `../VALIDATION.md`
