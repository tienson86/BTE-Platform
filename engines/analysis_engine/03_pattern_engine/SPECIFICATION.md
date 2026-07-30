# Pattern Engine Specification

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Functional Specification)

---

# 1. Purpose

This document defines the functional specification of the Pattern Engine.

It specifies the expected behavior, inputs, outputs, processing rules, constraints, validation requirements, and acceptance criteria.

This specification serves as the authoritative functional contract between the implementation and the rest of the BTE Platform.

---

# 2. Functional Objective

The Pattern Engine shall determine the natal Pattern (Ge Ju / 格局) using the official Rule Database and produce a normalized, explainable, deterministic `PatternResult`.

The engine shall not perform interpretation or recommendation.

The engine shall not recompute Day Master strength or climate balance.

---

# 3. Functional Scope

The Pattern Engine shall:

- Analyse chart structure.
- Evaluate Day Master relationship with chart composition.
- Identify standard patterns.
- Identify transformed patterns.
- Identify special patterns.
- Identify follow patterns.
- Support mixed and exceptional patterns through Pattern Rules.
- Generate and evaluate competing pattern candidates.
- Resolve pattern conflicts.
- Resolve priority contests.
- Apply official Pattern Rules.
- Consume published StrengthResult from AnalysisContext.strength_result.
- Consume published TemperatureResult from AnalysisContext.temperature_result.
- Calculate pattern confidence.
- Produce immutable analytical results.

---

# 4. Out of Scope

The engine shall not:

- Recompute Strength
- Recompute Temperature
- Determine Useful God
- Analyse Ten Gods quality
- Evaluate ShenSha
- Evaluate Luck
- Generate interpretations
- Generate reports
- Render templates
- Modify chart data
- Modify AnalysisContext.strength_result
- Modify AnalysisContext.temperature_result
- Modify rule data

These responsibilities belong to other modules.

---

# 5. Preconditions

Execution requires:

- A valid immutable `AnalysisContext`
- A valid immutable `AnalysisContext.strength_result`
- A valid immutable `AnalysisContext.temperature_result`
- Completed Four Pillars calculation
- Hidden Stem calculation completed
- Five Element distribution available
- Completed Strength Engine evaluation published into AnalysisContext
- Completed Temperature Engine evaluation published into AnalysisContext
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

The engine shall not read raw user input.
The engine shall not accept StrengthResult or TemperatureResult as separate function parameters.
No additional input models shall be introduced.

---

# 7. Output Specification

The engine shall return:

```text
PatternResult
```

The result shall contain at least:

- identified pattern
- pattern category
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

The engine shall reject invalid contexts or missing upstream stage results.

---

## FR-005

The engine shall load only applicable Pattern Rules from `knowledge/rule_database/04_pattern_rules/`.

---

## FR-006

The engine shall analyse chart structure for pattern eligibility.

---

## FR-007

The engine shall evaluate Day Master relationship with chart composition.

---

## FR-008

The engine shall identify standard pattern candidates.

---

## FR-009

The engine shall identify transformed pattern candidates.

---

## FR-010

The engine shall identify special pattern candidates.

---

## FR-011

The engine shall identify follow pattern candidates.

---

## FR-012

The engine shall support mixed and exceptional pattern candidates through Pattern Rules.

---

## FR-013

The engine shall generate competing pattern candidates.

---

## FR-014

The engine shall evaluate pattern candidates.

---

## FR-015

The engine shall resolve pattern conflicts.

---

## FR-016

The engine shall resolve priority contests.

---

## FR-017

The engine shall compute a confidence level.

---

## FR-018

The engine shall record every matched rule.

---

## FR-019

The engine shall record rejected candidates.

---

## FR-020

The engine shall produce traceable reasoning and diagnostics.

---

## FR-021

The engine shall return an immutable PatternResult.

---

## FR-022

The engine shall never recompute Day Master strength.

---

## FR-023

The engine shall never recompute climate balance.

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

New rules and pattern categories shall not require public API modification within Version 1.x.

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
5. Load Pattern Rules
6. Analyse Structure
7. Generate Pattern Candidates
8. Evaluate Candidates
9. Resolve Priority
10. Calculate Confidence
11. Build Immutable PatternResult
12. Publish PatternResult

No processing stage may be skipped.

---

# 11. Validation Rules

The engine shall verify:

- Required context fields exist.
- AnalysisContext.strength_result is present and valid.
- AnalysisContext.temperature_result is present and valid.
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

- Single clear pattern match
- Multiple competing standard patterns
- Competing special, follow, and transformation patterns
- Mixed and exceptional pattern candidates
- Borderline pattern scores
- Empty rejected-candidate list when only one candidate exists
- Missing optional metadata
- Empty matched rule list
- Conflicting rule matches
- Multiple equal-weight rule outcomes
- Upstream results present with minimal optional diagnostics

Behavior shall remain deterministic.

---

# 14. Rule Usage

The engine shall consume only official Pattern Rules from:

```text
knowledge/rule_database/04_pattern_rules/
```

Rules shall never be embedded within source code.

Rule selection shall be based on the Rule Registry.

---

# 15. Dependency Specification

The engine depends on:

- Calendar Engine
- Bazi Engine
- Strength Engine (via AnalysisContext.strength_result only)
- Temperature Engine (via AnalysisContext.temperature_result only)
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
- PatternResult is immutable.
- Day Master strength is never recomputed.
- Climate balance is never recomputed.
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
- Rule Database has been validated.
- Runtime configuration is available.

---

# 18. Constraints

The implementation shall not:

- Modify AnalysisContext
- Modify AnalysisContext.strength_result
- Modify AnalysisContext.temperature_result
- Modify Rule Database
- Recompute Day Master strength
- Recompute climate balance
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
- Rule Database V1.x
- Interpretation Engine V1.x

Breaking functional changes require a new major version.

---

# 20. Definition of Done

The Pattern Engine functional specification is considered complete when:

- Functional scope is frozen.
- Input and output contracts are frozen.
- Functional requirements are frozen.
- Validation rules are frozen.
- Error conditions are documented.
- Edge cases are documented.
- Acceptance criteria are approved.

Implementation may begin only after this specification is approved.
