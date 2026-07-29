# CHANGELOG.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Change Log
>
> BTE Platform

---

# 1. Giới thiệu

Tài liệu này ghi nhận toàn bộ lịch sử thay đổi (Change History) của module **01_support_rules**.

Mục tiêu của Change Log:

- Theo dõi sự phát triển của module.
- Ghi nhận các thay đổi về Rule, Schema và Specification.
- Hỗ trợ kiểm toán (Audit).
- Hỗ trợ Migration giữa các phiên bản.
- Đảm bảo khả năng truy vết (Traceability).

Mọi thay đổi ảnh hưởng đến cấu trúc dữ liệu, quy tắc nghiệp vụ hoặc khả năng tương thích đều phải được ghi nhận tại đây.

---

# 2. Chính sách Versioning

Module sử dụng chuẩn **Semantic Versioning (SemVer)**.

```
MAJOR.MINOR.PATCH
```

Trong đó:

| Thành phần | Ý nghĩa |
|------------|----------|
| MAJOR | Thay đổi không tương thích (Breaking Change) |
| MINOR | Thêm tính năng nhưng vẫn tương thích |
| PATCH | Sửa lỗi, cải thiện tài liệu, không thay đổi hành vi |

Ví dụ:

```
1.0.0
1.1.0
1.2.3
2.0.0
```

---

# 3. Chính sách quản lý thay đổi

Mọi thay đổi phải:

- Có Version.
- Có ngày thay đổi.
- Có người thực hiện.
- Có mô tả.
- Có mức ảnh hưởng.
- Có trạng thái.

Không được thay đổi Rule đã phát hành mà không tăng Version.

---

# 4. Phân loại thay đổi

## 4.1 Added

Thêm mới.

Ví dụ:

- Support Category mới.
- Rule mới.
- Metadata mới.

---

## 4.2 Changed

Thay đổi hành vi hoặc nội dung.

Ví dụ:

- Điều chỉnh Weight.
- Thay đổi Priority.
- Cập nhật Schema.

---

## 4.3 Deprecated

Đánh dấu ngừng sử dụng.

Rule vẫn tồn tại để đảm bảo tương thích nhưng không khuyến nghị sử dụng.

---

## 4.4 Removed

Loại bỏ hoàn toàn.

Chỉ được thực hiện trong phiên bản MAJOR.

---

## 4.5 Fixed

Sửa lỗi.

Ví dụ:

- Rule sai.
- Metadata sai.
- Điều kiện sai.

---

## 4.6 Security

Các thay đổi ảnh hưởng đến:

- Validation
- Data Integrity
- Rule Loading
- Version Compatibility

---

# 5. Nhật ký phiên bản

## Version 1.0.0

**Release Date**

2026-07-29

**Status**

Stable

### Added

- Khởi tạo module `01_support_rules`.
- Chuẩn hóa hệ thống Support Rule.
- Chuẩn hóa Taxonomy.
- Chuẩn hóa Rule Architecture.
- Chuẩn hóa Rule Specification.
- Chuẩn hóa JSON Schema.
- Chuẩn hóa Validation Rules.
- Chuẩn hóa Rule Priority.
- Chuẩn hóa JSON Examples.

### Changed

Không có.

### Deprecated

Không có.

### Removed

Không có.

### Fixed

Không có.

---

# 6. Lịch sử thay đổi

| Version | Date | Type | Description |
|----------|------|------|-------------|
| 1.0.0 | 2026-07-29 | Initial Release | Phát hành phiên bản đầu tiên |

---

# 7. Breaking Changes

## Version 1.x

Không có Breaking Change.

---

# 8. Migration Guide

## 1.0.0 → 1.1.0

Không yêu cầu Migration.

---

## 1.x → 2.0

Sẽ được cập nhật khi phát hành.

---

# 9. Rule Evolution Policy

Mỗi Rule có vòng đời:

```
Draft

↓

Review

↓

Approved

↓

Active

↓

Deprecated

↓

Archived
```

## Draft

Đang phát triển.

Không được sử dụng.

---

## Review

