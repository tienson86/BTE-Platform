Được. `06_POSITION_AND_TAIL_RULES.md` phải khóa một nguyên tắc rất quan trọng: **cùng một trường khí nhưng đứng ở đầu, giữa hay cuối dãy sẽ không được đọc giống nhau**. File này cũng là nơi xác định rõ “đuôi số” có trọng số cao nhưng không được phép xóa bỏ toàn bộ ngữ cảnh trước đó.

```markdown
# 06_POSITION_AND_TAIL_RULES.md

# BTE NUMBER ENERGY — POSITION & TAIL RULES

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Position & Tail Rules  
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

---

# 1. PURPOSE

Tài liệu này định nghĩa vai trò của vị trí
trong toàn bộ dãy số.

Canonical principle:

> Cùng một trường khí,
> nếu xuất hiện ở vị trí khác nhau,
> có thể mang trọng số và vai trò khác nhau.

Position Engine phải phân biệt ít nhất:

```text
HEAD
MIDDLE
REAR
TAIL
TERMINAL
```

Trong đó:

HEAD
=
khởi phát / nền

MIDDLE
=
quá trình / vận động / chuyển hóa

REAR
=
giai đoạn gần kết quả

TAIL
=
vùng kết quả

TERMINAL
=
trạng thái cuối cùng của dãy

---

# 2. POSITION IS SEMANTIC

Canonical:

```text
POSITION_IS_SEMANTIC = TRUE
```

Không được coi:

```text
ENERGY at HEAD
=
ENERGY at TAIL
```

Ví dụ:

```text
JUE_MING
```

ở giữa dãy có thể đóng vai:

```text
action
risk-taking
investment
movement
```

Nhưng nếu Tuyệt Mệnh trở thành
terminal state ở cuối dãy,
thì trọng số rủi ro phải cao hơn.

---

# 3. WHOLE-SEQUENCE ZONES

Recommended segmentation:

```text
HEAD
MIDDLE
REAR
TAIL
```

Đối với dãy đủ dài:

```text
HEAD:
khoảng 20–25% đầu

MIDDLE:
khoảng 40–50% giữa

REAR:
khoảng 20–25% gần cuối

TAIL:
2–3 chữ số cuối / interaction cuối
```

Đây là implementation guideline.

Không phải quy tắc huyền học tuyệt đối.

Với dãy ngắn như biển số,
engine phải dùng relative position
thay vì fixed length.

---

# 4. HEAD — CANONICAL ROLE

HEAD đại diện xu hướng:

```text
INITIATION
FOUNDATION
ENTRY_STATE
```

Có thể hiểu là:

- cách dãy bắt đầu;
- trường khí mở đầu;
- động lực ban đầu;
- nền của quá trình tiếp theo.

HEAD không nên có trọng số final outcome
cao bằng TAIL.

Nhưng HEAD quan trọng khi:

- tạo chuỗi chế hóa;
- mở đầu một interaction;
- kích hoạt modifier;
- quyết định hướng chuyển đầu tiên.

---

# 5. MIDDLE — CANONICAL ROLE

MIDDLE đại diện:

```text
PROCESS
MOVEMENT
INTERACTION
TRANSFORMATION
```

Đây là vùng quan trọng nhất để đọc:

- Hung làm dụng;
- Cát sinh tài nguyên;
- chuyển trường khí;
- tương tác;
- chế hóa;
- cách năng lượng vận hành.

Canonical principle:

> Phần giữa cho biết quá trình dãy số
> sử dụng năng lượng như thế nào.

Do đó nhiều Hung trường
có thể vẫn có giá trị
nếu đứng đúng vai trò trong MIDDLE.

---

# 6. REAR — CANONICAL ROLE

REAR đại diện:

```text
APPROACHING_OUTCOME
CONSOLIDATION
LATE_SEQUENCE_STATE
```

Các trường ở vùng REAR
có trọng số lớn hơn HEAD/MIDDLE
trong final synthesis.

REAR đặc biệt quan trọng với:

```text
TIAN_Y
YAN_NIAN
SHENG_QI
```

vì có thể thể hiện:

- tài nguyên được quy tụ;
- công việc được ổn định;
- quý nhân/cơ hội được giữ lại.

---

# 7. TAIL — CANONICAL ROLE

TAIL đại diện:

```text
OUTCOME
CONVERGENCE
RESULT
```

Canonical principle từ Knowledge Source:

> Số đuôi tất cát, mới có thể thành quả.

Implementation interpretation:

```text
AUSPICIOUS_TAIL
=
PREFERRED_OUTCOME_STRUCTURE
```

Không được hiểu:

```text
AUSPICIOUS_TAIL
=
GUARANTEED_GOOD_LIFE
```

TAIL có trọng số cao
nhưng KHÔNG được xóa
toàn bộ cấu trúc phía trước.

---

# 8. TERMINAL STATE

Terminal State là trường khí
hoặc modifier cuối cùng
mà sequence kết thúc.

Ví dụ:

```text
... → TIAN_Y
```

Terminal Energy:

```text
TIAN_Y
```

Ví dụ:

```text
... → TIAN_Y → ZERO
```

Terminal State:

```text
TIAN_Y_HIDDEN
```

Ví dụ:

```text
... → WU_GUI → FU_WEI
```

Terminal State:

```text
EXTENDED_WU_GUI
```

Final synthesis MUST use terminal state,
không chỉ terminal raw digit.

---

# 9. TAIL WEIGHT

Recommended engineering weights:

```text
HEAD    = 0.70
MIDDLE  = 1.00
REAR    = 1.15
TAIL    = 1.30
TERMINAL_STATE = 1.40
```

IMPORTANT:

Đây là normalized engineering weights
phục vụ ranking deterministic.

Không phải điểm huyền học gốc.

Không hiển thị cho khách.

---

# 10. POSITION WEIGHT ≠ FINAL SCORE

Forbidden:

```text
pair_score × tail_weight
=
final_good_bad
```

Correct:

```text
Energy
+
Strength
+
Directed Interaction
+
Position
+
Modifier
+
Control/Remedy
+
Domain
+
Whole Sequence

