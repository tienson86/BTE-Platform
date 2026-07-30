# Strength Engine Architecture

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Strength Engine.

It establishes the architectural principles, component boundaries, dependency rules, execution lifecycle, and extension mechanisms for the module.

This document serves as the architecture baseline for all future implementation and maintenance activities.

---

# 2. Architectural Goals

The Strength Engine is designed to achieve the following goals:

- Provide deterministic Day Master strength evaluation.
- Isolate strength analysis from all other analytical concerns.
- Maintain strict separation between business knowledge and implementation logic.
- Produce reusable outputs for downstream engines.
- Support future rule expansion without architectural changes.
- Enable independent testing of each analytical component.
- Guarantee reproducible analytical results.

---

# 3. Position in the BTE Platform

The Strength Engine is the first analytical module within the Analysis Engine.

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

The Strength Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module evaluates only the strength of the Day Master.

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

Every score must be traceable back to:

- Applied rule
- Analytical component
- Supporting evidence
- Calculation path

---

## 4.6 Extensibility

New rules and analyzers may be introduced without changing the public API.

---

# 5. Layered Architecture

The Strength Engine follows a layered architecture.

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
Calculator Layer
      │
      ▼
Result Builder
      │
      ▼
StrengthResult
```

Each layer has a single responsibility and communicates only with adjacent layers.

---

# 6. Component Architecture

The internal components are organized as follows:

- Engine Orchestrator
- Context Validator
- Rule Adapter
- Season Analyzer
- Root Analyzer
- Heavenly Stem Analyzer
- Earthly Branch Analyzer
- Support Analyzer
- Control Analyzer
- Score Calculator
- Confidence Evaluator
- Result Builder

Each component is independently testable.

---

# 7. Dependency Rules

Allowed dependencies:

- Calendar Engine
- Bazi Engine
- Rule Loader
- Rule Registry
- Shared Analysis Models

Forbidden dependencies:

- Temperature Engine
- Pattern Engine
- Useful God Engine
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
Rule Loading
      │
      ▼
Season Analysis
      │
      ▼
Root Analysis
      │
      ▼
Stem Analysis
      │
      ▼
Support Analysis
      │
      ▼
Control Analysis
      │
      ▼
Score Calculation
      │
      ▼
Confidence Evaluation
      │
      ▼
StrengthResult
```

No stage may mutate results produced by previous stages.

---

# 9. Component Responsibilities

## Engine Orchestrator

Coordinates the complete execution lifecycle.

---

## Validator

Validates the AnalysisContext before analysis begins.

---

## Rule Adapter

Retrieves normalized rule definitions from the Rule Database.

---

## Analyzer Layer

Evaluates individual analytical dimensions.

Examples include:

- Seasonal influence
- Root strength
- Heavenly Stem contribution
- Earthly Branch contribution
- Supporting elements
- Controlling elements

---

## Calculator

Combines analytical outputs into normalized scores.

---

## Confidence Evaluator

Determines confidence based on analytical completeness and rule coverage.

---

## Result Builder

Constructs the immutable StrengthResult object.

---

# 10. Interface Contracts

The module exposes a single public interface.

```text
StrengthEngine.evaluate(context)
```

Input:

- AnalysisContext

Output:

- StrengthResult

No internal component is considered part of the public contract.

---

# 11. Lifecycle

Execution proceeds through the following phases:

1. Receive AnalysisContext.
2. Validate input.
3. Load applicable rules.
4. Execute analyzers.
5. Aggregate scores.
6. Evaluate confidence.
7. Build immutable result.
8. Return StrengthResult.

Execution terminates immediately if validation fails.

---

# 12. Error Boundaries

The Strength Engine is responsible only for errors occurring within its own execution boundary.

Typical categories include:

- Invalid analysis context
- Missing rule definitions
- Unsupported rule versions
- Internal calculation failures
- Invalid analytical state

External failures are propagated to the caller.

---

# 13. Extension Points

Future extensions may include:

- Alternative scoring algorithms
- Regional evaluation profiles
- Experimental analyzers
- Parallel execution strategies
- Rule version selection
- Performance optimizations

Extensions must preserve the public API.

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

StrengthResult is immutable.

---

## ADR-004

Only one public API is exposed.

---

## ADR-005

The engine never performs interpretation.

---

## ADR-006

Evaluation follows a one-way pipeline.

---

## ADR-007

Dependencies flow only toward upstream modules or shared infrastructure.

---

## ADR-008

All analytical decisions must be explainable through matched rules.

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

---

# 18. Version Compatibility

This architecture is compatible with:

- Analysis Engine V1.x
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