# SUPPORT_RULE_ARCHITECTURE.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Architecture Blueprint
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này mô tả kiến trúc kỹ thuật của module **Support Rules**.

Module chịu trách nhiệm quản lý toàn bộ Rule liên quan đến **Support** dưới dạng dữ liệu có cấu trúc (JSON), cung cấp cho SupportAttack Engine thông qua các thành phần Loader, Validator và Matcher.

Module không thực hiện tính toán, không quyết định kết quả và không sinh luận giải.

---

# 2. Vai trò trong hệ thống

```
Knowledge Base
      │
      ▼
Support Rules
      │
      ▼
Rule Loader
      │
      ▼
Rule Validator
      │
      ▼
Rule Matcher
      │
      ▼
SupportAttack Engine
      │
      ▼
Interpretation Engine
```

Support Rules là **nguồn dữ liệu**, không phải nơi xử lý nghiệp vụ.

---

# 3. Kiến trúc phân lớp

```
Application Layer
        │
        ▼

Rule Access Layer
        │
        ▼

Rule Validation Layer
        │
        ▼

Rule Definition Layer
        │
        ▼

Knowledge Layer
```

### 3.1 Knowledge Layer

Lưu trữ toàn bộ Rule JSON.

Không chứa logic.

### 3.2 Rule Definition Layer

Chuẩn hóa cấu trúc Rule.

Bao gồm:

- Rule ID
- Category
- Type
- Condition
- Weight
- Priority
- Metadata

### 3.3 Rule Validation Layer

Kiểm tra:

- Schema
- Required Field
- Enum
- Version
- Circular Reference

### 3.4 Rule Access Layer

Cung cấp API nội bộ để Engine đọc Rule.

---

# 4. Rule Lifecycle

```
Created
   │
   ▼
Validated
   │
   ▼
Loaded
   │
   ▼
Matched
   │
   ▼
Applied
   │
   ▼
Archived
```

Mỗi Rule phải trải qua đúng vòng đời này.

---

# 5. Rule Pipeline

```
Load JSON
    │
    ▼
Validate Schema
    │
    ▼
Normalize
    │
    ▼
Register
    │
    ▼
Match
    │
    ▼
Return Result
```

---

# 6. Dependency

Support Rules có thể tham chiếu dữ liệu từ:

- Strength Rules
- Season Rules
- Temperature Rules
- Combination Rules
- Pattern Rules
- Priority Rules

Không được tham chiếu trực tiếp sang Attack Rules để tránh phụ thuộc vòng (circular dependency). Việc tổng hợp Support và Attack được thực hiện ở tầng `SupportAttack Engine`.

---

# 7. Rule Registry

Mọi Rule sau khi được nạp sẽ đăng ký vào Rule Registry.

Rule Registry chịu trách nhiệm:

- quản lý Rule ID
- tra cứu theo Category
- tra cứu theo Type
- tra cứu theo Priority
- hỗ trợ cache

---

# 8. Caching Strategy

Yêu cầu:

- Rule chỉ nạp một lần.
- Không đọc lại JSON mỗi lần đánh giá.
- Hỗ trợ cache theo phiên bản (version-aware cache).

---

# 9. Logging

Mỗi lần truy xuất Rule cần ghi nhận:

- Rule ID
- Category
- Version
- Timestamp
- Kết quả kiểm tra hợp lệ

---

# 10. Kiểm thử

Module phải hỗ trợ:

- Schema Test
- Rule Validation Test
- Registry Test
- Compatibility Test
- Golden Dataset Test

---

# 11. Khả năng mở rộng

Kiến trúc cho phép:

- thêm Category mới
- thêm Rule Type mới
- thêm Metadata mới
- thêm Strategy Loader
- thay đổi nguồn dữ liệu mà không ảnh hưởng Engine

---

# 12. Kết luận

Support Rules là tầng dữ liệu nền tảng của SupportAttack Engine.

Kiến trúc được thiết kế theo hướng **Data-driven**, **Rule-first** và **Single Source of Truth**, giúp mọi Engine sử dụng chung một hệ thống Rule thống nhất, dễ kiểm thử và dễ mở rộng.