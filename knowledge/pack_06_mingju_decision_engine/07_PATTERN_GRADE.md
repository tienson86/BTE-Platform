# MC-01 — STRUCTURAL INTEGRITY & PATTERN GRADE

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `07_PATTERN_GRADE.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines:

1. Structural Integrity synthesis
2. residual Damage after Rescue
3. structural-state classification
4. Pattern Grade
5. confidence propagation
6. grade traceability

Canonical flow:

```text
PatternDecision
      ↓
PatternPurityResult
      ↓
PatternStrengthResult
      ↓
Support
      ↓
Damage
      ↓
Rescue
      ↓
Useful-God Compatibility
      ↓
Climate Compatibility
      ↓
Structural Integrity
      ↓
Pattern Grade
The critical rule is:
STRUCTURAL INTEGRITY FIRST
GRADE SECOND
2. CORE PRINCIPLE
Grade is not a primitive fact.
Grade is a downstream summary of structural integrity.
Forbidden:
Pattern Strength = strong
→ Grade A
Forbidden:
Purity = very_pure
→ Grade S
Forbidden:
Rescue = strong
→ Grade A
Correct logic:
Purity
+ Strength
+ Support
- Damage
+ Rescue
+ Useful-God Compatibility
+ Climate Compatibility
→ Structural Integrity
→ Grade
3. STRUCTURAL INTEGRITY DEFINITION
Structural Integrity answers:
After all major structural forces are considered,
does the natal pattern actually hold together and function?
It evaluates:
- clarity
- power
- support
- damage
- rescue
- residual impairment
- compatibility
- climate
- unresolved uncertainty
4. STRUCTURAL INTEGRITY IS NOT SUCCESS
Critical rule:
HIGH INTEGRITY ≠ GUARANTEED SUCCESS
Structural Integrity describes the quality of natal structural organization.
It does not directly guarantee:
- wealth
- authority
- fame
- career success
- happiness
- social rank
Those belong to downstream Achievement models.
5. STRUCTURAL INTEGRITY OUTPUT
Canonical object:
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
residual_damage
critical_findings
positive_findings
negative_findings
evidence_ids
confidence
6. STRUCTURAL STATE ENUM
Canonical states:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
These states describe structure,
not life outcome.
7. STATE — COMPLETE
complete means:
primary pattern is clear
structural force is adequate
support is coherent
no major unresolved Damage
or Damage is negligible
compatibility is acceptable
structure functions without major dependency
This is a high-integrity state.
8. STATE — SUBSTANTIALLY COMPLETE
substantially_complete means:
structure is fundamentally sound
minor imperfections exist
some mixing or weakness exists
but core function remains stable
Typical profile:
Purity = moderate/high
Strength = moderate/strong
Damage = none/minor
Rescue = optional
9. STATE — CONDITIONALLY COMPLETE
conditionally_complete means:
structure can function well
but depends on one or more important conditions
Examples:
pattern needs a specific support structure
pattern depends on a bridge
pattern depends on climate balance
pattern depends on a rescue mechanism
If the condition is absent,
integrity may fall materially.
10. STATE — MIXED
mixed means:
multiple structurally meaningful forces coexist
without complete single-theme clarity
but the chart is not necessarily damaged
Important:
mixed ≠ bad
This state is used when Purity is materially reduced
but core functionality is not clearly broken.
11. STATE — DAMAGED_BUT_RESCUED
This state is critical.
It means:
significant Damage exists
but a valid Rescue mechanism materially mitigates it
Example:
Damage = major
Rescue = strong
Residual Damage = moderate/minor
This state must NOT be collapsed into:
complete
because the repair mechanism remains structurally important.
12. STATE — DAMAGED
damaged means:
significant Damage remains after available Rescue
The pattern still exists,
but functionality is materially impaired.
Possible profile:
Damage = major
Rescue = weak/none
or:
multiple moderate damages remain active
13. STATE — FAILED
failed is the strongest structural-negative classification.
Use only when:
core pattern function collapses
and
major/critical Damage remains
and
Rescue is absent or ineffective
and
structural identity cannot function as intended
failed must be rare.
14. FAILED IS NOT “POOR DESTINY”
Forbidden interpretation:
failed pattern
→ poor person
→ no success
Correct meaning:
the accepted natal pattern does not function coherently
The person may still have other usable structures.
15. STATE — UNRESOLVED
Use when:
pattern unresolved
major transformation unresolved
damage/rescue relation unresolved
critical upstream facts missing
Then:
integrity.score = null
grade = UNRESOLVED
Do not force a grade.
16. RESIDUAL DAMAGE
Structural Integrity must evaluate:
Damage after Rescue
not just original Damage.
Conceptually:
Residual Damage
=
Original Damage
-
Effective Rescue
Exact numeric formula remains unfrozen.
17. RESIDUAL DAMAGE MODEL
Recommended object:
ResidualDamageResult
Fields:
damage_id
original_severity
rescue_ids
effective_rescue
residual_severity
residual_state
confidence
evidence_ids
18. RESIDUAL SEVERITY
Suggested states:
none
minor
moderate
major
critical
unresolved
19. EFFECTIVE RESCUE
Effective Rescue should consider:
rescue strength
rescue reliability
rescue coverage
mechanism validity
target match
Conceptually:
effective_rescue
=
strength
× reliability
× coverage
× target relevance
Exact weights are not frozen.
20. ONE DAMAGE, MULTIPLE RESCUES
For:
DMG-001
there may be:
RSC-001
RSC-002
Integrity must combine them carefully.
Do not assume:
0.6 + 0.6 = 1.2
Rescue contributions may overlap.
Causal deduplication is required.
21. MULTIPLE DAMAGES
Integrity must preserve each Damage.
Example:
DMG-001 = major, rescued strongly
DMG-002 = moderate, no rescue
The chart should not be classified solely from the first repaired damage.
22. UNTREATED DAMAGE
untargeted_damage_ids from RescueResult are structurally important.
Any:
major
critical
untreated Damage should substantially limit Integrity.
23. SUPPORT COMPONENT
Support should improve Integrity only where it genuinely helps the pattern function.
Examples:
Tài sinh Quan
Ấn hộ Quan
root support
generation chain
Do not count every positive factor as equivalent.
24. SUPPORT VS RESCUE IN INTEGRITY
Both may contribute,
but they represent different roles.
Support
= structure was stronger because of help

