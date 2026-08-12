# Catalog Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | CATALOG_PIPELINE |
| Version | 1.0.0 |
| Section | 6 — Catalog |

---

# 6.1 Purpose

Convert approved **Knowledge Library** prose into **deterministic Knowledge Units** in the Knowledge Catalog.

Location: `knowledge/knowledge_catalog/PACK_XX_<DOMAIN>/`

---

# 6.2 Transformation rule

```text
Interpretation Knowledge (paragraph)
  ↓ split / gate / metadata
Knowledge Unit (one claim + schema)
  ↓ default status
Draft
```

**One primary claim per unit.** Composite paragraphs split into multiple units.

---

# 6.3 Catalog workflow

```text
Library topic approved (QG1)
  ↓
Define / confirm CATALOG_SCHEMA for pack
  ↓
Extract units per topic folder
  ↓
Assign knowledge_id (stable, never reused)
  ↓
Set source_document (exact filename)
  ↓
Set required_facts, limitations, class gate
  ↓
Declare duplicate_cluster where overlap known
  ↓
Update CATALOG_INDEX
  ↓
Self-check against QG2
  ↓
Domain Reviewer catalog sign-off
  ↓
QA phase may begin
```

---

# 6.4 Required catalog artifacts (per pack)

| Artifact | Purpose |
|----------|---------|
| README.md | Pack catalog entry |
| CATALOG_ARCHITECTURE.md | Structure and consumption |
| CATALOG_SCHEMA.md | Frozen unit fields |
| CATALOG_INDEX.md | Complete id index |
| KNOWLEDGE_UNIT_LIFECYCLE.md | Status definitions (aligns with Factory) |
| VALIDATION_RULES.md | Pack validation specifics |
| CHANGELOG.md | Catalog history |
| catalog/<topic>/ | Unit files |

Factory does not define schema — per-pack catalog owns schema. Factory defines **when** catalog is ready for QA.

---

# 6.5 Unit creation rules

| Rule | Detail |
|------|--------|
| Source fidelity | Claim must exist in cited `source_document` |
| No new knowledge | Split and gate only; no invention |
| Default status | **Draft** for all new units |
| Id policy | Pack-defined (e.g. `IK-STR-MEAN-0001`) |
| Class gate | Every class-specific unit gated |
| Evidence fields | required_facts match claim needs |
| Limitations | Gate unpublished dimensions |

---

# 6.6 Topic folder mapping (PACK-01)

| Library file | Catalog folder |
|--------------|----------------|
| 01_MEANINGS.md | catalog/meaning/ |
| 02_CAUSES.md | catalog/causes/ |
| 03_ADVANTAGES.md | catalog/advantages/ |
| … | … |

Full mapping in pack CATALOG_ARCHITECTURE.

---

# 6.7 Duplicate declaration

At catalog time, Author declares:

- `duplicate_cluster` ids
- Representative intent (documented in architecture or governance)

QA verifies clusters; does not invent them during review-only tasks.

Reference: `knowledge/knowledge_qa/STANDARD/DUPLICATE_POLICY.md`

---

# 6.8 Cursor role in catalog

Cursor may:

- Extract units from prose following schema
- Generate CATALOG_INDEX entries
- Flag missing source traces

Cursor may not:

- Mark units Validated or Frozen
- Invent claims not in Library

---

# 6.9 Exit criteria (QG2)

| Check | Required |
|-------|----------|
| Schema compliance | 100% units |
| Index match | File count = index count |
| All Draft | No premature promotion |
| Duplicate clusters | Declared for known overlaps |
| Domain Reviewer sign-off | Catalog ready for QA |

---

# 6.10 PACK-01 status

| Metric | Value |
|--------|-------|
| Units | 339 |
| Status | All Draft |
| QA | Phases 01–03 complete (78 units reviewed) |
| Remaining QA | CHALLENGES through EXAMPLES |

---

END
