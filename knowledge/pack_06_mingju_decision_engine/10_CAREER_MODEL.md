# MC-01 — CAREER MODEL

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `10_CAREER_MODEL.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the Career Model of MC-01.

The Career Model converts validated natal structural evidence into
structured recommendations about:

- work environment
- role style
- organizational fit
- autonomy needs
- leadership fit
- specialist fit
- entrepreneurial fit
- academic / technical / creative fit
- career stability
- career risk factors

It does NOT predict one exact profession.

Canonical flow:

```text
PatternDecision
      ↓
Structural Integrity
      ↓
Pattern Grade
      ↓
Achievement Profile
      ↓
Wealth Profile
      ↓
Career Model
      ↓
CareerProfile

2. CORE PRINCIPLE
Career recommendation must be based on a profile,
not a single Ten God.
Forbidden:
Chính Quan
→ công chức
Forbidden:
Thiên Tài
→ kinh doanh
Forbidden:
Chính Ấn
→ giáo viên
Correct logic:
Structural pattern
+ Achievement capabilities
+ Wealth behavior
+ autonomy
+ stability
+ leadership
+ management
+ technical / academic / creative profile
→ work-style recommendation
3. CAREER MODEL OUTPUT
Canonical object:
CareerProfile
Fields:
state
primary_work_styles
secondary_work_styles
organizational_fit
role_fit
autonomy_need
leadership_fit
management_fit
specialist_fit
entrepreneurial_fit
technical_fit
academic_fit
creative_fit
public_facing_fit
career_stability
career_risks
conditions_for_expression
avoid_conditions
confidence
evidence_ids
4. CAREER IS MULTI-AXIS
Career Model should not reduce fit to:
career_score = 85
Instead evaluate several dimensions.
Initial canonical dimensions:
institutional_fit
entrepreneurial_fit
leadership_fit
management_fit
specialist_fit
technical_fit
academic_fit
creative_fit
public_facing_fit
autonomy_need
career_stability
5. PRIMARY WORK STYLES
Canonical work-style IDs:
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
One chart may support more than one.
6. ORGANIZATIONAL FIT
organizational_fit answers:
What type of organizational environment best supports this structure?
Possible canonical values:
highly_structured
structured
semi_structured
flexible
high_autonomy
mixed
unresolved
7. STRUCTURED ENVIRONMENT SIGNALS
Potential positive signals:
authority high
institutional_career high
management high
stability high
Chính Quan
Chính Ấn
Quan–Ấn chain
high Structural Integrity
Potential negative signals:
extreme independence
strong unmediated Thương Quan
high volatility
low hierarchy tolerance
8. HIGH-AUTONOMY ENVIRONMENT SIGNALS
Potential signals:
independence high
entrepreneurship high
Thương Quan
Thiên Tài
Tỷ Kiên
Kiếp Tài
Dương Nhẫn
public visibility
creative strength
But autonomy must not be inferred from one signal only.
9. ROLE FIT
Role Fit answers:
What kind of responsibility does the structure handle best?
Initial role IDs:
subordinate_executor
specialist_executor
coordinator
manager
senior_manager
leader
owner_operator
advisor
researcher
creator
public_representative
mixed
These are structural role styles,
not exact job titles.
10. LEADERSHIP FIT
leadership_fit should consume:
AchievementProfile.leadership
AchievementProfile.authority
AchievementProfile.independence
Structural Integrity
Day Master capacity
Damage / Rescue
Potential profile:
high leadership
high authority
adequate stability
may support:
leadership_command
11. LEADERSHIP IS NOT MANAGEMENT
Leadership:
sets direction
takes responsibility
influences others
handles pressure
Management:
organizes resources
builds systems
coordinates execution
maintains continuity
Both must remain separate.
12. MANAGEMENT FIT
Potential signals:
management high
authority above_average+
stability high
Chính Quan
Chính Ấn
Tài
good structural continuity
Potential reducers:
high fragmentation
extreme volatility
weak execution structure
13. ENTREPRENEURIAL FIT
entrepreneurial_fit should consume:
AchievementProfile.entrepreneurship
AchievementProfile.independence
AchievementProfile.leadership
WealthProfile.wealth_creation
WealthProfile.business_expansion
WealthProfile.financial_volatility
WealthProfile.wealth_retention
This is essential.
Entrepreneurial fit must NOT be inferred only from Thiên Tài.
14. ENTREPRENEURIAL FIT — POSITIVE SIGNALS
Potential:
entrepreneurship high
independence high
wealth_creation high
business_expansion high
leadership adequate
management adequate
15. ENTREPRENEURIAL FIT — RISK SIGNALS
Potential:
wealth_retention low
financial_volatility high
management weak
stability low
peer competition severe
This allows nuanced output:
business aptitude high
but capital control is a risk
16. OWNER-OPERATOR VS INVESTOR
Future Career Model MAY distinguish:
owner_operator
capital_allocator
commercial_manager
But V1 should not over-specialize until Wealth Model is validated.
17. SPECIALIST FIT
specialist_fit evaluates suitability for:
deep expertise
individual contribution
professional specialization
precision work
specialized knowledge
Potential signals:
academic high
technical high
resource structure strong
public visibility not required
independence moderate/high
18. TECHNICAL FIT
Potential inputs:
AchievementProfile.technical
AchievementProfile.academic
management
stability
structured output
Possible environments:
engineering-like
systems
analysis
specialized technical execution
Career Model should not output literal engineering professions automatically.
19. ACADEMIC FIT
Potential inputs:
academic high
resource structure strong
stability high
technical/creative support
public visibility depending teaching role
Possible work style:
study
research
teaching
knowledge specialization
20. CREATIVE FIT
Potential inputs:
creative high
independence high
public_visibility
output strength
entrepreneurship depending structure
Possible work style:
creative_expression
independent_creation
public-facing creativity
21. PUBLIC-FACING FIT
public_facing_fit evaluates suitability for:
presentation
communication
representation
client-facing work
public influence
visibility
Potential evidence:
public_visibility high
creative high
leadership high
authority high
output exposed
22. PUBLIC-FACING IS NOT FAME
High public-facing fit means:
capable of functioning in visible roles
not:
guaranteed fame
23. AUTONOMY NEED
Canonical values:
very_low
low
moderate
high
very_high
unresolved
Potential signals:
independence
entrepreneurship
Thương Quan
Tỷ/Kiếp
Dương Nhẫn
Thiên Tài
High autonomy need can reduce fit with rigid hierarchy.
24. AUTONOMY VS DISCIPLINE
A chart may have:
autonomy high
discipline high
This may fit:
senior autonomous professional
executive role
owner-manager
rather than:
entry-level subordinate role
This interaction is valuable.
25. CAREER STABILITY
career_stability evaluates:
ability to sustain a career path
consistency of work environment
resistance to abrupt changes
Inputs may include:
AchievementProfile.stability
Structural Integrity
financial volatility
pattern continuity
unresolved Damage
26. CAREER STABILITY VS FINANCIAL STABILITY
These are related but separate.
career_stability
may be high even when:
financial_volatility
is moderate.
Example:
stable profession + variable investment income.
27. PRIMARY CAREER DIRECTION
Career Model may produce:
primary_work_styles
Example:
[
  "managerial",
  "structured_institutional"
]
or:
[
  "entrepreneurial",
  "independent_autonomous"
]
28. SECONDARY CAREER DIRECTION
Secondary styles may represent additional viable paths.
Example:
[
  "specialist",
  "public_facing"
]
29. CAREER DIRECTION IS NOT EXACT PROFESSION
Forbidden output from core engine:
lawyer
doctor
banker
police officer
architect
teacher
These are profession labels.
Core Career Model should output work characteristics.
30. PROFESSION MAPPING IS DOWNSTREAM
Future Composer or Recommendation layer may map:
structured_institutional
+
authority
+
management
to example fields such as:
administration
compliance
large organizations
regulated sectors
But examples must remain non-deterministic.
31. PATTERN FAMILY TENDENCIES
Conceptual only:
Chính Quan
→ structured / authority / management