→
Final Interpretation
```

Position chỉ là một dimension.

---

# 11. PREFERRED POSITION — SINH KHÍ

Canonical preference:

```text
SHENG_QI
preferred_position = MIDDLE
```

Reason:

Sinh Khí thiên về:

- mở cơ hội;
- quý nhân;
- kết nối;
- chuyển nguy thành thuận.

Ở MIDDLE,
Sinh Khí có thể:

- mở đường cho trường sau;
- làm bridge;
- tham gia chế Ngũ Quỷ;
- tạo trợ lực trong quá trình.

---

# 12. SINH KHÍ AT TAIL

Sinh Khí ở cuối dãy
vẫn là cấu trúc thuận.

Possible meaning:

- kết quả có trợ lực;
- kết thúc theo trạng thái sáng;
- quan hệ/quý nhân còn duy trì.

Nhưng:

Sinh Khí không phải Wealth Core.

Không được viết:

> đuôi Sinh Khí = giàu.

---

# 13. PREFERRED POSITION — THIÊN Y

Canonical preference:

```text
TIAN_Y
preferred_position = REAR / TAIL
```

Reason:

Thiên Y đại diện:

- tài nguyên;
- thành quả;
- tài khí;
- relationship result.

Ở vùng cuối,
Thiên Y phù hợp với nguyên tắc:

```text
PROCESS
→
RESOURCE
```

Ví dụ:

```text
HUO_HAI → TIAN_Y
```

ở cuối:

```text
communication
→
wealth/result
```

là cấu trúc có dòng kết quả rõ.

---

# 14. THIÊN Y AT HEAD

Thiên Y ở đầu không xấu.

Nhưng semantic có thể chuyển thành:

```text
RESOURCE
→
WHAT?
```

Tức phải xem trường phía sau
để biết tài nguyên đi đâu.

Ví dụ:

```text
TIAN_Y → JUE_MING
```

=

```text
resource
→
investment / expenditure
```

Do đó Thiên Y ở đầu
không được kết luận như Thiên Y ở cuối.

---

# 15. PREFERRED POSITION — DIÊN NIÊN

Canonical:

```text
YAN_NIAN
preferred_position = REAR / TAIL
```

Reason:

Diên Niên đại diện:

- năng lực;
- sự nghiệp;
- chuyên môn;
- ổn định;
- quản trị.

Ở phần cuối,
có thể biểu thị:

- công việc quy về ổn định;
- chuyên môn được củng cố;
- khả năng giữ kết quả.

---

# 16. DIÊN NIÊN IN MIDDLE

Diên Niên ở MIDDLE rất hữu dụng
khi đóng vai:

```text
professionalization
structure
execution
```

Ví dụ:

```text
WU_GUI → YAN_NIAN
```

=

```text
idea
→
execution
```

Nếu còn trường phía sau,
phải tiếp tục đọc.

---

# 17. PHỤC VỊ POSITION RULE

Phục Vị phụ thuộc rất mạnh vào vị trí.

Canonical:

```text
A → FU_WEI
```

ở bất kỳ vị trí nào:

```text
EXTEND(A)
```

Nhưng nếu:

```text
A → FU_WEI
```

nằm tại TAIL,
trường A có khả năng trở thành
terminal extended state.

Ví dụ:

```text
LIU_SHA → FU_WEI
```

ở cuối:

```text
EXTENDED_LIU_SHA
```

phải được đánh trọng số cao hơn
cùng interaction ở giữa dãy.

---

# 18. CHALLENGING ENERGY IN MIDDLE

Canonical philosophy:

> Hung tinh làm dụng.

Do đó Hung trường ở MIDDLE
không được tự động đánh giá xấu.

Possible functional roles:

```text
HUO_HAI
→ communication

