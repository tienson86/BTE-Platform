# TV-01 — TƯ VẤN HÔN NHÂN
## 03_DECISION_PROFILE.md

**Document ID:** TV-01-03  
**Module:** TV-01_MARRIAGE  
**Product:** BTE Platform  
**Document Type:** Decision Profile Specification  
**Status:** DRAFT FOR PRODUCT OWNER REVIEW  
**Version:** 1.0  
**Language:** Vietnamese  
**Directory:** `knowledge/consulting/TV-01_MARRIAGE/`

---

# 1. Mục đích tài liệu

Tài liệu này định nghĩa **Decision Profile** cho module:

> **TV-01 — Tư vấn hôn nhân**

Decision Profile trả lời câu hỏi:

> “Khi hai lá số đã được tính đúng theo BTE canonical, TV-01 sẽ sử dụng những tiêu chí nào để đánh giá hôn nhân, tiêu chí nào quan trọng hơn, tiêu chí nào chỉ là bằng chứng phụ, và cách các tiêu chí ảnh hưởng lẫn nhau ra sao?”

Tài liệu này không định nghĩa công thức score cuối cùng.

Chi tiết score sẽ nằm tại:

`04_SCORE_ENGINE.md`

Decision Profile xác định:

- domain nào được đánh giá;
- domain nào là primary;
- domain nào là secondary;
- các loại evidence;
- priority;
- dependency;
- amplification;
- damage;
- rescue;
- conflict;
- caps;
- guardrails;
- cách tạo finding.

---

# 2. Decision Profile là gì

Decision Profile không phải:

```text
bảng cộng điểm hợp tuổi
```

Decision Profile là:

```text
Bộ quy tắc ra quyết định
+
Thứ tự ưu tiên evidence
+
Quan hệ dependency
+
Cơ chế xử lý xung đột
+
Cơ chế tạo findings
```

Nó nằm giữa:

```text
Relationship Evidence
        ↓
Decision Profile
        ↓
Domain Findings
```

---

# 3. Core principle

TV-01 đánh giá hôn nhân theo:

> **Structure first, interaction second, timing third, secondary signals last.**

Tức là ưu tiên:

```text
1. Cấu trúc lá số
2. Tác động giữa hai lá số
3. Khả năng bổ trợ / gây áp lực
4. Sự tương tác của Thập thần
5. Các domain đời sống
6. Đại vận / lưu niên
7. Thần sát / Cung Phi / Nạp âm
```

Không đảo ngược thứ tự này.

---

# 4. Decision Profile ID

Canonical profile:

```text
marriage.profile.v1
```

Version phải stable.

Khi thay đổi behavior mang tính logic:

```text
marriage.profile.v2
```

Không silent overwrite V1.

---

# 5. Các nhóm domain V1

TV-01 V1 gồm 8 domain chính:

```text
D1 Five Elements
D2 Stem / Branch Interaction
D3 Ten Gods Dynamics
D4 Interaction & Behavioral Dynamics
D5 Finance
D6 Family
D7 Children
D8 Luck / Timing
```

Ngoài ra có:

```text
Overall Marriage Decision
```

---

# 6. Domain tier

Chia domain thành 3 tầng:

## Tier 1 — Structural Core

```text
D1 Five Elements
D2 Stem / Branch
D3 Ten Gods
```

Đây là foundation.

---

## Tier 2 — Life Domains

```text
D4 Interaction
D5 Finance
D6 Family
D7 Children
```

Các domain này phụ thuộc một phần vào Tier 1.

---

## Tier 3 — Activation

```text
D8 Luck / Timing
```

Luck không thay natal structure.

Luck chỉ kích hoạt, khuếch đại hoặc làm dịu.

---

# 7. Secondary evidence

Các lớp sau không được đứng ngang hàng với Tier 1:

```text
Shen Sha
Cung Phi
Mệnh Quái
Nhóm Trạch
Nạp âm
```

Chúng có thể:

- support;
- qualify;
- explain;
- add context.

Không được:

- override structural finding;
- quyết định overall result;
- tạo hard veto.

---

# 8. Priority hierarchy