Rescue
= Damage was mitigated after it occurred
Avoid double counting the same causal force.
25. PURITY COMPONENT
Purity influences:
clarity
coherence
ambiguity
competition
High Purity can support Integrity.
Low Purity can reduce Integrity.
But Purity must not dominate the entire decision.
26. STRENGTH COMPONENT
Pattern Strength influences whether the pattern has enough force to function.
Weak structure may reduce Integrity.
But excessive force may also require later contextual evaluation.
Therefore:
very_strong
is not automatically better than:
strong
27. NON-LINEAR STRENGTH PRINCIPLE
For some patterns:
too weak
is poor.
But:
too strong
may also be problematic if uncontrolled.
Therefore future Integrity scoring should permit:
optimal range
rather than:
more strength = always better
28. USEFUL-GOD COMPATIBILITY COMPONENT
Integrity should consider whether the pattern's structural needs align with:
Dụng Thần
Hỷ Thần
Kỵ Thần
Possible states:
strongly_aligned
aligned
partially_aligned
neutral
conflicting
strongly_conflicting
29. COMPATIBILITY IS NOT PATTERN IDENTITY
Example:
pattern = Chính Quan
may be structurally clear,
but its expression may conflict with Useful God needs.
Integrity should preserve this tension.
30. CLIMATE COMPONENT
Điều Hậu / climate may materially affect whether structure functions.
Example:
pattern structurally strong
but chart excessively cold
and required warming absent
Integrity may be reduced even if Pattern Strength is high.
31. CLIMATE DOES NOT REWRITE PURITY
High climate imbalance does not make pattern impure.
It affects Integrity through climate compatibility.
32. INTEGRITY COMPONENT MODEL
Recommended internal dimensions:
clarity
structural_power
support_quality
residual_damage
compatibility
climate_viability
This is more interpretable than one hidden formula.
33. INTEGRITY SCORE
Canonical score:
0..100
However exact aggregation remains unfrozen.
Provisional conceptual interpretation:
90–100 exceptional integrity
80–89  very high integrity
70–79  strong integrity
60–69  workable integrity
45–59  compromised integrity
30–44  heavily compromised
0–29   severe structural failure
These bands are provisional.
34. STRUCTURAL STATE VS SCORE
Structural state must not be inferred from score alone.
Example:
score = 78
could be:
substantially_complete
or:
damaged_but_rescued
depending on path.
State preserves structural story.
35. WHY STATE MATTERS
These two charts may both score 78:
Chart A:
small imperfections, no damage

