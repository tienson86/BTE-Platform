# Terminology Specification

**Document:** TERMINOLOGY_SPEC  
**Module:** knowledge/terminology  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, and cross-link rules for the BTE Terminology Framework.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for terminology authors and reviewers.

---

## 3. Design Principles

1. **One term, one ID**
2. **Multilingual identity**
3. **Definition before usage examples**
4. **Immutable published IDs**
5. **Domain-scoped organization**
6. **Traceability to References, Knowledge, Rules, and Sentences**
7. **No runtime coupling** — documentation framework only
8. **Frozen boundaries** — do not edit Governance or Reference Framework

---

## 4. Terminology ID

### 4.1 Format

```
TERM-<6-digit-number>
```

Examples:

```
TERM-000001
TERM-000100
```

### 4.2 Rules

- Numbers SHALL be unique.
- Allocation SHALL follow `TERMINOLOGY_INDEX.md` ranges.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

### 4.3 Governance Compatibility

Governance V1.0 describes Glossary IDs such as `GLS-…`.

This framework uses `TERM-NNNNNN` as catalog primary keys.

Optional later dual-labeling MAY be recorded in metadata notes without modifying Governance files.

---

## 5. Mandatory Metadata Schema

| Field | Required | Notes |
|-------|----------|-------|
| ID | Yes | `TERM-NNNNNN` |
| Chinese | Yes | May be `N/A` only if non-Chinese origin explicitly justified |
| Traditional Chinese | Yes | May equal Chinese or `N/A` |
| Simplified Chinese | Yes | May equal Chinese or `N/A` |
| Vietnamese | Yes | May be `N/A` |
| English | Yes | Official English label |
| Definition | Yes | Placeholder allowed only while Status = Placeholder |
| Aliases | Yes | Empty list allowed |
| Category | Yes | Controlled label |
| Domain | Yes | Must match directory domain |
| School | Yes | May be `Unspecified` |
| Usage | Yes | Placeholder allowed in framework stubs |
| Examples | Yes | Empty allowed |
| Related Terms | Yes | Empty allowed |
| References | Yes | Empty allowed; prefer `REF-*` |
| Knowledge Assets | Yes | Empty allowed |
| Rules | Yes | Empty allowed |
| Sentences | Yes | Empty allowed |
| Version | Yes | `V#.#.#` |
| Status | Yes | Controlled enum |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Domain

Must equal one of the framework domain directory names (snake_case) or the human domain label defined in README.

### 6.3 Category (examples)

`Core` | `Technical` | `Doctrinal` | `Operational` | `Deprecated Alias` | `Other`

---

## 7. Document Structure

Each term record SHOULD contain:

1. Title (English preferred)
2. Metadata table (all mandatory fields)
3. Definition section
4. Usage / Examples sections
5. Related links
6. Revision history

Root and domain templates are normative for new records.

---

## 8. Lifecycle

```
Placeholder / Draft
        ↓
     Review
        ↓
    Official
        ↓
   Deprecated (optional)
```

Transitions SHOULD follow Governance Terminology Registration procedures without editing frozen Governance documents.

---

## 9. Prohibitions

Authors MUST NOT:

- Modify Governance V1.0
- Modify Reference Framework documents
- Duplicate Terminology IDs
- Publish Official terms with empty Definition
- Invent fake Reference / Rule / Sentence IDs
- Add implementation code to this module

---

## 10. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All domain directories contain README / INDEX / TEMPLATE
- [ ] No term content records allocated
- [ ] ID policy documented
- [ ] Governance and Reference boundaries respected
