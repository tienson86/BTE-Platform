Được. `04_DIRECTED_INTERACTION_MATRIX.md` là một trong những file quan trọng nhất của toàn bộ hệ thống, vì từ đây engine bắt đầu chuyển từ:

`cặp số → trường khí`

sang:

`trường khí A → trường khí B → ý nghĩa của tổ hợp ba số`.

File này phải khóa nguyên tắc **có hướng**, tức `A → B` không được tự động coi bằng `B → A`.

```markdown
# 04_DIRECTED_INTERACTION_MATRIX.md

# BTE NUMBER ENERGY — DIRECTED INTERACTION MATRIX

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Directed Interaction Matrix  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** CORE KNOWLEDGE  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`

**Depends On:**
- `01_BAGUA_DIGIT_MAPPING.md`
- `02_EIGHT_ENERGY_CATALOG.md`
- `03_PAIR_STRENGTH_MATRIX.md`

---

# 1. PURPOSE

Tài liệu này khóa quan hệ có hướng giữa
hai trường khí liên tiếp trong một dãy số.

Canonical model:

DIGIT A
+
DIGIT B
+
DIGIT C

↓

PAIR AB
=
ENERGY X

PAIR BC
=
ENERGY Y

↓

ENERGY X
→
ENERGY Y

↓

DIRECTED INTERACTION

↓

"TAM SỐ THÀNH TƯỢNG"

Ví dụ:

813

↓

81 = Ngũ Quỷ
13 = Thiên Y

↓

WU_GUI
→
TIAN_Y

↓

trí tuệ / ý tưởng / biến hóa
→
tài phú / thành quả

Không được chỉ luận:

813 có Ngũ Quỷ và Thiên Y.

Phải luận:

Ngũ Quỷ đang chuyển về Thiên Y.

---

# 2. ORDER IS SEMANTIC

Canonical rule:

```text
ORDER_IS_SEMANTIC = TRUE
```

Do đó:

```text
ENERGY_A → ENERGY_B
```

KHÔNG mặc nhiên bằng:

```text
ENERGY_B → ENERGY_A
```

Ví dụ:

```text
JUE_MING → TIAN_Y
```

có thể mang nghĩa:

```text
action / investment
→
wealth / result
```

Trong khi:

```text
TIAN_Y → JUE_MING
```

có thể mang nghĩa:

```text
wealth / resource
→
investment / expenditure
```

Hai cấu trúc này không được merge.

---

# 3. MATRIX DIMENSION

Có tám trường khí:

```text
SHENG_QI
TIAN_Y
YAN_NIAN
FU_WEI
HUO_HAI
WU_GUI
LIU_SHA
JUE_MING
```

Do đó Directed Interaction Matrix có:

```text
8 × 8 = 64
```

quan hệ có hướng.

Tất cả 64 quan hệ phải tồn tại
trong canonical catalog.

---

# 4. INTERACTION DATA MODEL

Recommended canonical structure:

```text
DirectedInteraction {
    interaction_id
    source_energy
    target_energy

    core_process
    core_result

    summary

    personality
    wealth
    career
    relationship
    social
    risk

    positive_expression
    shadow_expression

    customer_narrative_key
    expert_notes

    source_strength_sensitive
    target_strength_sensitive
    position_sensitive

    confidence
}
```

Example:

```text
{
  interaction_id: "INT-WG-TY",
  source_energy: "WU_GUI",
  target_energy: "TIAN_Y",

  core_process: "intelligence_creativity",
  core_result: "wealth_resource",

  summary:
    "Dùng trí tuệ, ý tưởng hoặc tài hoa để tạo ra tài phú.",

  source_strength_sensitive: true,
  target_strength_sensitive: true,
  position_sensitive: true
}
```

---

# 5. INTERPRETATION PRINCIPLE

Source Energy thường cho biết:

```text
HOW
PROCESS
SKILL
STATE
SOURCE
```

Target Energy thường cho biết:

```text
WHERE
RESULT
OUTCOME
DESTINATION
NEXT_STATE
```

Nhưng đây là semantic tendency,
không phải hard rule cho mọi interaction.

---

# 6. SHENG_QI → SHENG_QI

**ID:** `INT-SQ-SQ`

Canonical:

```text
SHENG_QI
→
SHENG_QI
```

Core:

```text
support
→
more support
```

Meaning:

- quý nhân tụ tập;
- nhân duyên tăng;
- mạng lưới trợ lực được tăng cường;
- cơ hội nối tiếp cơ hội;
- trạng thái thuận lợi được củng cố.

Positive expression:

- được nhiều người hỗ trợ;
- dễ mở rộng quan hệ;
- gặp việc khó dễ có người giúp.

Shadow:

- quá dựa vào trợ lực;
- thiếu tính chủ động nếu cấu trúc quá thiên về Sinh Khí.

Canonical summary:

> Sinh Khí nối Sinh Khí làm tăng trường quý nhân,
> cơ hội và khả năng nhận trợ lực từ môi trường.

---

# 7. SHENG_QI → TIAN_Y

**ID:** `INT-SQ-TY`

Canonical:

```text
SHENG_QI
→
TIAN_Y
```

Core:

```text
benefactor / opportunity
→
wealth / relationship
```

Meaning:

- quý nhân mang tài;
- quan hệ đem cơ hội tài chính;
- nguồn lực đến qua người khác;
- thuận cho networking tạo giá trị.

