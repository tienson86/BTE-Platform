# Useful God Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/04_useful_god_engine` |
| Module Type | Analysis Engine Stage |
| Stage Order | 04 — Fourth analytical stage |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Useful God Engine determines the natal chart's balancing elements: Yong Shen (Useful God / Dụng Thần), Xi Shen (Favorable God / Hỷ Thần), Ji Shen (Unfavorable God / Kỵ Thần), and Xian Shen (Neutral God / Nhàn Thần).

It is the fourth analytical stage of the Analysis Engine pipeline. Its purpose is to produce a single, deterministic, explainable Useful God judgment that all downstream analytical stages may consume without re-deriving Useful God logic.

The engine answers one question only:

> Which elements balance this natal chart, and which elements hinder that balance?

It does not answer questions of Day Master strength recomputation, climate recomputation, Pattern recomputation, Ten Gods quality analysis, narrative meaning, or report presentation.

---

# 2. Responsibilities

The Useful God Engine is solely responsible for:

1. Accepting a validated analytical context produced after Calendar and Bazi construction.
2. Reading published `StrengthResult` from `AnalysisContext.strength_result`.
3. Reading published `TemperatureResult` from `AnalysisContext.temperature_result`.
4. Reading published `PatternResult` from `AnalysisContext.pattern_result`.
5. Loading and applying official Useful God Rules from the Useful God Rule Database.
6. Evaluating strength balance requirements.
7. Evaluating climate balance requirements.
8. Evaluating pattern requirements.
9. Evaluating five-element equilibrium.
10. Evaluating supporting and controlling relationships.
11. Evaluating adjustment priorities.
12. Generating and evaluating Useful God candidates.
13. Resolving multiple candidate contests and conflicts.
14. Determining Yong Shen, Xi Shen, Ji Shen, and Xian Shen.
15. Computing Useful God confidence.
16. Recording matched rules, rejected candidates, analytical reasoning, diagnostics, and execution metadata.
17. Publishing an immutable `UsefulGodResult` for downstream consumption.

---

# 3. Scope

V1.0 scope is limited to **natal Useful God determination**.

In scope:

- Yong Shen (Useful God / Dụng Thần) determination
- Xi Shen (Favorable God / Hỷ Thần) determination
- Ji Shen (Unfavorable God / Kỵ Thần) determination
- Xian Shen (Neutral God / Nhàn Thần) determination
- Strength-balance, climate-balance, and pattern-requirement evaluation as Useful God inputs
- Five-element equilibrium evaluation
- Supporting and controlling relationship evaluation
- Adjustment priority evaluation
- Primary, secondary, and alternative candidate handling
- Candidate priority and conflict resolution
- Useful God-domain rule loading, matching, priority resolution, and scoring
- Confidence computation
- Deterministic confidence and traceability artifacts
- Publication of `UsefulGodResult` into the Analysis Engine pipeline and `AnalysisResult`

The engine operates exclusively on structural chart facts, published upstream stage results attached to AnalysisContext, and Useful God Rules. It does not invent interpretive meaning beyond analytical Useful God evidence.

---

# 4. Out of Scope

The Useful God Engine must not perform any of the following:

| Concern | Owning Stage |
|---------|--------------|
| Day Master strength recomputation or reclassification | Strength Engine |
| Climate, warmth, coldness, dryness, or humidity recomputation | Temperature Engine |
| Pattern / Ge Ju recomputation | Pattern Engine |
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

Any feature that changes the semantic meaning of Useful God classification, or that expands the engine beyond Useful God determination, requires a new major version.

---

# 5. Architecture Position

The Useful God Engine is stage **04** of the Analysis Engine pipeline. It executes only after Strength, Temperature, and Pattern have completed, and only before Ten Gods.

