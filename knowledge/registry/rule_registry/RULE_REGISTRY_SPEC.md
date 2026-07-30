# Rule Registry Specification

> **Document ID:** REG-RULE-SPEC-001
>
> **Module:** `knowledge/registry/rule_registry`
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Domain Registry Specification
>
> **Language:** English

---

# 1. Purpose

This specification defines the `rule_registry` domain within the BTE Registry.

It catalogs metadata for objects identified by `RUL-NNNNNN`.

It does not store domain business content.

---

# 2. Objectives

- Provide a stable metadata catalog for `RUL-*` objects
- Enable discovery by ID, namespace, type, domain, version, and dependency
- Support governance, validation, and traceability
- Preserve one Registry Record ↔ one Canonical Object mapping

---

# 3. Scope

In scope:

- Registry metadata records (`RREG-*`)
- Domain indexes
- Schema conformance
- Mapping and traceability hooks

Out of scope:

- Authoritative content in `knowledge/rule_database/`
- Runtime evaluation engines
- Fabricated catalog entries

---

# 4. Identity

| Field | Value |
|-------|-------|
| Registry Prefix | `RREG` |
| Object ID Prefix | `RUL` |
| Sequence Format | 6 digits |
| Example Registry ID | `RREG-000001` |
| Example Object ID | `RUL-000001` |

Allocation follows `REGISTRY_ID_STANDARD.md`.

Reserved ranges:

- `000001–099999` Core Registry
- `100000–499999` Domain Registry
- `500000–899999` Future Expansion
- `900000–999999` Testing

---

# 5. Catalog File

Primary catalog:

`rule_registry.json`

Container format:

```json
{
  "version": "1.0.0",
  "registry_name": "rule_registry",
  "registry_prefix": "RREG",
  "description": "...",
  "schema": "../schemas/registry_record.schema.json",
  "records": []
}
```

Each element of `records` SHALL match `REGISTRY_JSON_SCHEMA.md` / `schemas/registry_record.schema.json`.

---

# 6. Required Record Fields

From Registry Core Metadata and JSON Schema:

- Registry ID
- Object ID
- Namespace
- Version
- Status
- Owner
- URI
- Trace ID
- Dependencies

---

# 7. Indexes

- `priority_index.json`
- `knowledge_link_index.json`
- `sentence_link_index.json`

Index container format:

```json
{
  "version": "1.0.0",
  "index_name": "...",
  "description": "...",
  "entries": []
}
```

Indexes are derived views. The primary catalog remains authoritative for metadata.

# Priority Index Notes

`priority_index.json` entries SHOULD include priority values when records exist.

# Link Index Notes

- `knowledge_link_index.json` maps Rule Registry IDs → Knowledge Registry IDs
- `sentence_link_index.json` maps Rule Registry IDs → Sentence Registry IDs

---

# 8. Mapping

Mapping hierarchy and relationship types follow `REGISTRY_MAPPING_STANDARD.md`.

This registry registers objects from `knowledge/rule_database/` and may declare dependencies on other Registry Records.

Circular registry dependencies are prohibited.

---

# 9. Lifecycle

Draft → Validated → Approved → Registered → Published → Deprecated → Archived

Rejected records return to Draft.

No unpublished Registry Record may be exposed through public APIs.

---

# 10. Quality & Review

- Quality threshold for publication: score ≥ 80
- Review workflow per `REGISTRY_REVIEW_GUIDE.md`
- Traceability levels per `REGISTRY_TRACEABILITY_SPEC.md`

---

# 11. Edge Cases

Handle per `EDGE_CASES.md`, including:

- Duplicate Registry ID
- Missing Object
- Broken Dependency
- Invalid Namespace
- Missing URI
- Circular Dependency
- Invalid Traceability

---

# 12. Compliance

Every `RUL-*` object SHALL be registered before becoming available to production systems.

Objects not present in the Registry are considered invalid for production use.

---

# 13. Non-Goals

- No business logic
- No Rule Engine
- No Interpretation Engine
- No modification of Knowledge Canon content

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
