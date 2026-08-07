# 04_VALIDATION_RULES.md

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

This document defines the canonical validation rules of the Calendar Engine.

Validation guarantees that only correct and complete birth information enters the runtime pipeline.

Invalid requests must never reach downstream Engines.

---

# 2. Validation Philosophy

Validation is performed before any calculation.

The Calendar Engine never attempts to "guess" missing information.

The Engine validates.

The Engine does not correct user mistakes automatically.

---

# 3. Validation Pipeline

BirthRequest

↓

Schema Validation

↓

Field Validation

↓

Business Validation

↓

Calendar Validation

↓

Geographic Validation

↓

Timezone Validation

↓

Ready for Runtime

Failure at any stage immediately terminates execution.

---

# 4. Validation Categories

The Calendar Engine performs seven categories of validation.

| Category | Responsibility |
|-----------|----------------|
| Schema | Required fields |
| Type | Data types |
| Date | Gregorian date |
| Time | Local time |
| Geography | Latitude / Longitude |
| Timezone | IANA timezone |
| Calendar | Supported calculation range |

---

# 5. Schema Validation

The following fields are mandatory.

- request_id
- full_name
- gender
- birth_date
- birth_time
- timezone
- latitude
- longitude

Missing required fields return

ValidationError.RequiredField

---

# 6. Data Type Validation

Validate data types.

| Field | Expected Type |
|--------|---------------|
| full_name | string |
| gender | enum |
| birth_date | date |
| birth_time | time |
| timezone | string |
| latitude | decimal |
| longitude | decimal |

Unexpected types are rejected.

No automatic conversion is performed.

---

# 7. Date Validation

The Gregorian birth date must satisfy:

✓ Valid calendar date

✓ Existing day

✓ Existing month

✓ Existing year

Examples

✓ 1987-01-21

✓ 2000-02-29

Invalid

✗ 2025-02-30

✗ 2025-13-10

✗ 2025-00-01

---

# 8. Time Validation

Birth time must satisfy:

Hour

00–23

Minute

00–59

Second

00–59

Examples

✓ 04:15

✓ 23:59

Invalid

✗ 24:10

✗ 12:61

---

# 9. Geographic Validation

Latitude

Range

-90

↓

90

Longitude

Range

-180

↓

180

Coordinates outside these ranges are rejected.

---

# 10. Timezone Validation

Timezone must be a valid IANA timezone.

Examples

Asia/Ho_Chi_Minh

Asia/Shanghai

Asia/Tokyo

UTC

Invalid

GMT+7

Vietnam

UTC+0700

---

# 11. Calendar Range Validation

Supported years

Configurable

Example

1600

↓

2200

Dates outside the supported range return

CalendarRangeError

---

# 12. Leap Year Validation

Leap year rules follow the Gregorian calendar.

Leap day

29 February

must exist only in leap years.

---

# 13. Leap Month Validation

Leap month validation occurs only after lunar conversion.

Leap month consistency must match the official calendar database.

---

# 14. Business Validation

Gender must be one of

Male

Female

Future versions may extend this enumeration.

Unknown values are rejected.

---

# 15. Duplicate Validation

Duplicate requests are allowed.

Each request receives a unique request_id.

The Calendar Engine does not perform deduplication.

---

# 16. Warning Rules

Certain inputs generate warnings instead of errors.

Examples

Unknown location name

Approximate coordinates

Historical timezone uncertainty

Warnings never stop execution.

Warnings are included in BirthContext.

---

# 17. Error Model

Validation errors include:

RequiredFieldError

InvalidTypeError

InvalidDateError

InvalidTimeError

InvalidTimezoneError

InvalidCoordinateError

CalendarRangeError

LeapMonthError

BusinessRuleError

Every error contains:

- code
- message
- field
- stage
- timestamp

---

# 18. Validation Result

Validation returns

Result<BirthRequest>

Success

↓

Continue pipeline

Failure

↓

Result.Error

↓

Pipeline terminated

---

# 19. Validation Principles

Validation must be:

- deterministic
- repeatable
- side-effect free
- stateless

Validation never modifies input data.

Validation never performs calculations.

Validation never creates output models.

---

# 20. Logging

Every validation stage records:

- stage
- execution time
- success
- warnings
- errors

Sensitive user data must never be written to logs.

---

# 21. Acceptance Checklist

Validation is complete when:

✓ Required fields validated

✓ Types validated

✓ Dates validated

✓ Times validated

✓ Coordinates validated

✓ Timezone validated

✓ Calendar range validated

✓ Leap year validated

✓ Leap month validated

✓ Warning system implemented

✓ Structured Result returned

---

END OF DOCUMENT