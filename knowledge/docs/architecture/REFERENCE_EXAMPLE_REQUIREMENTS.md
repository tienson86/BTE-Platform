# REFERENCE_EXAMPLE_REQUIREMENTS.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Reference Example Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định các yêu cầu bắt buộc đối với mọi tài liệu trong thư mục:

```
knowledge/docs/reference_examples/
```

Reference Example không chỉ là ví dụ minh họa mà là **Canonical Reference Implementation**, được sử dụng làm chuẩn tham chiếu cho:

- Developer
- Knowledge Engineer
- AI Generator
- Validator
- Unit Test
- Integration Test
- Golden Dataset
- Documentation

---

# 2. Phạm vi áp dụng

Áp dụng cho tất cả các mẫu tham chiếu:

- Rule
- Context
- Result
- Pipeline
- Metadata
- Validation Report
- Các mẫu được bổ sung trong tương lai

---

# 3. Mục tiêu

Mọi Reference Example phải:

- Chính xác.
- Đầy đủ.
- Hợp lệ.
- Có thể thực thi.
- Có thể kiểm thử.
- Có khả năng mở rộng.
- Có khả năng tái sử dụng.
- Là ví dụ chính thức của Framework.

---

# 4. Phân loại Example

Mỗi loại đối tượng nên có ba mức:

## Minimal

Ví dụ tối thiểu nhưng hợp lệ.

Mục tiêu:

- Học Schema.
- Unit Test.
- Kiểm tra Parser.

---

## Complete

Ví dụ đầy đủ.

Bao gồm toàn bộ:

- REQUIRED Field
- RECOMMENDED Field
- Metadata
- Lifecycle
- Điều kiện
- Giá trị mẫu

Đây là Canonical Example.

---

## Invalid

Ví dụ cố ý sai.

Chỉ được phép chứa **một lỗi duy nhất**.

Mỗi Invalid Example chỉ kiểm thử một quy tắc Validation.

Ví dụ:

```
missing_id

invalid_priority

unknown_enum

bad_version

duplicate_code
```

---

# 5. Quy tắc đặt tên

Các file phải tuân thủ:

```
<object>_<variant>_v<major>.json
```

Ví dụ:

```
rule_complete_v1.json

rule_minimal_v1.json

rule_invalid_missing_id_v1.json

context_complete_v1.json

result_complete_v1.json
```

Không sử dụng tên mơ hồ như:

```
example.json

sample.json

test.json
```

---

# 6. Tiêu chuẩn bắt buộc

Mọi Example phải:

- Tuân thủ RULE_MODEL_SPEC.md
- Tuân thủ CONTEXT_MODEL_SPEC.md (nếu áp dụng)
- Tuân thủ RESULT_MODEL_SPEC.md (nếu áp dụng)
- Tuân thủ RULE_SCHEMA_REFERENCE.md
- Tuân thủ METADATA_STANDARD.md
- Tuân thủ JSON_STYLE_GUIDE.md
- Tuân thủ NAMING_CONVENTIONS.md
- Tuân thủ VERSIONING_POLICY.md
- Vượt qua VALIDATION_STANDARD.md

---

# 7. Metadata bắt buộc

Mỗi Example phải có Metadata.

Ví dụ:

```json
{
    "metadata": {
        "schema_version": "1.0.0",
        "version": "1.0.0",
        "status": "active",
        "origin": "reference_example",
        "author": "BTE",
        "reviewer": "",
        "created_at": "2026-07-29T00:00:00Z",
        "updated_at": "2026-07-29T00:00:00Z",
        "approved_at": "",
        "tags": [
            "reference_example"
        ]
    }
}
```

---

# 8. Giá trị mẫu

Các giá trị phải:

- Có ý nghĩa.
- Thực tế.
- Dễ hiểu.
- Không dùng dữ liệu ngẫu nhiên.
- Không dùng Lorem Ipsum.
- Không dùng Placeholder vô nghĩa.

Đúng:

```
wood

fire

spring
```

Sai:

```
abc

xxx

value1
```

---

# 9. Giá trị cố định

Các giá trị sau nên được sử dụng nhất quán:

| Thuộc tính | Giá trị |
|------------|----------|
| Version | 1.0.0 |
| Schema Version | 1.0.0 |
| Status | active |
| Origin | reference_example |
| Author | BTE |

---

# 10. Invalid Example

Invalid Example phải:

- Chỉ chứa một lỗi.
- Không phát sinh lỗi phụ.
- Có tên mô tả chính xác lỗi.
- Có tài liệu giải thích lỗi nếu cần.

Ví dụ:

```
rule_invalid_missing_id_v1.json
```

Không được đồng thời:

- thiếu ID
- sai Version
- sai Enum

---

# 11. Documentation

Mỗi Example nên có phần mô tả:

```json
{
    "documentation": {
        "summary": "...",
        "description": "...",
        "references": [
            "RULE_MODEL_SPEC.md",
            "RULE_SCHEMA_REFERENCE.md"
        ]
    }
}
```

Phần này hỗ trợ:

- Documentation Generator
- AI
- Review
- Audit

---

# 12. Validation

Mọi Example phải được kiểm tra theo 5 cấp:

1. Schema Validation
2. Structural Validation
3. Reference Validation
4. Semantic Validation
5. Governance Validation

Complete Example phải vượt qua toàn bộ.

Invalid Example phải thất bại đúng một quy tắc.

---

# 13. Vai trò trong kiểm thử

Reference Example được sử dụng làm:

- Golden Dataset
- Snapshot Test
- Regression Test
- Parser Test
- Documentation Test
- AI Evaluation

Không sử dụng trực tiếp trong Production.

---

# 14. Versioning

Reference Example được quản lý độc lập.

Ví dụ:

```
rule_complete_v1.json

rule_complete_v2.json
```

Không sửa đổi nội dung của phiên bản đã phát hành.

Nếu có thay đổi không tương thích, tạo phiên bản mới.

---

# 15. Governance

Mọi Reference Example mới phải:

- Có Metadata hợp lệ.
- Đúng Naming Convention.
- Được Validator kiểm tra.
- Được Reviewer phê duyệt.
- Đồng bộ với tài liệu trong `core/` và `standards/`.

---

# 16. Quan hệ với các tài liệu khác

| Tài liệu | Vai trò |
|----------|----------|
| RULE_MODEL_SPEC.md | Mô hình Rule |
| CONTEXT_MODEL_SPEC.md | Mô hình Context |
| RESULT_MODEL_SPEC.md | Mô hình Result |
| RULE_SCHEMA_REFERENCE.md | Schema chuẩn |
| METADATA_STANDARD.md | Metadata |
| VALIDATION_STANDARD.md | Kiểm tra chất lượng |
| JSON_STYLE_GUIDE.md | Định dạng JSON |
| NAMING_CONVENTIONS.md | Quy tắc đặt tên |
| VERSIONING_POLICY.md | Quản lý phiên bản |

---

# 17. Kết luận

`REFERENCE_EXAMPLE_REQUIREMENTS.md` là tài liệu đặc tả chính thức cho toàn bộ thư mục `reference_examples/`.

Mọi mẫu tham chiếu trong Knowledge Framework phải tuân thủ tài liệu này để đảm bảo tính nhất quán, khả năng kiểm thử, khả năng mở rộng và giá trị tham chiếu lâu dài.