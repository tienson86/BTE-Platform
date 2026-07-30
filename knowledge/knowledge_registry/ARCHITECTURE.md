# Knowledge Registry Architecture

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of the Knowledge Registry.

---

# 2. Architectural Goals

The Registry shall:

- serve as the single canonical catalog of Knowledge Modules;
- index Knowledge Assets belonging to registered modules;
- manage versions, dependencies, and compatibility;
- support discovery and search without executing knowledge;
- remain independent of physical storage layout;
- remain independent of Runtime Engine execution.

---

# 3. Layer Position

```text
Knowledge Architecture
        │
        ▼
Knowledge Module Standard (KMS)
        │
        ▼
Knowledge Asset Standard (KAS)
        │
        ▼
Knowledge Registry
        │
        ├── Module Registry
        ├── Asset Registry
        ├── Metadata Index
        ├── Dependency Graph
        ├── Compatibility Matrix
        ├── Version Catalog
        ├── Discovery Services
        ├── Validation Services
        ├── Governance Controls
        │
        ▼
Knowledge Loader
        │
        ▼
Runtime Engine
```

---

# 4. Separation of Concerns

## Knowledge Registry Owns

- module catalog entries
- asset catalog entries
- registry metadata and indexes
- dependency graphs
- compatibility matrices
- version catalogs
- discovery and search contracts
- registration validation
- lifecycle governance records

## Knowledge Registry Does Not Own

- knowledge content authoring
- rule evaluation
- formula execution
- engine matching mechanics
- AnalysisContext orchestration
- physical packaging formats as public contracts

## Knowledge Loader Owns

- resolution of selected module versions for a request
- binding of abstract module identities to loadable snapshots

## Runtime Engine Owns

- consumption of resolved knowledge through abstract interfaces
- application of knowledge during evaluation

---

# 5. Logical Subsystems

| Subsystem | Responsibility |
|-----------|----------------|
| Module Registry | Catalog of Knowledge Modules |
| Asset Registry | Catalog of Knowledge Assets |
| Metadata Index | Searchable metadata store |
| Dependency Graph | Declared dependency relationships |
| Compatibility Matrix | Compatibility declarations and checks |
| Version Catalog | Module and asset version histories |
| Discovery Service | Find / list / search operations |
| Validation Service | Registration and compatibility validation |
| Governance Service | Lifecycle and change-control records |

---

# 6. Identity Model

All registry entries are identified by logical identifiers:

- registry_id
- module_id
- asset_id
- version

Physical location is never part of public identity.

---

# 7. Knowledge Flow

```text
Author / Publish Knowledge Module
        │
        ▼
Register Module and Assets in Registry
        │
        ▼
Validate Metadata, Dependencies, Compatibility
        │
        ▼
Publish Catalog Entry
        │
        ▼
Knowledge Loader discovers and resolves versions
        │
        ▼
Runtime Engine consumes resolved Knowledge Snapshot
```

---

# 8. Constraints

- One canonical Knowledge Registry for the platform.
- No runtime rule execution inside the Registry.
- No repository-path public contracts.
- No duplication of KMS / KAS semantic ownership.
- Registry manages catalog state, not domain knowledge content.