Chart B:
major damage, strong rescue
They should not receive identical structural explanation.
Therefore:
score
+
state
are both required.
36. STATE PRECEDENCE
Suggested conceptual precedence:
unresolved
>
failed
>
damaged
>
damaged_but_rescued
>
conditionally_complete
>
mixed
>
substantially_complete
>
complete
This is not a ranking of quality.
It is a resolution hierarchy for selecting the most informative state.
37. STATE RESOLUTION LOGIC
Example conceptual logic:
IF core evidence unresolved
→ unresolved

ELSE IF critical residual damage destroys core function
→ failed

ELSE IF major residual damage remains
→ damaged

ELSE IF major original damage existed
        AND rescue materially reduced it
→ damaged_but_rescued

ELSE IF pattern depends on major structural condition
→ conditionally_complete

ELSE IF material structural mixing remains
→ mixed

ELSE IF minor imperfections remain
→ substantially_complete

ELSE
→ complete
This is conceptual,
not final executable logic.
38. FAILED THRESHOLD
failed requires strong evidence.
Suggested prerequisites:
primary pattern still identified
core function materially destroyed
critical/major residual damage
no adequate rescue
low structural continuity
Do not use:
purity low
alone to declare failure.
39. DAMAGED_BUT_RESCUED THRESHOLD
Requires:
confirmed original Damage >= moderate
valid Rescue
Rescue addresses core Damage
Residual Damage materially reduced
This state should not be assigned if Rescue is merely symbolic.
40. CONDITIONALLY_COMPLETE THRESHOLD
Typical cases:
structure depends heavily on Ấn
structure depends on bridge element
structure depends on climate correction
structure depends on specific control mechanism
The condition must be structurally important.
41. MIXED THRESHOLD
Use when:
Purity materially mixed
but:
no major residual Damage
and:
core function remains available
42. COMPLETE VS SUBSTANTIALLY COMPLETE
complete should be relatively strict.
substantially_complete is appropriate when:
core structure works
but minor structural imperfections remain
This avoids inflating Grade.
43. CONFIDENCE PROPAGATION
Integrity confidence depends on:
Pattern confidence
Purity confidence
Pattern Strength confidence
Damage confidence
Rescue confidence
Useful-God compatibility confidence
Climate confidence
input completeness
44. CONFIDENCE IS NOT AVERAGE ONLY
Simple arithmetic average may hide critical uncertainty.
Example:
all components confidence ~0.95
but transformation confidence = 0.35
If transformation is core to the pattern,
Integrity confidence must reflect that critical low-confidence dependency.
45. CRITICAL DEPENDENCY PRINCIPLE
Integrity confidence should identify:
critical_dependency_ids
Any low-confidence critical dependency may cap overall confidence.
46. INTEGRITY WARNING MODEL
Possible warnings:
low_pattern_confidence
major_damage_unresolved
rescue_relation_uncertain
useful_god_conflict
climate_conflict
transformation_unresolved
follow_structure_unstable
missing_hour_pillar
47. GRADE MODEL
Canonical object:
PatternGradeResult
Fields:
state
grade
score
confidence
basis
integrity_state
evidence_ids
warnings
48. GRADE ENUM
Canonical:
SS
S
A
B
C
D
UNRESOLVED
49. GRADE SEMANTICS
Canonical meanings:
SS
= exceptional structural integrity

S
= very high structural integrity

A
= strong structural integrity

B
= workable / conditional structure

C
= substantially compromised structure

