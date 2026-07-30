# BTE Terminology Framework

**Module:** Knowledge Terminology  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen) — not modified  
**Reference Framework:** Frozen — not modified  

---

## Purpose

The Terminology Framework is the authoritative catalog structure for official BTE terms used across the Knowledge Canon, engines, sentences, and reports.

It provides:

- Stable Terminology IDs (`TERM-NNNNNN`)
- Multilingual metadata schema
- Domain directories and templates
- Quality, review, mapping, and traceability standards
- Machine-readable Foundation catalogs (`glossary.json`, `aliases.json`, `abbreviations.json`)

Validate:

```bash
python knowledge/terminology/validate_terminology.py
```

---

## Scope

In scope:

- Framework documents
- Templates and indexes
- Quality / review / mapping / traceability standards
- Domain directory scaffolding
- Foundation JSON glossary / alias / abbreviation catalogs

Out of scope:

- Deep academic definitions (use `TODO_REVIEW` until Academic Review)
- Runtime terminology services
- Redesign of Governance architecture
- Engine implementation
- Edits to locked Canon / schema / Rule Database

---

## Directory Structure

```
knowledge/terminology/
├── README.md
├── TERMINOLOGY_INDEX.md
├── TERMINOLOGY_SPEC.md
├── TERMINOLOGY_TEMPLATE.md
├── TERMINOLOGY_REVIEW_GUIDE.md
├── TERMINOLOGY_QUALITY_STANDARD.md
├── TERMINOLOGY_MAPPING_STANDARD.md
├── TERMINOLOGY_TRACEABILITY_SPEC.md
├── CHANGELOG.md
├── EDGE_CASES.md
├── glossary.json
├── aliases.json
├── abbreviations.json
├── validate_terminology.py
├── basic/
├── heavenly_stems/
├── earthly_branches/
├── hidden_stems/
├── five_elements/
├── ten_gods/
├── strength/
├── patterns/
├── useful_gods/
├── combinations/
├── clashes/
├── punishments/
├── harms/
├── transformations/
├── shensha/
├── fortune/
├── fengshui/
├── astrology/
└── glossary/
```

Each domain directory contains `README.md`, `INDEX.md`, and `TEMPLATE.md`.

---

## Terminology ID Format

```
TERM-000001
TERM-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- One Terminology ID maps to exactly one official term record.
- Domain is stored in metadata; it is not encoded in the ID string.

---

## Mandatory Metadata

| Field | Description |
|-------|-------------|
| ID | `TERM-NNNNNN` |
| Chinese | Primary Chinese form |
| Traditional Chinese | Traditional characters |
| Simplified Chinese | Simplified characters |
| Vietnamese | Vietnamese term |
| English | English term |
| Definition | Official definition |
| Aliases | Alternate forms |
| Category | Classification label |
| Domain | Domain directory / module domain |
| School | Doctrinal school |
| Usage | Usage guidance |
| Examples | Example usages |
| Related Terms | Other `TERM-*` IDs |
| References | `REF-*` IDs |
| Knowledge Assets | Knowledge asset IDs |
| Rules | Rule IDs |
| Sentences | Sentence IDs |
| Version | Document version |
| Status | Draft / Review / Official / Deprecated / Placeholder |

---

## Domains

| Domain | Directory |
|--------|-----------|
| Basic | `basic/` |
| Heavenly Stems | `heavenly_stems/` |
| Earthly Branches | `earthly_branches/` |
| Hidden Stems | `hidden_stems/` |
| Five Elements | `five_elements/` |
| Ten Gods | `ten_gods/` |
| Strength | `strength/` |
| Patterns | `patterns/` |
| Useful Gods | `useful_gods/` |
| Combinations | `combinations/` |
| Clashes | `clashes/` |
| Punishments | `punishments/` |
| Harms | `harms/` |
| Transformations | `transformations/` |
| ShenSha | `shensha/` |
| Fortune | `fortune/` |
| Feng Shui | `fengshui/` |
| Astrology | `astrology/` |
| Glossary | `glossary/` |

---

## How to Add a Term (Later Content Phase)

1. Allocate the next free `TERM-NNNNNN` in `TERMINOLOGY_INDEX.md`.
2. Copy the domain `TEMPLATE.md`.
3. Fill all mandatory metadata fields.
4. Link References / Knowledge / Rules / Sentences as needed.
5. Follow `TERMINOLOGY_QUALITY_STANDARD.md` and `TERMINOLOGY_REVIEW_GUIDE.md`.
6. Update the domain `INDEX.md`.
7. Register through Governance Terminology Registration procedures **without editing** frozen Governance V1.0 files.

---

## Related Module Documents

| Document | Role |
|----------|------|
| [TERMINOLOGY_INDEX.md](TERMINOLOGY_INDEX.md) | Master catalog |
| [TERMINOLOGY_SPEC.md](TERMINOLOGY_SPEC.md) | Formal specification |
| [TERMINOLOGY_TEMPLATE.md](TERMINOLOGY_TEMPLATE.md) | Root term template |
| [TERMINOLOGY_REVIEW_GUIDE.md](TERMINOLOGY_REVIEW_GUIDE.md) | Review procedure |
| [TERMINOLOGY_QUALITY_STANDARD.md](TERMINOLOGY_QUALITY_STANDARD.md) | Quality rules |
| [TERMINOLOGY_MAPPING_STANDARD.md](TERMINOLOGY_MAPPING_STANDARD.md) | Cross-mapping rules |
| [TERMINOLOGY_TRACEABILITY_SPEC.md](TERMINOLOGY_TRACEABILITY_SPEC.md) | Traceability rules |
| [EDGE_CASES.md](EDGE_CASES.md) | Edge cases |
| [CHANGELOG.md](CHANGELOG.md) | Module history |

---

## Governance Compatibility

Governance V1.0 uses Glossary ID examples such as `GLS-…`.

This framework uses sequential `TERM-NNNNNN` IDs as the **Terminology Framework catalog primary key**.

Compatibility is maintained by metadata (`domain`, `category`) and review procedures — not by modifying frozen Governance documents.

---

## Frozen Boundaries

Do not modify:

- `knowledge/governance/`
- `knowledge/references/` (Reference Framework frozen)
- Completed documents outside this framework task
