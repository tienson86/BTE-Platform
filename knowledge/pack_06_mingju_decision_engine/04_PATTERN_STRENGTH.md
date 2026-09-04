# MC-01 — PATTERN STRENGTH

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `04_PATTERN_STRENGTH.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines how MC-01 evaluates the structural strength of an identified Mệnh Cục pattern.

Pattern Strength answers:

```text
How much structural power does the accepted pattern actually possess?
It does NOT answer:
Is the Day Master strong or weak?
Is the pattern pure?
Is the pattern damaged?
Is the chart good or bad?
Will the person be rich or powerful?
Canonical flow:
PatternDecision
      ↓
PatternPurityResult
      ↓
Pattern Strength Analysis
      ↓
PatternStrengthResult
      ↓
Support
      ↓
Damage
      ↓
Rescue
      ↓
Integrity
      ↓
Grade
2. CORE PRINCIPLE
Pattern Strength measures the effective structural force of the pattern itself.
Example:
primary pattern = Chính Quan
Pattern Strength asks:
Quan có lực không?
Quan có đắc lệnh không?
Quan có căn không?
Quan có thấu không?
Quan có được sinh trợ không?
Quan có bị suy yếu tự nhiên không?
It does not ask:
Nhật chủ mạnh hay yếu?
That truth remains owned by Strength Engine.
3. DAY MASTER STRENGTH VS PATTERN STRENGTH
These are two distinct analytical dimensions.
Example A:
Day Master = strong
Pattern = Chính Quan
Quan = weak
Possible result:
day_master_strength = strong
pattern_strength = weak
Example B:
Day Master = weak
Pattern = Tài
Tài = extremely strong
Possible result:
day_master_strength = weak
pattern_strength = very_strong
This distinction is mandatory.
4. WHY THIS SEPARATION MATTERS
Without this distinction, the engine may incorrectly infer:
Thân vượng
→ cách cục mạnh
or:
Thân nhược
→ cách cục yếu
Both are invalid simplifications.
Pattern Strength evaluates the structural deity or structural force defining the pattern.
Day Master Strength evaluates the capacity of the Day Master.
The interaction between them is assessed later.
5. PATTERN STRENGTH OUTPUT
Canonical result:
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
position_power
weakening_factors
positive_factors
negative_factors
evidence_ids
confidence
Conceptual example:
{
  "state": "resolved",
  "score": 81,
  "classification": "strong",
  "root_power": 0.86,
  "season_power": 0.92,
  "exposure_power": 0.80,
  "generation_power": 0.74,
  "continuity_power": 0.83,
  "position_power": 0.78,
  "positive_factors": [],
  "negative_factors": [],
  "evidence_ids": [],
  "confidence": 0.91
}
Values above are illustrative only.
6. PATTERN STRENGTH CLASSIFICATION
Initial canonical states:
very_weak
weak
moderate
strong
very_strong
unresolved
Provisional bands:
0–19    very_weak
20–39   weak
40–59   moderate
60–79   strong
80–100  very_strong
These thresholds are not frozen yet.
They remain configurable until Golden Dataset validation.
7. STRUCTURAL POWER DIMENSIONS
Pattern Strength should evaluate at least:
season_power
root_power
exposure_power
generation_power
continuity_power
position_power
Each dimension must remain separately traceable.
8. SEASON POWER
Season Power evaluates whether the pattern force is supported by the seasonal/month-command environment.
Canonical questions:
Does the pattern element receive seasonal qi?
Is it prosperous, supported, resting, imprisoned, or dead?
Does month command directly reinforce the pattern force?
Does season weaken it?
Season is one of the strongest structural dimensions.
9. MONTH COMMAND
Month Command must be treated as a high-priority structural factor.
For a pattern deity that:
đắc lệnh
Pattern Strength should receive meaningful positive evidence.
For one that:
thất lệnh
it may lose structural power.
However:
month command ≠ total pattern strength
A deity may be out of season but still:
- have strong roots
- be repeatedly exposed
- receive powerful generation
- form strong branch structure
Therefore no single factor may decide Pattern Strength alone.
10. SEASON STATES
If upstream engine exposes seasonal states, MC-01 may consume them.
Conceptual states:
prosperous
minister
resting
imprisoned
dead
or equivalent upstream canonical vocabulary.
MC-01 must not create a conflicting seasonal system.
11. ROOT POWER
Root Power evaluates whether the pattern force has meaningful support in Earthly Branches.
Questions:
Does the pattern force have a root?
How many roots?
How deep are they?
Where are they located?
Are they primary qi or residual qi?
Are roots preserved or compromised?
12. ROOT PRESENCE VS ROOT POWER
Important distinction:
has_root = true
does not automatically mean:
root_power = strong
Root quality depends on:
branch position
hidden-stem layer
month relevance
season
clashes
combinations
root destruction
repetition
13. ROOT DEPTH
If upstream hidden-stem model supports:
main_qi
middle_qi
residual_qi
root strength may conceptually follow:
main_qi
>
middle_qi
>
residual_qi
Exact weights remain unfrozen.
14. MONTH ROOT
A root in Month Branch may carry high structural relevance.
But MC-01 must distinguish:
root in month branch
from:
month command directly equals pattern force
They may overlap but are not identical evidence.
Avoid double counting.
15. MULTIPLE ROOTS
Multiple meaningful roots may increase structural force.
But:
3 weak residual roots
must not automatically exceed:
1 strong month-command root
Root quality matters more than raw count.
16. ROOT DAMAGE
Root Power may be reduced when root is:
clashed
combined away
broken
punished
transformed
structurally neutralized
However, exact destructive interaction belongs partly to Damage stage.
Pattern Strength may register reduced effective root power if upstream relations clearly indicate root availability is compromised.
Do not duplicate later damage penalties.
17. EXPOSURE POWER
Exposure Power evaluates whether the defining deity is visible in Heavenly Stems and capable of direct structural expression.
Questions:
Is the deity exposed?
How many times?
Where?
Is exposure supported by roots?
Is it isolated?
Is it paired with competing structures?
18. EXPOSED + ROOTED
A pattern force that is:
thấu can
+
có căn
generally has stronger effective expression than one that is:
thấu nhưng vô căn
or:
tàng mà không thấu
This relationship is important.
19. EXPOSED BUT ROOTLESS
Example:
Chính Quan thấu can
nhưng không có căn
may show:
high exposure clarity
low root power
Therefore:
exposure_power high
root_power low
This is a valid result.
20. HIDDEN BUT ROOTED
Example:
Quan không thấu
nhưng tàng sâu và có căn mạnh
may produce:
exposure_power low
root_power strong
Do not collapse these dimensions.
21. POSITION POWER
Position can influence structural significance.
Potentially relevant positions:
month stem
month branch
day branch
hour stem
hour branch
year stem
year branch
Month Stem and Month Branch may carry greater structural relevance.
Exact weights remain unfrozen.
22. POSITION IS NOT DESTINY
Position Power only evaluates structural force.
It does not assign life-domain meaning such as:
year = ancestors
month = career
day = spouse
hour = children
unless a separate interpretation model explicitly needs that later.
Do not mix symbolic palace interpretation into Pattern Strength.
23. GENERATION POWER
Generation Power evaluates whether the pattern force is being generated by structurally meaningful upstream elements or Ten Gods.
Examples:
Tài sinh Quan
Ấn sinh Nhật chủ
Thực/Thương sinh Tài
Pattern Strength cares about:
Does something feed the pattern force?
How strong is that source?
Is the generating chain continuous?
24. DIRECT GENERATION
Direct generation is generally stronger evidence than remote indirect generation.
Conceptual hierarchy:
direct generator visible + rooted
>
direct generator hidden/rooted
>
indirect chain
>
weak symbolic relationship
Exact numeric values remain unfrozen.
25. GENERATOR CAPACITY
A generator must itself have structural power.
Forbidden simplification:
Tài exists
→ Tài strongly generates Quan
The engine must consider whether Tài itself is:
rooted
seasonally supported
exposed
continuous
damaged
before assigning strong generation evidence.
26. GENERATION CHAIN
Example:
Thực
→ Tài
→ Quan
can strengthen Quan structurally if the chain is real and sufficiently powered.
The engine should preserve:
chain_source
chain_intermediate
chain_target
chain_strength
for traceability.
27. BROKEN GENERATION CHAIN
A theoretical Five-Element sequence does not automatically create effective generation.
Example:
Thực exists
Tài exists
Quan exists
does not automatically mean:
Thực → Tài → Quan
The chain must be structurally meaningful.
28. CONTINUITY POWER
Continuity Power evaluates whether the pattern force is supported consistently across:
stems
branches
roots
season
generating structure
A pattern has high continuity when its force is not isolated.
Example:
month command supports Quan
Quan exposed
Quan rooted
Tài generates Quan
This suggests strong structural continuity.
29. ISOLATED PATTERN FORCE
Example:
one visible Quan
no root
no seasonal support
no generator
may produce:
exposure_power moderate
continuity_power very_low
pattern_strength weak
30. STRUCTURAL CONTINUITY VS PURITY
Do not confuse:
continuity
with:
purity
A structure may be continuous but mixed.
Example:
Quan + Sát both rooted and continuous
could produce:
pattern_strength high
purity low
31. WEAKENING FACTORS
Pattern Strength may register factors that reduce effective force.
Initial types:
out_of_season
rootless
isolated_exposure
generator_weak
generator_cut
root_compromised
structural_drain
direct_control
competing_force
transformation_loss
But care must be taken not to duplicate Damage stage.
32. STRENGTH REDUCTION VS DAMAGE
Pattern Strength reduction asks:
How much force remains?
Damage asks:
Is the pattern function structurally harmed?
Example:
Quan out of season
may lower strength.
But it is not necessarily structural Damage.
Example:
Thương Quan directly attacks Quan
may be Damage.
Both may coexist.
33. CONTROL AND STRENGTH
If a pattern force is directly controlled by another strong element, its effective strength may be reduced.
However:
control relation
should only reduce Pattern Strength if structurally active.
The Damage module later determines the functional consequences.
34. DRAIN AND STRENGTH
A pattern force may be weakened through excessive draining.
Example:
pattern element repeatedly generates another strong structure
This may reduce available force.
But the engine must avoid simplistic Five-Element arithmetic.
Structural relevance matters.
35. COMPETITION FOR QI
Two forces may compete for the same generating source.
Example:
resource feeds Day Master
and another structural branch
Potential reduction in effective pattern support may be considered if rule-defined.
Do not introduce speculative qi-allocation math without validated rules.
36. PATTERN FAMILY-SPECIFIC STRENGTH
Pattern Strength must respect pattern family.
Families:
standard
root_prosperity
follow
transformation
special
Each may require different dominant dimensions.
37. STANDARD PATTERN STRENGTH
For standard patterns, evaluate:
season
root
exposure
generation
continuity
position
weakening
Examples include:
Chính Quan
Thất Sát
Chính Tài
Thiên Tài
Chính Ấn
Thiên Ấn
Thực Thần
Thương Quan
38. CHÍNH QUAN STRENGTH
Potential positive factors:
Quan đắc lệnh
Quan có căn
Quan thấu
Tài sinh Quan
Quan được chi trợ
Quan liên tục can-chi
Potential weakening:
Quan thất lệnh
Quan vô căn
Quan cô lập
Quan bị khắc mạnh
Quan bị hợp mất tính độc lập
Functional Damage remains separate.
39. THẤT SÁT STRENGTH
Potential positive factors:
Sát đắc lệnh
Sát có căn
Sát thấu
Tài sinh Sát
Sát có nhiều nguồn hỗ trợ
Potential weakening:
Sát thất lệnh
Sát vô căn
Sát bị chế mạnh
Sát bị tiết quá mức
Important:
Sát mạnh
is not automatically bad.
Later layers evaluate whether Day Master can handle it and whether rescue/control exists.
40. TÀI STRENGTH
For:
zheng_cai
pian_cai
evaluate:
seasonal wealth qi
wealth roots
wealth exposure
output generating wealth
branch continuity
wealth concentration
Do not interpret:
wealth strong
as:
person rich
Wealth Potential is a separate later model.
41. ẤN STRENGTH
For:
zheng_yin
pian_yin
evaluate:
resource season
resource root
resource exposure
Quan/Sát generating Ấn
branch continuity
Do not assume strong Ấn is always favorable.
42. THỰC / THƯƠNG STRENGTH
Evaluate:
output season
output root
output exposure
Day Master ability to generate output
continuity into Tài
But Day Master ability is contextual support, not the base Pattern Strength itself.
This distinction should remain explicit.
43. ROOT PROSPERITY STRENGTH
For:
jian_lu
yang_ren
Pattern Strength centers on the self/root force itself.
Relevant dimensions:
month/root dominance
Day Master root continuity
peer/resource reinforcement
branch concentration
control/output channels
Strong self-force is intrinsic to the pattern.
Do not treat it as a foreign support factor.
44. KIẾN LỘC STRENGTH
Potential strength signals:
Day Master receives Lu at month command
multiple supporting roots
resource or peer reinforcement
strong continuity
Weakening:
month root compromised
strong opposing control
root fragmentation
45. DƯƠNG NHẪN STRENGTH
Potential strength signals:
Yang Ren root established
month/root dominance
peer reinforcement
strong Day Master continuity
But:
Dương Nhẫn mạnh
does not automatically mean high Grade.
Later stages must evaluate control, outlet, and damage.
46. FOLLOW PATTERN STRENGTH
Follow-pattern strength measures the force being followed.
Example:
cong_cai
Pattern Strength asks:
How overwhelmingly strong is the Wealth force?
not:
How strong is the Day Master?
47. TÒNG TÀI STRENGTH
Potential strength signals:
wealth dominates season
wealth rooted repeatedly
wealth exposed
output generates wealth
counterforce weak
Day Master support belongs to follow validity/purity/conflict analysis.
48. TÒNG QUAN SÁT STRENGTH
Evaluate combined Quan/Sát structural force where appropriate.
Important:
For a valid follow Quan/Sát structure:
Quan + Sát
may form one dominant control force rather than ordinary impurity.
Pattern-family-specific rules must apply.
49. TÒNG NHI STRENGTH
Evaluate output force:
Thực / Thương
as the dominant followed structure.
Relevant factors:
output roots
output season
output exposure
continuity into wealth
weak resource counterforce
50. TÒNG VƯỢNG STRENGTH
Evaluate:
self/resource concentration
seasonal dominance
root density
continuity
weak opposing structure
Do not use ordinary standard-pattern logic unchanged.
51. TRANSFORMATION PATTERN STRENGTH
For:
hua_qi
Pattern Strength evaluates strength of the transformed structure.
Potential factors:
transformed element season
transformed roots
supporting qi
completion
continuity
counterforce
residual original qi
Transformation validity remains upstream.
52. SPECIAL PATTERN STRENGTH
Special patterns require dedicated rule packs.
If no family-specific rule exists:
state = unresolved
or:
state = partially_resolved
Do not force standard-pattern metrics.
53. DAY MASTER CAPACITY IS NOT PATTERN STRENGTH
Very important:
Example:
Tài rất mạnh
Day Master rất yếu
Pattern Strength may still be:
very_strong
The mismatch is assessed later.
This is essential for conclusions such as:
Tài nhiều thân nhược
Without separate scores, that condition cannot be represented correctly.
54. PATTERN STRENGTH AND SUPPORT
Pattern Strength describes intrinsic/effective force.
Support module later describes structural helpers.
Some evidence may overlap.
To avoid double counting:
generation_power
in Pattern Strength should represent effective energy feeding the pattern.
Support module records the structural relationship and role.
Example:
Tài sinh Quan
may appear:
Pattern Strength:
generation_power increased
Support:
support finding = wealth_generates_officer
Integrity aggregation must prevent duplicate full scoring of the same cause.
55. CAUSAL GROUPING
Pattern Strength findings should expose:
causal_group
Possible groups:
season
root
exposure
generation
continuity
position
weakening
family_specific
This supports deduplication later.
56. STRENGTH FACTOR MODEL
Recommended object:
PatternStrengthFactor
Fields:
factor_id
factor_type
dimension
direction
severity
structural_power
causal_group
evidence_ids
rule_id
confidence
Direction:
increase
decrease
neutral
57. STRENGTH FACTOR TYPES
Initial types:
season_supported
season_dominant
season_weak
root_present
root_deep
multiple_roots
root_compromised
stem_exposed
multiple_exposure
exposed_rooted
exposed_rootless
generator_present
generator_strong
generation_chain
generation_chain_broken
structural_continuity
structural_isolation
position_advantage
direct_control
excessive_drain
family_specific_support
family_specific_weakness
58. SEVERITY
Use:
minor
moderate
major
critical
Severity represents structural significance.
Do not map directly to numeric weight yet.
59. STRUCTURAL POWER VALUE
A factor MAY later expose:
structural_power: 0.0 .. 1.0
This represents assessed strength of the evidence.
It is not necessarily the final scoring contribution.
60. NO ARBITRARY WEIGHTING YET
Do not freeze:
season = 30%
root = 25%
exposure = 15%
generation = 20%
continuity = 10%
at this stage.
Such a formula would create false precision before Golden Dataset calibration.
First freeze:
what evidence matters
how it is classified
how severity is determined
how contradictions are handled
Then calibrate weights.
61. PROVISIONAL AGGREGATION CONCEPT
Conceptually:
Pattern Strength
=
Season Power
+ Root Power
+ Exposure Power
+ Generation Power
+ Continuity Power
+ Position Power
- Effective Weakening
Exact aggregation remains unfrozen.
62. DIMENSION NORMALIZATION
Each dimension MAY later normalize to:
0..100
or:
0.0..1.0
but internal design should preserve dimension independence.
Example:
{
  "season_power": 0.9,
  "root_power": 0.8,
  "exposure_power": 0.6
}
These are not yet final contract values.
63. DIMENSION ABSENCE
If a dimension is not applicable:
state = not_applicable
Do not treat it as zero automatically.
Example:
A special pattern might not use standard exposure_power.
64. MISSING DATA
If hour pillar is unavailable:
Pattern Strength may still resolve if enough structural evidence exists.
But confidence should reflect missing evidence.
Example:
state = partially_resolved
confidence = reduced
when Hour Pillar could materially add roots/exposure.
65. UNRESOLVED PATTERN
If PatternDecision is unresolved:
PatternStrengthResult.state = unresolved
score = null
classification = unresolved
unless family-level analysis is explicitly supported.
66. LOW PATTERN CONFIDENCE
If PatternDecision confidence is low:
Pattern Strength may still analyze observed structural force.
But its confidence should not exceed pattern certainty without explicit justification.
67. STRENGTH CONFIDENCE
Potential confidence factors:
pattern confidence
hidden-stem completeness
relation completeness
season data completeness
root data completeness
hour pillar availability
transformation certainty
68. STRENGTH TRACE
Every resolved factor must generate trace.
Example:
TR-MC-STR-001

