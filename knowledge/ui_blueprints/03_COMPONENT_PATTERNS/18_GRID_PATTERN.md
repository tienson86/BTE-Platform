# BTE Platform

# Canonical Component Pattern — Grid

---

Version

1.0.0

Status

ACTIVE

Component

Grid

Category

Infrastructure Component

---

# 1. Purpose

Grid Pattern định nghĩa cách bố trí Component trên màn hình.

Grid không phải CSS Grid.

Grid là Business Layout System.

---

# 2. Business Goal

Giúp mọi màn hình:

- cân đối
- dễ đọc
- nhất quán

Grid không quyết định nội dung.

Grid chỉ quyết định bố cục.

---

# 3. Usage Context

Cho phép:

Dashboard

BaZi Result

Knowledge

Report

Admin

---

# 4. Grid Types

Type A

1 Column

Dùng cho:

Interpretation

Knowledge

Hero

---

Type B

2 Columns

Dùng cho:

Strength

Element Balance

Summary Pair

---

Type C

3 Columns

Dùng cho:

Metric Cards

Info Cards

Statistics

---

Type D

4 Columns

Dùng cho:

Dashboard KPI

Overview Metrics

---

# 5. Layout Structure

Desktop

1 / 2 / 3 / 4 Columns

Tablet

1 / 2 Columns

Mobile

1 Column

Không ngoại lệ.

---

# 6. Component Composition

Grid chỉ chứa:

Section

Card

Panel

Không chứa:

Logic

Rule

State

---

# 7. Visual Hierarchy

Grid không tạo Hierarchy.

Hierarchy do Component quyết định.

---

# 8. Grid Rules

Một Row chỉ chứa:

Cùng loại Component.

Ví dụ:

Info Card + Info Card

✓

Hero + Card

✗

Summary + Metric

✗

---

# 9. Spacing

Gap theo Design Token.

Không hardcode.

---

# 10. Alignment

Top Align.

Không Center toàn bộ Card.

---

# 11. Responsive Rules

Desktop

4 → 3 → 2 → 1

Tablet

2 → 1

Mobile

1

---

# 12. Breakpoint Behaviour

Desktop

≥1280

Tablet

768–1279

Mobile

<768

---

# 13. Accessibility

Reading Order không thay đổi khi Responsive.

Keyboard đúng thứ tự.

---

# 14. Anti-Patterns

Không:

❌ Hero trong Grid.

❌ Grid lồng quá 2 cấp.

❌ Card cao thấp lộn xộn.

❌ Grid chỉ vì "đẹp".

---

# 15. Screenshot Standard

Desktop

Tablet

Mobile

---

# 16. Cursor Rules

Không tự chọn số cột.

Luôn theo Pattern.

---

# 17. Product Owner Checklist

□ Reading Flow đúng.

□ Responsive đúng.

□ Khoảng cách đều.

---

# 18. Component Relationship

Layout

↓

Grid

↓

Section

↓

Component

---

# 19. Reuse Matrix

Dashboard ✓

BaZi ✓

Knowledge ✓

Report ✓

Admin ✓

---

# 20. Future Compatibility

Grid phải hỗ trợ:

Desktop

Tablet

Mobile

PDF

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

1 Column

┌──────────────┐
│ Component    │
└──────────────┘

2 Columns

┌──────┬──────┐
│Card A│Card B│
└──────┴──────┘

3 Columns

┌────┬────┬────┐
│ A  │ B  │ C  │
└────┴────┴────┘

4 Columns

┌──┬──┬──┬──┐
│A │B │C │D │
└──┴──┴──┴──┘

---

# Appendix B — Reading Order

Left

↓

Right

↓

Next Row

Không đổi theo Responsive.

---

# Appendix C — Priority Matrix

| Grid | Use Case |
|------|----------|
| 1 | Hero / Knowledge |
| 2 | Pair Analysis |
| 3 | Metrics |
| 4 | Dashboard KPI |

---

# Appendix D — Common Mistakes

- Trộn nhiều loại Card trong cùng hàng.
- Grid quá nhiều cột.
- Không responsive.
- Khoảng cách không đều.

---

# Appendix E — Design Principle

Grid không trả lời:

"Hiển thị cái gì?"

Grid chỉ trả lời:

"Các Component sẽ được sắp xếp như thế nào?"