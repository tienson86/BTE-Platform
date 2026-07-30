# Knowledge Dependency Versioning

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Specification)

---

# 1. Purpose

This document defines version planes and versioning rules for dependency contracts.

---

# 2. Version Planes

```text
1. Dependency Graph Specification Version
2. Knowledge Architecture / KMS / KAS Versions
3. Knowledge Registry / Loader / SDK Spec Versions
4. Knowledge Module Versions
5. Knowledge Asset Versions
6. Runtime Engine Versions
7. Registry Catalog Revision
```

These planes must not be conflated.

---

# 3. Dependency Graph Spec Versioning

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking dependency topology or forbidden/required edge changes |
| MINOR | Backward-compatible additive dependency clarifications |
| PATCH | Backward-compatible corrections |

Version 1.0.0 is the Frozen Architecture Baseline.

---

# 4. Versioned Dependency Declarations

Dependencies are always version-ranged:

```text
dependent@version → dependency@range
```

Examples of logical form:

- `pattern_knowledge@1.0.0 → fundamental_knowledge@1.x`
- `analysis_engine@1.x → knowledge_sdk@1.x`
- `knowledge_sdk@1.x → knowledge_loader@1.x`

Exact version selection occurs at runtime through SDK/Loader resolution.

---

# 5. Freeze Semantics

For one request, resolved dependency versions are frozen in the KnowledgeSession / KnowledgeSnapshot.

Catalog Revision observed at resolve time is part of reproducibility metadata.

---

# 6. Breaking Dependency Changes

Breaking changes include:

- removing a required dependency without migration
- reversing allowed dependency direction
- introducing a required cycle
- forcing engines to bypass SDK
- incompatible identity changes in Fundamental Knowledge relied upon by dependents

Such changes require MAJOR increments on affected subjects and Compatibility Matrix updates.

---

# 7. Acceptance Criteria

Versioning is accepted when version planes, ranged declarations, freeze semantics, and breaking-change rules are complete.
