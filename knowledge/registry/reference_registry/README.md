# Reference Registry

**Module:** `knowledge/registry`  
**Domain:** `reference_registry`  
**Version:** V1.0.0  
**Status:** Official Implementation Scaffold  
**Registry Prefix:** `REFREG`  
**Object ID Prefix:** `REF`  

---

## 1. Overview

The Reference Registry catalogs metadata for References (`REF-*`) owned by the Reference Library.

This directory stores **metadata catalog** artifacts only. Authoritative content remains in `knowledge/references/`.

---

## 2. Purpose

- Register metadata for `REF-*` objects
- Support discovery, dependency tracking, and governance
- Provide empty catalog containers ready for registration
- Conform to Registry JSON Schema and Identifier Standard

---

## 3. Scope

In scope:

- Domain SPEC
- Registry catalog JSON
- Index JSON files
- Empty sample registry records
- Schema reference

Out of scope:

- Business knowledge content
- Rule evaluation / sentence generation
- Runtime Registry Service implementation
- Edits to frozen source modules

---

## 4. Authority Model

| Layer | Role |
|-------|------|
| Source module (`knowledge/references/`) | Authoritative object content |
| This registry (`knowledge/registry/reference_registry/`) | Metadata catalog / locator |
| Governance registry | Frozen policy / control plane |

Conflict rule: source module wins over registry metadata until reconciled.

---

## 5. Identity

| Field | Value |
|-------|-------|
| Registry Prefix | `REFREG` |
| Object ID Pattern | `REF-NNNNNN` |
| Namespace | See `global_registry/namespace_registry.json` |

Registry IDs are immutable. Manual assignment is prohibited (REGISTRY_ID_STANDARD).

---

## 6. Files

| File | Role |
|------|------|
| `REFERENCE_REGISTRY_SPEC.md` | Domain specification |
| `reference_registry.json` | Primary catalog |
| `domain_index.json` | Index file |
| `category_index.json` | Index file |
| `samples/empty_registry_record.json` | Empty sample record structure |
| `../schemas/registry_record.schema.json` | Shared schema validation contract |

---

## 7. Lifecycle

Draft → Validated → Approved → Registered → Published → Deprecated → Archived

Per `REGISTRY_STATE_MODEL.md`.

---

## 8. Schema Validation

Every record in `reference_registry.json` SHALL conform to:

`knowledge/registry/schemas/registry_record.schema.json`

derived from `REGISTRY_JSON_SCHEMA.md`.

---

## 9. Current Status

Catalog `records` arrays are intentionally empty in V1.0.0 Implementation Scaffold.

No fabricated content entries are included.

---

## See Also

- [`../README.md`](../README.md)
- [`../../knowledge_canon/registry/REGISTRY_SPEC.md`](../../knowledge_canon/registry/REGISTRY_SPEC.md)
- [`../../knowledge_canon/registry/REGISTRY_JSON_SCHEMA.md`](../../knowledge_canon/registry/REGISTRY_JSON_SCHEMA.md)
- [`../../knowledge_canon/registry/REGISTRY_ID_STANDARD.md`](../../knowledge_canon/registry/REGISTRY_ID_STANDARD.md)
- [`../../knowledge_canon/registry/REGISTRY_STATE_MODEL.md`](../../knowledge_canon/registry/REGISTRY_STATE_MODEL.md)
- [`../../knowledge_canon/registry/REGISTRY_MAPPING_STANDARD.md`](../../knowledge_canon/registry/REGISTRY_MAPPING_STANDARD.md)
- [`../../knowledge_canon/registry/REGISTRY_TRACEABILITY_SPEC.md`](../../knowledge_canon/registry/REGISTRY_TRACEABILITY_SPEC.md)
- [`../../knowledge_canon/registry/REGISTRY_QUALITY_STANDARD.md`](../../knowledge_canon/registry/REGISTRY_QUALITY_STANDARD.md)
