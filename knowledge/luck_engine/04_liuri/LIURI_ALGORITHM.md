# LIURI ALGORITHM

Version

1.0

Status

Stable

Module

04_liuri

---

# 1. Purpose

This document defines the deterministic processing pipeline for the LiuRi Module.

The algorithm transforms

- Natal Chart
- Current Dayun
- Current LiuNian
- Current LiuYue
- Calendar Context

into a validated Daily Context.

No AI reasoning is involved.

The algorithm is completely deterministic.

---

# 2. Design Principles

The processing pipeline SHALL

- Produce deterministic results
- Produce immutable outputs
- Be rule-based
- Be reproducible
- Be independently testable
- Support batch execution

---

# 3. High-Level Pipeline

Input

↓

Validate Input

↓

Resolve Day Boundary

↓

Retrieve Sexagenary Day

↓

Generate Daily Pillar

↓

Expand Hidden Stems

↓

Calculate Ten Gods

↓

Calculate Five Elements

↓

Load Seasonal Context

↓

Evaluate Natal Relations

↓

Evaluate Dayun Relations

↓

Evaluate LiuNian Relations

↓

Evaluate LiuYue Relations

↓

Evaluate Stem Relations

↓

Evaluate Branch Relations

↓

Evaluate Hidden Stem Relations

↓

Evaluate Transformations

↓

Resolve Priorities

↓

Construct Daily Context

↓

Validate Output

↓

Return Result

---

# 4. Processing Stages

Stage 1

Input Validation

Stage 2

Calendar Resolution

Stage 3

Daily Pillar Generation

Stage 4

Hidden Stem Expansion

Stage 5

Ten Gods Calculation

Stage 6

Five Element Analysis

Stage 7

Seasonal Context Loading

Stage 8

Relationship Analysis

Stage 9

Transformation Analysis

Stage 10

Priority Resolution

Stage 11

Daily Context Construction

Stage 12

Output Validation

---

# 5. Stage 1 — Input Validation

Validate

Natal Chart

Dayun Context

LiuNian Context

LiuYue Context

Calendar Context

Rule Database

Priority Rules

Reject processing if any required object is missing.

---

# 6. Stage 2 — Calendar Resolution

Retrieve

Julian Day Number

↓

Sexagenary Day Index

↓

Daily Heavenly Stem

↓

Daily Earthly Branch

The LiuRi Module SHALL NOT calculate these values independently.

---

# 7. Stage 3 — Daily Pillar Generation

Construct

Daily Pillar

↓

Validate Sexagenary Pair

↓

Store immutable Daily Pillar

---

# 8. Stage 4 — Hidden Stem Expansion

Retrieve Hidden Stems from the Branch Database.

Store

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

Maintain canonical ordering.

---

# 9. Stage 5 — Ten Gods Calculation

Reference

Day Master

↓

Daily Heavenly Stem

↓

Daily Hidden Stems

Generate Ten Gods for every stem independently.

---

# 10. Stage 6 — Five Element Analysis

Map

Stem → Element

Branch → Dominant Element

Hidden Stem → Element

Generate

Daily Element Summary

Daily Element Count

Daily Element Balance

---

# 11. Stage 7 — Seasonal Context Loading

Load Seasonal Context from LiuYue.

The LiuRi Module SHALL NOT recalculate seasonal strength.

---

# 12. Stage 8 — Relationship Analysis

Evaluate independently

Natal Relations

↓

Dayun Relations

↓

LiuNian Relations

↓

LiuYue Relations

↓

Daily Relations

No layer may overwrite another.

---

# 13. Stage 9 — Transformation Analysis

Evaluate

Stem Transformation

↓

Branch Transformation

↓

Hidden Stem Transformation

↓

Seasonal Support

↓

Transformation Result

Transformation SHALL occur only if all prerequisites are satisfied.

---

# 14. Stage 10 — Priority Resolution

Load Priority Database.

Sort detected events.

Resolve conflicts.

Generate

Primary Events

Secondary Events

Suppressed Events

No event SHALL be discarded.

---

# 15. Stage 11 — Daily Context Construction

Generate

DailyContext

Containing

Daily Pillar

Hidden Stems

Ten Gods

Element Summary

Seasonal Context

Interaction Summary

Transformation Summary

Priority Events

Risk Flags

Metadata

Return immutable object.

---

# 16. Stage 12 — Output Validation

Validate

Mandatory Fields

Metadata

Priority Order

Interaction Consistency

Transformation Consistency

Element Counts

Ten Gods

Return validated Daily Context.

---

# 17. Performance Requirements

Average latency

<10 ms

Average complexity

O(n)

Support batch execution.

---

# 18. Error Handling

Every failure SHALL return

Error Code

Message

Processing Stage

Affected Object

Suggested Resolution

No partial output is allowed.

---

# 19. Deterministic Guarantee

Identical inputs SHALL always produce identical outputs.

Random behavior is prohibited.

AI-generated decisions are prohibited.

---

# 20. Future Extension Points

Reserved for

LiuShi

Unified Fortune Timeline

Cross-Day Event Engine

Predictive Timeline Engine

End of Document