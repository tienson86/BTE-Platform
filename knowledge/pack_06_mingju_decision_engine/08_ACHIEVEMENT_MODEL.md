# MC-01 — ACHIEVEMENT MODEL

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `08_ACHIEVEMENT_MODEL.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the Achievement Model of MC-01.

The Achievement Model converts the validated natal structural result into
separate domain potentials.

It answers:

```text
If this natal structure is expressed successfully,
what kinds of achievement does it structurally favor?

It does NOT answer:
Will the person definitely become successful?
Will the person definitely become rich?
Will the person definitely become an official?
What exact career will the person have?
When will success occur?
Those require separate downstream models and Luck activation.
Canonical flow:
PatternDecision
      ↓
Purity
      ↓
Pattern Strength
      ↓
Damage
      ↓
Rescue
      ↓
Structural Integrity
      ↓
Pattern Grade
      ↓
Achievement Model
      ↓
Domain Potentials
2. CORE PRINCIPLE
There is no universal success score.
Forbidden:
success_score = 87
as the primary result.
Instead MC-01 must evaluate multiple distinct dimensions:
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
Wealth-specific dimensions belong mainly to 09_WEALTH_MODEL.md.
3. WHY MULTI-DIMENSIONAL ACHIEVEMENT IS REQUIRED
A chart may structurally favor:
authority = high
management = high
entrepreneurship = moderate
creative = low
Another may favor:
entrepreneurship = very_high
authority = low
independence = very_high
stability = moderate
A single score would destroy this distinction.
4. ACHIEVEMENT IS DOWNSTREAM FROM STRUCTURE
Achievement Model MUST consume:
PatternDecision
PatternPurityResult
PatternStrengthResult
Support
Damage
Rescue
StructuralIntegrityResult
PatternGradeResult
Ten Gods
Day Master Strength
Useful God compatibility
Climate compatibility
It MUST NOT bypass Structural Integrity.
5. GRADE VS ACHIEVEMENT
Critical distinction:
Grade
= how well the natal structure holds together

Achievement Profile
= what kinds of capability that structure may favor
Example:
Grade A
does not automatically mean:
authority = high
wealth = high
entrepreneurship = high
academic = high
Different pattern structures should produce different profiles.
6. ACHIEVEMENT OUTPUT
Canonical object:
AchievementProfile
Fields:
state
dimensions
dominant_capabilities
secondary_capabilities
structural_risks
conditions_for_expression
confidence
evidence_ids
7. ACHIEVEMENT DIMENSION
Canonical object:
AchievementDimension
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
trace_ids
8. ACHIEVEMENT SCORE
Canonical scale:
0..100
But score is not probability.
Example:
leadership_score = 82
means:
strong structural support for leadership-type capability
not:
82% chance of becoming a leader
9. ACHIEVEMENT CLASSIFICATION
Canonical enum:
very_low
low
below_average
moderate
above_average
high
very_high
unresolved
Provisional bands:
0–19    very_low
20–34   low
35–44   below_average
45–59   moderate
60–69   above_average
70–84   high
85–100  very_high
These thresholds remain configurable.
10. ACHIEVEMENT DIMENSIONS V1
Initial canonical IDs:
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
Do not add more dimensions until these are validated.
11. AUTHORITY POTENTIAL
authority evaluates structural capacity related to:
formal authority
command
responsibility
status
control
discipline
hierarchy
It does NOT mean:
guaranteed government office
12. AUTHORITY EVIDENCE
Potential positive evidence:
Chính Quan quality
Thất Sát quality
Quan/Sát root
Quan/Sát exposure
Tài sinh Quan
Ấn hộ Quan
Sát Ấn tương sinh
strong Structural Integrity
adequate Day Master capacity
Potential negative evidence:
Thương Quan công Quan
Quan/Sát severe mixing
Quan weak/rootless
Sát overload without transformation
major residual Damage
13. AUTHORITY IS NOT “QUAN EXISTS”
Forbidden:
Quan present
→ authority high
The engine must consider:
quality
strength
purity
damage
rescue
capacity
integrity
14. INSTITUTIONAL CAREER
institutional_career evaluates fit for environments with:
rules
hierarchy
procedures
structured advancement
formal responsibility
Examples may later include:
government
large organizations
regulated professions
corporate hierarchy
But the engine should store structural capability, not job titles.
15. INSTITUTIONAL CAREER SIGNALS
Potential positive signals:
Chính Quan
Chính Ấn
stable Quan–Ấn structure
high discipline structure
high stability
strong integrity
Potential reducers:
very strong unmediated Thương Quan
extreme independence
high volatility
major authority conflict
16. LEADERSHIP POTENTIAL
Leadership is not identical to authority.
Authority may be formal.
Leadership may arise from:
command
initiative
influence
decision capacity
ability to mobilize others
Potential signals:
Quan/Sát
Dương Nhẫn
Kiến Lộc
Tài
Thương Quan
strong Day Master
high independence
depending on structure.
17. LEADERSHIP VS MANAGEMENT
Critical distinction:
leadership
= direction, influence, command

