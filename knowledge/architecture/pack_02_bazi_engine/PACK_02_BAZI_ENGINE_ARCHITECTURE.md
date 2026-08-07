# PACK_02_BAZI_ENGINE_ARCHITECTURE

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

The BaZi Engine is responsible for constructing the canonical BaZi chart from a validated BirthContext.

It transforms calendar information into a complete structural representation of a person's Four Pillars.

The BaZi Engine does not perform scoring, interpretation or report generation.

Its responsibility ends when the canonical BaziChart has been successfully constructed.

---

# 2. Position in the BTE Architecture

Runtime Pipeline

BirthRequest

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

BaziChart

↓

Score Engine

↓

AnalysisResult

↓

Interpretation Engine

↓

InterpretationResult

↓

Report Engine

↓

ReportResult

The BaZi Engine always consumes BirthContext.

The BaZi Engine always produces BaziChart.

---

# 3. Engine Responsibilities

The BaZi Engine is responsible for:

✓ Four Pillars construction

✓ Heavenly Stem construction

✓ Earthly Branch construction

✓ Hidden Stem calculation

✓ Na Yin calculation

✓ Twelve Growth Phase calculation

✓ Relationship detection

✓ Yin / Yang determination

✓ Five Elements structure

✓ Canonical BaZiChart construction

The BaZi Engine is NOT responsible for:

✗ Strength analysis

✗ Pattern determination

✗ Useful God selection

✗ Score calculation

✗ Interpretation

✗ Report rendering

---

# 4. Domain Philosophy

The BaZi Engine models the structural domain of BaZi.

It produces facts.

It never produces opinions.

Example

"Day Master = Canh Metal"

↓

Fact

"Day Master is weak"

↓

Analysis

(Not part of BaZi Engine)

This separation is mandatory.

---

# 5. Canonical Runtime

BirthContext

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

Five Elements Builder

↓

BaziChart Builder

↓

BaziChart

Each Builder has a single responsibility.

---

# 6. Canonical Domain Objects

The BaZi Engine produces one Aggregate Root.

BaziChart

The Aggregate contains:

PillarChart

HiddenStemChart

NaYinChart

GrowthChart

RelationshipChart

FiveElementChart

Metadata

Each object has one responsibility.

---

# 7. Builder Architecture

The Engine consists of independent builders.

PillarBuilder

↓

HiddenStemBuilder

↓

NaYinBuilder

↓

GrowthPhaseBuilder

↓

RelationshipBuilder

↓

FiveElementBuilder

↓

BaziChartBuilder

Builders never call downstream Engines.

Builders never perform scoring.

Builders never generate text.

---

# 8. Runtime Characteristics

The Engine must be:

- Deterministic
- Stateless
- Immutable
- Thread-safe
- Repeatable

The same BirthContext always produces the same BaziChart.

---

# 9. Public Contract

Input

BirthContext

Output

Result<BaziChart>

No additional public outputs are allowed.

No downstream Engine may modify BaziChart.

---

# 10. Integration Rules

Allowed Dependency

Calendar Engine Output

↓

BirthContext

Forbidden Dependency

Score Engine

Interpretation Engine

Report Engine

UI

The BaZi Engine must remain completely independent.

---

# 11. Domain Boundaries

The BaZi Engine defines structure only.

The following belong to later Engines.

Strength

Pattern

Useful God

Favorable Elements

Unfavorable Elements

Career Analysis

Marriage Analysis

Health Analysis

Luck Analysis

Report Sections

This separation must never be violated.

---

# 12. Canonical Aggregate

BaziChart is the Aggregate Root.

Every downstream Engine reads information from the Aggregate.

Downstream Engines must never reconstruct BaZi data independently.

The Aggregate is immutable after construction.

---

# 13. Error Handling

Every execution returns

Result<BaziChart>

Possible results

Success

↓

BaziChart

Failure

↓

Structured Error

The Engine never returns partial charts.

---

# 14. Performance Targets

Single Chart

< 100 ms

100 Charts

< 1 second

1000 Charts

< 10 seconds

No network dependency.

---

# 15. Versioning

Major

Breaking domain model changes.

Minor

Backward compatible additions.

Patch

Bug fixes.

BaziChart compatibility must be preserved whenever possible.

---

# 16. Documentation Structure

The BaZi Engine documentation consists of:

PACK_02_BAZI_ENGINE_ARCHITECTURE.md

01_DATA_MODEL.md

02_RUNTIME_PIPELINE.md

03_PUBLIC_API.md

04_BUILDERS.md

05_RELATIONSHIP_ENGINE.md

06_VALIDATION_RULES.md

07_TEST_STRATEGY.md

08_ACCEPTANCE_CHECKLIST.md

---

# 17. Acceptance Criteria

The BaZi Engine architecture is complete when:

✓ Domain boundaries are defined

✓ Runtime pipeline is defined

✓ Aggregate Root is defined

✓ Builder architecture is defined

✓ Public API is defined

✓ Integration rules are defined

✓ Downstream contracts are defined

✓ Documentation approved

---

# 18. Long-Term Vision

The BaZi Engine is designed to become the canonical structural engine of the BTE Platform.

Future analytical engines—including Strength Engine, Pattern Engine, Useful God Engine, Score Engine, Interpretation Engine and AI Advisory Engine—must consume the canonical BaziChart without rebuilding structural information.

The BaZi Engine is therefore the single source of truth for all BaZi structural data.

---

END OF DOCUMENT