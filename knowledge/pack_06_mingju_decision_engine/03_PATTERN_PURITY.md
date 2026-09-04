# MC-01 — PATTERN PURITY

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `03_PATTERN_PURITY.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the canonical logic for evaluating Pattern Purity in MC-01.

Pattern Purity answers:

```text
How cleanly is the identified pattern expressed?

It does NOT answer:
How strong is the pattern?
Is the pattern damaged?
Is the chart successful?
Is the chart wealthy?
Those belong to later stages.
Canonical flow:
PatternDecision
      ↓
Pattern Purity Analysis
      ↓
PatternPurityResult
      ↓
Pattern Strength
      ↓
Damage / Rescue
      ↓
Integrity
      ↓
Grade
2. CORE PRINCIPLE
Purity measures structural clarity.
A pattern is more pure when:
- its primary structural deity is clearly expressed
- competing same-domain structures are limited
- contradictory structures do not dominate
- stem exposure is coherent
- roots support a consistent structural theme
- hidden qi does not substantially contradict the main pattern
A pattern is less pure when:
- competing structural deities are equally prominent
- the main pattern is mixed with its counterpart
- multiple incompatible structures compete for dominance
- hidden/root structure contradicts exposed structure
- structural identity becomes ambiguous
3. PURITY IS NOT GOOD OR BAD
Critical rule:
PURE ≠ GOOD
MIXED ≠ BAD
A pure pattern may still be:
- weak
- unsupported
- damaged
- poorly aligned with Useful God
- climatically unsuitable
A mixed pattern may still:
- have strong structural power
- receive effective rescue
- function successfully
- produce high integrity after synthesis
Therefore Purity must remain an independent dimension.
4. PURITY IS NOT PATTERN STRENGTH
Example:
Chính Quan appears clearly and without competing Sát
may produce:
high purity
but if Chính Quan:
- lacks root
- is seasonally weak
- is not supported
then:
pattern_strength = weak
Conversely:
Quan and Sát are both very strong
may produce:
low purity
high pattern strength
These are valid simultaneous results.
5. PURITY IS NOT DAMAGE
A mixed structure does not automatically mean damaged.
Example:
Chính Tài + Thiên Tài both present
may reduce purity.
But this does not necessarily create structural damage.
Damage requires a separate rule showing that one force harms the function of another.
Therefore:
mixing
→ Purity concern

