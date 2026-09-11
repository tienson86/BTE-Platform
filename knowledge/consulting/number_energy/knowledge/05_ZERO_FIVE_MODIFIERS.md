Được. `05_ZERO_FIVE_MODIFIERS.md` phải khóa riêng cơ chế của **0 và 5**, vì đây là hai chữ số đặc biệt không được xử lý như tám quái số thông thường. File này cần phân biệt rất rõ `AB0`, `A0B`, `0AB` và tương tự với `5`, đồng thời không được hiểu 0 = xấu tuyệt đối hay 5 = tốt tuyệt đối.

```markdown
# 05_ZERO_FIVE_MODIFIERS.md

# BTE NUMBER ENERGY — ZERO / FIVE MODIFIER STANDARD

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Zero / Five Modifier Standard  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** CORE KNOWLEDGE  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`

**Depends On:**
- `01_BAGUA_DIGIT_MAPPING.md`
- `02_EIGHT_ENERGY_CATALOG.md`
- `03_PAIR_STRENGTH_MATRIX.md`
- `04_DIRECTED_INTERACTION_MATRIX.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa canonical behavior
của hai chữ số đặc biệt:

```text
0
5
```

trong Bát Cực Linh Số.

Hai chữ số này KHÔNG được xử lý như
các quái số:

```text
1 2 3 4 6 7 8 9
```

Mục tiêu:

SPECIAL DIGIT
↓
POSITION
↓
UNDERLYING ENERGY
↓
MODIFIER STATE
↓
INTERPRETATION CHANGE
↓
FINAL NARRATIVE

---

# 2. CORE CLASSIFICATION

Canonical:

```text
0 = YIN MODIFIER
5 = YANG MODIFIER
```

Internal IDs:

```text
ZERO
FIVE
```

Modifier Classes:

```text
ZERO_MODIFIER
FIVE_MODIFIER
```

---

# 3. ZERO — CORE SEMANTIC

Canonical polarity:

```text
YIN
```

Canonical behavior:

```text
HIDDEN
CONCEALED
REDUCED_EXPRESSION
INTERNALIZED
DELAYED
BLOCKED
INTERRUPTED
```

Số 0 thường làm trường khí:

- giảm khả năng biểu hiện ra ngoài;
- chuyển từ hiển sang ẩn;
- khó phát huy;
- trì hoãn;
- bị che;
- bị mắc kẹt;
- khó nhận thấy kết quả.

Important:

```text
ZERO != DELETE ENERGY
```

0 không mặc nhiên xóa trường khí.

Đúng hơn:

```text
ENERGY + ZERO
→
ENERGY_IN_HIDDEN_OR_REDUCED_STATE
```

---

# 4. FIVE — CORE SEMANTIC

Canonical polarity:

```text
YANG
```

Canonical behavior:

```text
EXPLICIT
ACTIVE
AMPLIFIED
VISIBLE
STRENGTHENED
EXTENDED
```

Số 5 thường làm trường khí:

- biểu hiện rõ;
- nổi bật;
- được kích hoạt;
- tăng khả năng phát huy;
- tăng tính chủ động;
- kéo dài hoặc làm trường khí mạnh hơn.

Important:

```text
FIVE != ALWAYS GOOD
```

Nếu 5 tác động lên Hung trường:

```text
CHALLENGING ENERGY + FIVE
```

có thể làm đặc tính bất lợi
biểu hiện mạnh hơn.

---

# 5. ZERO / FIVE ARE MODIFIERS, NOT DU NIEN

Canonical:

```text
0 != FU_WEI
5 != FU_WEI
```

Không được gán:

```text
10
15
50
05
```

thành một trong tám Du Niên
chỉ vì hai chữ số đứng cạnh nhau.

Resolver MUST nhận diện
underlying Bagua relationship
nếu cấu trúc cho phép.

---

# 6. POSITION IS SEMANTIC

Phải phân biệt:

## Zero

```text
AB0
A0B
0AB
```

## Five

```text
AB5
A5B
5AB
```

Các cấu trúc trên
KHÔNG được xử lý giống nhau.

---

# 7. POST-MODIFIER MODEL

## 7.1 AB0

Ví dụ:

```text
130
```

Underlying pair:

```text
13 = TIAN_Y
```

Structure:

```text
TIAN_Y
→
ZERO
```

Canonical:

```text
formed_energy
→
hidden / weakened expression
```

Meaning tendency:

- trường đã hình thành;
- sau đó bị ẩn;
- kết quả khó biểu hiện;
- năng lượng có nhưng khó phát huy.

---

## 7.2 AB5

Ví dụ:

```text
135
```

Underlying pair:

```text
13 = TIAN_Y
```

Structure:

```text
TIAN_Y
→
FIVE
```

Canonical:

```text
formed_energy
→
explicit / amplified
```

Meaning tendency:

- trường đã hình thành;
- sau đó được đẩy mạnh;
- biểu hiện rõ hơn;
- khả năng phát huy cao hơn.

---

# 8. INTERPOSED-MODIFIER MODEL

## 8.1 A0B

Ví dụ:

```text
103
```

Underlying relation:

```text
1 ↔ 3 = TIAN_Y
```

Nhưng 0 chen giữa.

Canonical:

```text
A
→ ZERO
→ B

