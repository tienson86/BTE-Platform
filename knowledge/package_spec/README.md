# Knowledge Package Specification

| Field | Value |
|-------|-------|
| **Sprint** | KD-3 |
| **Spec version** | 1.0.0 |
| **Schema version** | 2.0.0 |
| **Status** | Canonical |
| **Scope** | Architecture and specification only |

A **Knowledge Package** is the smallest independently versioned, validated, and deployable knowledge unit on the BTE Platform.

After this sprint, all future knowledge (rules, interpretation templates, report templates, metadata, sentence libraries, and analytical packages) MUST follow this specification.

This folder does **not** replace existing Rule Database packages or Knowledge Database V2 schemas. It defines the additive packaging standard those trees will migrate toward.

---

## Contents

| File | Role |
|------|------|
| `PACKAGE_SPECIFICATION.md` | Canonical specification |
| `package.schema.json` | Package identity envelope |
| `package_manifest.schema.json` | Manifest |
| `package_index.schema.json` | Deployment catalog |
| `package_dependency.schema.json` | Dependency declaration |
| `package_release.schema.json` | Release record |
| `package_validation.schema.json` | Validation profiles and reports |
| `lifecycle.md` | Package lifecycle |
| `versioning.md` | Versioning strategy |
| `compatibility.md` | Compatibility and dual-read |
| `packaging_guidelines.md` | Anatomy and folder layout |
| `release_process.md` | Release model |
| `naming_rules.md` | Deterministic naming |
| `package_examples/` | Conforming example packages |

Architecture summary also lives at:

`knowledge/docs/architecture/KNOWLEDGE_PACKAGE_SPECIFICATION.md`

---

## Related canonical sources

- Knowledge Database V2 — `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md`
- Taxonomy & Ontology — `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md`
- V1 Rule Database packages — `knowledge/rule_database/` (unchanged)
- KD-1 package envelope — `knowledge/schema/v2/knowledge_package.schema.json` (unchanged)