harmful interaction
→ Damage concern
These must not be merged.
6. PURITY INPUTS
Pattern Purity may consume:
- PatternDecision.primary
- PatternDecision.secondary
- Pattern family
- visible Ten Gods
- hidden Ten Gods
- stem exposure
- roots
- month command
- structural relations
- Pattern Engine evidence
- branch composition
- hidden qi distribution
It must not consume:
- current Đại Vận
- current year
- biography
- observed income
- social status
- subjective consultant opinion
7. PURITY OUTPUT
Canonical result:
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
Conceptual example:
{
  "state": "resolved",
  "score": 78,
  "classification": "pure",
  "positive_factors": [
    "primary_deity_clear",
    "root_structure_consistent"
  ],
  "negative_factors": [
    "minor_hidden_competitor"
  ],
  "conflicts": [],
  "evidence_ids": [
    "E-MC-PUR-001",
    "E-MC-PUR-002"
  ],
  "confidence": 0.9
}
8. PURITY CLASSIFICATION
Initial canonical classifications:
very_pure
pure
moderately_pure
mixed
heavily_mixed
structurally_impure
unresolved
Suggested provisional bands:
90–100  very_pure
75–89   pure
60–74   moderately_pure
40–59   mixed
20–39   heavily_mixed
0–19    structurally_impure
IMPORTANT:
These thresholds are provisional.
They must remain configurable until validated against Golden Cases.
9. PURITY FACTOR MODEL
Canonical factor:
PurityFactor
Fields:
factor_id
factor_type
effect
severity
description_key
evidence_ids
rule_id
Effect:
increase
decrease
neutral
Severity:
minor
moderate
major
critical
10. POSITIVE PURITY FACTORS
Initial positive factors:
primary_deity_clear
primary_deity_exposed
primary_deity_rooted
month_command_consistent
root_structure_consistent
secondary_structure_supportive
hidden_qi_consistent
single_structural_theme
stem_branch_consistency
low_competing_structure
These increase structural clarity.
11. NEGATIVE PURITY FACTORS
Initial negative factors:
competing_deity_visible
competing_deity_rooted
counterpart_mixing
multiple_dominant_structures
hidden_interference
root_exposure_mismatch
month_command_conflict
structural_fragmentation
secondary_pattern_competition
ambiguous_primary_theme
These reduce structural clarity.
12. PRIMARY DEITY CLARITY
A primary pattern is clearer when its defining structural force is:
- explicitly present
- structurally meaningful
- not overwhelmed by competitors
Example:
primary = zheng_guan
Purity evidence may include:
Chính Quan lộ can
Chính Quan có căn
Không có Thất Sát mạnh cạnh tranh
This supports purity.
13. STEM EXPOSURE
Stem exposure generally increases structural visibility.
Example:
primary deity exposed in Heavenly Stem
may contribute positively to purity.
However:
exposed ≠ automatically strong
Exposure is a clarity signal.
Strength is evaluated later.
14. ROOT CONSISTENCY
A primary structural deity supported by roots that match the exposed structure increases purity.
Example:
Chính Quan lộ
+
Chính Quan có căn
supports:
structural continuity
But root quality belongs partly to Pattern Strength.
Purity only asks:
Does the root reinforce the same structural identity?
not:
How powerful is that root?
15. HIDDEN QI CONSISTENCY
Hidden stems may support or complicate purity.
Case A:
visible structure = Chính Quan
hidden structure = Chính Quan / supportive Ấn
This may reinforce purity.
Case B:
visible structure = Chính Quan
hidden structure = strong Thất Sát
This may reduce purity.
Hidden factors should usually weigh less than clearly exposed competing forces unless strongly rooted or month-command relevant.
16. MONTH COMMAND CONSISTENCY
The Month Command is highly relevant to structural identity.
When month command aligns with the main pattern:
purity support
When the main pattern is exposed but month command strongly supports a competing structure:
purity concern
However:
Month Command influence must not automatically determine pattern identity inside MC-01.
Pattern identity remains upstream truth.
17. SAME-DOMAIN COUNTERPART MIXING
Important structural pairs:
Chính Quan ↔ Thất Sát
Chính Tài ↔ Thiên Tài
Chính Ấn ↔ Thiên Ấn
Thực Thần ↔ Thương Quan
Tỷ Kiên ↔ Kiếp Tài
Mixing of these pairs may reduce purity depending on:
- visibility
- root
- season
- dominance
- location
- structural relevance
Presence alone is not enough.
18. QUAN / SÁT MIXING
This is one of the most important Purity cases.
Potential structure:
Chính Quan
+
Thất Sát
MC-01 must distinguish:
mere presence
from:
structurally meaningful mixture
19. QUAN / SÁT MIXING CONDITIONS
Potential evidence that mixing is structurally meaningful:
both visible
both rooted
both seasonally supported
both connected to Day Master
both structurally active
neither clearly subordinate
Potential evidence that mixing is minor:
one visible, one weakly hidden
one dominant, one rootless
one active, one structurally irrelevant
Therefore:
Quan + Sát present
must NOT automatically generate:
major purity penalty
20. QUAN / SÁT PURITY STATES
Possible findings:
guan_sha_not_meaningfully_mixed
guan_sha_minor_mixing
guan_sha_moderate_mixing
guan_sha_strong_mixing
guan_sha_structural_competition
These are Purity findings.
Later Damage module may separately determine whether the mix causes functional harm.
21. TÀI MIXING
Structure:
Chính Tài
+
Thiên Tài
must be evaluated by structural prominence.
Possible states:
wealth_mix_minor
wealth_mix_moderate
wealth_mix_strong
Do not assume Tài mixing is always harmful.
It may simply indicate:
broader wealth expression
while reducing single-pattern purity.
22. ẤN MIXING
Structure:
Chính Ấn
+
Thiên Ấn
may reduce purity when both become structurally dominant.
But:
Chính Ấn primary
+
weak hidden Thiên Ấn
should not receive the same penalty.
The engine must consider:
exposure
root
season
structural relevance
23. THỰC / THƯƠNG MIXING
Structure:
Thực Thần
+
Thương Quan
requires careful evaluation.
Possible interpretation:
both output structures present
This may reduce purity.
But later Damage logic decides whether Thương Quan is actually harmful to another structure.
Purity must not pre-judge that.
24. TỶ / KIẾP MIXING
Tỷ Kiên and Kiếp Tài coexist frequently.
Their presence alone should not heavily reduce purity unless:
- one of them defines a root/prosperity pattern
- both compete structurally
- they undermine single-pattern clarity
Special handling may be needed for:
jian_lu
yang_ren
25. PRIMARY VS SECONDARY COHERENCE
Secondary patterns may be:
supportive
neutral
competitive
Example:
primary = Chính Quan
secondary = Chính Ấn
may be structurally coherent.
This should not automatically reduce purity.
In contrast:
primary = Chính Quan
secondary = Thất Sát
may indicate structural competition.
26. SECONDARY STRUCTURE CLASSIFICATION
Recommended relationship enum:
supportive
compatible
neutral
competitive
contradictory
unresolved
This relationship may affect Purity.
Exact compatibility tables will be rule-driven.
27. MULTIPLE STRUCTURAL THEMES
Purity decreases when several strong themes coexist without a clear hierarchy.
Example:
Quan strong
Tài strong
Thực strong
Ấn strong
does not automatically mean impure.
The engine must ask:
Do these forces form one coherent chain?
Example:
Thực → Tài → Quan
may be structurally coherent.
Whereas unrelated competing themes may reduce purity more strongly.
28. COHERENT CHAIN PRINCIPLE
This is important.
Multiple Ten Gods do not necessarily imply impurity.
Example:
Thực Thần
→ sinh Tài
→ sinh Quan
can form a coherent structural chain.
Purity evaluation should distinguish:
multiple but coherent
from:
multiple and competing
29. STRUCTURAL FRAGMENTATION
Fragmentation occurs when:
- multiple competing forces exist
- no clear primary flow exists
- exposed and rooted structures disagree
- Pattern identity is repeatedly contradicted
Potential finding:
structural_fragmentation
Severity:
minor
moderate
major
critical
30. ROOT / EXPOSURE MISMATCH
Example:
visible Chính Quan
but roots mainly support Thất Sát
This may reduce purity.
Likewise:
visible Chính Tài
but dominant rooted structure is Thiên Tài
may indicate structural mismatch.
This is a Purity factor.
Strength later determines the actual power of each.
31. HIDDEN INTERFERENCE
Hidden conflicting structures should generally have less Purity impact than clearly exposed ones.
Provisional hierarchy:
visible + rooted
>
visible only
>
hidden + rooted
>
hidden only
This is conceptual.
Exact weights remain unfrozen.
32. POSITIONAL SIGNIFICANCE
Location may affect purity relevance.
Potential positions:
month stem
month branch
day branch
year stem
year branch
hour stem
hour branch
Month-level evidence may carry greater structural relevance.
But exact positional weights must be defined later and validated.
33. MONTH BRANCH IMPORTANCE
Month Branch / month command is a high-priority structural reference.
However:
month branch contains multiple hidden stems
must not be treated as multiple equally dominant patterns.
Main qi, middle qi, residual qi may require distinction if upstream data supports it.
34. HIDDEN STEM LAYERS
If BaZi Engine publishes:
main_qi
middle_qi
residual_qi
Purity may treat these differently.
Suggested structural ordering:
main_qi
>
middle_qi
>
residual_qi
Exact numeric weights are not frozen.
35. PRIMARY QI CONSISTENCY
When month-branch main qi supports the primary pattern:
purity increase
When residual hidden qi conflicts:
minor purity concern
unless it becomes strongly activated elsewhere.
36. PATTERN FAMILY-SPECIFIC PURITY
Purity rules must respect Pattern family.
Canonical families:
standard
root_prosperity
follow
transformation
special
Do not apply all standard-pattern purity assumptions to every family.
37. STANDARD PATTERN PURITY
For standard patterns, evaluate:
primary deity clarity
counterpart mixing
root consistency
stem exposure
month-command consistency
secondary pattern relationship
hidden interference
structural coherence
38. ROOT PROSPERITY PURITY
For:
jian_lu
yang_ren
purity should focus on:
root dominance
self-force consistency
competing structural takeover
proper outlet/control structure
The presence of Tỷ/Kiếp is not automatically impurity.
It may be intrinsic to the pattern.
39. FOLLOW PATTERN PURITY
Follow-pattern purity must use a different conceptual model.
For example:
cong_cai
purity depends on:
Day Master lack of meaningful resistance
wealth-force continuity
absence of rescuing self-support
absence of structure-breaking counterforce
Do not use ordinary standard-pattern purity rules unchanged.
40. FOLLOW PATTERN COUNTERFORCE
For follow structures:
counterforce presence
may be a major purity issue.
Example:
cong_cai
+
strong Day Master root
could significantly reduce follow purity or challenge follow validity.
However Pattern validity itself remains owned upstream.
MC-01 Purity evaluates internal cleanliness of the accepted follow structure.
41. TRANSFORMATION PATTERN PURITY
For:
hua_qi
purity may depend on:
transformation completion
residual original qi
support for transformed element
counterforce
seasonal support
root consistency
Transformation validity remains upstream.
Purity measures how cleanly transformation is expressed.
42. SPECIAL PATTERN PURITY
Special patterns require explicit rule packs.
If no dedicated purity rules exist:
state = unresolved
or:
state = partially_resolved
Do not apply arbitrary standard-pattern rules.
43. PURITY SCORE MODEL
Purity score is conceptually:
base clarity
+ reinforcing factors
- competing factors
- fragmentation
- ambiguity
BUT:
No final formula is frozen yet.
Do NOT hard-code arbitrary weights before Golden Dataset validation.
44. INITIAL BASELINE
For implementation design, an internal neutral baseline MAY be considered conceptually:
50
but this is not yet canonical.
Alternative approaches may start from:
100 and subtract impurity
or:
0 and accumulate clarity
The final strategy will be validated later.
45. WHY WEIGHTS ARE NOT FROZEN YET
Premature weighting creates false precision.
Example:
Quan/Sát mixing = -20
hidden competitor = -8
root consistency = +12
looks scientific but may not reflect expert reasoning.
Therefore MC-01 must first define:
factor taxonomy
severity
conditions
evidence
before freezing numbers.
46. SEVERITY-BASED PURITY EFFECT
Each factor should first resolve:
effect
severity
Example:
factor:
mixed_guan_sha

