Được. `07_CONTROL_REMEDY_RULES.md` sẽ khóa toàn bộ **cơ chế chế ước – hóa giải – điều tiết** giữa các trường khí, đặc biệt là các quan hệ bạn đã cung cấp:

- Sinh Khí giáng Ngũ Quỷ
- Thiên Y chế Tuyệt Mệnh
- Diên Niên yểm Lục Sát
- Họa Hại cần phối hợp nhiều cát tinh
- Phục Vị dùng Sinh Khí hoặc Thiên Y để điều tiết
- Ngũ Quỷ có chuỗi mạnh `Sinh Khí → Thiên Y → Diên Niên` và **không được đảo thứ tự**

Tôi đề nghị file như sau:

```markdown
# 07_CONTROL_REMEDY_RULES.md

# BTE NUMBER ENERGY — CONTROL & REMEDY RULES

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Control & Remedy Rules  
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

---

# 1. PURPOSE

Tài liệu này định nghĩa canonical rules
cho:

- chế ước;
- điều tiết;
- hóa giải;
- giảm tác động;
- chuyển hóa;
- kéo trường khí về trạng thái cân bằng.

Canonical flow:

CHALLENGING ENERGY
↓
CONTROL / REMEDY ENERGY
↓
ORDER CHECK
↓
STRENGTH CHECK
↓
POSITION CHECK
↓
MODIFIER CHECK
↓
REMEDY EFFECT
↓
FINAL STATE

Không được chỉ kiểm tra:

"có sao hóa giải hay không"

mà phải kiểm tra:

- đứng trước hay sau;
- cường độ;
- vị trí;
- có 0/5 tác động không;
- có Phục Vị kéo dài không;
- có nằm gần tail không;
- có đúng chuỗi canonical không.

---

# 2. CORE CONTROL MANTRA

Canonical khẩu quyết:

> Sinh Khí giáng Ngũ Quỷ.

> Thiên Y chế Tuyệt Mệnh.

> Diên Niên yểm Lục Sát.

> Chế phục an bài đinh.

Runtime canonical mappings:

```text
WU_GUI
controlled_by
SHENG_QI

JUE_MING
controlled_by
TIAN_Y

