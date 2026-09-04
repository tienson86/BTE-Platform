# MC-01 — PATTERN DAMAGE

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `05_PATTERN_DAMAGE.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines how MC-01 detects and represents structural damage to an identified Mệnh Cục pattern.

Pattern Damage answers:

```text
What is actively harming, breaking, distorting, neutralizing,
or destabilizing the function of the accepted pattern?
It does NOT answer:
Is the pattern weak?
Is the pattern impure?
Is the chart good or bad?
Can the damage be rescued?
What final Grade should be assigned?
Those belong to other stages.
Canonical flow:
PatternDecision
      ↓
PatternPurityResult
      ↓
PatternStrengthResult
      ↓
Support Analysis
      ↓
Pattern Damage Analysis
      ↓
DamageFinding[]
      ↓
Rescue Analysis
      ↓
Structural Integrity
2. CORE PRINCIPLE
Damage requires a real structural mechanism.
A pattern is not "damaged" merely because:
- it is weak
- it is out of season
- it is mixed
- the Day Master is strong or weak
- an unfavorable element exists
- one clash exists somewhere in the chart
Damage must satisfy:
source
→ active relationship
→ target
→ structural effect
3. WEAKNESS VS DAMAGE
Critical distinction:
WEAKNESS ≠ DAMAGE
Example:
Chính Quan lộ
không căn
thất lệnh
may mean:
pattern_strength = weak
but not necessarily:
damage = present
By contrast:
Thương Quan mạnh
trực tiếp chế Chính Quan
may create:
damage = hurting_officer_attacks_officer
4. IMPURITY VS DAMAGE
Critical distinction:
IMPURITY ≠ DAMAGE
Example:
Quan + Sát cùng hiện
may reduce Purity.
But only if the mixed structure creates a harmful functional conflict should Damage be registered.
Therefore:
mixed structure
→ purity issue

harmful active interaction
→ damage issue
5. DAMAGE OUTPUT
Canonical object:
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
causal_group
conditions
Example:
{
  "damage_id": "DMG-MC-001",
  "damage_type": "hurting_officer_attacks_officer",
  "source": "shang_guan",
  "target": "zheng_guan",
  "severity": "major",
  "directness": "direct",
  "reversibility": "partially_reversible",
  "structural_effect": [
    "officer_function_disrupted"
  ],
  "evidence_ids": [
    "E-MC-DMG-001",
    "E-MC-DMG-002"
  ],
  "rule_id": "MC-DMG-GUAN-001",
  "confidence": 0.92,
  "causal_group": "guan_damage"
}
6. DAMAGE TYPE ENUM
Initial canonical damage types:
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
transformation_disrupted
follow_structure_counterforce
generator_destroyed
structural_chain_broken
other
Do not over-expand the enum without validated need.
7. DAMAGE SEVERITY
Allowed severity:
minor
moderate
major
critical
Severity must not be derived from damage name alone.
It must consider:
source strength
target importance
directness
root status
season
repetition
position
whether target is primary pattern deity
whether source is itself rooted/exposed
whether damage is buffered
8. DAMAGE DIRECTNESS
Enum:
direct
indirect
conditional
direct
Source directly attacks the primary structural function.
Example:
Thương Quan → Chính Quan
indirect
Damage weakens a supporting chain.
Example:
generator destroyed
→ primary pattern loses support
conditional
Damage becomes active only if additional conditions are satisfied.
Example:
branch clash
may only become structurally damaging if it actually attacks a meaningful root.
9. DAMAGE REVERSIBILITY
Enum:
fully_reversible
partially_reversible
difficult_to_reverse
irreversible
unknown
This is not Rescue itself.
It estimates whether the damage can theoretically be mitigated.
Actual Rescue is handled later.
10. DAMAGE TARGETS
Possible targets:
primary_pattern_deity
primary_pattern_root
primary_pattern_generator
pattern_chain
day_master_capacity
follow_structure
transformation_structure
support_structure
Every damage must identify what is being harmed.
11. PRIMARY PATTERN DAMAGE
Damage is more significant when it directly affects:
PatternDecision.primary
Example:
primary = zheng_guan
source = shang_guan
target = zheng_guan
This may be much more serious than a clash elsewhere unrelated to the pattern.
12. SOURCE STRENGTH MATTERS
A damaging source must itself have enough structural relevance.
Forbidden simplification:
Thương Quan exists
→ Chính Quan damaged
The engine must ask:
Is Thương Quan visible?
Is it rooted?
Is it seasonally supported?
Is it active?
Does it reach the Quan structure?
Weak or hidden presence may only justify:
minor
or no Damage at all.
13. TARGET STRENGTH MATTERS
A strong target may withstand damage better than a fragile one.
Example:
Quan very strong
+
weak Thương Quan
may produce:
minor damage
Whereas:
Quan weak
+
strong Thương Quan
may produce:
major damage
Severity must consider both sides.
14. DAMAGE IS RELATIONAL
Damage should be modeled as:
source_power
vs
target_power
+
relationship type
+
structural importance
Do not use damage names as fixed penalties.
15. THƯƠNG QUAN KIẾN QUAN
Canonical damage family:
hurting_officer_attacks_officer
Potential conditions:
primary pattern = zheng_guan
shang_guan structurally active
shang_guan can reach/control officer
officer remains relevant
Possible severity depends on:
Thương strength
Quan strength
visibility
roots
season
position
available mediation
Do not register major damage from weak hidden Thương alone.
16. THƯƠNG QUAN KIẾN QUAN — NON-AUTOMATIC RULE
The following is forbidden:
shang_guan present
+
zheng_guan present
=
major damage
Instead:
presence
→ candidate relation