Wealth:

```text
NETWORK
→
WEALTH
```

Relationship:

có thể hỗ trợ Chính Đào Hoa
khi cấu trúc và cường độ phù hợp.

Canonical customer meaning:

> Dãy số có xu hướng tạo giá trị thông qua
> quan hệ, cơ hội và sự hỗ trợ từ người khác.

---

# 8. SHENG_QI → YAN_NIAN

**ID:** `INT-SQ-YN`

Core:

```text
support / opportunity
→
career
```

Meaning:

- quý nhân hỗ trợ công việc;
- có người dẫn dắt;
- thuận cho thăng tiến;
- lợi học tập, phát triển chuyên môn;
- có thể gặp người thầy/người hướng dẫn.

Career:

```text
BENEFactor
→
PROFESSIONAL OPPORTUNITY
```

Canonical summary:

> Quý nhân và cơ hội có khả năng chuyển thành
> sự hỗ trợ trực tiếp cho công việc và sự nghiệp.

---

# 9. SHENG_QI → FU_WEI

**ID:** `INT-SQ-FW`

Core:

```text
support
→
continuation
```

Meaning:

- Sinh Khí được kéo dài;
- trường quý nhân duy trì;
- cơ hội/trợ lực có tính tiếp diễn.

Canonical:

```text
FU_WEI extends SHENG_QI
```

Risk:

- quá phụ thuộc vào môi trường thuận;
- thiếu động lực tự thân nếu quá mạnh.

---

# 10. SHENG_QI → HUO_HAI

**ID:** `INT-SQ-HH`

Core:

```text
social ease
→
speech / argument
```

Meaning:

- ban đầu giao tiếp thuận;
- sau đó lời nói trở thành yếu tố quan trọng;
- dễ phát sinh tranh luận nếu biểu đạt thiếu tiết chế.

Positive:

- tự tin trong giao tiếp;
- có khả năng trình bày.

Shadow:

- dễ nói quá;
- lời nói làm giảm lợi thế quan hệ.

---

# 11. SHENG_QI → WU_GUI

**ID:** `INT-SQ-WG`

Core:

```text
opportunity
→
creative response
```

Meaning:

- linh hoạt;
- khéo ứng biến;
- quan hệ/cơ hội kích hoạt tư duy mới.

Positive:

- nhanh nhạy;
- khéo đưa đẩy;
- biết thay đổi theo hoàn cảnh.

Shadow:

- dễ thay đổi ý định;
- sự thuận lợi ban đầu chuyển sang trạng thái bất định.

---

# 12. SHENG_QI → LIU_SHA

**ID:** `INT-SQ-LS`

Core:

```text
social connection
→
emotion / relationship
```

Meaning:

- quan hệ xã hội chuyển thành gắn kết cảm xúc;
- dễ phát triển tình cảm từ quan hệ quen biết;
- giao tiếp khéo léo;
- quan hệ có thể trở nên phức tạp.

Positive:

- nhân duyên tốt;
- khéo giao tiếp.

Shadow:

- tình bạn dễ chuyển thành cảm xúc;
- dễ bị quan hệ ảnh hưởng tâm trạng.

---

# 13. SHENG_QI → JUE_MING

**ID:** `INT-SQ-JM`

Core:

```text
optimism / opportunity
→
action / risk
```

Meaning:

- tinh thần phấn đấu;
- vui vẻ khi theo đuổi mục tiêu;
- dễ đặt mục tiêu lớn.

Positive:

- có động lực hành động.

Shadow:

- mộng tưởng lớn hơn khả năng thực thi;
- lạc quan có thể dẫn đến đánh giá thấp rủi ro.

---

# 14. TIAN_Y → SHENG_QI

**ID:** `INT-TY-SQ`

Core:

```text
resource / wealth
→
social / benefactor
```

Meaning:

- có điều kiện để giúp bạn bè;
- hào phóng;
- tiền/tài nguyên chảy vào quan hệ.

Positive:

- nhân duyên tốt;
- biết chia sẻ.

Shadow:

- chi tiêu nhiều cho bạn bè;
- tài nguyên phân tán qua quan hệ.

---

# 15. TIAN_Y → TIAN_Y

**ID:** `INT-TY-TY`

Core:

```text
wealth / relationship
→
wealth / relationship
```

Meaning:

- tài khí tập trung;
- Thiên Y được tăng cường;
- Chính Đào Hoa/hôn nhân có thể nổi bật.

Positive:

- tài nguyên mạnh;
- duyên tình cảm rõ.

Shadow:

- quá nhiều Thiên Y không mặc nhiên càng tốt;
- relationship complexity có thể tăng khi lặp nhiều.

---

# 16. TIAN_Y → YAN_NIAN

**ID:** `INT-TY-YN`

Core:

```text
resource / capital
→
career / enterprise
```

Meaning:

- có xu hướng tự làm chủ;
- dùng tài nguyên để lập nghiệp;
- thiên về kinh doanh hoặc đầu tư vào công việc.

Canonical:

```text
RESOURCE
→
PROFESSIONALIZATION
```

---

# 17. TIAN_Y → FU_WEI

**ID:** `INT-TY-FW`

Core:

```text
wealth / relationship
→
continuation
```

Meaning:

- Thiên Y được kéo dài;
- tài khí hoặc trạng thái tình cảm được duy trì.