Profile V1 dùng thứ tự:

```text
P0 — Structural decisive
P1 — Major relational evidence
P2 — Strong supporting / damaging evidence
P3 — Contextual evidence
P4 — Secondary supporting evidence
P5 — Decorative / low-impact reference
```

Không phải domain nào cũng có P0.

---

# 9. P0

P0 chỉ dành cho các evidence có tính cấu trúc rất mạnh.

Ví dụ conceptually:

```text
một cấu trúc hỗ trợ Dụng thần đặc biệt rõ
một damage rất mạnh vào cấu trúc chính
một interaction phá/rescue pattern quan trọng
```

Không dùng P0 cho:

```text
một Thần sát
một Cung Phi
một Nạp âm
một Lục hợp đơn lẻ
```

---

# 10. Evidence evaluation dimensions

Mỗi evidence phải được đánh giá tối thiểu theo:

```text
direction
significance
confidence
scope
dependency
strength
damage
rescue
activation
```

Không chỉ có:

```text
positive
negative
```

---

# 11. Evidence strength

Evidence strength là mức độ evidence thật sự có khả năng tác động trong context.

Ví dụ:

```text
Có Chi xung
```

chưa đủ.

Cần xét:

```text
Chi nào?
Ở trụ nào?
Có căn không?
Có bị hợp hóa không?
Có cứu giải không?
Có được vận kích hoạt không?
```

---

# 12. Scope

Evidence phải biết scope:

```text
natal
personality
relationship
finance
family
children
timing
```

Một evidence không được tự động lan sang mọi domain.

---

# 13. No universal propagation

Ví dụ:

```text
branch clash
```

không tự động tạo:

```text
finance risk
family risk
children risk
interaction risk
```

Chỉ propagate nếu có rule dependency rõ ràng.

---

# 14. Directionality

Profile phải giữ:

```text
A_TO_B
B_TO_A
MUTUAL
SHARED
```

Vì hôn nhân có thể không đối xứng.

Ví dụ:

```text
B hỗ trợ Dụng thần A rất mạnh
A hỗ trợ B ít
```

Kết luận phải phản ánh bất đối xứng này.

---

# 15. Mutuality

Chỉ tạo finding:

```text
mutual_support
```

khi có evidence đủ mạnh theo hai chiều hoặc có cấu trúc shared thực sự.

Không suy diễn mutual từ một chiều.

---

# 16. Domain D1 — Five Elements

Mục tiêu:

> Đánh giá mức độ hai lá số bổ trợ hoặc làm mất cân bằng cấu trúc ngũ hành của nhau.

Nguồn chính:

- five element distribution;
- strength;
- useful god;
- favorable;
- unfavorable;
- temperature need;
- pattern dependency.

---

# 17. D1 primary questions

D1 phải trả lời:

1. Người B có cung cấp yếu tố A cần không?
2. Người B có làm mạnh thêm yếu tố A kỵ không?
3. Điều tương tự từ A sang B?
4. Có mutual support không?
5. Có mutual pressure không?
6. Hỗ trợ này có phù hợp Dụng/Hỷ thực sự không?
7. Có làm tổn thương cấu trúc chính không?

---

# 18. D1 không dùng “thiếu hành”

Không được:

```text
A thiếu Hỏa
B nhiều Hỏa
→ tốt
```

Phải dùng:

```text
A cần Hỏa?
B có Hỏa?
Hỏa của B có vai trò hỗ trợ?
Có bị conflict với structure khác?
```

---

# 19. D1 evidence types

Primary:

```text
useful_god_support
favorable_support
unfavorable_activation
element_balance_support
element_excess_pressure
temperature_support
temperature_conflict
```

Secondary:

```text
raw_element_presence
```

---

# 20. D1 finding classes

Có thể tạo:

```text
strong_elementary_support
asymmetric_element_support
mutual_element_support
elementary_pressure
mixed_elementary_interaction
```

Không dùng wording customer ở factual layer.

---

# 21. Domain D2 — Stem / Branch Interaction

Mục tiêu:

> Phân tích tác động trực tiếp giữa Can Chi hai lá số.