Thất Sát
→ command / leadership / high-pressure roles

Chính Tài
→ management / operations / stable commercial roles

Thiên Tài
→ entrepreneurial / commercial / flexible roles

Chính Ấn
→ academic / technical / institutional / advisory

Thiên Ấn
→ specialized / academic / technical / creative

Thực Thần
→ creative / specialist / production / commercial

Thương Quan
→ creative / independent / entrepreneurial / public-facing

Kiến Lộc
→ independent / management / leadership

Dương Nhẫn
→ command / leadership / autonomy
Directional only.
32. NO DIRECT PATTERN→CAREER TABLE
Forbidden:
zheng_guan → government
pian_cai → business owner
zheng_yin → teacher
Pattern identity selects applicable evidence rules.
It does not decide career.
33. ACHIEVEMENT PROFILE IS PRIMARY CAREER INPUT
Career Model should rely heavily on:
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
This prevents duplicate reasoning.
34. WEALTH PROFILE AS CAREER CONTEXT
Wealth Profile helps distinguish:
entrepreneurial aptitude
from:
commercial sustainability
Example:
entrepreneurship high
wealth_creation high
retention low
volatility high
Career Model may say:
entrepreneurial fit high
but expansion should be controlled
35. STRUCTURAL INTEGRITY AS USABILITY
A strong Career profile needs usable structure.
Example:
leadership high
but Integrity = damaged
Career Model should preserve:
leadership potential
+
career execution risk
Do not zero potential.
36. CAREER PROFILE STATE
Allowed:
resolved
partially_resolved
unresolved
insufficient_evidence
37. CAREER FIT DIMENSION
Recommended generic object:
CareerFitDimension
Fields:
dimension
state
score
classification
confidence
positive_evidence_ids
negative_evidence_ids
conditions
risks
38. CAREER FIT CLASSIFICATION
Canonical:
very_low
low
below_average
moderate
above_average
high
very_high
unresolved
Same scale as Achievement where practical.
39. CAREER SCORE MEANING
Example:
entrepreneurial_fit = 84
means:
structure strongly supports entrepreneurial work style
not:
84% probability of owning a business
40. ORGANIZATIONAL FIT MODEL
Potential subdimensions:
hierarchy_tolerance
procedure_fit
autonomy_fit
team_fit
change_tolerance
V1 may expose only aggregated Organizational Fit.
41. HIERARCHY TOLERANCE
Potential positive signals:
institutional career high
authority structure coherent
Chính Quan
Chính Ấn
stability
Potential reducers:
independence very_high
uncontrolled Thương Quan
strong peer autonomy
42. PROCEDURE FIT
Potential signals:
management
stability
Chính Quan
Ấn
technical discipline
43. CHANGE TOLERANCE
Potential signals:
entrepreneurship
Thiên Tài
Thương Quan
independence
creative
financial volatility
High change tolerance may favor flexible environments.
44. TEAM FIT
Potentially influenced by:
management
authority
peer structures
independence
stability
Do not derive social personality too aggressively.
45. SPECIALIST VS GENERALIST
Future internal indicator:
specialist_orientation
generalist_orientation
Potential specialist signals:
academic
technical
Thiên Ấn
resource concentration
Potential generalist/managerial signals:
management
leadership
Tài
Quan
V1 may keep only specialist_fit.
46. ADVISORY FIT
Possible role:
advisor
Potential signals:
academic
technical
management
public-facing
Ấn
Thực
This can be included in role_fit.
47. OWNER-MANAGER FIT
Potential signals:
entrepreneurship high
management high
leadership high
independence high
wealth_creation high
business_expansion high
This differs from purely entrepreneurial creator.
48. FOUNDER / CREATOR PROFILE
Potential:
entrepreneurship high
creative high
independence very_high
management moderate
This may fit creation/startup style,
but may need stronger operational support.
49. PROFESSIONAL EXECUTIVE PROFILE
Potential:
authority high
management high
institutional high
leadership high
stability high
This is structurally different from founder profile.
50. TECHNICAL SPECIALIST PROFILE
Potential:
technical high
academic high
specialist_fit high
management moderate/low
public_facing moderate/low
51. CREATIVE INDEPENDENT PROFILE
Potential:
creative high
independence high
public_facing high
entrepreneurship above_average+
institutional fit low/moderate
52. ACADEMIC / RESEARCH PROFILE
Potential:
academic very_high
technical high
stability high
specialist high
entrepreneurship low/moderate
53. HYBRID PROFILE
Many charts will be hybrid.
Example:
managerial
+
entrepreneurial
or:
technical
+
leadership
Do not force a single path.
54. PRIMARY VS SECONDARY FIT
Recommended selection:
primary fit
= strongest coherent work-style cluster

