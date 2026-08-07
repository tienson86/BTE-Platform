# 02_RUNTIME_PIPELINE.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

This document defines the canonical runtime pipeline of the BaZi Engine.

It specifies:

- Runtime execution stages
- Builder sequence
- Aggregate construction
- Data flow
- Validation boundaries
- Error propagation

Every execution of the BaZi Engine must follow this pipeline.

---

# 2. Runtime Philosophy

The BaZi Engine is a deterministic structural engine.

It transforms a validated BirthContext into a canonical BaziChart.

The Engine constructs facts.

It never performs analysis.

It never produces interpretation.

It never generates reports.

---

# 3. Canonical Runtime Pipeline

BirthContext

↓

Input Validation

↓

Pillar Builder

↓

Hidden Stem Builder

↓

Na Yin Builder

↓

Growth Phase Builder

↓

Relationship Builder

↓

Five Element Builder

↓

Yin Yang Builder

↓

Aggregate Builder

↓

BaziChart Validation

↓

Result<BaziChart>

---

# 4. Runtime Overview

| Stage | Input | Output | Responsibility |
|--------|-------|--------|----------------|
| 01 | BirthContext | BirthContext | Input Validation |
| 02 | BirthContext | PillarChart | Four Pillars |
| 03 | PillarChart | HiddenStemChart | Hidden Stems |
| 04 | HiddenStemChart | NaYinChart | Na Yin |
| 05 | NaYinChart | GrowthChart | Twelve Growth Phases |
| 06 | GrowthChart | RelationshipChart | Heavenly Stem & Earthly Branch Relationships |
| 07 | RelationshipChart | FiveElementChart | Five Element Structure |
| 08 | FiveElementChart | YinYangChart | Yin / Yang Structure |
| 09 | All Components | BaziChart | Aggregate Builder |
| 10 | BaziChart | Result<BaziChart> | Final Validation |

---

# 5. Stage 01 — Input Validation

Input

BirthContext

Validate

- Required fields
- Ganzhi completeness
- Calendar consistency
- Metadata

Output

Validated BirthContext

Failure

Result.Error

---

# 6. Stage 02 — Pillar Builder

Consumes

BirthContext

Produces

PillarChart

Responsibilities

- Year Pillar
- Month Pillar
- Day Pillar
- Hour Pillar

No hidden stems.

No relationships.

---

# 7. Stage 03 — Hidden Stem Builder

Consumes

PillarChart

Produces

HiddenStemChart

Responsibilities

Resolve hidden stems for

- Year Branch
- Month Branch
- Day Branch
- Hour Branch

No Ten Gods.

No scoring.

---

# 8. Stage 04 — Na Yin Builder

Consumes

HiddenStemChart

Produces

NaYinChart

Responsibilities

Calculate

- Year Na Yin
- Month Na Yin
- Day Na Yin
- Hour Na Yin

No interpretation.

---

# 9. Stage 05 — Growth Phase Builder

Consumes

NaYinChart

Produces

GrowthChart

Responsibilities

Determine

- Trường Sinh
- Mộc Dục
- Quan Đới
- Lâm Quan
- Đế Vượng
- Suy
- Bệnh
- Tử
- Mộ
- Tuyệt
- Thai
- Dưỡng

No strength calculation.

---

# 10. Stage 06 — Relationship Builder

Consumes

GrowthChart

Produces

RelationshipChart

Responsibilities

Detect

Heavenly Stem

- Combination
- Clash
- Generation
- Control

Earthly Branch

- Six Combination
- Six Clash
- Three Harmony
- Three Meeting
- Punishment
- Harm
- Destruction
- Self Punishment
- Half Combination
- Hidden Combination

Store structure only.

---

# 11. Stage 07 — Five Element Builder

Consumes

RelationshipChart

Produces

FiveElementChart

Responsibilities

Calculate

- Wood
- Fire
- Earth
- Metal
- Water

Store

- Count
- Distribution

No strength evaluation.

---

# 12. Stage 08 — Yin Yang Builder

Consumes

FiveElementChart

Produces

YinYangChart

Responsibilities

Calculate

- Yin Count
- Yang Count
- Ratio

No interpretation.

---

# 13. Stage 09 — Aggregate Builder

Consumes

All structural components

Produces

BaziChart

Responsibilities

Assemble

- Metadata
- PillarChart
- HiddenStemChart
- RelationshipChart
- NaYinChart
- GrowthChart
- FiveElementChart
- YinYangChart

The Aggregate becomes immutable.

---

# 14. Stage 10 — Final Validation

Validate

BaziChart

Checks

- Aggregate completeness
- Required objects
- Internal consistency
- Duplicate detection

Output

Result<BaziChart>

---

# 15. Error Flow

BirthContext

↓

Validation

↓

❌ Error

↓

Result.Error

↓

Pipeline Stops

No partial chart is returned.

---

# 16. Success Flow

BirthContext

↓

Validation

↓

Builders

↓

Aggregate

↓

Validation

↓

Result<BaziChart>

---

# 17. Runtime Characteristics

The Engine must be

- Deterministic
- Stateless
- Immutable
- Thread-safe
- Repeatable

The same BirthContext always produces the same BaziChart.

---

# 18. Logging

Every stage records

- Start
- End
- Duration
- Warnings
- Errors

Sensitive personal data must never be logged.

---

# 19. Performance Targets

Single Chart

< 100 ms

100 Charts

< 1 second

1000 Charts

< 10 seconds

No external network dependency.

---

# 20. Downstream Contract

Only the completed BaziChart may leave the Engine.

Downstream Engines must never consume:

- PillarChart
- HiddenStemChart
- GrowthChart
- RelationshipChart

directly.

They consume only

BaziChart.

---

# 21. Runtime Diagram

BirthContext

↓

Validation

↓

Pillar Builder

↓

Hidden Stem Builder

↓

Na Yin Builder

↓

Growth Phase Builder

↓

Relationship Builder

↓

Five Element Builder

↓

Yin Yang Builder

↓

Aggregate Builder

↓

BaziChart

↓

Score Engine

---

# 22. Acceptance Criteria

The runtime pipeline is complete when:

✓ Every Builder has one responsibility

✓ Aggregate Root created successfully

✓ Runtime deterministic

✓ Thread-safe

✓ Unit tests pass

✓ Integration tests pass

✓ Golden Dataset verified

✓ Final Aggregate validated

---

END OF DOCUMENT