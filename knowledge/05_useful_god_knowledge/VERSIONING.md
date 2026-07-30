# Useful God Knowledge Versioning

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning and compatibility policy for Useful God Knowledge.

---

# 2. Version Scheme

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking Useful God semantics or incompatible contracts |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

---

# 3. Compatibility Policy

Compatibility shall be declared for:

- Fundamental Knowledge
- Knowledge Architecture / KMS / KAS
- Useful God Engine consumer range
- evidence-compatibility expectations for Strength / Temperature / Pattern published classifications
- asset-family compatibility

---

# 4. Runtime Selection

Compatible published versions are selected and frozen for one analysis request.

Consumers bind to logical version identity only.

---

# 5. Deprecation and Migration

Deprecated versions remain readable during compatibility windows and must declare successors.

Breaking changes require MAJOR increment, migration notes, and golden/regression updates.

---

# 6. Acceptance Criteria

Versioning is accepted when SemVer identity, compatibility matrices, and migration policy are complete.
