# Ten Gods Knowledge Architecture

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of Ten Gods Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete Ten Gods analytical knowledge domain;
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
Ten Gods Knowledge
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
Ten Gods Engine
```

---

# 4. Separation of Concerns

## Ten Gods Knowledge Owns

- Ten Gods analytical definitions and quality concepts
- relationship models among the Ten Gods
- strength / pattern / useful-god interaction knowledge
- favorability concepts
- personality / career / wealth / marriage / health concepts
- priority and confidence models
- Ten Gods terminology
- Ten Gods golden / validation knowledge

## Ten Gods Knowledge Does Not Own

- rule execution
- Ten Gods quality scoring runtime
- AnalysisContext orchestration
- Strength / Temperature / Pattern / Useful God recomputation
- report or interpretation content ownership

## Ten Gods Engine Owns

- matching mechanics
- interaction evaluation mechanics
- priority resolution mechanics
- TenGodsResult construction

---

# 5. Dependency Rules

Allowed:

```text
Ten Gods Knowledge → Fundamental Knowledge
Ten Gods Engine → Ten Gods Knowledge (abstract)
```

Forbidden:

```text
Ten Gods Knowledge → Ten Gods Engine
Ten Gods Knowledge → other domain engines
Ten Gods Engine → physical repository path
```

Upstream Strength / Pattern / Useful God results are consumed as published evidence by the engine, not recomputed by this Knowledge Module.

---

# 6. Consumption Contract

The Ten Gods Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published Ten Gods Knowledge Snapshot
        │
        ▼
Ten Gods Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable TenGodsResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional life-area concept refinements
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One Ten Gods domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Strength / Temperature / Pattern / Useful God recomputation ownership.