secondary fit
= viable alternate cluster
This is more useful than listing every high score.
55. CLUSTER MODEL
Future Career Model MAY derive clusters:
institutional_leader
commercial_manager
entrepreneurial_builder
technical_specialist
academic_specialist
creative_independent
public_leader
hybrid_operator
But do not freeze cluster scoring before dimensions stabilize.
56. CAREER RISK MODEL
Possible structured career risks:
hierarchy_conflict
overcontrol
under_management
overexpansion
poor_capital_control
career_volatility
role_mismatch
low_autonomy_tolerance
excessive_independence
specialist_isolation
public_pressure
57. HIERARCHY CONFLICT
Potential:
independence very_high
+
institutional fit low
+
Thương Quan authority conflict
May indicate:
rigid subordinate roles are difficult
not:
cannot work for anyone
58. OVERCONTROL RISK
Potential:
authority high
leadership high
flexibility low
May create:
over-control tendency in management roles
Keep wording structural, not judgmental.
59. UNDER-MANAGEMENT RISK
Potential:
entrepreneurship high
creative high
management low
Could imply:
strong initiation but weak operational discipline
This is useful commercially.
60. OVEREXPANSION RISK
Potential:
entrepreneurship high
business_expansion high
financial_volatility high
wealth_retention low
This is a key career-business risk.
61. CAREER CONDITION FOR EXPRESSION
Examples:
needs decision authority
needs autonomy
benefits from structured systems
benefits from specialist depth
benefits from public-facing role
needs operational support
needs capital discipline
These should be structured IDs.
62. AVOID CONDITIONS
Possible:
overly_rigid_subordinate_role
chaotic_unstructured_environment
excessive_financial_risk
role_without_autonomy
role_without_clear_systems
overloaded_management_scope
Final customer wording comes later.
63. CAREER RECOMMENDATION MUST BE RELATIVE
Prefer:
more suitable
less suitable
better expression
higher structural fit
Avoid:
must do
cannot do
64. CAREER VS DỤNG THẦN
Useful God may influence working environment,
but must not directly map to occupation.
Forbidden:
Hỏa = work in electricity
Mộc = work in wood industry
unless a separate validated advisory system exists.
Career Model should first use structural capabilities.
65. ELEMENT-BASED CAREER MAPPING
If future BTE wants element-associated industries,
that should be a separate downstream advisory layer.
Do not mix it into core Career Model.
66. CAREER VS WEALTH
A career may fit strongly but not maximize wealth.
Example:
academic_fit = very_high
wealth_creation = moderate
This is valid.
Do not optimize Career solely for money.
67. CAREER VS AUTHORITY
High authority potential does not require government work.
It may express in:
corporate leadership
professional authority
organizational responsibility
entrepreneurial leadership
68. CAREER VS ENTREPRENEURSHIP
High entrepreneurship does not require company ownership.
It can express in:
business development
commercial autonomy
project ownership
intrapreneurship
69. CAREER VS ACADEMIC
High academic potential may express through:
research
teaching
specialist advisory
knowledge work
not only formal academia.
70. CAREER VS TECHNICAL
High technical potential may express in any field requiring:
precision
systems
analysis
specialized skill
Do not over-map to engineering only.
71. CAREER VS CREATIVE
Creative potential may express in:
design
communication
strategy
content
product creation
problem solving
but core engine should not enumerate job titles.
72. CAREER AND PUBLIC VISIBILITY
A chart may have:
technical high
public_visibility high
supporting:
visible expert / spokesperson / technical leader
This is a valuable hybrid profile.
73. CAREER CONFIDENCE
Confidence depends on:
AchievementProfile confidence
WealthProfile confidence
Structural Integrity confidence
Career rule coverage
conflicting signals
missing hour pillar
74. CONFLICTING CAREER SIGNALS
Example:
institutional_fit high
independence very_high
This is not invalid.
It may imply:
best fit in senior or autonomous roles inside structured organizations
Career Composer should explain the tension.
75. CAREER PROFILE EXAMPLE — INSTITUTIONAL LEADER
Illustrative:
{
  "state": "resolved",

  "primary_work_styles": [
    "leadership_command",
    "structured_institutional",
    "managerial"
  ],

  "organizational_fit": "highly_structured",

  "leadership_fit": {
    "score": 85,
    "classification": "very_high"
  },

  "management_fit": {
    "score": 82,
    "classification": "high"
  },

  "entrepreneurial_fit": {
    "score": 58,
    "classification": "moderate"
  },

  "autonomy_need": "high",

  "career_stability": {
    "score": 81,
    "classification": "high"
  }
}
Numbers are illustrative only.
76. CAREER PROFILE — ENTREPRENEURIAL BUILDER
primary:
entrepreneurial
independent_autonomous
managerial

