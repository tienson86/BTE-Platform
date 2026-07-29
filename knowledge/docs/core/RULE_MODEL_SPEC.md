# RULE_MODEL_SPEC.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Rule Model Specification
>
> BTE Platform

---

# 1. Mục đích

`RULE_MODEL_SPEC.md` định nghĩa **Rule Model chuẩn** cho toàn bộ BTE Platform.

Rule Model mô tả cấu trúc logic của một Rule độc lập với:

- lĩnh vực nghiệp vụ,
- loại Rule,
- Engine thực thi.

Đây là mô hình dữ liệu nền tảng mà mọi Rule Database trong hệ thống phải tuân thủ.

---

# 2. Mục tiêu

Rule Model được thiết kế nhằm:

- Chuẩn hóa dữ liệu.
- Chuẩn hóa giao tiếp giữa Knowledge Base và Engine.
- Hỗ trợ mở rộng Rule Database.
- Hỗ trợ Validation.
- Hỗ trợ Versioning.
- Hỗ trợ Explainability.
- Đảm bảo khả năng kiểm thử.

---

# 3. Thiết kế tổng quát

Một Rule luôn được xem là một đơn vị tri thức độc lập.

```
Rule
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

Mỗi Rule phải có đầy đủ các thành phần bắt buộc trước khi được đăng ký vào Rule Registry.

---

# 4. Rule Identity

Identity xác định duy nhất một Rule trong toàn bộ hệ thống.

Bao gồm:

| Field | Required | Description |
|---------|----------|-------------|
| id | Yes | Rule ID duy nhất |
| code | Yes | Rule Code |
| name | Yes | Rule Name |

Nguyên tắc:

- ID không được thay đổi sau khi phát hành.
- Code phải duy nhất trong phạm vi Module.
- Name phục vụ hiển thị và tài liệu.

Ví dụ:

```json
{
  "id": "SUP-000001",
  "code": "wood_generate_fire",
  "name": "Wood Generates Fire"
}
```

---

# 5. Rule Classification

Classification xác định vị trí của Rule trong Taxonomy.

Bao gồm:

| Field | Description |
|---------|-------------|
| domain | Rule Domain |
| category | Rule Category |
| family | Rule Family |
| type | Rule Type |

Ví dụ:

```json
{
  "domain": "support",
  "category": "element_support",
  "family": "generating",
  "type": "wood_to_fire"
}
```

Các giá trị cụ thể do từng Module định nghĩa.

---

# 6. Rule Source

Source mô tả nguồn sinh ra tác động của Rule.

Ví dụ:

- Ngũ hành.
- Thiên Can.
- Địa Chi.
- Tàng Can.
- Mùa.
- Tiết khí.
- Nhiệt độ.
- Quan hệ Can Chi.
- Thần Sát.

Source không mô tả đối tượng chịu ảnh hưởng.

Ví dụ:

```json
{
  "source": {
    "element": "wood",
    "pillar": "month"
  }
}
```

---

# 7. Rule Target

Target mô tả đối tượng chịu tác động.

Ví dụ:

- Nhật Chủ.
- Dụng Thần.
- Hỷ Thần.
- Ngũ hành.
- Thiên Can.
- Địa Chi.
- Trụ.
- Cách Cục.

Ví dụ:

```json
{
  "target": {
    "role": "day_master"
  }
}
```

---

# 8. Rule Conditions

Conditions mô tả điều kiện kích hoạt Rule.

Một Rule có thể:

- không có Condition;
- có một Condition;
- có nhiều Condition.

Ví dụ:

```json
{
  "conditions": [
    {
      "type": "season",
      "operator": "equals",
      "value": "spring"
    }
  ]
}
```

Conditions chỉ mô tả điều kiện, không chứa thuật toán.

---

# 9. Rule Evaluation

Evaluation mô tả thông tin phục vụ đánh giá.

Bao gồm:

| Field | Description |
|---------|-------------|
| weight | Trọng số |
| stackable | Có cộng dồn hay không |
| max_stack | Giới hạn cộng dồn |
| exclusive | Có loại trừ Rule khác hay không |

Evaluation không phải kết quả cuối cùng của hệ thống.

---

# 10. Rule Priority

Priority xác định thứ tự xử lý.

Ví dụ:

```json
{
  "priority": {
    "level": "high",
    "order": 20
  }
}
```

Priority không biểu thị độ mạnh của Rule.

---

# 11. Rule Lifecycle

Lifecycle quản lý trạng thái của Rule.

Các trạng thái chuẩn:

```
Draft
Review
Approved
Active
Deprecated
Archived
```

Chỉ Rule ở trạng thái **Active** mới được sử dụng mặc định.

---

# 12. Rule Metadata

Metadata phục vụ quản trị.

Ví dụ:

```json
{
  "metadata": {
    "version": "1.0.0",
    "author": "BTE",
    "created_at": "2026-07-29",
    "updated_at": "2026-07-29",
    "tags": [
      "support",
      "element"
    ]
  }
}
```

Metadata không tham gia Matching.

---

# 13. Rule Object

Một Rule hoàn chỉnh:

```text
Rule
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

Đây là Object Model chuẩn của BTE Platform.

---

# 14. Rule Relationships

Một Rule có thể liên hệ với:

- Taxonomy.
- Validation.
- Priority.
- Rule Registry.
- Rule Loader.
- Rule Matcher.

Rule không được tham chiếu trực tiếp đến Engine.

---

# 15. Rule Invariants

Mọi Rule phải đảm bảo:

- Có Identity duy nhất.
- Có Classification hợp lệ.
- Có Metadata.
- Không chứa thuật toán.
- Không lưu trạng thái thực thi.
- Không thay đổi trong Runtime.
- Có thể tuần tự hóa (Serialize) thành JSON.

Đây là các bất biến (Invariants) của Rule Model.

---

# 16. Extension Policy

Rule Model chỉ cho phép mở rộng tại:

- Classification.
- Source.
- Target.
- Conditions.

Không được thay đổi:

- Identity.
- Evaluation.
- Priority.
- Lifecycle.
- Metadata.

Điều này đảm bảo tính tương thích giữa các Module.

---

# 17. Compatibility

Rule Model áp dụng cho mọi Rule Database:

- Support Rules.
- Attack Rules.
- Season Rules.
- Temperature Rules.
- Pattern Rules.
- Combination Rules.
- Strength Rules.
- Priority Rules.
- Interpretation Rules.

---

# 18. Versioning

Rule Model tuân theo Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Breaking Change chỉ được phép trong Major Version.

---

# 19. Governance

Mọi Rule mới phải:

- Tuân thủ Rule Model.
- Tuân thủ Rule Schema.
- Tuân thủ Validation.
- Tuân thủ Authoring Guide.

Rule không đạt yêu cầu sẽ không được đưa vào Rule Registry.

---

# 20. Kết luận

`RULE_MODEL_SPEC.md` là tài liệu định nghĩa **Rule Object chuẩn** của toàn bộ BTE Platform.

Mọi Rule Database, bất kể thuộc lĩnh vực nào, đều phải được xây dựng dựa trên mô hình này. Việc chuẩn hóa Rule Model giúp các Engine sử dụng chung một cấu trúc dữ liệu, giảm độ phức tạp của hệ thống và tạo nền tảng vững chắc cho việc mở rộng Knowledge Base trong tương lai.