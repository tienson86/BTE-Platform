# MODULE_SPEC.md — Season Rule Database

> Module: 02_season_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Season Rule Database module: seasonal classification, phase resolution, element affinity scoring, and solar term influence for Bazi analysis.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Four seasons (spring, summer, autumn, winter) | Strength month command (see 01_strength_rules) |
| Season phases (early/mid/late) | Temperature scoring (see 03_temperature_rules) |
| Element affinity by season | Useful god selection |
| Solar term influence | Pattern matching |

---

# 3. Rule Taxonomy

| Family | Count | ID Range |
|--------|-------|----------|
| season_classification | 4 | SEA-000001–004 |
| season_phase | 12 | SEA-000005–016 |
| element_affinity | 18 | SEA-000017–034 |
| solar_term_score | 8 | SEA-000035–042 |
| group_priority | 4 | SEA-000043–046 |

**Total rules:** 46

---

# 4. Rule Model

All rules use Rule Model v1.0.0 with:

- **Domain:** `season`
- **Target:** `day_master.season_score`
- **ID prefix:** `SEA`
- **Origin:** `rule_database`

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| spring dominant | wood |
| summer dominant | fire |
| autumn dominant | metal |
| winter dominant | water |

---

# 6. Data Sources

- `database/15_score_engine/02_wuxing/02_season_score.csv`
- `database/11_temperature/01_season_rules.csv` (reference)
- `database/14_pattern/06_pattern_conditions.csv` (season conditions)

---

# 7. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 51 objects validated
- Golden examples: 6
- Test cases: 5

---

# 8. Pipeline

```
Calendar → Bazi → Season Engine → Strength Engine → Temperature Engine
```

---

# 9. References

- `knowledge/rule_database/01_strength_rules/` (canonical pattern)
- `RULE_MODEL_SPEC.md`
- `RULE_SCHEMA_REFERENCE.md`
