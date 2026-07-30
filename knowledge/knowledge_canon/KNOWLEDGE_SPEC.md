# Knowledge Canon Specification

**Document:** KNOWLEDGE_SPEC  
**Module:** knowledge/knowledge_canon  
**Version:** V1.0.0  
**Status:** Official  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  
**Reference Library:** V1.0 (frozen — not modified)  
**Terminology Framework:** referenced only — not modified  

---

## 1. Purpose

Define identifiers, metadata, domain placement, lifecycle, mapping, and traceability rules for Knowledge Assets in the BTE Knowledge Canon.

This specification is **framework only**. No Knowledge Asset content is authored in V1.0.0.

---

## 2. Normative Language

The key words SHALL, MUST, SHOULD, and MAY are requirements for Knowledge Canon authors and reviewers.

---

## 3. Design Principles

1. **Single Source of Truth** — one concept, one Knowledge Asset
2. **Reference driven** — cite approved Reference IDs
3. **Atomic knowledge** — one asset = one concept
4. **Explainability** — full traceability chain
5. **Version immutability** — published versions do not silently change
6. **Machine-readable structure** — stable fields and IDs
7. **Frozen boundaries** — do not edit Governance, Reference, or Terminology modules

---

## 4. Knowledge ID

### 4.1 Format

```
KNO-<6-digit-number>
```

Examples:

```
KNO-000001
KNO-000002
```

### 4.2 Rules

- Numbers SHALL be unique within the Knowledge Canon.
- Numbers SHALL be zero-padded to six digits.
- Published IDs are immutable.
- Reuse of retired IDs is prohibited.
- Domain MUST NOT be encoded in the ID string.

### 4.3 Governance Compatibility

Governance V1.0 describes structured Knowledge IDs such as `KID-…`.

This Canon Framework uses sequential `KNO-NNNNNN` IDs as the **catalog primary key** for Knowledge Assets.

Compatibility SHALL be maintained by:

- Storing domain / category in metadata
- Optional later dual-label notes in metadata
- Never editing frozen Governance documents

---

## 5. Mandatory Knowledge Asset Support

Every Knowledge Asset MUST support:

| Field / Concern | Description |
|-----------------|-------------|
| Metadata | Bibliographic / administrative metadata block |
| Canonical Name | Official display name |
| Chinese | Chinese label |
| Vietnamese | Vietnamese label |
| English | English label |
| Definition | Canonical definition |
| Domain | Canon domain directory |
| Category | Classification label |
| Relationships | Links to related Knowledge Assets |
| Terminology Links | `TERM-*` IDs |
| Reference Links | `REF-*` IDs |
| Rule Links | Rule IDs |
| Sentence Links | Sentence IDs |
| Confidence | Confidence level |
| Evidence | Evidence notes / pointers |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace fields / chain completeness |

---

## 6. Controlled Enumerations

### 6.1 Status

`Placeholder` | `Draft` | `Review` | `Official` | `Deprecated`

### 6.2 Confidence

`High` | `Medium` | `Low` | `Unverified`

### 6.3 Category (examples)

`Core Concept` | `Relationship` | `Classification` | `Procedure` | `Special Case` | `Other`

---

## 7. Domains

| # | Directory | Domain |
|---|-----------|--------|
| 01 | `01_five_elements/` | Five Elements |
| 02 | `02_heavenly_stems/` | Heavenly Stems |
| 03 | `03_earthly_branches/` | Earthly Branches |
| 04 | `04_hidden_stems/` | Hidden Stems |
| 05 | `05_yin_yang/` | Yin Yang |
| 06 | `06_ten_gods/` | Ten Gods |
| 07 | `07_strength/` | Strength |
| 08 | `08_patterns/` | Patterns |
| 09 | `09_useful_gods/` | Useful Gods |
| 10 | `10_combinations/` | Combinations |
| 11 | `11_clashes/` | Clashes |
| 12 | `12_punishments/` | Punishments |
| 13 | `13_harms/` | Harms |
| 14 | `14_transformations/` | Transformations |
| 15 | `15_seasonal_qi/` | Seasonal Qi |
| 16 | `16_temperature/` | Temperature |
| 17 | `17_shensha/` | ShenSha |
| 18 | `18_luck_cycles/` | Luck Cycles |
| 19 | `19_special_cases/` | Special Cases |

Registry lives under `registry/`.

---

## 8. ID Allocation Ranges (Reserved)

| Range | Domain |
|-------|--------|
| KNO-000001 – KNO-000099 | 01_five_elements |
| KNO-000100 – KNO-000199 | 02_heavenly_stems |
| KNO-000200 – KNO-000299 | 03_earthly_branches |
| KNO-000300 – KNO-000399 | 04_hidden_stems |
| KNO-000400 – KNO-000499 | 05_yin_yang |
| KNO-000500 – KNO-000599 | 06_ten_gods |
| KNO-000600 – KNO-000699 | 07_strength |
| KNO-000700 – KNO-000799 | 08_patterns |
| KNO-000800 – KNO-000899 | 09_useful_gods |
| KNO-000900 – KNO-000999 | 10_combinations |
| KNO-001000 – KNO-001099 | 11_clashes |
| KNO-001100 – KNO-001199 | 12_punishments |
| KNO-001200 – KNO-001299 | 13_harms |
| KNO-001300 – KNO-001399 | 14_transformations |
| KNO-001400 – KNO-001499 | 15_seasonal_qi |
| KNO-001500 – KNO-001599 | 16_temperature |
| KNO-001600 – KNO-001799 | 17_shensha |
| KNO-001800 – KNO-001899 | 18_luck_cycles |
| KNO-001900 – KNO-001999 | 19_special_cases |
| KNO-002000+ | Future expansion |

No Knowledge Asset IDs are allocated in framework V1.0.0.

---

## 9. Lifecycle

```
Placeholder / Draft
        ↓
     Review
        ↓
    Official
        ↓
   Deprecated (optional)
```

Transitions follow `KNOWLEDGE_REVIEW_GUIDE.md` and Governance procedures without editing frozen Governance files.

---

## 10. Prohibitions

Authors MUST NOT:

- Modify Governance, Reference Library, or Terminology Framework
- Create actual knowledge content in this framework phase
- Extract concepts into assets yet
- Create rules or terminology records here
- Duplicate Knowledge IDs
- Invent fake `REF-*` / `TERM-*` / Rule / Sentence IDs

---

## 11. Acceptance Criteria (Framework V1.0.0)

- [ ] Root framework documents exist
- [ ] All 19 domains contain README / INDEX / TEMPLATE
- [ ] Registry scaffolding exists
- [ ] No Knowledge Asset content records created
- [ ] Frozen modules untouched