Canonical:

```text
FU_WEI extends TIAN_Y
```

---

# 18. TIAN_Y → HUO_HAI

**ID:** `INT-TY-HH`

Core:

```text
wealth
→
speech / social expenditure
```

Meaning:

- tiêu tiền vì sĩ diện;
- tiêu dùng để giao tế;
- thích mua sắm/chi tiêu để làm hài lòng người khác.

Risk:

- hao tài vì xã giao;
- chi tiêu cảm tính.

---

# 19. TIAN_Y → WU_GUI

**ID:** `INT-TY-WG`

Core:

```text
wealth / resource
→
volatility / ideas
```

Meaning:

- tài nguyên chuyển sang trạng thái biến động;
- tiền vào-ra nhanh;
- dễ dùng tiền cho ý tưởng hoặc việc khó dự đoán.

Positive:

- đầu tư cho sáng tạo.

Shadow:

- khó giữ tài;
- tài chính thiếu ổn định.

---

# 20. TIAN_Y → LIU_SHA

**ID:** `INT-TY-LS`

Core:

```text
wealth / relationship
→
social / emotional destination
```

Meaning:

- tiền chảy vào gia đình;
- quan hệ;
- phụ nữ;
- dịch vụ;
- làm đẹp;
- giao tế.

Relationship:

có thể tăng yếu tố Đào Hoa
hoặc tác động mạnh tới tình cảm.

---

# 21. TIAN_Y → JUE_MING

**ID:** `INT-TY-JM`

Core:

```text
wealth / resource
→
investment / action
```

Meaning:

- có tiền muốn đầu tư;
- tài nguyên được đưa vào hoạt động có rủi ro;
- dòng tiền chuyển thành hành động.

Canonical:

```text
MONEY
→
INVESTMENT
```

Risk:

- tiêu hao tài chính;
- quyết định đầu tư cảm tính nếu Tuyệt Mệnh mạnh.

---

# 22. YAN_NIAN → SHENG_QI

**ID:** `INT-YN-SQ`

Core:

```text
career
→
positive state / support
```

Meaning:

- làm việc vui;
- công việc ít cảm giác áp lực;
- có môi trường hỗ trợ;
- thuận cho học tập.

Canonical summary:

> Công việc được đặt trong môi trường tương đối
> thuận lợi, có trợ lực và cảm giác tích cực.

---

# 23. YAN_NIAN → TIAN_Y

**ID:** `INT-YN-TY`

Core:

```text
professional ability
→
wealth
```

Meaning:

- dùng chuyên môn kiếm tiền;
- năng lực tạo tài.

Canonical:

```text
SKILL
→
WEALTH
```

Strength relationship:

- Diên Niên mạnh + Thiên Y yếu:
  làm nhiều, thu hoạch tương đối nhỏ.

- Diên Niên yếu + Thiên Y mạnh:
  mức bỏ công thấp hơn nhưng khả năng thu hoạch cao hơn.

Không kết luận nếu chưa xét Tier.

---

# 24. YAN_NIAN → YAN_NIAN

**ID:** `INT-YN-YN`

Core:

```text
career
→
career
```

Meaning:

- năng lực làm việc tăng;
- chuyên môn nổi bật;
- quyền hạn;
- lãnh đạo;
- tinh thần trách nhiệm mạnh.

Shadow:

- áp lực;
- cứng;
- quá thiên về công việc.

---

# 25. YAN_NIAN → FU_WEI

**ID:** `INT-YN-FW`

Core:

```text
career
→
continuation
```

Meaning:

- năng lực nghề nghiệp được kéo dài;
- công việc bền;
- quyền hạn/năng lực được duy trì.

Canonical:

```text
FU_WEI extends YAN_NIAN
```

---

# 26. YAN_NIAN → HUO_HAI

**ID:** `INT-YN-HH`

Core:

```text
career
→
speech / complaint
```

Meaning:

- công việc phát sinh phàn nàn;
- giao tiếp nội bộ trở thành vấn đề;
- quyền hạn có thể bị thách thức;
- dễ hối hận vì cách nói hoặc xử lý.

---

# 27. YAN_NIAN → WU_GUI

**ID:** `INT-YN-WG`

Core:

```text
career
→
change / mental activity
```

Meaning:

- công việc biến động;
- vừa làm vừa suy nghĩ nhiều;
- dễ thay đổi cách làm;
- công việc cần trí óc.

Positive:

- linh hoạt nghề nghiệp.

Shadow:

- bất an;
- khó ổn định.

---

# 28. YAN_NIAN → LIU_SHA

**ID:** `INT-YN-LS`

Core:

```text
career
→
emotion
```

Meaning:

- làm việc không vui;
- cảm xúc ảnh hưởng công việc;
- u buồn;
- thiếu quả quyết.

Canonical:

```text
WORK
→
EMOTIONAL PRESSURE
```

---

# 29. YAN_NIAN → JUE_MING

**ID:** `INT-YN-JM`

Core:

```text
career
→
pressure / impulsive action
```

Meaning:

- công việc dễ gặp trắc trở;
- quyết định công việc mạnh hoặc vội;
- dễ thay đổi vị trí nếu mất cân bằng.

Positive:

- dám quyết.

Shadow:

- áp lực;
- xung động;
- khó duy trì ổn định.

---

# 30. FU_WEI → SHENG_QI

