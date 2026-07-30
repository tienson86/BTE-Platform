# Rule Database Specification

**Document:** RULE_DATABASE_SPEC  
**Module:** knowledge/rule_database  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, mapping, and traceability rules for Rule Database framework records.

This specification is **framework only**. No rule content is authored in V1.0.0.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for rule authors and reviewers.

---

## 3. Design Principles

1. **Knowledge-backed** — rules cite Knowledge Assets when applicable
2. **Atomic conditions** — one rule expresses one decision unit
3. **Deterministic intent** — conditions and outcomes are explicit
4. **Traceability** — links to Knowledge / Terminology / References / Sentences
5. **Priority awareness** — conflicts are resolved by declared priority policy
6. **Version immutability** — published rule versions do not silently change
7. **Frozen boundaries** — do not edit completed Knowledge Infrastructure modules or existing `*_rules/` packs

---

## 4. Rule ID

### 4.1 Format

```
RUL-<6-digit-number>
```

Examples:

```
RUL-000001
RUL-000100
```

### 4.2 Rules

- Numbers SHALL be unique within the Rule Database Framework catalog.
- Numbers SHALL be zero-padded to six digits.
- Published IDs are immutable.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

### 4.3 Governance Compatibility

Governance V1.0 uses examples such as `RID-STR-00125`.

This framework uses sequential `RUL-NNNNNN` as the **catalog primary key**.

Compatibility MAY be recorded in metadata (`governance_alias`) without modifying Governance files.

---

## 5. Mandatory Metadata Support

Every framework rule record MUST support:

| Field | Description |
|-------|-------------|
| Rule ID | `RUL-NNNNNN` |
| Title | Human-readable rule title |
| Domain | Framework domain directory |
| Category | Classification label |
| Priority | Numeric or ordered priority |
| Condition | Structured condition placeholder |
| Outcome | Structured outcome placeholder |
| Knowledge Links | `KNO-*` IDs |
| Terminology Links | `TERM-*` IDs |
| Reference Links | `REF-*` IDs |
| Sentence Links | Sentence IDs |
| Related Rules | Other `RUL-*` IDs |
| Confidence | Confidence level |
| Evidence | Evidence notes |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace level / notes |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Confidence

`High` | `Medium` | `Low` | `Unverified`

### 6.3 Category (examples)

`Classification` | `Selection` | `Conflict` | `Priority` | `Transformation` | `Special Case` | `Other`

---

## 7. ID Allocation Ranges (Reserved)

| Range | Domain |
|-------|--------|
| RUL-000001 – RUL-000099 | 01_strength |
| RUL-000100 – RUL-000199 | 02_season |
| RUL-000200 – RUL-000299 | 03_temperature |
| RUL-000300 – RUL-000399 | 04_patterns |
| RUL-000400 – RUL-000499 | 05_useful_gods |
| RUL-000500 – RUL-000599 | 06_ten_gods |
| RUL-000600 – RUL-000699 | 07_combinations |
| RUL-000700 – RUL-000799 | 08_clashes |
| RUL-000800 – RUL-000899 | 09_transformations |
| RUL-000900 – RUL-001099 | 10_shensha |
| RUL-001100 – RUL-001199 | 11_luck_cycles |
| RUL-001200 – RUL-001299 | 12_special_cases |
| RUL-001300+ | Future expansion |

No Rule IDs are allocated in framework V1.0.0.

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

- Modify frozen modules or existing `*_rules/` content
- Create actual rule logic in this framework phase
- Invent fake Knowledge / Terminology / Reference IDs
- Duplicate Rule IDs

---

## 10. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All 12 domains contain README / INDEX / RULE_TEMPLATE
- [ ] Registry scaffolding exists
- [ ] No rule content records created
- [ ] Existing operational packs untouched
