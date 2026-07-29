# SUPPORT_ATTACK_ARCHITECTURE.md

> Module: 08_support_attack
>
> Version: 1.0
>
> Status: Architecture Blueprint
>
> BTE Platform

---

# 1. Mục tiêu

## 1.1 Mục đích

Tài liệu này mô tả kiến trúc tổng thể của module **Support Attack** trong BTE Platform.

Module chịu trách nhiệm chuẩn hóa toàn bộ quy trình xác định:

- Quan hệ hỗ trợ (Support)
- Quan hệ khắc chế (Attack)
- Quan hệ trung gian (Relation)
- Điểm ảnh hưởng (Score)
- Thứ tự ưu tiên (Priority)

Đây là tài liệu kiến trúc, **không định nghĩa quy tắc nghiệp vụ chi tiết**. Các quy tắc cụ thể được mô tả trong `SUPPORT_ATTACK_SPEC.md` và các thư mục Rule Database.

---

## 1.2 Mục tiêu kiến trúc

Kiến trúc được thiết kế nhằm đáp ứng các yêu cầu sau:

- Data-driven
- Rule-driven
- Explainable
- Deterministic
- Modular
- Testable
- Extensible
- Backward Compatible

---

# 2. Vai trò trong hệ thống

```
                         Four Pillars
                               │
                               ▼

                      Strength Engine
                               │
                               ▼

                  Season / Temperature
                               │
                               ▼

                  Support Attack Module
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼

        Pattern Engine   Priority Engine   Score Engine

              └────────────────┼────────────────┘
                               ▼

                 Interpretation Engine
```

Module Support Attack không tạo kết quả luận giải cuối cùng mà chỉ cung cấp dữ liệu đã được chuẩn hóa cho các engine phía sau.

---

# 3. Kiến trúc phân lớp

Module được tổ chức theo kiến trúc nhiều lớp (Layered Architecture).

```
Application Layer
        │
        ▼

Pipeline Layer
        │
        ▼

Scoring Layer
        │
        ▼

Relation Layer
        │
        ▼

Rule Layer
        │
        ▼

Knowledge Layer
```

## 3.1 Knowledge Layer

Chứa toàn bộ dữ liệu tĩnh.

Ví dụ:

- support rules
- attack rules
- relation rules
- priority tables

Không chứa logic xử lý.

---

## 3.2 Rule Layer

Đọc dữ liệu từ Knowledge Layer.

Thực hiện:

- validation
- parsing
- normalization
- version checking

---

## 3.3 Relation Layer

Xây dựng các quan hệ giữa các thực thể.

Ví dụ:

- sinh
- khắc
- tiết
- hao
- đồng hành
- phản sinh
- phản khắc

Layer này không tính điểm.

---

## 3.4 Scoring Layer

Chuẩn hóa toàn bộ phép tính.

Bao gồm:

- Support Score
- Attack Score
- Relation Score
- Final Score

---

## 3.5 Pipeline Layer

Điều phối toàn bộ quá trình xử lý.

---

## 3.6 Application Layer

Là Public API mà các Engine khác gọi tới.

Ví dụ:

```python
SupportAttackEngine.evaluate(context)
```

---

# 4. Kiến trúc thư mục

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

Mỗi thư mục có một trách nhiệm duy nhất (Single Responsibility).

---

# 5. Luồng dữ liệu

```
Input Context
       │
       ▼

Normalize Context
       │
       ▼

Load Rule Database
       │
       ▼

Support Evaluation
       │
       ▼

Attack Evaluation
       │
       ▼

Relation Resolution
       │
       ▼

Scoring
       │
       ▼

Priority Resolution
       │
       ▼

Output Result
```

Pipeline luôn chạy theo đúng thứ tự trên.

---

# 6. Domain Model

Module định nghĩa năm miền nghiệp vụ chính.

## 6.1 Support Domain

Quản lý toàn bộ quan hệ hỗ trợ.

Ví dụ:

- sinh
- trợ lực
- đồng hành
- tăng cường

---

## 6.2 Attack Domain

Quản lý toàn bộ quan hệ khắc chế.

Ví dụ:

- khắc
- áp chế
- tiêu hao
- suy yếu

---

## 6.3 Relation Domain

Biểu diễn mối quan hệ giữa các thực thể.

Một Relation bao gồm:

