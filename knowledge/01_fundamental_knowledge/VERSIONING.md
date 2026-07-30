# Fundamental Knowledge Versioning

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning and compatibility policy for Fundamental Knowledge.

---

# 2. Version Scheme

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking change to fundamental semantics or identity contracts |
| MINOR | Backward-compatible additive references / locales / optional tables |
| PATCH | Backward-compatible corrections that preserve meaning |

---

# 3. Compatibility Dimensions

- Knowledge Architecture compatibility
- KMS / KAS compatibility
- Downstream Knowledge Module compatibility
- Asset compatibility

---

# 4. Stability Expectations

Fundamental Knowledge is a high-stability module.

Semantic changes should be rare and carefully governed because all domain modules depend on it.

---

# 5. Runtime Selection

Compatible published versions are selected and frozen per analysis request.

Consumers bind to logical version identity, not repository location.

---

# 6. Deprecation and Migration

Deprecated versions shall declare successors and remain readable during compatibility windows.

Breaking fundamental identity changes require MAJOR version and explicit migration notes for all dependents.

---

# 7. Acceptance Criteria

Versioning is accepted when SemVer identity, compatibility matrices, and migration policy are complete.
