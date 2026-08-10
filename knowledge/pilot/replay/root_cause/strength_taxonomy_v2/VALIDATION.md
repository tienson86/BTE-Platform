# VALIDATION — PILOT-1D

## Freeze / scope

| Constraint | Status |
|---|---|
| Production code unchanged | YES |
| Strength engine unchanged | YES |
| Knowledge packages unchanged | YES |
| Golden Expected unchanged | YES |
| AF-1 unchanged | YES |
| API / UI / pipelines unchanged | YES |
| No fabricated charts | YES |
| No fabricated expert judgments | YES |
| No silent fixture mutation | YES |
| Calibration ≠ released Golden | YES |

## Tests

```text
python -m pytest tests/golden_dataset -q
→ 1 passed

python -m pytest tests/score/test_strength.py -q
→ 1 passed
```

## Calibration validation

See `calibration/validation/VALIDATION.json` → `PASS_WITH_GAPS`

| Check | Result |
|---|---|
| Unique CAL IDs | pass |
| Provenance valid | pass |
| No SYNTHETIC/UNKNOWN in pool | pass |
| Expert review 1 present | pass |
| Expert review 2 complete | **fail/gap** (pending) |
| Coverage ≥5/level | **fail/gap** |
| Production mutations | none |

## Final decision cross-check

`PILOT_1D_SUMMARY.md` → **CALIBRATION_PARTIAL**
