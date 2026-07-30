# Knowledge Loader Versioning

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning for the Knowledge Loader specification and its interaction with knowledge versions.

---

# 2. Version Planes

```text
1. Loader Specification Version
2. Loader Policy Profile Version
3. Knowledge Module / Asset Versions (selected at runtime)
4. Registry Catalog Revision (observed at resolve/load time)
```

These planes must not be conflated.

---

# 3. Loader Specification Versioning

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking Loader contracts |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

Version 1.0.0 is the Frozen Architecture Baseline.

---

# 4. Runtime Version Selection

ResolveVersion selects Knowledge Module/Asset versions.

Loader Spec Version does not replace knowledge SemVer.

A single analysis request freezes selected knowledge versions for its KnowledgeSnapshot.

---

# 5. Compatibility

Loader shall declare compatibility with:

- Knowledge Registry V1.x
- KMS / KAS V1.x
- Runtime Engine consumer ranges

Incompatible combinations must fail closed.

---

# 6. Upgrade Policy

Minor Loader upgrades may add APIs or load modes without breaking existing contracts.

Major upgrades require migration notes for engine consumers.

---

# 7. Acceptance Criteria

Versioning is accepted when version planes, SemVer policy, freeze semantics, and compatibility declarations are complete.
