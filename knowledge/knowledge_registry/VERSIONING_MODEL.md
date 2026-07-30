# Knowledge Registry Versioning Model

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Model Specification)

---

# 1. Purpose

This document defines version identity and tracking across the Knowledge Registry.

---

# 2. Version Planes

```text
1. Registry Specification Version
2. Catalog Revision
3. Knowledge Module Version
4. Knowledge Asset Version
```

These planes are independent and must be tracked separately.

---

# 3. Semantic Versioning

Module and Asset versions follow:

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking semantics or incompatible contracts |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

---

# 4. Registry Specification Version

This constitutional document set uses SemVer.

Version 1.0.0 is the Frozen Architecture Baseline.

---

# 5. Catalog Revision

Catalog Revision is a monotonic identity for catalog state changes such as:

- new module registration
- new asset registration
- status transitions
- compatibility matrix updates
- metadata index updates

Catalog Revision does not replace module/asset SemVer.

---

# 6. Version Tracking Responsibilities

The Registry shall track:

- all registered versions per module_id / asset_id
- current recommended published version where declared
- deprecation windows
- successor version pointers
- compatibility impact of each published version

---

# 7. Immutability

Published module/asset versions are immutable.

Corrections create new versions.

Registry metadata about a published version may be updated only for non-semantic catalog fields under governance.

---

# 8. List Versions

List Versions returns ordered version histories for a module or asset, including status and successor references.

---

# 9. Acceptance Criteria

Versioning Model is accepted when all version planes, SemVer policy, immutability, and tracking responsibilities are complete.
