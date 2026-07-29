# MODULE_SPEC.md — Pattern Rule Database

> Module: 04_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Pattern Rule Database: standard, transformed, follow, pseudo-follow, broken, mixed, and exceptional pattern recognition with eligibility gates, conflict resolution, and priority groups.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Main pattern (Lệnh Tháng) | Strength month command (see 01_strength_rules) |
| Special/transformed patterns | Temperature scoring (see 03_temperature_rules) |
| Follow and pseudo-follow patterns | Useful god selection |
| Combination and mixed patterns | Report formatting |
| Broken and exceptional patterns | |
| Eligibility conditions | |
| Conflict resolution and priority | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| main_pattern | 11 |
| special_pattern | 5 |
| follow_pattern | 6 |
| combination_pattern | 5 |
| conflict_resolution | 7 |
| pseudo_follow | 4 |
| broken_pattern | 5 |
| mixed_pattern | 4 |
| exceptional_pattern | 4 |
| eligibility_condition | 10 |
| group_priority | 7 |

**Total rules:** 68

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01_strength_rules`, `02_season_rules`, `03_temperature_rules`
- **used_by:** `05_flow_rules`, Useful God Engine
- **execution_order:** Season → Strength → Temperature → Pattern → Flow

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| confidence_threshold | 0.65 |
| main_patterns | 10 |

---

# 6. Output

Pattern classification:

- `primary_pattern` — matched pattern code
- `pattern_quality` — intact | broken | mixed
- `confidence` — 0.0–1.0

---

# 7. Data Sources

- `database/14_pattern/01_main_pattern.csv`
- `database/14_pattern/02_special_pattern.csv`
- `database/14_pattern/03_follow_pattern.csv`
- `database/14_pattern/04_combination_pattern.csv`
- `database/14_pattern/05_priority_rules.csv`
- `database/14_pattern/06_pattern_conditions.csv`
- `database/14_pattern/07_pattern_examples.csv`

---

# 8. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 74 objects validated
- Golden examples: 6
- Test cases: 6

---

# 9. Design Documents

- `PATTERN_TAXONOMY.md` — Complete pattern taxonomy
- `PATTERN_DECISION_TREE.md` — Recognition and conflict resolution flow

---

# 10. References

- `knowledge/rule_database/01_strength_rules/` (canonical pattern)
- `knowledge/rule_database/02_season_rules/`
- `knowledge/rule_database/03_temperature_rules/`
- `RULE_MODEL_SPEC.md`
