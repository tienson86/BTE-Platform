# RULE_SCHEMA_REFERENCE.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Global Rule Schema Reference
>
> BTE Platform

---

# 1. Mục đích

`RULE_SCHEMA_REFERENCE.md` định nghĩa **Schema chuẩn** cho mọi Rule Database trong BTE Platform.

Đây là tài liệu nền tảng của toàn bộ Knowledge Base.

Mọi Rule Module phải kế thừa Schema này.

Ví dụ:

- Support Rule
- Attack Rule
- Season Rule
- Temperature Rule
- Pattern Rule
- Combination Rule
- Priority Rule
- Special Rule

Module chỉ được phép mở rộng (Extension), không được thay đổi cấu trúc nền.

---

# 2. Mục tiêu

Schema chuẩn nhằm:

- Chuẩn hóa dữ liệu.
- Tách dữ liệu khỏi Engine.
- Đảm bảo khả năng mở rộng.
- Đảm bảo khả năng kiểm thử.
- Đảm bảo tính nhất quán.
- Hỗ trợ Versioning.
- Hỗ trợ Backward Compatibility.

---

# 3. Nguyên tắc

Schema tuân thủ các nguyên tắc:

- Data Driven
- JSON First
- Deterministic
- Explainable
- Extensible
- Immutable Rule Identity
- Backward Compatible

---

# 4. Rule Model

Mọi Rule đều được xây dựng theo mô hình sau:

```
Rule
│
├── Identity
├── Classification
├── Source
├── Target
├── Conditions
├── Evaluation
├── Priority
├── Lifecycle
└── Metadata
```

Đây là cấu trúc bắt buộc.

---

# 5. Identity

Định danh duy nhất của Rule.

Bao gồm:

| Field | Required | Description |
|---------|----------|-------------|
| id | Yes | Rule ID |
| code | Yes | Rule Code |
| name | Yes | Rule Name |

Ví dụ:

```json
{
    "id":"SUP-000001",
    "code":"wood_generate_fire",
    "name":"Wood Generates Fire"
}
```

---

# 6. Classification

Phân loại Rule.

Bao gồm:

| Field | Description |
|---------|-------------|
| domain | Rule Domain |
| category | Rule Category |
| family | Rule Family |
| type | Rule Type |

Ví dụ:

```json
{
    "domain":"support",
    "category":"element_support",
    "family":"generating",
    "type":"wood_to_fire"
}
```

Mỗi Module tự định nghĩa Enum riêng cho:

- category
- family
- type

---

# 7. Source

Nguồn sinh Rule.

Ví dụ:

```json
{
    "source":{
        "element":"wood",
        "pillar":"month"
    }
}
```

Source mô tả nguyên nhân.

Không mô tả đối tượng chịu tác động.

---

# 8. Target

Đối tượng chịu ảnh hưởng.

Ví dụ:

```json
{
    "target":{
        "element":"fire",
        "role":"day_master"
    }
}
```

---

# 9. Conditions

Điều kiện kích hoạt.

Ví dụ:

```json
{
    "conditions":[
        {
            "type":"season",
            "operator":"equals",
            "value":"spring"
        }
    ]
}
```

Một Rule có thể có nhiều Condition.

---

# 10. Evaluation

Định nghĩa mức độ tác động.

Bao gồm:

| Field |
|---------|
| weight |
| stackable |
| max_stack |
| exclusive |

Ví dụ:

```json
{
    "evaluation":{
        "weight":25,
        "stackable":true,
        "max_stack":2
    }
}
```

Evaluation không phải kết quả cuối cùng.

---

# 11. Priority

Thứ tự xử lý Rule.

Ví dụ:

```json
{
    "priority":{
        "level":"high",
        "order":20
    }
}
```

Priority không biểu thị độ mạnh.

---

# 12. Lifecycle

Quản lý vòng đời Rule.

```json
{
    "status":"active",
    "enabled":true,
    "deprecated":false
}
```

---

# 13. Metadata

Thông tin quản trị.

```json
{
    "metadata":{
        "version":"1.0.0",
        "author":"BTE",
        "created_at":"2026-07-29",
        "updated_at":"2026-07-29"
    }
}
```

---

# 14. Schema tổng quát

```json
{
    "id":"",
    "code":"",
    "name":"",

    "classification":{},

    "source":{},

    "target":{},

    "conditions":[],

    "evaluation":{},

    "priority":{},

    "lifecycle":{},

    "metadata":{}
}
```

---

# 15. Extension Policy

Module không được thay đổi:

- Identity
- Evaluation
- Priority
- Lifecycle
- Metadata

Module chỉ được mở rộng:

- category
- family
- type
- source
- target
- conditions

---

# 16. Compatibility

Schema này áp dụng cho:

- Support Rule
- Attack Rule
- Season Rule
- Temperature Rule
- Pattern Rule
- Combination Rule
- Special Rule
- Priority Rule

---

# 17. Versioning

Schema tuân theo Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Breaking Change chỉ được phép trong Major Release.

---

# 18. Governance

Mọi Rule Module phải:

- Tuân thủ Schema chuẩn.
- Không thay đổi Rule Model.
- Không sửa Identity.
- Không tạo Field ngoài Schema nếu chưa được phê duyệt.

---

# 19. Kết luận

`RULE_SCHEMA_REFERENCE.md` là chuẩn dữ liệu cao nhất của toàn bộ Rule Database trong BTE Platform.

Mọi Rule Module phải kế thừa tài liệu này để đảm bảo tính nhất quán, khả năng mở rộng và khả năng bảo trì lâu dài.