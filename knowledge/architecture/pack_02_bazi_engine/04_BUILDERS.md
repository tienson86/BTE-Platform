# 04_BUILDERS.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

This document defines the Builder Framework used by the BaZi Engine.

Builders are responsible for constructing the canonical BaziChart.

Every Builder has one responsibility.

Builders never perform analysis.

Builders never generate interpretation.

Builders never produce reports.

---

# 2. Builder Philosophy

The BaZi Engine follows the Builder Pipeline pattern.

BirthContext

↓

Builder 01

↓

Builder 02

↓

Builder 03

↓

...

↓

Aggregate Root

Each Builder enriches the Aggregate.

Builders never modify previous Builder logic.

---

# 3. Builder Rules

Every Builder must satisfy:

✓ Stateless

✓ Deterministic

✓ Thread Safe

✓ Single Responsibility

✓ Immutable Output

Builders communicate only through the Aggregate.

Builders never call downstream Engines.

---

# 4. Builder Registry

The BaZi Engine contains the following canonical Builders.

01

PillarBuilder

02

HiddenStemBuilder

03

NaYinBuilder

04

GrowthPhaseBuilder

05

RelationshipBuilder

06

FiveElementBuilder

07

YinYangBuilder

08

MetadataBuilder

09

AggregateBuilder

Execution order is fixed.

---

# 5. Builder Lifecycle

Each Builder follows the same lifecycle.

Input

↓

Validate

↓

Build

↓

Verify

↓

Return Result

Every Builder returns

Result<T>

No Builder throws business exceptions.

---

# 6. Base Builder Contract

Every Builder implements the same contract.

Builder<Input, Output>

Required methods

validate()

build()

verify()

run()

The default execution path is

validate

↓

build

↓

verify

↓

Result

---

# 7. Builder Context

Builders receive

BuilderContext

BuilderContext contains

BirthContext

Current Aggregate

Metadata

Logger

Warnings

Execution State

Builders never communicate directly.

They use BuilderContext.

---

# 8. Builder 01

PillarBuilder

Consumes

BirthContext

Produces

PillarChart

Responsibilities

- Year Pillar
- Month Pillar
- Day Pillar
- Hour Pillar

No Hidden Stem.

No Relationships.

---

# 9. Builder 02

HiddenStemBuilder

Consumes

PillarChart

Produces

HiddenStemChart

Responsibilities

Resolve hidden stems

for every Earthly Branch.

No Ten Gods.

No Scoring.

---

# 10. Builder 03

NaYinBuilder

Consumes

HiddenStemChart

Produces

NaYinChart

Responsibilities

Calculate

Year Na Yin

Month Na Yin

Day Na Yin

Hour Na Yin

---

# 11. Builder 04

GrowthPhaseBuilder

Consumes

NaYinChart

Produces

GrowthChart

Responsibilities

Determine

Trường Sinh

Mộc Dục

Quan Đới

Lâm Quan

Đế Vượng

Suy

Bệnh

Tử

Mộ

Tuyệt

Thai

Dưỡng

---

# 12. Builder 05

RelationshipBuilder

Consumes

GrowthChart

Produces

RelationshipChart

Responsibilities

Detect Heavenly Stem relationships

Detect Earthly Branch relationships

Detect structural interactions

Store structure only.

---

# 13. Builder 06

FiveElementBuilder

Consumes

RelationshipChart

Produces

FiveElementChart

Responsibilities

Build

Wood

Fire

Earth

Metal

Water

Distribution

Count

Percentage

No scoring.

---

# 14. Builder 07

YinYangBuilder

Consumes

FiveElementChart

Produces

YinYangChart

Responsibilities

Calculate

Yin

Yang

Ratio

Distribution

---

# 15. Builder 08

MetadataBuilder

Responsibilities

Runtime Metadata

Version

Warnings

Execution Time

Builder Trace

Engine Version

---

# 16. Builder 09

AggregateBuilder

Consumes

Every previous Builder output.

Produces

Canonical

BaziChart

AggregateBuilder performs no calculations.

It assembles.

---

# 17. Builder Execution Order

BirthContext

↓

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

YinYangBuilder

↓

MetadataBuilder

↓

AggregateBuilder

↓

BaziChart

Execution order is immutable.

---

# 18. Error Handling

Every Builder returns

Result<T>

Possible outcomes

Success

Warning

Error

Errors stop the Builder Pipeline.

Warnings continue execution.

---

# 19. Logging

Every Builder records

Start

Finish

Duration

Warnings

Errors

Builder Name

Execution Order

Logs are used for debugging only.

---

# 20. Performance

Every Builder should execute independently.

Target

<10 ms

per Builder.

Entire BaZi Engine

<100 ms.

---

# 21. Builder Independence

Builders must never:

Call another Builder

Modify previous Builder output

Perform interpretation

Perform scoring

Access UI

Access Report Engine

Builders only enrich the Aggregate.

---

# 22. Extension Rules

Future Builders may be added.

Examples

SeasonContextBuilder

QiDistributionBuilder

VoidBranchBuilder

SpecialPatternBuilder

Extensions must preserve Builder order.

---

# 23. Acceptance Criteria

Builder Framework is complete when

✓ Every Builder has one responsibility

✓ Builder order is fixed

✓ BuilderContext implemented

✓ AggregateBuilder finalizes the chart

✓ Unit Tests pass

✓ Integration Tests pass

✓ Runtime deterministic

✓ Documentation approved

---

END OF DOCUMENT