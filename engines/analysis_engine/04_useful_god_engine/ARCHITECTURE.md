# Useful God Engine Architecture

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Useful God Engine.

It establishes the architectural principles, component boundaries, dependency rules, execution lifecycle, and extension mechanisms for the module.

This document serves as the architecture baseline for all future implementation and maintenance activities.

---

# 2. Architectural Goals

The Useful God Engine is designed to achieve the following goals:

- Provide deterministic natal Useful God determination.
- Isolate Useful God analysis from all other analytical concerns.
- Maintain strict separation between business knowledge and implementation logic.
- Consume published StrengthResult, TemperatureResult, and PatternResult from AnalysisContext without recomputation.
- Support Yong Shen, Xi Shen, Ji Shen, and Xian Shen determination.
- Produce reusable outputs for downstream engines.
- Support future rule expansion without architectural changes.
- Enable independent testing of each analytical component.
- Guarantee reproducible analytical results.

---

# 3. Position in the BTE Platform

The Useful God Engine is the fourth analytical module within the Analysis Engine.

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
Useful God Engine
        │
        ▼
Ten Gods Engine
```

Full orchestration context:

```text
Calendar Engine
        │
        ▼
Bazi Engine
        │
        ▼
AnalysisContext
        │
        ▼
Strength Engine
        │
        ▼
AnalysisContext.strength_result
        │
        ▼
Temperature Engine
        │
        ▼
AnalysisContext.temperature_result
        │
        ▼
Pattern Engine
        │
        ▼
AnalysisContext.pattern_result
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

The Useful God Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module determines only the natal chart's balancing elements.

No interpretation or recommendation logic is permitted.

---

## 4.2 Rule-Driven Design

All business knowledge resides in the Rule Database.

The engine implements evaluation logic only.

Business rules must never be hardcoded into analytical components.

---

## 4.3 Deterministic Execution

Identical inputs, rule versions, and configurations must always produce identical outputs.

Randomized behavior is prohibited.

---

## 4.4 Immutable Data Flow

Input objects are immutable.

Output objects are immutable.

Intermediate analytical results are immutable once finalized.

---

## 4.5 Explainability

Every Useful God decision must be traceable back to:

- Applied rule
- Analytical component
- Supporting evidence
- Rejected candidates
- Conflict and priority resolution path

---

## 4.6 Extensibility

New rules, Useful God categories, and analyzers may be introduced without changing the public API within Version 1.x.

---

# 5. Layered Architecture

The Useful God Engine follows a layered architecture.

```text
Public API
      │
      ▼
Engine Orchestrator
      │
      ▼
Validator
      │
      ▼
Rule Adapter
      │
      ▼
Analyzer Layer
      │
      ▼
Candidate Layer
      │
      ▼
Determination Layer
      │
      ▼
Calculator Layer
      │
      ▼
Result Builder
      │
      ▼
UsefulGodResult
```

Each layer has a single responsibility and communicates only with adjacent layers.

---

# 6. Component Architecture

The internal components are organized as follows:

- Engine Orchestrator
- Context Validator
- Rule Adapter
- Strength Balance Analyzer
- Climate Balance Analyzer
- Pattern Requirement Analyzer
- Equilibrium Analyzer
- Relation Analyzer
- Adjustment Priority Analyzer
- Candidate Generator
- Candidate Evaluator
- Conflict Resolver
- Priority Resolver
- Yong Shen Determiner
- Xi Shen Determiner
- Ji Shen Determiner
- Xian Shen Determiner
- Score Calculator
- Confidence Evaluator
- Result Builder

Each component is independently testable.

---

# 7. Dependency Rules

Allowed dependencies:

- Calendar Engine
- Bazi Engine
- Strength Engine (via AnalysisContext.strength_result only)
- Temperature Engine (via AnalysisContext.temperature_result only)
- Pattern Engine (via AnalysisContext.pattern_result only)
- Useful God Rule Database Knowledge Module (abstract)
- Rule Loader
- Rule Registry
- Shared Analysis Models

Forbidden dependencies:

- Ten Gods Engine
- ShenSha Engine
- Luck Engine
- Interpretation Engine
- Report Engine
- User Interface
- Persistence Layer
- Hard-coded physical paths to rule storage

Dependencies must always point upstream or toward shared infrastructure.

---

# 7.1 Knowledge Dependency

## Useful God Rule Database

| Field | Value |
|-------|-------|
| Status | Planned |
| Dependency Type | Knowledge Module |
| Availability | Future Analysis Knowledge Package |

The Useful God Engine depends on a dedicated Useful God Rule Database.

The Rule Database is not yet part of the repository.

The engine architecture is intentionally decoupled from the physical storage location of the rule database.

The actual repository path will be defined when the Useful God Knowledge Module is implemented.

The engine shall depend only on the abstract Knowledge Module.

---

# 8. Data Flow

The engine follows a one-way processing pipeline.

```text
AnalysisContext
      │
      ▼
Validation
      │
      ▼
Read StrengthResult from AnalysisContext
      │
      ▼
Read TemperatureResult from AnalysisContext
      │
      ▼
Read PatternResult from AnalysisContext
      │
      ▼
Rule Loading
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
Determine Xian Shen
      │
      ▼
Confidence Evaluation
      │
      ▼
UsefulGodResult
```