structural activation
→ confirmed damage
17. QUAN SÁT HỖN TẠP
Canonical type:
mixed_officer_killer
Important:
Quan/Sát mixing first belongs to Purity.
It becomes Damage only when the coexistence causes real functional conflict.
Potential damage conditions:
both strong
both structurally active
both compete for the same role
no clear hierarchy
no effective mediation
18. QUAN SÁT MIXED BUT NOT DAMAGED
Example:
Quan dominant
Sát weak/subordinate
may produce:
purity reduction
damage = none
Likewise:
valid cong_guan_sha
must not be treated using ordinary mixed Quan/Sát damage rules.
19. KIÊU THẦN ĐOẠT THỰC
Canonical type:
owl_robs_food
Potential conditions:
primary structure = shi_shen
pian_yin structurally active
pian_yin directly suppresses shi_shen
shi_shen function is important
Severity depends on:
Pian Yin strength
Shi Shen strength
root/exposure
season
support
mediation
20. KIÊU ĐOẠT THỰC — NON-AUTOMATIC
Forbidden:
pian_yin present
+
shi_shen present
=
damage
Only register if the relationship is structurally active.
21. TỶ KIẾP ĐOẠT TÀI
Canonical type:
peer_robs_wealth
Potential conditions:
wealth structure meaningful
Tỷ/Kiếp structurally strong
Tỷ/Kiếp directly competes with or controls Wealth
Day Master context supports the competition
Important:
Tỷ/Kiếp presence alone is not Damage.
This rule is especially sensitive to:
Day Master strength
peer strength
wealth strength
22. TÀI NHIỀU THÂN NHƯỢC
Canonical type:
wealth_overloads_weak_day_master
This is a capacity mismatch.
Potential conditions:
wealth pattern/force strong or very strong
Day Master strength weak/very weak
wealth demand exceeds Day Master capacity
This is an important example where:
Pattern Strength high
can coexist with:
Damage major
23. TÀI NHIỀU THÂN NHƯỢC IS NOT "WEALTH BAD"
The structural meaning is:
wealth force exceeds the carrier capacity
not:
wealth = bad
Later interpretation may describe:
high opportunity
+
high pressure
+
difficulty retaining/control
depending on support/rescue.
24. SÁT MẠNH THÂN NHƯỢC
Canonical type:
killer_overloads_weak_day_master
Potential conditions:
qi_sha very strong
Day Master weak
insufficient control/transformation
This is not triggered merely because Thất Sát exists.
25. RESOURCE OVERLOAD
Canonical type:
resource_overload
Potential conditions:
Ấn force excessive
Day Master already strong
output channel suppressed
structural flow blocked
This is context-dependent.
Do not define:
Ấn strong = damage
without structural imbalance.
26. ROOT DESTROYED
Canonical type:
root_destroyed
Potential mechanisms:
direct clash
combination removing root function
branch break
transformation
strong control
Conditions:
root must belong to primary pattern
root must be structurally meaningful
interaction must materially reduce root function
27. ROOT CLASH
A clash is not automatically root destruction.
Example:
branch clash exists
must be evaluated for:
which branch
which hidden qi
whether primary root is involved
whether root survives
whether clash activates or disperses
Only then may Damage be registered.
28. PATTERN DEITY CONTROLLED
Canonical type:
pattern_deity_controlled
Used when the primary pattern deity is directly controlled by a strong opposing force.
Example:
primary deity element
← strong controlling element
Severity depends on real structural activation.
29. PATTERN DEITY CLASHED
Canonical type:
pattern_deity_clashed
Used where branch/stem relations materially destabilize the primary structural force.
Do not use for every generic clash.
30. PATTERN DEITY COMBINED AWAY
Canonical type:
pattern_deity_combined_away
This requires more than a simple combination.
The combination must materially alter the independent function of the target.
Possible conditions:
combination valid
target is primary structural force
target loses functional independence
transformation or binding effect is meaningful
31. BRANCH PUNISHMENT
Canonical type:
branch_punishment
Only register as pattern Damage if:
punishment touches meaningful structural root/support
and
functional effect is evidenced
Do not assign damage from symbolic presence alone.
32. BRANCH HARM
Canonical type:
branch_harm
Same principle:
relation exists
≠
pattern damaged
Structural relevance must be demonstrated.
33. BRANCH BREAK
Canonical type:
branch_break
Use when a branch break materially weakens:
root
support
generation chain
not merely because the relation exists.
34. SEASONAL CONFLICT
Canonical type:
seasonal_conflict
This should be used carefully.
Seasonal weakness alone belongs to Pattern Strength.
Seasonal conflict becomes Damage only when the climate/season creates a specific structural dysfunction.
Example:
transformation structure cannot stabilize due to season
may count as Damage.
35. USEFUL GOD CONFLICT
Canonical type:
useful_god_conflict
This must not mean:
pattern element ≠ useful god
Damage exists only if the pattern's active structure materially conflicts with the canonical Useful God requirement.
This is a later-stage compatibility-sensitive rule.
36. TRANSFORMATION DISRUPTED
Canonical type:
transformation_disrupted
For:
hua_qi
Potential damage conditions:
transformed element loses support
strong counterforce emerges
residual original qi dominates
required season support absent
transformation chain broken
Pattern validity remains upstream.
Damage evaluates internal disruption of the accepted transformation.
37. FOLLOW STRUCTURE COUNTERFORCE
Canonical type:
follow_structure_counterforce
For:
cong_cai
cong_guan_sha
cong_er
cong_wang
Potential damage:
strong opposing root
strong resource/self support
strong counter-control
break in followed-force continuity
Do not apply standard damage rules blindly.
38. GENERATOR DESTROYED
Canonical type:
generator_destroyed
Example:
Tài sinh Quan
If Tài is heavily damaged or removed:
Quan loses generation source
This may create indirect pattern Damage.
39. STRUCTURAL CHAIN BROKEN
Canonical type:
structural_chain_broken
Example:
Thực → Tài → Quan
If the intermediate Tài is destroyed:
chain breaks
This is an indirect structural damage mechanism.
40. DAMAGE CASCADE
One damage can create downstream consequences.
Example:
root destroyed
→ Pattern Strength reduced
→ pattern continuity broken
However:
MC-01 must avoid recursively double-counting the same causal event.
41. CAUSAL GROUPING
Every damage should expose:
causal_group
Examples:
guan_damage
wealth_capacity_mismatch
root_failure
chain_failure
follow_counterforce
transformation_failure
This helps later Integrity avoid duplicate penalties.
42. PRIMARY DAMAGE VS SECONDARY DAMAGE
Recommended classification:
primary
secondary
supporting
Primary Damage:
directly harms the main pattern.
Secondary Damage:
harms a secondary structure.
Supporting Damage:
harms a generator/root/support chain.
Only structurally relevant damage should influence Integrity.
43. DAMAGE STACKING
Multiple damage events may coexist.
Example:
Chính Quan weak
+
Thương Quan attack
+
Quan root clashed
Possible:
DMG-1 = direct attack
DMG-2 = root destruction
Both may be valid because they arise from distinct causes.
But duplicated records from the same relation must be deduplicated.
44. NO DUPLICATE PENALTIES
Example:
One branch clash that destroys a Quan root should not blindly produce:
pattern_deity_clashed
root_destroyed
branch_break
structural_chain_broken
all as full independent penalties unless each has distinct structural effect.
Use:
causal_group
parent_damage_id
where needed.
45. PARENT / CHILD DAMAGE
Optional model:
parent_damage_id
Example:
DMG-001 root_destroyed
    ↓
