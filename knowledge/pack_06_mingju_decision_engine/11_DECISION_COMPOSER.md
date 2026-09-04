# MC-01 — DECISION COMPOSER

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `11_DECISION_COMPOSER.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`  
**Composer version target:** `bte.mingju.composer.v1`

---

# 1. PURPOSE

This document defines the Decision Composer layer of MC-01.

The Composer transforms structured MC-01 results into coherent customer-facing conclusions.

It consumes:

```text
PatternDecision
PatternPurityResult
PatternStrengthResult
Support
Damage
Rescue
StructuralIntegrityResult
PatternGradeResult
AchievementProfile
WealthProfile
CareerProfile

and produces:
headline
executive summary
key strengths
key risks
conditions for success
conditions to avoid
achievement summary
wealth summary
career summary
technical explanation summary
The Composer must remain deterministic.
2. CORE PRINCIPLE
The Composer does NOT own analytical truth.
Canonical separation:
Decision Engine
= determines facts

Decision Composer
= communicates facts
Forbidden:
Composer sees Chính Quan
→ invents "làm quan lớn"
Correct:
authority = high
institutional_career = high
integrity = substantially_complete
→ Composer may summarize:
"Cấu trúc có lợi thế rõ về quản trị và môi trường có tổ chức."
3. NO NEW INFERENCE
The Composer MUST NOT:
1. calculate Pattern
2. calculate Purity
3. calculate Pattern Strength
4. create Damage
5. create Rescue
6. assign Grade
7. calculate Achievement scores
8. calculate Wealth scores
9. calculate Career fit
10. use biography to strengthen conclusions
11. use current Đại Vận to rewrite natal conclusions
12. invent unsupported customer claims
4. COMPOSER INPUT
Recommended root input:
MingJuDecisionResult
Minimum fields:
pattern
purity
pattern_strength
support
damage
rescue
integrity
grade
achievement
wealth
career
confidence
warnings
trace
5. COMPOSER OUTPUT
Recommended object:
MingJuComposedDecision
Fields:
composer_version
state
headline
executive_summary
structural_summary
strengths
risks
conditions_for_success
conditions_to_avoid
achievement_summary
wealth_summary
career_summary
confidence_note
technical_summary
message_keys
source_evidence_ids
6. HEADLINE
Headline should answer:
Mệnh cục này là gì
và trạng thái tổng quát ra sao?
Example:
Chính Quan cách — thành cách khá vững.
Example:
Chính Quan cách — có phá nhưng có cứu.
Example:
Tài cách — thành cách có điều kiện.
Example unresolved:
Chưa đủ căn cứ xác định chắc chắn trạng thái mệnh cục.
7. HEADLINE MUST USE STRUCTURAL STATE
Headline should combine:
pattern label
+
integrity state
not:
pattern
+
wealth claim
Forbidden headline:
Chính Quan cách — số làm quan lớn.
8. CUSTOMER LABEL MAPPING
Suggested structural-state labels:
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
9. EXECUTIVE SUMMARY
Executive summary should ideally contain 3–6 concise findings.
Suggested order:
1. Structural identity
2. Structural quality
3. Dominant achievement potential
4. Wealth behavior
5. Career/work-style implication
6. Primary caution
10. EXECUTIVE SUMMARY EXAMPLE
Conceptual:
Mệnh cục lấy Chính Quan làm cấu trúc chính, độ thuần khá cao và có lực tốt.
Quan vận, quản trị và khả năng làm việc trong hệ thống là các thế mạnh nổi bật.
Tài vận thiên về khả năng tạo và mở rộng nguồn lực ở mức khá, nhưng cần giữ kỷ luật vốn.
Cấu trúc phù hợp với vai trò có trách nhiệm và quyền quyết định rõ.
Điểm cần chú ý là tác động của Thương Quan lên Quan tinh, dù đã có Ấn hỗ trợ giảm phá.
Every sentence must map to structured evidence.
11. SUMMARY LENGTH TIERS
Composer should support multiple output lengths.
Recommended modes:
compact
standard
detailed
12. COMPACT MODE
Target:
3–5 lines
Use for:
Tổng quan lá số
Mệnh cục card
dashboard summary
13. STANDARD MODE
Target:
1–3 short paragraphs
Use for:
main result page
commercial consulting summary
14. DETAILED MODE
Target:
structured multi-section explanation
Use for:
full report
PDF/DOCX
technical interpretation
All modes must originate from the same structured truth.
15. MESSAGE KEY MODEL
Core Composer SHOULD use message keys.
Example:
mingju.headline.zheng_guan.damaged_but_rescued
Example:
mingju.wealth.high_creation_low_retention
Example:
mingju.career.high_authority_high_autonomy
This separates logic from wording.
16. MESSAGE TEMPLATE EXAMPLE
Conceptual:
key:
mingju.headline.zheng_guan.damaged_but_rescued

template:
"Chính Quan cách — có phá nhưng có cứu."
17. TEMPLATE PARAMETERS
Templates may receive structured parameters.
Example:
pattern_label
grade
purity_label
strength_label
integrity_label
dominant_capability
wealth_mode
career_style
Do not pass raw arbitrary prose into templates.
18. COMPOSER DECISION PRIORITY
Not all findings should be shown.
Priority concept:
critical structural state
>
major damage/rescue
>
dominant achievement capability
>
dominant wealth behavior
>
primary career fit
>
secondary details
This prevents overloaded summaries.
19. STRUCTURAL SUMMARY
Structural summary should include:
Pattern
Purity
Pattern Strength
Damage
Rescue
Integrity
Grade
Example:
Mệnh cục Chính Quan khá thuần và có lực.
Có một cơ chế phá Quan ở mức đáng kể nhưng được Ấn tinh hỗ trợ chế Thương.
Sau tổng hợp, cấu trúc được xếp vào trạng thái "có phá nhưng có cứu", Grade A.
20. STRENGTH SUMMARY
strengths should contain 3–5 highest-confidence positive structural findings.
Potential sources:
Achievement dominant capabilities
high Wealth dimensions
high Career fit
major Support
high Integrity
21. STRENGTH SELECTION RULE
Do not select a strength solely because score is high.
Consider:
score
confidence
structural relevance
dominance
duplication
22. STRENGTH DEDUPLICATION
Example:
authority high
leadership high
management high
institutional_career high
may be summarized into:
Thế mạnh nổi bật về quản trị, lãnh đạo và môi trường có tổ chức.
instead of four repetitive sentences.
23. RISKS
risks should contain material structural risks only.
Possible sources:
major residual Damage
untreated Damage
financial volatility
poor wealth retention
career mismatch
structural instability
low confidence critical dependency
24. RISK PRIORITY
Suggested priority:
critical residual Damage
>
major untreated Damage
>
high financial volatility
>
low wealth retention
>
career-role conflict
>
secondary structural risk
25. RISK WORDING
Avoid:
sẽ thất bại
sẽ phá sản
không thể làm quan
Prefer:
đây là điểm dễ làm giảm hiệu quả
cần kiểm soát
cấu trúc này dễ chịu áp lực ở...
26. CONDITIONS FOR SUCCESS
This is one of the highest-value commercial outputs.
It should answer:
What conditions allow this natal structure to function well?
Possible sources:
conditionally_complete dependencies
Rescue requirements
Useful-God compatibility
Career autonomy needs
Management needs
Wealth discipline
27. CONDITIONS FOR SUCCESS EXAMPLE
- Phát huy tốt khi có quyền hạn và trách nhiệm rõ.
- Cần duy trì tính kỷ luật và hệ thống quản trị.
- Khi mở rộng tài chính, nên ưu tiên khả năng giữ vốn song song với tạo doanh thu.
- Cấu trúc phát huy tốt hơn khi Ấn tinh đóng vai trò điều tiết xung đột Quan–Thương.
These must come from structured conditions.
28. CONDITIONS TO AVOID
Should answer:
What conditions worsen the structural weaknesses?
Possible sources:
Damage activation
financial volatility
overexpansion
excessive hierarchy conflict
loss of autonomy
loss of structural support
29. CONDITIONS TO AVOID EXAMPLE
- Tránh mở rộng quá nhanh khi khả năng giữ vốn chưa theo kịp.
- Tránh môi trường chỉ yêu cầu phục tùng nhưng không có quyền quyết định nếu nhu cầu tự chủ rất cao.
- Tránh để xung đột giữa tính biểu đạt và cấu trúc quyền hạn trở thành đối đầu trực tiếp.
30. ACHIEVEMENT SUMMARY
Composer should summarize dominant Achievement dimensions.
Example input:
authority = high
leadership = very_high
management = high
academic = moderate
creative = low
Possible output:
Năng lực nổi bật tập trung ở lãnh đạo, quản trị và gánh trách nhiệm hơn là sáng tạo tự do.
31. ACHIEVEMENT SUMMARY MUST PRESERVE TRADE-OFFS
Example:
leadership high
management low
Composer should not say:
lãnh đạo và quản trị đều mạnh
Instead:
Có thiên hướng dẫn dắt và quyết định, nhưng năng lực tổ chức vận hành cần được củng cố.
32. WEALTH SUMMARY
Composer should synthesize:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
33. WEALTH PROFILE ARCHETYPES
Possible composer-only summary types:
strong_creation_strong_retention
strong_creation_weak_retention
stable_accumulator
high_expansion_high_volatility
moderate_creation_high_retention
mixed_financial_profile
These are summary labels only.
Do not replace raw dimensions.
34. WEALTH SUMMARY EXAMPLE — CREATE > RETAIN
Input:
creation = high
retention = moderate
expansion = high
volatility = high
Output:
Khả năng tạo và mở rộng nguồn tài chính khá mạnh,
nhưng khả năng giữ vốn thấp hơn khả năng kiếm tiền,
nên tài chính cần được quản trị theo hướng tăng trưởng có kiểm soát.
35. WEALTH SUMMARY EXAMPLE — STABLE
Input:
creation = moderate
accumulation = high
retention = very_high
volatility = low
Output:
Tài vận thiên về tích lũy bền và giữ tài sản hơn là tăng trưởng quá nhanh.
36. CAREER SUMMARY
Composer should use:
primary_work_styles
organizational_fit
leadership_fit
management_fit
entrepreneurial_fit
specialist_fit
autonomy_need
career_stability
37. CAREER SUMMARY EXAMPLE
Input:
structured_institutional
managerial
leadership high
autonomy high
Output:
Phù hợp với vai trò quản trị hoặc lãnh đạo trong môi trường có hệ thống rõ,
nhưng cần mức quyền chủ động đủ lớn để phát huy tốt.
38. CAREER SUMMARY — ENTREPRENEURIAL
Input:
entrepreneurial high
independence very_high
management moderate
wealth_volatility high
Output:
Khả năng tự triển khai công việc và kinh doanh khá mạnh,
nhưng hiệu quả phụ thuộc đáng kể vào năng lực quản trị hệ thống và kiểm soát vốn.
39. CONTRADICTION RESOLUTION
The Composer must detect contradictory statements.
Example invalid output:
Bạn rất hợp môi trường ổn định.
Bạn rất hợp môi trường biến động.
Instead synthesize:
Cấu trúc cần nền tảng ổn định nhưng vẫn cần đủ quyền tự chủ và không gian thay đổi trong phạm vi kiểm soát.
40. CONTRADICTION TYPES
Common conflicts:
institutional_fit high + autonomy_need high
leadership high + management low
entrepreneurship high + retention low
creative high + stability high
authority high + hierarchy_conflict risk
These should be expressed as trade-offs.
41. TRADE-OFF MODEL
Recommended composer object:
DecisionTradeoff
Fields:
tradeoff_id
positive_dimension
counter_dimension
resolution_key
evidence_ids
42. TRADE-OFF EXAMPLE
high_independence
+
high_institutional_fit
may resolve to:
best_in_autonomous_role_inside_structured_system
43. UNCERTAINTY PRESERVATION
If confidence is low:
Composer must soften wording.
Example:
High confidence:
Lãnh đạo là một thế mạnh nổi bật.
Medium confidence:
Lá số có xu hướng khá rõ về năng lực lãnh đạo.
Low confidence:
Có một số tín hiệu hỗ trợ năng lực lãnh đạo, nhưng mức độ chưa đủ chắc để kết luận mạnh.
44. CONFIDENCE LANGUAGE BANDS
Suggested:
0.85–1.00
→ clear / strong language

0.70–0.84
→ moderate confidence language

0.50–0.69
→ cautious language

< 0.50
→ unresolved / limited-evidence language
Exact wording remains configurable.
45. COMPOSER MUST NOT HIDE UNRESOLVED STATE
If:
grade = UNRESOLVED
do not generate:
Mệnh cục Grade B.
Instead:
Hiện chưa đủ căn cứ để chốt cấp độ mệnh cục.
46. WARNING COMPOSITION
Warnings may appear when materially relevant.
Examples:
Giờ sinh chưa đủ chắc chắn nên một số kết luận có độ tin cậy thấp hơn.
Cấu trúc Hóa Khí còn có điều kiện chưa được xác định chắc chắn.
Do not overload customer output with internal warning codes.
47. INTERNAL VS CUSTOMER LABELS
Engine:
damaged_but_rescued
Customer:
Có phá nhưng có cứu
Engine:
wealth_overloads_weak_day_master
Customer:
Tài lực lớn hơn khả năng gánh của Nhật chủ
Keep mapping explicit.
48. TECHNICAL SUMMARY
Detailed report may expose a technical summary.
Example:
Chính Quan là cách chính.
Quan có căn và được sinh trợ nên lực cách khá mạnh.
Thương Quan lộ tạo phá Quan ở mức đáng kể.
Ấn có lực và chế Thương, tạo cơ chế cứu cách.
Sau tổng hợp, phần phá còn lại ở mức nhẹ.
This should be generated from trace.
49. TECHNICAL SUMMARY MUST FOLLOW TRACE ORDER
Recommended:
Pattern
→ Purity
→ Strength
→ Damage
→ Rescue
→ Integrity
→ Grade
This mirrors the engine.
50. CUSTOMER SUMMARY ORDER
Recommended commercial order:
Headline
→ Key conclusion
→ Strengths
→ Wealth
→ Career
→ Risks
→ Conditions for success
This is more customer-friendly than raw engine order.
51. COMPOSER MODES
Recommended enum:
dashboard
commercial
technical
report
52. DASHBOARD MODE
Target:
very concise
Show:
pattern
integrity state
grade
1–2 strengths
1 risk
53. COMMERCIAL MODE
Target:
customer-readable
action-oriented
moderate detail
Show:
summary
strengths
wealth
career
risks
conditions
54. TECHNICAL MODE
Target:
expert-readable
Show:
structural reasoning
damage/rescue
confidence
trace-backed conclusion
55. REPORT MODE
Target:
full structured narrative
Used for PDF/DOCX.
Must remain consistent with dashboard mode.
56. ONE SOURCE OF TRUTH
All output modes must consume the same:
MingJuDecisionResult
No separate independent narrative calculation.
57. PARITY REQUIREMENT
If dashboard says:
Grade A
report must not say:
Grade B
If dashboard says:
wealth retention moderate
PDF must not say:
giữ tiền rất tốt
Narrative parity is mandatory.
58. COMPOSER PRIORITY MODEL
Possible priority levels:
P0 critical
P1 major
P2 important
P3 supporting
P4 optional
59. P0 CONTENT
Examples:
failed structure
critical damage
unresolved major evidence
extreme financial volatility
Always surface where relevant.
60. P1 CONTENT
Examples:
integrity state
grade
dominant achievement
major rescue
wealth creation/retention gap
61. P2 CONTENT
Examples:
secondary career fit
moderate risk
supporting structural themes
62. P3/P4 CONTENT
Detailed technical evidence,
mostly for report mode.
63. DUPLICATION CONTROL
Avoid repeating the same point across:
executive_summary
strengths
career_summary
conditions_for_success
Use semantic grouping.
64. SENTENCE DEDUPLICATION
Future implementation may assign:
semantic_key
Example:
high_authority
Once used in executive summary,
later sections should expand, not repeat identically.
65. LANGUAGE STYLE
Customer-facing language should be:
clear
structured
specific
non-mystifying
non-deterministic
practical
Avoid excessive classical terminology without explanation.
66. TECHNICAL TERMS
When using terms such as:
Thương Quan kiến Quan
Sát Ấn tương sinh
Tỷ Kiếp đoạt Tài
Composer should optionally explain them.
Example:
Thương Quan tác động trực tiếp lên Chính Quan,
tức lực biểu đạt/phản biện có thể xung với cấu trúc quyền hạn và kỷ luật.
67. NO FAKE CERTAINTY
Avoid:
chắc chắn
nhất định
số phải
định sẵn
Prefer:
thiên hướng
có lợi thế
dễ phát huy
cần điều kiện
có nguy cơ
68. NO FEAR-BASED WORDING
Avoid:
đại bại
đại hung
cả đời nghèo
không thể thành công
unless a separate traditional-label display explicitly requires it,
and even then the explanatory text should remain measured.
69. NO CUSTOMER BIOGRAPHY FITTING
Composer must not say:
Bạn đang kinh doanh nên...
unless the user explicitly requests personalized consulting outside canonical natal inference.
MC-01 Composer itself remains chart-driven.
70. NO LUCK-CYCLE LEAKAGE
Natal Composer cannot use current Đại Vận to alter statements such as:
Natal Grade
Natal Wealth Profile
Natal Career Profile
Future luck narrative may be separate.
71. STRUCTURAL SUMMARY KEY SET
Suggested keys:
mingju.pattern
mingju.purity
mingju.strength
mingju.damage
mingju.rescue
mingju.integrity
mingju.grade
72. ACHIEVEMENT KEY SET
Suggested:
mingju.achievement.authority
mingju.achievement.leadership
mingju.achievement.management
mingju.achievement.entrepreneurship
mingju.achievement.academic
mingju.achievement.technical
mingju.achievement.creative
mingju.achievement.visibility
mingju.achievement.independence
mingju.achievement.stability
73. WEALTH KEY SET
Suggested:
mingju.wealth.creation
mingju.wealth.accumulation
mingju.wealth.retention
mingju.wealth.expansion
mingju.wealth.volatility
74. CAREER KEY SET
Suggested:
mingju.career.organizational_fit
mingju.career.primary_style
mingju.career.secondary_style
mingju.career.autonomy
mingju.career.risk
mingju.career.condition
75. MESSAGE VERSIONING
Message templates should be versioned independently.
Example:
bte.mingju.messages.vi.v1
This allows wording changes without changing engine rules.
76. COMPOSER VERSIONING
Canonical:
bte.mingju.composer.v1
Changing composition policy requires Composer version update.
77. ENGINE VERSION VS COMPOSER VERSION
Example:
schema:
bte.mingju.decision.v1

rules:
bte.mingju.rules.v1

composer:
bte.mingju.composer.v2
This should be valid.
Wording evolution should not require recalculating engine truth.
78. LOCALIZATION
Canonical engine IDs remain stable.
Composer may support:
vi
en
later.
Localization should not change conclusions.
79. OUTPUT TRACEABILITY
Each composed section should preserve:
source_evidence_ids
source_result_paths
message_keys
This supports audit.
80. COMPOSED SECTION MODEL
Recommended:
ComposedSection
Fields:
section_id
state
message_key
text
priority
source_paths
evidence_ids
confidence
81. EXAMPLE COMPOSED SECTION
{
  "section_id": "wealth_summary",
  "message_key": "mingju.wealth.high_creation_lower_retention",
  "priority": "P1",
  "source_paths": [
    "wealth.dimensions.wealth_creation",
    "wealth.dimensions.wealth_retention"
  ],
  "evidence_ids": [
    "E-MC-WLT-001",
    "E-MC-WLT-008"
  ],
  "confidence": 0.88
}
82. CUSTOMER HEADLINE EXAMPLE — HIGH INTEGRITY
Chính Quan cách — thành cách khá vững.
83. CUSTOMER HEADLINE EXAMPLE — RESCUED
Chính Quan cách — có phá nhưng có cứu.
84. CUSTOMER HEADLINE EXAMPLE — CONDITIONAL
Thiên Tài cách — thành cách có điều kiện.
85. CUSTOMER HEADLINE EXAMPLE — FAILED
Prefer:
Cách cục khó phát huy trọn vẹn do tổn thương cấu trúc còn lớn.
rather than:
Bại cách, số xấu.
86. COMPOSER MUST PRESERVE GRADE
If Grade is resolved,
it should be available consistently in:
dashboard
commercial
technical
report
Whether it is shown visually in all modes is a UI decision.
87. GRADE WORDING
Do not overinterpret.
Example:
Grade A — cấu trúc mạnh và có khả năng vận hành tốt.
Not:
Grade A — người giàu và thành đạt.
88. WEALTH VOLATILITY WORDING
Because higher score means higher risk,
Composer must not use generic positive adjectives.
Input:
financial_volatility = high
Output:
Biến động tài chính cao.
Not:
Năng lực biến động tài chính cao.
89. CONDITIONAL WORDING
For conditionally_complete:
Cấu trúc có khả năng vận hành tốt khi các điều kiện hỗ trợ chính được duy trì.
Composer should mention the top 1–3 dependencies.
90. DAMAGE/RESCUE WORDING
Recommended structure:
Damage
→ Rescue
→ Residual meaning
Example:
Thương Quan tạo áp lực lên Chính Quan,
nhưng Ấn tinh có lực giúp chế Thương,
nên mức phá còn lại được giảm đáng kể.
91. DO NOT CALL ALL POSITIVE FACTORS “RESCUE”
Composer should use Rescue wording only when:
RescueFinding exists.
Otherwise say:
được hỗ trợ
được sinh trợ
not:
được cứu
92. WEALTH GAP DETECTION
Composer should detect useful gaps.
Examples:
creation high > retention low
entrepreneurship high > management low
authority high > autonomy conflict
These gaps often produce the most commercially valuable advice.
93. GAP FINDING MODEL
Recommended:
DecisionGap
Fields:
gap_id
dimension_a
dimension_b
gap_type
severity
message_key
evidence_ids
94. GAP EXAMPLES
wealth_creation_vs_retention
entrepreneurship_vs_management
leadership_vs_stability
authority_vs_hierarchy_tolerance
public_visibility_vs_stability
95. GAP SEVERITY
Suggested:
minor
moderate
major
Do not create false precision.
96. ACTIONABILITY
Composer may produce actionable structural advice.
Examples:
strengthen financial discipline
seek roles with decision authority
use stronger operational systems
avoid uncontrolled expansion
But advice must map to structured findings.
97. ACTION BOUNDARY
Do not output specific high-stakes advice such as:
invest in X
quit job
borrow money
divorce
MC-01 should remain structural and advisory.
98. DECISION SUMMARY MODEL
Recommended:
MingJuDecisionSummary
Fields:
state
headline_key
summary_keys
strength_keys
risk_keys
condition_for_success_keys
condition_to_avoid_keys
achievement_keys
wealth_keys
career_keys
confidence_note_key
99. SAMPLE ROOT OUTPUT
Conceptual:
{
  "headline": {
    "message_key": "mingju.headline.zheng_guan.damaged_but_rescued"
  },

  "executive_summary": [
    "mingju.summary.high_authority",
    "mingju.summary.strong_management",
    "mingju.wealth.high_creation_lower_retention"
  ],

  "strengths": [
    "mingju.strength.authority",
    "mingju.strength.management"
  ],

  "risks": [
    "mingju.risk.financial_volatility"
  ],

  "conditions_for_success": [
    "mingju.condition.needs_decision_authority",
    "mingju.condition.capital_discipline"
  ]
}
100. CUSTOMER OUTPUT EXAMPLE
Conceptual:
MỆNH CỤC

Chính Quan cách — có phá nhưng có cứu.
Grade A.

Cấu trúc Quan khá rõ và có lực.
Thương Quan tạo một cơ chế phá đáng kể, nhưng Ấn tinh có lực nên mức tổn thương được giảm xuống.

THẾ MẠNH

Năng lực lãnh đạo, quản trị và làm việc trong môi trường có hệ thống là các thế mạnh nổi bật.

TÀI VẬN

Khả năng tạo và mở rộng nguồn tài chính khá tốt.
Khả năng giữ tiền thấp hơn khả năng kiếm tiền, vì vậy quản trị vốn là điểm cần đặc biệt chú ý.

NGHỀ NGHIỆP

Phù hợp với vai trò có trách nhiệm, quyền quyết định và khả năng tổ chức người khác.
Môi trường có cấu trúc rõ nhưng vẫn cho phép quyền tự chủ sẽ phát huy tốt hơn.

ĐIỂM CẦN TRÁNH

Tránh mở rộng quá nhanh khi hệ thống quản trị và giữ vốn chưa theo kịp.
Every statement must be traceable.
101. CUSTOMER OUTPUT — DIFFERENT PROFILE
Example:
Thực Thần cách — thành cách khá vững.

Thế mạnh nổi bật ở khả năng sáng tạo, tạo sản phẩm và chuyển đầu ra thành giá trị thương mại.

Tài vận thiên về khả năng tạo dòng tiền từ năng lực sản xuất hoặc biểu đạt.
Khả năng tích lũy khá nhưng không nên mở rộng quá nhanh nếu biến động tài chính tăng.

Nghề nghiệp phù hợp với môi trường có không gian tự chủ, chuyên môn và khả năng tạo sản phẩm hơn là hệ thống quá cứng nhắc.
102. CONFLICT PREVENTION RULES
Composer must prevent:
high institutional fit
from generating:
không hợp môi trường hệ thống
and prevent:
wealth_retention low
from generating:
giữ tiền rất tốt
Validation must compare wording keys to source state.
103. TEMPLATE CONTRACT TESTS
Each template should declare:
required source state
forbidden source state
Example:
mingju.wealth.high_creation_low_retention

requires:
wealth_creation >= high
wealth_retention <= moderate
104. MESSAGE KEY VALIDATION
A message key must fail validation if invoked with incompatible source data.
This prevents narrative drift.
105. COMPOSER DETERMINISM
Given:
same MingJuDecisionResult
same composer version
same locale
same output mode
the composed output must be identical.
No LLM randomness inside canonical Composer.
106. LLM BOUNDARY
An LLM may later:
rephrase
expand explanation
answer follow-up questions
but must not replace canonical Composer decisions.
Recommended:
Structured Decision
→ Canonical Composer
→ optional LLM presentation layer
107. OPTIONAL LLM RULE
If LLM is used later,
it must receive structured conclusions and explicit constraints.
It should not independently reinterpret raw BaZi.
108. REPORT PARITY
The same canonical decision must feed:
/result
PDF
DOCX
commercial consulting
report
No independent report-specific conclusion logic.
109. COMPOSER GOLDEN DATASET
Golden cases must cover:
complete high-integrity pattern
damaged but rescued
damaged no rescue
mixed but usable
conditional structure
failed structure
unresolved structure

high authority profile
high entrepreneurship profile
high academic profile

high wealth creation + low retention
stable accumulator
high expansion + high volatility

high institutional + high autonomy
high leadership + low management
technical specialist
creative independent
110. GOLDEN CASE — RESCUED PATTERN
Example:
{
  "case_id": "MC-CMP-RSC-001",

  "input": {
    "pattern": "zheng_guan",
    "integrity_state": "damaged_but_rescued",
    "grade": "A",
    "damage": "hurting_officer_attacks_officer",
    "rescue": "seal_controls_hurting_officer"
  },

  "expected_message_keys": [
    "mingju.headline.zheng_guan.damaged_but_rescued"
  ],

  "forbidden_phrases": [
    "không có phá cách"
  ]
}
111. GOLDEN CASE — WEALTH GAP
{
  "case_id": "MC-CMP-WLT-001",

  "input": {
    "wealth_creation": "high",
    "wealth_retention": "low",
    "financial_volatility": "high"
  },

  "expected_message_keys": [
    "mingju.wealth.high_creation_low_retention"
  ],

  "forbidden_message_keys": [
    "mingju.wealth.stable_accumulator"
  ]
}
112. GOLDEN CASE — CAREER TRADE-OFF
{
  "case_id": "MC-CMP-CAR-001",

  "input": {
    "institutional_fit": "high",
    "autonomy_need": "very_high"
  },

  "expected_message_keys": [
    "mingju.career.structured_with_autonomy"
  ]
}
113. GOLDEN CASE — UNRESOLVED
{
  "case_id": "MC-CMP-UNRESOLVED-001",

  "input": {
    "integrity_state": "unresolved",
    "grade": "UNRESOLVED"
  },

  "forbidden": {
    "resolved_grade_language": true,
    "strong_success_claim": true
  }
}
114. COMPOSER INVARIANTS
CMP-01
Composer cannot create analytical truth.
CMP-02
Every material sentence must map to structured input.
CMP-03
Composer cannot change Grade.
CMP-04
Composer cannot change Integrity state.
CMP-05
Composer cannot hide major unresolved Damage.
CMP-06
Composer must preserve uncertainty.
CMP-07
Composer must preserve Wealth score direction.
CMP-08
Composer must not use biography.
CMP-09
Composer must not use current Đại Vận to rewrite natal result.
CMP-10
Composer output must be deterministic.
CMP-11
All output modes must use same structured truth.
CMP-12
Contradictory message keys must not coexist.
115. FAILURE CONDITIONS
Composer implementation FAILS if it:
1. invents conclusions not present in structured data
2. changes Grade
3. hides Damage because Rescue exists
4. turns high volatility into a positive capability
5. maps Achievement directly to guaranteed life outcomes
6. predicts exact profession
7. predicts exact wealth
8. uses biography
9. uses current luck cycle
10. contradicts dashboard/report output
11. produces duplicate repetitive sections
12. ignores confidence
13. uses incompatible template keys
14. cannot trace statements to evidence
116. COMPOSER PIPELINE
Canonical:
MingJuDecisionResult
      ↓
Validate source completeness
      ↓
Resolve headline
      ↓
Resolve structural summary
      ↓
Rank dominant strengths
      ↓
Rank material risks
      ↓
Detect trade-offs / gaps
      ↓
Compose Achievement summary
      ↓
Compose Wealth summary
      ↓
Compose Career summary
      ↓
Resolve success conditions
      ↓
Resolve avoid conditions
      ↓
Apply confidence language
      ↓
Deduplicate semantic content
      ↓
Select output mode
      ↓
Resolve templates
      ↓
Attach evidence references
      ↓
MingJuComposedDecision
117. COMPOSER SECTION ORDER
Recommended commercial order:
1. Headline
2. Executive Summary
3. Structural Quality
4. Strengths
5. Wealth
6. Career
7. Risks
8. Conditions for Success
9. Conditions to Avoid
Technical report may use engine-order instead.
118. EXECUTIVE SUMMARY REQUIREMENT
The executive summary should answer within approximately 30 seconds:
Cách gì?
Có thành không?
Mạnh ở đâu?
Tài vận kiểu gì?
Nghề nghiệp kiểu gì?
Điểm cần tránh là gì?
This is the customer-value target.
119. DECISION COMPOSER AND UI
UI may display only selected Composer fields.
Example:
Mệnh Cục card
→ headline
→ grade
→ short structural summary

Tổng quan lá số
→ executive summary

Consulting zone
→ conditions for success
→ conditions to avoid

Detailed interpretation
→ technical summary
Composer remains UI-independent.
120. DECISION COMPOSER AND REPORT
Report Engine should consume the same composed result.
No separate narrative logic for PDF/DOCX.
121. VERSION CONTRACT
Composer output should expose:
composer_version
message_catalog_version
locale
mode
Example:
{
  "composer_version": "bte.mingju.composer.v1",
  "message_catalog_version": "bte.mingju.messages.vi.v1",
  "locale": "vi",
  "mode": "commercial"
}
122. ARCHITECTURAL DECISION
Canonical rule:
DECISION COMPOSER COMMUNICATES STRUCTURED TRUTH; IT DOES NOT CREATE STRUCTURAL TRUTH.

And:
THE SAME MC-01 DECISION MUST PRODUCE CONSISTENT DASHBOARD, REPORT, PDF, DOCX, AND CONSULTING OUTPUTS.

123. FINAL COMPOSITION MODEL
Structured Mệnh Cục Truth
        ↓
Priority
        ↓
Conflict Resolution
        ↓
Trade-off Detection
        ↓
Confidence Language
        ↓
Template Selection
        ↓
Semantic Deduplication
        ↓
Customer Narrative
124. FREEZE TARGET
Before moving to Public API, freeze:
Composer ownership boundary
output structure
headline policy
summary policy
strength/risk selection
trade-off model
wealth summary policy
career summary policy
confidence language
message-key architecture
template validation
determinism
output-mode parity
no new inference
traceability
125. NEXT DOCUMENT
Next:
12_PUBLIC_API.md
Purpose:
- define MC-01 public entry points
- define input/output contracts
- define MingJuContext
- define MingJuDecisionResult
- define Composer output contract
- define version fields
- define error states
- define partial/unresolved behavior
- define integration with Orchestrator
- define runtime ownership
- prevent frontend from assembling MC-01 logic independently

Đến đây chuỗi MC-01 đã khá hoàn chỉnh về mặt thiết kế:

**Pattern → Purity → Strength → Damage → Rescue → Integrity → Grade → Achievement → Wealth → Career → Composer.**

Bước tiếp theo `12_PUBLIC_API.md` sẽ bắt đầu khóa **đường vào/đường ra của cả engine**, để khi Cursor thực thi sau này frontend, Report Engine hay Orchestrator chỉ gọi một contract chuẩn, không tự lấy từng field rồi ghép logic riêng.