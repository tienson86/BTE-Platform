# MC-01 — WEALTH MODEL

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `09_WEALTH_MODEL.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines the Wealth Model of MC-01.

The Wealth Model evaluates the natal structural capacity related to money, resource generation, accumulation, retention, expansion, and financial volatility.

It answers:

```text
How does this chart structurally interact with wealth?
It does NOT answer:
How much money will the person earn?
What exact net worth will the person have?
Will the person definitely be rich?
At what age will wealth peak?
Those require later Luck activation and real-world context.
Canonical flow:
Structural Integrity
      ↓
Pattern Grade
      ↓
Achievement Profile
      ↓
Wealth Model
      ↓
Wealth Dimensions
2. CORE PRINCIPLE
Wealth is multi-dimensional.
The Wealth Model MUST NOT reduce all financial interpretation to:
wealth_score
as one universal number.
Instead evaluate separate dimensions:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
Optional future dimensions may include:
capital_efficiency
asset_growth
income_stability
speculative_tendency
but V1 should remain focused.
3. WHY WEALTH MUST BE SPLIT INTO MULTIPLE DIMENSIONS
A person may be:
wealth_creation = very_high
wealth_retention = low
Meaning:
kiếm tiền giỏi
nhưng giữ tiền kém
Another may be:
wealth_creation = moderate
wealth_retention = very_high
Meaning:
không tạo tiền quá nhanh
nhưng tích lũy và giữ tài sản tốt
These are structurally different financial profiles.
4. WEALTH IS NOT TÀI STAR COUNT
Critical rule:
TÀI NHIỀU ≠ GIÀU
The engine must evaluate:
Tài quality
Tài strength
Tài root
Tài exposure
Day Master capacity
Thực/Thương generation
Tỷ/Kiếp pressure
Quan protection
Useful-God compatibility
Structural Integrity
Damage
Rescue
5. WEALTH OUTPUT
Canonical object:
WealthProfile
Fields:
state
dimensions
wealth_structure
dominant_financial_mode
financial_risks
conditions_for_growth
conditions_for_loss
confidence
evidence_ids
6. WEALTH DIMENSION
Canonical object:
WealthDimension
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
7. WEALTH DIMENSIONS V1
Canonical IDs:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
8. WEALTH CREATION
wealth_creation evaluates structural capacity to generate income, opportunities, or commercial resources.
It answers:
Can the chart structurally create financial opportunity?
Potential positive signals:
Tài meaningful
Thực/Thương → Tài
Thiên Tài active
commercial chain coherent
entrepreneurship high
Day Master able to carry Wealth
Potential reducers:
Tài weak/rootless
Tài heavily damaged
Day Master unable to carry Wealth
Tỷ/Kiếp excessive
structural chain broken
9. WEALTH CREATION IS NOT WEALTH RETENTION
A person may create a lot of money but fail to hold it.
Therefore:
wealth_creation
must not automatically increase:
wealth_retention
10. WEALTH ACCUMULATION
wealth_accumulation evaluates the ability to convert repeated income into a growing financial base.
Conceptually:
income
→ retained resources
→ accumulated assets
Potential positive evidence:
Tài stable
low excessive peer pressure
good structural continuity
adequate management
stable cash-flow structure
Potential negative evidence:
high volatility
peer robbery
unstable Tài
frequent structural leakage
11. WEALTH RETENTION
wealth_retention evaluates ability to keep and preserve acquired wealth.
This is one of the most important dimensions.
Potential positive evidence:
Tài protected
Quan controls Tỷ/Kiếp
low peer competition
stable roots
high stability
high Structural Integrity
Potential negative evidence:
Tỷ Kiếp đoạt Tài
wealth overload
volatile output
unstable Tài
major financial Damage
12. BUSINESS EXPANSION
business_expansion evaluates structural capacity to scale resources.
It is not identical to entrepreneurship.
Entrepreneurship asks:
Can the person initiate business activity?
Business expansion asks:
Can that activity grow in scale?
Potential positive signals:
strong Tài
strong output→wealth chain
management capability
leadership capability
resource mobilization
wealth retention adequate
Structural Integrity high
Potential reducers:
wealth retention low
financial volatility very high
peer competition severe
structural instability
13. FINANCIAL VOLATILITY
financial_volatility measures structural instability in financial outcomes.
Important:
For this dimension:
high score
means:
high volatility
not favorable.
Therefore this dimension must define score direction explicitly.
Possible scale:
0 = very stable
100 = extremely volatile
14. SCORE DIRECTION POLICY
Most wealth dimensions:
higher = stronger financial capability
But:
financial_volatility
uses:
higher = more unstable
This direction must be explicit in schema.
Recommended field:
score_direction
Values:
higher_is_better
higher_is_riskier
15. WEALTH CREATION SIGNALS
Potential positive rule groups:
wealth_star_quality
wealth_root
wealth_exposure
output_generates_wealth
commercial_continuity
capacity_to_carry_wealth
useful_god_alignment
entrepreneurial_support
16. WEALTH CREATION NEGATIVE SIGNALS
Potential:
wealth_rootless
wealth_out_of_season
wealth_damaged
wealth_overloads_day_master
peer_competition
wealth_chain_broken
useful_god_conflict
17. TÀI STRENGTH VS WEALTH CREATION
Critical distinction:
Tài strong
is not automatically:
wealth_creation high
Because strong Tài may:
overload weak Day Master
Therefore Wealth Model must compare:
wealth force
vs
Day Master carrying capacity
18. CARRYING CAPACITY
Canonical concept:
wealth_carrying_capacity
This should consume:
Day Master Strength
Resource support
Peer support
Structural Integrity
Damage / Rescue
It MUST NOT recalculate Strength Engine.
19. CARRYING CAPACITY STATES
Possible canonical classification:
insufficient
limited
adequate
strong
very_strong
unresolved
Exact score formula remains unfrozen.
20. TÀI NHIỀU THÂN NHƯỢC
This is a central wealth rule.
Scenario:
Wealth force = strong/very_strong
Day Master capacity = weak/very_weak
Potential result:
wealth_creation opportunity = may remain high
wealth_retention = reduced
financial_volatility = increased
This nuance is critical.
Do NOT simply classify wealth as bad.
21. FINANCIAL PRESSURE VS FINANCIAL OPPORTUNITY
A strong Wealth structure may simultaneously create:
high opportunity
+
high pressure
The Wealth Model must support both.
Example:
wealth_creation = high
wealth_retention = low
financial_volatility = high
22. THỰC / THƯƠNG → TÀI
A coherent output-to-wealth chain is one of the most important Wealth signals.
Canonical chain:
Thực / Thương
      ↓
