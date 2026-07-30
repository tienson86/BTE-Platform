# Luck Knowledge

| Field | Value |
|-------|-------|
| Module ID | luck_knowledge |
| Module Type | Knowledge Module |
| Domain | Luck / Vận Trình (大运流年) |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Luck Knowledge provides the complete canonical knowledge required for Luck Analysis of the natal chart over time.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime logic**.

It is consumed by the Luck Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Luck Knowledge defines WHAT Luck evaluation knows.
Luck Engine defines HOW Luck evaluation computes.
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
Luck Knowledge              ← this module
        │
        ▼
Luck Engine
```

Upstream published natal analytical results may be referenced as chart evidence by Luck Engine where declared. Luck Knowledge does not recompute Strength, Temperature, Pattern, Useful God, Ten Gods, Combination, or ShenSha.

---

# 5. Scope

In scope:

- Da Yun
- Liu Nian
- Liu Yue
- Liu Ri
- Liu Shi
- Luck Interaction
- Timing Principles
- Activation Rules
- Favorability Concepts
- Confidence Models
- Priority Concepts
- Reference Tables

Out of scope:

- Runtime luck pillar generation mechanics
- Runtime scoring execution
- Natal Day Master strength recomputation
- Temperature recomputation
- Pattern recomputation
- Useful God recomputation
- Ten Gods recomputation
- Combination recomputation
- ShenSha recomputation
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Luck Engine | Primary consumer of Luck Knowledge Assets |
| Downstream Knowledge Modules | May reference Luck terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference Luck terms only; must not recompute Luck |

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