No stage may mutate results produced by previous stages.

---

# 9. Component Responsibilities

## Engine Orchestrator

Coordinates the complete execution lifecycle.

---

## Validator

Validates the AnalysisContext, including upstream stage results, before analysis begins.

---

## Rule Adapter

Retrieves normalized rule definitions from the Rule Database.

---

## Analyzer Layer

Evaluates individual analytical dimensions.

Examples include:

- Strength balance
- Climate balance
- Pattern requirements
- Five-element equilibrium
- Supporting and controlling relationships
- Adjustment priorities

---

## Candidate Layer

Generates, evaluates, and resolves competing Useful God candidates.

---

## Determination Layer

Determines Yong Shen, Xi Shen, Ji Shen, and Xian Shen.

---

## Calculator

Combines analytical outputs into normalized scores and classifications.

---

## Confidence Evaluator

Determines confidence based on analytical completeness and rule coverage.

---

## Result Builder

Constructs the immutable UsefulGodResult object.

---

# 10. Interface Contracts

The module exposes a single public interface.

```text
UsefulGodEngine.evaluate(
    context: AnalysisContext
) -> UsefulGodResult
```

Input:

- AnalysisContext

Output:

- UsefulGodResult

No internal component is considered part of the public contract.

No additional public methods are exposed.

---

# 11. Lifecycle

Execution proceeds through the following phases:

1. Receive AnalysisContext.
2. Validate context.
3. Read StrengthResult from AnalysisContext.
4. Read TemperatureResult from AnalysisContext.
5. Read PatternResult from AnalysisContext.
6. Load Useful God Rules.
7. Generate candidates.
8. Evaluate candidates.
9. Resolve priority and conflicts.
10. Determine Yong Shen.
11. Determine Xi Shen.
12. Determine Ji Shen.
13. Determine Xian Shen.
14. Calculate confidence.
15. Build immutable UsefulGodResult.
16. Publish UsefulGodResult.

Execution terminates immediately if validation fails.

---

# 12. Error Boundaries

The Useful God Engine is responsible only for errors occurring within its own execution boundary.

Typical categories include:

- Invalid analysis context
- Missing or invalid AnalysisContext.strength_result
- Missing or invalid AnalysisContext.temperature_result
- Missing or invalid AnalysisContext.pattern_result
- Missing rule definitions
- Unsupported rule versions
- Internal calculation failures
- Invalid analytical state
- Unresolvable Useful God candidate conflicts

External failures are propagated to the caller.

---

# 13. Extension Points

Future extensions may include:

- Additional Useful God category dimensions
- Alternative scoring algorithms
- Regional evaluation profiles
- Experimental analyzers
- Parallel execution strategies
- Rule version selection
- Performance optimizations

Extensions must preserve the public API within Version 1.x.

---

# 14. Performance Considerations

The architecture is designed to support:

- Rule caching
- Immutable object reuse
- Stateless execution
- Parallel analyzer execution where dependencies permit
- Minimal object mutation

Performance optimizations must not alter analytical correctness.

---

# 15. Thread Safety

The engine should be stateless.

No shared mutable state is permitted.

Execution must be safe for concurrent requests.

---

# 16. Architecture Decision Records (ADR)

## ADR-001

Business knowledge resides exclusively in the Rule Database.

---

## ADR-002

AnalysisContext is immutable.

---

## ADR-003

StrengthResult, TemperatureResult, and PatternResult are consumed as immutable upstream contracts through AnalysisContext.

---

## ADR-004

UsefulGodResult is immutable.

---

## ADR-005

Only one public API is exposed.

---

## ADR-006

The engine never performs interpretation.

---

## ADR-007

The engine never recomputes Strength, Temperature, or Pattern.

---

## ADR-008

Evaluation follows a one-way pipeline.

---

## ADR-009

Dependencies flow only toward upstream modules or shared infrastructure.

---

## ADR-010

All analytical decisions must be explainable through matched rules and rejected candidates.

---

## ADR-011

Useful God categories are extensible within Version 1.x without public API breakage.

---

# 17. Constraints

The architecture imposes the following constraints:

- No circular dependencies.
- No direct access to persistence.
- No direct modification of rule definitions.
- No coupling to downstream engines.
- No presentation logic.
- No localization logic.
- No report rendering.
- No Strength, Temperature, or Pattern recomputation.
- No additional public methods beyond evaluate.

---

# 18. Version Compatibility

This architecture is compatible with:

- Analysis Engine V1.x
- Strength Engine V1.x
- Temperature Engine V1.x
- Pattern Engine V1.x
- Useful God Rule Database Knowledge Module (Planned)
- Interpretation Engine V1.x

Breaking architectural changes require a new major version.

---

# 19. Definition of Architectural Completion

The architecture is considered complete when:

- Component boundaries are frozen.
- Public API is frozen.
- Dependency rules are frozen.
- Lifecycle is frozen.
- Extension strategy is documented.
- ADR records are finalized.

Implementation may begin only after this document is approved.
