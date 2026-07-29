# ATTACK_RULE_ARCHITECTURE.md

> Module: 08_support_attack / 02_attack_rules
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Architecture Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này mô tả kiến trúc tổng thể của **Attack Rule Module**.

Attack Rule Module chịu trách nhiệm lưu trữ, tổ chức và cung cấp toàn bộ quy tắc liên quan đến các yếu tố làm suy yếu (Attack) trong hệ thống BTE Platform.

Module không thực hiện tính toán hay diễn giải, mà chỉ cung cấp dữ liệu chuẩn hóa cho các Engine.

---

# 2. Mục tiêu kiến trúc

Kiến trúc được thiết kế nhằm:

- Chuẩn hóa Attack Rule.
- Tách dữ liệu khỏi thuật toán.
- Hỗ trợ mở rộng Rule Database.
- Đảm bảo khả năng kiểm chứng.
- Đảm bảo tính quyết định (Deterministic).
- Hỗ trợ nhiều trường phái Bát Tự trong tương lai.

---

# 3. Kiến trúc phân tầng

```
Knowledge Layer
        │
        ▼
Attack Rule Definition
        │
        ▼
Validation Layer
        │
        ▼
Rule Registry
        │
        ▼
Rule Matching
        │
        ▼
Priority Resolution
        │
        ▼
Engine Consumer
```

---

# 4. Kiến trúc dữ liệu

Mỗi Attack Rule bao gồm các thành phần:

```
Attack Rule
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

Các thành phần này được định nghĩa chi tiết trong `SCHEMA_REFERENCE.md`.

---

# 5. Rule Lifecycle

Mỗi Rule trải qua vòng đời sau:

```
Draft
    │
    ▼
Review
    │
    ▼
Approved
    │
    ▼
Active
    │
    ▼
Deprecated
    │
    ▼
Archived
```

Chỉ Rule ở trạng thái **Active** mới được Rule Registry nạp vào hệ thống.

---

# 6. Validation Layer

Trước khi đăng ký vào Registry, mọi Rule phải vượt qua:

- Schema Validation
- Data Validation
- Enum Validation
- Business Validation
- Dependency Validation
- Duplicate Validation

Nếu bất kỳ bước nào thất bại, Rule sẽ bị loại khỏi quá trình nạp.

---

# 7. Rule Registry

Rule Registry là nơi quản lý toàn bộ Attack Rule hợp lệ.

Nhiệm vụ:

- Đăng ký Rule.
- Tra cứu Rule.
- Lập chỉ mục (Index).
- Quản lý Version.
- Hỗ trợ Cache.

Registry không thay đổi nội dung Rule.

---

# 8. Rule Matching

Rule Matching xác định Rule nào phù hợp với Context hiện tại.

Quy trình:

```
Context
    │
    ▼
Condition Matching
    │
    ▼
Candidate Rules
```

Module chỉ trả về các Rule phù hợp, không tính điểm hay đưa ra kết luận.

---

# 9. Priority Resolution

Sau khi Match:

```
Candidate Rules
        │
        ▼
Priority Engine
        │
        ▼
Resolved Rules
```

Quy tắc Priority được định nghĩa riêng trong `RULE_PRIORITY.md`.

---

# 10. Quan hệ với các Engine

Attack Rule Module được sử dụng bởi:

```
SupportAttack Engine
        │
        ▼
Strength Engine
        │
        ▼
Pattern Engine
        │
        ▼
Interpretation Engine
```

Module không phụ thuộc trực tiếp vào các Engine này.

---

# 11. Dependency

Attack Rule Module phụ thuộc vào:

- Dictionary
- Terminology
- Shared Schema
- Rule Database Framework

Module không được phụ thuộc trực tiếp vào:

- Support Rules
- Strength Engine
- Pattern Engine
- Interpretation Engine

Mọi tích hợp phải thông qua các Interface hoặc Adapter được định nghĩa ở tầng Engine.

---

# 12. Logging

Mọi quá trình nạp Rule phải ghi nhận:

- Rule ID
- Version
- Validation Result
- Load Time
- Registry Status

Logging không được làm thay đổi dữ liệu Rule.

---

# 13. Performance

Mục tiêu thiết kế:

- O(1) tra cứu theo Rule ID.
- Hỗ trợ Index theo Category và Family.
- Hỗ trợ Lazy Loading.
- Hỗ trợ Cache.
- Khả năng mở rộng lên hàng chục nghìn Rule.

---

# 14. Kiểm thử

Kiến trúc phải hỗ trợ:

- Unit Test
- Integration Test
- Golden Dataset
- Snapshot Test
- Regression Test

---

# 15. Nguyên tắc thiết kế

Module tuân thủ:

- Single Source of Truth
- Data Driven
- JSON First
- Explainable
- Deterministic
- No Hard-code
- Separation of Concerns
- Backward Compatibility

---

# 16. Khả năng mở rộng

Kiến trúc hỗ trợ:

- Thêm Category mới.
- Thêm Family mới.
- Thêm Type mới.
- Plugin Rule Provider.
- Dynamic Rule Loading.
- Multi-school Rule Set.

Các thay đổi phải đảm bảo không phá vỡ Schema đã phát hành.

---

# 17. Kết luận

Attack Rule Architecture xác định cách tổ chức, quản lý và cung cấp Attack Rule cho toàn bộ BTE Platform.

Kiến trúc này đảm bảo Rule Database luôn nhất quán, có khả năng mở rộng, dễ kiểm thử và không phụ thuộc vào thuật toán thực thi của các Engine.