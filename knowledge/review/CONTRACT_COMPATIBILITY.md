# Contract Compatibility

## Method

Compare `assets/published_inputs.json` and `assets/published_outputs.json` across packages. Foundation packages without those assets are recorded as **implicit contracts**.

## Producer registry (explicit assets)

| Signal | Producer |
| --- | --- |
| pattern_quality, pattern_confidence, pattern_integrity, pattern_stability, pattern_score | bz_05_pattern_evaluation |
| evaluation_diagnostics | bz_05_pattern_evaluation |
| useful_god, favorable_gods, unfavorable_gods, decision_confidence, decision_score, decision_reasoning, decision_diagnostics | bz_06_useful_god_foundation |
| resolved_useful_god, resolved_favorable_gods, resolved_unfavorable_gods, decision_priority, conflict_resolution, resolution_confidence, resolution_reasoning, resolution_diagnostics | bz_07_useful_god_priority |
| final_useful_god, final_favorable_gods, final_unfavorable_gods, override_applied, override_reason, override_confidence, decision_trace, decision_audit | bz_08_useful_god_override |
| natal_chart, major_cycles, annual_cycles, monthly_cycles, timeline_metadata, timeline_version | bz_09_luck_foundation |
| follow_pattern, follow_pattern_type, follow_pattern_confidence, follow_pattern_score, follow_pattern_reasoning, follow_pattern_diagnostics | bz_10_follow_pattern_core |
| transformation_detected, transformation_type, transformation_strength, transformation_score, transformation_confidence, transformation_reasoning, transformation_diagnostics | bz_11_transformation_core |
| combination_detected, combination_types, clash_detected, interaction_strength, interaction_score, interaction_confidence, interaction_reasoning, interaction_diagnostics | bz_12_combination_clash_core |
| ten_gods_profile, ten_gods_balance, ten_gods_dominance, ten_gods_score, ten_gods_confidence, ten_gods_reasoning, ten_gods_diagnostics | bz_13_ten_gods_advanced |
| growth_phase, growth_profile, growth_balance, growth_score, growth_confidence, growth_reasoning, growth_diagnostics | bz_14_twelve_growth_advanced |
| hidden_stems_profile, hidden_stems_balance, hidden_stems_dominance, hidden_stems_score, hidden_stems_confidence, hidden_stems_reasoning, hidden_stems_diagnostics | bz_15_hidden_stems_advanced |

## Implicit contracts (no published_* assets)

| Signal (consumed downstream) | Expected producer | Asset status |
| --- | --- | --- |
| strength_score | bz_01_strength_core | Missing explicit publish file |
| season_score | bz_02_seasonal_core | Missing explicit publish file |
| temperature_score | bz_03_temperature_core | Missing explicit publish file |
| principal / pattern internals used conceptually | bz_04_pattern_core | Missing explicit publish file |

This is the primary **contract evolution** item: downstream Wave 1 packages treat these scores as official contracts, but bz_01–bz_04 do not ship `assets/published_outputs.json`.

## Duplicate contracts

No two packages publish the **same output name**. Diagnostic/reasoning suffixes are namespaced per domain (`follow_pattern_reasoning` vs `transformation_reasoning`, etc.).

Semantic overlap (not name collision): combination labels exist in Transformation (state) and Combination & Clash (relationship). Intentional split. See [SEMANTIC_DUPLICATION_REPORT.md](SEMANTIC_DUPLICATION_REPORT.md).

## Unused contracts

Published but not consumed by any later package (expected until Interpretation):

- Most `*_reasoning` / `*_diagnostics` / `*_confidence` tails after the primary score/type
- UG override finals (`final_useful_god`, `override_*`, `decision_audit`)
- All bz_09 timeline outputs
- All bz_15 hidden-stems outputs
- `combination_detected`, `clash_detected`, `growth_phase`, `ten_gods_score`, etc. (later packages often consume only a subset)

Unused ≠ invalid. They remain official contracts for future consumers.

## Unproduced inputs (declared consume, no explicit producer asset)

| Input | Notes |
| --- | --- |
| season_score, strength_score, temperature_score | Implicit from bz_01–bz_03 |
| year_pillar, month_pillar, day_pillar, hour_pillar, gender, birth_* | bz_09 chart/timeline inputs — engine/chart layer, not a V2 analytical package |

## Compatibility

| Check | Result |
| --- | --- |
| Schema 2.0.0 across all packages | Pass |
| compatibility_version 1.0.0 | Pass |
| No required circular contracts | Pass |
| Name uniqueness of published outputs | Pass |
| Explicit publish files on bz_01–bz_04 | **Gap** |
| Luck vs analytical input model | Divergent (reference vs score-band) — documented |

## Evolution readiness

- Additive new outputs: allowed via new package or SemVer minor after RM.
- Renaming published outputs: **forbidden** without wrapper (AF-1 / KD freeze).
- Closing bz_01–bz_04 asset gap: new patch/minor **on those packages** — out of KX-6D scope (must not modify packages now).
