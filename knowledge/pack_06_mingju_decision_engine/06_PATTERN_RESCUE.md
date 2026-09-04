# MC-01 — PATTERN RESCUE

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `06_PATTERN_RESCUE.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines how MC-01 detects and represents structural Rescue mechanisms.

Pattern Rescue answers:

```text
What force actually mitigates, controls, transforms,
bridges, restores, or offsets a registered structural Damage?
It does NOT answer:
What merely supports the pattern?
Is the chart good?
Is the pattern strong?
Is the Damage erased?
What final Grade should be assigned?
Canonical flow:
PatternDecision
      ↓
Purity
      ↓
Pattern Strength
      ↓
Support
      ↓
Damage
      ↓
Rescue Analysis
      ↓
RescueFinding[]
      ↓
Structural Integrity
      ↓
Grade
2. CORE PRINCIPLE
Rescue exists only when there is:
registered Damage
+
a structurally active mitigating force
+
a valid mechanism connecting the two
Therefore:
SUPPORT ≠ RESCUE
and:
RESCUE MUST TARGET DAMAGE
3. SUPPORT VS RESCUE
This distinction is mandatory.
Example:
Tài sinh Quan
may be:
Support
because it strengthens Quan.
But if the Damage is:
Thương Quan công Quan
then:
Tài sinh Quan
is not automatically Rescue.
A true Rescue must directly or meaningfully reduce the damaging mechanism.
4. RESCUE OUTPUT
Canonical object:
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
mechanism
conditions
evidence_ids
rule_id
confidence
causal_group
Example:
{
  "rescue_id": "RSC-MC-001",
  "rescue_type": "seal_controls_hurting_officer",
  "source": "zheng_yin",
  "target_damage_ids": [
    "DMG-MC-001"
  ],
  "strength": "strong",
  "reliability": "high",
  "coverage": "substantial",
  "damage_offset": 0.72,
  "mechanism": "resource_controls_hurting_officer",
  "evidence_ids": [
    "E-MC-RSC-001",
    "E-MC-RSC-002"
  ],
  "rule_id": "MC-RSC-GUAN-001",
  "confidence": 0.91
}
Numbers are illustrative only.
5. RESCUE TYPE ENUM
Initial canonical types:
seal_controls_hurting_officer
seal_transforms_killer
officer_controls_peer
resource_restores_structure
wealth_bridges_structure
output_releases_excess
combination_resolves_conflict
root_restoration
generator_restoration
structural_chain_repair
climate_balance
follow_counterforce_removed
transformation_stabilized
other
Do not over-expand this list prematurely.
6. RESCUE STRENGTH
Allowed states:
minor
moderate
strong
critical
Meaning:
minor
→ limited mitigating power

moderate
→ meaningful but incomplete rescue

strong
→ substantial mitigation

critical
→ structurally decisive rescue
critical should be rare.
7. RESCUE RELIABILITY
Enum:
very_low
low
moderate
high
very_high
Reliability answers:
How consistently can this Rescue mechanism actually function?
This is different from Rescue Strength.
8. STRENGTH VS RELIABILITY
Example:
Rescue force very strong
but only conditionally connected to Damage
Possible:
strength = strong
reliability = moderate
Another:
Rescue modest in force
but directly positioned and always active
Possible:
strength = moderate
reliability = high
9. RESCUE COVERAGE
Allowed coverage:
full
substantial
partial
weak
conditional
Coverage answers:
How much of the specific Damage mechanism is actually addressed?
10. DAMAGE OFFSET
Canonical numeric field:
0.0 .. 1.0
Conceptual meaning:
0.0 = no meaningful offset
1.0 = theoretical full mitigation
This value must not be guessed.
It should be derived only after Rescue rules are calibrated.
Until then, it may remain null.
11. RESCUE REQUIRES A TARGET
Invariant:
RescueFinding.target_damage_ids
must contain at least one existing Damage ID.
This prevents vague statements such as:
"Ấn là cứu thần"
without specifying what it rescues.
12. DAMAGE HISTORY REMAINS
Critical rule:
Damage + Rescue
does NOT become:
No Damage
Instead preserve both.
Example:
Damage:
hurting_officer_attacks_officer
severity = major

