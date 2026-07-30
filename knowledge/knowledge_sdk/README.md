# Knowledge SDK

| Field | Value |
|-------|-------|
| SDK ID | knowledge_sdk |
| Document Type | Constitutional Knowledge SDK Specification |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

The Knowledge SDK is the only public interface between Runtime Engines and the Knowledge Layer.

Runtime Engines shall never access Knowledge Modules directly.

Runtime Engines shall never call Knowledge Registry or Knowledge Loader internals directly.

All runtime knowledge access must be performed through the Knowledge SDK.

The SDK does **not** execute business rules.

The SDK does **not** interpret knowledge.

---

# 2. Core Principle

```text
Knowledge Registry catalogs WHAT is published.
Knowledge Loader resolves and loads WHAT is selected.
Knowledge SDK exposes WHAT engines may access.
Runtime Engines apply HOW selected knowledge is used.
```

---

# 3. Constitutional Compliance

This SDK fully complies with and sits beneath:

- Knowledge Architecture V1.x
- Knowledge Module Standard (KMS) V1.x
- Knowledge Asset Standard (KAS) V1.x
- Knowledge Registry V1.x
- Knowledge Loader V1.x

---

# 4. Architectural Relationship

```text
Knowledge Registry
        │
        ▼
Knowledge Loader
        │
        ▼
Knowledge SDK               ← this specification
        │
        ▼
Analysis Engine
        │
        ▼
Interpretation Engine
```

Other Runtime Engines consume knowledge through the same SDK.

---

# 5. Scope

In scope:

- Module Access
- Asset Access
- Registry Access
- Loader Access
- Cache Access
- Version Resolution
- Compatibility Resolution
- Validation
- Search
- Discovery
- Metadata Access
- Dependency Resolution

Out of scope:

- Rule execution
- Knowledge interpretation
- Engine evaluation logic
- Knowledge content authoring
- Registry catalog mutation beyond governed refresh/discovery
- Physical storage layout contracts

---

# 6. SDK Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Module Access | Provide stable module retrieval for engines |
| Asset Access | Provide stable asset retrieval for engines |
| Registry Access | Expose discovery/search/metadata via Registry contracts |
| Loader Access | Expose load/bind/get operations via Loader contracts |
| Cache Access | Expose governed cache clear/refresh operations |
| Version Resolution | Resolve exact knowledge versions for a request |
| Compatibility Resolution | Surface compatibility checks for selected sets |
| Validation | Validate proposed or loaded knowledge sets |
| Search / Discovery | Find modules and assets by query |
| Metadata Access | Return registry/loader metadata summaries |
| Dependency Resolution | Resolve dependency closures for consumers |

---

# 7. Document Set

| # | Document |
|---|----------|
| 01 | README.md |
| 02 | ARCHITECTURE.md |
| 03 | DOMAIN_MODEL.md |
| 04 | SDK_OVERVIEW.md |
| 05 | PUBLIC_API.md |
| 06 | MODULE_ACCESS.md |
| 07 | ASSET_ACCESS.md |
| 08 | CACHE_ACCESS.md |
| 09 | VERSION_RESOLUTION.md |
| 10 | DEPENDENCY_RESOLUTION.md |
| 11 | ERROR_MODEL.md |
| 12 | SECURITY_MODEL.md |
| 13 | PERFORMANCE_MODEL.md |
| 14 | GOVERNANCE.md |
| 15 | VERSIONING.md |
| 16 | CHANGELOG.md |

---

# 8. Design Principles

- Single public engine-facing facade
- Path-independent identity
- Version-aware
- Dependency-aware
- Compatibility-aware
- Fail-closed on integrity/compatibility errors
- No business-rule execution
- Stable contracts across engine consumers
- Deterministic resolution for one analysis request

---

# 9. Version

| Item | Value |
|------|-------|
| SDK Spec Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

Breaking semantic changes require a major version increment.
