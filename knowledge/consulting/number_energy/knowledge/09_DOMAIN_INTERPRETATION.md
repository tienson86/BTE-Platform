Được. `09_DOMAIN_INTERPRETATION.md` là file chuyển **kết quả kỹ thuật của Chain Engine** thành các miền luận giải mà khách hàng thực sự quan tâm.

File này phải khóa rõ:

- cùng một chain nhưng khi luận **Tài vận** khác khi luận **Công việc**;
- số điện thoại dùng profile đầy đủ hơn;
- biển số xe giảm mạnh phần hôn nhân/đào hoa;
- không được dùng một cặp số để kết luận toàn bộ một domain;
- không được biến các liên hệ sức khỏe trong tài liệu nguồn thành chẩn đoán y khoa.

Tôi đề nghị nội dung như sau:

```markdown
# 09_DOMAIN_INTERPRETATION.md

# BTE NUMBER ENERGY — DOMAIN INTERPRETATION STANDARD

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Domain Interpretation Standard  
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
- `08_CHAIN_INTERPRETATION_RULES.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa cách chuyển
Whole-Sequence Analysis thành các miền
luận giải cụ thể cho khách hàng.

Canonical domains:

1. GENERAL
2. WEALTH
3. CAREER
4. RELATIONSHIP
5. PERSONALITY
6. SOCIAL
7. INVESTMENT
8. LEARNING
9. WELLNESS_REFERENCE
10. BALANCE
11. RECOMMENDATION_CONTEXT

Tài liệu này trả lời:

> Dãy số biểu hiện thế nào
> trong từng lĩnh vực cụ thể?

---

# 2. DOMAIN INTERPRETATION PRINCIPLE

Không được dùng:

PAIR
→
DOMAIN CONCLUSION

Canonical:

PAIR
↓
ENERGY
↓
STRENGTH
↓
INTERACTION
↓
CHAIN
↓
POSITION
↓
MODIFIER
↓
CONTROL
↓
DOMAIN FILTER
↓
DOMAIN CONCLUSION

Mỗi Domain phải dựa trên
whole-sequence context.

---

# 3. ONE CHAIN — MULTIPLE DOMAINS

Một chain có thể có
nhiều ý nghĩa đồng thời.

Ví dụ:

JUE_MING → TIAN_Y

Trong WEALTH:

action / investment
→ wealth

Trong INVESTMENT:

risk-taking
→ financial result

Trong BALANCE:

Tuyệt Mệnh được Thiên Y điều tiết.

Một sequence có thể
phát sinh nhiều Domain Findings.

---

# 4. DOMAIN RESULT MODEL

Recommended:

```text
DomainResult {
    domain_id

    prominence
    structural_state

    primary_findings
    secondary_findings

    strengths
    cautions

    supporting_interactions
    supporting_energies

    terminal_relevance
    control_status

    customer_summary_key
}
```

---

# 5. PROMINENCE

Recommended internal values:

```text
PRIMARY
STRONG
MODERATE
LIGHT
REFERENCE_ONLY
```

Prominence phải xét:

- số lượng tín hiệu;
- pair strength;
- chain continuity;
- position;
- terminal relevance;
- repetition;
- modifier;
- control.

Không dùng raw count.

---

# 6. GENERAL DOMAIN

## Purpose

GENERAL tạo bức tranh tổng thể
của toàn dãy.

Phải trả lời:

1. Trường chủ đạo là gì?
2. Dòng năng lượng chính đi theo hướng nào?
3. Cát/Hung được phối như thế nào?
4. Điểm mạnh chính là gì?
5. Điểm mất cân bằng chính là gì?
6. Cuối dãy quy tụ về đâu?
7. Có chế hóa hay không?

---

# 7. GENERAL — PRIMARY ENERGY

GENERAL phải lấy:

```text
PRIMARY_ENERGY
SECONDARY_ENERGY
TERMINAL_ENERGY
```

từ Chain Summary.

Ví dụ:

```text
PRIMARY = YAN_NIAN
SECONDARY = TIAN_Y
TERMINAL = SHENG_QI
```

Customer meaning:

> Dãy số thiên về năng lực nghề nghiệp và
> khả năng tạo thành quả, trong khi phần cuối
> quy về quý nhân và trợ lực.

---

# 8. GENERAL — STRUCTURE TYPES

Recommended:

```text
SUPPORTIVE
BALANCED
MIXED
CHALLENGING
VOLATILE
HIDDEN
AMPLIFIED
```

Không dùng:

```text
ĐẠI CÁT
ĐẠI HUNG
```

như classification mặc định.

---

# 9. GENERAL — CORE CUSTOMER OUTPUT

GENERAL should include:

- trường khí chủ đạo;
- flow;
- terminal;
- balance;
- one strength;
- one caution.

Recommended length:

2–4 sentences.

---

# 10. WEALTH DOMAIN

Canonical core:

```text
TIAN_Y
```

Thiên Y là Wealth Core.

Nhưng WEALTH không được xác định
chỉ từ số lượng Thiên Y.

Phải xét:

```text
source_of_wealth
wealth_strength
wealth_destination
wealth_visibility
wealth_stability
```

---

# 11. WEALTH SOURCE

Canonical:

```text
X → TIAN_Y
```

X cho biết cách/nơi
tài nguyên được hình thành.

---

# 12. SHENG_QI → TIAN_Y

Meaning:

```text
NETWORK / OPPORTUNITY
→
WEALTH
```

