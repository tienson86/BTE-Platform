# 07_combination_rules

## Mục đích

Module `07_combination_rules` định nghĩa toàn bộ các quy tắc kết hợp (Combination Rules) của BTE Platform.

Đây là tầng Rule Engine dùng để tổng hợp kết quả từ nhiều nhóm quy tắc khác nhau nhằm đưa ra kết luận cuối cùng.

Module này không tính toán trực tiếp mà chỉ mô tả:

- Điều kiện áp dụng
- Độ ưu tiên
- Nhãn kết quả
- Ví dụ kiểm thử
- Quy tắc ghi đè (Override)
- Quy tắc kết hợp nhiều điều kiện

---

# Cấu trúc thư mục

```text
07_combination_rules/
├── combination_rules.json
├── combination_conditions.json
├── combination_priority.json
├── combination_labels.json
├── combination_examples.json
└── README.md
```

---

# Các file dữ liệu

## combination_rules.json

Chứa danh sách toàn bộ Combination Rule.

Mỗi Rule bao gồm:

- Rule ID
- Rule Code
- Category
- Điều kiện
- Kết quả
- Trạng thái

Ví dụ:

```json
{
  "id": "CBR001",
  "rule_code": "strength_pattern_support",
  "category": "strength_pattern"
}
```

---

## combination_conditions.json

Mô tả chi tiết điều kiện để Combination Rule được kích hoạt.

Ví dụ:

- Strength = Vuong
- Season = Phu Hop
- Pattern = Chinh Cach

Rule Engine sẽ sử dụng file này để kiểm tra dữ liệu đầu vào.

---

## combination_priority.json

Định nghĩa mức ưu tiên giữa các Rule.

Ví dụ:

- Priority 100
- Priority 90
- Priority 80

Khi nhiều Rule cùng khớp:

Rule có Priority cao hơn sẽ được ưu tiên.

---

## combination_labels.json

Định nghĩa Label trả về.

Ví dụ:

- support
- weaken
- balanced
- adjust
- confirmed
- candidate
- override
- complete

Label được sử dụng cho:

- Interpretation Engine
- Report Engine
- API Output
- Frontend

---

## combination_examples.json

Golden Dataset dùng để kiểm thử Rule Engine.

Bao gồm:

- dữ liệu đầu vào
- Rule tương ứng
- Priority
- Label
- Expected Result

Ví dụ:

```json
{
  "rule_id": "CBR001",
  "expected_result": "strength_pattern_support"
}
```

---

# Các nhóm Combination Rule

Module hiện bao gồm các nhóm:

## 1. Strength + Pattern

Đánh giá quan hệ:

- Thân
- Cách Cục

---

## 2. Strength + Useful God

Đánh giá:

- Thân
- Dụng Thần

---

## 3. Season + Pattern

Kết hợp:

- Mùa sinh
- Cách Cục

---

## 4. Temperature + Pattern

Kết hợp:

- Hàn
- Nhiệt
- Táo
- Thấp

với

- Cách Cục

---

## 5. Pattern + Pattern

Đánh giá:

- nhiều Cách Cục
- xung đột Cách Cục
- ưu tiên Cách Cục

---

## 6. Pattern + Special Case

Kết hợp:

- Tòng Cách
- Phá Cách
- Đặc Cách

---

## 7. Pattern + Follow Pattern

Đánh giá:

- Theo Cách
- Giả Theo Cách
- Không Theo Cách

---

## 8. Pattern + Luck Cycle

Kết hợp:

- Đại Vận
- Cách Cục

---

## 9. Multi Combination

Đánh giá đồng thời:

- Strength
- Season
- Temperature
- Pattern
- Special Case
- Follow Pattern
- Luck Cycle

---

## 10. Complex Combination

Giải quyết:

- nhiều Rule cùng đúng
- nhiều Rule xung đột
- Rule Override
- Rule Priority

---

## 11. Final Integration

Đây là tầng cuối của Rule Engine.

Bao gồm:

- tổng hợp toàn bộ Rule
- chọn Rule tốt nhất
- trả kết quả cuối cùng

---

# Thứ tự xử lý

Rule Engine thực hiện theo trình tự:

```text
Strength
      │
      ▼
Season
      │
      ▼
Temperature
      │
      ▼
Pattern
      │
      ▼
Special Case
      │
      ▼
Follow Pattern
      │
      ▼
Luck Cycle
      │
      ▼
Combination Rules
      │
      ▼
Priority
      │
      ▼
Final Result
```

---

# Quan hệ với các module khác

Module này sử dụng dữ liệu từ:

- 01_strength_rules
- 02_season_rules
- 03_temperature_rules
- 04_pattern_rules
- 05_special_case_rules
- 06_follow_pattern_rules

và chuyển kết quả đến:

- 08_priority_rules
- Interpretation Engine
- Report Engine
- API Layer

---

# Kiểm thử

Module được thiết kế để hỗ trợ:

- Unit Test
- Rule Test
- Golden Dataset Test
- Regression Test
- Integration Test

Nguồn dữ liệu kiểm thử nằm trong:

```text
combination_examples.json
```

---

# Quy ước đặt tên

Rule ID

```text
CBR001
...
CBR100
```

Condition ID

```text
CCD001
...
CCD100
```

Priority ID

```text
CPP001
...
CPP100
```

Label ID

```text
CLB001
...
CLB100
```

Example ID

```text
CEX001
...
CEX100
```

---

# Phiên bản

```text
Module:
07_combination_rules

Version:
1.0

Status:
Production Ready

Dataset:
100 Rules
100 Conditions
100 Priorities
100 Labels
100 Examples

Compatibility:
BTE Platform V1.0
```