# Knowledge Module Architecture

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of a conforming Knowledge Module.

It establishes identity, boundaries, asset composition, consumption contracts, and independence from physical storage.

---

# 2. Architectural Goals

A Knowledge Module shall:

- own exactly one knowledge domain;
- aggregate one or more Knowledge Assets;
- expose a stable abstract contract;
- remain independent of Runtime Engine internals;
- remain independent of physical repository layout;
- support deterministic, versioned consumption.

---

# 3. Logical Identity

Every Knowledge Module shall declare:

| Field | Requirement |
|-------|-------------|
| module_id | Stable logical identifier |
| domain | Single owned domain |
| display_name | Human-readable name |
| status | Planned / Draft / Validated / Published / Deprecated |
| version | SemVer identity |
| asset_inventory | Declared Knowledge Asset types |
| consumers | Declared Runtime Engine or Knowledge consumers |
| dependencies | Declared upstream Knowledge Modules |

`module_id` is logical. It is not a repository path.

---

# 4. Layered Relationship

```text
Knowledge Architecture
        │
        ▼
Knowledge Module
        │
        ├── Documentation
        ├── Metadata
        ├── Manifest
        ├── Version
        ├── Governance
        └── Knowledge Assets
                │
                ▼
        Abstract Interfaces
                │
                ▼
        Runtime Engine
```

---

# 5. Separation of Concerns

## Knowledge Module Owns

- domain knowledge
- Knowledge Assets
- terminology
- metadata
- examples
- validation and golden datasets
- version and compatibility declarations

## Knowledge Module Does Not Own

- scoring algorithms
- pipeline orchestration
- chart construction
- runtime state
- report rendering execution
- physical storage topology as a public contract

## Runtime Engine Owns

- validation of inputs
- matching mechanics
- scoring mechanics
- priority resolution mechanics
- result construction
- execution metadata

## Runtime Engine Does Not Own

- business rule content
- terminology definitions as source of truth
- golden knowledge outcomes as editable engine code
- repository paths to knowledge packages

---

# 6. Abstract Consumption Contract

```text
Runtime Engine
      │
      ▼
Knowledge Gateway / Registry
      │
      ▼
Abstract Knowledge Module
      │
      ▼
Immutable Knowledge Asset Snapshot
```

Forbidden:

```text
Runtime Engine → Physical repository path
Runtime Engine → Unpublished draft assets
Runtime Engine → Mutation of Knowledge Assets
```

---

# 7. Asset Composition Model

A Knowledge Module is a container of Knowledge Assets.

The Rule Database is only one Knowledge Asset type.

Other asset types include Decision Tables, Mapping Tables, Terminology, Metadata, Examples, Golden Datasets, Validation Datasets, Priority Tables, Formula Libraries, Reference Tables, Configuration, and Documentation.

See KNOWLEDGE_ASSETS.md.

---

# 8. Analysis Engine Relationship

Analysis Engine stages consume Knowledge Modules through abstract interfaces.

| Runtime Stage | Knowledge Module |
|---------------|------------------|
| Strength Engine | Strength Knowledge |
| Temperature Engine | Temperature Knowledge |
| Pattern Engine | Pattern Knowledge |
| Useful God Engine | Useful God Knowledge |
| Ten Gods Engine | Ten Gods Knowledge |
| Combination Engine | Combination Knowledge |
| ShenSha Engine | ShenSha Knowledge |
| Luck Engine | Luck Knowledge |

Interpretation Engine and Report Engine consume Interpretation Knowledge and Report Knowledge under the same architecture.

---

# 9. Repository Independence

Physical packaging may change over time.

Logical module identity, asset identity, and version identity must remain stable.

Engine architecture shall be unaffected by repository reorganization.

---

# 10. Extension Architecture

Within Version 1.x, a module may add:

- optional metadata fields
- additional asset types declared in the Manifest
- additional categories
- additional locales
- additional examples and datasets

Extensions must preserve existing consumer contracts.

---

# 11. Architecture Constraints

- One domain per Knowledge Module.
- No engine logic inside Knowledge Assets.
- No path-coupled public contracts.
- No silent cross-domain duplication.
- No unversioned publication.
- No treatment of Rule Database as the entire module.

---

# 12. Definition of Architectural Completion

A Knowledge Module architecture is complete when:

- logical identity is declared;
- asset inventory is declared;
- abstract contract is complete;
- mandatory documentation exists;
- metadata and Manifest are defined;
- validation and golden datasets are declared;
- dependency and compatibility matrices are present;
- governance status is defined.
