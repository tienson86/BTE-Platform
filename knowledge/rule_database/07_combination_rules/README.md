# Combination Rule Database

> Module: Rule Database
>
> Version: 1.0.0
>
> Status: Active
>
> Document Type: Module README
>
> BTE Platform

---

# 1. Purpose

`07_combination_rules/` is the JSON Rule Database module for **Combination** (multi-module composite) analysis in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `COMBINATION_TAXONOMY.md` | Combination classification taxonomy |
| `COMBINATION_DECISION_TREE.md` | Matching and resolution flow |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `combination_rules.json` | Complete rule dataset (61 rules) |
| `combination_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Combination → Priority
```

Depends on: `01_strength_rules/` through `06_follow_pattern_rules/`

Used by: `08_priority_rules/`, Useful God Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| pattern_combination | 5 |
| strength_season | 9 |
| season_temperature | 5 |
| pattern_special_case | 5 |
| pattern_follow | 5 |
| multi_module | 5 |
| composite_decision | 4 |
| override | 4 |
| conflict | 4 |
| candidate_selection | 4 |
| execution_group | 4 |
| element_combination | 7 |

**ID prefix:** `COM` | **Range:** COM-000001 to COM-000061

---

# 5. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/` through `06_follow_pattern_rules/`
- Spec: `MODULE_SPEC.md`
- Source data: `database/14_pattern/`, `database/12_strength/`, `database/15_score_engine/`

---

# 6. Conclusion

Complete Combination Rule Database with 61 rules covering strength+season, season+temperature, pattern+special case, pattern+follow, multi-module composites, override combinations, conflict detection, candidate selection, and execution grouping.
