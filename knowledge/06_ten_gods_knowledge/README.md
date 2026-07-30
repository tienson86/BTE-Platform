# Ten Gods Knowledge

| Field | Value |
|-------|-------|
| Module ID | ten_gods_knowledge |
| Module Type | Knowledge Module |
| Domain | Ten Gods / Thập Thần (十神) |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Ten Gods Knowledge provides the complete canonical knowledge required for Ten Gods Analysis of the natal chart.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime logic**.

It is consumed by the Ten Gods Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Ten Gods Knowledge defines WHAT Ten Gods evaluation knows.
Ten Gods Engine defines HOW Ten Gods evaluation computes.
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
Ten Gods Knowledge          ← this module
        │
        ▼
Ten Gods Engine
```

Upstream published StrengthResult, PatternResult, and UsefulGodResult may be referenced as chart evidence by Ten Gods Engine. Ten Gods Knowledge does not recompute Strength, Temperature, Pattern, or Useful God.

---

# 5. Scope

In scope:

- Ten Gods Definitions
- Relationship Models
- Strength Interaction
- Pattern Interaction
- Useful God Interaction
- Favorability
- Personality Concepts
- Career Concepts
- Wealth Concepts
- Marriage Concepts
- Health Concepts
- Priority Concepts
- Confidence Concepts

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Day Master strength recomputation
- Temperature recomputation
- Pattern recomputation
- Useful God recomputation
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Ten Gods Engine | Primary consumer of Ten Gods Knowledge Assets |
| Downstream Knowledge Modules | May reference Ten Gods terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference Ten Gods terms only; must not recompute Ten Gods |

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