stage:
pattern_strength

rule:
MC-STR-GUAN-001

input:
primary = zheng_guan
month_command supports officer
officer rooted in month branch

finding:
season_supported
root_deep

dimension:
season
root

effect:
increase pattern strength
69. GOOD TRACE
Bad:
pattern_strength = 83
Good:
+ Quan đắc lệnh
+ Quan có căn
+ Quan thấu can
+ Tài sinh Quan
- Có một lực tiết Quan nhỏ
= Quan có lực mạnh và liên tục
70. DOUBLE COUNTING CONTROL
Example:
Quan in Month Branch main qi
could trigger:
season_supported
root_present
month_position_advantage
These may all be valid descriptions of one fact.
But Integrity must not blindly count the same causal fact three times.
Each factor must expose causal grouping.
71. ROOT + MONTH COMMAND OVERLAP
Recommended handling:
month command support
and:
root in month branch
may both be recorded.
But aggregation rules must know they partially overlap.
Possible metadata:
overlap_group = month_branch_pattern_power
72. EXPOSURE + CONTINUITY OVERLAP
Similarly:
primary exposed
and:
exposed + rooted continuity
are related.
Avoid full duplicate contributions without explicit calibration.
73. GENERATION + SUPPORT OVERLAP
Example:
Tài sinh Quan
may affect:
generation_power
support finding
Both are valid.
But later Integrity should aggregate by causal meaning rather than simply summing raw scores.
74. PATTERN STRENGTH VS DAMAGE
Example:
Quan strongly rooted
+
Thương Quan attacks Quan
Possible result:
pattern_strength = strong
damage = major
Do not reduce Pattern Strength to weak just because Damage is serious.
Strength describes available force.
Damage describes structural impairment.
75. PATTERN STRENGTH VS RESCUE
Rescue should not rewrite historical Pattern Strength.
Example:
Sát strong
Damage major
Ấn rescues
Pattern Strength remains:
strong
Rescue changes Integrity.
76. PATTERN STRENGTH VS PURITY
Possible states:
pure + strong
pure + weak
mixed + strong
mixed + weak
All are valid.
This two-axis model is required.
77. PATTERN STRENGTH VS GRADE
Forbidden direct mapping:
very_strong → S
strong → A
weak → C
A very strong harmful/uncontrolled structure may have poor Integrity.
Grade is downstream synthesis.
78. PATTERN STRENGTH VS USEFUL GOD
Useful God compatibility does not directly define Pattern Strength.
A strong pattern may be:
compatible with Useful God
or:
conflicting with Useful God
That is evaluated later.
79. PATTERN STRENGTH VS TEMPERATURE
A pattern may be structurally strong but climatically problematic.
Example:
strong Water structure
in extremely cold chart
Pattern Strength can still be high.
Climate Compatibility is separate.
80. HIGH STRENGTH IS NOT ALWAYS FAVORABLE
Critical rule:
STRONG ≠ GOOD
Examples:
Sát quá mạnh
Tài quá mạnh khi Thân nhược
Ấn quá mạnh gây bế tắc tiết khí
Pattern Strength merely measures force.
The later system decides whether that force is usable.
81. LOW STRENGTH IS NOT ALWAYS BAD
A weak negative force may be beneficial by being unable to damage the structure.
Therefore:
weak
cannot be directly interpreted as:
bad
82. STRUCTURAL CAPACITY INTERACTION
Later stages should compare:
Pattern Strength
vs
Day Master Capacity
Examples:
strong Tài
+
weak Day Master
may lead to:
wealth overload weak Day Master
Damage/Integrity handles this.
Another:
strong Quan
+
adequate Day Master
+
Ấn support
may be structurally favorable.
83. CAPACITY RATIO — FUTURE
A future model MAY define:
pattern_force / day_master_capacity
to detect overload.
But this ratio must not be introduced until both scales are proven compatible.
Do not compare unrelated arbitrary scores.
84. STANDARD PATTERN RULE NAMESPACES
Recommended:
MC-STR-GUAN-*
MC-STR-SHA-*
MC-STR-CAI-*
MC-STR-YIN-*
MC-STR-SHI-*
MC-STR-SHANG-*
MC-STR-JIANLU-*
MC-STR-YANGREN-*
MC-STR-CONG-*
MC-STR-HUAQI-*
MC-STR-GENERAL-*
85. GENERAL STRENGTH RULES
General rule families:
season
root
exposure
generation
continuity
position
weakening
Pattern-specific rules refine them.
86. FAMILY-SPECIFIC OVERRIDE
Recommended rule precedence:
explicit exception
>
family-specific rule
>
pattern-specific rule
>
general strength rule
Example:
Ordinary:
Quan + Sát competition may split force
But:
cong_guan_sha
may intentionally treat Quan/Sát as one following structural force.
Family-specific rule should win.
87. STRENGTH RESULT — STRONG EXAMPLE
Illustrative:
{
  "state": "resolved",
  "score": 82,
  "classification": "very_strong",
  "root_power": 0.88,
  "season_power": 0.92,
  "exposure_power": 0.76,
  "generation_power": 0.81,
  "continuity_power": 0.85,
  "position_power": 0.79,
  "positive_factors": [
    "season_dominant",
    "root_deep",
    "generator_strong"
  ],
  "negative_factors": [],
  "confidence": 0.93
}
Numbers are illustrative only.
88. STRENGTH RESULT — WEAK EXAMPLE
{
  "state": "resolved",
  "score": 31,
  "classification": "weak",
  "root_power": 0.18,
  "season_power": 0.24,
  "exposure_power": 0.62,
  "generation_power": 0.20,
  "continuity_power": 0.25,
  "position_power": 0.42,
  "positive_factors": [
    "stem_exposed"
  ],
  "negative_factors": [
    "rootless",
    "out_of_season",
    "structural_isolation"
  ],
  "confidence": 0.88
}
Again illustrative only.
89. UNRESOLVED EXAMPLE
{
  "state": "unresolved",
  "score": null,
  "classification": "unresolved",
  "root_power": null,
  "season_power": null,
  "exposure_power": null,
  "generation_power": null,
  "continuity_power": null,
  "position_power": null,
  "confidence": 0.34
}
90. GOLDEN DATASET REQUIREMENTS
Golden cases must include:
Quan đắc lệnh + có căn + thấu
Quan thấu nhưng vô căn
Quan có căn nhưng không thấu
Quan thất lệnh nhưng nhiều sinh trợ
Sát rất mạnh
Tài mạnh nhưng Thân yếu
Ấn mạnh
Thực mạnh
Thương mạnh
Kiến Lộc mạnh
Dương Nhẫn mạnh
Tòng Tài lực rất mạnh
Tòng Tài yếu/counterforce
Tòng Quan Sát
Tòng Nhi
Tòng Vượng
Hóa Khí mạnh
Hóa Khí yếu
pattern unresolved
missing hour pillar
91. GOLDEN CASE STRUCTURE
Example:
{
  "case_id": "MC-STR-GUAN-001",

  "pattern": {
    "primary": "zheng_guan",
    "family": "standard"
  },

  "facts": {
    "season_support": "strong",
    "root": "strong",
    "exposed": true,
    "generator": "moderate",
    "continuity": "strong"
  },

  "expected": {
    "classification": [
      "strong",
      "very_strong"
    ],
    "must_include_positive": [
      "season_supported",
      "root_present"
    ]
  }
}
92. NEGATIVE GOLDEN CASE
Example:
{
  "case_id": "MC-STR-NEG-001",

  "facts": {
    "exposed": true,
    "root": "none",
    "season_support": "weak"
  },

  "forbidden": {
    "classification": "very_strong"
  }
}
This prevents:
thấu can = mạnh
simplification.
93. GOLDEN CASE — STRONG PATTERN / WEAK DAY MASTER
Required case:
Day Master = weak
Tài pattern = very_strong
Expected:
Pattern Strength remains high
Do not automatically reduce it due to weak Day Master.
94. GOLDEN CASE — STRONG DAY MASTER / WEAK PATTERN
Required case:
Day Master = strong
Quan pattern = weak
Expected:
Pattern Strength remains weak
This verifies separation.
95. INVARIANTS
STR-01
Pattern Strength MUST NOT recalculate Day Master Strength.
STR-02
Pattern Strength MUST NOT overwrite PatternDecision.
STR-03
Every strength factor must reference evidence.
STR-04
Raw Ten-God counts alone cannot determine Pattern Strength.
STR-05
Month Command alone cannot determine Pattern Strength.
STR-06
Exposure alone cannot determine Pattern Strength.
STR-07
Root presence alone cannot determine Pattern Strength.
STR-08
Pattern Strength must be pattern-family aware.
STR-09
Luck-cycle data must not affect natal Pattern Strength.
STR-10
Pattern Strength cannot assign Grade.
STR-11
Pattern Strength cannot assign wealth/authority outcomes.
STR-12
Same input + same ruleset = same result.
STR-13
Unresolved Pattern cannot silently produce resolved Pattern Strength.
STR-14
High Pattern Strength must not be interpreted as automatically favorable.
96. CUSTOMER-FACING WORDING
Future Composer may show:
Lực cách cục: Mạnh
or:
Chính Quan có lực khá rõ nhờ đắc lệnh, có căn và được Tài sinh.
Weak example:
Chính Quan tuy lộ nhưng lực chưa mạnh do thất lệnh, căn yếu và thiếu sinh trợ.
Core engine stores structured facts only.
97. CUSTOMER WORDING SAFETY
Avoid:
Cách mạnh nên chắc chắn thành công.
Prefer:
Cách cục có lực mạnh, nhưng cần xét tiếp Nhật chủ có đủ sức tiếp nhận, cấu trúc có bị phá và có được cứu hay không.
This matches MC-01 architecture.
98. IMPLEMENTATION RECOMMENDATION
Future structure:
engines/mingju/
├── pattern_strength.py
├── pattern_strength_types.py
└── rules/
    └── pattern_strength/
        ├── general.py
        ├── guan.py
        ├── sha.py
        ├── wealth.py
        ├── resource.py
        ├── output.py
        ├── root_prosperity.py
        ├── follow.py
        └── transformation.py
