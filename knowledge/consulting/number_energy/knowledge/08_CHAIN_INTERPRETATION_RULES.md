Được. `08_CHAIN_INTERPRETATION_RULES.md` là file nối tất cả các lớp trước lại với nhau để engine đọc **một dãy số dài như một dòng chuyển trạng thái**, thay vì chỉ nhìn từng cặp hoặc từng bộ ba rời rạc.

```markdown
# 08_CHAIN_INTERPRETATION_RULES.md

# BTE NUMBER ENERGY — CHAIN INTERPRETATION RULES

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Chain Interpretation Rules  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** CORE KNOWLEDGE  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`

**Depends On:**
- `01_BAGUA_DIGIT_MAPPING.md`
- `02_EIGHT_ENERGY_CATALOG.md`
- `03_PAIR_STRENGTH_MATRIX.md`
- `04_DIRECTED_INTERACTION_MATRIX.md`
- `05_ZERO_FIVE_MODIFIERS.md`
- `06_POSITION_AND_TAIL_RULES.md`
- `07_CONTROL_REMEDY_RULES.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa cách đọc
toàn bộ dãy số như một chuỗi năng lượng liên tục.

Canonical principle:

> Hai số thành Cục.  
> Ba số thành Tượng.  
> Nhiều Tượng nối nhau thành Thế.  
> Toàn dãy hình thành Cấu Trúc.

Chain Engine chịu trách nhiệm:

PAIR
↓
ENERGY
↓
DIRECTED INTERACTION
↓
MODIFIED INTERACTION
↓
CONTROL / REMEDY
↓
POSITIONAL CHAIN
↓
DOMAIN FLOW
↓
WHOLE-SEQUENCE SYNTHESIS

---

# 2. CHAIN IS NOT A BAG OF PAIRS

Forbidden model:

```text
number
→ list of pairs
→ count good
→ count bad
→ final score
```

Canonical model:

```text
number
→ ordered pairs
→ ordered energies
→ ordered interactions
→ ordered states
→ chain
→ terminal convergence
```

Thứ tự không được bỏ.

---

# 3. ADJACENT-PAIR PRINCIPLE

Với dãy:

```text
A B C D E
```

engine tạo:

```text
AB
BC
CD
DE
```

Mỗi pair phải có:

- Energy;
- Strength;
- modifier state nếu có;
- position.

Sau đó tạo interactions:

```text
Energy(AB) → Energy(BC)

Energy(BC) → Energy(CD)

Energy(CD) → Energy(DE)
```

---

# 4. CHAIN OBJECT

Recommended:

```text
EnergyChain {
    raw_input
    normalized_digits

    pair_nodes
    interaction_edges

    modifier_events
    control_events

    head_state
    middle_states
    rear_state
    terminal_state

    dominant_energy
    secondary_energy

    domain_flows

    balance_state
    convergence_state
}
```

---

# 5. NODE MODEL

Mỗi pair tạo một Node.

Recommended:

```text
EnergyNode {
    pair
    start_index
    end_index

    energy_id
    strength_tier
    strength_weight

    modifier_state

    zone
    distance_to_tail

    repetition_group

    active_role
}
```

---

# 6. EDGE MODEL

Mỗi interaction tạo một Edge.

Recommended:

```text
EnergyEdge {
    source_node
    target_node

    interaction_id
    directed_meaning

    control_rule
    control_state

    domain_tags

    position_relevance
}
```

---

# 7. CHAIN PRESERVES OVERLAP

Ví dụ:

```text
813
```

Pairs:

```text
81
13
```

Shared digit:

```text
1
```

Đây không phải hai cặp độc lập ngẫu nhiên.

Canonical:

```text
81 → 13
```

là một continuous triple structure.

---

# 8. TRIPLE = MINIMUM DIRECTED UNIT

Canonical:

```text
ABC
```

tạo:

```text
AB → BC
```

Đây là đơn vị nhỏ nhất
để luận Directed Interaction.

Ví dụ:

```text
813
```

=

```text
WU_GUI → TIAN_Y
```

---

# 9. FOUR DIGITS CREATE TWO INTERACTIONS

Ví dụ:

```text
8139
```

Pairs:

```text
81 = WU_GUI
13 = TIAN_Y
39 = SHENG_QI
```

Interactions:

```text
WU_GUI → TIAN_Y
TIAN_Y → SHENG_QI
```

Không được chỉ chọn interaction mạnh nhất
rồi bỏ interaction còn lại.

---

# 10. FIVE DIGITS CREATE THREE INTERACTIONS

Ví dụ:

```text
81396
```

Pairs:

```text
81 = WU_GUI
13 = TIAN_Y
39 = SHENG_QI
96 = JUE_MING
```

Chain:

```text
WU_GUI
→ TIAN_Y
→ SHENG_QI
→ JUE_MING
```

Narrative phải hiểu cả quá trình.

---

# 11. CHAIN AS STATE TRANSITION

Canonical abstraction:

```text
STATE_1
→ STATE_2
→ STATE_3
→ ...
→ TERMINAL_STATE
```

Mỗi Energy có semantic role.

Ví dụ:

```text
WU_GUI
→ TIAN_Y
→ YAN_NIAN
```

có thể đọc:

```text
idea / volatility
→ resource
→ structure / profession
```

Tức:

```text
ý tưởng
→ tạo thành quả
→ đưa thành quả vào khuôn khổ nghề nghiệp
```

---

# 12. SOURCE / CORE / DESTINATION

Trong chuỗi ba Energy:

```text
A → B → C
```

B có thể đóng vai:

```text
RESULT_OF_A
+
SOURCE_FOR_C
```

Ví dụ:

```text
HUO_HAI → TIAN_Y → JUE_MING
```

Thiên Y là:

```text
result of communication
```

và đồng thời:

```text
resource sent into investment
```

Do đó narrative:

> Khả năng giao tiếp tạo ra tài nguyên,
> sau đó tài nguyên được đưa vào hoạt động đầu tư
> hoặc hành động có mức độ rủi ro cao hơn.

Đây là Chain semantics.

---

# 13. DO NOT RESET AT EACH INTERACTION

Forbidden:

```text
A → B
analyze
STOP

