# Temperature Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/02_temperature_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 02 — Second analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Temperature Engine evaluates the climatic balance of a completed BaZi natal chart.

It is the second analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable judgment of climate conditions that all downstream analytical stages may consume without re-deriving temperature logic.

The engine answers one question only:

> What is the climatic state of this natal chart, and does it require climate adjustment?

It does not answer questions of Day Master strength recomputation, pattern identity, Useful God selection, narrative meaning, or report presentation.

---

# 2. Responsibilities

The Temperature Engine is solely responsible for:

1. Accepting a validated analytical context produced after Calendar and Bazi construction.
2. Reading the published immutable `StrengthResult` from `AnalysisContext.strength_result`.
3. Loading and applying official Temperature Rules from the Temperature Rule Database.
4. Evaluating seasonal temperature influence on the natal chart.
5. Evaluating warm / cold balance.
6. Evaluating dryness.
7. Evaluating humidity.
8. Evaluating climate equilibrium.
9. Evaluating environmental support for climatic balance.
10. Evaluating climate adjustment requirements defined by Temperature Rules.
11. Resolving rule priority conflicts within the temperature domain.
12. Computing normalized component scores and an overall climate score.
13. Classifying overall climate into a canonical temperature level.
14. Recording matched rules, confidence, analytical reasoning, and execution metadata.
15. Publishing an immutable `TemperatureResult` for downstream consumption.

---

# 3. Scope

V1.0 scope is limited to **natal climate analysis**.

In scope:

- Seasonal temperature evaluation
- Warm / cold balance scoring and classification
- Dryness evaluation
- Humidity evaluation
- Climate equilibrium evaluation
- Environmental support contribution to climate
- Climate adjustment requirement determination
- Temperature-domain rule loading, matching, priority resolution, and scoring
- Deterministic confidence and traceability artifacts
- Publication of `TemperatureResult` into the Analysis Engine pipeline

The engine operates exclusively on structural chart facts, published `StrengthResult`, and Temperature Rules. It does not invent interpretive meaning beyond analytical climate evidence.

---

# 4. Out of Scope

The Temperature Engine must not perform any of the following:

| Concern | Owning Stage |
|---------|--------------|
| Day Master strength recomputation or reclassification | Strength Engine |
| Pattern / Ge Ju determination | Pattern Engine |
| Useful God, Favorable God, or Unfavorable God selection | Useful God Engine |
| Ten Gods quality, role analysis, or interpretive mapping beyond climate inputs | Ten Gods Engine |
| Combination, clash, harm, or transformation analysis as a chart-structure stage | Combination Engine |
| ShenSha detection or ranking | ShenSha Engine |
| Luck pillar generation or luck-layer evaluation | Luck Engine |
| Cross-stage analytical summary | Summary Engine |
| Natural-language interpretation or sentence generation | Interpretation Engine |
| Report rendering, templates, or portal presentation | Report Engine |
| Calendar conversion | Calendar Engine |
| Pillar construction or Day Master identity derivation | Bazi Engine |
| Mutation of upstream chart data, StrengthResult, or rule source data | Forbidden for all analysis stages |

Any feature that changes the semantic meaning of climate classification, or that expands the engine beyond temperature evaluation, requires a new major version.

---

# 5. Architecture Position

The Temperature Engine is stage **02** of the Analysis Engine pipeline. It executes only after Strength has completed, and only before Pattern.