Nguồn:

```text
stem interaction
branch interaction
pillar position
strength
pattern
rescue
damage
```

---

# 22. D2 interaction types

Có thể gồm:

```text
stem combination
stem control

branch combination
branch clash
branch harm
branch punishment
branch break
branch meeting
three harmony
three meeting
six combination
```

theo canonical rule set của BTE.

---

# 23. D2 không cộng điểm cố định

Không được:

```text
lục hợp = +10
xung = -10
hại = -5
```

Mỗi interaction phải xét context.

---

# 24. Pillar significance

Không mọi trụ có giá trị như nhau.

Decision Profile phải cho phép phân biệt:

```text
year pillar
month pillar
day pillar
hour pillar
```

và đặc biệt:

```text
day branch
```

có thể có relevance cao cho quan hệ hôn nhân.

Nhưng không được tạo một quy tắc duy nhất:

```text
day branch clash = fail marriage
```

---

# 25. D2 context questions

Khi có interaction, phải xét:

- vị trí;
- direction;
- strength;
- repetition;
- dependency;
- pattern impact;
- useful god impact;
- rescue;
- luck activation.

---

# 26. D2 finding classes

Ví dụ:

```text
structural_harmony
relational_tension
recurrent_clash
resolved_conflict
latent_conflict
mixed_stem_branch_dynamics
```

---

# 27. Domain D3 — Ten Gods Dynamics

Mục tiêu:

> Đánh giá cách hai người tác động vào hệ vai trò của nhau.

Nguồn:

```text
Ten Gods
visible/hidden
strength
position
combination
pattern
useful god
```

---

# 28. D3 areas

Ưu tiên đánh giá:

```text
Authority / responsibility
Resource / support
Output / expression
Wealth / resource management
Peer / competition
```

---

# 29. D3 không stereotype

Không được suy luận:

```text
nam phải thế này
nữ phải thế kia
```

Decision Profile có thể sử dụng các rule truyền thống liên quan spouse star, nhưng:

- phải explicit;
- phải có evidence;
- phải là một component;
- không được biến thành phán xét đạo đức.

---

# 30. D3 spouse-related evidence

Có thể sử dụng:

```text
spouse-role resonance
role support
role pressure
authority mismatch
resource dependency
wealth competition
output conflict
peer competition
```

tùy rule catalog.

---

# 31. D3 finding classes

```text
role_complement
role_imbalance
supportive_role_exchange
competitive_role_exchange
control_pressure
expression_mismatch
```

---

# 32. Domain D4 — Interaction & Behavioral Dynamics

D4 là derived domain.

Không đọc trực tiếp birth data để “đoán tính cách”.

D4 lấy từ:

```text
D1
D2
D3
canonical interpretation findings
```

---

# 33. D4 mục tiêu

Đánh giá:

- giao tiếp;
- cách phản ứng khi áp lực;
- tốc độ ra quyết định;
- nhu cầu kiểm soát;
- nhu cầu tự do;
- khả năng nhường nhịn;
- cách biểu đạt;
- conflict resolution.

---

# 34. D4 không làm psychology test

Không được tạo những claim như:

```text
Person A narcissistic
Person B avoidant
```

trừ khi hệ thống có psychological data riêng.

Bát Tự chỉ cung cấp xu hướng trong phạm vi model.

---

# 35. D4 finding classes

```text
communication_support
communication_friction
decision_style_mismatch
control_tension
adaptive_interaction
emotional_pressure
```

---

# 36. Domain D5 — Finance

Mục tiêu:

> Phân tích khả năng phối hợp về tiền bạc và tài sản.

D5 dựa trên:

```text
Ten Gods
Wealth structure
Resource structure
Peer competition
Output
Pattern
Useful God
Interaction
Luck
```

---

# 37. D5 không dự đoán giàu nghèo tuyệt đối

Không được:

```text
lấy nhau sẽ giàu
lấy nhau sẽ nghèo
```

Chỉ phân tích:

- xu hướng kiếm tiền;
- xu hướng giữ tiền;
- risk appetite;
- resource competition;
- decision mismatch;
- complementarity.

---

