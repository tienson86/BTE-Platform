# Pattern Knowledge

| Field | Value |
|-------|-------|
| Module ID | pattern_knowledge |
| Module Type | Knowledge Module |
| Domain | Pattern / Ge Ju (格局) |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Pattern Knowledge provides the complete canonical knowledge required for Pattern Analysis of the natal chart.

This module contains **domain knowledge only**.

It does **not** perform calculations.

It does **not** execute rules.

It contains **no runtime logic**.

It is consumed by the Pattern Engine through abstract interfaces only.

---

# 2. Core Principle

```text
Pattern Knowledge defines WHAT pattern evaluation knows.
Pattern Engine defines HOW pattern evaluation computes.
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
Pattern Knowledge           ← this module
        │
        ▼
Pattern Engine
```

Upstream published StrengthResult and TemperatureResult may be referenced as chart evidence by Pattern Engine. Pattern Knowledge does not recompute Strength or Temperature.

---

# 5. Scope

In scope:

- Standard Patterns
- Special Patterns
- Follow Patterns
- Transformation Patterns
- Pattern Conditions
- Pattern Priority
- Pattern Compatibility
- Pattern Exceptions
- Pattern Confidence
- Decision Concepts
- Reference Tables
- Formula Concepts
- Validation Concepts

Out of scope:

- Runtime matching mechanics
- Runtime scoring execution
- Day Master strength recomputation
- Temperature recomputation
- Useful God determination
- Interpretation narrative generation
- Report rendering

---

# 6. Consumers

| Consumer | Usage |
|----------|-------|
| Pattern Engine | Primary consumer of Pattern Knowledge Assets |
| Downstream Knowledge Modules | May reference pattern terminology and published classifications where declared |
| Interpretation / Report Knowledge | May reference pattern terms only; must not recompute Pattern |

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
