# 01_support_rules

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Module Type: Knowledge Base
>
> BTE Platform

---

# 1. Giới thiệu

`01_support_rules` là module lưu trữ toàn bộ các quy tắc xác định **Support (Hỗ trợ)** trong hệ thống BTE Platform.

Support được hiểu là mọi yếu tố có khả năng **gia tăng, duy trì hoặc củng cố sức mạnh** của một đối tượng (Target) trong quá trình luận giải Bát Tự.

Module này là một phần của `08_support_attack` và đóng vai trò là **nguồn dữ liệu chuẩn (Single Source of Truth)** cho mọi logic liên quan đến Support.

Module **không chứa thuật toán xử lý**, không thực hiện tính toán và không đưa ra kết luận. Toàn bộ nội dung chỉ bao gồm các quy tắc (Rule), điều kiện áp dụng (Condition), trọng số (Weight) và metadata phục vụ cho các Engine.

---

# 2. Mục tiêu

Module được xây dựng nhằm:

- Chuẩn hóa toàn bộ tri thức về Support thành dữ liệu.
- Loại bỏ hoàn toàn hard-code trong Engine.
- Đảm bảo mọi quyết định đều có thể truy vết và giải thích.
- Hỗ trợ mở rộng bằng cách bổ sung Rule mà không sửa mã nguồn.
- Tạo nền tảng thống nhất cho Strength Engine, Pattern Engine, Score Engine và Interpretation Engine.

---

# 3. Phạm vi

Module chịu trách nhiệm mô tả:

- Quan hệ sinh (Generating Support)
- Quan hệ đồng hành (Same Element Support)
- Hỗ trợ theo mùa
- Hỗ trợ theo tàng can và căn khí
- Hỗ trợ từ hợp hóa
- Hỗ trợ từ cách cục
- Hỗ trợ từ Dụng Thần và Hỷ Thần
- Hỗ trợ từ Thần Sát cát
- Hỗ trợ theo điều kiện đặc biệt
- Trọng số và mức ưu tiên của từng Support Rule

Module **không** chịu trách nhiệm:

- Quan hệ khắc chế (Attack)
- Quan hệ xung, hình, hại, phá
- Tính điểm cuối cùng
- Giải quyết xung đột giữa nhiều Rule
- Luận giải kết quả
- Sinh câu văn
- Render báo cáo

---

# 4. Vai trò trong hệ thống

```
Knowledge Base
      │
      ▼

Support Rules
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

Support Rules chỉ cung cấp dữ liệu.

Mọi quá trình đánh giá được thực hiện bởi Engine.

---

# 5. Kiến trúc thư mục

```
01_support_rules/

├── README.md
├── SUPPORT_RULE_ARCHITECTURE.md
├── SUPPORT_RULE_SPEC.md

├── SCHEMA_REFERENCE.md
├── JSON_EXAMPLES.md
├── VALIDATION_RULES.md
├── RULE_PRIORITY.md
└── CHANGELOG.md
```

Các nhóm dữ liệu Rule sẽ được tổ chức thành các thư mục chuyên biệt trong các giai đoạn tiếp theo.

---

# 6. Khái niệm Support

Support là mọi quan hệ có khả năng:

- tăng cường sức mạnh
- duy trì trạng thái ổn định
- giảm tác động bất lợi
- bổ sung khí lực
- cải thiện điều kiện phát huy của Target

Support **không đồng nghĩa** với quan hệ "sinh" trong Ngũ hành.

Quan hệ sinh chỉ là một loại Support.

---

# 7. Phân loại Support

Module phân loại Support thành các nhóm chính sau.

## 7.1 Direct Support

Hỗ trợ trực tiếp.

Ví dụ:

- Mộc sinh Hỏa
- Hỏa sinh Thổ
- Thổ sinh Kim
- Kim sinh Thủy
- Thủy sinh Mộc

---

## 7.2 Same Element Support

Hỗ trợ từ cùng Ngũ hành.

Ví dụ:

- Kim trợ Kim
- Hỏa trợ Hỏa
- Thủy trợ Thủy

---

## 7.3 Seasonal Support

Hỗ trợ theo mùa và tiết khí.

Ví dụ:

- Mộc được tăng lực vào mùa Xuân.
- Hỏa được tăng lực vào mùa Hạ.

---

## 7.4 Root Support

Hỗ trợ từ căn khí.

Bao gồm:

- Tàng Can
- Thông Căn
- Đắc Địa
- Đắc Lệnh

---

## 7.5 Combination Support

Hỗ trợ hình thành từ:

- Thiên Can Hợp
- Địa Chi Tam Hợp
- Địa Chi Tam Hội
- Lục Hợp
- Bán Hợp
- Hợp Hóa

---

## 7.6 Pattern Support

Hỗ trợ đến từ Cách Cục.

Ví dụ:

- Cách cục thành cách
- Cách cục thuần
- Cách cục được bảo vệ

---

## 7.7 Useful God Support

Hỗ trợ liên quan đến:

- Dụng Thần
- Hỷ Thần

---

## 7.8 Special Support

Hỗ trợ từ:

- Quý Nhân
- Thiên Đức
- Nguyệt Đức
- Văn Xương
- Thiên Ất Quý Nhân
- các quy tắc đặc biệt khác

---

# 8. Thành phần của một Support Rule

Mỗi Rule tối thiểu bao gồm:

- Rule ID
- Rule Name
- Category
- Support Type
- Source
- Target
- Condition
- Weight
- Priority
- Version
- Metadata

Mọi Rule phải tuân thủ Schema chung của module.

---

# 9. Luồng xử lý

```
Load Rule

