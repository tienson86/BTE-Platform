# Pattern Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/03_pattern_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 03 — Third analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Pattern Engine determines the natal chart Pattern (Ge Ju / 格局) within a completed BaZi chart.

It is the third analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable pattern judgment that all downstream analytical stages may consume without re-deriving pattern logic.

The engine answers one question only:

> What is the governing Pattern (Ge Ju / 格局) of this natal chart?

It does not answer questions of Day Master strength recomputation, climate recomputation, Useful God selection, narrative meaning, or report presentation.

---

# 2. Responsibilities

The Pattern Engine is solely responsible for:

1. Accepting a validated analytical context produced after Calendar and Bazi construction.
2. Reading published `StrengthResult` from `AnalysisContext.strength_result`.
3. Reading published `TemperatureResult` from `AnalysisContext.temperature_result`.
4. Loading and applying official Pattern Rules from the Pattern Rule Database.
5. Analysing natal chart structure relevant to pattern determination.
6. Evaluating Day Master relationship with chart composition.
7. Identifying standard patterns.
8. Identifying transformed patterns.
9. Identifying special patterns.
10. Identifying follow patterns.
11. Generating and evaluating competing pattern candidates.
12. Resolving pattern conflicts and priority contests.
13. Computing pattern confidence.
14. Recording matched rules, rejected candidates, analytical reasoning, diagnostics, and execution metadata.
15. Publishing an immutable `PatternResult` for downstream consumption.

---

# 3. Scope

V1.0 scope is limited to **natal Pattern (Ge Ju / 格局) determination**.

In scope:

- Chart structure analysis for pattern purposes
- Day Master relationship evaluation against chart composition
- Standard pattern identification
- Transformation pattern identification
- Special pattern identification
- Follow pattern identification
- Mixed and exceptional pattern support through Pattern Rules
- Competing pattern candidate generation and evaluation
- Conflict resolution and priority resolution
- Pattern-domain rule loading, matching, priority resolution, and scoring
- Pattern confidence computation
- Deterministic confidence and traceability artifacts
- Publication of `PatternResult` into the Analysis Engine pipeline and `AnalysisResult`

The engine operates exclusively on structural chart facts, published upstream stage results attached to AnalysisContext, and Pattern Rules. It does not invent interpretive meaning beyond analytical pattern evidence.

---

# 4. Out of Scope

The Pattern Engine must not perform any of the following:

| Concern | Owning Stage |
|---------|--------------|
| Day Master strength recomputation or reclassification | Strength Engine |
| Climate, warmth, coldness, dryness, or humidity recomputation | Temperature Engine |
| Useful God, Favorable God, or Unfavorable God selection | Useful God Engine |
| Ten Gods quality analysis | Ten Gods Engine |
| Combination, clash, harm, or transformation analysis as a chart-structure stage | Combination Engine |
| ShenSha detection or ranking | ShenSha Engine |
| Luck pillar generation or luck-layer evaluation | Luck Engine |
| Cross-stage analytical summary | Summary Engine |
| Natural-language interpretation or sentence generation | Interpretation Engine |
| Report rendering, templates, or portal presentation | Report Engine |
| Calendar conversion | Calendar Engine |
| Pillar construction or Day Master identity derivation | Bazi Engine |
| Mutation of upstream chart data or rule source data | Forbidden for all analysis stages |

Any feature that changes the semantic meaning of Pattern classification, or that expands the engine beyond pattern determination, requires a new major version.

---

# 5. Architecture Position

The Pattern Engine is stage **03** of the Analysis Engine pipeline. It executes only after Strength and Temperature have completed, and only before Useful God.

```text
Strength Engine
        │
        ▼
Temperature Engine
        │
        ▼
Pattern Engine           ← this module (03)
        │
        ▼
Useful God Engine
```

Full pipeline context:

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
Temperature Engine
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

- The Pattern Engine never invokes downstream engines.
- The Pattern Engine never bypasses upstream Calendar, Bazi, Strength, or Temperature stages.
- Downstream engines may read `PatternResult`; they must not recompute Pattern as a competing source of truth.
- Strength and Temperature evaluation remain outside Pattern scope; Pattern consumes their published results from AnalysisContext only.

---

# 6. Input

## Primary Input

The Pattern Engine accepts one immutable analytical input:

```text
AnalysisContext
```

