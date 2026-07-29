# MODULE_SPEC.md — Special Case Rule Database

> Module: 05_special_case_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Special Case Rule Database: edge case detection, override resolution, and fallback behavior for Bazi analysis pipeline exceptions.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Transformed edge cases | Standard pattern matching (see 04_pattern_rules) |
| Pseudo-follow overrides | Follow pattern logic (see 06_follow_pattern_rules) |
| Pattern-breaking exceptions | Strength scoring (see 01_strength_rules) |
| Seasonal exceptions | Report formatting |
| Hidden stem exceptions | |
| Clash/combine handling | |
| Priority overrides and tie-breaking | |
| Fallback behavior | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| transformed_edge | 14 |
| pseudo_follow_override | 8 |
| pattern_breaking | 9 |
| seasonal_exception | 7 |
| hidden_stem_exception | 5 |
| clash_combine | 11 |
| priority_override | 5 |
| tie_breaking | 4 |
| fallback_behavior | 3 |

**Total rules:** 66

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01_strength_rules`, `02_season_rules`, `03_temperature_rules`, `04_pattern_rules`
- **used_by:** `06_follow_pattern_rules`, Useful God Engine
- **execution_order:** Season → Strength → Temperature → Pattern → Special Case → Follow Pattern

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| confidence_threshold | 0.65 |

---

# 6. Output

- `special_case_flag` — boolean special case detected
- `matched_rules` — list of applied rule IDs
- `rejected_rules` — list of rejected rule IDs

---

# 7. Data Sources

- `database/12_strength/07_special_rules.csv`
- `database/11_temperature/07_special_rules.csv`
- `database/13_useful_god/06_special_rules.csv`
- `database/15_score_engine/02_wuxing/07_special_score.csv`
- `database/15_score_engine/03_strength/06_special_case.csv`
- `database/15_score_engine/04_ten_gods/05_special_case.csv`
- `database/15_score_engine/02_wuxing/05_clash_score.csv`

---

# 8. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 72 objects validated
- Golden examples: 6
- Test cases: 6

---

# 9. Design Documents

- `SPECIAL_CASE_TAXONOMY.md` — Complete special case taxonomy
- `SPECIAL_CASE_DECISION_TREE.md` — Detection and resolution flow

---

# 10. References

- `knowledge/rule_database/04_pattern_rules/` (immediate upstream)
- `RULE_MODEL_SPEC.md`