# 38. D5 evidence classes

```text
wealth_support
wealth_pressure
resource_competition
financial_role_complement
financial_decision_conflict
risk_alignment
risk_misalignment
```

---

# 39. D5 findings

```text
financial_complement
financial_tension
resource_competition
strong_shared_financial_structure
need_for_financial_rules
```

---

# 40. Domain D6 — Family

Mục tiêu:

> Đánh giá khả năng phối hợp trong đời sống gia đình.

D6 phụ thuộc nhiều vào:

```text
D2
D3
D4
```

và có thể tham chiếu:

```text
family-related Shen Sha
```

chỉ ở mức secondary.

---

# 41. D6 areas

Có thể gồm:

- trách nhiệm;
- phối hợp;
- conflict;
- authority;
- care;
- stability;
- extended family pressure;
- shared structure.

---

# 42. D6 findings

```text
family_stability
family_role_support
family_role_tension
responsibility_mismatch
shared_structure_strength
```

---

# 43. Domain D7 — Children

TV-01 V1 chỉ đánh giá:

> khả năng phối hợp của hai người trong domain con cái.

Không phải:

```text
khả năng sinh sản y khoa
```

---

# 44. D7 scope

Có thể xem:

- cách hai người phối hợp vai trò;
- support;
- pressure;
- child-related symbolic structure;
- timing context.

Không được dự đoán chắc chắn:

```text
số con
giới tính con
vô sinh
ngày sinh con
```

---

# 45. D7 dependencies

D7 có thể phụ thuộc:

```text
Ten Gods
Output
Resource
Family
Luck
```

---

# 46. D7 findings

```text
parenting_role_complement
parenting_role_tension
child_domain_support
child_domain_pressure
```

---

# 47. Domain D8 — Luck / Timing

Mục tiêu:

> Xác định khi nào natal dynamics được kích hoạt.

D8 không thay natal decision.

---

# 48. D8 inputs

```text
Luck A
Luck B
Natal findings
Domain findings
Requested time window
```

---

# 49. Timing logic

Mỗi period có thể:

```text
amplify positive finding
amplify risk
reduce conflict
activate latent issue
create mismatch
create shared support
```

---

# 50. Timing alignment

Ví dụ:

```text
A enters supportive cycle
B enters supportive cycle
→ shared supportive timing
```

hoặc:

```text
A strong upward cycle
B high-pressure cycle
→ timing mismatch
```

Không tự gọi tốt/xấu tuyệt đối.

---

# 51. D8 findings

```text
shared_supportive_period
shared_pressure_period
asymmetric_timing
risk_activation
support_activation
```

---

# 52. Domain dependency graph

Canonical dependency concept:

```text
D1 Five Elements ─────┐
                      │
D2 Stem/Branch ───────┼──→ D4 Interaction
                      │
D3 Ten Gods ──────────┘
        │
        ├────────────→ D5 Finance
        │
        ├────────────→ D6 Family
        │
        └────────────→ D7 Children

D1–D7 ───────────────→ D8 Timing
```

---

# 53. Cross-domain evidence

Một finding ở domain này có thể support domain khác.

Ví dụ:

```text
D3 role competition
   ↓
D5 resource competition
```

Nhưng phải qua explicit cross-domain rule.

---

# 54. Cross-domain amplification

Ví dụ:

```text
D2 relational tension
+
D4 communication friction
+
D8 pressure activation
```

có thể tạo:

```text
major relationship pressure
```

Tuy nhiên finding mới vẫn phải trace nguồn.

---

# 55. Cross-domain rescue

Ví dụ:

```text
D2 clash
+
D1 strong useful-god support
+
D3 strong role complement
```

có thể giảm severity của clash finding.

Không xóa evidence gốc.

---

# 56. Damage / Rescue model

Decision Profile phải hỗ trợ:

```text
base evidence
→ damage
→ rescue
→ residual impact
```

Ví dụ:

```text
branch clash
→ negative base
→ rescued by structural combination/support
→ residual = moderate
```

---

# 57. Evidence cancellation

Không nên “cancel = delete”.

Nếu hai evidence đối nghịch:

```text
positive
negative
```

cần lưu cả hai.

Decision Result có thể kết luận:

```text
mixed
```

---

# 58. Mixed finding

`mixed` là một kết quả hợp lệ.

Không cố ép:

```text
positive
```

hoặc:

```text
negative
```

nếu evidence cân bằng.

---

# 59. Conflict resolver

Khi evidence conflict, thứ tự xem xét:

```text
1. Priority
2. Structural relevance
3. Significance
4. Confidence
5. Dependency
6. Damage
7. Rescue
8. Timing activation
```

Không dùng:

```text
count positive vs count negative
```

---

# 60. Evidence count rule

5 evidence nhỏ không nhất thiết thắng 1 evidence structural major.

Ví dụ:

```text
5 x P4 positive
```

không được tự động vượt:

```text
1 x P0 negative
```

---

# 61. Structural cap

Một domain không được lên mức rất cao chỉ vì nhiều secondary evidence tốt nếu core evidence yếu.

Concept:

```text
secondary evidence cannot manufacture structural strength
```

---

# 62. Secondary cap

Nếu domain chỉ có evidence từ:

```text
Shen Sha
Cung Phi
Nạp âm
```

thì grade tối đa phải bị cap.

Mức cap cụ thể sẽ được chốt ở Score Engine.

---

# 63. Shen Sha policy

Shen Sha chỉ có thể:

```text
support
qualify
amplify slightly
```

Không được:

```text
hard veto
hard guarantee
```

---

# 64. Feng Shui / Cung Phi policy

Cung Phi có thể dùng cho:

```text
living compatibility reference
household orientation context
```

Không phải core marriage decision.

---

# 65. Na Yin policy

Nạp âm chỉ là:

```text
reference evidence
```

Không được dùng:

```text
nạp âm sinh nhau = hợp
nạp âm khắc nhau = không hợp
```

---

# 66. Decision Profile output

Decision Profile không trả customer prose.

Output là:

```text
resolved evidence
findings
priority
domain state
cross-domain state
```

---

# 67. Domain state

Khuyến nghị mỗi domain có:

```ts
interface MarriageDomainState {
  domain: MarriageDomain;

  structural_state:
    | "supportive"
    | "balanced"
    | "mixed"
    | "pressured"
    | "insufficient";

  confidence: number;

  dominant_finding_ids: string[];

  supporting_finding_ids: string[];

  limiting_finding_ids: string[];
}
```

---

# 68. Structural state khác Grade

Ví dụ:

```text
structural_state = mixed
```

nhưng score sau Score Engine có thể:

```text
grade = B
```

Hai khái niệm khác nhau.

---

# 69. Finding threshold

Không phải evidence nào cũng tạo customer-relevant finding.

Một evidence nhỏ có thể chỉ:

```text
support existing finding
```

Không cần sinh finding riêng.

---

# 70. Finding creation rules

Tạo finding khi:

```text
significance đủ
hoặc
nhiều evidence cùng chain
hoặc
có cross-domain relevance
hoặc
có timing significance
```

---

# 71. Evidence chain

Ví dụ:

```text
A useful god needs Fire
B provides favorable Fire
B does not strongly activate A's unfavorable structure
```

có thể hình thành một chain:

```text
useful-god support chain
```

mạnh hơn raw presence.

---

# 72. Negative chain

Ví dụ:

```text
branch clash
+
role pressure
+
communication mismatch
```

có thể tạo:

```text
relationship pressure chain
```

---

# 73. Chain ID

Có thể dùng:

```text
marriage.chain.element_support.v1
marriage.chain.relationship_pressure.v1
```

nếu implementation cần.

---

# 74. Hard veto policy

TV-01 V1:

> Không có hard veto hôn nhân.

Không có rule:

```text
X xuất hiện
→ không nên kết hôn
```

Mọi kết luận đều là:

```text
support
risk
condition
pressure
```

---

# 75. Hard guarantee policy

Tương tự không có:

```text
X xuất hiện
→ hôn nhân chắc chắn hạnh phúc
```

---

# 76. Overall Decision philosophy