Rescue:
seal_controls_hurting_officer
strength = strong
coverage = substantial
The later Integrity stage determines the net structural condition.
13. RESCUE DOES NOT REWRITE DAMAGE SEVERITY
Damage describes the original structural injury.
Rescue describes mitigation.
Therefore:
Damage severity = major
may remain major even when:
Rescue strength = strong
Net result belongs to Integrity.
14. DIRECT RESCUE
Direct Rescue acts on the damaging source or target directly.
Example:
Thương Quan → phá Quan
Ấn → chế Thương
This is a direct Rescue candidate.
Canonical type:
seal_controls_hurting_officer
15. INDIRECT RESCUE
Indirect Rescue restores the structural environment.
Example:
Quan loses its generator
and another force restores the generator chain.
This may be:
generator_restoration
or:
structural_chain_repair
16. CONDITIONAL RESCUE
A Rescue may require conditions.
Example:
combination resolves conflict
only if:
combination is valid
target is actually bound/redirected
no stronger counterforce breaks it
Then:
coverage = conditional
may apply.
17. ẤN CHẾ THƯƠNG
Canonical type:
seal_controls_hurting_officer
Potential scenario:
primary = zheng_guan
damage = hurting_officer_attacks_officer
resource/seal structurally active
resource controls or suppresses shang_guan
Potential result:
Damage remains registered
Rescue targets that Damage
18. ẤN CHẾ THƯƠNG CONDITIONS
Potential conditions:
damage exists
Ấn structurally meaningful
Ấn has sufficient force
Ấn can actually act on Thương
Thương is not overwhelmingly dominant
Do not register Rescue merely because Ấn exists.
19. ẤN CHẾ THƯƠNG — NON-AUTOMATIC RULE
Forbidden:
Ấn present
+
Thương present
=
Rescue
Correct logic:
Thương creates confirmed Damage
+
Ấn is active
+
Ấn reaches/controls Thương
=
Rescue candidate
20. ẤN HÓA SÁT
Canonical type:
seal_transforms_killer
Potential scenario:
damage = killer_overloads_weak_day_master
qi_sha strong
Ấn structurally active
Ấn receives Sát and transforms it into support
This is one of the most important Rescue mechanisms.
21. ẤN HÓA SÁT CONDITIONS
Potential evidence:
Sát strong
Ấn exists
Ấn rooted or exposed
Sát → Ấn relation structurally active
Ấn can support Day Master
Rescue strength depends on:
Sát power
Ấn power
Day Master weakness
continuity of Sát → Ấn → Nhật chủ
22. SÁT ẤN TƯƠNG SINH
When valid:
Sát
→ sinh Ấn
→ sinh Nhật chủ
the harmful control force may become structurally useful.
This is not simply:
Sát disappears
Instead:
Sát function is transformed
Damage history remains visible.
23. QUAN CHẾ TỶ KIẾP
Canonical type:
officer_controls_peer
Potential Damage:
peer_robs_wealth
Potential Rescue:
Quan controls Tỷ/Kiếp
Conditions:
Tỷ/Kiếp damage confirmed
Quan active
Quan has sufficient force
Quan directly controls peer force
24. QUAN CHẾ TỶ KIẾP IS NOT GENERIC SUPPORT
If there is no:
peer_robs_wealth
Damage, then:
Quan controls peers
may be structurally relevant,
but should not be stored as Rescue.
It may belong to Support or another structural finding.
25. TÀI LÀM CẦU NỐI
Canonical type:
wealth_bridges_structure
Example:
Thực / Thương
→ Tài
→ Quan
A Tài bridge may redirect output force toward a constructive chain.
Potential use:
reduce direct conflict
restore flow
But the bridge must be real.
26. BRIDGE PRINCIPLE
A bridge exists when an intermediate force creates a valid generation path between two otherwise conflicting forces.
Conceptually:
A conflicts with C
A → B → C
If B is structurally active and sufficiently strong,
it may mediate the conflict.
27. BRIDGE IS NOT SYMBOLIC
Forbidden:
Element B exists somewhere
→ bridge exists
Required:
B structurally active
B connects both sides
B has enough force
chain is not broken
28. THỰC / THƯƠNG TIẾT VƯỢNG
Canonical type:
output_releases_excess
Potential scenario:
Day Master / peer structure excessively strong
output provides a release channel
This may mitigate over-concentration.
But this is Rescue only if a registered Damage or structural overload is being reduced.
29. RESOURCE RESTORATION
Canonical type:
resource_restores_structure
Potential scenario:
Day Master capacity damaged/insufficient
resource provides meaningful support
This may help:
wealth_overloads_weak_day_master
killer_overloads_weak_day_master
but only if resource does not create another worse conflict.
30. RESOURCE RESTORATION AND CAPACITY
Example:
Tài rất mạnh
Thân yếu
Damage = wealth_overloads_weak_day_master
Ấn strong
Possible Rescue:
resource_restores_structure
if Ấn materially improves Day Master carrying capacity.
31. ROOT RESTORATION
Canonical type:
root_restoration
Potential scenario:
root compromised
another branch/root structure preserves equivalent anchoring
Important:
A second root does not literally reverse the destroyed root.
It may provide functional replacement.
Therefore:
coverage = partial/substantial
may be more appropriate than full.
32. GENERATOR RESTORATION
Canonical type:
generator_restoration
If a primary generator is damaged,
another valid generating source may restore pattern feeding.
Example:
Tài generator lost
but second strong Tài source remains
This may mitigate:
generator_destroyed
33. STRUCTURAL CHAIN REPAIR
Canonical type:
structural_chain_repair
Example original flow:
Thực → Tài → Quan
Damage:
Tài link weakened
Rescue may occur if:
another structurally valid Tài link restores continuity
34. COMBINATION RESOLVES CONFLICT
Canonical type:
combination_resolves_conflict
Potential scenario:
one damaging force is bound, redirected, or transformed
But:
Hợp
is not automatically Rescue.
35. HỢP AS RESCUE CONDITIONS
Potential requirements:
Damage source is identified
combination directly involves source or critical relation
combination materially reduces damaging function
combination is valid
transformation/binding result is known
36. XUNG AS RESCUE
Rarely, a clash may break an otherwise harmful combination or release a blocked structure.
If validated, this can be modeled as Rescue.
However:
xung = rescue

