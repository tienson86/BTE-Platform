# CHANGELOG

> Module: 02_season_rules
>
> Version: 1.0.0
>
> BTE Platform

---

## [1.0.0] - 2026-07-29

### Added

Complete Season Rule Database module.

Files:

```
README.md
MODULE_SPEC.md
CHANGELOG.md
MANIFEST.json
RULE_INDEX.json
STATISTICS.json
season_rules.json
season_examples.json
TEST_CASES.json
validation_report.json
```

Rule dataset:

- 46 rules (SEA-000001 to SEA-000046)
- 4 season classification rules
- 12 season phase rules
- 18 element affinity rules
- 8 solar term rules
- 4 priority rules

Golden examples: 6 | Test cases: 5

### Governance

- Origin: `rule_database`
- Schema version: `1.0.0`
- Validation Level 1–5: 51 objects, 0 errors
- Derived from `database/15_score_engine/02_wuxing/02_season_score.csv`

---

## Version Policy

| Level | When |
|-------|------|
| MAJOR | Breaking schema change |
| MINOR | New rules |
| PATCH | Metadata or documentation |
