# Knowledge Loader Architecture

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of the Knowledge Loader.

---

# 2. Architectural Goals

The Loader shall:

- isolate Runtime Engines from Knowledge storage and packaging details;
- load only Registry-published knowledge identities;
- resolve versions and dependencies deterministically for a request;
- validate integrity and compatibility before exposing knowledge to engines;
- support caching without altering knowledge semantics;
- never execute or interpret business knowledge.

---

# 3. Layer Position

```text
Knowledge Registry
        │
        ▼
Knowledge Loader
        │
        ├── Version Resolver
        ├── Dependency Resolver
        ├── Module Loader
        ├── Asset Loader
        ├── Integrity Validator
        ├── Compatibility Checker
        ├── Cache Manager
        ├── Error Handler
        │
        ▼
Runtime Engines
 (Analysis / Interpretation / Report / other consumers)
```

---

# 4. Separation of Concerns

## Knowledge Loader Owns

- module and asset loading into runtime memory
- version selection for a request
- dependency resolution collaboration with Registry declarations
- cache lifecycle for loaded snapshots
- pre-bind validation and integrity checks
- stable GetKnowledge / GetAsset access for engines

## Knowledge Loader Does Not Own

- Knowledge Registry catalog authorship
- business-rule evaluation
- engine scoring / matching / narrative generation
- knowledge content mutation
- physical repository path contracts as public API

## Knowledge Registry Owns

- module/asset catalog
- published versions
- dependency and compatibility declarations

## Runtime Engines Own

- consumption of loaded knowledge through Loader APIs
- domain evaluation using loaded KnowledgeReferences

---

# 5. Logical Subsystems

| Subsystem | Responsibility |
|-----------|----------------|
| Version Resolver | Select compatible versions |
| Dependency Resolver | Resolve required dependency closure |
| Module Loader | Load / unload / reload modules |
| Asset Loader | Load / unload assets |
| Integrity Validator | Check integrity references and structural loadability |
| Compatibility Checker | Validate consumer–module compatibility |
| Cache Manager | Cache, invalidate, refresh loaded snapshots |
| Access Facade | Expose GetKnowledge / GetAsset to engines |
| Error Handler | Classify and surface load failures |

---

# 6. Identity Model

Loading is keyed by logical identities:

- module_id
- asset_id
- version
- KnowledgeReference

Physical location is an internal resolution detail and never part of the public Loader contract.

---

# 7. Request Binding

For one analysis request, the Loader shall:

1. resolve a consistent knowledge snapshot set;
2. freeze selected versions for the request;
3. expose only that frozen set to participating engines.

Mid-request silent version drift is forbidden.

---

# 8. Constraints

- Engines must not bypass the Loader.
- Loader must not execute rules.
- Loader must not interpret knowledge meaning.
- Failures are explicit; silent fallback to stale incompatible knowledge is forbidden unless a governed recovery policy explicitly allows a declared compatible substitute.
