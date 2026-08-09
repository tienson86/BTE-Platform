# Validation Summary

## Package PVP-RELEASE rollup

| Package | Profile | Status | Errors | Warnings |
| --- | --- | --- | --- | --- |
| bz_01_strength_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_02_seasonal_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_03_temperature_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_04_pattern_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_05_pattern_evaluation | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_06_useful_god_foundation | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_07_useful_god_priority | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_08_useful_god_override | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_09_luck_foundation | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_10_follow_pattern_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_11_transformation_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_12_combination_clash_core | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_13_ten_gods_advanced | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_14_twelve_growth_advanced | PVP-RELEASE | pass_with_warnings | 0 | 1 |
| bz_15_hidden_stems_advanced | PVP-RELEASE | pass_with_warnings | 0 | 1 |

Common warning: **VAL-GOLDEN** — Golden Dataset not applicable until Analysis Engine wiring.

## KX-6D governance checks (this sprint)

| Check | Result |
| --- | --- |
| All bz_01–bz_15 present | Pass |
| No cyclic optional/required deps | Pass |
| No dangling dependency package_id | Pass |
| Duplicate published output names | None |
| Evidence count == rule count (non-luck) | Pass |
| Sealed checksum length | Pass |
| This sprint mutated packages / engines / APIs | **No** (additive `knowledge/review/` only) |

## Ecosystem validation verdict

**Pass with warnings** — same class as individual packages: commercially reviewable knowledge, not engine-certified.