management
= organization, systems, execution, coordination
A person may be:
leadership high
management moderate
or the reverse.
18. MANAGEMENT POTENTIAL
Potential signals:
Chính Quan
Chính Ấn
Tài
stable structure
strong continuity
moderate/high discipline
good resource organization
Potential reducers:
extreme structural fragmentation
very high volatility
uncontrolled peer competition
19. ENTREPRENEURSHIP POTENTIAL
entrepreneurship evaluates aptitude for:
initiative
market activity
resource mobilization
opportunity recognition
risk-taking
independence
expansion
It does NOT equal wealth.
20. ENTREPRENEURSHIP SIGNALS
Potential positive signals:
Thiên Tài
Chính Tài
Thực Thần
Thương Quan
Tỷ/Kiếp
leadership
independence
strong output→wealth chain
Potential negative signals:
extreme dependence on institutional structure
weak execution
severe wealth retention risk
major structural instability
21. ENTREPRENEURSHIP VS WEALTH
Critical distinction:
entrepreneurship
≠
wealth_creation
A chart may have:
entrepreneurship = very_high
wealth_retention = low
This could describe someone good at starting businesses but poor at retaining capital.
Wealth model handles the second part.
22. ACADEMIC POTENTIAL
academic evaluates structural support for:
learning
study
theory
knowledge accumulation
examination
research
teaching
Potential evidence:
Chính Ấn
Thiên Ấn
Thực Thần
Văn-related structures when formally modeled
high continuity
stable cognition structure
23. ACADEMIC IS NOT EDUCATIONAL OUTCOME
Forbidden:
Ấn strong
→ university degree guaranteed
Achievement model evaluates aptitude,
not guaranteed credential.
24. TECHNICAL POTENTIAL
technical evaluates capability related to:
systems
precision
engineering-like thinking
analysis
implementation
specialized skill
Potential evidence may include:
Ấn
Thực Thần
Thương Quan
Quan
strong structured output
stable technical continuity
Exact rules require Golden Cases.
25. CREATIVE POTENTIAL
creative evaluates:
expression
novelty
artistic production
concept generation
non-standard thinking
Potential signals:
Thực Thần
Thương Quan
Thiên Ấn
output structures
high expression
But creative potential must not equal:
good artist
automatically.
26. PUBLIC VISIBILITY
public_visibility evaluates structural tendency toward:
recognition
visibility
public influence
reputation
external expression
Potential signals:
output strength
authority structure
wealth visibility
strong exposed structure
public-facing coherence
27. PUBLIC VISIBILITY VS FAME
Critical distinction:
public_visibility
≠
guaranteed fame
It measures structural capacity for external recognition.
Luck, environment, profession, and opportunity affect realization.
28. INDEPENDENCE
independence evaluates:
autonomy
self-direction
resistance to external control
initiative
individual decision-making
Potential signals:
Tỷ Kiên
Kiếp Tài
Dương Nhẫn
Thương Quan
Thiên Tài
strong Day Master
29. HIGH INDEPENDENCE IS NOT ALWAYS GOOD
High independence may support:
entrepreneurship
leadership
but reduce:
institutional fit
compliance
stability
depending on structure.
This is why dimensions remain separate.
30. STABILITY
stability evaluates:
consistency
predictability
ability to sustain structure
resistance to volatility
long-term continuity
Potential evidence:
high Structural Integrity
Chính Quan
Chính Ấn
strong roots
low unresolved Damage
high continuity
Potential reducers:
fragmentation
heavy unresolved Damage
high conflict
unstable transformation
31. STABILITY IS NOT WEALTH RETENTION
These are related but distinct.
stability
= general structural continuity

