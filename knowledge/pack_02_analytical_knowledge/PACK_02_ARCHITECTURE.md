# PACK_02_ARCHITECTURE.md

> **BTE Platform — Analytical Knowledge Architecture Skeleton**
>
> **Pack:** 02 — Analytical Knowledge
>
> **Document Version:** 0.0.0
>
> **Status:** Initialized (Structure Only)
>
> **Depends On:** Pack 01 Architecture principles
>
> **Root:** `knowledge/pack_02_analytical_knowledge/`
>
> **Last Updated:** 2026-08-01

---

# TABLE OF CONTENTS

1. Purpose
2. Scope
3. Design Goals
4. Relationship to Pack 01
5. Overall Architecture
6. Analytical Modules
7. Dependency Rules
8. Registry / Validation / Compiler Compatibility
9. Non-Goals
10. Document Status

---

# 1. Purpose

Pack 02 defines the **Analytical Knowledge** layer above Pack 01.

It provides structured analytical knowledge modules for Analysis Engines.

This document is an **architecture skeleton only**.

---

# 2. Scope

In scope:

- Analytical module boundaries
- Dependency direction
- Compatibility with Registry, Validation, Compiler
- Directory and governance skeleton

Out of scope (this initialization):

- Business logic
- Analysis rules
- Scoring formulas
- Engine algorithms
- Report / interpretation narrative

---

# 3. Design Goals

- Follow Pack 01 architecture principles (Knowledge First, Schema First, Versioned, Traceable)
- One module, one analytical responsibility
- One-way dependency to Pack 01
- No duplication of Pack 01 fundamentals
- Extensible for future analytical domains

---

# 4. Relationship to Pack 01

```text
Client / API
    │
    ▼
Analysis Engines
    │
    ▼
Pack 02 — Analytical Knowledge
    │
    ▼
Pack 01 — Fundamental Theory / Knowledge Infrastructure
```

Pack 02 consumes Pack 01.

Pack 01 MUST NOT depend on Pack 02.

---

# 5. Overall Architecture

```text
Layer: Analytical Knowledge (Pack 02)
├── Domain Analysis Modules (01–10)
├── Scoring Knowledge (11)
├── Conflict Resolution Knowledge (12)
└── Analysis Pipeline Knowledge (13)
```

Pack 02 does not replace Pack 01 Schema, Registry, Validation, or Dictionary/Terminology.

---

# 6. Analytical Modules

See `PACK_02_MODULE_INDEX.md` and `PACK_02_STRUCTURE.md`.

Logical modules:

```text
01_strength_analysis
02_pattern_analysis
03_temperature_analysis
04_useful_god_analysis
05_ten_gods_analysis
06_combination_analysis
07_shensha_analysis
08_dayun_analysis
09_liunian_analysis
10_liuyue_analysis
11_scoring
12_conflict_resolution
13_analysis_pipeline
```

---

# 7. Dependency Rules

Allowed:

```text
Pack 02 module → Pack 01 knowledge / schema / registry IDs
Pack 02 higher pipeline module → Pack 02 lower analysis module (when approved)
Engine → Pack 02 (via Registry)
```

Forbidden:

```text
Pack 01 → Pack 02
Circular module dependencies
Embedding Pack 01 fundamental records inside Pack 02
Runtime engine code inside Pack 02 knowledge modules
```

---

# 8. Registry / Validation / Compiler Compatibility

Pack 02 MUST remain compatible with:

| Capability | Expectation |
|------------|-------------|
| Registry | Analytical objects registerable without forking Pack 01 Registry model |
| Validation | Schema / duplicate / dependency validation applicable |
| Compiler | Index/build outputs generatable from Pack 02 modules |

Detailed Pack 02 Registry / Validation / Compiler specs are skeletons in sibling documents.

---

# 9. Non-Goals

- No implementation in this document
- No business rules in this document
- No freeze declaration until content exists

---

# 10. Document Status

| Item | Status |
|------|--------|
| Architecture Skeleton | ✅ Initialized |
| Module Tree | ✅ Created |
| Business Rules | ❌ Not started |
| Freeze Ready | ❌ No |

**Next:** Populate module `SPEC.md` files without violating Pack 01 boundaries.
