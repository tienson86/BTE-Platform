# BTE Knowledge Reference Library

**Module:** `knowledge/references`  
**Version:** V1.0.0  
**Status:** Official Library Scaffold  
**Role:** Single Source of Truth for Reference IDs (`REF-NNNNNN`)

---

## Purpose

This library is the authoritative catalog of bibliographic sources cited by the Knowledge Canon and downstream modules.

Machine-readable catalogs:

- `references.json` — full reference records
- `reference_index.json` — lightweight discovery index

Normative documents:

- `REFERENCES_SPEC.md`
- `citation_style.md`
- `validation_rules.md`
- `CHANGELOG.md`

---

## Directory (V1.0 library layer)

```
knowledge/references/
├── README.md
├── REFERENCES_SPEC.md
├── references.json
├── reference_index.json
├── citation_style.md
├── validation_rules.md
├── CHANGELOG.md
└── (legacy framework docs / classics|modern|papers|internal remain for coexistence)
```

Legacy Markdown placeholders under `classics/`, `modern/`, `papers/`, and `internal/` are **not** the ID authority in V1.0.  
**Authority = `references.json`.**

---

## Initial canonical seed (V1.0)

| Reference ID | Work |
|--------------|------|
| REF-000001 | Huang Di Nei Jing |
| REF-000002 | Zhou Yi |
| REF-000003 | Yuan Hai Zi Ping |
| REF-000004 | San Ming Tong Hui |
| REF-000005 | Di Tian Sui |
| REF-000006 | Zi Ping Zhen Quan |
| REF-000007 | Qiong Tong Bao Jian |

See `REFERENCE_COVERAGE_REPORT.md` for mapping notes versus legacy placeholder IDs.

---

## Validation

```bash
python knowledge/references/validate_references.py
```

Rules: `validation_rules.md`

Reports:

- `VALIDATION_REPORT.md`
- `REFERENCE_COVERAGE_REPORT.md`
- `TODO_REVIEW.md`

---

## Non-goals

- No Knowledge Canon content edits
- No schema edits
- No Rule Database / Engine changes
- No full classical transcription