must never be a generic rule.
37. CLIMATE BALANCE
Canonical type:
climate_balance

This requires careful handling.
Pure Điều Hậu support is not automatically Rescue.
It becomes Rescue only when climate imbalance contributes to a registered structural Damage.
38. CLIMATE RESCUE EXAMPLE
Example:
accepted transformation structure
is destabilized by excessive cold

If Hỏa materially stabilizes the structure:
climate_balance
may target:
transformation_disrupted
This must remain rule-driven.
39. FOLLOW COUNTERFORCE REMOVED
Canonical type:
follow_counterforce_removed
For valid follow patterns.
Potential Damage:
follow_structure_counterforce
Potential Rescue:
counterforce itself is controlled, drained, transformed, or neutralized
40. TRANSFORMATION STABILIZED
Canonical type:
transformation_stabilized

For:
hua_qi

Potential Rescue:
transformed element receives strong support
counterforce is neutralized
residual original qi loses dominance
This targets:
transformation_disrupted
41. RESCUE SOURCE POWER
Rescue source must have enough force.
Forbidden simplification:
Ấn exists
→ cứu
The engine must evaluate:
season
root
exposure
continuity
position
structural connection
42. RESCUE TARGET IMPORTANCE
A Rescue that addresses the core damage should rank higher than one addressing a secondary symptom.
Example:
Damage:
Thương Quan attacks Quan

Directly controlling Thương may be stronger Rescue than merely adding more Quan.
43. ROOT CAUSE VS SYMPTOM
Rescue should prefer mechanisms that mitigate the root cause.
Example:
Damage source = strong Thương
target = Quan

Potential:
Ấn chế Thương

addresses root cause.
Potential:
more Quan
may only reinforce target.
That may be Support rather than true Rescue.
44. RESCUE MECHANISM FIELD
Every RescueFinding should expose:
mechanism
Examples:
control_source
transform_source
strengthen_target
restore_root
restore_generator
bridge_conflict
redirect_flow
release_excess
neutralize_counterforce
stabilize_transformation
45. RESCUE MECHANISM ENUM
Recommended initial enum:
control_source
transform_source
strengthen_target
restore_root
restore_generator
repair_chain
bridge_conflict
redirect_flow
release_excess
neutralize_counterforce
stabilize_climate
stabilize_transformation
other

46. STRENGTHEN TARGET AS RESCUE
This is allowed only when target reinforcement materially improves resilience against registered Damage.
Example:
weak Quan under attack
+
strong generator restores Quan

may partially rescue.
But not every positive support is automatically Rescue.
47. RESCUE COVERAGE MODEL
Coverage should consider:
number of target damages addressed
core vs secondary damage
directness
source power
persistence
dependence on conditions

48. FULL COVERAGE
Use only when:
Damage mechanism is comprehensively neutralized
and
Rescue is reliable
and
no major residual damage remains
Rare.
49. SUBSTANTIAL COVERAGE
Most strong rescues may fall here.
Meaning:
core damage greatly reduced
but residual impairment remains
50. PARTIAL COVERAGE
Meaning:
meaningful reduction
but Damage remains structurally important
51. WEAK COVERAGE
Meaning:
Rescue exists but has limited practical effect

