# Special Case Rule Database

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

`05_special_case_rules/` is the JSON Rule Database module for **Special Case** detection and resolution in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `SPECIAL_CASE_TAXONOMY.md` | Special case classification taxonomy |
| `SPECIAL_CASE_DECISION_TREE.md` | Detection and resolution flow |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `special_case_rules.json` | Complete rule dataset (66 rules) |
| `special_case_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Calendar → Bazi → Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Useful God
```

Depends on: `01_strength_rules/`, `02_season_rules/`, `03_temperature_rules/`, `04_pattern_rules/`

Used by: `06_follow_pattern_rules/`, Useful God Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| transformed_edge | 14 |
| pseudo_follow | 8 |
| pattern_breaking | 9 |
| seasonal | 7 |
| hidden_stem | 5 |
| clash_combine | 11 |
| priority | 9 |
| fallback | 3 |

**ID prefix:** `SPC` | **Range:** SPC-000001 to SPC-000066

---

# 5. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/` through `04_pattern_rules/`
- Spec: `MODULE_SPEC.md`
- Source data: `database/12_strength/`, `database/11_temperature/`, `database/13_useful_god/`, `database/15_score_engine/`

---

# 6. Conclusion

Complete Special Case Rule Database with 66 rules covering transformed edge cases, pseudo-follow overrides, pattern-breaking exceptions, seasonal exceptions, hidden stem exceptions, clash/combine handling, priority overrides, tie-breaking, and fallback behavior.
