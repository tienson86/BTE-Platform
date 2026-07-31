# BTE Knowledge Ontology Infrastructure

**Sprint:** 5B  
**Location:** `knowledge/ontology/`  
**Version:** 1.0.0  
**Status:** Official (specification)  
**Runtime:** Not included

---

## Purpose

Provide the **global ontology SSOT** for the entire BTE Knowledge Canon.

Every future Knowledge Record SHALL reference this ontology for:

- ontology classes
- entity types
- relationship types
- node / edge categories
- namespaces
- semantic levels
- property definitions

Records MUST NOT invent private ontology vocabularies that conflict with this registry.

---

## Architecture

```text
knowledge/ontology/
        │
        ├── ontology_schema.json          ← Draft 2020-12 master schema
        ├── ontology_classes.json         ← classes (OCL-*)
        ├── entity_types.json             ← entity types (ENTT-*)
        ├── relationship_types.json       ← relationships (RELTYPE-*)
        ├── relationship_constraints.json
        ├── property_definitions.json
        ├── node_types.json               ← graph node categories (NODE-*)
        ├── edge_types.json               ← graph edge categories (EDGECAT-*)
        ├── semantic_levels.json
        ├── namespace_registry.json        ← NS-*
        ├── ONTOLOGY_SPEC.md
        └── examples/
```

Compatibility bridges:

- `compatible_graph_node` / `compatible_graph_edge` map to `knowledge/graph/` vocabularies.
- Relationship types include graph edges (`FOUNDATIONAL_FOR`, `DEPENDS_ON`, …) plus expanded ontology relations.

---

## Design Principles

1. **Single vocabulary** — one canonical name per class/type/relationship.
2. **Immutable IDs** — `OCL-*`, `ENTT-*`, `RELTYPE-*`, `NODE-*`, `EDGECAT-*`, `NS-*` do not remap meaning after official.
3. **Explicit inheritance** — classes declare `parent_class`; cycles forbidden.
4. **Typed relationships** — direction, inverse, allowed source/target.
5. **Graph compatibility** — ontology extends, does not break, Sprint 3B graph types.
6. **Specification first** — no runtime ontology engine in this sprint.

---

## Scope

In scope: declarative ontology registries and documentation.  
Out of scope: Python, compiler, validator engine, knowledge-graph runtime, analysis/rule engines.

Does **not** modify: governance, validation, consistency, manifest, templates, or Golden Knowledge Records.

---

## Coverage (v1.0.0)

| Registry | Count (approx.) |
|----------|-----------------|
| Ontology classes | 50 |
| Entity types | 36 |
| Relationship types | 101 |
| Properties | 129 |
| Node types | 18 |
| Edge categories | 10 |
| Semantic levels | 8 |
| Namespaces | 20 |

---

## Dependencies

Consumes concepts from (read-only compatibility):

- `knowledge/graph/`
- `knowledge/validation/`
- `knowledge/consistency/`
- `knowledge/manifest/`
- `knowledge/package/`
- `knowledge/dependency/`

---

## Compatibility

Compatible with Golden Records KR-000001…KR-000005 and Pack 01 packaging/manifests.  
Future KR authoring SHALL bind `ontology_class` / `entity_type` / relationship names from this folder.

---

## Future Usage

- KR templates reference ontology class & entity type IDs
- Compiler resolves relationship types via `relationship_types.json`
- Graph projection uses `node_types` / `edge_types` categories
- Validation engine checks `relationship_constraints.json` (ONT-C-*)
- Search/docs use namespaces and semantic levels for browse facets

---

## Documents

| File | Role |
|------|------|
| [ONTOLOGY_SPEC.md](ONTOLOGY_SPEC.md) | Philosophy, naming, policies, expectations |
| [ontology_schema.json](ontology_schema.json) | Schema for all registry (+ example) JSON |
| [examples/](examples/) | Binding / relationship / graph illustrations |
