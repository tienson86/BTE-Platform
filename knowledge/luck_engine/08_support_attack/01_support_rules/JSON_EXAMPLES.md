# JSON_EXAMPLES.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: JSON Examples
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này cung cấp các ví dụ JSON chuẩn cho Support Rule.

Các ví dụ không phải toàn bộ Rule Database.

Mục tiêu là minh họa cách sử dụng Schema.

---

# 2. Direct Support

Mộc sinh Hỏa

```json
{
    "id":"SUP-000001",
    "category":"five_elements",
    "support_type":"direct_support",
    "source":{
        "element":"wood"
    },
    "target":{
        "element":"fire"
    },
    "evaluation":{
        "weight":20
    }
}
```

---

# 3. Same Element

Kim trợ Kim

```json
{
    "id":"SUP-000002",
    "category":"five_elements",
    "support_type":"same_element",
    "source":{
        "element":"metal"
    },
    "target":{
        "element":"metal"
    },
    "evaluation":{
        "weight":15
    }
}
```

---

# 4. Seasonal Support

```json
{
    "id":"SUP-000003",
    "category":"seasonal",
    "support_type":"seasonal_support",
    "conditions":[
        {
            "type":"season",
            "value":"spring"
        }
    ],
    "target":{
        "element":"wood"
    },
    "evaluation":{
        "weight":30
    }
}
```

---

# 5. Root Support

```json
{
    "id":"SUP-000004",
    "category":"root",
    "support_type":"root_support",
    "conditions":[
        {
            "type":"has_hidden_root"
        }
    ],
    "evaluation":{
        "weight":40
    }
}
```

---

# 6. Combination Support

```json
{
    "id":"SUP-000005",
    "category":"combination",
    "support_type":"combination_support",
    "conditions":[
        {
            "type":"stem_combination"
        }
    ],
    "evaluation":{
        "weight":25
    }
}
```

---

# 7. Useful God Support

```json
{
    "id":"SUP-000006",
    "category":"useful_god",
    "support_type":"useful_god_support",
    "conditions":[
        {
            "type":"is_useful_god"
        }
    ],
    "evaluation":{
        "weight":50
    }
}
```

---

# 8. Special Support

```json
{
    "id":"SUP-000007",
    "category":"special",
    "support_type":"special_support",
    "conditions":[
        {
            "type":"has_tian_yi_nobleman"
        }
    ],
    "evaluation":{
        "weight":10
    }
}
```

---

# 9. Rule có nhiều điều kiện

```json
{
    "id":"SUP-000008",
    "conditions":[
        {
            "type":"season",
            "value":"spring"
        },
        {
            "type":"has_root",
            "value":true
        },
        {
            "type":"temperature",
            "value":"warm"
        }
    ],
    "evaluation":{
        "weight":35
    }
}
```

---

# 10. Rule cộng dồn

```json
{
    "id":"SUP-000009",
    "evaluation":{
        "weight":15,
        "stackable":true,
        "max_stack":3
    }
}
```

---

# 11. Rule không cộng dồn

```json
{
    "id":"SUP-000010",
    "evaluation":{
        "weight":50,
        "stackable":false
    }
}
```

---

# 12. Rule bị vô hiệu

```json
{
    "id":"SUP-000011",
    "enabled":false,
    "status":"deprecated"
}
```

---

# 13. Rule đầy đủ

```json
{
    "id":"SUP-000100",
    "code":"wood_generate_fire",
    "name":"Wood Generates Fire",

    "category":"five_elements",
    "family":"generating_cycle",
    "support_type":"direct_support",

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
        "weight":20,
        "stackable":true,
        "max_stack":2
    },

    "priority":{
        "level":"high",
        "order":20
    },

    "status":"active",
    "enabled":true,

    "metadata":{
        "version":"1.0",
        "author":"BTE"
    }
}
```

---

# 14. Ghi chú

Các ví dụ trong tài liệu này chỉ nhằm minh họa cấu trúc dữ liệu.

Giá trị `weight`, `priority`, `conditions` và các trường khác sẽ được quy định chính thức trong:

- `SUPPORT_RULE_SPEC.md`
- `VALIDATION_RULES.md`
- `RULE_PRIORITY.md`

và các tệp Rule Database tương ứng.