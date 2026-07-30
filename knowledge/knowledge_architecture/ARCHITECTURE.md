# Knowledge Layer Architecture

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the BTE Knowledge Layer.

It establishes component boundaries, dependency rules, consumption contracts, extension mechanisms, and separation between Knowledge Modules and Engine Modules.

---

# 2. Architectural Goals

The Knowledge Architecture shall:

- centralize business knowledge outside engine code;
- provide abstract, stable Knowledge Module contracts;
- support domain-oriented organization of knowledge;
- enable independent evolution of knowledge and engines;
- guarantee versioned, reproducible knowledge consumption;
- prevent engines from depending on physical storage paths;
- support rule, sentence, and report-template assets under one governance model.

---

# 3. Layered Platform View

```text
┌──────────────────────────────────────────────┐
│                 Knowledge Layer              │
│  Knowledge Modules · Rule Databases          │
│  Sentence Libraries · Report Templates       │
└───────────────────────┬──────────────────────┘
                        │ abstract contracts
                        ▼
┌──────────────────────────────────────────────┐
│                  Engine Layer                │
│  Calendar · BaZi · Analysis · Interpretation │
│  Report                                      │
└──────────────────────────────────────────────┘
```

Knowledge flows downward into engines.

Engines never write knowledge assets.

---

# 4. Separation of Concerns

## Knowledge Modules

Own:

- business rules
- interpretive content
- report templates
- domain taxonomies
- knowledge metadata
- knowledge versioning

Do not own:

- scoring algorithms
- pipeline orchestration
- chart construction
- runtime state

## Engine Modules

Own:

- validation
- matching mechanics
- scoring mechanics
- priority resolution
- result construction
- execution metadata

Do not own:

- business rule content
- sentence wording
- report layout content
- physical knowledge paths

---

# 5. Abstract Knowledge Module Contract

Every Knowledge Module exposes an abstract contract:

```text
KnowledgeModule
  ├── identity
  ├── version
  ├── domain
  ├── capability descriptors
  ├── asset catalogs
  └── read APIs
```

Engines consume only these abstract capabilities.

Physical package layout, filesystem directories, and storage backends are implementation details outside engine contracts.

---

# 6. Knowledge Module Topology

```text
Fundamental Knowledge
        │
        ├── Strength Knowledge
        ├── Temperature Knowledge
        ├── Pattern Knowledge
        ├── Useful God Knowledge
        ├── Ten Gods Knowledge
        ├── Combination Knowledge
        ├── ShenSha Knowledge
        └── Luck Knowledge
                │
                ▼
        Interpretation Knowledge
                │
                ▼
        Report Knowledge
```

Analytical Knowledge Modules feed Analysis Engine stages.

Interpretation Knowledge and Report Knowledge feed downstream presentation engines.

---

# 7. Dependency Rules

Allowed:

```text
Engine → Abstract Knowledge Module
Knowledge Module → Fundamental Knowledge
Interpretation Knowledge → Analytical Knowledge contracts
Report Knowledge → Interpretation / Analysis result contracts
```

Forbidden:

```text
Engine → Physical repository path
Engine → Another engine's internal knowledge loader path
Knowledge Module → Engine internals
Circular Knowledge Module dependencies
```

---

# 8. Storage Independence

The Knowledge Architecture is storage-agnostic.

Valid future storage backends may include:

- repository packages
- packaged knowledge distributions
- remote knowledge registries
- versioned knowledge bundles

Engine contracts remain unchanged across storage backends.

---

# 9. Runtime Consumption Model

```text
Engine Request
      │
      ▼
Knowledge Gateway / Registry
      │
      ▼
Abstract Knowledge Module
      │
      ▼
Validated Knowledge Assets
      │
      ▼
Engine Matching / Scoring / Rendering
```

Engines receive immutable, versioned knowledge views.

---

# 10. Immutability and Determinism

During a single analysis execution:

- knowledge views are immutable;
- selected knowledge versions are fixed;
- identical engine inputs and identical knowledge versions produce identical analytical outcomes.

Knowledge mutation during execution is prohibited.

---

# 11. Extension Strategy

New Knowledge Modules may be added without modifying existing engine public APIs.

New asset families may be added under the same abstract Knowledge Module model.

Extensions must preserve Version 1.x consumer contracts.

---

# 12. Architecture Decision Records

## ADR-001

Business knowledge resides exclusively in the Knowledge Layer.

---

## ADR-002

Engines depend only on abstract Knowledge Modules.

---

## ADR-003

Physical repository paths are not part of engine contracts.

---

## ADR-004

Knowledge assets are immutable during analysis execution.

---

## ADR-005

Rule, Sentence, and Report Template assets are distinct families under shared governance.

---

## ADR-006

Knowledge Modules are domain-oriented, not engine-implementation-oriented.

---

# 13. Constraints

- No business knowledge in engine source code.
- No engine logic in knowledge assets.
- No path-coupled engine dependencies.
- No unversioned knowledge publication.
- No silent cross-domain knowledge reuse without contract.

---

# 14. Definition of Architectural Completion

The architecture is complete when:

- Knowledge / Engine separation is frozen.
- Abstract Knowledge Module contracts are frozen.
- Dependency rules are frozen.
- Asset family boundaries are frozen.
- Governance and versioning strategy are documented.

Implementation of individual Knowledge Modules may begin only against this baseline.
