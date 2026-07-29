# Follow Pattern Rule Database

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

`06_follow_pattern_rules/` is the JSON Rule Database module for **Follow Pattern** (Tòng Cách) analysis in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `FOLLOW_PATTERN_TAXONOMY.md` | Follow pattern classification taxonomy |
| `FOLLOW_PATTERN_DECISION_TREE.md` | Detection and resolution flow |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `follow_pattern_rules.json` | Complete rule dataset (51 rules) |
| `follow_pattern_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Calendar → Bazi → Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Combination
```

Depends on: `01_strength_rules/` through `05_special_case_rules/`

Used by: `07_combination_rules/`, Useful God Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| true_follow | 6 |
| pseudo_follow | 5 |
| eligibility | 6 |
| maintenance | 4 |
| break | 5 |
| conversion | 4 |
| seasonal | 4 |
| threshold | 4 |
| special_interaction | 4 |
| priority | 7 |
| fallback | 2 |

**ID prefix:** `FOL` | **Range:** FOL-000001 to FOL-000051

---

# 5. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/` through `05_special_case_rules/`
- Spec: `MODULE_SPEC.md`
- Source data: `database/14_pattern/03_follow_pattern.csv`

---

# 6. Conclusion

Complete Follow Pattern Rule Database with 51 rules covering true follow, pseudo-follow, eligibility, maintenance, break conditions, conversion, season confirmation, strength thresholds, special case interaction, priority ordering, and fallback behavior.
