# SCHEMA_REFERENCE.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Schema Reference
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa cấu trúc dữ liệu (Schema) chuẩn cho tất cả Support Rule.

Mọi Rule trong module phải tuân thủ tài liệu này.

Schema được thiết kế theo nguyên tắc:

- Data Driven
- JSON First
- Backward Compatible
- Versioned
- Explainable

---

# 2. Cấu trúc tổng thể

```
Support Rule

├── Metadata
├── Identity
├── Classification
├── Source
├── Target
├── Conditions
├── Evaluation
├── Priority
├── Lifecycle
└── Audit
```

---

# 3. Schema

## 3.1 Identity

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| id | string | Yes | Rule ID duy nhất |
| code | string | Yes | Rule Code |
| name | string | Yes | Rule Name |

Ví dụ

```json
{
  "id":"SUP-000001",
  "code":"wood_generate_fire",
  "name":"Wood Generates Fire"
}
```

---

## 3.2 Classification

| Field | Type |
|--------|------|
| category | string |
| family | string |
| support_type | string |
| level | integer |

Ví dụ

```json
{
    "category":"five_elements",
    "family":"generating_cycle",
    "support_type":"direct_support",
    "level":1
}
```

---

## 3.3 Source

Nguồn tạo Support.

```json
{
    "source":{
        "element":"wood",
        "pillar":"month",
        "location":"stem"
    }
}
```

Các trường:

| Field | Description |
|---------|------------|
| element | Ngũ hành |
| pillar | Trụ |
| location | Can / Chi / Tàng Can |

---

## 3.4 Target

```json
{
    "target":{
        "element":"fire",
        "role":"day_master"
    }
}
```

---

## 3.5 Conditions

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

Mỗi Rule có thể có nhiều điều kiện.

---

## 3.6 Evaluation

```json
{
    "evaluation":{
        "weight":25,
        "stackable":true,
        "max_stack":2
    }
}
```

| Field | Description |
|---------|------------|
| weight | Điểm Support |
| stackable | Có cộng dồn không |
| max_stack | Số lần cộng tối đa |

---

## 3.7 Priority

```json
{
    "priority":{
        "level":"high",
        "order":20
    }
}
```

Priority chỉ quyết định thứ tự xử lý.

---

## 3.8 Lifecycle

```json
{
    "status":"active",
    "enabled":true,
    "deprecated":false
}
```

---

## 3.9 Metadata

```json
{
    "metadata":{
        "version":"1.0",
        "author":"BTE",
        "created_at":"2026-01-01",
        "updated_at":"2026-01-01"
    }
}
```

---

# 4. Schema hoàn chỉnh

```json
{
    "id":"SUP-000001",
    "code":"wood_generate_fire",
    "name":"Wood Generates Fire",

    "category":"five_elements",
    "family":"generating_cycle",
    "support_type":"direct_support",
    "level":1,

    "source":{
        "element":"wood",
        "pillar":"month",
        "location":"stem"
    },

    "target":{
        "element":"fire",
        "role":"day_master"
    },

    "conditions":[],

    "evaluation":{
        "weight":25,
        "stackable":true,
        "max_stack":2
    },

    "priority":{
        "level":"high",
        "order":20
    },

    "status":"active",
    "enabled":true,
    "deprecated":false,

    "metadata":{
        "version":"1.0",
        "author":"BTE"
    }
}
```

---

# 5. Enum

## category

- five_elements
- seasonal
- root
- combination
- pattern
- useful_god
- special

---

## support_type

- direct_support
- same_element
- seasonal_support
- root_support
- combination_support
- pattern_support
- useful_god_support
- special_support

---

## priority

- absolute
- high
- normal
- low

---

## status

- draft
- active
- deprecated
- archived

---

# 6. Quy tắc

Mọi Rule:

- phải có ID duy nhất.
- phải có Version.
- phải có Metadata.
- phải đúng Schema.
- không được thiếu Required Field.

---

# 7. Version

Schema hiện tại:

```
Schema Version 1.0
```

Các thay đổi trong tương lai phải đảm bảo khả năng tương thích ngược (backward compatibility).