Tài
Potential effects:
wealth_creation increase
business_expansion increase
entrepreneurship synergy
23. OUTPUT→WEALTH CHAIN VALIDITY
The chain is valid only if:
output force structurally active
wealth force structurally active
generation relationship effective
chain not broken
Day Master can sustain output
Theoretical element sequence alone is insufficient.
24. THỰC THẦN SINH TÀI
Potentially favorable for:
wealth_creation
wealth_accumulation
business_expansion
when:
Thực has force
Tài receives generation
Day Master can produce output
25. THƯƠNG QUAN SINH TÀI
Potentially favorable for:
wealth_creation
entrepreneurship
business expansion
market adaptation
but may also increase:
financial_volatility
depending on stability.
26. TỶ KIẾP PRESSURE
Tỷ/Kiếp pressure is central to Wealth retention.
Potential condition:
Tỷ/Kiếp strong
Tài meaningful
competition relation active
Possible effects:
wealth_retention down
wealth_accumulation down
financial_volatility up
27. TỶ KIẾP DOES NOT ALWAYS DESTROY WEALTH
Forbidden:
Tỷ/Kiếp present
→ wealth retention low
The engine must evaluate:
peer strength
wealth strength
Day Master strength
Quan control
structural context
28. QUAN PROTECTION OF WEALTH
Potential mechanism:
Quan controls Tỷ/Kiếp
This may improve:
wealth_retention
wealth_accumulation
financial stability
if peer robbery is a real threat.
29. QUAN AS WEALTH PROTECTOR
Do not automatically give positive wealth score because Quan exists.
Quan only protects Wealth when:
Tỷ/Kiếp pressure exists
Quan has force
Quan can control peer force
30. WEALTH ROOTS
Wealth rooted in Earthly Branches may support:
wealth continuity
wealth retention
accumulation
But root quality matters.
Do not use raw count only.
31. EXPOSED WEALTH
Tài exposed may support:
wealth visibility
wealth activity
commercial expression
But exposed + rootless Wealth may produce:
high opportunity visibility
low stability
32. HIDDEN WEALTH
Hidden but rooted Wealth may support:
accumulation
retention
underlying asset base
This should be tested with Golden Cases.
Do not overstate without calibration.
33. CHÍNH TÀI VS THIÊN TÀI
These should not be mapped simplistically.
Conceptual tendencies:
Chính Tài
→ stability
→ disciplined accumulation
→ predictable income structure