D
= severely compromised structure

UNRESOLVED
= insufficient basis
50. GRADE IS STRUCTURAL ONLY
Grade MUST NOT directly mean:
SS = đại phú đại quý
S = giàu lớn
A = giàu
B = trung bình
C = nghèo
D = khổ
This mapping is forbidden.
51. PROVISIONAL GRADE BANDS
Suggested initial bands:
90–100 → SS
82–89  → S
72–81  → A
60–71  → B
45–59  → C
0–44   → D
These are provisional only.
Golden Dataset calibration is mandatory.
52. GRADE STATE GUARD
Grade may not be resolved when:
StructuralIntegrity.state = unresolved
Then:
grade = UNRESOLVED
score = null
53. GRADE STATE CAP
Structural state may constrain Grade.
Example conceptual caps:
failed
→ cannot exceed D/C

damaged
→ cannot exceed B/C without exceptional justification

damaged_but_rescued
→ may reach B/A depending on residual impairment

conditionally_complete
→ may reach A/S depending on condition stability

complete
→ may qualify for high Grade
Exact caps remain unfrozen.
54. WHY STATE CAP MAY BE NEEDED
Without state constraints,
a chart could theoretically produce:
Integrity score = 86
State = damaged
Grade = S
which may be structurally contradictory.
State-aware calibration prevents this.
55. GRADE DOES NOT OVERRIDE STATE
Example:
Grade = A
State = damaged_but_rescued
customer interpretation should preserve both.
Do not display only:
A
and hide the structural condition.
56. GRADE BASIS
basis should summarize key factors.
Example:
high purity
strong pattern force
major damage
strong rescue
moderate useful-god alignment
These are structured IDs, not prose.
57. GRADE TRACE
Every Grade must be traceable.
Bad:
grade = A
Good:
Purity = 84 / pure
Pattern Strength = 79 / strong
Damage = major
Rescue = substantial
Residual Damage = minor
Integrity state = damaged_but_rescued
Integrity score = 78
Grade = A
58. NO HIDDEN GRADE ADJUSTMENT
Forbidden:
expert thinks chart looks better
→ manually +8 points
All adjustments must be rule-based and traceable.
59. GRADE CONFIDENCE
Grade confidence should generally equal or be bounded by Integrity confidence.
Do not emit:
Integrity confidence = 0.58
Grade confidence = 0.95
without explicit justification.
60. GRADE ROUNDING
Serialized Grade score should:
maximum 2 decimal places
Internal precision may be higher.
61. GRADE TIE / BOUNDARY POLICY
Example:
score = 81.99
must deterministically map according to defined threshold.
Do not use fuzzy runtime boundaries.
62. GRADE THRESHOLD VERSIONING
Grade thresholds belong to:
bte.mingju.rules.v1
not hard-coded UI.
Changing thresholds requires ruleset version update.
63. INTEGRITY FORMULA — NOT FROZEN YET
Do not freeze:
Purity 20%
Strength 25%
Support 15%
Damage -20%
Rescue +10%
Compatibility 5%
Climate 5%
yet.
This would create false precision.
64. REQUIRED PRE-CALIBRATION WORK
Before final weights:
define all structural factors
build Golden Cases
expert-label integrity states
compare candidate formulas
analyze contradictions
calibrate thresholds
65. CALIBRATION STRATEGY
Recommended future process:
Golden Case
→ experts assign:
   structural state
   acceptable score range
   acceptable Grade range

Engine candidate weights
→ compare

Adjust rules
→ rerun

