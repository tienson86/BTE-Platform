# Knowledge Base

> Project: BTE Platform
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Package README

---

# 1. Giới thiệu

Thư mục `knowledge/` là kho tri thức (Knowledge Base) chính thức của BTE Platform.

Knowledge Base lưu trữ toàn bộ dữ liệu nghiệp vụ, quy tắc, từ điển, thư viện câu, tài liệu đặc tả và các chuẩn kỹ thuật phục vụ cho hệ thống phân tích Bát Tự, Tử Bình và các Engine liên quan.

Knowledge Base là nguồn dữ liệu chuẩn (Single Source of Truth) cho toàn bộ nền tảng.

---

# 2. Mục tiêu

Knowledge Base được xây dựng nhằm:

- Chuẩn hóa tri thức.
- Tách dữ liệu khỏi mã nguồn.
- Hỗ trợ Rule Engine.
- Hỗ trợ Interpretation Engine.
- Hỗ trợ Report Engine.
- Dễ mở rộng.
- Dễ kiểm thử.
- Dễ bảo trì.
- Dễ tự động hóa.

---

# 3. Cấu trúc

```
knowledge/
│
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── MANIFEST.json
│
├── docs/
│
├── rule_database/
│
├── dictionaries/
│
├── terminology/
│
├── phrase_library/
│
├── sentence_library/
│
└── report_templates/
```

---

# 4. Thành phần

| Thư mục | Vai trò |
|----------|----------|
| docs | Framework, Standards, Core Models |
| rule_database | Rule JSON |
| dictionaries | Dictionary |
| terminology | Thuật ngữ |
| phrase_library | Thư viện cụm từ |
| sentence_library | Thư viện câu |
| report_templates | Mẫu báo cáo |

---

# 5. Governance

Mọi thay đổi phải tuân thủ:

- Architecture
- Core Models
- Standards
- Validation
- Versioning

---

# 6. Version

Knowledge Base sử dụng Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

---

# 7. Kết luận

Knowledge Base là nền tảng dữ liệu của BTE Platform và là nguồn tham chiếu duy nhất cho toàn bộ các Engine.
