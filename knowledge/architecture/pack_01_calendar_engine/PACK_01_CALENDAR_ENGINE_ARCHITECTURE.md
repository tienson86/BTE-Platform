# PACK_01_CALENDAR_ENGINE_ARCHITECTURE

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

Calendar Engine is the root engine of the BTE Platform.

Its responsibility is to transform a user's birth information into a canonical BirthContext.

Every downstream engine depends on this output.

The Calendar Engine performs calendar calculations only.

It must never contain BaZi logic, scoring logic, interpretation logic, or report logic.

---

# 2. Position in the Architecture

Pipeline

Birth Request

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

Score Engine

↓

Interpretation Engine

↓

Report Engine

The Calendar Engine is always executed first.

No Engine may bypass or replace it.

---

# 3. Responsibilities

Calendar Engine is responsible for:

✓ Date validation

✓ Time validation

✓ Timezone normalization

✓ Geographic normalization

✓ Solar calendar

✓ Lunar calendar

✓ Julian Day

✓ Ganzhi calculation

✓ Solar Terms

✓ Season detection

✓ Calendar metadata

Calendar Engine is NOT responsible for:

✗ Four Pillars interpretation

✗ Pattern analysis

✗ Strength calculation

✗ Useful God

✗ Ten Gods

✗ Report generation

---

# 4. Inputs

The Engine accepts exactly one input model.

BirthRequest

Required fields

- full_name
- gender
- birth_date
- birth_time
- timezone
- latitude
- longitude

Optional

- daylight_saving
- calendar_override
- location_name

No other input is allowed.

---

# 5. Output

Calendar Engine produces exactly one canonical output.

BirthContext

BirthContext is immutable.

It becomes the official input for all downstream Engines.

---

# 6. BirthContext

BirthContext contains:

Identity

- request_id

- generated_at

- version

Birth

- solar_datetime

- lunar_datetime

Calendar

- julian_day

- leap_month

- timezone

- utc_offset

Astronomy

- solar_term

- season

- longitude

- latitude

Ganzhi

- year_ganzhi

- month_ganzhi

- day_ganzhi

- hour_ganzhi

Metadata

- calculation_source

- confidence

- warnings

---

# 7. Public API

The Engine exposes one public service.

CalendarEngine

Methods

validate()

normalize()

calculate()

build_context()

run()

run()

returns

Result<BirthContext>

---

# 8. Runtime Flow

BirthRequest

↓

Validate

↓

Normalize

↓

Solar Calendar

↓

Lunar Calendar

↓

Julian Day

↓

Solar Terms

↓

Season

↓

Ganzhi

↓

BirthContext

↓

Result

---

# 9. Validation

The Engine validates

Date

Time

Timezone

Coordinates

Calendar Range

Leap Month

Invalid input returns

Result.Error

No downstream execution occurs.

---

# 10. Error Handling

Every execution returns

Result<BirthContext>

Never

null

Never

exceptions as business flow.

Business failures become Result.Error.

Unexpected failures are logged.

---

# 11. Dependency Rules

Allowed

Utilities

Astronomy Library

Timezone Library

Calendar Database

Forbidden

BaZi Engine

Score Engine

Interpretation Engine

Report Engine

UI

Calendar Engine must not know downstream systems.

---

# 12. Performance

Target

Single calculation

<50ms

Batch

1000 charts

<5 seconds

No network dependency during calculation.

---

# 13. Thread Safety

The Engine must be stateless.

No shared mutable state.

Safe for concurrent execution.

---

# 14. Test Strategy

Unit Tests

Validation

Timezone

Julian

Solar Terms

Ganzhi

Leap Month

Boundary

Integration Tests

BirthRequest

↓

BirthContext

Golden Dataset

Verified historical charts

Regression Tests

Every release

---

# 15. Golden Dataset

The Calendar Engine must maintain an official Golden Dataset.

Each dataset contains

BirthRequest

Expected BirthContext

Expected Ganzhi

Expected Solar Terms

Expected Julian Day

The dataset becomes the reference for all future releases.

---

# 16. Logging

Log

Start

Validation

Calculation

Warnings

Errors

Completion

Logs must never contain private user information beyond what is necessary for debugging.

---

# 17. Versioning

Major

Breaking model changes

Minor

New fields

Patch

Bug fixes

BirthContext schema changes require Major version approval.

---

# 18. Integration Contract

Downstream Engines consume only

BirthContext.

No Engine recalculates calendar information.

No Engine reconstructs Ganzhi independently.

BirthContext is the single source of truth.

---

# 19. Future Extension

Future support may include

Historical calendars

Regional calendar variants

Astronomical precision improvements

High-precision solar calculations

Alternative calendar systems

Extensions must preserve BirthContext compatibility.

---

# 20. Acceptance Checklist

The Pack is complete only if:

✓ Public API implemented

✓ BirthContext finalized

✓ Validation complete

✓ Unit Tests pass

✓ Integration Tests pass

✓ Golden Dataset verified

✓ Documentation complete

✓ Performance targets met

✓ Thread safety verified

✓ Architecture review approved

---

END OF DOCUMENT