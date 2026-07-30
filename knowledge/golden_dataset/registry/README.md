# Dataset Registry — Golden Dataset Framework Domain

**Module:** `knowledge/golden_dataset`  
**Domain:** `registry`  
**Version:** V1.0.0  
**Status:** Official Framework  
**Root Specification:** `knowledge/golden_dataset/GOLDEN_DATASET_SPEC.md`  

---

## 1. Overview

This domain is a framework container within **Golden Dataset Framework**.

It holds indexes and templates for future `CASE` records related to **Dataset Registry**.

No content records are allocated in the current framework phase.

---

## 2. Purpose

Provide a stable domain boundary for **Dataset Registry** so authors can:

- allocate IDs from the reserved range
- register future records consistently
- maintain mapping and traceability hooks
- keep Governance V1.0 alignment without modifying frozen modules

---

## 3. Scope

In scope:

- Domain README / INDEX / template scaffolding
- ID allocation metadata
- Mapping and traceability placeholders
- Versioning and expansion notes

Out of scope:

- Academic content
- Populated Knowledge Assets, Rules, Sentences, Datasets, or Reports
- Runtime implementation
- Edits to frozen root specifications or other modules

---

## 4. Included Topics

Framework topic placeholders for this domain:

- Locator rows for Cases across domains

Concrete records are not authored in this refinement phase.

---

## 5. Excluded Topics

- Full doctrinal extraction or commentary
- Engine algorithms and scoring implementation
- Cross-module content owned by other domains
- Operational packs outside this framework domain (when coexisting)

---

## 6. Dependencies

This domain depends on:

- Governance V1.0 (read-only)
- Root specification: `knowledge/golden_dataset/GOLDEN_DATASET_SPEC.md`
- All Golden Dataset domain indexes

---

## 7. Relationships with other domains

- Secondary to domain authoritative records

Domain relationships are organizational. Content links are added only when records exist.

---

## 8. Knowledge Boundaries

- This domain owns only **Dataset Registry** framework placement under `knowledge/golden_dataset/registry/`.
- It does not redefine other modules' authoritative records.
- Global registry locators (if used) remain secondary to domain records.

---

## 9. Naming Convention

| Item | Convention |
|------|------------|
| Domain directory | `registry` |
| Record files (future) | `CASE-NNNNNN_<ENGLISH_SNAKE>.md` |
| Template file | `TEMPLATE.md` |
| Index file | `INDEX.md` |

---

## 10. ID Allocation

| Field | Value |
|-------|-------|
| ID Prefix | `CASE` |
| Reserved Range | `Cross-domain locator` |
| Next Free ID | **See domain ranges** |
| Allocated Records | None (framework phase) |

IDs are immutable once published. Reuse is prohibited.

---

## 11. Mapping

Future records in this domain SHOULD support links to:

- References (`REF-*`)
- Terminology (`TERM-*`)
- Knowledge Assets (`KNO-*`)
- Rules (`RUL-*`)
- Sentences (`SEN-*`)

Exact required link sets follow `knowledge/golden_dataset/GOLDEN_DATASET_SPEC.md` and related mapping standards.

---

## 12. Traceability

Traceability for future Official records SHOULD follow the module traceability specification and declare:

- upstream source links
- downstream consumer links where applicable
- version / status / review evidence

Framework phase traceability level: **L0** (scaffolding only).

---

## 13. Versioning

| Field | Value |
|-------|-------|
| Domain Framework Version | V1.0.0 |
| Record Versioning | `V#.#.#` per record when content exists |
| Compatibility | Align with root specification updates |

Root specifications remain the source of truth. Domain documents must stay aligned when roots change.

---

## 14. Future Expansion

- Allocate IDs from the reserved range
- Create records from `TEMPLATE.md`
- Update `INDEX.md` and module/global registries
- Advance Status through Draft → Review → Official

No expansion content is created in this refinement task.

---

## Domain Files

| File | Role |
|------|------|
| [INDEX.md](INDEX.md) | Domain catalog |
| [TEMPLATE.md](TEMPLATE.md) | Record template |

---

## See Also

- [../README.md](../README.md)
- [../GOLDEN_DATASET_SPEC.md](../GOLDEN_DATASET_SPEC.md)