wealth_retention
= ability to retain financial resources
Wealth retention belongs to 09_WEALTH_MODEL.md.
32. DIMENSION RULE ARCHITECTURE
Each dimension should be computed from:
positive structural signals
negative structural signals
integrity modifier
pattern-family context
capacity compatibility
critical conditions
33. DOMAIN RULE MODEL
Conceptual object:
AchievementRule
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
34. POSITIVE EVIDENCE
Each dimension should store:
positive_evidence_ids
Example authority:
E-MC-AUTH-001
E-MC-AUTH-002
35. NEGATIVE EVIDENCE
Each dimension should also store:
negative_evidence_ids
Example authority:
major hurting_officer attack
weak officer root
36. DOMAIN-SPECIFIC TRACE
Every score must have trace.
Bad:
leadership = 84
Good:
+ Thất Sát có lực
+ Nhật chủ đủ sức tiếp nhận
+ Có Ấn hóa Sát
+ Cấu trúc toàn cục Grade A
- Quan/Sát hơi tạp
= leadership high
37. INTEGRITY MODIFIER
Structural Integrity should affect confidence and usable expression.
Example:
leadership structural signals = high
Integrity = damaged
Final leadership score may remain meaningful,
but realization confidence should decrease.
Do not simply zero the dimension.
38. POTENTIAL VS USABILITY
Future model MAY distinguish:
raw_potential
usable_potential
Example:
raw leadership = 88
usable leadership = 72
because structural damage limits expression.
This is useful but not required in V1.
39. STRUCTURAL GRADE MODIFIER
Grade may provide a broad integrity modifier,
but must not become the main Achievement formula.
Forbidden:
Grade A
→ all dimensions +20
Grade reflects overall structure,
not domain-specific capability.
40. PATTERN FAMILY MODIFIER
Different pattern families emphasize different achievement domains.
Examples:
Chính Quan
→ authority / institutional / management

Thất Sát
→ leadership / authority / high-pressure command

Tài
→ commercial / resource / entrepreneurship

Ấn
→ academic / institutional / technical

Thực
→ creative / technical / production

Thương
→ creative / entrepreneurship / independence
These are directional tendencies,
not fixed conclusions.
41. PRIMARY PATTERN DOES NOT MONOPOLIZE PROFILE
Secondary structures matter.
Example:
primary = Chính Quan
secondary = Chính Ấn
may strengthen:
institutional_career
management
academic
Another:
primary = Thực Thần
secondary = Thiên Tài
may strengthen:
entrepreneurship
creative
wealth_creation
42. TEN-GOD CHAINS
Achievement Model should recognize coherent chains.
Examples:
Tài → Quan
may support:
authority
management
institutional career
Thực → Tài
may support:
entrepreneurship
production
commercialization
Sát → Ấn
may support:
authority
institutional career
technical discipline
43. CHAIN QUALITY MATTERS
A chain is useful only if:
components have force
links are valid
chain is not broken
structural integrity supports it
Theoretical elemental sequence alone is insufficient.
44. DAY MASTER CAPACITY
Some achievement structures require adequate Day Master capacity.
Example:
strong authority force
+
very weak Day Master
without rescue may reduce:
usable authority potential
because pressure exceeds capacity.
45. DAY MASTER CAPACITY MUST COME FROM STRENGTH ENGINE
MC-01 MUST consume canonical Day Master Strength.
No recalculation is allowed.
46. AUTHORITY MODEL — CORE FACTORS
Potential positive factor groups:
officer_quality
killer_quality
officer_root
killer_root
officer_support
seal_mediation
day_master_capacity
structural_integrity
Potential negative:
hurting_officer_damage
mixed_officer_killer_damage
killer_overload
weak_officer
major_residual_damage
47. AUTHORITY SUBDIMENSIONS
Authority may later split into:
formal_authority
command_authority
institutional_status
But V1 should keep one core authority score.
48. INSTITUTIONAL CAREER MODEL — CORE FACTORS
Positive:
Chính Quan
Chính Ấn
Quan–Ấn chain
stability
discipline structure
low structural volatility
Negative:
uncontrolled Thương Quan
extreme independence
severe hierarchy conflict
49. LEADERSHIP MODEL — CORE FACTORS
Positive:
Sát
Quan
Dương Nhẫn
Kiến Lộc
strong Day Master
independence
resource mobilization
Negative:
very low confidence
severe fragmentation
weak carrying capacity
50. MANAGEMENT MODEL — CORE FACTORS
Positive:
Quan
Ấn
Tài
stability
continuity
resource organization
Negative:
extreme volatility
uncontrolled peer conflict
poor structural continuity
51. ENTREPRENEURSHIP MODEL — CORE FACTORS
Positive:
Thiên Tài
Chính Tài
Thực
Thương
Tỷ/Kiếp
independence
output→wealth chain
Negative:
extreme risk without control
weak financial retention structure
very low stability
52. ACADEMIC MODEL — CORE FACTORS
Positive:
Chính Ấn
Thiên Ấn
Thực Thần
stable resource structure
high continuity
Negative:
resource damaged
extreme output/resource conflict
severe instability
53. TECHNICAL MODEL — CORE FACTORS
Potential positive:
Ấn
Thực
Thương
Quan
structured output
precision-oriented structure
This domain requires expert calibration.
Avoid overclaiming until Golden Cases exist.
54. CREATIVE MODEL — CORE FACTORS
Potential positive:
Thực Thần
Thương Quan
Thiên Ấn
output strength
independence
Potential negative:
extreme suppression of output
very rigid unresolved authority conflict
55. PUBLIC VISIBILITY MODEL — CORE FACTORS
Potential positive:
strong exposed pattern
output expression
authority visibility
wealth exposure
public-facing structural chain
Potential negative:
hidden-only structure
weak expression
severe instability
56. INDEPENDENCE MODEL — CORE FACTORS
Positive:
Tỷ Kiên
Kiếp Tài
Dương Nhẫn
Thương Quan
Thiên Tài
strong Day Master
Negative:
very dominant institutional dependence
weak self-force
57. STABILITY MODEL — CORE FACTORS
Positive:
high Integrity
strong roots
Chính Quan
Chính Ấn
low residual Damage
stable pattern continuity
Negative:
structural fragmentation
major unresolved Damage
unstable follow structure
unstable transformation
58. PATTERN-SPECIFIC TENDENCY TABLE
Conceptual only:
Pattern	Commonly Favored Domains
Chính Quan	authority, institutional, management, stability
Thất Sát	leadership, authority, command, high-pressure execution
Chính Tài	management, commercial discipline, stability
Thiên Tài	entrepreneurship, independence, commercial expansion
Chính Ấn	academic, institutional, technical, stability
Thiên Ấn	academic, technical, creative, specialized thinking
Thực Thần	creative, technical, production, entrepreneurship
Thương Quan	creative, entrepreneurship, independence, visibility
Kiến Lộc	leadership, independence, management
Dương Nhẫn	leadership, independence, command
Tòng Tài	commercial / resource-oriented domains
Tòng Quan Sát	authority / institutional / command
Tòng Nhi	output / creative / commercial expression
Tòng Vượng	leadership / independence depending structure
Hóa Khí	family-specific; dedicated rules required


