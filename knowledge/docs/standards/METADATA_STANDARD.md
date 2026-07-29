# METADATA_STANDARD.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Metadata Standard
>
> BTE Platform

---

# 1. Mục đích

`METADATA_STANDARD.md` quy định cấu trúc và nguyên tắc sử dụng Metadata trong toàn bộ Knowledge Base của BTE Platform.

Metadata phục vụ:

- Quản trị dữ liệu.
- Truy vết thay đổi.
- Versioning.
- Review.
- Audit.
- Validation.
- Release Management.

Metadata không tham gia vào quá trình suy luận (Inference), Matching hoặc Scoring.

---

# 2. Phạm vi áp dụng

Metadata được sử dụng cho:

- Rule
- Rule Module
- Dictionary
- Terminology
- Phrase Library
- Sentence Library
- Report Template
- Configuration
- Documentation Manifest

---

# 3. Nguyên tắc

Metadata phải:

- Chuẩn hóa.
- Có cấu trúc thống nhất.
- Độc lập với nghiệp vụ.
- Có khả năng mở rộng.
- Có khả năng truy vết.
- Không chứa Logic.

---

# 4. Metadata chuẩn

Mọi đối tượng trong Knowledge Base nên có Metadata theo cấu trúc:

```json
{
    "metadata": {
        "version": "1.0.0",
        "status": "active",
        "author": "BTE",
        "reviewer": "",
        "created_at": "",
        "updated_at": "",
        "approved_at": "",
        "deprecated_at": null,
        "tags": [],
        "source": "",
        "license": ""
    }
}
```

---

# 5. Các trường chuẩn

| Field | Required | Mô tả |
|--------|----------|--------|
| version | MUST | Phiên bản hiện tại |
| status | MUST | Trạng thái |
| author | MUST | Người tạo |
| reviewer | SHOULD | Người rà soát |
| created_at | MUST | Ngày tạo |
| updated_at | MUST | Ngày cập nhật gần nhất |
| approved_at | MAY | Ngày phê duyệt |
| deprecated_at | MAY | Ngày ngừng sử dụng |
| tags | MAY | Nhãn phân loại |
| source | SHOULD | Nguồn tham khảo |
| license | MAY | Thông tin bản quyền |

---

# 6. Status chuẩn

Các giá trị hợp lệ:

```
draft
review
approved
active
deprecated
archived
```

---

# 7. Version

Version tuân theo:

```
MAJOR.MINOR.PATCH
```

Theo tài liệu:

```
VERSIONING_POLICY.md
```

---

# 8. Timestamp

Định dạng chuẩn:

```
ISO-8601 UTC
```

Ví dụ:

```
2026-07-29T08:30:00Z
```

Không sử dụng định dạng phụ thuộc vùng miền.

---

# 9. Tags

Tags:

- snake_case
- tiếng Anh
- không trùng lặp

Ví dụ:

```json
[
    "support",
    "five_elements",
    "wood"
]
```

---

# 10. Source

Source dùng để ghi nhận:

- Sách tham khảo.
- Tài liệu nghiên cứu.
- Quy chuẩn nội bộ.

Không dùng để lưu URL tạm thời hoặc ghi chú cá nhân.

---

# 11. Reviewer

Reviewer là người xác nhận nội dung đã được kiểm tra.

Không bắt buộc trong giai đoạn Draft nhưng bắt buộc trước khi Release.

---

# 12. Lifecycle

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

Metadata phải phản ánh đúng vòng đời của đối tượng.

---

# 13. Immutable Fields

Các trường sau không được thay đổi sau khi phát hành:

- created_at
- author

Các trường có thể thay đổi:

- version
- reviewer
- updated_at
- status
- tags

---

# 14. Validation

Metadata phải được kiểm tra:

- Đầy đủ Field bắt buộc.
- Định dạng Version.
- Định dạng Timestamp.
- Giá trị Status.
- Kiểu dữ liệu.

---

# 15. Governance

Không được phát hành đối tượng nếu:

- Thiếu Metadata.
- Sai Version.
- Sai Timestamp.
- Sai Status.

---

# 16. Kết luận

Metadata là nền tảng cho việc quản trị, kiểm soát chất lượng và truy vết toàn bộ Knowledge Base của BTE Platform.

Mọi thành phần trong hệ thống phải tuân thủ tiêu chuẩn Metadata này để đảm bảo tính minh bạch và khả năng bảo trì lâu dài.