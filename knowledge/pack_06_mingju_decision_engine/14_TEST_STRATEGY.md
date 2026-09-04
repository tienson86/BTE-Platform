# MC-01 — TEST STRATEGY

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `14_TEST_STRATEGY.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`  
**Ruleset target:** `bte.mingju.rules.v1`

---

# 1. PURPOSE

This document defines the canonical testing strategy for MC-01 — Mệnh Cục Decision Engine.

The strategy must verify:

- data-model correctness
- rule correctness
- stage correctness
- cross-stage consistency
- evidence integrity
- trace integrity
- Damage/Rescue linkage
- Structural Integrity synthesis
- Grade correctness
- Achievement correctness
- Wealth correctness
- Career correctness
- Composer correctness
- deterministic runtime behavior
- serialization stability
- Orchestrator integration
- UI / Report / PDF / DOCX parity
- expert agreement / disagreement handling
- regression safety

Testing must validate the inference path,
not merely the final label.

---

# 2. CORE TESTING PRINCIPLE

Canonical rule:

```text
TEST THE REASONING CONTRACT,
NOT ONLY THE FINAL ANSWER.
Bad test:
expected Grade = A
Better:
expected Pattern = Chính Quan
expected Purity = pure/moderately_pure
expected Strength = strong
expected Damage = hurting_officer_attacks_officer
expected Rescue = seal_controls_hurting_officer
expected Integrity = damaged_but_rescued
expected Grade = A/B
The second form protects the inference chain.
3. TEST PYRAMID
Recommended layers:
Rule Unit Tests
      ↓
Stage Unit Tests
      ↓
Cross-Stage Contract Tests
      ↓
Golden Dataset Tests
      ↓
Negative / Adversarial Tests
      ↓
Metamorphic Tests
      ↓
Serialization / Determinism Tests
      ↓
Orchestrator Integration Tests
      ↓
Portal / Report Parity Tests
      ↓
Live Runtime Acceptance
No single layer is sufficient.
4. TEST CATEGORIES
Canonical categories:
unit
rule
contract
cross_stage
golden
negative
metamorphic
determinism
snapshot
integration
runtime
parity
expert_validation
regression
5. UNIT TESTS
Unit tests validate isolated functions and models.
Targets include:
enum validation
normalization
classification
score range
confidence range
ID generation
ordering
serialization helpers
message-key mapping
Examples:
normalize "chinh_quan"
→ zheng_guan
confidence = 1.2
→ validation failure
6. MODEL TESTS
Every canonical model should have tests for:
valid construction
invalid construction
nullability
enum validation
serialization
round-trip reconstruction
deterministic field ordering
Models include:
MingJuContext
PatternDecision
PatternPurityResult
PatternStrengthResult
DamageFinding
RescueFinding
StructuralIntegrityResult
PatternGradeResult
AchievementProfile
WealthProfile
CareerProfile
MingJuComposedDecision
7. RULE UNIT TESTS
Every frozen rule must have at least:
one positive match test
one negative match test
one boundary test
Where relevant:
one exception test
one competing-rule test
8. RULE TEST NAMING
Recommended format:
test_{rule_id}_matches_when_conditions_met
test_{rule_id}_does_not_match_when_condition_missing
test_{rule_id}_respects_exception
Example:
test_mc_dmg_guan_001_matches_strong_shang_guan_attack
9. RULE POSITIVE TEST
Example:
primary = zheng_guan
shang_guan active = true
shang_guan strong = true
direct relation = true
Expected:
Damage:
hurting_officer_attacks_officer
10. RULE NEGATIVE TEST
Example:
primary = zheng_guan
shang_guan hidden = true
shang_guan very weak = true
direct relation = false
Forbidden:
major hurting_officer_attacks_officer
11. RULE BOUNDARY TEST
If a rule requires:
source strength >= moderate
test:
minor
moderate
strong
to verify exact boundary behavior.
12. RULE EXCEPTION TEST
Example:
General:
Quan + Sát meaningful
→ mixed_officer_killer candidate
Exception:
valid cong_guan_sha
Expected:
ordinary mixed_officer_killer rule does not fire
13. PATTERN RECOGNITION TESTS
Must cover:
standard pattern
secondary pattern
root prosperity
follow pattern
transformation
special structure
unknown pattern ID
unresolved pattern
conflicting pattern evidence
legacy alias normalization
14. PURITY TESTS
Required categories:
pure standard pattern
minor counterpart mixing
major counterpart mixing
root/exposure consistency
root/exposure mismatch
hidden competitor
visible competitor
coherent chain
fragmented structure
follow purity
transformation purity
15. STRENGTH TESTS
Must verify:
season contribution
root contribution
exposure contribution
generation contribution
continuity
position
weakening
family-specific handling
Critical test:
Day Master strong
Pattern weak
must remain possible.
Also:
Day Master weak
Pattern very strong
must remain possible.
16. DAMAGE TESTS
Must cover all canonical damage families.
At minimum:
hurting_officer_attacks_officer
owl_robs_food
peer_robs_wealth
mixed_officer_killer
wealth_overloads_weak_day_master
killer_overloads_weak_day_master
resource_overload
root_destroyed
pattern_deity_controlled
pattern_deity_combined_away
generator_destroyed
structural_chain_broken
follow_structure_counterforce
transformation_disrupted
17. DAMAGE NON-AUTOMATIC TESTS
Mandatory tests must prove:
Thương + Quan
≠ automatic major damage

Kiêu + Thực
≠ automatic damage

Tỷ/Kiếp + Tài
≠ automatic đoạt Tài

Quan + Sát
≠ automatic damaging mixture

xung
≠ automatic Damage
These are high-priority regression tests.
18. RESCUE TESTS
Must cover:
seal_controls_hurting_officer
seal_transforms_killer
officer_controls_peer
resource_restores_structure
wealth_bridges_structure
output_releases_excess
root_restoration
generator_restoration
structural_chain_repair
follow_counterforce_removed
transformation_stabilized
19. RESCUE TARGET TEST
Every Rescue test must verify:
target_damage_ids
references the correct Damage.
20. ORPHAN RESCUE TEST
Input:
no Damage
Attempted:
RescueFinding exists
Expected:
validation failure
This is mandatory.
21. SUPPORT VS RESCUE TEST
Example:
Tài sinh Quan
with no Damage.
Expected:
Support
Forbidden:
Rescue
22. DAMAGE HISTORY TEST
Input:
major Damage
strong Rescue
Expected:
Damage remains
Rescue exists
Residual Damage reduced
Forbidden:
Damage deleted
23. STRUCTURAL INTEGRITY TESTS
Must cover:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
Each state requires at least one Golden Case.
24. STRUCTURAL STATE PATH TEST
Tests must validate not only state,
but why that state was selected.
Example:
major original Damage
strong valid Rescue
minor residual Damage
Expected:
damaged_but_rescued
not:
complete
25. FAILED STATE TEST
failed should require:
core function lost
major/critical residual Damage
no adequate Rescue
Test must ensure:
low Purity only
cannot produce failed.
26. GRADE TESTS
Every Grade test should include:
Integrity state
Integrity score
Grade
confidence
basis
27. GRADE NEGATIVE TESTS
Mandatory:
very_strong Pattern
+ critical Damage
+ no Rescue
≠ SS/S automatically
very_pure
+ weak Pattern
+ major Damage
≠ SS automatically
strong Rescue
+ critical partially-resolved Damage
≠ complete automatically
28. GRADE / INTEGRITY GUARD TEST
Input:
Integrity = unresolved
Expected:
Grade = UNRESOLVED
No exception.
29. ACHIEVEMENT TESTS
Each dimension should eventually have dedicated tests:
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
30. ACHIEVEMENT DIMENSION INDEPENDENCE TEST
Example:
leadership high
management moderate
must remain possible.
Also:
entrepreneurship very_high
stability low
must remain possible.
31. NO UNIVERSAL SUCCESS TEST
Ensure no canonical logic derives:
success_score
as the sole or dominant Achievement output.
32. AUTHORITY TESTS
Cover:
strong Chính Quan
strong Sát–Ấn
damaged Quan
rescued Quan
weak Quan
Quan present but irrelevant
33. ENTREPRENEURSHIP TESTS
Cover:
Thiên Tài strong
Thực→Tài
Thương→Tài
independence high
management weak
high entrepreneurship + poor retention
34. WEALTH TESTS
Must separately test:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
35. WEALTH DIMENSION SEPARATION TEST
Required scenario:
wealth_creation = high
wealth_retention = low
financial_volatility = high
This combination must be valid.
36. WEALTH OVERLOAD TEST
Input:
Tài very strong
Day Master capacity insufficient
Expected:
wealth opportunity may remain high
retention reduced
volatility increased
Forbidden:
all Wealth dimensions low
37. WEALTH STABLE ACCUMULATOR TEST
Input:
creation moderate
retention very_high
stability high
volatility low
Expected:
accumulation high
This confirms “kiếm chậm nhưng giữ tốt” profile.
38. VOLATILITY DIRECTION TEST
Input:
financial_volatility = 82
Expected:
classification = high/very_high risk
score_direction = higher_is_riskier
Forbidden:
positive capability wording
39. TỶ KIẾP WEALTH TESTS
Cover:
Tỷ/Kiếp present but harmless
peer_robs_wealth active
peer robbery rescued by Quan
This protects against simplistic presence rules.
40. CAREER TESTS
Must cover:
institutional leader
entrepreneurial builder
technical specialist
academic specialist
creative independent
public-facing leader
hybrid profile
41. CAREER TRADE-OFF TESTS
Required:
institutional high
autonomy very_high
Expected:
structured environment
+
decision authority required
not contradictory output.
42. LEADERSHIP VS MANAGEMENT TEST
Input:
leadership very_high
management low
Expected:
leader potential preserved
management risk surfaced
43. ENTREPRENEURSHIP VS WEALTH TEST
Input:
entrepreneurship very_high
wealth_creation high
wealth_retention low
Expected:
entrepreneurial fit high
capital-control risk high
not:
entrepreneurial fit low
44. CAREER NO EXACT JOB TEST
Canonical CareerProfile must not output:
CEO
doctor
judge
teacher
as deterministic inference.
45. COMPOSER TESTS
Composer tests must verify:
message-key selection
priority
deduplication
trade-off handling
confidence language
unresolved wording
structural parity
wealth parity
career parity
46. COMPOSER NO-NEW-INFERENCE TEST
Feed a DecisionResult without:
authority high
Composer must not invent:
"có số làm quan"
47. COMPOSER DAMAGE/RESCUE TEST
Input:
Damage major
Rescue strong
Integrity damaged_but_rescued
Expected wording must preserve:
có phá
+
có cứu
Forbidden:
không có phá
48. COMPOSER CONFIDENCE TEST
Input:
leadership high
confidence = 0.42
Expected cautious language.
Forbidden:
"thế mạnh chắc chắn"
49. COMPOSER CONTRADICTION TEST
Input:
institutional_fit high
autonomy very_high
Expected:
structured_with_autonomy
not two contradictory standalone statements.
50. GOLDEN DATASET STRATEGY
Golden Dataset is central to MC-01.
It should contain:
synthetic structural cases
real expert-reviewed charts
boundary cases
counterexamples
unresolved cases
special-pattern cases
Do not rely only on one case such as CASE-0001.
51. GOLDEN DATASET PURPOSE
Golden cases validate:
rule semantics
stage semantics
accepted expert conclusions
forbidden conclusions
reasoning path
They are not just snapshots.
52. GOLDEN CASE TYPES
Recommended categories:
G-STD
G-MIX
G-DMG
G-RSC
G-INT
G-GRD
G-ACH
G-WLT
G-CAR
G-CONG
G-HUA
G-NEG
G-UNRESOLVED
53. GOLDEN CASE STRUCTURE
Recommended:
{
  "case_id": "MC-G-DMG-001",

  "input": {},

  "expected": {
    "pattern": {},
    "purity": {},
    "strength": {},
    "damage": {},
    "rescue": {},
    "integrity": {},
    "grade": {}
  },

  "forbidden": {},

  "accepted_alternatives": {},

  "expert_notes": []
}
54. GOLDEN EXPECTATIONS SHOULD BE STRUCTURAL
Prefer:
must_include_damage
must_not_include_damage
must_include_rescue
integrity_state
allowed_grade_range
over:
exact score = 78.43
until calibration is frozen.
55. SCORE RANGE GOLDENS
Before numeric weights freeze,
use ranges:
purity_score: 70..90
strength_score: 65..85
After calibration,
exact or tighter ranges may be frozen.
56. ACCEPTED ALTERNATIVES
When expert traditions legitimately differ:
accepted_primary = [zheng_guan, qi_sha]
required_state = conflicting_evidence
or:
allowed_grade = [A, B]
This is better than forcing one false certainty.
57. EXPERT ANNOTATION
Each expert-reviewed Golden Case should record:
expert conclusion
confidence
reasoning summary
points of disagreement
source tradition if relevant
Do not store expert identity as inference data.
58. EXPERT CONSENSUS LEVEL
Possible metadata:
high_consensus
moderate_consensus
contested
This helps determine strictness of assertions.
59. HIGH-CONSENSUS CASE
Use strict assertions:
must match
60. CONTESTED CASE
Use:
accepted alternatives
required uncertainty
forbidden overconfidence
61. NEGATIVE TEST STRATEGY
Negative tests are mandatory because MC-01 is vulnerable to classical-rule overfiring.
Targets:
false Tòng
false Hóa
false Quan/Sát damage
false Kiêu đoạt Thực
false Tỷ Kiếp đoạt Tài
false wealth-rich conclusion
false authority conclusion
false career mapping
62. FALSE TÒNG TEST
Scenario:
candidate follow structure
but Day Master has meaningful root/support
Expected:
follow not resolved
or upstream rejection preserved
63. FALSE HÓA TEST
Scenario:
stem combination exists
but transformation conditions incomplete
Expected:
hua_qi not resolved
64. FALSE WEALTH TEST
Scenario:
Tài very strong
Day Master very weak
peer pressure strong
Forbidden:
wealth_retention very_high
65. FALSE AUTHORITY TEST
Scenario:
Quan present
Quan very weak
major Damage
Forbidden:
authority very_high
66. FALSE CAREER TEST
Scenario:
Chính Quan present
Achievement institutional low
Forbidden:
structured_institutional automatically primary
67. METAMORPHIC TESTING
Metamorphic tests verify that controlled input changes produce logically consistent output changes.
This is important when exact answer is difficult to specify.
68. METAMORPHIC EXAMPLE — ADD ROOT
Base:
Quan exposed
no root
Mutation:
add strong valid Quan root
Expected:
Pattern Strength should not decrease
unless another explicit effect dominates.
69. METAMORPHIC EXAMPLE — REMOVE RESCUE
Base:
major Damage
strong Rescue
Mutation:
remove Rescue source
Expected:
Residual Damage should not improve
Integrity should not improve
70. METAMORPHIC EXAMPLE — ADD PEER PRESSURE
Base:
wealth_retention high
Mutation:
add strong active peer_robs_wealth
Expected:
wealth_retention should not increase
financial_volatility should not decrease
unless compensating Rescue is also added.
71. METAMORPHIC EXAMPLE — REMOVE DAMAGE
Base:
damaged_but_rescued
Mutation:
remove damaging source entirely
Expected:
state should not remain damaged_but_rescued
It may become:
complete
substantially_complete
mixed
depending on remaining structure.
72. METAMORPHIC EXAMPLE — BIOGRAPHY
Add:
job_title = CEO
income = high
Expected:
no change in canonical natal result
This test is mandatory.
73. METAMORPHIC EXAMPLE — CURRENT YEAR
Change execution date or current year.
Expected:
no change in natal MC-01 result
74. DETERMINISM TESTS
Given:
same context
same ruleset
repeated runs must produce:
same values
same IDs
same ordering
same serialized payload
75. MULTI-RUN DETERMINISM
Recommended test:
run analyze_mingju 100 times
Expected:
one unique normalized result hash
76. RULE ORDER DETERMINISM
Changing internal iteration order of a rule registry must not change result,
unless priority semantics intentionally change.
77. SERIALIZATION DETERMINISM
Ensure:
sets are sorted
maps normalized
floats normalized
trace ordered
IDs deterministic
78. HASH TEST
If decision_hash exists:
same result
→ same hash
79. SNAPSHOT TESTS
Snapshots are useful for full structured payloads.
But snapshots must not replace semantic assertions.
Use snapshots for:
schema shape
ordering
IDs
trace structure
serialized contract
80. SNAPSHOT UPDATE POLICY
Do NOT automatically update snapshots after failing tests.
Every snapshot change must be reviewed for:
intentional ruleset change
schema change
bug fix
81. CROSS-STAGE CONTRACT TESTS
Must verify:
Pattern → Purity
Pattern → Strength
Damage → Rescue
Damage + Rescue → Integrity
Integrity → Grade
Integrity → Achievement
Achievement + Wealth → Career
Decision → Composer
82. DAMAGE→RESCUE CONTRACT TEST
For every Rescue:
target damage exists
target type compatible
mechanism compatible
83. INTEGRITY→GRADE CONTRACT TEST
For every resolved Grade:
Integrity resolved
Grade integrity_state matches
score/state combination valid
84. ACHIEVEMENT→CAREER CONTRACT TEST
Career high-confidence result requires adequate Achievement evidence.
85. WEALTH→CAREER CONTRACT TEST
High entrepreneurial Career fit should consider:
wealth_creation
business_expansion
retention/volatility context
86. COMPOSER CONTRACT TEST
Every material composed section must reference:
source paths
or evidence IDs
87. ORCHESTRATOR INTEGRATION TESTS
Test actual pipeline:
Calendar
→ BaZi
→ Strength
→ Pattern
→ Useful God
→ MC-01
Verify upstream truth reaches MingJuContext unchanged.
88. UPSTREAM IMMUTABILITY TEST
Before MC-01:
serialize upstream result
After MC-01:
serialize upstream result
Expected:
identical
MC-01 must not mutate upstream facts.
89. ORCHESTRATOR ATTACHMENT TEST
Verify canonical result is attached at one stable path:
analysis.mingju
or final frozen path.
No duplicate semantic copies.
90. NO SECONDARY ROUTING TEST
Ensure Portal/Report does not use a legacy alternative Mệnh Cục calculation path.
91. LIVE RUNTIME TESTS
Live runtime must verify:
POST analyze
→ MC-01 runs
→ result persisted
→ /result reads same MingJuDecisionResult
92. RUNTIME RESULT ID TEST
The same analysis ID must propagate through:
analysis
mingju
result page
report
export
This protects routing correctness.
93. UI PARITY TESTS
Portal must not independently alter analytical truth.
Verify:
pattern label
purity
strength
damage
rescue
integrity
grade
achievement
wealth
career
match canonical result.
94. REPORT PARITY TESTS
PDF/DOCX/Report should use identical canonical values.
Example:
/result:
Grade A

PDF:
Grade A

DOCX:
Grade A
95. NARRATIVE PARITY TESTS
If:
wealth_retention = low
then no output surface may say:
giữ tiền rất tốt
96. COMPOSER MODE PARITY
dashboard, commercial, technical, report may differ in detail.
They must not differ in analytical truth.
97. FRONTEND NO-LOGIC TEST
Static tests should scan for forbidden duplicated business rules.
Examples:
authority > 70 → làm quan
wealth_creation > 70 → giàu
grade == A → high success
These should not exist in presentation code.
98. REPORT NO-LOGIC TEST
Similarly, report templates must not calculate:
Grade
Integrity
wealth classification
career fit
99. COMPOSER TEMPLATE TESTS
Every message key should have:
positive selection test
negative selection test
incompatible source test
confidence-language test
100. EXPERT VALIDATION WORKFLOW
Recommended workflow:
1. Select chart
2. Hide engine result
3. Experts classify manually
4. Record evidence and uncertainty
5. Run MC-01
6. Compare stage-by-stage
7. Review disagreement
8. Decide:
   engine bug
   rule ambiguity
   expert disagreement
   insufficient data
9. Update rules only with documented reason
101. DO NOT TUNE DIRECTLY TO OUTCOME
Forbidden workflow:
customer is rich
→ modify engine until Wealth = high
Correct:
review structural evidence
→ determine whether rule logic is wrong
Observed biography is validation evidence,
not target truth by itself.
102. EXPERT BLIND VALIDATION
Where possible,
experts should not see engine output before giving initial judgment.
This reduces confirmation bias.
103. MULTI-EXPERT REVIEW
For difficult cases:
2–3 expert assessments
may be recorded separately.
Do not force artificial consensus.
104. DISAGREEMENT CLASSIFICATION
Recommended:
rule_error
data_error
tradition_difference
interpretive_difference
insufficient_evidence
105. EXPERT DISAGREEMENT TEST
If experts disagree strongly,
Golden Case may require:
engine returns uncertainty
instead of arbitrary certainty.
106. REGRESSION TEST STRATEGY
Every production bug must add:
minimal regression test
before closing the ticket.
107. REGRESSION TEST NAMING
Recommended:
test_regression_{ticket_id}_{short_description}
Example:
test_regression_mc01_false_guan_sha_damage
108. RULESET CHANGE REGRESSION
Whenever ruleset changes:
run all Golden Cases
run all negative cases
run all snapshots
compare diff
109. EXPECTED DIFF REVIEW
Ruleset changes must produce a report:
changed cases
unchanged cases
new unresolved cases
grade changes
wealth changes
career changes
No silent bulk changes.
110. GOLDEN DRIFT REPORT
Recommended artifact:
MC01_GOLDEN_DRIFT_REPORT.md
Fields:
ruleset before
ruleset after
case ID
old result
new result
reason
approved yes/no
111. TEST DATA SEPARATION
Recommended folders:
tests/mingju/
├── unit/
├── rules/
├── contract/
├── golden/
├── negative/
├── metamorphic/
├── snapshots/
├── integration/
└── runtime/
112. GOLDEN DATA LOCATION
Recommended:
knowledge/golden/mingju/
or existing BTE canonical Golden Dataset location if one is already frozen.
Do not create competing Golden roots.
113. GOLDEN CASE FILE FORMAT
Recommended:
JSON or YAML
Requirements:
stable field order
human-readable
machine-validated
versioned
114. TEST FIXTURE PRINCIPLE
Fixtures should represent:
canonical facts
not UI payloads.
Avoid building core tests from frontend view models.
115. SYNTHETIC CASES
Synthetic cases are useful for isolating rules.
Example:
only Quan + Thương relationship
This helps prove one rule without unrelated chart noise.
116. REAL CHART CASES
Real charts are necessary for:
interaction effects
multiple competing rules
traditional interpretation
commercial realism
Use both synthetic and real cases.
117. BOUNDARY CASES
Must include:
just below threshold
at threshold
just above threshold
for every frozen numeric threshold.
118. UNRESOLVED CASES
Test that engine can validly return:
unresolved
for:
Pattern conflict
Transformation uncertainty
insufficient relation data
missing critical upstream facts
119. PARTIAL CASES
Test:
core structure resolved
Career incomplete
Expected:
status = partial
not failure.
120. INVALID INPUT CASES
Test:
bad enum
bad score
bad confidence
malformed Pattern
broken Rescue reference
unknown version
121. PERFORMANCE TESTING
MC-01 should be in-memory and deterministic.
Performance tests should ensure no severe regression.
Suggested initial target:
single chart analysis comfortably below interactive latency budget
Do not optimize at expense of correctness.
Exact threshold may be frozen later.
122. BATCH PERFORMANCE
Future test:
1000 charts
to detect pathological rules or O(N²) growth.
123. MEMORY TESTING
Trace/evidence should not grow uncontrollably.
Test maximum reasonable:
evidence count
trace count
rule match count
for one chart.
124. PROPERTY TESTING
Where useful, property-based tests may validate invariants such as:
scores remain 0..100
confidence remains 0..1
no orphan Rescue
all IDs unique
deterministic serialization
125. FUZZ TESTING
Light fuzzing may be applied to:
model parsing
enum inputs
null combinations
serialization
Do not fuzz domain rules blindly without meaningful constraints.
126. MUTATION TESTING
Recommended later for critical rule modules.
Purpose:
change condition operator
remove guard
flip boolean
and verify tests fail.
High-value modules:
Damage
Rescue
Integrity
Grade
127. TRACE TESTING
Tests should verify:
rule ID present
evidence IDs present
stage correct
output ID valid
sequence deterministic
128. TRACE COVERAGE
Every major material conclusion must have at least one trace path.
129. EXPLAINABILITY TEST
Given a resolved Grade,
test harness should be able to reconstruct:
Pattern
→ Purity
→ Strength
→ Damage
→ Rescue
→ Integrity
→ Grade
from structured trace.
130. EVIDENCE COVERAGE TEST
Every:
major Damage
major Rescue
high Achievement dimension
high Wealth dimension
primary Career recommendation
should have evidence references.
131. CAUSAL DUPLICATION TEST
Construct a case where one branch clash creates:
root destroyed
continuity reduced
Expected:
causal metadata links them
and aggregate result does not apply uncontrolled duplicate penalty.
132. SUPPORT/RESCUE DUPLICATION TEST
Same Ấn may:
support Day Master
rescue Sát overload
Expected:
two roles preserved
causal overlap controlled
133. SCORE CALIBRATION TESTS
Before weight freeze,
tests should assert:
relative ordering
acceptable band
state consistency
not exact decimals.
134. POST-CALIBRATION TESTS
After weights freeze,
tighten tests to:
exact thresholds
narrow score ranges
grade mappings
135. CALIBRATION DATASET
Use a separate labeled dataset for tuning.
Do not calibrate and evaluate on exactly the same cases.
Recommended split:
development/calibration set
validation set
holdout regression set
136. HOLDOUT TESTS
Maintain a set of expert-reviewed charts that are not used for rule tuning.
Purpose:
detect overfitting
137. OVERFITTING GUARD
If tuning improves calibration cases but worsens holdout cases,
do not freeze.
138. CASE DIVERSITY
Golden/holdout sets should include variation across:
Day Masters
seasons
strong/weak Day Master
standard patterns
follow patterns
transformation
mixed structures
different Damage types
different Rescue types
139. NO SINGLE-CASE DEVELOPMENT
CASE-0001 may be a runtime reference,
but MC-01 correctness must not be determined by CASE-0001 alone.
140. CUSTOMER REPORT ACCEPTANCE TEST
Full customer report should be reviewed for:
coherence
non-contradiction
evidence parity
actionability
uncertainty honesty
141. COMMERCIAL QUALITY TEST
A report should fail commercial acceptance if it is:
generic
repetitive
contradictory
untraceable
overconfident
even if the code technically passes.
142. UI ACCEPTANCE TEST
Mệnh Cục display should present canonical values without hiding important structural state.
Minimum:
pattern
integrity state
grade
purity
strength
damage/rescue indicator
depending on final UI design.
143. ACCESSIBILITY / PRESENTATION TEST
Presentation tests may verify:
risk vs positive metric visually distinguishable
volatility not displayed as positive
unresolved clearly labeled
144. TEST GATES
Recommended gates:
Gate A — Model / Contract
Gate B — Structural Rules
Gate C — Golden Dataset
Gate D — Determinism
Gate E — Runtime Integration
Gate F — UI/Report Parity
Gate G — Expert Acceptance
Gate H — Final Freeze
145. GATE A — MODEL / CONTRACT
PASS requires:
all models valid
all enums valid
serialization valid
versioning valid
validation invariants pass
146. GATE B — STRUCTURAL RULES
PASS requires:
Pattern
Purity
Strength
Damage
Rescue
Integrity
Grade
unit/rule tests pass.
147. GATE C — GOLDEN DATASET
PASS requires:
all high-consensus cases pass
no forbidden conclusions
accepted alternatives respected
148. GATE D — DETERMINISM
PASS requires:
multi-run identical result
stable IDs
stable ordering
stable serialization
149. GATE E — RUNTIME INTEGRATION
PASS requires:
Orchestrator uses canonical API
one result path
upstream truth unchanged
live analyze result contains mingju
150. GATE F — UI/REPORT PARITY
PASS requires:
/result
report
PDF
DOCX
all show same canonical MC-01 truth.
151. GATE G — EXPERT ACCEPTANCE
PASS requires:
expert-reviewed sample set
material disagreements documented
no unresolved critical methodological issue
152. GATE H — FINAL FREEZE
PASS requires:
all prior gates PASS
ruleset version frozen
schema frozen
Golden Dataset snapshot frozen
known limitations documented
153. REQUIRED CI SUITES
Recommended CI suites:
mc01_unit
mc01_rules
mc01_contract
mc01_golden
mc01_negative
mc01_determinism
mc01_integration
mc01_parity
154. FAST CI
For every commit:
unit
rules
contract
negative smoke
determinism smoke
155. FULL CI
Before merge/release:
all Golden
all negative
metamorphic
snapshots
integration
runtime
parity
156. EXPERT SUITE
Expert validation does not need to run on every commit.
Run when:
rule semantics change
Grade thresholds change
Wealth model changes
Career model changes
ruleset release candidate created
157. TEST REPORT
Recommended artifact:
MC01_TEST_REPORT.md
Fields:
schema version
ruleset version
test commit
suite results
Golden pass rate
negative pass rate
determinism status
integration status
parity status
known failures
158. GOLDEN PASS RATE
For frozen high-consensus cases:
100% required
for release.
Do not use:
95% is good enough
for known canonical cases.
159. CONTESTED CASE PASS POLICY
A contested case passes when:
engine result lies within accepted alternatives
uncertainty is represented correctly
forbidden overconfidence absent
160. TEST FAILURE CLASSIFICATION
Recommended:
engine_bug
rule_bug
contract_bug
data_fixture_bug
test_bug
expected_ruleset_change
expert_disagreement
runtime_integration_bug
presentation_parity_bug
161. FAILURE TRIAGE
Do not immediately change rules after a failed Golden test.
Investigate in order:
1. Input truth
2. Adapter
3. Pattern
4. Rule match
5. Evidence
6. Cross-stage effect
7. Aggregation
8. Expected Golden annotation
162. TEST MUST NOT PATCH PRODUCTION
Tests should never contain production semantic fixes.
Bad:
if CASE-0001:
    expected = A
Production and test data remain separated.
163. KNOWN LIMITATIONS TEST
Known unsupported structures should explicitly test:
unresolved
rather than silently skip.
164. SPECIAL PATTERN COVERAGE
Every formally supported special/follow/transformation pattern must have:
one positive Golden case
one negative candidate case
one damaged case where applicable
165. RELEASE BLOCKERS
Release blockers include:
orphan Rescue
non-deterministic result
Grade without Integrity
UI/report truth mismatch
false resolved Tòng/Hóa
biography affecting natal result
current year affecting natal result
untraceable major conclusion
166. NON-BLOCKING WARNINGS
Potential:
secondary Career dimension low confidence
missing optional technical summary
non-critical wording polish
provided canonical structural truth is correct.
167. TEST STRATEGY INVARIANTS
TST-01
Every frozen rule has positive and negative tests.
TST-02
Every major stage has unit tests.
TST-03
Every Structural Integrity state has a Golden Case.
TST-04
Every major Damage type has a test.
TST-05
Every major Rescue type has a test.
TST-06
Grade is never tested without Integrity path.
TST-07
Wealth dimensions are tested separately.
TST-08
Career fit is not tested from raw Ten-God labels alone.
TST-09
Biography and current date independence are explicitly tested.
TST-10
Determinism is a release gate.
TST-11
UI/Report/PDF/DOCX parity is a release gate.
TST-12
Golden tests validate reasoning path, not only final labels.
168. FAILURE CONDITIONS
Testing strategy FAILS if:
1. only final Grade is tested
2. CASE-0001 is the only real chart
3. no negative tests exist
4. no false-Tòng / false-Hóa tests exist
5. Damage/Rescue linkage is not tested
6. no determinism tests exist
7. no biography-independence test exists
8. no current-year-independence test exists
9. no UI/report parity test exists
10. expert disagreement is forced into one answer
11. snapshots are auto-updated without review
12. rules are tuned directly to known biographies
169. ACCEPTANCE PRINCIPLE
MC-01 testing is accepted only when the system can demonstrate:
Correct facts
→ Correct rule matches
→ Correct evidence
→ Correct findings
→ Correct cross-stage synthesis
→ Correct structural state
→ Correct Grade
→ Correct domain profiles
→ Correct customer wording
and each arrow is independently testable.
170. ARCHITECTURAL DECISION
Canonical rule:
MC-01 RELEASE QUALITY IS DETERMINED BY STRUCTURAL REASONING CONSISTENCY, NOT BY WHETHER A FEW SAMPLE CHARTS “LOOK RIGHT”.

And:
GOLDEN DATASET, NEGATIVE TESTING, DETERMINISM, AND RUNTIME PARITY ARE MANDATORY RELEASE GATES.

171. FINAL TEST MODEL
MC-01 Confidence
=
Rule Tests
+ Structural Golden Cases
+ Negative Cases
+ Metamorphic Consistency
+ Determinism
+ Runtime Integration
+ Presentation Parity
+ Expert Review
No single component is sufficient.
172. FREEZE TARGET
Before Acceptance Checklist, freeze:
test categories
Golden Dataset policy
negative-case policy
metamorphic testing
determinism gate
snapshot policy
expert-validation workflow
calibration/holdout separation
runtime integration tests
UI/report parity tests
release gates
regression policy
173. NEXT DOCUMENT
Next:
15_ACCEPTANCE_CHECKLIST.md
Purpose:
- define final architecture acceptance
- define implementation readiness
- define data-model freeze checks
- define rule freeze checks
- define API checks
- define validation checks
- define test gates
- define runtime integration checks
- define UI/report parity checks
- define expert sign-off conditions
- define MC-01 release/freeze criteria

Sau file này, phần thiết kế MC-01 gần như đã kín từ **architecture → data → rule semantics → API → validation → testing**.

Bước tiếp theo nên làm luôn **`15_ACCEPTANCE_CHECKLIST.md`**. Đây sẽ là file cuối của bộ thiết kế MC-01, dùng để quyết định rất rõ: **khi nào được phép giao Cursor bắt đầu implementation, khi nào được tích hợp runtime, và khi nào MC-01 đủ điều kiện FINAL FREEZE**.