potential_energy(A,B)
→ hidden / interrupted
```

Meaning tendency:

- trường khí tồn tại ở dạng ẩn;
- khó biểu hiện trực tiếp;
- có yếu tố kín;
- kết quả không dễ nhìn thấy.

Không được parse:

```text
10 + 03
```

như hai pair Du Niên bình thường.

---

## 8.2 A5B

Ví dụ:

```text
153
```

Underlying relation:

```text
1 ↔ 3 = TIAN_Y
```

5 chen giữa.

Canonical:

```text
A
→ FIVE
→ B

potential_energy(A,B)
→ explicit / activated
```

Meaning tendency:

- trường khí được đưa ra ngoài;
- biểu hiện rõ;
- dễ nhìn thấy;
- chủ động hơn.

---

# 9. PRE-MODIFIER MODEL

## 9.1 0AB

Ví dụ:

```text
013
```

Underlying:

```text
13 = TIAN_Y
```

Canonical tendency:

```text
ZERO
→ TIAN_Y
```

Interpretation:

- trường Thiên Y vẫn tồn tại;
- nhưng trạng thái khởi phát có tính ẩn,
  chậm hoặc kín.

Không được coi 0 là một pair độc lập.

---

## 9.2 5AB

Ví dụ:

```text
513
```

Canonical tendency:

```text
FIVE
→ TIAN_Y
```

Interpretation:

- Thiên Y được khởi phát theo hướng chủ động;
- trường khí có tính hiển lộ mạnh hơn.

---

# 10. MODIFIER STATE ENUM

Canonical states:

```text
NORMAL
HIDDEN
AMPLIFIED
INTERRUPTED
EXTENDED
REDUCED
INTERNALIZED
EXPLICIT
```

Recommended normalized runtime:

```text
NORMAL
HIDDEN
AMPLIFIED
```

và detail flags:

```text
delayed
blocked
internalized
extended
visible
active
```

---

# 11. ZERO DOES NOT ALWAYS MEAN NEGATIVE

Important:

```text
ZERO != BAD
```

0 có thể:

- làm trường khí ẩn;
- làm giảm biểu hiện;
- làm chậm kết quả;
- làm năng lượng mang tính nội tại.

Với một số trường:

```text
HIDDEN
```

có thể làm bất lợi giảm biểu hiện ra ngoài.

Nhưng với một số trường cát:

```text
HIDDEN
```

cũng có thể làm lợi ích khó phát huy.

Do đó:

```text
ZERO EFFECT
=
CONTEXTUAL
```

---

# 12. FIVE DOES NOT ALWAYS MEAN POSITIVE

Important:

```text
FIVE != GOOD
```

5 khuếch đại thứ nó tác động.

Nếu:

```text
GOOD ENERGY + FIVE
```

có thể tăng biểu hiện thuận.

Nếu:

```text
CHALLENGING ENERGY + FIVE
```

có thể làm:

- biến động mạnh hơn;
- thị phi mạnh hơn;
- cảm xúc mạnh hơn;
- hành động cực đoan hơn.

Do đó:

```text
FIVE EFFECT
=
AMPLIFY TARGET
```

không phải:

```text
ADD GOODNESS
```

---

# 13. THIÊN Y + ZERO / FIVE

Thiên Y canonical:

```text
wealth
relationship
resource
```

## 13.1 103

```text
1 - 0 - 3
```

Underlying:

```text
13 = TIAN_Y
```

Canonical interpretation:

```text
TIAN_Y
state = HIDDEN
```

Wealth tendency:

- tài khí tồn tại nhưng khó phát huy;
- tiền/tài nguyên có thể bị khóa;
- thanh khoản kém;
- khó thu hồi tài nguyên.

Relationship tendency:

- tình cảm khó biểu đạt;
- trạng thái tình cảm kín;
- khó nhìn rõ.

Không được kết luận:

> ngoại tình

chỉ từ `103`.

---

## 13.2 153

```text
1 - 5 - 3
```

Underlying:

```text
13 = TIAN_Y
```

Canonical:

```text
TIAN_Y
state = AMPLIFIED / EXPLICIT
```

Meaning:

- tài khí biểu hiện rõ hơn;
- tình cảm dễ bộc lộ;
- trường Thiên Y dễ được nhận thấy.

---

## 13.3 130

```text
13 → 0
```

Canonical:

```text
formed TIAN_Y
→ reduced / hidden
```

Meaning:

- lợi ích Thiên Y ban đầu hình thành;
- sau đó biểu hiện giảm.

---

## 13.4 135

```text
13 → 5
```

Canonical:

```text
formed TIAN_Y
→ amplified
```

Meaning:

- Thiên Y tiếp tục được đẩy mạnh;
- tài/tình dễ biểu hiện rõ hơn.

---

# 14. SINH KHÍ + ZERO / FIVE

Canonical example:

## 104

```text
1 - 0 - 4
```

Underlying:

```text
14 = SHENG_QI
```

Interpretation:

```text
SHENG_QI
state = HIDDEN
```

Meaning:

- quý nhân/trợ lực khó nhìn thấy;
- có cơ hội nhưng chưa chắc nhận biết;
- hỗ trợ có thể đến theo cách gián tiếp.

Không được nói:

> 104 chắc chắn có tiểu nhân.

Nếu Knowledge Source có ghi,
chỉ giữ ở expert reference.

---

## 154

```text
1 - 5 - 4
```

Underlying:

```text
14 = SHENG_QI
```

Meaning:

```text
SHENG_QI
state = EXPLICIT
```

- quý nhân dễ xuất hiện;
- cơ hội rõ;
- trợ lực dễ nhận biết.

---

## 140

```text
14 → 0
```

Meaning:

- Sinh Khí hình thành;
- sau đó khả năng phát huy giảm.

---

## 145

```text
14 → 5
```

Meaning:

- Sinh Khí được khuếch đại;
- quý nhân/cơ hội tăng biểu hiện.

---

# 15. DIÊN NIÊN + ZERO / FIVE

## 109

Underlying:

```text
19 = YAN_NIAN
```

0 chen giữa.

Meaning:

- năng lực có nhưng khó phát huy;
- chuyên môn khó được nhìn thấy;
- công việc có cảm giác bị giữ lại.

---

## 159

Underlying:

```text
19 = YAN_NIAN
```

5 chen giữa.

Meaning:

- năng lực được hiển;
- chuyên môn dễ thấy;
- khả năng chủ động cao hơn.

---

## 190

```text
19 → 0
```

Meaning:

- năng lực hình thành;
- sau đó suy giảm khả năng biểu hiện;
- công việc có thể bị trì hoãn hoặc khó phát huy.

---

## 195

```text
19 → 5
```

Meaning:

- Diên Niên tăng biểu hiện;
- chuyên môn/quyền hạn/công việc được đẩy mạnh.

---

# 16. CHALLENGING ENERGY + ZERO

Zero làm Hung trường
chuyển sang trạng thái:

```text
HIDDEN
INTERNALIZED
DELAYED
```

Không được hiểu:

```text
Hung + 0 = hết Hung
```

Ví dụ:

```text
108
```

Underlying:

```text
18 = WU_GUI
```

0 chen giữa:

```text
1 - 0 - 8
```

Canonical:

```text
WU_GUI
state = HIDDEN / INTERNALIZED
```

Meaning tendency:

- suy nghĩ nhiều nhưng ít thể hiện;
- biến động nội tại;
- ý tưởng/lo lắng mang tính kín;
- khó đoán.

---

# 17. CHALLENGING ENERGY + FIVE

Five làm Hung trường:

```text
VISIBLE
ACTIVE
AMPLIFIED
```

Ví dụ:

nếu underlying là:

```text
WU_GUI
```

gặp 5:

- biến động biểu hiện mạnh hơn;
- phản ứng nhanh hơn;
- tư duy thay đổi rõ hơn;
- bất ổn cũng dễ lộ rõ hơn.

Do đó:

```text
WU_GUI + FIVE
```

không được tự động coi là tốt.

---

# 18. ZERO AND TAIL POSITION

Nguồn Knowledge coi số 0
ở phần cuối dãy là cần lưu ý.

Canonical:

```text
TAIL_ZERO
=
OUTCOME_REDUCTION_OR_HIDDENNESS
```

Possible interpretation:

- kết quả khó tụ;
- năng lượng cuối dãy bị ẩn;
- thành quả khó biểu hiện trọn vẹn.

Không được nói:

> số kết thúc 0 = chắc chắn xấu.

Tail weighting thuộc:

`06_POSITION_AND_TAIL_RULES.md`

---

# 19. FIVE AND TAIL POSITION

5 ở cuối dãy có thể:

- khuếch đại trạng thái trước;
- làm kết quả biểu hiện rõ hơn;
- nhưng nếu trạng thái trước là Hung,
  cũng có thể khuếch đại Hung.

Canonical:

```text
TAIL_FIVE
=
AMPLIFY_PREVIOUS_TERMINAL_STATE
```

---

# 20. ZERO / FIVE WITH PHỤC VỊ

Không được merge modifier rule
với Phục Vị rule.

Phục Vị:

```text
EXTEND PREVIOUS ENERGY
```

0:

```text
HIDE / REDUCE EXPRESSION
```

5:

```text
EXPOSE / AMPLIFY
```

Ba operator khác nhau.

Ví dụ:

```text
18 → 88
```

khác:

```text
180
```

và khác:

```text
185
```

Engine MUST preserve operator type.

---

# 21. ZERO / FIVE WITH CONTROL RULES

Modifier không được làm mất
Control/Remedy logic.

Ví dụ:

```text
WU_GUI
→
SHENG_QI
```

vẫn là control relation.

Nhưng nếu:

```text
WU_GUI
→
SHENG_QI
→
0
```

thì phải xét:

- Sinh Khí có hình thành không?
- Sinh Khí có bị giảm biểu hiện bởi 0 không?
- mức chế Ngũ Quỷ có bị giảm không?

Chi tiết final effect thuộc
`07_CONTROL_REMEDY_RULES.md`.

---

# 22. MODIFIER PRIORITY

Recommended processing order:

```text
1. identify raw digits
2. identify active Bagua digits
3. identify potential underlying pair
4. detect 0 / 5 modifier position
5. resolve underlying Energy
6. attach Strength Tier
7. apply modifier state
8. build Directed Interaction
9. apply Position rules
10. apply Control/Remedy
11. Domain interpretation
12. Narrative
```

Không được resolve narrative trước modifier.

---

# 23. MULTIPLE MODIFIERS

Ví dụ:

```text
1053
```

có:

```text
0
5
```

trong cùng structure.

Không được simplify thành:

```text
0 cancels 5
```

hoặc:

```text
5 cancels 0
```

MUST preserve sequence.

Recommended representation:

```text
ModifierChain [
  ZERO,
  FIVE
]
```

Final interpretation phải xét:

- thứ tự;
- vị trí;
- energy context.

---

# 24. MULTIPLE ZERO

Ví dụ:

```text
1003
```

Canonical tendency:

```text
hiddenness ↑
delay ↑
visibility ↓
```

Không được mặc định:

```text
two_zero = twice_bad
```

Recommended:

```text
zero_density
```

là một feature riêng.

---

# 25. MULTIPLE FIVE

Ví dụ:

```text
1553
```

Canonical tendency:

```text
activation ↑
explicitness ↑
amplification ↑
```

Nhưng final effect phụ thuộc
trường bị khuếch đại.

---

# 26. ZERO / FIVE DENSITY

Recommended metrics:

```text
zero_count
five_count
zero_ratio
five_ratio
```

Nhưng các metric này
KHÔNG được dùng độc lập để kết luận tốt/xấu.

---

# 27. EXAMPLE — 856 VS 806

Nguồn Knowledge đưa cặp so sánh:

```text
856
806
```

Canonical reading:

## 856

5 làm trạng thái phía sau
biểu hiện theo hướng hiển/chủ động.

Nguồn liên hệ với tài phú có biểu hiện
nhưng đi cùng quá trình lao động/nỗ lực.

## 806

0 làm trạng thái phía sau
ẩn hoặc bị khóa.

Nguồn liên hệ với tài khí
khó biểu hiện hoặc bị mắc kẹt.

Important:

Không hard-code:

```text
856 = good
806 = bad
```

MUST resolve full sequence.

---

# 28. SOURCE PATTERN — 103 / 301 / 608 / 806

Knowledge Source liên hệ
các tổ hợp này với:

```text
hidden relationship
```

Canonical engine label:

```text
RELATIONSHIP_VISIBILITY = HIDDEN
```

Không dùng:

```text
AFFAIR = TRUE
```

Customer Narrative:

> Trường tình cảm có xu hướng kín,
> khó biểu đạt hoặc khó được nhìn thấy rõ.

---

# 29. SOURCE PATTERN — FINANCIAL LOCK

Các cấu trúc Thiên Y + 0
có thể liên quan:

- tài nguyên bị khóa;
- tiền khó quay vòng;
- cho vay khó thu;
- đầu tư khó phát huy.

Canonical label:

```text
RESOURCE_LIQUIDITY_RISK
```

Không được nói:

> chắc chắn mất tiền.

---

# 30. SOURCE PATTERN — HIDDEN WU_GUI

Ngũ Quỷ + 0:

Canonical:

```text
MENTAL_ACTIVITY = HIGH
EXTERNAL_VISIBILITY = LOW
```

Possible narrative:

> Dãy số cho thấy tư duy hoạt động mạnh nhưng
> phần lớn diễn ra bên trong; người sử dụng có thể
> suy nghĩ nhiều hơn mức thể hiện ra bên ngoài.

---

# 31. ZERO / FIVE CUSTOMER LANGUAGE

Không dùng các câu:

> số 0 triệt tiêu tất cả.

> số 5 làm mọi thứ tốt hơn.

Recommended:

### Zero

> Số 0 làm trường khí chuyển sang trạng thái
> ẩn hoặc giảm khả năng biểu hiện,
> vì vậy cần xem trường nào đang bị tác động.

### Five

> Số 5 có tác dụng làm nổi bật và tăng khả năng
> biểu hiện của trường khí đứng trong cấu trúc,
> nên lợi hay bất lợi còn phụ thuộc trường được khuếch đại.

---

# 32. EXPERT MODE

Expert Mode có thể hiển thị:

```text
Input: 103