Do not implement until documentation freeze is approved.
99. PATTERN STRENGTH PIPELINE
Canonical pipeline:
PatternDecision
      ↓
Select pattern-family rule set
      ↓
Collect seasonal evidence
      ↓
Collect root evidence
      ↓
Collect exposure evidence
      ↓
Collect generation evidence
      ↓
Collect continuity evidence
      ↓
Collect position evidence
      ↓
Collect effective weakening
      ↓
Deduplicate causal overlaps
      ↓
Resolve dimension strength
      ↓
Aggregate structural power
      ↓
Classify
      ↓
Resolve confidence
      ↓
Generate trace
      ↓
PatternStrengthResult
100. FAILURE CONDITIONS
Pattern Strength implementation FAILS if it:
1. equates Pattern Strength with Day Master Strength
2. uses raw element counts as the main method
3. treats one root as sufficient proof of high strength
4. treats one exposed stem as sufficient proof of high strength
5. ignores season
6. ignores root quality
7. ignores generation continuity
8. applies ordinary rules blindly to Tòng/Hóa patterns
9. converts strong into favorable
10. assigns Grade
11. uses current luck cycle
12. produces score without evidence trace
13. double-counts Month Branch evidence uncontrollably
14. silently changes upstream facts
101. ACCEPTANCE PRINCIPLE
Pattern Strength is accepted only when:
Same pattern facts
→ Same structural power factors
→ Same strength classification
→ Same confidence
→ Explainable trace
and a domain expert can answer:
Vì sao cách này mạnh hoặc yếu?
from evidence rather than from a hidden score.
102. ARCHITECTURAL DECISION
Canonical definition:
PATTERN STRENGTH MEASURES HOW MUCH EFFECTIVE NATAL STRUCTURAL POWER THE IDENTIFIED PATTERN POSSESSES.

