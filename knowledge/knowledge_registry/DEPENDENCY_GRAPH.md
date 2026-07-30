# Knowledge Registry Dependency Graph

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Dependency Graph Specification)

---

# 1. Purpose

This document defines the Registry Dependency Graph used for dependency declaration and resolution.

---

# 2. Graph Model

```text
Node = Knowledge Module Version
     or Knowledge Asset Version (optional fine-grained edges)

Edge = Declared Dependency
```

Edges are directed from dependent → dependency.

Example:

```text
useful_god_knowledge@1.0.0 → fundamental_knowledge@1.x
pattern_knowledge@1.0.0 → fundamental_knowledge@1.x
luck_knowledge@1.0.0 → fundamental_knowledge@1.x
```

---

# 3. Allowed Dependency Types

| Type | Meaning |
|------|---------|
| module_requires_module | Module depends on another module |
| module_requires_standard | Module depends on KMS / KAS / Architecture range |
| asset_requires_asset | Optional fine-grained asset dependency |
| consumer_requires_module | Declared engine consumer dependency range |

---

# 4. Dependency Declaration Fields

Each edge shall include:

- from_id / from_version_range
- to_id / to_version_range
- dependency_type
- strength (required / optional)
- compatibility_notes
- declared_by
- declared_at

---

# 5. Resolution Principles

Dependency Resolution shall:

1. select compatible versions within declared ranges;
2. reject unresolved required dependencies;
3. detect cycles among required module dependencies;
4. produce a deterministic resolved set for a request;
5. expose KnowledgeReferences for the resolved set.

Resolution algorithms are logical contracts only; runtime implementation belongs to Knowledge Loader collaboration.

---

# 6. Cycle Policy

Required dependency cycles are forbidden.

Optional cycles, if ever declared, must be explicitly justified and must not block deterministic resolution.

---

# 7. Non-Goals

The Dependency Graph does not:

- execute knowledge
- reorder engine pipeline stages
- invent undeclared dependencies
- bind to physical package locations

---

# 8. Acceptance Criteria

Dependency Graph is accepted when node/edge model, dependency types, resolution principles, and cycle policy are complete and deterministic.