Freeze when stable
66. EXPERT VALIDATION SHOULD FOCUS ON STATE FIRST
Experts should first answer:
Thành cách?
Thành cách có điều kiện?
Tạp nhưng dùng được?
Bị phá có cứu?
Bị phá?
Bại cách?
Only after that should numeric Grade be calibrated.
67. WHY STATE-FIRST VALIDATION
Traditional reasoning is more naturally expressed in structural states than arbitrary scores.
For example:
Thương Quan kiến Quan nhưng Ấn chế được Thương
maps naturally to:
damaged_but_rescued
before assigning:
A / B
68. SUPPORT-RESCUE DOUBLE COUNTING
If the same Ấn:
supports Day Master
and:
transforms Sát
Integrity must distinguish:
support role
rescue role
but avoid unrestricted double reward.
Use causal groups.
69. DAMAGE-STRENGTH DOUBLE COUNTING
If root destruction has already reduced:
Pattern Strength
and is also registered as:
Damage
Integrity must avoid applying full penalty twice.
This is one of the most important implementation risks.
70. CAUSAL ACCOUNTING
Recommended concept:
IntegrityContribution
Fields:
contribution_id
source_stage
source_id
causal_group
direction
importance
overlap_group
evidence_ids
This allows later aggregation without uncontrolled duplication.
71. CAUSAL GROUP EXAMPLES
month_pattern_power
primary_root
guan_sha_mixing
hurting_officer_attack
seal_mediation
wealth_capacity
climate_balance
transformation_stability
72. PRIMARY VS DERIVED EFFECT
Example:
branch clash
→ root destroyed
→ continuity reduced
The branch clash is primary cause.
Root destruction and continuity reduction are downstream consequences.
Integrity must recognize the causal chain.
73. INTEGRITY SHOULD NOT JUST SUM ALL FINDINGS
Forbidden:
+10 support
+10 root
-20 clash
-20 root destroyed
-10 continuity broken
when all negative findings stem from one clash.
Use causal accounting.
74. INTEGRITY POSITIVE FINDINGS
Potential types:
clear_pattern_identity
high_purity
adequate_pattern_strength
strong_support
valid_rescue
useful_god_alignment
climate_alignment
structural_continuity
75. INTEGRITY NEGATIVE FINDINGS
Potential:
low_purity
insufficient_pattern_strength
major_residual_damage
unsupported_pattern
useful_god_conflict
climate_conflict
critical_dependency
structural_fragmentation
76. CRITICAL FINDINGS
Examples:
critical_damage_unrescued
follow_structure_broken
transformation_collapsed
primary_pattern_function_lost
Critical findings may determine state even if aggregate score appears moderate.
77. SCORE OVERRIDE BY CRITICAL RULE
Some structural conditions may require a state override.
Example:
critical transformation collapse
may force:
state = failed
even if other positive components are strong.
Such overrides must be explicit rules.
78. OVERRIDE RULES MUST BE RARE
Do not create too many hard overrides.
Otherwise the score becomes meaningless.
Use them only for truly structural-critical conditions.
79. FOLLOW PATTERN INTEGRITY
For follow patterns,
Integrity must emphasize:
follow validity preserved
dominant force continuity
counterforce control
useful-god alignment
Ordinary balance assumptions may not apply.
80. TRANSFORMATION PATTERN INTEGRITY
For Hóa Khí:
transformation stability
completion
residual original qi
season support
counterforce
must be central.
81. ROOT PROSPERITY INTEGRITY
For:
jian_lu
yang_ren
high self-force is not itself a defect.
Integrity must evaluate:
control
outlet
flow
damage
usable structure
82. SPECIAL PATTERN INTEGRITY
If dedicated rules do not exist:
state = unresolved
grade = UNRESOLVED
Do not force standard model.
83. INTEGRITY RESULT EXAMPLE — COMPLETE
Illustrative:
{
  "state": "resolved",
  "score": 91,
  "classification": "complete",
  "residual_damage": [],
  "confidence": 0.93
}
84. INTEGRITY RESULT EXAMPLE — DAMAGED BUT RESCUED
{
  "state": "resolved",
  "score": 78,
  "classification": "damaged_but_rescued",
  "residual_damage": [
    {
      "damage_id": "DMG-001",
      "original_severity": "major",
      "residual_severity": "minor"
    }
  ],
  "confidence": 0.89
}
85. INTEGRITY RESULT EXAMPLE — DAMAGED
{
  "state": "resolved",
  "score": 54,
  "classification": "damaged",
  "residual_damage": [
    {
      "damage_id": "DMG-002",
      "original_severity": "major",
      "residual_severity": "major"
    }
  ],
  "confidence": 0.88
}
86. INTEGRITY RESULT EXAMPLE — FAILED
{
  "state": "resolved",
  "score": 28,
  "classification": "failed",
  "critical_findings": [
    "primary_pattern_function_lost"
  ],
  "confidence": 0.91
}
87. GRADE EXAMPLE
{
  "state": "resolved",
  "grade": "A",
  "score": 78,
  "confidence": 0.89,
  "integrity_state": "damaged_but_rescued",
  "basis": [
    "high_purity",
    "strong_pattern_strength",
    "major_damage",
    "strong_rescue"
  ]
}
88. CUSTOMER-FACING SUMMARY
Future UI may show:
MỆNH CỤC

