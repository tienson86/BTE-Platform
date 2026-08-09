# Ecosystem Review

## Scope

Fifteen released Knowledge Packages (`bz_01` … `bz_15`). No engines, pipelines, or APIs were opened.

## Inventory

| ID | Path | Type | Domain | Version | Rules | Evidence | Chains |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bz_01_strength_core | strength/core | analytical | DOM-STRENGTH | 1.2.0 | 110 | 110 | 3 |
| bz_02_seasonal_core | seasonal/core | analytical | DOM-SEASONAL | 1.0.0 | 110 | 110 | 3 |
| bz_03_temperature_core | temperature/core | analytical | DOM-TEMPERATURE | 1.0.0 | 110 | 110 | 3 |
| bz_04_pattern_core | pattern/core | analytical | DOM-PATTERN | 1.0.0 | 110 | 110 | 3 |
| bz_05_pattern_evaluation | pattern/evaluation | analytical | DOM-PATTERN | 1.0.0 | 110 | 110 | 3 |
| bz_06_useful_god_foundation | useful_god/foundation | decision | DOM-USEFUL_GOD | 1.0.0 | 109 | 109 | 3 |
| bz_07_useful_god_priority | useful_god/priority | decision | DOM-USEFUL_GOD | 1.0.0 | 110 | 110 | 5 |
| bz_08_useful_god_override | useful_god/override | decision | DOM-USEFUL_GOD | 1.0.0 | 110 | 110 | 5 |
| bz_09_luck_foundation | luck/foundation | reference | DOM-LUCK_CYCLE | 1.0.0 | 0 | 0 | 0 |
| bz_10_follow_pattern_core | follow_pattern/core | analytical | DOM-PATTERN | 1.0.0 | 250 | 250 | 6 |
| bz_11_transformation_core | transformation/core | analytical | DOM-TRANSFORMATION | 1.0.0 | 280 | 280 | 7 |
| bz_12_combination_clash_core | combination_clash/core | analytical | DOM-COMBINATION | 1.0.0 | 300 | 300 | 8 |
| bz_13_ten_gods_advanced | ten_gods/advanced | analytical | DOM-TEN_GODS | 1.0.0 | 400 | 400 | 8 |
| bz_14_twelve_growth_advanced | twelve_growth/advanced | analytical | DOM-TWELVE_GROWTH | 1.0.0 | 360 | 360 | 8 |
| bz_15_hidden_stems_advanced | hidden_stems/advanced | analytical | DOM-HIDDEN_STEM | 1.0.0 | 380 | 380 | 8 |

**Totals:** 15 packages · 2 849 rules · 2 849 evidence bundles · 73 reasoning chains.

## Findings (executive)

1. **No cyclic dependencies.** All declared edges are optional. Independently deployable.
2. **Analytical spine is complete** from Strength → Seasonal → Temperature → Pattern → Useful God → Follow → Transformation → Combination/Clash → Ten Gods → Twelve Growth → Hidden Stems.
3. **Contract assets are incomplete on bz_01–bz_04** (no `assets/published_*.json`). Downstream packages still consume `strength_score` / `season_score` / `temperature_score` as published contracts. Evolution debt, not a cycle.
4. **bz_09_luck_foundation is isolated** (reference timeline; 0 production rules; raw pillar inputs). Not on the analytical consumer path.
5. **Leaves without in-ecosystem consumers:** bz_08 (final UG override), bz_15 (hidden stems). Expected until Interpretation packages exist.
6. **All packages released, checksummed (64 hex), PVP-RELEASE `pass_with_warnings`, 0 validation errors.** Golden Dataset remains N/A until engine wiring.
7. **11 of 34 taxonomy domains** have a primary package. Clash/Harm/Punishment live inside bz_12 under `DOM-COMBINATION`. Calendar, Shen Sha, Interpretation, Report, and luck analytical layers are missing.

## Governance posture

Additive Wave 1 knowledge is **Gold / RM-reviewable**. It is **not** engine-complete. Do not mutate sealed packages to close gaps; open new packages or a later SemVer minor after Release Manager policy.
