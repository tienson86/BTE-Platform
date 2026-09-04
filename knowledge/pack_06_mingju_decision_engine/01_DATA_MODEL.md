# MC-01 — DATA MODEL

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `01_DATA_MODEL.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the canonical data model for MC-01 — Mệnh Cục Decision Engine.

The model must support:

- deterministic inference
- explainable decisions
- structured evidence
- rule traceability
- unresolved states
- conflicting evidence
- future scoring
- runtime serialization
- report/UI consumption
- golden-case testing

This contract is the foundation for:

- Purity analysis
- Pattern Strength analysis
- Support analysis
- Damage analysis
- Rescue analysis
- Structural Integrity
- Pattern Grade
- Achievement models
- Wealth model
- Authority model
- Career model
- Decision Composer

No MC-01 runtime rule should introduce arbitrary output shapes outside this contract.

---

# 2. DESIGN PRINCIPLES

The MC-01 data model follows these principles:

```text
Facts
→ Evidence
→ Findings
→ Scores
→ Decisions
→ Customer interpretation
Đường dẫn:
knowledge/pack_06_mingju_decision_engine/01_DATA_MODEL.md
Bạn có thể dùng nguyên nội dung dưới đây.
# MC-01 — DATA MODEL

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `01_DATA_MODEL.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the canonical data model for MC-01 — Mệnh Cục Decision Engine.

The model must support:

- deterministic inference
- explainable decisions
- structured evidence
- rule traceability
- unresolved states
- conflicting evidence
- future scoring
- runtime serialization
- report/UI consumption
- golden-case testing

This contract is the foundation for:

- Purity analysis
- Pattern Strength analysis
- Support analysis
- Damage analysis
- Rescue analysis
- Structural Integrity
- Pattern Grade
- Achievement models
- Wealth model
- Authority model
- Career model
- Decision Composer

No MC-01 runtime rule should introduce arbitrary output shapes outside this contract.

---

# 2. DESIGN PRINCIPLES

The MC-01 data model follows these principles:

```text
Facts
→ Evidence
→ Findings
→ Scores
→ Decisions
→ Customer interpretation
Strict separation must remain between:
upstream facts
and:
MC-01 derived findings
MC-01 must never silently rewrite upstream canonical facts.
3. SCHEMA VERSION
Canonical schema version:
bte.mingju.decision.v1
Ruleset version:
bte.mingju.rules.v1
Composer version:
bte.mingju.composer.v1
Every MingJuDecisionResult MUST expose its schema and ruleset versions.
4. ROOT RESULT MODEL
Canonical conceptual result:
MingJuDecisionResult
Fields:
schema_version
ruleset_version
status
context
pattern
purity
pattern_strength
support
damage
rescue
useful_god_compatibility
climate_compatibility
integrity
grade
achievement
decision
confidence
warnings
trace
Initial Phase 1 implementation may leave downstream fields unresolved.
5. RESULT STATUS
Enum:
MingJuDecisionStatus
Allowed values:
complete
partial
unresolved
insufficient_evidence
invalid_input
Meaning:
complete
All mandatory structural stages completed.
partial
Some structural stages completed but one or more optional stages unavailable.
unresolved
Evidence exists but structural conclusion cannot yet be resolved.
insufficient_evidence
Required upstream facts are missing.
invalid_input
Canonical upstream data violates required contract.
6. ANALYSIS STATE ENUM
Reusable enum:
AnalysisState
Values:
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
This enum should be reusable across submodules.
7. SCORE MODEL
Generic score object:
ScoreResult
Fields:
score
minimum
maximum
normalized
state
confidence
evidence_ids
Recommended canonical scale:
0..100
Example:
{
  "score": 82.0,
  "minimum": 0.0,
  "maximum": 100.0,
  "normalized": 0.82,
  "state": "resolved",
  "confidence": 0.91,
  "evidence_ids": [
    "E-MC-001",
    "E-MC-002"
  ]
}
Important:
score and confidence are different concepts.
8. CONFIDENCE MODEL
Generic confidence:
0.0 .. 1.0
Confidence may be influenced by:
- upstream completeness
- pattern confidence
- missing hour pillar
- unresolved transformations
- conflicting rules
- weak evidence coverage
Conceptual model:
ConfidenceResult
Fields:
value
state
factors
Example:
{
  "value": 0.73,
  "state": "partially_resolved",
  "factors": [
    "pattern_confidence_medium",
    "branch_transformation_unresolved"
  ]
}
9. EVIDENCE MODEL
All significant findings require structured evidence.
Canonical object:
MingJuEvidence
Fields:
evidence_id
evidence_type
source_module
source_path
subject
predicate
object
value
polarity
strength
confidence
metadata
10. EVIDENCE TYPE
Enum:
EvidenceType
Initial values:
upstream_fact
derived_fact
relation
rule_match
support
damage
rescue
compatibility
conflict
exception
11. EVIDENCE POLARITY
Enum:
EvidencePolarity
Values:
positive
negative
neutral
mixed
Example:
{
  "evidence_id": "E-MC-001",
  "evidence_type": "upstream_fact",
  "source_module": "pattern_engine",
  "source_path": "pattern.main_pattern",
  "subject": "main_pattern",
  "predicate": "equals",
  "object": "zheng_guan",
  "value": "zheng_guan",
  "polarity": "neutral",
  "strength": 1.0,
  "confidence": 0.96
}
12. EVIDENCE STRENGTH
Evidence strength:
0.0 .. 1.0
This represents the structural importance of an evidence item.
It is NOT automatically a score weight.
Example:
month command support
may have strong structural evidence.
But its numerical contribution must still be defined by the rule system.
13. RULE MATCH RECORD
Every matched rule must produce a traceable record.
Object:
RuleMatch
Fields:
rule_id
rule_version
domain
priority
matched
conditions
evidence_ids
effects
exceptions_triggered
confidence
Example:
{
  "rule_id": "MC-DAMAGE-GUAN-001",
  "rule_version": "1.0",
  "domain": "damage",
  "priority": 100,
  "matched": true,
  "conditions": [
    "main_pattern == zheng_guan",
    "hurting_officer_exposed == true"
  ],
  "evidence_ids": [
    "E-MC-102",
    "E-MC-103"
  ],
  "effects": [
    "register_damage:hurt_officer_attacks_officer"
  ],
  "exceptions_triggered": [],
  "confidence": 0.91
}
14. TRACE EVENT
Canonical trace object:
MingJuTraceEvent
Fields:
trace_id
stage
sequence
rule_id
input_evidence_ids
output_ids
action
result
notes
Stages:
context
pattern
purity
pattern_strength
support
damage
rescue
compatibility
climate
integrity
grade
achievement
composer
Trace must preserve execution order.
15. MC CONTEXT
Root input adapter for MC-01:
MingJuContext
MC-01 SHOULD consume one normalized context instead of directly reading many unrelated engine payloads.
Conceptual fields:
chart
five_elements
ten_gods
strength
temperature
pattern
useful_god
relations
metadata
16. CHART CONTEXT
Object:
ChartContext
Fields:
day_master
year_pillar
month_pillar
day_pillar
hour_pillar
heavenly_stems
earthly_branches
hidden_stems
month_command
season
MC-01 must consume these facts, not recompute calendar rules.
17. PATTERN INPUT CONTEXT
Object:
PatternInputContext
Fields:
main_pattern
secondary_patterns
special_pattern
follow_pattern
combination_pattern
confidence
evidence
Allowed unresolved state:
main_pattern = null
state = unresolved
18. PATTERN RESULT MODEL
Object:
PatternDecision
Fields:
state
primary
secondary
special
confidence
source
evidence_ids
source should identify:
canonical_pattern_engine
MC-01 must not pretend the pattern was independently rediscovered if it came from upstream.
19. PATTERN ENUM
Initial canonical pattern identifiers SHOULD be stable IDs.
Examples:
zheng_guan
qi_sha
zheng_cai
pian_cai
zheng_yin
pian_yin
shi_shen
shang_guan
jian_lu
yang_ren
cong_cai
cong_guan_sha
cong_er
cong_wang
hua_qi
special_combination
unresolved
Customer-facing Vietnamese labels belong in presentation mapping.
20. PURITY MODEL
Object:
PatternPurityResult
Fields:
state
score
classification
positive_factors
negative_factors
conflicts
evidence_ids
confidence
Classification enum:
very_pure
pure
moderately_pure
mixed
heavily_mixed
structurally_impure
unresolved
21. PURITY FACTOR
Object:
PurityFactor
Fields:
factor_id
factor_type
effect
severity
description_key
evidence_ids
Effect:
increase
decrease
neutral
Possible factor types:
primary_deity_dominance
competing_deity
mixed_guan_sha
mixed_wealth
root_consistency
stem_exposure
hidden_interference
structural_continuity
22. PATTERN STRENGTH MODEL
Object:
PatternStrengthResult
Fields:
state
score
classification
root_power
season_power
exposure_power
generation_power
continuity_power
weakening_factors
evidence_ids
confidence
Classification:
very_weak
weak
moderate
strong
very_strong
unresolved
Important:
This object is distinct from Day Master strength.
23. SUPPORT MODEL
Object:
SupportFinding
Fields:
support_id
support_type
source
target
strength
reliability
effect
evidence_ids
rule_id
Support types may include:
resource_support
wealth_generates_officer
seal_protects_officer
seal_transforms_killer
output_generates_wealth
root_support
season_support
stem_support
branch_support
day_master_capacity
other
24. SUPPORT STRENGTH
Enum:
minor
moderate
strong
critical
"critical" means structurally decisive support,
not necessarily positive destiny.
25. DAMAGE MODEL
Object:
DamageFinding
Fields:
damage_id
damage_type
source
target
severity
directness
reversibility
structural_effect
evidence_ids
rule_id
confidence
26. DAMAGE TYPE
Initial enum:
hurting_officer_attacks_officer
owl_robs_food
peer_robs_wealth
mixed_officer_killer
wealth_overloads_weak_day_master
killer_overloads_weak_day_master
resource_overload
root_destroyed
pattern_deity_controlled
pattern_deity_clashed
pattern_deity_combined_away
branch_punishment
branch_harm
branch_break
seasonal_conflict
useful_god_conflict
other
Do not over-expand this enum prematurely.
27. DAMAGE SEVERITY
Enum:
minor
moderate
major
critical
Severity must be derived from:
presence
root strength
season
exposure
repetition
direct targeting
available rescue
not from name alone.
28. DAMAGE DIRECTNESS
Enum:
direct
indirect
conditional
Example:
Thương Quan directly attacks Chính Quan
may be direct.
A seasonal weakening may be indirect.
29. DAMAGE REVERSIBILITY
Enum:
fully_reversible
partially_reversible
difficult_to_reverse
irreversible
unknown
This becomes important in Rescue analysis.
30. RESCUE MODEL
Object:
RescueFinding
Fields:
rescue_id
rescue_type
source
target_damage_ids
strength
reliability
coverage
damage_offset
conditions
evidence_ids
rule_id
confidence
31. RESCUE TYPE
Initial enum:
seal_controls_hurting_officer
seal_transforms_killer
officer_controls_peer
resource_restores_structure
wealth_bridges_structure
output_releases_excess
combination_resolves_conflict
root_restoration
climate_balance
other
32. RESCUE COVERAGE
Enum:
full
substantial
partial
weak
conditional
A rescue should not automatically erase all damage.
33. DAMAGE OFFSET
Numeric:
0.0 .. 1.0
Meaning:
0.0 = no meaningful rescue
1.0 = theoretical full offset
This field is only valid after a rescue rule is matched.
34. USEFUL GOD COMPATIBILITY
Object:
UsefulGodCompatibilityResult
Fields:
state
score
agreements
conflicts
neutral_factors
evidence_ids
confidence
35. COMPATIBILITY FINDING
Object:
CompatibilityFinding
Fields:
finding_id
factor
relationship
effect
severity
evidence_ids
Relationship:
aligned
partially_aligned
neutral
conflicting
strongly_conflicting
36. CLIMATE COMPATIBILITY
Object:
ClimateCompatibilityResult
Fields:
state
score
temperature_state
required_adjustment
pattern_alignment
useful_god_alignment
conflicts
evidence_ids
confidence
Climate logic must remain separate from elemental strength.
37. STRUCTURAL INTEGRITY MODEL
Object:
StructuralIntegrityResult
Fields:
state
score
classification
purity_component
strength_component
support_component
damage_component
rescue_component
useful_god_component
climate_component
critical_findings
evidence_ids
confidence
The exact formula is NOT frozen in this document.
38. STRUCTURAL STATE
Enum:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
Important distinction:
damaged_but_rescued
must not collapse into:
complete
because the explanation matters.
39. GRADE MODEL
Object:
PatternGradeResult
Fields:
state
grade
score
confidence
basis
evidence_ids
Grade enum:
SS
S
A
B
C
D
UNRESOLVED
40. GRADE SEMANTICS
Canonical interpretation:
SS = exceptional structural integrity
S  = very high structural integrity
A  = strong structural integrity
B  = workable / conditional structure
C  = substantially compromised
D  = severely compromised
Forbidden direct mapping:
SS = đại phú đại quý
D = nghèo
Grade evaluates natal structural integrity only.
41. ACHIEVEMENT DIMENSION MODEL
Generic object:
AchievementDimension
Fields:
dimension
score
classification
confidence
positive_evidence_ids
negative_evidence_ids
conditions
risks
42. ACHIEVEMENT DIMENSIONS
Initial canonical IDs:
authority
institutional_career
leadership
management
entrepreneurship
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
academic
technical
creative
public_visibility
stability
independence
Phase 1 may leave these unresolved.
43. ACHIEVEMENT CLASSIFICATION
Enum:
very_low
low
below_average
moderate
above_average
high
very_high
unresolved
These labels represent relative structural potential.
44. ACHIEVEMENT RESULT
Object:
AchievementProfile
Fields:
state
dimensions
dominant_capabilities
secondary_capabilities
structural_risks
confidence
45. DECISION MODEL
Object:
MingJuDecisionSummary
Fields:
state
headline_key
summary_keys
strength_keys
risk_keys
condition_for_success_keys
condition_to_avoid_keys
dominant_theme
secondary_themes
Important:
Core engine should prefer message keys over final Vietnamese prose.
Example:
headline_key =
mingju.zheng_guan.conditional_complete
Composer resolves wording later.
46. DOMINANT THEME
Possible structural themes:
authority
wealth
output
resource
competition
mixed
follow_structure
special_structure
unresolved
This is for interpretation grouping,
not a replacement for pattern identity.
47. WARNING MODEL
Object:
MingJuWarning
Fields:
code
severity
message_key
related_evidence_ids
Severity:
info
warning
error
critical
Examples:
missing_hour_pillar
pattern_conflict
transformation_unresolved
low_pattern_confidence
insufficient_relation_data
48. UPSTREAM SOURCE REFERENCE
Object:
SourceReference
Fields:
module
schema_version
field_path
value_hash
Purpose:
MC-01 audit can identify which upstream data produced the result.
Do not duplicate full upstream payload inside result unless necessary.
49. RULE EFFECT MODEL
Conceptual:
RuleEffect
Fields:
effect_type
target
operation
value
reason_key
Operations may include:
add_score
subtract_score
register_support
register_damage
register_rescue
add_warning
add_conflict
set_state
Actual runtime rule format will be defined later.
50. NO HIDDEN DERIVATION
Every material field MUST be one of:
upstream canonical fact
rule-derived finding
aggregate derived from explicit findings
composer-only presentation
No hidden/manual field injection is allowed.
51. NULLABILITY POLICY
MC-01 MUST distinguish:
null
from:
0
Example:
authority_score = null
means:
not computed / unresolved.
authority_score = 0
means:
computed and determined to be minimum.
These must never be treated as equivalent.
52. UNKNOWN ENUM POLICY
Enums SHOULD support:
unknown
or:
unresolved
where domain logic requires uncertainty.
Do not silently default unknown to positive or negative states.
53. SERIALIZATION POLICY
Runtime JSON should:
- use stable English IDs
- avoid localized labels inside engine payload
- preserve arrays in deterministic order
- preserve trace sequence
- preserve evidence references
- expose version fields
- avoid floating-point noise where possible
Example:
{
  "schema_version": "bte.mingju.decision.v1",
  "ruleset_version": "bte.mingju.rules.v1",
  "status": "complete"
}
54. DETERMINISTIC ORDERING
Arrays MUST use deterministic order.
Recommended ordering:
Support
priority
→ rule_id
→ support_id
Damage
severity desc
→ priority
→ rule_id
→ damage_id
Rescue
target_damage_id
→ strength desc
→ rule_id
Evidence
source_module
→ source_path
→ evidence_id
Trace
sequence
This prevents unstable snapshots.
55. ID POLICY
Stable prefixes:
E-MC-*     evidence
SUP-MC-*   support
DMG-MC-*   damage
RSC-MC-*   rescue
CMP-MC-*   compatibility
TR-MC-*    trace
WRN-MC-*   warning
Runtime-generated IDs must be deterministic when possible.
Avoid random UUIDs in snapshot-critical outputs.
56. SCORE PRECISION
Canonical calculation may use floating point internally.
Serialized output SHOULD normalize:
scores → maximum 2 decimal places
confidence → maximum 4 decimal places
unless an upstream contract requires more precision.
57. PRESENTATION SEPARATION
Do NOT store:
"Bạn là người có số làm quan..."
inside the decision engine.
Instead:
decision.headline_key
decision.summary_keys
Composer converts structured results into Vietnamese.
58. GOLDEN DATASET REPRESENTATION
Golden cases should validate structured fields.
Example:
{
  "expected": {
    "pattern.primary": "zheng_guan",
    "integrity.classification": [
      "complete",
      "substantially_complete"
    ],
    "damage.must_include": [],
    "damage.must_not_include": [
      "owl_robs_food"
    ],
    "grade.allowed": [
      "A",
      "S"
    ]
  }
}
Golden tests SHOULD allow expert-approved alternative classifications when appropriate.
59. FORBIDDEN GOLDEN FORMAT
Avoid:
{
  "expected_result": "A"
}
without structural expectations.
Grade-only testing encourages black-box tuning.
60. MINIMUM PHASE 1 CONTRACT
MC-01A–D require these fields:
schema_version
ruleset_version
status
pattern
purity
pattern_strength
support
damage
rescue
integrity
grade
warnings
trace
Achievement models are optional until MC-01E.
61. PHASE 1 ROOT EXAMPLE
Conceptual example:
{
  "schema_version": "bte.mingju.decision.v1",
  "ruleset_version": "bte.mingju.rules.v1",

  "status": "complete",

  "pattern": {
    "state": "resolved",
    "primary": "zheng_guan",
    "secondary": [],
    "confidence": 0.94
  },

  "purity": {
    "state": "resolved",
    "score": 84,
    "classification": "pure",
    "positive_factors": [],
    "negative_factors": [],
    "conflicts": [],
    "evidence_ids": [],
    "confidence": 0.9
  },

  "pattern_strength": {
    "state": "resolved",
    "score": 79,
    "classification": "strong",
    "evidence_ids": [],
    "confidence": 0.88
  },

  "support": [],

  "damage": [],

  "rescue": [],

  "integrity": {
    "state": "resolved",
    "score": 82,
    "classification": "substantially_complete",
    "critical_findings": [],
    "evidence_ids": [],
    "confidence": 0.88
  },

  "grade": {
    "state": "resolved",
    "grade": "A",
    "score": 82,
    "confidence": 0.88,
    "basis": []
  },

  "warnings": [],

  "trace": []
}
Values above are illustrative only.
They are NOT canonical scoring rules.
62. EMPTY RESULT POLICY
If required input is unavailable:
{
  "status": "insufficient_evidence",
  "pattern": {
    "state": "unresolved",
    "primary": null
  },
  "grade": {
    "state": "unresolved",
    "grade": "UNRESOLVED"
  }
}
Do not fabricate fallback grade B or C.
63. ERROR BOUNDARY
Invalid canonical data should produce:
status = invalid_input
Examples:
- impossible Day Master ID
- malformed pattern payload
- impossible strength state
- duplicate contradictory canonical field
Engine must distinguish:
invalid input
from:
valid but unresolved chart
64. API STABILITY
Once bte.mingju.decision.v1 is published:
- field meanings cannot silently change
- enum meaning cannot silently change
- score direction cannot change
- grade semantics cannot change
Breaking changes require:
bte.mingju.decision.v2
65. INTERNAL EXTENSIBILITY
The model must support future domains without breaking V1.
Potential future extensions:
luck_activation
relationship_profile
health_tendency
education_profile
social_mobility
entrepreneurial_cycle
wealth_cycle
authority_cycle
These should be added as optional downstream models.
66. DATA MODEL INVARIANTS
The following invariants MUST hold:
I-01
Every damage record has at least one evidence reference.
I-02
Every rescue targets at least one registered damage.
I-03
Rescue cannot exist for a nonexistent damage.
I-04
Grade cannot be resolved if Integrity is unresolved.
I-05
Integrity cannot be resolved if both Pattern and Pattern Strength are unresolved.
I-06
Achievement score cannot claim high confidence when core structural confidence is insufficient.
I-07
No MC-01 score may silently replace upstream Strength score.
I-08
Natal Grade is independent of current Đại Vận.
I-09
All rule-derived findings must be represented in trace.
I-10
All customer wording is downstream from structured facts.
67. VALIDATION CHECKS
At model validation time verify:
score in allowed range
confidence in 0..1
valid enums
valid evidence references
valid damage→rescue references
deterministic ordering
required version fields
required status fields
no unresolved grade with resolved-looking score
68. MODEL OWNERSHIP
Ownership boundaries:
Calendar Engine
owns calendar truth

