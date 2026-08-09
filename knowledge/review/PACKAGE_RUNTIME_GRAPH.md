# Package Runtime Graph

Suggested load / evaluation order for a future Analysis Engine. **Documentation only** — no pipeline code changed.

## Canonical analytical order

Aligns with AF-1 pipeline direction and optional-dep topology:

1. Chart construction (Calendar / Four Pillars — **no V2 package yet**)
2. `bz_01_strength_core`
3. `bz_02_seasonal_core`
4. `bz_03_temperature_core`
5. `bz_04_pattern_core`
6. `bz_05_pattern_evaluation`
7. `bz_06_useful_god_foundation`
8. `bz_07_useful_god_priority`
9. `bz_08_useful_god_override` (optional final UG pass)
10. `bz_10_follow_pattern_core`
11. `bz_11_transformation_core`
12. `bz_12_combination_clash_core`
13. `bz_13_ten_gods_advanced`
14. `bz_14_twelve_growth_advanced`
15. `bz_15_hidden_stems_advanced`
16. Interpretation / Report packages (**missing**)

## Parallel track

- `bz_09_luck_foundation` — timeline reference after natal chart exists. Not a predecessor of bz_02–bz_15.

## Runtime constraints

- Do not evaluate a consumer before its optional producers if those signals are required for a given profile.
- Missing optional signals → withhold / low-confidence publication (already encoded in Wave 1 rules).
- Never write back into upstream package outputs.

## Ordering invariants

| Invariant | Status |
| --- | --- |
| Strength before Seasonal/Temperature consumers | Hold |
| Pattern Core before Pattern Evaluation | Hold |
| UGD before UGP before UGO | Hold |
| Follow after Pattern Evaluation + UGP | Hold |
| Transformation after Follow | Hold |
| Combination/Clash after Transformation | Hold |
| Ten Gods after Combination/Clash | Hold |
| Twelve Growth after Ten Gods | Hold |
| Hidden Stems after Twelve Growth | Hold |
| No reverse import | Hold |
