# Golden Dataset Specification

**Document:** GOLDEN_DATASET_SPEC  
**Module:** knowledge/golden_dataset  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (read-only compliance)

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, validation, and traceability rules for Golden Dataset framework cases.

This specification is **framework only**. No actual datasets are authored in V1.0.0.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for dataset authors and reviewers.

---

## 3. Design Principles

1. **Determinism** — expected outputs are fixed for a given version
2. **Knowledge-backed** — cases cite Knowledge / Rules / Sentences when applicable
3. **Atomic intent** — one case validates one primary concern
4. **Immutability** — published expected outputs do not silently change
5. **Traceability** — full link chain to upstream assets
6. **Separation** — framework docs do not mutate operational test fixtures
7. **Frozen boundaries** — do not edit completed Knowledge Infrastructure modules

---

## 4. Dataset ID

### 4.1 Format

```
CASE-<6-digit-number>
```

Examples:

```
CASE-000001
CASE-000100
```

### 4.2 Rules

- Numbers SHALL be unique within this framework catalog.
- Numbers SHALL be zero-padded to six digits.
- Published IDs are immutable.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

---

## 5. Mandatory Metadata Support

Every case MUST support:

| Field | Description |
|-------|-------------|
| Dataset ID | `CASE-NNNNNN` |
| Title | Human-readable title |
| Domain | Framework domain directory |
| Category | Classification label |
| Input | Input fixture object / description |
| Expected Output | Deterministic expected result |
| Knowledge Assets | `KNO-*` IDs |
| Rules | `RUL-*` / rule IDs |
| Sentences | `SEN-*` IDs |
| Score | Score expectations / notes |
| References | `REF-*` IDs |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Review | Review state / reviewer notes |
| Traceability | Trace level / notes |
| Tolerance Policy | Exact match unless versioned otherwise |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Category (examples)

`Canonical` | `Boundary` | `Conflict` | `Regression` | `Locale` | `Special Case` | `Other`

### 6.3 Tolerance Policy

`Exact` | `NumericTolerance` | `SetEquality` | `CustomVersioned`

Default for framework phase documentation: `Exact`.

---

## 7. ID Allocation Ranges (Reserved)

| Range | Domain |
|-------|--------|
| CASE-000001 – CASE-000099 | 01_basic |
| CASE-000100 – CASE-000199 | 02_strength |
| CASE-000200 – CASE-000299 | 03_patterns |
| CASE-000300 – CASE-000399 | 04_useful_gods |
| CASE-000400 – CASE-000499 | 05_ten_gods |
| CASE-000500 – CASE-000599 | 06_temperature |
| CASE-000600 – CASE-000699 | 07_combinations |
| CASE-000700 – CASE-000899 | 08_shensha |
| CASE-000900 – CASE-000999 | 09_luck_cycles |
| CASE-001000 – CASE-001099 | 10_special_cases |
| CASE-001100+ | Future expansion |

No Dataset IDs are allocated in framework V1.0.0.

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

Changing Official Expected Output requires a new Version and Review gate.

---

## 9. Prohibitions

Authors MUST NOT:

- Modify frozen modules
- Modify `tests/golden_dataset/` from this framework task
- Create actual case content in this phase
- Invent fake Knowledge / Rule / Sentence / Reference IDs
- Duplicate Dataset IDs

---

## 10. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All 10 domains contain README / INDEX / DATASET_TEMPLATE
- [ ] Registry scaffolding exists
- [ ] No actual datasets created
- [ ] Frozen modules and test fixtures untouched
