# SUPPORT_TAXONOMY.md

> Module: 08_support_attack / 01_support_rules
>
> Version: 1.0
>
> Status: Stable
>
> Document Type: Taxonomy Specification
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa hệ thống phân loại (Taxonomy) cho toàn bộ Support Rule của BTE Platform.

Mục tiêu:

- Chuẩn hóa thuật ngữ.
- Chuẩn hóa tên Rule.
- Chuẩn hóa Category.
- Chuẩn hóa Support Type.
- Đảm bảo mọi Rule đều thuộc đúng nhóm.
- Tránh trùng lặp và mâu thuẫn khi mở rộng Rule Database.

Taxonomy là nền tảng để xây dựng Rule Schema, Rule Database và SupportAttack Engine.

---

# 2. Kiến trúc phân loại

Support được phân loại theo nhiều tầng.

```

Support

├── Direct Support

├── Indirect Support

├── Seasonal Support

├── Root Support

├── Combination Support

├── Pattern Support

├── Useful God Support

└── Special Support

```

---

# 3. Direct Support

## Định nghĩa

Quan hệ làm tăng sức mạnh trực tiếp của Target mà không cần điều kiện trung gian.

### Ví dụ

- Mộc sinh Hỏa
- Hỏa sinh Thổ
- Kim sinh Thủy

### Đặc điểm

- tác động trực tiếp
- trọng số ổn định
- luôn ưu tiên cao

---

# 4. Indirect Support

## Định nghĩa

Support được hình thành thông qua điều kiện trung gian.

Ví dụ

- hợp hóa thành hành sinh Nhật Chủ
- chuỗi sinh nhiều bước
- trợ lực gián tiếp

---

# 5. Seasonal Support

Support đến từ:

- mùa
- tiết khí
- khí hậu

Ví dụ

Mùa Xuân

↓

Mộc tăng lực

---

# 6. Root Support

Support đến từ:

- Tàng Can
- Thông Căn
- Đắc Địa
- Đắc Lệnh

Đây là nguồn Support nền tảng của Nhật Chủ.

---

# 7. Combination Support

Bao gồm:

- Thiên Can Hợp
- Lục Hợp
- Tam Hợp
- Tam Hội
- Bán Hợp
- Hợp Hóa

---

# 8. Pattern Support

Support đến từ:

- Cách Cục
- Thành Cách
- Thuần Cách
- Phá Cách
- Phục Cách

---

# 9. Useful God Support

Support liên quan:

- Dụng Thần
- Hỷ Thần

Không bao gồm Kỵ Thần.

---

# 10. Special Support

Bao gồm:

- Thiên Ất Quý Nhân
- Thiên Đức
- Nguyệt Đức
- Văn Xương
- Hoa Cái
- các Support đặc biệt khác

---

# 11. Taxonomy Levels

Support được chuẩn hóa theo 5 cấp.

| Level | Ý nghĩa |
|--------|----------|
| Level 1 | Category |
| Level 2 | Support Group |
| Level 3 | Support Type |
| Level 4 | Rule Family |
| Level 5 | Individual Rule |

Ví dụ:

Category

↓

Seasonal Support

↓

Spring Support

↓

Wood Support

↓

SUP-000123

---

# 12. Quy tắc đặt tên

Rule ID

```

SUP-000001

```

Category

```

seasonal_support

```

Support Type

```

direct_generate

```

Rule Family

```

wood_to_fire

```

---

# 13. Quan hệ giữa các nhóm

```

Direct Support

↓

Seasonal Modifier

↓

Root Modifier

↓

Combination Modifier

↓

Special Modifier

↓

Final Support

```

---

# 14. Khả năng mở rộng

Có thể bổ sung:

- Category mới
- Support Type mới
- Rule Family mới

mà không thay đổi Taxonomy hiện tại.

---

# 15. Kết luận

Taxonomy là nền tảng phân loại cho toàn bộ Support Rule trong BTE Platform.

Mọi Rule, Schema, Pipeline và Engine phải sử dụng cùng hệ thống phân loại này để đảm bảo tính nhất quán, khả năng mở rộng và khả năng bảo trì lâu dài.