Customer interpretation:

- tài đến qua quý nhân;
- quan hệ đem cơ hội;
- networking có giá trị;
- dễ nhận trợ lực tài chính/cơ hội kinh doanh.

---

# 13. YAN_NIAN → TIAN_Y

Meaning:

```text
PROFESSIONAL CAPACITY
→
WEALTH
```

Customer:

- kiếm tiền bằng chuyên môn;
- thu nhập gắn với năng lực;
- phù hợp phát triển kỹ năng để tăng tài.

---

# 14. LIU_SHA → TIAN_Y

Meaning:

```text
SERVICE / SOCIAL / AESTHETIC
→
WEALTH
```

Possible contexts:

- dịch vụ;
- chăm sóc khách hàng;
- thẩm mỹ;
- bán lẻ;
- giao tiếp;
- ngành phục vụ.

---

# 15. HUO_HAI → TIAN_Y

Meaning:

```text
COMMUNICATION
→
WEALTH
```

Possible contexts:

- bán hàng;
- tư vấn;
- đào tạo;
- diễn thuyết;
- đàm phán;
- truyền thông.

---

# 16. WU_GUI → TIAN_Y

Meaning:

```text
INTELLIGENCE / CREATIVITY
→
WEALTH
```

Possible contexts:

- công nghệ;
- thiết kế;
- sáng tạo;
- nghiên cứu;
- kế hoạch;
- chuyên môn trí tuệ.

---

# 17. JUE_MING → TIAN_Y

Meaning:

```text
ACTION / INVESTMENT
→
WEALTH
```

Possible contexts:

- đầu tư;
- kinh doanh;
- dự án;
- hành động mạnh;
- cạnh tranh.

Risk/reward phải xét strength.

---

# 18. WEALTH DESTINATION

Canonical:

```text
TIAN_Y → Y
```

Y cho biết
tài nguyên có xu hướng chảy đi đâu.

---

# 19. TIAN_Y → SHENG_QI

Meaning:

- tiền cho quan hệ;
- bạn bè;
- kết nối;
- mở rộng network.

---

# 20. TIAN_Y → YAN_NIAN

Meaning:

- đưa tài nguyên vào công việc;
- lập nghiệp;
- kinh doanh;
- phát triển sự nghiệp.

---

# 21. TIAN_Y → LIU_SHA

Meaning:

- chi cho gia đình;
- giao tế;
- dịch vụ;
- thẩm mỹ;
- quan hệ.

---

# 22. TIAN_Y → HUO_HAI

Meaning:

- chi cho xã giao;
- sĩ diện;
- giao tiếp;
- các hoạt động mang tính thể hiện.

---

# 23. TIAN_Y → WU_GUI

Meaning:

- tài chính biến động;
- tiền dùng cho ý tưởng;
- khó giữ tài nếu toàn chain thiếu ổn định.

---

# 24. TIAN_Y → JUE_MING

Meaning:

```text
RESOURCE
→
INVESTMENT / RISK
```

Customer:

> Tài nguyên có xu hướng được đưa trở lại
> hoạt động đầu tư hoặc mở rộng.

Risk note:

> Cần quản trị mức độ mạo hiểm.

---

# 25. TIAN_Y → FU_WEI

Meaning:

- tài nguyên kéo dài;
- duy trì;
- tích lũy.

Nhưng phải xét toàn chain
để biết tích lũy hay trì trệ.

---

# 26. WEALTH + ZERO

Nếu Thiên Y bị ZERO:

```text
WEALTH_VISIBILITY = HIDDEN
```

Possible interpretation:

- tài khí khó biểu hiện;
- vốn bị khóa;
- tiền khó quay vòng;
- tài nguyên khó phát huy.

Không nói:

> chắc chắn mất tiền.

---

# 27. WEALTH + FIVE

Nếu Thiên Y bị FIVE:

```text
WEALTH_VISIBILITY = AMPLIFIED
```

Meaning:

- tài khí rõ;
- tài nguyên nổi bật;
- khả năng tạo/thu hút giá trị được nhấn mạnh.

Nhưng phải xét cả flow sau đó.

---

# 28. WEALTH DOMAIN RESULT

Recommended fields:

```text
wealth_source
wealth_strength
wealth_stability
wealth_destination
wealth_visibility
wealth_risk
```

---

# 29. CAREER DOMAIN

Canonical Core:

```text
YAN_NIAN
```

Diên Niên đại diện:

- công việc;
- chuyên môn;
- năng lực;
- trách nhiệm;
- tổ chức;
- quyền hạn;
- khả năng quản lý.

---

# 30. CAREER SOURCE

Canonical:

```text
X → YAN_NIAN
```

X cho biết
kỹ năng/ngành nghề nổi bật.

---

# 31. SHENG_QI → YAN_NIAN

Meaning:

```text
NETWORK / SUPPORT
→
CAREER
```

Possible interpretation:

- quý nhân trợ sự nghiệp;
- có người dẫn dắt;
- công việc phát triển qua network;
- phù hợp môi trường hợp tác.

---

# 32. TIAN_Y → YAN_NIAN

Meaning:

```text
RESOURCE
→
CAREER
```

Possible:

- có điều kiện lập nghiệp;
- dùng vốn/tài nguyên phát triển công việc;
- thiên về tự làm chủ.

---

# 33. LIU_SHA → YAN_NIAN

Meaning:

```text
SERVICE / SOCIAL
→
CAREER
```

Possible jobs:

- dịch vụ;
- đối ngoại;
- chăm sóc khách hàng;
- hành chính;
- làm đẹp;
- giao tiếp.

---

# 34. HUO_HAI → YAN_NIAN

Meaning:

```text
COMMUNICATION
→
CAREER
```

Possible:

- bán hàng;
- tư vấn;
- giảng dạy;
- truyền thông;
- pháp lý;
- đàm phán.

---

# 35. WU_GUI → YAN_NIAN

Meaning:

```text
INTELLIGENCE / CREATIVITY
→
CAREER
```

Possible:

- công nghệ;
- sáng tạo;
- thiết kế;
- nghiên cứu;
- phân tích;
- chiến lược.

---

# 36. JUE_MING → YAN_NIAN

Meaning:

```text
ACTION / COMPETITION
→
CAREER
```

Possible:

- kinh doanh;
- đầu tư;
- quản lý tài sản;
- nghề cạnh tranh;
- công việc cần tốc độ quyết định.

---

# 37. CAREER AFTER-STATE

Canonical:

```text
YAN_NIAN → Y
```

Y cho biết trải nghiệm
hoặc diễn biến sau công việc.

---

# 38. YAN_NIAN → SHENG_QI

Meaning:

- làm việc vui;
- có trợ lực;
- môi trường thuận.

---

# 39. YAN_NIAN → TIAN_Y

Meaning:

- chuyên môn sinh tài;
- công việc cho thành quả kinh tế.

---

# 40. YAN_NIAN → WU_GUI

Meaning:

- công việc biến động;
- nhiều suy nghĩ;
- thường xuyên đổi cách làm.

---

# 41. YAN_NIAN → LIU_SHA

Meaning:

- công việc ảnh hưởng cảm xúc;
- thiếu thoải mái;
- do dự;
- dễ mệt tâm lý.

---

# 42. YAN_NIAN → HUO_HAI

Meaning:

- công việc có tranh luận;
- phàn nàn;
- vấn đề giao tiếp.

---

# 43. YAN_NIAN → JUE_MING

Meaning:

- áp lực;
- hành động mạnh;
- dễ thay đổi quyết định;
- cạnh tranh cao.

---

# 44. YAN_NIAN → FU_WEI

Meaning:

- nghề nghiệp duy trì;
- năng lực được kéo dài;
- ổn định nhưng có thể thành trì trệ nếu quá mạnh.

---

# 45. CAREER + ZERO

YAN_NIAN_HIDDEN:

- năng lực có nhưng khó phát huy;
- khó được nhìn thấy;
- chuyên môn chưa được dùng đúng mức.

---

# 46. CAREER + FIVE

YAN_NIAN_AMPLIFIED:

- năng lực nổi bật;
- tính chuyên nghiệp rõ;
- khả năng lãnh đạo/chủ động dễ được thể hiện.

---

# 47. RELATIONSHIP DOMAIN

Core Energies:

```text
TIAN_Y
LIU_SHA
SHENG_QI
FU_WEI
```

Nhưng mỗi trường mang kiểu quan hệ khác nhau.

---

# 48. TIAN_Y — RELATIONSHIP

Canonical:

- chính Đào Hoa;
- tình cảm có khả năng đi tới ổn định;
- hôn nhân;
- kết đôi.

Strong Thiên Y
làm Relationship Domain nổi bật hơn.

---

# 49. SHENG_QI — RELATIONSHIP

Canonical:

- hòa hợp;
- thoải mái;
- duyên tự nhiên;
- quan hệ qua bạn bè/quý nhân.

---

# 50. LIU_SHA — RELATIONSHIP

Canonical:

- cảm xúc;
- duyên khác giới;
- sức hút;
- nhạy cảm;
- Đào Hoa;
- dễ phức tạp.

Không được equate:

LIU_SHA = ngoại tình.

---

# 51. FU_WEI — RELATIONSHIP

Canonical:

- kéo dài;
- chờ đợi;
- dè dặt;
- giữ trạng thái;
- khó thay đổi.

Nếu sau Lục Sát:

```text
LIU_SHA → FU_WEI
```

có thể:

- tình cảm kéo dài;
- do dự;
- khó dứt.

---

# 52. PRIMARY MARRIAGE PATTERNS

Knowledge Source:

```text
SHENG_QI → TIAN_Y
TIAN_Y → TIAN_Y
```

có thể liên hệ:

```text
PRIMARY_RELATIONSHIP_SUPPORT
```

Không nói:

> chắc chắn kết hôn.

Customer wording:

> Cấu trúc có trường hỗ trợ khá rõ
> cho việc hình thành và ổn định mối quan hệ.

---

# 53. RELATIONSHIP + ZERO

Example:

```text
103
608
```

Canonical:

```text
TIAN_Y_HIDDEN
```

Meaning:

- tình cảm kín;
- khó biểu đạt;
- khó nhận biết;
- trạng thái quan hệ không rõ.

Không kết luận:

- ngoại tình;
- ly hôn;
- người thứ ba.

---

# 54. RELATIONSHIP + FIVE

TIAN_Y_AMPLIFIED
hoặc LIU_SHA_AMPLIFIED:

- tình cảm biểu hiện rõ hơn;
- quan hệ trở thành chủ đề nổi bật.

Nếu là Lục Sát:

- cảm xúc mạnh hơn;
- Đào Hoa/quan hệ phức tạp cũng có thể tăng.

---

# 55. RELATIONSHIP RISK PATTERNS

Có thể gắn:

```text
RELATIONSHIP_COMPLEXITY
```

khi chain chứa:

- LIU_SHA → WU_GUI;
- LIU_SHA → LIU_SHA;
- LIU_SHA → FU_WEI;
- TIAN_Y → WU_GUI;
- nhiều Relationship Energy mất cân bằng.

Không dùng deterministic fate.

---

# 56. PERSONALITY DOMAIN

PERSONALITY lấy từ:

- dominant energy;
- repeated energy;
- strongest interaction;
- modifiers;
- balance.

Không kết luận tính cách
chỉ từ một pair.

---

# 57. SHENG_QI — PERSONALITY

Positive:

- lạc quan;
- cởi mở;
- dễ hòa nhập;
- mềm;
- nhân duyên.

Shadow:

- tùy duyên;
- thiếu chủ kiến;
- thiếu sức ép tiến lên.

---

# 58. TIAN_Y — PERSONALITY

Positive:

- thiện lương;
- thông minh;
- rộng rãi;
- dễ giúp người.

Shadow:

- dễ tin người;
- ít phòng bị;
- dễ bị lợi dụng.

---

# 59. YAN_NIAN — PERSONALITY

Positive:

- trách nhiệm;
- quyết đoán;
- chủ kiến;
- tổ chức;
- chịu áp lực.

Shadow:

- cứng;
- cố chấp;
- thích kiểm soát.

---

# 60. FU_WEI — PERSONALITY

Positive:

- kiên nhẫn;
- phân tích;
- bền bỉ;
- cẩn trọng.

Shadow:

- bảo thủ;
- do dự;
- bị động;
- thiếu cảm giác an toàn.

---

# 61. HUO_HAI — PERSONALITY

Positive:

- nói tốt;
- hùng biện;
- phản biện;
- biểu đạt.

Shadow:

- nóng lời;
- thích tranh luận;
- sĩ diện.

---

# 62. WU_GUI — PERSONALITY

Positive:

- thông minh;
- nhanh;
- sáng tạo;
- khác biệt.

Shadow:

- đa nghi;
- thiếu ổn định;
- thay đổi nhiều;
- suy nghĩ quá mức.

---

# 63. LIU_SHA — PERSONALITY

Positive:

- tinh tế;
- nhạy cảm;
- giao tế;
- thẩm mỹ.

Shadow:

- đa cảm;
- do dự;
- dễ bị tình cảm ảnh hưởng.

---

# 64. JUE_MING — PERSONALITY

Positive:

- dám làm;
- quyết liệt;
- nhanh;
- chịu áp lực;
- mạo hiểm.

Shadow:

- xung động;
- cực đoan;
- chủ quan;
- khó dừng.

---

# 65. SOCIAL DOMAIN

Primary Energies:

```text
SHENG_QI
LIU_SHA
HUO_HAI
```

Secondary:

```text
TIAN_Y
```

---

# 66. SOCIAL — SHENG_QI

- quý nhân;
- bạn bè;
- kết nối;
- quan hệ thuận.

---

# 67. SOCIAL — LIU_SHA

- giao tế;
- sự tinh tế;
- tương tác;
- quan hệ khác giới;
- khả năng đọc cảm xúc.

---

# 68. SOCIAL — HUO_HAI

- ngôn ngữ;
- nói;
- đàm phán;
- tranh luận.

---

# 69. INVESTMENT DOMAIN

Primary Energy:

```text
JUE_MING
```

Support:

```text
TIAN_Y
YAN_NIAN
WU_GUI
```

---

# 70. JUE_MING — INVESTMENT

Represents:

- risk appetite;
- hành động;
- đầu tư;
- quyết định nhanh;
- cạnh tranh.

Không phải:

> có Tuyệt Mệnh = đầu tư tốt.

---

# 71. JUE_MING → TIAN_Y

Canonical:

```text
ACTION / INVESTMENT
→
WEALTH
```

Investment effectiveness phụ thuộc strength relation.

---

# 72. TIAN_Y → JUE_MING

Canonical:

```text
RESOURCE
→
INVESTMENT
```

Meaning:

- vốn đi vào đầu tư;
- tiền được đưa vào hành động.

---

# 73. JUE_MING → WU_GUI

Canonical:

```text
RISK
→
VOLATILITY
```

Meaning:

- mức biến động cao;
- quyết định nhanh;
- tài chính khó ổn định.

---

# 74. JUE_MING → YAN_NIAN

Canonical:

```text
ACTION
→
STRUCTURE / CAREER
```

Can indicate:

- kinh doanh;
- đầu tư có tính tổ chức;
- bất động sản;
- quản lý tài sản.

---

# 75. INVESTMENT RISK–REWARD MATRIX

| Action/Risk | Result/Wealth | Meaning |
|---|---|---|
| Weak | Weak | thử nghiệm nhỏ |
| Weak | Strong | mức bỏ ra nhỏ, tiềm năng thu hoạch tốt |
| Strong | Strong | rủi ro lớn, tiềm năng thu hoạch lớn |
| Strong | Weak | mức rủi ro lớn hơn khả năng thu hoạch |

Không phải dự báo lợi nhuận.

---

# 76. LEARNING DOMAIN

Primary support:

```text
SHENG_QI
YAN_NIAN
FU_WEI
WU_GUI
```

mỗi trường đóng vai khác nhau.

---

# 77. SHENG_QI — LEARNING

- hứng thú;
- tiếp nhận mới;
- có người hỗ trợ;
- môi trường học thuận.