52. CONDITIONAL COVERAGE
Use when:
Rescue works only if another condition remains valid

Example:
combination must remain intact

53. RESCUE RELIABILITY FACTORS
Possible factors:
source rooted
source seasonally supported
source exposed
direct structural reach
target connection
chain continuity
absence of stronger counterforce
no unresolved transformation
54. RESCUE RELIABILITY REDUCERS
Examples:
source rootless
source out of season
source hidden only
rescue depends on unresolved combination
strong counterforce
multiple competing roles
55. MULTIPLE RESCUES
One Damage may have multiple Rescue mechanisms.
Example:
Damage:
killer_overloads_weak_day_master

Rescue 1:
seal_transforms_killer

Rescue 2:
resource_restores_structure

Both may be recorded if structurally distinct.
56. MULTIPLE DAMAGE TARGETING
One Rescue may target multiple damages.
Example:
strong Ấn
may:
control Thương
support Day Master
Potentially targeting:
hurting_officer_attacks_officer
wealth_overloads_weak_day_master
But each target relationship must be explicitly justified.
57. NO RESCUE OVERCOUNTING
A single Ấn fact should not automatically create multiple full-strength rescues.
Use:
causal_group
to control duplicated impact.
58. CAUSAL GROUPING
Suggested Rescue causal groups:
seal_mediation
officer_control
resource_restoration
wealth_bridge
output_release
root_restoration
chain_repair
climate_stabilization
follow_stabilization
transformation_stabilization
59. RESCUE PARENT / CHILD RELATIONSHIP
Optional:
parent_rescue_id
Example:
RSC-001 seal_transforms_killer
    ↓
RSC-002 Day Master capacity restored
The child effect should not be counted as an entirely separate independent rescue unless justified.
60. RESCUE VS SUPPORT
Canonical rule:
Support:
helps the pattern

Rescue:
mitigates a registered Damage
Example:
Tài sinh Quan

without Damage:
Support

With Damage and if it materially restores target resilience:
possible Rescue + Support
but the roles must remain separate.
61. RESCUE VS USEFUL GOD
A Useful God may function as Rescue if it actually mitigates Damage.
But:
Dụng thần = Hỏa
does not automatically create:
Rescue = Hỏa
The engine requires a structural mechanism.
62. RESCUE VS HỶ THẦN
Same principle.
Hỷ Thần may support favorable flow,
but Rescue requires a Damage target.
63. RESCUE VS KỴ THẦN
A Kỵ Thần may still participate in a local structural relation.
MC-01 should not reject a Rescue mechanism solely because source element is globally unfavorable.
This is why local structure and global compatibility are separate layers.
64. RESCUE VS PATTERN STRENGTH
Rescue does not automatically increase Pattern Strength.
Example:
Ấn controls Thương
may reduce Damage without increasing Quan's intrinsic structural power.
Pattern Strength remains historical structural force.
65. RESCUE VS PURITY
Rescue does not make a mixed pattern pure.
Example:
Quan/Sát mixed
+
valid mediation
Purity remains mixed.
Integrity may improve.
66. RESCUE VS DAMAGE
Rescue does not delete Damage.
This invariant is mandatory.
67. RESCUE VS GRADE
Forbidden:
strong rescue → Grade A

Grade requires full Integrity synthesis.
68. RESCUE AND STRUCTURAL INTEGRITY
Rescue becomes important only in Integrity.
Conceptually:
Damage severity
-
effective Rescue
=
residual structural impairment

But the exact formula remains unfrozen.
69. RESIDUAL DAMAGE
Later Integrity should be able to derive:
residual_damage
for each Damage.
Conceptually:
residual_damage
=
original_damage
×
(1 - effective_rescue)
This is conceptual only.
No numeric formula is frozen yet.
70. RESCUE EFFECTIVENESS
Effective Rescue depends on:
strength
× reliability
× coverage
× structural relevance
Exact formula remains unfrozen.
71. RESCUE CONFIDENCE
Confidence depends on:
Damage confidence
source certainty
relation certainty
source strength certainty
coverage certainty
transformation certainty
hour-pillar completeness
Rescue confidence should generally not exceed target Damage confidence dramatically without justification.
72. UNRESOLVED DAMAGE
If target Damage is unresolved:
Rescue should usually be:
partially_resolved
or:
unresolved
Do not emit certain Rescue for uncertain Damage.
73. NO DAMAGE FOUND
If:
DamageResult.state = resolved
DamageResult.findings = []
then:
RescueResult.findings = []
is expected.
Do not invent Rescue merely to make the chart look good.
74. DAMAGE EXISTS, NO RESCUE
Valid state:
Damage = major
Rescue = none
This is important and must be representable.
75. DAMAGE EXISTS, WEAK RESCUE
Valid:
Damage = major
Rescue = minor

