# MODULE_SPEC.md — Follow Pattern Rule Database

> Module: 06_follow_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Follow Pattern Rule Database: Tòng Cách detection, validation, override resolution, and fallback behavior.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| True follow patterns (6 types) | Primary pattern matching (see 04_pattern_rules) |
| Pseudo-follow detection | Special case logic (see 05_special_case_rules) |
| Follow eligibility and thresholds | Useful god selection |
| Follow maintenance and break | Report formatting |
| Season confirmation | |
| Special case interaction | |
| Priority ordering | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| true_follow | 6 |
| pseudo_follow | 5 |
| follow_eligibility | 6 |
| follow_maintenance | 4 |
| follow_break | 5 |
| follow_conversion | 4 |
| season_confirmation | 4 |
| strength_threshold | 4 |
| special_case_interaction | 4 |
| priority_ordering | 7 |
| fallback_behavior | 2 |

**Total rules:** 51

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01_strength_rules`, `02_season_rules`, `03_temperature_rules`, `04_pattern_rules`, `05_special_case_rules`
- **used_by:** `07_combination_rules`, Useful God Engine
- **execution_order:** Pattern → Special Case → Follow Pattern → Combination

---

# 5. Configuration

| Key | Value |
|-----|-------|
| weak_support_ratio | 0.25 |
| strong_support_ratio | 0.70 |
| dominant_ratio_threshold | 0.50 |
| dominant_count_minimum | 2 |
| confidence_threshold | 0.65 |

---

# 6. Output

- `follow_pattern_match` — matched follow type code
- `is_true_follow` — boolean true follow confirmed
- `is_pseudo_follow` — boolean pseudo follow detected
- `follow_confidence` — 0.0–1.0

---

# 7. Data Sources

- `database/14_pattern/03_follow_pattern.csv`
- `engines/pattern_engine/calculators/follow_pattern.py`
- `knowledge/rule_database/05_special_case_rules/`

---

# 8. Validation

- Level 1–5 per `VALIDATION_STANDARD.md`
- 57 objects validated
- Golden examples: 6
- Test cases: 6

---

# 9. Design Documents

- `FOLLOW_PATTERN_TAXONOMY.md` — Complete follow pattern taxonomy
- `FOLLOW_PATTERN_DECISION_TREE.md` — Detection and resolution flow

---

# 10. References

- `knowledge/rule_database/05_special_case_rules/` (immediate upstream)
- `RULE_MODEL_SPEC.md`
