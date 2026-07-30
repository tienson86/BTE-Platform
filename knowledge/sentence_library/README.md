# BTE Sentence Library Framework

**Module:** Knowledge Sentence Library  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Frozen modules (not modified by this framework):

- Governance V1.0
- Reference Library
- Terminology Framework
- Knowledge Canon Framework
- Rule Database Framework

---

## Purpose

The Sentence Library Framework defines the architecture, standards, templates, and domain scaffolding for BTE interpretation sentences that consume Knowledge and Rule assets.

This release is **framework only**. It does not author interpretation sentences or academic content.

---

## Scope

In scope:

- Framework documentation
- Domain directories and templates
- Mapping, traceability, review, and quality standards
- Registry scaffolding

Out of scope:

- Writing interpretation sentences
- Academic doctrine content
- Runtime sentence engines
- Changes to frozen Knowledge Infrastructure modules

---

## Directory Structure

```
knowledge/sentence_library/
├── README.md
├── SENTENCE_LIBRARY_SPEC.md
├── SENTENCE_TEMPLATE.md
├── SENTENCE_MAPPING_STANDARD.md
├── SENTENCE_TRACEABILITY_SPEC.md
├── SENTENCE_REVIEW_GUIDE.md
├── SENTENCE_QUALITY_STANDARD.md
├── CHANGELOG.md
├── EDGE_CASES.md
├── 01_strength/
├── 02_five_elements/
├── 03_heavenly_stems/
├── 04_earthly_branches/
├── 05_ten_gods/
├── 06_patterns/
├── 07_useful_gods/
├── 08_combinations/
├── 09_temperature/
├── 10_shensha/
├── 11_luck_cycles/
├── 12_special_cases/
└── registry/
```

Each domain contains `README.md`, `INDEX.md`, and `SENTENCE_TEMPLATE.md`.

---

## Sentence ID Format

```
SEN-000001
SEN-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- Domain is metadata, not part of the ID string.

This aligns with Governance Sentence ID prefix `SEN-` without modifying Governance documents.

---

## Mandatory Sentence Support

Every sentence record MUST support:

| Field / Concern | Description |
|-----------------|-------------|
| Metadata | Administrative metadata block |
| Category | Classification label |
| Tone | Communicative tone |
| Style | Stylistic register |
| Language | Language of the sentence template |
| Variables | Placeholder variables |
| Conditions | When the sentence may apply |
| Knowledge Links | `KNO-*` IDs |
| Rule Links | `RUL-*` / rule IDs |
| Reference Links | `REF-*` IDs |
| Confidence | Confidence level |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace level / notes |

---

## Domains

| # | Directory | Domain |
|---|-----------|--------|
| 01 | `01_strength/` | Strength |
| 02 | `02_five_elements/` | Five Elements |
| 03 | `03_heavenly_stems/` | Heavenly Stems |
| 04 | `04_earthly_branches/` | Earthly Branches |
| 05 | `05_ten_gods/` | Ten Gods |
| 06 | `06_patterns/` | Patterns |
| 07 | `07_useful_gods/` | Useful Gods |
| 08 | `08_combinations/` | Combinations |
| 09 | `09_temperature/` | Temperature |
| 10 | `10_shensha/` | ShenSha |
| 11 | `11_luck_cycles/` | Luck Cycles |
| 12 | `12_special_cases/` | Special Cases |

---

## Related Documents

| Document | Role |
|----------|------|
| [SENTENCE_LIBRARY_SPEC.md](SENTENCE_LIBRARY_SPEC.md) | Formal specification |
| [SENTENCE_TEMPLATE.md](SENTENCE_TEMPLATE.md) | Root sentence template |
| [SENTENCE_MAPPING_STANDARD.md](SENTENCE_MAPPING_STANDARD.md) | Cross-mapping rules |
| [SENTENCE_TRACEABILITY_SPEC.md](SENTENCE_TRACEABILITY_SPEC.md) | Traceability rules |
| [SENTENCE_REVIEW_GUIDE.md](SENTENCE_REVIEW_GUIDE.md) | Review procedure |
| [SENTENCE_QUALITY_STANDARD.md](SENTENCE_QUALITY_STANDARD.md) | Quality rules |
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
Sentence Library (SEN-*)
        ↓
Interpretation / Report
```