WU_GUI
→ intelligence / creativity

LIU_SHA
→ social / service / aesthetic

JUE_MING
→ action / investment
```

Nếu Hung ở giữa:

```text
HUNG
→ AUSPICIOUS
```

có thể tạo structure tốt.

Ví dụ:

```text
HUO_HAI → TIAN_Y
```

=

```text
communication
→ wealth
```

---

# 19. CHALLENGING ENERGY AT TAIL

Challenging Energy ở TAIL
cần được đánh trọng số rủi ro cao hơn.

Ví dụ:

```text
... → WU_GUI
```

terminal tendency:

- biến động;
- bất ổn;
- khó giữ trạng thái.

```text
... → LIU_SHA
```

terminal tendency:

- cảm xúc;
- quan hệ;
- do dự.

```text
... → HUO_HAI
```

terminal tendency:

- thị phi;
- tranh luận;
- giao tiếp bất ổn.

```text
... → JUE_MING
```

terminal tendency:

- hành động mạnh;
- tiêu hao;
- mạo hiểm.

Không được nói:

> đuôi Hung = chắc chắn xấu.

Phải nói:

> trạng thái cuối dãy thiên về
> trường có tính biến động/rủi ro,
> cần xem có chế hóa hay không.

---

# 20. ZERO AT TAIL

Canonical:

```text
TAIL_ZERO
=
RESULT_HIDDEN_OR_REDUCED
```

Possible interpretation:

- thành quả khó hiển;
- trạng thái cuối bị giảm biểu hiện;
- tài nguyên khó tụ;
- kết quả thiếu rõ ràng.

Không hard-code:

```text
TAIL_ZERO = BAD
```

---

# 21. FIVE AT TAIL

Canonical:

```text
TAIL_FIVE
=
AMPLIFY_PREVIOUS_TERMINAL_ENERGY
```

Nếu:

```text
TIAN_Y → FIVE
```

có thể:

```text
TIAN_Y_AMPLIFIED
```

Nếu:

```text
WU_GUI → FIVE
```

có thể:

```text
WU_GUI_AMPLIFIED
```

5 không tự mang cát tính.

---

# 22. TAIL PHỤC VỊ

Nếu:

```text
ENERGY → FU_WEI
```

kết thúc dãy,

final state là:

```text
EXTENDED(ENERGY)
```

Không được coi final state là:

```text
FU_WEI = GOOD
```

Ví dụ:

```text
18 → 88
```

nếu canonical interaction là
Ngũ Quỷ được kéo dài,

terminal result phải phản ánh
Ngũ Quỷ kéo dài.

---

# 23. TAIL CÁT TINH

Preferred terminal energies:

```text
SHENG_QI
TIAN_Y
YAN_NIAN
```

Phục Vị chỉ được đánh giá sau khi xác định
nó đang kéo dài trường gì.

Canonical concept:

```text
AUSPICIOUS_TERMINAL
=
favorable convergence
```

không phải guarantee.

---

# 24. TAIL HUNG + REMEDY

Nếu Hung ở vùng cuối
nhưng có remedy sau đó,
không được kết luận ở Hung.

Ví dụ:

```text
WU_GUI
→
SHENG_QI
```

Nếu Sinh Khí là terminal:

```text
WU_GUI controlled
→ terminal support
```

khác hoàn toàn:

```text
SHENG_QI
→
WU_GUI
```

với WU_GUI terminal.

Order MUST be preserved.

---

# 25. NEAR-TAIL REMEDY

Một remedy chỉ có giá trị final cao
khi nó:

- xuất hiện sau Hung;
- còn hiệu lực gần tail;
- không bị 0 làm ẩn;
- không bị cấu trúc khác phá vỡ;
- đúng thứ tự canonical.

Position Engine phải cung cấp:

```text
distance_to_tail
```

cho Control Engine.

---

# 26. DISTANCE-TO-TAIL

Recommended metric:

```text
distance_to_tail = number of transitions
from current interaction
to terminal state
```

Ví dụ:

```text
A → B → C → D
```

D:

```text
distance = 0
```

C:

```text
distance = 1
```

B:

```text
distance = 2
```

A:

```text
distance = 3
```

Có thể dùng cho weighting.

---

# 27. RECENCY PRINCIPLE

Trong một dãy dài,
trường gần cuối có thể
được ưu tiên hơn trường cùng loại ở đầu.

Canonical:

```text
LATE_SEQUENCE_STATE
>
EARLY_SEQUENCE_STATE
```

chỉ trong final convergence analysis.

Không được xóa giá trị early state
trong process interpretation.

---

# 28. REPETITION + POSITION

Repetition phải xét vị trí.

Ví dụ:

```text
TIAN_Y → TIAN_Y
```

ở MIDDLE:

- tài khí mạnh trong quá trình.

Ở TAIL:

- tài khí mạnh ở vùng kết quả.

Tương tự:

```text
WU_GUI → WU_GUI
```

ở TAIL:

- biến động mạnh ở trạng thái cuối.

---

# 29. POSITION + STRENGTH

Final prominence depends on:

```text
PAIR_STRENGTH
×
POSITION_WEIGHT
```

nhưng chỉ dùng để đo:

```text
PROMINENCE
```

không phải:

```text
GOODNESS
```

Ví dụ:

```text
JUE_MING_T1 at TAIL
```

có prominence cao.

Nhưng final narrative
phải xét remedy.

---

# 30. ACTIVE / PASSIVE PAIR + POSITION

Nếu `03_PAIR_STRENGTH_MATRIX`
sau này khóa thêm:

```text
ACTIVE_YANG
PASSIVE_YIN
```

thì Position Engine có thể xét:

```text
ACTIVE energy at HEAD/MIDDLE
```

phù hợp với movement.

Trong khi:

```text
PASSIVE energy at TAIL
```

có thể phù hợp với stabilization.

Nhưng chưa được tự suy diễn ngoài
Knowledge đã khóa.

---

# 31. POSITION PROFILE — PHONE NUMBER

Số điện thoại thường có dãy đủ dài.

Recommended zones:

```text
PREFIX / HEAD
BODY / MIDDLE
REAR
TAIL
```

Customer narrative ưu tiên:

- whole sequence;
- middle flow;
- rear transition;
- terminal state.

Không được chỉ luận 4 số cuối.

---

# 32. PHONE PREFIX POLICY

Đầu số điện thoại có thể là
yếu tố nhà mạng / lịch sử cấp số.

Do đó Product Layer có thể
cung cấp hai mode:

```text
FULL_NUMBER_MODE
PERSONAL_SEQUENCE_MODE
```

Nếu có yêu cầu bỏ đầu số,
phải được quy định riêng.

Default canonical:

```text
FULL_NUMBER_MODE
```

tức toàn bộ chữ số
được đưa vào phân tích.

---

# 33. POSITION PROFILE — VEHICLE PLATE

Biển số xe ngắn hơn.

Do đó không dùng fixed percentage
như số điện thoại.

Recommended:

```text
FIRST_PAIR
MIDDLE_INTERACTIONS
LAST_PAIR
TERMINAL_INTERACTION
```

Tail có trọng số cao.

Nhưng toàn biển vẫn phải được phân tích.

---

# 34. CAR / MOTORBIKE PLATE

Ô tô và xe máy
dùng cùng position rules.

Narrative Profile có thể khác về:

- mục đích;
- công việc;
- tài vận;
- sử dụng cá nhân;
- sử dụng kinh doanh.

Nhưng không thay đổi
canonical position semantics.

---

# 35. NON-NUMERIC CHARACTERS

Biển số có thể chứa:

```text
letters
hyphen
dot
space
province code
```

Position Engine chỉ xử lý:

```text
CANONICAL_NUMERIC_SEQUENCE
```

Non-numeric formatting
được xử lý tại Input Normalizer.

Không được coi ký tự chữ
là trường khí.

---

# 36. LEADING ZERO

Nếu dãy hợp lệ có leading zero:

```text
0AB...
```

không được tự động xóa số 0.

Zero phải được chuyển qua:

```text
05_ZERO_FIVE_MODIFIERS.md
```

Trừ khi Product Input Standard
quy định đó chỉ là formatting artifact.

---

# 37. TRAILING ZERO

Trailing zero là semantic.

Ví dụ:

```text
...130
```

0 cuối không được trim.

Canonical:

```text
TERMINAL_ZERO = TRUE
```

và phải được xử lý.

---

# 38. POSITION + DIRECTED INTERACTION

Mỗi Directed Interaction phải có:

```text
start_index
end_index
zone
distance_to_tail
```

Example:

```text
813968
```

engine có thể resolve:

```text
81 = WG
13 = TY
39 = SQ
96 = JM
68 = TY
```

Interactions:

```text
WG → TY
TY → SQ
SQ → JM
JM → TY
```

Mỗi interaction phải giữ
position riêng.

Không chỉ giữ list Energy.

---

# 39. POSITIONAL INTERACTION OBJECT

Recommended:

```text
PositionedInteraction {
    interaction_id

    source_pair
    target_pair

    source_energy
    target_energy

    start_index
    end_index

    zone
    distance_to_tail

    source_strength
    target_strength

    source_modifier
    target_modifier

    terminal_relevance
}
```

---

# 40. DOMINANT ENERGY ≠ LAST ENERGY

Final result không được chọn đơn giản:

```text
dominant_energy = last_energy
```

Dominant Energy cần xét:

- count;
- strength;
- repetition;
- position;
- modifier;
- interaction;
- domain;
- control/remedy.

Tail chỉ có trọng số cao hơn.

---

# 41. TERMINAL ENERGY ≠ DOMINANT ENERGY

Ví dụ:

Một dãy có rất nhiều Diên Niên
nhưng cuối là Sinh Khí.

Có thể:

```text
dominant = YAN_NIAN
terminal = SHENG_QI
```

Narrative cần nói cả hai:

> Dãy thiên về năng lực/sự nghiệp,
> nhưng trạng thái cuối quy về quý nhân,
> hỗ trợ và cơ hội.

Không được chọn một và bỏ một.

---

# 42. PRIMARY / SECONDARY / TERMINAL

Recommended whole-sequence labels:

```text
PRIMARY_ENERGY
SECONDARY_ENERGY
TERMINAL_ENERGY
```

Ví dụ:

```text
PRIMARY:
YAN_NIAN