effect:
decrease

severity:
major
Numeric weighting can be calibrated later.
47. FACTOR SEVERITY CRITERIA
Severity should consider:
visibility
root
season
frequency
structural relevance
month-command relevance
relationship to primary pattern
Conceptual model:
minor
→ weak or hidden interference

moderate
→ meaningful but subordinate interference

major
→ strong structural competition

critical
→ primary structural identity becomes unclear
48. DOMINANCE RATIO
Future implementation MAY define a dominance measure:
primary structural power
/
competing structural power
This may help distinguish:
clear primary
from:
near-equal structural competition
But dominance must use structural evidence, not raw Ten-God counts alone.
49. RAW COUNTS ARE INSUFFICIENT
Forbidden simplification:
Quan count = 2
Sát count = 1
therefore Quan is pure
This ignores:
- month command
- root
- visibility
- season
- position
- relations
Ten-God count alone cannot determine purity.
50. PURITY CONFIDENCE
Purity confidence is separate from Purity score.
Example:
purity_score = 80
confidence = 0.55
may occur when:
- pattern itself is uncertain
- hour pillar is missing
- hidden-stem structure is incomplete
- transformation remains unresolved
51. PURITY CONFIDENCE DEPENDENCIES
Purity confidence should not exceed core evidence confidence without reason.
Potential dependencies:
pattern confidence
ten-god completeness
hidden-stem completeness
relation completeness
hour-pillar availability
52. MISSING HOUR PILLAR
If hour pillar is missing:
Purity may still be computed if sufficient evidence exists.
But result should:
state = partially_resolved
or reduce confidence if hour pillar could materially change structural mixing.
Do not automatically mark unresolved.
53. UNRESOLVED PATTERN
If:
PatternDecision.primary = null
Purity should generally return:
state = unresolved
classification = unresolved
score = null
Do not score purity for an unidentified pattern unless a special pattern-independent model explicitly exists.
54. CONFLICTING PATTERN
If Pattern Recognition returns:
conflicting_evidence
Purity may return:
state = partially_resolved
with conflict records.
Example:
Quan/Sát competition prevents reliable purity classification
55. PURITY CONFLICT MODEL
Recommended:
PurityConflict
Fields:
conflict_id
conflict_type
primary_factor
competing_factor
severity
evidence_ids
resolution_state
56. PURITY CONFLICT TYPES
Initial values:
mixed_guan_sha
mixed_wealth
mixed_resource
mixed_output
root_exposure_mismatch
month_command_mismatch
multiple_primary_themes
hidden_visible_conflict
follow_counterforce
transformation_residual_conflict
other
57. NO DOUBLE COUNTING
Critical implementation rule:
The same structural fact must not reduce purity multiple times unintentionally.
Example:
Thất Sát visible + rooted
should not automatically trigger:
competing_deity_visible
mixed_guan_sha
multiple_dominant_structures
structural_fragmentation
with full penalties for all four unless rules explicitly justify distinct effects.
MC-01 must track causal overlap.
58. FACTOR GROUPING
Recommended factor groups:
identity_clarity
counterpart_mixing
root_consistency
exposure_consistency
month_command_consistency
hidden_interference
secondary_relationship
structural_coherence
family_specific
This helps prevent uncontrolled stacking.
59. FACTOR DEDUPLICATION
Each matched factor should expose:
causal_group
Example:
causal_group = guan_sha_mixing
Multiple evidence items can support one factor without creating multiple penalties.
60. POSITIVE AND NEGATIVE EVIDENCE MAY COEXIST
Example:
primary Chính Quan clearly exposed
+
strong hidden Thất Sát
can produce:
positive:
primary_deity_clear