Thiên Tài
→ opportunity
→ expansion
→ flexible commercial activity
→ higher variability
These are directional tendencies only.
34. CHÍNH TÀI MODEL
Potential support for:
wealth_accumulation
wealth_retention
financial stability
management
Potentially less associated with:
extreme expansion
unless supported by other structures.
35. THIÊN TÀI MODEL
Potential support for:
wealth_creation
business_expansion
entrepreneurship
opportunity capture
Potential risk:
financial_volatility
if structural controls are weak.
36. CHÍNH + THIÊN TÀI MIX
Mixed Wealth structures may produce:
diversified financial capacity
or:
fragmented financial focus
depending on coherence.
Purity determines mixing.
Wealth Model determines financial effect.
37. WEALTH AS DỤNG THẦN
If Wealth element / Ten-God function aligns with Dụng/Hỷ:
Possible positive modifier:
wealth usability increases
But:
Tài = Dụng
does not automatically mean rich.
Still evaluate capacity and damage.
38. WEALTH AS KỴ THẦN
If Wealth force is structurally unfavorable:
Possible effects:
wealth opportunity may exist
but carrying cost / pressure increases
This is especially important.
Do not output:
Tài is Kỵ
→ no wealth
39. USEFUL GOD COMPATIBILITY
Wealth Model should consume:
UsefulGodCompatibilityResult
not recompute Useful God.
Possible states:
strongly_aligned
aligned
neutral
conflicting
strongly_conflicting
40. WEALTH AND CLIMATE
Climate may affect whether financial structure is usable.
Example:
Tài structure strong
but chart climate prevents effective flow
This may reduce usability or stability.
Climate should not be ignored.
41. STRUCTURAL INTEGRITY MODIFIER
High Structural Integrity may improve:
wealth_accumulation
wealth_retention
business_expansion reliability
Low Integrity may increase:
financial volatility
But Integrity must not simply add to every Wealth dimension equally.
42. GRADE VS WEALTH
Critical distinction:
Grade A
does not imply:
wealth very_high
A high-grade Ấn/Quan structure may have:
authority high
wealth moderate
A lower-grade Tài structure may still have:
wealth creation high
volatility high
43. ACHIEVEMENT VS WEALTH
Entrepreneurship may support Wealth creation.
Management may support Wealth accumulation.
Stability may support Wealth retention.
But Wealth Model remains separate.
44. WEALTH PROFILE OUTPUT
Conceptual example:
{
  "state": "resolved",

  "dimensions": {
    "wealth_creation": {
      "score": 82,
      "classification": "high"
    },
    "wealth_accumulation": {
      "score": 69,
      "classification": "above_average"
    },
    "wealth_retention": {
      "score": 54,
      "classification": "moderate"
    },
    "business_expansion": {
      "score": 77,
      "classification": "high"
    },
    "financial_volatility": {
      "score": 71,
      "classification": "high"
    }
  }
}
Numbers are illustrative only.
45. FINANCIAL PROFILE EXAMPLE — HIGH CREATION / LOW RETENTION
wealth_creation = very_high
wealth_accumulation = moderate
wealth_retention = low
business_expansion = high
financial_volatility = very_high
Customer interpretation may later be:
Khả năng tạo cơ hội tài chính mạnh,
nhưng dòng tiền dễ biến động và cần kỷ luật giữ vốn.
46. PROFILE — SLOW BUT STABLE WEALTH
wealth_creation = moderate
wealth_accumulation = high
wealth_retention = very_high
business_expansion = moderate
financial_volatility = low
This may represent:
tích lũy bền
giữ tài sản tốt
không thiên về mở rộng nhanh
47. PROFILE — STRONG BUSINESS EXPANSION
Potential:
wealth_creation = high
wealth_retention = high
business_expansion = very_high
management = high
leadership = high
financial_volatility = moderate
This is structurally different from speculative high-volatility wealth.
48. FINANCIAL VOLATILITY SIGNALS
Potential increases:
Thiên Tài very strong
Thương Quan strong
Tỷ/Kiếp competition
wealth overload
root instability
structural fragmentation
low Stability
Potential decreases:
Chính Tài stable
Quan protection
strong roots
high Stability
high Integrity
low unresolved Damage
49. VOLATILITY IS NOT LOSS
Critical:
high volatility
does not mean:
financial loss
It means:
larger swings
less predictability
greater need for risk control
50. WEALTH RETENTION SIGNALS
Potential positive:
wealth rooted
wealth protected
low peer robbery
high stability
high management
strong Integrity
Potential negative:
peer robbery
weak wealth roots
high volatility
wealth overload
uncontrolled expansion
51. WEALTH ACCUMULATION SIGNALS
Potential positive:
wealth creation adequate
wealth retention adequate
stability
management
repeatable income structure
Potential negative:
creation high but retention low
high volatility
repeated structural leakage
52. BUSINESS EXPANSION SIGNALS
Potential positive:
wealth creation high
entrepreneurship high
management high
leadership adequate
wealth retention adequate
commercial chain strong
Potential negative:
retention low
capacity weak
volatility extreme
peer competition severe
53. CAPITAL CARRYING CAPACITY
A future internal measure may evaluate:
How much Wealth force can the Day Master and structure carry?
Conceptual inputs:
Day Master Strength
Resource
Peers
Integrity
Rescue
Do not freeze numeric ratios yet.
54. WEALTH OVERLOAD
Potential finding:
wealth_overload
when:
wealth force >> carrying capacity
Possible effects:
wealth_creation may remain strong
wealth_retention decreases
financial_volatility increases
55. WEALTH UNDERUTILIZATION
Opposite case:
carrying capacity strong
but Wealth force weak
Possible:
financial capacity exists
but wealth opportunity structure is limited
This distinction can later improve customer wording.
56. WEALTH OPPORTUNITY VS WEALTH CAPACITY
Recommended conceptual split:
wealth_opportunity
wealth_capacity
Even if these remain internal.
Example:
opportunity = high
capacity = low
creates overload.
opportunity = moderate
capacity = high
creates stable but slower wealth.
57. DOMINANT FINANCIAL MODE
Future dominant_financial_mode may classify profile.
Possible IDs:
steady_accumulator
opportunity_creator
expansion_builder
high_turnover_high_volatility
capital_preserver
resource_manager
mixed_financial_profile
unresolved
Do not implement until dimensions are stable.
58. FINANCIAL RISKS
Possible structured risks:
wealth_overload
peer_competition
poor_retention
overexpansion
high_volatility
weak_wealth_root
broken_income_chain
excessive_risk_taking
These should reference evidence.
59. CONDITIONS FOR GROWTH
Possible structured conditions:
maintain capital discipline
strengthen management
use structured expansion
avoid excessive leverage
benefit from stable support
benefit from commercial output
Final Vietnamese prose belongs to Composer.
60. CONDITIONS FOR LOSS
Possible structural conditions:
peer competition increases
overexpansion
loss of control
high-risk speculation
capacity overload
wealth root disruption
These are not event predictions.
61. NO SPECIFIC INVESTMENT ADVICE
Core Wealth Model should not output:
buy stocks
buy real estate
buy gold
use leverage
Those are advisory decisions beyond structural inference.
The engine only describes structural financial tendencies.
62. NO EXACT INCOME PREDICTION
Forbidden:
monthly income = 500 million
or:
will become millionaire
MC-01 has no basis for exact financial outcome.
63. NO “RICH / POOR” BINARY YET
At this stage avoid direct canonical labels:
rich
poor
Instead use:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
A later Composer may summarize carefully.
64. FUTURE WEALTH SUMMARY
Composer may later generate:
Tài vận có khả năng tạo dòng tiền khá tốt,
đặc biệt ở các hoạt động chủ động và mở rộng.
Tuy nhiên khả năng giữ tiền chỉ ở mức trung bình,
nên kỷ luật vốn là điều quan trọng.
This is much more informative than:
Tài vận tốt.
65. WEALTH SCORE MODEL
Conceptually:
Wealth Dimension
=
Relevant Wealth Structure
+ Output→Wealth Flow
+ Carrying Capacity
+ Protection
+ Structural Integrity
- Domain-Specific Damage
± Useful-God Compatibility
± Stability
Exact numeric formula remains unfrozen.
66. FINANCIAL VOLATILITY MODEL
Conceptually:
Financial Volatility
=
Instability
+ Peer Competition
+ Speculative/Opportunity Structure
+ Weak Retention
+ Residual Damage
- Structural Stability
- Wealth Protection
Exact formula remains unfrozen.
67. WEALTH EVIDENCE MODEL
Recommended:
WealthEvidence
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
68. WEALTH SIGNAL TYPES
Initial:
wealth_pattern
wealth_strength
wealth_root
wealth_exposure
output_to_wealth
carrying_capacity
peer_pressure
officer_protection
damage
rescue
integrity
useful_god_alignment
stability
entrepreneurship
management
69. CAUSAL DEDUPLICATION
The same Tỷ Kiếp đoạt Tài event may affect:
wealth_retention
wealth_accumulation
financial_volatility
This is allowed.
But each dimension must apply its own rule.
Do not apply one hidden global penalty and then duplicate it.
70. RULE NAMESPACES
Recommended:
MC-WLT-CREATE-*
MC-WLT-ACCUM-*
MC-WLT-RETAIN-*
MC-WLT-EXPAND-*
MC-WLT-VOL-*
MC-WLT-CAPACITY-*
MC-WLT-PEER-*
MC-WLT-PROTECT-*
MC-WLT-GENERAL-*
71. RULE PRIORITY
Conceptual precedence:
explicit exception
>
pattern-family wealth rule
>
capacity-mismatch rule
>
wealth-protection rule
>
wealth-flow rule
>
general wealth rule
72. STANDARD WEALTH PATTERN
For standard Tài patterns, evaluate:
wealth power
root
exposure
generation
capacity
peer pressure
protection
integrity
73. NON-WEALTH PRIMARY PATTERN
Important:
A chart does NOT need:
primary pattern = Tài
to have strong Wealth potential.
Example:
primary = Thực Thần
secondary = Tài
with strong:
Thực → Tài
may produce strong Wealth creation.
74. QUAN PATTERN WEALTH
A strong Quan structure may produce financial stability through:
management
institutional income
Tài→Quan structure
even if Tài is not the primary pattern.
Wealth Model must evaluate entire structure.
75. ẤN PATTERN WEALTH
Ấn-heavy structures may have:
wealth_creation moderate
wealth_retention high
or other combinations depending on chart.
Do not stereotype.
76. THỰC / THƯƠNG PATTERN WEALTH
Output structures may strongly support:
wealth_creation
entrepreneurship
business_expansion
if they effectively generate Tài.
77. KIẾN LỘC / DƯƠNG NHẪN WEALTH
Potentially important factors:
self-force strong
capacity strong
peer pressure strong
need for Tài/Quan/output control
High carrying capacity may coexist with:
high peer competition
so Wealth retention must be evaluated carefully.
78. TÒNG TÀI WEALTH
For valid:
cong_cai
Wealth orientation may be structurally dominant.
But Wealth quality depends on:
follow purity
follow strength
counterforce
integrity
useful-god alignment
Do not automatically assign maximum scores.
79. TÒNG QUAN SÁT WEALTH
Wealth may act mainly as:
generator of authority
rather than the dominant financial theme.
So strong Tài in such structure may contribute indirectly.
80. TÒNG NHI WEALTH
Output-heavy follow structures may have strong:
output→wealth
commercial potential.
Evaluate continuity and stability.
81. HÓA KHÍ WEALTH
Requires dedicated rules based on transformed structure.
Do not apply ordinary Wealth assumptions blindly.
82. WEALTH MODEL AND RESCUE
Rescue may improve Wealth profile when it mitigates a relevant Damage.
Example:
peer_robs_wealth
+
officer_controls_peer
may improve:
wealth_retention
wealth_accumulation
But original Damage remains in trace.
83. WEALTH MODEL AND DAMAGE
Relevant damage types may include:
peer_robs_wealth
wealth_overloads_weak_day_master
generator_destroyed
structural_chain_broken
root_destroyed
useful_god_conflict
Each affects specific Wealth dimensions differently.
84. DAMAGE-SPECIFIC EFFECTS
Example:
peer_robs_wealth
likely affects:
wealth_retention ↓
wealth_accumulation ↓
volatility ↑
Example:
wealth_overloads_weak_day_master
may affect:
creation opportunity may remain
retention ↓
volatility ↑
85. WEALTH PROFILE STATE
Allowed:
resolved
partially_resolved
unresolved
insufficient_evidence
86. WEALTH CONFIDENCE
Confidence depends on:
Integrity confidence
wealth evidence coverage
Day Master Strength confidence
Useful God confidence
Damage/Rescue confidence
Achievement support confidence
missing hour pillar
87. MISSING HOUR PILLAR
Hour Pillar absence may affect:
wealth roots
wealth exposure
peer pressure
Therefore confidence may decrease.
Do not assume missing facts are absent.
88. WEALTH PROFILE EXAMPLE
Illustrative:
{
  "state": "resolved",

  "dimensions": {
    "wealth_creation": {
      "score": 84,
      "classification": "high",
      "confidence": 0.9
    },

    "wealth_accumulation": {
      "score": 68,
      "classification": "above_average",
      "confidence": 0.86
    },

    "wealth_retention": {
      "score": 49,
      "classification": "moderate",
      "confidence": 0.88
    },

    "business_expansion": {
      "score": 78,
      "classification": "high",
      "confidence": 0.84
    },

    "financial_volatility": {
      "score": 74,
      "classification": "high",
      "confidence": 0.87,
      "score_direction": "higher_is_riskier"
    }
  },

  "financial_risks": [
    "peer_competition",
    "high_volatility"
  ]
}
Numbers are illustrative only.
89. CUSTOMER PRESENTATION
Future UI may show:
TÀI VẬN

