# Pattern Rule Database

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

`04_pattern_rules/` is the JSON Rule Database module for **Pattern** (Cách Cục) analysis in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `PATTERN_TAXONOMY.md` | Pattern classification taxonomy |
| `PATTERN_DECISION_TREE.md` | Recognition and conflict resolution flow |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `pattern_rules.json` | Complete rule dataset (68 rules) |
| `pattern_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Calendar → Bazi → Season → Strength → Temperature → Pattern → Useful God
```

Depends on: `01_strength_rules/`, `02_season_rules/`, `03_temperature_rules/`

Used by: `05_flow_rules/`, Useful God Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| standard | 11 |
| transformed | 5 |
| follow | 6 |
| mixed | 9 |
| pseudo_follow | 4 |
| broken | 5 |
| exceptional | 4 |
| eligibility | 10 |
| priority | 14 |

**ID prefix:** `PAT` | **Range:** PAT-000001 to PAT-000068

---

# 5. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/`, `02_season_rules/`, `03_temperature_rules/`
- Spec: `MODULE_SPEC.md`
- Source data: `database/14_pattern/`

---

# 6. Conclusion

Complete Pattern Rule Database with 68 rules covering standard, transformed, follow, pseudo-follow, broken, mixed, and exceptional patterns, plus eligibility conditions, conflict resolution, and priority groups.