DMG-002 continuity_broken
The child should not necessarily receive full independent weight.
46. DAMAGE CONFIDENCE
Damage confidence depends on:
source strength certainty
target identity certainty
relation certainty
pattern certainty
root certainty
transformation certainty
hour pillar completeness
A dramatic damage label with low confidence must not be presented as certain.
47. DAMAGE STATE
Damage collection may itself have state:
resolved
partially_resolved
unresolved
insufficient_evidence
Example:
possible root destruction
but transformation unresolved
may remain:
partially_resolved
48. DAMAGE FINDING CONDITIONS
Each damage record should preserve:
conditions
Example:
{
  "damage_type": "wealth_overloads_weak_day_master",
  "conditions": [
    "wealth_strength >= strong",
    "day_master_strength <= weak"
  ]
}
Do not hide rule conditions.
49. DAMAGE RULE MODEL
Conceptual:
{
  "rule_id": "MC-DMG-GUAN-001",
  "domain": "damage",
  "pattern": "zheng_guan",
  "conditions": [
    "shang_guan_active == true",
    "shang_guan_reaches_officer == true"
  ],
  "effect": {
    "damage_type": "hurting_officer_attacks_officer"
  }
}
Exact runtime format remains unfrozen.
50. RULE PRIORITY
Recommended precedence:
explicit exception
>
family-specific rule
>
pattern-specific rule
>
general damage rule
This is important for:
follow patterns
transformation patterns
root/prosperity patterns
51. DAMAGE EXCEPTIONS
Example:
General:
Quan + Sát strong mixture
→ possible damage
Exception:
valid cong_guan_sha
may treat both as one dominant force.
Therefore:
ordinary mixed_officer_killer rule
must not fire blindly.
52. SUPPORT DOES NOT ERASE DAMAGE
If support exists:
Tài sinh Quan
and damage exists:
Thương Quan công Quan
both should remain registered.
Support is not Rescue unless it directly mitigates the damage mechanism.
53. DAMAGE VS RESCUE
Damage stage asks:
What is broken?
Rescue asks:
What repairs or mitigates it?
Damage must be recorded first.
Do not suppress Damage because a Rescue exists.
54. DAMAGE HISTORY MUST REMAIN
Example:
major damage
+
strong rescue
Final Integrity may still be good.
But the result should retain:
damage = major
rescue = strong
not rewrite history to:
damage = none
55. DAMAGE VS PATTERN STRENGTH
Possible combinations:
strong + undamaged
strong + damaged
weak + undamaged
weak + damaged
All are valid.
56. DAMAGE VS PURITY
Possible combinations:
pure + damaged
mixed + undamaged
pure + undamaged
mixed + damaged
All must be representable.
57. DAMAGE VS GRADE
Forbidden:
major damage → Grade D
Damage must later be combined with:
Pattern Strength
Support
Rescue
Compatibility
Climate
before Grade is determined.
58. DAMAGE VS USEFUL GOD
Useful God conflict may become a damage factor only when:
structural interaction
is demonstrated.
Do not use:
Kỵ thần present
→ damage
as a simplistic rule.
59. DAMAGE VS CLIMATE
Climate imbalance may:
weaken
destabilize
block
a structure.
But pure temperature need belongs primarily to Climate Compatibility.
Only register Damage when there is a structural failure mechanism.
60. DAMAGE SEVERITY MODEL
Severity should consider at least:
source_power
target_power
target_importance
directness
persistence
root involvement
season involvement
repetition
structural reach
Conceptually:
severity
=
attack strength
× target criticality
× structural reach
Exact formula is not frozen.
61. MINOR DAMAGE
Typical characteristics:
weak source
limited reach
secondary target
strong target
conditional activation
62. MODERATE DAMAGE
Typical:
meaningful source
relevant target
partial disruption
target retains function
63. MAJOR DAMAGE
Typical:
strong source
primary target
clear disruption
root/continuity affected
64. CRITICAL DAMAGE
Typical:
primary structure loses core function
multiple core supports destroyed
follow/transformation structure collapses
Critical should be rare.
65. CRITICAL IS NOT AUTOMATIC FAILURE
Even:
critical damage
does not itself finalize:
failed
because Rescue may be powerful.
Final structural state belongs to Integrity.
66. DIRECT ATTACK MODEL
Potential reusable fields:
source_force
target_force
relation_type
source_power
target_resilience
net_pressure
Do not compare scores unless scales are compatible.
67. CAPACITY MISMATCH MODEL
Certain damages are not attacks but overloads.
Examples:
Tài nhiều Thân nhược
Sát mạnh Thân nhược
Model:
external_force
>
carrier_capacity
These require canonical Strength Engine input.
68. CAPACITY MISMATCH IS CONTEXTUAL
Example:
wealth very strong
Day Master balanced
may not be Damage.
But:
wealth very strong
Day Master very weak
may be major Damage.
69. DAY MASTER STRENGTH OWNERSHIP
MC-01 must consume:
canonical Strength Engine output
It MUST NOT recalculate Day Master strength to trigger capacity-mismatch rules.
70. RELATION DAMAGE MODEL
Branch/stem relations may generate Damage only if:
relation exists
+
structural target exists
+
functional effect exists
All three are required.
71. HỢP IS NOT ALWAYS BENEFICIAL
A combination can:
support
bind
remove
transform
neutralize
depending on context.
Therefore:
hợp = tốt
is forbidden.
72. XUNG IS NOT ALWAYS DAMAGE
A clash can:
activate
release
dislodge
break
depending on context.
Therefore:
xung = xấu
is forbidden.
73. HÌNH / HẠI / PHÁ ARE NOT AUTOMATIC DAMAGE
Same rule:
relation label
≠
damage conclusion
Structural effect must be proven.
74. TRANSFORMATION RELATIONS
If a combination transforms:
target identity may change
Damage should reference upstream transformation truth.
MC-01 must not independently determine transformation validity.
75. FAMILY-SPECIFIC DAMAGE
Damage rules must respect:
standard
root_prosperity
follow
transformation
special
76. STANDARD PATTERN DAMAGE
Common families:
direct pattern-deity control
counterpart attack
root destruction
generator destruction
capacity mismatch
chain break
77. ROOT PROSPERITY DAMAGE
For:
jian_lu
yang_ren
potential damage is not:
peer force strong
because that is intrinsic.
Instead evaluate:
loss of control
loss of outlet
root destruction
over-concentration
when rule-supported.
78. FOLLOW PATTERN DAMAGE
Potential:
counterforce returns
Day Master regains strong independent support
followed force loses dominance
support chain breaks
But follow validity remains upstream.
79. TRANSFORMATION DAMAGE
Potential:
transformation incomplete
transformed qi weakened
residual original qi reasserts
counterforce breaks transformation
80. SPECIAL PATTERN DAMAGE
Special patterns require dedicated rule packs.
If unsupported:
state = unresolved
Do not apply random standard rules.
81. DAMAGE TRACE
Every DamageFinding must generate trace.
Example:
TR-MC-DMG-001

