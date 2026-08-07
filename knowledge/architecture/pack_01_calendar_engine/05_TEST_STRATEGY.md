# 05_TEST_STRATEGY.md

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

This document defines the official testing strategy for the Calendar Engine.

The objective is to ensure that every calculation performed by the Calendar Engine is:

- Correct
- Repeatable
- Deterministic
- Backward Compatible
- Production Ready

No release may proceed without passing all required test levels.

---

# 2. Testing Philosophy

The Calendar Engine is the root engine of the BTE Platform.

Errors introduced here propagate to every downstream Engine.

Testing therefore focuses on correctness before performance.

The same BirthRequest must always produce the same BirthContext.

---

# 3. Testing Pyramid

The Calendar Engine uses six testing layers.

Level 1

Unit Tests

↓

Level 2

Component Tests

↓

Level 3

Integration Tests

↓

Level 4

Golden Dataset Tests

↓

Level 5

Regression Tests

↓

Level 6

Performance Tests

All six levels are mandatory.

---

# 4. Unit Tests

Purpose

Verify every class in isolation.

Coverage includes:

- ValidationService
- NormalizationService
- SolarCalendarCalculator
- LunarCalendarCalculator
- JulianCalculator
- SolarTermCalculator
- GanzhiCalculator
- BirthContextBuilder

Requirements

✓ Independent

✓ Deterministic

✓ Fast

Target execution time

< 2 seconds

Coverage target

≥ 95%

---

# 5. Component Tests

Purpose

Verify interaction between closely related components.

Examples

Validation

↓

Normalization

Calendar

↓

Astronomy

Astronomy

↓

Ganzhi

BirthContextBuilder

↓

BirthContext

Mock external dependencies when appropriate.

---

# 6. Integration Tests

Purpose

Verify the complete Calendar Engine pipeline.

Pipeline

BirthRequest

↓

Validation

↓

Normalization

↓

Calendar

↓

Astronomy

↓

Ganzhi

↓

BirthContext

↓

Result

All stages execute together.

No mocked runtime pipeline.

---

# 7. Golden Dataset Tests

Purpose

Protect calculation accuracy.

The Golden Dataset contains officially verified birth cases.

Each case includes:

BirthRequest

Expected BirthContext

Expected Solar Calendar

Expected Lunar Calendar

Expected Julian Day

Expected Solar Term

Expected Ganzhi

Expected Season

The Golden Dataset is the highest authority for runtime correctness.

---

# 8. Regression Tests

Purpose

Prevent previously fixed bugs from returning.

Every production bug must generate:

- Regression case
- Regression dataset
- Regression unit test

Regression tests are permanent.

---

# 9. Performance Tests

Purpose

Ensure acceptable runtime performance.

Target

Single request

< 50 ms

100 requests

< 500 ms

1000 requests

< 5 s

Performance tests use release builds.

---

# 10. Boundary Tests

Verify extreme values.

Examples

Minimum supported year

Maximum supported year

Leap year

Leap day

Leap month

Midnight

23:59

Timezone boundary

Coordinate boundary

Historical timezone changes

Boundary cases are mandatory.

---

# 11. Error Tests

Verify expected failures.

Examples

Missing required fields

Invalid dates

Invalid time

Invalid timezone

Invalid latitude

Invalid longitude

Unsupported year

Every error must return Result.Error.

No runtime crashes are acceptable.

---

# 12. Determinism Tests

Given identical input,

the Engine must always produce identical output.

BirthRequest A

↓

Run #1

↓

BirthContext X

BirthRequest A

↓

Run #2

↓

BirthContext X

Random output is prohibited.

---

# 13. Concurrency Tests

Verify thread safety.

Multiple calculations execute simultaneously.

Requirements

No shared mutable state.

No race conditions.

No inconsistent results.

---

# 14. Serialization Tests

Verify that canonical models support serialization.

Required formats

- JSON
- YAML
- MessagePack

Serialization must preserve every field.

---

# 15. Compatibility Tests

Verify compatibility across releases.

BirthContext V1.x

must remain readable by

supported consumers.

Breaking schema changes require a major version.

---

# 16. Test Data Organization

tests/

unit/

component/

integration/

golden/

regression/

performance/

Fixtures

must be version controlled.

Golden datasets

must never be edited without architecture approval.

---

# 17. Continuous Integration

Every Pull Request must execute:

✓ Unit Tests

✓ Component Tests

✓ Integration Tests

✓ Golden Dataset Tests

Regression and Performance tests may run separately in CI pipelines.

A failing mandatory test blocks merge.

---

# 18. Coverage Requirements

| Category | Target |
|----------|--------|
| Unit Test Coverage | ≥ 95% |
| Component Coverage | 100% of services |
| Integration Coverage | 100% of runtime pipeline |
| Golden Dataset Coverage | 100% official cases |
| Regression Coverage | 100% known defects |
| Public API Coverage | 100% |

Coverage numbers are minimum requirements.

---

# 19. Acceptance Criteria

The Calendar Engine passes testing only if:

✓ All Unit Tests pass

✓ All Component Tests pass

✓ All Integration Tests pass

✓ Golden Dataset matches expected results

✓ Regression Tests pass

✓ Performance targets achieved

✓ No critical defects remain

---

# 20. Test Governance

Tests are part of the architecture.

No implementation is considered complete without tests.

Every new feature requires:

- Unit Tests
- Integration Tests
- Golden Dataset update (if applicable)

Every bug fix requires:

- Regression Test

Every release requires:

- Full test execution

Testing is mandatory for every version of the Calendar Engine.

---

END OF DOCUMENT