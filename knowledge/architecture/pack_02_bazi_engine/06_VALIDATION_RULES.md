# 06_VALIDATION_RULES.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

This document defines the canonical validation rules of the BaZi Engine.

Validation ensures that every BaziChart produced by the engine is structurally complete, internally consistent and suitable for downstream analysis.

Validation is performed before the BaziChart is released to the Score Engine.

---

# 2. Validation Philosophy

The BaZi Engine validates domain integrity.

It does not validate calendar calculations.

Those belong to the Calendar Engine.

The BaZi Engine validates only structural correctness.

---

# 3. Validation Pipeline

BirthContext

↓

Input Validation

↓

Builder Validation

↓

Aggregate Validation

↓

Relationship Validation

↓

Structural Validation

↓

Consistency Validation

↓

Final Validation

↓

Result<BaziChart>

Any failed validation terminates the pipeline.

---

# 4. Validation Categories

The BaZi Engine performs the following validation groups.

| Category | Responsibility |
|----------|----------------|
| Input | BirthContext integrity |
| Builder | Builder outputs |
| Aggregate | Aggregate completeness |
| Relationship | Structural relationships |
| Consistency | Cross-model consistency |
| Metadata | Runtime metadata |

---

# 5. Input Validation

Validate BirthContext.

Checks

✓ Calendar information exists

✓ Four Ganzhi exist

✓ Solar term exists

✓ Timezone exists

✓ Metadata exists

Failure

↓

Result.Error

---

# 6. Pillar Validation

Validate Four Pillars.

Checks

✓ Year Pillar

✓ Month Pillar

✓ Day Pillar

✓ Hour Pillar

Each Pillar must contain

- Heavenly Stem

- Earthly Branch

- Element

- Yin/Yang

Missing Pillars are not allowed.

---

# 7. Hidden Stem Validation

Validate HiddenStemChart.

Checks

✓ Every Branch has Hidden Stems

✓ Hidden Stem count matches knowledge database

✓ Priority values exist

✓ Duplicate stems prohibited

---

# 8. Na Yin Validation

Checks

✓ Every Pillar has Na Yin

✓ Na Yin mapping exists

✓ Element mapping exists

Invalid mappings terminate execution.

---

# 9. Growth Phase Validation

Checks

✓ Every Heavenly Stem has one Growth Phase

✓ Enumeration valid

✓ No duplicate Growth Phase objects

---

# 10. Relationship Validation

Validate

Heavenly Stem Relationships

Earthly Branch Relationships

Checks

✓ Members exist

✓ Relationship type valid

✓ No self-reference

✓ Transformation metadata complete

✓ Priority assigned

Relationship evidence must be complete.

---

# 11. Five Element Validation

Checks

✓ Wood

✓ Fire

✓ Earth

✓ Metal

✓ Water

Every element must exist.

Distribution totals must be internally consistent.

No negative values.

---

# 12. Yin Yang Validation

Checks

✓ Yin count

✓ Yang count

✓ Ratio

✓ Distribution

Values must match pillar data.

---

# 13. Aggregate Validation

Validate

BaziChart

Checks

✓ Metadata

✓ PillarChart

✓ HiddenStemChart

✓ RelationshipChart

✓ NaYinChart

✓ GrowthChart

✓ FiveElementChart

✓ YinYangChart

No missing Aggregate Members.

---

# 14. Cross-Model Consistency

Verify consistency across all domain models.

Examples

Pillar

↓

Hidden Stem

↓

Relationship

↓

Five Element

↓

Yin Yang

The same structural fact must never appear with conflicting values.

---

# 15. Structural Integrity

Verify

✓ Immutable Aggregate

✓ No circular references

✓ No orphan relationships

✓ No duplicated members

✓ No invalid references

The Aggregate must form one consistent graph.

---

# 16. Metadata Validation

Validate

✓ Engine Version

✓ Runtime Version

✓ Builder Trace

✓ Execution Time

✓ Warning Collection

Metadata is mandatory.

---

# 17. Warning Rules

Warnings allow execution to continue.

Examples

Unknown optional metadata

Deprecated lookup entry

Historical uncertainty

Warnings are attached to Result<BaziChart>.

---

# 18. Error Model

Possible errors

InputValidationError

BuilderValidationError

AggregateValidationError

RelationshipValidationError

ConsistencyError

MetadataError

InternalError

Every error contains

- code

- stage

- builder

- message

- timestamp

- trace_id

---

# 19. Validation Result

Validation returns

Result<BaziChart>

Possible states

SUCCESS

WARNING

ERROR

ERROR stops the runtime.

WARNING continues execution.

---

# 20. Logging

Validation logs

Stage

Builder

Duration

Warnings

Errors

Trace ID

No sensitive user information may appear in logs.

---

# 21. Acceptance Checklist

Validation is complete when

✓ BirthContext validated

✓ Four Pillars validated

✓ Hidden Stems validated

✓ Na Yin validated

✓ Growth Phases validated

✓ Relationships validated

✓ Five Elements validated

✓ Yin/Yang validated

✓ Aggregate validated

✓ Cross-model consistency verified

✓ Metadata validated

✓ Structured Result returned

---

END OF DOCUMENT