This table MUST NOT be used as direct scoring.
59. NO DIRECT PATTERN→SCORE TABLE
Forbidden:
Chính Quan
authority = 90
management = 80
Pattern identity only determines applicable rule families.
Actual score requires chart-specific evidence.
60. POSITIVE AND NEGATIVE SIGNALS CAN COEXIST
Example:
strong Thất Sát
+
strong Ấn rescue
+
mixed Quan/Sát
may produce:
leadership high
authority high
institutional moderate/high
stability moderate
The system should preserve nuance.
61. DOMAIN CONFLICT
Some dimensions may be structurally in tension.
Example:
independence = very_high
institutional_career = moderate
This is not an error.
It may explain why the person performs better as:
autonomous leader
than as:
strict subordinate
The Composer can explain later.
62. DOMAIN SYNERGY
Some dimensions may reinforce each other.
Example:
authority high
management high
stability high
may create a coherent:
institutional leadership
theme.
Another:
entrepreneurship high
independence high
public_visibility high
may create:
entrepreneurial/public-facing
theme.
63. DOMINANT CAPABILITIES
dominant_capabilities should contain the strongest validated domains.
Example:
[
  "authority",
  "management",
  "institutional_career"
]
Ordering must be deterministic.
64. SECONDARY CAPABILITIES
secondary_capabilities contains meaningful but non-dominant domains.
Example:
[
  "academic",
  "stability"
]
65. DOMINANT CAPABILITY THRESHOLD
Do not define merely:
score >= 70
as dominant.
Dominance should consider:
absolute score
relative rank
confidence
difference from other dimensions
Exact rule remains unfrozen.
66. PROFILE THEMES
Achievement Profile may later expose:
profile_themes
Examples:
institutional_leader
entrepreneurial_builder
technical_specialist
academic_researcher
creative_independent
commercial_manager
These are downstream synthesis labels.
Do not calculate them before dimension scores are stable.
67. CONDITIONS FOR EXPRESSION
Each dimension should support:
conditions
Example authority:
requires adequate Day Master capacity
works best when Ấn mediation remains active
Example entrepreneurship:
requires financial discipline to prevent volatility
68. STRUCTURAL RISKS
Each dimension should support:
risks
Example leadership:
over-control
conflict with authority
overextension
These must be derived from structural evidence,
not generic personality text.
69. ACHIEVEMENT CONFIDENCE
Confidence depends on:
Integrity confidence
pattern confidence
domain evidence coverage
conflicting evidence
missing hour pillar
rule coverage
70. LOW RULE COVERAGE
If a domain lacks mature rules:
state = partially_resolved
or:
confidence = low
Do not fabricate precision.
71. UNRESOLVED INTEGRITY
If:
StructuralIntegrity.state = unresolved
Achievement dimensions should generally be:
unresolved
or low-confidence partial,
depending on rule design.
Do not emit very high-confidence life capability from unresolved structure.
72. GRADE D DOES NOT ZERO ACHIEVEMENT
A compromised structural pattern may still contain a strong isolated capability.
Therefore:
Grade D
does not automatically mean:
all achievement dimensions = very_low
But usability/confidence may be limited.
73. GRADE SS DOES NOT MAX ALL ACHIEVEMENT
Similarly:
Grade SS
does not mean all domains are very_high.
It only means the structural pattern is exceptionally coherent.
74. ACHIEVEMENT VS WEALTH MODEL
Wealth-specific dimensions are reserved for:
09_WEALTH_MODEL.md
Achievement may reference:
entrepreneurship
but should not own:
wealth_creation
wealth_accumulation
wealth_retention
financial_volatility
business_expansion
Those belong to Wealth Model.
75. ACHIEVEMENT VS CAREER MODEL
Achievement evaluates structural capability.
Career Model later maps capability profiles into work environments and career directions.
Example:
authority high
management high
stability high
Achievement Model stops there.
Career Model may later interpret:
structured management / institutional leadership
76. ACHIEVEMENT VS LUCK
Natal Achievement Profile answers:
What capability exists structurally?
Luck answers:
When is that capability easier or harder to activate?
Natal scores must remain stable across Đại Vận.
77. FUTURE ACTIVATION MODEL
Future:
Natal leadership = 82
Luck activation 2031–2040 = high
Do not rewrite:
Natal leadership = 95
just because the luck cycle is favorable.
78. NO BIOGRAPHICAL FITTING
Forbidden:
user is CEO
→ leadership score increased
Biography may be used for validation only.
Never use observed life outcome as hidden inference input.
79. NO PROFESSION FITTING
Likewise:
customer is doctor
→ academic score high
is forbidden.
The engine must infer independently.
80. DOMAIN SCORE MODEL
Conceptually:
Domain Potential
=
Pattern-specific signals
+ coherent Ten-God chains
+ capacity compatibility
+ structural support
- domain-specific damage
± Integrity usability
Exact numeric formula remains unfrozen.
81. DOMAIN SCORE SHOULD NOT BE RAW COUNT
Forbidden:
2 Quan = authority 80
3 Ấn = academic 90
Structural context is mandatory.
82. SIGNAL STRENGTH
Each domain evidence should consider:
visibility
root
season
pattern relevance
integrity
damage
rescue
83. DOMAIN EVIDENCE MODEL
Recommended:
AchievementEvidence
Fields:
evidence_id
dimension
signal_type
direction
strength
structural_role
source_stage
source_id
confidence
causal_group
84. DOMAIN SIGNAL TYPES
Initial:
pattern_identity
pattern_strength
pattern_purity
support_chain
damage
rescue
day_master_capacity
ten_god_structure
structural_integrity
compatibility
climate
85. CAUSAL DEDUPLICATION
The same Quan structure should not produce:
authority +30
leadership +30
management +30
institutional +30
without domain-specific justification.
The evidence may support several dimensions,
but each dimension must apply a separate rule.
86. CROSS-DOMAIN EVIDENCE IS ALLOWED
Example:
strong Chính Quan
may legitimately support:
authority
institutional_career
management
stability
But with different effects and rule IDs.
87. ACHIEVEMENT RULE NAMESPACES
Recommended:
MC-ACH-AUTH-*
MC-ACH-INSTITUTION-*
MC-ACH-LEAD-*
MC-ACH-MGMT-*
MC-ACH-ENTRE-*
MC-ACH-ACADEMIC-*
MC-ACH-TECH-*
MC-ACH-CREATIVE-*
MC-ACH-VISIBILITY-*
MC-ACH-INDEPENDENCE-*
MC-ACH-STABILITY-*
MC-ACH-GENERAL-*
88. RULE PRIORITY
Suggested conceptual precedence:
explicit exception
>
family-specific domain rule
>
pattern-specific domain rule
>
Ten-God chain rule
>
general achievement rule
89. FAMILY-SPECIFIC HANDLING
Follow and transformation structures require dedicated Achievement logic.
Do not blindly apply ordinary Ten-God profiles.
90. FOLLOW PATTERN ACHIEVEMENT
Examples:
cong_cai
→ commercial/resource orientation

