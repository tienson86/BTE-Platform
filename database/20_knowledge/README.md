# Classical Knowledge Base (Epic 03)

Version: **0.3.0** (Wave 1.1 frozen · Domain 01 P0 authored)

Path: `database/20_knowledge/`

This folder holds the **classical / commercial BaZi knowledge corpus**.

It is **not** a calculation rule database.

- Calculation engines continue to use `database/11_temperature` … `15_score_engine` and related folders.
- Interpretation engines continue to use `database/interpretation_rules/`.
- This corpus stores explainable classical / modern knowledge entries for retrieval and citation.

---

## Files

### Legacy topic files (schema `01`–`20`)

| File | Topic | Content rows |
|------|--------|-------------:|
| `01_five_elements.csv` … `20_glossary.csv` | Topic families | 0 (headers only) |

Schema (stable — do not reorder):

```text
id,topic,keyword,condition,classical_text,modern_interpretation,priority,confidence,reference
```

### Commercial Knowledge Units (Wave 1.1+)

| File | Purpose |
|------|---------|
| `21_knowledge_units.csv` | Wave 1.1 Golden Baseline cores (**frozen** — 5 units) |
| `22_domain01_career_business.csv` | Domain 01 Career & Business **P0** (4 units) |

Wave 1.1 contains **exactly five** units: `KU-ID-001`, `KU-ST-001`, `KU-WK-001`, `KU-UG-001`, `KU-RC-001`.

Domain 01 P0/Sprint C Career Selection contains SEL units in `22_domain01_career_business.csv` (`CAP-D1-CA-SEL`, wave `W-D01-C-SEL`) plus retained light LE/BU P0 rows.

Supporting docs:

| File | Purpose |
|------|---------|
| `README.md` | This document |
| `CHANGELOG.md` | Version history |
| `COVERAGE.md` | Coverage report |

---

## Pipeline position

```text
RuleContext (from engines)
        ↓
Knowledge Retriever  ←  database/20_knowledge/  (future wiring)
        ↓
Evidence + Interpretation + Narrative
```

Wave 1.1 **authors content only** — no engine/runtime changes.

---

## Compatibility

- Existing `01`–`20` column order unchanged.
- `21_knowledge_units.csv` is additive.
- No calculation engine imports required for this wave.
