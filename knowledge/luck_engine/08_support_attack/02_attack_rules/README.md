# README.md

> Module: 08_support_attack / 02_attack_rules
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Module Overview
>
> BTE Platform

---

# 1. Giới thiệu

`02_attack_rules` là module quản lý toàn bộ **Attack Rules (Quy tắc Công/Khắc/Tiết/Hao Tổn)** trong hệ thống BTE Platform.

Module này đóng vai trò là **Single Source of Truth** cho mọi quy tắc xác định các yếu tố làm suy yếu Nhật Chủ (Day Master) hoặc làm giảm sức mạnh của các thành phần trong lá số Bát Tự.

Toàn bộ dữ liệu trong module được xây dựng theo nguyên tắc:

- Data Driven
- JSON First
- Explainable
- Deterministic
- Versioned
- Testable
- Extensible

Module chỉ lưu trữ **tri thức (Knowledge)** và **quy tắc (Rules)**, không chứa thuật toán xử lý hay logic nghiệp vụ.

---

# 2. Mục tiêu

Module được xây dựng nhằm:

- Chuẩn hóa toàn bộ Attack Rule trong hệ thống.
- Tách dữ liệu khỏi thuật toán (Separation of Data and Logic).
- Hỗ trợ Strength Engine đánh giá mức độ suy yếu.
- Cung cấp dữ liệu cho SupportAttack Engine.
- Hỗ trợ Pattern Engine xác định Cách Cục.
- Hỗ trợ Interpretation Engine tạo luận giải có thể giải thích.
- Đảm bảo mọi quyết định của hệ thống đều có khả năng truy vết (Traceability).

---

# 3. Phạm vi

Module bao gồm các nhóm Rule liên quan đến:

- Quan hệ Ngũ hành gây khắc hoặc tiết.
- Ảnh hưởng của mùa làm suy yếu.
- Gốc rễ (Root) bị tổn hại.
- Quan hệ Can hợp, Chi hợp làm biến đổi lực.
- Xung.
- Hình.
- Hại.
- Phá.
- Quan hệ với Dụng Thần, Hỷ Thần và Kỵ Thần.
- Các trường hợp đặc biệt theo Rule Database.

Module không thực hiện:

- Tính điểm.
- Xác định Thân Vượng/Nhược.
- Giải đoán.
- Sinh câu luận.
- Quyết định Priority cuối cùng.

Các nhiệm vụ trên thuộc các Engine chuyên trách.

---

# 4. Vai trò trong kiến trúc

```
Knowledge Base
        │
        ▼
Attack Rules
        │
        ▼
SupportAttack Engine
        │
        ▼
Strength Engine
        │
        ▼
Pattern Engine
        │
        ▼
Interpretation Engine
```

Attack Rules là tầng dữ liệu nền, không phụ thuộc vào các Engine phía trên.

---

# 5. Cấu trúc thư mục

```
02_attack_rules/
│
├── README.md
├── ATTACK_TAXONOMY.md
├── ATTACK_RULE_ARCHITECTURE.md
├── ATTACK_RULE_SPEC.md
├── SCHEMA_REFERENCE.md
├── JSON_EXAMPLES.md
├── VALIDATION_RULES.md
├── RULE_PRIORITY.md
└── CHANGELOG.md
```

---

# 6. Thành phần của Attack Rule

Mỗi Attack Rule bao gồm các nhóm thông tin chính:

```
Attack Rule

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

Mọi Rule phải tuân thủ cấu trúc chuẩn được định nghĩa trong `SCHEMA_REFERENCE.md`.

---

# 7. Các nhóm Attack

Hệ thống phân loại Attack theo nhiều nguồn tác động khác nhau.

Ví dụ:

- Direct Attack
- Drain Attack
- Seasonal Attack
- Root Attack
- Combination Attack
- Clash Attack
- Punishment Attack
- Harm Attack
- Destruction Attack
- Pattern Attack
- Useful God Attack
- Special Attack

Chi tiết được mô tả trong `ATTACK_TAXONOMY.md`.

---

# 8. Quy trình xử lý

Attack Rule không tự thực thi.

Quy trình chuẩn:

```
Load Rule
      │
      ▼
Validate
      │
      ▼
Register
      │
      ▼
Match
      │
      ▼
Priority Resolution
      │
      ▼
Return Result
```

Engine chỉ đọc Rule Database và không được phép sửa đổi nội dung Rule trong quá trình thực thi.

---

# 9. Quan hệ với các module khác

Module phụ thuộc vào:

- Dictionary.
- Terminology.
- Rule Database.
- Priority Rules.

Module được sử dụng bởi:

- SupportAttack Engine.
- Strength Engine.
- Pattern Engine.
- Interpretation Engine.
- Golden Dataset.
- Rule Validator.

---

# 10. Nguyên tắc thiết kế

Module tuân thủ các nguyên tắc:

- Single Source of Truth.
- Data Driven.
- No Hard-code.
- Explainable Rules.
- Backward Compatibility.
- Semantic Versioning.
- Separation of Concerns.
- Deterministic Evaluation.

Không được viết thuật toán trong Rule Database.

Không được lưu trạng thái thực thi trong Rule.

Không được để Rule phụ thuộc trực tiếp vào Rule khác nếu không có định nghĩa rõ ràng.

---

# 11. Kiểm thử

Mọi Rule phải vượt qua:

- Schema Validation.
- Data Validation.
- Business Validation.
- Rule Validation.
- Golden Dataset Test.
- Regression Test.

Rule không vượt Validation sẽ không được nạp vào hệ thống.

---

# 12. Khả năng mở rộng

Module được thiết kế để:

- Bổ sung loại Attack mới.
- Mở rộng điều kiện đánh giá.
- Hỗ trợ nhiều trường phái Bát Tự.
- Hỗ trợ Plugin Rule Provider.
- Hỗ trợ Dynamic Rule Loading.

Các thay đổi phải đảm bảo khả năng tương thích ngược.

---

# 13. Roadmap

## Version 1.x

- Hoàn thiện Rule Database.
- Chuẩn hóa Taxonomy.
- Chuẩn hóa Validation.
- Chuẩn hóa Priority.

## Version 2.x

- Dynamic Rule Provider.
- Context-aware Attack Rule.
- Adaptive Rule Selection.
- Plugin-based Knowledge Source.

---

# 14. Kết luận

`02_attack_rules` là nền tảng tri thức chuẩn hóa cho toàn bộ các quy tắc **Attack** trong BTE Platform.

Module này cung cấp dữ liệu nhất quán, có khả năng giải thích và mở rộng, giúp các Engine phía trên đánh giá chính xác các yếu tố làm suy yếu Nhật Chủ và các thành phần của lá số Bát Tự mà không cần sử dụng logic hard-code.