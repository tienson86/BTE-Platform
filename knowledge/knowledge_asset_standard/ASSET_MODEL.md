# Canonical Asset Model

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Asset Model Specification)

---

# 1. Purpose

This document defines the canonical model shared by every Knowledge Asset.

All asset-type specifications specialize this model.

---

# 2. Canonical Fields

Every Knowledge Asset shall define:

| Concern | Fields |
|---------|--------|
| Identity | asset_id, asset_type, display_name |
| Ownership | module_id, owner |
| Versioning | version, compatibility |
| Dependencies | depends_on, references |
| Lifecycle | status, effective dating |
| Validation | validation_status, integrity_reference |
| Metadata | author, reviewer, created, modified, status, references |
| Governance | approval_reference, deprecation_reference |

---

# 3. Asset Identity

`asset_id` shall be:

- stable
- unique within its Knowledge Module
- logical
- independent of repository path

`asset_type` shall be a value from the official taxonomy.

---

# 4. Asset Owner

Every asset belongs to exactly one Knowledge Module (`module_id`).

Shared assets are owned by the shared upstream module and referenced by dependents.

---

# 5. Asset Version

Asset versions follow SemVer alignment with the owning Knowledge Module package version policy.

Package version is authoritative for consumption.

Asset-level version metadata must not contradict package compatibility.

---

# 6. Asset Compatibility

Every asset shall declare compatibility with:

- owning Knowledge Module version range
- dependent asset version ranges where applicable
- Knowledge Asset Standard version
- consumer expectations where explicitly required

---

# 7. Asset Dependencies

Dependencies shall be:

- explicit
- directional
- acyclic within the module graph
- versioned

Assets may reference Terminology, Formula Library, Priority Tables, Mapping Tables, and other published assets.

---

# 8. Asset Lifecycle

Allowed status values:

- Draft
- Validated
- Published
- Deprecated

Transitions:

```text
Draft → Validated → Published → Deprecated
```

Direct mutation of Published assets is prohibited.

---

# 9. Asset Validation

Every asset shall pass type-specific validation plus canonical checks:

- identity uniqueness
- taxonomy validity
- metadata completeness
- referential integrity
- integrity reference presence

---

# 10. Asset Metadata

Mandatory metadata includes at least:

- author
- reviewer
- created
- modified
- version
- compatibility
- status
- references

See METADATA_SPEC.md.

---

# 11. Asset Governance

Every published asset shall retain:

- approval evidence
- validation evidence
- changelog linkage through the owning module
- deprecation / migration notes when applicable

See GOVERNANCE.md.

---

# 12. Immutability

Within a published version, asset content is immutable.

Corrections require a new version.
