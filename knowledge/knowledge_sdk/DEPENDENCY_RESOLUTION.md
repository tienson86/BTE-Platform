# Knowledge SDK Dependency Resolution

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Dependency Resolution Specification)

---

# 1. Purpose

This document defines ResolveDependency behavior exposed by the Knowledge SDK.

Dependency declarations are owned by the Knowledge Registry.

Runtime resolution/binding is performed through Knowledge Loader services and surfaced by the SDK.

---

# 2. ResolveDependency()

ResolveDependency computes a DependencyResolution for a root module version.

Inputs:

- root module_id / version
- consumer context
- resolution policy
- optional include-optional-dependencies flag

Outputs:

- ordered/closed set of KnowledgeReferences
- resolution status
- compatibility summary
- unresolved optional notes where applicable

---

# 3. Resolution Guarantees

- required dependencies are complete or the call fails
- forbidden required cycles fail closed
- selected versions are exact
- compatibility is validated for the closure and consumer
- results are deterministic for identical inputs and catalog revision

---

# 4. Relationship to GetModule / GetAsset

ResolveDependency may be used before materialization.

Subsequent GetModule/GetAsset calls for closure members must use the resolved frozen versions when executed in the same KnowledgeSession.

---

# 5. Compatibility Resolution

DependencyResolution includes or references CompatibilityResolution outcomes.

Incompatible closures are not returned as bindable successes.

---

# 6. Error Conditions

- DependencyError
- VersionResolutionError
- CompatibilityError
- NotFound
- AuthorizationError

---

# 7. Acceptance Criteria

Dependency Resolution is accepted when guarantees, session binding rules, and fail-closed behavior are complete.
