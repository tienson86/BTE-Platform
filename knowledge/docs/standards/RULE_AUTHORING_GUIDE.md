# RULE_AUTHORING_GUIDE.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Rule Authoring Guide
>
> BTE Platform

---

# 1. Mục đích

`RULE_AUTHORING_GUIDE.md` quy định các nguyên tắc và quy trình xây dựng Rule trong BTE Platform.

Tài liệu này nhằm đảm bảo mọi Rule được tạo ra đều:

- nhất quán;
- dễ hiểu;
- dễ bảo trì;
- có thể kiểm thử;
- tương thích với Knowledge Framework.

Tài liệu này áp dụng cho cả con người và các công cụ hỗ trợ sinh dữ liệu (AI, script, generator...).

---

# 2. Phạm vi áp dụng

Áp dụng cho mọi Rule Database, bao gồm nhưng không giới hạn:

- Support Rules
- Attack Rules
- Strength Rules
- Season Rules
- Temperature Rules
- Pattern Rules
- Combination Rules
- Follow Pattern Rules
- Special Rules
- Priority Rules

---

# 3. Nguyên tắc chung

Mọi Rule phải tuân thủ các nguyên tắc sau:

- Một Rule chỉ mô tả **một tri thức**.
- Rule không chứa thuật toán.
- Rule không chứa mã nguồn.
- Rule không phụ thuộc vào Engine.
- Rule phải có khả năng diễn giải.
- Rule phải có khả năng kiểm thử độc lập.

---

# 4. Quy tắc bắt buộc

Các mức độ yêu cầu được sử dụng trong tài liệu:

| Mức | Ý nghĩa |
|------|----------|
| MUST | Bắt buộc phải tuân thủ |
| SHOULD | Nên tuân thủ, chỉ ngoại lệ khi có lý do rõ ràng |
| MAY | Tùy chọn |

Ví dụ:

- Rule **MUST** có ID duy nhất.
- Rule **MUST** có Metadata.
- Rule **SHOULD** càng đơn giản càng tốt.
- Rule **MAY** có Tags bổ sung.

---

# 5. Quy trình tạo Rule

Quy trình chuẩn:

```
Business Knowledge
        │
        ▼
Rule Analysis
        │
        ▼
Rule Design
        │
        ▼
JSON Authoring
        │
        ▼
Validation
        │
        ▼
Peer Review
        │
        ▼
Approval
        │
        ▼
Merge
```

Không được bỏ qua bước Validation.

---

# 6. Khi nào tạo Rule mới

Tạo Rule mới khi:

- Xuất hiện tri thức mới.
- Có điều kiện kích hoạt mới.
- Có đối tượng tác động mới.
- Có mức ưu tiên khác.
- Không thể mở rộng Rule hiện tại mà vẫn giữ tính đơn nhiệm.

Không tạo Rule mới chỉ vì muốn thay đổi cách diễn giải.

---

# 7. Khi nào sửa Rule

Chỉ sửa Rule khi:

- Sửa lỗi dữ liệu.
- Bổ sung Metadata.
- Cập nhật tài liệu.
- Điều chỉnh mô tả.

Không thay đổi ý nghĩa nghiệp vụ của Rule đã phát hành.

Nếu ý nghĩa thay đổi, tạo Rule mới và đánh dấu Rule cũ là `deprecated`.

---

# 8. Nguyên tắc "Một Rule - Một Ý nghĩa"

Mỗi Rule chỉ biểu diễn một tri thức.

Đúng:

- Mộc sinh Hỏa.
- Hỏa sinh Thổ.

Sai:

- Mộc sinh Hỏa và Hỏa sinh Thổ trong cùng một Rule.

---

# 9. Thiết kế Conditions

Conditions phải:

- độc lập;
- rõ ràng;
- có thể kiểm thử.

Không viết điều kiện mơ hồ.

Ưu tiên chia nhiều điều kiện nhỏ thay vì một điều kiện quá phức tạp.

---

# 10. Thiết kế Source và Target

Source mô tả nguyên nhân.

Target mô tả đối tượng chịu tác động.

Không đảo ngược hai vai trò này.

Ví dụ:

```
Source: Wood

Target: Fire
```

---

# 11. Metadata

Mọi Rule phải có Metadata tối thiểu:

```json
{
  "version": "1.0.0",
  "status": "active",
  "created_at": "",
  "updated_at": ""
}
```

Không bỏ trống Metadata.

---

# 12. Naming

Tên Rule phải:

- ngắn gọn;
- rõ nghĩa;
- ổn định theo thời gian.

Không sử dụng:

- tên tạm;
- viết tắt khó hiểu;
- ký tự đặc biệt không cần thiết.

---

# 13. JSON Authoring

Rule phải:

- UTF-8.
- JSON hợp lệ.
- Không có comment.
- Không có field thừa.
- Thứ tự field theo `RULE_SCHEMA_REFERENCE.md`.

---

# 14. Validation

Mọi Rule phải vượt qua:

- Schema Validation.
- Enum Validation.
- Reference Validation.
- Duplicate Validation.
- Semantic Validation.

Không được Merge nếu Validation thất bại.

---

# 15. Review

Peer Review cần xác nhận:

- Rule đúng nghiệp vụ.
- Rule đúng Schema.
- Không trùng lặp.
- Không xung đột.
- Có Metadata.
- Có thể kiểm thử.

---

# 16. Versioning

Rule tuân theo Semantic Versioning.

- PATCH: sửa lỗi.
- MINOR: mở rộng tương thích.
- MAJOR: thay đổi không tương thích.

---

# 17. Deprecation

Không xóa Rule đang phát hành.

Quy trình:

```
Active
    │
    ▼
Deprecated
    │
    ▼
Archived
```

Rule Deprecated phải giữ nguyên ID để đảm bảo khả năng truy vết.

---

# 18. Checklist trước khi Merge

Mỗi Rule phải đáp ứng:

- [ ] Có ID duy nhất.
- [ ] Có Code.
- [ ] Có Name.
- [ ] Có Classification.
- [ ] Có Source.
- [ ] Có Target.
- [ ] Có Conditions.
- [ ] Có Evaluation.
- [ ] Có Priority.
- [ ] Có Lifecycle.
- [ ] Có Metadata.
- [ ] Validation thành công.
- [ ] Review hoàn tất.

---

# 19. Những điều không được làm

Không được:

- Thêm field ngoài Schema.
- Chứa thuật toán.
- Chứa mã nguồn.
- Tham chiếu trực tiếp tới Engine.
- Thay đổi ID sau khi phát hành.
- Gộp nhiều tri thức vào một Rule.
- Bỏ qua Validation.
- Bỏ qua Review.

---

# 20. Quan hệ với các tài liệu khác

Tài liệu này được sử dụng cùng với:

- RULE_SCHEMA_REFERENCE.md
- RULE_MODEL_SPEC.md
- VALIDATION_STANDARD.md
- NAMING_CONVENTIONS.md
- VERSIONING_POLICY.md

Nếu có mâu thuẫn, ưu tiên theo thứ tự:

1. RULE_SCHEMA_REFERENCE.md
2. RULE_MODEL_SPEC.md
3. RULE_AUTHORING_GUIDE.md
4. Các tài liệu Standards khác.

---

# 21. Kết luận

`RULE_AUTHORING_GUIDE.md` là tiêu chuẩn hướng dẫn xây dựng Rule của BTE Platform.

Mọi Rule phải được tạo, kiểm tra, rà soát và quản lý theo tài liệu này nhằm đảm bảo tính nhất quán, khả năng mở rộng và chất lượng lâu dài của Knowledge Base.