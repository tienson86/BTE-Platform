# Season Rule Database

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

`02_season_rules/` is the JSON Rule Database module for **Season** analysis in the BTE Knowledge Base.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate rule statistics |
| `season_rules.json` | Complete rule dataset (46 rules) |
| `season_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Taxonomy

| Category | Count |
|----------|-------|
| season_classification | 4 |
| season_phase | 12 |
| element_affinity | 18 |
| solar_term | 8 |
| priority | 4 |

**ID prefix:** `SEA` | **Range:** SEA-000001 to SEA-000046

---

# 4. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/`
- Spec: `MODULE_SPEC.md`

---

# 5. Conclusion

Complete Season Rule Database with 46 rules covering all supported seasonal scenarios.
