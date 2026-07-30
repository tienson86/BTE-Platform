# Knowledge Dependency Model

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Dependency Model Specification)

---

# 1. Purpose

This document enumerates canonical dependency edges among all in-scope components.

---

# 2. Dependency Edge Schema

Each dependency edge includes:

| Field | Meaning |
|-------|---------|
| from | Dependent subject |
| to | Dependency subject |
| type | Dependency type |
| strength | required / optional / evidence |
| direction_rule | Allowed architectural direction |
| notes | Clarifying constraint |

---

# 3. Dependency Types

| Type | Meaning |
|------|---------|
| standards_conformance | Subject must conform to a standard |
| catalog_registration | Subject is registered/indexed by catalog |
| runtime_resolution | Subject resolves/loads via another subject |
| public_facade | Subject is accessed only through facade |
| module_requires_module | Knowledge Module depends on another module |
| asset_owned_by_module | Asset belongs to a module version |
| asset_references_asset | Asset references another asset |
| engine_consumes_sdk | Engine consumes knowledge via SDK |
| stage_consumes_module | Analysis stage consumes a domain module via SDK |
| evidence_reference | Uses published upstream classification concepts |

---

# 4. Standards Dependencies

| From | To | Type | Strength |
|------|----|------|----------|
| Knowledge Modules | Knowledge Architecture | standards_conformance | required |
| Knowledge Modules | KMS | standards_conformance | required |
| Knowledge Assets | KAS | standards_conformance | required |
| Knowledge Registry | Knowledge Architecture / KMS / KAS | standards_conformance | required |
| Knowledge Loader | Knowledge Registry contracts | standards_conformance | required |
| Knowledge SDK | Knowledge Loader + Registry contracts | standards_conformance | required |

---

# 5. Control-Plane Dependencies

| From | To | Type | Strength |
|------|----|------|----------|
| Knowledge Modules | Knowledge Registry | catalog_registration | required (for publish/consume) |
| Knowledge Assets | Knowledge Registry | catalog_registration | required (for publish/consume) |
| Knowledge Loader | Knowledge Registry | runtime_resolution | required |
| Knowledge SDK | Knowledge Loader | runtime_resolution | required |
| Knowledge SDK | Knowledge Registry | runtime_resolution | required (discovery/metadata) |
| Analysis Engine | Knowledge SDK | engine_consumes_sdk / public_facade | required |
| Interpretation Engine | Knowledge SDK | engine_consumes_sdk / public_facade | required |
| Report Engine | Knowledge SDK | engine_consumes_sdk / public_facade | required |

---

# 6. Knowledge Module → Knowledge Module Dependencies

| From | To | Type | Strength |
|------|----|------|----------|
| Strength Knowledge | Fundamental Knowledge | module_requires_module | required |
| Temperature Knowledge | Fundamental Knowledge | module_requires_module | required |
| Pattern Knowledge | Fundamental Knowledge | module_requires_module | required |
| Useful God Knowledge | Fundamental Knowledge | module_requires_module | required |
| Ten Gods Knowledge | Fundamental Knowledge | module_requires_module | required |
| Combination Knowledge | Fundamental Knowledge | module_requires_module | required |
| ShenSha Knowledge | Fundamental Knowledge | module_requires_module | required |
| Luck Knowledge | Fundamental Knowledge | module_requires_module | required |

Evidence dependencies (non-owning):

| From | To | Type | Strength |
|------|----|------|----------|
| Pattern Knowledge | Strength Knowledge | evidence_reference | optional/declared |
| Pattern Knowledge | Temperature Knowledge | evidence_reference | optional/declared |
| Useful God Knowledge | Strength Knowledge | evidence_reference | optional/declared |
| Useful God Knowledge | Temperature Knowledge | evidence_reference | optional/declared |
| Useful God Knowledge | Pattern Knowledge | evidence_reference | optional/declared |
| Ten Gods Knowledge | Strength Knowledge | evidence_reference | optional/declared |
| Ten Gods Knowledge | Pattern Knowledge | evidence_reference | optional/declared |
| Ten Gods Knowledge | Useful God Knowledge | evidence_reference | optional/declared |
| Luck Knowledge | Strength / Temperature / Pattern / Useful God / Ten Gods / Combination / ShenSha Knowledge | evidence_reference | optional/declared |

Evidence references do not authorize recomputation of the referenced domain.

---

# 7. Knowledge Asset Dependencies

| From | To | Type | Strength |
|------|----|------|----------|
| Any Knowledge Asset | Owning Knowledge Module version | asset_owned_by_module | required |
| Rule / Table / Formula Assets | Terminology / Reference / Mapping Assets | asset_references_asset | optional/declared |
| Golden / Validation Datasets | Participating Assets | asset_references_asset | required for those datasets |
| Manifest | Declared Asset set of module version | asset_references_asset | required |

---

# 8. Analysis Engine Stage → Module Dependencies

Accessed exclusively through Knowledge SDK:

| Stage / Concern | Primary Knowledge Module |
|-----------------|--------------------------|
| Strength Engine | Strength Knowledge |
| Temperature Engine | Temperature Knowledge |
| Pattern Engine | Pattern Knowledge |
| Useful God Engine | Useful God Knowledge |
| Ten Gods Engine | Ten Gods Knowledge |
| Combination Engine | Combination Knowledge |
| ShenSha Engine | ShenSha Knowledge |
| Luck Engine | Luck Knowledge |
| Shared fundamentals as needed | Fundamental Knowledge |

Stages may read upstream published engine results from AnalysisContext; that is engine-pipeline data dependency, distinct from Knowledge Module dependency.

---

# 9. Interpretation and Report Dependencies

| From | To | Type | Strength |
|------|----|------|----------|
| Interpretation Engine | Knowledge SDK | public_facade | required |
| Interpretation Engine | Interpretation / Sentence Knowledge Modules | stage_consumes_module via SDK | required when those modules are published |
| Report Engine | Knowledge SDK | public_facade | required |
| Report Engine | Report Template Knowledge Modules | stage_consumes_module via SDK | required when those modules are published |

Interpretation and Report Engines may reference analytical KnowledgeReferences for explainability but must not recompute Analysis Engine domains.

---

# 10. Complete Directed Summary

```text
Standards ← Modules / Assets / Registry / Loader / SDK
Modules → Fundamental (required)
Modules → Upstream analytical modules (evidence only, where declared)
Assets → Owning Module (required)
Modules/Assets → Registry (registration)
Loader → Registry
SDK → Loader
SDK → Registry (discovery/metadata)
Analysis / Interpretation / Report Engines → SDK
SDK-selected Modules → Engines (content consumption only via SDK views)
```

---

# 11. Acceptance Criteria

Dependency Model is accepted when all required edges, evidence edges, forbidden directions, and stage-to-module mappings are complete and unambiguous.
