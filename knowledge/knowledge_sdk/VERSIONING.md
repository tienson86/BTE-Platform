# Knowledge SDK Versioning

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning for the Knowledge SDK specification and its interaction with lower-layer versions.

---

# 2. Version Planes

```text
1. SDK Specification Version
2. SDK Policy Profile Version
3. Loader Specification Version
4. Registry Specification Version
5. Knowledge Module / Asset Versions (resolved at runtime)
6. Registry Catalog Revision (observed during resolve/load)
```

These planes must not be conflated.

---

# 3. SDK Specification Versioning

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking SDK contracts |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

Version 1.0.0 is the Frozen Architecture Baseline.

---

# 4. Compatibility Declarations

SDK shall declare compatibility with:

- Knowledge Registry V1.x
- Knowledge Loader V1.x
- KMS / KAS V1.x
- Runtime Engine consumer ranges

Incompatible combinations fail closed.

---

# 5. Runtime Knowledge Versions

ResolveVersion selects Knowledge Module/Asset versions.

SDK Spec Version does not replace knowledge SemVer.

KnowledgeSession freezes selected knowledge versions for one analysis request.

---

# 6. Upgrade Policy

Minor SDK upgrades may add APIs without breaking existing engine contracts.

Major upgrades require migration notes for all Runtime Engine consumers.

---

# 7. Acceptance Criteria

Versioning is accepted when version planes, SemVer policy, compatibility declarations, and freeze semantics are complete.
