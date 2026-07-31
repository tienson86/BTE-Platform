# BTE Ontology Specification

**Document:** ONTOLOGY_SPEC  
**Version:** 1.0.0  
**Status:** Official  
**Location:** `knowledge/ontology/`

---

## 1. Ontology philosophy

The BTE Knowledge Ontology is the shared semantic backbone of the Knowledge Canon.

It separates:

- **What kind of thing something is** (ontology class / entity type)
- **How things relate** (relationship types / edge categories)
- **Where things live** (namespaces / packages / modules)
- **How deep they sit academically** (semantic levels)
- **What attributes they may carry** (property definitions)

Golden Knowledge Records express academic content; this ontology expresses reusable vocabulary. Records SHALL reuse, not redefine, that vocabulary.

---

## 2. Naming conventions

| Kind | ID pattern | Canonical name form |
|------|------------|---------------------|
| Ontology class | `OCL-NNNNNN` | PascalCase (`DynamicConcept`) |
| Entity type | `ENTT-NNNNNN` | PascalCase (`HeavenlyStem`) |
| Relationship type | `RELTYPE-NNNNNN` | UPPER_SNAKE (`FOUNDATIONAL_FOR`) |
| Node type | `NODE-NNNNNN` | PascalCase (`KnowledgeRecord`) |
| Edge category | `EDGECAT-NNNNNN` | PascalCase (`Dependency`) |
| Namespace | `NS-NNNNNN` | dotted lowercase (`bazi.pack01`) |
| Property | (name only) | snake_case (`record_id`) |

Rules:

1. Canonical names are unique within their registry.
2. IDs are immutable after `official` status.
3. Graph-compatible relationship names keep historical UPPER_SNAKE forms used in `knowledge/graph/`.

---

## 3. Inheritance rules

1. Every class except `Thing` SHOULD declare `parent_class` referencing an `OCL-*` id.
2. Class inheritance MUST be acyclic (constraint ONT-C-001).
3. Child classes inherit semantic intent; they do not automatically inherit all properties — properties are bound explicitly via `applies_to` / authoring templates.
4. Multi-inheritance of classes is out of scope for v1.0.0 (single parent only).

---

## 4. Relationship rules

1. Use only names registered in `relationship_types.json`.
2. Honor `direction` and `inverse_relationship` when materializing graphs.
3. `allowed_source` / `allowed_target` of `["*"]` means unrestricted within registered node/entity kinds; future revisions MAY narrow wildcards.
4. Duplicate `(type, source, target)` triples are forbidden (ONT-C-003).
5. `FOUNDATIONAL_FOR` and `DEPENDS_ON` remain acyclic (ONT-C-005), aligning with graph and dependency frameworks.
6. Prefer precise types over `RELATED_TO` / `ASSOCIATED_WITH` when meaning is known.

---

## 5. Property conventions

1. Property names are global snake_case identifiers.
2. `required` and `immutable` are declared per property; identity fields (`record_id`, `entity_id`) are immutable.
3. Enumerated properties list `enum_values` when datatype is `enum`.
4. Records MAY omit optional properties; required properties MUST be present for the applying artifact type when that type is in `applies_to`.
5. Do not invent parallel property names for the same meaning (`name` vs `canonical_name` — use the registered property).

---

## 6. Namespace policy

1. All new packs/modules SHOULD register a namespace under `namespace_registry.json`.
2. Namespace strings are dotted lowercase tokens owned by a team/role.
3. `bazi.pack01` is the namespace for Pack 01 fundamental records.
4. Cross-namespace references are allowed via relationship types; they do not merge namespaces.

---

## 7. Version policy

1. Ontology registries use SemVer at document and entry level (`version` fields).
2. v1.0.0 is the first official baseline of Sprint 5B.
3. Adding optional classes/types/properties is MINOR.
4. Renaming or removing official vocabulary is MAJOR and requires governance change request.
5. Deprecate via `status=deprecated` before removal in a later major version.

---

## 8. Compatibility policy

1. This ontology is compatible with:
   - `knowledge/graph/` node/edge types (via compatibility fields)
   - `knowledge/validation/` VAL-* expectations for types/relationships
   - `knowledge/consistency/` ontology consistency rules
   - `knowledge/dependency/` dependency levels (semantic overlay, not a replacement)
   - `knowledge/manifest/` and `knowledge/package/` discovery units
2. Sprint 5B does **not** modify those folders.
3. When vocabulary differs historically (e.g. prose `SUPPORTS`), map to registered `SUPPORTED_BY` / `SUPPORTS` pair at index time.

---

## 9. Compiler expectations

Future compilers SHALL:

1. Load `ontology_schema.json` and registry documents during LOAD/VALIDATE.
2. Resolve relationship names through `relationship_types.json`.
3. Reject unknown relationship types and unknown ontology classes on official compile.
4. Emit graph artifacts tagged with `NODE-*` / `EDGECAT-*` categories.
5. Treat ontology registries as read-only inputs (Database/ontology First — no write-back from engines).

---

## 10. Knowledge Graph expectations

1. Nodes map to `node_types.json` categories and optionally `compatible_graph_node` values used by `knowledge/graph/`.
2. Edges map to `edge_types.json` categories; fine-grained meaning uses `relationship_types.json`.
3. Graph constraints in `relationship_constraints.json` complement `knowledge/graph/graph_constraints.json`.
4. Orphan and cycle policies align across ontology and graph specs.

---

## 11. Validation expectations

Future validation engines SHALL treat ONT-C-* constraints as ontology-layer rules, distinct from but complementary to VAL-* codes.

At minimum enforce:

- unique class / relationship names
- acyclic inheritance
- no duplicate relationship triples
- immutable identity properties
- registered namespaces when declared

---

## 12. Semantic levels

```text
Level 1 Principles
  → Level 2 Concepts
    → Level 3 Classification
      → Level 4 Entity Collections
        → Level 5 Entities
          → Level 6 Relationships
            → Level 7 Rules
              → Level 8 Interpretation
```

Pack 01 foundations (Yin Yang, Qi, Wu Xing, Stems, Branches) occupy levels 1–5 primarily.

---

## 13. Authoring rule

New Knowledge Records SHALL:

1. Select an `ontology_class` / `entity_type` from this ontology.
2. Use only registered relationship type names.
3. Prefer registered properties for metadata fields.
4. Declare namespace (typically `bazi.packNN`).
5. Avoid embedding a private ontology section that redefines global terms.

---

## 14. Non-goals (v1.0.0)

- OWL/RDF export runtime
- Automated reasoner
- Mutation of Golden Records to inject ontology IDs (deferred to an authoring/migration sprint)
- Python or compiler implementation