negative:
mixed_guan_sha
Do not cancel evidence before trace.
Both findings must remain visible.
61. PURITY RESULT EXAMPLE — PURE
Conceptual only:
{
  "state": "resolved",
  "score": 88,
  "classification": "pure",
  "positive_factors": [
    {
      "factor_type": "primary_deity_exposed",
      "severity": "major"
    },
    {
      "factor_type": "root_structure_consistent",
      "severity": "major"
    }
  ],
  "negative_factors": [
    {
      "factor_type": "hidden_interference",
      "severity": "minor"
    }
  ],
  "confidence": 0.91
}
Scores are illustrative only.
62. PURITY RESULT EXAMPLE — MIXED
Conceptual:
{
  "state": "resolved",
  "score": 52,
  "classification": "mixed",
  "positive_factors": [
    {
      "factor_type": "primary_deity_clear",
      "severity": "moderate"
    }
  ],
  "negative_factors": [
    {
      "factor_type": "counterpart_mixing",
      "severity": "major"
    },
    {
      "factor_type": "root_exposure_mismatch",
      "severity": "moderate"
    }
  ],
  "conflicts": [
    "mixed_guan_sha"
  ],
  "confidence": 0.86
}
63. PURITY RESULT EXAMPLE — UNRESOLVED
{
  "state": "unresolved",
  "score": null,
  "classification": "unresolved",
  "positive_factors": [],
  "negative_factors": [],
  "conflicts": [
    "primary_pattern_unresolved"
  ],
  "confidence": 0.31
}
64. TRACE REQUIREMENT
Every Purity factor must generate trace.
Example:
TR-MC-PUR-001