cong_guan_sha
→ authority/institutional orientation

cong_er
→ output/creative/commercial orientation
But only if follow structure Integrity is valid.
91. TRANSFORMATION ACHIEVEMENT
For:
hua_qi
achievement profile should depend on:
transformed structural theme
transformation stability
useful-god compatibility
integrity
No generic score should be assigned without dedicated rules.
92. ROOT PROSPERITY ACHIEVEMENT
For:
jian_lu
yang_ren
likely important domains:
leadership
independence
management
command
entrepreneurship
But control/outlet structure determines usability.
93. ACHIEVEMENT PROFILE EXAMPLE
Illustrative:
{
  "state": "resolved",

  "dimensions": {
    "authority": {
      "score": 82,
      "classification": "high",
      "confidence": 0.9
    },

    "institutional_career": {
      "score": 78,
      "classification": "high",
      "confidence": 0.88
    },

    "leadership": {
      "score": 85,
      "classification": "very_high",
      "confidence": 0.87
    },

    "management": {
      "score": 80,
      "classification": "high",
      "confidence": 0.91
    },

    "entrepreneurship": {
      "score": 61,
      "classification": "above_average",
      "confidence": 0.81
    }
  },

  "dominant_capabilities": [
    "leadership",
    "authority",
    "management"
  ]
}
Numbers are illustrative only.
94. PROFILE EXAMPLE — ENTREPRENEURIAL
entrepreneurship = very_high
independence = very_high
public_visibility = high
leadership = high
institutional_career = below_average
stability = moderate
This is a valid profile.
95. PROFILE EXAMPLE — ACADEMIC / TECHNICAL
academic = very_high
technical = high
stability = high
institutional_career = high
entrepreneurship = low
public_visibility = moderate
Also valid.
96. PROFILE EXAMPLE — MIXED TALENT
The engine may produce:
authority = high
creative = high
independence = high
stability = low
This apparent tension is useful,
not an error.
Composer should explain the trade-off.
97. DOMINANT PROFILE SHOULD NOT HIDE TRADE-OFFS
If:
leadership = high
stability = low
do not summarize only:
born leader
Later Composer should include both capability and risk.
98. CUSTOMER-FACING PRESENTATION
Future UI may display:
NĂNG LỰC THÀNH TỰU

