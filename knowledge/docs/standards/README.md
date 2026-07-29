# Knowledge Standards

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable

---

# Giới thiệu

Thư mục `standards/` chứa các tiêu chuẩn kỹ thuật áp dụng cho toàn bộ Knowledge Base của BTE Platform.

Các tài liệu trong thư mục này đóng vai trò là nền tảng quản trị (Governance Layer), đảm bảo mọi dữ liệu tri thức được xây dựng, kiểm tra và phát hành theo cùng một bộ quy tắc.

---

# Mục tiêu

Các tiêu chuẩn nhằm:

- Chuẩn hóa dữ liệu.
- Chuẩn hóa quy trình xây dựng Rule.
- Chuẩn hóa Metadata.
- Chuẩn hóa Validation.
- Chuẩn hóa Versioning.
- Chuẩn hóa Naming.
- Đảm bảo khả năng mở rộng.
- Đảm bảo tính nhất quán giữa các Module.

---

# Cấu trúc

```
standards/
│
├── RULE_SCHEMA_REFERENCE.md
├── RULE_AUTHORING_GUIDE.md
├── NAMING_CONVENTIONS.md
├── VERSIONING_POLICY.md
├── VALIDATION_STANDARD.md
├── JSON_STYLE_GUIDE.md
├── METADATA_STANDARD.md
└── README.md
```

---

# Vai trò của từng tài liệu

| Tài liệu | Vai trò |
|----------|----------|
| RULE_SCHEMA_REFERENCE | Định nghĩa Schema chuẩn của Rule |
| RULE_AUTHORING_GUIDE | Hướng dẫn xây dựng Rule |
| NAMING_CONVENTIONS | Quy tắc đặt tên |
| VERSIONING_POLICY | Chính sách quản lý phiên bản |
| VALIDATION_STANDARD | Chuẩn kiểm tra dữ liệu |
| JSON_STYLE_GUIDE | Quy tắc định dạng JSON |
| METADATA_STANDARD | Chuẩn Metadata |

---

# Thứ tự áp dụng

Các tài liệu được áp dụng theo thứ tự ưu tiên sau:

1. RULE_SCHEMA_REFERENCE.md
2. RULE_MODEL_SPEC.md *(thuộc thư mục `core/`)*
3. RULE_AUTHORING_GUIDE.md
4. NAMING_CONVENTIONS.md
5. VERSIONING_POLICY.md
6. VALIDATION_STANDARD.md
7. JSON_STYLE_GUIDE.md
8. METADATA_STANDARD.md

Nếu có xung đột, tài liệu có mức ưu tiên cao hơn sẽ được áp dụng.

---

# Quan hệ với các thư mục khác

```
architecture/
        │
        ▼
core/
        │
        ▼
standards/
        │
        ▼
rule_database/
```

- **architecture/** định nghĩa kiến trúc tổng thể.
- **core/** định nghĩa các mô hình dữ liệu cốt lõi.
- **standards/** quy định các tiêu chuẩn quản trị.
- **rule_database/** triển khai dữ liệu tri thức theo các tiêu chuẩn trên.

---

# Đối tượng áp dụng

Các tiêu chuẩn trong thư mục này áp dụng cho:

- Rule Database
- Dictionary
- Terminology
- Phrase Library
- Sentence Library
- Report Templates
- Configuration
- Các công cụ sinh dữ liệu (AI, Script, Generator)
- Các công cụ Validation và CI/CD

---

# Governance

Mọi thay đổi đối với các tiêu chuẩn phải:

- Có Version.
- Có CHANGELOG.
- Được Review.
- Được phê duyệt trước khi phát hành.

---

# Kết luận

Thư mục `standards/` là nền tảng quản trị của Knowledge Framework trong BTE Platform.

Việc tuân thủ các tiêu chuẩn này giúp toàn bộ Knowledge Base duy trì tính nhất quán, khả năng kiểm thử, khả năng mở rộng và chất lượng lâu dài.