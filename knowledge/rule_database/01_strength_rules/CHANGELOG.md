# CHANGELOG

> Module: 01_strength_rules
>
> Version: 1.0.0
>
> BTE Platform

---

## [1.0.0] - 2026-07-29

### Added

Initial Strength Rule Database module.

Files:

```
README.md
CHANGELOG.md
MANIFEST.json
strength_rules.json
strength_examples.json
validation_report.json
```

Rule dataset:

- 45 rules (STR-000001 to STR-000045)
- 8 categories: season, root, support, control, drain, special, combination, priority
- Normalization config: baseline, scale, strong/weak thresholds

Golden examples:

- 5 chart scenarios (ex_001 to ex_005)

### Governance

- Origin: `rule_database`
- Schema version: `1.0.0`
- Validation Level 1–5 applied
- Derived from `database/12_strength/` CSV source
- Aligned with Knowledge Framework Rule Model

### Validation

- 47 objects validated (2 module files + 45 rules)
- 0 errors, 0 warnings, 0 fatal

---

## Version Policy

| Level | When |
|-------|------|
| MAJOR | Breaking schema or rule model change |
| MINOR | New rules or compatible fields |
| PATCH | Metadata, documentation, or correction |