- nguồn tác động
- đích tác động
- loại quan hệ
- cường độ
- điều kiện áp dụng

---

## 6.4 Score Domain

Chịu trách nhiệm tổng hợp điểm.

Không quyết định ý nghĩa luận giải.

---

## 6.5 Pipeline Domain

Điều phối thứ tự thực thi giữa các Domain.

---

# 7. Nguyên tắc thiết kế

Module tuân thủ các nguyên tắc:

- Single Responsibility
- Separation of Concerns
- Open / Closed Principle
- Immutable Knowledge
- Rule First
- JSON First
- Explainable Decision
- Deterministic Output

---

# 8. Kiến trúc Rule Engine

Rule Engine bao gồm các thành phần:

```
Rule Loader
      │
      ▼

Rule Validator
      │
      ▼

Rule Normalizer
      │
      ▼

Rule Matcher
      │
      ▼

Rule Resolver
```

Mỗi thành phần chỉ thực hiện một nhiệm vụ.

---

# 9. Kiến trúc Scoring

Scoring được chia thành bốn giai đoạn:

```
Support Score

↓

Attack Score

↓

Relation Adjustment

↓

Final Score
```

Mỗi giai đoạn có thể được mở rộng mà không ảnh hưởng tới các giai đoạn còn lại.

---

# 10. Priority Resolution

Nếu nhiều quy tắc cùng áp dụng, Priority Engine sẽ:

1. Xác định các quy tắc đủ điều kiện.
2. So sánh mức ưu tiên.
3. Loại bỏ các quy tắc bị ghi đè.
4. Hợp nhất các quy tắc có thể cộng dồn.
5. Trả về tập quy tắc cuối cùng.

Support Attack Module không tự định nghĩa mức ưu tiên mà sử dụng dữ liệu từ `RULE_PRIORITY.md`.

---

# 11. Quản lý lỗi

Module phân loại lỗi theo các nhóm:

- Input Error
- Schema Error
- Validation Error
- Rule Error
- Pipeline Error
- Configuration Error

Mã lỗi được định nghĩa trong `ERROR_CODES.md`.

---

# 12. Logging

Mỗi bước trong Pipeline cần ghi nhận:

- Stage
- Rule áp dụng
- Rule bị loại
- Điểm trước điều chỉnh
- Điểm sau điều chỉnh
- Thời gian xử lý

Việc ghi log nhằm phục vụ kiểm thử, truy vết và giải thích kết quả.

---

# 13. Hiệu năng

Các yêu cầu tối thiểu:

- Rule Database chỉ nạp một lần (lazy loading hoặc cache).
- Không đọc lại tệp JSON trong mỗi lần đánh giá.
- Các Rule đã chuẩn hóa phải có thể tái sử dụng.
- Hỗ trợ mở rộng theo hướng bất đồng bộ nếu cần.

---

# 14. Kiểm thử

Module phải hỗ trợ:

- Unit Test
- Integration Test
- Regression Test
- Golden Dataset Test
- Snapshot Test

Tất cả quyết định của Rule Engine cần có khả năng tái lập với cùng dữ liệu đầu vào.

---

# 15. Khả năng mở rộng

Kiến trúc cho phép mở rộng:

- Thêm loại Support mới.
- Thêm loại Attack mới.
- Thêm Relation Type.
- Thêm chiến lược tính điểm.
- Thêm Pipeline Stage.
- Thêm Rule Source.

Không yêu cầu thay đổi Public API hoặc sửa đổi các Rule hiện có.

---

# 16. Tương thích

Module tương thích với:

- Strength Rules
- Season Rules
- Temperature Rules
- Pattern Rules
- Combination Rules
- Priority Rules
- Interpretation Engine
- Report Engine (thông qua kết quả đã chuẩn hóa)

---

# 17. Kết luận

Module **Support Attack** là tầng kiến trúc trung gian giữa Rule Database và các Engine nghiệp vụ.

Nó chuẩn hóa quá trình xác định quan hệ hỗ trợ và khắc chế thành một pipeline rõ ràng, có khả năng giải thích, kiểm thử và mở rộng. Mọi quyết định đều được điều khiển bởi dữ liệu trong Knowledge Base thay vì logic hard-code, giúp đảm bảo tính nhất quán và khả năng bảo trì lâu dài cho toàn bộ BTE Platform.