BaZi Engine
owns pillar truth

Strength Engine
owns Day Master strength truth

Pattern Engine
owns pattern identity truth

Useful God Engine
owns useful/favorable/unfavorable truth

MC-01
owns structural synthesis and Mệnh Cục decision
This boundary is mandatory.
69. IMPLEMENTATION RECOMMENDATION
Recommended Python structure:
engines/
└── mingju/
    ├── __init__.py
    ├── models.py
    ├── context.py
    ├── evidence.py
    ├── trace.py
    ├── rules/
    ├── purity.py
    ├── pattern_strength.py
    ├── support.py
    ├── damage.py
    ├── rescue.py
    ├── integrity.py
    ├── grade.py
    └── composer.py
This document does NOT authorize implementation yet.
Runtime structure can be finalized after architecture review.
70. FREEZE TARGET
Once approved, the following should be frozen before rule coding:
root result shape
status enums
evidence model
trace model
support model
damage model
rescue model
integrity model
grade model
nullability semantics
versioning semantics
Scoring weights remain unfrozen.
71. ARCHITECTURAL DECISION
MC-01 data model is built around:
STRUCTURED EVIDENCE
        ↓
STRUCTURED FINDINGS
        ↓
STRUCTURAL DECISION
        ↓
EXPLAINABLE RESULT
not:
pattern name
→ arbitrary score
→ customer conclusion
This distinction is mandatory for all later MC-01 implementation.
72. NEXT DOCUMENT
Next:
02_PATTERN_RECOGNITION.md
Purpose:
- define exactly what MC-01 consumes from Pattern Engine
- normalize pattern identities
- define main / secondary / special patterns
- define unresolved pattern handling
- define pattern precedence
- define pattern conflicts
- define what MC-01 may and may not reinterpret
- establish the Pattern Decision input contract for all later MC-01 stages

Tôi muốn chốt thêm một nguyên tắc ở file này: **`Evidence` và `Trace` phải được xây ngay từ phiên bản đầu**, không để đến cuối mới bổ sung. Nếu đợi tới khi engine đã có hàng trăm rule mới làm explainability thì gần như chắc chắn sẽ phải viết lại rất nhiều.

Sau khi lưu `01_DATA_MODEL.md`, bước tiếp theo chúng ta làm **`02_PATTERN_RECOGNITION.md`**. Đây sẽ là nơi khóa rất rõ mối quan hệ giữa **Pattern Engine hiện tại** và **MC-01**, đặc biệt là chuyện **chính cách, phụ cách, đặc cách, tòng cách, hóa cách và khi nào phải trả về `unresolved`**.