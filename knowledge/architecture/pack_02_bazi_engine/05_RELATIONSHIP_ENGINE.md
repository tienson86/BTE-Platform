# 05_RELATIONSHIP_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 02

Engine: BaZi Engine

Component: Relationship Engine

---

# 1. Purpose

The Relationship Engine detects and normalizes all structural relationships inside a BaZi chart.

Its responsibility is to identify factual interactions between Heavenly Stems and Earthly Branches.

The Relationship Engine never performs analysis, scoring or interpretation.

---

# 2. Position in Runtime

BirthContext

↓

BaZi Engine

↓

Relationship Engine

↓

RelationshipChart

↓

BaziChart

↓

Score Engine

---

# 3. Relationship Philosophy

The Relationship Engine produces facts.

Examples

✓ Jia combines with Ji

✓ Yin clashes with Shen

✓ Hai harms Si

✓ Yin belongs to Three Harmony Fire Group

The engine never determines whether these relationships are favorable or unfavorable.

---

# 4. Runtime Flow

PillarChart

↓

Stem Relationship Detector

↓

Branch Relationship Detector

↓

Special Relationship Detector

↓

Transformation Checker

↓

Relationship Normalizer

↓

RelationshipChart

---

# 5. Relationship Categories

The Relationship Engine detects five major categories.

| Category | Description |
|----------|-------------|
| Heavenly Stem | Thiên Can |
| Earthly Branch | Địa Chi |
| Seasonal | Seasonal interactions |
| Structural | Structural combinations |
| Special | Advanced structural rules |

---

# 6. Heavenly Stem Relationships

Supported relationships

- Combination (Hợp)
- Clash (Xung)
- Generate (Sinh)
- Control (Khắc)
- Drain (Tiết)
- Consume (Hao)
- Peer (Tỷ)

Each detected relationship records

- Source Stem
- Target Stem
- Relationship Type
- Direction
- Priority

No interpretation.

---

# 7. Earthly Branch Relationships

Supported relationships

- Six Combination (Lục Hợp)
- Six Clash (Lục Xung)
- Three Harmony (Tam Hợp)
- Three Meeting (Tam Hội)
- Punishment (Hình)
- Harm (Hại)
- Destruction (Phá)
- Self Punishment (Tự Hình)
- Half Combination (Bán Hợp)
- Half Meeting (Bán Hội)
- Hidden Combination (Ám Hợp)

Each relationship stores

- Source Branch
- Target Branch
- Type
- Priority
- Required Members
- Completed Members

---

# 8. Transformation Rules

Relationship Engine verifies whether a combination transforms successfully.

Examples

- Stem Combination Transformation
- Branch Combination Transformation
- Three Harmony Transformation
- Three Meeting Transformation

The engine records

- Possible
- Completed
- Failed

No qualitative judgment is made.

---

# 9. Seasonal Influence

The engine records structural seasonal context.

Examples

- Current Season
- Dominant Element
- Seasonal Support

These values are structural inputs only.

No strength analysis.

---

# 10. Structural Priority

Relationships may overlap.

Priority determines normalization order.

Example

Transformation

↓

Combination

↓

Clash

↓

Punishment

↓

Harm

↓

Destruction

Priority values are structural only.

Business meaning belongs to the Score Engine.

---

# 11. Relationship Model

Every relationship contains

| Field | Description |
|--------|-------------|
| id | Unique identifier |
| category | Stem / Branch / Special |
| type | Relationship type |
| source | Source object |
| target | Target object |
| members | Participating pillars |
| completed | Boolean |
| transformed | Boolean |
| priority | Resolution order |
| metadata | Additional information |

---

# 12. RelationshipChart

RelationshipChart contains

Stem Relationships

Branch Relationships

Transformation Results

Seasonal Context

Normalization Metadata

RelationshipChart is immutable.

---

# 13. Conflict Resolution

When multiple relationships coexist

Normalization rules apply.

The engine records

- Applied
- Ignored
- Deferred

No relationship is deleted.

All detected relationships remain traceable.

---

# 14. Validation

RelationshipChart validates

- Duplicate relationships
- Invalid members
- Circular references
- Missing dependencies

Invalid charts return

Result.Error

---

# 15. Performance

Target

Single chart

<20 ms

Relationship detection must not require external services.

---

# 16. Thread Safety

Relationship Engine is

- Stateless
- Deterministic
- Thread-safe

Identical inputs always produce identical outputs.

---

# 17. Downstream Contract

Score Engine consumes RelationshipChart.

Interpretation Engine consumes normalized relationship data.

Neither Engine recalculates structural relationships.

RelationshipChart is the single source of truth.

---

# 18. Extension Rules

Future relationship types may be added.

Examples

- Hidden Relationships
- School-specific Relationships
- Regional Variants

Existing relationship types remain backward compatible.

---

# 19. Acceptance Criteria

The Relationship Engine is complete when

✓ Heavenly Stem relationships detected

✓ Earthly Branch relationships detected

✓ Transformation rules applied

✓ Relationship normalization completed

✓ RelationshipChart validated

✓ Unit Tests pass

✓ Golden Dataset verified

✓ Documentation approved

---

END OF DOCUMENT