# 01_DATA_MODEL.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

---

# 1. Purpose

This document defines the canonical data model of the BaZi Engine.

The BaZi Engine exposes one canonical output model:

BaziChart

BaziChart is the Aggregate Root of the BaZi domain.

All downstream Engines consume this Aggregate.

---

# 2. Design Principles

The BaZi data model follows these principles.

- Immutable
- Strongly Typed
- Canonical
- Versioned
- Serializable
- Domain Driven
- Aggregate Root

Every structural fact of the BaZi chart exists exactly once.

---

# 3. Canonical Input

Input

BirthContext

Produced by

Calendar Engine

BirthContext is immutable.

The BaZi Engine never modifies BirthContext.

---

# 4. Canonical Output

Output

BaziChart

BaziChart is immutable.

It becomes the single source of truth for every downstream Engine.

---

# 5. Aggregate Root

BaziChart

contains

Metadata

PillarChart

HiddenStemChart

RelationshipChart

NaYinChart

GrowthChart

FiveElementChart

YinYangChart

ChartMetadata

---

# 6. Metadata

| Field | Type | Description |
|--------|------|-------------|
| chart_id | UUID | Unique chart identifier |
| request_id | UUID | Original request |
| version | string | Schema version |
| engine_version | string | BaZi Engine version |
| generated_at | datetime | Chart creation time |

---

# 7. PillarChart

Contains the Four Pillars.

Year Pillar

Month Pillar

Day Pillar

Hour Pillar

Each pillar is represented by the same canonical model.

---

# 8. Pillar

Every pillar contains

Heavenly Stem

Earthly Branch

Stem Element

Branch Element

Stem YinYang

Branch YinYang

Display Name

Sequence

Example

Year

↓

Bính

↓

Dần

---

# 9. HiddenStemChart

Contains hidden stems for every branch.

Year Branch

↓

Hidden Stems

Month Branch

↓

Hidden Stems

Day Branch

↓

Hidden Stems

Hour Branch

↓

Hidden Stems

Each hidden stem stores

Stem

Element

Strength

Priority

---

# 10. RelationshipChart

Contains all structural relationships.

Heavenly Stem

- Combination
- Clash
- Generation
- Control

Earthly Branch

- Six Combination
- Six Clash
- Harm
- Punishment
- Destruction
- Self Punishment
- Three Harmony
- Three Meeting
- Half Combination
- Hidden Combination

RelationshipChart stores structure only.

No interpretation.

---

# 11. NaYinChart

Contains

Year NaYin

Month NaYin

Day NaYin

Hour NaYin

Each item includes

Name

Element

Description Code

---

# 12. GrowthChart

Contains the Twelve Growth Phases.

Every Heavenly Stem receives one Growth Phase.

Examples

Birth

Bath

Prosperity

Peak

Decline

Death

Storage

Each value is stored as an enumeration.

---

# 13. FiveElementChart

Contains elemental distribution.

Wood

Fire

Earth

Metal

Water

Stores

Count

Percentage

Distribution

No scoring.

---

# 14. YinYangChart

Contains

Yin Count

Yang Count

Ratio

Distribution

No interpretation.

---

# 15. ChartMetadata

Contains runtime information.

Calculation Source

Warnings

Validation Status

Confidence

Runtime Duration

---

# 16. Model Relationships

BirthContext

↓

BaZi Engine

↓

PillarChart

↓

HiddenStemChart

↓

RelationshipChart

↓

NaYinChart

↓

GrowthChart

↓

FiveElementChart

↓

YinYangChart

↓

BaziChart

---

# 17. Serialization

Every model supports

JSON

YAML

MessagePack

Future binary serialization must preserve compatibility.

---

# 18. Versioning

Major

Breaking model changes.

Minor

Backward compatible additions.

Patch

Documentation and bug fixes.

Aggregate compatibility must be preserved.

---

# 19. Extension Rules

New Aggregate Members

may be added.

Existing members

must not change meaning.

Existing property names

must remain stable.

Field removal requires a major version.

---

# 20. Downstream Contract

The following Engines consume

BaziChart

Score Engine

Interpretation Engine

Report Engine

No downstream Engine reconstructs

Pillars

Hidden Stems

Relationships

NaYin

Growth Phases

Five Elements

Yin Yang

The BaZi Engine is the canonical source.

---

# 21. Canonical Aggregate Diagram

BirthContext

↓

BaZi Engine

↓

+---------------------------+
|        BaziChart          |
|---------------------------|
| Metadata                  |
| PillarChart               |
| HiddenStemChart           |
| RelationshipChart         |
| NaYinChart                |
| GrowthChart               |
| FiveElementChart          |
| YinYangChart              |
| ChartMetadata             |
+---------------------------+

↓

Score Engine

↓

Interpretation Engine

↓

Report Engine

---

# 22. Source of Truth

The BaziChart Aggregate is the only structural representation of a BaZi chart within the BTE Platform.

Every downstream Engine must consume the Aggregate.

No Engine may reconstruct structural BaZi information independently.

---

END OF DOCUMENT