↓

Validate

↓

Normalize

↓

Match

↓

Apply

↓

Export Result
```

Module chỉ định nghĩa Rule.

Pipeline thực tế được thực hiện trong SupportAttack Engine.

---

# 10. Quan hệ với các module khác

Support Rules có phụ thuộc dữ liệu vào:

- Strength Rules
- Season Rules
- Temperature Rules
- Combination Rules
- Pattern Rules
- Useful God Rules
- Priority Rules

Support Rules không được tự tính các dữ liệu đầu vào này.

---

# 11. Nguyên tắc thiết kế

Module tuân thủ các nguyên tắc:

- Data Driven
- JSON First
- Explainable
- Deterministic
- Immutable Rule
- Single Responsibility
- Version Controlled
- Backward Compatible

---

# 12. Không sử dụng Hard-code

Mọi Rule đều phải được định nghĩa trong Rule Database.

Không được triển khai các quyết định như:

- if mùa xuân...
- if Mộc sinh Hỏa...
- if Nhật Chủ mạnh...

trực tiếp trong Engine.

Engine chỉ đọc và áp dụng Rule.

---

# 13. Chuẩn hóa dữ liệu

Mọi Rule phải:

- sử dụng UTF-8
- lưu dưới dạng JSON
- dùng snake_case
- có Rule ID duy nhất
- có Version
- có trạng thái (Status)
- có Metadata

---

# 14. Testing

Module phải hỗ trợ:

- Schema Validation
- Rule Validation
- Unit Test
- Integration Test
- Regression Test
- Golden Dataset Test

Mọi Rule phải có khả năng kiểm thử độc lập.

---

# 15. Khả năng mở rộng

Module được thiết kế để:

- thêm Support Type mới
- thêm Category mới
- thêm Weight Strategy mới
- thêm Priority Strategy mới
- thêm Condition mới

mà không cần sửa đổi Engine hoặc Rule hiện có.

---

# 16. Tài liệu liên quan

- SUPPORT_RULE_ARCHITECTURE.md
- SUPPORT_RULE_SPEC.md
- SCHEMA_REFERENCE.md
- JSON_EXAMPLES.md
- VALIDATION_RULES.md
- RULE_PRIORITY.md

---

# 17. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Stable | Initial release |

---

# 18. Roadmap

## V1.0

- Chuẩn hóa Support Rule
- Chuẩn hóa Schema
- Chuẩn hóa Metadata
- Chuẩn hóa Validation

## V1.1

- Dynamic Weight
- Conditional Support
- Context-aware Support

## V2.0

- Adaptive Rule
- Rule Recommendation
- AI-assisted Optimization

---

# 19. Kết luận

`01_support_rules` là module chuẩn hóa toàn bộ tri thức về **Hỗ trợ (Support)** trong hệ thống BTE Platform.

Module cung cấp dữ liệu có cấu trúc cho các Engine thông qua các Rule được chuẩn hóa, đảm bảo mọi quyết định về Support đều minh bạch, có khả năng giải thích, kiểm thử và mở rộng. Đây là nền tảng để các tầng xử lý phía trên đánh giá sức mạnh của Nhật Chủ, xác định Cách Cục, tính điểm và sinh luận giải một cách nhất quán trên toàn hệ thống.