B → C
analyze separately
STOP
```

Correct:

```text
A → B → C
```

phải được tổng hợp thành một dòng.

---

# 14. INTERACTION COMPOSITION

Nếu:

```text
A → B
```

có meaning:

```text
X → Y
```

và:

```text
B → C
```

có meaning:

```text
Y → Z
```

thì Chain Engine có thể compose:

```text
X → Y → Z
```

nhưng không được tự sáng tạo semantic
không có trong canonical knowledge.

---

# 15. CHAIN LENGTH

Không có fixed maximum
ở Knowledge Layer.

Engine phải hỗ trợ:

- short chains;
- medium chains;
- full phone number chains.

Phone:

```text
long chain
```

Plate:

```text
short chain
```

---

# 16. CHAIN ROLE TYPES

Recommended:

```text
ORIGIN
PROCESS
BRIDGE
RESOURCE
ACTION
CONTROL
RESULT
TERMINAL
```

Một node có thể mang nhiều role.

Ví dụ:

Thiên Y có thể là:

```text
RESOURCE
RESULT
BRIDGE
```

tùy vị trí.

---

# 17. CHAIN HEAD

Head Energy cho biết:

- trạng thái khởi phát;
- nguồn đầu tiên;
- cách chain bắt đầu.

Không được coi Head là final outcome.

---

# 18. CHAIN MIDDLE

Middle là vùng:

```text
PROCESS
TRANSFORMATION
FUNCTIONAL_USE
CONTROL
```

Đây là nơi đặc biệt quan trọng
để nhận diện:

```text
Hung làm dụng
```

---

# 19. CHAIN TAIL

Tail cho biết:

```text
CONVERGENCE
RESULT
TERMINAL STATE
```

Nhưng Tail phải được hiểu
trong bối cảnh đường đi trước đó.

---

# 20. SAME TERMINAL, DIFFERENT PATH

Hai chain:

```text
HUO_HAI → TIAN_Y
```

và:

```text
WU_GUI → TIAN_Y
```

cùng terminal:

```text
TIAN_Y
```

nhưng nguồn tài khác nhau:

```text
HUO_HAI → TIAN_Y
= communication → wealth
```

```text
WU_GUI → TIAN_Y
= intelligence → wealth
```

Do đó:

```text
same tail
!=
same narrative
```

---

# 21. SAME START, DIFFERENT TERMINAL

Ví dụ:

```text
WU_GUI → TIAN_Y
```

khác:

```text
WU_GUI → JUE_MING
```

Cùng source Ngũ Quỷ.

Nhưng:

- một chain hướng về tài nguyên;
- một chain hướng về hành động/rủi ro.

---

# 22. STRONGEST PATH ≠ STRONGEST PAIR

Không được chọn pair mạnh nhất
và coi đó là toàn bộ dãy.

Dominant Path phải xét:

- cường độ;
- continuity;
- position;
- repetition;
- terminal relevance;
- control;
- domain coherence.

---

# 23. CONTINUOUS SAME-ENERGY CHAIN

Ví dụ:

```text
131
```

gives:

```text
TIAN_Y → TIAN_Y
```

Đây là:

```text
REINFORCED_TIAN_Y
```

Ví dụ:

```text
181
```

=

```text
WU_GUI → WU_GUI
```

=

```text
REINFORCED_WU_GUI
```

Repeated chain phải được ghi nhận
như một state amplification.

---

# 24. ENERGY RUN

Nếu có nhiều node liên tiếp cùng Energy:

```text
E → E → E
```

tạo:

```text
EnergyRun
```

Recommended:

```text
EnergyRun {
    energy
    count
    total_strength
    start_index
    end_index
    zone
}
```

---

# 25. REPEATED AUSPICIOUS ENERGY

Không mặc nhiên:

```text
more auspicious repetition = better
```

Example:

```text
TIAN_Y → TIAN_Y → TIAN_Y
```

có thể:

- tăng tài/tình;
- nhưng excessive relationship/resource concentration
  cũng phải xét.

---

# 26. REPEATED CHALLENGING ENERGY

Ví dụ:

```text
WU_GUI → WU_GUI
```

hoặc:

```text
JUE_MING → JUE_MING
```

có thể làm:

```text
volatility ↑
risk ↑
```

Nếu gần tail,
prominence càng cao.

---

# 27. PHUC_VI IN CHAIN

Phục Vị là operator-like Energy.

Canonical:

```text
A → FU_WEI
```

=

```text
EXTEND(A)
```

Nếu chain:

```text
A → FU_WEI → B
```

phải hiểu:

```text
A persists
then transitions to B
```

Không được bỏ A.

---

# 28. PHUC_VI BRIDGE

Ví dụ:

```text
WU_GUI
→ FU_WEI
→ SHENG_QI
```

phải đọc:

1. Ngũ Quỷ;
2. Ngũ Quỷ được kéo dài;
3. sau đó mới chuyển sang Sinh Khí.

Không được rút gọn:

```text
WU_GUI → SHENG_QI
```

---

# 29. ZERO IN CHAIN

0 có thể tạo:

```text
HIDDEN SEGMENT
```

Ví dụ:

```text
1-0-3
```

Underlying:

```text
TIAN_Y_HIDDEN
```

Trong chain,
node phải mang:

```text
energy = TIAN_Y
state = HIDDEN
```

Không được drop node.

---

# 30. FIVE IN CHAIN

5 tạo:

```text
AMPLIFIED SEGMENT
```

Ví dụ:

```text
1-5-3
```

=

```text
TIAN_Y_AMPLIFIED
```

Node vẫn là Thiên Y,
nhưng state khác.

---

# 31. MODIFIER CHAIN PRIORITY

Modifier được apply
trước whole-chain synthesis.

Canonical order:

```text
raw pair
→ underlying energy
→ strength
→ modifier
→ interaction
→ position
→ remedy
→ chain synthesis
```

---

# 32. CONTROL IN CHAIN

Control là edge/event.

Ví dụ:

```text
WU_GUI → SHENG_QI
```

gắn:

```text
CTRL-WG-SQ
```

Nhưng chain có thể tiếp tục:

```text
WU_GUI
→ SHENG_QI
→ JUE_MING
```

Do đó final status:

```text
local control
+
challenging terminal
```

---

# 33. LOCAL CONTROL

```text
LOCAL_CONTROL
```

= Hung cụ thể được điều tiết
ở một đoạn chain.

Không có nghĩa toàn chain cân bằng.

---

# 34. GLOBAL CONTROL

Global control chỉ có khi:

- major Hung được kiểm soát;
- không tái xuất hiện mạnh ở phần sau;
- terminal không còn unresolved challenge đáng kể;
- modifiers không làm yếu control.

---

# 35. REAPPEARING ENERGY

Example:

```text
WU_GUI
→ SHENG_QI
→ WU_GUI
```

Interpretation:

```text
control occurs
but volatility returns
```

Terminal:

```text
WU_GUI
```

Không được gọi là balanced.

---

# 36. CONTROL CHAIN

Example:

```text
WU_GUI
→ SHENG_QI
→ TIAN_Y
→ YAN_NIAN
```

Canonical:

```text
volatility
→ support
→ resource
→ structure
```

Có thể là strong controlled chain.

---

# 37. WRONG-ORDER CONTROL CHAIN

Example:

```text
WU_GUI
→ TIAN_Y
→ SHENG_QI
→ YAN_NIAN
```

không được match
strong Ngũ Quỷ remedy chain.

Directed semantics vẫn được luận riêng.

---

# 38. CHAIN DOMAIN FLOW

Chain Engine phải có khả năng
map sequence sang domain flow.

Ví dụ:

```text
HUO_HAI
→ TIAN_Y
→ JUE_MING
```

Domain:

```text
COMMUNICATION
→ WEALTH
→ INVESTMENT
```

---

# 39. CAREER CHAIN

Diên Niên là Career Core.

Canonical:

```text
X → YAN_NIAN
```

X thường giúp xác định:

```text
career_skill_source
```

Ví dụ:

```text
HUO_HAI → YAN_NIAN
```

=

```text
communication → career
```

---

# 40. CAREER AFTER-STATE

Nếu:

```text
X → YAN_NIAN → Y
```

Y giúp xác định:

```text
work_after_state
```

Ví dụ:

```text
HUO_HAI
→ YAN_NIAN
→ SHENG_QI
```

có thể đọc:

```text
communication skill
→ profession
→ supportive / positive work state
```

---

# 41. WEALTH CHAIN

Thiên Y là Wealth Core.

Canonical:

```text
X → TIAN_Y
```

X cho biết:

```text
wealth_source
```

---

# 42. WEALTH DESTINATION

```text
X → TIAN_Y → Y
```

Y cho biết:

```text
wealth_destination
```

Ví dụ:

```text
HUO_HAI
→ TIAN_Y
→ JUE_MING
```

=

```text
communication earns money
→ money goes into investment
```

---

# 43. RELATIONSHIP CHAIN

Các Energy nổi bật:

```text
TIAN_Y
LIU_SHA
SHENG_QI
FU_WEI
```

nhưng phải đọc flow.

Ví dụ:

```text
SHENG_QI → LIU_SHA
```

có thể:

```text
friendship/social connection
→ emotional attachment
```

---

# 44. RELATIONSHIP + FU_WEI

Ví dụ:

```text
LIU_SHA
→ FU_WEI
```

=

```text
emotion / attachment
→ prolonged
```

Nếu ở tail:

```text
relationship state becomes persistent
```

---

# 45. LEARNING CHAIN

Knowledge Source gợi ý:

```text
SHENG_QI
→ YAN_NIAN
→ SHENG_QI
```

có thể biểu thị:

```text
support / motivation
→ method / discipline
→ positive state
```

Đây là learning-context pattern.

---

# 46. INVESTMENT CHAIN

Tuyệt Mệnh là Action/Risk Core.

Examples:

```text
JUE_MING → TIAN_Y
```

=

```text
investment/action
→ wealth
```

```text
TIAN_Y → JUE_MING
```

=

```text
resource
→ investment
```

```text
JUE_MING → WU_GUI
```

=

```text
risk
→ volatility
```

---

# 47. CHAIN CLASSIFICATION

Recommended V1:

```text
SUPPORTIVE_FLOW
RESOURCE_FLOW
CAREER_FLOW
RELATIONSHIP_FLOW
INVESTMENT_FLOW
VOLATILE_FLOW
CONTROLLED_FLOW
MIXED_FLOW
```

Một chain có thể có nhiều tags.

---

# 48. DOMINANT FLOW

Dominant Flow xác định từ:

- số interaction thuộc domain;
- strength;
- position;
- continuity;
- terminal relevance.

Không chỉ đếm Energy.

---

# 49. FLOW COHERENCE

Chain có coherence cao khi:

```text
A → B → C
```

tạo một logic domain rõ.

Ví dụ:

```text
HUO_HAI
→ TIAN_Y
→ YAN_NIAN
```

có thể:

```text
communication
→ resource
→ profession
```

Logic khá rõ.

---

# 50. LOW-COHERENCE CHAIN

Nếu chain thay đổi liên tục:

```text
WU_GUI
→ LIU_SHA
→ HUO_HAI
→ JUE_MING
```

có thể được đánh dấu:

```text
LOW_COHERENCE
HIGH_VARIABILITY
```

Không có nghĩa chắc chắn xấu,
nhưng narrative phải nói
cấu trúc thiếu ổn định.

---

# 51. CHAIN VOLATILITY

Recommended internal feature:

```text
energy_transition_count
```

và:

```text
challenging_transition_count
```

Có thể hỗ trợ
structural volatility detection.

Không hiển thị raw metric cho khách.

---

# 52. CHAIN BALANCE

Không được dùng:

```text
auspicious_count - challenging_count
```

Canonical balance phải xét:

```text
dominant flow
terminal state
control coverage
modifier state
repetition
position
```

---

# 53. CHAIN CONVERGENCE

Recommended:

```text
FAVORABLE_CONVERGENCE
BALANCED_CONVERGENCE
MIXED_CONVERGENCE
CHALLENGING_CONVERGENCE
HIDDEN_CONVERGENCE
AMPLIFIED_CONVERGENCE
```

Dựa trên Terminal State
và chain trước đó.

---

# 54. POSITIVE PROCESS, CHALLENGING TERMINAL

Example:

```text
SHENG_QI
→ TIAN_Y
→ WU_GUI
```

Meaning:

```text
support
→ resource
→ volatility
```

Narrative:

> Dãy có khả năng tạo cơ hội và tài nguyên,
> nhưng trạng thái cuối vẫn có tính biến động,
> vì vậy khả năng giữ ổn định cần được chú ý.

---

# 55. CHALLENGING PROCESS, POSITIVE TERMINAL

Example:

```text
HUO_HAI
→ TIAN_Y
```

Meaning:

```text
communication
→ resource
```

Narrative:

> Một trường có tính thử thách được sử dụng
> như kỹ năng để tạo ra kết quả thuận hơn.

---

# 56. POSITIVE START, CHALLENGING MIDDLE, POSITIVE TAIL

Example:

```text
SHENG_QI
→ JUE_MING
→ TIAN_Y
```

Possible:

```text
opportunity
→ action / investment
→ result / wealth
```

Đây là cấu trúc:

```text
AUSPICIOUS
→ FUNCTIONAL CHALLENGE
→ AUSPICIOUS
```

phù hợp triết lý:

```text
Cát làm chủ
Hung làm dụng
```

nếu strength và remedy phù hợp.

---

# 57. ALL-AUSPICIOUS CHAIN

Không mặc nhiên tối ưu.

Example:

```text
SHENG_QI
→ TIAN_Y
→ YAN_NIAN
```

có thể rất thuận,
nhưng vẫn phải xét:

- cân bằng;
- mục tiêu;
- repetition;
- position.

---

# 58. ALL-CHALLENGING CHAIN

Example:

```text
HUO_HAI
→ WU_GUI
→ LIU_SHA
→ JUE_MING
```

có thể là:

```text
HIGH_CHALLENGE_DENSITY
```

Nhưng vẫn phải phân tích
functional skills trước khi kết luận.

Không được chỉ nói:

> đại hung.

---

# 59. CHAIN SEGMENTATION

Một dãy dài có thể chia
thành các segment theo domain.

Ví dụ:

```text
A → B → C → D → E
```

Segments:

```text
A → B → C
C → D → E
```

nếu domain flow thay đổi rõ.

Không được segmentation tùy tiện.

---

# 60. SEGMENT BOUNDARY

Possible boundaries:

- strong modifier;
- change of dominant domain;
- strong control event;
- strong repetition;
- major terminal transition.

---

# 61. PRIMARY SEGMENT

Segment có prominence cao nhất
theo:

```text
strength
× position
× continuity
× terminal relevance
```

có thể là Primary Segment.

Engineering only.

---

# 62. SECONDARY SEGMENT

Segment kế tiếp
có thể dùng cho supporting narrative.

---

# 63. CUSTOMER NARRATIVE ORDER

Recommended:

1. Tổng quan chain.
2. Dominant flow.
3. Strength.
4. Important interaction.
5. Control/remedy.
6. Terminal state.
7. Domain interpretation.
8. Recommendation.

---

# 64. DO NOT DUMP ALL PAIRS

Customer Mode không được hiển thị:

```text
14 = Sinh Khí
13 = Thiên Y
19 = Diên Niên
...
```

thành danh sách dài
nếu không có narrative tổng hợp.

Có thể có expandable
"Cơ sở đánh giá".

---

# 65. EXPERT MODE

Expert Mode có thể hiển thị:

```text
Chain:
WG(T1)
→ TY(T1)
→ SQ(T3)
→ JM(T2)
→ TY(T2)

