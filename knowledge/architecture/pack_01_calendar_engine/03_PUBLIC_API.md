# 03_PUBLIC_API.md

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

This document defines the official Public API of the Calendar Engine.

Only the interfaces described here may be used by external modules.

Everything else inside the Calendar Engine is considered internal implementation.

---

# 2. API Philosophy

The Calendar Engine exposes a single public service.

External modules never call internal calculators.

External modules never construct BirthContext manually.

The Calendar Engine owns the complete calendar calculation process.

---

# 3. Public Service

Canonical Service

CalendarEngine

Responsibilities

- Validate input
- Normalize input
- Execute runtime pipeline
- Produce BirthContext
- Return Result<BirthContext>

This is the only supported public entry point.

---

# 4. Public Interface

CalendarEngine

run(
    request: BirthRequest
)

↓

Result<BirthContext>

No other method is required by downstream Engines.

---

# 5. Input Contract

Input

BirthRequest

The request must already conform to the BirthRequest schema defined in

01_DATA_MODEL.md

The Calendar Engine never accepts raw dictionaries or anonymous objects.

---

# 6. Output Contract

Output

Result<BirthContext>

Possible outcomes

Success

↓

BirthContext

Failure

↓

Error Information

BirthContext is immutable.

---

# 7. Result Model

Result<T>

contains

success

value

error

warnings

metadata

The Engine never returns null.

The Engine never returns partially initialized objects.

---

# 8. Error Model

Errors include

ValidationError

TimezoneError

CalendarRangeError

CalculationError

UnsupportedDateError

InternalError

Every error includes

- code

- message

- stage

- timestamp

---

# 9. Internal API

The following services are internal only.

ValidationService

NormalizationService

SolarCalendarCalculator

LunarCalendarCalculator

JulianCalculator

SolarTermCalculator

GanzhiCalculator

BirthContextBuilder

These classes must never be used outside the Calendar Engine.

---

# 10. Dependency Rules

Allowed

AnalyzeService

BaZi Engine

Testing Framework

Forbidden

Desktop UI

Score Engine

Interpretation Engine

Report Engine

They must consume BirthContext instead.

---

# 11. Thread Safety

Every call

CalendarEngine.run()

must be independent.

No global mutable state.

Safe for concurrent execution.

---

# 12. Performance

Target

Single request

<50 ms

The API must not require network connectivity.

---

# 13. Versioning

Public API follows semantic versioning.

Major

Breaking API changes

Minor

Backward-compatible additions

Patch

Bug fixes

Breaking changes require architecture approval.

---

# 14. Integration Example

BirthRequest

↓

CalendarEngine.run()

↓

Result<BirthContext>

↓

BaZiEngine.run()

↓

Result<BaziChart>

The Calendar Engine never invokes downstream Engines.

---

# 15. Future Compatibility

Future internal algorithms may change.

Public API must remain stable.

Consumers should never depend on internal implementation details.

---

# 16. Acceptance Criteria

The Public API is considered complete when:

✓ One public service

✓ One public entry point

✓ Strongly typed input

✓ Strongly typed output

✓ Immutable BirthContext

✓ Structured Result<T>

✓ Internal services hidden

✓ Fully documented

---

END OF DOCUMENT