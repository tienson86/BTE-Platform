# Strength Engine Specification

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Functional Specification)

---

# 1. Purpose

This document defines the functional specification of the Strength Engine.

It specifies the expected behavior, inputs, outputs, processing rules, constraints, validation requirements, and acceptance criteria.

This specification serves as the authoritative functional contract between the implementation and the rest of the BTE Platform.

---

# 2. Functional Objective

The Strength Engine shall evaluate the strength of the Day Master (Nhật Chủ) using the official Rule Database and produce a normalized, explainable, deterministic `StrengthResult`.

The engine shall not perform interpretation or recommendation.

---

# 3. Functional Scope

The Strength Engine shall:

- Evaluate seasonal influence.
- Evaluate Heavenly Stem contribution.
- Evaluate Earthly Branch contribution.
- Evaluate hidden stem rooting.
- Evaluate supporting elements.
- Evaluate controlling elements.
- Evaluate draining effects.
- Apply official Strength Rules.
- Calculate normalized scores.
- Calculate confidence.
- Produce immutable analytical results.

---

# 4. Out of Scope

The engine shall not:

- Determine Pattern (Cách Cục)
- Determine Useful God (Dụng Thần)
- Evaluate Ten Gods quality
- Evaluate ShenSha
- Evaluate Luck Pillars
- Generate interpretations
- Generate reports
- Render templates
- Modify chart data
- Modify rule data

These responsibilities belong to downstream modules.

---

# 5. Preconditions

Execution requires:

- A valid immutable `AnalysisContext`
- Completed Four Pillars calculation
- Hidden Stem calculation completed
- Five Element distribution available
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

The engine shall not read raw user input.

---

# 7. Output Specification

The engine shall return:

```text
StrengthResult
```

The result shall contain:

- Overall score
- Strength level
- Seasonal score
- Root score
- Heavenly Stem score
- Earthly Branch score
- Support score
- Control score
- Drain score
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

The engine shall reject invalid contexts.

---

## FR-003

The engine shall load only applicable Strength Rules.

---

## FR-004

The engine shall evaluate seasonal influence.

---

## FR-005

The engine shall evaluate root strength.

---

## FR-006

The engine shall evaluate Heavenly Stem influence.

---

## FR-007

The engine shall evaluate Earthly Branch influence.

---

## FR-008

The engine shall evaluate support relationships.

---

## FR-009

The engine shall evaluate control relationships.

---

## FR-010

The engine shall evaluate draining relationships.

---

## FR-011

The engine shall aggregate all analytical dimensions into a normalized score.

---

## FR-012

The engine shall determine a normalized strength level.

---

## FR-013

The engine shall compute a confidence level.

---

## FR-014

The engine shall record every matched rule.

---

## FR-015

The engine shall produce traceable reasoning.

---

## FR-016

The engine shall return an immutable StrengthResult.

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
2. Load applicable rules
3. Analyze seasonal influence
4. Analyze root strength
5. Analyze Heavenly Stems
6. Analyze Earthly Branches
7. Analyze support
8. Analyze control
9. Analyze drain
10. Aggregate scores
11. Evaluate confidence
12. Build StrengthResult

No processing stage may be skipped.

---

# 11. Validation Rules

The engine shall verify:

- Required context fields exist.
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
- Missing rules
- Unsupported rule version
- Invalid calculation state
- Missing analytical data
- Internal evaluation failure

Errors shall be propagated without modifying input data.

---

# 13. Edge Cases

The implementation shall correctly handle:

- Extremely strong Day Master
- Extremely weak Day Master
- Borderline strength values
- Missing optional metadata
- Empty matched rule list
- Conflicting rule matches
- Multiple equal-weight rule outcomes

Behavior shall remain deterministic.

---

# 14. Rule Usage

The engine shall consume only official Strength Rules.

Rules shall never be embedded within source code.

Rule selection shall be based on the Rule Registry.

---

# 15. Dependency Specification

The engine depends on:

- Calendar Engine
- Bazi Engine
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
- StrengthResult is immutable.
- Unit tests pass.
- Integration tests pass.
- Golden dataset validation passes.

---

# 17. Assumptions

The specification assumes:

- Calendar Engine has completed all calendar calculations.
- Bazi Engine has produced a valid AnalysisContext.
- Rule Database has been validated.
- Runtime configuration is available.

---

# 18. Constraints

The implementation shall not:

- Modify AnalysisContext
- Modify Rule Database
- Perform interpretation
- Generate reports
- Call downstream engines
- Access persistence directly

---

# 19. Version Compatibility

Compatible with:

- Analysis Engine V1.x
- Rule Database V1.x
- Interpretation Engine V1.x

Breaking functional changes require a new major version.

---

# 20. Definition of Done

The Strength Engine functional specification is considered complete when:

- Functional scope is frozen.
- Input and output contracts are frozen.
- Functional requirements are frozen.
- Validation rules are frozen.
- Error conditions are documented.
- Edge cases are documented.
- Acceptance criteria are approved.

Implementation may begin only after this specification is approved.