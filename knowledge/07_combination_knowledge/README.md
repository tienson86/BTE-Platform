# Combination Knowledge

| Field | Value |
|-------|-------|
| Module ID | combination_knowledge |
| Module Type | Knowledge Module |
| Domain | Combination / Hợp Hóa Xung Hình Hại (合化冲刑害) |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Combination Knowledge provides the complete canonical knowledge required for Combination Analysis of the natal chart.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime logic**.

It is consumed by the Combination Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Combination Knowledge defines WHAT Combination evaluation knows.
Combination Engine defines HOW Combination evaluation computes.
```

---

# 3. Constitutional Compliance

This module fully complies with:

- Knowledge Architecture V1.x
- Knowledge Module Standard (KMS) V1.x
- Knowledge Asset Standard (KAS) V1.x

---

# 4. Architectural Relationship

```text
Knowledge Architecture
        │
        ▼
Knowledge Module Standard
        │
        ▼
Knowledge Asset Standard
        │
        ▼
Fundamental Knowledge
        │
        ▼
Combination Knowledge       ← this module
        │
        ▼
Combination Engine
```

Upstream published analytical results may be referenced as chart evidence by Combination Engine where declared. Combination Knowledge does not recompute Strength, Temperature, Pattern, Useful God, or Ten Gods.

---

# 5. Scope

In scope:

- Heavenly Stem Combination
- Earthly Branch Combination
- Clash
- Harm
- Punishment
- Destruction
- Hidden Combination
- Transformation
- Priority Resolution
- Conflict Resolution
- Formula Concepts
- Mapping Tables

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Day Master strength recomputation
- Temperature recomputation
- Pattern recomputation
- Useful God recomputation
- Ten Gods recomputation
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Combination Engine | Primary consumer of Combination Knowledge Assets |
| Downstream Knowledge Modules | May reference Combination terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference Combination terms only; must not recompute Combination |

---

# 7. Document Set

| # | Document |
|---|----------|
| 01 | README.md |
| 02 | ARCHITECTURE.md |
| 03 | DOMAIN_MODEL.md |
| 04 | KNOWLEDGE_ASSETS.md |
| 05 | RULE_ASSET_SPEC.md |
| 06 | DECISION_TABLE_SPEC.md |
| 07 | MAPPING_TABLE_SPEC.md |
| 08 | FORMULA_LIBRARY_SPEC.md |
| 09 | TERMINOLOGY.md |
| 10 | METADATA_SPEC.md |
| 11 | VALIDATION_STANDARD.md |
| 12 | GOLDEN_DATASET_SPEC.md |
| 13 | QUALITY_STANDARD.md |
| 14 | VERSIONING.md |
| 15 | GOVERNANCE.md |
| 16 | CHANGELOG.md |

---

# 8. Design Principles

- Domain-oriented
- Rule-driven knowledge content
- Explainable
- Versioned
- Validated
- Governed
- Repository-independent
- Engine-independent

---

# 9. Version

| Item | Value |
|------|-------|
| Module Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

Breaking semantic changes require a major version increment.
