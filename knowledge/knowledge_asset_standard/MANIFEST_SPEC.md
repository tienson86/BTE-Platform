# Manifest Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Manifest Specification)

---

# 1. Purpose

This document defines Manifest requirements for Knowledge Modules and their Knowledge Assets.

---

# 2. Scope

The Manifest is the authoritative inventory of a published Knowledge Module version.

A published module without a complete Manifest is invalid.

---

# 3. Mandatory Manifest Contents

| Section | Requirement |
|---------|-------------|
| Module identity | module_id, version, status |
| Asset index | All Knowledge Assets by asset_id and asset_type |
| Category / terminology index | Controlled vocabularies and categories |
| Example index | Example Assets |
| Validation dataset index | Validation Datasets |
| Golden dataset index | Golden Datasets |
| Regression dataset index | Where declared |
| Dependency declarations | Upstream modules / assets |
| Compatibility matrix | Consumer and dependency ranges |
| Integrity references | Checksums or equivalents |
| Governance references | Approval / validation evidence |

---

# 4. Consistency Invariants

- Manifest inventory must match actual published assets.
- No orphan published assets outside the Manifest.
- Deprecated assets remain listed with deprecated status during compatibility windows.
- Removed assets require MAJOR version and migration notes.

---

# 5. Consumption Role

Registries and Runtime Engines resolve assets through Manifest identity and version.

Manifests must not encode repository paths as public identity.

---

# 6. Validation Requirements

Validate completeness, uniqueness, referential integrity, and compatibility matrix consistency.

---

# 7. Acceptance Criteria

A Manifest is accepted when it fully inventories the published module and supports abstract asset resolution.
