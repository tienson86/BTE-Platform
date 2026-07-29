# MODULE_SPEC.md — Priority Rule Database

> Module: 08_priority_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Priority Rule Database: module and rule priority, override resolution, conflict handling, tie-breaking, fallback selection, weighted selection, score normalization, execution order, and final rule selection.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Module execution order | Individual module scoring logic |
| Rule group priority | Pattern/strength rule definitions |
| Override rules (special, follow, combination) | Report formatting |
| Conflict detection and resolution | |
| Tie-breaking strategies | |
| Fallback selection | |
| Dimension weight application | |
| Score normalization | |
| Final winner selection | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| module_priority | 7 |
| rule_priority | 11 |
| override_rule | 6 |
| conflict_resolution | 5 |
| tie_breaking | 4 |
| fallback_selection | 3 |
| weighted_selection | 14 |
| score_normalization | 7 |
| execution_order | 8 |
| final_selection | 4 |

**Total rules:** 69

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01_strength_rules` through `07_combination_rules`
- **used_by:** Useful God Engine, Score Engine
- **execution_order:** Combination → Priority (stage 8)

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| confidence_threshold | 0.65 |
| pipeline_stages | 8 |

---

# 6. Output

- `priority_resolution` — selected rule and winning module
- `normalized_score` — baseline-normalized composite score
- `selected_rule_id` — final winning rule ID
- `rejected_candidates[]` — rules eliminated during resolution

---

# 7. Data Sources

- `database/14_pattern/05_priority_rules.csv`
- `database/13_useful_god/05_priority_rules.csv`
- `database/12_strength/06_priority_rules.csv`
- `database/15_score_engine/09_final_score/04_dimension_weight.csv`
- `database/15_score_engine/08_luck/05_luck_priority.csv`

---

# 8. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 75 objects validated
- Golden examples: 6
- Test cases: 6
- Coverage: 10/10 families complete (100%)

---

# 9. Design Documents

- `PRIORITY_HIERARCHY.md`
- `PRIORITY_DECISION_TREE.md`

---

# 10. References

- `knowledge/rule_database/07_combination_rules/` (immediate upstream)
- `RULE_MODEL_SPEC.md`