**ID:** `INT-FW-SQ`

Core:

```text
waiting / accumulation
→
opportunity
```

Meaning:

- chờ thời rồi gặp cơ hội;
- Sinh Khí được tăng thế;
- cơ hội đến sau giai đoạn tích lũy.

Positive:

- kiên nhẫn tạo điều kiện cho quý nhân/cơ hội xuất hiện.

---

# 31. FU_WEI → TIAN_Y

**ID:** `INT-FW-TY`

Core:

```text
patience
→
wealth
```

Meaning:

- nhờ kiên trì mà tạo tài;
- chờ đợi đúng thời điểm;
- tài phú đến chậm nhưng có quá trình tích lũy.

Canonical:

```text
PATIENCE
→
RESOURCE
```

---

# 32. FU_WEI → YAN_NIAN

**ID:** `INT-FW-YN`

Core:

```text
accumulation
→
professional capacity
```

Meaning:

- năng lực được tăng dần;
- càng làm càng có kinh nghiệm;
- quyền hạn/công việc được củng cố.

---

# 33. FU_WEI → FU_WEI

**ID:** `INT-FW-FW`

Core:

```text
continuation
→
continuation
```

Meaning:

- vận sức chờ phát động;
- tính kiên trì tăng;
- trạng thái kéo dài mạnh.

Positive:

- sức bền.

Shadow:

- trì trệ;
- bảo thủ;
- khó thay đổi.

---

# 34. FU_WEI → HUO_HAI

**ID:** `INT-FW-HH`

Core:

```text
fixed state
→
speech
```

Meaning:

- mạnh miệng;
- khó thay đổi quan điểm;
- tự cho mình đúng;
- tranh luận dai.

---

# 35. FU_WEI → WU_GUI

**ID:** `INT-FW-WG`

Core:

```text
accumulation
→
mental volatility
```

Meaning:

- Ngũ Quỷ được tăng thế;
- suy nghĩ kéo dài;
- dễ suy nghĩ nhiều.

Positive:

- nghiên cứu sâu.

Shadow:

- overthinking;
- nghi ngờ kéo dài.

---

# 36. FU_WEI → LIU_SHA

**ID:** `INT-FW-LS`

Core:

```text
waiting
→
emotion
```

Meaning:

- Lục Sát được tăng cường;
- cảm xúc kéo dài;
- lo được lo mất;
- thiếu cảm giác an toàn.

Relationship:

- dễ giữ cảm xúc lâu;
- khó dứt khỏi trạng thái tình cảm.

---

# 37. FU_WEI → JUE_MING

**ID:** `INT-FW-JM`

Core:

```text
accumulation
→
strong action
```

Meaning:

- sức xung động tăng sau thời gian tích tụ;
- khi quyết định thì hành động mạnh;
- có thể rất liều trong công việc.

Positive:

- quyết tâm lớn.

Shadow:

- hành động quá mức khi đã bị dồn nén.

---

# 38. HUO_HAI → SHENG_QI

**ID:** `INT-HH-SQ`

Core:

```text
speech
→
social acceptance
```

Meaning:

- khẩu tài tốt;
- lời nói dễ được người khác nghe;
- giao tiếp đem lại quan hệ.

Canonical:

```text
COMMUNICATION
→
NETWORK
```

---

# 39. HUO_HAI → TIAN_Y

**ID:** `INT-HH-TY`

Core:

```text
speech
→
wealth
```

Meaning:

- dùng lời nói kiếm tiền;
- bán hàng;
- tư vấn;
- diễn thuyết;
- đào tạo;
- đàm phán.

Canonical:

```text
COMMUNICATION
→
WEALTH
```

Đây là một Wealth Source Pattern quan trọng.

---

# 40. HUO_HAI → YAN_NIAN

**ID:** `INT-HH-YN`

Core:

```text
speech
→
career
```

Meaning:

- nghề nghiệp dựa vào khẩu tài;
- công việc cần giao tiếp;
- thuyết phục;
- trình bày.

Canonical:

```text
COMMUNICATION_SKILL
→
PROFESSION
```

---

# 41. HUO_HAI → FU_WEI

**ID:** `INT-HH-FW`

Core:

```text
speech
→
continuation
```

Meaning:

- đặc tính Họa Hại kéo dài;
- mạnh miệng;
- tranh luận dai;
- khó chịu thua.

Positive:

- kiên trì trong tranh luận.

Shadow:

- cãi vã kéo dài;
- làm quan hệ mệt mỏi.

---

# 42. HUO_HAI → HUO_HAI

**ID:** `INT-HH-HH`

Core:

```text
speech
→
more speech
```

Meaning:

- khẩu tài tăng;
- lời nói mạnh;
- tranh luận tăng;
- nóng nảy;
- dễ phát sinh thị phi.

Functional:

- hùng biện mạnh.

Shadow:

- thắng lời nhưng mất quan hệ.

---

# 43. HUO_HAI → WU_GUI

**ID:** `INT-HH-WG`

Core:

```text
speech
→
overthinking / counterargument
```

Meaning:

- nhiều lý lẽ;
- thích phản bác;
- dễ chất vấn;
- khó bị thuyết phục trực tiếp.

Communication advice:

```text
build_rapport
use_evidence
avoid_direct_confrontation
```

---

# 44. HUO_HAI → LIU_SHA

**ID:** `INT-HH-LS`

