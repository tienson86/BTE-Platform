# Pattern Knowledge Architecture

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Pattern Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Pattern / Ge Ju knowledge domain;
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
Pattern Knowledge
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
Pattern Engine
```

---

# 4. Separation of Concerns

## Pattern Knowledge Owns

- pattern factor and evidence definitions
- pattern rule content
- pattern condition definitions
- priority and compatibility concepts
- confidence models
- pattern terminology
- pattern golden / validation knowledge

## Pattern Knowledge Does Not Own

- rule execution
- candidate resolution runtime
- AnalysisContext orchestration
- Strength / Temperature / Useful God business ownership
- report or interpretation content ownership

## Pattern Engine Owns

- matching mechanics
- candidate generation / evaluation mechanics
- priority resolution mechanics
- PatternResult construction

---

# 5. Dependency Rules

Allowed:

```text
Pattern Knowledge → Fundamental Knowledge
Pattern Engine → Pattern Knowledge (abstract)
```

Forbidden:

```text
Pattern Knowledge → Pattern Engine
Pattern Knowledge → other domain engines
Pattern Engine → physical repository path
```

---

# 6. Consumption Contract

The Pattern Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Pattern Knowledge Snapshot
        │
        ▼
Pattern Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable PatternResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional optional pattern categories
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One pattern domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Strength or Temperature recomputation ownership.