SECONDARY:
TIAN_Y

TERMINAL:
SHENG_QI
```

Điều này hỗ trợ Customer Hero Summary.

---

# 43. TAIL BALANCE

Tail không chỉ xét raw Energy.

Phải xét:

```text
tail_energy
tail_modifier
tail_repetition
tail_control_status
tail_strength
```

Canonical Tail State:

```text
TailState {
    energy
    strength
    modifier_state
    extended_by_fu_wei
    controlled
    controlling_energy
    final_semantic
}
```

---

# 44. TAIL WITH ZERO EXAMPLE

Input:

```text
...130
```

Resolve:

```text
13 = TIAN_Y_T1
0 = POST modifier
```

Tail State:

```text
energy = TIAN_Y
strength = T1
modifier = ZERO
state = HIDDEN/REDUCED
```

Narrative:

> Cuối dãy vẫn mang trường Thiên Y,
> nhưng khả năng biểu hiện của tài khí
> hoặc kết quả có xu hướng bị giảm,
> ẩn hoặc khó phát huy hoàn toàn.

Không được viết:

> không có Thiên Y.

---

# 45. TAIL WITH FIVE EXAMPLE

Input:

```text
...135
```

Resolve:

```text
13 = TIAN_Y_T1
5 = POST modifier
```

Tail State:

```text
TIAN_Y_AMPLIFIED
```

Narrative:

> Trường Thiên Y ở cuối dãy được làm nổi bật,
> vì vậy tài nguyên, thành quả hoặc yếu tố quan hệ
> có khả năng trở thành điểm nhấn của cấu trúc.

---

# 46. TAIL WITH FU_WEI EXAMPLE

Input concept:

```text
LIU_SHA → FU_WEI
```

at tail.

Final:

```text
EXTENDED_LIU_SHA
```

Narrative:

> Trạng thái cảm xúc và quan hệ của Lục Sát
> có xu hướng kéo dài tới cuối dãy,
> vì vậy cần chú ý khả năng do dự
> hoặc quan hệ thiếu ổn định.

---

# 47. GOOD PROCESS / BAD TAIL

Example concept:

```text
SHENG_QI
→
TIAN_Y
→
WU_GUI
```

Process:

- quý nhân;
- tạo tài.

Tail:

- Ngũ Quỷ.

Interpretation:

> Quá trình có cơ hội và tài nguyên,
> nhưng trạng thái cuối còn biến động.

Không được kết luận đơn giản:

> có 2 cát 1 hung = tốt.

---

# 48. CHALLENGING PROCESS / GOOD TAIL

Example:

```text
HUO_HAI
→
TIAN_Y
```

Interpretation:

> Họa Hại được sử dụng như khẩu tài,
> sau đó quy về Thiên Y.

Có thể là:

```text
communication
→
wealth
```

Đây là ví dụ canonical của:

```text
CHALLENGING AS TOOL
→
AUSPICIOUS RESULT
```

---

# 49. MULTIPLE CHALLENGING ENERGIES NEAR TAIL

Nếu:

```text
CHALLENGING
→
CHALLENGING
```

xuất hiện ở cuối,

risk prominence tăng.

Ví dụ:

```text
JUE_MING → WU_GUI
```

near tail:

- risk;
- volatility.

Nếu cả hai strong:

```text
TAIL_RISK_PROMINENCE = HIGH
```

Nhưng final narrative vẫn phải xét
có remedy tiếp sau hay không.

---

# 50. REMEDY AFTER TAIL-HUNG

Nếu Hung không phải terminal
mà còn trường chế hóa phía sau:

Ví dụ:

```text
WU_GUI → SHENG_QI
```

thì không gọi WU_GUI là Tail Hung.

Terminal là SHENG_QI.

Order > raw proximity.

---

# 51. REMEDY BEFORE HUNG

Ví dụ:

```text
SHENG_QI → WU_GUI
```

không được coi Sinh Khí đã chế xong Ngũ Quỷ
chỉ vì cả hai cùng có mặt.

Control direction phải theo
`07_CONTROL_REMEDY_RULES.md`.

Position MUST preserve order.

---

# 52. CUSTOMER TAIL LANGUAGE

Không hiển thị:

> Đuôi này đại hung.

> Số đuôi này chắc chắn phá tài.

Recommended:

> Phần cuối dãy quy về trường Ngũ Quỷ,
> vì vậy yếu tố biến động và thay đổi vẫn còn
> khá rõ trong trạng thái cuối của cấu trúc.

Hoặc:

> Phần đuôi quy về Thiên Y,
> giúp toàn dãy có xu hướng kết thúc
> ở trạng thái thiên về tài nguyên và thành quả.

---

# 53. TAIL SUMMARY LEVELS

Recommended internal labels:

```text
FAVORABLE_CONVERGENCE
BALANCED_CONVERGENCE
MIXED_CONVERGENCE
CHALLENGING_CONVERGENCE
HIDDEN_CONVERGENCE
AMPLIFIED_CONVERGENCE
```

Không hiển thị raw enum cho khách.

---

# 54. POSITION STATUS

Recommended:

```text
PositionStatus {
    zone
    positional_weight

    is_tail
    is_terminal

    distance_to_tail

    preferred_for_energy
    position_fit
}
```

`position_fit`:

```text
PREFERRED
ACCEPTABLE
CONTEXTUAL
UNFAVORABLE
```

Chỉ dùng khi canonical rule tồn tại.

---

# 55. POSITION FIT — CURRENT V1

V1 canonical preferences:

```text
SHENG_QI:
MIDDLE = PREFERRED
TAIL = ACCEPTABLE

