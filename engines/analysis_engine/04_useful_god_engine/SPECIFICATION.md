# Useful God Engine Specification

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Functional Specification)

---

# 1. Purpose

This document defines the functional specification of the Useful God Engine.

It specifies the expected behavior, inputs, outputs, processing rules, constraints, validation requirements, and acceptance criteria.

This specification serves as the authoritative functional contract between the implementation and the rest of the BTE Platform.

---

# 2. Functional Objective

The Useful God Engine shall determine the natal chart's balancing elements using the official Rule Database and produce a normalized, explainable, deterministic `UsefulGodResult`.

The engine shall determine:

- Yong Shen (Useful God / Dụng Thần)
- Xi Shen (Favorable God / Hỷ Thần)
- Ji Shen (Unfavorable God / Kỵ Thần)
- Xian Shen (Neutral God / Nhàn Thần)

The engine shall not perform interpretation or recommendation.

The engine shall not recompute Strength, Temperature, or Pattern.

---

# 3. Functional Scope

The Useful God Engine shall:

- Evaluate strength balance.
- Evaluate climate balance.
- Evaluate pattern requirements.
- Evaluate five-element equilibrium.
- Evaluate supporting and controlling relationships.
- Evaluate adjustment priorities.
- Generate Useful God candidates.
- Evaluate primary, secondary, and alternative candidates.
- Resolve candidate priority and conflicts.
- Determine Yong Shen, Xi Shen, Ji Shen, and Xian Shen.
- Apply official Useful God Rules.
- Consume published StrengthResult, TemperatureResult, and PatternResult from AnalysisContext.
- Calculate confidence.
- Produce immutable analytical results.

---

# 4. Out of Scope

The engine shall not:

- Recompute Strength
- Recompute Temperature
- Recompute Pattern
- Analyse Ten Gods
- Evaluate ShenSha
- Calculate Luck
- Generate interpretations
- Generate reports
- Render templates
- Modify chart data
- Modify AnalysisContext.strength_result
- Modify AnalysisContext.temperature_result
- Modify AnalysisContext.pattern_result
- Modify rule data

These responsibilities belong to other modules.

---

# 5. Preconditions

Execution requires:

- A valid immutable `AnalysisContext`
- A valid immutable `AnalysisContext.strength_result`
- A valid immutable `AnalysisContext.temperature_result`
- A valid immutable `AnalysisContext.pattern_result`
- Completed Four Pillars calculation
- Hidden Stem calculation completed
- Five Element distribution available
- Completed Strength, Temperature, and Pattern evaluations published into AnalysisContext
- Rule Loader initialized
- Rule Registry available
- Supported Rule Database version

Execution shall not begin if any prerequisite is missing.

---

# 6. Input Specification

## Primary Input

```text
AnalysisContext
```

The context shall contain, at minimum:

- Calendar data
- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Five Elements distribution
- Relationships
- Runtime metadata
- `strength_result` published by the Strength Engine
- `temperature_result` published by the Temperature Engine
- `pattern_result` published by the Pattern Engine

The engine shall not read raw user input.
The engine shall not accept upstream stage results as separate function parameters.
No dedicated input wrapper models shall be introduced.

---

# 7. Output Specification

The engine shall return:

```text
UsefulGodResult
```

The result shall contain at least:

- useful_god
- favorable_gods
- unfavorable_gods
- neutral_gods
- candidate rankings
- confidence
- matched rules
- rejected candidates
- reasoning
- diagnostics
- metadata

The result shall be immutable and published into AnalysisResult.

---

# 8. Functional Requirements

## FR-001

The engine shall validate the input context before processing.

---

## FR-002

The engine shall validate AnalysisContext.strength_result before processing.

---

## FR-003

The engine shall validate AnalysisContext.temperature_result before processing.

---

## FR-004

The engine shall validate AnalysisContext.pattern_result before processing.

---

## FR-005

The engine shall reject invalid contexts or missing upstream stage results.

---

## FR-006

The engine shall load only applicable Useful God Rules from the Useful God Rule Database Knowledge Module.

---

## FR-007

The engine shall evaluate strength balance requirements.

---

## FR-008

The engine shall evaluate climate balance requirements.

---

## FR-009

The engine shall evaluate pattern requirements.

---

## FR-010

The engine shall evaluate five-element equilibrium.

---

## FR-011

The engine shall evaluate supporting and controlling relationships.

---

## FR-012

The engine shall evaluate adjustment priorities.

---

## FR-013

The engine shall generate Useful God candidates.

---

## FR-014

The engine shall evaluate primary, secondary, and alternative candidates.

---

## FR-015

The engine shall resolve candidate priority contests.

---

## FR-016

The engine shall resolve Useful God conflicts.

---

## FR-017

The engine shall determine Yong Shen.

---

## FR-018

The engine shall determine Xi Shen.

---

## FR-019

The engine shall determine Ji Shen.

---

## FR-020

The engine shall determine Xian Shen.

---

## FR-021

The engine shall compute a confidence level.

---

## FR-022

The engine shall record every matched rule.

---

## FR-023

The engine shall record rejected candidates.

---

## FR-024

The engine shall produce traceable reasoning and diagnostics.

---

## FR-025

The engine shall return an immutable UsefulGodResult.

---

## FR-026

The engine shall never recompute Strength, Temperature, or Pattern.