Overall không chỉ hỏi:

```text
hợp bao nhiêu %
```

Mà phải trả:

```text
Nền tảng
Điểm bổ trợ
Điểm xung đột
Điều kiện
Timing
```

---

# 77. Overall primary components

Overall V1 nên xem xét:

```text
Structural Compatibility
Relational Dynamics
Life-domain Compatibility
Timing Context
Confidence
```

Score weights sẽ nằm trong file 04.

---

# 78. Structural Compatibility

Derived chủ yếu từ:

```text
D1
D2
D3
```

Đây là phần có trọng lượng lớn nhất.

---

# 79. Relational Dynamics

Derived chủ yếu từ:

```text
D4
```

cùng relevant findings từ D2/D3.

---

# 80. Life-domain Compatibility

Derived từ:

```text
D5 Finance
D6 Family
D7 Children
```

---

# 81. Timing Context

Derived từ:

```text
D8
```

Timing không nên có quyền đảo ngược hoàn toàn natal compatibility.

---

# 82. Timing cap

Ví dụ:

```text
natal = strong
current timing = sensitive
```

thì không đổi natal thành:

```text
poor
```

Mà presentation nên nói:

```text
nền tảng tốt nhưng giai đoạn hiện tại cần điều chỉnh
```

---

# 83. Confidence behavior

Confidence thấp có thể:

- giảm strength of wording;
- hạ confidence label;
- limit score precision;
- suppress fragile findings.

Confidence thấp không tự biến positive thành negative.

---

# 84. Low confidence finding

Nếu confidence dưới threshold:

finding có thể:

```text
remain internal
```

hoặc:

```text
publish as reference-only
```

Threshold cụ thể sẽ chốt tại Validation / Score.

---

# 85. Missing hour profile behavior

Nếu thiếu giờ:

- không chạy hour-dependent rules;
- không tạo evidence giả;
- không penalize compatibility chỉ vì missing data;
- giảm confidence;
- domain nào bị thiếu dữ liệu thì mark limitation.

---

# 86. Asymmetric data quality

Nếu A đủ giờ nhưng B thiếu giờ:

```text
A_TO_B evidence
B_TO_A evidence
```

có thể có confidence khác nhau.

Không bắt buộc confidence hai chiều bằng nhau.

---

# 87. Profile rule object

Khuyến nghị concept:

```ts
interface MarriageDecisionRule {
  rule_id: string;

  domain: MarriageDomain;

  priority: FindingPriority;

  evidence_types: MarriageEvidenceType[];

  dependencies?: string[];

  conditions: RuleCondition[];

  output: RuleOutput;

  confidence_policy: ConfidencePolicy;
}
```

---

# 88. RuleCondition

Có thể biểu diễn:

```text
source path
operator
threshold
context
```

nhưng không định nghĩa DSL cụ thể ở file này.

---

# 89. RuleOutput

Có thể tạo:

```text
evidence
finding candidate
modifier
cross-domain reference
```

---

# 90. Decision Profile không chứa Narrative

Không được để:

```text
rule.output.text = "Hai bạn rất hợp..."
```

Rule chỉ chứa semantic output.

---

# 91. Semantic keys

Ví dụ:

```text
finding.marriage.element.mutual_support
finding.marriage.finance.resource_competition
finding.marriage.interaction.communication_friction
```

Narrative catalog sẽ map sau.

---

# 92. Decision Profile immutable inputs

Profile chỉ đọc:

```text
canonical snapshots
relationship context
evidence
```

Không được mutate:

```text
canonical A
canonical B
```

---

# 93. Decision Profile version bundle

Decision Result phải lưu:

```text
decision_profile_version = marriage.profile.v1
```

Nếu rule catalog version riêng:

```text
rule_catalog_version = marriage.rules.v1
```

---

# 94. Profile configuration

V1 nên hạn chế config runtime.

Không cho UI tùy tiện thay:

```text
weight
priority
rule
```

Profile phải do hệ thống kiểm soát.

---

# 95. Expert configuration

Sau này có thể có:

```text
expert profile
traditional profile
modern profile
```

nhưng không thuộc V1.

