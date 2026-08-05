# BTE Platform V1.0

# Work Package 05 — BaZi Result Header

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP05 |
| Name | BaZi Result Header |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Critical) |
| Estimated | 6–8 giờ |

---

# 1. Goal

Xây dựng phần Header của màn hình Kết Quả Bát Tự.

Header là khu vực đầu tiên người dùng nhìn thấy sau khi lập lá số.

Header phải truyền tải ngay:

- Thông tin lá số
- Thông tin người được xem
- Trạng thái phân tích
- Các hành động chính

Không thực hiện bất kỳ tính toán nào.

Chỉ hiển thị dữ liệu.

---

# 2. Scope

Bao gồm:

- Page Header
- Chart Summary
- User Information
- Chart Metadata
- Quick Actions

Không bao gồm:

- Four Pillars
- Five Elements
- Ten Gods
- Analysis
- Interpretation
- Report

---

# 3. Layout

```
+-----------------------------------------------------------+

              KẾT QUẢ PHÂN TÍCH BÁT TỰ

------------------------------------------------------------

Người xem

Ngày sinh

Giới tính

Âm lịch

Dương lịch

Giờ sinh

Nơi sinh

Ngày lập lá số

Phiên bản Engine

------------------------------------------------------------

[ Xuất PDF ]

[ In ]

[ Chia sẻ ]

[ Phân tích lại ]

------------------------------------------------------------

```

---

# 4. Sections

## 4.1 Page Title

Hiển thị

- Kết Quả Bát Tự
- Mã lá số (nếu có)

---

## 4.2 Profile Summary

Hiển thị:

- Họ tên
- Giới tính
- Ngày sinh Dương lịch
- Ngày sinh Âm lịch
- Giờ sinh
- Nơi sinh

---

## 4.3 Chart Metadata

Hiển thị:

- Thời gian lập
- Engine Version
- Rule Database Version
- Interpretation Version

Dùng mock data nếu backend chưa có.

---

## 4.4 Quick Actions

Bao gồm:

- Xuất PDF
- In
- Chia sẻ
- Phân tích lại

Nếu chức năng chưa có:

Disable Button.

Không ẩn.

---

# 5. UX Rules

Header phải:

- Gọn
- Dễ đọc
- Không quá cao
- Responsive
- Có khoảng trắng hợp lý

---

# 6. Component Usage

Chỉ được sử dụng:

- Card
- Button
- Badge
- Avatar
- Divider
- IconButton

Không tạo component mới.

---

# 7. Responsive

Desktop

Thông tin chia 2–3 cột.

Tablet

2 cột.

Mobile

1 cột.

---

# 8. Accessibility

- Tất cả button có aria-label.
- Keyboard navigation.
- Contrast đạt chuẩn.

---

# 9. Coding Rules

- Không hardcode text.
- Chuẩn bị sẵn i18n.
- Không gọi API trực tiếp trong component.
- Không xử lý business logic.

---

# 10. Acceptance Criteria

PASS khi:

- Header hiển thị đầy đủ.
- Responsive đúng.
- Không lỗi TypeScript.
- Build thành công.
- Chỉ dùng Component Library.

---

# 11. Cursor Instructions

Cursor chỉ xây dựng Header.

Không thêm section mới.

Không sửa Layout.

Không sửa Engine.

Không sửa API.

Nếu thiếu dữ liệu:

→ sử dụng mock data.

→ ghi TODO.