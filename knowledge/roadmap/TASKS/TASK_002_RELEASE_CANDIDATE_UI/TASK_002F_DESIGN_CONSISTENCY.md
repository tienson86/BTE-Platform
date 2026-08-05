# BTE Platform V1.0

# TASK 002F — Design Consistency Review

---

## Document Information

| Item | Value |
|------|-------|
| Task | TASK_002F |
| Name | Design Consistency Review |
| Sprint | 01 |
| Phase | Release Candidate UI |
| Priority | P0 |
| Status | READY |
| Estimated | 4–6 giờ |

---

# Objective

Thực hiện kiểm tra toàn bộ Portal để đảm bảo sử dụng cùng một ngôn ngữ thiết kế (Design Language).

Mục tiêu là mọi màn hình của BTE Platform V1.0 phải mang cảm giác như một sản phẩm thống nhất, không phải tập hợp của nhiều màn hình được phát triển độc lập.

---

# Scope

Kiểm tra:

- Dashboard
- BaZi Result
- Header
- Sidebar
- Footer
- Dialog
- Drawer
- Tooltip
- Empty State
- Error State
- Skeleton
- Loading

---

# Design Consistency Checklist

## Typography

- Font family thống nhất.
- Font size theo Design System.
- Font weight đúng quy chuẩn.
- Line height đồng nhất.

---

## Colors

- Chỉ sử dụng Semantic Tokens.
- Không hardcode màu.
- Disabled state đồng nhất.
- Success / Warning / Error đồng nhất.

---

## Spacing

- Padding theo hệ 8px.
- Margin thống nhất.
- Khoảng trắng giữa các section đồng đều.

---

## Components

- Card cùng style.
- Button cùng style.
- Badge cùng style.
- Tooltip cùng style.
- Divider cùng style.

---

## Icons

- Kích thước thống nhất.
- Căn lề đúng.
- Không dùng icon trùng ý nghĩa khác style.

---

## Layout

- Card alignment.
- Grid spacing.
- Section spacing.
- Responsive alignment.

---

## Visual Hierarchy

- Tiêu đề nổi bật.
- Nội dung chính dễ nhận biết.
- Hành động chính (Primary Action) rõ ràng.
- Không có thành phần gây nhiễu.

---

# Out of Scope

- Engine
- API
- Business Logic
- Rule Engine
- Report Engine

---

# Deliverables

- Danh sách các điểm chưa thống nhất.
- Đề xuất chỉnh sửa.
- Sau khi chỉnh sửa, toàn bộ Portal có cùng Design Language.

---

# Acceptance Criteria

PASS khi:

- Không còn sự khác biệt về phong cách giữa Dashboard và BaZi Result.
- Typography đồng nhất.
- Colors đồng nhất.
- Components đồng nhất.
- Khoảng trắng đồng nhất.
- Product Owner chấp thuận.

---

# Cursor Instructions

Không thêm tính năng mới.

Không sửa Business Logic.

Chỉ điều chỉnh giao diện để đạt sự thống nhất.

Nếu phát hiện thay đổi ngoài phạm vi:

→ ghi TODO.

→ không tự triển khai.

---

# Completion Report

## Files Modified

...

## Design Issues Fixed

...

## Remaining Issues

...

## Build

PASS / FAIL

## TypeScript

PASS / FAIL

## Notes

...