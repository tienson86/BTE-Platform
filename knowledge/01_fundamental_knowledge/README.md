# Fundamental Knowledge

| Field | Value |
|-------|-------|
| Module ID | fundamental_knowledge |
| Module Path | `knowledge/01_fundamental_knowledge` |
| Module Type | Knowledge Module |
| Domain | Shared BaZi Fundamentals |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

Fundamental Knowledge defines the canonical shared concepts required by every future Knowledge Module on the BTE Platform.

It is the foundation layer of the Knowledge Architecture.

It publishes **canonical knowledge only**.

It does **not** publish analytical business rules.

---

# 2. Core Principle

```text
Fundamental Knowledge defines WHAT the shared universe is.
Domain Knowledge Modules define HOW domain decisions are made.
Runtime Engines define HOW computation is executed.
```

---

# 3. Scope

In scope:

- Yin Yang
- Wu Xing (Five Elements)
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Chang Sheng cycle
- Na Yin
- Ten Gods Relationships
- Five Element Relationships
- Stem Relationships
- Branch Relationships
- Season Definitions
- Climate Definitions
- Shared Terminology

Out of scope:

- Strength scoring rules
- Temperature scoring rules
- Pattern determination rules
- Useful God determination rules
- Ten Gods quality analysis rules
- Combination / ShenSha / Luck business rules
- Interpretation sentences
- Report templates
- Engine algorithms

---

# 4. Architectural Position

```text
Knowledge Architecture
        │
        ▼
Knowledge Module Standard
        │
        ▼
Fundamental Knowledge          ← this module
        │
        ├── Strength Knowledge
        ├── Temperature Knowledge
        ├── Pattern Knowledge
        ├── Useful God Knowledge
        ├── Ten Gods Knowledge
        ├── Combination Knowledge
        ├── ShenSha Knowledge
        ├── Luck Knowledge
        ├── Interpretation Knowledge
        └── Report Knowledge
```

All domain Knowledge Modules may depend on Fundamental Knowledge.

Fundamental Knowledge shall never depend on domain Knowledge Modules or Runtime Engines.

---

# 5. Consumers

| Consumer Type | Usage |
|---------------|-------|
| Analytical Knowledge Modules | Shared taxonomies, mappings, relationships |
| Interpretation Knowledge | Shared terminology |
| Report Knowledge | Shared reference labels |
| Runtime Engines | Abstract read of canonical fundamentals via Knowledge Modules |

Runtime Engines must never depend on physical repository paths.

---

# 6. Knowledge Asset Profile

Primary asset families:

- Terminology
- Mapping Tables
- Reference Tables
- Formula Library (structural cycle formulas only)
- Metadata
- Manifest
- Examples
- Validation Datasets
- Golden Datasets
- Documentation

Explicitly excluded:

- Analytical Rule Assets / business Rule Database

---

# 7. Document Set

| Document | Purpose |
|----------|---------|
| README.md | Module overview |
| ARCHITECTURE.md | Logical architecture |
| DOMAINS.md | Fundamental domains |
| MODELS.md | Canonical models |
| KNOWLEDGE_ASSETS.md | Asset inventory |
| RULE_SPEC.md | Business-rule exclusion policy |
| MAPPING_SPEC.md | Mapping / relationship tables |
| FORMULA_SPEC.md | Structural formula definitions |
| TERMINOLOGY.md | Shared terminology |
| VALIDATION.md | Validation requirements |
| QUALITY.md | Quality criteria |
| VERSIONING.md | Version policy |
| GOVERNANCE.md | Ownership and change control |
| CHANGELOG.md | Change history |

---

# 8. Standards Compliance

This module conforms to:

- Knowledge Architecture V1.x
- Knowledge Module Standard (KMS) V1.x
- Knowledge Asset Standard (KAS) V1.x

---

# 9. Version

| Item | Value |
|------|-------|
| Module Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

Breaking changes to fundamental semantics require a major version increment.
