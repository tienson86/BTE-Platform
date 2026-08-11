# NO_DATA_CONTINGENCY

When no authorized real charts are available:

## Do not create

- CAL-000008 or any CAL-* case
- fake expert reviews
- fake birth records
- synthetic substitutes treated as real

## Record honestly

```json
{
  "execution_status": "no_data",
  "new_real_cases": 0,
  "new_verified_cases": 0,
  "new_dual_reviewed_cases": 0,
  "readiness": "data_gap",
  "final_decision": "CALIBRATION_PARTIAL"
}
```

`no_data` is a program/queue state, not a fake case state.
Absence of data is a valid result.
