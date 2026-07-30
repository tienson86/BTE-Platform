# Knowledge Dependency Graph

| Field | Value |
|-------|-------|
| Document Set ID | knowledge_dependency_graph |
| Document Type | Constitutional Dependency Architecture |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

This document set describes every canonical dependency among:

- Knowledge Modules
- Knowledge Assets
- Knowledge Registry
- Knowledge Loader
- Knowledge SDK
- Analysis Engine
- Interpretation Engine
- Report Engine

It is the authoritative dependency map for the Knowledge Layer and its Runtime Engine consumers.

This set does **not** implement runtime code.

It does **not** execute knowledge.

---

# 2. Core Principle

```text
Dependencies flow downward toward more fundamental knowledge
and outward toward runtime consumption through SDK only.
```

Forbidden:

- Engine → Knowledge Module direct access
- Engine → Registry / Loader internals
- Knowledge Module → Runtime Engine
- Circular required Knowledge Module dependencies

---

# 3. Constitutional Stack

```text
Knowledge Architecture
        │
        ▼
Knowledge Module Standard (KMS)
        │
        ▼
Knowledge Asset Standard (KAS)
        │
        ▼
Knowledge Dependency Graph     ← this specification
        │
        ├── Knowledge Registry
        ├── Knowledge Loader
        ├── Knowledge SDK
        └── Domain Knowledge Modules / Assets
```

---

# 4. Document Set

| # | Document |
|---|----------|
| 01 | README.md |
| 02 | ARCHITECTURE.md |
| 03 | DEPENDENCY_MODEL.md |
| 04 | LIFECYCLE.md |
| 05 | COMPATIBILITY.md |
| 06 | VERSIONING.md |
| 07 | GOVERNANCE.md |
| 08 | CHANGELOG.md |

---

# 5. Scope

In scope:

- structural dependencies among knowledge and runtime components
- module-to-module knowledge dependencies
- asset-to-module ownership dependencies
- Registry / Loader / SDK control-plane dependencies
- engine consumption dependencies via SDK
- lifecycle, compatibility, versioning, and governance of those dependencies

Out of scope:

- implementation code
- physical repository paths as public contracts
- business-rule content
- engine-internal scoring algorithms

---

# 6. Version

| Item | Value |
|------|-------|
| Spec Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

Breaking dependency-contract changes require a major version increment.
