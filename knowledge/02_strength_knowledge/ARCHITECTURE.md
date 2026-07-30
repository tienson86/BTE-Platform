# Strength Knowledge Architecture

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Strength Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Day Master Strength knowledge domain;
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
Strength Knowledge
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
Strength Engine
```

---

# 4. Separation of Concerns

## Strength Knowledge Owns

- strength factors and evidence definitions
- strength rule content
- weight models
- confidence models
- priority concepts
- strength terminology
- strength golden / validation knowledge

## Strength Knowledge Does Not Own

- rule execution
- score aggregation runtime
- AnalysisContext orchestration
- Pattern / Useful God / Temperature business ownership
- report or interpretation content ownership

## Strength Engine Owns

- matching mechanics
- scoring mechanics
- priority resolution mechanics
- StrengthResult construction

---

# 5. Dependency Rules

Allowed:

```text
Strength Knowledge → Fundamental Knowledge
Strength Engine → Strength Knowledge (abstract)
```

Forbidden:

```text
Strength Knowledge → Strength Engine
Strength Knowledge → other domain engines
Strength Engine → physical repository path
```

---

# 6. Consumption Contract

The Strength Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Strength Knowledge Snapshot
        │
        ▼
Strength Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable StrengthResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional optional rule categories
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One strength domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