V1 chỉ một canonical profile.

---

# 96. No user-selectable scoring philosophy

Customer không được chọn:

```text
ưu tiên nạp âm
ưu tiên cung phi
ưu tiên thần sát
```

vì sẽ phá consistency.

---

# 97. Explainability requirement

Mỗi domain decision phải giải thích được:

```text
Why this domain is strong/weak?
Which evidence dominates?
Which evidence conflicts?
What was rescued?
What was activated?
```

---

# 98. Audit record

Decision audit concept:

```ts
interface MarriageDecisionAudit {
  profile_version: string;

  evaluated_rule_ids: string[];

  activated_rule_ids: string[];

  suppressed_rule_ids?: string[];

  resolution_steps?: DecisionResolutionStep[];
}
```

Không cần expose cho customer.

---

# 99. Suppressed evidence

Evidence có thể bị:

```text
suppressed from final finding
```

nhưng không được xóa khỏi audit nếu đã hợp lệ.

---

# 100. Suppression reasons

Ví dụ:

```text
low significance
low confidence
dominated by higher-priority evidence
duplicate semantic evidence
fully rescued
out of domain scope
```

---

# 101. Duplicate evidence handling

Nếu cùng một fact được phát hiện từ nhiều rule tương đương:

không tạo nhiều finding lặp.

Dùng:

```text
semantic deduplication
```

---

# 102. Finding deduplication

Ví dụ 3 evidence đều chỉ về:

```text
financial resource competition
```

nên ưu tiên:

```text
1 finding
+
3 supporting evidence
```

thay vì 3 câu lặp.

---

# 103. Narrative repetition prevention starts here

Muốn Narrative sau này không lặp, Decision Profile phải tránh sinh findings trùng nghĩa.

Không đẩy toàn bộ trách nhiệm cho Composer.

---

# 104. Domain ordering for presentation

Canonical recommended order:

```text
1. Overall
2. Five Elements
3. Stem / Branch
4. Ten Gods
5. Interaction
6. Finance
7. Family
8. Children
9. Timing
```

UI có thể rearrange presentation nhưng không đổi semantic dependency.

---

# 105. Primary vs secondary source table

| Source | Role | Can dominate? |
|---|---|---|
| Useful God / Hỷ / Kỵ | Primary | Yes |
| Strength / Pattern | Primary | Yes |
| Five Elements | Primary with context | Yes |
| Stem/Branch | Primary interaction | Yes |
| Ten Gods | Primary relational | Yes |
| Luck | Activation | Limited |
| Shen Sha | Secondary | No |
| Cung Phi | Secondary | No |
| Nạp âm | Secondary | No |

---

# 106. Decision anti-patterns

Cấm:

```text
Tuổi tam hợp → marriage good
```

```text
Tuổi xung → marriage bad
```

```text
Nạp âm sinh nhau → +20
```

```text
Cung Phi Sinh Khí → pass
```

```text
Cô Thần → divorce
```

```text
Đào Hoa → infidelity
```

---

# 107. Correct pattern

Đúng:

```text
Canonical structure
+
Relational interaction
+
Domain relevance
+
Context
+
Timing
+
Confidence
→ Finding
```

---

# 108. Example A — Positive support

Giả định:

```text
A useful god = Fire
B has structurally favorable Fire
B Fire does not strongly activate A's unfavorable configuration
```

Decision:

```text
evidence:
useful_god_support
```

có thể tạo:

```text
finding:
element_support
```

Không tự tạo:

```text
marriage = excellent
```

---

# 109. Example B — Conflict with rescue

Giả định:

```text
Day branches clash
```

nhưng:

```text
strong useful-god support
role complement
no repeated clash
```

Decision có thể:

```text
finding = relational_tension
severity = moderate
condition = manageable
```

Không:

```text
bad marriage
```

---

# 110. Example C — Secondary conflict

Giả định:

```text
Cung Phi unfavorable
```

nhưng structural compatibility tốt.

Decision:

```text
feng_shui_reference = negative minor evidence
```

Không được hạ overall mạnh.

---

# 111. Example D — Strong secondary but weak core

Giả định:

