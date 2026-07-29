# SPECIAL_CASE_DECISION_TREE.md — Special Case Decision Tree

> Module: 05_special_case_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Documents the decision flow for Special Case detection, override resolution, and fallback behavior.

---

# 2. Pipeline Position

```
Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Useful God
```

---

# 3. Decision Tree

```
START
  │
  ├─► Load upstream signals
  │     (strength_level, season, temperature_type, primary_pattern)
  │
  ├─► Phase 1: Eligibility Check
  │     └─ Required upstream signals present? ──NO──► fallback_no_special_case
  │
  ├─► Phase 2: Match Special Case Rules
  │     ├─ Transformed edge cases (Củng cục, Hóa khí, Nhất khí)
  │     ├─ Pseudo-follow overrides (Tòng giả, partial follow)
  │     ├─ Pattern-breaking (clash, drain, structure)
  │     ├─ Seasonal exceptions (element + season)
  │     ├─ Hidden stem exceptions (reveal, clash, combine)
  │     └─ Clash/combine handling (Lục xung, Lục hại, etc.)
  │
  ├─► Phase 3: Priority Resolution
  │     ├─ Apply group priority (special > pseudo > breaking > seasonal > clash)
  │     ├─ Equal priority? ──► tiebreak_higher_weight
  │     ├─ Equal weight? ──► tiebreak_first_match
  │     └─ Special vs standard? ──► tiebreak_special_over_standard
  │
  ├─► Phase 4: Output
  │     ├─ special_case_flag = true/false
  │     ├─ matched_rules[]
  │     └─ rejected_rules[]
  │
  └─► No match? ──► fallback_no_special_case (order 1)
```

---

# 4. Override Rules

| Scenario | Resolution | Rule Family |
|----------|------------|-------------|
| Follow detected but strength not weak | Pseudo follow penalty | pseudo_follow_override |
| Officer clash breaks Quan pattern | Pattern break downgrade | pattern_breaking |
| Six clash in chart | Clash score penalty | clash_combine |
| Useful god follow override | Follow tai/quan/sat | pseudo_follow_override |
| Ambiguous pattern confidence | Conservative fallback | fallback_behavior |

---

# 5. Tie-Breaking Order

1. Higher priority order wins
2. Higher evaluation weight wins
3. First matched rule wins
4. Special case beats standard pattern rule

---

# 6. Fallback Behavior

| Rule | Condition | Action |
|------|-----------|--------|
| fallback_no_special_case | No rules matched | Proceed standard pipeline |
| fallback_ambiguous_pattern | pattern_confidence < 0.65 | Conservative handling |
| fallback_default_resolution | All tiebreakers exhausted | Default resolution |

---

# 7. References

- `SPECIAL_CASE_TAXONOMY.md`
- `DEPENDENCIES.json`
- `knowledge/rule_database/04_pattern_rules/PATTERN_DECISION_TREE.md`
