# SUPPORT_ATTACK_SPEC.md

> Module: 08_support_attack
>
> Version: 1.0
>
> Status: Specification
>
> BTE Platform

---

# 1. Mục đích

## 1.1 Giới thiệu

Tài liệu này đặc tả toàn bộ quy tắc nghiệp vụ và yêu cầu kỹ thuật của module **Support Attack**.

Module có nhiệm vụ chuẩn hóa cách xác định:

- Support
- Attack
- Relation
- Score
- Priority

Tất cả các quyết định đều phải được điều khiển bởi dữ liệu trong Knowledge Base thay vì logic hard-code.

---

## 1.2 Phạm vi

Module chịu trách nhiệm:

- xác định quan hệ hỗ trợ
- xác định quan hệ khắc chế
- xác định quan hệ trung gian
- tính điểm
- chuẩn hóa kết quả
- xuất dữ liệu cho Engine

Module không chịu trách nhiệm:

- luận giải
- sinh văn bản
- hiển thị báo cáo
- AI Rewrite

---

# 2. Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|------------|----------|
| Support | Quan hệ hỗ trợ |
| Attack | Quan hệ khắc chế |
| Relation | Quan hệ giữa hai thực thể |
| Source | Thực thể tạo tác động |
| Target | Thực thể nhận tác động |
| Weight | Trọng số |
| Score | Điểm |
| Priority | Độ ưu tiên |

---

# 3. Input Specification

Module nhận Context đã được chuẩn hóa.

Context tối thiểu gồm:

- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Season
- Temperature
- Strength Result
- Pattern Result (nếu có)

Module không tự tính các dữ liệu này.

---

# 4. Output Specification

Output chuẩn:

```json
{
  "support": [],
  "attack": [],
  "relations": [],
  "scores": {},
  "priority": {},
  "metadata": {}
}
```

Output luôn là JSON.

---

# 5. Support Specification

## 5.1 Khái niệm

Support là mọi quan hệ có tác dụng tăng cường hoặc duy trì sức mạnh của Target.

Support không đồng nghĩa với "sinh".

Một Support có thể đến từ:

- sinh
- đồng hành
- trợ mùa
- trợ căn
- trợ khí
- hợp hóa

---

## 5.2 Thuộc tính

Support gồm:

- id
- source
- target
- support_type
- weight
- condition
- priority
- explanation

---

## 5.3 Điều kiện áp dụng

Một Support Rule chỉ được áp dụng khi:

- điều kiện đầu vào hợp lệ
- không bị Rule Priority loại bỏ
- không bị Override
- không bị Conflict Resolution hủy

---

# 6. Attack Specification

## 6.1 Khái niệm

Attack là mọi quan hệ làm giảm sức mạnh của Target.

Attack có thể là:

- khắc
- tiết
- hao
- áp chế
- phá hủy
- triệt tiêu

---

## 6.2 Thuộc tính

Attack gồm:

- id
- source
- target
- attack_type
- weight
- condition
- priority

---

## 6.3 Điều kiện

Rule chỉ được kích hoạt nếu:

- source tồn tại
- target tồn tại
- điều kiện đúng
- priority cho phép

---

# 7. Relation Specification

Relation mô tả mối quan hệ giữa hai hoặc nhiều thực thể.

Ví dụ:

- sinh
- khắc
- đồng hành
- tương hợp
- tương xung
- tương hình
- phá
- hại
- bán hợp
- tam hợp
- tam hội

Relation không tự tính điểm.

---

# 8. Scoring Specification

Scoring chia thành bốn giai đoạn.

## 8.1 Support Score

Tổng hợp toàn bộ lực hỗ trợ.

---

## 8.2 Attack Score

Tổng hợp toàn bộ lực khắc.

---

## 8.3 Adjustment

Điều chỉnh theo:

- Priority
- Override
- Seasonal Modifier
- Temperature Modifier

---

## 8.4 Final Score

Điểm cuối cùng.

---

# 9. Rule Execution

Pipeline thực hiện:

```
Load Rules

↓

Validate

↓

Normalize

↓

Support

↓

Attack

↓

Relation

↓

Score

↓

Priority

↓

Output
```

Không được thay đổi thứ tự.

---

# 10. Conflict Resolution

Nếu nhiều Rule cùng áp dụng:

1.

Loại Rule không hợp lệ

↓

2.

So sánh Priority

↓

3.

Override

↓

4.

Merge

↓

5.

Final Rule

---

# 11. Priority

Priority chia thành:

- Absolute
- High
- Normal
- Low
- Disabled

Priority không được hard-code.

---

# 12. Validation

Mỗi Rule phải kiểm tra:

- Schema
- Version
- Required Field
- Enum
- Data Type
- Circular Reference

---

# 13. Error Handling

Các nhóm lỗi:

- Invalid Input
- Invalid Schema
- Missing Field
- Unknown Rule
- Invalid Priority
- Invalid Relation
- Invalid Weight

Mã lỗi được định nghĩa trong ERROR_CODES.md.

---

# 14. Logging

Mỗi Rule phải log:

- Rule ID
- Stage
- Source
- Target
- Weight
- Result
- Time

---

# 15. JSON Schema

Support Rule:

```json
{
  "id": "",
  "source": "",
  "target": "",
  "support_type": "",
  "weight": 0,
  "priority": ""
}
```

Attack Rule:

```json
{
  "id": "",
  "source": "",
  "target": "",
  "attack_type": "",
  "weight": 0,
  "priority": ""
}
```

Relation:

```json
{
  "source": "",
  "target": "",
  "relation": ""
}
```

---

# 16. Ví dụ

## Ví dụ 1

Kim sinh Thủy

↓

Support

---

## Ví dụ 2

Thủy khắc Hỏa

↓

Attack

---

## Ví dụ 3

Mộc sinh Hỏa

↓

Support

Thủy khắc Hỏa

↓

Attack

↓

Final Score

---

# 17. Performance Requirement

Yêu cầu tối thiểu:

- Rule Load một lần
- Cache Rule
- Không đọc lại JSON
- O(n) với tập Rule cùng loại
- Hỗ trợ mở rộng song song trong tương lai

---

# 18. Compatibility

Module tương thích với:

- Strength Rules
- Season Rules
- Temperature Rules
- Pattern Rules
- Combination Rules
- Priority Rules
- Interpretation Engine

---

# 19. Versioning

Mỗi Rule bắt buộc có:

- version
- created_at
- updated_at
- author
- status

---

# 20. Glossary

Danh sách toàn bộ thuật ngữ sử dụng trong module.

---

# 21. Kết luận

Support Attack Specification là tài liệu chuẩn mô tả toàn bộ quy tắc nghiệp vụ và yêu cầu kỹ thuật của module Support Attack.

Mọi dữ liệu, Rule Database, Scoring Engine và SupportAttack Engine phải tuân thủ đặc tả trong tài liệu này nhằm đảm bảo tính nhất quán, khả năng kiểm thử, khả năng giải thích và mở rộng lâu dài cho BTE Platform.