stage:
purity

rule:
MC-PUR-GUAN-001

input:
primary = zheng_guan
qi_sha_visible = true
qi_sha_rooted = true

finding:
mixed_guan_sha

effect:
purity decrease

severity:
major
65. TRACE MUST SHOW WHY
Bad trace:
purity_score = 61
Good trace:
+ primary structure clearly exposed
+ month command supports primary structure
- strong counterpart visible
- counterpart has root
= mixed but still primary-dominant
The expert must be able to inspect the inference chain.
66. STANDARD PATTERN PURITY RULE FAMILIES
Recommended rule namespaces:
MC-PUR-GUAN-*
MC-PUR-SHA-*
MC-PUR-CAI-*
MC-PUR-YIN-*
MC-PUR-SHI-*
MC-PUR-SHANG-*
MC-PUR-JIANLU-*
MC-PUR-YANGREN-*
MC-PUR-CONG-*
MC-PUR-HUAQI-*
MC-PUR-GENERAL-*
67. GENERAL PURITY RULES
General rules may cover:
primary exposed
primary rooted
month command alignment
secondary supportive
multiple competing themes
hidden interference
root/exposure mismatch
Pattern-specific rules refine them.
68. CHÍNH QUAN PURITY
Potential positive conditions:
Quan clear
Quan exposed
Quan rooted
Quan structurally dominant
Ấn supportive
Tài supports Quan without competing structurally
Potential purity reducers:
Sát structurally meaningful
Thương Quan strongly competing
root identity conflicts
multiple dominant incompatible structures
Damage interpretation remains separate.
69. THẤT SÁT PURITY
Potential positive conditions:
Sát clear
Sát rooted
Sát structurally dominant
Ấn structurally coherent
Potential reducers:
Quan equally prominent
competing standard structure
root/exposure mismatch
fragmented support
Do not assume Sát itself is impure because it is aggressive.
70. CHÍNH / THIÊN TÀI PURITY
Purity focuses on:
which wealth structure is primary
whether counterpart is subordinate
whether wealth structures form a coherent theme
whether other structures obscure identity
Do not map purity to wealth amount.
71. CHÍNH / THIÊN ẤN PURITY
Purity focuses on:
resource identity
counterpart mixing
root consistency
structural coherence
Do not classify Kiêu đoạt Thực here.
That belongs to Damage.
72. THỰC THẦN PURITY
Potential purity support:
Thực clear
Thực rooted
output structure coherent
Tài downstream supportive
Potential impurity:
strong competing Thương Quan
root/exposure mismatch
fragmented output structure
Kiêu đoạt Thực belongs to Damage.
73. THƯƠNG QUAN PURITY
Potential purity support:
Thương clear
Thương rooted
output structure dominant
supporting downstream flow coherent
Quan conflict belongs to Damage.
Purity only evaluates structural clarity.
74. KIẾN LỘC PURITY
Potential criteria:
Day Master root structure clearly dominant
month command/root supports Jian Lu
competing pattern does not replace identity
outlet/control structure remains coherent
Do not penalize strong self-force simply for existing.
75. DƯƠNG NHẪN PURITY
Potential criteria:
Yang Ren root clearly established
self-force structure coherent
control/output relationships consistent
competing pattern not structurally dominant
Again:
strong peer force
is part of this pattern, not automatic impurity.
76. TÒNG TÀI PURITY
Potential purity support:
wealth force continuous
Day Master lacks meaningful independent support
counterforce weak
structure consistently follows wealth
Potential purity reduction:
strong Day Master root
strong resource support
competing self-support
Pattern validity itself remains upstream.
77. TÒNG QUAN SÁT PURITY
Potential purity support:
Quan/Sát force dominates coherently
Day Master cannot resist meaningfully
support structure aligns with following force
Counterforce reduces purity.
Do not treat ordinary Quan/Sát mixing rules identically.
78. TÒNG NHI PURITY
Potential purity support:
output force dominates
Day Master consistently releases
resource counterforce absent/weak
Strong restoring Ấn may reduce follow purity.
79. TÒNG VƯỢNG PURITY
Potential purity support:
self/resource force overwhelmingly coherent
counter-control weak
structure consistently follows strong side
Opposing structural forces may reduce purity.
80. HÓA KHÍ PURITY
Potential purity support:
transformation clearly completed
transformed element supported
residual original force weak
counterforce absent
Potential purity reducers:
partial transformation
strong residual original qi
season conflict
root conflict
81. PURITY VS USEFUL GOD
Useful God should not directly determine purity.
Example:
pattern is pure Chính Quan
but Useful God conflicts with Quan element
Purity may still be high.
Compatibility is evaluated later.
82. PURITY VS TEMPERATURE
Temperature / Điều Hậu does not directly determine purity.
A chart may be:
very pure
but climatically imbalanced
These are independent dimensions.
83. PURITY VS DAY MASTER STRENGTH
Day Master strength may influence whether a pattern functions,
but should not directly define pattern purity.
Example:
pure Tài structure
+
Day Master weak
means:
high purity
potentially poor functional capacity
The latter belongs to later stages.
84. PURITY VS GRADE
Forbidden mapping:
very_pure → S
pure → A
mixed → C
Grade requires:
Purity
+
Pattern Strength
+
Support
-
Damage
+
Rescue
+
Compatibility
Purity alone cannot determine Grade.
85. SPECIAL CASE — PURE BUT DAMAGED
Example:
very pure Chính Quan
+
strong Thương Quan attack
Possible:
purity = high
damage = major
integrity = reduced
This must be supported.
86. SPECIAL CASE — MIXED BUT STRONG
Example:
Quan/Sát mixed
+
both structurally powerful
Possible:
purity = moderate/low
pattern_strength = high
Do not collapse one into the other.
87. SPECIAL CASE — MIXED BUT RESCUED
Example:
mixed structure
+
clear mediating force
Purity remains mixed.
Rescue may improve Integrity.
Rescue does NOT rewrite historical Purity.
88. PURITY FREEZE PRINCIPLES
Freeze now:
Purity is structural clarity
Purity is separate from Strength
Purity is separate from Damage
Purity is separate from Grade
Mixing requires structural relevance
Presence alone is insufficient
Family-specific rules are required
No arbitrary weights yet
Explainability is mandatory
89. GOLDEN DATASET REQUIREMENTS
Purity golden cases must cover:
pure Chính Quan
Quan/Sát minor mixing
Quan/Sát major mixing
pure Thất Sát
Tài mixed but coherent
Ấn mixed
Thực/Thương mixed
root/exposure mismatch
hidden competitor only
multiple coherent structures
multiple competing structures
Kiến Lộc
Dương Nhẫn
Tòng Tài clean
Tòng Tài with counterforce
Hóa Khí clean
Hóa Khí residual qi
unresolved pattern
missing hour pillar
90. GOLDEN CASE STRUCTURE
Example:
{
  "case_id": "MC-PUR-001",

  "pattern": {
    "primary": "zheng_guan",
    "family": "standard"
  },

  "facts": {
    "zheng_guan_exposed": true,
    "zheng_guan_rooted": true,
    "qi_sha_exposed": false,
    "qi_sha_rooted": false
  },

  "expected": {
    "classification": [
      "pure",
      "very_pure"
    ],
    "must_include_positive": [
      "primary_deity_exposed",
      "root_structure_consistent"
    ],
    "must_not_include_conflict": [
      "mixed_guan_sha"
    ]
  }
}
91. MIXED GOLDEN CASE
Example:
{
  "case_id": "MC-PUR-GUAN-SHA-001",

  "pattern": {
    "primary": "zheng_guan"
  },

  "facts": {
    "zheng_guan_exposed": true,
    "zheng_guan_rooted": true,
    "qi_sha_exposed": true,
    "qi_sha_rooted": true
  },

  "expected": {
    "must_include_conflict": [
      "mixed_guan_sha"
    ],
    "classification": [
      "mixed",
      "moderately_pure"
    ]
  }
}
Exact classification remains expert-calibrated.
92. NEGATIVE TESTS
Tests must ensure:
hidden weak Sát
does not automatically produce:
major Quan/Sát mixing
and:
two visible Ten Gods
does not automatically mean:
impure
93. INVARIANTS
PUR-01
Purity cannot be resolved if primary pattern is unresolved unless a family-specific exception exists.
PUR-02
Every negative factor must reference evidence.
PUR-03
Every conflict must reference evidence.
PUR-04
Purity score cannot exceed allowed range.
PUR-05
Purity confidence must remain within 0..1.
PUR-06
Purity must not modify PatternDecision.
PUR-07
Purity must not modify upstream Strength.
PUR-08
Purity must not register Damage.
PUR-09
Purity must not assign Grade.
PUR-10
Purity must not depend on luck-cycle data.
PUR-11
Same input and ruleset must produce same Purity result.
PUR-12
The same causal structural issue must not receive uncontrolled duplicate penalties.
94. CUSTOMER-FACING INTERPRETATION
Future Composer may express:
Độ thuần: Cao
or:
Mệnh cục khá thuần, Chính Quan biểu hiện rõ và có căn.
Mixed example:
Cấu trúc Quan – Sát cùng hiện khá rõ nên mệnh cục không hoàn toàn thuần.
But the engine stores structured findings, not final prose.
95. CUSTOMER WORDING SAFETY
Avoid:
Mệnh không thuần nên cuộc đời xấu.
Prefer:
Cấu trúc có nhiều lực cạnh tranh, vì vậy cần xét tiếp mức mạnh, phá và khả năng cứu trước khi kết luận chất lượng mệnh cục.
This reflects the actual MC-01 architecture.
96. IMPLEMENTATION RECOMMENDATION
Future files/modules:
engines/mingju/
├── purity.py
├── purity_types.py
└── rules/
    └── purity/
        ├── general.py
        ├── guan_sha.py
        ├── wealth.py
        ├── resource.py
        ├── output.py
        ├── root_prosperity.py
        ├── follow.py
        └── transformation.py
