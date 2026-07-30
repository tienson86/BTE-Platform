# Knowledge Module Standard (KMS)

| Field | Value |
|-------|-------|
| Standard ID | KMS |
| Module Path | `knowledge/knowledge_module_standard` |
| Document Type | Constitutional Knowledge Module Specification |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

This document set is the official Knowledge Module Standard of the BTE Platform.

It is the constitutional specification for every future Knowledge Module.

No Knowledge Module may be Drafted, Validated, or Published unless it conforms to this standard.

---

# 2. Background

The following architecture baselines are frozen:

- Knowledge Architecture — `knowledge/knowledge_architecture/`
- Analysis Engine Architecture — `engines/analysis_engine/`

Future engine development depends on a standardized Knowledge Layer.

This standard defines how every Knowledge Module must be designed, documented, versioned, validated, and governed.

---

# 3. What Is a Knowledge Module

A Knowledge Module is a **logical collection of domain knowledge**.

It is a domain architecture unit.

A Knowledge Module is **NOT**:

- an Engine
- a Rule Database
- a JSON folder
- a repository directory

A Rule Database is only one possible Knowledge Asset inside a Knowledge Module.

---

# 4. Core Principle

```text
Knowledge Modules define WHAT the system knows.
Runtime Engines define HOW the system computes.
```

Knowledge Modules shall never embed engine execution logic.

Runtime Engines shall never embed business knowledge.

Runtime Engines shall never depend on repository paths.

---

# 5. Architectural Relationship

```text
Knowledge Architecture
        │
        ▼
Knowledge Module Standard
        │
        ▼
Knowledge Module
        │
        ▼
Knowledge Assets
        │
        ▼
Runtime Engine
```

The Runtime Engine consumes Knowledge Assets through abstract interfaces only.

---

# 6. Repository Independence

Knowledge Modules are logical units.

Repository folders are implementation details.

Future versions may reorganize physical storage without affecting engine architecture.

No document in this standard treats a filesystem path as a public contract.

---

# 7. Applicable Modules

This standard applies to all current and future Knowledge Modules, including:

- Fundamental Knowledge
- Strength Knowledge
- Temperature Knowledge
- Pattern Knowledge
- Useful God Knowledge
- Ten Gods Knowledge
- Combination Knowledge
- ShenSha Knowledge
- Luck Knowledge
- Interpretation Knowledge
- Report Knowledge

---

# 8. Document Set

| # | Document | Purpose |
|---|----------|---------|
| 01 | README.md | Standard overview |
| 02 | ARCHITECTURE.md | Logical architecture and contracts |
| 03 | MODULE_STRUCTURE.md | Mandatory logical structure and documentation |
| 04 | KNOWLEDGE_ASSETS.md | Official asset taxonomy |
| 05 | RULE_SPEC.md | Rule asset specification |
| 06 | EXAMPLE_SPEC.md | Example asset specification |
| 07 | TERMINOLOGY_SPEC.md | Terminology asset specification |
| 08 | METADATA_SPEC.md | Metadata and Manifest specification |
| 09 | VALIDATION_STANDARD.md | Validation, golden, and regression standards |
| 10 | QUALITY_STANDARD.md | Measurable quality criteria |
| 11 | DEPENDENCY_RULES.md | Dependency and consumption rules |
| 12 | VERSIONING.md | Version and compatibility policy |
| 13 | GOVERNANCE.md | Review, approval, change, deprecation |
| 14 | CHANGELOG.md | Standard change history |

---

# 9. Design Principles

Every Knowledge Module shall be:

- Domain-oriented
- Logical, not path-coupled
- Asset-complete for its declared scope
- Versioned
- Validated
- Governed
- Explainable
- Deterministic in consumption
- Extensible within Version 1.x

---

# 10. Non-Goals

This standard does not:

- implement Knowledge Modules
- implement Runtime Engines
- prescribe physical repository layout as architecture
- redefine frozen Analysis Engine public APIs
- redefine Knowledge Architecture principles

---

# 11. Version

| Item | Value |
|------|-------|
| Standard Version | 1.0.0 |
| Status | Frozen Architecture Baseline |
| Compatibility | Knowledge Architecture V1.x |

Breaking changes to this standard require a major version increment.