stage:
damage

rule:
MC-DMG-GUAN-001

input:
primary = zheng_guan
shang_guan = strong
shang_guan exposed = true
officer rooted = weak

finding:
hurting_officer_attacks_officer

severity:
major

target:
primary_pattern_deity
82. GOOD DAMAGE TRACE
Bad:
damage = major
Good:
+ Chính Quan là cấu trúc chính
+ Thương Quan lộ và có căn
+ Thương Quan có lực mạnh
+ Quan yếu hơn và bị tác động trực tiếp
= phát hiện phá Quan mức major
83. DAMAGE EXAMPLE — PURE BUT DAMAGED
{
  "pattern": "zheng_guan",
  "purity": "very_pure",
  "pattern_strength": "strong",
  "damage": [
    {
      "damage_type": "hurting_officer_attacks_officer",
      "severity": "major"
    }
  ]
}
This is valid.
84. DAMAGE EXAMPLE — MIXED BUT NOT DAMAGED
{
  "pattern": "zheng_cai",
  "purity": "mixed",
  "damage": []
}
This is valid.
85. DAMAGE EXAMPLE — STRONG WEALTH / WEAK DAY MASTER
{
  "pattern": "pian_cai",
  "pattern_strength": "very_strong",
  "day_master_strength": "weak",
  "damage": [
    {
      "damage_type": "wealth_overloads_weak_day_master",
      "severity": "major"
    }
  ]
}
86. DAMAGE EXAMPLE — UNRESOLVED
{
  "state": "partially_resolved",
  "damage": [
    {
      "damage_type": "root_destroyed",
      "severity": "moderate",
      "confidence": 0.54
    }
  ],
  "warnings": [
    "branch_transformation_unresolved"
  ]
}
87. DAMAGE COLLECTION RESULT
Recommended conceptual wrapper:
PatternDamageResult
Fields:
state
findings
critical_damage_ids
major_damage_ids
aggregate_severity
confidence
evidence_ids
Do not collapse all Damage into one number only.
88. AGGREGATE DAMAGE
A future aggregate may use:
none
minor
moderate
major
critical
but must preserve individual findings.
Aggregate does not replace trace.
89. AGGREGATE DAMAGE IS NOT SIMPLE MAX
If multiple moderate damages attack distinct core areas:
aggregate may become major
If several findings are all duplicates of one cause:
aggregate must not inflate
Aggregation requires causal grouping.
90. DAMAGE DEDUPLICATION
Deduplicate by:
causal_group
source
target
relation
evidence overlap
The exact algorithm will be defined later.
91. DAMAGE CONFIDENCE PROPAGATION
If:
pattern confidence low
or:
relation unresolved
Damage confidence must reflect it.
Do not emit:
critical / confidence 1.0
from uncertain inputs.
92. MISSING HOUR PILLAR
If hour pillar is missing:
- Damage can still resolve if unaffected
- confidence may decrease
- possible hidden roots/relations should remain unknown
Do not fabricate absence.
93. NO DAMAGE FOUND
Important distinction:
damage = []
may mean:
no damage detected
only if Damage analysis state is resolved.
If:
state = unresolved
an empty list does not mean no damage.
94. EXPLICIT NO-DAMAGE STATE
Recommended:
state = resolved
findings = []
means:
no structurally meaningful damage detected
95. GOLDEN DATASET REQUIREMENTS
Damage Golden Cases must cover:
Thương Quan kiến Quan — weak source
Thương Quan kiến Quan — strong source
Quan/Sát mixed but not damaging
Quan/Sát mixed and damaging
Kiêu đoạt Thực
Kiêu present but no active damage
Tỷ Kiếp đoạt Tài
Tỷ Kiếp present but no damage
Tài nhiều Thân nhược
Tài strong / Day Master adequate
Sát mạnh Thân nhược
Ấn overload
root clash but root survives
root clash destroys key root
pattern deity combined away
generator destroyed
structural chain broken
follow counterforce
transformation disrupted
branch harm irrelevant to pattern
branch punishment relevant to pattern
unresolved relation
missing hour pillar
96. GOLDEN CASE — THƯƠNG QUAN KIẾN QUAN
Example:
{
  "case_id": "MC-DMG-GUAN-001",

  "pattern": {
    "primary": "zheng_guan"
  },

  "facts": {
    "shang_guan_active": true,
    "shang_guan_strength": "strong",
    "zheng_guan_strength": "weak",
    "direct_relation": true
  },

  "expected": {
    "must_include_damage": [
      "hurting_officer_attacks_officer"
    ],
    "severity": [
      "major",
      "critical"
    ]
  }
}
97. NEGATIVE GOLDEN CASE — WEAK HIDDEN THƯƠNG
{
  "case_id": "MC-DMG-GUAN-NEG-001",

  "facts": {
    "shang_guan_hidden": true,
    "shang_guan_strength": "very_weak",
    "zheng_guan_strength": "strong"
  },

  "forbidden": {
    "severity": [
      "major",
      "critical"
    ]
  }
}
98. GOLDEN CASE — TÀI NHIỀU THÂN NHƯỢC
{
  "case_id": "MC-DMG-WEALTH-001",

  "facts": {
    "wealth_pattern_strength": "very_strong",
    "day_master_strength": "very_weak"
  },

  "expected": {
    "must_include_damage": [
      "wealth_overloads_weak_day_master"
    ]
  }
}
99. GOLDEN CASE — QUAN SÁT MIXED BUT COHERENT
{
  "case_id": "MC-DMG-GUANSHA-NEG-001",

  "facts": {
    "guan_present": true,
    "sha_present": true,
    "primary_clear": true,
    "secondary_subordinate": true
  },

  "expected": {
    "purity_conflict_allowed": true
  },

  "forbidden": {
    "must_not_force_damage": [
      "mixed_officer_killer"
    ]
  }
}
100. DAMAGE INVARIANTS
DMG-01
Every DamageFinding must have evidence.
DMG-02
Every DamageFinding must identify source and target.
DMG-03
Weakness alone cannot create Damage.
DMG-04
Impurity alone cannot create Damage.
DMG-05
Branch/stem relation presence alone cannot create Damage.
DMG-06
Damage severity must not be fixed by damage type name.
DMG-07
Damage must respect pattern family.
DMG-08
Damage must not assign Rescue.
DMG-09
Damage must not assign final Grade.
DMG-10
Damage must not rewrite Pattern Strength.
DMG-11
Damage must not depend on current Đại Vận for natal result.
DMG-12
Same input + same ruleset = same damage findings.
DMG-13
Causal duplication must be controlled.
DMG-14
Uncertain source relation must not create false high-confidence Damage.
101. CUSTOMER-FACING WORDING
Future Composer may say:
Phá cách:
Có
or more specifically:
Mệnh cục có dấu hiệu Thương Quan tác động trực tiếp lên Chính Quan,
mức phá hiện được đánh giá là khá rõ.
Another example:
Tài tinh có lực mạnh trong khi Nhật chủ yếu,
tạo áp lực lớn lên khả năng gánh và giữ Tài.
Core engine stores structured findings only.
102. CUSTOMER WORDING SAFETY
Avoid:
Mệnh bị phá nên cuộc đời thất bại.
Prefer:
Cấu trúc đang có một cơ chế phá đáng kể;
cần xét tiếp có lực cứu, Dụng thần hỗ trợ và khả năng hóa giải hay không.
103. IMPLEMENTATION RECOMMENDATION
Future structure:
engines/mingju/
├── damage.py
├── damage_types.py
└── rules/
    └── damage/
        ├── general.py
        ├── guan_sha.py
        ├── wealth.py
        ├── resource.py
        ├── output.py
        ├── capacity.py
        ├── relations.py
        ├── root_prosperity.py
        ├── follow.py
        └── transformation.py
