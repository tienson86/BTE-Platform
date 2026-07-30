# Knowledge Dependency Graph Architecture

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the architectural dependency topology of the Knowledge Layer and Runtime Engine consumers.

---

# 2. Top-Level Topology

```text
                    Knowledge Standards
                 (Architecture / KMS / KAS)
                            │
                            ▼
                   Knowledge Registry
                            │
                            ▼
                   Knowledge Loader
                            │
                            ▼
                    Knowledge SDK
                     /     |     \
                    /      |      \
                   ▼       ▼       ▼
          Analysis Engine  Interpretation  Report Engine
                           Engine
                   │
                   ▼
            Analysis Stages
     (Strength … Luck … Summary)
```

Runtime Engines depend on Knowledge SDK only for knowledge access.

Knowledge SDK depends on Knowledge Loader.

Knowledge Loader depends on Knowledge Registry.

Knowledge Registry catalogs Knowledge Modules and Knowledge Assets.

---

# 3. Knowledge Module Dependency Layer

```text
Fundamental Knowledge
        │
        ├──────────────► Strength Knowledge
        ├──────────────► Temperature Knowledge
        ├──────────────► Pattern Knowledge
        ├──────────────► Useful God Knowledge
        ├──────────────► Ten Gods Knowledge
        ├──────────────► Combination Knowledge
        ├──────────────► ShenSha Knowledge
        └──────────────► Luck Knowledge
```

Analytical Knowledge Modules may declare evidence dependencies on published upstream analytical classifications, but must not recompute or own those upstream domains.

Illustrative evidence-dependency direction (knowledge-level, not engine pipeline):

```text
Strength Knowledge ──evidence──► Useful God / Pattern / Ten Gods / Luck Knowledge
Temperature Knowledge ──evidence──► Useful God / Pattern / Luck Knowledge
Pattern Knowledge ──evidence──► Useful God / Ten Gods / Luck Knowledge
Useful God Knowledge ──evidence──► Ten Gods / Luck Knowledge
Ten Gods / Combination / ShenSha Knowledge ──evidence──► Luck Knowledge
```

Evidence dependency means reference-to-published-classification concepts, not ownership transfer.

---

# 4. Knowledge Asset Ownership Layer

```text
Knowledge Module
        │ owns
        ▼
Knowledge Assets
  (Rules, Decision Tables, Mappings, Formulas,
   Terminology, Reference Tables, Metadata,
   Manifest, Examples, Validation / Golden Datasets,
   Documentation, Version Information, Configuration)
```

Assets depend on their owning module version.

Assets may declare optional fine-grained references to other assets, but required asset cycles are forbidden.

---

# 5. Control-Plane Dependency Layer

```text
Knowledge Modules / Assets
        │ registered in
        ▼
Knowledge Registry
        │ consulted by
        ▼
Knowledge Loader
        │ exposed by
        ▼
Knowledge SDK
        │ consumed by
        ▼
Runtime Engines
```

---

# 6. Runtime Engine Consumption Layer

| Engine | Knowledge Access Dependency |
|--------|-----------------------------|
| Analysis Engine | Knowledge SDK only |
| Interpretation Engine | Knowledge SDK only |
| Report Engine | Knowledge SDK only |

Analysis Engine stages consume domain Knowledge Modules through SDK according to stage responsibility.

Interpretation Engine consumes Interpretation / Sentence knowledge through SDK.

Report Engine consumes Report Template knowledge through SDK.

Engines must not depend on each other’s internal knowledge loaders.

---

# 7. Forbidden Edges

```text
Runtime Engine → Knowledge Module (direct)
Runtime Engine → Knowledge Registry (direct)
Runtime Engine → Knowledge Loader (direct)
Knowledge Module → Runtime Engine
Knowledge Asset → Runtime Engine
Knowledge Loader → Knowledge Module authoring APIs
Circular required Module → Module dependencies
```

---

# 8. Architectural Guarantees

- Single knowledge access door for engines: Knowledge SDK
- Catalog authority: Knowledge Registry
- Load/bind authority: Knowledge Loader
- Domain knowledge ownership: Knowledge Modules
- Asset ownership: parent Knowledge Module versions

---

# 9. Constraints

- Path-independent identities only
- No runtime execution in this document set
- Dependency Graph describes contracts, not deployment wiring details
