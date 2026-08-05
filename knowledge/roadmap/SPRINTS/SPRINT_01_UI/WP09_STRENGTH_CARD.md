# BTE Platform V1.0

# Work Package 09 — Strength Card

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP09 |
| Name | Strength Card |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Critical) |
| Estimated | 8–10 giờ |

---

# 1. Goal

Xây dựng khu vực hiển thị kết quả đánh giá **Thân Vượng / Thân Nhược** trên màn hình Kết Quả Bát Tự.

Đây là một trong những thông tin quan trọng nhất của toàn bộ hệ thống BTE.

WP này chỉ hiển thị dữ liệu.

Không thực hiện tính toán.

---

# 2. Scope

Bao gồm

- Strength Summary
- Score Display
- Level Indicator
- Progress Visualization
- Short Description
- Confidence Badge (placeholder)

Không bao gồm

- Useful God
- Favorable Elements
- Interpretation
- Rule Logic
- Score Engine

---

# 3. Layout

```
THÂN VƯỢNG NHƯỢC

────────────────────────────

Điểm tổng

82 / 100

██████████████░░░

Kết luận

THÂN VƯỢNG

Mức độ

Mạnh

Độ tin cậy

98 %

────────────────────────────

Mô tả ngắn

Thân được mùa sinh,
có nhiều trợ lực,
khả năng tự lập cao.

```

---

# 4. Data Structure

API trả về

```
strength:

score

level

label

confidence

summary
```

Ví dụ

```
{
    score:82,
    label:"THÂN VƯỢNG",
    level:"Strong",
    confidence:98,
    summary:"..."
}
```

Nếu backend chưa hoàn thiện

→ sử dụng Mock Data.

---

# 5. Components

Chỉ sử dụng

- Card
- Badge
- ProgressBar
- Typography
- Tooltip

Không tạo component mới.

---

# 6. Visual Rules

Hiển thị

- Điểm số
- Thanh tiến trình
- Trạng thái
- Badge
- Mô tả

Card phải nổi bật hơn các Card thông thường.

---

# 7. Future Ready

Chuẩn bị vị trí cho

- Seasonal Influence
- Temperature Effect
- Root Strength
- Support Score
- Exhaust Score

Không triển khai trong WP này.

---

# 8. UX Rules

Có

- Loading Skeleton
- Empty State
- Error State

Hover hiển thị Tooltip.

---

# 9. Responsive

Desktop

Card toàn chiều ngang.

Tablet

Thu gọn.

Mobile

Stack toàn bộ.

---

# 10. Coding Rules

Không xử lý Business Logic.

Không gọi API.

Không hardcode dữ liệu.

Component độc lập.

---

# 11. Acceptance Criteria

PASS khi

- Hiển thị đúng trạng thái.
- Responsive đúng.
- Có Loading / Empty / Error.
- Build thành công.
- Không lỗi TypeScript.

---

# 12. Cursor Instructions

Cursor chỉ xây dựng giao diện.

Không tính toán Thân Vượng Nhược.

Không sửa Engine.

Không sửa Rule Database.

Nếu thiếu dữ liệu

→ dùng Mock Data.

→ ghi TODO.