entrepreneurial_fit = very_high
management_fit = high
leadership_fit = high
institutional_fit = moderate
autonomy_need = very_high
career_stability = moderate
77. CAREER PROFILE — SPECIALIST
primary:
specialist
technical

technical_fit = very_high
academic_fit = high
management_fit = moderate
leadership_fit = low/moderate
autonomy_need = high
78. CAREER PROFILE — CREATIVE PUBLIC
primary:
creative_expression
public_facing
independent_autonomous

creative_fit = very_high
public_facing_fit = high
entrepreneurial_fit = high
institutional_fit = low
79. CUSTOMER PRESENTATION
Future UI may show:
ĐỊNH HƯỚNG NGHỀ NGHIỆP

Môi trường phù hợp
Có cấu trúc, quyền chủ động cao

Vai trò nổi bật
Lãnh đạo / Quản trị

Khả năng làm chủ
Cao

Khả năng chuyên môn
Khá

Khả năng làm việc hệ thống
Rất cao

Nhu cầu tự chủ
Cao
80. CUSTOMER SUMMARY EXAMPLE
Cấu trúc phù hợp với vai trò quản trị hoặc lãnh đạo trong môi trường có hệ thống rõ ràng.
Khả năng tự chủ khá cao, vì vậy các vị trí có quyền quyết định sẽ phát huy tốt hơn vai trò thuần chấp hành.
81. ENTREPRENEURIAL CUSTOMER SUMMARY
Lá số có lợi thế về tính chủ động, thương mại và khả năng mở rộng công việc.
Tuy nhiên nếu năng lực quản trị vốn thấp hơn năng lực tạo cơ hội,
mô hình kinh doanh cần hệ thống kiểm soát tài chính chặt.
82. SPECIALIST CUSTOMER SUMMARY
Cấu trúc thiên về chuyên môn sâu và xử lý hệ thống,
phù hợp hơn với vai trò cần kiến thức, kỹ thuật và quyền tự chủ chuyên môn
so với công việc quá thiên về bán hàng hoặc giao tiếp liên tục.
83. CUSTOMER WORDING SAFETY
Avoid:
Bạn phải làm lãnh đạo.
Prefer:
Năng lực lãnh đạo và quản trị là nhóm thế mạnh nổi bật.
Avoid:
Bạn không hợp làm thuê.
Prefer:
Mức tự chủ cao khiến các vị trí có quyền quyết định thường dễ phát huy hơn các vai trò quá bị động.
84. NO EXACT JOB PREDICTION
Core engine MUST NOT predict:
CEO
police officer
doctor
judge
architect
teacher
as deterministic results.
85. NO CAREER STATUS PREDICTION
Forbidden:
will become director
will become minister
will run a company
Career Model describes fit and capacity,
not guaranteed outcome.
86. CAREER MODEL VS LUCK
Natal Career Profile answers:
What work style fits the natal structure?
Luck answers:
When is that work style easier to activate or advance?
Natal profile must remain stable.
87. FUTURE CAREER ACTIVATION
Future:
Natal leadership_fit = high