LIU_SHA
controlled_by
YAN_NIAN
```

---

# 3. CONTROL IS DIRECTIONAL

Critical rule:

```text
CONTROL_IS_DIRECTIONAL = TRUE
```

Không được hiểu:

```text
A controls B
=
B controls A
```

Ví dụ:

```text
WU_GUI → SHENG_QI
```

có thể là:

```text
Ngũ Quỷ được Sinh Khí chế / giáng
```

Nhưng:

```text
SHENG_QI → WU_GUI
```

không được tự động coi
là Ngũ Quỷ đã được hóa giải.

Order MUST be preserved.

---

# 4. CONTROL ≠ DELETE

Canonical:

```text
CONTROLLED_ENERGY
!=
REMOVED_ENERGY
```

Một Hung trường được chế
vẫn tồn tại.

Nhưng trạng thái có thể chuyển:

```text
UNCONTROLLED
→
MITIGATED
→
CONTROLLED
→
TRANSFORMED
```

Không được xóa Hung khỏi trace.

---

# 5. REMEDY STATE ENUM

Canonical internal states:

```text
UNCONTROLLED
PARTIALLY_MITIGATED
MITIGATED
CONTROLLED
STRONGLY_CONTROLLED
TRANSFORMED
OVERRIDDEN
```

V1 recommended customer grouping:

```text
UNCONTROLLED
PARTIALLY_CONTROLLED
CONTROLLED
WELL_BALANCED
```

Không hiển thị raw enum nếu không cần.

---

# 6. CONTROL STRENGTH FACTORS

Remedy effectiveness phụ thuộc:

```text
challenging_strength
control_strength
distance
position
modifier_state
repetition
tail_relevance
```

Recommended conceptual model:

```text
effective_control
=
control_strength
× position_relevance
× visibility_factor
× sequence_fit
```

Đây là engineering abstraction,
không phải công thức huyền học gốc.

---

# 7. STRENGTH RELATION

Nếu Hung mạnh
và Control yếu:

```text
CHALLENGING_T1
→
CONTROL_T4
```

không được gọi là
"chế hoàn toàn".

Possible state:

```text
PARTIALLY_MITIGATED
```

Nếu:

```text
CHALLENGING_T4
→
CONTROL_T1
```

control có thể mạnh hơn.

Possible state:

```text
CONTROLLED
```

Nhưng vẫn phải xét position/modifier.

---

# 8. POSITION RELATION

Một control field ở sau Hung
có giá trị khác control ở trước Hung.

Preferred canonical:

```text
CHALLENGING
→
CONTROL
```

Ví dụ:

```text
WU_GUI
→
SHENG_QI
```

Không phải:

```text
SHENG_QI
→
WU_GUI
```

Distance càng gần,
control càng trực tiếp.

---

# 9. DISTANCE-TO-CONTROL

Recommended metric:

```text
control_distance
```

Example:

```text
WU_GUI → SHENG_QI
```

distance = 1

```text
WU_GUI → X → SHENG_QI
```

distance = 2

Control gần hơn
thường có precedence cao hơn.

Không được hard-code
distance > N = invalid
nếu canonical rule chưa quy định.

---

# 10. WU_GUI CONTROL — SHENG_QI

Canonical:

> Sinh Khí giáng Ngũ Quỷ.

Model:

```text
WU_GUI
→
SHENG_QI
```

Meaning:

- biến động được giảm;
- ý tưởng được đưa về hướng hữu dụng;
- nghi ngờ/bất ổn được giảm;
- sáng tạo có cơ hội đi vào thực tế;
- năng lượng Ngũ Quỷ được điều tiết.

Canonical semantic:

```text
VOLATILITY
→
SUPPORT / OPPORTUNITY
```

---

# 11. WU_GUI CONTROL — CUSTOMER LANGUAGE

Không dùng:

> Ngũ Quỷ bị tiêu diệt.

Nên dùng:

> Trường Ngũ Quỷ được Sinh Khí phía sau điều tiết,
> giúp phần biến động và bất ổn giảm bớt,
> đồng thời hướng tư duy và sự linh hoạt
> về phía cơ hội và trợ lực thực tế.

---

# 12. WU_GUI + SHENG_QI + TAIL

Nếu:

```text
WU_GUI
→
SHENG_QI
```

và Sinh Khí gần tail:

Remedy relevance tăng.

Nếu:

```text
WU_GUI
→
SHENG_QI
→
ZERO
```

thì Sinh Khí bị giảm biểu hiện.

Control Engine MUST xét:

```text
SHENG_QI.state
```

không chỉ raw energy.

---

# 13. WU_GUI + SHENG_QI + FIVE

Nếu:

```text
WU_GUI
→
SHENG_QI
→
FIVE
```

Sinh Khí được khuếch đại.

Possible effect:

```text
control_effectiveness ↑
```

nhưng final result vẫn phải xét
whole sequence.

---

# 14. JUE_MING CONTROL — TIAN_Y

Canonical:

> Thiên Y chế Tuyệt Mệnh.

Model:

```text
JUE_MING
→
TIAN_Y
```

Meaning:

- hành động mạnh được đưa về kết quả/tài nguyên;
- tính mạo hiểm được định hướng;
- xung động có cơ hội chuyển thành thành quả;
- risk-taking được cân bằng bởi resource/result.

Canonical semantic:

```text
RISK / ACTION
→
RESOURCE / RESULT
```

---

# 15. JUE_MING CONTROL — CUSTOMER LANGUAGE

Recommended:

> Tuyệt Mệnh tạo lực hành động và tính quyết liệt,
> trong khi Thiên Y phía sau giúp dòng năng lượng
> quy về tài nguyên và thành quả.
> Khi cường độ cân bằng,
> cấu trúc này có thể biến sức hành động
> thành giá trị thực tế thay vì để rủi ro phát tán.

---

# 16. JUE_MING → TIAN_Y IS ALSO WEALTH PATTERN

Important:

```text
JUE_MING → TIAN_Y
```

vừa là:

```text
CONTROL_RELATION
```

vừa có thể là:

```text
INVESTMENT / ACTION
→
WEALTH
```

Engine MUST preserve
multiple semantic roles.

Không được collapse thành chỉ "remedy".

---

# 17. JUE_MING + TIAN_Y STRENGTH

Canonical risk–reward relation:

```text
JM small → TY small
small action / small result

