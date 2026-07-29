# PIPELINE_MODEL_SPEC.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Pipeline Model Specification
>
> BTE Platform

---

# 1. Mục đích

`PIPELINE_MODEL_SPEC.md` định nghĩa Pipeline chuẩn của BTE Platform.

Pipeline mô tả **thứ tự xử lý**, **trách nhiệm của từng giai đoạn** và **dữ liệu trao đổi giữa các bước**.

Pipeline không mô tả thuật toán chi tiết của từng Engine.

---

# 2. Mục tiêu

Pipeline được thiết kế để:

- Chuẩn hóa luồng xử lý.
- Giảm phụ thuộc giữa các Engine.
- Dễ kiểm thử.
- Dễ mở rộng.
- Dễ thay thế từng bước.

---

# 3. Kiến trúc tổng quát

```
Raw Input
      │
      ▼
Context Builder
      │
      ▼
Context
      │
      ▼
Validation
      │
      ▼
Rule Loader
      │
      ▼
Rule Matcher
      │
      ▼
Priority Resolver
      │
      ▼
Score Engine
      │
      ▼
Interpretation Builder
      │
      ▼
Result Builder
      │
      ▼
Result
```

---

# 4. Các giai đoạn

| Stage | Mục đích |
|--------|----------|
| Input | Nhận dữ liệu gốc |
| Context Builder | Chuẩn hóa dữ liệu |
| Validation | Kiểm tra tính hợp lệ |
| Rule Loader | Nạp Rule Database |
| Rule Matcher | Tìm Rule phù hợp |
| Priority Resolver | Giải quyết xung đột |
| Score Engine | Tính điểm |
| Interpretation Builder | Sinh diễn giải |
| Result Builder | Chuẩn hóa đầu ra |

---

# 5. Input

Đầu vào của Pipeline là Raw Data.

Ví dụ:

- Ngày giờ sinh.
- Giới tính.
- Địa điểm.
- Múi giờ.

---

# 6. Context Builder

Tạo Context theo chuẩn `CONTEXT_MODEL_SPEC.md`.

Đây là bước duy nhất được phép chuyển đổi Raw Data thành Context.

---

# 7. Validation

Kiểm tra:

- Thiếu dữ liệu.
- Sai định dạng.
- Không hợp lệ.

Nếu Validation thất bại, Pipeline phải dừng hoặc trả về lỗi chuẩn hóa.

---

# 8. Rule Loader

Đọc Rule Database.

Không thực hiện Matching.

Không sửa đổi Rule.

---

# 9. Rule Matcher

Đánh giá Rule với Context.

Đầu ra là danh sách Rule Match.

---

# 10. Priority Resolver

Giải quyết:

- Rule trùng.
- Rule xung đột.
- Rule loại trừ.
- Rule ghi đè.

Theo chính sách Priority.

---

# 11. Score Engine

Tính toán điểm số dựa trên Rule đã được chọn.

Đầu ra là Scores.

---

# 12. Interpretation Builder

Chuyển kết quả có cấu trúc thành nội dung diễn giải.

Không thực hiện Layout.

---

# 13. Result Builder

Tạo Result theo chuẩn `RESULT_MODEL_SPEC.md`.

Đây là bước cuối cùng của Pipeline.

---

# 14. Đầu ra

Pipeline chỉ sinh duy nhất một đối tượng:

```
Result
```

Report, API hoặc UI không phải là một phần của Pipeline.

---

# 15. Nguyên tắc

Pipeline phải:

- Deterministic.
- Stateless.
- Idempotent.
- Traceable.
- Testable.
- Modular.

---

# 16. Quan hệ với các Model

```
Raw Input
      │
      ▼
Context
      │
      ▼
Rule
      │
      ▼
Pipeline
      │
      ▼
Result
```

Pipeline sử dụng:

- Context Model.
- Rule Model.
- Result Model.

Pipeline không định nghĩa lại các Model này.

---

# 17. Extension

Có thể bổ sung Stage mới nếu:

- Không phá vỡ thứ tự chuẩn.
- Có tài liệu đặc tả.
- Có kiểm thử.

---

# 18. Versioning

Pipeline tuân theo Semantic Versioning.

---

# 19. Governance

Mọi Engine mới phải tích hợp vào Pipeline thông qua các Stage chuẩn, không được bỏ qua các bước bắt buộc hoặc thay đổi giao diện dữ liệu giữa các Stage nếu chưa được chuẩn hóa.

---

# 20. Kết luận

`PIPELINE_MODEL_SPEC.md` định nghĩa luồng xử lý chuẩn của BTE Platform, kết nối **Context**, **Rule** và **Result** thành một quy trình thống nhất, giúp các Engine hoạt động độc lập nhưng vẫn tương thích với nhau.