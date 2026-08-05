# BTE Platform

# MASTER_GRID

---

Version

1.0.0

Status

MASTER

Module

UI_MASTER

Document

MASTER_GRID

Owner

Product Owner

---

# 1. Purpose

MASTER_GRID định nghĩa hệ thống lưới (Grid System) chuẩn của toàn bộ BTE Platform Desktop.

Đây là nền tảng vật lý của toàn bộ Portal.

Mọi Screen, mọi Section, mọi Component đều phải được xây dựng trên Grid này.

MASTER_GRID là tài liệu có độ ưu tiên cao nhất đối với Layout.

---

# 2. Design Goal

Grid không tồn tại để chia cột.

Grid tồn tại để:

- tạo nhịp thị giác
- tạo sự nhất quán
- kiểm soát khoảng trắng
- giữ Information Hierarchy
- tăng khả năng đọc

Người dùng không nhìn thấy Grid.

Nhưng phải cảm nhận được sự cân bằng.

---

# 3. Design Philosophy

BTE sử dụng:

Content First Grid

không phải

Bootstrap Grid.

Không phụ thuộc:

- Tailwind
- Bootstrap
- Ant Design
- Material UI

Grid thuộc về Business.

Không thuộc Framework.

---

# 4. Desktop Canvas

Canonical Desktop Canvas

Resolution

1920 × 1080

Safe Area

1800 px

Content Width

1440 px

Viewport Center

Always Centered

Không kéo giãn theo toàn bộ màn hình.

---

# 5. Master Layout Zones

Desktop chia thành 4 vùng chính.

```
┌──────────────────────────────────────────────────────────────┐
│                         HEADER                               │
├──────────────┬───────────────────────────────────────────────┤
│              │                                               │
│   SIDEBAR    │               CONTENT                         │
│              │                                               │
│              │                                               │
│              │                                               │
│              │                                               │
│              │                                               │
├──────────────┴───────────────────────────────────────────────┤
│                         FOOTER                               │
└──────────────────────────────────────────────────────────────┘
```

Không thay đổi cấu trúc này.

---

# 6. Horizontal Grid

Desktop sử dụng 12 cột logic.

Không bắt buộc hiển thị.

```
|1|2|3|4|5|6|7|8|9|10|11|12|
```

Các Section có thể sử dụng:

- 12
- 6 + 6
- 4 + 4 + 4
- 3 + 3 + 3 + 3

Không chia cột tùy ý.

---

# 7. Vertical Rhythm

Toàn bộ Portal tuân theo Vertical Rhythm thống nhất.

Section

↓

Section Header

↓

Content

↓

Section

Khoảng cách phải tạo được nhịp đọc liên tục.

Không được để các Section "dính" nhau.

---

# 8. Content Container

Content luôn nằm trong một Container chính.

```
┌────────────────────────────────────┐
│                                    │
│            CONTENT                 │
│                                    │
└────────────────────────────────────┘
```

Không tạo nhiều Container cùng cấp.

---

# 9. Sidebar Grid

Sidebar là vùng điều hướng.

Không phải vùng hiển thị dữ liệu.

Sidebar luôn:

- cố định
- chiều rộng ổn định
- không co giãn theo nội dung

---

# 10. Header Grid

Header gồm ba vùng.

```
LOGO

↓

NAVIGATION

↓

USER AREA
```

Ba vùng này luôn cân bằng.

Không được để Navigation lấn User Area.

---

# 11. Content Flow

Content luôn đọc theo:

```
TOP

↓

LEFT

↓

RIGHT

↓

BOTTOM
```

Không tạo Zig-zag Layout.

Không tạo nhiều điểm bắt đầu.

---

# 12. Section Grid

Mỗi Section luôn gồm:

```
Section Header

↓

Primary Content

↓

Supporting Content

↓

Actions (nếu có)
```

Không đảo thứ tự.

---

# 13. Card Grid

Card là đơn vị cơ bản.

Card phải:

- cùng chiều cao trong cùng một hàng
- cùng khoảng cách
- cùng căn lề

Không Card nào được phá Grid.

---

# 14. Reading Columns

Portal ưu tiên:

1 cột đọc.

Grid nhiều cột chỉ dùng cho:

- Card
- Metric
- Overview
- Four Pillars

Không chia nhiều cột cho văn bản luận giải.

---

# 15. Grid Alignment

Mọi Component phải căn theo Grid.

Không căn theo cảm tính.

Các cạnh trái và phải phải tạo thành các đường thẳng liên tục.

---

# 16. White Space

Whitespace là một phần của Grid.

Không dùng Whitespace ngẫu nhiên.

Whitespace dùng để:

- phân tách
- dẫn mắt
- giảm tải nhận thức

---

# 17. Grid Scaling

Grid không thay đổi theo dữ liệu.

Nếu dữ liệu dài hơn:

- Component mở rộng theo chiều dọc.

Không mở rộng theo chiều ngang.

---

# 18. Anti-Patterns

Không:

✗ Card lệch Grid

✗ Sidebar co giãn

✗ Content Full Width

✗ Card Width ngẫu nhiên

✗ Section Width khác nhau

✗ Căn lề bằng mắt

✗ Layout không theo cột

---

# 19. Cursor Implementation Rules

Cursor phải:

- dựng Grid trước
- dựng Container sau
- dựng Component cuối

Không dựng Component trước khi có Grid.

Không hard-code vị trí.

Không căn bằng margin ngẫu nhiên.

---

# 20. Product Owner Review Checklist

Desktop Grid PASS khi:

□ Canvas đúng

□ Safe Area đúng

□ Content Width đúng

□ Sidebar đúng

□ Header đúng

□ Section thẳng hàng

□ Card đúng Grid

□ Reading Flow đúng

□ Không có Component phá Grid

---

# 21. Grid Freeze

MASTER_GRID sau khi Freeze sẽ trở thành:

Desktop Grid Canonical

Mọi UI của BTE Platform phải kế thừa Grid này.

Không được sửa nếu không có:

Grid Change Request.

---

# Appendix A — Grid Hierarchy

```
Canvas

↓

Safe Area

↓

Content Width

↓

12 Column Grid

↓

Section

↓

Container

↓

Component

↓

Element
```

Không được bỏ qua tầng nào.

---

# Appendix B — Grid Priority

| Priority | Layer |
|----------|-------|
| 1 | Canvas |
| 2 | Safe Area |
| 3 | Header |
| 4 | Sidebar |
| 5 | Content |
| 6 | Section |
| 7 | Container |
| 8 | Component |
| 9 | Element |

Component phải phục tùng Grid.

Không ngược lại.

---

# Appendix C — Golden Rule

Một giao diện BTE đạt chuẩn khi:

- Người dùng không nhận ra Grid.
- Nhưng mọi thành phần đều có cảm giác cân bằng, thống nhất và dễ đọc.

Nếu phải phá Grid để "đẹp hơn",

thì Grid đúng,

thiết kế sai.

---

Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | MASTER | Initial Master Grid |