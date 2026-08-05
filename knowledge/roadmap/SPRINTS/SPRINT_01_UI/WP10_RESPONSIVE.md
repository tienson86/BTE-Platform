# BTE Platform V1.0

# Work Package 10 — Responsive Foundation

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP10 |
| Name | Responsive Foundation |
| Version | 1.0 |
| Status | READY |
| Priority | P0 |
| Estimated | 6–8 giờ |

---

# 1. Goal

Chuẩn hóa toàn bộ Responsive cho Portal.

Sau WP này

Responsive được xem là chuẩn của toàn bộ V1.

Các WP sau phải tuân theo chuẩn này.

---

# 2. Scope

Bao gồm

- Breakpoints
- Grid
- Container
- Typography Scale
- Card Layout
- Navigation
- Table
- Chart
- Drawer
- Dialog

Không bao gồm

- Business Logic
- API
- Engine

---

# 3. Breakpoints

```
Mobile

0 — 767

Tablet

768 — 1023

Laptop

1024 — 1439

Desktop

1440+
```

Không tự định nghĩa breakpoint khác.

---

# 4. Grid Rules

Desktop

12 cột.

Tablet

8 cột.

Mobile

4 cột.

Gap

24px.

---

# 5. Container

Desktop

Max Width

1440px

Laptop

1280px

Tablet

100%

Mobile

100%

---

# 6. Typography

Desktop

100%

Tablet

95%

Mobile

90%

Không dùng font-size cố định trong component.

---

# 7. Card Rules

Desktop

Grid nhiều cột.

Tablet

2 cột.

Mobile

1 cột.

Chiều cao card phải tự co giãn.

---

# 8. Tables

Desktop

Hiển thị đầy đủ.

Tablet

Scroll ngang nếu cần.

Mobile

Chuyển sang Card List nếu phù hợp.

---

# 9. Charts

Desktop

Hiển thị đầy đủ.

Tablet

Thu gọn.

Mobile

Stack.

Không overflow.

---

# 10. Sidebar

Desktop

Sidebar cố định.

Tablet

Sidebar thu gọn.

Mobile

Drawer.

---

# 11. Dialog

Desktop

Centered.

Tablet

Centered.

Mobile

Full Width.

---

# 12. Performance

Không render 2 phiên bản Desktop và Mobile cùng lúc.

Không duplicate component.

Ưu tiên CSS Responsive thay vì render condition nếu không cần.

---

# 13. Accessibility

Touch Target

≥44px

Focus rõ ràng.

Keyboard Navigation.

---

# 14. Testing Checklist

Cursor phải kiểm tra

□ 320 px

□ 375 px

□ 390 px

□ 414 px

□ 768 px

□ 1024 px

□ 1280 px

□ 1440 px

Không được có

- Overflow
- Horizontal Scroll
- Layout Break

---

# 15. Acceptance Criteria

PASS khi

- Responsive đúng trên tất cả breakpoint.
- Không có Horizontal Scroll.
- Không có Layout Shift.
- Không lỗi TypeScript.
- Build thành công.

---

# 16. Cursor Instructions

Cursor chỉ tối ưu Responsive.

Không thay đổi Business Logic.

Không thay đổi Component API.

Không refactor ngoài phạm vi.

Nếu phát hiện lỗi ngoài WP

→ ghi TODO.

→ không tự sửa.