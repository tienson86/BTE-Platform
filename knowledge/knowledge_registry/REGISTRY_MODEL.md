# Knowledge Registry Model

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Registry Model Specification)

---

# 1. Purpose

This document defines the canonical Registry Model used to catalog Knowledge Modules and Knowledge Assets.

---

# 2. Registry Composition

```text
Knowledge Registry
 ├── Knowledge Module Registry
 ├── Knowledge Asset Registry
 ├── Registry Metadata
 ├── Registry Version Catalog
 ├── Dependency Graph
 ├── Compatibility Matrix
 ├── Knowledge Index
 └── Governance Records
```

---

# 3. Knowledge Module Registry

The Module Registry is the authoritative inventory of Knowledge Modules.

Each entry shall include at least:

| Field | Requirement |
|-------|-------------|
| module_id | Stable unique logical identity |
| domain | Knowledge domain |
| display_name | Human-readable name |
| versions | Published version set |
| current_published_version | Optional current recommended version |
| status | Module lifecycle status |
| owners | Ownership records |
| consumers | Declared consumers |
| dependencies | Declared module dependencies |
| compatibility | Compatibility declarations |
| asset_inventory_ref | Reference to registered assets |
| metadata | Searchable metadata |
| created / modified | Audit timestamps |
| integrity_reference | Integrity / checksum reference where declared |

---

# 4. Knowledge Asset Registry

The Asset Registry is the authoritative inventory of Knowledge Assets.

Each entry shall include at least:

| Field | Requirement |
|-------|-------------|
| asset_id | Stable unique logical identity |
| module_id | Owning module identity |
| asset_type | KAS asset type |
| versions | Published version set |
| status | Asset lifecycle status |
| references | Related assets / terms / rules |
| metadata | Searchable metadata |
| created / modified | Audit timestamps |
| integrity_reference | Integrity / checksum reference where declared |

---

# 5. Registry Metadata

Registry Metadata includes:

- registry_id
- registry_version
- catalog_revision
- supported_kms_range
- supported_kas_range
- indexing_policy
- retention / audit policy references

---

# 6. Registry Version

Registry Version distinguishes:

1. Registry Specification Version — this constitutional document set
2. Catalog Revision — incremental catalog state identity
3. Module / Asset Versions — published knowledge content versions

These three version planes must not be conflated.

---

# 7. Knowledge Index

The Knowledge Index indexes facets such as:

- module_id / asset_id
- domain
- asset_type
- status
- version
- owner
- consumer
- tags / locales
- dependency edges
- compatibility keys

---

# 8. Non-Goals

The Registry Model does not:

- store executable engine code
- evaluate rule conditions
- bind consumers to physical locations
- replace KMS or KAS content contracts

---

# 9. Acceptance Criteria

The Registry Model is accepted when Module Registry, Asset Registry, Metadata, Version planes, Dependency Graph hooks, Compatibility Matrix hooks, and Knowledge Index are fully defined and path-independent.
