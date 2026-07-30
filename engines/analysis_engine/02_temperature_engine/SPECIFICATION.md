# Temperature Engine Specification

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Functional Specification)

---

# 1. Purpose

This document defines the functional specification of the Temperature Engine.

It specifies the expected behavior, inputs, outputs, processing rules, constraints, validation requirements, and acceptance criteria.

This specification serves as the authoritative functional contract between the implementation and the rest of the BTE Platform.

---

# 2. Functional Objective

The Temperature Engine shall evaluate the climatic balance of the natal chart using the official Rule Database and produce a normalized, explainable, deterministic `TemperatureResult`.

The engine shall not perform interpretation or recommendation.

The engine shall not recompute Day Master strength.

---

# 3. Functional Scope

The Temperature Engine shall:

- Evaluate seasonal temperature.
- Evaluate warm / cold balance.
- Evaluate dryness.
- Evaluate humidity.
- Evaluate climate equilibrium.
- Evaluate environmental support.
- Evaluate climate adjustment requirements.
- Apply official Temperature Rules.
- Consume published StrengthResult as upstream evidence.
- Calculate normalized scores.
- Calculate confidence.
- Produce immutable analytical results.

---

# 4. Out of Scope

The engine shall not:

- Recompute Day Master strength
- Determine Pattern (Cách Cục)
- Determine Useful God (Dụng Thần)
- Evaluate Ten Gods quality
- Evaluate ShenSha
- Evaluate Luck Pillars
- Generate interpretations
- Generate reports
- Render templates
- Modify chart data
- Modify StrengthResult
- Modify rule data

These responsibilities belong to other modules.

---

# 5. Preconditions

Execution requires:

- A valid immutable `AnalysisContext`
- A valid immutable `StrengthResult`
- Completed Four Pillars calculation
- Hidden Stem calculation completed
- Five Element distribution available
- Completed Strength Engine evaluation
- Rule Loader initialized
- Rule Registry available
- Supported Rule Database version

Execution shall not begin if any prerequisite is missing.

---

# 6. Input Specification

## Primary Inputs

```text
AnalysisContext
StrengthResult
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

The StrengthResult shall contain, at minimum:

- Strength level
- Strength score
- Component score evidence required by Temperature Rules
- Execution metadata

The engine shall not read raw user input.

---

# 7. Output Specification

The engine shall return:

```text
TemperatureResult
```

The result shall contain:

- Overall climate score
- Temperature level
- Seasonal temperature score
- Warm / cold score
- Dryness score
- Humidity score
- Equilibrium score
- Environmental support score
- Adjustment requirement indicators
- Weight breakdown
- Matched rules
- Confidence
- Reasoning
- Execution metadata

The result shall be immutable.

---

# 8. Functional Requirements

## FR-001

The engine shall validate the input context before processing.

---

## FR-002

The engine shall validate the published StrengthResult before processing.

---

## FR-003

The engine shall reject invalid contexts or invalid StrengthResult inputs.

---

## FR-004

The engine shall load only applicable Temperature Rules.

---

## FR-005

The engine shall evaluate seasonal temperature.

---

## FR-006

The engine shall evaluate warm / cold balance.

---

## FR-007

The engine shall evaluate dryness.

---

## FR-008

The engine shall evaluate humidity.

---

## FR-009

The engine shall evaluate climate equilibrium.

---

## FR-010

The engine shall evaluate environmental support.

---

## FR-011

The engine shall evaluate climate adjustment requirements.

---

## FR-012

The engine shall aggregate all analytical dimensions into a normalized climate score.

---

## FR-013

The engine shall determine a normalized temperature level.

---

## FR-014

The engine shall compute a confidence level.

---

## FR-015

The engine shall record every matched rule.

---

## FR-016

The engine shall produce traceable reasoning.

---

## FR-017

The engine shall return an immutable TemperatureResult.

---

## FR-018

The engine shall never recompute Day Master strength.

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

New rules shall not require architectural modification.

---

## Testable

Every analytical component shall be independently testable.

---

## Thread Safe

Concurrent execution shall be supported.

---

# 10. Processing Sequence

The engine shall execute the following sequence:

1. Validate AnalysisContext
2. Validate StrengthResult
3. Load applicable rules
4. Analyze seasonal temperature
5. Analyze warm / cold balance
6. Analyze dryness
7. Analyze humidity
8. Analyze climate equilibrium
9. Analyze environmental support
10. Analyze climate adjustment requirements
11. Aggregate scores
12. Evaluate confidence
13. Build TemperatureResult

No processing stage may be skipped.

---

# 11. Validation Rules

The engine shall verify:

- Required context fields exist.
- StrengthResult is present and valid.
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
- Invalid or missing StrengthResult
- Missing rules
- Unsupported rule version
- Invalid calculation state
- Missing analytical data
- Internal evaluation failure

Errors shall be propagated without modifying input data.

---

# 13. Edge Cases

The implementation shall correctly handle:

- Extremely warm climate profile
- Extremely cold climate profile
- Extreme dryness
- Extreme humidity
- Borderline climate values
- Climate already in equilibrium
- Missing optional metadata
- Empty matched rule list
- Conflicting rule matches
- Multiple equal-weight rule outcomes
- StrengthResult present but with minimal optional diagnostics

Behavior shall remain deterministic.

---

# 14. Rule Usage

The engine shall consume only official Temperature Rules.

Rules shall never be embedded within source code.

Rule selection shall be based on the Rule Registry.

---

# 15. Dependency Specification

The engine depends on:

- Calendar Engine
- Bazi Engine
- Strength Engine (published StrengthResult only)
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
- TemperatureResult is immutable.
- Day Master strength is never recomputed.
- Unit tests pass.
- Integration tests pass.
- Golden dataset validation passes.

---

# 17. Assumptions

The specification assumes:

- Calendar Engine has completed all calendar calculations.
- Bazi Engine has produced a valid AnalysisContext.
- Strength Engine has published a valid StrengthResult.
- Rule Database has been validated.
- Runtime configuration is available.

---

# 18. Constraints

The implementation shall not:

- Modify AnalysisContext
- Modify StrengthResult
- Modify Rule Database
- Recompute Day Master strength
- Perform interpretation
- Generate reports
- Call downstream engines
- Access persistence directly

---

# 19. Version Compatibility

Compatible with:

- Analysis Engine V1.x
- Strength Engine V1.x
- Rule Database V1.x
- Interpretation Engine V1.x

Breaking functional changes require a new major version.

---

# 20. Definition of Done

The Temperature Engine functional specification is considered complete when:

- Functional scope is frozen.
- Input and output contracts are frozen.
- Functional requirements are frozen.
- Validation rules are frozen.
- Error conditions are documented.
- Edge cases are documented.
- Acceptance criteria are approved.

Implementation may begin only after this specification is approved.
