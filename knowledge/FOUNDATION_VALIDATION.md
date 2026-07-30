# Knowledge Foundation Validation

**Module:** Knowledge Foundation  
**Document:** FOUNDATION_VALIDATION  
**Version:** V1.0.0  
**Status:** Official Foundation (Freeze Candidate)  

---

## 1. Purpose

Define validation coverage for the Knowledge Foundation infrastructure layer.

This document is infrastructure-only. It does not validate academic correctness of classical doctrines.

---

## 2. Validation domains

| Domain | Goal |
|--------|------|
| Reference integrity | Unique IDs, required fields, enum validity, index consistency |
| Terminology integrity | Unique term IDs, alias/abbreviation resolution |
| Citation integrity | Policy completeness; IDs cited must exist in Reference Library |
| Naming consistency | `REF-` / `TERM-` / status / category enums consistent |
| Directory consistency | Required Foundation files present |
| Cross-reference integrity | Related IDs resolve within Foundation catalogs |
| Duplicate detection | No duplicate IDs or canonical titles/terms |

---

## 3. Reference integrity

Executable:

```bash
python knowledge/references/validate_references.py
```

MUST fail on:

- Duplicate `reference_id`
- Duplicate `title_english`
- Invalid category / source_type / canonical_status
- Missing required fields
- Index entry without catalog record (or reverse)

`TODO_REVIEW` values are WARNINGS, not errors.

---

## 4. Terminology integrity

Executable:

```bash
python knowledge/terminology/validate_terminology.py
```

MUST fail on:

- Duplicate `term_id`
- Duplicate `canonical_term`
- Alias/abbreviation pointing to missing term
- Missing required glossary fields
- `related_terms` that do not resolve

---

## 5. Citation integrity

Manual + future automation checklist:

1. Citation policy documents exist
2. Knowledge Record citations (when present) use `REF-NNNNNN`
3. Cited IDs exist in `references.json`
4. Titles SHOULD match library `title_english`
5. Unverified chapters use `TODO_REVIEW`

Canon content is locked in this sprint; citation integrity for Canon is reported as observed risk only.

---

## 6. Naming consistency

| Pattern | Rule |
|---------|------|
| `REF-[0-9]{6}` | Reference IDs |
| `TERM-[0-9]{6}` | Terminology IDs |
| Status enums | draft / review / official / deprecated / placeholder / archived |
| Category (references) | classic / modern / paper / internal |

---

## 7. Directory consistency

Required Foundation paths MUST exist as listed in `FOUNDATION_DIRECTORY_TREE.md`.

Missing required files = ERROR for freeze readiness.

---

## 8. Cross-reference integrity

| From | To | Rule |
|------|----|------|
| `reference_index.json` | `references.json` | bidirectional presence |
| `aliases.json` | `glossary.json` | target term exists |
| `abbreviations.json` | `glossary.json` | target term exists |
| glossary `related_terms` | `glossary.json` | target term exists |
| citation examples | `references.json` | example IDs exist |

---

## 9. Duplicate detection

Detect duplicates for:

- `reference_id`
- `title_english` (case-insensitive)
- `term_id`
- `canonical_term` (case-insensitive)
- alias strings (SHOULD be unique)
- abbreviation strings (SHOULD be unique)

---

## 10. Freeze gate

Foundation Freeze V1.0 REQUIRES:

1. Reference validator PASS (0 errors)
2. Terminology validator PASS (0 errors)
3. Required directories/files present
4. Governance / citation foundation docs present
5. TODO_REVIEW inventory published
6. No modifications to locked modules

Academic completion of `TODO_REVIEW` fields is **not** a freeze blocker for infrastructure freeze, but blocks Official bibliographic promotion.