Underlying pair:
13 = TIAN_Y / Tier 1

Modifier:
ZERO

Modifier position:
INTERPOSED

State:
HIDDEN

Interpretation key:
TIAN_Y_HIDDEN
```

Customer Mode chỉ hiển thị narrative.

---

# 33. RUNTIME DATA CONTRACT

Recommended:

```text
ModifierResult {
    modifier_id
    digit
    modifier_type

    position_type

    underlying_pair
    underlying_energy
    underlying_strength

    state

    visibility_effect
    activation_effect
    continuity_effect

    notes
}
```

Position types:

```text
PRE
INTERPOSED
POST
TERMINAL
```

---

# 34. ZERO OBJECT

```text
{
  modifier_id: "ZERO",
  digit: 0,
  polarity: "YIN",
  default_state: "HIDDEN",

  effects: [
    "REDUCE_VISIBILITY",
    "INTERNALIZE",
    "DELAY",
    "BLOCK"
  ]
}
```

---

# 35. FIVE OBJECT

```text
{
  modifier_id: "FIVE",
  digit: 5,
  polarity: "YANG",
  default_state: "AMPLIFIED",

  effects: [
    "INCREASE_VISIBILITY",
    "ACTIVATE",
    "AMPLIFY",
    "EXTEND"
  ]
}
```

---

# 36. TEST CASE — 103

Input:

```text
103
```

Expected:

```text
underlying_pair = 13
energy = TIAN_Y
strength = TIER_1
modifier = ZERO
modifier_position = INTERPOSED
state = HIDDEN
```

MUST NOT resolve:

```text
10 = ?
03 = ?
```

as normal Du Niên.

---

# 37. TEST CASE — 153

Input:

```text
153
```

Expected:

```text
underlying_pair = 13
energy = TIAN_Y
strength = TIER_1
modifier = FIVE
modifier_position = INTERPOSED
state = AMPLIFIED
```

---

# 38. TEST CASE — 130

Expected:

```text
13 = TIAN_Y
0 = POST modifier