Đang kiểm tra.

Chưa được phát hành.

---

## Approved

Đã được phê duyệt.

Có thể đưa vào Release.

---

## Active

Được Engine sử dụng.

---

## Deprecated

Không khuyến nghị sử dụng.

Vẫn giữ để đảm bảo Backward Compatibility.

---

## Archived

Ngừng sử dụng.

Không được nạp mặc định.

---

# 10. Schema Evolution

Schema phải tuân thủ các nguyên tắc:

- Không đổi tên Field bắt buộc trong phiên bản MINOR.
- Không thay đổi ý nghĩa Field đã phát hành.
- Không thay đổi Rule ID.
- Không tái sử dụng Rule ID đã phát hành.
- Mọi Field mới phải có khả năng tương thích ngược.

---

# 11. Rule Versioning

Mỗi Rule phải có:

```json
{
  "version": "1.0.0",
  "status": "active"
}
```

Nếu Rule thay đổi nội dung nghiệp vụ:

- Tăng MINOR nếu tương thích.
- Tăng MAJOR nếu phá vỡ tương thích.

---

# 12. Compatibility Matrix

| Module | Minimum Version |
|----------|----------------:|
| SupportAttack | 1.0.0 |
| Strength Rules | 1.0.0 |
| Season Rules | 1.0.0 |
| Temperature Rules | 1.0.0 |
| Pattern Rules | 1.0.0 |
| Priority Rules | 1.0.0 |

---

# 13. Documentation History

| Document | Version |
|-----------|---------|
| README.md | 1.0.0 |
| SUPPORT_TAXONOMY.md | 1.0.0 |
| SUPPORT_RULE_ARCHITECTURE.md | 1.0.0 |
| SUPPORT_RULE_SPEC.md | 1.0.0 |
| SCHEMA_REFERENCE.md | 1.0.0 |
| JSON_EXAMPLES.md | 1.0.0 |
| VALIDATION_RULES.md | 1.0.0 |
| RULE_PRIORITY.md | 1.0.0 |
| CHANGELOG.md | 1.0.0 |

---

# 14. Roadmap

## Version 1.1

Dự kiến:

- Mở rộng Support Category.
- Chuẩn hóa Weight Strategy.
- Bổ sung Validation Rule.
- Bổ sung JSON Examples.

---

## Version 1.2

Dự kiến:

- Context-aware Support.
- Dynamic Condition.
- Rule Grouping.

---

## Version 2.0

Dự kiến:

- Plugin-based Rule Provider.
- Dynamic Rule Loading.
- Adaptive Support Strategy.
- Distributed Rule Repository.

---

# 15. Governance

Mọi thay đổi phải tuân thủ các nguyên tắc:

- Review trước khi Merge.
- Có kiểm thử tự động.
- Không phá vỡ Backward Compatibility (trừ MAJOR Release).
- Cập nhật đầy đủ tài liệu liên quan.
- Đồng bộ Schema, Specification và JSON Rule Database.

---

# 16. Audit Checklist

Trước mỗi lần phát hành cần xác nhận:

- [ ] Tất cả Rule vượt qua Validation.
- [ ] Không có Rule ID trùng lặp.
- [ ] Schema hợp lệ.
- [ ] Metadata đầy đủ.
- [ ] JSON Examples được cập nhật.
- [ ] Rule Priority được rà soát.
- [ ] Tài liệu đồng bộ với Rule Database.
- [ ] Golden Dataset Test thành công.
- [ ] Regression Test thành công.
- [ ] CHANGELOG được cập nhật.

---

# 17. Kết luận

`CHANGELOG.md` là tài liệu quản trị phiên bản chính thức của module **01_support_rules**.

Tài liệu này đảm bảo mọi thay đổi đối với Rule Database đều được ghi nhận đầy đủ, có khả năng truy vết, hỗ trợ kiểm toán và duy trì tính ổn định lâu dài cho toàn bộ BTE Platform.

Mọi cập nhật đối với Rule, Schema, Validation hoặc Specification phải được phản ánh trong Change Log trước khi phát hành phiên bản mới.