Do not implement yet unless the documentation phase is explicitly approved.
97. RULE STRUCTURE
Conceptual rule:
{
  "rule_id": "MC-PUR-GUAN-001",
  "domain": "purity",
  "family": "standard",
  "pattern": "zheng_guan",

  "conditions": [
    "qi_sha_exposed == true",
    "qi_sha_structurally_meaningful == true"
  ],

  "effect": {
    "factor": "mixed_guan_sha",
    "direction": "decrease",
    "severity": "major"
  }
}
Exact runtime rule representation remains unfrozen.
98. RULE PRIORITY
Rules may require priority to handle:
general rule
vs
pattern-specific rule
vs
family-specific exception
Recommended conceptual precedence:
explicit exception
>
family-specific rule
>
pattern-specific rule
>
general purity rule
Actual priority numbers will be frozen later.
99. EXCEPTION MODEL
Example:
General rule:
counterpart mixing decreases purity
Exception:
follow Quan/Sát structure
may intentionally contain both Quan and Sát as one following force.
Therefore ordinary Quan/Sát mixing logic must not blindly apply.
100. PURITY DECISION PIPELINE
Canonical internal flow:
PatternDecision
      ↓
Identify applicable purity rule family
      ↓
Collect structural evidence
      ↓
Detect positive clarity factors
      ↓
