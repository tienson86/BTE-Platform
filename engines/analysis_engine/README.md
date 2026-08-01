# Analysis Engine

> **Path:** `engines/analysis_engine/`
>
> **Architecture Version:** `0.0.0-architecture` (`VERSION`)
>
> **Status:** Architecture skeleton + legacy stage engines coexist
>
> **Depends On:** Pack 01 Registry / Validation / Compiler contracts (read-only)

---

## Purpose

The Analysis Engine defines the orchestration architecture for analytical stages.

This README documents **directory layout and architecture packages only**.
It does not document BaZi business rules or analysis algorithms.

---

## Architecture Layout

```text
engines/analysis_engine/
├── engine.py                 # Orchestration skeleton
├── config.py
├── constants.py
├── VERSION / CHANGELOG.md / README.md
├── ANALYSIS_ENGINE_AUDIT.md
│
├── models/                   # Immutable result/context dataclasses
├── interfaces/               # Public ABC contracts
├── types/                    # Shared enums / aliases / Literal / TypedDict
├── exceptions/               # Exception hierarchy
│
├── context/                  # Typed context packages
├── results/                  # Result infrastructure runtime
├── events/                   # Internal in-process event framework
├── metrics/                  # Infrastructure metrics collectors
├── cache/                    # In-memory cache subsystem
├── api/                      # Public API facade (+ legacy FastAPI coexistence)
├── pipeline/                 # Pipeline orchestration interfaces + contracts
├── analyzers/                # Analyzer module skeletons + contracts
├── registry/                 # Registry layer (Pack 01 compatible)
├── compiler/                 # Compiler layer interfaces
├── validation/               # Expanded validator framework
├── validators/               # Validator architecture skeleton
│
├── scoring/                  # Scoring package skeleton
├── conflict/                 # Conflict package skeleton
├── cache/ metrics/ utils/ adapters/
│
├── docs/                     # Architecture documentation tree
└── (legacy stage engines / runtime / api — coexistence)
```

---

## Core Architecture Packages

| Package | Role |
|---------|------|
| `models/` | Immutable dataclasses (`AnalysisContext`, `AnalysisResult`, …) |
| `interfaces/` | Public ABCs (`AnalysisEngineInterface`, providers, …) |
| `types/` | Shared type system |
| `exceptions/` | `AnalysisError` hierarchy |
| `context/` | Typed context models + lifecycle runtime |
| `results/` | Result builder/merger/aggregator/serializer/repository |
| `events/` | Internal in-process event bus / dispatcher / listeners |
| `metrics/` | Execution / performance / rule / pipeline / result metrics |
| `cache/` | In-memory cache manager / policy / context / registry caches |
| `api/` | Public API facade (`AnalysisEngineAPI`) + legacy FastAPI app |
| `pipeline/` | Pipeline interfaces + `contracts.py` |
| `analyzers/` | Twelve analyzer skeletons + contracts |
| `registry/` | Registry interfaces + Pack 01-compatible contracts |
| `compiler/` | Compiler interfaces |
| `validation/` | Context/result/decision/score/pipeline/schema/metadata validators |
| `validators/` | Earlier validator skeleton layer |
| `docs/` | Architecture docs placeholders |
| `tests/analysis_engine/` | Pytest framework skeleton |

---

## Analyzers

| Analyzer | Path |
|----------|------|
| Strength | `analyzers/strength/` |
| Pattern | `analyzers/pattern/` |
| Temperature | `analyzers/temperature/` |
| Useful God | `analyzers/useful_god/` |
| Ten Gods | `analyzers/ten_gods/` |
| Combination | `analyzers/combination/` |
| Shen Sha | `analyzers/shensha/` |
| Dayun | `analyzers/dayun/` |
| Liunian | `analyzers/liunian/` |
| Liuyue | `analyzers/liuyue/` |
| Scoring | `analyzers/scoring/` |
| Conflict | `analyzers/conflict/` |

Each analyzer contains: `README`, `VERSION`, `CHANGELOG`, `SPEC`, `analyzer.py`, `models.py`, `interfaces.py`, `validator.py`, `contracts.py`.

---

## Dependency Direction

```text
Analysis Engine
      │
      ▼
Pack 02 Analytical Knowledge (when authored)
      │
      ▼
Pack 01 Fundamental Theory / Knowledge Infrastructure
```

Forbidden: Pack 01 depending on Analysis Engine. Analysis Engine must not mutate Pack 01 source knowledge.

---

## Coexistence Note

Legacy directories (`01_strength_engine` … `10_report_generator`, `runtime`, `api`, etc.) remain present.

New architecture packages are the canonical skeleton for future implementation.
See `ANALYSIS_ENGINE_AUDIT.md` for consistency status.

---

## Related Architecture Docs

- `docs/architecture/`
- `docs/pipeline/`
- `docs/analyzers/`
- `docs/registry/`
- `docs/compiler/`
- `docs/validation/`
- `docs/api/`
- `docs/examples/`
- `ARCHITECTURE.md` (legacy baseline doc)
- `PIPELINE.md` / `PUBLIC_API.md` / `SHARED_MODELS.md` (legacy baseline docs)