JM small → TY large
small risk / stronger reward potential

JM large → TY large
large risk / large potential result

JM large → TY small
large risk / weaker reward potential
```

Remedy state phải xét
relative strength.

---

# 18. LIU_SHA CONTROL — YAN_NIAN

Canonical:

> Diên Niên yểm Lục Sát.

Model:

```text
LIU_SHA
→
YAN_NIAN
```

Meaning:

- cảm xúc được đưa về khuôn khổ;
- quan hệ/giao tế được chuyển thành năng lực nghề;
- do dự được giảm nhờ cấu trúc/kỷ luật;
- yếu tố Đào Hoa được điều tiết.

Canonical semantic:

```text
EMOTION / SOCIAL
→
STRUCTURE / CAREER
```

---

# 19. LIU_SHA CONTROL — CUSTOMER LANGUAGE

Recommended:

> Lục Sát tạo độ nhạy trong quan hệ và giao tiếp,
> còn Diên Niên phía sau giúp trường này
> đi vào khuôn khổ, trách nhiệm và mục tiêu rõ hơn.
> Đây là cấu trúc có khả năng biến giao tế
> thành năng lực nghề nghiệp khi được sử dụng đúng.

---

# 20. LIU_SHA + YAN_NIAN AS CAREER PATTERN

```text
LIU_SHA → YAN_NIAN
```

cũng là:

```text
service/social ability
→
career
```

Possible contexts:

- dịch vụ;
- đối ngoại;
- chăm sóc khách hàng;
- hành chính;
- thẩm mỹ;
- giao tiếp.

Remedy and Career semantics
cùng tồn tại.

---

# 21. HUO_HAI — NO SINGLE UNIVERSAL CONTROL

Họa Hại không có
một single control mapping đơn giản
như ba Hung trường trên.

Canonical:

```text
HUO_HAI
requires
COMPOSITE_REMEDY
```

Nguồn Knowledge chỉ ra:

- Phục Vị + Sinh Khí;
- Sinh Khí + Diên Niên;
- thứ tự trong một số cấu trúc có thể đảo;
- cần phối hợp nhiều Cát trường.

Do đó V1 không được hard-code
một sao duy nhất chế Họa Hại.

---

# 22. HUO_HAI REMEDY — CORE PRINCIPLE

Họa Hại thiên về:

```text
speech
argument
controversy
```

Remedy có thể cần:

- duy trì/stabilize;
- mở support;
- đưa vào structure.

Conceptual:

```text
HUO_HAI
↓
SUPPORT / STABILITY / STRUCTURE
↓
speech becomes functional
```

---

# 23. HUO_HAI REMEDY PATTERN — FU_WEI + SHENG_QI

Nguồn example:

```text
114
1414
```

Concept:

```text
FU_WEI
+
SHENG_QI
```

dùng để:

- ổn định;
- mở trợ lực;
- giảm tranh luận;
- giúp ngôn ngữ đi về hướng thuận hơn.

Không được nói:

> 114 chắc chắn hóa giải Họa Hại.

MUST resolve full context.

---

# 24. HUO_HAI REMEDY PATTERN — SHENG_QI + YAN_NIAN

Nguồn example:

```text
1419
```

Concept:

```text
SHENG_QI
→
YAN_NIAN
```

Meaning:

- support;
- structure;
- professionalization.

Có thể điều tiết Họa Hại
nếu nằm đúng cấu trúc.

---

# 25. HUO_HAI CONTROL STATUS

Recommended V1 states:

```text
HUO_HAI_UNCONTROLLED
HUO_HAI_PARTIALLY_SUPPORTED
HUO_HAI_BALANCED
```

Không dùng:

```text
HUO_HAI_FULLY_REMOVED
```

---

# 26. FU_WEI REMEDY

Phục Vị không phải Hung tinh thuần,
nhưng khi quá mạnh có thể:

- trì trệ;
- kéo dài;
- bảo thủ;
- làm Hung đứng trước dai dẳng.

Nguồn Knowledge cho phép:

```text
SHENG_QI
or
TIAN_Y
```

điều tiết Phục Vị.

---

# 27. FU_WEI + SHENG_QI

Concept:

```text
FU_WEI
→
SHENG_QI
```

Meaning:

- chờ đợi → cơ hội;
- trì trệ → mở;
- tích lũy → trợ lực.

Canonical:

```text
STAGNATION
→
OPPORTUNITY
```

---

# 28. FU_WEI + TIAN_Y

Concept:

```text
FU_WEI
→
TIAN_Y
```

Meaning:

- kiên trì → thành quả;
- chờ đợi → tài nguyên;
- trạng thái tĩnh → kết quả.

Canonical:

```text
PATIENCE
→
RESOURCE
```

---

# 29. FU_WEI AS AMPLIFIER OF HUNG

Critical:

```text
CHALLENGING
→
FU_WEI
```

không phải remedy.

Ví dụ:

```text
WU_GUI → FU_WEI
```

=

```text
EXTENDED_WU_GUI
```

```text
LIU_SHA → FU_WEI
```

=

```text
EXTENDED_LIU_SHA
```

```text
HUO_HAI → FU_WEI
```

=

```text
EXTENDED_HUO_HAI
```

```text
JUE_MING → FU_WEI
```

=

```text
EXTENDED_JUE_MING
```

Engine MUST NOT
gán Phục Vị là Cát rồi cộng điểm.

---

# 30. NGŨ QUỶ STRONG REMEDY CHAIN

Nguồn canonical:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

được sử dụng
cho Ngũ Quỷ mạnh.

Example source patterns:

```text
141319
14134
4134
2862
```

Important:

```text
ORDER_IS_FIXED = TRUE
```

Không được đảo:

```text
YAN_NIAN
→
TIAN_Y
→
SHENG_QI
```

và gọi là tương đương.

---

# 31. NGŨ QUỶ STRONG REMEDY SEMANTIC

Concept:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

có thể đọc:

```text
SUPPORT
→
RESOURCE
→
STRUCTURE
```

Đối với Ngũ Quỷ:

```text
VOLATILITY
↓
SUPPORT
↓
RESOURCE
↓
STRUCTURE
```

Meaning:

- biến động được giảm;
- có hướng;
- có tài nguyên;
- có cấu trúc;
- có khả năng thực thi.

---

# 32. FIXED ORDER VALIDATION

Valid:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Invalid as same remedy:

```text
TIAN_Y
→
SHENG_QI
→
YAN_NIAN
```

Invalid:

```text
YAN_NIAN
→
TIAN_Y
→
SHENG_QI
```

Invalid:

```text
SHENG_QI
→
YAN_NIAN
→
TIAN_Y
```

unless another canonical rule
explicitly defines it.

---

# 33. REMEDY CHAIN LENGTH

A control pattern
có thể là:

```text
single-step
```

or:

```text
multi-step
```

Examples:

Single-step:

```text
WU_GUI → SHENG_QI
```

Multi-step:

```text
WU_GUI
→
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Engine must preserve chain.

