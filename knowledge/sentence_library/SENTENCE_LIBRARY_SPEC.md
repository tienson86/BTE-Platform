# Sentence Library Specification

**Document:** SENTENCE_LIBRARY_SPEC  
**Module:** knowledge/sentence_library  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, mapping, and traceability rules for Sentence Library framework records.

This specification is **framework only**. No interpretation sentences are authored in V1.0.0.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for sentence authors and reviewers.

---

## 3. Design Principles

1. **Knowledge- and rule-backed** — sentences cite Knowledge / Rules when applicable
2. **Template-first** — variables are explicit; no hidden free text coupling
3. **Tone and style controlled** — communicative register is declared
4. **Conditional applicability** — conditions state when a sentence may fire
5. **Traceability** — links to Knowledge / Rules / References
6. **Version immutability** — published sentence versions do not silently change
7. **Frozen boundaries** — do not edit completed Knowledge Infrastructure modules

---

## 4. Sentence ID

### 4.1 Format

```
SEN-<6-digit-number>
```

Examples:

```
SEN-000001
SEN-000100
```

### 4.2 Rules

- Numbers SHALL be unique within the Sentence Library catalog.
- Numbers SHALL be zero-padded to six digits.
- Published IDs are immutable.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

### 4.3 Governance Compatibility

Governance V1.0 uses Sentence ID examples such as `SEN-00412`.

This framework uses zero-padded `SEN-NNNNNN` as the **catalog primary key**, preserving the `SEN-` prefix without modifying Governance files.

---

## 5. Mandatory Metadata Support

Every sentence record MUST support:

| Field | Description |
|-------|-------------|
| Sentence ID | `SEN-NNNNNN` |
| Title | Human-readable title |
| Category | Classification label |
| Tone | Communicative tone |
| Style | Stylistic register |
| Language | Language code / label |
| Template | Sentence template text (placeholder allowed in framework stubs) |
| Variables | Placeholder variable list |
| Conditions | Applicability conditions |
| Knowledge Links | `KNO-*` IDs |
| Rule Links | `RUL-*` / rule IDs |
| Reference Links | `REF-*` IDs |
| Confidence | Confidence level |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace level / notes |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Confidence

`High` | `Medium` | `Low` | `Unverified`

### 6.3 Tone (examples)

`Neutral` | `Formal` | `Cautious` | `Supportive` | `Direct` | `Other`

### 6.4 Style (examples)

`Analytical` | `Narrative` | `Summary` | `Advisory` | `Technical` | `Other`

### 6.5 Language (examples)

`English` | `Vietnamese` | `Chinese` | `Bilingual` | `Other`

### 6.6 Category (examples)

`Overview` | `Classification` | `Explanation` | `Warning` | `Recommendation` | `Special Case` | `Other`

---

## 7. ID Allocation Ranges (Reserved)

| Range | Domain |
|-------|--------|
| SEN-000001 – SEN-000099 | 01_strength |
| SEN-000100 – SEN-000199 | 02_five_elements |
| SEN-000200 – SEN-000299 | 03_heavenly_stems |
| SEN-000300 – SEN-000399 | 04_earthly_branches |
| SEN-000400 – SEN-000499 | 05_ten_gods |
| SEN-000500 – SEN-000599 | 06_patterns |
| SEN-000600 – SEN-000699 | 07_useful_gods |
| SEN-000700 – SEN-000799 | 08_combinations |
| SEN-000800 – SEN-000899 | 09_temperature |
| SEN-000900 – SEN-001099 | 10_shensha |
| SEN-001100 – SEN-001199 | 11_luck_cycles |
| SEN-001200 – SEN-001299 | 12_special_cases |
| SEN-001300+ | Future expansion |

No Sentence IDs are allocated in framework V1.0.0.

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
- Create interpretation sentence content in this framework phase
- Invent fake Knowledge / Rule / Reference IDs
- Duplicate Sentence IDs

---

## 10. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All 12 domains contain README / INDEX / SENTENCE_TEMPLATE
- [ ] Registry scaffolding exists
- [ ] No sentence content records created
- [ ] Frozen modules untouched
