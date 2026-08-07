# 02_RUNTIME_PIPELINE.md

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

This document defines the runtime execution pipeline of the Calendar Engine.

It specifies:

- Execution stages
- Input and output models
- Validation boundaries
- Processing order
- Error propagation
- Runtime guarantees

The pipeline defined here is canonical.

Every execution of the Calendar Engine must follow this sequence.

---

# 2. Runtime Philosophy

The Calendar Engine is deterministic.

Given the same BirthRequest,
the Engine must always produce the same BirthContext.

The Engine:

- has no UI
- has no business logic
- has no interpretation
- has no scoring
- has no side effects

The Engine transforms data only.

---

# 3. Canonical Pipeline

BirthRequest

↓

Validation

↓

Normalization

↓

Calendar Calculation

↓

Astronomical Calculation

↓

Ganzhi Calculation

↓

BirthContext Builder

↓

BirthContext Validation

↓

Result<BirthContext>

---

# 4. Stage Overview

| Stage | Input | Output | Responsibility |
|--------|-------|--------|----------------|
| 01 | BirthRequest | BirthRequest | Validation |
| 02 | BirthRequest | NormalizedBirthRequest | Normalization |
| 03 | NormalizedBirthRequest | CalendarData | Solar/Lunar conversion |
| 04 | CalendarData | AstronomyData | Julian, Solar Terms, Season |
| 05 | AstronomyData | GanzhiData | Heavenly Stems & Earthly Branches |
| 06 | GanzhiData | BirthContext | Canonical Context Builder |
| 07 | BirthContext | Result<BirthContext> | Final Validation |

---

# 5. Stage 01 — Validation

Input

BirthRequest

Checks

✓ Required fields

✓ Date format

✓ Time format

✓ Timezone

✓ Latitude

✓ Longitude

✓ Supported calendar range

Output

Validated BirthRequest

Failure

Result.Error

No downstream execution.

---

# 6. Stage 02 — Normalization

Responsibilities

Normalize:

- Date
- Time
- UTC Offset
- Timezone
- Coordinates

Resolve:

- DST
- Historical timezone
- Internal formatting

Output

NormalizedBirthRequest

No calculations occur here.

---

# 7. Stage 03 — Calendar Calculation

Consumes

NormalizedBirthRequest

Produces

CalendarData

Responsibilities

- Solar calendar
- Lunar calendar
- Leap month
- Lunar date

No Ganzhi calculation.

---

# 8. Stage 04 — Astronomical Calculation

Consumes

CalendarData

Produces

AstronomyData

Responsibilities

- Julian Day Number
- Solar Terms
- Seasonal information
- Astronomical metadata

No BaZi logic.

---

# 9. Stage 05 — Ganzhi Calculation

Consumes

AstronomyData

Produces

GanzhiData

Responsibilities

Calculate

- Year Pillar
- Month Pillar
- Day Pillar
- Hour Pillar

Calculate

- Heavenly Stem
- Earthly Branch

Determine

- Yin / Yang
- Zodiac

No hidden stems.

No Ten Gods.

No Na Yin.

Those belong to the BaZi Engine.

---

# 10. Stage 06 — BirthContext Builder

Consumes

GanzhiData

Produces

BirthContext

Responsibilities

Merge

- Original Request
- Calendar Data
- Astronomy Data
- Ganzhi Data

into one immutable object.

BirthContext becomes the canonical output.

---

# 11. Stage 07 — Final Validation

Validate

BirthContext

Checks

✓ Required fields

✓ Consistency

✓ Timezone

✓ Ganzhi

✓ Solar/Lunar relationship

Output

Result<BirthContext>

---

# 12. Error Flow

Errors stop execution immediately.

BirthRequest

↓

Validation

↓

❌ Error

↓

Result.Error

↓

Pipeline terminated

The Engine never returns partial results.

---

# 13. Success Flow

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

Success

Every stage must complete successfully.

---

# 14. Runtime Characteristics

The pipeline must be

- deterministic
- stateless
- thread-safe
- repeatable
- idempotent

The same input always produces the same output.

---

# 15. Logging Pipeline

Log

START

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

END

Errors are logged with stage information.

No sensitive personal data should be written to logs.

---

# 16. Performance Targets

Single chart

Target

<50 ms

Batch

100 charts

<500 ms

Batch

1000 charts

<5 s

The runtime must not depend on network connectivity.

---

# 17. Thread Safety

Every execution creates its own context.

No shared mutable state.

Safe for concurrent execution.

---

# 18. Extension Points

Future stages may be inserted only after architecture approval.

Possible extensions

- High precision astronomy
- Historical calendar corrections
- Regional calendar variants

Extensions must preserve the canonical BirthContext schema.

---

# 19. Downstream Contract

The Calendar Engine guarantees:

BirthContext is complete.

BirthContext is immutable.

BirthContext is validated.

Every downstream Engine must consume BirthContext directly.

No Engine is allowed to recalculate:

- Solar calendar
- Lunar calendar
- Ganzhi
- Solar Terms

The Calendar Engine is the single source of truth.

---

# 20. Runtime Diagram

BirthRequest

↓

[01 Validation]

↓

[02 Normalization]

↓

[03 Calendar]

↓

[04 Astronomy]

↓

[05 Ganzhi]

↓

[06 BirthContext Builder]

↓

[07 Final Validation]

↓

Result<BirthContext>

↓

BaZi Engine

---

# 21. Acceptance Criteria

The Runtime Pipeline is considered complete when:

✓ Every stage has a single responsibility.

✓ Every stage has unit tests.

✓ Every stage has integration tests.

✓ The complete pipeline passes the Golden Dataset.

✓ BirthContext is produced successfully.

✓ Downstream Engines consume BirthContext without recalculating calendar data.

---

END OF DOCUMENT