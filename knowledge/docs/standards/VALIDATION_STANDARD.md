# VALIDATION_STANDARD.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Validation Standard
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định tiêu chuẩn kiểm tra (Validation) áp dụng cho toàn bộ Knowledge Base của BTE Platform.

Validation nhằm đảm bảo dữ liệu:

- đúng cấu trúc;
- đúng ngữ nghĩa;
- đầy đủ;
- nhất quán;
- có thể sử dụng bởi các Engine.

Validation là bước bắt buộc trước khi dữ liệu được đưa vào Rule Registry hoặc phát hành.

---

# 2. Phạm vi áp dụng

Áp dụng cho:

- Rule Database
- Dictionary
- Terminology
- Phrase Library
- Sentence Library
- Report Templates
- Metadata
- Configuration

---

# 3. Nguyên tắc

Mọi dữ liệu phải:

- Validate được.
- Có thể tự động kiểm tra.
- Không phụ thuộc vào Engine.
- Có khả năng tái kiểm tra (Repeatable).
- Cho kết quả xác định (Deterministic).

---

# 4. Các cấp độ Validation

Validation gồm 5 cấp:

```
Level 1
Schema Validation

↓

Level 2
Structural Validation

↓

Level 3
Reference Validation

↓

Level 4
Semantic Validation

↓

Level 5
Governance Validation
```

Mỗi cấp chỉ được thực hiện khi cấp trước đã thành công.

---

# 5. Schema Validation

Kiểm tra:

- JSON hợp lệ.
- Đúng Schema.
- Đúng kiểu dữ liệu.
- Field bắt buộc.
- Enum hợp lệ.

Ví dụ:

- thiếu `id`
- sai kiểu `priority`
- enum không tồn tại

---

# 6. Structural Validation

Kiểm tra:

- Thứ tự field chuẩn.
- Không có field dư.
- Không thiếu object bắt buộc.
- Mảng hợp lệ.
- Không có object rỗng nếu không được phép.

---

# 7. Reference Validation

Kiểm tra:

- Rule ID tồn tại.
- Dictionary tồn tại.
- Terminology tồn tại.
- Cross Reference hợp lệ.
- Namespace hợp lệ.

Không được tham chiếu tới đối tượng không tồn tại.

---

# 8. Semantic Validation

Kiểm tra ý nghĩa nghiệp vụ.

Ví dụ:

- Rule không tự mâu thuẫn.
- Source hợp Target.
- Category đúng Family.
- Family đúng Type.
- Priority hợp lệ.

Semantic Validation không kiểm tra thuật toán.

---

# 9. Governance Validation

Kiểm tra:

- Version.
- Metadata.
- Naming Convention.
- Authoring Guide.
- Changelog.

---

# 10. Validation Severity

Có 4 mức:

| Level | Ý nghĩa |
|--------|----------|
| INFO | Thông tin |
| WARNING | Cảnh báo |
| ERROR | Lỗi |
| FATAL | Không thể phát hành |

---

# 11. Validation Report

Mỗi lần Validation phải sinh báo cáo gồm:

- Tổng số đối tượng.
- Số lỗi.
- Số cảnh báo.
- Danh sách lỗi.
- Thời gian chạy.
- Phiên bản Validator.

---

# 12. Validation Checklist

Mỗi Rule phải kiểm tra:

- Identity
- Classification
- Source
- Target
- Conditions
- Evaluation
- Priority
- Lifecycle
- Metadata

---

# 13. Exit Criteria

Một Module chỉ được phép phát hành khi:

- Không có FATAL.
- Không có ERROR.
- WARNING đã được xem xét.
- Validation Report được lưu trữ.

---

# 14. Automation

Validation phải có khả năng:

- Chạy bằng CLI.
- Chạy trong CI/CD.
- Chạy trước Merge.
- Chạy trước Release.

---

# 15. Governance

Không Merge dữ liệu nếu:

- Validation thất bại.
- Thiếu Metadata.
- Sai Naming Convention.
- Sai Versioning.

---

# 16. Kết luận

Validation là cơ chế đảm bảo chất lượng của Knowledge Base.

Mọi dữ liệu phải vượt qua Validation trước khi được sử dụng hoặc phát hành.