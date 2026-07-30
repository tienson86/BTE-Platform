# Fundamental Knowledge Architecture

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of the Fundamental Knowledge Module.

---

# 2. Architectural Goals

The module shall:

- centralize shared BaZi fundamentals;
- prevent duplication across domain Knowledge Modules;
- remain free of analytical business rules;
- expose canonical knowledge through abstract contracts;
- remain independent of repository layout and Runtime Engine internals.

---

# 3. Layer Position

```text
Fundamental Knowledge
        │
        ├── Terminology
        ├── Mapping Tables
        ├── Reference Tables
        ├── Structural Formula Library
        ├── Examples / Validation / Golden Datasets
        └── Manifest / Metadata / Documentation
                │
                ▼
        Domain Knowledge Modules
                │
                ▼
        Runtime Engines
```

---

# 4. Separation of Concerns

## Owns

- Yin Yang polarity definitions
- Wu Xing element definitions
- Stem and Branch catalogs
- Hidden Stem compositions
- Chang Sheng cycle definitions
- Na Yin pairings
- Relationship matrices
- Season and climate definition frames
- Shared terminology

## Does Not Own

- domain scoring thresholds
- pattern candidate rules
- Useful God selection rules
- interpretive narrative content
- report layout templates
- engine matching or scoring algorithms

---

# 5. Dependency Rules

Allowed:

```text
Domain Knowledge Module → Fundamental Knowledge
Runtime Engine → Abstract Knowledge Interfaces
```

Forbidden:

```text
Fundamental Knowledge → Domain Knowledge Module
Fundamental Knowledge → Runtime Engine
Runtime Engine → Physical repository path
```

---

# 6. Consumption Contract

Consumers resolve Fundamental Knowledge by:

- module_id
- version
- asset_id / term_id / mapping_id

Physical storage location is not part of the contract.

---

# 7. Immutability

Published fundamental definitions are immutable within a version.

Semantic corrections require a new module version.

---

# 8. Extension Strategy

Within Version 1.x, the module may add:

- optional reference tables
- additional locales for terminology
- additional examples and datasets

It must not introduce analytical business rules under this module identity.

---

# 9. Constraints

- One shared-fundamental domain only.
- No business Rule Assets.
- No path-coupled public contracts.
- No silent redefinition of canonical terms.
