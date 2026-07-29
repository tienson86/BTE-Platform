# SPECIAL_CASE_TAXONOMY.md — Special Case Rule Taxonomy

> Module: 05_special_case_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the complete taxonomy for Special Case detection and resolution in the BTE Knowledge Base.

---

# 2. Categories

| Category | Family | Description |
|----------|--------|-------------|
| transformed_edge | transformed_edge | Củng cục, hóa khí, nhất khí, extreme strength |
| pseudo_follow | pseudo_follow_override | Tòng giả, follow overrides without true follow |
| pattern_breaking | pattern_breaking | Pattern broken by clash, drain, or structure |
| seasonal | seasonal_exception | Season/element temperature exceptions |
| hidden_stem | hidden_stem_exception | Hidden stem reveal, clash, combine |
| clash_combine | clash_combine | Lục xung, lục hại, lục phá, hình |
| priority | priority_override | Group execution order overrides |
| priority | tie_breaking | Score/priority tiebreak rules |
| fallback | fallback_behavior | Default resolution when no match |

---

# 3. Source Data

| Source | Rules | Category |
|--------|-------|----------|
| database/12_strength/07_special_rules.csv | 7 | pattern_breaking, seasonal, transformed |
| database/11_temperature/07_special_rules.csv | 8 | seasonal, clash_combine |
| database/13_useful_god/06_special_rules.csv | 4 | pseudo_follow |
| database/15_score_engine/02_wuxing/07_special_score.csv | 8 | transformed, pseudo_follow |
| database/15_score_engine/03_strength/06_special_case.csv | 2 | pattern_breaking |
| database/15_score_engine/04_ten_gods/05_special_case.csv | 7 | transformed, pattern_breaking |
| database/15_score_engine/02_wuxing/05_clash_score.csv | 7 | clash_combine |
| Synthetic extensions | 22 | hidden_stem, tie_breaking, priority, fallback |

---

# 4. Priority Hierarchy

```
Special Case Group     (order 200)
  ↓
Pseudo Follow Group    (order 195)
  ↓
Pattern Breaking Group (order 190)
  ↓
Seasonal Group         (order 185)
  ↓
Clash/Combine Group   (order 180)
  ↓
Tie-breaking Rules    (order 170–185)
  ↓
Fallback              (order 1–5)
```

---

# 5. Condition Fields

| Field | Type | Source Module |
|-------|------|---------------|
| strength_level | str | 01_strength_rules |
| season | str | 02_season_rules |
| temperature_type | str | 03_temperature_rules |
| primary_pattern | str | 04_pattern_rules |
| follow_pattern | str/bool | Pattern Engine |
| hidden_stems_flat | list | Bazi Engine |
| clash_type | str | Score Engine |
| ten_gods_list | list | Bazi Engine |

---

# 6. References

- `MODULE_SPEC.md`
- `SPECIAL_CASE_DECISION_TREE.md`
- `database/12_strength/07_special_rules.csv`
