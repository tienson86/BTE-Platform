# COMBINATION_TAXONOMY.md — Combination Rule Taxonomy

> Module: 07_combination_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the complete taxonomy for multi-module Combination rules in the BTE Knowledge Base.

---

# 2. Categories

| Category | Family | Description |
|----------|--------|-------------|
| pattern_combination | pattern_combination | Ten-god pattern pairs (Quan Ấn, Sát Ấn, etc.) |
| strength_season | strength_season | Strength level + season alignment |
| season_temperature | season_temperature | Season + climate/temperature alignment |
| pattern_special_case | pattern_special_case | Pattern + special case interaction |
| pattern_follow | pattern_follow | Primary pattern + follow pattern |
| multi_module | multi_module | Three or more module signals combined |
| composite_decision | composite_decision | Aggregate favorable/unfavorable decisions |
| override | override_combination | Cross-module override rules |
| conflict | conflict_detection | Conflicting signal detection |
| candidate_selection | candidate_selection | Winner selection among candidates |
| execution_group | execution_grouping | Rule group execution order |
| element_combination | element_combination | Stem/branch harmony combinations |

---

# 3. Pattern Combinations

| Code | Vietnamese | Ten Gods |
|------|------------|----------|
| quan_an | Quan Ấn | Chính Quan + Chính Ấn |
| sat_an | Sát Ấn | Thất Sát + Chính Ấn |
| thuc_than_sinh_tai | Thực Thần sinh Tài | Thực Thần + Chính Tài |
| thuong_quan_phoi_an | Thương Quan phối Ấn | Thương Quan + Chính Ấn |
| tai_quan_song_my | Tài Quan Song Mỹ | Chính Tài + Chính Quan |

---

# 4. Element Combinations

| Type | Description |
|------|-------------|
| TIAN_GAN_HE | Heavenly stem combine |
| DI_ZHI_LIUHE | Six branch combine |
| TAM_HOP | Three harmony |
| TAM_HOI | Three meeting |
| BAN_HOP | Half combine |
| HUA_SUCCESS | Successful transformation |
| HUA_FAIL | Combine without transform |

---

# 5. Execution Groups

```
strength_season  (order 100)
  ↓
pattern_follow   (order 95)
  ↓
special_override (order 90)
  ↓
final_selection  (order 85)
```

---

# 6. References

- `database/14_pattern/04_combination_pattern.csv`
- `COMBINATION_DECISION_TREE.md`
