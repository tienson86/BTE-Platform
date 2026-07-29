# COMBINATION_DECISION_TREE.md — Combination Decision Tree

> Module: 07_combination_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Documents the decision flow for multi-module combination matching, conflict resolution, and candidate selection.

---

# 2. Pipeline Position

```
Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Combination → Priority
```

---

# 3. Decision Tree

```
START
  │
  ├─► Load all upstream signals
  │     (strength, season, temperature, pattern, special_case, follow)
  │
  ├─► Phase 1: Execution Group — strength_season
  │     ├─ Match strength+season combinations
  │     └─ Match season+temperature combinations
  │
  ├─► Phase 2: Execution Group — pattern_follow
  │     ├─ Match pattern combinations (Quan Ấn, etc.)
  │     └─ Match pattern+follow combinations
  │
  ├─► Phase 3: Execution Group — special_override
  │     ├─ Match pattern+special case combinations
  │     └─ Apply override rules (follow > pattern > main)
  │
  ├─► Phase 4: Multi-Module Composites
  │     └─ Evaluate 3+ module signal combinations
  │
  ├─► Phase 5: Conflict Detection
  │     ├─ pattern vs follow conflict?
  │     ├─ special vs pattern conflict?
  │     └─ strength vs season conflict?
  │
  ├─► Phase 6: Candidate Selection
  │     ├─ Highest priority wins
  │     ├─ Equal priority → highest score
  │     └─ Equal score → first match
  │
  ├─► Phase 7: Composite Decision
  │     ├─ score > 70 → favorable
  │     ├─ score < 30 → unfavorable
  │     └─ else → neutral / mixed
  │
  └─► OUTPUT: combination_match
        ├─ selected_combination
        ├─ combination_score
        ├─ matched_rules[]
        └─ rejected_rules[]
```

---

# 4. Override Hierarchy

| Order | Rule | Resolution |
|-------|------|------------|
| 195 | ov_follow_beats_pattern | Follow wins |
| 190 | ov_special_beats_pattern | Special case wins |
| 185 | ov_combination_beats_main | Combination beats single |
| 180 | ov_multi_winner | Highest score across modules |

---

# 5. Candidate Selection

1. `sel_highest_priority` — highest priority order
2. `sel_highest_score` — highest evaluation weight
3. `sel_best_composite` — best multi-module composite
4. `sel_first_match` — tiebreaker

---

# 6. References

- `COMBINATION_TAXONOMY.md`
- `DEPENDENCIES.json`