Chính Quan cách

Trạng thái:
Bị phá nhưng có cứu

Grade:
A

Độ thuần:
84%

Lực cách:
79%

Độ hoàn chỉnh:
78%
This is more informative than Grade alone.
89. CUSTOMER-FACING STATE LABELS
Suggested mappings:
complete
→ Thành cách rõ

substantially_complete
→ Thành cách khá vững

conditionally_complete
→ Thành cách có điều kiện

mixed
→ Cách cục pha tạp

damaged_but_rescued
→ Có phá nhưng có cứu

damaged
→ Cách cục bị tổn

failed
→ Cách cục khó thành

unresolved
→ Chưa đủ căn cứ kết luận
Display wording can be refined later.
90. CUSTOMER WORDING SAFETY
Avoid:
Grade D nên số nghèo.
Prefer:
Cấu trúc mệnh cục bị suy giảm đáng kể;
cần xét tiếp các khả năng riêng về tài vận, nghề nghiệp và từng giai đoạn vận.
91. GRADE IS NOT ACHIEVEMENT POTENTIAL
A chart may have:
Grade A
but:
wealth potential moderate
authority potential high
Another may have:
Grade B
but:
entrepreneurship high
wealth volatility high
This is why Achievement models come later.
92. GRADE IS NOT SOCIAL CLASS
Forbidden:
SS = upper class
D = lower class
Grade is structural quality only.
93. NATAL GRADE STABILITY
Natal Grade must remain stable across:
Đại Vận
Lưu Niên
current year
Luck cycles activate expression,
not rewrite natal structural Grade.
94. FUTURE LUCK ACTIVATION
Future model may compute:
activation_score_by_luck_cycle
Example:
Natal Grade = A

