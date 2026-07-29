# Temperature Rule Database

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

`03_temperature_rules/` is the JSON Rule Database module for **Temperature** analysis (Ấm-Hàn, Táo-Thấm) in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `temperature_rules.json` | Complete rule dataset (56 rules) |
| `temperature_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Calendar → Bazi → Season → Strength → Temperature → Pattern → Useful God
```

Depends on: `01_strength_rules/`, `02_season_rules/`

Used by: `04_pattern_rules/`, Useful God Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| season | 6 |
| climate | 6 |
| dryness | 5 |
| humidity | 5 |
| balance | 9 |
| element | 5 |
| special | 4 |
| interaction | 5 |
| priority | 11 |

**ID prefix:** `TMP` | **Range:** TMP-000001 to TMP-000056

---

# 5. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/`, `02_season_rules/`
- Spec: `MODULE_SPEC.md`
- Source data: `database/11_temperature/`

---

# 6. Conclusion

Complete Temperature Rule Database with 56 rules covering seasonal influence, climate correction, dry/humid balance, hot/cold classification, element adjustment, cross-module interaction, and priority resolution.