```text
multiple favorable Shen Sha
Cung Phi favorable
Nạp âm favorable
```

nhưng:

```text
core interaction mixed
```

Overall không được nâng thành A chỉ vì secondary signals.

---

# 112. Domain score input preparation

Decision Profile phải xuất một normalized state cho Score Engine.

Ví dụ:

```ts
interface MarriageScoreInput {
  domain: MarriageDomain;

  state: MarriageDomainState;

  dominant_findings: string[];

  positive_mass: number;

  negative_mass: number;

  mixed_mass: number;

  confidence: number;

  caps?: string[];

  modifiers?: string[];
}
```

Chi tiết numeric logic ở file 04.

---

# 113. No score constants here

File này không chốt:

```text
D1 = 25%
D2 = 20%
...
```

Đó là trách nhiệm của `04_SCORE_ENGINE.md`.

---

# 114. Score Engine receives meaning, not raw facts

Score Engine nên nhận:

```text
resolved decision state
```

không trực tiếp tự đọc:

```text
pillars
```

để tránh duplicate logic.

---

# 115. Decision Profile freeze criteria

File `03_DECISION_PROFILE.md` chỉ được FREEZE khi Product Owner xác nhận:

- [ ] Có 8 domain rõ ràng.
- [ ] Có Tier 1/2/3.
- [ ] Core structure ưu tiên hơn secondary evidence.
- [ ] Có directionality A→B/B→A.
- [ ] Có dependency.
- [ ] Có damage/rescue.
- [ ] Có mixed finding.
- [ ] Không cộng số lượng evidence.
- [ ] Không hard veto.
- [ ] Không hard guarantee.
- [ ] Shen Sha là secondary.
- [ ] Cung Phi là secondary.
- [ ] Nạp âm là secondary.
- [ ] Luck là activation.
- [ ] Missing hour không bị phạt compatibility.
- [ ] Có cross-domain rules.
- [ ] Có deduplication.
- [ ] Findings phải trace về evidence.
- [ ] Profile không chứa customer prose.
- [ ] Profile versioned.
- [ ] Score logic chưa bị hard-code vào Decision Profile.

---

# 116. Core Decision Rule

> **Không đánh giá hôn nhân bằng một dấu hiệu đơn lẻ.**

Kết luận phải được xây từ:

```text
structure
+
interaction
+
context
+
dependency
+
timing
+
confidence
```

---

# 117. Second Core Rule

> **Secondary evidence không được quyền lật ngược kết luận structural nếu không có primary evidence hỗ trợ.**

---

# 118. Third Core Rule

> **Xung không đồng nghĩa xấu tuyệt đối; hợp không đồng nghĩa tốt tuyệt đối.**

Mọi interaction phải được xét theo cấu trúc thực tế.

---

# 119. Fourth Core Rule

> **Timing activates — it does not rewrite natal truth.**

---

# 120. Fifth Core Rule

> **No raw evidence count → no naïve compatibility scoring.**

---

# 121. Architectural contract

```text
Canonical A/B
    ↓
Evidence
    ↓
Decision Profile
    ↓
Resolved Domain State
    ↓
Findings
    ↓
Score Input
```

Không được:

```text
Canonical A/B
    ↓
Score Engine
```

bỏ qua Decision Profile.

---

# 122. Status

**TV-01-03 STATUS: DRAFT**

Bước tiếp theo sau khi Product Owner duyệt và FREEZE:

`TV-01 / 04_SCORE_ENGINE.md`

Không implementation scoring trước khi Decision Profile được chốt.
```

File này là phần quan trọng nhất về mặt **phương pháp luận** của TV-01, vì nó chốt rằng hệ thống hôn nhân không vận hành theo kiểu “tam hợp cộng điểm, xung trừ điểm”, mà theo cấu trúc **evidence → dependency → damage/rescue → finding → score input**. Sang `04_SCORE_ENGINE.md`, chúng ta mới quyết định cụ thể **8 domain sẽ được quy đổi ra 0–100 thế nào, trọng số bao nhiêu, có cap/floor ra sao và Grade A–E được xác định như thế nào**.