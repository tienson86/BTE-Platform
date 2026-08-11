# VALIDATION — PILOT-1F

## Freeze / scope

| Constraint | Status |
|---|---|
| Production code unchanged | YES |
| Strength engine unchanged | YES |
| Knowledge packages unchanged | YES |
| Golden Expected unchanged | YES |
| AF-1 unchanged | YES |
| No fabricated charts | YES |
| No fabricated expert judgments | YES |
| CAL-000001…007 identities preserved | YES |
| No new CAL IDs assigned (none acquired) | YES |
| T1–T6 not frozen | YES |

## Tests

```text
python -m pytest tests/golden_dataset -q
→ 1 passed

python -m pytest tests/score/test_strength.py -q
→ 1 passed
```

## Final decision

**CALIBRATION_PARTIAL** (Round-2 DATA_GAP; dual-reviewed = 2)