TIAN_Y:
REAR = PREFERRED
TAIL = PREFERRED

YAN_NIAN:
REAR = PREFERRED
TAIL = PREFERRED

FU_WEI:
CONTEXTUAL

HUO_HAI:
MIDDLE = FUNCTIONAL
TAIL = CHALLENGING

WU_GUI:
MIDDLE = FUNCTIONAL
TAIL = CHALLENGING

LIU_SHA:
MIDDLE = FUNCTIONAL
TAIL = CHALLENGING

JUE_MING:
MIDDLE = FUNCTIONAL
TAIL = CHALLENGING
```

Đây là V1 policy.

Không mở rộng ngoài dữ liệu đã khóa.

---

# 56. POSITION AND BALANCE

Preferred composition:

```text
AUSPICIOUS MASTER
+
FUNCTIONAL CHALLENGING MIDDLE
+
CONTROL / TRANSFORMATION
+
AUSPICIOUS REAR/TAIL
```

Đây là kiến trúc lý tưởng
theo Knowledge hiện tại.

Không phải template bắt buộc cho mọi dãy.

---

# 57. "CÁT TINH LÀM CHỦ"

Để xác định Cát làm chủ,
không chỉ đếm số lượng.

Cần xét:

```text
strength
position
repetition
terminal state
modifier
control
```

Một Cát mạnh ở cuối
có thể có vai trò lớn
hơn nhiều Cát yếu ở đầu.

---

# 58. "HUNG TINH LÀM DỤNG"

Hung được coi là functional khi:

1. không chiếm dominant terminal role;
2. có domain use rõ;
3. chuyển về một trường phù hợp;
4. không bị amplification bất lợi;
5. nếu cần, có control/remedy.

Ví dụ:

```text
HUO_HAI → TIAN_Y
```

functional.

```text
HUO_HAI → HUO_HAI → FU_WEI
```

near tail có thể không functional,
mà là extended argument pattern.

---

# 59. TAIL RULE FOR WEALTH

Thiên Y ở vùng cuối
có thể tăng prominence cho Wealth Domain.

Nhưng phải xét:

```text
previous_energy
```

để biết nguồn tài.

Ví dụ:

```text
WU_GUI → TIAN_Y
```

near tail:

> trí tuệ/sáng tạo tạo thành quả tài chính.

```text
HUO_HAI → TIAN_Y
```

near tail:

> giao tiếp tạo thành quả tài chính.

---

# 60. TAIL RULE FOR CAREER

Diên Niên ở vùng cuối
tăng prominence cho Career Domain.

Phải xét previous:

```text
previous → YAN_NIAN
```

để xác định loại kỹ năng.

Ví dụ:

```text
LIU_SHA → YAN_NIAN
```

near tail:

> dịch vụ/giao tiếp → nghề nghiệp.

---

# 61. TAIL RULE FOR RELATIONSHIP

Thiên Y/Lục Sát near tail
có thể tăng Relationship prominence.

Nhưng:

```text
TIAN_Y
```

và:

```text
LIU_SHA
```

không được luận giống nhau.

Thiên Y:

- chính Đào Hoa;
- ổn định;
- kết quả quan hệ.

Lục Sát:

- cảm xúc;
- duyên;
- phức tạp;
- dễ dao động.

---

# 62. TAIL RULE FOR VEHICLE PLATE

Đối với biển số xe,
Tail Narrative KHÔNG ưu tiên:

- hôn nhân;
- Đào Hoa.

Ưu tiên:

- ổn định;
- công việc;
- tài vận;
- vận động;
- risk/balance;
- terminal energy.

Same knowledge,
different profile.

---

# 63. SEQUENCE LENGTH NORMALIZATION

Engine phải hỗ trợ:

```text
PHONE:
long sequence