Luck cycle:
2021–2030
activation = high
But:
Natal Grade remains A
95. GOLDEN DATASET REQUIREMENTS
Golden cases must cover:
pure + strong + no damage
pure + weak + no damage
mixed + strong + no damage
major damage + no rescue
major damage + weak rescue
major damage + strong rescue
critical damage + strong rescue
multiple damages, one untreated
conditional structure
follow pattern stable
follow pattern damaged
transformation stable
transformation collapsed
root prosperity strong but uncontrolled
unresolved pattern
low confidence
missing hour pillar
useful-god conflict
climate conflict
96. GOLDEN CASE — COMPLETE
{
  "case_id": "MC-GRADE-COMPLETE-001",

  "facts": {
    "purity": "pure",
    "pattern_strength": "strong",
    "damage": [],
    "support": "strong"
  },

  "expected": {
    "integrity_state": [
      "complete",
      "substantially_complete"
    ],
    "grade": [
      "S",
      "A"
    ]
  }
}
97. GOLDEN CASE — DAMAGED BUT RESCUED
{
  "case_id": "MC-GRADE-RESCUED-001",

  "facts": {
    "damage": {
      "severity": "major"
    },
    "rescue": {
      "strength": "strong",
      "coverage": "substantial",
      "reliability": "high"
    }
  },

  "expected": {
    "integrity_state": "damaged_but_rescued"
  }
}
98. GOLDEN CASE — FAILED
{
  "case_id": "MC-GRADE-FAILED-001",

  "facts": {
    "critical_damage": true,
    "core_function_lost": true,
    "effective_rescue": false
  },

  "expected": {
    "integrity_state": "failed",
    "grade": [
      "C",
      "D"
    ]
  }
}
Exact Grade band remains calibration-dependent.
99. NEGATIVE GOLDEN CASE — HIGH STRENGTH
{
  "case_id": "MC-GRADE-NEG-001",

  "facts": {
    "pattern_strength": "very_strong",
    "damage": "critical",
    "rescue": "none"
  },

  "forbidden": {
    "grade": [
      "SS",
      "S"
    ]
  }
}
This prevents:
strong = high grade
100. NEGATIVE GOLDEN CASE — HIGH PURITY
{
  "case_id": "MC-GRADE-NEG-002",

  "facts": {
    "purity": "very_pure",
    "pattern_strength": "weak",
    "damage": "major"
  },

  "forbidden": {
    "grade": "SS"
  }
}
101. NEGATIVE GOLDEN CASE — STRONG RESCUE
{
  "case_id": "MC-GRADE-NEG-003",

  "facts": {
    "damage": "critical",
    "rescue": "strong",
    "coverage": "partial"
  },

  "forbidden": {
    "integrity_state": "complete"
  }
}
102. INVARIANTS
GRD-01
Grade cannot be resolved if Structural Integrity is unresolved.
GRD-02
Grade must be downstream from Integrity.
GRD-03
Pattern Strength alone cannot determine Grade.
GRD-04
Purity alone cannot determine Grade.
GRD-05
Damage alone cannot determine Grade.
GRD-06
Rescue alone cannot determine Grade.
GRD-07
Grade must preserve Integrity state.
GRD-08
Natal Grade must not depend on current Đại Vận.
GRD-09
Grade must have trace.
GRD-10
Grade confidence must reflect Integrity confidence.
GRD-11
Critical unresolved evidence must prevent false high-confidence Grade.
GRD-12
Same input + same ruleset = same Grade.
103. INTEGRITY INVARIANTS
INT-01
Residual Damage must reference original Damage.
INT-02
Rescue cannot reduce nonexistent Damage.
INT-03
Untreated major Damage must remain visible.
INT-04
Causal duplication must be controlled.
INT-05
Integrity must respect pattern family.
INT-06
Integrity must preserve structural uncertainty.
INT-07
Integrity cannot rewrite upstream facts.
INT-08
Integrity state must describe the structural path, not only score.
104. FAILURE CONDITIONS
Implementation FAILS if it:
1. computes Grade before Integrity
2. maps strength directly to Grade
3. maps purity directly to Grade
4. deletes Damage after Rescue
5. ignores residual Damage
6. ignores untreated Damage
7. double-counts one causal event
8. ignores Useful-God conflict
9. ignores climate compatibility
10. uses current luck cycle
11. calls failed pattern "poor destiny"
12. produces Grade without trace
13. produces resolved Grade from unresolved Integrity
14. uses fixed arbitrary weights without validation
105. RULE NAMESPACES
Recommended:
MC-INT-GENERAL-*
MC-INT-STANDARD-*
MC-INT-CONG-*
MC-INT-HUAQI-*
MC-INT-JIANLU-*
MC-INT-YANGREN-*
MC-INT-CRITICAL-*

MC-GRADE-*
106. STRUCTURAL INTEGRITY PIPELINE
Canonical flow:
Pattern
      ↓
Purity
      ↓
Pattern Strength
      ↓
Support
      ↓
Damage
      ↓
Rescue
      ↓
Map Rescue → Damage
      ↓
Calculate Residual Damage
      ↓
Useful-God Compatibility
      ↓
Climate Compatibility
      ↓
Causal Deduplication
      ↓
Critical Finding Resolution
      ↓
Structural State Resolution
      ↓
Integrity Score
      ↓
Integrity Confidence
      ↓
Pattern Grade
      ↓
Trace
107. GRADE PIPELINE
StructuralIntegrityResult
      ↓
Validate state
      ↓
Read integrity score
      ↓
Apply ruleset thresholds
      ↓
Apply structural-state guards/caps
      ↓
Resolve Grade
      ↓
Resolve confidence
      ↓
Generate basis
      ↓