---

# 78. YAN_NIAN — LEARNING

- phương pháp;
- kỷ luật;
- tập trung;
- chuyên môn;
- tổ chức.

---

# 79. FU_WEI — LEARNING

- ngồi lâu;
- nghiên cứu;
- kiên trì;
- phân tích.

Risk:

- quá chậm;
- quá bảo thủ.

---

# 80. WU_GUI — LEARNING

- phản ứng nhanh;
- sáng tạo;
- suy luận;
- nghệ thuật;
- tư duy khác biệt.

Risk:

- dễ phân tán;
- đổi chủ đề nhiều.

---

# 81. LEARNING PATTERN

Canonical source pattern:

```text
SHENG_QI
→
YAN_NIAN
→
SHENG_QI
```

Meaning:

```text
motivation/support
→ method/discipline
→ positive learning state
```

---

# 82. WELLNESS_REFERENCE DOMAIN

IMPORTANT:

This domain is NOT medical diagnosis.

Canonical ID:

```text
WELLNESS_REFERENCE
```

Not:

```text
HEALTH_DIAGNOSIS
```

---

# 83. WELLNESS LANGUAGE POLICY

Allowed:

> Theo hệ thống Bát Cực Linh Số,
> trường này được liên hệ tham khảo
> với một số phương diện sức khỏe.

Not allowed:

> Bạn sẽ bị ung thư.

Not allowed:

> Số này gây tai nạn.

Not allowed:

> Bạn có bệnh gan.

---

# 84. WELLNESS — SHENG_QI SOURCE ASSOCIATIONS

Nguồn liên hệ:

- dạ dày;
- tai;
- mắt;
- mũi.

Customer:

> nên chú ý duy trì sinh hoạt cân bằng.

---

# 85. WELLNESS — TIAN_Y

Nguồn liên hệ:

- tuần hoàn;
- huyết áp;
- tai;
- mắt;
- mũi.

---

# 86. WELLNESS — YAN_NIAN

Nguồn liên hệ:

- vai;
- cổ;
- khớp;
- thần kinh;
- mất ngủ;
- áp lực.

---

# 87. WELLNESS — FU_WEI

Nguồn liên hệ:

- tim;
- não;
- trạng thái tích tụ.

---

# 88. WELLNESS — HUO_HAI

Nguồn liên hệ:

- khoang miệng;
- họng;
- khí quản;
- vùng ngực.

---

# 89. WELLNESS — WU_GUI

Nguồn liên hệ:

- tim;
- tuần hoàn;
- trạng thái đột phát.

Sensitive source claims
không customer-facing.

---

# 90. WELLNESS — LIU_SHA

Nguồn liên hệ:

- da;
- dạ dày;
- stress/cảm xúc.

---

# 91. WELLNESS — JUE_MING

Nguồn liên hệ:

- gan;
- thận;
- tiết niệu;
- quá sức.

No diagnosis.

---

# 92. BALANCE DOMAIN

BALANCE không hỏi:

> có bao nhiêu cát?

Mà hỏi:

1. Cát có làm chủ không?
2. Hung có đang làm dụng không?
3. Có Hung nào uncontrolled?
4. Terminal có cân bằng không?
5. 0/5 có làm lệch cấu trúc không?
6. Phục Vị đang kéo dài gì?
7. Chain có coherent không?

---

# 93. BALANCE STATES

Recommended:

```text
WELL_BALANCED
MOSTLY_BALANCED
BALANCED_WITH_CAUTION
MIXED
UNDER_CONTROLLED
VOLATILE
```

---

# 94. WELL_BALANCED

Typical traits:

- Cát có vai trò chủ;
- Hung có chức năng;
- control tương đối tốt;
- terminal thuận;
- không có repeated unresolved challenge lớn.

---

# 95. MIXED

Typical:

- có điểm mạnh;
- có rủi ro;
- terminal không quá xấu nhưng chưa hoàn toàn thuận;
- flow nhiều hướng.

Customer:

> Dãy có cả yếu tố hỗ trợ và yếu tố biến động.

---

# 96. VOLATILE

Possible:

- Ngũ Quỷ/Tuyệt Mệnh lặp mạnh;
- challenging tail;
- control yếu;
- nhiều transition khó ổn định.

Không dùng:

> đại hung.

---

# 97. DOMAIN CONFLICT

Một dãy có thể:

```text
WEALTH = STRONG
RELATIONSHIP = MIXED
CAREER = SUPPORTIVE
```

Đây là hợp lệ.

Không ép mọi domain
về cùng một grade.

---

# 98. PHONE DOMAIN PROFILE

Số điện thoại dùng đầy đủ:

```text
GENERAL
WEALTH
CAREER
RELATIONSHIP
PERSONALITY
SOCIAL
INVESTMENT
LEARNING
WELLNESS_REFERENCE
BALANCE
```

Recommended customer priority:

1. Tổng quan
2. Tài vận
3. Công việc
4. Tình cảm
5. Tính cách
6. Cân bằng
7. Khuyến nghị

Các domain khác có thể
hiển thị phụ hoặc Expert Mode.

---

# 99. VEHICLE PLATE DOMAIN PROFILE

Biển số xe ưu tiên:

```text
GENERAL
BALANCE
CAREER
WEALTH
ACTION
STABILITY
TERMINAL
```

Giảm trọng số:

```text
RELATIONSHIP
LEARNING
DEEP_PERSONALITY
```

---

