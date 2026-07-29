# REFERENCE_EXAMPLE_CHECKLIST.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Reference Example Checklist
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này cung cấp danh sách kiểm tra (Checklist) nhằm xác nhận rằng mọi Reference Example trong:

```
knowledge/docs/reference_examples/
```

đã tuân thủ đầy đủ các tiêu chuẩn của Knowledge Framework trước khi được:

- Commit
- Merge
- Release
- Sử dụng trong Unit Test
- Sử dụng làm Golden Dataset
- Sử dụng làm Canonical Reference

Checklist này là tài liệu thực thi (Execution Checklist) của:

```
REFERENCE_EXAMPLE_REQUIREMENTS.md
```

---

# 2. Hướng dẫn sử dụng

Checklist phải được áp dụng cho:

- Rule Examples
- Context Examples
- Result Examples
- Metadata Examples
- Validation Examples
- Pipeline Examples
- Các Reference Example được bổ sung trong tương lai

Mỗi mục phải được đánh dấu:

```
☐ Chưa kiểm tra

☑ Đạt

⚠ Cần xem xét

✖ Không đạt
```

---

# 3. Naming

| Kiểm tra | Trạng thái |
|----------|------------|
| File đúng quy tắc đặt tên | ☐ |
| Đúng phiên bản (`v1`, `v2`...) | ☐ |
| Không dùng tên mơ hồ (`sample`, `test`, `example`) nếu không có hậu tố rõ ràng | ☐ |
| Thư mục đúng cấu trúc | ☐ |

---

# 4. JSON Structure

| Kiểm tra | Trạng thái |
|----------|------------|
| JSON hợp lệ | ☐ |
| UTF-8 | ☐ |
| Không BOM | ☐ |
| Indent 4 spaces | ☐ |
| Key theo snake_case | ☐ |
| Không duplicate key | ☐ |
| Root object hợp lệ | ☐ |

---

# 5. Schema

| Kiểm tra | Trạng thái |
|----------|------------|
| Đúng Schema | ☐ |
| Đủ REQUIRED field | ☐ |
| Đủ RECOMMENDED field | ☐ |
| Không có field ngoài Schema | ☐ |
| Đúng kiểu dữ liệu | ☐ |

---

# 6. Metadata

| Kiểm tra | Trạng thái |
|----------|------------|
| Có Metadata | ☐ |
| Có schema_version | ☐ |
| Có version | ☐ |
| Có status | ☐ |
| Có origin | ☐ |
| Có author | ☐ |
| Timestamp đúng ISO-8601 UTC | ☐ |
| Metadata hợp lệ | ☐ |

---

# 7. Nội dung

| Kiểm tra | Trạng thái |
|----------|------------|
| Giá trị có ý nghĩa | ☐ |
| Không dùng Lorem Ipsum | ☐ |
| Không dùng Placeholder vô nghĩa | ☐ |
| Dữ liệu nhất quán | ☐ |
| Ví dụ phản ánh đúng nghiệp vụ | ☐ |

---

# 8. Documentation

| Kiểm tra | Trạng thái |
|----------|------------|
| Có documentation (nếu áp dụng) | ☐ |
| Có summary | ☐ |
| Có description | ☐ |
| Có references | ☐ |

---

# 9. Validation

| Kiểm tra | Trạng thái |
|----------|------------|
| Schema Validation | ☐ |
| Structural Validation | ☐ |
| Reference Validation | ☐ |
| Semantic Validation | ☐ |
| Governance Validation | ☐ |

---

# 10. Complete Example

Áp dụng cho các file `*_complete_*`.

| Kiểm tra | Trạng thái |
|----------|------------|
| Bao gồm toàn bộ REQUIRED field | ☐ |
| Bao gồm toàn bộ RECOMMENDED field | ☐ |
| Metadata đầy đủ | ☐ |
| Lifecycle đầy đủ | ☐ |
| Điều kiện mẫu đầy đủ | ☐ |
| Có thể dùng làm Canonical Reference | ☐ |

---

# 11. Minimal Example

Áp dụng cho các file `*_minimal_*`.

| Kiểm tra | Trạng thái |
|----------|------------|
| Chỉ giữ các trường tối thiểu | ☐ |
| Vẫn hợp lệ theo Schema | ☐ |
| Không chứa trường thừa | ☐ |

---

# 12. Invalid Example

Áp dụng cho các file `*_invalid_*`.

| Kiểm tra | Trạng thái |
|----------|------------|
| Chỉ chứa đúng một lỗi | ☐ |
| Lỗi đúng với tên file | ☐ |
| Không phát sinh lỗi phụ | ☐ |
| Phục vụ đúng mục đích kiểm thử | ☐ |

---

# 13. Versioning

| Kiểm tra | Trạng thái |
|----------|------------|
| Đúng Version Policy | ☐ |
| Không sửa đổi phiên bản đã phát hành | ☐ |
| Phiên bản mới được tạo khi có Breaking Change | ☐ |

---

# 14. Governance

| Kiểm tra | Trạng thái |
|----------|------------|
| Đã được Reviewer xác nhận | ☐ |
| Đã chạy Validator | ☐ |
| Đã cập nhật Metadata | ☐ |
| Đã đồng bộ với tài liệu `core/` | ☐ |
| Đã đồng bộ với `standards/` | ☐ |

---

# 15. Kết quả kiểm tra

| Mục | Giá trị |
|------|----------|
| Reviewer | |
| Ngày kiểm tra | |
| Phiên bản | |
| Kết quả | PASS / FAIL |
| Ghi chú | |

---

# 16. Tiêu chí PASS

Một Reference Example chỉ được coi là **PASS** khi:

- Không có lỗi Schema.
- Không có lỗi Validation.
- Đáp ứng đầy đủ các yêu cầu trong `REFERENCE_EXAMPLE_REQUIREMENTS.md`.
- Có Metadata hợp lệ.
- Được Reviewer xác nhận.

---

# 17. Quan hệ với các tài liệu khác

Checklist này được xây dựng dựa trên:

- `REFERENCE_EXAMPLE_REQUIREMENTS.md`
- `RULE_SCHEMA_REFERENCE.md`
- `RULE_MODEL_SPEC.md`
- `CONTEXT_MODEL_SPEC.md`
- `RESULT_MODEL_SPEC.md`
- `METADATA_STANDARD.md`
- `VALIDATION_STANDARD.md`
- `JSON_STYLE_GUIDE.md`
- `NAMING_CONVENTIONS.md`
- `VERSIONING_POLICY.md`

---

# 18. Kết luận

`REFERENCE_EXAMPLE_CHECKLIST.md` là công cụ kiểm soát chất lượng cuối cùng trước khi một Reference Example được đưa vào Knowledge Framework.

Mọi Canonical Reference Example của BTE Platform phải vượt qua Checklist này trước khi được sử dụng làm chuẩn tham chiếu hoặc Golden Dataset.