Core:

```text
speech
→
emotional consequence
```

Meaning:

- lời nói gây cảm xúc tiêu cực;
- nói xong dễ hối hận;
- quan hệ bị ảnh hưởng bởi giao tiếp.

Canonical:

```text
WORDS
→
EMOTION
```

---

# 45. HUO_HAI → JUE_MING

**ID:** `INT-HH-JM`

Core:

```text
speech / controversy
→
impulsive action
```

Meaning:

- lời nói có thể kích hoạt hành động mạnh;
- dễ phản ứng quá mức;
- tranh luận có thể chuyển thành hành động.

Customer narrative phải tránh
các dự đoán tai nạn chắc chắn.

---

# 46. WU_GUI → SHENG_QI

**ID:** `INT-WG-SQ`

Core:

```text
ideas
→
useful opportunity
```

Meaning:

- nghĩ ra giải pháp hữu dụng;
- trí óc tạo cơ hội;
- sáng tạo được người khác hỗ trợ.

Canonical:

```text
CREATIVITY
→
OPPORTUNITY
```

---

# 47. WU_GUI → TIAN_Y

**ID:** `INT-WG-TY`

Core:

```text
intelligence / creativity
→
wealth
```

Meaning:

- kiếm tiền bằng trí óc;
- tài hoa tạo tài;
- nghề sáng tạo;
- kế hoạch;
- công nghệ;
- chuyên môn trí tuệ.

Possible contexts:

- thiết kế;
- công nghệ;
- IT;
- nghiên cứu;
- lập kế hoạch;
- nghề chuyên môn cao.

Canonical:

```text
CREATIVE_INTELLIGENCE
→
WEALTH
```

---

# 48. WU_GUI → YAN_NIAN

**ID:** `INT-WG-YN`

Core:

```text
ideas
→
execution / career
```

Meaning:

- biến ý tưởng thành công việc;
- sáng tạo đi cùng thực thi;
- có thể phát triển thành năng lực lãnh đạo.

Canonical:

```text
IDEA
→
EXECUTION
```

Positive:

- sáng tạo + tổ chức.

Shadow:

- áp lực cao;
- làm việc quá nhiều.

---

# 49. WU_GUI → FU_WEI

**ID:** `INT-WG-FW`

Core:

```text
change / thinking
→
continuation
```

Meaning:

- Ngũ Quỷ kéo dài;
- suy nghĩ liên tục;
- biến động khó dừng.

Positive:

- nghiên cứu sâu;
- liên tục đổi mới.

Shadow:

- thiếu ổn định;
- overthinking.

---

# 50. WU_GUI → HUO_HAI

**ID:** `INT-WG-HH`

Core:

```text
idea
→
argument
```

Meaning:

- suy nghĩ tạo tranh luận;
- ý tưởng khác biệt khó được hiểu;
- dễ nói ra điều gây tranh cãi.

---

# 51. WU_GUI → WU_GUI

**ID:** `INT-WG-WG`

Core:

```text
creativity / volatility
→
more creativity / volatility
```

Meaning:

- tài hoa mạnh;
- phản ứng nhanh;
- ý tưởng nhiều;
- bất ổn tăng;
- dễ thay đổi phương án.

Canonical:

```text
CREATIVITY ↑↑
VOLATILITY ↑↑
STABILITY ↓
```

---

# 52. WU_GUI → LIU_SHA

**ID:** `INT-WG-LS`

Core:

```text
thinking
→
emotion
```

Meaning:

- suy nghĩ làm cảm xúc bất ổn;
- dễ động tình;
- ý nghĩ thiếu thực tế khi cảm xúc mạnh.

Shadow:

- suy nghĩ nhiều;
- tình cảm phức tạp.

---

# 53. WU_GUI → JUE_MING

**ID:** `INT-WG-JM`

Core:

```text
idea / information
→
strong action
```

Meaning:

- thấy cơ hội là hành động nhanh;
- dám liều;
- phản ứng cực nhanh với thông tin.

Positive:

- chớp thời cơ.

Shadow:

- quá nhanh;
- hành động khi chưa đủ kiểm chứng.

---

# 54. LIU_SHA → SHENG_QI

**ID:** `INT-LS-SQ`

Core:

```text
social / emotion
→
support
```

Meaning:

- nhân duyên tốt;
- đối người nhiệt tình;
- quan hệ xã hội tạo trợ lực.

Canonical:

```text
RELATIONSHIP
→
SUPPORT
```

---

# 55. LIU_SHA → TIAN_Y

**ID:** `INT-LS-TY`

Core:

```text
service / social ability
→
wealth
```

Meaning:

- kiếm tiền bằng dịch vụ;
- giao tiếp;
- quan hệ;
- ngành làm đẹp;
- công việc cần sự tinh tế.

Canonical:

```text
SERVICE
→
WEALTH
```

---

# 56. LIU_SHA → YAN_NIAN

**ID:** `INT-LS-YN`

Core:

```text
social / service ability
→
career
```

Meaning:

- nghề dịch vụ;
- hành chính;
- đối ngoại;
- chăm sóc khách hàng;
- quan hệ xã hội.

Canonical:

```text
SERVICE_SKILL
→
PROFESSION
```

---

# 57. LIU_SHA → FU_WEI

**ID:** `INT-LS-FW`

Core:

```text
emotion / relationship
→
continuation
```

