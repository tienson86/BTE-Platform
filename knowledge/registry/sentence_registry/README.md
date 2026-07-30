# Sentence Registry

**Module:** `knowledge/registry`  
**Domain:** `sentence_registry`  
**Version:** V1.0.0  
**Status:** Official Implementation Scaffold  
**Registry Prefix:** `SREG`  
**Object ID Prefix:** `SEN`  

---

## 1. Overview

The Sentence Registry catalogs metadata for Sentence Templates (`SEN-*`) owned by the Sentence Library.

This directory stores **metadata catalog** artifacts only. Authoritative content remains in `knowledge/sentence_library/`.

---

## 2. Purpose

- Register metadata for `SEN-*` objects
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
| Source module (`knowledge/sentence_library/`) | Authoritative object content |
| This registry (`knowledge/registry/sentence_registry/`) | Metadata catalog / locator |
| Governance registry | Frozen policy / control plane |

Conflict rule: source module wins over registry metadata until reconciled.

---

## 5. Identity

| Field | Value |
|-------|-------|
| Registry Prefix | `SREG` |
| Object ID Pattern | `SEN-NNNNNN` |
| Namespace | See `global_registry/namespace_registry.json` |

Registry IDs are immutable. Manual assignment is prohibited (REGISTRY_ID_STANDARD).

---

## 6. Files

| File | Role |
|------|------|
| `SENTENCE_REGISTRY_SPEC.md` | Domain specification |
| `sentence_registry.json` | Primary catalog |
| `template_index.json` | Index file |
| `language_index.json` | Index file |
| `rule_link_index.json` | Index file |
| `samples/empty_registry_record.json` | Empty sample record structure |
| `../schemas/registry_record.schema.json` | Shared schema validation contract |

---

## 7. Lifecycle

Draft → Validated → Approved → Registered → Published → Deprecated → Archived

Per `REGISTRY_STATE_MODEL.md`.

---

## 8. Schema Validation

Every record in `sentence_registry.json` SHALL conform to:

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
