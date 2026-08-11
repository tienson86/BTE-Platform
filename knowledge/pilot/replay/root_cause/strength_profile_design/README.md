# Strength Profile Design — PILOT-1I

**Mode:** DESIGN ONLY. No production Strength Profile runtime. No Taxonomy V2.

## Architecture

```text
Strength Engine V1
      |
      v
Strength Evidence
      |
      v
Strength Profile
      |
      v
Future Taxonomy V2 (not implemented)
      |
      v
Confidence
      |
      v
Public Contract
```

## Principles

- Score remains the quantitative net-strength index (V1 authoritative).
- Profile preserves multidimensional evidence currently compressed by V1.
- Profile does **not** emit taxonomy labels or T1-T6 thresholds.
- Populations stay separated: REAL_CALIBRATION / SYNTHETIC_STRESS / RUNTIME_REFERENCE / DESIGN_EXAMPLES.

## Schema version

`strength_profile_design_v0.1.0-candidate`
