# Calibration Dataset (PILOT-1D)

**Dataset type:** `CALIBRATION_DATASET` (separate from released Golden Dataset)  
**Production / Golden Expected:** unchanged  

## Principle

A smaller verified set beats fabricated balance. Dual expert reviews were **not invented**.

## Contents

| Path | Content |
|---|---|
| `dataset_index.json` | Index + coverage |
| `cases/CAL-*.json` | Case records |
| `evidence/` | Evidence snapshots |
| `reviews/` | Expert review 1 (existing reference) |
| `adjudications/` | Provisional single-reference |
| `distributions/` | Score distribution |
| `boundaries/` | Boundary cohort |
| `conflicts/` | Conflict cohort |
| `provenance/` | Provenance cards |
| `validation/VALIDATION.json` | Quality gates |

## Current population

- **7** provisional verified projections (`CAL-000001`…`CAL-000007`) from `EXISTING_PILOT`
- **0** new real-world acquisitions this sprint
- **0** dual-reviewed cases (second expert PENDING)
- Acquisition gaps: see `../CASE_ACQUISITION_QUEUE.md`

## Parent reports

- `../PILOT_1D_SUMMARY.md`
- `../CALIBRATION_READINESS.md`
- `../CASE_0001_EXPERT_CALIBRATION.md`
- `../CASE_0006_CALIBRATION_RECORD.md`
- `../GOLDEN_DATASET_SEPARATION.md`
- `../VALIDATION.md`