Meaning:

- Lục Sát kéo dài;
- do dự;
- cảm xúc khó dứt;
- Đào Hoa kéo dài;
- thiếu cảm giác an toàn.

Canonical:

```text
FU_WEI extends LIU_SHA
```

---

# 58. LIU_SHA → HUO_HAI

**ID:** `INT-LS-HH`

Core:

```text
emotion
→
speech problem
```

Meaning:

- tâm trạng ảnh hưởng cách nói;
- dễ đắc tội vì lời nói;
- khi không vui dễ giao tiếp kém.

---

# 59. LIU_SHA → WU_GUI

**ID:** `INT-LS-WG`

Core:

```text
emotion
→
instability / suspicion
```

Meaning:

- cảm xúc biến hóa;
- thiếu an toàn;
- quan hệ dễ phức tạp;
- dễ suy nghĩ nhiều về tình cảm.

---

# 60. LIU_SHA → LIU_SHA

**ID:** `INT-LS-LS`

Core:

```text
emotion
→
more emotion
```

Meaning:

- cảm xúc tăng mạnh;
- Đào Hoa tăng;
- quan hệ phức tạp;
- dễ lo được lo mất.

Positive:

- cảm nhận tinh tế.

Shadow:

- thiếu ổn định tình cảm.

---

# 61. LIU_SHA → JUE_MING

**ID:** `INT-LS-JM`

Core:

```text
emotion
→
forceful action
```

Meaning:

- hành động dưới áp lực cảm xúc;
- dễ cảm thấy bị ép;
- quyết định vì tình cảm.

Risk:

- thiếu bình tĩnh khi hành động.

---

# 62. JUE_MING → SHENG_QI

**ID:** `INT-JM-SQ`

Core:

```text
risk / action
→
positive state
```

Meaning:

- thích hành động;
- hưởng thụ quá trình thử thách;
- đầu tư/mạo hiểm mang lại cảm giác hứng thú.

Canonical:

```text
ACTION
→
OPTIMISM
```

---

# 63. JUE_MING → TIAN_Y

**ID:** `INT-JM-TY`

Core:

```text
action / investment
→
wealth
```

Meaning:

- nỗ lực kiếm tiền;
- đầu tư tạo tài;
- hành động hướng tới kết quả tài chính.

Canonical:

```text
ACTION
→
WEALTH
```

Đây là Investment/Wealth Pattern quan trọng.

---

# 64. JUE_MING → YAN_NIAN

**ID:** `INT-JM-YN`

Core:

```text
action / risk
→
career
```

Meaning:

- phấn đấu mạnh;
- kinh doanh;
- đầu tư;
- phát triển sự nghiệp bằng hành động;
- có xu hướng mở rộng.

Canonical:

```text
ACTION
→
PROFESSION
```

Có thể liên hệ:

- kinh doanh;
- quản lý tài sản;
- bất động sản;
- công việc cạnh tranh.

---

# 65. JUE_MING → FU_WEI

**ID:** `INT-JM-FW`

Core:

```text
action / risk
→
continuation
```

Meaning:

- đặc tính Tuyệt Mệnh kéo dài;
- quyết liệt;
- hành động dai;
- khó dừng khi đã quyết.

Positive:

- kiên trì mạnh.

Shadow:

- mạo hiểm kéo dài;
- khó biết điểm dừng.

---

# 66. JUE_MING → HUO_HAI

**ID:** `INT-JM-HH`

Core:

```text
action
→
controversy
```

Meaning:

- cách làm dễ gây tranh luận;
- hành động tạo thị phi;
- quyết định mạnh dễ bị phản ứng.

Canonical:

```text
ACTION
→
CONTROVERSY
```

---

# 67. JUE_MING → WU_GUI

**ID:** `INT-JM-WG`

Core:

```text
risk
→
volatility
```

Meaning:

- mạo hiểm đi vào biến động;
- tài chính lên xuống;
- quyết định nhanh;
- thích đầu tư;
- tiền ra nhanh.

Canonical:

```text
RISK
→
VOLATILITY
```

Risk level:

HIGH when both energies are strong.

---

# 68. JUE_MING → LIU_SHA

**ID:** `INT-JM-LS`

Core:

```text
action / risk
→
emotional consequence
```

Meaning:

- quyết định xong dễ hối hận;
- thất bại tài chính gây áp lực cảm xúc;
- hành động mạnh dẫn tới tâm trạng không ổn định.

Canonical:

```text
ACTION
→
REGRET / EMOTIONAL_PRESSURE
```

---

# 69. JUE_MING → JUE_MING

**ID:** `INT-JM-JM`

Core:

```text
risk / action
→
more risk / action
```

Meaning:

- tính quyết liệt rất mạnh;
- chủ quan;
- xung động;
- cực đoan;
- hành động nhanh;
- tài chính biến động.

Functional:

- sức hành động rất cao.

Shadow:

- risk control thấp;
- phá tài;
- khó dừng;
- dễ quyết định quá mức.

---

# 70. COMPLETE 8 × 8 MATRIX