```text
Calendar Engine
        │
        ▼
Bazi Engine
        │
        ▼
Strength Engine
        │
        ▼
Temperature Engine       ← this module (02)
        │
        ▼
Pattern Engine
        │
        ▼
Useful God Engine
        │
        ▼
Ten Gods Engine
        │
        ▼
Combination Engine
        │
        ▼
ShenSha Engine
        │
        ▼
Luck Engine
        │
        ▼
Summary Engine
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

Architectural constraints:

- The Temperature Engine never invokes downstream engines.
- The Temperature Engine never bypasses upstream Calendar, Bazi, or Strength stages.
- Downstream engines may read `TemperatureResult`; they must not recompute climate balance as a competing source of truth.
- Strength evaluation remains outside Temperature scope; Temperature consumes `StrengthResult` as published evidence only.

---

# 6. Input

## Primary Input

The Temperature Engine accepts one immutable analytical input:

```text
AnalysisContext
```

`AnalysisContext` is assembled by the Analysis Engine orchestrator from upstream products. Published `StrengthResult` is accessed through `AnalysisContext.strength_result`. The Temperature Engine does not accept raw birth data and does not accept `StrengthResult` as a separate function parameter.

## Required Upstream Content

The context must provide, at minimum:

| Domain | Required Content |
|--------|------------------|
| Calendar | Season, solar-term positioning, and related temporal metadata needed by Temperature Rules |
| Bazi | Four Pillars, Day Master identity, Day Master element and polarity |
| Structural facts | Hidden stems, Earthly Branch composition, Five Element distribution |
| Relational facts | Production/control and climate-relevant elemental relationships as chart facts |
| Strength | `AnalysisContext.strength_result` including strength level, score, and component evidence |
| Runtime | Rule-database version reference and execution metadata |

## Input Contract Rules

- Input is read-only.
- Missing mandatory chart facts or missing `AnalysisContext.strength_result` must fail validation before scoring.
- The engine does not reconstruct pillars from calendar data.
- The engine does not recompute Day Master strength.
- The engine does not load Pattern, Useful God, or Interpretation results as inputs.

---

# 7. Output

## Primary Output

The Temperature Engine publishes one immutable result object:

```text
TemperatureResult
```

## Canonical Result Fields

| Field Group | Description |
|-------------|-------------|
| Success state | Whether temperature evaluation completed successfully |
| `temperature_level` | Canonical climate classification (for example: `warm`, `cold`, `balanced`, `dry`, `humid`, or rule-defined composite levels) |
| `temperature_score` | Normalized overall climate score |
| Component scores | Seasonal temperature, warm/cold, dryness, humidity, equilibrium, and environmental support contributions |
| Adjustment flag | Whether climate adjustment is required, with rule-defined adjustment indicators |
| Confidence | Confidence of the matched-rule evaluation |
| Matched rules | Ordered identifiers of applied Temperature Rules |
| Analytical reasoning | Traceable climate rationale derived from matched rules and scores |
| Metadata | Execution trace, rule-version reference, and debug diagnostics |

## Output Contract Rules

- `TemperatureResult` is immutable after publication.
- `TemperatureResult` is the single source of truth for natal climate analysis inside the Analysis Engine pipeline.
- Downstream stages may project temperature fields into their own contexts; they must not alter the published `TemperatureResult`.
- Analytical reasoning is evidence for climate scoring. It is not an interpretation product and must not be treated as report narrative.

---

# 8. Dependencies

## Upstream Runtime Dependencies

| Dependency | Role |
|------------|------|
| Calendar Engine | Supplies temporal and seasonal facts |
| Bazi Engine | Supplies chart structure and Day Master identity |
| Strength Engine | Publishes `StrengthResult` into `AnalysisContext.strength_result` |
| Analysis Engine orchestrator | Supplies validated `AnalysisContext` and consumes `TemperatureResult` |

## Knowledge Dependencies

| Dependency | Role |
|------------|------|
| Temperature Rule Database | Canonical temperature business rules |
| Rule loading / registry services | Read-only access to temperature rule assets |
| Shared rule-contract utilities | Condition evaluation conventions shared across analysis stages |

## Explicit Non-Dependencies

The Temperature Engine must not depend on:

- Pattern Engine
- Useful God Engine
- Ten Gods Engine
- Combination Engine
- ShenSha Engine
- Luck Engine
- Summary Engine
- Interpretation Engine
- Report Engine

---

# 9. Public API Overview

V1.0 exposes one stable execution entry point.

```text
TemperatureEngine.evaluate(
    context: AnalysisContext
) -> TemperatureResult
```

## Public Surface

| Symbol | Stability | Role |
|--------|-----------|------|
| `TemperatureEngine` | Stable | Primary engine façade |
| `TemperatureEngine.evaluate` | Stable | Sole public execution method |
| `TemperatureResult` | Stable | Published output contract |
| `AnalysisContext` | Stable | Shared analytical input contract |
| `AnalysisContext.strength_result` | Stable | Upstream strength evidence accessed through context |

## Public API Guarantees

- Callers interact only through the public façade.
- Internal analyzers, scorers, loaders, and matchers are not part of the public contract.
- Alternate internal method names may exist for adapters, but V1.0 architectural stability is defined by `evaluate(context) -> TemperatureResult`.
- Breaking changes to the public surface require a major version increment.

---

# 10. Internal Modules Overview

Internal modules implement a single-responsibility pipeline within the temperature domain.

| Internal Module | Responsibility |
|-----------------|----------------|
| Context Validator | Validates required `AnalysisContext` fields and `AnalysisContext.strength_result` before evaluation |
| Temperature Context Adapter | Projects chart facts and strength evidence into a temperature-matching view |
| Rule Loader | Loads Temperature Rules and configuration in read-only mode |
| Rule Matcher | Evaluates rule conditions against the temperature context |
| Season Temperature Analyzer | Evaluates seasonal temperature contribution |
| Warm Cold Analyzer | Evaluates warm / cold balance |
| Dryness Analyzer | Evaluates dryness contribution |
| Humidity Analyzer | Evaluates humidity contribution |
| Equilibrium Analyzer | Evaluates climate equilibrium |
| Environmental Support Analyzer | Evaluates environmental support for climate |
| Adjustment Analyzer | Evaluates climate adjustment requirements |
| Priority Resolver | Resolves conflicts among matched temperature rules |
| Temperature Scorer | Aggregates component scores and classifies temperature level |
| Confidence Evaluator | Computes confidence from match quality and completeness |
| Result Builder | Assembles the immutable `TemperatureResult` |

Internal modules may be refactored freely within V1.x provided the public API and published result contract remain unchanged.

---

# 11. Directory Structure

```text
engines/analysis_engine/02_temperature_engine/
├── README.md                 # This architecture baseline
├── ARCHITECTURE.md
├── SPECIFICATION.md
├── MODELS.md
├── PUBLIC_API.md
├── FLOW.md
├── RULE_MAPPING.md
├── ALGORITHM.md
├── SCORING_MODEL.md
├── VALIDATION.md
├── ERROR_HANDLING.md
├── CACHE.md
├── CHANGELOG.md
├── __init__.py               # Public exports
├── engine.py                 # TemperatureEngine façade
├── models.py                 # TemperatureResult and related contracts
├── context.py                # Temperature-domain context view
├── loader.py                 # Temperature Rule loading
├── matcher.py                # Condition matching
├── analyzer.py               # Stage orchestration across analyzers
├── priority.py               # Priority resolution
├── scorer.py                 # Scoring and level classification
├── exceptions.py             # Temperature-domain errors
├── utils/
│   └── context_builder.py    # AnalysisContext → temperature view projection
└── analyzers/
    ├── season_temperature.py
    ├── warm_cold.py
    ├── dryness.py
    ├── humidity.py
    ├── equilibrium.py
    ├── environmental_support.py
    └── adjustment.py
