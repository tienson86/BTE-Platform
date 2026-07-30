# Strength Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/01_strength_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 01 — First analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Strength Engine evaluates the structural strength of the **Day Master (Nhật Chủ)** within a completed BaZi chart.

It is the first analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable judgment of Day Master strength that all downstream analytical stages may consume without re-deriving strength logic.

The engine answers one question only:

> How strong is the Day Master in this natal chart?

It does not answer questions of climate balance, pattern identity, Useful God selection, narrative meaning, or report presentation.

---

# 2. Responsibilities

The Strength Engine is solely responsible for:

1. Accepting a validated analytical context produced after Calendar and Bazi construction.
2. Loading and applying official Strength Rules from the Strength Rule Database.
3. Evaluating seasonal command influence on the Day Master.
4. Evaluating rooting of the Day Master in the Earthly Branches.
5. Evaluating supportive forces acting on the Day Master.
6. Evaluating controlling forces acting on the Day Master.
7. Evaluating draining and exhausting forces acting on the Day Master.
8. Evaluating multi-factor strength combinations and special-case strength overrides defined by Strength Rules.
9. Resolving rule priority conflicts within the strength domain.
10. Computing normalized component scores and an overall strength score.
11. Classifying overall strength into a canonical strength level.
12. Recording matched rules, confidence, analytical reasoning, and execution metadata.
13. Publishing an immutable `StrengthResult` for downstream consumption.

---

# 3. Scope

V1.0 scope is limited to **natal Day Master strength analysis**.

In scope:

- Day Master strength scoring and classification
- Strength-domain rule loading, matching, priority resolution, and scoring
- Season-command contribution to strength
- Root contribution to strength
- Support contribution to strength
- Control contribution to strength
- Drain contribution to strength
- Strength-domain combination and special-case adjustments
- Deterministic confidence and traceability artifacts
- Publication of `StrengthResult` into the Analysis Engine pipeline

The engine operates exclusively on structural chart facts and Strength Rules. It does not invent interpretive meaning beyond analytical strength evidence.

---

# 4. Out of Scope

The Strength Engine must not perform any of the following:

| Concern | Owning Stage |
|---------|--------------|
| Climate, warmth, coldness, dryness, or humidity judgment | Temperature Engine |
| Pattern / Ge Ju determination | Pattern Engine |
| Useful God, Favorable God, or Unfavorable God selection | Useful God Engine |
| Ten Gods quality, role analysis, or interpretive mapping beyond strength inputs | Ten Gods Engine |
| Combination, clash, harm, or transformation analysis as a chart-structure stage | Combination Engine |
| ShenSha detection or ranking | ShenSha Engine |
| Luck pillar generation or luck-layer evaluation | Luck Engine |
| Cross-stage analytical summary | Summary Engine |
| Natural-language interpretation or sentence generation | Interpretation Engine |
| Report rendering, templates, or portal presentation | Report Engine |
| Calendar conversion | Calendar Engine |
| Pillar construction or Day Master identity derivation | Bazi Engine |
| Mutation of upstream chart data or rule source data | Forbidden for all analysis stages |

Any feature that changes the semantic meaning of Day Master strength classification, or that expands the engine beyond strength evaluation, requires a new major version.

---

# 5. Architecture Position

The Strength Engine is stage **01** of the Analysis Engine pipeline. It executes only after Calendar and Bazi have completed, and only before Temperature.