```text
Strength Engine
        │
        ▼
Temperature Engine
        │
        ▼
Pattern Engine
        │
        ▼
Useful God Engine        ← this module (04)
        │
        ▼
Ten Gods Engine
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

- The Useful God Engine never invokes downstream engines.
- The Useful God Engine never bypasses upstream Calendar, Bazi, Strength, Temperature, or Pattern stages.
- Downstream engines may read `UsefulGodResult`; they must not recompute Useful God as a competing source of truth.
- Strength, Temperature, and Pattern evaluation remain outside Useful God scope; Useful God consumes their published results from AnalysisContext only.

---

# 6. Input

## Primary Input

The Useful God Engine accepts one immutable analytical input:

```text
AnalysisContext
```

`AnalysisContext` is assembled by the Analysis Engine orchestrator from upstream products. Published upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
```

The Useful God Engine does not accept raw birth data and does not accept upstream stage results as separate function parameters.

No dedicated input wrapper models shall be introduced.

## Required Upstream Content

The context must provide, at minimum:

| Domain | Required Content |
|--------|------------------|
| Calendar | Season, solar-term positioning, and related temporal metadata needed by Useful God Rules |
| Bazi | Four Pillars, Day Master identity, Day Master element and polarity |
| Structural facts | Hidden stems, Earthly Branch composition, Five Element distribution |
| Relational facts | Production/control relationships as chart facts |
| Strength | `AnalysisContext.strength_result` |
| Temperature | `AnalysisContext.temperature_result` |
| Pattern | `AnalysisContext.pattern_result` |
| Runtime | Rule-database version reference and execution metadata |

## Input Contract Rules

- Input is read-only.
- Missing mandatory chart facts or missing upstream stage results must fail validation before scoring.
- The engine does not reconstruct pillars from calendar data.
- The engine does not recompute Day Master strength.
- The engine does not recompute climate balance.
- The engine does not recompute Pattern.
- The engine does not load Ten Gods, Interpretation, or Report results as inputs.

---

# 7. Output

## Primary Output

The Useful God Engine publishes one immutable result object:

```text
UsefulGodResult
```

`UsefulGodResult` becomes part of `AnalysisResult`.

## Canonical Result Fields

| Field Group | Description |
|-------------|-------------|
| `useful_god` | Determined Yong Shen (Useful God / Dụng Thần) |
| `favorable_gods` | Determined Xi Shen set (Favorable God / Hỷ Thần) |
| `unfavorable_gods` | Determined Ji Shen set (Unfavorable God / Kỵ Thần) |
| `neutral_gods` | Determined Xian Shen set (Neutral God / Nhàn Thần) |
| Candidate rankings | Primary, secondary, and alternative candidate rankings |
| Confidence | Confidence of the matched-rule evaluation |
| Matched rules | Ordered identifiers of applied Useful God Rules |
| Rejected candidates | Candidates considered and rejected during resolution |
| Reasoning | Traceable Useful God rationale derived from matched rules and resolution evidence |
| Diagnostics | Debug and audit diagnostics |
| Metadata | Execution trace and rule-version reference |

## Output Contract Rules

- `UsefulGodResult` is immutable after publication.
- `UsefulGodResult` is the single source of truth for natal Useful God determination inside the Analysis Engine pipeline.
- Downstream stages may project Useful God fields into their own contexts; they must not alter the published `UsefulGodResult`.
- Analytical reasoning is evidence for Useful God determination. It is not an interpretation product and must not be treated as report narrative.

---

# 8. Dependencies

## Upstream Runtime Dependencies

| Dependency | Role |
|------------|------|
| Calendar Engine | Supplies temporal and seasonal facts |
| Bazi Engine | Supplies chart structure and Day Master identity |
| Strength Engine | Publishes `StrengthResult` into `AnalysisContext.strength_result` |
| Temperature Engine | Publishes `TemperatureResult` into `AnalysisContext.temperature_result` |
| Pattern Engine | Publishes `PatternResult` into `AnalysisContext.pattern_result` |
| Analysis Engine orchestrator | Supplies validated `AnalysisContext` and consumes `UsefulGodResult` |

## Knowledge Dependencies

### Useful God Rule Database

| Field | Value |
|-------|-------|
| Status | Planned |
| Dependency Type | Knowledge Module |
| Availability | Future Analysis Knowledge Package |

Description:

The Useful God Engine depends on a dedicated Useful God Rule Database.

