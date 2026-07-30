# Combination Knowledge Architecture

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Combination Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Combination knowledge domain;
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
Combination Knowledge
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
Combination Engine
```

---

# 4. Separation of Concerns

## Combination Knowledge Owns

- Heavenly Stem Combination definitions
- Earthly Branch Combination definitions
- Clash / Harm / Punishment / Destruction definitions
- Hidden Combination definitions
- Transformation definitions and conditions
- priority and conflict resolution knowledge
- Combination terminology
- Combination golden / validation knowledge

## Combination Knowledge Does Not Own

- rule execution
- combination / clash matching runtime
- AnalysisContext orchestration
- Strength / Temperature / Pattern / Useful God / Ten Gods recomputation
- report or interpretation content ownership

## Combination Engine Owns

- matching mechanics
- transformation evaluation mechanics
- priority / conflict resolution mechanics
- CombinationResult construction

---

# 5. Dependency Rules

Allowed:

```text
Combination Knowledge → Fundamental Knowledge
Combination Engine → Combination Knowledge (abstract)
```

Forbidden:

```text
Combination Knowledge → Combination Engine
Combination Knowledge → other domain engines
Combination Engine → physical repository path
```

Upstream analytical results are consumed as published evidence by the engine where required, not recomputed by this Knowledge Module.

---

# 6. Consumption Contract

The Combination Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Combination Knowledge Snapshot
        │
        ▼
Combination Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable CombinationResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional optional combination subtypes
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One Combination domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Strength / Temperature / Pattern / Useful God / Ten Gods recomputation ownership.
