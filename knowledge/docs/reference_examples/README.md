# Reference Examples

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Reference Examples
>
> BTE Platform

---

# 1. Mục đích

Thư mục `reference_examples/` chứa các mẫu tham chiếu chính thức (Canonical Reference Examples) của Knowledge Framework.

Các mẫu này minh họa cách áp dụng các tiêu chuẩn được định nghĩa trong:

- `architecture/`
- `core/`
- `standards/`

Chúng được sử dụng làm cơ sở tham chiếu cho việc phát triển, kiểm thử và xác thực dữ liệu trong toàn bộ BTE Platform.

---

# 2. Mục tiêu

Các Reference Example nhằm:

- Minh họa cấu trúc dữ liệu chuẩn.
- Làm mẫu cho việc xây dựng Rule mới.
- Hỗ trợ lập trình viên và AI sinh dữ liệu đúng chuẩn.
- Cung cấp dữ liệu mẫu cho Unit Test và Golden Dataset.
- Hỗ trợ kiểm tra tính tương thích của Framework.

---

# 3. Cấu trúc

```
reference_examples/
│
├── README.md
├── rule/
├── context/
├── result/
├── pipeline/
├── validation/
└── metadata/
```

---

# 4. Quy ước

Mỗi mẫu tham chiếu phải:

- Tuân thủ `RULE_SCHEMA_REFERENCE.md`.
- Tuân thủ `RULE_MODEL_SPEC.md`.
- Tuân thủ `JSON_STYLE_GUIDE.md`.
- Vượt qua `VALIDATION_STANDARD.md`.
- Có Metadata hợp lệ.

---

# 5. Các loại mẫu

## Minimal

Mẫu tối thiểu nhưng hợp lệ theo Schema.

## Complete

Mẫu đầy đủ, thể hiện tất cả các trường được khuyến nghị.

## Invalid

Mẫu cố ý chứa lỗi để phục vụ kiểm thử Validator.

---

# 6. Mục đích sử dụng

Reference Examples có thể được sử dụng cho:

- Tài liệu hướng dẫn.
- Unit Test.
- Integration Test.
- Golden Dataset.
- AI Prompting.
- Đào tạo thành viên mới.

Không sử dụng trực tiếp trong môi trường Production.

---

# 7. Nguyên tắc bảo trì

Mọi thay đổi đối với các Reference Example phải:

- Đồng bộ với các tài liệu trong `core/` và `standards/`.
- Được kiểm tra bằng Validator.
- Được cập nhật Metadata và CHANGELOG nếu thay đổi cấu trúc.

---

# 8. Kết luận

`reference_examples/` là tập hợp các mẫu tham chiếu chính thức của Knowledge Framework. Đây là cầu nối giữa tài liệu đặc tả và việc triển khai thực tế, giúp đảm bảo mọi thành phần trong BTE Platform đều tuân thủ cùng một chuẩn dữ liệu và quy trình.