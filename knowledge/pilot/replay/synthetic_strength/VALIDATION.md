# VALIDATION — PILOT-1G

## Dataset gates

| Check | Status |
|---|---|
| Exactly 21 cases | PASS |
| IDs unique | PASS |
| All IDs use SYN-STR prefix | PASS |
| No CAL-* identifiers created | PASS |
| Seven expected levels x3 | PASS |
| calibration_eligible=false for all | PASS |
| golden_eligible=false for all | PASS |
| No Han characters in fixtures | PASS |
| ASCII machine identifiers | PASS |

## Freeze / scope

| Constraint | Status |
|---|---|
| Production code unchanged | YES |
| Strength engine unchanged | YES |
| Knowledge packages unchanged | YES |
| Golden Expected unchanged | YES |
| AF-1 unchanged | YES |
| Taxonomy v2 not implemented | YES |
| T1-T6 not frozen | YES |

## Replay outcome

- Exact matches: 16
- Mismatches: 5
- Final decision: **SYNTHETIC_REPLAY_PARTIAL**

## Tests

```text
python -m pytest knowledge/pilot/replay/synthetic_strength/tests -q
→ 33 passed

python -m pytest tests/golden_dataset -q
→ 1 passed

python -m pytest tests/score/test_strength.py -q
→ 1 passed
```

TEST_REGRESSION: NO