Khả năng tạo tiền
★★★★☆

Khả năng tích lũy
★★★☆☆

Khả năng giữ tiền
★★★☆☆

Khả năng mở rộng kinh doanh
★★★★☆

Biến động tài chính
★★★★☆  Cao
Important:
Volatility must be clearly labeled as risk,
not positive stars.
90. BETTER UI FOR VOLATILITY
Prefer:
Biến động tài chính:
Cao
rather than:
★★★★☆
to avoid confusion.
91. CUSTOMER SUMMARY EXAMPLE
Khả năng tạo tiền và mở rộng khá tốt,
nhưng dòng tiền có xu hướng biến động hơn mức trung bình.
Khả năng giữ tiền không mạnh bằng khả năng kiếm tiền,
vì vậy cấu trúc phù hợp với chiến lược tăng trưởng có kiểm soát hơn là mở rộng thiếu kỷ luật.
Generated only after structured evidence exists.
92. CUSTOMER WORDING SAFETY
Avoid:
Bạn có số đại gia.
Prefer:
Lá số có nhiều tín hiệu hỗ trợ khả năng tạo và mở rộng nguồn tài chính.
Avoid:
Bạn không giữ được tiền.
Prefer:
Khả năng giữ tiền yếu hơn khả năng tạo tiền,
nên quản trị vốn là điểm cần chú ý.
93. GOLDEN DATASET REQUIREMENTS
Wealth Golden Cases must cover:
strong Tài + strong Day Master
strong Tài + weak Day Master
weak Tài + strong Day Master
Thực sinh Tài
Thương sinh Tài
Tỷ Kiếp đoạt Tài
Tỷ Kiếp pressure + Quan protection
Chính Tài stable
Thiên Tài expansion
mixed Chính/Thiên Tài
high creation + low retention
low creation + high retention
high expansion + high volatility
stable accumulation
Tòng Tài
Kiến Lộc with peer pressure
Dương Nhẫn with Wealth
damaged wealth root
wealth as Useful God
wealth as Kỵ
missing hour pillar
94. GOLDEN CASE — STRONG CREATION
{
  "case_id": "MC-WLT-CREATE-001",

  "facts": {
    "wealth_strength": "strong",
    "wealth_rooted": true,
    "output_to_wealth_chain": true,
    "day_master_capacity": "adequate",
    "major_wealth_damage": false
  },

  "expected": {
    "wealth_creation": [
      "high",
      "very_high"
    ]
  }
}
95. GOLDEN CASE — WEALTH OVERLOAD
{
  "case_id": "MC-WLT-OVERLOAD-001",

  "facts": {
    "wealth_strength": "very_strong",
    "day_master_capacity": "insufficient"
  },

  "expected": {
    "wealth_creation": [
      "above_average",
      "high",
      "very_high"
    ],
    "wealth_retention": [
      "very_low",
      "low",
      "below_average",
      "moderate"
    ],
    "financial_volatility": [
      "high",
      "very_high"
    ]
  }
}
This verifies that opportunity and carrying capacity are separate.
96. GOLDEN CASE — PEER ROBS WEALTH
{
  "case_id": "MC-WLT-RETAIN-001",

  "facts": {
    "damage": "peer_robs_wealth",
    "rescue": "none"
  },

  "expected": {
    "wealth_retention": [
      "low",
      "below_average"
    ]
  }
}
97. GOLDEN CASE — QUAN PROTECTS WEALTH
{
  "case_id": "MC-WLT-PROTECT-001",

  "facts": {
    "damage": "peer_robs_wealth",
    "rescue": "officer_controls_peer"
  },

  "expected": {
    "wealth_retention": [
      "moderate",
      "above_average",
      "high"
    ]
  }
}
Exact range remains calibration-dependent.
98. GOLDEN CASE — THỰC SINH TÀI
{
  "case_id": "MC-WLT-FLOW-001",

  "facts": {
    "shi_shen_strength": "strong",
    "wealth_strength": "strong",
    "output_generates_wealth": true,
    "chain_intact": true
  },

  "expected": {
    "wealth_creation": [
      "high",
      "very_high"
    ]
  }
}
99. NEGATIVE GOLDEN CASE — TÀI EXISTS ONLY
{
  "case_id": "MC-WLT-NEG-001",

  "facts": {
    "wealth_present": true,
    "wealth_strength": "very_weak",
    "wealth_rooted": false
  },

  "forbidden": {
    "wealth_creation": "very_high"
  }
}
100. NEGATIVE GOLDEN CASE — TÀI STRONG ≠ RETENTION
{
  "case_id": "MC-WLT-NEG-002",

  "facts": {
    "wealth_strength": "very_strong",
    "peer_pressure": "very_strong"
  },

  "forbidden": {
    "wealth_retention": "very_high"
  }
}
101. NEGATIVE GOLDEN CASE — GRADE SS
{
  "case_id": "MC-WLT-NEG-003",

  "facts": {
    "grade": "SS",
    "wealth_structure": "weak"
  },

  "forbidden": {
    "wealth_creation": "very_high"
  }
}
Grade does not substitute Wealth evidence.
102. NEGATIVE GOLDEN CASE — BIOGRAPHY
Adding:
income = high
net_worth = high
business_owner = true
must NOT alter WealthProfile.
Biography is validation-only.
103. WEALTH INVARIANTS
WLT-01
Tài presence alone cannot determine Wealth Profile.
WLT-02
Tài strength alone cannot determine Wealth Profile.
WLT-03
Wealth creation and Wealth retention are separate.
WLT-04
Wealth creation and financial volatility may both be high.
WLT-05
Day Master carrying capacity must use canonical Strength Engine output.
WLT-06
Tỷ/Kiếp presence alone cannot determine poor retention.
WLT-07
Quan protection requires an actual relevant relation.
WLT-08
Grade alone cannot determine Wealth.
WLT-09
Achievement entrepreneurship alone cannot determine Wealth.
WLT-10
Biography cannot affect natal Wealth Profile.
WLT-11
Current Đại Vận cannot change natal Wealth dimensions.
WLT-12
Every dimension must have trace.
WLT-13
Financial volatility score direction must be explicit.
WLT-14
Same input + same ruleset = same Wealth Profile.
104. FAILURE CONDITIONS
Wealth implementation FAILS if it:
1. maps Tài count directly to wealth
2. creates only one wealth score
3. treats strong Tài as guaranteed wealth
4. ignores Day Master carrying capacity
5. ignores Tỷ/Kiếp pressure
6. ignores Thực/Thương → Tài chains
7. ignores protection/rescue
8. collapses creation and retention
9. treats volatility as positive
10. uses biography
11. uses current luck cycle
12. predicts exact income
13. labels rich/poor without structured basis
14. produces unexplained financial scores
105. WEALTH PIPELINE
Canonical:
StructuralIntegrityResult
      ↓
