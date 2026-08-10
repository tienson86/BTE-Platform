# VALIDATION — PILOT-1E-B

## Freeze / scope

| Constraint | Status |
|---|---|
| Production code unchanged | YES |
| Strength engine unchanged | YES |
| Knowledge packages unchanged | YES |
| Golden Expected unchanged | YES |
| AF-1 unchanged | YES |
| T1–T6 not frozen | YES |
| Expert-A preserved | YES |
| Expert-B recorded exactly (level+confidence) | YES |
| Rationale not invented | YES |
| Adjudication does not overwrite reviews | YES |
| CAL-000006 month = Mậu Ngọ | YES |

## Tests

```text
python -m pytest tests/golden_dataset -q
→ 1 passed

python -m pytest tests/score/test_strength.py -q
→ 1 passed

python .../adjudication/validation/validate_adjudication.py
→ ok: true
```

## Final decision

**CALIBRATION_PARTIAL**