`AnalysisContext` is assembled by the Analysis Engine orchestrator from upstream products. Published upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
```

The Pattern Engine does not accept raw birth data and does not accept StrengthResult or TemperatureResult as separate function parameters.

No additional input models shall be introduced.

## Required Upstream Content

The context must provide, at minimum:

| Domain | Required Content |
|--------|------------------|
| Calendar | Season, solar-term positioning, and related temporal metadata needed by Pattern Rules |
| Bazi | Four Pillars, Day Master identity, Day Master element and polarity |
| Structural facts | Hidden stems, Earthly Branch composition, Five Element distribution |
| Relational facts | Ten Gods labels and Day Master relationships as chart facts |
| Strength | `AnalysisContext.strength_result` |
| Temperature | `AnalysisContext.temperature_result` |
| Runtime | Rule-database version reference and execution metadata |

## Input Contract Rules

- Input is read-only.
- Missing mandatory chart facts or missing upstream stage results must fail validation before scoring.
- The engine does not reconstruct pillars from calendar data.
- The engine does not recompute Day Master strength.
- The engine does not recompute climate balance.
- The engine does not load Useful God or Interpretation results as inputs.

---

# 7. Output

## Primary Output

The Pattern Engine publishes one immutable result object:

```text
PatternResult
```

`PatternResult` becomes part of `AnalysisResult`.

## Canonical Result Fields

| Field Group | Description |
|-------------|-------------|
| Identified pattern | Canonical governing Pattern (Ge Ju / 格局) |
| Pattern category | Category such as standard, special, follow, transformation, mixed, or exceptional |
| Confidence | Confidence of the matched-rule evaluation |
| Matched rules | Ordered identifiers of applied Pattern Rules |
| Rejected candidates | Pattern candidates considered and rejected during resolution |
| Reasoning | Traceable pattern rationale derived from matched rules and resolution evidence |
| Diagnostics | Debug and audit diagnostics |
| Metadata | Execution trace and rule-version reference |

## Output Contract Rules

- `PatternResult` is immutable after publication.
- `PatternResult` is the single source of truth for natal Pattern inside the Analysis Engine pipeline.
- Downstream stages may project pattern fields into their own contexts; they must not alter the published `PatternResult`.
- Analytical reasoning is evidence for pattern determination. It is not an interpretation product and must not be treated as report narrative.

---

# 8. Dependencies

## Upstream Runtime Dependencies

| Dependency | Role |
|------------|------|
| Calendar Engine | Supplies temporal and seasonal facts |
| Bazi Engine | Supplies chart structure and Day Master identity |
| Strength Engine | Publishes `StrengthResult` into `AnalysisContext.strength_result` |
| Temperature Engine | Publishes `TemperatureResult` into `AnalysisContext.temperature_result` |
| Analysis Engine orchestrator | Supplies validated `AnalysisContext` and consumes `PatternResult` |

## Knowledge Dependencies

| Dependency | Role |
|------------|------|
| Pattern Rule Database (`knowledge/rule_database/04_pattern_rules/`) | Canonical pattern business rules |
| Rule loading / registry services | Read-only access to pattern rule assets |
| Shared rule-contract utilities | Condition evaluation conventions shared across analysis stages |

## Explicit Non-Dependencies

The Pattern Engine must not depend on:

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
PatternEngine.evaluate(
    context: AnalysisContext
) -> PatternResult
```

## Public Surface

| Symbol | Stability | Role |
|--------|-----------|------|
| `PatternEngine` | Stable | Primary engine façade |
| `PatternEngine.evaluate` | Stable | Sole public execution method |
| `PatternResult` | Stable | Published output contract |
| `AnalysisContext` | Stable | Shared analytical input contract |
| `AnalysisContext.strength_result` | Stable | Upstream strength evidence accessed through context |
| `AnalysisContext.temperature_result` | Stable | Upstream temperature evidence accessed through context |

## Public API Guarantees

- Callers interact only through the public façade.
- No additional public methods are exposed.
- Upstream stage results are never passed as function parameters.
- Internal analyzers, scorers, loaders, and matchers are not part of the public contract.
- V1.0 architectural stability is defined by `evaluate(context) -> PatternResult`.
- Breaking changes to the public surface require a major version increment.

---

# 10. Internal Modules Overview

Internal modules implement a single-responsibility pipeline within the pattern domain.

| Internal Module | Responsibility |
|-----------------|----------------|
| Context Validator | Validates required `AnalysisContext` fields and upstream stage results before evaluation |
| Pattern Context Adapter | Projects chart facts and upstream evidence into a pattern-matching view |
| Rule Loader | Loads Pattern Rules and configuration in read-only mode |
| Rule Matcher | Evaluates rule conditions against the pattern context |
| Structure Analyzer | Analyses chart structure for pattern eligibility |
| Day Master Relation Analyzer | Evaluates Day Master relationship with chart composition |
| Standard Pattern Analyzer | Identifies standard pattern candidates |
| Transformation Pattern Analyzer | Identifies transformed pattern candidates |
| Special Pattern Analyzer | Identifies special pattern candidates |
| Follow Pattern Analyzer | Identifies follow pattern candidates |
| Mixed / Exceptional Analyzer | Evaluates mixed and exceptional pattern candidates |
| Candidate Generator | Generates the competing pattern candidate set |
| Candidate Evaluator | Evaluates candidate strength and eligibility |
| Conflict Resolver | Resolves pattern conflicts |
| Priority Resolver | Resolves priority contests among matched pattern rules and candidates |
| Pattern Scorer | Aggregates scores and classifies pattern identity |
| Confidence Evaluator | Computes confidence from match quality and completeness |
| Result Builder | Assembles the immutable `PatternResult` |