The Rule Database is not yet part of the repository.

The engine architecture is intentionally decoupled from the physical storage location of the rule database.

The actual repository path will be defined when the Useful God Knowledge Module is implemented.

Supporting services:

| Dependency | Role |
|------------|------|
| Rule loading / registry services | Read-only access to Useful God rule assets when available |
| Shared rule-contract utilities | Condition evaluation conventions shared across analysis stages |

The engine shall depend only on the abstract Knowledge Module. No hard-coded repository path is part of this contract.

## Explicit Non-Dependencies

The Useful God Engine must not depend on:

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
UsefulGodEngine.evaluate(
    context: AnalysisContext
) -> UsefulGodResult
```

## Public Surface

| Symbol | Stability | Role |
|--------|-----------|------|
| `UsefulGodEngine` | Stable | Primary engine façade |
| `UsefulGodEngine.evaluate` | Stable | Sole public execution method |
| `UsefulGodResult` | Stable | Published output contract |
| `AnalysisContext` | Stable | Shared analytical input contract |
| `AnalysisContext.strength_result` | Stable | Upstream strength evidence accessed through context |
| `AnalysisContext.temperature_result` | Stable | Upstream temperature evidence accessed through context |
| `AnalysisContext.pattern_result` | Stable | Upstream pattern evidence accessed through context |

## Public API Guarantees

- Callers interact only through the public façade.
- No additional public methods are exposed.
- Upstream stage results are never passed as function parameters.
- Internal analyzers, scorers, loaders, and matchers are not part of the public contract.
- V1.0 architectural stability is defined by `evaluate(context) -> UsefulGodResult`.
- Breaking changes to the public surface require a major version increment.

---

# 10. Internal Modules Overview

Internal modules implement a single-responsibility pipeline within the Useful God domain.

| Internal Module | Responsibility |
|-----------------|----------------|
| Context Validator | Validates required `AnalysisContext` fields and upstream stage results before evaluation |
| Useful God Context Adapter | Projects chart facts and upstream evidence into a Useful God matching view |
| Rule Loader | Loads Useful God Rules and configuration in read-only mode |
| Rule Matcher | Evaluates rule conditions against the Useful God context |
| Strength Balance Analyzer | Evaluates strength-balance requirements |
| Climate Balance Analyzer | Evaluates climate-balance requirements |
| Pattern Requirement Analyzer | Evaluates pattern requirements |
| Equilibrium Analyzer | Evaluates five-element equilibrium |
| Relation Analyzer | Evaluates supporting and controlling relationships |
| Adjustment Priority Analyzer | Evaluates adjustment priorities |
| Candidate Generator | Generates Useful God candidates |
| Candidate Evaluator | Evaluates primary, secondary, and alternative candidates |
| Conflict Resolver | Resolves Useful God conflicts |
| Priority Resolver | Resolves candidate priority contests |
| Yong Shen Determiner | Determines Useful God |
| Xi Shen Determiner | Determines Favorable Gods |
| Ji Shen Determiner | Determines Unfavorable Gods |
| Xian Shen Determiner | Determines Neutral Gods |
| Confidence Evaluator | Computes confidence from match quality and completeness |
| Result Builder | Assembles the immutable `UsefulGodResult` |

Internal modules may be refactored freely within V1.x provided the public API and published result contract remain unchanged.

---

# 11. Directory Structure

```text
engines/analysis_engine/04_useful_god_engine/
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
├── engine.py                 # UsefulGodEngine façade
├── models.py                 # UsefulGodResult and related contracts
├── context.py                # Useful God-domain context view
├── loader.py                 # Useful God Rule loading
├── matcher.py                # Condition matching
├── analyzer.py               # Stage orchestration across analyzers
├── priority.py               # Priority and conflict resolution
├── scorer.py                 # Scoring and classification
├── exceptions.py             # Useful God-domain errors
├── utils/
│   └── context_builder.py    # AnalysisContext → Useful God view projection
└── analyzers/
    ├── strength_balance.py
    ├── climate_balance.py
    ├── pattern_requirement.py
    ├── equilibrium.py
    ├── relation.py
    ├── adjustment_priority.py
    ├── candidate_generator.py
    ├── candidate_evaluator.py
    ├── yong_shen.py
    ├── xi_shen.py
    ├── ji_shen.py
    └── xian_shen.py
