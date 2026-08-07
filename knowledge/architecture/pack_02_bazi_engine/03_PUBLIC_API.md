# 03_PUBLIC_API.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

This document defines the official Public API of the BaZi Engine.

The Public API is the only supported interface between the BaZi Engine and the rest of the BTE Platform.

All internal builders, calculators and repositories are private implementation details.

---

# 2. API Philosophy

The BaZi Engine exposes one public service only.

Consumers never invoke builders directly.

Consumers never construct BaziChart manually.

The BaZi Engine owns the complete structural construction process.

---

# 3. Public Service

Canonical Service

BaZiEngine

Responsibilities

- Validate BirthContext
- Execute Builder Pipeline
- Construct Aggregate Root
- Return canonical BaziChart

---

# 4. Public Interface

BaZiEngine.run(
    context: BirthContext
)

↓

Result<BaziChart>

This is the only supported public entry point.

---

# 5. Input Contract

Input

BirthContext

Produced only by

Calendar Engine

BirthContext must already be validated.

The BaZi Engine never accepts

- raw JSON
- dictionaries
- anonymous objects

Only canonical BirthContext.

---

# 6. Output Contract

Output

Result<BaziChart>

Success

↓

BaziChart

Failure

↓

Structured Error

The Engine never returns partially constructed charts.

---

# 7. Result Model

Result<T>

contains

success

value

error

warnings

metadata

Result is immutable.

Null is never returned.

---

# 8. Public Model

The only public output model is

BaziChart

The Aggregate contains

- Metadata
- PillarChart
- HiddenStemChart
- RelationshipChart
- NaYinChart
- GrowthChart
- FiveElementChart
- YinYangChart

No downstream Engine may modify these values.

---

# 9. Internal API

The following services are private.

InputValidator

PillarBuilder

HiddenStemBuilder

NaYinBuilder

GrowthPhaseBuilder

RelationshipBuilder

FiveElementBuilder

YinYangBuilder

AggregateBuilder

ChartValidator

These services are implementation details.

They are never exposed outside the BaZi Engine.

---

# 10. Dependency Rules

Allowed

BirthContext

Utilities

Knowledge Database

Calendar Engine Output

Forbidden

Score Engine

Interpretation Engine

Report Engine

Desktop UI

Mobile UI

Tablet UI

The BaZi Engine never communicates directly with downstream Engines.

---

# 11. Runtime Ownership

The BaZi Engine owns

- Pillar construction
- Hidden Stem construction
- Na Yin construction
- Growth Phase construction
- Structural relationship construction
- Five Element distribution
- Yin / Yang distribution

No downstream Engine recalculates structural information.

---

# 12. Error Model

Errors include

ValidationError

BuilderError

RelationshipError

KnowledgeBaseError

AggregateError

InternalError

Every error contains

- code
- stage
- message
- timestamp
- engine_version

---

# 13. Warning Model

Warnings do not stop execution.

Examples

- uncommon historical calendar

- incomplete optional metadata

- deprecated lookup table

Warnings are included inside

Result<BaziChart>

---

# 14. Thread Safety

Every execution is independent.

No global mutable state.

Safe for parallel execution.

---

# 15. Performance

Target

Single chart

<100 ms

100 charts

<1 second

1000 charts

<10 seconds

No external network dependency.

---

# 16. Semantic Versioning

Public API follows

Semantic Versioning

Major

Breaking API changes

Minor

Backward-compatible additions

Patch

Bug fixes

Breaking changes require Architecture Review.

---

# 17. Integration Example

BirthContext

↓

BaZiEngine.run()

↓

Result<BaziChart>

↓

ScoreEngine.run()

↓

Result<AnalysisResult>

The BaZi Engine never invokes downstream Engines.

---

# 18. Extension Rules

Future builders may be added.

Examples

QiDistributionBuilder

SeasonContextBuilder

DynamicBranchBuilder

Extensions must remain internal.

Public API remains unchanged.

---

# 19. API Stability

The Public API is considered stable when

- Input remains BirthContext
- Output remains Result<BaziChart>

Internal implementation may evolve freely.

Consumers must never depend on internal classes.

---

# 20. Acceptance Criteria

The Public API is complete when

✓ One public service

✓ One public entry point

✓ One canonical input

✓ One canonical output

✓ Aggregate Root returned

✓ Internal Builders hidden

✓ Strong typing enforced

✓ Thread-safe

✓ Fully documented

---

END OF DOCUMENT