CAR PLATE:
short sequence

MOTORBIKE PLATE:
short sequence
```

Không dùng cùng absolute index logic.

Recommended:

```text
normalized_position =
index / sequence_length
```

sau đó map zone.

---

# 64. SHORT-SEQUENCE RULE

Nếu dãy quá ngắn,
ví dụ 4–5 số,

mỗi interaction có trọng số cao.

Recommended:

```text
FIRST
MIDDLE
LAST
```

thay vì HEAD/MIDDLE/REAR/TAIL đầy đủ.

Last interaction vẫn là terminal interaction.

---

# 65. ONE-INTERACTION CASE

Nếu chỉ có một valid interaction:

```text
A → B
```

thì interaction đó đồng thời là:

```text
PRIMARY
TERMINAL
```

Không invent additional structure.

---

# 66. INVALID POSITION IMPLEMENTATIONS

Forbidden:

```text
only analyze last 4 digits
```

Forbidden:

```text
tail overrides everything
```

Forbidden:

```text
same pair always means same final result
```

Forbidden:

```text
challenging energy at middle = automatic bad
```

Forbidden:

```text
auspicious energy at tail = guaranteed fortune
```

Forbidden:

```text
trim trailing 0
```

Forbidden:

```text
ignore modifier at terminal
```

---

# 67. POSITION RUNTIME PIPELINE

Canonical:

```text
NORMALIZED DIGITS
↓
PAIR RESOLUTION
↓
ENERGY + STRENGTH
↓
DIRECTED INTERACTIONS
↓
MODIFIER STATES
↓
POSITION INDEXING
↓
ZONE ASSIGNMENT
↓
DISTANCE TO TAIL
↓
TERMINAL STATE
↓
CONTROL / REMEDY
↓
DOMAIN
↓
WHOLE-SEQUENCE SYNTHESIS
```

---

# 68. POSITION TEST — 813

Input:

```text
813
```

Pairs:

```text
81 = WU_GUI
13 = TIAN_Y
```

Interaction:

```text
WU_GUI → TIAN_Y
```

Because only one interaction:

```text
interaction_role = PRIMARY + TERMINAL
```

Expected:

```text
terminal_energy = TIAN_Y
```

Not:

```text
terminal_energy = WU_GUI
```

---

# 69. POSITION TEST — 318

Input:

```text
318
```

Pairs:

```text
31 = TIAN_Y
18 = WU_GUI
```

Terminal:

```text
WU_GUI
```

Therefore:

```text
318
!=
813
```

even though both contain
Thiên Y + Ngũ Quỷ.

---

# 70. POSITION TEST — 103

Input:

```text
103
```

Underlying:

```text
13 = TIAN_Y
```

Modifier:

```text
ZERO INTERPOSED
```

Terminal State:

```text
TIAN_Y_HIDDEN
```

Not:

```text
TIAN_Y_NORMAL
```

---

# 71. POSITION TEST — 135

Input:

```text
135
```

Underlying:

```text
13 = TIAN_Y
```

5 POST.

Terminal:

```text
TIAN_Y_AMPLIFIED
```

---

# 72. POSITION TEST — 181

Input:

```text
181
```

Pairs:

```text
18 = WU_GUI_T1
81 = WU_GUI_T1
```

Interaction:

```text
WU_GUI → WU_GUI
```

Terminal:

```text
WU_GUI
```

State:

```text
REINFORCED_WU_GUI
```

Prominence:

HIGH.

---

# 73. POSITION TEST — 131

Input:

```text
131
```

Pairs:

```text
13 = TIAN_Y_T1
31 = TIAN_Y_T1
```

Interaction:

```text
TIAN_Y → TIAN_Y
```

Terminal:

```text
TIAN_Y
```

State:

```text
REINFORCED_TIAN_Y
```

---

# 74. POSITION TEST — HUO_HAI → TIAN_Y

Example:

```text
713
```

Pairs:

```text
71 = HUO_HAI
13 = TIAN_Y
```

Terminal:

```text
TIAN_Y
```

Interpretation:

```text
communication
→
wealth/result
```

Preferred convergence.

---

# 75. POSITION TEST — TIAN_Y → HUO_HAI

Example:

```text
317
```

Pairs:

```text
31 = TIAN_Y
17 = HUO_HAI
```

Terminal:

```text
HUO_HAI
```

Interpretation:

```text
resource
→
speech/social expenditure/controversy
```

Must NOT equal 713.

---

# 76. CUSTOMER SUMMARY CONTRACT

Customer summary should describe:

1. dominant energy;
2. important middle process;
3. terminal state;
4. whether terminal is:
   - supported;
   - hidden;
   - amplified;
   - controlled;
   - extended.

Example:

> Dãy số có quá trình vận động thiên về
> giao tiếp và khả năng tạo tài,
> trong khi phần cuối quy về Thiên Y.
> Điều này giúp tài nguyên và thành quả
> trở thành điểm nhấn rõ của cấu trúc.

---

# 77. EXPERT TRACE

Expert Mode may show:

```text
Position Trace