Controls:
JM → TY

Terminal:
TY

Modifiers:
None
```

---

# 66. WHOLE-SEQUENCE SUMMARY OBJECT

Recommended:

```text
ChainSummary {
    dominant_energy
    secondary_energy

    dominant_flow
    secondary_flow

    strongest_interaction
    strongest_challenge
    strongest_support

    control_summary

    terminal_state

    convergence_state

    balance_state

    key_strengths
    key_risks
}
```

---

# 67. DOMINANT ENERGY CALCULATION

Dominant Energy must consider:

```text
pair_strength
position
repetition
continuity
modifier
domain relevance
```

Do not use raw count only.

---

# 68. DOMINANT INTERACTION

Dominant Interaction may differ
from Dominant Energy.

Example:

many Thiên Y,
but one strong:

```text
WU_GUI_T1 → TIAN_Y_T1
```

near tail

có thể là key interaction.

---

# 69. KEY STRENGTH

Key Strength phải mô tả
một functional advantage.

Examples:

```text
communication_to_wealth
creative_intelligence
social_to_career
support_network
```

Không chỉ:

```text
has_good_energy
```

---

# 70. KEY RISK

Key Risk phải mô tả
structural issue.

Examples:

```text
tail_volatility
hidden_resource
extended_emotional_state
high_risk_low_reward
```

Không chỉ:

```text
has_bad_energy
```

---

# 71. HIGH-RISK LOW-REWARD PATTERN

If:

```text
JUE_MING strong
→ TIAN_Y weak
```

possible:

```text
HIGH_RISK_LOW_REWARD
```

nhưng phải xét chain context.

---

# 72. LOW-RISK HIGH-REWARD PATTERN

If:

```text
JUE_MING weak
→ TIAN_Y strong
```

possible:

```text
LOWER_RISK_STRONGER_RESULT
```

Không phải financial guarantee.

---

# 73. CHAIN WITH ZERO

Example:

```text
WU_GUI
→ TIAN_Y_HIDDEN
→ YAN_NIAN
```

Interpretation:

- trí tuệ tạo tài nguyên;
- tài nguyên khó hiển;
- sau đó đi vào nghề nghiệp.

Không được bỏ hidden state.

---

# 74. CHAIN WITH FIVE

Example:

```text
HUO_HAI
→ TIAN_Y_AMPLIFIED
```

Interpretation:

- khẩu tài tạo tài;
- tài khí biểu hiện mạnh.

Nhưng nếu Họa Hại cũng amplified,
phải xét cả mặt tranh luận.

---

# 75. CHAIN WITH MULTIPLE MODIFIERS

Preserve modifier sequence.

Example:

```text
A0B5C
```

không simplify.

Need:

```text
modifier_events ordered
```

---

# 76. CHAIN WITH MULTIPLE CONTROLS

Example:

```text
WU_GUI
→ SHENG_QI
→ JUE_MING
→ TIAN_Y
```

Contains:

```text
CTRL-WG-SQ
CTRL-JM-TY
```

Chain may have multiple local control events.

---

# 77. CONTROL COVERAGE IN CHAIN

Global summary must track:

```text
controlled
partially_controlled
uncontrolled
```

challenging segments.

---

# 78. TAIL OVERRIDES? NO

Critical:

```text
TAIL_WEIGHT_HIGH
```

but:

```text
TAIL_DOES_NOT_ERASE_CHAIN
```

Narrative must describe:

```text
process + terminal
```

---

# 79. HEAD OVERRIDES? NO

Head establishes context,
not final result.

---

# 80. LONG PHONE NUMBER

For phone numbers:

- preserve full chain;
- do not analyze only last 4 digits;
- tail gets higher weight;
- middle flow remains important.

---

# 81. SHORT VEHICLE PLATE

For plates:

- fewer interactions;
- each interaction has higher importance;
- final pair and terminal interaction are prominent;
- whole sequence still required.

---

# 82. PHONE PROFILE

Chain domains:

```text
wealth
career
relationship
personality
social
investment
balance
```

---

# 83. VEHICLE PROFILE

Chain domains prioritize:

```text
stability
career
wealth
action
balance
terminal_state
```

Relationship narrative reduced.

---

# 84. CHAIN NARRATIVE STYLE

Avoid:

> Có Ngũ Quỷ, Thiên Y, Sinh Khí.

Preferred:

> Dãy số bắt đầu bằng một trường tư duy và biến động,
> sau đó chuyển sang khả năng tạo tài nguyên,
> rồi tiếp tục mở ra yếu tố quý nhân và trợ lực.
> Điều này cho thấy giá trị của dãy nằm ở việc
> biến ý tưởng thành cơ hội và kết quả thực tế.

---

# 85. CHAIN CONFLICT

Nếu chain có conflicting signals:

```text
supportive process
+
challenging terminal
```

Narrative phải nói cả hai.

Không ép về một kết luận cực đoan.

---

# 86. MIXED STRUCTURE

Recommended wording:

> Cấu trúc có cả lực hỗ trợ và lực biến động.
> Điểm mạnh nằm ở...
> Trong khi điểm cần lưu ý là...

---

# 87. CUSTOMER RESULT LEVELS

Recommended structural labels:

```text
STRONGLY_SUPPORTIVE
SUPPORTIVE
BALANCED
MIXED
CHALLENGING
HIGHLY_VOLATILE
```

Chỉ dùng sau whole-chain synthesis.

Không derive từ cát/hung count đơn giản.

---

# 88. RESULT LEVEL IS NOT FATE

Customer-facing:

> Đây là đánh giá cấu trúc dãy số
> theo Bát Cực Linh Số.

Không nói:

> số này quyết định vận mệnh.

---

# 89. NARRATIVE DEDUPLICATION

Nếu cùng một meaning
xuất hiện nhiều lần:

không lặp câu.

Example:

3 interaction cùng cho:

```text
wealth
```

Composer phải tổng hợp thành:

> Tài vận là một trong những chủ đề nổi bật.

Không viết ba đoạn giống nhau.

---

# 90. PRIORITY ORDER

Recommended narrative priority:

```text
1. terminal state
2. dominant flow
3. strong interaction near tail
4. control/remedy
5. dominant energy
6. important repetition
7. secondary domain
```

Không phải engine scoring order tuyệt đối.

---

# 91. CUSTOMER SUMMARY LENGTH

Hero summary:

```text
2–4 sentences
```

Detailed domain:

```text
1–3 paragraphs
```

Expert trace:

no strict narrative limit.

---

# 92. CHAIN ACCEPTANCE TEST — 813

Input:

```text
813
```

Expected:

```text
81 = WU_GUI T1
13 = TIAN_Y T1

