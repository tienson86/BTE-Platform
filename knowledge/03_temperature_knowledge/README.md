# Temperature Knowledge

| Field | Value |
|-------|-------|
| Module ID | temperature_knowledge |
| Module Type | Knowledge Module |
| Domain | Temperature / Climate Balance |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Temperature Knowledge provides the complete canonical knowledge required for Temperature Analysis of the natal chart.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime behavior**.

It is consumed by the Temperature Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Temperature Knowledge defines WHAT climate evaluation knows.
Temperature Engine defines HOW climate evaluation computes.
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
Temperature Knowledge       ← this module
        │
        ▼
Temperature Engine
```

Upstream analytical evidence such as StrengthResult may be referenced as published chart facts by Temperature Engine; Temperature Knowledge does not recompute Strength.

---

# 5. Scope

In scope:

- Seasonal Temperature
- Climate Categories
- Cold and Hot Classification
- Warm and Cool Adjustment
- Dryness and Humidity
- Seasonal Energy
- Month Climate Characteristics
- Climate Balance
- Temperature Exceptions
- Adjustment Principles
- Formula Concepts
- Weight Models
- Confidence Models
- Priority Concepts

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Day Master strength recomputation
- Pattern determination
- Useful God determination
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Temperature Engine | Primary consumer of Temperature Knowledge Assets |
| Downstream Knowledge Modules | May reference climate terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference climate terms only; must not recompute temperature |

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