# 100. VEHICLE — STABILITY

Vehicle-specific interpretation
có thể lấy từ:

- YAN_NIAN;
- SHENG_QI;
- FU_WEI context;
- control status;
- terminal state.

Không được dùng
wellness/accident claim từ sách
để dự đoán an toàn giao thông.

---

# 101. VEHICLE — ACTION

Tuyệt Mệnh trong Vehicle Profile:

đọc theo:

- tính hành động;
- tốc độ;
- mạo hiểm;
- biến động.

Không nói:

> biển số này gây tai nạn.

---

# 102. VEHICLE — WU_GUI

Ngũ Quỷ trong Vehicle Profile:

- biến động;
- thay đổi;
- tính khó đoán.

Nếu được chế bởi Sinh Khí:

- khả năng cân bằng tốt hơn.

---

# 103. PHONE VS VEHICLE SAME KNOWLEDGE

Canonical rule:

```text
SAME ENGINE
DIFFERENT DOMAIN WEIGHTING
```

Không xây 2 bộ huyền học riêng.

---

# 104. DOMAIN WEIGHTING — PHONE

Recommended conceptual weighting:

```text
GENERAL        HIGH
WEALTH         HIGH
CAREER         HIGH
RELATIONSHIP   HIGH
PERSONALITY    MEDIUM
SOCIAL         MEDIUM
INVESTMENT     CONTEXTUAL
LEARNING       LIGHT
WELLNESS       REFERENCE
BALANCE        HIGH
```

Engineering config only.

---

# 105. DOMAIN WEIGHTING — VEHICLE

Recommended:

```text
GENERAL        HIGH
BALANCE        HIGH
CAREER         MEDIUM-HIGH
WEALTH         MEDIUM-HIGH
ACTION         MEDIUM
STABILITY      HIGH
RELATIONSHIP   LOW
PERSONALITY    LOW
WELLNESS       OMIT / REFERENCE ONLY
```

---

# 106. DOMAIN FINDING MODEL

Recommended:

```text
DomainFinding {
    finding_id
    domain

    title
    structural_meaning

    evidence
    strength

    favorable_side
    caution_side

    position_relevance
    control_relevance

    customer_narrative_key
}
```

---

# 107. DOMAIN EVIDENCE

Evidence can include:

```text
pair
interaction
run
modifier
control
terminal
dominant_flow
```

Every Finding MUST have evidence.

Cursor MUST NOT invent
unsupported domain conclusions.

---

# 108. EVIDENCE PRIORITY

Recommended:

1. Whole-chain flow
2. Terminal interaction
3. Strong directed interaction
4. Repeated Energy
5. Strong pair
6. Single weak pair

---

# 109. SINGLE WEAK PAIR RULE

Một Tier 4 pair đơn lẻ,
ở đầu dãy,
không lặp,
không liên quan terminal:

thường không đủ
để tạo Primary Domain Finding.

---

# 110. REPEATED STRONG PAIR RULE

Một Energy mạnh,
lặp liên tục,
gần tail:

có thể tạo Primary Finding.

---

# 111. CUSTOMER LANGUAGE — WEALTH

Avoid:

> Số này rất giàu.

Preferred:

> Cấu trúc tài vận khá nổi bật,
> đặc biệt ở khả năng tạo giá trị thông qua...

---

# 112. CUSTOMER LANGUAGE — CAREER

Avoid:

> Số này làm quan.

Preferred:

> Dãy số nhấn mạnh năng lực chuyên môn,
> trách nhiệm và khả năng đảm nhận vai trò quản lý.

---

# 113. CUSTOMER LANGUAGE — RELATIONSHIP

Avoid:

> chắc chắn ngoại tình.

Preferred:

> Trường quan hệ khá mạnh,
> nhưng đi kèm yếu tố cảm xúc và biến động,
> vì vậy sự rõ ràng trong giao tiếp
> là điểm cần lưu ý.

---

# 114. CUSTOMER LANGUAGE — INVESTMENT

Avoid:

> đầu tư sẽ thắng.

Preferred:

> Dãy số có thiên hướng hành động
> và chấp nhận rủi ro cao hơn,
> phù hợp với môi trường cần quyết định nhanh,
> nhưng cần kiểm soát mức độ mạo hiểm.

---

# 115. CUSTOMER LANGUAGE — WELLNESS

Avoid:

> Bạn mắc bệnh tim.

Preferred:

> Theo hệ thống này,
> trường khí liên quan được xem là tín hiệu tham khảo
> để chú ý hơn tới cân bằng sinh hoạt và sức khỏe.

---

# 116. DOMAIN DEDUPLICATION

Nếu cùng một interaction
hỗ trợ nhiều domain:

không copy nguyên câu.

Ví dụ:

```text
WU_GUI → TIAN_Y
```

WEALTH:

> Trí tuệ/sáng tạo có khả năng tạo tài.

CAREER:

> Phù hợp công việc dùng tư duy và sáng tạo.

PERSONALITY:

> Điểm mạnh nằm ở phản ứng nhanh và khả năng nghĩ khác.

Mỗi domain dùng góc nhìn riêng.

---

# 117. DOMAIN CONTRADICTION

Nếu evidence trái chiều:

Ví dụ:

```text
WEALTH SOURCE strong
but
TAIL_RESOURCE_HIDDEN
```

Narrative:

> Khả năng tạo tài là điểm mạnh,
> tuy nhiên phần cuối cho thấy
> dòng tài nguyên chưa thật sự dễ tích tụ
> hoặc phát huy trọn vẹn.

