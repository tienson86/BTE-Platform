# Knowledge Compatibility Matrix

| Field | Value |
|-------|-------|
| Document Set ID | knowledge_compatibility_matrix |
| Document Type | Constitutional Compatibility Architecture |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

This document set defines compatibility rules among:

- Knowledge Modules
- Knowledge Assets
- Knowledge SDK
- Knowledge Registry
- Knowledge Loader
- Analysis Engine
- Interpretation Engine
- Report Engine

It is the authoritative compatibility architecture for co-selection, upgrade, and migration of Knowledge Layer and Runtime Engine versions.

This set does **not** implement runtime code.

It does **not** execute knowledge.

---

# 2. Core Principle

```text
Compatibility is explicit, versioned, and fail-closed.
SemVer communicates expectation.
The Compatibility Matrix authorizes co-selection.
```

Unknown compatibility is not production-eligible.

---

# 3. Constitutional Position

```text
Knowledge Architecture / KMS / KAS
        │
        ▼
Knowledge Dependency Graph
        │
        ▼
Knowledge Compatibility Matrix   ← this specification
        │
        ├── Registry Compatibility declarations
        ├── Loader / SDK resolution gates
        └── Engine consumer declarations
```

---

# 4. Document Set

| # | Document |
|---|----------|
| 01 | README.md |
| 02 | VERSION_MATRIX.md |
| 03 | COMPATIBILITY_RULES.md |
| 04 | UPGRADE_POLICY.md |
| 05 | MIGRATION_POLICY.md |
| 06 | CHANGELOG.md |

---

# 5. Scope

In scope:

- compatibility status model
- version matrix planes
- co-selection rules across modules, assets, and control plane
- engine-to-SDK compatibility
- upgrade and migration policy

Out of scope:

- implementation code
- physical repository paths
- business-rule content
- concrete per-release matrix instance data beyond architectural baselines

---

# 6. Version

| Item | Value |
|------|-------|
| Spec Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

Breaking compatibility-contract changes require a major version increment.