Đại Vận 2031–2040:
authority activation = high
career expansion = high
But natal leadership score remains unchanged.
88. BIOGRAPHY MUST NOT ALTER CAREER PROFILE
Adding:
current_job
education
income
position
must not affect natal inference.
These may be used only for validation.
89. CAREER RULE MODEL
Conceptual:
CareerRule
Fields:
rule_id
dimension
conditions
positive_effect
negative_effect
priority
exceptions
evidence_requirements
confidence_policy
90. CAREER EVIDENCE MODEL
Recommended:
CareerEvidence
Fields:
evidence_id
dimension
signal_type
direction
strength
source_stage
source_id
confidence
causal_group
91. CAREER SIGNAL TYPES
Initial:
achievement_dimension
wealth_dimension
pattern_identity
pattern_integrity
authority_structure
output_structure
resource_structure
wealth_structure
independence
stability
damage
rescue
92. RULE NAMESPACES
Recommended:
MC-CAR-INST-*
MC-CAR-LEAD-*
MC-CAR-MGMT-*
MC-CAR-ENTRE-*
MC-CAR-SPEC-*
MC-CAR-TECH-*
MC-CAR-ACA-*
MC-CAR-CREAT-*
MC-CAR-PUBLIC-*
MC-CAR-AUTO-*
MC-CAR-STAB-*
MC-CAR-GENERAL-*
93. RULE PRIORITY
Conceptual precedence:
explicit exception
>
profile-cluster rule
>
family-specific career rule
>
Achievement-driven rule
>
Wealth-driven rule
>
general career rule
94. NO DOUBLE REWARD
If:
leadership = high
already derives from strong Quan/Sát,
Career Model should not separately add full bonuses from:
Quan present
Sát present
leadership high
for the same causal reason.
Use Achievement Profile as primary derived evidence
to reduce duplication.
95. PRIMARY SOURCE PREFERENCE
Recommended preference:
Achievement Profile
>
Wealth Profile
>
Structural Integrity
>
raw pattern evidence
Raw upstream evidence should be used for exceptions or explanation,
not to duplicate downstream reasoning.
96. CAREER CLUSTER DEDUPLICATION
If several dimensions point to the same career cluster,
combine them into one coherent recommendation.
Example:
authority high
management high
institutional high
stability high
→
institutional_leader
rather than four separate redundant recommendations.
97. CAREER CLUSTER MODEL
Optional future object:
CareerCluster
Fields:
cluster_id
score
confidence
supporting_dimensions
risks
conditions
98. INITIAL CLUSTER IDS
Potential:
institutional_leader
commercial_manager
entrepreneurial_builder
owner_manager
technical_specialist
academic_specialist
creative_independent
public_facing_leader
advisor_specialist
hybrid_operator
Do not freeze numeric rules yet.
99. CAREER RANKING
Primary career styles should be ranked by:
fit score
confidence
cluster coherence
risk penalty
canonical order
Exact algorithm remains unfrozen.
100. GOLDEN DATASET REQUIREMENTS
Career Golden Cases must include:
Chính Quan + Ấn institutional profile
Sát–Ấn leadership profile
Thiên Tài + Thương entrepreneurial profile
Thực sinh Tài commercial profile
strong academic/resource profile
technical specialist profile
creative independent profile
Kiến Lộc management/independence
Dương Nhẫn leadership/autonomy
high entrepreneurship + poor retention
high institutional + high autonomy
high leadership + weak management
high technical + low public visibility
hybrid technical leader
damaged authority structure
rescued authority structure
unresolved profile
missing hour pillar
101. GOLDEN CASE — INSTITUTIONAL
{
  "case_id": "MC-CAR-INST-001",

  "facts": {
    "authority": "high",
    "institutional_career": "very_high",
    "management": "high",
    "stability": "high"
  },

  "expected": {
    "primary_work_styles": [
      "structured_institutional",
      "managerial"
    ],
    "organizational_fit": [
      "highly_structured",
      "structured"
    ]
  }
}
102. GOLDEN CASE — ENTREPRENEUR
{
  "case_id": "MC-CAR-ENTRE-001",

  "facts": {
    "entrepreneurship": "very_high",
    "independence": "very_high",
    "wealth_creation": "high",
    "business_expansion": "high",
    "management": "high"
  },

  "expected": {
    "primary_work_styles": [
      "entrepreneurial",
      "independent_autonomous"
    ]
  }
}
103. GOLDEN CASE — ENTREPRENEUR WITH RISK
{
  "case_id": "MC-CAR-ENTRE-RISK-001",

  "facts": {
    "entrepreneurship": "very_high",
    "wealth_creation": "high",
    "wealth_retention": "low",
    "financial_volatility": "very_high"
  },

  "expected": {
    "entrepreneurial_fit": [
      "high",
      "very_high"
    ],
    "career_risks_must_include": [
      "poor_capital_control",
      "overexpansion"
    ]
  }
}
104. GOLDEN CASE — SPECIALIST
{
  "case_id": "MC-CAR-SPEC-001",

  "facts": {
    "technical": "very_high",
    "academic": "high",
    "management": "moderate",
    "public_visibility": "low"
  },

  "expected": {
    "primary_work_styles": [
      "technical",
      "specialist"
    ]
  }
}
105. GOLDEN CASE — HIGH AUTONOMY INSIDE STRUCTURE
{
  "case_id": "MC-CAR-HYBRID-001",

  "facts": {
    "institutional_career": "high",
    "management": "high",
    "independence": "very_high"
  },

  "expected": {
    "conditions_for_expression_must_include": [
      "needs_decision_authority"
    ]
  }
}
106. NEGATIVE GOLDEN CASE — ONE TEN GOD
{
  "case_id": "MC-CAR-NEG-001",

  "facts": {
    "zheng_guan_present": true,
    "authority": "low"
  },

  "forbidden": {
    "primary_work_styles": [
      "structured_institutional"
    ]
  }
}
This verifies that raw Quan presence does not override Achievement evidence.
107. NEGATIVE GOLDEN CASE — BIOGRAPHY
Adding:
current_job = entrepreneur
must not increase:
entrepreneurial_fit
108. NEGATIVE GOLDEN CASE — HIGH GRADE
{
  "case_id": "MC-CAR-NEG-002",

  "facts": {
    "grade": "SS",
    "achievement_profile": {
      "entrepreneurship": "low"
    }
  },

  "forbidden": {
    "entrepreneurial_fit": "very_high"
  }
}
109. CAREER INVARIANTS
CAR-01
Career Model cannot map one Ten God directly to one profession.
CAR-02
Career Model must consume Achievement Profile.
CAR-03
Wealth Profile must inform entrepreneurial/commercial career analysis.
CAR-04
Leadership and Management must remain separate.
CAR-05
Entrepreneurial fit and Wealth potential must remain separate.
CAR-06
Specialist fit and Academic fit must remain separate.
CAR-07
Career Model must not use biography as inference input.
CAR-08
Natal Career Profile must not depend on current Đại Vận.
CAR-09
Career Model must preserve trade-offs.
CAR-10
Career Model must not predict exact job title.
CAR-11
Every fit dimension must have trace.
CAR-12
Same input + same ruleset = same Career Profile.
110. FAILURE CONDITIONS
Career implementation FAILS if it:
1. maps Chính Quan directly to government
2. maps Thiên Tài directly to entrepreneur
3. maps Ấn directly to teacher
4. maps Thương Quan directly to artist
5. ignores Achievement Profile
6. ignores Wealth Profile for business fit
7. collapses leadership and management
8. collapses career fit and wealth
9. uses biography
10. uses current luck cycle
11. outputs deterministic job title
12. outputs “must do / cannot do”
13. ignores conflicting career signals
14. produces recommendations without trace
15. double-counts the same causal evidence excessively
111. CAREER PIPELINE
Canonical:
StructuralIntegrityResult
      ↓
