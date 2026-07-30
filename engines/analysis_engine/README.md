# 01 Strength Engine

**Version:** V1.0.0 (Architecture Baseline)  
**Status:** Active (Frozen)  
**Module Type:** Analysis Engine  
**Owner:** BTE Platform

---

# 1. Overview

The **Strength Engine** is the first analytical module within the BTE Analysis Engine pipeline.

Its sole responsibility is to evaluate the overall strength of the **Day Master (Nhật Chủ)** based on the natal chart and the official Strength Rule Database.

The evaluation result becomes a foundational input for all subsequent analytical engines, including Temperature, Pattern, Useful God, Ten Gods, Combination, ShenSha, Luck, and Summary.

The Strength Engine is a **pure analytical component**. It performs no interpretation, recommendation, or report generation.

---

# 2. Purpose

The purpose of this module is to produce a standardized, reproducible, and explainable evaluation of Day Master strength.

The engine must provide a single source of truth regarding:

- Overall Day Master strength
- Individual contributing factors
- Rule matching results
- Confidence level
- Supporting evidence
- Intermediate analytical data required by downstream modules

Every execution using identical inputs and rule versions must produce identical outputs.

---

# 3. Responsibilities

The Strength Engine is responsible for:

- Evaluating seasonal influence.
- Evaluating hidden stem rooting.
- Evaluating Heavenly Stem support.
- Evaluating Earthly Branch support.
- Evaluating production, control, and draining effects.
- Applying official Strength Rules.
- Calculating normalized strength scores.
- Calculating confidence levels.
- Producing a complete `StrengthResult`.
- Providing traceable reasoning for every score.

---

# 4. Out of Scope

The Strength Engine must **NOT** perform any of the following:

- Determine Pattern (Cách Cục)
- Select Useful God (Dụng Thần)
- Evaluate Ten Gods quality
- Analyze combinations or clashes
- Analyze ShenSha
- Analyze Luck Pillars
- Generate interpretations
- Generate reports
- Render templates
- Rewrite natural language
- Modify chart data
- Modify rule data

These responsibilities belong to dedicated downstream engines.

---

# 5. Architecture Position

The Strength Engine is the first analytical stage after chart construction.

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

The Strength Engine never bypasses this pipeline and never invokes downstream engines.

---

# 6. Input

The module accepts a single immutable input object.

```
AnalysisContext
```

The context is expected to contain:

- Calendar information
- Four Pillars
- Hidden Stems
- Five Elements distribution
- Ten Gods mapping
- Relationships
- Metadata
- Runtime configuration

The Strength Engine never reads raw user input directly.

---

# 7. Output

The module returns one standardized object.

```
StrengthResult
```

The result includes:

- Overall strength score
- Strength level
- Seasonal contribution
- Root contribution
- Stem contribution
- Support contribution
- Control contribution
- Drain contribution
- Weight breakdown
- Matched rules
- Confidence level
- Analytical reasoning
- Execution metadata

The output is immutable after creation.

---

# 8. Dependencies

The Strength Engine depends on:

## Upstream

- Calendar Engine
- Bazi Engine
- Rule Database
- Rule Loader
- Rule Registry

## Internal

- Validator
- Analyzer Pipeline
- Score Calculator
- Result Builder

The engine does not depend on Interpretation Engine or Report Engine.

---

# 9. Public API

The module exposes a single public entry point.

```
StrengthEngine.evaluate(context)
```

Input:

- AnalysisContext

Output:

- StrengthResult

No other public execution interface is guaranteed to remain stable.

---

# 10. Internal Components

The implementation is internally divided into specialized components.

- Context Validator
- Rule Adapter
- Season Analyzer
- Root Analyzer
- Stem Analyzer
- Support Analyzer
- Control Analyzer
- Score Calculator
- Confidence Evaluator
- Result Builder

Each component has a single responsibility.

---

# 11. Directory Structure

```
01_strength_engine/

README.md
ARCHITECTURE.md
SPECIFICATION.md
FLOW.md
MODELS.md
PUBLIC_API.md
RULE_MAPPING.md
ALGORITHM.md
VALIDATION.md
ERROR_HANDLING.md
CACHE.md
CHANGELOG.md

engine.py
service.py
validator.py
loader.py
registry.py
models.py
interfaces.py
exceptions.py
cache.py

analyzers/
calculator/
tests/
```

The documentation defines the architecture. The implementation must conform to these specifications.

---

# 12. Execution Flow

The Strength Engine follows a deterministic processing pipeline.

```
Validate Context
        │
        ▼
Load Rules
        │
        ▼
Analyze Season
        │
        ▼
Analyze Roots
        │
        ▼
Analyze Heavenly Stems
        │
        ▼
Analyze Support & Control
        │
        ▼
Calculate Score
        │
        ▼
Evaluate Confidence
        │
        ▼
Build StrengthResult
```

Every stage produces deterministic intermediate results.

---

# 13. Design Principles

The Strength Engine follows the following architectural principles.

## Single Responsibility

Only evaluates Day Master strength.

## Deterministic

Same input always produces the same output.

## Explainable

Every score must be traceable to rules.

## Immutable

Inputs and outputs remain unchanged after creation.

## Extensible

New rules can be added without changing engine behavior.

## Rule-Driven

Business knowledge resides in the Rule Database.

## Testable

Every analyzer can be tested independently.

---

# 14. Future Extensions

Future versions may introduce:

- Alternative strength algorithms
- Regional calculation variants
- Multiple scoring strategies
- Rule version switching
- Parallel evaluation
- Performance optimizations
- Explainability enhancements
- Statistical calibration
- Plugin-based analyzers

All future extensions must preserve the public API unless a major version is released.

---

# 15. Versioning Policy

This document defines the official architecture baseline of the Strength Engine.

- Current Version: **V1.0.0**
- Status: **Frozen**
- Compatibility: Analysis Engine V1.x
- Public API Stability: Guaranteed within V1.x

Breaking architectural changes require a major version increment.

---

# 16. Definition of Done

The Strength Engine V1.0 is considered complete only when:

- Architecture documentation is finalized.
- Domain models are frozen.
- Public API is frozen.
- Rule mappings are documented.
- Algorithms are specified.
- Validation rules are documented.
- Error handling is documented.
- Test strategy is documented.
- All downstream engines can consume `StrengthResult` without requiring architectural changes.

Only after these conditions are satisfied may implementation begin.