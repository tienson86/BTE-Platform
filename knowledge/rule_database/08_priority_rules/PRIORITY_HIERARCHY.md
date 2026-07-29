# PRIORITY_HIERARCHY.md — Priority Hierarchy

> Module: 08_priority_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the complete priority hierarchy for the BTE analysis pipeline.

---

# 2. Module Execution Order

| Stage | Module | Output |
|-------|--------|--------|
| 1 | 02_season_rules | season_score |
| 2 | 01_strength_rules | strength_score |
| 3 | 03_temperature_rules | temperature_score |
| 4 | 04_pattern_rules | pattern_match |
| 5 | 05_special_case_rules | special_case_flag |
| 6 | 06_follow_pattern_rules | follow_pattern_match |
| 7 | 07_combination_rules | combination_match |
| 8 | 08_priority_rules | priority_resolution |

---

# 3. Override Hierarchy

```
Special Case Override     (order 198–200)
  ↓
Follow Pattern Override   (order 195–200)
  ↓
Combination Override      (order 185–190)
  ↓
Pattern Module            (order 85–95)
  ↓
Strength Module           (order 80–100)
  ↓
Season Module             (order 90–100)
  ↓
Temperature Module        (order 70)
  ↓
Fallback                  (order 1–10)
```

---

# 4. Rule Group Priority (Within Module)

| Group | Priority Order |
|-------|----------------|
| special | 100 |
| follow | 95 |
| season | 95 |
| root | 90 |
| support | 85 |
| control | 80 |
| combination | 70 |
| eligibility | 50–60 |

---

# 5. Dimension Weights (Score Engine)

| Module | Weight | Priority |
|--------|--------|----------|
| STRENGTH | 0.25 | 100 |
| PATTERN | 0.20 | 95 |
| USEFUL_GOD | 0.20 | 95 |
| TEN_GODS | 0.15 | 85 |
| WUXING | 0.10 | 70 |
| LUCK | 0.05 | 60 |
| SHENSHA | 0.05 | 50 |

---

# 6. Tie-Breaking Order

1. Higher priority order
2. Higher evaluation weight
3. Pipeline module stage order
4. First match

---

# 7. References

- `PRIORITY_DECISION_TREE.md`
- `database/14_pattern/05_priority_rules.csv`
- `database/13_useful_god/05_priority_rules.csv`