chain:
WU_GUI → TIAN_Y

dominant flow:
CREATIVE_INTELLIGENCE → WEALTH

terminal:
TIAN_Y
```

---

# 93. CHAIN ACCEPTANCE TEST — 318

Expected:

```text
31 = TIAN_Y T1
18 = WU_GUI T1

chain:
TIAN_Y → WU_GUI

flow:
RESOURCE → VOLATILITY

terminal:
WU_GUI
```

Must differ from 813.

---

# 94. CHAIN ACCEPTANCE TEST — 219

Expected:

```text
21 = JUE_MING T1
19 = YAN_NIAN T1

chain:
JUE_MING → YAN_NIAN

flow:
ACTION → CAREER

control:
none from canonical 3-control mapping
```

---

# 95. CHAIN ACCEPTANCE TEST — 213

Expected:

```text
21 = JUE_MING T1
13 = TIAN_Y T1

flow:
ACTION / INVESTMENT → WEALTH

control:
CTRL-JM-TY
```

Both meanings preserved.

---

# 96. CHAIN ACCEPTANCE TEST — 103

Expected:

```text
underlying:
13 = TIAN_Y T1

modifier:
ZERO INTERPOSED

node:
TIAN_Y_HIDDEN

terminal:
TIAN_Y_HIDDEN
```

---

# 97. CHAIN ACCEPTANCE TEST — 153

Expected:

```text
13 = TIAN_Y T1

