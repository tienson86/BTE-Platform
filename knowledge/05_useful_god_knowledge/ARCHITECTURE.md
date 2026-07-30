# Useful God Knowledge Architecture

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Useful God Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Useful God knowledge domain;
- publish Knowledge Assets conforming to KAS;
- depend on Fundamental Knowledge for shared fundamentals;
- remain free of Runtime Engine execution logic;
- remain independent of physical repository layout.

---

# 3. Layer Position

```text
Fundamental Knowledge
        │
        ▼
Useful God Knowledge
        │
        ├── Rule Assets
        ├── Decision Tables
        ├── Mapping Tables
        ├── Formula Library
        ├── Priority Tables
        ├── Terminology
        ├── Reference Tables
        ├── Examples / Validation / Golden Datasets
        ├── Metadata / Manifest / Documentation
        │
        ▼
Abstract Interfaces
        │
        ▼
Useful God Engine
```

---

# 4. Separation of Concerns

## Useful God Knowledge Owns

- Yong Shen / Xi Shen / Ji Shen / Chou Shen definitions
- seasonal selection knowledge
- strength / temperature / pattern dependency concepts
- candidate selection knowledge
- priority and confidence models
- Useful God terminology
- Useful God golden / validation knowledge

## Useful God Knowledge Does Not Own

- rule execution
- candidate resolution runtime
- AnalysisContext orchestration
- Strength / Temperature / Pattern recomputation
- report or interpretation content ownership

## Useful God Engine Owns

- matching mechanics
- candidate evaluation mechanics
- priority resolution mechanics
- UsefulGodResult construction

---

# 5. Dependency Rules

Allowed:

```text
Useful God Knowledge → Fundamental Knowledge
Useful God Engine → Useful God Knowledge (abstract)
```

Forbidden:

```text
Useful God Knowledge → Useful God Engine
Useful God Knowledge → other domain engines
Useful God Engine → physical repository path
```

Upstream Strength / Temperature / Pattern results are consumed as published evidence by the engine, not recomputed by this Knowledge Module.

---

# 6. Consumption Contract

The Useful God Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Useful God Knowledge Snapshot
        │
        ▼
Useful God Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable UsefulGodResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional optional candidate classes
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One Useful God domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Strength / Temperature / Pattern recomputation ownership.