Pattern Grade
      ↓
AchievementProfile
      ↓
WealthProfile
      ↓
Collect career-domain evidence
      ↓
Resolve organizational fit
      ↓
Resolve leadership / management fit
      ↓
Resolve entrepreneurial fit
      ↓
Resolve specialist / technical / academic fit
      ↓
Resolve creative / public-facing fit
      ↓
Resolve autonomy need
      ↓
Resolve career stability
      ↓
Resolve structural risks
      ↓
Detect coherent work-style clusters
      ↓
Rank primary / secondary styles
      ↓
Resolve conditions / avoid conditions
      ↓
Resolve confidence
      ↓
Generate trace
      ↓
CareerProfile
112. TEN-QUESTION CAREER MODEL
Before Career Model is accepted,
it should be able to answer:
1. Hợp môi trường có hệ thống hay tự do?
2. Hợp làm chuyên môn hay quản lý?
3. Có thiên hướng lãnh đạo không?
4. Năng lực quản trị đến đâu?
5. Khả năng làm chủ / kinh doanh thế nào?
6. Có cần quyền tự chủ cao không?
7. Hợp kỹ thuật hay học thuật không?
8. Hợp sáng tạo / đối ngoại không?
9. Sự nghiệp thiên ổn định hay biến động?
10. Điều kiện nào giúp năng lực nghề nghiệp phát huy tốt nhất?
113. CAREER MODEL DOES NOT YET ANSWER TIMING
It does not answer:
khi nào thăng chức
khi nào đổi nghề
khi nào mở doanh nghiệp
That belongs to Luck activation.
114. CAREER MODEL DOES NOT ANSWER SALARY
It does not predict:
salary
income
net worth
Financial capacity is handled structurally by Wealth Model,
not exact economic outcomes.
115. CUSTOMER VALUE TARGET
Commercially, the output should eventually be closer to:
Thế mạnh nghề nghiệp:
Lãnh đạo – Quản trị

