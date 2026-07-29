# ATTACK_TAXONOMY.md

> Module: 08_support_attack / 02_attack_rules
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Taxonomy Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa hệ thống phân loại (Taxonomy) chuẩn cho toàn bộ Attack Rule trong BTE Platform.

Taxonomy là nền tảng để:

- Phân loại Rule.
- Chuẩn hóa Rule Database.
- Thống nhất Schema.
- Hỗ trợ Validation.
- Hỗ trợ Priority.
- Hỗ trợ mở rộng trong tương lai.

Mọi Attack Rule phải thuộc đúng một nhánh trong Taxonomy này.

---

# 2. Nguyên tắc thiết kế

Taxonomy được xây dựng theo các nguyên tắc:

- Phân loại theo bản chất của Rule, không theo hiện tượng.
- Mỗi Rule chỉ thuộc một Category chính.
- Có khả năng mở rộng mà không phá vỡ cấu trúc hiện có.
- Độc lập với Engine và thuật toán thực thi.
- Tương thích với Support Rule Taxonomy.

---

# 3. Cấu trúc phân cấp

```
Attack
│
├── Element Attack
│   ├── Controlling
│   ├── Draining
│   └── Weakening
│
├── Context Attack
│   ├── Seasonal
│   ├── Temperature
│   └── Climate
│
├── Relation Attack
│   ├── Clash
│   ├── Punishment
│   ├── Harm
│   ├── Destruction
│   └── Combination Failure
│
├── Structure Attack
│   ├── Root Loss
│   ├── Pattern Break
│   ├── Useful God Damage
│   └── Follow Pattern Break
│
└── Special Attack
    ├── ShenSha
    ├── Exceptional Rule
    └── School Specific Rule
```

---

# 4. Phân cấp Taxonomy

Mỗi Rule được định danh theo 5 tầng:

```
Level 1 : Domain
Level 2 : Category
Level 3 : Family
Level 4 : Type
Level 5 : Rule
```

Ví dụ:

```
Attack
    ↓
Element Attack
    ↓
Draining
    ↓
Wood to Fire
    ↓
SUP-ATT-000001
```

---

# 5. Quy ước định danh

| Thành phần | Ví dụ |
|------------|-------|
| Category | `element_attack` |
| Family | `draining` |
| Type | `wood_to_fire` |
| Rule ID | `ATT-000001` |

---

# 6. Quy tắc mở rộng

- Không đổi tên Category đã phát hành.
- Chỉ bổ sung Family hoặc Type mới trong phiên bản MINOR.
- Thay đổi Category chỉ được thực hiện trong phiên bản MAJOR.
- Mọi Rule mới phải tuân thủ Taxonomy hiện hành.

---

# 7. Quan hệ với các tài liệu khác

Taxonomy được sử dụng bởi:

- ATTACK_RULE_SPEC.md
- SCHEMA_REFERENCE.md
- VALIDATION_RULES.md
- RULE_PRIORITY.md
- Attack Rule Database

---

# 8. Kết luận

Taxonomy là chuẩn phân loại chính thức của toàn bộ Attack Rule trong BTE Platform và là nền tảng để xây dựng Rule Database có khả năng mở rộng, kiểm chứng và bảo trì lâu dài.