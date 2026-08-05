# BTE Platform V1.0

# Work Package 02 — Component Library

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP02 |
| Version | 1.0 |
| Status | READY |
| Priority | P0 |
| Estimated | 6–8 giờ |

---

# 1. Goal

Xây dựng Component Library thống nhất cho toàn bộ Portal.

Tất cả màn hình trong BTE V1.0 phải sử dụng chung các component này.

---

# 2. Scope

## Được phép

- Xây dựng component
- Refactor component trùng lặp
- Áp dụng Design Token từ WP01

## Không được phép

- Chỉnh sửa Engine
- Chỉnh sửa API
- Chỉnh sửa Business Logic
- Thay đổi Routing
- Thêm package ngoài khi chưa được phê duyệt

---

# 3. Folder Structure

```
components/

base/
layout/
forms/
feedback/
navigation/
display/
charts/
```

Không thay đổi cấu trúc này.

---

# 4. Base Components

Bắt buộc có:

- Button
- IconButton
- Card
- Divider
- Badge
- Tag
- Avatar
- Chip

---

# 5. Form Components

- Input
- PasswordInput
- TextArea
- NumberInput
- Select
- MultiSelect
- Checkbox
- Radio
- Switch
- DatePicker
- SearchBox

---

# 6. Navigation

- Tabs
- Breadcrumb
- Pagination
- SidebarItem
- Topbar
- Menu
- Dropdown

---

# 7. Feedback

- Alert
- Toast
- Dialog
- Drawer
- Loading
- Skeleton
- EmptyState
- ErrorState

---

# 8. Display

- StatCard
- InfoCard
- MetricCard
- Timeline
- ScoreBar
- ProgressBar
- SectionTitle

---

# 9. Common Rules

Tất cả component phải:

- Reusable
- Stateless nếu có thể
- Có Props rõ ràng
- Có TypeScript Interface
- Không hardcode màu
- Không inline CSS

---

# 10. Documentation

Mỗi component cần có:

- Tên
- Props
- Ví dụ sử dụng
- Ghi chú nếu có hạn chế

---

# 11. Acceptance Criteria

PASS khi:

- Build thành công.
- Không lỗi TypeScript.
- Component không trùng chức năng.
- Đã sử dụng Design Tokens từ WP01.
- Không phá vỡ UI hiện có.

---

# 12. Cursor Instructions

Chỉ xây dựng Component Library.

Không cập nhật các page.

Không thay đổi giao diện nghiệp vụ.

Không tạo component ngoài danh sách nếu không có lý do kỹ thuật rõ ràng.