Integrity will still be significantly reduced.
76. DAMAGE EXISTS, STRONG RESCUE
Valid:
Damage = major
Rescue = strong/substantial
This may lead to:
damaged_but_rescued
later.
77. CRITICAL DAMAGE + STRONG RESCUE
Must not automatically become complete.
Possible later state:
conditionally_complete
or:
damaged_but_rescued
depending on residual risk.
78. ẤN CHẾ THƯƠNG EXAMPLE
Conceptual:
{
  "damage": {
    "damage_id": "DMG-MC-001",
    "damage_type": "hurting_officer_attacks_officer",
    "severity": "major"
  },
  "rescue": {
    "rescue_id": "RSC-MC-001",
    "rescue_type": "seal_controls_hurting_officer",
    "target_damage_ids": [
      "DMG-MC-001"
    ],
    "strength": "strong",
    "coverage": "substantial",
    "reliability": "high"
  }
}
79. SÁT ẤN TƯƠNG SINH EXAMPLE
{
  "damage": {
    "damage_type": "killer_overloads_weak_day_master",
    "severity": "major"
  },
  "rescue": {
    "rescue_type": "seal_transforms_killer",
    "strength": "strong",
    "coverage": "substantial",
    "mechanism": "transform_source"
  }
}
80. TỶ KIẾP ĐOẠT TÀI / QUAN CHẾ TỶ EXAMPLE
{
  "damage": {
    "damage_type": "peer_robs_wealth",
    "severity": "moderate"
  },
  "rescue": {
    "rescue_type": "officer_controls_peer",
    "strength": "moderate",
    "coverage": "partial"
  }
}
81. RESOURCE RESTORATION EXAMPLE
{
  "damage": {
    "damage_type": "wealth_overloads_weak_day_master",
    "severity": "major"
  },
  "rescue": {
    "rescue_type": "resource_restores_structure",
    "strength": "moderate",
    "coverage": "partial"
  }
}
82. ROOT RESTORATION EXAMPLE
{
  "damage": {
    "damage_type": "root_destroyed",
    "severity": "major"
  },
  "rescue": {
    "rescue_type": "root_restoration",
    "strength": "moderate",
    "coverage": "partial"
  }
}
83. FOLLOW PATTERN EXAMPLE
{
  "pattern": "cong_cai",
  "damage": {
    "damage_type": "follow_structure_counterforce"
  },
  "rescue": {
    "rescue_type": "follow_counterforce_removed",
    "coverage": "substantial"
  }
}
84. TRANSFORMATION EXAMPLE
{
  "pattern": "hua_qi",
  "damage": {
    "damage_type": "transformation_disrupted"
  },
  "rescue": {
    "rescue_type": "transformation_stabilized",
    "coverage": "substantial"
  }
}

85. RESCUE RESULT WRAPPER
Recommended:
PatternRescueResult
Fields:
state
findings
targeted_damage_ids
untargeted_damage_ids
strongest_rescue_ids
confidence
warnings
evidence_ids
86. UNTREATED DAMAGE
Very important field:
untargeted_damage_ids
This allows Integrity to know which damages have no Rescue.
Example:
DMG-001 rescued
DMG-002 not rescued
87. PARTIALLY TREATED DAMAGE
Later model may expose:
partially_rescued_damage_ids
This is useful for explainability.
88. RESCUE AGGREGATION
Do not reduce all Rescue to one score prematurely.
Preserve:
per-damage rescue findings
because one Damage may be fully mitigated while another remains unresolved.
89. RESCUE MAPPING
Recommended mapping:
Damage ID
→ RescueFinding[]
Example:
DMG-001
→ RSC-001
→ RSC-002

DMG-002
→ none
90. DAMAGE-RESCUE MATRIX
Future internal representation may use:
             RESCUE
Damage       R1   R2   R3

D1           X    X
D2                     X
D3           -
This makes target coverage explicit.
91. RESCUE DEDUPLICATION
Deduplicate by:
same source
same mechanism
same target damage
same evidence
same causal group