Internal modules may be refactored freely within V1.x provided the public API and published result contract remain unchanged.

---

# 11. Directory Structure

```text
engines/analysis_engine/03_pattern_engine/
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
├── engine.py                 # PatternEngine façade
├── models.py                 # PatternResult and related contracts
├── context.py                # Pattern-domain context view
├── loader.py                 # Pattern Rule loading
├── matcher.py                # Condition matching
├── analyzer.py               # Stage orchestration across analyzers
├── priority.py               # Priority and conflict resolution
├── scorer.py                 # Scoring and pattern classification
├── exceptions.py             # Pattern-domain errors
├── utils/
│   └── context_builder.py    # AnalysisContext → pattern view projection
└── analyzers/
    ├── structure.py
    ├── day_master_relation.py
    ├── standard_pattern.py
    ├── transformation_pattern.py
    ├── special_pattern.py
    ├── follow_pattern.py
    ├── mixed_exceptional.py
    ├── candidate_generator.py
    └── candidate_evaluator.py
```

Structural rules:

- All Pattern Engine source for the Analysis Engine pipeline resides under this module path.
- Pattern business knowledge remains in `knowledge/rule_database/04_pattern_rules/`; this directory contains execution architecture only.
- This README defines the frozen V1.0 architectural baseline together with the accompanying documentation set.

---

# 12. Execution Flow

Evaluation is strictly sequential and deterministic.

```text
Receive AnalysisContext
        │
        ▼
Validate Context
        │
        ▼
Read StrengthResult
        │
        ▼
Read TemperatureResult
        │
        ▼
Load Pattern Rules
        │
        ▼
Analyse Structure
        │
        ▼
Generate Pattern Candidates
        │
        ▼
Evaluate Candidates
        │
        ▼
Resolve Priority
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable PatternResult
        │
        ▼
Publish PatternResult
```

Execution invariants:

- Identical `AnalysisContext` and identical Pattern Rule version must yield identical `PatternResult`.
- Validation failure terminates evaluation before scoring.
- No downstream engine is called during this flow.
- No Strength recomputation, Temperature recomputation, Useful God, Interpretation, or Report logic is executed inside this flow.

---

# 13. Design Principles

## Single Responsibility

The module determines natal Pattern (Ge Ju / 格局) and nothing else.

## Stage Isolation

Pattern communicates with the rest of the platform only through published contracts: `AnalysisContext` in, `PatternResult` out. Upstream evidence is read from `AnalysisContext.strength_result` and `AnalysisContext.temperature_result`.

## Determinism

Equal inputs and equal rule versions always produce equal outputs.

## Rule-Driven Knowledge

Business pattern knowledge lives in the Pattern Rule Database. Engine code executes matching, priority, and scoring mechanics.

## Explainability

Every published pattern identity must be traceable to matched rules, rejected candidates, and resolution evidence.

## Immutability

Published inputs and outputs are not mutated after creation.

## Fail Fast

Invalid or incomplete upstream context or missing upstream stage results stops evaluation immediately.

## Non-Overlap

Pattern must not absorb Strength recomputation, Temperature recomputation, Useful God selection, or Interpretation narrative generation.

## Downstream Neutrality

The engine publishes pattern facts usable by later stages, without encoding later-stage decisions.

## Extensibility

Pattern categories and analyzers may expand within V1.x without breaking the public API.

## Testability

Each internal analyzer and the scoring stage must be independently verifiable against golden Pattern Rule examples.

---

# 14. Future Extensions

Future major or minor versions may introduce extensions such as:

- Additional pattern categories expressed as rule packs
- Alternate pattern resolution strategies selectable by configuration
- Rule-version switching without public API breakage
- Regional or school-specific pattern profiles
- Enhanced explainability payloads for audit and QA tooling
- Performance optimizations in matching and scoring

Extension constraints:

- Extensions must preserve the V1 public API within the 1.x series.
- Extensions must not move Strength, Temperature, Useful God, or Interpretation responsibilities into this module.
- Any change that alters the meaning of Pattern identity or replaces `PatternResult` as the pattern source of truth requires a major version.

---

# 15. Version

| Item | Value |
|------|-------|
| Architecture Version | 1.0.0 |
| Status | Frozen Architecture Baseline |
| Compatibility | Analysis Engine V1.x |
| Public API Stability | Guaranteed within V1.x |
| Result Contract | `PatternResult` is authoritative for natal Pattern (Ge Ju / 格局) |

This README is the official V1.0 architecture baseline for `engines/analysis_engine/03_pattern_engine`.

Breaking architectural changes require an explicit major version increment and a replacement architecture baseline.
