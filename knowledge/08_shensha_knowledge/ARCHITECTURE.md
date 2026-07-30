# ShenSha Knowledge Architecture

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of ShenSha Knowledge.

---

# 2. Architectural Goals

The module shall:

- own the complete ShenSha knowledge domain;
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
ShenSha Knowledge
        │
        ├── Rule Assets
        ├── Decision Tables
        ├── Mapping Tables
        ├── Lookup Tables
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
ShenSha Engine
```

---

# 4. Separation of Concerns

## ShenSha Knowledge Owns

- Auspicious ShenSha definitions
- Inauspicious ShenSha definitions
- calculation reference knowledge
- lookup and mapping tables
- priority, interaction, compatibility, and exception concepts
- confidence models
- ShenSha terminology
- ShenSha golden / validation knowledge

## ShenSha Knowledge Does Not Own

- rule execution
- ShenSha detection runtime
- AnalysisContext orchestration
- Strength / Temperature / Pattern / Useful God / Ten Gods / Combination recomputation
- report or interpretation content ownership

## ShenSha Engine Owns

- matching / detection mechanics
- interaction evaluation mechanics
- priority resolution mechanics
- ShenShaResult construction

---

# 5. Dependency Rules

Allowed:

```text
ShenSha Knowledge → Fundamental Knowledge
ShenSha Engine → ShenSha Knowledge (abstract)
```

Forbidden:

```text
ShenSha Knowledge → ShenSha Engine
ShenSha Knowledge → other domain engines
ShenSha Engine → physical repository path
```

Upstream analytical results are consumed as published evidence by the engine where required, not recomputed by this Knowledge Module.

---

# 6. Consumption Contract

The ShenSha Engine consumes this module by:

- module_id
- version
- asset_id / rule_id / term_id

Storage location is never part of the contract.

---

# 7. Knowledge Flow

```text
Published ShenSha Knowledge Snapshot
        │
        ▼
ShenSha Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable ShenShaResult
```

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- additional optional ShenSha identities
- additional examples and datasets
- additional locales for terminology

Extensions must preserve published consumer contracts.

---

# 9. Constraints

- One ShenSha domain only.
- No runtime code in Knowledge Assets.
- No path-coupled public contracts.
- No duplication of Fundamental Knowledge definitions.
- No Strength / Temperature / Pattern / Useful God / Ten Gods / Combination recomputation ownership.
