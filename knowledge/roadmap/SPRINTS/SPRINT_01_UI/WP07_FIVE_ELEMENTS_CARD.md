# BTE Platform V1.0

# Work Package 07 — Five Elements Card

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP07 |
| Name | Five Elements Card |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Critical) |
| Estimated | 8–10 giờ |

---

# 1. Goal

Xây dựng khu vực hiển thị Ngũ Hành trên màn hình Kết Quả Bát Tự.

Đây là khu vực trực quan giúp người dùng nhanh chóng đánh giá sự phân bố Ngũ Hành của lá số.

WP này chỉ hiển thị dữ liệu.

Không thực hiện bất kỳ phép tính nào.

---

# 2. Scope

Bao gồm:

- Five Elements Summary
- Distribution Chart
- Percentage Display
- Score Display
- Strength Indicator
- Legend

Không bao gồm:

- Thân Vượng Nhược
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Luận giải

---

# 3. Layout

```
NGŨ HÀNH

┌─────────────────────────────────────┐

Biểu đồ phân bố

███████

Kim

███████████

Mộc

██████

Thủy

██████████████

Hỏa

████████

Thổ

---------------------------------------

Kim     xx %

Mộc     xx %

Thủy    xx %

Hỏa     xx %

Thổ     xx %

```

---

# 4. Data Structure

API trả về:

- Kim
- Mộc
- Thủy
- Hỏa
- Thổ

Mỗi hành gồm:

- Score
- Percentage
- Strength Level

Nếu backend chưa hoàn thiện:

Sử dụng Mock Data.

---

# 5. Components

Chỉ sử dụng:

- Card
- ProgressBar
- Badge
- Tooltip
- Typography

Không tạo component trùng.

---

# 6. Visualization

Biểu đồ phải hỗ trợ:

- Horizontal Bar
- Percentage
- Value
- Hover Tooltip

Thiết kế đủ linh hoạt để sau này có thể thay bằng Chart Library nếu cần.

---

# 7. UX Rules

- Dễ đọc.
- Khoảng cách đều.
- Hover hiển thị thông tin.
- Loading Skeleton.
- Empty State.
- Error State.

---

# 8. Responsive

Desktop

- Chart bên trái.
- Thống kê bên phải.

Tablet

- Chart trên.
- Thống kê dưới.

Mobile

- Một cột.

---

# 9. Future Ready

Thiết kế dự phòng cho:

- Seasonal Power
- Temperature Score
- Hidden Element Contribution
- Favorable Element Highlight

Không triển khai trong WP này.

---

# 10. Coding Rules

- Không xử lý business logic.
- Không gọi API trực tiếp.
- Không hardcode dữ liệu.
- Tách FiveElementsCard thành component độc lập.

---

# 11. Acceptance Criteria

PASS khi:

- Hiển thị đủ 5 hành.
- Responsive đúng.
- Có Loading / Empty / Error State.
- Không lỗi TypeScript.
- Build thành công.

---

# 12. Cursor Instructions

Cursor chỉ xây dựng giao diện.

Không tính toán Ngũ Hành.

Không sửa Engine.

Không sửa Rule Database.

Nếu thiếu dữ liệu:

→ sử dụng Mock Data.

→ ghi TODO để tích hợp sau.