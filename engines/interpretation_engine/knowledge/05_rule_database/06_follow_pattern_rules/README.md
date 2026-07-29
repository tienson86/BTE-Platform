# Follow Pattern Rules Module

## 1. Mục đích

Module **Follow Pattern Rules** chịu trách nhiệm xác định và đánh giá **Cách Cục (Pattern)** của lá số Bát Tự sau khi hoàn thành các bước tính toán Tứ Trụ, Thập Thần, Ngũ Hành và Thân Vượng/Nhược.

Module này không trực tiếp sinh luận giải mà cung cấp kết quả chuẩn hóa cho:

- Rule Engine
- Score Engine
- Interpretation Engine
- Report Engine

---

# 2. Vị trí trong kiến trúc BTE

```text
Input Bazi
      │
      ▼
Calendar Engine
      │
      ▼
Bazi Engine
      │
      ▼
Score Engine
      │
      ▼
Follow Pattern Rules
      │
      ▼
Interpretation Engine
      │
      ▼
Report Engine
```

---

# 3. Cấu trúc thư mục

```text
06_follow_pattern_rules/
├── follow_pattern_rules.json
├── follow_pattern_conditions.json
├── follow_pattern_priority.json
├── follow_pattern_labels.json
├── follow_pattern_examples.json
└── README.md
```

---

# 4. Thành phần dữ liệu

## 4.1 follow_pattern_rules.json

Chứa toàn bộ Rule dùng để nhận diện các Pattern.

Ví dụ:

- Tong Cach
- Quan Sat Cach
- Tai Cach
- Xuat Cach
- An Cach
- Ty Kiep Cach
- Special Pattern

Mỗi Rule định nghĩa:

- id
- pattern
- dieu kien
- do uu tien
- kich hoat

---

## 4.2 follow_pattern_conditions.json

Mô tả toàn bộ điều kiện cần để Rule được kích hoạt.

Ví dụ:

- Than vuong
- Than nhuoc
- Tai sinh Quan
- An hoa Sat
- Ty Kiep doat Tai
- Thuong Quan kien Quan

Condition chỉ trả về:

- true
- false

---

## 4.3 follow_pattern_priority.json

Khi nhiều Pattern đồng thời hợp lệ, Priority quyết định:

- Pattern nào được giữ
- Pattern nào bị loại
- Cách xử lý xung đột
- Thứ tự đánh giá

Priority không chứa nội dung luận giải.

---

## 4.4 follow_pattern_labels.json

Chuyển kết quả xử lý thành Label chuẩn.

Ví dụ:

- Pattern Detected
- Confirmed
- Broken
- Balanced
- Selected
- Completed

Interpretation Engine chỉ làm việc với Label thay vì đọc Rule trực tiếp.

---

## 4.5 follow_pattern_examples.json

Bộ Golden Dataset dùng cho:

- Unit Test
- Integration Test
- Regression Test
- Demo dữ liệu

Mỗi Example bao gồm:

- Input
- Rule mong đợi
- Condition mong đợi
- Priority mong đợi
- Label mong đợi
- Kết quả mong đợi

---

# 5. Luồng xử lý

```text
Input
 │
 ▼
Rule Matching
 │
 ▼
Condition Checking
 │
 ▼
Priority Resolution
 │
 ▼
Label Generation
 │
 ▼
Pattern Result
 │
 ▼
Interpretation Engine
```

---

# 6. Pattern được hỗ trợ

Module hiện hỗ trợ các nhóm Pattern sau:

- Tong Cach
- Quan Sat Cach
- Tai Cach
- Xuat Cach
- An Cach
- Ty Kiep Cach
- Special Pattern

Có thể mở rộng thêm Pattern mới mà không cần thay đổi Engine.

---

# 7. Quy trình đánh giá

Mỗi Pattern đều tuân theo quy trình chuẩn:

```text
Detected
    │
Confirmed
    │
Strength Evaluation
    │
Relationship Evaluation
    │
Score
    │
Conflict Resolution
    │
Selected
    │
Completed
```

---

# 8. Conflict Resolution

Khi nhiều Pattern cùng hợp lệ:

1. So sánh Priority.
2. So sánh Score.
3. Loại bỏ Pattern bị phá.
4. Giữ Pattern có độ tin cậy cao nhất.
5. Trả về Pattern cuối cùng.

---

# 9. Chuẩn hóa ID

## Rule

```text
FPR001
FPR002
...
FPR100
```

## Condition

```text
FPC001
...
FPC100
```

## Priority

```text
FPP001
...
FPP100
```

## Label

```text
FLB001
...
FLB100
```

## Example

```text
FEX001
...
FEX100
```

---

# 10. Chuỗi ánh xạ

Mọi dữ liệu trong module tuân theo quan hệ:

```text
Rule
   │
   ▼
Condition
   │
   ▼
Priority
   │
   ▼
Label
   │
   ▼
Example
```

Việc chuẩn hóa này giúp truy vết toàn bộ quá trình xử lý một cách dễ dàng.

---

# 11. Tích hợp với các Engine

## Rule Engine

Đọc:

- follow_pattern_rules.json
- follow_pattern_conditions.json

Trả về danh sách Pattern hợp lệ.

---

## Score Engine

Đọc:

- follow_pattern_priority.json

Xác định Pattern có điểm và độ ưu tiên cao nhất.

---

## Interpretation Engine

Đọc:

- follow_pattern_labels.json

Sinh các câu luận giải dựa trên Label.

---

## Test Framework

Đọc:

- follow_pattern_examples.json

So sánh kết quả thực tế với Golden Dataset để kiểm thử tự động.

---

# 12. Nguyên tắc thiết kế

Module được xây dựng theo các nguyên tắc:

- Data-driven.
- Rule và Engine tách biệt.
- Không hard-code nghiệp vụ.
- Dễ mở rộng Pattern mới.
- Dễ kiểm thử bằng Golden Dataset.
- Dễ tích hợp với các Engine khác.

---

# 13. Trạng thái module

| Thành phần | Trạng thái |
|------------|------------|
| Rules | Hoàn thành |
| Conditions | Hoàn thành |
| Priority | Hoàn thành |
| Labels | Hoàn thành |
| Examples | Hoàn thành |
| README | Hoàn thành |

---

# 14. Phiên bản

| Thuộc tính | Giá trị |
|------------|----------|
| Module | Follow Pattern Rules |
| Version | 1.0 |
| Status | Stable |
| Architecture | Data-driven Rule Engine |
| Test Dataset | 100 Golden Examples |
| Compatible | BTE Platform V1 |