It is independent from:
Day Master Strength
Pattern Purity
Structural Damage
Pattern Grade
Life outcome
103. FINAL CONCEPTUAL FORMULA
Conceptually:
Pattern Strength
=
Seasonal Power
+ Root Power
+ Exposure Power
+ Generation Power
+ Structural Continuity
+ Positional Relevance
- Effective Weakening
Exact weights remain unfrozen.
104. TWO-AXIS MODEL
After 03_PATTERN_PURITY.md and 04_PATTERN_STRENGTH.md,
every pattern can now occupy a two-dimensional structural state:
                 PATTERN STRENGTH
                 Weak → Strong

PURITY
High        Pure + Weak     Pure + Strong

Low         Mixed + Weak    Mixed + Strong
This two-axis model is canonical.
Neither axis alone determines quality.
105. PREPARATION FOR DAMAGE
Pattern Strength establishes:
How much force exists?
The next stage must ask:
What is attacking, breaking, neutralizing, or distorting the structure?
That is a different question.
106. FREEZE TARGET
Before continuing, freeze:
Pattern Strength definition
Day Master Strength boundary
strength dimensions
season principle
root principle
exposure principle
generation principle
continuity principle
position principle
family-specific handling
no-double-counting principle
no arbitrary weights
Pattern Strength / Damage boundary
Pattern Strength / Grade boundary
107. NEXT DOCUMENT
Next:
05_PATTERN_DAMAGE.md
Purpose:
- define what constitutes true structural damage
- distinguish weakness from damage
- define direct vs indirect damage
- define severity
- define Thương Quan kiến Quan
- define Quan Sát hỗn tạp where it becomes damage
- define Kiêu thần đoạt Thực
- define Tỷ Kiếp đoạt Tài
- define Tài nhiều Thân nhược
- define Sát mạnh Thân nhược
- define root destruction
- define clash / punishment / harm / break effects
- define pattern deity control
- define transformation damage
- prepare damage records for Rescue analysis

Điểm chúng ta vừa khóa rất quan trọng là từ nay MC-01 có **hai trục độc lập**:

**Độ thuần** cho biết cấu trúc rõ hay tạp.  
**Lực cách cục** cho biết cấu trúc đó mạnh hay yếu.

Như vậy đã có thể xuất hiện bốn trường hợp rất khác nhau: **thuần–mạnh, thuần–yếu, tạp–mạnh, tạp–yếu**. Đây sẽ là nền tảng để file tiếp theo `05_PATTERN_DAMAGE.md` trả lời câu khó hơn: **cách đó dù mạnh và thuần, có đang bị phá thật sự hay không**.