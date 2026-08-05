# BTE Platform V1.0

# Work Package 08 — Ten Gods Card

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP08 |
| Name | Ten Gods Card |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Critical) |
| Estimated | 8–10 giờ |

---

# 1. Goal

Xây dựng khu vực hiển thị Thập Thần.

Đây là khu vực phản ánh mối quan hệ giữa Nhật Chủ và các Thiên Can trong lá số.

WP này chỉ hiển thị dữ liệu.

Không thực hiện tính toán.

---

# 2. Scope

Bao gồm:

- Ten Gods Grid
- God Name
- Count
- Strength
- Description Preview
- Distribution Summary

Không bao gồm:

- Luận giải Thập Thần
- Chấm điểm
- Khuyến nghị

---

# 3. Layout

```
THẬP THẦN

┌──────────────────────────────────────────┐

Chính Quan

■■■■■■

Thiên Quan

■■■

Chính Ấn

■■■■■■■■

Thiên Ấn

■■■■

Tỷ Kiên

■■■■■

Kiếp Tài

■■■

Thực Thần

■■■■■■

Thương Quan

■■

Chính Tài

■■■■■■

Thiên Tài

■■■■

```

---

# 4. Data Structure

API trả về:

Mỗi Thập Thần gồm:

- Name
- Count
- Score
- Strength Level

Nếu backend chưa hoàn thiện:

Mock Data.

---

# 5. Components

Chỉ sử dụng:

- Card
- Badge
- ProgressBar
- Tooltip
- Typography

Không tạo component mới nếu đã có.

---

# 6. Visual Rules

Mỗi Thập Thần hiển thị:

- Tên
- Giá trị
- Thanh tiến trình
- Mức độ mạnh/yếu

Khoảng cách đồng đều.

Không dùng màu quá rực.

---

# 7. Future Ready

Thiết kế đủ chỗ cho:

- Favorable Marker
- Unfavorable Marker
- Detail Popup
- Interpretation Preview

Không triển khai trong WP này.

---

# 8. UX Rules

- Hover hiển thị Tooltip.
- Loading Skeleton.
- Empty State.
- Error State.

---

# 9. Responsive

Desktop

- Grid 2 cột.

Tablet

- Grid 2 cột.

Mobile

- 1 cột.

---

# 10. Coding Rules

- Không business logic.
- Không API trực tiếp.
- Không hardcode dữ liệu.
- Component độc lập.
- Reusable.

---

# 11. Acceptance Criteria

PASS khi:

- Hiển thị đầy đủ 10 Thập Thần.
- Responsive đúng.
- Có Loading / Empty / Error State.
- Không lỗi TypeScript.
- Build thành công.

---

# 12. Cursor Instructions

Cursor chỉ xây dựng giao diện.

Không tính toán Thập Thần.

Không sửa Engine.

Không sửa Rule Database.

Nếu dữ liệu chưa có:

→ sử dụng Mock Data.

→ ghi TODO để thay bằng dữ liệu thật sau khi tích hợp Analysis Engine.