# Knowledge Loader Dependency Resolution

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Dependency Resolution Specification)

---

# 1. Purpose

This document defines how the Loader resolves and loads Knowledge Module dependencies.

Dependency declarations are owned by the Knowledge Registry.

Resolution for runtime binding is performed by the Knowledge Loader.

---

# 2. Resolution Inputs

- root module_id / version constraints
- consumer context
- Registry Dependency Graph
- Compatibility Matrix
- LoadMode
- resolution policy (strict / governed substitute rules)

---

# 3. Resolution Algorithm Contract

Resolve Dependency shall:

1. read required and optional dependency edges from Registry;
2. select versions via Resolve Version for each dependency;
3. detect unresolved required dependencies;
4. detect forbidden required cycles;
5. validate compatibility of the candidate closure;
6. produce a deterministic DependencyClosure;
7. load closure subjects according to LoadMode.

The algorithm is a logical contract; implementation may vary if outcomes remain deterministic for identical inputs.

---

# 4. Version Selection Collaboration

Resolve Version selects exact versions using:

- explicit requested version
- declared compatible ranges
- current recommended published version where allowed
- consumer compatibility constraints
- deprecation policy

Ambiguous multi-version candidates must be resolved by deterministic precedence rules declared in policy.

---

# 5. Compatibility Check

A DependencyClosure is bindable only when Validate Compatibility succeeds for:

- module ↔ module dependencies
- module ↔ standards ranges
- module ↔ consumer engine

---

# 6. Loading the Closure

| Mode | Behavior |
|------|----------|
| Eager | Load entire required closure immediately |
| Lazy | Record closure identities; load on demand |
| Incremental | Load closure in dependency layers |

Optional dependencies are loaded only when requested or policy requires them.

---

# 7. Failure Behavior

Unresolved required dependency, cycle, or incompatible closure results in fail-closed LoaderError.

Engines must not receive partial required closures.

---

# 8. Acceptance Criteria

Dependency Resolution is accepted when inputs, deterministic selection, compatibility gating, load-mode behavior, and fail-closed rules are complete.
