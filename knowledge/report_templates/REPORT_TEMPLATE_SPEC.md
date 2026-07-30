# Report Template Specification

**Document:** REPORT_TEMPLATE_SPEC  
**Module:** knowledge/report_templates  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, and traceability rules for Report Template framework records.

This specification is **framework only**. No report contents are authored in V1.0.0.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for template authors and reviewers.

---

## 3. Design Principles

1. **Structure before content** — section outlines precede narrative text
2. **Sentence-backed** — report sections prefer `SEN-*` links for wording
3. **Knowledge-backed** — doctrinal claims prefer `KNO-*` / `RUL-*` grounding
4. **Audience clarity** — Audience / Language / Category are declared
5. **Version immutability** — published templates do not silently change
6. **Frozen boundaries** — do not edit completed Knowledge Infrastructure modules

---

## 4. Report Template ID

### 4.1 Format

```
RPT-<6-digit-number>
```

Examples:

```
RPT-000001
RPT-000100
```

### 4.2 Rules

- Numbers SHALL be unique within this framework catalog.
- Numbers SHALL be zero-padded to six digits.
- Published IDs are immutable.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

---

## 5. Mandatory Metadata Support

Every template MUST support:

| Field | Description |
|-------|-------------|
| Report Template ID | `RPT-NNNNNN` |
| Title | Human-readable title |
| Domain | Framework domain directory |
| Category | Classification label |
| Audience | Intended audience |
| Language | Language label |
| Structure | Ordered section outline |
| Knowledge Links | `KNO-*` IDs |
| Rule Links | `RUL-*` IDs |
| Sentence Links | `SEN-*` IDs |
| Reference Links | `REF-*` IDs |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace level / notes |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Category (examples)

`General` | `Professional` | `Thematic` | `Custom` | `Other`

### 6.3 Audience (examples)

`General Reader` | `Analyst` | `Client` | `Internal` | `Other`

### 6.4 Language (examples)

`English` | `Vietnamese` | `Chinese` | `Bilingual` | `Other`

---

## 7. ID Allocation Ranges (Reserved)

| Range | Domain |
|-------|--------|
| RPT-000001 – RPT-000099 | 01_basic |
| RPT-000100 – RPT-000199 | 02_professional |
| RPT-000200 – RPT-000299 | 03_business |
| RPT-000300 – RPT-000399 | 04_marriage |
| RPT-000400 – RPT-000499 | 05_career |
| RPT-000500 – RPT-000599 | 06_health |
| RPT-000600 – RPT-000699 | 07_children |
| RPT-000700 – RPT-000799 | 08_wealth |
| RPT-000800 – RPT-000899 | 09_luck_cycles |
| RPT-000900 – RPT-000999 | 10_custom |
| RPT-001000+ | Future expansion |

No Report Template IDs are allocated in framework V1.0.0.

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

---

## 9. Prohibitions

Authors MUST NOT:

- Modify frozen Knowledge Infrastructure modules
- Create report narrative contents in this framework phase
- Invent fake Knowledge / Rule / Sentence / Reference IDs
- Duplicate Report Template IDs

---

## 10. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All 10 domains contain README / INDEX / REPORT_TEMPLATE
- [ ] Registry scaffolding exists
- [ ] No report contents created
- [ ] Frozen modules untouched
