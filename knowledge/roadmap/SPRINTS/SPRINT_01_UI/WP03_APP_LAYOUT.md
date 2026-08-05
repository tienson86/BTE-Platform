# BTE Platform V1.0

# Work Package 03 — Application Layout

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP03 |
| Name | Application Layout |
| Version | 1.0 |
| Status | READY |
| Priority | P0 |
| Estimated | 6–8 giờ |

---

# 1. Goal

Xây dựng bộ khung (Application Shell) thống nhất cho toàn bộ Portal BTE Platform.

Đây là nền tảng dùng chung cho tất cả các màn hình của V1.0.

Sau khi WP03 được nghiệm thu, Layout được xem là **UI Architecture Lock** và không thay đổi nếu không có quyết định từ Release Plan.

---

# 2. Scope

## Bao gồm

- App Shell
- Header
- Navigation
- Sidebar
- Content Container
- Footer
- Breadcrumb
- Page Wrapper
- Scroll Behavior
- Responsive Layout

## Không bao gồm

- Dashboard
- BaZi Result
- Analysis
- Report
- Business Logic
- API
- Engine

---

# 3. Folder Structure

```text
layouts/
├── AppLayout.tsx
├── AuthLayout.tsx
├── BlankLayout.tsx
├── Header/
├── Sidebar/
├── Footer/
├── Breadcrumb/
└── Navigation/
```

Không thay đổi cấu trúc này.

---

# 4. App Shell

Ứng dụng phải có:

- Header cố định
- Sidebar cố định (Desktop)
- Sidebar Drawer (Tablet/Mobile)
- Content Area
- Footer
- Notification Area
- Modal Root

---

# 5. Header

Header phải chứa:

- Logo BTE
- Search (placeholder)
- Notification Icon
- Theme Toggle (nếu đã có)
- User Menu

Không thêm chức năng nghiệp vụ.

---

# 6. Sidebar

Sidebar chỉ hiển thị điều hướng.

Menu V1.0:

- Dashboard
- Lập Lá Số
- Kết Quả Bát Tự
- Luận Giải
- Báo Cáo
- Hồ Sơ
- Cài Đặt

Không thêm menu V2.

---

# 7. Footer

Hiển thị:

- Phiên bản phần mềm
- Copyright
- Liên kết hỗ trợ (placeholder)

Không thêm nội dung marketing.

---

# 8. Responsive

Desktop:

- Sidebar cố định.

Tablet:

- Sidebar thu gọn.

Mobile:

- Sidebar dạng Drawer.

Không xuất hiện thanh cuộn ngang.

---

# 9. UX Rules

- Transition mượt.
- Khoảng trắng thống nhất.
- Header luôn hiển thị.
- Sidebar không nhấp nháy khi chuyển trang.
- Nội dung không bị che bởi Header.

---

# 10. Accessibility

- Hỗ trợ điều hướng bằng bàn phím.
- Focus rõ ràng.
- Sidebar có aria-label.
- Header có landmark.

---

# 11. Performance

- Layout không render lại khi chuyển trang nếu không cần.
- Lazy load nội dung trang.
- Không tạo state thừa.

---

# 12. Acceptance Criteria

PASS khi:

- Layout hoạt động ổn định trên Desktop, Tablet, Mobile.
- Không lỗi TypeScript.
- Không warning mới.
- Không thay đổi logic nghiệp vụ.
- Build thành công.

---

# 13. Cursor Instructions

Cursor chỉ xây dựng App Layout.

Không tạo màn hình nghiệp vụ.

Không chỉnh sửa Engine.

Không chỉnh sửa API.

Không thêm package mới nếu chưa được yêu cầu.