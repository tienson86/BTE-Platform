# Dependency Rules

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Dependency Standard)

---

# 1. Purpose

This document defines dependency rules among Knowledge Modules and between Knowledge Modules and Runtime Engines.

---

# 2. Dependency Principles

Dependencies shall be:

- explicit
- directional
- versioned
- acyclic
- minimal
- abstract

---

# 3. Allowed Dependencies

Knowledge Modules may depend on:

- Fundamental Knowledge
- Shared Terminology
- Shared Metadata
- Shared Formula Library
- other upstream Knowledge Modules declared in the canonical dependency direction

Runtime Engines may depend on:

- Abstract Knowledge Modules
- Abstract Knowledge Asset interfaces

---

# 4. Forbidden Dependencies

Knowledge Modules shall never depend directly on Runtime Engines.

Also forbidden:

```text
Knowledge Module → Engine internals
Runtime Engine → Physical repository path
Knowledge Module → Downstream Knowledge Module
Circular Knowledge Module dependencies
Runtime Engine → Unpublished Knowledge Module
```

---

# 5. Canonical Dependency Direction

```text
Fundamental Knowledge
        │
        ├── Strength Knowledge
        ├── Temperature Knowledge
        ├── Pattern Knowledge
        ├── Useful God Knowledge
        ├── Ten Gods Knowledge
        ├── Combination Knowledge
        ├── ShenSha Knowledge
        └── Luck Knowledge
                │
                ▼
        Interpretation Knowledge
                │
                ▼
        Report Knowledge
```

---

# 6. Engine Mapping Rules

Each Analysis Engine stage depends on exactly one primary Knowledge Module for its domain.

Shared fundamentals are consumed through Fundamental Knowledge or declared upstream references.

Engines shall not import another stage's Knowledge Module as a substitute for their own domain module.

---

# 7. Declaration Requirements

Every Knowledge Module shall declare dependencies in:

- Metadata
- Manifest
- Dependencies documentation

Each dependency entry shall include:

- module_id
- relationship type
- compatible version range
- required / optional flag

---

# 8. Reference vs Duplication

If knowledge already exists upstream:

- reference it;
- do not copy it;
- do not redefine it with a new identity.

Duplication is a governance defect.

---

# 9. Optional Dependencies

Optional dependencies may enrich a module but must not be required for mandatory publication behavior unless declared required.

---

# 10. Acceptance Criteria

Dependency rules are satisfied when:

- all dependencies are declared;
- graph is acyclic;
- version ranges resolve;
- no Runtime Engine dependency exists from Knowledge Modules;
- no path-coupled engine dependency exists.