```text
Calendar Engine
        │
        ▼
Bazi Engine
        │
        ▼
Strength Engine          ← this module (01)
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

- The Strength Engine never invokes downstream engines.
- The Strength Engine never bypasses upstream Calendar or Bazi stages.
- Downstream engines may read `StrengthResult`; they must not recompute Day Master strength as a competing source of truth.
- Temperature Engine consumes strength outputs where required, but strength evaluation itself remains outside Temperature scope.

---

# 6. Input

## Primary Input

The Strength Engine accepts one immutable analytical input:

```text
AnalysisContext
```

`AnalysisContext` is assembled by the Analysis Engine orchestrator from upstream products. The Strength Engine does not accept raw birth data.

## Required Upstream Content

The context must provide, at minimum:

| Domain | Required Content |
|--------|------------------|
| Calendar | Season, solar-term positioning, and related temporal metadata needed by Strength Rules |
| Bazi | Four Pillars, Day Master identity, Day Master element and polarity |
| Structural facts | Hidden stems, Earthly Branch composition, Five Element distribution |
| Relational facts | Ten Gods labels and production/control relationships as chart facts |
| Runtime | Rule-database version reference and execution metadata |

## Input Contract Rules

- Input is read-only.
- Missing mandatory chart facts must fail validation before scoring.
- The engine does not reconstruct pillars from calendar data.
- The engine does not load Temperature, Pattern, Useful God, or Interpretation results as inputs.

---

# 7. Output

## Primary Output

The Strength Engine publishes one immutable result object:

```text
StrengthResult
```

## Canonical Result Fields

| Field Group | Description |
|-------------|-------------|
| Success state | Whether strength evaluation completed successfully |
| `strength_level` | Canonical classification: `strong`, `weak`, or `balanced` |
| `strength_score` | Normalized overall Day Master strength score |
| Component scores | Season, root, support, control, and drain contributions |
| Confidence | Confidence of the matched-rule evaluation |
| Matched rules | Ordered identifiers of applied Strength Rules |
| Analytical reasoning | Traceable strength rationale derived from matched rules and scores |
| Metadata | Execution trace, rule-version reference, and debug diagnostics |

## Output Contract Rules

- `StrengthResult` is immutable after publication.
- `StrengthResult` is the single source of truth for Day Master strength inside the Analysis Engine pipeline.
- Downstream stages may project strength fields into their own contexts; they must not alter the published `StrengthResult`.
- Analytical reasoning is evidence for strength scoring. It is not an interpretation product and must not be treated as report narrative.

---

# 8. Dependencies

## Upstream Runtime Dependencies

| Dependency | Role |
|------------|------|
| Calendar Engine | Supplies temporal and seasonal facts |
| Bazi Engine | Supplies chart structure and Day Master identity |
| Analysis Engine orchestrator | Supplies validated `AnalysisContext` and consumes `StrengthResult` |

## Knowledge Dependencies

| Dependency | Role |
|------------|------|
| Strength Rule Database | Canonical strength business rules |
| Rule loading / registry services | Read-only access to strength rule assets |
| Shared rule-contract utilities | Condition evaluation conventions shared across analysis stages |

## Explicit Non-Dependencies

The Strength Engine must not depend on:

- Temperature Engine
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
StrengthEngine.evaluate(context: AnalysisContext) -> StrengthResult
```

## Public Surface

| Symbol | Stability | Role |
|--------|-----------|------|
| `StrengthEngine` | Stable | Primary engine façade |
| `StrengthEngine.evaluate` | Stable | Sole public execution method |
| `StrengthResult` | Stable | Published output contract |
| `AnalysisContext` | Stable | Shared analytical input contract |

## Public API Guarantees

- Callers interact only through the public façade.
- Internal analyzers, scorers, loaders, and matchers are not part of the public contract.
- Alternate internal method names may exist for adapters, but V1.0 architectural stability is defined by `evaluate(context) -> StrengthResult`.
- Breaking changes to the public surface require a major version increment.

---

# 10. Internal Modules Overview

Internal modules implement a single-responsibility pipeline within the strength domain.

| Internal Module | Responsibility |
|-----------------|----------------|
| Context Validator | Validates required `AnalysisContext` fields before evaluation |
| Strength Context Adapter | Projects chart facts into a strength-matching view |
| Rule Loader | Loads Strength Rules and configuration in read-only mode |
| Rule Matcher | Evaluates rule conditions against the strength context |
| Season Analyzer | Evaluates seasonal-command contribution |
| Root Analyzer | Evaluates Day Master rooting contribution |
| Support Analyzer | Evaluates supportive contribution |
| Control Analyzer | Evaluates controlling contribution |
| Drain Analyzer | Evaluates draining contribution |
| Combination Analyzer | Evaluates strength-domain multi-factor adjustments |
| Special-Case Analyzer | Applies strength-domain special overrides |
| Priority Resolver | Resolves conflicts among matched strength rules |
| Strength Scorer | Aggregates component scores and classifies strength level |
| Confidence Evaluator | Computes confidence from match quality and completeness |
| Result Builder | Assembles the immutable `StrengthResult` |

