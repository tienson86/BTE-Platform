# VALIDATION_RULES.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Validation Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa các quy tắc kiểm tra tính hợp lệ của mọi Support Rule trước khi được nạp vào hệ thống.

Mục tiêu:

- đảm bảo dữ liệu nhất quán
- loại bỏ Rule sai
- phát hiện lỗi sớm
- đảm bảo khả năng tương thích giữa các phiên bản

Validation được thực hiện trước khi Rule được đưa vào Rule Registry.

---

# 2. Nguyên tắc

Mọi Support Rule phải:

- đúng Schema
- đúng Data Type
- đầy đủ Required Field
- không trùng Rule ID
- không vi phạm Enum
- không tham chiếu sai
- không tạo vòng lặp (Circular Reference)

Nếu bất kỳ bước nào thất bại, Rule phải bị từ chối.

---

# 3. Validation Pipeline

```
Load Rule
    │
    ▼
Schema Validation
    │
    ▼
Field Validation
    │
    ▼
Enum Validation
    │
    ▼
Reference Validation
    │
    ▼
Business Validation
    │
    ▼
Registry Validation
    │
    ▼
Accepted
```

---

# 4. Schema Validation

Kiểm tra:

- JSON hợp lệ
- UTF-8
- đúng cấu trúc
- đúng Schema Version

Nếu sai:

```
VAL-001
```

---

# 5. Required Fields

Các trường bắt buộc:

- id
- code
- name
- category
- support_type
- source
- target
- evaluation
- priority
- metadata.version

Thiếu bất kỳ trường nào đều không hợp lệ.

---

# 6. Data Type Validation

Ví dụ:

| Field | Type |
|--------|------|
| id | string |
| weight | number |
| enabled | boolean |
| conditions | array |
| metadata | object |

Sai kiểu dữ liệu:

```
VAL-002
```

---

# 7. Enum Validation

Các trường Enum phải thuộc danh sách cho phép.

Ví dụ:

category

- five_elements
- seasonal
- root
- combination
- pattern
- useful_god
- special

Nếu không:

```
VAL-003
```

---

# 8. Reference Validation

Kiểm tra các tham chiếu:

- category tồn tại
- support_type hợp lệ
- priority tồn tại
- family tồn tại

Không được tham chiếu đến giá trị chưa được định nghĩa.

---

# 9. Rule ID Validation

Rule ID:

- duy nhất
- không đổi sau khi phát hành
- đúng định dạng

Ví dụ:

```
SUP-000001
```

Không hợp lệ:

```
SUP001
```

---

# 10. Weight Validation

Weight phải:

- là số
- không âm
- nằm trong khoảng quy định của hệ thống

Giá trị cụ thể sẽ do tài liệu Scoring định nghĩa.

---

# 11. Priority Validation

Priority phải thuộc:

- absolute
- high
- normal
- low

Không được sử dụng giá trị khác.

---

# 12. Condition Validation

Mỗi Condition phải có:

- type
- operator (nếu áp dụng)
- value (nếu áp dụng)

Condition không được rỗng nếu Rule yêu cầu điều kiện.

---

# 13. Circular Reference

Không được tạo chuỗi phụ thuộc vòng.

Ví dụ không hợp lệ:

```
Rule A
↓

Rule B
↓

Rule C
↓

Rule A
```

---

# 14. Duplicate Validation

Không được phép:

- trùng Rule ID
- trùng Rule Code

Cho phép nhiều Rule có cùng Category nếu khác điều kiện hoặc mục đích.

---

# 15. Version Validation

Mỗi Rule phải khai báo:

- version
- status

Engine chỉ nạp các phiên bản được hỗ trợ.

---

# 16. Metadata Validation

Metadata tối thiểu:

- version
- author
- created_at

Khuyến nghị:

- updated_at
- tags
- notes
- references

---

# 17. Validation Result

Kết quả kiểm tra:

```json
{
    "valid": true,
    "errors": [],
    "warnings": []
}
```

Nếu không hợp lệ:

```json
{
    "valid": false,
    "errors": [
        "VAL-002"
    ]
}
```

---

# 18. Error Levels

| Level | Ý nghĩa |
|--------|----------|
| ERROR | Không được nạp |
| WARNING | Được nạp nhưng cần xem xét |
| INFO | Chỉ ghi log |

---

# 19. Kiểm thử

Validation phải hỗ trợ:

- Unit Test
- Regression Test
- Golden Dataset
- Snapshot Test

---

# 20. Kết luận

Validation là lớp bảo vệ đầu tiên của Support Rules.

Không có Rule nào được phép tham gia vào quá trình đánh giá nếu chưa vượt qua toàn bộ các bước Validation.