Pair 1:
index 0–1
zone HEAD

Pair 2:
index 1–2
zone MIDDLE

...

Final Interaction:
INT-WG-TY

Terminal Energy:
TIAN_Y

Terminal Modifier:
NONE

Distance to tail:
0
```

Customer Mode MUST NOT expose
low-level implementation unless requested.

---

# 78. ENGINE BOUNDARY

File này chịu trách nhiệm:

```text
ENERGY / INTERACTION
→
POSITIONAL MEANING
→
TAIL / TERMINAL STATE
```

File này KHÔNG chịu trách nhiệm:

- control/remedy truth;
- final domain narrative;
- customer wording library;
- owner compatibility;
- final score.

---

# 79. NEXT DEPENDENCY

Output của file này
được dùng trực tiếp bởi:

```text
07_CONTROL_REMEDY_RULES.md
08_CHAIN_INTERPRETATION_RULES.md
09_DOMAIN_INTERPRETATION.md
10_CUSTOMER_NARRATIVE_CATALOG.md
11_ACCEPTANCE_GOLDEN_CASES.md
```

---

# 80. FREEZE RULE

Once accepted:

`06_POSITION_AND_TAIL_RULES.md`

becomes canonical source of truth
for:

- HEAD;
- MIDDLE;
- REAR;
- TAIL;
- TERMINAL;
- distance-to-tail;
- positional prominence;
- preferred energy placement;
- tail convergence;
- terminal state semantics.

Cursor MUST NOT:

- invent new position meaning;
- hard-code last four digits only;
- ignore whole sequence;
- let tail completely override chain;
- trim semantic zero;
- ignore terminal modifier;
- automatically classify tail Hung as fatal;
- automatically classify tail Cát as guaranteed success.

Any change requires:

1. expert review;
2. canonical document update;
3. version bump;
4. regression tests;
5. Golden Dataset update.

---

# END OF DOCUMENT
```

Với `06` này, chúng ta đã khóa được một điểm rất quan trọng cho engine: **“đường đi” và “nơi đến” là hai lớp khác nhau**. Một dãy có thể có quá trình rất đẹp nhưng kết thúc ở trạng thái biến động, hoặc có phần giữa dùng Hung làm công cụ nhưng cuối cùng quy về Cát; hai trường hợp đó phải được luận hoàn toàn khác nhau.