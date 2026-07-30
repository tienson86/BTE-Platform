# Knowledge Assets

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Taxonomy)

---

# 1. Purpose

This document defines the official Knowledge Asset taxonomy.

A Knowledge Module is a container of Knowledge Assets.

The Rule Database is only one Knowledge Asset.

---

# 2. What Is a Knowledge Asset

A Knowledge Asset is a versioned, governed unit of domain knowledge that can be consumed through abstract interfaces.

Knowledge Assets are logical.

They are not equivalent to files, folders, or engine classes.

---

# 3. Official Asset Taxonomy

A Knowledge Module may contain the following asset types:

| Asset Type | Purpose |
|------------|---------|
| Rule Database | Analytical decision rules |
| Decision Tables | Tabular decision logic |
| Mapping Tables | Deterministic mapping relationships |
| Terminology | Canonical terms and definitions |
| Metadata | Descriptive and operational metadata |
| Examples | Illustrative domain cases |
| Golden Dataset | Deterministic expected outcomes |
| Validation Dataset | Machine-checkable integrity and behavior checks |
| Priority Tables | Priority and conflict-ordering data |
| Formula Library | Declarative formulas and coefficient sets |
| Reference Tables | Shared reference values and lookups |
| Configuration | Domain configuration profiles |
| Documentation | Human-readable module documentation |

Additional asset types may be introduced in Version 1.x if declared, manifested, and validated.

---

# 4. Rule Database Clarification

```text
Knowledge Module
   └── Knowledge Assets
          ├── Rule Database          ← one asset type
          ├── Decision Tables
          ├── Mapping Tables
          ├── Terminology
          ├── ...
```

A Knowledge Module must never be equated with a Rule Database.

A module may publish zero Rule Databases if its domain is Terminology, Interpretation sentences, or Report templates, provided other required assets for that domain are present.

---

# 5. Asset Contract Requirements

Every Knowledge Asset shall define:

| Field | Requirement |
|-------|-------------|
| asset_id | Stable logical identifier |
| asset_type | Value from official taxonomy |
| module_id | Owning Knowledge Module |
| version | Compatible module / asset version |
| status | Draft / Validated / Published / Deprecated |
| checksum / integrity reference | Integrity evidence |
| metadata | Required descriptive metadata |
| references | Upstream asset references where applicable |

---

# 6. Consumption Model

```text
Runtime Engine
      │
      ▼
Abstract Interface
      │
      ▼
Knowledge Asset Snapshot
```

Runtime Engines consume assets by logical identity and version.

Runtime Engines must never depend on repository paths.

---

# 7. Domain Composition Patterns

## Analytical Knowledge Modules

Typically declare:

- Rule Database
- Decision Tables / Mapping Tables as needed
- Priority Tables
- Formula Library / Reference Tables as needed
- Terminology references
- Examples
- Validation Dataset
- Golden Dataset
- Metadata
- Documentation

## Interpretation Knowledge

Typically declare:

- Terminology
- Examples
- Validation / Golden Datasets
- Configuration
- Documentation
- sentence-oriented assets under Documentation / Configuration / Reference models as domain-appropriate

## Report Knowledge

Typically declare:

- Reference Tables
- Configuration
- Examples
- Validation / Golden Datasets
- Documentation
- template-oriented assets as domain-appropriate

---

# 8. Non-Duplication Rule

If an asset already exists in an upstream Knowledge Module:

- reference it;
- do not copy it;
- do not redefine it under a new identity without migration.

---

# 9. Immutability

Published Knowledge Assets are immutable within a version.

Corrections require a new version publication.

---

# 10. Acceptance Criteria

Knowledge Asset taxonomy compliance is accepted when:

- every declared asset maps to the official taxonomy;
- Rule Database is not treated as the entire module;
- assets are manifested and versioned;
- engines consume assets abstractly;
- no physical-path identity is required.
