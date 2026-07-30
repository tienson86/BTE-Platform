# Global Registry Specification

> **Document ID:** REG-GLOBAL-SPEC-001
>
> **Module:** `knowledge/registry/global_registry`
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

The Global Registry provides the platform-wide metadata control plane for all Registry domains.

It catalogs:

- Cross-domain registry records (`GREG-*` / `REG-*`)
- Canonical namespaces
- Canonical object types
- Master registry index
- Aggregate registry statistics

---

# 2. Objectives

- Act as the single discovery root for Registry domains
- Define valid namespaces and object types
- Track aggregate registration statistics
- Support governance and audit of the Registry system itself

---

# 3. Scope

In scope:

- `global_registry.json`
- `namespace_registry.json`
- `object_type_registry.json`
- `registry_index.json`
- `registry_statistics.json`

Out of scope:

- Domain content authorship
- Runtime Registry Service code
- Modifications to frozen Governance registries

---

# 4. Architecture Position

```
Knowledge Sources
        │
        ▼
Global Registry
        │
 ┌──────┼──────────────┐
 ▼      ▼              ▼
Domain Registries   Discovery   Governance
```

Per `REGISTRY_SPEC.md` Architecture and Registry Domains.

---

# 5. Identity

| Field | Value |
|-------|-------|
| Registry Prefix | `GREG` |
| Generic Prefix | `REG` |
| Namespace | `global` / `generic` |

---

# 6. Files

## 6.1 global_registry.json

Primary Global Registry catalog. `records` is empty until cross-domain objects are registered.

## 6.2 namespace_registry.json

Defines namespaces recognized by the Registry.

Seeded from official Registry domains / prefixes. This is architecture metadata, not business content.

## 6.3 object_type_registry.json

Defines object types from `REGISTRY_SPEC.md` Scope:

- reference
- terminology
- knowledge_asset
- rule
- priority_rule
- sentence_template
- report_template
- golden_dataset
- runtime_component
- api
- validator

## 6.4 registry_index.json

Master locator for all domain registry catalogs.

## 6.5 registry_statistics.json

Aggregate counters by registry, status, and namespace. Zeroed in V1.0.0 scaffold.

---

# 7. Required Metadata

Global Registry Records SHALL include Core Metadata from `REGISTRY_SPEC.md`:

- Registry ID
- Object ID
- Object Type
- Namespace
- Status
- Version
- Owner
- Created Date
- Updated Date
- Checksum
- Source Location
- Dependencies

---

# 8. Lifecycle

Draft → Validated → Approved → Registered → Published → Deprecated → Archived

---

# 9. Compliance

Domain registries SHALL be listed in `registry_index.json` before production use.

Namespace and object type values used by domain registries SHOULD resolve through the Global Registry catalogs.

---

# 10. TODOs

- TODO: Confirm whether `runtime_component`, `api`, and `validator` object types require dedicated domain registries in a future minor release.
- TODO: Confirm statistics refresh ownership (manual vs Registry Service).

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
