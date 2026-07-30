# BTE Rule Database Framework

**Module:** Knowledge Rule Database  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Frozen modules (not modified by this framework):

- Governance V1.0
- Reference Library
- Terminology Framework
- Knowledge Canon Framework
- Existing operational rule packs under `knowledge/rule_database/*_rules/`

---

## Purpose

The Rule Database Framework defines the architecture, standards, templates, and domain scaffolding for BTE executable and documentary rules that consume Knowledge Canon assets.

This release is **framework only**. It does not author rule content, academic explanations, or JSON rule payloads.

---

## Scope

In scope:

- Framework documentation
- Domain directories and templates
- Mapping, traceability, review, and quality standards
- Registry scaffolding

Out of scope:

- Creating actual rules
- Extracting doctrine into rule conditions
- Modifying existing `*_rules/` operational modules
- Runtime engine implementation
- Changes to frozen Knowledge Infrastructure modules

---

## Coexistence Note

This repository already contains operational rule modules such as:

- `01_strength_rules/`
- `02_season_rules/`
- `03_temperature_rules/`
- …

Those modules remain frozen and untouched.

This framework adds parallel domain scaffolding:

- `01_strength/`
- `02_season/`
- …

and root framework documents. Future content phases may align or migrate deliberately; this phase does not rewrite existing packs.

---

## Directory Structure

```
knowledge/rule_database/
├── README.md
├── RULE_DATABASE_SPEC.md
├── RULE_TEMPLATE.md
├── RULE_MAPPING_STANDARD.md
├── RULE_TRACEABILITY_SPEC.md
├── RULE_REVIEW_GUIDE.md
├── RULE_QUALITY_STANDARD.md
├── CHANGELOG.md
├── EDGE_CASES.md
├── 01_strength/
├── 02_season/
├── 03_temperature/
├── 04_patterns/
├── 05_useful_gods/
├── 06_ten_gods/
├── 07_combinations/
├── 08_clashes/
├── 09_transformations/
├── 10_shensha/
├── 11_luck_cycles/
├── 12_special_cases/
└── registry/
```

Each framework domain contains `README.md`, `INDEX.md`, and `RULE_TEMPLATE.md`.

---

## Rule ID Format

```
RUL-000001
RUL-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- Domain is metadata, not part of the ID string.

Governance V1.0 examples such as `RID-STR-00125` remain compatible via metadata notes; Governance files are not modified.

---

## Domains

| # | Directory | Domain |
|---|-----------|--------|
| 01 | `01_strength/` | Strength |
| 02 | `02_season/` | Season |
| 03 | `03_temperature/` | Temperature |
| 04 | `04_patterns/` | Patterns |
| 05 | `05_useful_gods/` | Useful Gods |
| 06 | `06_ten_gods/` | Ten Gods |
| 07 | `07_combinations/` | Combinations |
| 08 | `08_clashes/` | Clashes |
| 09 | `09_transformations/` | Transformations |
| 10 | `10_shensha/` | ShenSha |
| 11 | `11_luck_cycles/` | Luck Cycles |
| 12 | `12_special_cases/` | Special Cases |

---

## Related Documents

| Document | Role |
|----------|------|
| [RULE_DATABASE_SPEC.md](RULE_DATABASE_SPEC.md) | Formal specification |
| [RULE_TEMPLATE.md](RULE_TEMPLATE.md) | Root rule template |
| [RULE_MAPPING_STANDARD.md](RULE_MAPPING_STANDARD.md) | Cross-mapping rules |
| [RULE_TRACEABILITY_SPEC.md](RULE_TRACEABILITY_SPEC.md) | Traceability rules |
| [RULE_REVIEW_GUIDE.md](RULE_REVIEW_GUIDE.md) | Review procedure |
| [RULE_QUALITY_STANDARD.md](RULE_QUALITY_STANDARD.md) | Quality rules |
| [EDGE_CASES.md](EDGE_CASES.md) | Edge cases |
| [CHANGELOG.md](CHANGELOG.md) | Module history |
| [registry/](registry/) | Central registry scaffolding |

---

## Architecture Position

```
Reference Library (REF-*)
        ↓
Terminology (TERM-*)
        ↓
Knowledge Canon (KNO-*)
        ↓
Rule Database (RUL-*)
        ↓
Sentence / Interpretation / Report
```