---

# 34. CONTROL EFFECT ≠ COUNT

Forbidden:

```text
1 good energy = 1 remedy point
```

Control effectiveness
không được tính bằng số lượng Cát đơn giản.

Phải xét:

```text
right_energy
right_order
right_strength
right_position
right_modifier_state
```

---

# 35. MODIFIER IMPACT ON CONTROL

Nếu control energy gặp ZERO:

```text
CONTROL
→
ZERO
```

control effectiveness có thể giảm
do trường bị ẩn/giảm biểu hiện.

Nếu control energy gặp FIVE:

```text
CONTROL
→
FIVE
```

control field có thể mạnh hơn.

But:

```text
FIVE
```

không tự tạo remedy.

---

# 36. ZERO BETWEEN CHALLENGE AND CONTROL

Ví dụ:

```text
WU_GUI
→
ZERO
→
SHENG_QI
```

Không được xử lý giống:

```text
WU_GUI
→
SHENG_QI
```

Control may be:

```text
INTERRUPTED
HIDDEN
REDUCED
```

depending modifier semantics.

---

# 37. FIVE BETWEEN CHALLENGE AND CONTROL

Ví dụ:

```text
WU_GUI
→
FIVE
→
SHENG_QI
```

không được simplify.

5 có thể:

- làm relationship explicit;
- khuếch đại energy tương tác.

