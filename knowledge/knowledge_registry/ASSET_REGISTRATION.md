# Knowledge Asset Registration

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Asset Registration Specification)

---

# 1. Purpose

This document defines how Knowledge Assets are registered, updated, and removed in the Knowledge Registry.

---

# 2. Registration Preconditions

A Knowledge Asset may be registered only when:

- its owning module_id is already registered;
- it conforms to KAS for its asset_type;
- asset_id is unique within the owning module version scope as declared;
- version identity is valid;
- mandatory metadata is complete;
- references are valid logical identities;
- no repository-path identity is used as a public contract.

---

# 3. Register Asset

Register Asset creates an Asset Registry Entry.

Required inputs:

- asset_id
- module_id
- asset_type
- version
- status
- references
- metadata
- integrity_reference where declared

Effects:

- create or reject duplicate asset identity within declared scope
- index metadata
- link asset to owning module version
- record governance audit event

---

# 4. Update Asset

Update Asset modifies an existing Asset Registry Entry under change-control rules.

Published asset content is immutable within a version.

Corrections require a new asset version and corresponding module compatibility impact assessment.

---

# 5. Remove Asset

Remove Asset follows governed lifecycle transitions:

```text
Published → Deprecated → Retired → Removed (optional archival retention)
```

Assets referenced by published golden datasets or historical KnowledgeReferences must remain resolvable according to retention policy.

---

# 6. Asset Status

Asset Status values align with module lifecycle classes and may include:

- Draft
- Validated
- Published
- Deprecated
- Retired

An asset cannot be Published if its owning module version is Retired.

---

# 7. Inventory Consistency

The Module Registry asset_inventory_ref must remain consistent with Asset Registry entries for that module version.

Validation rejects orphan assets and undeclared inventory claims.

---

# 8. Acceptance Criteria

Asset Registration is accepted when register / update / remove semantics, status constraints, inventory consistency, and audit requirements are complete.
