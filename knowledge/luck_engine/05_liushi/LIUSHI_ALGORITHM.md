# LIUSHI ALGORITHM

Version

1.0

Status

Stable

Module

05_liushi

---

# 1. Purpose

This document defines the deterministic processing pipeline for the LiuShi Module.

The algorithm transforms

- Natal Chart
- Current Dayun
- Current LiuNian
- Current LiuYue
- Current LiuRi
- Calendar Context

into a validated Hourly Context.

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
- Support continuous execution

---

# 3. High-Level Pipeline

Input

↓

Validate Input

↓

Resolve Hour Boundary

↓

Retrieve Sexagenary Hour

↓

Generate Hourly Pillar

↓

Expand Hidden Stems

↓

Calculate Ten Gods

↓

Calculate Five Elements

↓

Load Seasonal Context

↓

Load Daily Context

↓

Evaluate Natal Relations

↓

Evaluate Dayun Relations

↓

Evaluate LiuNian Relations

↓

Evaluate LiuYue Relations

↓

Evaluate LiuRi Relations

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

Construct Hourly Context

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

Hourly Pillar Generation

Stage 4

Hidden Stem Expansion

Stage 5

Ten Gods Calculation

Stage 6

Five Element Analysis

Stage 7

Context Loading

Stage 8

Relationship Analysis

Stage 9

Transformation Analysis

Stage 10

Priority Resolution

Stage 11

Hourly Context Construction

Stage 12

Output Validation

---

# 5. Stage 1 — Input Validation

Validate

Natal Chart

Dayun Context

LiuNian Context

LiuYue Context

LiuRi Context

Calendar Context

Rule Database

Priority Rules

Reject processing if any required object is missing.

---

# 6. Stage 2 — Calendar Resolution

Retrieve

Hour Boundary

↓

Hour Branch

↓

Hour Stem

↓

Sexagenary Hour

The LiuShi Module SHALL NOT calculate these values independently.

---

# 7. Stage 3 — Hourly Pillar Generation

Construct

Hourly Pillar

↓

Validate Stem

↓

Validate Branch

↓

Validate Stem-Branch Pair

↓

Store immutable Hourly Pillar

---

# 8. Stage 4 — Hidden Stem Expansion

Retrieve Hidden Stems from the Hidden Stem Database.

Generate

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

Maintain canonical ordering.

---

# 9. Stage 5 — Ten Gods Calculation

Reference

Day Master

↓

Hourly Heavenly Stem

↓

Hourly Hidden Stems

Generate Ten Gods independently.

---

# 10. Stage 6 — Five Element Analysis

Map

Stem

↓

Element

Branch

↓

Dominant Element

Hidden Stems

↓

Elements

Generate

Element Count

Element Balance

Element Summary

---

# 11. Stage 7 — Context Loading

Load

Seasonal Context

↓

Daily Context

↓

Monthly Context

↓

Annual Context

↓

Dayun Context

All inherited contexts SHALL remain immutable.

---

# 12. Stage 8 — Relationship Analysis

Evaluate independently

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

Store every interaction.

---

# 13. Stage 9 — Transformation Analysis

Evaluate

Stem Transformation

↓

Branch Transformation

↓

Hidden Stem Transformation

↓

Season Support

↓

Element Support

↓

Transformation Result

Transformation SHALL occur only when every prerequisite is satisfied.

---

# 14. Stage 10 — Priority Resolution

Load Priority Database.

Resolve

Primary Events

Secondary Events

Suppressed Events

No event SHALL be discarded.

---

# 15. Stage 11 — Hourly Context Construction

Generate immutable

HourlyContext

Containing

- Hourly Pillar
- Hidden Stems
- Ten Gods
- Five Elements
- Seasonal Context
- Daily Context
- Interaction Summary
- Transformation Summary
- Priority Events
- Risk Flags
- Metadata

---

# 16. Stage 12 — Output Validation

Validate

Mandatory Fields

Interaction Consistency

Priority Order

Metadata

Transformation Result

Output Integrity

Return validated Hourly Context.

---

# 17. Performance Requirements

Average latency

<10 ms

Average complexity

O(n)

Support continuous hourly execution.

---

# 18. Error Handling

Every failure SHALL return

Error Code

Message

Processing Stage

Affected Object

Suggested Resolution

No partial output is permitted.

---

# 19. Deterministic Guarantee

Identical inputs SHALL always produce identical outputs.

Random behavior is prohibited.

AI-generated decisions are prohibited.

---

# 20. Future Extension Points

Reserved for

Unified Fortune Timeline

Timeline Scoring

Event Prediction

Cross-Time Analysis

End of Document