Do not create duplicate rescues from repeated wording.
92. FAMILY-SPECIFIC RESCUE
Rescue rules must respect:
standard
root_prosperity
follow
transformation
special

93. STANDARD PATTERN RESCUE
Typical mechanisms:
control damaging source
transform damaging source
strengthen damaged target
restore generator
bridge conflicting structures
restore Day Master capacity
94. ROOT PROSPERITY RESCUE
For:
jian_lu
yang_ren
potential Rescue may involve:
control excess
release excess
restore outlet
restore balance
Strong Tỷ/Kiếp itself is not damage by default.
95. FOLLOW PATTERN RESCUE
Potential:
remove counterforce
restore followed-force continuity
stabilize dominant flow
Ordinary self-strengthening Rescue may actually damage a follow structure.
Family-specific rules are mandatory.
96. TRANSFORMATION RESCUE
Potential:
reinforce transformed qi
remove residual counterforce
restore transformation chain
stabilize climate condition
97. SPECIAL PATTERN RESCUE
Special structures require dedicated rule packs.
If unsupported:
state = unresolved
Do not improvise.
98. RULE NAMESPACES
Recommended:
MC-RSC-GUAN-*
MC-RSC-SHA-*
MC-RSC-CAI-*
MC-RSC-YIN-*
MC-RSC-SHI-*
MC-RSC-CAPACITY-*
MC-RSC-ROOT-*
MC-RSC-CHAIN-*
MC-RSC-CONG-*
MC-RSC-HUAQI-*
MC-RSC-CLIMATE-*
MC-RSC-GENERAL-*
99. RULE PRIORITY
Recommended conceptual precedence:
explicit exception
>
family-specific rescue
>
damage-specific rescue
>
pattern-specific rescue
>
general rescue
100. RESCUE RULE EXAMPLE
{
  "rule_id": "MC-RSC-GUAN-001",
  "domain": "rescue",
  "target_damage_type": "hurting_officer_attacks_officer",

  "conditions": [
    "resource_active == true",
    "resource_controls_shang_guan == true",
    "resource_strength >= moderate"
  ],

  "effect": {
    "rescue_type": "seal_controls_hurting_officer",
    "mechanism": "control_source"
  }
}
Exact runtime format remains unfrozen.
101. RESCUE TRACE
Every RescueFinding must generate trace.
Example:
TR-MC-RSC-001

stage:
rescue

target_damage:
DMG-MC-001

damage:
hurting_officer_attacks_officer

source:
zheng_yin

mechanism:
control_source

finding:
seal_controls_hurting_officer

strength:
strong

coverage:
substantial
102. GOOD TRACE
Bad:
Có Ấn cứu.
Good:
+ DMG-MC-001: Thương Quan đang phá Chính Quan
+ Chính Ấn lộ, có căn và có lực
+ Chính Ấn trực tiếp chế Thương Quan
+ lực Ấn đủ để giảm đáng kể tác động của Thương
= xác định rescue: seal_controls_hurting_officer
103. TRACE MUST LINK DAMAGE
Every Rescue trace must include:
target_damage_ids
This is mandatory.
104. RESCUE CONFIDENCE EXAMPLE
Damage confidence = 0.91
Rescue source certainty = 0.88
relation certainty = 0.90
Possible Rescue confidence:
~ high
But no exact formula is frozen.
105. MISSING HOUR PILLAR
If Hour Pillar is missing:
- Rescue can resolve if existing evidence is sufficient
- confidence may decrease
- possible hidden rescue source must remain unknown
Do not assume absent.
106. UNKNOWN RESCUE
If a potentially relevant Rescue cannot be verified:
state = partially_resolved
or:
warning = rescue_relation_unresolved
Prefer uncertainty over fabrication.
107. RESCUE INVARIANTS
RSC-01
Every Rescue must target at least one existing Damage.
RSC-02
Rescue cannot exist for nonexistent Damage.
RSC-03
Every Rescue must have evidence.
RSC-04
Support alone does not imply Rescue.
RSC-05
Useful God alone does not imply Rescue.
RSC-06
Rescue must identify a mechanism.
RSC-07
Rescue must not delete Damage.
RSC-08
Rescue must not rewrite Pattern Strength.
RSC-09
Rescue must not rewrite Purity.
RSC-10
Rescue must not assign Grade.
RSC-11
Rescue must respect pattern family.
RSC-12
Same input + same ruleset = same Rescue findings.
RSC-13
Uncertain Damage cannot produce false certain Rescue.
RSC-14
Duplicate Rescue effects must be controlled.
108. FAILURE CONDITIONS
Rescue implementation FAILS if it:
1. calls every favorable force a Rescue
2. registers Rescue without Damage
3. registers Ấn as Rescue merely because Ấn exists
4. ignores source strength
5. ignores target Damage
6. ignores mechanism
7. erases Damage after Rescue
8. treats Support and Rescue as identical
9. treats Useful God as automatic Rescue
10. applies standard rules blindly to follow patterns
11. ignores transformation-specific logic
12. double-counts one rescue source repeatedly
13. assigns Grade
14. produces Rescue without trace
109. GOLDEN DATASET REQUIREMENTS
Golden cases must cover:
Thương Quan kiến Quan + strong Ấn rescue
Thương Quan kiến Quan + weak Ấn
Thương Quan kiến Quan + no Rescue