state:
REDUCED / HIDDEN
```

---

# 39. TEST CASE — 135

Expected:

```text
13 = TIAN_Y
5 = POST modifier

state:
AMPLIFIED
```

---

# 40. TEST CASE — 104

Expected:

```text
14 = SHENG_QI
0 = INTERPOSED
state = HIDDEN
```

---

# 41. TEST CASE — 154

Expected:

```text
14 = SHENG_QI
5 = INTERPOSED
state = AMPLIFIED
```

---

# 42. TEST CASE — 109

Expected:

```text
19 = YAN_NIAN
0 = INTERPOSED
state = HIDDEN
```

---

# 43. TEST CASE — 159

Expected:

```text
19 = YAN_NIAN
5 = INTERPOSED
state = AMPLIFIED
```

---

# 44. TEST CASE — 108

Expected:

```text
18 = WU_GUI
0 = INTERPOSED
state = HIDDEN / INTERNALIZED
```

MUST NOT conclude:

```text
WU_GUI removed
```

---

# 45. INVALID IMPLEMENTATIONS

The following implementations are forbidden:

```text
0 always = bad
5 always = good
```

Forbidden:

```text
0 removes all adjacent energy
```

Forbidden:

```text
5 converts bad energy into good
```

Forbidden:

```text
0 or 5 treated as normal Bagua digit
```

Forbidden:

```text
103 parsed only as 10 + 03
```

Forbidden:

```text
A0B = AB0
```

Forbidden:

```text
A5B = AB5
```

---

# 46. CUSTOMER SAFETY

Một số Knowledge Source
gán cấu trúc có 0/5 với:

- bệnh nặng;
- tai nạn;
- tử vong;
- ngoại tình;
- ly hôn;
- lừa đảo;
- các kết luận định mệnh.

Các claim này:

```text
MUST NOT
```

được customer engine dùng
như deterministic prediction.

Allowed:

> Theo hệ thống này, cấu trúc làm tăng
> tính ẩn, biến động hoặc khó biểu đạt
> của trường liên quan.

Not allowed:

> Người này chắc chắn ngoại tình.

> Số này gây tai nạn.

---

# 47. ENGINE BOUNDARY

File này chịu trách nhiệm:

```text
0 / 5
→
MODIFIER STATE
```

File này KHÔNG chịu trách nhiệm:

- final tail score;
- remedy;
- owner compatibility;
- whole sequence;
- phone vs vehicle weighting;
- final recommendation.

---

# 48. DEPENDENCIES FOR NEXT STAGES

Output của file này được dùng bởi:

```text
06_POSITION_AND_TAIL_RULES.md
07_CONTROL_REMEDY_RULES.md
08_CHAIN_INTERPRETATION_RULES.md
09_DOMAIN_INTERPRETATION.md
10_CUSTOMER_NARRATIVE_CATALOG.md
```

---

# 49. FREEZE RULE

Once accepted:

`05_ZERO_FIVE_MODIFIERS.md`

becomes canonical source of truth
for all 0 / 5 behavior.

Cursor MUST NOT:

- tự định nghĩa ý nghĩa số 0;
- tự định nghĩa ý nghĩa số 5;
- coi 0 là triệt tiêu tuyệt đối;
- coi 5 là cát tinh;
- bỏ qua vị trí modifier;
- tự merge modifier với Phục Vị;
- tạo narrative mới ngoài canonical knowledge.

Any change requires:

1. expert review;
2. document update;
3. version bump;
4. regression tests;
5. Golden Dataset update.

---

# END OF DOCUMENT
```

Điểm quan trọng nhất file `05` đã khóa là: **0 và 5 là “operator” tác động lên trường khí, không phải một trường khí ngang hàng với tám Du Niên**. Nhờ đó engine sau này mới đọc đúng sự khác nhau giữa `13`, `103`, `153`, `130`, `135` thay vì phá dãy thành những cặp vô nghĩa.