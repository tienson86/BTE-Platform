# VERSIONING_POLICY.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Versioning Policy
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định chính sách quản lý phiên bản của toàn bộ Knowledge Base.

Mục tiêu:

- Theo dõi thay đổi.
- Đảm bảo tương thích.
- Hỗ trợ rollback.
- Hỗ trợ phát hành.

---

# 2. Phạm vi áp dụng

Áp dụng cho:

- Knowledge Framework
- Rule Database
- Dictionary
- Terminology
- Sentence Library
- Report Templates
- Rule Modules
- Individual Rule

---

# 3. Semantic Versioning

Mọi thành phần sử dụng:

```
MAJOR.MINOR.PATCH
```

Ví dụ:

```
1.0.0

1.1.0

1.1.3

2.0.0
```

---

# 4. MAJOR

Tăng MAJOR khi:

- Thay đổi Schema.
- Thay đổi Rule Model.
- Thay đổi API dữ liệu.
- Không còn tương thích ngược.

Ví dụ:

```
1.5.2

↓

2.0.0
```

---

# 5. MINOR

Tăng MINOR khi:

- Thêm Rule.
- Thêm Module.
- Thêm Field tương thích.
- Bổ sung Metadata.
- Mở rộng Dictionary.

Ví dụ:

```
1.2.0

↓

1.3.0
```

---

# 6. PATCH

Tăng PATCH khi:

- Sửa lỗi.
- Sửa chính tả.
- Sửa Metadata.
- Cập nhật Documentation.
- Điều chỉnh Validation.

Ví dụ:

```
1.3.2

↓

1.3.3
```

---

# 7. Version theo cấp

Framework:

```
2.0.0
```

Module:

```
support_rules

1.4.0
```

Rule:

```
SUP-000025

1.1.0
```

---

# 8. Compatibility

Mọi bản MINOR và PATCH phải tương thích ngược.

Chỉ MAJOR được phép tạo Breaking Change.

---

# 9. Deprecation

Quy trình:

```
Active

↓

Deprecated

↓

Archived
```

Không xóa Rule ngay sau khi Deprecated.

---

# 10. Release

Mỗi lần phát hành phải:

- Cập nhật Version.
- Cập nhật CHANGELOG.
- Chạy Validation.
- Chạy Regression Test.

---

# 11. Rollback

Mọi bản phát hành phải có khả năng:

- Xác định Version.
- Khôi phục dữ liệu.
- Khôi phục Rule.

---

# 12. CHANGELOG

Mỗi Version phải ghi:

- Added
- Changed
- Fixed
- Deprecated
- Removed

---

# 13. Rule Version

Rule chỉ tăng Version khi:

- Có thay đổi nội dung.
- Có thay đổi Metadata quan trọng.
- Có thay đổi Validation.

Không tăng Version khi chỉ thay đổi vị trí lưu trữ.

---

# 14. Module Version

Module Version độc lập với Framework Version.

Ví dụ:

```
Framework

2.0.0

Support Module

1.8.0

Attack Module

1.5.0
```

---

# 15. Governance

Mọi thay đổi phải:

- Có Version.
- Có CHANGELOG.
- Có Reviewer.
- Có Validation.

Không Merge nếu thiếu Version.

---

# 16. Kết luận

Chính sách Versioning giúp BTE Platform quản lý thay đổi một cách minh bạch, hỗ trợ mở rộng lâu dài và đảm bảo khả năng tương thích giữa các phiên bản của Knowledge Base.