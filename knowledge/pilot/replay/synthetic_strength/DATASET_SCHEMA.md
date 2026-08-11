# DATASET_SCHEMA — Synthetic Strength Stress

## Case object (minimum)

```json
{
  "case_id": "SYN-STR-000001",
  "dataset_type": "SYNTHETIC_STRENGTH_STRESS",
  "calibration_eligible": false,
  "golden_eligible": false,
  "expert_calibration_eligible": false,
  "production_expected": false,
  "synthetic_pillars": true,
  "calendar_verified": false,
  "birth_datetime": null,
  "birth_location": null,
  "timezone": null,
  "day_master": "quy",
  "pillars": {
    "year": "binh_ngo",
    "month": "giap_ngo",
    "day": "quy_ti",
    "hour": "mau_ngo"
  },
  "synthetic_expected_taxonomy": "very_weak",
  "evidence_profile": "extreme hoa dominance against thuy",
  "stress_purpose": "VERY_WEAK extreme: ..."
}
```

## Field rules

| Field | Rule |
|---|---|
| case_id | `SYN-STR-` + 6 digits; unique |
| dataset_type | always `SYNTHETIC_STRENGTH_STRESS` |
| pillars.* | ASCII `stem_branch` using BTE stem/branch tokens |
| day_master | ASCII stem token; must equal day pillar stem |
| synthetic_expected_taxonomy | one of seven candidate levels (stress label only) |
| birth_* / timezone | always null / unverified |
| *\_eligible / production_expected | always false |

## Canonical ASCII tokens

Stems: `canh tan nham quy giap at binh dinh mau ky`  
Branches: `ty suu dan mao thin ti ngo mui than dau tuat hoi`

## Result object (replay)

Stored under `results/SYN-STR-*.json` with:

- runtime score / profile / v1 band / diagnostics
- comparison.match / mismatch_category
- explicit notes that mismatches are diagnostic only

## Forbidden destinations

Do not copy `synthetic_expected_taxonomy` into:

- `tests/golden_dataset`
- released Golden Dataset
- production Expected
- Knowledge Packages