Không chọn một phía và bỏ phía còn lại.

---

# 118. DOMAIN SUMMARY STRUCTURE

Recommended:

```text
1. Kết luận ngắn
2. Vì sao
3. Điểm mạnh
4. Điểm cần lưu ý
5. Gợi ý
```

---

# 119. GENERAL EXAMPLE

> Dãy số có cấu trúc khá linh hoạt,
> trong đó trường trí tuệ và sáng tạo
> chuyển về khả năng tạo thành quả.
> Điểm mạnh nằm ở tư duy nhanh và khả năng
> biến ý tưởng thành giá trị; điểm cần chú ý
> là duy trì sự ổn định khi đưa quyết định vào thực tế.

---

# 120. WEALTH EXAMPLE

For:

```text
WU_GUI → TIAN_Y
```

> Tài vận của dãy nghiêng về khả năng
> kiếm tiền bằng trí tuệ, ý tưởng hoặc chuyên môn.
> Cấu trúc phù hợp với công việc cần sáng tạo,
> phân tích hoặc xử lý vấn đề.
> Tuy nhiên, nếu trường biến động phía trước quá mạnh,
> cần chú ý tính ổn định trong quản lý tiền.

---

# 121. CAREER EXAMPLE

For:

```text
HUO_HAI → YAN_NIAN
```

> Năng lực nghề nghiệp nổi bật ở giao tiếp,
> thuyết phục và khả năng sử dụng ngôn ngữ.
> Đây là cấu trúc phù hợp với bán hàng,
> tư vấn, đào tạo, truyền thông hoặc các công việc
> cần trình bày và đàm phán.

---

# 122. RELATIONSHIP EXAMPLE

For:

```text
SHENG_QI → TIAN_Y
```

> Trường quan hệ có sự hỗ trợ khá tốt,
> dễ hình thành từ sự kết nối, giới thiệu
> hoặc môi trường quen biết.
> Khi Thiên Y đủ mạnh và phần đuôi ổn định,
> xu hướng xây dựng một mối quan hệ nghiêm túc
> sẽ nổi bật hơn.

---

# 123. BALANCE EXAMPLE

> Dãy có cả Cát và Hung nhưng các trường
> không đối đầu một cách rời rạc.
> Hung trường chủ yếu đóng vai trò tạo kỹ năng
> và được dẫn về các trường ổn định hơn,
> vì vậy cấu trúc tổng thể có tính cân bằng tương đối tốt.

---

# 124. RECOMMENDATION CONTEXT

File này chỉ xác định
loại recommendation cần tạo.

Ví dụ:

```text
WEALTH_STABILITY
CAREER_FOCUS
RELATIONSHIP_CLARITY
RISK_CONTROL
COMMUNICATION_CONTROL
BALANCE_SUPPORT
```

Câu recommendation cụ thể
nằm ở:

`10_CUSTOMER_NARRATIVE_CATALOG.md`

---

# 125. PHONE RECOMMENDATION PRIORITY

Suggested:

1. balance;
2. dominant strength;
3. key risk;
4. wealth/career;
5. relationship;
6. sequence improvement.

---

# 126. VEHICLE RECOMMENDATION PRIORITY

Suggested:

1. balance;
2. terminal stability;
3. action/risk;
4. work/wealth;
5. overall suitability.

---

# 127. OWNER COMPATIBILITY

V1 Domain Interpretation
không tự động xét:

- Bát Tự;
- Dụng Thần;
- Cung Phi chủ nhân;

trừ khi Owner Compatibility Layer
được gọi rõ ràng.

Number Energy Intrinsic Analysis
phải tách khỏi Owner Compatibility.

Canonical:

```text
NUMBER_STRUCTURE
!=
OWNER_COMPATIBILITY
```

---

# 128. FUTURE OWNER LAYER

Future flow:

```text
Intrinsic Number Analysis
↓
Owner Cung Phi
↓
Owner BaZi / Useful God
↓
Usage Purpose
↓
Personal Suitability
```

Không trộn vào V1 Intrinsic Truth.

---

# 129. INTERNAL DOMAIN IDS

Canonical:

```text
GENERAL
WEALTH
CAREER
RELATIONSHIP
PERSONALITY
SOCIAL
INVESTMENT
LEARNING
WELLNESS_REFERENCE
BALANCE
STABILITY
ACTION
```

---

# 130. CUSTOMER LABELS

```text
GENERAL
→ Tổng quan năng lượng

WEALTH
→ Tài vận

CAREER
→ Công việc & sự nghiệp

RELATIONSHIP
→ Tình cảm & quan hệ

PERSONALITY
→ Tính cách & năng lực

SOCIAL
→ Giao tiếp & nhân duyên

INVESTMENT
→ Đầu tư & mức độ mạo hiểm

LEARNING
→ Học tập & tư duy

WELLNESS_REFERENCE
→ Sức khỏe tham khảo

BALANCE
→ Cân bằng trường khí

STABILITY
→ Tính ổn định

ACTION
→ Khả năng hành động
```

---

# 131. EXPERT MODE

Expert Mode có thể hiển thị:

```text
Domain: WEALTH

Evidence:
WG(T1) → TY(T1)

Meaning:
Creative intelligence → wealth

Position:
REAR → TAIL

Control:
N/A

Modifier:
NONE

Prominence:
PRIMARY
```

Customer Mode chỉ hiển thị
nội dung đã biên tập.

