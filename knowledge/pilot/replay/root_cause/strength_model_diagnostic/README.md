# Strength Model Diagnostic — PILOT-1H

**Mode:** DIAGNOSTIC DESIGN only. Production Strength behavior unchanged.

## Populations (strictly separate)

| Population | IDs | Role |
|---|---|---|
| REAL_CALIBRATION | CAL-000001, CAL-000006 (dual-reviewed); other CAL-* provisional only | Expert-backed |
| SYNTHETIC_STRESS | SYN-STR-000001..000021 | Diagnostic stress labels only |
| RUNTIME_REFERENCE | engine outputs on both | Observations, not truth |

Never merge into one calibration metric.

## Scope

Allowed: read-only analysis + reports under this folder.  
Forbidden: engine/rules/thresholds/Golden/Knowledge/AF-1/calibration label edits.

## Key read-only sources

- `../strength_calibration/`
- `../strength_taxonomy_v2/` (+ calibration, acquisition, expert_review, adjudication)
- `../../synthetic_strength/`
- `database/12_strength/` (read-only)
- `engines/strength_engine/` (read-only)
