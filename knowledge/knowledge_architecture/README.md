# Knowledge Architecture

| Field | Value |
|-------|-------|
| Module Path | `knowledge/knowledge_architecture` |
| Module Type | Knowledge Layer Architecture Baseline |
| Layer | Knowledge |
| Version | 1.0.0 |
| Status | Frozen Architecture Baseline |

---

# 1. Purpose

This document set defines the canonical Knowledge Architecture of the BTE Platform.

The Knowledge Layer is the authoritative source of business knowledge for all analytical, interpretive, and presentation engines.

Its purpose is to separate knowledge from execution so that Engine Modules remain deterministic, reusable, and independent of knowledge storage details.

---

# 2. Core Principle

```text
Knowledge Modules define WHAT the system knows.
Engine Modules define HOW the system computes.
```

Engine Modules shall never embed business knowledge.

Knowledge Modules shall never embed engine execution logic.

---

# 3. Architectural Position

```text
Knowledge Layer
        │
        ▼
Calendar / BaZi Engines
        │
        ▼
Analysis Engine
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

The Knowledge Layer is consumed by engines through abstract Knowledge Module contracts.

Engines shall never depend on physical repository paths.

---

# 4. Knowledge Domains

Future and planned Knowledge Modules include:

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

Each Knowledge Module owns one domain of business knowledge.

---

# 5. Knowledge Asset Types

The Knowledge Layer manages three primary asset families:

| Asset Family | Purpose |
|--------------|---------|
| Rule Database | Analytical decision knowledge |
| Sentence Library | Interpretive language assets |
| Report Templates | Presentation and layout assets |

Additional asset families may be introduced without breaking Version 1.x contracts.

---

# 6. Dependency Rule

```text
Engine Module
      │
      ▼
Abstract Knowledge Module
      │
      ▼
Knowledge Assets
```

Forbidden:

```text
Engine Module → Physical Repository Path
```

---

# 7. Document Set

| Document | Purpose |
|----------|---------|
| README.md | Architecture baseline overview |
| ARCHITECTURE.md | Knowledge Layer software architecture |
| DOMAIN_MODEL.md | Shared knowledge domain models |
| KNOWLEDGE_PIPELINE.md | Knowledge lifecycle and consumption flow |
| KNOWLEDGE_MODULES.md | Module catalog and ownership |
| RULE_DATABASE_SPEC.md | Rule Database architecture |
| SENTENCE_LIBRARY_SPEC.md | Sentence Library architecture |
| REPORT_TEMPLATE_SPEC.md | Report Template architecture |
| KNOWLEDGE_GOVERNANCE.md | Ownership, change control, quality gates |
| VERSIONING.md | Compatibility and version policy |
| ROADMAP.md | Delivery sequence for Knowledge Modules |

---

# 8. Design Principles

The Knowledge Architecture shall be:

- Domain-oriented
- Modular
- Abstract
- Versioned
- Deterministic in consumption
- Explainable
- Extensible
- Governed
- Storage-agnostic

---

# 9. Non-Goals

This architecture baseline does not:

- implement Knowledge Modules
- implement Rule Databases
- implement Sentence Libraries
- implement Report Templates
- bind engines to filesystem locations
- redefine Analysis Engine public APIs

---

# 10. Version

| Item | Value |
|------|-------|
| Architecture Version | 1.0.0 |
| Status | Frozen Architecture Baseline |
| Compatibility | Analysis Engine V1.x and later Knowledge Modules |

This README is the official V1.0 architecture baseline for `knowledge/knowledge_architecture`.

Breaking architectural changes require an explicit major version increment.