Do not implement until documentation freeze is approved.
104. DAMAGE RULE NAMESPACES
Recommended:
MC-DMG-GUAN-*
MC-DMG-SHA-*
MC-DMG-CAI-*
MC-DMG-YIN-*
MC-DMG-SHI-*
MC-DMG-SHANG-*
MC-DMG-CAPACITY-*
MC-DMG-ROOT-*
MC-DMG-RELATION-*
MC-DMG-CONG-*
MC-DMG-HUAQI-*
MC-DMG-GENERAL-*
105. DAMAGE PIPELINE
Canonical flow:
PatternDecision
      ↓
PatternStrengthResult
      ↓
Identify applicable damage rule family
      ↓
Collect source forces
      ↓
Collect target structures
      ↓
Validate structural relation
      ↓
Resolve source power
      ↓
Resolve target resilience
      ↓
Detect capacity mismatch
      ↓
Detect root/support-chain damage
      ↓
Apply family-specific exceptions
      ↓
Deduplicate causal overlaps
      ↓
Resolve severity
      ↓
Resolve reversibility
      ↓
Generate DamageFinding[]
      ↓
Resolve confidence
      ↓
Generate trace
106. FAILURE CONDITIONS
Damage implementation FAILS if it:
1. equates weak with damaged
2. equates mixed with damaged
3. treats every xung/hình/hại/phá as damage
4. treats every Thương + Quan as major Thương Quan kiến Quan
5. treats every Quan + Sát as harmful mixing
6. treats every Kiêu + Thực as Kiêu đoạt Thực
7. treats every Tỷ/Kiếp + Tài as đoạt Tài
8. ignores source strength
9. ignores target strength
10. ignores Day Master capacity where required
11. ignores family-specific exceptions
12. assigns Grade
13. erases damage because support/rescue exists
14. double-counts one causal relation repeatedly
15. produces damage without trace
107. ACCEPTANCE PRINCIPLE
Pattern Damage is accepted only when:
Same structural facts
→ Same damage mechanism
→ Same severity band
→ Same source/target relation
→ Same trace
and a domain expert can answer:
Cái gì đang phá cách?
Phá vào đâu?
Phá bằng cơ chế nào?
Mức độ bao nhiêu?
without reading source code.
108. ARCHITECTURAL DECISION
Canonical definition:
PATTERN DAMAGE IS A STRUCTURALLY ACTIVE MECHANISM THAT IMPAIRS THE FUNCTION OF THE ACCEPTED NATAL PATTERN.

