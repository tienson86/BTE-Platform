# Knowledge Module Structure

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Module Structure Specification)

---

# 1. Purpose

This document defines the mandatory **logical structure** of every Knowledge Module.

This is a logical specification.

It is not a repository requirement.

Physical folders may differ, provided the logical package contents remain complete and discoverable through the Knowledge Registry.

---

# 2. Canonical Logical Structure

```text
Knowledge Module
├── Documentation
├── Rule Assets
├── Example Assets
├── Validation Assets
├── Metadata
├── Manifest
├── Version
└── Governance
```

Additional logical areas may exist when corresponding Knowledge Asset types are declared, including:

- Decision Tables
- Mapping Tables
- Terminology
- Priority Tables
- Formula Library
- Reference Tables
- Configuration
- Golden Datasets
- Regression Datasets

---

# 3. Area Responsibilities

| Logical Area | Responsibility |
|--------------|----------------|
| Documentation | Purpose, architecture, scope, assets, dependencies, version, governance, validation, quality, roadmap |
| Rule Assets | Rule Database and related rule indexes when declared |
| Example Assets | Canonical, boundary, conflict, negative, localization examples |
| Validation Assets | Validation, golden, and regression datasets |
| Metadata | Module and asset metadata |
| Manifest | Authoritative published inventory |
| Version | SemVer identity and compatibility matrix |
| Governance | Ownership, approval, change, deprecation records |

---

# 4. Mandatory Documentation

Every future Knowledge Module shall contain documentation covering:

| Topic | Requirement |
|-------|-------------|
| Purpose | Why the module exists |
| Architecture | Logical architecture and consumers |
| Scope | In-scope and out-of-scope boundaries |
| Assets | Declared Knowledge Asset inventory |
| Dependencies | Upstream knowledge dependencies |
| Version | SemVer and compatibility |
| Governance | Ownership and approval state |
| Validation | Validation approach and dataset references |
| Quality | Quality criteria and gate status |
| Roadmap | Planned extensions within compatibility policy |

---

# 5. Documentation Invariants

Documentation shall:

- describe domain purpose clearly;
- declare consumers;
- declare non-goals;
- avoid embedding engine algorithms;
- avoid hard-coded physical paths;
- remain synchronized with published assets.

---

# 6. Manifest Completeness

A published Knowledge Module is invalid without a complete Manifest indexing:

- all Knowledge Assets
- categories / taxonomies
- examples
- validation datasets
- golden datasets
- regression datasets where declared
- compatibility matrix
- integrity references

---

# 7. Declared vs Optional Areas

- Optional asset areas may be omitted only if not declared.
- Declared asset types must be fully populated for publication.
- Rule Assets are mandatory only when the module declares Rule Database or related rule families.
- Interpretation Knowledge and Report Knowledge may omit Rule Assets if outside scope.

---

# 8. Structural Invariants

- Logical package completeness is mandatory.
- Physical folder names are not part of the public contract.
- Repository reorganization shall not change logical module identity.
- Rule Database alone does not constitute a complete Knowledge Module.

---

# 9. Extension Rules

Additional logical areas may be added in Version 1.x if:

- existing mandatory areas remain intact;
- consumers remain compatible;
- the Manifest indexes the additions;
- documentation is updated.