---

# 132. DOMAIN ACCEPTANCE — 813

Input:

```text
813
```

Expected:

```text
81 = WU_GUI T1
13 = TIAN_Y T1

WEALTH:
PRIMARY

wealth_source:
INTELLIGENCE / CREATIVITY

terminal:
TIAN_Y
```

Customer direction:

> tạo tài bằng trí tuệ / ý tưởng.

---

# 133. DOMAIN ACCEPTANCE — 719

```text
71 = HUO_HAI
19 = YAN_NIAN
```

Expected CAREER:

```text
COMMUNICATION
→
CAREER
```

Primary occupation theme:

communication-based profession.

---

# 134. DOMAIN ACCEPTANCE — 619

Expected:

```text
LIU_SHA → YAN_NIAN
```

CAREER:

```text
SERVICE / SOCIAL
→
CAREER
```

Control:

```text
CTRL-LS-YN
```

Both preserved.

---

# 135. DOMAIN ACCEPTANCE — 213

Expected:

```text
JUE_MING → TIAN_Y
```

WEALTH:

```text
ACTION / INVESTMENT
→
WEALTH
```

INVESTMENT:

strong.

CONTROL:

```text
CTRL-JM-TY
```

---

# 136. DOMAIN ACCEPTANCE — 103

Expected:

```text
TIAN_Y_HIDDEN
```

WEALTH:

hidden / reduced visibility.

RELATIONSHIP:

hidden / reduced expression.

Not:

```text
AFFAIR
```

---

# 137. DOMAIN ACCEPTANCE — 153

Expected:

```text
TIAN_Y_AMPLIFIED
```

WEALTH:

more visible.

RELATIONSHIP:

more visible.

---

# 138. DOMAIN ACCEPTANCE — 181

Expected:

```text
WU_GUI → WU_GUI
```

PERSONALITY:

creative + unstable.

BALANCE:

volatility elevated.

WEALTH:

not automatically negative
unless chain supports it.

---

# 139. DOMAIN ACCEPTANCE — 131

Expected:

```text
TIAN_Y → TIAN_Y
```

WEALTH:

resource prominence high.

RELATIONSHIP:

relationship prominence high.

Need excessive/repetition caution.

---

# 140. DOMAIN ACCEPTANCE — MIXED

Example:

```text
SHENG_QI
→ TIAN_Y
→ WU_GUI
```

WEALTH:

source may be supportive.

BALANCE:

challenging terminal.

GENERAL:

mixed.

Must preserve contradiction.

---

# 141. INVALID IMPLEMENTATIONS

Forbidden:

```text
TIAN_Y present = rich
```

Forbidden:

```text
LIU_SHA present = affair
```

Forbidden:

```text
JUE_MING present = financial loss
```

Forbidden:

```text
HUO_HAI present = bad career
```

Forbidden:

```text
WU_GUI present = bad number
```

Forbidden:

```text
one pair creates primary domain
without context
```

Forbidden:

```text
medical diagnosis from number
```

Forbidden:

```text
vehicle plate relationship narrative
same weight as phone
```

---

# 142. DOMAIN PIPELINE

Canonical:

```text
CHAIN SUMMARY
↓
DOMAIN RELEVANCE FILTER
↓
EVIDENCE GROUPING
↓
PROMINENCE
↓
CONFLICT RESOLUTION
↓
DOMAIN FINDINGS
↓
NARRATIVE KEYS
↓
CUSTOMER NARRATIVE
```

---

# 143. NARRATIVE BOUNDARY

This file defines:

```text
WHAT TO SAY
```

at semantic level.

It does NOT define:

```text
EXACT CUSTOMER SENTENCE
```

Exact wording belongs to:

`10_CUSTOMER_NARRATIVE_CATALOG.md`

---

# 144. ENGINE BOUNDARY

File này chịu trách nhiệm:

```text
WHOLE-SEQUENCE STRUCTURE
→
DOMAIN FINDINGS
```

File này KHÔNG chịu trách nhiệm:

- final prose;
- UI presentation;
- PDF layout;
- scoring display;
- owner compatibility;
- recommendation sentence library.

---

# 145. NEXT DEPENDENCY

Output trực tiếp cho:

```text
10_CUSTOMER_NARRATIVE_CATALOG.md
11_ACCEPTANCE_GOLDEN_CASES.md
```

---

# 146. FREEZE RULE

Once accepted:

`09_DOMAIN_INTERPRETATION.md`

becomes canonical source of truth
for domain interpretation.

Cursor MUST NOT:

- invent new domains;
- map one Energy directly to fate;
- ignore chain evidence;
- ignore terminal state;
- ignore modifiers;
- ignore control;
- use medical diagnosis;
- use relationship accusation;
- copy Phone profile directly to Vehicle profile;
- treat all domains as equally strong;
- generate unsupported career/wealth conclusions.

Any change requires:

1. expert review;
2. canonical document update;
3. version bump;
4. regression tests;
5. Golden Dataset update.

---

# END OF DOCUMENT
```

Với `09` này, chúng ta đã hoàn tất phần **“engine hiểu gì về khách hàng”**. File tiếp theo `10_CUSTOMER_NARRATIVE_CATALOG.md` sẽ là phần rất quan trọng về thương mại: chúng ta tự viết các câu luận chuẩn, mềm, dễ hiểu và hấp dẫn cho từng Finding để Cursor chỉ **chọn + bind + ghép**, tuyệt đối không tự nghĩ câu chữ.