# Knowledge Taxonomy & Ontology

| Field | Value |
|-------|-------|
| **Document** | KNOWLEDGE_TAXONOMY_ONTOLOGY |
| **Sprint** | KD-2 |
| **Version** | 1.0.0 |
| **Status** | Canonical reference |

---

## 1. Purpose

This document explains the combined taxonomy and ontology architecture for BTE Knowledge Database V2.

It is the canonical reference for future knowledge package design, AI-assisted authoring, validation, and package-based deployment.

---

## 2. Taxonomy philosophy

Taxonomy organizes knowledge into stable domains and a deterministic hierarchy:

```
Domain → Category → Knowledge Package → Knowledge Record → Rule → Condition → Result
```

Principles:

- one primary domain per object
- extensible reserved domains for Feng Shui / Qi Men / I Ching
- multilingual via language axis, not via ID mutation
- compatible with existing V1 packages and KD-1 architecture

Source of truth: `knowledge/taxonomy/`

---

## 3. Ontology philosophy

Ontology defines meaning:

- specialization / generalization
- equivalence
- aggregation / composition
- override semantics

Structural relations (contains, belongs_to, depends_on) are distinct from semantic relations (inherits, specializes, equivalent_to).

Source of truth: `knowledge/ontology/`

---

## 4. Relationship model

Supported structural relationships include:

`contains`, `references`, `depends_on`, `extends`, `inherits`, `overrides`, `conflicts_with`, `requires`, `belongs_to`, `generated_from`, `validated_by`

Each relationship declares source, target, cardinality, direction, and semantics.

---

## 5. Dependency model

Dependency kinds:

- package dependency
- domain dependency
- rule dependency
- metadata dependency

Circular dependencies are prohibited by default.  
Resolution is deterministic topological ordering with stable ID tie-breaks.

---

## 6. Override strategy

Override classes in precedence order:

1. priority override
2. package override
3. version override
4. project override

Resolution never mutates overridden objects; it emits deterministic winners.

---

## 7. Semantic evolution strategy

1. Prefer additive specialization.
2. Map multilingual and school variants through equivalence links.
3. Deprecate instead of deleting released knowledge.
4. Use migration manifests for breaking parent/identity changes.
5. Scale to 100,000+ records through indexes and package deployment, not monolithic files.

---

## 8. Compatibility guarantees

- Existing Knowledge Database V2 files remain untouched.
- Existing Rule Database packages remain untouched.
- Rule Engine / Analysis / Interpretation / API remain untouched.
- Dual-read compatibility with V1 envelopes remains required until a future migration.

---

## 9. Related artifacts

- `knowledge/taxonomy/*`
- `knowledge/ontology/*`
- `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md`
- `knowledge/docs/architecture/KD1_AUDIT_REPORT.md`
