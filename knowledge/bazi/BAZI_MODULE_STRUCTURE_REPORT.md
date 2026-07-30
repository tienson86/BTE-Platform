# BaZi Blueprint — Module Structure Report

**Sprint:** BaZi Knowledge Blueprint V1.0  
**Date:** 2026-07-31  
**Path:** `knowledge/bazi/`

---

## Summary

| Metric | Value |
|--------|-------|
| Modules required | 14 |
| Modules present | 14 |
| Standard files per module | 9 (+ reserved dirs) |
| Academic records in `knowledge_records/` | **0** |

---

## Module inventory

| Module | Title | Structure |
|--------|-------|-----------|
| `01_fundamental_knowledge` | Fundamental Knowledge | Complete |
| `02_strength_knowledge` | Strength Knowledge | Complete |
| `03_temperature_knowledge` | Temperature Knowledge | Complete |
| `04_pattern_knowledge` | Pattern Knowledge | Complete |
| `05_useful_god_knowledge` | Useful God Knowledge | Complete |
| `06_ten_gods_knowledge` | Ten Gods Knowledge | Complete |
| `07_combination_knowledge` | Combination Knowledge | Complete |
| `08_shensha_knowledge` | Shensha Knowledge | Complete |
| `09_luck_knowledge` | Luck Knowledge | Complete |
| `10_marriage_knowledge` | Marriage Knowledge | Complete |
| `11_career_knowledge` | Career Knowledge | Complete |
| `12_wealth_knowledge` | Wealth Knowledge | Complete |
| `13_health_knowledge` | Health Knowledge | Complete |
| `14_children_knowledge` | Children Knowledge | Complete |

---

## Per-module standard layout

Each module includes:

```
README.md
MODULE_SPEC.md
FIELD_GUIDE.md
validation.md
CHANGELOG.md
knowledge_records/README.md   # reserved; no academic JSON
examples/example_record.json
examples/template_record.json
docs/README.md
```

Root also includes:

- `knowledge/bazi/README.md`
- `knowledge/bazi/CHANGELOG.md`
- Blueprint reports

---

## Locked modules (untouched)

- Foundation (`references`, `terminology`, `citation_rules`, `governance`)
- `knowledge/schema`
- `knowledge/knowledge_canon`
- `knowledge/rule_database`
