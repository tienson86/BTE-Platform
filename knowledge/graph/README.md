# BTE Knowledge Graph — Specification

**Sprint:** 3B  
**Location:** `knowledge/graph/`  
**Status:** Specification only (no runtime implementation)

---

## Purpose

Declarative ontology and document schema for the BTE Knowledge Graph: node types, edge types, hard constraints, and a Draft 2020-12 graph document schema.

This sprint does **not** ship a graph engine, validator binary, compiler plugin, or database.

---

## Folder tree

```text
knowledge/graph/
├── README.md
├── node_types.json
├── edge_types.json
├── graph_constraints.json
├── graph_schema.json
├── ontology_registry.json
└── examples/
    └── graph_infrastructure_example.json
```

---

## Node types

| Type | Role |
|------|------|
| Concept | Canonical academic concept (typically `KR-*`) |
| Entity | Non-concept named entity |
| Rule | Formal rule node |
| Pattern | Structural / interpretive pattern |
| Example | Illustrative example (`EX-*`) |
| Source | Bibliography source (`SRC-*`) |
| Pack | Pack container (`PACK_NN`) |
| Module | Module container |

Defined in `node_types.json`.

---

## Edge types

| Type | Role |
|------|------|
| FOUNDATIONAL_FOR | Academic foundation toward target |
| DEPENDS_ON | Structural / academic dependency |
| CLASSIFIES | Classification applied to target |
| REFERENCES | Citation / pointer without dependency |
| SUPPORTED_BY | Support from source or related node |
| RELATED_TO | Non-hierarchical association |
| CONFLICTS_WITH | Tracked incompatibility |
| IMPLEMENTS | Realization / operationalization mapping |

Defined in `edge_types.json`.

`FOUNDATIONAL_FOR` and `DEPENDS_ON` participate in the acyclicity constraint.

---

## Constraints

| ID | Name |
|----|------|
| GRAPH-C-001 | No cyclic dependency |
| GRAPH-C-002 | Unique Canonical Node |
| GRAPH-C-003 | Immutable Record ID |
| GRAPH-C-004 | No duplicate relationships |

Defined in `graph_constraints.json`. Enforcement is deferred.

---

## Schema & registry

- `graph_schema.json` — JSON Schema Draft 2020-12 for a graph document (`GRAPH-*`, nodes, edges).
- `ontology_registry.json` — index of type IDs, constraint IDs, document paths, and ID conventions.

---

## Examples

`examples/graph_infrastructure_example.json` is a **synthetic** subgraph for shape illustration. It is not academic canon and does not modify any Knowledge Record.

---

## Out of scope (Sprint 3B)

- Graph database / query runtime
- Cycle detection code
- Compiler integration
- Changes to `knowledge/bazi/**`, bibliography, compiler, or authored Knowledge Records