Lãnh đạo
★★★★☆

Quản trị
★★★★☆

Quan vận / hệ thống
★★★★☆

Kinh doanh
★★★☆☆

Học thuật
★★★☆☆

Sáng tạo
★★☆☆☆

Tính độc lập
★★★★☆
But engine should store numeric structured dimensions.
99. CUSTOMER-FACING HEADLINE
Possible Composer output:
Cấu trúc thiên về quản trị và lãnh đạo trong môi trường có tổ chức.
or:
Cấu trúc nổi bật về tính độc lập, thương mại và khả năng tự triển khai công việc.
These are downstream summaries.
100. CUSTOMER WORDING SAFETY
Avoid:
Bạn sinh ra để làm lãnh đạo.
Prefer:
Lá số có nhiều tín hiệu hỗ trợ năng lực lãnh đạo và quản trị.
Avoid:
Bạn không hợp làm công.
Prefer:
Tính độc lập cao có thể khiến môi trường quá cứng nhắc khó phát huy hết năng lực.
101. GOLDEN DATASET REQUIREMENTS
Achievement Golden Cases must cover:
pure Chính Quan
Quan–Ấn structure
Sát–Ấn structure
strong Thiên Tài
Thực sinh Tài
Thương Quan strong
Kiến Lộc
Dương Nhẫn
Tòng Tài
Tòng Quan Sát
Tòng Nhi
academic/resource-heavy structure
creative/output-heavy structure
high independence
high authority + low independence
high entrepreneurship + low stability
mixed talent profile
damaged authority structure
rescued authority structure
unresolved pattern
102. GOLDEN CASE — AUTHORITY
Example:
{
  "case_id": "MC-ACH-AUTH-001",

  "facts": {
    "pattern": "zheng_guan",
    "pattern_strength": "strong",
    "integrity": "substantially_complete",
    "officer_rooted": true,
    "officer_supported": true,
    "major_officer_damage": false
  },

  "expected": {
    "authority": [
      "high",
      "very_high"
    ]
  }
}
103. GOLDEN CASE — DAMAGED AUTHORITY
{
  "case_id": "MC-ACH-AUTH-DMG-001",

  "facts": {
    "pattern": "zheng_guan",
    "pattern_strength": "strong",
    "damage": "hurting_officer_attacks_officer",
    "rescue": "none"
  },

  "forbidden": {
    "authority": "very_high"
  }
}
104. GOLDEN CASE — RESCUED AUTHORITY
{
  "case_id": "MC-ACH-AUTH-RSC-001",

  "facts": {
    "damage": "hurting_officer_attacks_officer",
    "rescue": "seal_controls_hurting_officer",
    "integrity": "damaged_but_rescued"
  },

  "expected": {
    "authority": [
      "above_average",
      "high"
    ]
  }
}
Exact calibration remains open.
105. GOLDEN CASE — ENTREPRENEURSHIP
{
  "case_id": "MC-ACH-ENTRE-001",

  "facts": {
    "wealth_structure": "strong",
    "output_to_wealth_chain": true,
    "independence_signals": "strong",
    "integrity": "strong"
  },

  "expected": {
    "entrepreneurship": [
      "high",
      "very_high"
    ]
  }
}
106. GOLDEN CASE — ACADEMIC
{
  "case_id": "MC-ACH-ACADEMIC-001",

  "facts": {
    "resource_structure": "strong",
    "resource_integrity": "high",
    "structural_continuity": "high"
  },

  "expected": {
    "academic": [
      "high",
      "very_high"
    ]
  }
}
107. NEGATIVE GOLDEN CASE — ONE TEN GOD
{
  "case_id": "MC-ACH-NEG-001",

  "facts": {
    "zheng_guan_present": true,
    "zheng_guan_strength": "very_weak"
  },

  "forbidden": {
    "authority": "very_high"
  }
}
This prevents presence-only scoring.
108. NEGATIVE GOLDEN CASE — HIGH GRADE
{
  "case_id": "MC-ACH-NEG-002",

  "facts": {
    "grade": "SS",
    "pattern": "zheng_yin"
  },

  "forbidden": {
    "all_dimensions": "very_high"
  }
}
109. NEGATIVE GOLDEN CASE — BIOGRAPHY
Tests must prove that adding:
job_title = CEO
or:
income = high
does not change Achievement Profile.
110. ACHIEVEMENT INVARIANTS
ACH-01
There is no mandatory universal success score.
ACH-02
Each dimension must be independently traceable.
ACH-03
Pattern identity alone cannot determine a final domain score.
ACH-04
Ten-God presence alone cannot determine a final domain score.
ACH-05
Grade alone cannot determine domain scores.
ACH-06
Achievement must consume Structural Integrity.
ACH-07
Achievement must not use biography as inference input.
ACH-08
Achievement must not depend on current Đại Vận for natal scores.
ACH-09
Achievement must preserve conflicting strengths and weaknesses.
ACH-10
Unresolved structure must not produce false high-confidence domain scores.
ACH-11
Same input + same ruleset = same Achievement Profile.
ACH-12
Wealth-specific financial outputs remain owned by Wealth Model.
111. FAILURE CONDITIONS
Achievement implementation FAILS if it:
1. creates only one success score
2. maps pattern directly to fixed domain scores
3. treats Quan presence as guaranteed authority
4. treats Tài presence as entrepreneurship automatically
5. treats Ấn presence as academic success automatically
6. treats Thương Quan as creative genius automatically
7. ignores Damage
8. ignores Rescue
9. ignores Structural Integrity
10. uses biography
11. uses current luck cycle
12. assigns job titles directly
13. collapses leadership and management
14. collapses entrepreneurship and wealth
15. produces unexplained scores
112. RULE NAMESPACE
Recommended:
MC-ACH-AUTH-*
MC-ACH-INST-*
MC-ACH-LEAD-*
MC-ACH-MGMT-*
MC-ACH-ENTRE-*
MC-ACH-ACA-*
MC-ACH-TECH-*
MC-ACH-CREAT-*
MC-ACH-VIS-*
MC-ACH-IND-*
MC-ACH-STAB-*
MC-ACH-GENERAL-*
113. ACHIEVEMENT PIPELINE
Canonical:
StructuralIntegrityResult
      ↓