Final effect phải qua
Modifier Engine + Control Engine.

---

# 38. POSITION IMPACT ON CONTROL

Remedy gần tail
có final relevance cao hơn.

Example:

```text
WU_GUI → SHENG_QI
```

at tail

có thể tạo:

```text
CONTROLLED_TERMINAL
```

Trong khi cùng control ở đầu
không đảm bảo Hung sau đó
không tái xuất hiện.

---

# 39. REAPPEARING CHALLENGING ENERGY

Nếu:

```text
WU_GUI
→
SHENG_QI
→
WU_GUI
```

không được nói:

> Ngũ Quỷ đã được hóa giải.

Phải đọc:

1. Ngũ Quỷ đầu được Sinh Khí điều tiết;
2. Ngũ Quỷ lại xuất hiện sau đó;
3. terminal state vẫn có Ngũ Quỷ.

Canonical:

```text
CONTROL_LOCAL
!=
CONTROL_GLOBAL
```

---

# 40. LOCAL VS GLOBAL CONTROL

Define:

```text
LOCAL_CONTROL
```

= một interaction Hung → Control.

```text
GLOBAL_CONTROL
```

= toàn chuỗi không còn Hung uncontrolled
ở phần sau quan trọng.

Final Narrative ưu tiên
Global Control status.

---

# 41. CONTROL COVERAGE

Recommended metric:

```text
control_coverage
=
controlled_challenging_prominence
/
total_challenging_prominence
```

Engineering-only.

Không hiển thị % cho khách
trừ khi có Score Standard riêng.

---

# 42. REMEDY DENSITY

Không dùng:

```text
more remedy patterns
= automatically better
```

Quá nhiều Cát/remedy
có thể tạo cấu trúc thiếu cân bằng.

Must follow:

```text
Cát làm chủ
Hung làm dụng
Có thu có phóng
```

---

# 43. CONTROL OF STRONG WU_GUI

Nếu:

```text
WU_GUI_T1
```

mà chỉ có:

```text
SHENG_QI_T4
```

Remedy state:

```text
PARTIAL
```

Nếu:

```text
WU_GUI_T4
→
SHENG_QI_T1
```

Remedy có thể mạnh hơn.

Strength relation MUST be visible
to expert trace.

---

# 44. CONTROL OF STRONG JUE_MING

Nếu:

```text
JUE_MING_T1
→
TIAN_Y_T4
```

risk vẫn nổi bật.

Không được nói:

> đã hóa giải hoàn toàn.

Narrative:

> Thiên Y có tác dụng điều tiết,
> nhưng lực Tuyệt Mệnh vẫn mạnh hơn
> nên yếu tố mạo hiểm còn đáng lưu ý.

---

# 45. CONTROL OF STRONG LIU_SHA

Nếu:

```text
LIU_SHA_T1
→
YAN_NIAN_T4
```

control may be partial.

Nếu:

```text
LIU_SHA_T4
→
YAN_NIAN_T1
```

stabilization stronger.

---

# 46. CONTROL + REPETITION

Ví dụ:

```text
WU_GUI
→
WU_GUI
→
SHENG_QI
```

Remedy phải đối diện
repeated Ngũ Quỷ.

Control Engine cần xét:

```text
repetition_factor
```

Không được coi giống:

```text
WU_GUI
→
SHENG_QI
```

---

# 47. CONTROL + PHUC_VI

Ví dụ:

```text
WU_GUI
→
FU_WEI
→
SHENG_QI
```

Phục Vị làm Ngũ Quỷ kéo dài
trước khi Sinh Khí xuất hiện.

Control hiệu quả có thể thấp hơn
so với direct control.

---

# 48. CONTROL + TAIL ZERO

Ví dụ:

