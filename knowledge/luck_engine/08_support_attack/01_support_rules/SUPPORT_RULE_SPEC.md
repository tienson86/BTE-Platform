# SUPPORT_RULE_SPEC.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Business & Technical Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này đặc tả toàn bộ quy tắc nghiệp vụ của Support Rule.

Mọi Rule trong `01_support_rules` phải tuân thủ tài liệu này.

---

# 2. Định nghĩa

Support là bất kỳ quan hệ nào có tác dụng:

- tăng cường
- duy trì
- củng cố
- bổ trợ
- khuếch đại

sức mạnh của Target trong một ngữ cảnh xác định.

Support không đồng nghĩa với "sinh". Quan hệ sinh chỉ là một trường hợp của Support.

---

# 3. Thành phần của Support Rule

Mỗi Rule phải có tối thiểu các trường:

- `id`
- `name`
- `category`
- `support_type`
- `source`
- `target`
- `conditions`
- `weight`
- `priority`
- `enabled`
- `version`
- `metadata`

---

# 4. Phân loại Support

Support được chia thành:

1. Direct Support
2. Same Element Support
3. Seasonal Support
4. Root Support
5. Combination Support
6. Pattern Support
7. Useful God Support
8. Special Support

Chi tiết phân loại được quy định trong `SUPPORT_TAXONOMY.md`.

---

# 5. Điều kiện áp dụng

Một Rule chỉ được áp dụng khi:

- Input hợp lệ.
- Điều kiện của Rule được thỏa mãn.
- Rule đang ở trạng thái `enabled`.
- Không bị Rule Priority loại bỏ.
- Không bị Override bởi Rule có mức ưu tiên cao hơn.

---

# 6. Weight

`weight` biểu diễn mức độ ảnh hưởng của Rule.

Yêu cầu:

- Giá trị phải là số.
- Không âm.
- Có thể là số nguyên hoặc số thực.
- Ý nghĩa cụ thể của từng mức được quy định trong tài liệu Scoring.

---

# 7. Priority

Các mức ưu tiên:

- absolute
- high
- normal
- low
- disabled

Priority chỉ xác định **thứ tự xử lý**, không phản ánh mức độ mạnh yếu của Support.

---

# 8. Metadata

Mỗi Rule nên có các thông tin:

- author
- version
- created_at
- updated_at
- status
- tags
- references
- notes

---

# 9. Validation

Rule phải vượt qua các kiểm tra:

- Schema Validation
- Required Fields
- Enum Validation
- Type Validation
- Duplicate ID
- Version Compatibility

---

# 10. Quy tắc đánh giá

Thứ tự khuyến nghị:

1. Direct Support
2. Same Element Support
3. Seasonal Support
4. Root Support
5. Combination Support
6. Pattern Support
7. Useful God Support
8. Special Support

Thứ tự này giúp đánh giá từ các yếu tố nền tảng đến các yếu tố đặc biệt.

---

# 11. JSON Compliance

Mọi Rule phải:

- dùng UTF-8
- dùng snake_case
- có ID duy nhất
- tuân thủ Schema chính thức
- không chứa dữ liệu dư thừa

---

# 12. Ví dụ khái quát

```json
{
  "id": "SUP-000001",
  "name": "wood_generates_fire",
  "category": "five_elements",
  "support_type": "direct_support",
  "source": "wood",
  "target": "fire",
  "conditions": [],
  "weight": 20,
  "priority": "normal",
  "enabled": true,
  "version": "1.0"
}
```

---

# 13. Khả năng mở rộng

Cho phép bổ sung:

- Category mới.
- Support Type mới.
- Metadata mới.
- Điều kiện mới.
- Trọng số mới.

Không được làm thay đổi ý nghĩa của các Rule đã phát hành.

---

# 14. Tương thích

Support Rule phải tương thích với:

- Strength Rules
- Season Rules
- Temperature Rules
- Pattern Rules
- Priority Rules
- SupportAttack Engine

---

# 15. Kết luận

`SUPPORT_RULE_SPEC.md` là đặc tả chính thức cho toàn bộ Support Rule trong BTE Platform.

Mọi Rule, Schema, Pipeline và Engine phải tuân thủ tài liệu này nhằm đảm bảo tính nhất quán, khả năng kiểm thử, khả năng giải thích và khả năng mở rộng lâu dài của hệ thống.