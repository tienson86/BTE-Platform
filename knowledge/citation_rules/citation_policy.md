# Citation Policy

**Module:** `knowledge/citation_rules`  
**Document:** citation_policy  
**Version:** V1.0.0  
**Status:** Official Foundation (Freeze Candidate)  

---

## 1. Reference IDs

Every bibliographic citation in Official Knowledge Records MUST use a Reference ID:

```text
REF-NNNNNN
```

Rules:

1. IDs are allocated only in `knowledge/references/references.json`
2. Do not invent Reference IDs in Canon or Rule files
3. Do not cite by title alone in Official records
4. Deprecated Reference IDs MUST NOT be newly cited

---

## 2. Citation format

Preferred human-readable form:

```text
<title_english> (<title_original>), <reference_id>
```

Example:

```text
Yuan Hai Zi Ping (淵海子平), REF-000003
```

Short form (space-constrained UI):

```text
<title_english> [<reference_id>]
```

---

## 3. How Knowledge Records cite References

Knowledge Records SHALL store citations as structured objects:

```json
{
  "reference_id": "REF-000003",
  "title": "Yuan Hai Zi Ping",
  "chapter": "TODO_REVIEW",
  "notes": "TODO_REVIEW"
}
```

Rules:

| Field | Rule |
|-------|------|
| `reference_id` | Required; MUST exist in Reference Library |
| `title` | SHOULD match library `title_english` |
| `chapter` | Optional; use `TODO_REVIEW` if unverified |
| `notes` | Optional; no interpretive claims without review |

Multiple citations are allowed as an array under `references`.

---

## 4. Validation requirements

1. Every `reference_id` MUST resolve in `references.json`
2. Title mismatch against the library is a WARNING
3. Missing `reference_id` in Official status records is an ERROR
4. `TODO_REVIEW` chapter/notes are allowed in `draft` / `review`
5. Invented IDs are an ERROR
6. Citation examples in this module MUST use existing seed IDs

Executable companion checks: `knowledge/FOUNDATION_VALIDATION.md`.

---

## 5. Citation lifecycle

```text
Draft citation
    ↓
Technical check (ID exists, shape valid)
    ↓
Academic Review (chapter/notes accuracy)
    ↓
Official citation
    ↓
(optional) Deprecated if Reference ID deprecated
```

| Record / citation status | Requirement |
|--------------------------|-------------|
| draft | Reference IDs SHOULD exist; unresolved IDs flagged |
| review | All cited IDs MUST exist |
| official | All cited IDs MUST exist and SHOULD be non-deprecated |
| deprecated / archived | Existing citations frozen; no new unverified IDs |

---

## 6. Reference usage (non-interpretive)

Allowed uses of Reference IDs:

- Knowledge Record `references` arrays
- Traceability tables
- Report bibliography lines
- Registry / mapping documents that point to bibliographic sources

Disallowed:

- Using a Reference ID as a Rule ID or Knowledge ID
- Encoding school or doctrine inside the ID string
- Silent remapping of an Official ID to a different work

---

## 7. Ownership

- Reference Library owners allocate IDs
- Knowledge authors cite allocated IDs
- Technical Reviewers verify ID resolution and title alignment
- Academic Reviewers approve chapter anchors and interpretive notes

---

## 8. Related documents

- `citation_examples.md`
- `knowledge/references/citation_style.md`
- `knowledge/FOUNDATION_VALIDATION.md`
