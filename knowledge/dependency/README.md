# BTE Knowledge Dependency — Specification

**Sprint:** 4C  
**Location:** `knowledge/dependency/`  
**Status:** Specification only (no resolver / no runtime graph engine)

---

## Purpose

Define dependency levels and policies between Knowledge Records: Hard, Soft, Reference, Inheritance, Extension, and Semantic Dependency.

Complements `knowledge/graph/` (ontology/edges) and `knowledge/index/cross_reference_index.json` (lookup). This folder is the **level & policy** SSOT.

---

## Folder tree

```text
knowledge/dependency/
├── README.md
├── dependency_levels.json
├── dependency_rules.json
├── inheritance_rules.json
├── override_policy.json
├── reference_policy.json
├── semantic_dependency.json
└── examples/
    └── dependency_pack01_example.json
```

---

## Dependency Levels

| Level | Role |
|-------|------|
| Hard Dependency | Blocking; required for official release; cycle-checked |
| Soft Dependency | Optional completeness; warning if missing |
| Reference | Citation / pointer; not a release hard-gate |
| Inheritance | Structural/classificatory parentage |
| Extension | Additive scope on a named base record |
| Semantic Dependency | Meaning presupposition; document & warn |

Defined in `dependency_levels.json`.

---

## Document map

| File | Role |
|------|------|
| `dependency_rules.json` | Cross-cutting DEP-R-* rules |
| `inheritance_rules.json` | Inheritance kinds + INH-* |
| `override_policy.json` | When levels may be waived |
| `reference_policy.json` | Reference-level REF-* policy |
| `semantic_dependency.json` | Semantic Dependency SEM-* |
| `examples/` | Illustrative Pack 01-shaped declarations |

---

## Interaction with graph edges

Dependency **levels** classify intent. Graph **edge types** (`FOUNDATIONAL_FOR`, `DEPENDS_ON`, …) remain the ontology vocabulary. A single relationship MAY carry both an edge type and a level_id in tooling that consumes both specs.

---

## Out of scope

- Dependency resolver implementation
- Compiler plugin
- Mutation of `knowledge/bazi/**` records
