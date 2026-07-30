# Knowledge Dependency Lifecycle

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Lifecycle Specification)

---

# 1. Purpose

This document defines how dependencies are created, validated, published, consumed, deprecated, and retired.

---

# 2. Lifecycle Stages

```text
Declare Dependency
        │
        ▼
Validate Dependency
        │
        ▼
Register in Registry
        │
        ▼
Publish Compatible Set
        │
        ▼
Resolve via Loader / SDK
        │
        ▼
Consume in Runtime Engines
        │
        ▼
Deprecate / Migrate
        │
        ▼
Retire
```

---

# 3. Declare Dependency

Knowledge Modules declare:

- required module dependencies (typically Fundamental Knowledge)
- optional/evidence dependencies on upstream analytical modules
- standards compatibility ranges
- consumer engine compatibility ranges

Knowledge Assets declare:

- owning module version
- referenced assets where needed

Control-plane components declare compatibility with standards and adjacent layers.

---

# 4. Validate Dependency

Validation must prove:

- dependency endpoints exist or are explicitly ranged
- no forbidden required cycles among modules
- direction rules are respected
- compatibility status is not Unknown for production publication
- evidence dependencies do not claim ownership of upstream domains

---

# 5. Register and Publish

Dependencies become consumable only after Registry registration and publication gates pass.

Unregistered dependencies are invisible to production SDK consumers.

---

# 6. Runtime Resolution Lifecycle

For one analysis / interpretation / report request:

1. SDK receives consumer request
2. ResolveVersion / ResolveDependency compute closure
3. Loader loads and freezes KnowledgeSnapshot
4. Engines consume ModuleView / AssetView
5. Session ends; cache retention follows policy without breaking freeze history of completed results

---

# 7. Deprecation and Migration

When a dependency target is deprecated:

- dependents remain resolvable during compatibility windows
- successors must be declared
- Compatibility Matrix updates are mandatory
- engines are notified through governance records

Breaking dependency removals require MAJOR version impact on affected modules and migration notes.

---

# 8. Retirement

Retired dependency targets reject new production bindings.

Historical KnowledgeReferences remain resolvable according to retention policy.

---

# 9. Engine Pipeline vs Knowledge Dependency Lifecycle

Engine pipeline order (Strength → … → Luck → Interpretation → Report) is runtime execution order.

Knowledge dependency lifecycle is publication/resolution order.

They are related but not identical and must not be conflated.

---

# 10. Acceptance Criteria

Lifecycle is accepted when declare → validate → publish → resolve → consume → deprecate → retire controls are complete.