```text
WU_GUI
→
SHENG_QI
→
ZERO
```

Terminal:

```text
SHENG_QI_HIDDEN
```

Meaning:

- có control;
- nhưng khả năng phát huy
  của trường chế bị giảm.

Final status:

```text
PARTIALLY_CONTROLLED
```

hoặc context-equivalent.

---

# 49. CONTROL + TAIL FIVE

Ví dụ:

```text
WU_GUI
→
SHENG_QI
→
FIVE
```

Terminal:

```text
SHENG_QI_AMPLIFIED
```

Remedy prominence tăng.

---

# 50. CONTROL + AUSPICIOUS TAIL

Preferred architecture:

```text
CHALLENGING
→
CONTROL
→
AUSPICIOUS TAIL
```

Example:

```text
WU_GUI
→
SHENG_QI
→
TIAN_Y
```

Possible semantic:

```text
volatility
→
support
→
resource
```

Đây là stronger convergence
than Hung at tail.

---

# 51. CHALLENGING TAIL AFTER REMEDY

Example:

```text
WU_GUI
→
SHENG_QI
→
JUE_MING
```

Local control exists,
nhưng terminal vẫn challenging.

Final:

```text
LOCAL_CONTROL
+
CHALLENGING_TERMINAL
```

Không được gọi
whole sequence đã cân bằng hoàn toàn.

---

# 52. CUSTOMER REMEDY LANGUAGE

Không dùng:

> hóa giải 100%.

> tiêu trừ hung khí hoàn toàn.

> số này đã hết xấu.

Recommended:

> Trường bất lợi đã có yếu tố điều tiết phía sau,
> giúp mức biến động giảm bớt
> và đưa dòng năng lượng về hướng cân bằng hơn.

Hoặc:

> Có yếu tố chế ước, nhưng cường độ chưa đủ mạnh
> để triệt tiêu hoàn toàn ảnh hưởng của trường trước.

---

# 53. EXPERT TRACE

Expert Mode example:

```text
Challenge:
81 = WU_GUI / Tier 1

Control:
14 = SHENG_QI / Tier 1

Relation:
WU_GUI → SHENG_QI

Control type:
DIRECT

Distance:
1

Modifier:
NONE

Position:
REAR → TAIL

Control status:
STRONGLY_CONTROLLED
```

Customer Mode không cần hiển thị trace kỹ thuật.

---

# 54. CONTROL OBJECT

Recommended runtime:

```text
ControlResult {
    challenge_energy
    challenge_pair
    challenge_strength

    control_energy
    control_pair
    control_strength

    rule_id

    order_valid
    distance

    challenge_position
    control_position

    challenge_modifier
    control_modifier

    repetition_factor

    control_state
    control_effectiveness_class

    terminal_relevance
}
```

---

# 55. CONTROL RULE IDs

Canonical:

```text
CTRL-WG-SQ
CTRL-JM-TY
CTRL-LS-YN
CTRL-HH-COMPOSITE
CTRL-FW-SQ
CTRL-FW-TY
CTRL-WG-STRONG-CHAIN
```

---

# 56. CTRL-WG-SQ

```text
challenge = WU_GUI
control = SHENG_QI
order = FIXED
```

---

# 57. CTRL-JM-TY

```text
challenge = JUE_MING
control = TIAN_Y
order = FIXED
```

---

# 58. CTRL-LS-YN

```text
challenge = LIU_SHA
control = YAN_NIAN
order = FIXED
```

---

# 59. CTRL-HH-COMPOSITE

```text
challenge = HUO_HAI
control = COMPOSITE
```

Allowed V1 support patterns include:

```text
FU_WEI + SHENG_QI
SHENG_QI + YAN_NIAN
```

Final validation depends full sequence.

---

# 60. CTRL-FW-SQ

```text
target = excessive / stagnant FU_WEI
regulator = SHENG_QI
```

---

# 61. CTRL-FW-TY

```text
target = excessive / stagnant FU_WEI
regulator = TIAN_Y
```

---

# 62. CTRL-WG-STRONG-CHAIN

Canonical chain:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Purpose:

```text
strong WU_GUI regulation
```

Order:

```text
FIXED
```