| FROM ↓ / TO → | Sinh Khí | Thiên Y | Diên Niên | Phục Vị | Họa Hại | Ngũ Quỷ | Lục Sát | Tuyệt Mệnh |
|---|---|---|---|---|---|---|---|---|
| **Sinh Khí** | Quý nhân tăng | Quý nhân sinh tài | Quý nhân trợ sự nghiệp | Kéo dài Sinh Khí | Quan hệ → lời nói | Cơ hội → ứng biến | Quan hệ → cảm xúc | Lạc quan → hành động |
| **Thiên Y** | Tài → quan hệ | Tài/tình tăng | Tài nguyên → sự nghiệp | Kéo dài Thiên Y | Tài → xã giao | Tài → biến động | Tài → quan hệ | Tài → đầu tư |
| **Diên Niên** | Công việc thuận | Chuyên môn sinh tài | Năng lực tăng | Kéo dài Diên Niên | Công việc → thị phi | Công việc → biến động | Công việc → cảm xúc | Công việc → áp lực |
| **Phục Vị** | Chờ thời → cơ hội | Kiên trì → tài | Tích lũy → năng lực | Phục Vị tăng | Cố định → khẩu chiến | Kéo dài suy nghĩ | Kéo dài cảm xúc | Tích tụ → hành động |
| **Họa Hại** | Khẩu tài → quan hệ | Khẩu tài → tài | Khẩu tài → nghề | Kéo dài Họa Hại | Khẩu chiến tăng | Lời nói → suy nghĩ | Lời nói → cảm xúc | Lời nói → hành động |
| **Ngũ Quỷ** | Ý tưởng → cơ hội | Trí tuệ → tài | Ý tưởng → sự nghiệp | Kéo dài Ngũ Quỷ | Ý tưởng → tranh luận | Sáng tạo + biến động | Suy nghĩ → cảm xúc | Ý tưởng → hành động |
| **Lục Sát** | Quan hệ → trợ lực | Dịch vụ → tài | Dịch vụ → nghề | Kéo dài Lục Sát | Cảm xúc → lời nói | Cảm xúc → bất ổn | Cảm xúc tăng | Cảm xúc → hành động |
| **Tuyệt Mệnh** | Hành động → lạc quan | Đầu tư → tài | Hành động → nghề | Kéo dài Tuyệt Mệnh | Hành động → tranh luận | Rủi ro → biến động | Hành động → áp lực cảm xúc | Rủi ro tăng |

This matrix is CANONICAL.

---

# 71. STRENGTH MODULATION

Directed Interaction không được luận
mà bỏ qua Pair Strength.

Final interaction intensity phụ thuộc:

```text
source_strength
+
target_strength
```

Ví dụ:

```text
JUE_MING_T1 → TIAN_Y_T1
```

khác:

```text
JUE_MING_T4 → TIAN_Y_T1
```

và khác:

```text
JUE_MING_T1 → TIAN_Y_T4
```

Tuy nhiên:

Pair Strength Matrix chỉ cung cấp cường độ.

Không được biến cường độ thành final quality.

---

# 72. RISK–REWARD EXAMPLE

Đối với:

```text
JUE_MING → TIAN_Y
```

có thể xét:

| Tuyệt Mệnh | Thiên Y | Interpretation |
|---|---|---|
| Nhỏ | Nhỏ | Đầu tư nhỏ – thu hoạch nhỏ |
| Nhỏ | Lớn | Rủi ro nhỏ – tiềm năng thu hoạch lớn |
| Lớn | Lớn | Rủi ro lớn – tiềm năng thu hoạch lớn |
| Lớn | Nhỏ | Rủi ro lớn – khả năng thu hoạch tương đối nhỏ |

Đây là relative pattern.

Không phải dự báo lợi nhuận thực tế.

---

# 73. POSITION MODULATION

Cùng một interaction có thể khác
tùy vị trí:

```text
HEAD
MIDDLE
TAIL
```

Ví dụ:

```text
JUE_MING → WU_GUI
```

ở giữa dãy có thể là:

process volatility.

Ở cuối dãy có thể có trọng số cao hơn
trong final outcome.

Position logic thuộc:

`06_POSITION_AND_TAIL_RULES.md`

---

# 74. ZERO / FIVE MODIFICATION

Nếu interaction chứa:

```text
0
5
```

không được dùng matrix này một cách naïve.

Ví dụ:

```text
103
```

không được parse đơn giản là:

```text
10
03
```

Phải nhận diện underlying:

```text
13 = TIAN_Y
```

và:

```text
0 = HIDDEN modifier
```

Chi tiết thuộc:

`05_ZERO_FIVE_MODIFIERS.md`

---

# 75. PHUC_VI SPECIAL BEHAVIOR

Phục Vị có hai role khác nhau:

## Target

```text
A → FU_WEI
```

thường biểu thị:

```text
EXTEND(A)
```

## Source

```text
FU_WEI → B
```

thường biểu thị:

```text
accumulated / delayed state
→
B
```

Hai hướng không được đồng nhất.

---

# 76. INTERACTION ≠ FINAL CONCLUSION

Không được dùng:

```text
one triple
=
whole number conclusion
```

Ví dụ:

```text
813
=
WU_GUI → TIAN_Y
```

không đủ để kết luận:

> Đây là số tốt.

Phải tiếp tục xét:

- các cặp tiếp theo;
- strength;
- chain;
- 0/5;
- position;
- control/remedy;
- tail;
- domain;
- whole sequence.

---

# 77. CUSTOMER NARRATIVE RULE

Customer Narrative KHÔNG hiển thị thô:

> Ngũ Quỷ + Thiên Y.

