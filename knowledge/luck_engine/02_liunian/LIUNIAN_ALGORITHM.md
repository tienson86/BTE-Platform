# LIUNIAN ALGORITHM

Version: 1.0

Status: Stable

Module:
02_liunian

---

# 1. Purpose

This document defines the deterministic algorithm used to generate and evaluate
the Annual Luck (LiuNian) context.

The algorithm produces a structured Annual Context without performing any
natural language interpretation.

---

# 2. Overview

Input

↓

Validate Input

↓

Determine Annual Pillar

↓

Generate Hidden Stems

↓

Calculate Ten Gods

↓

Evaluate Five Elements

↓

Evaluate Stem Relations

↓

Evaluate Branch Relations

↓

Evaluate Hidden Stem Relations

↓

Evaluate Dayun Relations

↓

Evaluate Special Rules

↓

Resolve Priorities

↓

Generate Annual Context

↓

Validate Output

↓

Return Result

---

# 3. Processing Pipeline

Stage 1

Input Validation

Stage 2

Annual Pillar Generation

Stage 3

Hidden Stem Expansion

Stage 4

Ten Gods Calculation

Stage 5

Five Element Mapping

Stage 6

Stem Interaction Detection

Stage 7

Branch Interaction Detection

Stage 8

Hidden Stem Interaction

Stage 9

Dayun Interaction

Stage 10

Special Rule Detection

Stage 11

Priority Resolution

Stage 12

Annual Context Construction

---

# 4. Stage 1 — Input Validation

Validate:

• Natal Chart

• Day Master

• Current Gregorian Year

• Solar Term Calendar

• Dayun Context

• Rule Database

Reject processing if any mandatory object is missing.

---

# 5. Stage 2 — Annual Pillar Generation

Input

Gregorian Year

↓

Locate Li Chun

↓

Determine Effective Solar Year

↓

Generate Heavenly Stem

↓

Generate Earthly Branch

↓

Annual Pillar

Annual Pillar SHALL always be based on the Solar Calendar.

---

# 6. Stage 3 — Hidden Stem Expansion

Retrieve Hidden Stems from the Branch Database.

Example

Yin

甲

丙

戊

Store

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

Maintain canonical ordering.

---

# 7. Stage 4 — Ten Gods Calculation

Reference

Day Master

↓

Annual Stem

↓

Hidden Stems

Each stem receives an independent Ten God.

---

# 8. Stage 5 — Five Element Mapping

Map

Stem → Element

Branch → Dominant Element

Hidden Stem → Element

Compute

Element Counts

Element Balance

Element Strength

---

# 9. Stage 6 — Stem Interaction Detection

Evaluate:

Generation

Control

Combination

Transformation

Competition

Store every detected interaction.

---

# 10. Stage 7 — Branch Interaction Detection

Evaluate

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

# 11. Stage 8 — Hidden Stem Interaction

Compare Hidden Stems against

Natal Hidden Stems

Natal Stems

Annual Stem

Dayun Stem

Store all detected relationships.

---

# 12. Stage 9 — Dayun Interaction

Evaluate

Annual Stem

↓

Dayun Stem

Annual Branch

↓

Dayun Branch

Hidden Stem

↓

Dayun Hidden Stem

Generate Dayun Interaction Context.

---

# 13. Stage 10 — Special Rule Detection

Evaluate

Fu Yin

Fan Yin

Tai Sui

Kong Wang

Heavenly Virtue

Monthly Virtue

Peach Blossom

Traveling Horse

All detected events are stored independently.

---

# 14. Stage 11 — Priority Resolution

Load Priority Rules.

Apply rule precedence.

If multiple rules conflict

↓

Higher Priority wins

↓

Lower Priority preserved as metadata

No information is discarded.

---

# 15. Stage 12 — Annual Context Construction

Construct

AnnualContext

Containing

Annual Pillar

Hidden Stems

Ten Gods

Element Summary

Interaction Summary

Transformation Summary

Priority Events

Risk Flags

Metadata

Return immutable object.

---

# 16. Output Validation

Verify

No missing fields

No duplicated identifiers

Valid Priority Order

Valid Metadata

Consistent Element Counts

Consistent Ten Gods

Return validated Annual Context.

---

# 17. Performance Requirements

Target latency

<10 ms

Average complexity

O(n)

No recursive processing.

---

# 18. Error Handling

Return structured errors only.

No partial output.

Every failure shall include

Error Code

Message

Source Stage

Suggested Resolution

---

# 19. Determinism

Identical input SHALL always produce identical output.

No random behavior.

No AI dependency.

---

# 20. Future Extension Points

Reserved for

LiuYue

LiuRi

LiuShi

Unified Fortune Engine

Multi-Year Forecast Engine

Cross-Year Event Prediction