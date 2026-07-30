# BTE Golden Dataset Framework

**Module:** Knowledge Golden Dataset  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Frozen modules (not modified by this framework):

- Governance V1.0
- Reference Library
- Terminology Framework
- Knowledge Canon Framework
- Rule Database Framework
- Sentence Library Framework
- Validation Console workspace datasets
- `tests/golden_dataset/` operational fixtures

---

## Purpose

The Golden Dataset Framework defines the architecture, standards, templates, and domain scaffolding for deterministic Knowledge Infrastructure validation cases.

This release is **framework only**. It does not author actual datasets, expected outputs, or academic content.

---

## Scope

In scope:

- Framework documentation
- Domain directories and templates
- Validation, review, quality, and traceability standards
- Registry scaffolding

Out of scope:

- Creating actual golden cases
- Writing expected engine outputs
- Modifying `tests/golden_dataset/`
- Modifying frozen Knowledge Infrastructure modules
- Runtime validators / engines

---

## Directory Structure

```
knowledge/golden_dataset/
├── README.md
├── GOLDEN_DATASET_SPEC.md
├── DATASET_TEMPLATE.md
├── VALIDATION_STANDARD.md
├── TRACEABILITY_SPEC.md
├── REVIEW_GUIDE.md
├── QUALITY_STANDARD.md
├── CHANGELOG.md
├── EDGE_CASES.md
├── 01_basic/
├── 02_strength/
├── 03_patterns/
├── 04_useful_gods/
├── 05_ten_gods/
├── 06_temperature/
├── 07_combinations/
├── 08_shensha/
├── 09_luck_cycles/
├── 10_special_cases/
└── registry/
```

Each domain contains `README.md`, `INDEX.md`, and `DATASET_TEMPLATE.md`.

---

## Dataset ID Format

```
CASE-000001
CASE-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- Domain is metadata, not part of the ID string.

---

## Mandatory Dataset Support

Every golden dataset case MUST support:

| Field / Concern | Description |
|-----------------|-------------|
| Metadata | Administrative metadata block |
| Input | Input fixture |
| Expected Output | Deterministic expected result |
| Knowledge Assets | `KNO-*` links |
| Rules | `RUL-*` / rule links |
| Sentences | `SEN-*` links |
| Score | Score-related expected fields / notes |
| References | `REF-*` links |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Review | Review record / gate status |
| Traceability | Trace level / notes |

---

## Domains

| # | Directory | Domain |
|---|-----------|--------|
| 01 | `01_basic/` | Basic |
| 02 | `02_strength/` | Strength |
| 03 | `03_patterns/` | Patterns |
| 04 | `04_useful_gods/` | Useful Gods |
| 05 | `05_ten_gods/` | Ten Gods |
| 06 | `06_temperature/` | Temperature |
| 07 | `07_combinations/` | Combinations |
| 08 | `08_shensha/` | ShenSha |
| 09 | `09_luck_cycles/` | Luck Cycles |
| 10 | `10_special_cases/` | Special Cases |

---

## Related Documents

| Document | Role |
|----------|------|
| [GOLDEN_DATASET_SPEC.md](GOLDEN_DATASET_SPEC.md) | Formal specification |
| [DATASET_TEMPLATE.md](DATASET_TEMPLATE.md) | Root case template |
| [VALIDATION_STANDARD.md](VALIDATION_STANDARD.md) | Validation rules |
| [TRACEABILITY_SPEC.md](TRACEABILITY_SPEC.md) | Traceability rules |
| [REVIEW_GUIDE.md](REVIEW_GUIDE.md) | Review procedure |
| [QUALITY_STANDARD.md](QUALITY_STANDARD.md) | Quality rules |
| [EDGE_CASES.md](EDGE_CASES.md) | Edge cases |
| [CHANGELOG.md](CHANGELOG.md) | Module history |
| [registry/](registry/) | Central registry scaffolding |

---

## Architecture Position

```
Reference / Terminology / Knowledge / Rules / Sentences
                        ↓
              Golden Dataset (CASE-*)
                        ↓
         Validation / Regression / Approval
```

This Knowledge Infrastructure framework is documentary. Operational fixtures under `tests/golden_dataset/` remain separate and frozen unless a later migration task explicitly authorizes alignment.
