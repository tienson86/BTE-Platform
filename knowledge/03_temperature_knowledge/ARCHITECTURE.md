# Temperature Knowledge Architecture

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Temperature Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Temperature / Climate knowledge domain;
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
Temperature Knowledge
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
Temperature Engine
```

---

# 4. Separation of Concerns

## Temperature Knowledge Owns

- climate factors and evidence definitions
- temperature rule content
- weight models
- confidence models
- priority concepts
- climate terminology
- temperature golden / validation knowledge

## Temperature Knowledge Does Not Own

- rule execution
- score aggregation runtime
- AnalysisContext orchestration
- Strength / Pattern / Useful God business ownership
- report or interpretation content ownership

## Temperature Engine Owns

- matching mechanics
- scoring mechanics
- priority resolution mechanics
- TemperatureResult construction

---

# 5. Dependency Rules

Allowed:

```text
Temperature Knowledge → Fundamental Knowledge
Temperature Engine → Temperature Knowledge (abstract)
```

Forbidden:

```text
Temperature Knowledge → Temperature Engine
Temperature Knowledge → other domain engines
Temperature Engine → physical repository path
```

---

# 6. Consumption Contract

The Temperature Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Temperature Knowledge Snapshot
        │
        ▼
Temperature Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable TemperatureResult
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

- One temperature/climate domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Day Master strength recomputation knowledge ownership.