Pattern Grade
      ↓
Select domain rule families
      ↓
Collect Ten-God structural signals
      ↓
Collect pattern-family signals
      ↓
Collect coherent structural chains
      ↓
Apply Day Master capacity context
      ↓
Apply Damage / Rescue effects
      ↓
Apply Integrity usability
      ↓
Deduplicate causal evidence
      ↓
Resolve each domain independently
      ↓
Resolve confidence
      ↓
Rank dominant capabilities
      ↓
Generate trace
      ↓
AchievementProfile
114. PROFILE RANKING
Domain ranking should be deterministic.
Recommended ordering criteria:
score desc
confidence desc
canonical dimension order
Do not use random tie-breaks.
115. CANONICAL DIMENSION ORDER
Recommended stable order:
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
This supports stable serialization and UI.
116. CONFIDENCE POLICY
A dimension may have:
score = high
confidence = low
This is valid.
Example:
strong leadership signals
but unresolved transformation structure
UI should not hide low confidence.
117. PROFILE STATE
Allowed:
resolved
partially_resolved
unresolved
insufficient_evidence
A profile may be partially resolved if only some dimensions have adequate rules.
118. STRUCTURAL RISKS
AchievementProfile should preserve profile-level risks.
Examples:
high_authority_low_flexibility
high_independence_low_institutional_fit
high_entrepreneurship_low_stability
high_creativity_low_structure
high_management_low_independence
These are synthesis findings,
not deterministic personality judgments.
119. PROFILE CONDITION EXAMPLES
Possible conditions:
performs best with formal authority
needs autonomy
requires stable support structure
benefits from strong team/process
needs financial controls
benefits from specialist environment
Composer generates final language.
120. ACHIEVEMENT MODEL DOES NOT DECIDE “RICH OR POOR”
This boundary is mandatory.
Achievement Model can say:
entrepreneurship = high
management = high
But it cannot yet conclude:
wealth = high
because financial capacity requires separate evaluation of:
Tài quality
wealth creation
wealth retention
competition
capacity
volatility
That belongs to 09_WEALTH_MODEL.md.
121. ACHIEVEMENT MODEL DOES NOT DECIDE EXACT CAREER
It can say:
authority high
management high
institutional fit high
But should not directly output:
police
judge
bank director
Career mapping belongs to 10_CAREER_MODEL.md.
122. ARCHITECTURAL DECISION
Canonical definition:
ACHIEVEMENT MODEL MEASURES THE DOMAIN-SPECIFIC CAPABILITIES SUPPORTED BY THE NATAL STRUCTURE AFTER STRUCTURAL INTEGRITY HAS BEEN RESOLVED.

