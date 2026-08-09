# BTE Knowledge Taxonomy

| Field | Value |
|-------|-------|
| **Status** | Canonical architecture |
| **Sprint** | KD-2 |
| **Version** | 1.0.0 |
| **Scope** | Semantic taxonomy for Knowledge Database V2 |

---

## Purpose

Define the canonical classification of all knowledge domains, entities, relationships, hierarchies, dependencies, lifecycle states, and naming rules for the BTE Platform.

This taxonomy is the foundation for every future knowledge package, rule, interpretation template, report template, and AI-assisted authoring tool.

---

## Files

| File | Responsibility |
|------|----------------|
| `domains.json` | Canonical knowledge domains |
| `entities.json` | Canonical knowledge entities |
| `relationships.json` | Structural relationship catalog |
| `hierarchy.json` | Deterministic semantic hierarchy |
| `classifications.json` | Category / family / type axes |
| `dependency_graph.json` | Package/domain/rule/metadata dependency rules |
| `lifecycle.json` | Knowledge lifecycle states |
| `naming_conventions.md` | Stable identifier and naming rules |

---

## Philosophy

1. **Domain-first** — every knowledge object belongs to one primary domain.
2. **Deterministic hierarchy** — Domain → Category → Package → Record → Rule → Condition → Result.
3. **Extensible** — new schools (Feng Shui, Qi Men, I Ching) attach as domains without breaking existing IDs.
4. **Compatible** — existing Knowledge Database V2 architecture and V1 packages remain valid.
5. **No runtime logic** — taxonomy files are specifications and declarative data only.

---

## Related documents

- `knowledge/ontology/README.md`
- `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md`
- `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md`
