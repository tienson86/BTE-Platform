# ATTACK_RULE_SPEC.md

> Module: 08_support_attack / 02_attack_rules
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Business Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả nghiệp vụ (Business Specification) cho toàn bộ **Attack Rule** trong BTE Platform.

Attack Rule mô tả các điều kiện và quan hệ làm suy yếu hoặc gây bất lợi cho một đối tượng đánh giá (Target) trong quá trình phân tích Bát Tự.

Specification này không mô tả thuật toán thực thi mà chỉ định nghĩa ý nghĩa, cấu trúc và hành vi của Rule.

---

# 2. Phạm vi

Attack Rule được sử dụng để biểu diễn:

- Quan hệ khắc (Controlling).
- Quan hệ tiết (Draining).
- Tác động bất lợi của mùa.
- Tác động bất lợi của nhiệt độ hoặc khí hậu.
- Tổn hại gốc rễ (Root Loss).
- Quan hệ Xung.
- Quan hệ Hình.
- Quan hệ Hại.
- Quan hệ Phá.
- Phá Cách.
- Tổn hại Dụng Thần.
- Các trường hợp đặc biệt.

Attack Rule không biểu diễn:

- Điểm số cuối cùng.
- Kết luận luận giải.
- Văn bản diễn giải.
- Logic xử lý trong Engine.

---

# 3. Định nghĩa Attack Rule

Một Attack Rule là một đơn vị tri thức mô tả:

- nguồn gây tác động (Source),
- đối tượng chịu tác động (Target),
- điều kiện áp dụng,
- mức độ ảnh hưởng,
- mức ưu tiên,
- vòng đời quản lý.

Rule phải độc lập và có thể đánh giá riêng lẻ.

---

# 4. Thành phần của Rule

Một Attack Rule bao gồm:

```
Attack Rule
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

Ý nghĩa từng trường được định nghĩa trong `SCHEMA_REFERENCE.md`.

---

# 5. Classification

Mỗi Rule phải thuộc đúng một Category.

Ví dụ:

- element_attack
- context_attack
- relation_attack
- structure_attack
- special_attack

Trong mỗi Category có thể có nhiều Family.

Ví dụ:

```
element_attack
    ↓
controlling
```

hoặc

```
relation_attack
    ↓
clash
```

---

# 6. Source

Source mô tả nguyên nhân tạo ra Attack.

Ví dụ:

- Ngũ hành.
- Thiên Can.
- Địa Chi.
- Tàng Can.
- Mùa.
- Nhiệt độ.
- Quan hệ Can Chi.
- Thần Sát.

Source không mô tả đối tượng bị tác động.

---

# 7. Target

Target mô tả đối tượng chịu Attack.

Ví dụ:

- Nhật Chủ.
- Dụng Thần.
- Hỷ Thần.
- Ngũ hành cụ thể.
- Trụ Năm.
- Trụ Tháng.
- Trụ Ngày.
- Trụ Giờ.

Một Rule có thể có một hoặc nhiều Target nếu được định nghĩa rõ trong Schema.

---

# 8. Conditions

Conditions xác định khi nào Rule được kích hoạt.

Điều kiện có thể dựa trên:

- Ngũ hành.
- Thiên Can.
- Địa Chi.
- Mùa.
- Tiết khí.
- Nhiệt độ.
- Quan hệ Can Chi.
- Pattern.
- Root.
- Các Context khác.

Nhiều Condition được kết hợp bằng toán tử logic theo quy định của Engine.

---

# 9. Evaluation

Evaluation mô tả mức độ ảnh hưởng của Rule.

Bao gồm:

- Weight.
- Stackable.
- Max Stack.
- Exclusive.
- Override Policy.

Evaluation không phải là điểm cuối cùng của hệ thống.

---

# 10. Priority

Priority xác định thứ tự xử lý khi nhiều Rule cùng thỏa điều kiện.

Priority không biểu thị mức độ mạnh yếu.

Priority chỉ phục vụ quá trình lựa chọn Rule.

Các mức chuẩn:

- absolute
- high
- normal
- low

---

# 11. Lifecycle

Mỗi Rule phải có trạng thái:

```
Draft
Review
Approved
Active
Deprecated
Archived
```

Chỉ Rule ở trạng thái **Active** mới được Engine nạp mặc định.

---

# 12. Metadata

Metadata tối thiểu bao gồm:

- version
- author
- created_at

Khuyến nghị bổ sung:

- updated_at
- tags
- references
- notes

Metadata không tham gia vào quá trình Match.

---

# 13. Quy tắc nghiệp vụ

Mọi Attack Rule phải tuân thủ:

- Có ID duy nhất.
- Có Category hợp lệ.
- Có Family hợp lệ.
- Có Source rõ ràng.
- Có Target rõ ràng.
- Có ít nhất một Evaluation.
- Có Priority.
- Có Metadata.
- Có Version.

Rule không đáp ứng các yêu cầu trên sẽ bị Validation từ chối.

---

# 14. Quan hệ giữa các Rule

Attack Rule không được phụ thuộc trực tiếp vào Rule khác.

Nếu cần biểu diễn quan hệ, phải thông qua:

- Category.
- Family.
- Type.
- Condition.
- Reference.

Không được tạo Circular Dependency.

---

# 15. Khả năng mở rộng

Specification hỗ trợ:

- Category mới.
- Family mới.
- Type mới.
- Context mới.
- Multi-school Rule Set.
- Dynamic Rule Loading.

Các mở rộng phải tương thích ngược với Schema hiện hành.

---

# 16. Kiểm thử

Mỗi Rule phải vượt qua:

- Schema Validation.
- Business Validation.
- Rule Validation.
- Golden Dataset.
- Regression Test.

Rule không hợp lệ không được phép đưa vào Rule Registry.

---

# 17. Quan hệ với các tài liệu khác

Tài liệu này được sử dụng cùng với:

- README.md
- ATTACK_TAXONOMY.md
- ATTACK_RULE_ARCHITECTURE.md
- SCHEMA_REFERENCE.md
- VALIDATION_RULES.md
- RULE_PRIORITY.md
- JSON_EXAMPLES.md

---

# 18. Kết luận

Attack Rule Specification là chuẩn nghiệp vụ chính thức của module `02_attack_rules`.

Tài liệu này đảm bảo mọi Attack Rule được xây dựng theo cùng một tiêu chuẩn, có thể kiểm chứng, mở rộng và sử dụng nhất quán trong toàn bộ BTE Platform mà không phụ thuộc vào thuật toán của các Engine.