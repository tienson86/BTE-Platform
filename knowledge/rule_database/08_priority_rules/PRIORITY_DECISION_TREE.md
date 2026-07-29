# PRIORITY_DECISION_TREE.md — Priority Decision Tree

> Module: 08_priority_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Documents the decision flow for final priority resolution across all upstream modules.

---

# 2. Pipeline Position

```
Modules 01–07 → Priority Engine (08) → Score Engine / Useful God
```

---

# 3. Decision Tree

```
START
  │
  ├─► Collect all matched rules from upstream modules
  │
  ├─► Phase 1: Apply Override Rules
  │     ├─ special_case_flag? ──► ov_special_beats_all
  │     ├─ follow_type set? ──► ov_follow_beats_pattern
  │     └─ combination_match? ──► ov_combination_beats_single
  │
  ├─► Phase 2: Conflict Detection
  │     ├─ Multiple candidates? ──► conflict_multi_module
  │     ├─ Pattern + follow? ──► conflict_pattern_follow
  │     └─ Equal priority? ──► conflict_equal_priority
  │
  ├─► Phase 3: Tie-Breaking
  │     ├─ tie_higher_priority
  │     ├─ tie_higher_weight
  │     ├─ tie_module_order
  │     └─ tie_first_match
  │
  ├─► Phase 4: Score Normalization
  │     ├─ norm_baseline_50
  │     ├─ norm_scale_100
  │     └─ norm_weighted_aggregate
  │
  ├─► Phase 5: Weighted Selection
  │     └─ Apply dimension weights (STRENGTH 25%, PATTERN 20%, etc.)
  │
  ├─► Phase 6: Final Selection
  │     ├─ final_confidence_gate (≥ 0.65)
  │     ├─ final_highest_composite
  │     ├─ final_single_winner
  │     └─ final_mark_selected
  │
  └─► OUTPUT: priority_resolution
        ├─ selected_rule_id
        ├─ normalized_score
        ├─ winning_module
        └─ rejected_candidates[]
```

---

# 4. Fallback Behavior

| Rule | Condition | Action |
|------|-----------|--------|
| fallback_no_match | No rules matched | Pipeline default |
| fallback_default_module | No priority rule | Use module default output |
| fallback_lowest_priority | All rejected | Lowest priority fallback |

---

# 5. References

- `PRIORITY_HIERARCHY.md`
- `DEPENDENCIES.json`
