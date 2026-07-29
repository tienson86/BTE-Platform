# LIUYUE ALGORITHM

Version: 1.0

Status

Stable

Module

03_liuyue

---

# 1. Purpose

This document defines the deterministic processing pipeline used by the LiuYue
Module.

The algorithm converts

- Natal Chart
- Current Dayun
- Current LiuNian
- Gregorian Date

into a fully validated Monthly Context.

The algorithm contains no AI reasoning.

The algorithm is completely deterministic.

---

# 2. Design Principles

The processing pipeline SHALL

- Produce deterministic results
- Produce immutable outputs
- Be rule-driven
- Be reproducible
- Be independently testable
- Be version controlled

---

# 3. High-Level Pipeline

Input

↓

Validate Input

↓

Determine Solar Month

↓

Generate Monthly Pillar

↓

Generate Hidden Stems

↓

Calculate Ten Gods

↓

Calculate Five Elements

↓

Evaluate Seasonal Context

↓

Evaluate Natal Relations

↓

Evaluate Dayun Relations

↓

Evaluate LiuNian Relations

↓

Evaluate Stem Relations

↓

Evaluate Branch Relations

↓

Evaluate Hidden Stem Relations

↓

Evaluate Transformations

↓

Evaluate Priority Rules

↓

Build Monthly Context

↓

Validate Output

↓

Return Result

---

# 4. Processing Stages

The LiuYue Module SHALL execute the following stages.

Stage 1

Input Validation

Stage 2

Solar Month Resolution

Stage 3

Monthly Pillar Generation

Stage 4

Hidden Stem Expansion

Stage 5

Ten Gods Calculation

Stage 6

Five Element Analysis

Stage 7

Seasonal Analysis

Stage 8

Relationship Analysis

Stage 9

Transformation Analysis

Stage 10

Priority Resolution

Stage 11

Monthly Context Construction

Stage 12

Output Validation

---

# 5. Stage 1 — Input Validation

Validate

Natal Chart

Current Dayun

Current LiuNian

Gregorian Date

Solar Term Calendar

Rule Database

Priority Rules

Configuration

Reject processing immediately if any mandatory object is missing.

---

# 6. Stage 2 — Solar Month Resolution

Input

Gregorian Date

↓

Locate Current Solar Term

↓

Locate Solar Month

↓

Determine Monthly Branch

The Lunar Calendar SHALL NOT be used.

The Solar Term Calendar SHALL be the only source of month boundaries.

---

# 7. Stage 3 — Monthly Pillar Generation

Generate

Monthly Heavenly Stem

↓

Monthly Earthly Branch

↓

Monthly Pillar

The Monthly Heavenly Stem SHALL follow the Five Tiger Dunjia rules.

The Monthly Earthly Branch SHALL follow the Solar Month sequence.

---

# 8. Stage 4 — Hidden Stem Expansion

Retrieve

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

Store every Hidden Stem in canonical order.

---

# 9. Stage 5 — Ten Gods Calculation

Reference

Day Master

↓

Monthly Heavenly Stem

↓

Monthly Hidden Stems

Generate

Monthly Ten Gods

Every Hidden Stem SHALL receive its own Ten God.

---

# 10. Stage 6 — Five Element Analysis

Map

Monthly Stem

↓

Element

Monthly Branch

↓

Dominant Element

Hidden Stems

↓

Elements

Generate

Monthly Element Summary

Monthly Element Count

Monthly Element Balance

---

# 11. Stage 7 — Seasonal Analysis

Determine

Current Season

Current Solar Qi

Season Strength

Temperature

Humidity

Dryness

Generate

Seasonal Context

Seasonal Context SHALL be attached to Monthly Context.

---

# 12. Stage 8 — Relationship Analysis

Relationship Analysis is divided into

Natal Chart

Dayun

LiuNian

Monthly Stem

Monthly Branch

Hidden Stems

Every layer SHALL be evaluated independently.

---

# 13. Natal Relationship Analysis

Evaluate

Monthly Stem

↓

Natal Heavenly Stems

Monthly Branch

↓

Natal Earthly Branches

Hidden Stems

↓

Natal Hidden Stems

Store every detected interaction.

---

# 14. Dayun Relationship Analysis

Evaluate

Monthly Stem

↓

Dayun Stem

Monthly Branch

↓

Dayun Branch

Hidden Stems

↓

Dayun Hidden Stems

Generate

Dayun Interaction Context

---

# 15. LiuNian Relationship Analysis

Evaluate

Monthly Stem

↓

Annual Stem

Monthly Branch

↓

Annual Branch

Hidden Stems

↓

Annual Hidden Stems

Generate

LiuNian Interaction Context

---

# 16. Stem Interaction Analysis

Detect

Generation

Control

Combination

Transformation

Competition

Every detected interaction SHALL be preserved.

---

# 17. Branch Interaction Analysis

Detect

Six Harmony

Six Clash

Three Harmony

Three Meetings

Punishment

Harm

Destruction

Self Punishment

Transformation

Multiple interactions SHALL coexist.

---

# 18. Hidden Stem Analysis

Every Monthly Hidden Stem SHALL be compared against

Natal Hidden Stems

↓

Dayun Hidden Stems

↓

LiuNian Hidden Stems

↓

Monthly Heavenly Stem

Store every interaction independently.

---

# 19. Transformation Analysis

Evaluate

Stem Transformation

↓

Branch Transformation

↓

Hidden Stem Transformation

↓

Seasonal Requirements

↓

Transformation Success

Transformation SHALL only occur if every prerequisite is satisfied.

---

# 20. Priority Resolution

Load

Priority Database

Sort

Detected Events

Resolve

Priority Order

Store

Primary Events

Secondary Events

Suppressed Events

No event SHALL be discarded.

---

# 21. Monthly Context Construction

Generate

MonthlyContext

Containing

Monthly Pillar

Hidden Stems

Ten Gods

Element Summary

Seasonal Context

Natal Relations

Dayun Relations

LiuNian Relations

Combination Result

Clash Result

Transformation Result

Priority Events

Risk Flags

Metadata

Return immutable object.

---

# 22. Output Validation

Validate

Mandatory Fields

Required Metadata

Priority Order

Interaction Consistency

Transformation Consistency

Five Element Counts

Ten Gods

Return validated Monthly Context.

---

# 23. Performance Requirements

Average evaluation latency

<10 ms

Average complexity

O(n)

No recursive processing.

No duplicated calculations.

---

# 24. Error Handling

Every failure SHALL return

Error Code

Error Message

Processing Stage

Affected Object

Suggested Resolution

No partial output SHALL be returned.

---

# 25. Deterministic Guarantee

Identical

Natal Chart

Current Dayun

Current LiuNian

Gregorian Date

Solar Term Calendar

Rule Database

Priority Rules

shall always produce identical Monthly Context.

Random behavior is prohibited.

AI-generated decisions are prohibited.

---

# 26. Future Extension Points

Reserved for

LiuRi Module

LiuShi Module

Unified Fortune Timeline Engine

Cross-Month Interaction Engine

Event Prediction Engine

Batch Monthly Forecast Engine

End of Document