Nên viết:

> Cấu trúc này cho thấy khả năng sử dụng
> trí tuệ, ý tưởng hoặc sự sáng tạo để tạo
> ra giá trị tài chính. Điểm mạnh nằm ở tư duy
> linh hoạt; điểm cần lưu ý là giữ sự ổn định
> trong quá trình thực hiện.

Expert Mode có thể hiển thị:

```text
81 = Ngũ Quỷ / Tier 1
13 = Thiên Y / Tier 1

Interaction:
WU_GUI → TIAN_Y
```

---

# 78. HEALTH / ACCIDENT CLAIM SAFETY

Một số tài liệu nguồn có gắn các interaction
với:

- bệnh nặng;
- ung thư;
- tai nạn;
- tử vong;
- vô sinh;
- các kết luận y khoa khác.

Các nội dung này:

```text
MAY_EXIST_IN_SOURCE_REFERENCE
```

nhưng:

```text
MUST_NOT_BE_DETERMINISTIC_CUSTOMER_OUTPUT
```

Customer Narrative chỉ được dùng ngôn ngữ:

> Theo hệ thống Năng lượng số,
> cấu trúc này được xem là cần chú ý hơn
> tới sự cân bằng và trạng thái sinh hoạt.

Không dự đoán bệnh.

Không chẩn đoán.

Không dự đoán tai nạn chắc chắn.

---

# 79. IMPLEMENTATION CONTRACT

Runtime MUST:

1. resolve every valid adjacent pair;
2. attach Energy ID;
3. attach Strength Tier;
4. preserve pair order;
5. build consecutive Energy interactions;
6. resolve Directed Interaction ID;
7. preserve sequence position;
8. pass interaction to Chain Engine;
9. pass special digits to Modifier Engine;
10. never create narrative directly from raw pair.

Canonical pipeline:

```text
NUMBER
↓
DIGITS
↓
ADJACENT PAIRS
↓
PAIR ENERGY
↓
PAIR STRENGTH
↓
DIRECTED INTERACTION
↓
CHAIN
↓
POSITION
↓
MODIFIER
↓
CONTROL
↓
DOMAIN
↓
NARRATIVE
```

---

# 80. VALIDATION

Minimum canonical tests:

```text
813
```

must resolve:

```text
81 = WU_GUI
13 = TIAN_Y
INT-WG-TY
```

---

```text
318
```

must resolve:

```text
31 = TIAN_Y
18 = WU_GUI
INT-TY-WG
```

and MUST NOT equal `813`.

---

```text
719
```

must resolve:

```text
71 = HUO_HAI
19 = YAN_NIAN
INT-HH-YN
```

---

```text
219
```

must resolve:

```text
21 = JUE_MING
19 = YAN_NIAN
INT-JM-YN
```

---

```text
619
```

must resolve:

```text
61 = LIU_SHA
19 = YAN_NIAN
INT-LS-YN
```

---

```text
131
```

must resolve:

```text
13 = TIAN_Y
31 = TIAN_Y
INT-TY-TY
```

---

```text
181
```

must resolve:

```text
18 = WU_GUI
81 = WU_GUI
INT-WG-WG
```

---

# 81. NON-GOALS

File này KHÔNG định nghĩa:

- modifier chi tiết của 0;
- modifier chi tiết của 5;
- position scoring;
- tail weighting;
- remedy algorithm;
- whole-sequence scoring;
- owner compatibility;
- phone vs vehicle weighting;
- final narrative templates.

Các nội dung đó thuộc các Knowledge Pack sau.

---

# 82. DEPENDENCY ORDER

Canonical Knowledge order:

```text
00_NUMBER_ENERGY_MASTER
        ↓
01_BAGUA_DIGIT_MAPPING
        ↓
02_EIGHT_ENERGY_CATALOG
        ↓
03_PAIR_STRENGTH_MATRIX
        ↓
04_DIRECTED_INTERACTION_MATRIX
        ↓
05_ZERO_FIVE_MODIFIERS
        ↓
06_POSITION_AND_TAIL_RULES
        ↓
07_CONTROL_REMEDY_RULES
        ↓
08_CHAIN_INTERPRETATION_RULES
        ↓
09_DOMAIN_INTERPRETATION
        ↓
10_CUSTOMER_NARRATIVE_CATALOG
        ↓
11_ACCEPTANCE_GOLDEN_CASES
```

---

# 83. FREEZE RULE

Once accepted:

```text
04_DIRECTED_INTERACTION_MATRIX.md
```

becomes the canonical source of truth
for all directed Energy → Energy relationships.

Cursor / implementation MUST NOT:

- merge reverse interactions;
- invent new meanings;
- infer missing spiritual rules;
- simplify 64 relationships into Cát/Hung counting;
- replace directed semantics with scoring alone;
- generate customer interpretations not supported
  by canonical Knowledge.

Any knowledge change requires:

1. expert review;
2. canonical document update;
3. version update;
4. regression test;
5. Golden Dataset validation.

---

# END OF DOCUMENT
```

File `04` này về bản chất đã khóa được **64 “động từ” của Number Energy Engine**. Từ file sau `05_ZERO_FIVE_MODIFIERS.md`, chúng ta xử lý lớp khó tiếp theo: cùng một Thiên Y nhưng `13`, `103`, `153`, `130`, `135` phải được hiểu khác nhau như thế nào.