Internal modules may be refactored freely within V1.x provided the public API and published result contract remain unchanged.

---

# 11. Directory Structure

```text
engines/analysis_engine/01_strength_engine/
├── README.md                 # This architecture baseline
├── __init__.py               # Public exports
├── engine.py                 # StrengthEngine façade
├── models.py                 # StrengthResult and related contracts
├── context.py                # Strength-domain context view
├── loader.py                 # Strength Rule loading
├── matcher.py                # Condition matching
├── analyzer.py               # Stage orchestration across analyzers
├── priority.py               # Priority resolution
├── scorer.py                 # Scoring and level classification
├── exceptions.py             # Strength-domain errors
├── utils/
│   └── context_builder.py    # AnalysisContext → strength view projection
└── analyzers/
    ├── season.py
    ├── root.py
    ├── support.py
    ├── control.py
    ├── drain.py
    ├── combination.py
    └── special_case.py
```

Structural rules:

- All Strength Engine source for the Analysis Engine pipeline resides under this module path.
- Strength business knowledge remains in the Strength Rule Database; this directory contains execution architecture only.
- Documentation beyond this README may be added later, but this file alone defines the frozen V1.0 architectural baseline.

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
Build Strength Context View
        │
        ▼
Load Strength Rules and Config
        │
        ▼
Match Season Rules
        │
        ▼
Match Root Rules
        │
        ▼
Match Support Rules
        │
        ▼
Match Control Rules
        │
        ▼
Match Drain Rules
        │
        ▼
Match Combination and Special-Case Rules
        │
        ▼
Resolve Priority Conflicts
        │
        ▼
Aggregate Component Scores
        │
        ▼
Classify Strength Level
        │
        ▼
Evaluate Confidence
        │
        ▼
Build Immutable StrengthResult
        │
        ▼
Return to Analysis Engine Orchestrator
```

Execution invariants:

- Identical `AnalysisContext` and identical Strength Rule version must yield identical `StrengthResult`.
- Validation failure terminates evaluation before scoring.
- No downstream engine is called during this flow.
- No Temperature, Pattern, Useful God, Interpretation, or Report logic is executed inside this flow.

---

# 13. Design Principles

## Single Responsibility

The module evaluates Day Master strength and nothing else.

## Stage Isolation

Strength communicates with the rest of the platform only through published contracts: `AnalysisContext` in, `StrengthResult` out.

## Determinism

Equal inputs and equal rule versions always produce equal outputs.

## Rule-Driven Knowledge

Business strength knowledge lives in the Strength Rule Database. Engine code executes matching, priority, and scoring mechanics.

## Explainability

Every published score and level must be traceable to matched rules and component contributions.

## Immutability

Published inputs and outputs are not mutated after creation.

## Fail Fast

Invalid or incomplete upstream context stops evaluation immediately.

## Non-Overlap

Strength must not absorb Temperature climate judgment, Pattern identity, Useful God selection, or Interpretation narrative generation.

## Downstream Neutrality

The engine publishes strength facts usable by later stages, without encoding later-stage decisions.

## Testability

Each internal analyzer and the scoring stage must be independently verifiable against golden Strength Rule examples.

---

# 14. Future Extensions

Future major or minor versions may introduce extensions such as:

- Alternate strength scoring strategies selectable by configuration
- Rule-version switching without public API breakage
- Regional or school-specific strength profiles expressed as rule packs
- Enhanced explainability payloads for audit and QA tooling
- Performance optimizations in matching and scoring
- Additional strength component dimensions approved by architecture review

Extension constraints:

- Extensions must preserve the V1 public API within the 1.x series.
- Extensions must not move Temperature, Pattern, Useful God, or Interpretation responsibilities into this module.
- Any change that alters the meaning of `strength_level` or replaces `StrengthResult` as the strength source of truth requires a major version.

---

# 15. Version

| Item | Value |
|------|-------|
| Architecture Version | 1.0.0 |
| Status | Frozen |
| Compatibility | Analysis Engine V1.x |
| Public API Stability | Guaranteed within V1.x |
| Result Contract | `StrengthResult` is authoritative for Day Master strength |

This README is the official V1.0 architecture baseline for `engines/analysis_engine/01_strength_engine`.

Breaking architectural changes require an explicit major version increment and a replacement architecture baseline.
