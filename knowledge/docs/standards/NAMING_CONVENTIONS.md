# NAMING_CONVENTIONS.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Naming Conventions
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định quy tắc đặt tên cho mọi thành phần trong Knowledge Base nhằm:

- Đảm bảo tính nhất quán.
- Dễ tìm kiếm.
- Dễ bảo trì.
- Dễ mở rộng.
- Tránh trùng lặp.

---

# 2. Phạm vi áp dụng

Áp dụng cho:

- Rule ID
- Rule Code
- File
- Folder
- JSON Key
- Enum
- Metadata
- Namespace
- Document

---

# 3. Nguyên tắc chung

Tên phải:

- Ngắn gọn.
- Có ý nghĩa.
- Không phụ thuộc ngôn ngữ hiển thị.
- Không thay đổi theo thời gian.
- Không chứa thông tin tạm thời.

---

# 4. Quy tắc đặt Rule ID

Cấu trúc:

```
<PREFIX>-<NUMBER>
```

Ví dụ:

```
SUP-000001
ATT-000001
SEA-000001
TMP-000001
PAT-000001
COM-000001
PRI-000001
```

Quy định:

- Prefix viết hoa.
- Number gồm 6 chữ số.
- Không tái sử dụng ID.

---

# 5. Prefix chuẩn

| Module | Prefix |
|----------|--------|
| Support | SUP |
| Attack | ATT |
| Strength | STR |
| Season | SEA |
| Temperature | TMP |
| Pattern | PAT |
| Combination | COM |
| Follow Pattern | FOL |
| Special | SPC |
| Priority | PRI |

---

# 6. Rule Code

Rule Code dùng:

- lowercase
- snake_case

Ví dụ:

```
wood_generate_fire
fire_control_metal
summer_fire_support
```

Không sử dụng:

- khoảng trắng
- CamelCase
- PascalCase

---

# 7. Rule Name

Rule Name:

- Tiếng Anh chuẩn hóa.
- Có thể bổ sung bản dịch trong tài liệu.
- Viết theo Title Case.

Ví dụ:

```
Wood Generates Fire

Fire Controls Metal
```

---

# 8. Folder

Folder:

- lowercase
- snake_case

Ví dụ:

```
support_rules
attack_rules
temperature_rules
```

---

# 9. File

Markdown:

```
RULE_MODEL_SPEC.md
```

JSON:

```
support_rules.json
```

Python:

```
rule_loader.py
```

---

# 10. JSON Keys

JSON Key:

- snake_case
- tiếng Anh

Ví dụ:

```
rule_id

source

target

priority
```

Không viết:

```
RuleID

RuleId

Rule_ID
```

---

# 11. Enum

Enum:

```
lowercase_with_underscore
```

Ví dụ:

```
element_support

temperature_attack

follow_pattern
```

---

# 12. Namespace

Namespace:

```
knowledge.rule.support

knowledge.rule.attack

knowledge.rule.pattern
```

Không dùng namespace mơ hồ.

---

# 13. Metadata

Metadata Key:

```
created_at

updated_at

version

status
```

Theo chuẩn snake_case.

---

# 14. Tài liệu

Document:

```
RULE_SCHEMA_REFERENCE.md

RULE_MODEL_SPEC.md

RULE_AUTHORING_GUIDE.md
```

Tên tài liệu chuẩn:

- UPPER_SNAKE_CASE
- Có hậu tố SPEC / GUIDE / POLICY / STANDARD khi phù hợp.

---

# 15. Những điều cấm

Không:

- Viết tắt khó hiểu.
- Dùng tiếng Việt trong mã định danh.
- Đổi ID sau khi phát hành.
- Dùng ký tự đặc biệt.
- Dùng khoảng trắng.

---

# 16. Governance

Mọi thành phần mới phải tuân thủ tài liệu này.

Nếu có ngoại lệ phải được ghi rõ trong tài liệu thiết kế của module.

---

# 17. Kết luận

Việc chuẩn hóa tên gọi giúp toàn bộ Knowledge Base nhất quán, giảm lỗi và tăng khả năng tự động hóa trong quá trình phát triển.