It is not synonymous with:
weakness
impurity
unfavorable element
branch relation presence
bad destiny
109. FINAL CONCEPTUAL MODEL
Conceptually:
Damage
=
Active Source
× Structural Relation
× Target Importance
× Source Power
× Target Vulnerability
× Structural Reach
Exact numeric formula remains unfrozen.
110. THREE-AXIS STRUCTURAL MODEL
After Purity, Pattern Strength, and Damage,
MC-01 can now represent:
Purity
Strength
Damage
independently.
Example:
Pure
Strong
Major Damage
is valid.
Likewise:
Mixed
Strong
No Damage
is valid.
This separation is canonical.
111. PREPARATION FOR RESCUE
Damage now establishes:
What is broken?
How severe is it?
What is the target?
Can it theoretically be reversed?
The next stage must ask:
Is there a force that actually repairs, controls,
transforms, bridges, or offsets the damage?
That is the purpose of Rescue.
112. FREEZE TARGET
Before continuing, freeze:
Damage definition
Weakness/Damage boundary
Purity/Damage boundary
source-target model
severity model
directness model
reversibility model
capacity mismatch principle
relation relevance principle
family-specific handling
causal deduplication
Damage/Rescue boundary
Damage/Grade boundary
113. NEXT DOCUMENT
Next:
06_PATTERN_RESCUE.md
Purpose:
- define what counts as true Rescue
- distinguish Support from Rescue
- define direct vs indirect Rescue
- define Ấn chế Thương
- define Ấn hóa Sát
- define Quan chế Tỷ Kiếp
- define bridge / mediation mechanisms
- define root restoration
- define climate rescue where structurally valid
- define rescue strength
- define rescue reliability
- define rescue coverage
- define damage offset
- preserve Damage history while improving Structural Integrity

Điểm quan trọng nhất của file này là từ giờ chúng ta không còn nói chung chung **“có phá cách”**. MC-01 bắt buộc phải trả lời đủ bốn câu:

**cái gì phá → phá vào đâu → bằng cơ chế gì → mức độ bao nhiêu**.

Bước tiếp theo nên làm ngay `06_PATTERN_RESCUE.md`, vì đây mới là nửa còn lại của logic “thành cách/bại cách”: một lá số có phá chưa chắc bại nếu **có cứu đúng, cứu đủ lực và cứu trúng cơ chế phá**.