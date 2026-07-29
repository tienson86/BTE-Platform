# LIURI EDGE CASES

Version

1.0

Status

Stable

Module

04_liuri

---

# 1. Purpose

Defines all exceptional scenarios during Daily Luck calculation.

Every implementation SHALL follow these rules.

---

# 2. Categories

A. Calendar

B. Day Boundary

C. Daily Pillar

D. Hidden Stems

E. Stem Relations

F. Branch Relations

G. LiuYue Relations

H. LiuNian Relations

I. Dayun Relations

J. Transformations

K. Validation

---

# 3. Calendar Cases

## 3.1 Missing Calendar Context

Return

LIURI_001

CALENDAR_CONTEXT_NOT_FOUND

---

## 3.2 Invalid Julian Day

Return

INVALID_JDN

---

## 3.3 Invalid Sexagenary Index

Return

INVALID_DAY_INDEX

---

## 3.4 Leap Year

Leap years SHALL NOT affect Sexagenary Day generation.

---

# 4. Day Boundary Cases

## 4.1 Midnight Boundary

New day begins at 00:00.

---

## 4.2 Zi Hour Boundary

New day begins according to configured Zi Hour policy.

---

## 4.3 Boundary Timestamp

Exact boundary timestamps SHALL switch immediately.

---

# 5. Daily Pillar Cases

Invalid Stem

↓

INVALID_DAILY_STEM

Invalid Branch

↓

INVALID_DAILY_BRANCH

Invalid Pillar

↓

INVALID_DAILY_PILLAR

---

# 6. Hidden Stem Cases

Missing Hidden Stem

↓

DATABASE_ERROR

Duplicate Hidden Stem

↓

Validation Failure

---

# 7. Stem Relation Cases

Combination + Control

↓

Store both

Transformation failure

↓

Transformation = FALSE

---

# 8. Branch Relation Cases

Harmony + Clash

↓

Both preserved

Partial Three Harmony

↓

Candidate only

Multiple Clashes

↓

Store all

---

# 9. LiuYue Cases

Daily interacts with Monthly.

All interactions SHALL be stored.

---

# 10. LiuNian Cases

Daily interacts with Annual.

Store independently.

---

# 11. Dayun Cases

Daily interacts with Dayun.

Store independently.

---

# 12. Multi-Layer Cases

Natal

↓

Dayun

↓

LiuNian

↓

LiuYue

↓

LiuRi

All interaction layers SHALL coexist.

---

# 13. Transformation Cases

Transformation only succeeds when

Combination

Season Support

Element Support

Rule Support

are all satisfied.

---

# 14. Priority Cases

Harmony

Clash

Transformation

Punishment

Harm

shall coexist.

Priority Engine resolves significance.

---

# 15. Validation Cases

Reject when

Missing Natal Chart

Missing Dayun

Missing LiuNian

Missing LiuYue

Missing Calendar Context

Missing Rule Database

---

# 16. Error Codes

LIURI_001

CALENDAR_CONTEXT_NOT_FOUND

LIURI_002

INVALID_DAILY_STEM

LIURI_003

INVALID_DAILY_BRANCH

LIURI_004

INVALID_DAILY_PILLAR

LIURI_005

MISSING_HIDDEN_STEM

LIURI_006

INVALID_TRANSFORMATION

LIURI_007

INVALID_PRIORITY

LIURI_008

INVALID_DAILY_CONTEXT

LIURI_009

OUTPUT_VALIDATION_FAILED

---

# 17. Deterministic Guarantee

Identical inputs SHALL always generate identical Daily Context.

End of Document