---

# 63. STRONG CHAIN EXAMPLE — 141319

Possible parsing:

```text
14 = SHENG_QI
13 = TIAN_Y
19 = YAN_NIAN
```

Canonical control sequence:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

This pattern may be recognized
as strong WU_GUI remedy chain.

Must not use raw substring match only.

Parser must validate actual Energy sequence.

---

# 64. PATTERN VALIDATION

Forbidden:

```text
if number contains "141319"
then fixed result
```

Correct:

```text
resolve pairs
resolve energies
resolve order
resolve strengths
resolve modifiers
resolve position
then match remedy rule
```

---

# 65. CONTROL VS NORMAL INTERACTION

Control relationship
does not replace
Directed Interaction semantics.

Example:

```text
JUE_MING → TIAN_Y
```

must emit both:

```text
interaction:
ACTION → WEALTH

control:
TIAN_Y controls JUE_MING
```

Narrative Composer decides
how to combine.

---

# 66. CONTROL VS DOMAIN

Control may affect domain interpretation.

Example:

```text
LIU_SHA → YAN_NIAN
```

Relationship Domain:

- Lục Sát được ổn định hơn.

Career Domain:

- social/service ability → profession.

One sequence,
multiple domain meanings.

---

# 67. REMEDY IS NOT PRESCRIPTION

Customer system phải tránh
ngôn ngữ:

> bạn phải mua số chứa 14 để chữa số xấu.

Recommended:

> Nếu lựa chọn dãy số mới,
> có thể ưu tiên cấu trúc có trường
> điều tiết phù hợp để tăng tính cân bằng.

Không tạo guarantee.

---

# 68. PHONE REMEDY PROFILE

Phone number có thể dùng
full Control/Remedy interpretation.

Priority:

- whole chain;
- repeated challenge;
- tail;
- 0/5;
- control coverage.

---

# 69. VEHICLE REMEDY PROFILE

Vehicle plate dùng cùng rules,
nhưng narrative ưu tiên:

- ổn định;
- công việc;
- tài vận;
- trạng thái cuối;
- balance.

Giảm:

- hôn nhân;
- Đào Hoa.

---

# 70. INVALID IMPLEMENTATIONS

Forbidden:

```text
good pair after bad pair = always remedy
```

Forbidden:

```text
same energies anywhere = control
```

Forbidden:

```text
reverse order = same remedy
```

Forbidden:

```text
presence of SHENG_QI means all WU_GUI controlled
```

Forbidden:

```text
presence of TIAN_Y means all JUE_MING controlled
```

Forbidden:

```text
presence of YAN_NIAN means all LIU_SHA controlled
```

Forbidden:

```text
FU_WEI always good
```

Forbidden:

```text
remedy deletes challenge
```

Forbidden:

```text
ignore 0 / 5 on control energy
```

---

# 71. TEST — WU_GUI → SHENG_QI

Input energy sequence:

```text
WU_GUI
→
SHENG_QI
```

Expected:

```text
rule = CTRL-WG-SQ
order_valid = true
control_state >= MITIGATED
```

depending strength/position.

---

# 72. TEST — SHENG_QI → WU_GUI

Expected:

```text
CTRL-WG-SQ
NOT MATCHED
```

Must NOT be treated as same rule.

---

# 73. TEST — JUE_MING → TIAN_Y

Expected:

```text
rule = CTRL-JM-TY
```

and retain:

```text
ACTION → WEALTH
```

interaction meaning.

---

# 74. TEST — TIAN_Y → JUE_MING

Expected:

```text
CTRL-JM-TY
NOT MATCHED
```

Interaction:

```text
RESOURCE → INVESTMENT
```

---

# 75. TEST — LIU_SHA → YAN_NIAN

Expected:

```text
rule = CTRL-LS-YN
```

plus Career semantic.

---

# 76. TEST — YAN_NIAN → LIU_SHA

Expected:

```text
CTRL-LS-YN
NOT MATCHED
```

Interaction remains:

```text
CAREER → EMOTION
```

---

# 77. TEST — WU_GUI → FU_WEI → SHENG_QI

Expected:

```text
WU_GUI extended first
then SHENG_QI control attempt
```

Control effectiveness
must be lower than direct
WU_GUI → SHENG_QI
if other factors equal.

---

# 78. TEST — WU_GUI → SHENG_QI → ZERO

Expected:

```text
control exists
control energy hidden/reduced
final status != fully controlled
```

---

# 79. TEST — WU_GUI → SHENG_QI → FIVE

Expected:

```text
control exists
control energy amplified
```

---

# 80. TEST — STRONG CHAIN

Input energy chain:

```text
WU_GUI
→
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Expected:

```text
CTRL-WG-SQ
+
CTRL-WG-STRONG-CHAIN
```

if sequence conditions pass.

---

# 81. TEST — WRONG ORDER STRONG CHAIN

Input:

```text
WU_GUI
→
TIAN_Y
→
SHENG_QI
→
YAN_NIAN
```

Expected:

```text
CTRL-WG-STRONG-CHAIN = NO MATCH
```

---

# 82. GLOBAL CONTROL SUMMARY

Recommended output:

```text
ControlSummary {
    total_challenging_patterns
    controlled_patterns
    partially_controlled_patterns
    uncontrolled_patterns

    strongest_control
    weakest_control

    tail_control_state

    overall_balance_state
}
```

No deterministic fate claims.

---

# 83. OVERALL BALANCE STATES

Recommended V1:

```text
WELL_BALANCED
MOSTLY_BALANCED
MIXED
UNDER_CONTROLLED
VOLATILE
```

These are structural labels,
not life predictions.

---

# 84. CUSTOMER SUMMARY EXAMPLE

Example:

> Dãy số có xuất hiện Ngũ Quỷ với cường độ khá rõ,
> nhưng phía sau được Sinh Khí điều tiết.
> Điều này giúp phần biến động và tư duy thay đổi
> có xu hướng được dẫn về cơ hội và trợ lực thực tế.
> Tuy vậy, mức cân bằng cuối cùng vẫn cần xét
> cường độ của hai trường và trạng thái phần đuôi.

---

# 85. EXPERT SUMMARY EXAMPLE

```text
Challenge:
WU_GUI T1

Control:
SHENG_QI T2

Order:
VALID

Distance:
1

Modifier:
NONE

Position:
MIDDLE → REAR

State:
CONTROLLED_PARTIAL

Tail relevance:
MEDIUM
```

---

# 86. ENGINE BOUNDARY

File này chịu trách nhiệm:

```text
CHALLENGING ENERGY
→
CONTROL / REMEDY
→
CONTROL STATE
```

File này KHÔNG chịu trách nhiệm:

- whole-chain narrative;
- final domain conclusion;
- final customer wording;
- owner compatibility;
- recommendation ranking.

---

# 87. NEXT DEPENDENCY

Output được dùng bởi:

```text
08_CHAIN_INTERPRETATION_RULES.md
09_DOMAIN_INTERPRETATION.md
10_CUSTOMER_NARRATIVE_CATALOG.md
11_ACCEPTANCE_GOLDEN_CASES.md
```

---

# 88. FREEZE RULE

Once accepted:

`07_CONTROL_REMEDY_RULES.md`

becomes canonical source of truth
for Number Energy control/remedy logic.

Cursor MUST NOT:

- invent new control pair;
- reverse control direction;
- delete challenged energy after remedy;
- call any Cát after Hung a remedy;
- ignore relative strength;
- ignore 0/5 modifier;
- ignore Phục Vị extension;
- ignore position;
- ignore reappearing Hung after local control;
- reorder the strong Ngũ Quỷ remedy chain;
- promise complete "hóa giải" to customers.

Any change requires:

1. expert review;
2. canonical document update;
3. version bump;
4. regression tests;
5. Golden Dataset update.

---

# END OF DOCUMENT
```

File `07` này khóa rất rõ một điều: **“có cát tinh” khác hoàn toàn với “được chế hóa đúng”**. Từ đây engine phải hiểu đúng thứ tự, cường độ và vị trí, nên sẽ tránh kiểu luận quá đơn giản như “có Ngũ Quỷ nhưng cũng có Sinh Khí nên tốt”.