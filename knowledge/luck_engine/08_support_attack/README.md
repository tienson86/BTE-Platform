# 08_support_attack

> Version: 1.0
>
> Status: Stable Architecture
>
> Module Type: Knowledge Base
>
> BTE Platform

---

# 1. Giới thiệu

`08_support_attack` là module chịu trách nhiệm mô tả toàn bộ tri thức liên quan đến **quan hệ Hỗ trợ (Support)** và **Khắc chế (Attack)** giữa các thành phần trong hệ thống Bát Tự.

Đây là một trong những module nền tảng của Rule Database, cung cấp dữ liệu và quy tắc cho các engine:

- Strength Engine
- Pattern Engine
- Priority Engine
- Interpretation Engine
- Scoring Engine

Module này **không trực tiếp đưa ra kết luận luận mệnh**, mà chỉ cung cấp các quy tắc đánh giá về:

- lực hỗ trợ
- lực khắc chế
- quan hệ giữa các hành
- mức ảnh hưởng
- điểm số
- thứ tự ưu tiên

---

# 2. Mục tiêu

Module được xây dựng nhằm chuẩn hóa toàn bộ tri thức về Support và Attack thành dữ liệu có cấu trúc.

Các mục tiêu chính gồm:

- loại bỏ hard-code trong engine
- chuẩn hóa dữ liệu
- dễ mở rộng
- dễ kiểm thử
- dễ bảo trì
- có khả năng giải thích (Explainable AI)

---

# 3. Phạm vi

Module xử lý:

- Support Rules
- Attack Rules
- Relation Rules
- Support Scoring
- Attack Scoring
- Priority Resolution
- Pipeline Specification

Module không xử lý:

- luận giải cuối cùng
- sinh câu văn
- report
- render
- giao diện
- AI rewrite

---

# 4. Vai trò trong hệ thống

```

```
                    Knowledge Base

                         │
                         ▼

               08_support_attack

                         │

        ┌────────────────┼─────────────────┐
        ▼                ▼                 ▼

 Strength Engine   Pattern Engine   Priority Engine

        │                │                 │

        └────────────────┼─────────────────┘
                         ▼

              Interpretation Engine
```

---

# 5. Kiến trúc thư mục

```
08_support_attack/

├── README.md
├── SUPPORT_ATTACK_ARCHITECTURE.md
├── SUPPORT_ATTACK_SPEC.md

├── 01_support_rules/
├── 02_attack_rules/
├── 03_relation_rules/
├── 04_scoring/
├── 05_pipeline/

├── SCHEMA_REFERENCE.md
├── DATA_MODELS.md
├── JSON_EXAMPLES.md
├── ERROR_CODES.md
├── RULE_PRIORITY.md
├── EDGE_CASES.md
└── CHANGELOG.md
```

---

# 6. Thành phần

## 6.1 Support Rules

Lưu toàn bộ quy tắc xác định lực hỗ trợ.

Ví dụ:

- Ngũ hành sinh
- Đồng hành
- Trợ lực theo mùa
- Trợ lực theo tàng can

---

## 6.2 Attack Rules

Lưu toàn bộ quy tắc xác định lực khắc.

Ví dụ:

- Ngũ hành khắc
- Tiết khí làm suy
- Mất căn
- Bị hợp hóa

---

## 6.3 Relation Rules

Mô tả quan hệ giữa hai hoặc nhiều thực thể.

Ví dụ:

- sinh
- khắc
- tiết
- hao
- phản sinh
- phản khắc
- tương trợ
- trung hòa

---

## 6.4 Scoring

Chuẩn hóa cách tính điểm.

Ví dụ:

Support Score

Attack Score

Net Score

Final Score

---

## 6.5 Pipeline

Định nghĩa trình tự xử lý.

---

# 7. Luồng xử lý

```

```
Input

↓

Normalize

↓

Load Support Rules

↓

Load Attack Rules

↓

Evaluate Support

↓

Evaluate Attack

↓

Resolve Relation

↓

Calculate Score

↓

Apply Priority

↓

Output
```

---

# 8. Input

Module nhận dữ liệu từ:

- Four Pillars
- Hidden Stems
- Season Rules
- Temperature Rules
- Strength Rules
- Pattern Rules

Module không tự tính toán các dữ liệu này.

---

# 9. Output

Module trả về:

- SupportResult
- AttackResult
- RelationResult
- ScoreResult
- PriorityResult

Output luôn ở dạng JSON.

---

# 10. Quan hệ với các module khác

```
Strength Rules
        │
        ▼

Support Attack

        ▼

Pattern Rules

        ▼

Priority Rules

        ▼

Interpretation
```

---

# 11. Nguyên tắc thiết kế

Module tuân theo các nguyên tắc sau:

- Data Driven
- JSON First
- Deterministic
- Explainable
- Testable
- Modular
- Version Controlled
- Backward Compatible

---

# 12. Không sử dụng Hard-code

Mọi quy tắc đều phải được định nghĩa trong Rule Database.

Engine không được chứa:

- if ngũ hành...
- if nhật chủ...
- if mùa...

Mọi quyết định đều được lấy từ dữ liệu.

---

# 13. Quy trình xử lý

```
Load Rules

↓

Validate

↓

Normalize

↓

Execute

↓

Score

↓

Priority

↓

Export
```

---

# 14. Khả năng mở rộng

Module hỗ trợ mở rộng:

- thêm quy tắc mới
- thêm loại Support
- thêm loại Attack
- thêm Relation Type
- thêm Scoring Strategy
- thêm Priority Strategy

không cần sửa Engine.

---

# 15. Quy ước dữ liệu

Tất cả dữ liệu phải:

- UTF-8
- JSON
- snake_case
- versioned
- immutable sau khi phát hành

---

# 16. Testing

Module phải hỗ trợ:

- Unit Test
- Integration Test
- Regression Test
- Golden Dataset
- Snapshot Test

---

# 17. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Stable | Initial Architecture |

---

# 18. Roadmap

V1.0

- Support Rules
- Attack Rules
- Relation Rules
- Score Rules
- Pipeline

V1.1

- Multi-layer Support
- Dynamic Weight
- Advanced Priority

V2.0

- AI-assisted Rule Recommendation
- Adaptive Scoring
- Rule Optimization

---

# 19. Tài liệu liên quan

- SUPPORT_ATTACK_ARCHITECTURE.md
- SUPPORT_ATTACK_SPEC.md
- SCHEMA_REFERENCE.md
- DATA_MODELS.md
- RULE_PRIORITY.md
- EDGE_CASES.md

---

# 20. Kết luận

`08_support_attack` là module chuẩn hóa toàn bộ tri thức về **Hỗ trợ**, **Khắc chế** và **Quan hệ tương tác** trong hệ thống Bát Tự.

Mọi engine liên quan đến đánh giá sức mạnh, xác định cách cục, tính điểm và sinh luận giải đều phải sử dụng dữ liệu từ module này thay vì triển khai quy tắc trực tiếp trong mã nguồn.

Module đóng vai trò là nguồn dữ liệu trung tâm (Single Source of Truth) cho toàn bộ logic Support/Attack của BTE Platform.