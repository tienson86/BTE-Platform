# MC-01 — ACCEPTANCE CHECKLIST

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `15_ACCEPTANCE_CHECKLIST.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`  
**Ruleset target:** `bte.mingju.rules.v1`  
**Composer target:** `bte.mingju.composer.v1`

---

# 1. PURPOSE

This document defines the final acceptance criteria for MC-01 — Mệnh Cục Decision Engine.

It determines when MC-01 is ready for:

```text
DESIGN FREEZE
IMPLEMENTATION START
ENGINE INTEGRATION
RUNTIME INTEGRATION
UI / REPORT BINDING
EXPERT ACCEPTANCE
FINAL FREEZE

No phase may be declared complete without satisfying its mandatory acceptance conditions.
2. CORE ACCEPTANCE PRINCIPLE
Canonical rule:
NO FREEZE BY IMPRESSION.
FREEZE BY VERIFIED CONTRACT.
MC-01 is accepted only when:
architecture is stable
contracts are stable
rules are traceable
invariants are enforced
tests exist
runtime is deterministic
UI/report parity is proven
expert review is completed
3. ACCEPTANCE LEVELS
Canonical levels:
A0 — Documentation Complete
A1 — Design Freeze Ready
A2 — Implementation Ready
A3 — Core Engine PASS
A4 — Runtime Integration PASS
A5 — Presentation Parity PASS
A6 — Expert Validation PASS
A7 — FINAL FREEZE
4. A0 — DOCUMENTATION COMPLETE
A0 requires all MC-01 design files to exist.
Expected document set:
MC01_ARCHITECTURE.md
02_PATTERN_RECOGNITION.md
03_PATTERN_PURITY.md
04_PATTERN_STRENGTH.md
05_PATTERN_DAMAGE.md
06_PATTERN_RESCUE.md
07_PATTERN_GRADE.md
08_ACHIEVEMENT_MODEL.md
09_WEALTH_MODEL.md
10_CAREER_MODEL.md
11_DECISION_COMPOSER.md
12_PUBLIC_API.md
13_VALIDATION_RULES.md
14_TEST_STRATEGY.md
15_ACCEPTANCE_CHECKLIST.md
PASS only when:
all files exist
all files use compatible terminology
no unresolved document-number conflicts
no duplicate ownership definitions
5. DOCUMENT CONSISTENCY CHECK
Before A0 PASS, confirm consistent meanings for:
Pattern
Purity
Pattern Strength
Damage
Rescue
Structural Integrity
Grade
Achievement
Wealth
Career
Composer
No file may redefine these concepts inconsistently.
6. TERMINOLOGY FREEZE
Canonical terminology must be stable.
Examples:
Pattern
= cách cục identity

Purity
= độ thuần / structural clarity

Pattern Strength
= lực cách cục

Damage
= phá cách / structural damage

Rescue
= cứu cách

Structural Integrity
= độ hoàn chỉnh cấu trúc

Grade
= cấp chất lượng cấu trúc
7. OWNERSHIP FREEZE
Before implementation, freeze ownership:
Pattern Engine
→ pattern identity

Strength Engine
→ Day Master strength

Useful God Engine
→ Dụng/Hỷ/Kỵ

MC-01
→ structural synthesis

Composer
→ wording only

Frontend
→ presentation only

Report
→ presentation only
8. A1 — DESIGN FREEZE READY
A1 requires all core conceptual boundaries to be frozen.
Mandatory boundaries:
Pattern ≠ Purity
Purity ≠ Strength
Strength ≠ Damage
Damage ≠ Rescue
Rescue ≠ Support
Grade ≠ Wealth
Achievement ≠ Wealth
Career ≠ exact profession
Natal ≠ Luck activation
Composer ≠ analytical engine
9. PATTERN RECOGNITION ACCEPTANCE
PASS when:
canonical pattern IDs defined
pattern families defined
alias normalization defined
upstream ownership defined
unresolved behavior defined
follow handling defined
transformation handling defined
precedence ownership defined
FAIL if MC-01 is allowed to silently replace Pattern Engine truth.
10. PURITY ACCEPTANCE
PASS when:
Purity definition frozen
same-domain mixing principle frozen
Quan/Sát mixing principle frozen
coherent-chain principle frozen
family-specific purity handling defined
double-counting policy defined
FAIL if:
mixed automatically means damaged
or:
pure automatically means good
11. PATTERN STRENGTH ACCEPTANCE
PASS when:
Pattern Strength separated from Day Master Strength
season dimension defined
root dimension defined
exposure dimension defined
generation dimension defined
continuity dimension defined
position dimension defined
family-specific handling defined
FAIL if:
Thân vượng
→ cách mạnh
is allowed as shorthand.
12. DAMAGE ACCEPTANCE
PASS when:
Damage requires source
Damage requires target
Damage requires mechanism
Damage requires evidence
severity model defined
directness defined
reversibility defined
capacity-mismatch model defined
relation relevance defined
FAIL if:
xung = damage
Thương + Quan = damage
Quan + Sát = damage
automatically.
13. RESCUE ACCEPTANCE
PASS when:
Rescue must target registered Damage
Support/Rescue boundary frozen
mechanism required
strength defined
reliability defined
coverage defined
Damage history preserved
family-specific Rescue defined
FAIL if:
favorable force = Rescue
automatically.
14. INTEGRITY ACCEPTANCE
PASS when all structural states are frozen:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
and state-resolution logic is documented.
15. GRADE ACCEPTANCE
PASS when:
Grade is downstream from Integrity
Grade enum frozen
SS/S/A/B/C/D/UNRESOLVED defined
state guard defined
confidence propagation defined
no direct wealth/status meaning attached
FAIL if:
Grade A = rich
Grade S = official
is allowed.
16. ACHIEVEMENT ACCEPTANCE
PASS when the multi-dimensional profile is frozen:
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
FAIL if implementation uses one universal success score.
17. WEALTH ACCEPTANCE
PASS when five V1 dimensions are frozen:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
and score direction is defined.
FAIL if Wealth is reduced to:
Tài mạnh = giàu
18. CAREER ACCEPTANCE
PASS when Career model defines:
organizational fit
leadership fit
management fit
entrepreneurial fit
specialist fit
technical fit
academic fit
creative fit
public-facing fit
autonomy
career stability
FAIL if one Ten God maps directly to one profession.
19. COMPOSER ACCEPTANCE
PASS when:
Composer cannot create new analytical truth
message-key model defined
confidence wording defined
trade-off model defined
deduplication defined
output modes defined
same source-of-truth policy defined
20. PUBLIC API ACCEPTANCE
PASS when:
one normalized context exists
one canonical analyze entry point exists
one canonical result exists
one Composer entry point exists
version fields frozen
partial/unresolved behavior frozen
frontend/report boundaries frozen
21. VALIDATION ACCEPTANCE
PASS when validators cover:
score ranges
confidence ranges
Pattern invariants
Damage references
Rescue references
Residual Damage references
Integrity/Grade consistency
Achievement dependencies
Wealth direction
Career dependencies
Composer parity
version compatibility
determinism
22. TEST STRATEGY ACCEPTANCE
PASS when testing includes:
unit
rule
contract
cross-stage
Golden Dataset
negative
metamorphic
determinism
snapshot
runtime
parity
expert validation
regression
23. A2 — IMPLEMENTATION READY
A2 means Cursor may begin coding MC-01.
Mandatory preconditions:
A0 PASS
A1 PASS
public models identified
module boundaries frozen
public API frozen enough for implementation
test folder strategy frozen
no critical conceptual TODO remains
24. IMPLEMENTATION MUST NOT START IF
Do NOT start implementation if any of these remain unclear:
who owns Pattern
whether Grade means wealth
whether Support equals Rescue
whether Luck can modify natal Grade
whether UI may infer conclusions
whether Composer may recalculate logic
These are architecture blockers.
25. IMPLEMENTATION PHASES
Recommended implementation sequence:
MC-01A — Models / Context / API skeleton
MC-01B — Pattern Recognition
MC-01C — Purity / Pattern Strength
MC-01D — Damage / Rescue
MC-01E — Structural Integrity / Grade
MC-01F — Achievement
MC-01G — Wealth
MC-01H — Career
MC-01I — Decision Composer
MC-01J — Runtime / Portal / Report integration
26. MC-01A ACCEPTANCE
PASS when:
MingJuContext exists
MingJuDecisionResult exists
versions defined
status enums defined
serialization works
validation skeleton works
public API import surface exists
No real high-level inference required yet.
27. MC-01B ACCEPTANCE
Pattern Recognition PASS when:
canonical IDs normalize
Pattern Engine truth preserved
pattern family resolved
unresolved preserved
follow/transformation cases preserved
trace generated
tests pass
28. MC-01C ACCEPTANCE
Purity + Strength PASS when:
Purity factors generated
Strength dimensions generated
Day Master Strength remains untouched
family-specific rules applied
causal metadata present
negative cases pass
29. MC-01D ACCEPTANCE
Damage + Rescue PASS when:
Damage source-target-mechanism generated
false-positive Damage tests pass
Rescue targets valid Damage
orphan Rescue impossible
Damage history preserved
causal overlap controlled
30. MC-01E ACCEPTANCE
Integrity + Grade PASS when:
Residual Damage works
all structural states work
Integrity state is traceable
Grade depends on Integrity
UNRESOLVED guard works
no direct Grade→wealth mapping
31. MC-01F ACCEPTANCE
Achievement PASS when:
all V1 dimensions exist
dimensions are independent
no universal success score controls output
authority/leadership/management distinctions work
trace exists
32. MC-01G ACCEPTANCE
Wealth PASS when:
five dimensions exist
creation ≠ retention
volatility direction correct
capacity mismatch supported
Tỷ/Kiếp pressure supported
Quan protection supported
Thực/Thương→Tài supported
33. MC-01H ACCEPTANCE
Career PASS when:
Achievement is primary input
Wealth informs commercial/entrepreneurial fit
leadership ≠ management
autonomy modeled
work styles produced
trade-offs preserved
no exact profession prediction
34. MC-01I ACCEPTANCE
Composer PASS when:
headline generated from pattern + integrity
executive summary deterministic
wealth summary parity maintained
career summary parity maintained
confidence language applied
contradictions resolved
message keys validated
no new truth created
35. MC-01J ACCEPTANCE
Runtime integration PASS when:
Orchestrator calls public MC-01 API
one canonical result path exists
analysis.mingju populated
result persisted
/result consumes same result
report consumes same result
PDF/DOCX consume same result
36. A3 — CORE ENGINE PASS
A3 requires structural engine suites PASS:
Pattern
Purity
Pattern Strength
Damage
Rescue
Integrity
Grade
This is the minimum threshold before full domain profiles are trusted.
37. CORE ENGINE MUST PASS NEGATIVE CASES
Mandatory negatives:
false Tòng
false Hóa
false Quan/Sát damage
false Kiêu đoạt Thực
false Tỷ Kiếp đoạt Tài
false Grade elevation
38. DETERMINISM GATE
A3 cannot PASS unless:
same input
+
same ruleset
=
same result
including:
same IDs
same ordering
same serialization
39. TRACE GATE
A3 cannot PASS if a material finding lacks trace.
Required trace chain:
Pattern
→ Purity
→ Strength
→ Damage
→ Rescue
→ Integrity
→ Grade
40. A4 — RUNTIME INTEGRATION PASS
Runtime PASS requires:
live analyze invokes MC-01
result is persisted
current result routing preserved
no legacy Mệnh Cục route overrides canonical result
41. RUNTIME SOURCE-OF-TRUTH GATE
Live UI must read:
analysis.mingju
or frozen equivalent.
It must NOT reconstruct from:
pattern + ten_gods + strength
inside frontend.
42. RUNTIME ANALYSIS-ID PARITY
Verify one analysis ID across:
Analyze
/result
Interpretation
Report
PDF
DOCX
43. CURRENT VS HISTORY ROUTING
MC-01 integration must not reintroduce stale-result behavior.
Current result must remain canonical unless explicit history selection is requested.
44. UPSTREAM IMMUTABILITY GATE
MC-01 runtime integration PASS only if:
BaZi unchanged
Strength unchanged
Pattern unchanged
Useful God unchanged
after MC-01 runs.
45. A5 — PRESENTATION PARITY PASS
A5 requires:
/result
report
PDF
DOCX
to show the same canonical MC-01 truth.
46. REQUIRED PARITY FIELDS
At minimum compare:
Pattern
Integrity state
Grade
Purity
Pattern Strength
Damage
Rescue
Achievement highlights
Wealth profile
Career profile
47. NARRATIVE PARITY
Example:
If canonical:
wealth_creation = high
wealth_retention = low
no surface may say:
giữ tiền rất tốt
48. GRADE PARITY
Forbidden:
/result = A
PDF = B
Any such difference blocks A5.
49. DAMAGE/RESCUE PARITY
If canonical:
damage = major
rescue = strong
all detailed outputs must preserve:
có phá
+
có cứu
No surface may simplify to:
không có phá
50. UI PRESENTATION ACCEPTANCE
UI must present canonical MC-01 results clearly.
Recommended minimum visual fields:
Mệnh Cục
Trạng thái
Grade
Độ thuần
Lực cách
Phá cách
Cứu cách
Achievement/Wealth/Career may appear in detailed sections.
51. UI MUST DISTINGUISH RISK METRICS
Example:
financial_volatility = high
must visually read as:
Rủi ro / Biến động cao
not a positive-strength indicator.
52. UNRESOLVED UI ACCEPTANCE
If unresolved:
Chưa đủ căn cứ kết luận
must be shown.
No blank, fake zero, or fallback Grade.
53. A6 — EXPERT VALIDATION PASS
A6 requires expert review of a diverse validation set.
Minimum categories:
standard pattern
mixed structure
damaged pattern
rescued pattern
follow pattern
transformation pattern
wealth-heavy case
authority-heavy case
career-specialist case
unresolved case
54. EXPERT REVIEW MUST BE STAGE-BY-STAGE
Experts should review:
Pattern
Purity
Strength
Damage
Rescue
Integrity
Grade
Achievement
Wealth
Career
not only final prose.
55. EXPERT BLIND REVIEW
Preferred:
expert conclusion first
engine result second
to reduce confirmation bias.
56. EXPERT CONSENSUS GATE
High-consensus cases must match frozen expected outcomes.
Contested cases may pass if:
accepted alternatives respected
uncertainty preserved
no false certainty
57. EXPERT DISAGREEMENT DOES NOT AUTOMATICALLY MEAN ENGINE BUG
Classify disagreement as:
rule error
input error
tradition difference
interpretive difference
insufficient evidence
before changing rules.
58. NO BIOGRAPHY TUNING GATE
A6 FAILS if rule tuning is performed only because:
person is rich
person is CEO
person is official
Observed biography may trigger investigation,
but cannot directly define rule truth.
59. A7 — FINAL FREEZE
FINAL FREEZE requires:
A0 PASS
A1 PASS
A2 PASS
A3 PASS
A4 PASS
A5 PASS
A6 PASS
plus final release conditions below.
60. FINAL SCHEMA FREEZE
Freeze:
bte.mingju.context.v1
bte.mingju.decision.v1
No breaking field changes after final freeze without V2.
61. FINAL RULESET FREEZE
Freeze:
bte.mingju.rules.v1
with:
rule IDs
priority
exceptions
thresholds
62. FINAL COMPOSER FREEZE
Freeze:
bte.mingju.composer.v1
bte.mingju.messages.vi.v1
Analytical truth and wording versions remain separate.
63. FINAL PUBLIC API FREEZE
Freeze:
build_mingju_context()
analyze_mingju()
compose_mingju_decision()
plus canonical serialization functions.
64. FINAL RESULT PATH FREEZE
Freeze one runtime path:
analysis.mingju
or the approved equivalent.
No competing semantic result paths.
65. FINAL GOLDEN DATASET FREEZE
Freeze:
Golden Dataset version
expected structural states
accepted alternatives
forbidden conclusions
66. GOLDEN DATASET PASS REQUIREMENT
For frozen high-consensus cases:
100% PASS
required.
67. NEGATIVE DATASET PASS REQUIREMENT
All critical negative tests must PASS.
Especially:
false Tòng
false Hóa
false Damage
false Rescue
false Wealth
false Career
68. DETERMINISM PASS REQUIREMENT
Required:
multi-run result = identical
serialization = identical
IDs = stable
ordering = stable
69. RUNTIME PARITY PASS REQUIREMENT
Required parity:
analysis
/result
report
PDF
DOCX
70. REGRESSION PASS REQUIREMENT
All existing MC-01 regression tests must pass before final freeze.
71. NO KNOWN P0/P1 BUGS
Final freeze blocked by:
incorrect Pattern identity
incorrect Damage/Rescue linkage
incorrect Integrity
incorrect Grade
stale runtime result
UI/report truth mismatch
non-determinism
72. KNOWN LIMITATIONS DOCUMENTED
Final freeze may proceed with known non-critical limitations only if documented.
Examples:
some special pattern Achievement rules incomplete
technical domain confidence lower
some contested expert cases remain unresolved
73. KNOWN LIMITATION MUST NOT BE HIDDEN
If unsupported:
state = unresolved
or lower confidence.
Do not silently fake support.
74. ACCEPTANCE STATUS ENUM
Recommended:
NOT_STARTED
IN_PROGRESS
BLOCKED
PASS
PASS_WITH_KNOWN_LIMITATIONS
FAIL
FROZEN
75. CHECKLIST FORMAT
Each acceptance item should record:
ID
Requirement
Status
Evidence
Owner
Notes
76. SAMPLE CHECKLIST ROW
ID:
MC01-ACC-API-001

Requirement:
One canonical analyze_mingju() entry point

Status:
PASS

Evidence:
tests/mingju/contract/test_public_api.py
77. ACCEPTANCE EVIDENCE
Evidence may include:
test report
Golden report
runtime screenshot
serialized payload
API snapshot
expert validation sheet
parity report
No PASS without evidence for mandatory gates.
78. DOCUMENTATION ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-DOC-001	All MC-01 design files exist	YES
ACC-DOC-002	Terminology consistent	YES
ACC-DOC-003	Ownership boundaries frozen	YES
ACC-DOC-004	No critical design TODO	YES


79. PATTERN ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-PAT-001	Canonical Pattern IDs frozen	YES
ACC-PAT-002	Family mapping deterministic	YES
ACC-PAT-003	Upstream Pattern ownership preserved	YES
ACC-PAT-004	Follow/Transformation handling defined	YES
ACC-PAT-005	Unresolved state supported	YES


80. PURITY ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-PUR-001	Purity separated from Strength	YES
ACC-PUR-002	Mixing requires structural relevance	YES
ACC-PUR-003	Quan/Sát handling defined	YES
ACC-PUR-004	Family-specific rules supported	YES
ACC-PUR-005	No causal duplicate penalties	YES


81. STRENGTH ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-STR-001	Pattern Strength separated from Day Master Strength	YES
ACC-STR-002	Season modeled	YES
ACC-STR-003	Roots modeled	YES
ACC-STR-004	Exposure modeled	YES
ACC-STR-005	Generation/Continuity modeled	YES


82. DAMAGE ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-DMG-001	Source required	YES
ACC-DMG-002	Target required	YES
ACC-DMG-003	Mechanism required	YES
ACC-DMG-004	Evidence required	YES
ACC-DMG-005	Weakness ≠ Damage	YES
ACC-DMG-006	Relation presence ≠ Damage	YES


83. RESCUE ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-RSC-001	Rescue targets real Damage	YES
ACC-RSC-002	No orphan Rescue	YES
ACC-RSC-003	Mechanism required	YES
ACC-RSC-004	Damage history preserved	YES
ACC-RSC-005	Support ≠ Rescue	YES


84. INTEGRITY / GRADE ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-INT-001	All structural states supported	YES
ACC-INT-002	Residual Damage modeled	YES
ACC-INT-003	Causal deduplication works	YES
ACC-GRD-001	Grade downstream from Integrity	YES
ACC-GRD-002	UNRESOLVED guard works	YES
ACC-GRD-003	Grade does not imply wealth/status	YES


85. ACHIEVEMENT ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-ACH-001	Multi-dimensional profile exists	YES
ACC-ACH-002	Leadership ≠ Management	YES
ACC-ACH-003	Entrepreneurship ≠ Wealth	YES
ACC-ACH-004	No biography fitting	YES
ACC-ACH-005	No universal success score	YES


86. WEALTH ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-WLT-001	Creation separated from Retention	YES
ACC-WLT-002	Accumulation modeled	YES
ACC-WLT-003	Expansion modeled	YES
ACC-WLT-004	Volatility direction explicit	YES
ACC-WLT-005	Carrying capacity modeled	YES
ACC-WLT-006	No Tài=giàu shortcut	YES


87. CAREER ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-CAR-001	Achievement drives Career	YES
ACC-CAR-002	Wealth informs business fit	YES
ACC-CAR-003	Autonomy modeled	YES
ACC-CAR-004	Trade-offs preserved	YES
ACC-CAR-005	No exact profession prediction	YES


88. COMPOSER ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-CMP-001	No new analytical truth	YES
ACC-CMP-002	Message keys validated	YES
ACC-CMP-003	Confidence language works	YES
ACC-CMP-004	Contradictions resolved	YES
ACC-CMP-005	Dashboard/report parity preserved	YES


89. API ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-API-001	One public analyze entry point	YES
ACC-API-002	One normalized Context	YES
ACC-API-003	One canonical Result	YES
ACC-API-004	Version fields exposed	YES
ACC-API-005	Partial/unresolved supported	YES
ACC-API-006	Natal/Luck separated	YES


90. VALIDATION ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-VAL-001	Score ranges enforced	YES
ACC-VAL-002	Confidence ranges enforced	YES
ACC-VAL-003	Reference integrity enforced	YES
ACC-VAL-004	Grade/Integrity consistency enforced	YES
ACC-VAL-005	Volatility direction enforced	YES
ACC-VAL-006	Determinism validated	YES


91. TEST ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-TST-001	Unit suite PASS	YES
ACC-TST-002	Rule suite PASS	YES
ACC-TST-003	Golden suite PASS	YES
ACC-TST-004	Negative suite PASS	YES
ACC-TST-005	Determinism PASS	YES
ACC-TST-006	Integration PASS	YES
ACC-TST-007	Parity PASS	YES


92. EXPERT ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-EXP-001	Diverse expert-reviewed cases exist	YES
ACC-EXP-002	High-consensus cases pass	YES
ACC-EXP-003	Contested cases preserve uncertainty	YES
ACC-EXP-004	No biography-driven tuning	YES


93. RUNTIME ACCEPTANCE TABLE
ID	Requirement	Mandatory
ACC-RT-001	MC-01 runs in live analyze	YES
ACC-RT-002	Same analysis ID maintained	YES
ACC-RT-003	Canonical result persisted	YES
ACC-RT-004	/result binds canonical result	YES
ACC-RT-005	Report binds canonical result	YES
ACC-RT-006	PDF/DOCX parity	YES


94. RELEASE BLOCKERS
Any of the following blocks FINAL FREEZE:
incorrect Pattern routing
orphan Rescue
Damage erased after Rescue
Grade resolved while Integrity unresolved
nondeterministic output
biography changes natal result
current year changes natal result
frontend calculates canonical truth
report calculates canonical truth
UI/PDF/DOCX disagreement
high-consensus Golden failure
95. RELEASE WARNING CONDITIONS
May allow:
PASS_WITH_KNOWN_LIMITATIONS
for non-critical issues such as:
secondary technical dimension low confidence
some special pattern Career rules not implemented
customer wording polish pending
provided core analytical truth is safe.
96. STOP CONDITIONS
Implementation should STOP if a discovered issue changes:
ownership
schema semantics
Pattern identity rules
Damage/Rescue model
Integrity states
Grade meaning
A design review is required before continuing.
97. NO SCOPE CREEP DURING IMPLEMENTATION
MC-01 implementation must not quietly add:
Luck activation
relationship model
health model
marriage prediction
children prediction
exact profession engine
exact wealth prediction
unless separately approved.
98. V1 SCOPE FREEZE
MC-01 V1 scope:
Natal Mệnh Cục structural decision
Achievement
Wealth
Career
Composer
No Luck activation inside core V1.
99. FUTURE MODULES
Potential later modules:
MC-02 Luck Activation
MC-03 Authority Realization
MC-04 Wealth Activation
MC-05 Career Timing
These must consume frozen natal MC-01 truth,
not rewrite it.
100. IMPLEMENTATION HANDOFF CHECKLIST
Before giving Cursor implementation command, confirm:
[ ] All 15 design files reviewed
[ ] Architecture approved
[ ] Public models approved
[ ] Rule namespaces approved
[ ] Version IDs approved
[ ] Test strategy approved
[ ] No critical open question
101. CURSOR IMPLEMENTATION RULE
Cursor should be instructed:
IMPLEMENT FROM FROZEN DOCUMENTS.
DO NOT REDESIGN RULE SEMANTICS.
DO NOT CHANGE EXISTING UPSTREAM ENGINES.
DO NOT MODIFY UI UNTIL CORE CONTRACT PASSES.
102. IMPLEMENTATION EVIDENCE REQUIRED
For every phase Cursor should return:
status
files changed
tests added
tests run
PASS/FAIL
known limitations
no-out-of-scope confirmation
103. PHASE STOP RULE
After each implementation phase:
STOP
and wait for Product Owner approval.
Do not automatically continue into runtime/UI.
104. DESIGN FREEZE REPORT
Recommended artifact:
MC01_DESIGN_FREEZE.md
Contents:
document set
frozen architecture
frozen schema target
frozen ruleset target
known open calibration items
approval status
105. CORE ENGINE COMPLETION REPORT
Recommended:
MC01_CORE_ENGINE_COMPLETION_REPORT.md
Include:
stages implemented
tests
Golden results
negative results
determinism
known limitations
106. RUNTIME INTEGRATION REPORT
Recommended:
MC01_RUNTIME_INTEGRATION_REPORT.md
Include:
Orchestrator binding
result path
analysis ID
live verification
routing
persistence
107. PARITY REPORT
Recommended:
MC01_PRESENTATION_PARITY_REPORT.md
Compare:
/result
Report
PDF
DOCX
108. EXPERT VALIDATION REPORT
Recommended:
MC01_EXPERT_VALIDATION_REPORT.md
Include:
case IDs
expert assessments
engine results
disagreements
resolution
accepted limitations
109. FINAL FREEZE REPORT
Recommended final artifact:
MC01_FINAL_FREEZE.md
110. FINAL FREEZE REPORT CONTENT
Minimum:
Status: PASS / FAIL

Schema:
bte.mingju.decision.v1

Ruleset:
bte.mingju.rules.v1

Composer:
bte.mingju.composer.v1

Golden Dataset:
version

Tests:
summary

Runtime:
PASS/FAIL

Parity:
PASS/FAIL

Expert validation:
PASS/FAIL

Known limitations:
...

Frozen:
YES/NO
111. FINAL FREEZE DECLARATION
Only when all mandatory gates pass:
MC-01 — MỆNH CỤC DECISION ENGINE
STATUS: FINAL FROZEN
112. POST-FREEZE CHANGE POLICY
After FINAL FREEZE:
Bug fix that preserves semantics:
patch release
Rule semantic change:
ruleset version bump
Breaking schema change:
schema v2
Major model redesign:
MC-01 V2
113. NO SILENT POST-FREEZE RULE CHANGE
Forbidden:
change threshold
change Pattern precedence
change Damage rule
change Grade semantics
without versioning and Golden drift review.
114. GOLDEN DRIFT REQUIREMENT
Any rule change after freeze requires:
old vs new Golden comparison
reason
approved affected cases
regression review
115. COMPOSER-ONLY CHANGE
If only wording changes:
Composer/message catalog version bump
No need to rerun MC-01 analytical truth unless template requirements changed.
116. UI-ONLY CHANGE
Presentation/layout changes must not alter:
canonical MC-01 values
message semantics
Analytical tests should remain unchanged.
117. FINAL QUALITY PRINCIPLE
MC-01 should not be frozen because:
the screen looks good
or:
one chart seems correct
It should be frozen because:
the inference architecture is consistent
the evidence chain is auditable
the tests are adversarial
the runtime is deterministic
the outputs are consistent
the expert cases are acceptable
118. CUSTOMER QUALITY PRINCIPLE
Commercial acceptance requires that the customer can understand:
Mệnh cục gì?
Thành hay chưa?
Mạnh ở đâu?
Bị phá ở đâu?
Có cứu không?
Tài chính mạnh theo kiểu nào?
Nghề nghiệp hợp theo kiểu nào?
Điều gì giúp phát?
Điều gì cần tránh?
without receiving contradictory generic prose.
119. EXPERT QUALITY PRINCIPLE
Expert acceptance requires the engine to answer:
Rule nào?
Evidence nào?
Source nào?
Causal path nào?
Tại sao Grade này?
without reading hidden arbitrary constants.
120. PRODUCT QUALITY PRINCIPLE
Product acceptance requires:
one canonical truth
one runtime path
one stored result
one Composer truth
consistent UI/report/export
121. FINAL ACCEPTANCE MODEL
MC-01 FINAL ACCEPTANCE
=
Architecture PASS
+ Contract PASS
+ Rules PASS
+ Validation PASS
+ Tests PASS
+ Determinism PASS
+ Runtime PASS
+ Presentation Parity PASS
+ Expert Validation PASS
No single part may substitute for another.
122. FINAL CHECKLIST — DESIGN
[ ] Architecture complete
[ ] Ownership frozen
[ ] Pattern boundary frozen
[ ] Purity boundary frozen
[ ] Strength boundary frozen
[ ] Damage boundary frozen
[ ] Rescue boundary frozen
[ ] Integrity states frozen
[ ] Grade meaning frozen
[ ] Achievement dimensions frozen
[ ] Wealth dimensions frozen
[ ] Career model frozen
[ ] Composer boundary frozen
[ ] Public API frozen
[ ] Validation model frozen
[ ] Test strategy frozen
123. FINAL CHECKLIST — IMPLEMENTATION
[ ] Models implemented
[ ] Context adapter implemented
[ ] Pattern Recognition implemented
[ ] Purity implemented
[ ] Pattern Strength implemented
[ ] Damage implemented
[ ] Rescue implemented
[ ] Integrity implemented
[ ] Grade implemented
[ ] Achievement implemented
[ ] Wealth implemented
[ ] Career implemented
[ ] Composer implemented
[ ] Validation implemented
[ ] Serialization implemented
124. FINAL CHECKLIST — TESTS
[ ] Unit PASS
[ ] Rule PASS
[ ] Contract PASS
[ ] Cross-stage PASS
[ ] Golden PASS
[ ] Negative PASS
[ ] Metamorphic PASS
[ ] Determinism PASS
[ ] Snapshot PASS
[ ] Integration PASS
[ ] Runtime PASS
[ ] Parity PASS
125. FINAL CHECKLIST — EXPERT
[ ] Expert cases selected
[ ] Blind review completed
[ ] High-consensus cases pass
[ ] Contested cases documented
[ ] No biography tuning
[ ] Remaining limitations accepted
126. FINAL CHECKLIST — PRODUCT
[ ] Live /result correct
[ ] Mệnh Cục card correct
[ ] Detailed interpretation correct
[ ] Wealth content correct
[ ] Career content correct
[ ] Report parity correct
[ ] PDF parity correct
[ ] DOCX parity correct
[ ] No stale runtime source
[ ] No legacy semantic path
127. FINAL DECISION
Only two valid final decisions:
FINAL FREEZE APPROVED
or:
FINAL FREEZE BLOCKED
Do not use ambiguous final states such as:
mostly done
probably okay
good enough
128. ARCHITECTURAL DECISION
Canonical rule:
MC-01 MAY ENTER IMPLEMENTATION ONLY AFTER ITS INFERENCE BOUNDARIES, PUBLIC CONTRACT, VALIDATION RULES, AND TEST STRATEGY ARE FROZEN.

And:
MC-01 MAY ENTER FINAL FREEZE ONLY AFTER CORE REASONING, LIVE RUNTIME, PRESENTATION PARITY, AND EXPERT VALIDATION HAVE ALL PASSED.

129. NEXT ACTION AFTER THIS DOCUMENT
Once this document is approved:
1. Create MC01_DESIGN_FREEZE.md
2. Freeze the 15-document design set
3. Issue MC-01A implementation ticket to Cursor
4. Implement Models / Context / Public API skeleton first
5. STOP after MC-01A report
Do NOT jump directly into full engine implementation in one ticket.
130. FINAL STATUS TARGET
MC-01 DESIGN PACK
STATUS: READY FOR DESIGN FREEZE
after Product Owner review.
Then:
MC-01A IMPLEMENTATION
STATUS: READY TO START

Với file này thì bộ thiết kế MC-01 đã đủ kín để **không nên viết thêm logic mới ngay**, mà bước đúng tiếp theo là tạo `MC01_DESIGN_FREEZE.md`, khóa toàn bộ 15 tài liệu, rồi giao Cursor **MC-01A — Models / Context / Public API Skeleton** trước. Làm như vậy sẽ tránh Cursor lao thẳng vào viết hàng loạt rule trong khi contract chưa được đóng băng.