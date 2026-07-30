# Reference Library Specification

**Document:** REFERENCE_SPEC  
**Module:** knowledge/references  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

This specification defines the structure, identifiers, metadata, lifecycle, and cross-reference rules for the BTE Reference Library.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are interpreted as requirements for Reference Library authors and maintainers.

---

## 3. Design Principles

1. **Traceability** — Every cited source is addressable by `REF-NNNNNN`.
2. **Single record** — One work (or defined edition family) has one official ID.
3. **Metadata first** — Bibliographic identity precedes academic body text.
4. **Immutability of IDs** — Published IDs never change.
5. **Separation from Governance** — Library content lives under `knowledge/references/`; Governance remains frozen.
6. **No runtime coupling** — This module is documentation and registry only.

---

## 4. Reference ID

### 4.1 Format

```
REF-<6-digit-number>
```

Examples:

```
REF-000001
REF-000002
```

### 4.2 Rules

- Numbers SHALL be unique within the Reference Library.
- Numbers SHALL be allocated monotonically via `REFERENCE_INDEX.md`.
- Reuse of retired IDs is prohibited.
- Category MUST NOT be encoded in the ID string.

### 4.3 Governance Compatibility

Governance V1.0 describes category-prefixed examples (for example `REF-CLASSIC-0001`).

This library uses sequential `REF-NNNNNN` IDs as the **catalog primary key**.

Compatibility SHALL be maintained by:

- Storing Governance category code in `category` / `category_code` metadata
- Recording optional `governance_alias` if a dual label is required later
- Never editing frozen Governance documents to force ID format changes

---

## 5. Mandatory Metadata Schema

Every reference record SHALL include the following fields.

| Field | Type | Required |
|-------|------|----------|
| Reference ID | string (`REF-NNNNNN`) | Yes |
| Title | string | Yes |
| Chinese Title | string | Yes (may be `N/A`) |
| English Title | string | Yes |
| Vietnamese Title | string | Yes (may be `N/A`) |
| Author | string | Yes (may be `Traditional attribution` / `Unknown`) |
| Dynasty | string | Yes (may be `N/A`) |
| School | string | Yes (may be `Unspecified`) |
| Language | string | Yes |
| Category | enum | Yes |
| Reliability | enum | Yes |
| Edition | string | Yes (may be `Unspecified`) |
| Translator | string | Yes (may be `N/A`) |
| Publisher | string | Yes (may be `N/A`) |
| ISBN | string | Yes (may be `N/A`) |
| Year | string | Yes (may be `Unspecified`) |
| Status | enum | Yes |
| Version | string (`V#.#.#`) | Yes |
| License | string | Yes |
| Keywords | list | Yes (may be empty list noted as `None`) |
| Summary | string | Yes (placeholder allowed) |
| Related References | list of REF IDs | Yes (may be empty) |
| Related Knowledge | list of Knowledge IDs | Yes (may be empty) |
| Related Rules | list of Rule IDs | Yes (may be empty) |
| Related Sentences | list of Sentence IDs | Yes (may be empty) |

---

## 6. Controlled Enumerations

### 6.1 Category

`Classic` | `Modern` | `Paper` | `Internal`

### 6.2 Status

`Draft` | `Review` | `Official` | `Deprecated` | `Placeholder`

### 6.3 Reliability

`Primary` | `Secondary` | `Tertiary` | `Unverified` | `Internal`

### 6.4 Language (examples)

`Classical Chinese` | `Modern Chinese` | `Vietnamese` | `English` | `Bilingual` | `Other`

---

## 7. Document Structure

Each reference Markdown file SHOULD contain:

1. Title heading
2. Metadata table (all mandatory fields)
3. Summary placeholder
4. Structural outline placeholders (not full academic content)
5. Related-links section
6. Revision history

Category templates under `classics/`, `modern/`, `papers/`, and `internal/` are normative for new records.

---

## 8. Directory Rules

| Path | Content |
|------|---------|
| `classics/` | Classical references |
| `modern/` | Modern books |
| `papers/` | Papers / journals |
| `internal/` | Internal references |
| `mapping/` | Cross-reference JSON registries |
| Root | Module README, index, spec, guides, YAML catalog |

---

## 9. Mapping Framework

Cross-references SHALL be recorded in:

- Reference document Related-* fields
- `mapping/*.json` registries

Registries are authoritative for bulk lookup; document fields are authoritative for human review.

Conflict rule: if document and JSON disagree, the document wins until the registry is reconciled in the next patch.

---

## 10. Lifecycle

```
Placeholder / Draft
        ↓
     Review
        ↓
    Official
        ↓
   Deprecated (optional)
```

Transitions SHOULD follow Governance Reference Registration procedures without modifying Governance V1.0 files.

---

## 11. Prohibitions

Authors MUST NOT:

- Modify `knowledge/governance/`
- Duplicate Reference IDs
- Replace published expected Golden Dataset content via this module
- Treat placeholder summaries as verified academic conclusions
- Embed executable code in reference records

---

## 12. Acceptance Criteria

A Reference Library V1.0 framework release is accepted when:

- [ ] Directory structure matches the module README
- [ ] Seed classics REF-000001–REF-000010 exist with metadata tables
- [ ] Templates and indexes exist for all categories
- [ ] Mapping JSON skeletons exist
- [ ] `REFERENCE_METADATA.yaml` lists seed IDs
- [ ] No Governance files were changed
