# BTE Platform V1.0

# Work Package 04 — Dashboard

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP04 |
| Name | Dashboard |
| Version | 1.0 |
| Status | READY |
| Priority | P0 |
| Estimated | 8–10 giờ |

---

# 1. Goal

Xây dựng Dashboard làm trang chủ của Portal.

Dashboard chỉ hiển thị thông tin tổng quan và các lối vào chức năng chính.

Không thực hiện phân tích Bát Tự tại đây.

---

# 2. Scope

Bao gồm:

- Welcome Section
- Quick Actions
- Recent Analyses
- Statistics Cards
- Shortcut Cards
- Announcement Area (placeholder)

Không bao gồm:

- Luận giải
- Report
- Engine
- API mới

---

# 3. Layout

Dashboard sử dụng App Layout từ WP03.

Không tự tạo Layout mới.

---

# 4. Sections

## 4.1 Welcome

Hiển thị:

- Lời chào.
- Tên người dùng (nếu có).
- Mô tả ngắn về hệ thống.

---

## 4.2 Quick Actions

Các nút:

- Lập Lá Số Mới
- Xem Kết Quả
- Luận Giải
- Báo Cáo

Nếu chưa có chức năng thì điều hướng tới placeholder.

---

## 4.3 Statistics

Hiển thị dạng Card:

- Tổng số lá số
- Số lần phân tích
- Báo cáo đã tạo
- Hoạt động gần đây

Cho phép dùng dữ liệu mẫu (mock data).

---

## 4.4 Recent Analyses

Danh sách các lá số gần đây.

Hiển thị:

- Họ tên
- Ngày tạo
- Trạng thái
- Nút mở

Nếu chưa có dữ liệu thì hiển thị Empty State.

---

## 4.5 Announcement

Khu vực thông báo.

Chỉ sử dụng placeholder.

Không tích hợp CMS.

---

# 5. UX Rules

- Dashboard tải nhanh.
- Không có khoảng trắng bất hợp lý.
- Card đồng đều.
- Hover thống nhất.
- Empty State đẹp.
- Loading Skeleton đầy đủ.

---

# 6. Responsive

Desktop:

- Grid nhiều cột.

Tablet:

- Grid 2 cột.

Mobile:

- Grid 1 cột.

---

# 7. Coding Rules

- Tái sử dụng Component Library.
- Không hardcode màu.
- Không tạo component trùng.
- Dữ liệu mẫu tách riêng.

---

# 8. Acceptance Criteria

PASS khi:

- Dashboard hiển thị đúng trên Desktop, Tablet và Mobile.
- Build thành công.
- Không lỗi TypeScript.
- Không warning mới.
- Chỉ sử dụng App Layout từ WP03.

---

# 9. Cursor Instructions

Cursor chỉ xây dựng Dashboard.

Không tạo chức năng mới.

Không sửa Layout.

Không sửa API.

Không sửa Engine.

Nếu phát hiện thiếu dữ liệu, sử dụng mock data và ghi TODO để thay thế khi tích hợp backend.