```

Structural rules:

- All Temperature Engine source for the Analysis Engine pipeline resides under this module path.
- Temperature business knowledge remains in the Temperature Rule Database; this directory contains execution architecture only.
- This README defines the frozen V1.0 architectural baseline together with the accompanying documentation set.

---

# 12. Execution Flow

Evaluation is strictly sequential and deterministic.

```text
Receive AnalysisContext
        │
        ▼
Validate AnalysisContext
        │
        ▼
Read StrengthResult from AnalysisContext
        │
        ▼
Build Temperature Context View
        │
        ▼
Load Temperature Rules and Config
        │
        ▼
Match Season Temperature Rules
        │
        ▼
Match Warm / Cold Rules
        │
        ▼
Match Dryness Rules
        │
        ▼
Match Humidity Rules
        │
        ▼
Match Equilibrium Rules
        │
        ▼
Match Environmental Support Rules
        │
        ▼
Match Adjustment Rules
        │
        ▼
Resolve Priority Conflicts
        │
        ▼
Aggregate Component Scores
        │
        ▼
Classify Temperature Level
        │
        ▼
Evaluate Confidence
        │
        ▼
Build Immutable TemperatureResult
        │
        ▼
Return to Analysis Engine Orchestrator
```

Execution invariants:

- Identical `AnalysisContext` and identical Temperature Rule version must yield identical `TemperatureResult`.
- Validation failure terminates evaluation before scoring.
- No downstream engine is called during this flow.
- No Strength recomputation, Pattern, Useful God, Interpretation, or Report logic is executed inside this flow.

---

# 13. Design Principles

## Single Responsibility

The module evaluates natal climate balance and nothing else.

## Stage Isolation

Temperature communicates with the rest of the platform only through published contracts: `AnalysisContext` in, `TemperatureResult` out. Upstream strength evidence is read from `AnalysisContext.strength_result`.

## Determinism

Equal inputs and equal rule versions always produce equal outputs.

## Rule-Driven Knowledge

Business temperature knowledge lives in the Temperature Rule Database. Engine code executes matching, priority, and scoring mechanics.

## Explainability

Every published score and level must be traceable to matched rules and component contributions.

## Immutability

Published inputs and outputs are not mutated after creation.

## Fail Fast

Invalid or incomplete upstream context or missing `AnalysisContext.strength_result` stops evaluation immediately.

## Non-Overlap

Temperature must not absorb Strength recomputation, Pattern identity, Useful God selection, or Interpretation narrative generation.

## Downstream Neutrality

The engine publishes climate facts usable by later stages, without encoding later-stage decisions.

## Testability

Each internal analyzer and the scoring stage must be independently verifiable against golden Temperature Rule examples.

---

# 14. Future Extensions

Future major or minor versions may introduce extensions such as:

- Alternate climate scoring strategies selectable by configuration
- Rule-version switching without public API breakage
- Regional or school-specific climate profiles expressed as rule packs
- Enhanced explainability payloads for audit and QA tooling
- Performance optimizations in matching and scoring
- Additional climate component dimensions approved by architecture review

Extension constraints:

- Extensions must preserve the V1 public API within the 1.x series.
- Extensions must not move Strength, Pattern, Useful God, or Interpretation responsibilities into this module.
- Any change that alters the meaning of `temperature_level` or replaces `TemperatureResult` as the climate source of truth requires a major version.

---

# 15. Version

| Item | Value |
|------|-------|
| Architecture Version | 1.0.0 |
| Status | Frozen |
| Compatibility | Analysis Engine V1.x |
| Public API Stability | Guaranteed within V1.x |
| Result Contract | `TemperatureResult` is authoritative for natal climate analysis |

This README is the official V1.0 architecture baseline for `engines/analysis_engine/02_temperature_engine`.

Breaking architectural changes require an explicit major version increment and a replacement architecture baseline.

---

## Architecture Coexistence

This directory is part of the **legacy stage documentation/engine tree**.

Canonical architecture skeleton packages live at the Analysis Engine root (`models/`, `pipeline/`, `analyzers/`, `registry/`, `validation/`, …).

See `engines/analysis_engine/README.md` and `ANALYSIS_ENGINE_AUDIT.md`.
