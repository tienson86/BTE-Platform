# Metadata Specification

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Metadata and Manifest Standard)

---

# 1. Purpose

This document defines mandatory Metadata and Manifest requirements for every Knowledge Module.

---

# 2. Metadata Scope

Metadata describes Knowledge Modules and Knowledge Assets.

Metadata is itself a Knowledge Asset type and also a cross-cutting requirement on all other assets.

---

# 3. Module Metadata Contract

Every Knowledge Module shall define:

| Field | Requirement |
|-------|-------------|
| module_id | Stable logical identifier |
| domain | Single owned domain |
| display_name | Human-readable name |
| version | SemVer identity |
| status | Planned / Draft / Validated / Published / Deprecated |
| owners | Domain ownership |
| consumers | Declared consumers |
| asset_inventory | Declared Knowledge Asset types |
| dependencies | Upstream knowledge dependencies |
| compatibility_matrix | Consumer and dependency ranges |
| created_at / updated_at | Logical timestamps |
| integrity_reference | Checksum or equivalent |

---

# 4. Asset Metadata Contract

Every Knowledge Asset shall define:

| Field | Requirement |
|-------|-------------|
| asset_id | Stable logical identifier |
| asset_type | Official taxonomy type |
| module_id | Owning module |
| version | Compatible version |
| status | Draft / Validated / Published / Deprecated |
| category | Optional category |
| integrity_reference | Integrity evidence |
| references | Upstream references |

---

# 5. Manifest Specification

The Manifest is the authoritative inventory of a published Knowledge Module version.

The Manifest shall include:

- module metadata
- complete asset index
- category / terminology index
- example index
- validation dataset index
- golden dataset index
- regression dataset index where declared
- dependency declarations
- compatibility matrix
- governance approval reference
- integrity references

A published module without a complete Manifest is invalid.

---

# 6. Integrity and Traceability

Metadata and Manifest data shall support:

- asset resolution by logical identity
- version selection
- explainability references
- auditability

They shall not depend on physical repository paths.

---

# 7. Consistency Rules

- Manifest inventory must match actual declared assets.
- Metadata versions must align with module version policy.
- Deprecated assets remain listed with deprecated status during compatibility windows.
- Removed assets require MAJOR version and migration notes.

---

# 8. Prohibited Content

Metadata shall not embed:

- engine source code
- business rule bodies as a substitute for Rule Assets
- filesystem paths as public identifiers

---

# 9. Acceptance Criteria

Metadata and Manifest are accepted when:

- mandatory fields are complete;
- inventories are consistent;
- integrity references exist;
- consumers can resolve the module abstractly;
- no path-coupled identity is required.
