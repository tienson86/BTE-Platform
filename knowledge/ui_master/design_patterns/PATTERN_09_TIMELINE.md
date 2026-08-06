# BTE Platform

# PATTERN_09 — TIMELINE

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

09

Name

Timeline

Type

Foundation Pattern

---

# 1. Mục đích

Timeline là Pattern tiêu chuẩn dùng để trực quan hóa các sự kiện, trạng thái hoặc giai đoạn theo trình tự thời gian.

Pattern này giúp người dùng trả lời nhanh các câu hỏi:

• Điều gì xảy ra trước?

• Điều gì đang diễn ra?

• Điều gì sẽ xảy ra tiếp theo?

Timeline không nhằm phân tích.

Timeline chỉ trình bày diễn tiến theo thời gian.

---

# 2. Triết lý

Time First.

Details Later.

Người dùng phải hiểu được diễn tiến theo thời gian trước khi đọc từng sự kiện.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Đại vận

• Lưu niên

• Lưu nguyệt

• Chu kỳ vận hạn

• Lịch sử luận giải

• Tiến trình AI

• Nhật ký phân tích

• Workflow hệ thống

---

# 4. Không sử dụng

Không dùng cho:

✗ Dashboard

✗ Data Table

✗ KPI

✗ Pie Chart

✗ Comparison

✗ Decision Card

---

# 5. Reading Flow

```
Timeline

↓

Current Point

↓

Past

↓

Future

↓

Details
```

Người dùng luôn phải xác định được:

Hiện tại đang ở đâu.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────────────────┐

ĐẠI VẬN

──────────────────────────────────────────────────────────

○ 1995 — 2004

Ất Hợi

────────────────────────────

● 2005 — 2014

Bính Tý

(Hiện tại)

────────────────────────────

○ 2015 — 2024

Đinh Sửu

────────────────────────────

○ 2025 — 2034

Mậu Dần

└──────────────────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
Timeline

├── Header
│
├── TimelineTrack
│
│   ├── TimelineItem
│   ├── TimelineItem
│   ├── TimelineItem
│   └── TimelineItem
│
└── Footer
```

---

# 8. Timeline Item

Mỗi Item gồm:

```
Marker

↓

Time Range

↓

Title

↓

Optional Status
```

Không thêm Paragraph.

---

# 9. Marker

Chỉ dùng:

○

●

✓

Không dùng:

Emoji

3D Icon

Illustration

---

# 10. Current Position

Chỉ có duy nhất

01

Current Item.

Hiển thị:

●

Màu đỏ BTE.

Label

"Hiện tại"

Không Highlight nhiều hơn một Item.

---

# 11. Time Range

Ví dụ

```
2025 — 2034
```

Font

14 px

600

---

# 12. Title

Ví dụ

```
Mậu Dần

Đại vận 6
```

Font

15 px

600

---

# 13. Optional Status

Ví dụ

```
Đang diễn ra

Đã kết thúc

Sắp bắt đầu
```

Font

13 px

500

Không bắt buộc.

---

# 14. Timeline Direction

Desktop

Vertical

Tablet

Vertical

Mobile

Vertical

Không dùng Timeline ngang.

---

# 15. Information Hierarchy

★★★★★

Current Item

★★★★☆

Time Range

★★★★☆

Title

★★★☆☆

Status

---

# 16. White Space

Padding

20 px

Item Gap

16 px

Header Bottom

20 px

Không để Item dính nhau.

---

# 17. Card Style

Background

White

Radius

12 px

Border

1 px

Soft Shadow

Theo Enterprise Design System.

---

# 18. Accessibility

Current Item luôn có text.

Không chỉ dùng màu.

Keyboard Focus.

Contrast đạt WCAG AA.

---

# 19. Responsive

Desktop

Vertical Timeline

Tablet

Vertical Timeline

Mobile

Vertical Timeline

Không đổi Reading Flow.

---

# 20. Những điều KHÔNG được phép

Không sử dụng:

✗ Horizontal Timeline

✗ Animation

✗ Gradient

✗ Glass

✗ Timeline 3D

✗ Carousel

✗ Auto Scroll

---

# 21. Các màn hình sử dụng

Có thể áp dụng cho:

✓ Đại vận

✓ Lưu niên

✓ Lưu nguyệt

✓ Chu kỳ vận hạn

✓ AI Process

✓ Analysis History

✓ Workflow

---

# 22. Design Principles

Chronology

>

Decoration

Current State

>

Past

Clarity

>

Density

Scanning

>

Reading

---

# 23. Reusability

Timeline phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

Desktop

Tablet

Mobile

Chỉ thay đổi dữ liệu.

Không thay đổi cấu trúc.

---

# 24. Acceptance Criteria

PASS khi:

✓ Người dùng xác định được Current Item trong dưới 3 giây.

✓ Timeline đọc theo thứ tự tự nhiên.

✓ Không có hơn một Current Item.

✓ Timeline mở rộng được.

✓ Không cần cuộn ngang.

---

# 25. Design Decision Record

Timeline của BTE sử dụng **Vertical Timeline** làm chuẩn.

Không sử dụng Horizontal Timeline vì:

• Dễ đọc hơn trên mọi thiết bị.

• Mở rộng không giới hạn.

• Phù hợp với dữ liệu Đại vận và Lưu niên.

• Không cần xử lý cuộn ngang.

Đây là quyết định chính thức của Design System.

---

# 26. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|----------|---------|
| Đại vận | ⭐⭐⭐⭐⭐ |
| Lưu niên | ⭐⭐⭐⭐⭐ |
| Lưu nguyệt | ⭐⭐⭐⭐ |
| Vận trình cuộc đời | ⭐⭐⭐⭐⭐ |
| AI Workflow | ⭐⭐⭐ |
| Analysis History | ⭐⭐⭐⭐ |

---

# 27. Evolution Policy

Timeline là Foundation Pattern.

Có thể thay đổi:

- Responsive spacing

- Typography responsive

Không được thay đổi:

- Vertical Layout

- Current Item Rule

- Reading Flow

- Component Tree

---

# 28. Relationship với các Pattern khác

Timeline thường kết hợp với:

PATTERN_07 — Status Panel

↓

Hiển thị trạng thái hiện tại.

PATTERN_05 — Decision Card

↓

Đưa ra kết luận của từng giai đoạn.

PATTERN_06 — Information List

↓

Liệt kê các sự kiện hoặc đặc điểm của từng mốc thời gian.

Timeline chịu trách nhiệm tổ chức thông tin theo trục thời gian, trong khi các Pattern khác trình bày nội dung của từng mốc.

---

# 29. Future Extensions

Timeline có thể mở rộng:

• Bộ lọc theo năm.

• Thu gọn / mở rộng từng giai đoạn.

• Hiển thị mốc quan trọng.

• Liên kết đến báo cáo chi tiết.

Các mở rộng này không được làm thay đổi cấu trúc Timeline chuẩn.

---

# 30. Freeze Statement

PATTERN_09_TIMELINE.md là tài liệu chuẩn duy nhất mô tả Timeline của BTE Platform.

Mọi màn hình sử dụng Timeline phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**PATTERN_09_TIMELINE.md là Single Source of Truth.**