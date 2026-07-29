# MODULE_SPEC.md — Combination Rule Database

> Module: 07_combination_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Combination Rule Database: multi-module composite rules, conflict detection, override resolution, and candidate selection.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Pattern ten-god combinations | Single-module scoring (see upstream modules) |
| Strength + season combinations | Priority final resolution (see 08_priority_rules) |
| Season + temperature combinations | Report formatting |
| Pattern + special case / follow | |
| Multi-module composites | |
| Conflict detection and selection | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| pattern_combination | 5 |
| strength_season | 9 |
| season_temperature | 5 |
| pattern_special_case | 5 |
| pattern_follow | 5 |
| multi_module | 5 |
| composite_decision | 4 |
| override_combination | 4 |
| conflict_detection | 4 |
| candidate_selection | 4 |
| execution_grouping | 4 |
| element_combination | 7 |

**Total rules:** 61

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01`–`06` rule database modules
- **used_by:** `08_priority_rules`, Useful God Engine
- **execution_order:** Follow Pattern → Combination → Priority

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| favorable_threshold | 70 |
| unfavorable_threshold | 30 |
| confidence_threshold | 0.65 |

---

# 6. Output

- `combination_match` — selected combination code
- `combination_score` — aggregate score
- `matched_rules` / `rejected_rules`

---

# 7. Data Sources

- `database/14_pattern/04_combination_pattern.csv`
- `database/12_strength/07_special_rules.csv`
- `database/15_score_engine/02_wuxing/04_combination_score.csv`

---

# 8. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 67 objects validated
- Golden examples: 6
- Test cases: 6

---

# 9. Design Documents

- `COMBINATION_TAXONOMY.md`
- `COMBINATION_DECISION_TREE.md`

---

# 10. References

- `knowledge/rule_database/06_follow_pattern_rules/` (immediate upstream)
- `RULE_MODEL_SPEC.md`
