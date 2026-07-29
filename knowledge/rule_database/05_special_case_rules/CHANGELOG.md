# CHANGELOG

> Module: 05_special_case_rules
>
> Version: 1.0.0
>
> BTE Platform

---

## [1.0.0] - 2026-07-29

### Added

Complete Special Case Rule Database module.

Files:

```
README.md
MODULE_SPEC.md
SPECIAL_CASE_TAXONOMY.md
SPECIAL_CASE_DECISION_TREE.md
DEPENDENCIES.json
CHANGELOG.md
MANIFEST.json
RULE_INDEX.json
STATISTICS.json
special_case_rules.json
special_case_examples.json
TEST_CASES.json
validation_report.json
```

Rule dataset:

- 66 rules (SPC-000001 to SPC-000066)
- Transformed edge: 14 rules
- Pseudo-follow override: 8 rules
- Pattern breaking: 9 rules
- Seasonal exception: 7 rules
- Hidden stem exception: 5 rules
- Clash/combine: 11 rules
- Priority override: 5 rules
- Tie-breaking: 4 rules
- Fallback: 3 rules

### Dependencies

- depends_on: `01_strength_rules`, `02_season_rules`, `03_temperature_rules`, `04_pattern_rules`
- used_by: `06_follow_pattern_rules`, Useful God Engine

### Validation

- 72 objects, 0 errors
- Coverage: 100% families complete

---

## Version Policy

| Level | When |
|-------|------|
| MAJOR | Breaking schema |
| MINOR | New rules |
| PATCH | Metadata fix |