Sát mạnh Thân nhược + Ấn hóa Sát
Sát strong + Ấn too weak

Tỷ Kiếp đoạt Tài + Quan chế Tỷ
Tỷ Kiếp damage + weak Quan

Tài nhiều Thân nhược + Resource restoration
Tài overload + no resource

root destroyed + secondary root restoration
generator destroyed + alternate generator
chain broken + bridge restoration

follow counterforce + counterforce removed
transformation disrupted + stabilization

climate-related structural damage + climate rescue
support present but not Rescue
Useful God present but not Rescue
110. GOLDEN CASE — ẤN CHẾ THƯƠNG
{
  "case_id": "MC-RSC-GUAN-001",

  "damage": {
    "damage_id": "DMG-001",
    "damage_type": "hurting_officer_attacks_officer",
    "severity": "major"
  },

  "facts": {
    "resource_active": true,
    "resource_strength": "strong",
    "resource_controls_shang_guan": true
  },

  "expected": {
    "must_include_rescue": [
      "seal_controls_hurting_officer"
    ],
    "target_damage_ids": [
      "DMG-001"
    ],
    "coverage": [
      "substantial",
      "full"
    ]
  }
}
Exact coverage remains calibration-dependent.
111. NEGATIVE GOLDEN CASE — ẤN TOO WEAK
{
  "case_id": "MC-RSC-GUAN-NEG-001",

  "damage": {
    "damage_type": "hurting_officer_attacks_officer",
    "severity": "major"
  },

  "facts": {
    "resource_present": true,
    "resource_strength": "very_weak"
  },

  "forbidden": {
    "coverage": [
      "full",
      "substantial"
    ]
  }
}
112. GOLDEN CASE — ẤN HÓA SÁT
{
  "case_id": "MC-RSC-SHA-001",

  "damage": {
    "damage_type": "killer_overloads_weak_day_master",
    "severity": "major"
  },

  "facts": {
    "seal_active": true,
    "seal_strength": "strong",
    "killer_generates_seal": true,
    "seal_supports_day_master": true
  },

  "expected": {
    "must_include_rescue": [
      "seal_transforms_killer"
    ]
  }
}
113. GOLDEN CASE — SUPPORT BUT NOT RESCUE
{
  "case_id": "MC-RSC-NEG-SUPPORT-001",

  "damage": {
    "damage_type": "hurting_officer_attacks_officer"
  },

  "facts": {
    "wealth_generates_officer": true,
    "wealth_does_not_control_hurting_officer": true
  },

  "forbidden": {
    "must_not_register_as_rescue": [
      "wealth_bridges_structure"
    ]
  }
}
This verifies Support/Rescue separation.
114. CUSTOMER-FACING WORDING
Future Composer may show:
Có cứu cách: Có
or:
Cấu trúc bị Thương Quan tác động lên Chính Quan,
nhưng Ấn tinh có lực và trực tiếp chế Thương,
nên mức phá được giảm đáng kể.
Another:
Thất Sát khá mạnh so với Nhật chủ,
nhưng có Ấn tiếp Sát và sinh Thân,
tạo thành cơ chế Sát–Ấn tương sinh giúp cấu trúc ổn định hơn.
Core engine stores structured findings only.
115. CUSTOMER WORDING SAFETY
Avoid:
Có cứu nên chắc chắn thành công.
Prefer:
Có cơ chế cứu khá rõ,
nhưng vẫn cần xét mức tổn thương còn lại và toàn bộ độ hoàn chỉnh của mệnh cục.
116. IMPLEMENTATION RECOMMENDATION
Future structure:
engines/mingju/
├── rescue.py
├── rescue_types.py
└── rules/
    └── rescue/
        ├── general.py
        ├── guan.py
        ├── sha.py
        ├── wealth.py
        ├── resource.py
        ├── capacity.py
        ├── root.py
        ├── chain.py
        ├── follow.py
        ├── transformation.py
        └── climate.py
