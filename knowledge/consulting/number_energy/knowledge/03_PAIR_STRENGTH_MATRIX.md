# 03_PAIR_STRENGTH_MATRIX.md

# BTE NUMBER ENERGY — PAIR STRENGTH MATRIX

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Pair Strength Matrix  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** CORE KNOWLEDGE  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`  
**Depends On:**
- `01_BAGUA_DIGIT_MAPPING.md`
- `02_EIGHT_ENERGY_CATALOG.md`

---

# 1. PURPOSE

Tài liệu này khóa thứ tự mạnh – yếu của các cặp số
thuộc tám trường khí Bát Cực Linh Số.

Mục tiêu:

PAIR
↓
ENERGY CLASS
↓
STRENGTH TIER
↓
RELATIVE INTENSITY
↓
INTERPRETATION WEIGHT

Nguyên tắc bắt buộc:

> Hai cặp số cùng thuộc một trường khí
> không mặc nhiên có cùng cường độ.

Ví dụ:

13 và 27 đều là Thiên Y.

Nhưng:

13 > 27

về cường độ trường khí.

Do đó engine không được chỉ lưu:

13 = THIEN_Y
27 = THIEN_Y

mà phải lưu thêm:

13 = THIEN_Y / TIER_1
27 = THIEN_Y / TIER_4

---

# 2. CORE PRINCIPLE

Mỗi trường khí gồm bốn cấp cường độ.

Canonical:

TIER_1 = mạnh nhất  
TIER_2 = mạnh  
TIER_3 = trung bình  
TIER_4 = yếu nhất trong cùng trường

Có thể biểu diễn:

TIER_1
>
TIER_2
>
TIER_3
>
TIER_4

Các từ:

- mạnh nhất;
- mạnh;
- trung bình;
- yếu;

chỉ là mô tả tương đối
TRONG CÙNG MỘT ENERGY FAMILY.

Không được hiểu:

TIER_4 = không có tác dụng.

TIER_4 vẫn mang đầy đủ Energy Class,
nhưng cường độ biểu hiện thấp hơn.

---

# 3. DIRECTION REVERSAL PRESERVES STRENGTH TIER

Trong cùng một cặp đảo chiều:

AB
BA

Energy Class giống nhau
và Strength Tier giống nhau.

Ví dụ:

13 = Thiên Y / Tier 1  
31 = Thiên Y / Tier 1

68 = Thiên Y / Tier 2  
86 = Thiên Y / Tier 2

Canonical:

strength(AB) = strength(BA)

ở tầng Pair Strength.

Điều này KHÔNG xóa directional meaning
ở tầng chuỗi nhiều trường khí.

---

# 4. STRENGTH SCALE

Canonical internal representation:

| Tier | ID | Relative Weight | Customer Meaning |
|---|---|---:|---|
| 1 | VERY_STRONG | 1.00 | Trường khí rất mạnh |
| 2 | STRONG | 0.75 | Trường khí mạnh |
| 3 | MEDIUM | 0.50 | Trường khí trung bình |
| 4 | LIGHT | 0.25 | Trường khí nhẹ |

IMPORTANT:

Các giá trị:

1.00 / 0.75 / 0.50 / 0.25

là **normalized engineering weights** phục vụ:

- ranking;
- comparison;
- aggregation;
- deterministic testing.

Chúng KHÔNG phải điểm huyền học gốc.

Không được hiển thị cho khách hàng dưới dạng:

“Thiên Y = 75%”

trừ khi sau này có một Score Standard riêng
định nghĩa rõ cách chuyển đổi.

---

# 5. THIÊN Y — STRENGTH MATRIX

Canonical order:

13 / 31
>
68 / 86
>
49 / 94
>
27 / 72

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 13 | 31 | 1 | 1.00 |
| 68 | 86 | 2 | 0.75 |
| 49 | 94 | 3 | 0.50 |
| 27 | 72 | 4 | 0.25 |

Canonical IDs:

13,31 = TIAN_Y_T1  
68,86 = TIAN_Y_T2  
49,94 = TIAN_Y_T3  
27,72 = TIAN_Y_T4

Interpretive principle:

Tier càng cao:

- đặc tính Thiên Y càng nổi bật;
- khả năng tác động vào Wealth/Relationship
  càng đáng được ưu tiên khi tổng hợp;
- interaction chứa Thiên Y càng có trọng lượng.

Không được kết luận độc lập
chỉ dựa trên Tier.

---

# 6. SINH KHÍ — STRENGTH MATRIX

Canonical order:

14 / 41
>
67 / 76
>
39 / 93
>
28 / 82

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 14 | 41 | 1 | 1.00 |
| 67 | 76 | 2 | 0.75 |
| 39 | 93 | 3 | 0.50 |
| 28 | 82 | 4 | 0.25 |

Canonical IDs:

14,41 = SHENG_QI_T1  
67,76 = SHENG_QI_T2  
39,93 = SHENG_QI_T3  
28,82 = SHENG_QI_T4

Interpretive principle:

Tier càng cao:

- quý nhân / trợ lực / cơ hội càng nổi;
- Sinh Khí càng có khả năng trở thành
  dominant support field;
- interaction với trường khác càng cần
  được ưu tiên trong narrative.

---

# 7. DIÊN NIÊN — STRENGTH MATRIX

Canonical order:

19 / 91
>
78 / 87
>
34 / 43
>
26 / 62

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 19 | 91 | 1 | 1.00 |
| 78 | 87 | 2 | 0.75 |
| 34 | 43 | 3 | 0.50 |
| 26 | 62 | 4 | 0.25 |

Canonical IDs:

19,91 = YAN_NIAN_T1  
78,87 = YAN_NIAN_T2  
34,43 = YAN_NIAN_T3  
26,62 = YAN_NIAN_T4

Interpretive principle:

Tier càng cao:

- tính chuyên nghiệp;
- trách nhiệm;
- khả năng tổ chức;
- sức làm việc;
- tính chủ động/lãnh đạo

càng dễ trở thành tín hiệu nổi bật.

Nhưng Diên Niên quá mạnh
không được mặc nhiên luận là hoàn toàn tốt.

Phải tiếp tục xét:

- giới tính;
- vị trí;
- trường đứng trước;
- trường đứng sau;
- repetition;
- modifiers;
- whole-sequence balance.

---

# 8. PHỤC VỊ — STRENGTH MATRIX

Canonical order theo dữ liệu đã khóa:

11 / 22
>
88 / 99
>
66 / 77
>
33 / 44

| Pair Group | Tier | Weight |
|---|---:|---:|
| 11, 22 | 1 | 1.00 |
| 88, 99 | 2 | 0.75 |
| 66, 77 | 3 | 0.50 |
| 33, 44 | 4 | 0.25 |

Canonical IDs:

11,22 = FU_WEI_T1  
88,99 = FU_WEI_T2  
66,77 = FU_WEI_T3  
33,44 = FU_WEI_T4

IMPORTANT:

Phục Vị là trường phụ thuộc context.

Strength của Phục Vị KHÔNG được
tự động chuyển thành positive score.

Ví dụ:

BAD
→ FU_WEI_T1

có thể kéo dài / tăng tính dai dẳng
của một trạng thái bất lợi.

GOOD
→ FU_WEI_T1

có thể duy trì trường thuận lợi.

Do đó:

FU_WEI_STRENGTH
=
AMPLIFICATION / CONTINUATION CAPACITY

không phải:

FU_WEI_STRENGTH
=
GOODNESS.

---

# 9. HỌA HẠI — STRENGTH MATRIX

Canonical order:

17 / 71
>
89 / 98
>
46 / 64
>
23 / 32

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 17 | 71 | 1 | 1.00 |
| 89 | 98 | 2 | 0.75 |
| 46 | 64 | 3 | 0.50 |
| 23 | 32 | 4 | 0.25 |

Canonical IDs:

17,71 = HUO_HAI_T1  
89,98 = HUO_HAI_T2  
46,64 = HUO_HAI_T3  
23,32 = HUO_HAI_T4

Interpretive principle:

Tier càng cao,
đặc tính Họa Hại càng rõ:

Positive functional expression:

- khẩu tài;
- biểu đạt;
- phản biện;
- thuyết phục.

Risk expression:

- tranh luận;
- thị phi;
- nóng lời;
- xung đột giao tiếp.

Engine MUST xét trường đứng sau
để biết năng lực khẩu tài đang
được chuyển về domain nào.

---

# 10. NGŨ QUỶ — STRENGTH MATRIX

Canonical order:

18 / 81
>
79 / 97
>
36 / 63
>
24 / 42

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 18 | 81 | 1 | 1.00 |
| 79 | 97 | 2 | 0.75 |
| 36 | 63 | 3 | 0.50 |
| 24 | 42 | 4 | 0.25 |

Canonical IDs:

18,81 = WU_GUI_T1  
79,97 = WU_GUI_T2  
36,63 = WU_GUI_T3  
24,42 = WU_GUI_T4

Interpretive principle:

Tier càng cao,
đặc tính Ngũ Quỷ càng nổi:

Functional:

- trí tuệ;
- phản ứng;
- sáng tạo;
- biến hóa;
- ý tưởng.

Risk:

- bất ổn;
- đa nghi;
- thay đổi;
- suy nghĩ quá nhiều;
- biến động.

Ngũ Quỷ mạnh không được tự động
chuyển thành negative final judgment.

Phải xét:

WU_GUI
→ WHAT?

Ví dụ:

WU_GUI → TIAN_Y

khác hoàn toàn:

WU_GUI → WU_GUI.

---

# 11. LỤC SÁT — STRENGTH MATRIX

Canonical order:

16 / 61
>
47 / 74
>
38 / 83
>
29 / 92

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 16 | 61 | 1 | 1.00 |
| 47 | 74 | 2 | 0.75 |
| 38 | 83 | 3 | 0.50 |
| 29 | 92 | 4 | 0.25 |

Canonical IDs:

16,61 = LIU_SHA_T1  
47,74 = LIU_SHA_T2  
38,83 = LIU_SHA_T3  
29,92 = LIU_SHA_T4

Interpretive principle:

Tier càng cao,
đặc tính Lục Sát càng rõ:

Functional:

- giao tế;
- nhân duyên;
- cảm nhận;
- thẩm mỹ;
- dịch vụ;
- khả năng tương tác.

Risk:

- cảm xúc;
- do dự;
- nhạy cảm;
- Đào Hoa;
- bất ổn quan hệ.

Không được kết luận tình cảm
chỉ từ một Lục Sát đơn lẻ.

---

# 12. TUYỆT MỆNH — STRENGTH MATRIX

Canonical order:

12 / 21
>
69 / 96
>
48 / 84
>
37 / 73

| Pair | Reverse | Tier | Weight |
|---|---|---:|---:|
| 12 | 21 | 1 | 1.00 |
| 69 | 96 | 2 | 0.75 |
| 48 | 84 | 3 | 0.50 |
| 37 | 73 | 4 | 0.25 |

Canonical IDs:

12,21 = JUE_MING_T1  
69,96 = JUE_MING_T2  
48,84 = JUE_MING_T3  
37,73 = JUE_MING_T4

Interpretive principle:

Tier càng cao,
đặc tính Tuyệt Mệnh càng mạnh:

Functional:

- hành động;
- quyết đoán;
- đầu tư;
- cạnh tranh;
- dám làm;
- chịu áp lực.

Risk:

- xung động;
- cực đoan;
- mạo hiểm;
- tiêu hao;
- quyết định cảm tính.

Tuyệt Mệnh mạnh
KHÔNG đồng nghĩa final result luôn xấu.

Phải xét:

- trường đứng sau;
- chế hóa;
- vị trí;
- tail;
- repetition;
- 0/5;
- domain.

---

# 13. COMPLETE PAIR STRENGTH MATRIX

| Energy | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Thiên Y | 13/31 | 68/86 | 49/94 | 27/72 |
| Sinh Khí | 14/41 | 67/76 | 39/93 | 28/82 |
| Diên Niên | 19/91 | 78/87 | 34/43 | 26/62 |
| Phục Vị | 11/22 | 88/99 | 66/77 | 33/44 |
| Họa Hại | 17/71 | 89/98 | 46/64 | 23/32 |
| Ngũ Quỷ | 18/81 | 79/97 | 36/63 | 24/42 |
| Lục Sát | 16/61 | 47/74 | 38/83 | 29/92 |
| Tuyệt Mệnh | 12/21 | 69/96 | 48/84 | 37/73 |

This table is CANONICAL.

---

# 14. STRENGTH ≠ VALENCE

Critical rule:

STRENGTH
!=
GOOD / BAD

Ví dụ:

TIAN_Y_T1

nghĩa là:

Thiên Y biểu hiện mạnh.

Không có nghĩa:

100% tốt.

Tương tự:

WU_GUI_T1

nghĩa là:

Ngũ Quỷ biểu hiện mạnh.

Không có nghĩa:

100% xấu.

Final meaning phải qua:

ENERGY
+
STRENGTH
+
POSITION
+
DIRECTION
+
INTERACTION
+
MODIFIER
+
CONTROL
+
DOMAIN
+
WHOLE_SEQUENCE

---

# 15. STRENGTH ≠ SCORE

Không được sử dụng trực tiếp:

Tier 1 = +100  
Tier 2 = +75  
Tier 3 = +50  
Tier 4 = +25

cho cát trường,

và:

Tier 1 = -100  
Tier 2 = -75...

cho hung trường.

Đó là mô hình sai.

Weight chỉ đo:

RELATIVE ENERGY INTENSITY

không đo:

FINAL QUALITY.

---

# 16. SAME ENERGY REPETITION

Nếu một dãy có nhiều pair
cùng Energy Class:

ví dụ:

13
31
68

thì không được chỉ chọn một pair.

Engine phải ghi nhận:

- count;
- tiers;
- positions;
- continuity;
- overlap;
- modifier;
- domain context.

Recommended:

energy_presence = Σ contextual_pair_weight

Nhưng final interpretation
không được chỉ dựa vào tổng số học.

---

# 17. OVERLAPPING PAIRS

Ví dụ:

131

sinh ra:

13 = Thiên Y Tier 1  
31 = Thiên Y Tier 1

Đây là:

CONTINUOUS_REINFORCEMENT

không chỉ là:

“có hai Thiên Y”.

Tương tự:

181

18 = Ngũ Quỷ Tier 1  
81 = Ngũ Quỷ Tier 1

là:

CONTINUOUS_WU_GUI_REINFORCEMENT

và phải được đánh dấu
là cấu trúc cường hóa mạnh.

Chi tiết triple semantics
do file `04_DIRECTED_INTERACTION_MATRIX.md`
và `08_CHAIN_INTERPRETATION_RULES.md` xử lý.

---

# 18. TIER TRANSITION

Trong chuỗi cùng Energy Family:

TIER_1 → TIER_4

có thể biểu thị xu hướng:

STRONG
→
WEAKENING

Trong khi:

TIER_4 → TIER_1

có thể biểu thị:

WEAK
→
STRENGTHENING

Ví dụ:

Diên Niên lớn → Diên Niên nhỏ

không được luận giống:

Diên Niên nhỏ → Diên Niên lớn.

Pair Strength Matrix chỉ cung cấp
cường độ.

Sequence Engine quyết định
ý nghĩa dòng chuyển động.

---

# 19. LARGE / SMALL TERMINOLOGY

Customer Narrative không nên lạm dụng:

“đại năng lượng”
“tiểu năng lượng”

Recommended internal terminology:

TIER_1 = very strong  
TIER_2 = strong  
TIER_3 = moderate  
TIER_4 = light

Customer Vietnamese:

TIER_1:
“trường khí nổi bật và có cường độ mạnh”

TIER_2:
“trường khí tương đối mạnh”

TIER_3:
“trường khí ở mức vừa”

TIER_4:
“tr