Detect competing factors
      ↓
Detect conflicts
      ↓
Deduplicate causal groups
      ↓
Resolve factor severity
      ↓
Aggregate Purity
      ↓
Classify
      ↓
Calculate confidence
      ↓
Generate trace
      ↓
PatternPurityResult
101. FAILURE CONDITIONS
Purity implementation FAILS if it:
1. equates purity with strength
2. equates purity with quality
3. treats every mixed Ten-God pair as severe impurity
4. uses raw counts alone
5. ignores root/exposure
6. ignores pattern family
7. applies standard rules blindly to Tòng/Hóa patterns
8. double-counts one conflict repeatedly
9. changes upstream pattern identity
10. assigns Grade directly
11. uses current Đại Vận
12. produces score without trace
102. ACCEPTANCE PRINCIPLE
Pattern Purity is accepted only when:
Same structural facts
→ Same factors
→ Same conflict detection
→ Same purity classification
→ Explainable trace
and an expert can answer:
Why is this pattern considered pure or mixed?
without reading source code.
103. ARCHITECTURAL DECISION
Canonical definition:
PATTERN PURITY MEASURES THE CLARITY AND INTERNAL CONSISTENCY OF THE NATAL STRUCTURAL PATTERN.

It does not measure:
destiny quality
wealth
authority
success
pattern strength
damage
104. FINAL FORMULA CONCEPT
Conceptually:
Pattern Purity
=
Primary Structural Clarity
+ Structural Consistency
+ Root / Exposure Coherence
+ Supportive Secondary Coherence
- Meaningful Counterpart Mixing
- Structural Competition
- Hidden / Visible Contradiction
- Fragmentation
Numeric weighting remains unfrozen.
105. FREEZE TARGET
Before proceeding, freeze:
Purity definition
Purity classifications
Purity factor model
Purity conflict model
same-domain mixing principle
Quan/Sát mixing principle
coherent-chain principle
family-specific handling
no-double-counting rule
Purity/Strength boundary
Purity/Damage boundary
Purity/Grade boundary
106. NEXT DOCUMENT
Next:
04_PATTERN_STRENGTH.md
Purpose:
- define what “mạnh/yếu của cách cục” means
- distinguish Pattern Strength from Day Master Strength
- evaluate month command
- evaluate roots
- evaluate stem exposure
- evaluate seasonal support
- evaluate generation chains
- evaluate continuity
- define pattern-family-specific strength
- prepare structural power for later Damage/Rescue and Integrity stages

Điểm quan trọng nhất của file này là chúng ta đã khóa ba khái niệm rất dễ bị trộn lẫn:

**Thuần** = cấu trúc có rõ ràng, nhất quán không.  
**Mạnh** = cấu trúc đó có lực không.  
**Tốt/xấu** = chưa được phép kết luận ở đây.

Ví dụ hoàn toàn có thể tồn tại một lá số **“Chính Quan rất thuần nhưng Quan yếu”**, hoặc **“Quan Sát hỗn tạp nhưng cả hai đều rất mạnh”**. Chính sự tách này sẽ giúp MC-01 về sau luận được sâu hơn rất nhiều thay vì chỉ dán nhãn “thành cách/bại cách”.

Bước tiếp theo chúng ta làm **`04_PATTERN_STRENGTH.md`**. Đây sẽ là nơi xác định chính xác “lực của cách cục” dựa trên **nguyệt lệnh, đắc căn, thấu can, mùa, sinh trợ, liên tục cấu trúc**, nhưng tuyệt đối không tính lại Thân vượng/nhược của Nhật chủ.