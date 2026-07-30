# Knowledge Versioning

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Versioning Policy)

---

# 1. Purpose

This document defines versioning and compatibility policy for the Knowledge Layer and its consumers.

---

# 2. Versioning Scheme

Knowledge Modules follow Semantic Versioning (SemVer):

```text
MAJOR.MINOR.PATCH
```

| Increment | Meaning |
|-----------|---------|
| MAJOR | Breaking knowledge contract or incompatible semantics |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible corrections |

---

# 3. Version Surfaces

Versioning applies independently to:

- Knowledge Architecture baseline
- each Knowledge Module
- Rule Database packages
- Sentence Library packages
- Report Template packages

Engine Modules declare compatible Knowledge Module version ranges.

---

# 4. Compatibility Rules

Within Version 1.x:

- existing KnowledgeReferences remain resolvable;
- existing mandatory fields remain present;
- existing category meanings remain stable;
- engines depending on abstract modules continue to operate.

Breaking changes require MAJOR version increments.

---

# 5. Engine Compatibility Matrix

Each Knowledge Module publication shall declare:

| Consumer | Compatible Range |
|----------|------------------|
| Target Engine | e.g. >=1.0.0 <2.0.0 |
| Dependent Knowledge Modules | explicit ranges |

Unresolved compatibility blocks publication.

---

# 6. Runtime Version Selection

At analysis start:

1. Engine requests required Knowledge Modules.
2. Registry selects compatible published versions.
3. Snapshot freezes selected versions for the request.
4. Results record selected KnowledgeVersions.

No mid-request version switching is allowed.

---

# 7. Storage Independence and Version Identity

Version identity is logical, not path-based.

A Knowledge Module version remains the same across:

- repository packaging
- distribution bundles
- remote registries

Engines bind to version identity, never to filesystem location.

---

# 8. Deprecation and Sunset

Deprecated versions:

- remain available during a declared compatibility window;
- must advertise successors;
- may be removed only after sunset date and consumer migration.

---

# 9. Architecture Baseline Version

This Knowledge Architecture baseline is:

```text
Version 1.0.0
Status: Frozen Architecture Baseline
```

Changes to architectural principles require a new architecture major version.

---

# 10. Acceptance Criteria

Versioning policy is accepted when:

- every published module carries SemVer identity;
- compatibility matrices are complete;
- engines resolve versions abstractly;
- request-scoped snapshots are reproducible.
