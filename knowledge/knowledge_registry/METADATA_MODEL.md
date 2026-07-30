# Knowledge Registry Metadata Model

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Metadata Model Specification)

---

# 1. Purpose

This document defines Registry Metadata used for indexing, discovery, audit, and governance.

---

# 2. Metadata Layers

```text
Registry Metadata
Module Metadata
Asset Metadata
Index Metadata
Governance Metadata
```

---

# 3. Registry Metadata Fields

Mandatory:

- registry_id
- registry_spec_version
- catalog_revision
- supported_kms_range
- supported_kas_range
- indexing_policy_id
- owners
- created / modified

---

# 4. Module Metadata Fields

Mandatory:

- module_id
- domain
- version
- status
- owners
- consumers
- dependencies
- compatibility
- tags / locales where applicable
- created / modified
- integrity_reference

---

# 5. Asset Metadata Fields

Mandatory:

- asset_id
- module_id
- asset_type
- version
- status
- references
- tags / locales where applicable
- created / modified
- integrity_reference

---

# 6. Index Metadata

Index Metadata defines which fields are searchable and facetable, including:

- identity fields
- domain / asset_type
- status / version
- owner / consumer
- tags / locales
- dependency and compatibility keys

---

# 7. Governance Metadata

Governance Metadata includes:

- approval records
- reviewer identities
- change-control tickets / decision references
- deprecation notices
- migration note references

---

# 8. Constraints

Metadata must be:

- path-independent
- stable across storage backends
- sufficient for discovery without loading full knowledge content
- consistent with KMS / KAS metadata requirements

---

# 9. Acceptance Criteria

Metadata Model is accepted when all layers, mandatory fields, and indexing constraints are complete.