Pattern Grade
      ↓
Achievement Profile
      ↓
Collect Wealth structural signals
      ↓
Resolve Wealth force
      ↓
Resolve Day Master carrying capacity
      ↓
Resolve output→wealth flow
      ↓
Resolve peer pressure
      ↓
Resolve protection / Rescue
      ↓
Resolve Useful-God compatibility
      ↓
Resolve stability / volatility
      ↓
Deduplicate causal evidence
      ↓
Compute Wealth dimensions independently
      ↓
Resolve dominant financial mode
      ↓
Resolve risks / conditions
      ↓
Resolve confidence
      ↓
Generate trace
      ↓
WealthProfile
106. FIVE-QUESTION WEALTH MODEL
Before the Wealth Model is considered complete,
it must answer five separate questions:
1. Có khả năng tạo tiền không?
2. Có khả năng tích lũy không?
3. Có khả năng giữ tiền không?
4. Có khả năng mở rộng quy mô không?
5. Mức biến động tài chính lớn đến đâu?
No single dimension may substitute for the others.
107. PHÚ / BẦN DECISION BOUNDARY
MC-01 should NOT yet produce a canonical binary:
phú
bần
from this model alone.
A later synthesis may infer:
wealth potential high
wealth retention high
wealth accumulation high
financial volatility controlled
and summarize:
tiềm năng tài chính cao và bền
But direct traditional “phú/bần” classification requires additional validation and probably Luck activation.
108. WHY THIS BOUNDARY MATTERS
Two charts may both have:
wealth_creation = high
but:
Chart A:
retention = high
volatility = low
Chart B:
retention = low
volatility = very_high
Calling both:
giàu
would destroy important information.
109. NATAL WEALTH VS LUCK ACTIVATION
Natal Wealth Profile asks:
What financial potential exists?
Luck asks:
When does Wealth become easier or harder to activate?
Example future model:
Natal wealth_creation = 82

