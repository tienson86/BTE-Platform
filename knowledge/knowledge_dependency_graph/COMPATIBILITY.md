# Knowledge Dependency Compatibility

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Compatibility Specification)

---

# 1. Purpose

This document defines compatibility rules for all dependency edges in the Knowledge Dependency Graph.

---

# 2. Compatibility Planes

1. Standards ↔ Modules / Registry / Loader / SDK
2. Module ↔ Module
3. Asset ↔ Module / Asset
4. Registry ↔ Loader ↔ SDK
5. SDK ↔ Analysis / Interpretation / Report Engines
6. Stage ↔ Domain Knowledge Module

---

# 3. Compatibility Status

| Status | Production Meaning |
|--------|--------------------|
| Compatible | Safe to co-select |
| CompatibleWithMigration | Usable with documented migration |
| Incompatible | Must not be co-selected |
| Unknown | Not production-eligible |

---

# 4. Required Compatibility Declarations

Every published Knowledge Module shall declare compatibility with:

- Fundamental Knowledge range (if dependent)
- KMS / KAS / Architecture ranges
- Knowledge SDK / Loader / Registry ranges as consumer-facing expectations
- primary consumer engine range

Every published control-plane component (Registry / Loader / SDK) shall declare compatibility with adjacent layers.

Every Runtime Engine shall declare the Knowledge SDK range it supports.

---

# 5. Co-Selection Rules

A resolved dependency closure is production-bindable only when:

- all required edges resolve within Compatible or CompatibleWithMigration status;
- no Incompatible pair is present;
- no required edge is Unknown;
- SDK, Loader, and Registry versions in the runtime stack are mutually Compatible.

---

# 6. Evidence Dependency Compatibility

Evidence dependencies require that referenced upstream classification identities remain recognizable.

They do not require the dependent module to re-implement upstream engines.

If upstream classification semantics break, dependents must MAJOR-version and update Compatibility Matrix entries.

---

# 7. Engine Compatibility

| Engine | Must remain compatible with |
|--------|-----------------------------|
| Analysis Engine | Knowledge SDK; stage-specific Knowledge Modules |
| Interpretation Engine | Knowledge SDK; Interpretation / Sentence Knowledge |
| Report Engine | Knowledge SDK; Report Template Knowledge |

Engines are incompatible with any mode that bypasses SDK.

---

# 8. Failure Behavior

Incompatible dependency sets fail closed at ResolveDependency / Validate / Load time.

Silent downgrade to incompatible versions is forbidden.

---

# 9. Acceptance Criteria

Compatibility is accepted when planes, statuses, co-selection rules, and fail-closed behavior are complete.
