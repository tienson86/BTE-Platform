# 01_BAGUA_DIGIT_MAPPING.md

# BTE NUMBER ENERGY — BAGUA DIGIT MAPPING STANDARD

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Bagua Digit Mapping  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** CORE KNOWLEDGE  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`

---

# 1. PURPOSE

Tài liệu này khóa bảng quy chiếu cơ sở giữa:

DIGIT
↓
HẬU THIÊN BÁT QUÁI
↓
QUÁI
↓
PHƯƠNG VỊ
↓
NGŨ HÀNH
↓
ĐÔNG / TÂY TỨ
↓
TAM HÀO
↓
BÁT BIẾN DU NIÊN

Đây là tầng dữ liệu nền của toàn bộ
Number Energy Engine.

Mọi Pair Resolver, Energy Resolver,
Interaction Engine và Validation Engine
MUST sử dụng mapping trong tài liệu này.

Không implementation layer nào được phép
tự thay đổi mapping.

---

# 2. CANONICAL DIGIT → BAGUA MAPPING

| Digit | Quái | Vietnamese | Direction | Element | Group |
|---:|---|---|---|---|---|
| 1 | 坎 | Khảm | Bắc | Thủy | Đông Tứ |
| 2 | 坤 | Khôn | Tây Nam | Thổ | Tây Tứ |
| 3 | 震 | Chấn | Đông | Mộc | Đông Tứ |
| 4 | 巽 | Tốn | Đông Nam | Mộc | Đông Tứ |
| 5 | 中 | Trung Cung | Trung | Thổ | SPECIAL |
| 6 | 乾 | Càn | Tây Bắc | Kim | Tây Tứ |
| 7 | 兌 | Đoài | Tây | Kim | Tây Tứ |
| 8 | 艮 | Cấn | Đông Bắc | Thổ | Tây Tứ |
| 9 | 離 | Ly | Nam | Hỏa | Đông Tứ |
| 0 | — | Không quái | — | — | SPECIAL |

Canonical IDs:

```text
1 = KAN
2 = KUN
3 = ZHEN
4 = XUN
5 = CENTER
6 = QIAN
7 = DUI
8 = GEN
9 = LI
0 = ZERO
```

---

# 3. EIGHT ACTIVE BAGUA DIGITS

Tám chữ số trực tiếp tham gia
Pair → Du Niên là:

```text
1
2
3
4
6
7
8
9
```

Canonical set:

```text
ACTIVE_BAGUA_DIGITS =
{1, 2, 3, 4, 6, 7, 8, 9}
```

Số `0` và `5` KHÔNG thuộc tập này.

Do đó:

```text
0 ∉ ACTIVE_BAGUA_DIGITS
5 ∉ ACTIVE_BAGUA_DIGITS
```

---

# 4. EAST FOUR GROUP

Đông Tứ gồm:

| Digit | Quái | Element |
|---:|---|---|
| 1 | Khảm | Thủy |
| 3 | Chấn | Mộc |
| 4 | Tốn | Mộc |
| 9 | Ly | Hỏa |

Canonical:

```text
EAST_GROUP = {1, 3, 4, 9}
```

ID:

```text
DONG_TU
```

---

# 5. WEST FOUR GROUP

Tây Tứ gồm:

| Digit | Quái | Element |
|---:|---|---|
| 2 | Khôn | Thổ |
| 6 | Càn | Kim |
| 7 | Đoài | Kim |
| 8 | Cấn | Thổ |

Canonical:

```text
WEST_GROUP = {2, 6, 7, 8}
```

ID:

```text
TAY_TU
```

---

# 6. SPECIAL DIGIT — ZERO

## 6.1 Definition

Số `0` không đại diện cho một quái
trong tám quái số dùng để tạo Du Niên.

Canonical ID:

```text
ZERO
```

Canonical class:

```text
SPECIAL_MODIFIER
```

Canonical polarity:

```text
YIN
```

Core semantic:

```text
hidden
latent
reduced_expression
concealed
interrupted
```

---

# 7. ZERO MUST NOT CREATE A NORMAL PAIR

Ví dụ:

```text
10
01
20
02
30
03
...
```

KHÔNG được Pair Resolver xử lý như:

```text
Bagua A
+
Bagua B
=
Du Nien
```

vì `0` không phải Active Bagua Digit.

Thay vào đó phải chuyển sang:

```text
ZERO_MODIFIER_ENGINE
```

---

# 8. ZERO POSITION MATTERS

Phải phân biệt ít nhất:

```text
AB0
A0B
0AB
```

Trong đó A và B là Active Bagua Digits.

## 8.1 AB0

```text
A → B → 0
```

Pair `AB` đã hình thành trường khí.

Sau đó `0` tác động lên trường đó.

Canonical concept:

```text
formed_energy
→ hidden / reduced
```

---

## 8.2 A0B

```text
A → 0 → B
```

0 nằm giữa hai quái số.

Không được xử lý giống `AB0`.

Canonical concept:

```text
potential_relation(A,B)
→ interrupted / concealed
```

Ví dụ:

```text
103
```

Không được naïvely parse thành:

```text
10 + 03
```

Mà phải nhận diện:

```text
1 - 0 - 3
```

với underlying pair:

```text
13 = TIAN_Y
```

và modifier:

```text
0 = hidden
```

---

## 8.3 0AB

```text
0 → A → B
```

Pair `AB` vẫn phải được nhận diện.

0 là contextual modifier phía trước.

Chi tiết narrative do
`05_ZERO_FIVE_MODIFIERS.md` quyết định.

---

# 9. SPECIAL DIGIT — FIVE

## 9.1 Definition

Số `5` thuộc Trung Cung.

Canonical:

```text
digit = 5
bagua = CENTER
element = EARTH
polarity = YANG
```

Nhưng trong Bát Cực Linh Số:

```text
5 != NORMAL_DU_NIEN_DIGIT
```

Canonical class:

```text
SPECIAL_MODIFIER
```

Core semantic:

```text
explicit
activated
amplified
strengthened
extended
```

---

# 10. FIVE MUST NOT CREATE NORMAL DU NIEN

Các cấu trúc:

```text
15
51
25
52
35
53
...
```

không được resolver gán trực tiếp
một trong tám Du Niên chỉ dựa trên `5`.

Chúng phải được xử lý bởi:

```text
FIVE_MODIFIER_ENGINE
```

---

# 11. FIVE POSITION MATTERS

Phải phân biệt:

```text
AB5
A5B
5AB
```

## AB5

Trường `AB` đã hình thành.

Sau đó số 5 làm trường đó
hiển/lộ/tăng cường tùy context.

## A5B

5 chen giữa A và B.

Underlying relationship A↔B
phải được bảo tồn để Modifier Engine xử lý.

## 5AB

5 tác động từ phía trước lên
cấu trúc `AB`.

Chi tiết được định nghĩa trong:

`05_ZERO_FIVE_MODIFIERS.md`

---

# 12. ZERO AND FIVE ARE NOT PHUC VI

Important canonical distinction:

```text
0 != PHUC_VI
5 != PHUC_VI
```

Phục Vị chuẩn được tạo bởi
các quái giống nhau:

```text
11
22
33
44
66
77
88
99
```

0 và 5 có thể mang tính chất
kéo dài / ẩn / hiển trong một số cấu trúc,
nhưng KHÔNG được đổi classification thành
Du Niên Phục Vị.

---

# 13. BAGUA TRIGRAM FOUNDATION

Bát Quái được hình thành từ ba hào.

Canonical trigram order:

```text
THƯỢNG HÀO
TRUNG HÀO
HẠ HÀO
```

Hay theo semantic layer:

```text
THIÊN
NHÂN
ĐỊA
```

Implementation MUST sử dụng một quy ước
bit-order duy nhất và không được thay đổi
giữa các engine.

---

# 14. CANONICAL TRIGRAM LINES

Quy ước:

```text
1 = Dương
0 = Âm
```

Canonical representation theo thứ tự:

```text
[HẠ, TRUNG, THƯỢNG]
```

| Digit | Quái | Hạ | Trung | Thượng |
|---:|---|---:|---:|---:|
| 1 | Khảm | 0 | 1 | 0 |
| 2 | Khôn | 0 | 0 | 0 |
| 3 | Chấn | 1 | 0 | 0 |
| 4 | Tốn | 0 | 1 | 1 |
| 6 | Càn | 1 | 1 | 1 |
| 7 | Đoài | 1 | 1 | 0 |
| 8 | Cấn | 0 | 0 | 1 |
| 9 | Ly | 1 | 0 | 1 |

Canonical objects:

```text
KAN  = [0,1,0]
KUN  = [0,0,0]
ZHEN = [1,0,0]
XUN  = [0,1,1]
QIAN = [1,1,1]
DUI  = [1,1,0]
GEN  = [0,0,1]
LI   = [1,0,1]
```

---

# 15. DU NIEN FORMATION PRINCIPLE

Hai quái được so sánh theo ba hào.

Mẫu biến hào xác định Du Niên.

Canonical comparison:

```text
LOWER
MIDDLE
UPPER
```

---

# 16. BÁT BIẾN DU NIÊN — CANONICAL RULE

## 16.1 Sinh Khí

Khác:

```text
THƯỢNG
```

Giống:

```text
TRUNG
HẠ
```

Canonical mutation mask:

```text
[0,0,1]
```

Energy:

```text
SHENG_QI
```

---

## 16.2 Tuyệt Mệnh

Khác:

```text
TRUNG
```

Giống:

```text
THƯỢNG
HẠ
```

Mutation mask:

```text
[0,1,0]
```

Energy:

```text
JUE_MING
```

---

## 16.3 Họa Hại

Khác:

```text
HẠ
```

Giống:

```text
TRUNG
THƯỢNG
```

Mutation mask:

```text
[1,0,0]
```

Energy:

```text
HUO_HAI
```

---

## 16.4 Ngũ Quỷ

Khác:

```text
TRUNG
THƯỢNG
```

Giống:

```text
HẠ
```

Mutation mask:

```text
[0,1,1]
```

Energy:

```text
WU_GUI
```

---

## 16.5 Thiên Y

Khác:

```text
HẠ
TRUNG
```

Giống:

```text
THƯỢNG
```

Mutation mask:

```text
[1,1,0]
```

Energy:

```text
TIAN_Y
```

---

## 16.6 Lục Sát

Khác:

```text
HẠ
THƯỢNG
```

Giống:

```text
TRUNG
```

Mutation mask:

```text
[1,0,1]
```

Energy:

```text
LIU_SHA
```

---

## 16.7 Diên Niên

Khác cả:

```text
HẠ
TRUNG
THƯỢNG
```

Mutation mask:

```text
[1,1,1]
```

Energy:

```text
YAN_NIAN
```

---

## 16.8 Phục Vị

Không hào nào biến.

Mutation mask:

```text
[0,0,0]
```

Energy:

```text
FU_WEI
```

---

# 17. COMPLETE MUTATION TABLE

| Hạ | Trung | Thượng | Energy |
|---:|---:|---:|---|
| 0 | 0 | 0 | Phục Vị |
| 1 | 0 | 0 | Họa Hại |
| 0 | 1 | 0 | Tuyệt Mệnh |
| 0 | 0 | 1 | Sinh Khí |
| 1 | 1 | 0 | Thiên Y |
| 1 | 0 | 1 | Lục Sát |
| 0 | 1 | 1 | Ngũ Quỷ |
| 1 | 1 | 1 | Diên Niên |

Đây là canonical truth table.

---

# 18. DERIVED PAIR VALIDATION

Từ trigram mapping và mutation table,
engine MUST tự suy ra đúng Pair Catalog.

## Sinh Khí

```text
14 41
67 76
39 93
28 82
```

## Thiên Y

```text
13 31
68 86
49 94
27 72
```

## Diên Niên

```text
19 91
78 87
34 43
26 62
```

## Phục Vị

```text
11 22 33 44
66 77 88 99
```

## Họa Hại

```text
17 71
89 98
46 64
23 32
```

## Ngũ Quỷ

```text
18 81
79 97
36 63
24 42
```

## Lục Sát

```text
16 61
47 74
38 83
29 92
```

## Tuyệt Mệnh

```text
12 21
69 96
48 84
37 73
```

---

# 19. PAIR SYMMETRY AT CLASSIFICATION LEVEL

Ở tầng xác định loại Du Niên:

```text
AB
BA
```

có cùng Energy Class.

Ví dụ:

```text
13 = TIAN_Y
31 = TIAN_Y
```

```text
18 = WU_GUI
81 = WU_GUI
```

```text
19 = YAN_NIAN
91 = YAN_NIAN
```

Nhưng điều này KHÔNG có nghĩa:

```text
AB == BA
```

ở mọi tầng luận giải.

Classification symmetry:

```text
TRUE
```

Narrative / sequence symmetry:

```text
NOT GUARANTEED
```

Thứ tự vẫn phải được giữ nguyên trong
Sequence Engine.

---

# 20. PAIR RESOLUTION ALGORITHM

Input:

```text
digit_a
digit_b
```

## Step 1

Kiểm tra cả hai digit có thuộc:

```text
ACTIVE_BAGUA_DIGITS
```

hay không.

Nếu YES:

```text
resolve trigram A
resolve trigram B
```

## Step 2

XOR ba hào:

```text
mutation =
trigram_A XOR trigram_B
```

## Step 3

Tra mutation table.

## Step 4

Return:

```text
pair
energy_id
energy_name
bagua_a
bagua_b
mutation_mask
```

Nếu A hoặc B là `0` hoặc `5`:

```text
DO NOT resolve normal Du Nien
```

Chuyển sang Modifier Engine.

---

# 21. CANONICAL DATA CONTRACT

Recommended object:

```text
BaguaDigit {
    digit
    bagua_id
    bagua_name
    direction
    element
    group
    polarity
    trigram
    active_for_du_nien
    modifier_type
}
```

Example:

```text
{
  digit: 1,
  bagua_id: "KAN",
  bagua_name: "Khảm",
  direction: "Bắc",
  element: "THUY",
  group: "DONG_TU",
  trigram: [0,1,0],
  active_for_du_nien: true,
  modifier_type: null
}
```

---

# 22. ZERO CONTRACT

```text
{
  digit: 0,
  bagua_id: null,
  bagua_name: null,
  direction: null,
  element: null,
  group: "SPECIAL",
  polarity: "YIN",
  trigram: null,
  active_for_du_nien: false,
  modifier_type: "HIDDEN"
}
```

---

# 23. FIVE CONTRACT

```text
{
  digit: 5,
  bagua_id: "CENTER",
  bagua_name: "Trung Cung",
  direction: "Trung",
  element: "THO",
  group: "SPECIAL",
  polarity: "YANG",
  trigram: null,
  active_for_du_nien: false,
  modifier_type: "AMPLIFY"
}
```

---

# 24. ENGINE BOUNDARY

File này CHỈ chịu trách nhiệm:

```text
DIGIT
→ BAGUA
→ TRIGRAM
→ DU_NIEN_CLASSIFICATION
```

File này KHÔNG chịu trách nhiệm:

- mạnh/yếu;
- tài vận;
- nghề nghiệp;
- tình cảm;
- sức khỏe;
- 0/5 narrative;
- vị trí;
- tổ hợp ba số;
- chế hóa;