Đại Vận A:
wealth_activation = high

Đại Vận B:
wealth_activation = low
Natal score remains 82.
110. FUTURE WEALTH ACTIVATION MODEL
Possible later inputs:
luck-cycle Tài
luck-cycle Dụng/Hỷ/Kỵ
activation of natal wealth root
activation of output→wealth chain
activation of peer robbery
This is outside 09_WEALTH_MODEL.md.
111. CUSTOMER VALUE
The intended commercial result is not:
Tài vận: Tốt
but something closer to:
Khả năng tạo tiền: Cao
Khả năng tích lũy: Khá
Khả năng giữ tiền: Trung bình
Khả năng mở rộng: Cao
Biến động tài chính: Cao

Kết luận:
Có năng lực tạo và mở rộng dòng tiền,
nhưng giữ vốn yếu hơn khả năng kiếm tiền.
This is much more useful and believable.
112. ARCHITECTURAL DECISION
Canonical definition:
WEALTH MODEL EVALUATES THE STRUCTURAL CAPACITY TO CREATE, ACCUMULATE, RETAIN, AND EXPAND FINANCIAL RESOURCES, WHILE SEPARATELY MEASURING FINANCIAL VOLATILITY.

It is not:
Tài count
→ rich / poor
113. FINAL CONCEPTUAL MODEL
Wealth Creation
=
Wealth Structure
+ Output→Wealth Flow
+ Commercial Capability
+ Carrying Capacity
- Relevant Damage
Wealth Accumulation
=
Creation
+ Stability
+ Management
+ Retention
- Leakage
Wealth Retention
=
Wealth Protection
+ Roots
+ Stability
- Peer Pressure
- Overload
- Volatility
Business Expansion
=
Creation
+ Entrepreneurship
+ Management
+ Leadership
+ Capital Capacity
- Expansion Risk
Financial Volatility
=
Structural Instability
+ Peer Pressure
+ High-Risk Opportunity Structure
+ Residual Damage
- Stability
- Protection
Exact numeric weights remain unfrozen.
114. FREEZE TARGET
Before moving to Career Model, freeze:
five-dimensional Wealth model
wealth creation definition
wealth accumulation definition
wealth retention definition
business expansion definition
financial volatility definition
score-direction rule
Tài strength / Wealth boundary
carrying-capacity principle
output→wealth principle
Tỷ/Kiếp pressure principle
Quan protection principle
Useful-God compatibility principle
Grade/Wealth boundary
Achievement/Wealth boundary
Natal/Luck boundary
no biography fitting
no rich/poor binary yet
trace requirement
115. NEXT DOCUMENT
Next:
10_CAREER_MODEL.md
Purpose:
- convert Achievement + Wealth profiles into work-style recommendations
- distinguish formal institution vs entrepreneurship
- distinguish leadership vs specialist roles
- define management fit
- define technical / academic / creative work environments
- define autonomy needs
- define risk tolerance
- define primary / secondary career directions
- avoid mapping one Ten God directly to one profession
- avoid deterministic job predictions

Điểm quan trọng nhất của file này là chúng ta đã tách hẳn **“kiếm tiền”**, **“tích lũy”**, **“giữ tiền”**, **“mở rộng”** và **“biến động”**. Đây sẽ giúp BTE sau này trả lời khách hàng rất thực tế, ví dụ: **“người này kiếm được nhiều nhưng khó giữ”** khác hoàn toàn **“người này kiếm chậm nhưng tích sản rất bền”**.

Bước tiếp theo là `10_CAREER_MODEL.md`, nơi chúng ta ghép **Achievement Profile + Wealth Profile + Mệnh cục** để suy luận môi trường nghề nghiệp phù hợp: **làm trong hệ thống, quản trị, làm chủ, chuyên môn kỹ thuật, học thuật, sáng tạo hay kinh doanh**.