Môi trường phù hợp:
Có hệ thống nhưng cần quyền tự chủ cao

Khả năng làm chủ:
Cao

Khả năng chuyên môn sâu:
Khá

Rủi ro:
Dễ mở rộng quá nhanh nếu quản trị vốn không theo kịp

Khuyến nghị:
Phù hợp vai trò có quyền quyết định,
quản trị đội ngũ hoặc vận hành hoạt động riêng.
rather than:
Nghề hợp: kinh doanh.
116. ARCHITECTURAL DECISION
Canonical definition:
CAREER MODEL MAPS STRUCTURAL CAPABILITIES INTO WORK-STYLE AND ROLE FIT — NOT INTO DETERMINISTIC JOB TITLES.

The primary inference is:
Achievement capabilities
+
Wealth behavior
+
Structural Integrity
+
Autonomy
+
Stability
→ Career fit
not:
Ten God
→ profession
117. FINAL CONCEPTUAL MODEL
Career Fit
=
Achievement Capability
+ Organizational Compatibility
+ Role Compatibility
+ Autonomy Compatibility
+ Wealth / Business Sustainability
+ Structural Usability
- Career-Specific Risks
Exact weights remain unfrozen.
118. FREEZE TARGET
Before moving to Decision Composer, freeze:
multi-axis Career model
work-style IDs
organizational-fit model
leadership/management distinction
entrepreneurial-fit model
specialist-fit model
technical/academic/creative boundaries
autonomy model
career-stability model
career-risk model
Achievement/Career boundary
Wealth/Career boundary
Career/Luck boundary
no exact profession prediction
no biography fitting
trace requirement
119. NEXT DOCUMENT
Next:
11_DECISION_COMPOSER.md
Purpose:
- combine Pattern, Purity, Strength, Damage, Rescue, Integrity, Grade,
  Achievement, Wealth, and Career into one coherent customer-facing decision
- define headline
- define executive summary
- define strengths
- define risks
- define conditions for success
- define conditions to avoid
- prevent contradictory wording
- preserve uncertainty
- generate concise and detailed outputs from the same structured truth

Đến đây MC-01 đã đi được từ **“cách gì?”** cho tới **“người này phù hợp kiểu thành tựu, tài chính và nghề nghiệp nào?”** mà vẫn chưa phải dựa vào mô tả chung chung hay dữ liệu tiểu sử.

Bước tiếp theo `11_DECISION_COMPOSER.md` rất quan trọng vì nó sẽ gom toàn bộ các kết quả đang rời nhau thành một kết luận kiểu:

**Mệnh cục gì → chất lượng thế nào → điểm mạnh → điểm yếu → quan vận → tài vận → kinh doanh → nghề nghiệp → điều kiện để phát → điều cần tránh.**

Đây chính là tầng sẽ biến engine kỹ thuật thành bản luận mà khách hàng thực sự đọc và cảm thấy thuyết phục.