Generate trace
108. STRUCTURAL STATE MATRIX
Conceptual:
Purity	Strength	Residual Damage	Rescue	Likely Structural State
High	Strong	None	N/A	complete / substantially_complete
High	Weak	None	N/A	substantially_complete / conditionally_complete
Mixed	Strong	None	N/A	mixed
High	Strong	Major	None	damaged
High	Strong	Minor after rescue	Strong	damaged_but_rescued
Mixed	Strong	Minor	Moderate	mixed / conditionally_complete
Any	Any	Critical	None	failed candidate
Unresolved	Any	Any	Any	unresolved


This table is conceptual only.
109. FOUR QUESTIONS BEFORE GRADE
Before assigning Grade, engine must be able to answer:
1. Cách có rõ không?
2. Cách có lực không?
3. Cách bị phá đến đâu?
4. Phá có được cứu đến đâu?
Then:
5. Sau tất cả, cấu trúc còn đứng được không?
Only after question 5:
6. Grade là gì?
110. EXPLAINABILITY TARGET
For every resolved Grade,
an expert should be able to read:
Pattern:
Chính Quan

Purity:
Pure

Strength:
Strong

Damage:
Thương Quan kiến Quan — major

Rescue:
Ấn chế Thương — strong/substantial

Residual Damage:
minor

Structural State:
damaged_but_rescued

Grade:
A
This is the minimum explainability target.
111. CUSTOMER VALUE
The Mệnh Cục card can later explain:
Mệnh cục:
Chính Quan cách

Độ thuần:
84%

Lực cách:
79%

Phá cách:
Có — mức mạnh

Cứu cách:
Có — khá rõ

Trạng thái:
Có phá nhưng có cứu

Độ hoàn chỉnh:
78%

Grade:
A
This gives customers a meaningful structural explanation
instead of a single pattern label.
112. ARCHITECTURAL DECISION
Canonical rule:
STRUCTURAL INTEGRITY IS THE SYNTHESIS OF PATTERN CLARITY, STRUCTURAL POWER, SUPPORT, RESIDUAL DAMAGE, RESCUE, USEFUL-GOD COMPATIBILITY, AND CLIMATE VIABILITY.

And:
PATTERN GRADE IS A SUMMARY OF STRUCTURAL INTEGRITY — NOT A DIRECT PREDICTION OF WEALTH, AUTHORITY, OR LIFE SUCCESS.

113. FINAL CONCEPTUAL MODEL
Structural Integrity
=
Pattern Clarity
+ Effective Structural Power
+ Coherent Support
- Residual Structural Damage
+ Valid Repair Mechanisms
+ Useful-God Alignment
+ Climate Viability
± Critical Structural Conditions
Then:
Structural Integrity
→ Structural State
→ Integrity Score
→ Pattern Grade
114. FREEZE TARGET
Before moving to Achievement models, freeze:
Structural Integrity definition
Structural states
Residual Damage model
Damage/Rescue synthesis
state-first principle
Grade semantics
Grade enum
Grade/wealth boundary
Grade/authority boundary
Grade/luck boundary
confidence propagation
causal deduplication
critical finding handling
no arbitrary final weights yet
115. NEXT DOCUMENT
Next:
08_ACHIEVEMENT_MODEL.md
Purpose:
- define separate achievement dimensions
- distinguish structural Grade from realized capability
- define authority potential
- management potential
- leadership potential
- entrepreneurship potential
- academic potential
- technical potential
- creative potential
- public visibility
- independence
- stability
- define evidence-based domain scores
- prevent one universal “success score”

Đến đây phần **lõi Mệnh Cục** đã hình thành khá hoàn chỉnh:

**Cách gì → thuần không → có lực không → bị phá thế nào → cứu ra sao → cuối cùng còn đứng được không → Grade bao nhiêu.**

Điểm rất quan trọng là tôi vẫn giữ **Grade chưa đồng nghĩa với “phú quý”**. Bước tiếp theo `08_ACHIEVEMENT_MODEL.md` mới bắt đầu trả lời một câu khác: **cấu trúc đó nếu tốt thì mạnh ở loại thành tựu nào — làm quan, lãnh đạo, kinh doanh, học thuật, kỹ thuật hay sáng tạo**. Đây mới là bước dẫn trực tiếp tới bài toán mà chúng ta muốn giải cho khách hàng.