Do not implement until documentation freeze is approved.
117. RESCUE PIPELINE
Canonical flow:
DamageResult
      ↓
For each registered Damage
      ↓
Identify applicable rescue rule family
      ↓
Collect candidate rescue sources
      ↓
Validate structural connection
      ↓
Resolve source power
      ↓
Resolve mechanism
      ↓
Resolve target coverage
      ↓
Resolve reliability
      ↓
Apply family-specific exceptions
      ↓
Deduplicate causal overlap
      ↓
Generate RescueFinding[]
      ↓
Map Rescue → Damage
      ↓
Identify untreated Damage
      ↓
Resolve confidence
      ↓
Generate trace
118. DAMAGE-RESCUE PAIRING PRINCIPLE
Canonical pairing:
DMG
↓
specific mechanism
↓
RSC
Examples:
hurting_officer_attacks_officer
↓
control damaging source
↓
seal_controls_hurting_officer
killer_overloads_weak_day_master
↓
transform killer + support Day Master
↓
seal_transforms_killer
peer_robs_wealth
↓
control peer force
↓
officer_controls_peer
This pairing must be explicit.
119. ARCHITECTURAL DECISION
Canonical definition:
PATTERN RESCUE IS A STRUCTURALLY ACTIVE MECHANISM THAT MITIGATES A SPECIFIC REGISTERED DAMAGE WITHOUT ERASING THE ORIGINAL DAMAGE HISTORY.

It is not synonymous with:
support
favorable element
Useful God
good relationship
positive Ten God
120. FINAL CONCEPTUAL MODEL
Conceptually:
Rescue Effectiveness
=
Rescue Source Power
× Structural Connection
× Reliability
× Coverage
applied to:
specific Damage
Exact numeric weighting remains unfrozen.
121. FOUR-LAYER STRUCTURAL MODEL
MC-01 now has four distinct structural layers:
Purity
Strength
Damage
Rescue
Example:
Purity: High
Pattern Strength: Strong
Damage: Major
Rescue: Strong
This may later produce:
damaged_but_rescued
rather than a simplistic:
good
or:
bad
122. PREPARATION FOR STRUCTURAL INTEGRITY
We now know:
How clear is the pattern?
How strong is the pattern?
What damages it?
What rescues those damages?
The next major question is:
After considering all of these together,
does the natal structure actually hold?
That belongs to Structural Integrity.
123. FREEZE TARGET
Before proceeding, freeze:
Rescue definition
Support/Rescue boundary
Damage-target requirement
Rescue mechanism model
Rescue strength
Rescue reliability
Rescue coverage
damage_offset semantics
Ấn chế Thương principle
Ấn hóa Sát principle
Quan chế Tỷ Kiếp principle
bridge principle
root restoration principle
family-specific handling
Damage history preservation
causal deduplication
Rescue/Grade boundary
124. NEXT DOCUMENT
Next:
07_PATTERN_GRADE.md
But before Grade is computed, the implementation design must include
the Structural Integrity synthesis layer defined in the architecture.
Therefore 07_PATTERN_GRADE.md MUST first define:
1. Structural Integrity aggregation
2. residual Damage after Rescue
3. complete / substantially_complete
4. conditionally_complete
5. mixed
6. damaged_but_rescued
7. damaged
8. failed
9. unresolved
10. Grade mapping SS / S / A / B / C / D
The Grade must be downstream from Structural Integrity,
not calculated directly from Pattern Strength or Rescue.

Có một điểm tôi muốn chỉnh nhẹ so với tên tài liệu ban đầu: danh sách kiến trúc trước đây ghi **`07_PATTERN_GRADE.md`**, nhưng thực chất file số 07 phải làm **hai việc theo đúng thứ tự**:

**Structural Integrity → Grade**.

Tôi không muốn tạo Grade trước rồi mới tìm cách giải thích. Chúng ta phải suy ra trước trạng thái như **“thành cách”, “thành cách có điều kiện”, “bị phá nhưng có cứu”, “bại cách”**, sau đó SS/S/A/B/C/D mới chỉ là lớp tóm tắt.

Vì vậy bước tiếp theo chúng ta làm **`07_PATTERN_GRADE.md`**, nhưng nội dung đầu tiên của file sẽ là **Structural Integrity Model** rồi mới đến Grade. Đây sẽ là một trong những file quan trọng nhất của toàn bộ MC-01.

