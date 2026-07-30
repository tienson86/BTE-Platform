# Versioning

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Standard)

---

# 1. Purpose

This document defines versioning and compatibility requirements for every Knowledge Module and its Knowledge Assets.

---

# 2. Version Scheme

Knowledge Modules use Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking semantics or contract incompatibility |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

---

# 3. Compatibility Dimensions

Knowledge Modules shall support:

| Dimension | Meaning |
|-----------|---------|
| Module version | Package SemVer identity |
| Knowledge compatibility | Compatibility with Knowledge Architecture and peer modules |
| Asset compatibility | Compatibility of each Knowledge Asset family with consumers |
| Engine compatibility | Compatible Runtime Engine version ranges |

---

# 4. Version Surfaces

Version identity applies to:

- Knowledge Module package
- Manifest
- Metadata
- Knowledge Assets
- compatibility matrix

Package version is authoritative for consumption.

---

# 5. Backward Compatibility within 1.x

Within Version 1.x:

- existing asset IDs remain resolvable;
- existing mandatory fields remain present;
- existing category and terminology meanings remain stable;
- existing consumer contracts continue to operate.

Silent semantic drift is prohibited.

---

# 6. Runtime Selection

Registries select compatible published module versions.

Selected versions are frozen for the duration of one analysis request.

Results record selected Knowledge Module and asset versions.

---

# 7. Storage Independence

Version identity is logical.

The same Knowledge Module version remains equivalent across packaging or distribution mechanisms.

Runtime Engines bind to version identity, never to storage location.

---

# 8. Deprecation and Migration

Deprecated versions shall:

- declare successors;
- remain readable during a compatibility window;
- reject new consumer bindings;
- retain audit history.

Migration policy shall define:

- what changed;
- what remains compatible;
- what consumer actions are required.

---

# 9. Standard Compatibility

This Knowledge Module Standard is:

```text
Version 1.0.0
Status: Frozen Architecture Baseline
```

Knowledge Modules published under this standard shall declare compatibility with KMS V1.x.

---

# 10. Acceptance Criteria

Versioning is accepted when:

- SemVer identity is present;
- knowledge and asset compatibility are declared;
- request-scoped resolution is reproducible;
- no consumer depends on physical location for version identity.
