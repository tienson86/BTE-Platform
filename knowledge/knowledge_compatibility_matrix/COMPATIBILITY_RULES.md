# Knowledge Compatibility Rules

**Component:** Knowledge Compatibility Matrix  
**Version:** V1.0.0  
**Status:** Frozen (Compatibility Rules Specification)

---

# 1. Purpose

This document defines the normative compatibility rules applied across Knowledge Modules, Knowledge Assets, SDK, Registry, Loader, and Runtime Engines.

---

# 2. Status Definitions

| Status | Meaning | Production Bindable |
|--------|---------|---------------------|
| Compatible | Safe to co-select within declared range | Yes |
| CompatibleWithMigration | Bindable only with documented migration steps | Yes, with migration |
| Incompatible | Must not be co-selected | No |
| Unknown | Not assessed | No |

---

# 3. Universal Rules

1. Compatibility is explicit; absence of a required matrix entry is treated as Unknown.
2. Unknown is not production-eligible.
3. SemVer MAJOR implies presumed incompatibility until matrix entries say otherwise.
4. SemVer MINOR/PATCH within a declared Compatible range remains Compatible unless matrix overrides.
5. Fail closed on Incompatible co-selection.
6. Path-based identity is never a compatibility key.
7. Engines access knowledge only through SDK; any bypass is Incompatible.

---

# 4. Module Compatibility Rules

- Every published analytical module must be Compatible with Fundamental Knowledge 1.x (or declare a new MAJOR migration).
- Evidence dependencies require recognizable upstream classification identities.
- Evidence dependency does not grant ownership or recomputation rights.
- Required module dependency cycles are Incompatible by architecture.
- Deprecated module versions may remain Compatible during declared windows; Retired versions are Incompatible for new bindings.

---

# 5. Asset Compatibility Rules

- Asset version must be Compatible with its owning module version.
- Asset type must be Compatible with declared KAS range.
- Referenced assets in golden/validation datasets must resolve to Compatible versions.
- Published asset content is immutable; compatibility changes require new versions and matrix updates.

---

# 6. Registry / Loader / SDK Rules

```text
Registry 1.x  ↔  Loader 1.x  ↔  SDK 1.x
```

- Loader must be Compatible with Registry catalog contracts in use.
- SDK must be Compatible with both Loader and Registry contracts it surfaces.
- Catalog Revision advances do not alone break SemVer compatibility, but changed subjects require matrix-valid versions.
- Integrity/compatibility validation failures block bind even if matrix status was previously Compatible for older catalog content.

---

# 7. Engine Compatibility Rules

| Engine | Rules |
|--------|-------|
| Analysis Engine | Must be Compatible with SDK; each stage with its Knowledge Module range |
| Interpretation Engine | Must be Compatible with SDK and Interpretation/Sentence Knowledge ranges |
| Report Engine | Must be Compatible with SDK and Report Template Knowledge ranges |

Cross-engine knowledge sharing must occur through published results / KnowledgeReferences, not through private knowledge handles borrowed across unauthorized consumers.

---

# 8. Co-Selection Algorithm Contract

Validate Compatibility for a proposed set shall:

1. expand required dependency closure;
2. collect all required subject↔target pairs;
3. lookup matrix status for each pair;
4. reject if any required pair is Incompatible or Unknown;
5. accept CompatibleWithMigration only when migration policy requirements are acknowledged by governed process;
6. return a deterministic compatibility report.

---

# 9. Override Policy

Emergency overrides are forbidden in production without governance approval and audit records.

No local engine hard-code may mark Incompatible pairs as Compatible.

---

# 10. Acceptance Criteria

Compatibility Rules are accepted when statuses, universal rules, per-layer rules, co-selection contract, and override prohibition are complete.
