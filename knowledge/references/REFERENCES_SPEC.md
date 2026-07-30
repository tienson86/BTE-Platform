# Knowledge References Specification

> **Document ID:** REF-LIB-SPEC-001  
> **Module:** `knowledge/references`  
> **Version:** V1.0.0  
> **Status:** Official  
> **Document Type:** Library Specification  

---

# 1. Purpose

This specification defines the official Knowledge Reference Library for the BTE Platform.

The library is the Single Source of Truth for every `REF-NNNNNN` identifier used by Knowledge Canon, Rules, Sentences, and Reports.

---

# 2. Scope

In scope:

- Reference identity and bibliographic metadata
- Machine-readable catalogs (`references.json`, `reference_index.json`)
- Citation style and validation rules
- Initial classical seed set

Out of scope:

- Knowledge Record authorship
- Rule / Interpretation / Scoring logic
- Schema modification
- Engine implementation

---

# 3. Identifier Standard

Format:

```text
REF-NNNNNN
```

Rules:

- Globally unique within the platform
- Immutable after publication
- Zero-padded to six digits
- Allocated only through this library

---

# 4. Record Model

Each record in `references.json` SHALL include:

| Field | Requirement |
|-------|-------------|
| `reference_id` | Required, unique |
| `title_original` | Required |
| `title_english` | Required |
| `author` | Required (may be `TODO_REVIEW` / `Traditional attribution`) |
| `dynasty` | Required (may be `TODO_REVIEW`) |
| `estimated_year` | Required (may be `TODO_REVIEW`) |
| `category` | Required; enum below |
| `school` | Required (may be `TODO_REVIEW`) |
| `language` | Required |
| `source_type` | Required; enum below |
| `canonical_status` | Required; enum below |
| `description` | Required |
| `citation_format` | Required |
| `identifier` | Required (ISBN or other identifier; may be `TODO_REVIEW` / `N/A`) |
| `publisher` | Required (may be `TODO_REVIEW` / `N/A`) |
| `edition` | Required (may be `TODO_REVIEW` / `N/A`) |
| `volume` | Required (may be `TODO_REVIEW` / `N/A`) |
| `chapter_support` | Required array (may be empty) |
| `notes` | Required (may be empty string) |
| `keywords` | Required array |
| `related_modules` | Required array |

---

# 5. Enumerations

## category

- `classic`
- `modern`
- `paper`
- `internal`

## source_type

- `classical_text`
- `commentary`
- `modern_book`
- `journal_article`
- `internal_document`

## canonical_status

- `draft`
- `review`
- `official`
- `deprecated`
- `placeholder`

---

# 6. Index Model

`reference_index.json` entries SHALL include:

- `reference_id`
- `title`
- `category`
- `keywords`
- `related_modules`

The index is a derived discovery view. `references.json` remains authoritative.

---

# 7. Authority Rules

1. If `references.json` and a legacy Markdown placeholder disagree, **`references.json` wins**.
2. Knowledge Records MUST cite IDs that exist in `references.json` before Official publication.
3. Uncertain bibliographic facts MUST use `TODO_REVIEW` rather than invented values.

---

# 8. Validation

Validators SHALL enforce `validation_rules.md`.

---

# 9. Extensibility

New references are added by:

1. Allocating the next free `REF-NNNNNN`
2. Appending to `references.json`
3. Refreshing `reference_index.json`
4. Running validation
5. Updating `CHANGELOG.md`