---

# 9. Non-Functional Requirements

## Deterministic

Identical inputs shall always produce identical outputs.

---

## Stateless

The engine shall maintain no execution state.

---

## Explainable

Every analytical decision shall be traceable.

---

## Extensible

New rules and Useful God categories shall not require public API modification within Version 1.x.

---

## Testable

Every analytical component shall be independently testable.

---

## Thread Safe

Concurrent execution shall be supported.

---

## Versioned

Public contracts and scoring behavior shall be versioned.

---

# 10. Processing Sequence

The engine shall execute the following sequence:

1. Receive AnalysisContext
2. Validate Context
3. Read StrengthResult
4. Read TemperatureResult
5. Read PatternResult
6. Load Useful God Rules
7. Generate Candidates
8. Evaluate Candidates
9. Resolve Priority
10. Determine Yong Shen
11. Determine Xi Shen
12. Determine Ji Shen
13. Calculate Confidence
14. Build Immutable UsefulGodResult
15. Publish UsefulGodResult

No processing stage may be skipped.

---

# 11. Validation Rules

The engine shall verify:

- Required context fields exist.
- AnalysisContext.strength_result is present and valid.
- AnalysisContext.temperature_result is present and valid.
- AnalysisContext.pattern_result is present and valid.
- Pillars are complete.
- Hidden Stems are available.
- Rule version is supported.
- Metadata is valid.
- Required analyzers are available.

Execution shall terminate on validation failure.

---

# 12. Error Conditions

The engine shall detect and report:

- Invalid context
- Invalid or missing AnalysisContext.strength_result
- Invalid or missing AnalysisContext.temperature_result
- Invalid or missing AnalysisContext.pattern_result
- Missing rules
- Unsupported rule version
- Invalid calculation state
- Missing analytical data
- Unresolvable candidate conflicts
- Internal evaluation failure

Errors shall be propagated without modifying input data.

---

# 13. Edge Cases

The implementation shall correctly handle:

- Single clear Useful God match
- Multiple competing primary candidates
- Competing secondary and alternative candidates
- Conflicting favorable and unfavorable assignments
- Borderline candidate scores
- Empty rejected-candidate list when only one candidate exists
- Missing optional metadata
- Empty matched rule list
- Conflicting rule matches
- Multiple equal-weight rule outcomes
- Upstream results present with minimal optional diagnostics

Behavior shall remain deterministic.

---

# 14. Rule Usage

The engine shall consume only official Useful God Rules from the Useful God Rule Database Knowledge Module.

### Knowledge Dependency

| Field | Value |
|-------|-------|
| Status | Planned |
| Dependency Type | Knowledge Module |
| Availability | Future Analysis Knowledge Package |

The Rule Database is not yet part of the repository.

The engine architecture is intentionally decoupled from the physical storage location of the rule database.

The actual repository path will be defined when the Useful God Knowledge Module is implemented.

Rules shall never be embedded within source code.

Rule selection shall be based on the Rule Registry.

---

# 15. Dependency Specification

The engine depends on:

- Calendar Engine
- Bazi Engine
- Strength Engine (via AnalysisContext.strength_result only)
- Temperature Engine (via AnalysisContext.temperature_result only)
- Pattern Engine (via AnalysisContext.pattern_result only)
- Rule Loader
- Rule Registry
- Shared Analysis Models

The engine shall not depend on downstream analytical modules.

---

# 16. Acceptance Criteria

The implementation shall be accepted only if:

- All functional requirements are satisfied.
- Validation rules are enforced.
- Output is deterministic.
- Rule matching is reproducible.
- Confidence calculation is available.
- Rejected candidates are recorded.
- UsefulGodResult is immutable.
- Strength, Temperature, and Pattern are never recomputed.
- Unit tests pass.
- Integration tests pass.
- Golden dataset validation passes.

---

# 17. Assumptions

The specification assumes:

- Calendar Engine has completed all calendar calculations.
- Bazi Engine has produced a valid AnalysisContext.
- Strength Engine has published a valid StrengthResult into AnalysisContext.
- Temperature Engine has published a valid TemperatureResult into AnalysisContext.
- Pattern Engine has published a valid PatternResult into AnalysisContext.
- Rule Database has been validated.
- Runtime configuration is available.

---

# 18. Constraints

The implementation shall not:

- Modify AnalysisContext
- Modify AnalysisContext.strength_result
- Modify AnalysisContext.temperature_result
- Modify AnalysisContext.pattern_result
- Modify Rule Database
- Recompute Strength, Temperature, or Pattern
- Perform interpretation
- Generate reports
- Call downstream engines
- Access persistence directly
- Expose additional public methods beyond evaluate

---

# 19. Version Compatibility

Compatible with:

- Analysis Engine V1.x
- Strength Engine V1.x
- Temperature Engine V1.x
- Pattern Engine V1.x
- Useful God Rule Database Knowledge Module (Planned)
- Interpretation Engine V1.x

Breaking functional changes require a new major version.

---

# 20. Definition of Done

The Useful God Engine functional specification is considered complete when:

- Functional scope is frozen.
- Input and output contracts are frozen.
- Functional requirements are frozen.
- Validation rules are frozen.
- Error conditions are documented.
- Edge cases are documented.
- Acceptance criteria are approved.

Implementation may begin only after this specification is approved.
