# Strength Knowledge

| Field | Value |
|-------|-------|
| Module ID | strength_knowledge |
| Module Type | Knowledge Module |
| Domain | Day Master Strength (Thân Vượng / Thân Nhược) |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Strength Knowledge provides the complete canonical knowledge required for evaluating Day Master Strength (Thân Vượng / Thân Nhược).

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It is consumed by the Strength Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Strength Knowledge defines WHAT strength evaluation knows.
Strength Engine defines HOW strength evaluation computes.
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
Strength Knowledge          ← this module
        │
        ▼
Strength Engine
```

---

# 5. Scope

In scope:

- Seasonal Strength
- Monthly Branch Influence
- Heavenly Stem Support
- Hidden Stem Support
- Root Strength
- Five Element Support
- Five Element Restriction
- Combination Influence
- Clash Influence
- Harm Influence
- Punishment Influence
- Void Influence
- Temperature Adjustment Influence
- Growth Stage (Trường Sinh)
- Tong Gen (Thông Căn)
- De Ling (Đắc Lệnh)
- De Di (Đắc Địa)
- De Shi (Đắc Thế)
- Special Exceptions
- Weight Models
- Confidence Models
- Priority Concepts

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Pattern determination
- Useful God determination
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Strength Engine | Primary consumer of Strength Knowledge Assets |
| Downstream Knowledge Modules | May reference strength terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference strength terms only; must not recompute strength |

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
