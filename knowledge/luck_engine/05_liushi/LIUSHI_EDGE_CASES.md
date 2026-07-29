# LIUSHI EDGE CASES

Version

1.0

Status

Stable

Module

05_liushi

---

# 1. Purpose

Defines exceptional situations during Hourly Luck calculation.

Every implementation SHALL follow these rules.

---

# 2. Categories

A. Calendar

B. Hour Boundary

C. Hourly Pillar

D. Hidden Stems

E. Stem Relations

F. Branch Relations

G. LiuRi Relations

H. LiuYue Relations

I. LiuNian Relations

J. Dayun Relations

K. Transformations

L. Validation

---

# 3. Calendar Cases

Missing Calendar Context

↓

LIUSHI_001

Invalid Hour Index

↓

INVALID_HOUR_INDEX

Invalid Sexagenary Hour

↓

INVALID_SEXAGENARY_HOUR

Timezone mismatch

↓

CONFIGURATION_ERROR

---

# 4. Hour Boundary Cases

Traditional Double Hour

Timezone-adjusted Hour

DST transition (if configured)

Boundary timestamp

All transitions SHALL be handled exclusively by the Calendar Engine.

---

# 5. Hourly Pillar Cases

Invalid Stem

↓

INVALID_HOUR_STEM

Invalid Branch

↓

INVALID_HOUR_BRANCH

Invalid Pillar

↓

INVALID_HOUR_PILLAR

---

# 6. Hidden Stem Cases

Missing Hidden Stem

↓

DATABASE_ERROR

Duplicate Hidden Stem

↓

Validation Failure

Canonical order violation

↓

Validation Failure

---

# 7. Stem Relation Cases

Combination

Control

Generation

Transformation

Competition

All SHALL coexist.

---

# 8. Branch Relation Cases

Six Harmony

Six Clash

Three Harmony

Three Meetings

Punishment

Harm

Destruction

Self Punishment

Store all detected relations.

---

# 9. LiuRi Cases

Hourly interacts with Daily.

Every interaction SHALL remain independent.

---

# 10. LiuYue Cases

Hourly interacts with Monthly.

Store independently.

---

# 11. LiuNian Cases

Hourly interacts with Annual.

Store independently.

---

# 12. Dayun Cases

Hourly interacts with Dayun.

Store independently.

---

# 13. Multi-Layer Cases

Natal

↓

Dayun

↓

LiuNian

↓

LiuYue

↓

LiuRi

↓

LiuShi

No layer may overwrite another.

---

# 14. Transformation Cases

Transformation succeeds only when

Combination exists

Season Support

Element Support

Rule Support

Otherwise

Transformation = FALSE

---

# 15. Validation Cases

Reject when

Missing Natal Chart

Missing Dayun

Missing LiuNian

Missing LiuYue

Missing LiuRi

Missing Calendar Context

Missing Rule Database

---

# 16. Error Codes

LIUSHI_001

CALENDAR_CONTEXT_NOT_FOUND

LIUSHI_002

INVALID_HOUR_STEM

LIUSHI_003

INVALID_HOUR_BRANCH

LIUSHI_004

INVALID_HOUR_PILLAR

LIUSHI_005

MISSING_HIDDEN_STEM

LIUSHI_006

INVALID_TRANSFORMATION

LIUSHI_007

INVALID_PRIORITY

LIUSHI_008

INVALID_HOURLY_CONTEXT

LIUSHI_009

OUTPUT_VALIDATION_FAILED

---

# 17. Deterministic Guarantee

Identical inputs SHALL always produce identical Hourly Context.

End of Document