It is multi-dimensional.
It is not:
one success score
one destiny ranking
one profession prediction
123. FINAL CONCEPTUAL MODEL
Conceptually:
Achievement Dimension
=
Relevant Pattern Signals
+ Ten-God Structural Signals
+ Coherent Chains
+ Capacity Compatibility
+ Structural Support
- Domain-Specific Damage
+ Valid Rescue
± Integrity Usability
Exact weights remain unfrozen.
124. FREEZE TARGET
Before moving to Wealth Model, freeze:
multi-dimensional achievement principle
dimension IDs
authority definition
institutional career definition
leadership definition
management definition
entrepreneurship definition
academic definition
technical definition
creative definition
public visibility definition
independence definition
stability definition
Grade/Achievement boundary
Achievement/Wealth boundary
Achievement/Career boundary
Achievement/Luck boundary
no biography fitting
no direct pattern→score mapping
trace requirement
125. NEXT DOCUMENT
Next:
09_WEALTH_MODEL.md
Purpose:
- define wealth creation
- define wealth accumulation
- define wealth retention
- define business expansion
- define financial volatility
- distinguish Tài strength from actual wealth potential
- evaluate Day Master carrying capacity
- evaluate Thực/Thương → Tài
- evaluate Tỷ/Kiếp pressure
- evaluate Quan protection
- evaluate Tài as Dụng/Hỷ/Kỵ
- distinguish “kiếm được tiền” from “giữ được tiền”
- avoid direct claims of rich / poor until validated

Đến đây chúng ta đã có thể tách một câu rất quan trọng mà trước đây thường bị nhập làm một: **“người này có năng lực thành tựu cao không?”** và **“người này có giàu không?”** là hai bài toán khác nhau.

Ví dụ hoàn toàn có thể có người **lãnh đạo rất mạnh nhưng tài vận chỉ khá**, hoặc **kinh doanh rất mạnh nhưng khả năng giữ tiền yếu**. Vì vậy `09_WEALTH_MODEL.md` tiếp theo sẽ là file cực kỳ quan trọng để giải riêng bài toán **tạo tiền – tích lũy – giữ tiền – mở rộng tài sản – biến động tài chính**, thay vì chỉ nhìn thấy Tài tinh rồi kết luận giàu.