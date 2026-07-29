# RULE_PRIORITY.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Priority Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định cách xác định thứ tự ưu tiên giữa nhiều Support Rule cùng thỏa điều kiện.

Priority không phản ánh mức độ mạnh yếu của Support.

Priority chỉ quyết định:

- Rule nào được thực thi trước.
- Rule nào được ghi đè.
- Rule nào được cộng dồn.
- Rule nào bị loại bỏ.

---

# 2. Nguyên tắc

Priority luôn được xử lý sau khi:

- Validation hoàn tất
- Rule đã được Match

Thứ tự:

```
Match

↓

Priority

↓

Merge

↓

Apply
```

---

# 3. Các mức Priority

| Level | Ý nghĩa |
|--------|----------|
| absolute | Luôn ưu tiên cao nhất |
| high | Ưu tiên cao |
| normal | Mặc định |
| low | Ưu tiên thấp |
| disabled | Không áp dụng |

---

# 4. Thứ tự xử lý

```
absolute

↓

high

↓

normal

↓

low

↓

disabled
```

---

# 5. Quy tắc Merge

Nếu nhiều Rule có thể cùng tồn tại:

```
Rule A

+

Rule B

↓

Merge
```

Điều kiện:

- không xung đột
- stackable = true

---

# 6. Quy tắc Override

Nếu Rule mới có Priority cao hơn:

```
Rule A

↓

Rule B

↓

Override
```

Rule bị ghi đè không tiếp tục được áp dụng.

---

# 7. Quy tắc Stack

Rule được cộng dồn khi:

- stackable = true
- không vượt max_stack

Nếu vượt giới hạn:

```
max_stack
```

được áp dụng.

---

# 8. Tie Break

Nếu hai Rule có cùng Priority:

So sánh theo:

1. specificity (độ cụ thể)
2. order
3. Rule ID

Quy tắc này giúp kết quả luôn xác định (deterministic).

---

# 9. Category Priority

Mặc định:

1. Direct Support
2. Same Element
3. Seasonal Support
4. Root Support
5. Combination Support
6. Pattern Support
7. Useful God Support
8. Special Support

Engine có thể điều chỉnh nếu có quy định đặc biệt ở tầng cao hơn.

---

# 10. Disabled Rule

Rule có:

```json
{
    "enabled": false
}
```

hoặc

```json
{
    "status": "deprecated"
}
```

không được đưa vào quá trình Priority Resolution.

---

# 11. Priority Output

Ví dụ:

```json
{
    "applied_rules": [
        "SUP-000001",
        "SUP-000005"
    ],
    "ignored_rules": [
        "SUP-000002"
    ]
}
```

---

# 12. Logging

Priority Engine phải ghi nhận:

- Rule được chọn
- Rule bị loại
- lý do
- mức Priority
- kết quả Merge hoặc Override

---

# 13. Khả năng mở rộng

Có thể bổ sung:

- Priority Strategy mới
- Merge Strategy mới
- Override Strategy mới

mà không thay đổi cấu trúc Rule.

---

# 14. Tương thích

Priority phải tương thích với:

- SupportAttack Engine
- Strength Engine
- Pattern Engine
- Rule Registry

---

# 15. Kết luận

Priority Resolution đảm bảo rằng khi nhiều Support Rule cùng phù hợp với một ngữ cảnh, hệ thống luôn tạo ra một tập Rule cuối cùng rõ ràng, nhất quán và có thể giải thích. Đây là nền tảng để quá trình tính điểm và luận giải ở các tầng sau hoạt động ổn định.