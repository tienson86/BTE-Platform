# Pattern Engine Architecture

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Pattern Engine.

It establishes the architectural principles, component boundaries, dependency rules, execution lifecycle, and extension mechanisms for the module.

This document serves as the architecture baseline for all future implementation and maintenance activities.

---

# 2. Architectural Goals

The Pattern Engine is designed to achieve the following goals:

- Provide deterministic natal Pattern (Ge Ju / 格局) determination.
- Isolate pattern analysis from all other analytical concerns.
- Maintain strict separation between business knowledge and implementation logic.
- Consume published StrengthResult and TemperatureResult from AnalysisContext without recomputation.
- Support standard, special, follow, transformation, mixed, and exceptional pattern categories.
- Produce reusable outputs for downstream engines.
- Support future rule expansion without architectural changes.
- Enable independent testing of each analytical component.
- Guarantee reproducible analytical results.

---

# 3. Position in the BTE Platform

The Pattern Engine is the third analytical module within the Analysis Engine.

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

The Pattern Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module determines only the Pattern (Ge Ju / 格局) of the natal chart.

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

Every pattern decision must be traceable back to:

- Applied rule
- Analytical component
- Supporting evidence
- Rejected candidates
- Conflict and priority resolution path

---

## 4.6 Extensibility

New rules, pattern categories, and analyzers may be introduced without changing the public API within Version 1.x.

---

# 5. Layered Architecture

The Pattern Engine follows a layered architecture.

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
Calculator Layer
      │
      ▼
Result Builder
      │
      ▼
PatternResult
```

Each layer has a single responsibility and communicates only with adjacent layers.

---

# 6. Component Architecture

The internal components are organized as follows:

- Engine Orchestrator
- Context Validator
- Rule Adapter
- Structure Analyzer
- Day Master Relation Analyzer
- Standard Pattern Analyzer
- Transformation Pattern Analyzer
- Special Pattern Analyzer
- Follow Pattern Analyzer
- Mixed / Exceptional Analyzer
- Candidate Generator
- Candidate Evaluator
- Conflict Resolver
- Priority Resolver
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
- Rule Loader
- Rule Registry
- Shared Analysis Models

Forbidden dependencies:

- Useful God Engine
- Ten Gods Engine
- Interpretation Engine
- Report Engine
- User Interface
- Persistence Layer

Dependencies must always point upstream or toward shared infrastructure.

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
Rule Loading
      │
      ▼
Structure Analysis
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
Score Calculation
      │
      ▼
Confidence Evaluation
      │
      ▼
PatternResult
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

- Chart structure eligibility
- Day Master relationship with chart composition
- Standard patterns
- Transformation patterns
- Special patterns
- Follow patterns
- Mixed and exceptional patterns

---

## Candidate Layer

Generates, evaluates, and resolves competing pattern candidates.

---

## Calculator

Combines analytical outputs into normalized scores and pattern classification.

---

## Confidence Evaluator

Determines confidence based on analytical completeness and rule coverage.

---

## Result Builder

Constructs the immutable PatternResult object.

---

# 10. Interface Contracts

The module exposes a single public interface.

```text
PatternEngine.evaluate(
    context: AnalysisContext
) -> PatternResult
```

Input:

- AnalysisContext

Output:

- PatternResult

No internal component is considered part of the public contract.

No additional public methods are exposed.

---

# 11. Lifecycle

Execution proceeds through the following phases:

1. Receive AnalysisContext.
2. Validate context.
3. Read StrengthResult from AnalysisContext.
4. Read TemperatureResult from AnalysisContext.
5. Load Pattern Rules.
6. Analyse structure.
7. Generate pattern candidates.
8. Evaluate candidates.
9. Resolve priority and conflicts.
10. Calculate confidence.
11. Build immutable PatternResult.
12. Publish PatternResult.

Execution terminates immediately if validation fails.

---

# 12. Error Boundaries

The Pattern Engine is responsible only for errors occurring within its own execution boundary.

Typical categories include:

- Invalid analysis context
- Missing or invalid AnalysisContext.strength_result
- Missing or invalid AnalysisContext.temperature_result
- Missing rule definitions
- Unsupported rule versions
- Internal calculation failures
- Invalid analytical state
- Unresolvable pattern candidate conflicts

External failures are propagated to the caller.

---

# 13. Extension Points

Future extensions may include:

- Additional pattern categories
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

StrengthResult and TemperatureResult are consumed as immutable upstream contracts through AnalysisContext.

---

## ADR-004

PatternResult is immutable.

---

## ADR-005

Only one public API is exposed.

---

## ADR-006

The engine never performs interpretation.

---

## ADR-007

The engine never recomputes Day Master strength or climate balance.

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

Pattern categories are extensible within Version 1.x without public API breakage.

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
- No Day Master strength recomputation.
- No climate recomputation.
- No additional public methods beyond evaluate.

---

# 18. Version Compatibility

This architecture is compatible with:

- Analysis Engine V1.x
- Strength Engine V1.x
- Temperature Engine V1.x
- Rule Database V1.x
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