```

Structural rules:

- All Useful God Engine source for the Analysis Engine pipeline resides under this module path.
- Useful God business knowledge remains in the Useful God Rule Database Knowledge Module; this directory contains execution architecture only.
- The physical storage path of the Rule Database is intentionally undefined until the Useful God Knowledge Module is implemented.
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
Read PatternResult
        │
        ▼
Load Useful God Rules
        │
        ▼
Generate Candidates
        │
        ▼
Evaluate Candidates
        │
        ▼
Resolve Priority
        │
        ▼
Determine Yong Shen
        │
        ▼
Determine Xi Shen
        │
        ▼
Determine Ji Shen
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable UsefulGodResult
        │
        ▼
Publish UsefulGodResult
```

Execution invariants:

- Identical `AnalysisContext` and identical Useful God Rule version must yield identical `UsefulGodResult`.
- Validation failure terminates evaluation before scoring.
- No downstream engine is called during this flow.
- No Strength, Temperature, Pattern, Ten Gods, Interpretation, or Report logic is executed inside this flow.

---

# 13. Design Principles

## Single Responsibility

The module determines natal Useful God balancing elements and nothing else.

## Stage Isolation

Useful God communicates with the rest of the platform only through published contracts: `AnalysisContext` in, `UsefulGodResult` out. Upstream evidence is read from AnalysisContext stage-result fields.

## Determinism

Equal inputs and equal rule versions always produce equal outputs.

## Rule-Driven Knowledge

Business Useful God knowledge lives in the Useful God Rule Database. Engine code executes matching, priority, and scoring mechanics.

## Explainability

Every published Useful God decision must be traceable to matched rules, rejected candidates, and resolution evidence.

## Immutability

Published inputs and outputs are not mutated after creation.

## Fail Fast

Invalid or incomplete upstream context or missing upstream stage results stops evaluation immediately.

## Non-Overlap

Useful God must not absorb Strength, Temperature, or Pattern recomputation, Ten Gods analysis, or Interpretation narrative generation.

## Downstream Neutrality

The engine publishes Useful God facts usable by later stages, without encoding later-stage decisions.

## Extensibility

Useful God categories and analyzers may expand within V1.x without breaking the public API.

## Testability

Each internal analyzer and the scoring stage must be independently verifiable against golden Useful God Rule examples.

---

# 14. Future Extensions

Future major or minor versions may introduce extensions such as:

- Additional Useful God category dimensions expressed as rule packs
- Alternate candidate resolution strategies selectable by configuration
- Rule-version switching without public API breakage
- Regional or school-specific Useful God profiles
- Enhanced explainability payloads for audit and QA tooling
- Performance optimizations in matching and scoring

Extension constraints:

- Extensions must preserve the V1 public API within the 1.x series.
- Extensions must not move Strength, Temperature, Pattern, Ten Gods, or Interpretation responsibilities into this module.
- Any change that alters the meaning of Useful God identity or replaces `UsefulGodResult` as the Useful God source of truth requires a major version.

---

# 15. Version

| Item | Value |
|------|-------|
| Architecture Version | 1.0.0 |
| Status | Frozen Architecture Baseline |
| Compatibility | Analysis Engine V1.x |
| Public API Stability | Guaranteed within V1.x |
| Result Contract | `UsefulGodResult` is authoritative for natal Useful God determination |

This README is the official V1.0 architecture baseline for `engines/analysis_engine/04_useful_god_engine`.

Breaking architectural changes require an explicit major version increment and a replacement architecture baseline.

---

## Architecture Coexistence

This directory is part of the **legacy stage documentation/engine tree**.

Canonical architecture skeleton packages live at the Analysis Engine root (`models/`, `pipeline/`, `analyzers/`, `registry/`, `validation/`, …).

See `engines/analysis_engine/README.md` and `ANALYSIS_ENGINE_AUDIT.md`.
