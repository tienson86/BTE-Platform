# BTE Knowledge Ontology

| Field | Value |
|-------|-------|
| **Status** | Canonical architecture |
| **Sprint** | KD-2 |
| **Version** | 1.0.0 |
| **Scope** | Semantic ontology for Knowledge Database V2 |

---

## Purpose

Define semantic inheritance, links, constraints, and override behavior for BTE knowledge.

The ontology complements the taxonomy:

- **Taxonomy** answers “where does this belong?”
- **Ontology** answers “what does this mean, and how does it specialize or override?”

---

## Files

| File | Responsibility |
|------|----------------|
| `ontology.json` | Core concepts and class graph |
| `semantic_links.json` | Semantic (non-structural) relations |
| `inheritance.json` | Specialization / generalization model |
| `constraints.json` | Semantic constraints |
| `override_rules.json` | Deterministic override resolution |
| `reference_model.md` | Ontology reference narrative |
| `examples.md` | Illustrative examples |

---

## Philosophy

1. Distinguish **structural** relationships (contains, belongs_to) from **semantic** relationships (inherits, equivalent_to).
2. Prefer explicit specialization over hidden side effects.
3. Keep released knowledge immutable; overrides create layered resolutions, not silent mutation.
4. Remain compatible with Knowledge Database V2 dual-read of V1 packages.
5. Specification only — no runtime engine code in this sprint.

---

## Related documents

- `knowledge/taxonomy/README.md`
- `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md`
