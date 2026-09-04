# MC-01 — VALIDATION RULES

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `13_VALIDATION_RULES.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`  
**Ruleset target:** `bte.mingju.rules.v1`

---

# 1. PURPOSE

This document defines canonical validation rules for MC-01.

Validation must protect:

- data integrity
- stage consistency
- reference integrity
- score ranges
- confidence ranges
- unresolved-state correctness
- Damage/Rescue linkage
- Structural Integrity correctness
- Grade correctness
- Achievement dependency correctness
- Wealth score direction
- Career dependency correctness
- version compatibility
- deterministic ordering
- no hidden mutation
- no duplicate causal inflation

Validation is not optional.

Every published `MingJuDecisionResult` must pass validation.

---

# 2. VALIDATION PHILOSOPHY

Canonical validation layers:

```text
Input Contract Validation
        ↓
Stage-Level Validation
        ↓
Cross-Stage Validation
        ↓
Reference Integrity Validation
        ↓
Semantic Invariant Validation
        ↓
Serialization Validation
        ↓
Determinism Validation

The validator must distinguish:
technical invalidity
from:
domain uncertainty
3. VALIDATION RESULT
Recommended object:
ValidationResult
Fields:
valid
errors
warnings
invariant_failures
stage_failures
version_failures
reference_failures
4. VALIDATION SEVERITY
Canonical levels:
info
warning
error
critical
Meaning:
info
Diagnostic only.
warning
Result may remain valid but confidence/status may be affected.
error
Result is not publishable as complete canonical output.
critical
Core contract or semantic integrity is broken.
5. FAIL-FAST VS COLLECT-ALL
Recommended policy:
contract-critical violations
→ fail fast

domain consistency violations
→ collect all when safe
Examples fail-fast:
unsupported schema version
invalid enum
score outside impossible range
broken Damage→Rescue reference
Examples collect-all:
missing optional relation
low confidence
partial Career rule coverage
6. INPUT VALIDATION
MingJuContext must validate before analysis.
Required checks:
context schema version valid
Day Master valid
Four Pillars structurally valid
Pattern input structurally valid
Strength state valid
Ten Gods payload valid
confidence fields within range
source versions present where required
7. INPUT NULLABILITY
Validation must distinguish:
null
from:
empty
and from:
zero
Example:
hour_pillar = null
may be valid.
But:
hour_pillar = ""
may be invalid depending on contract.
8. SCORE RANGE VALIDATION
All canonical 0..100 scores must satisfy:
0 <= score <= 100
unless:
score = null
for unresolved/not-computed state.
9. CONFIDENCE RANGE VALIDATION
All confidence values must satisfy:
0.0 <= confidence <= 1.0
10. SCORE / STATE CONSISTENCY
Forbidden:
state = unresolved
score = 82
unless the field explicitly supports provisional score.
Default policy:
unresolved
→ score = null
11. CLASSIFICATION / SCORE CONSISTENCY
If a classification is score-derived,
the classification must match current ruleset thresholds.
Example:
score = 83
classification = weak
must fail if ruleset defines 83 as strong.
12. VERSION VALIDATION
Every result must expose:
schema_version
ruleset_version
context_schema_version
Composer output must expose:
composer_version
message_catalog_version
locale
mode
13. VERSION COMPATIBILITY
Validator must verify compatibility between:
context version
decision schema
ruleset
composer version
message catalog
Do not silently accept incompatible combinations.
14. UNKNOWN VERSION
Unknown version must produce:
error or typed version failure
not silent fallback.
15. PATTERN VALIDATION
Validate:
primary ID valid
family valid
state valid
confidence valid
secondary IDs valid
special/follow/transformation IDs valid
16. PATTERN RESOLVED INVARIANT
If:
pattern.state = resolved
then:
pattern.primary != null
and:
pattern.primary_family != unresolved
17. PATTERN UNRESOLVED INVARIANT
If:
pattern.primary = null
then:
pattern.state != resolved
18. PATTERN FAMILY CONSISTENCY
Examples:
cong_cai
→ family = follow

hua_qi
→ family = transformation

zheng_guan
→ family = standard
Any mismatch fails validation.
19. FOLLOW PATTERN CONSISTENCY
If:
pattern.primary_family = follow
then standard-only rule outputs must not appear unless explicitly allowed.
20. TRANSFORMATION PATTERN CONSISTENCY
If:
pattern.primary_family = transformation
then transformation-specific validation rules must apply.
21. PURITY VALIDATION
Validate:
state
score
classification
positive_factors
negative_factors
conflicts
evidence references
confidence
22. PURITY RESOLVED DEPENDENCY
By default:
Pattern unresolved
→ Purity cannot be resolved
unless a documented family-level exception exists.
23. PURITY EVIDENCE REQUIREMENT
Every:
negative factor
conflict
major positive factor
must reference at least one evidence item.
24. PURITY NO-GRADE LEAKAGE
Purity output must not contain:
grade
wealth outcome
authority outcome
career recommendation
Any such field indicates layer leakage.
25. PATTERN STRENGTH VALIDATION
Validate:
score
classification
season_power
root_power
exposure_power
generation_power
continuity_power
position_power
confidence
26. PATTERN STRENGTH VS DAY MASTER STRENGTH
Validator must ensure MC-01 Pattern Strength has not overwritten or duplicated canonical Day Master Strength field semantics.
Forbidden:
pattern_strength.state = strong
being serialized into the upstream:
strength.classification
27. PATTERN STRENGTH UNRESOLVED RULE
If:
pattern.state = unresolved
then:
pattern_strength.state
must usually be:
unresolved
or partially_resolved
not fully resolved without explicit exception.
28. SUPPORT VALIDATION
Every support finding must contain:
support_id
support_type
source
target
strength
evidence_ids
rule_id
29. SUPPORT EVIDENCE INVARIANT
Every support finding requires at least one evidence reference.
30. SUPPORT VS RESCUE INVARIANT
A support finding must not be serialized as Rescue merely because it is favorable.
Support and Rescue IDs/types must remain distinct.
31. DAMAGE VALIDATION
Every DamageFinding must contain:
damage_id
damage_type
source
target
severity
directness
reversibility
evidence_ids
rule_id
confidence
causal_group
32. DAMAGE SOURCE INVARIANT
Damage source must exist as a valid structural entity or registered relation.
33. DAMAGE TARGET INVARIANT
Damage target must exist and be structurally relevant.
Forbidden:
target = unknown/nonexistent
for resolved Damage.
34. DAMAGE EVIDENCE INVARIANT
Every DamageFinding must reference at least one evidence item.
35. DAMAGE SEVERITY ENUM
Allowed only:
minor
moderate
major
critical
36. DAMAGE DIRECTNESS ENUM
Allowed:
direct
indirect
conditional
37. DAMAGE REVERSIBILITY ENUM
Allowed:
fully_reversible
partially_reversible
difficult_to_reverse
irreversible
unknown
38. WEAKNESS ≠ DAMAGE VALIDATION
Validator should detect prohibited shorthand rules where possible.
Example forbidden condition:
pattern_strength = weak
→ damage_type = pattern_deity_controlled
without an actual damaging relation.
39. IMPURITY ≠ DAMAGE VALIDATION
Forbidden:
purity = mixed
→ damage = mixed_officer_killer
unless independent Damage conditions are satisfied.
40. RELATION PRESENCE ≠ DAMAGE
A raw:
xung
hình
hại
phá
hợp
relation may not create Damage unless a structural target/effect exists.
41. RESCUE VALIDATION
Every RescueFinding must contain:
rescue_id
rescue_type
source
target_damage_ids
strength
reliability
coverage
mechanism
evidence_ids
rule_id
confidence
42. RESCUE TARGET INVARIANT
Every:
target_damage_id
must reference a real registered DamageFinding.
This is a critical invariant.
43. NO ORPHAN RESCUE
Forbidden:
Rescue exists
but target Damage does not exist
This must fail validation.
44. NO EMPTY TARGET RESCUE
Forbidden:
target_damage_ids = []
for resolved Rescue.
45. RESCUE EVIDENCE INVARIANT
Every Rescue requires evidence.
46. RESCUE MECHANISM INVARIANT
Every Rescue must define a mechanism such as:
control_source
transform_source
restore_root
repair_chain
bridge_conflict
47. DAMAGE HISTORY PRESERVATION
If Rescue targets Damage,
the original Damage must still exist in the result.
Forbidden:
Rescue exists
Damage removed from output
48. DAMAGE OFFSET RANGE
If:
damage_offset != null
then:
0.0 <= damage_offset <= 1.0
49. RESCUE COVERAGE ENUM
Allowed:
full
substantial
partial
weak
conditional
50. RESCUE RELIABILITY ENUM
Allowed:
very_low
low
moderate
high
very_high
51. RESIDUAL DAMAGE VALIDATION
Every ResidualDamageResult must reference:
existing original Damage
and optionally:
existing Rescue IDs
52. RESIDUAL DAMAGE SOURCE INVARIANT
Forbidden:
residual_damage.damage_id
that does not exist in DamageResult.
53. RESIDUAL SEVERITY ENUM
Allowed:
none
minor
moderate
major
critical
unresolved
54. STRUCTURAL INTEGRITY VALIDATION
Validate:
state
score
classification
components
residual_damage
critical_findings
confidence
evidence_ids
55. INTEGRITY DEPENDENCY
Structural Integrity cannot be fully resolved if:
pattern unresolved
and no explicit pattern-independent exception exists.
56. INTEGRITY SCORE RANGE
If resolved:
0 <= integrity.score <= 100
57. INTEGRITY STATE ENUM
Allowed:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
58. DAMAGED_BUT_RESCUED INVARIANT
If:
integrity.classification = damaged_but_rescued
then there must exist:
at least one meaningful Damage
and
at least one valid Rescue targeting it
59. DAMAGED INVARIANT
If:
integrity.classification = damaged
there must be:
meaningful residual Damage
60. FAILED INVARIANT
If:
integrity.classification = failed
validator must require:
core structural failure evidence
and
major/critical residual impairment
Do not allow failed from low Purity alone.
61. COMPLETE INVARIANT
If:
classification = complete
there must not be:
major untreated residual Damage
critical unresolved finding
62. CONDITIONALLY_COMPLETE INVARIANT
If:
classification = conditionally_complete
then:
conditions_for_function
or equivalent structural dependency must be present.
63. MIXED INVARIANT
If:
classification = mixed
there should be meaningful Purity/mixing evidence.
64. GRADE VALIDATION
Validate:
state
grade
score
confidence
basis
integrity_state
65. GRADE ENUM
Allowed:
SS
S
A
B
C
D
UNRESOLVED
66. GRADE DEPENDS ON INTEGRITY
Critical:
Integrity unresolved
→ Grade = UNRESOLVED
Any other result fails.
67. GRADE SCORE RANGE
Resolved Grade score:
0..100
68. GRADE STATE CONSISTENCY
Forbidden:
grade = UNRESOLVED
score = 82
unless a future explicit provisional-score contract exists.
69. GRADE / INTEGRITY STATE CONSISTENCY
Validator should detect impossible combinations under current ruleset.
Example conceptual forbidden:
integrity = failed
grade = SS
70. GRADE TRACE REQUIREMENT
Every resolved Grade must have:
basis
or trace reference
No unexplained grade.
71. ACHIEVEMENT VALIDATION
Each dimension must validate:
dimension ID
score
classification
confidence
positive evidence
negative evidence
conditions
risks
72. ACHIEVEMENT DIMENSION ENUM
Allowed V1 dimensions:
authority
institutional_career
leadership
management
entrepreneurship
academic
technical
creative
public_visibility
independence
stability
73. ACHIEVEMENT SCORE RANGE
Resolved dimension:
0..100
74. ACHIEVEMENT DEPENDS ON INTEGRITY
If:
integrity = unresolved
then Achievement cannot be fully high-confidence resolved.
75. ACHIEVEMENT NO UNIVERSAL SUCCESS SCORE
If schema exposes a single:
success_score
as primary decision,
validation should fail architecture compliance.
76. ACHIEVEMENT EVIDENCE REQUIREMENT
Every material high/very_high or low/very_low dimension should have supporting evidence.
77. ACHIEVEMENT BIOGRAPHY GUARD
Achievement input must not contain biography-derived decision fields such as:
job_title
income
net_worth
known_status
unless strictly stored as non-inference metadata.
78. WEALTH VALIDATION
Validate dimensions:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
79. WEALTH SCORE RANGE
All resolved Wealth scores:
0..100
80. FINANCIAL VOLATILITY DIRECTION
Critical invariant:
financial_volatility.score_direction
=
higher_is_riskier
Never:
higher_is_better
81. OTHER WEALTH SCORE DIRECTION
Default:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
should use:
higher_is_better
unless future schema explicitly changes.
82. WEALTH CREATION ≠ RETENTION
Validator should reject schemas/logic that alias:
wealth_creation
and:
wealth_retention
to the same field.
83. TÀI STRENGTH ≠ WEALTH PROFILE
Wealth output must not be copied directly from Pattern Strength.
Example forbidden shortcut:
wealth_creation.score = pattern_strength.score
without domain rules.
84. WEALTH CAPACITY DEPENDENCY
If Wealth capacity logic is used,
it must consume canonical Day Master Strength.
It must not introduce a second Day Master strength result.
85. WEALTH BIOGRAPHY GUARD
No use of:
income
assets
business ownership
as inference input.
86. CAREER VALIDATION
Validate:
primary_work_styles
secondary_work_styles
organizational_fit
role_fit
autonomy_need
leadership_fit
management_fit
entrepreneurial_fit
specialist_fit
technical_fit
academic_fit
creative_fit
public_facing_fit
career_stability
career_risks
87. CAREER WORK STYLE ENUM
Allowed V1:
structured_institutional
managerial
leadership_command
entrepreneurial
specialist
technical
academic_research
creative_expression
public_facing
independent_autonomous
hybrid
unresolved
88. CAREER MUST CONSUME ACHIEVEMENT
Career output should not be fully resolved if Achievement is unavailable,
unless an explicitly documented exception exists.
89. ENTREPRENEURIAL CAREER MUST CONSUME WEALTH CONTEXT
For high-confidence entrepreneurial fit,
Wealth context should be available.
If Wealth is unresolved:
career entrepreneurial fit confidence
should be reduced or partial.
90. CAREER NO EXACT JOB TITLE
Core CareerProfile must not contain deterministic exact profession fields such as:
doctor
lawyer
CEO
teacher
police
unless stored only as optional downstream examples outside canonical inference.
91. CAREER BIOGRAPHY GUARD
Current occupation must not alter canonical CareerProfile.
92. COMPOSER VALIDATION
Validate:
composer_version
message_catalog_version
locale
mode
source paths
message keys
evidence references
confidence
93. COMPOSER SOURCE INVARIANT
Every material composed statement must map to:
source path
or evidence ID
94. COMPOSER NO NEW TRUTH
Composer must not introduce facts absent from MingJuDecisionResult.
95. MESSAGE KEY COMPATIBILITY
Each message key should declare source requirements.
Example:
mingju.wealth.high_creation_low_retention
requires:
wealth_creation >= high
wealth_retention <= moderate
96. INCOMPATIBLE MESSAGE KEY
If requirements are not met,
Composer validation must fail.
97. COMPOSER GRADE PARITY
Composer cannot display:
Grade A
when canonical result is:
Grade B
98. COMPOSER INTEGRITY PARITY
Composer cannot say:
thành cách vững
if:
integrity = damaged
unless wording policy explicitly maps that state compatibly.
99. COMPOSER WEALTH PARITY
Composer cannot say:
giữ tiền tốt
if:
wealth_retention = low
100. COMPOSER CAREER PARITY
Composer cannot say:
phù hợp môi trường cứng nhắc
if canonical CareerProfile indicates:
institutional_fit low
autonomy_need very_high
unless expressed as a trade-off.
101. CONFIDENCE LANGUAGE VALIDATION
Strong wording must not be used with very low confidence.
Example forbidden:
confidence = 0.35
text = "Đây là thế mạnh nổi bật chắc chắn..."
102. TRACE VALIDATION
Each MingJuTraceEvent must contain:
trace_id
stage
sequence
action
result
and where applicable:
rule_id
input_evidence_ids
output_ids
103. TRACE SEQUENCE
Trace sequence must be:
unique
strictly deterministic
ordered
104. TRACE OUTPUT REFERENCES
Any:
output_id
in trace should reference a real produced object where applicable.
105. RULE MATCH VALIDATION
Each matched rule should expose:
rule_id
rule_version
domain
matched
conditions
effects
confidence
106. RULE VERSION CONSISTENCY
All rule matches in one result must belong to the active:
ruleset_version
unless explicit compatibility is defined.
107. EVIDENCE VALIDATION
Every evidence object must have:
evidence_id
evidence_type
source_module
subject
predicate
polarity
confidence
where applicable.
108. EVIDENCE ID UNIQUENESS
All evidence IDs must be unique inside a result.
109. FINDING ID UNIQUENESS
All:
support_id
damage_id
rescue_id
trace_id
warning code instance ID if used
must be unique.
110. DETERMINISTIC ID VALIDATION
IDs should not be random between identical runs.
Snapshot-critical output must be stable.
111. ORDERING VALIDATION
Arrays must follow deterministic order.
Recommended:
Damage
severity desc
→ priority
→ rule_id
→ damage_id
Rescue
target_damage_id
→ strength desc
→ rule_id
Trace
sequence asc
112. SET / MAP SERIALIZATION
Do not serialize unordered sets directly.
Maps should use stable serialization where required for hashing/snapshots.
113. FLOAT PRECISION VALIDATION
Serialized scores:
max 2 decimals
Serialized confidence:
max 4 decimals
unless upstream contract requires otherwise.
114. NO FLOAT NOISE
Values such as:
81.9999999997
should not leak into canonical serialized payload.
115. CAUSAL DUPLICATION VALIDATION
Validator should detect possible duplicate causal effects.
Example:
same clash
→ root_destroyed
→ continuity_broken
→ full independent penalties
without causal metadata.
116. REQUIRED CAUSAL METADATA
For stages participating in aggregate scoring,
findings should expose:
causal_group
and when needed:
overlap_group
parent_id
117. DUPLICATE CAUSAL GROUP WARNING
If multiple full-score findings share:
same causal_group
same evidence set
same target
validator should emit warning or error depending on policy.
118. SUPPORT / STRENGTH DOUBLE-COUNT WARNING
Example:
Tài sinh Quan
appears in:
generation_power
support
This is allowed,
but Integrity aggregation must mark overlap.
119. DAMAGE / STRENGTH DOUBLE-COUNT WARNING
Example:
root destroyed
reduces Pattern Strength
and also appears as Damage.
Allowed only if overlap metadata prevents full duplicate penalty.
120. RESCUE / SUPPORT DOUBLE-COUNT WARNING
Same Ấn may:
support Day Master
and
rescue Sát overload
Allowed but must be causally tracked.
121. STRUCTURAL STATE / SCORE COHERENCE
Validator should compare state and score under ruleset.
Example suspicious:
state = failed
score = 92
must fail or trigger critical error.
122. GRADE / SCORE COHERENCE
Example:
grade = D
score = 91
must fail if current thresholds contradict it.
123. ACHIEVEMENT / CONFIDENCE COHERENCE
Example suspicious:
authority = very_high
confidence = 0.15
may be valid only if low-confidence classification is explicitly allowed.
Otherwise should warn.
124. WEALTH VOLATILITY PRESENTATION GUARD
UI/composer adapters should be validated so that:
high volatility
is presented as risk,
not as positive capability.
125. NATAL / LUCK SEPARATION
Critical invariant:
Natal MingJuDecisionResult must not contain:
current_luck_cycle-derived Grade
current-year adjusted Purity
luck-adjusted natal WealthProfile
126. LUCK FIELD GUARD
If input context contains:
current_luck_cycle
current_year
validator should either:
ignore with warning
or reject
depending on final API design.
Preferred:
reject from natal context
127. BIOGRAPHY SEPARATION
Natal context must not contain inference-driving biography fields.
Potential forbidden inputs:
occupation
income
net_worth
education_level
marital_status
known_success
These may exist only in external validation harnesses.
128. FRONTEND OWNERSHIP VALIDATION
Static/integration tests should ensure frontend code does not contain duplicated core rules such as:
if grade ...
if authority > ...
if wealth_creation > ...
to create canonical interpretation.
129. REPORT OWNERSHIP VALIDATION
Report Engine must consume canonical MC-01 output.
It must not independently recompute:
Mệnh cục
Grade
wealth profile
career profile
130. COMPOSER OWNERSHIP VALIDATION
Composer may synthesize,
but must not access raw engine inputs for new analytical inference.
131. IMMUTABILITY VALIDATION
After MingJuDecisionResult is created,
downstream stages must not mutate it.
Possible strategy:
frozen dataclasses
immutable models
copy-on-adapt
132. SOURCE HASH VALIDATION
If source/result hashes are implemented,
validator should verify:
hash matches normalized serialization
133. IDEMPOTENCY VALIDATION
Run:
analyze_mingju(context)
multiple times.
Expected:
same semantic result
same IDs
same ordering
same serialized output
134. COMPOSER IDEMPOTENCY
Same:
decision result
composer version
message catalog
locale
mode
must produce identical composition.
135. SNAPSHOT VALIDATION
Snapshots should cover:
complete
partial
unresolved
damaged
damaged_but_rescued
failed
not only happy paths.
136. GOLDEN DATASET VALIDATION
Golden cases should verify:
required findings
forbidden findings
accepted alternatives
allowed score range
allowed Grade range
required trace
137. DO NOT VALIDATE ONLY FINAL GRADE
Forbidden Golden approach:
expected Grade = A
alone.
Must also validate reasoning path.
138. ACCEPTED ALTERNATIVES
Expert-approved alternatives may be represented as:
allowed classifications
allowed grade range
accepted structural states
where classical interpretation genuinely differs.
139. FORBIDDEN CONCLUSIONS
Golden cases should include:
must_not_include
for known incorrect conclusions.
This is especially important for:
false Tòng
false Hóa
false Quan/Sát damage
false wealth conclusion
140. VALIDATION ERROR CODE FORMAT
Recommended stable code format:
MCV-{DOMAIN}-{NNN}
Examples:
MCV-API-001
MCV-PAT-001
MCV-PUR-001
MCV-STR-001
MCV-DMG-001
MCV-RSC-001
MCV-INT-001
MCV-GRD-001
MCV-ACH-001
MCV-WLT-001
MCV-CAR-001
MCV-CMP-001
141. SAMPLE ERROR
{
  "code": "MCV-RSC-001",
  "severity": "critical",
  "message": "Rescue references nonexistent Damage ID",
  "path": "rescue.findings[0].target_damage_ids[0]"
}
142. WARNING CODE EXAMPLE
{
  "code": "MCV-CTX-101",
  "severity": "warning",
  "message": "Hour pillar unavailable; confidence may be reduced."
}
143. VALIDATION PIPELINE
Canonical:
MingJuContext
      ↓
Validate Context
      ↓
Run Engine
      ↓
Validate Stage Outputs
      ↓
Validate Cross-References
      ↓
Validate Cross-Stage Semantics
      ↓
Validate Score / State Coherence
      ↓
Validate Causal Dedup Metadata
      ↓
Validate Version Compatibility
      ↓
Validate Deterministic Ordering
      ↓
Validate Serialization
      ↓
Publish MingJuDecisionResult
144. COMPOSER VALIDATION PIPELINE
MingJuDecisionResult
      ↓
Validate Source Result
      ↓
Compose
      ↓
Validate Message Keys
      ↓
Validate Source Requirements
      ↓
Validate Confidence Language
      ↓
Validate Contradictions
      ↓
Validate Evidence Mapping
      ↓
Publish MingJuComposedDecision
145. PUBLISHABILITY
Recommended concept:
is_publishable(result)
Return true only when:
no critical validation failures
no unresolved technical errors
schema valid
reference integrity valid
Domain status may still be:
partial
unresolved
and remain publishable if explicitly represented.
146. UNRESOLVED CAN BE PUBLISHABLE
Example:
status = unresolved
grade = UNRESOLVED
can still be a valid/publishable analytical result.
This is different from:
invalid_input
147. INVALID INPUT IS NOT PUBLISHABLE AS ANALYSIS
invalid_input may be returned,
but should not be shown as if it were a real Mệnh Cục conclusion.
148. VALIDATION MUST NOT “FIX” DATA
Validator must not silently:
change Grade
drop Damage
invent Rescue
normalize semantic contradictions
It reports violations.
149. REPAIR BELONGS TO SOURCE STAGE
If validation finds:
wrong Pattern family
repair Pattern adapter/engine.
If:
orphan Rescue
repair Rescue stage.
Do not patch inside validator.
150. CROSS-STAGE INVARIANT MATRIX
Source Stage	Dependent Stage	Mandatory Relationship
Pattern	Purity	Purity cannot silently replace Pattern
Pattern	Strength	Strength uses accepted Pattern
Damage	Rescue	Rescue must target existing Damage
Damage + Rescue	Integrity	Residual Damage must preserve source
Integrity	Grade	Grade downstream only
Integrity	Achievement	Achievement must respect structural usability
Achievement	Career	Career uses Achievement profile
Wealth	Career	Entrepreneurial/commercial career uses Wealth context
Decision	Composer	Composer cannot create new analytical truth


151. MINIMUM VALIDATION BEFORE PHASE 1 FREEZE
For MC-01A–D at minimum validate:
context
pattern
purity
pattern_strength
support
damage
rescue
integrity
grade
trace
versions
serialization
determinism
Achievement/Wealth/Career validators may activate later.
152. PHASED VALIDATION POLICY
Recommended:
MC-01A–D
→ structural validators mandatory

MC-01E
→ Achievement validators enabled

MC-01F
→ Wealth validators enabled

MC-01G/H
→ Career/authority validators enabled

MC-01I
→ Composer validators enabled

MC-01J
→ Runtime / parity validators enabled
153. TEST FAILURE POLICY
A validation test must FAIL when a frozen invariant is broken.
Do not weaken assertions merely to pass runtime tests.
154. WARNING-ONLY CONDITIONS
Possible warning-only cases:
missing hour pillar
low Pattern confidence
missing optional relations
low rule coverage in secondary Achievement domain
unless they become critical to the current decision.
155. ERROR CONDITIONS
Examples:
orphan Rescue
invalid Grade with unresolved Integrity
score out of range
unsupported enum
invalid Pattern family
message key incompatible with source state
156. CRITICAL CONDITIONS
Examples:
schema corruption
duplicate contradictory canonical IDs
broken core references
result claims resolved Grade without valid Integrity
mutated upstream truth
nondeterministic canonical result
157. VALIDATION LOGGING
Recommended logs:
analysis_id
validation_status
error_count
warning_count
critical_count
failed_invariants
Do not log excessive private customer details.
158. VALIDATION REPORT
Recommended development artifact:
MC01_VALIDATION_REPORT
Fields:
schema
ruleset
status
passed_invariants
failed_invariants
warnings
reference_integrity
determinism
serialization
159. ACCEPTANCE CHECK
A result is structurally valid only if:
all mandatory invariants pass
references are intact
scores/states are coherent
versions are compatible
ordering is deterministic
no hidden mutation exists
160. ARCHITECTURAL DECISION
Canonical rule:
VALIDATION MUST PROTECT THE INFERENCE CHAIN, NOT ONLY THE FINAL OUTPUT.

And:
A RESULT WITH A PLAUSIBLE GRADE BUT BROKEN EVIDENCE, DAMAGE/RESCUE REFERENCES, OR CROSS-STAGE SEMANTICS IS INVALID.

161. FINAL VALIDATION MODEL
Valid MC-01 Result
=
Valid Input
+ Valid Stage Outputs
+ Valid Cross-References
+ Valid Cross-Stage Semantics
+ Valid State/Score Coherence
+ Valid Causal Accounting
+ Valid Versions
+ Deterministic Serialization
162. FREEZE TARGET
Before moving to Test Strategy, freeze:
validation severity model
input validation
score/confidence ranges
Pattern invariants
Purity invariants
Pattern Strength invariants
Damage invariants
Rescue target integrity
Residual Damage integrity
Integrity/Grade relationship
Achievement dependencies
Wealth direction rules
Career dependencies
Composer parity rules
trace validation
reference uniqueness
causal duplication rules
version validation
determinism rules
publishability rules
163. NEXT DOCUMENT
Next:
14_TEST_STRATEGY.md
Purpose:
- define unit tests
- define rule tests
- define cross-stage tests
- define Golden Dataset strategy
- define negative tests
- define metamorphic tests
- define determinism tests
- define snapshot tests
- define runtime integration tests
- define report/UI parity tests
- define expert-validation workflow
- define regression gates before MC-01 freeze

Điểm quan trọng nhất của file này là chúng ta đã khóa được nguyên tắc: **MC-01 không chỉ test “ra kết quả gì”, mà phải test “ra kết quả đó bằng chuỗi suy luận nào”**.

Bước tiếp theo là `14_TEST_STRATEGY.md`. File này sẽ biến toàn bộ các invariant ở trên thành kế hoạch test thực tế: unit, Golden Case, negative case, determinism, snapshot, runtime, UI/PDF parity và test phản biện chuyên gia.