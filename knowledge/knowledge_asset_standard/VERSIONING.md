# Versioning

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning and compatibility policy for Knowledge Assets.

---

# 2. Version Scheme

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking semantics or incompatible contracts |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

---

# 3. Compatibility Matrix

Knowledge Assets shall support:

- module compatibility
- asset compatibility
- standard compatibility (KAS / KMS / Knowledge Architecture)
- consumer compatibility where declared

---

# 4. Runtime Selection

Compatible published versions are selected and frozen for one analysis request.

Results record selected asset and module versions.

---

# 5. Storage Independence

Version identity is logical and independent of repository layout.

---

# 6. Deprecation and Migration

Deprecated assets shall declare successors and remain readable during compatibility windows.

Breaking changes require MAJOR increments and migration notes.

---

# 7. Standard Compatibility

This Knowledge Asset Standard is:

```text
Version 1.0.0
Status: Frozen Architecture Baseline
```

Published assets shall declare compatibility with KAS V1.x.

---

# 8. Acceptance Criteria

Versioning is accepted when SemVer identity, compatibility matrices, and request-scoped resolution are complete and path-independent.
