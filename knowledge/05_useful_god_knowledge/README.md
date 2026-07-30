# Useful God Knowledge

| Field | Value |
|-------|-------|
| Module ID | useful_god_knowledge |
| Module Type | Knowledge Module |
| Domain | Useful God / Dụng Thần |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Useful God Knowledge provides the complete canonical knowledge required for Useful God Analysis of the natal chart.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime logic**.

It is consumed by the Useful God Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Useful God Knowledge defines WHAT Useful God evaluation knows.
Useful God Engine defines HOW Useful God evaluation computes.
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
Useful God Knowledge        ← this module
        │
        ▼
Useful God Engine
```

Upstream published StrengthResult, TemperatureResult, and PatternResult may be referenced as chart evidence by Useful God Engine. Useful God Knowledge does not recompute Strength, Temperature, or Pattern.

---

# 5. Scope

In scope:

- Yong Shen
- Xi Shen
- Ji Shen
- Chou Shen
- Seasonal Selection
- Strength Dependency
- Temperature Dependency
- Pattern Dependency
- Priority Rules
- Candidate Selection
- Confidence Concepts
- Formula Concepts
- Decision Tables
- Reference Tables

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Day Master strength recomputation
- Temperature recomputation
- Pattern recomputation
- Ten Gods quality analysis ownership
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Useful God Engine | Primary consumer of Useful God Knowledge Assets |
| Downstream Knowledge Modules | May reference Useful God terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference Useful God terms only; must not recompute Useful God |

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
