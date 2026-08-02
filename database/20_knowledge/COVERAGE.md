# Coverage Report — Classical Knowledge Base

**Epic:** 03 — Knowledge & AI Expert System  
**Milestone:** 01 — Classical Knowledge Base Foundation  
**Date:** 2026-08-02  
**Database version:** 0.1.0  
**Status:** Schema only (not content-ready)

---

## Summary

| Metric | Value |
|--------|------:|
| Topic files expected | 20 |
| Topic files present | 20 |
| Schema columns per file | 9 |
| Content rows (all files) | 0 |
| Files with matching schema | 20 / 20 |
| Content coverage | 0% |
| Schema readiness | 100% |

---

## Schema checklist

Required columns (stable order):

1. `id`
2. `topic`
3. `keyword`
4. `condition`
5. `classical_text`
6. `modern_interpretation`
7. `priority`
8. `confidence`
9. `reference`

All 20 files use this exact header and contain **no data rows**.

---

## Per-file coverage

| File | Header OK | Data rows | Content status |
|------|-----------|----------:|----------------|
| `01_five_elements.csv` | yes | 0 | empty — schema only |
| `02_yin_yang.csv` | yes | 0 | empty — schema only |
| `03_ten_gods.csv` | yes | 0 | empty — schema only |
| `04_hidden_stems.csv` | yes | 0 | empty — schema only |
| `05_growth_stage.csv` | yes | 0 | empty — schema only |
| `06_nayin.csv` | yes | 0 | empty — schema only |
| `07_patterns.csv` | yes | 0 | empty — schema only |
| `08_useful_god.csv` | yes | 0 | empty — schema only |
| `09_strength.csv` | yes | 0 | empty — schema only |
| `10_temperature.csv` | yes | 0 | empty — schema only |
| `11_shensha.csv` | yes | 0 | empty — schema only |
| `12_career.csv` | yes | 0 | empty — schema only |
| `13_wealth.csv` | yes | 0 | empty — schema only |
| `14_marriage.csv` | yes | 0 | empty — schema only |
| `15_children.csv` | yes | 0 | empty — schema only |
| `16_health.csv` | yes | 0 | empty — schema only |
| `17_parents.csv` | yes | 0 | empty — schema only |
| `18_luck_cycles.csv` | yes | 0 | empty — schema only |
| `19_feng_shui.csv` | yes | 0 | empty — schema only |
| `20_glossary.csv` | yes | 0 | empty — schema only |

---

## Domain coverage (planned)

| Domain group | Files | Seeded | Notes |
|--------------|------:|-------:|-------|
| Fundamentals | 01–06 | 0 | Five elements, yin-yang, ten gods, hidden stems, growth, nayin |
| Analytical | 07–11 | 0 | Patterns, useful god, strength, temperature, shensha |
| Life domains | 12–17 | 0 | Career, wealth, marriage, children, health, parents |
| Cycles / space | 18–19 | 0 | Luck cycles, feng shui |
| Glossary | 20 | 0 | Terminology |

---

## Gaps / next milestones

1. Curate initial seed rows for high-priority topics (ten gods, shensha, useful god, five elements).
2. Bind `reference` values to `SRC-*` / `REF-*` bibliography ids.
3. Add Knowledge Expert loader + validation (duplicate `id`, missing required fields).
4. Do **not** treat 0% content coverage as a failure of Milestone 01 — schema foundation is the goal.

---

## Compatibility

- No engines read or write this folder in Milestone 01.
- Existing calculation / interpretation databases unchanged.
- Safe to add rows in later milestones without renaming columns.