modifier:
FIVE INTERPOSED

node:
TIAN_Y_AMPLIFIED
```

---

# 98. CHAIN ACCEPTANCE TEST — 181

Expected:

```text
18 = WU_GUI T1
81 = WU_GUI T1

chain:
WU_GUI → WU_GUI

state:
REINFORCED_WU_GUI
```

---

# 99. CHAIN ACCEPTANCE TEST — 131

Expected:

```text
13 = TIAN_Y T1
31 = TIAN_Y T1

chain:
TIAN_Y → TIAN_Y

state:
REINFORCED_TIAN_Y
```

---

# 100. CHAIN ACCEPTANCE TEST — WG → SQ → WG

Expected:

```text
first WG locally controlled by SQ
later WG reappears
terminal remains WG
global control = false
```

---

# 101. CHAIN ACCEPTANCE TEST — STRONG REMEDY

Input energy chain:

```text
WU_GUI
→ SHENG_QI
→ TIAN_Y
→ YAN_NIAN
```

Expected:

```text
local control:
CTRL-WG-SQ

strong chain:
CTRL-WG-STRONG-CHAIN

terminal:
YAN_NIAN

convergence:
support/resource/structure
```

---

# 102. INVALID IMPLEMENTATIONS

Forbidden:

```text
sort energies before interpretation
```

Forbidden:

```text
deduplicate same energy before chain building
```

Forbidden:

```text
analyze pairs independently only
```

Forbidden:

```text
ignore overlapping pairs
```

Forbidden:

```text
stop at first good/bad interaction
```

Forbidden:

```text
only analyze tail
```

Forbidden:

```text
count good minus bad
```

Forbidden:

```text
discard modifiers
```

Forbidden:

```text
discard controlled challenging energy
```

---

# 103. IMPLEMENTATION PIPELINE

Canonical:

```text
INPUT
↓
NORMALIZE
↓
DIGITS
↓
PAIR RESOLUTION
↓
ENERGY + STRENGTH
↓
MODIFIER STATE
↓
DIRECTED INTERACTION
↓
POSITION
↓
CONTROL / REMEDY
↓
CHAIN BUILD
↓
SEGMENT / FLOW
↓
DOMINANT / SECONDARY
↓
TERMINAL
↓
DOMAIN INTERPRETATION
↓
CUSTOMER NARRATIVE
```

---

# 104. CHAIN ENGINE BOUNDARY

File này chịu trách nhiệm:

```text
ORDERED ENERGY STATES
→
WHOLE-SEQUENCE STRUCTURE
```

File này KHÔNG chịu trách nhiệm:

- domain wording cuối;
- recommendation wording;
- owner compatibility;
- final UI layout;
- numerical score display.

---

# 105. NEXT DEPENDENCY

Output của file này
được sử dụng trực tiếp bởi:

```text
09_DOMAIN_INTERPRETATION.md
10_CUSTOMER_NARRATIVE_CATALOG.md
11_ACCEPTANCE_GOLDEN_CASES.md
```

---

# 106. FREEZE RULE

Once accepted:

`08_CHAIN_INTERPRETATION_RULES.md`

becomes canonical source of truth
for whole-sequence interpretation.

Cursor MUST NOT:

- reduce sequence analysis to pair counting;
- ignore direction;
- ignore overlap;
- ignore chain continuation;
- ignore modifier state;
- ignore local/global control difference;
- ignore terminal convergence;
- invent chain semantics outside canonical knowledge;
- simplify repeated energies without context;
- turn structural interpretation into deterministic fate prediction.

Any change requires:

1. expert review;
2. canonical document update;
3. version bump;
4. regression tests;
5. Golden Dataset update.

---

# END OF DOCUMENT
```

Với `08` này, lõi Number Energy Engine gần như đã hoàn chỉnh về mặt suy luận: **01–03 xác định “có gì”, 04 xác định “A chuyển sang B nghĩa là gì”, 05–07 xử lý trạng thái đặc biệt và chế hóa, còn 08 đọc tất cả thành một câu chuyện liên tục của toàn dãy**. File `09_DOMAIN_INTERPRETATION.md` tiếp theo sẽ biến chính chuỗi đó thành các kết luận riêng cho **Tài vận, Công việc, Tình cảm, Tính cách, Học hành, Sức khỏe tham khảo**, đồng thời phân biệt profile số điện thoại và biển số xe.