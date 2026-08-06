# BTE Platform

# PATTERN_01 — IDENTITY CARD

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

01

Name

Identity Card

Type

Foundation Pattern

---

# 1. Mục đích

Identity Card là Pattern tiêu chuẩn dùng để hiển thị thông tin nhận diện của một thực thể (Entity) trong hệ thống BTE.

Đây là Pattern đầu tiên của toàn bộ Design System.

Pattern này được sử dụng khi mục tiêu chính là giúp người dùng nhận biết nhanh "đối tượng đang được xem".

Không dùng để trình bày phân tích.

Không dùng để hiển thị báo cáo.

Không dùng để hiển thị Dashboard.

---

# 2. Triết lý

Identity trước.

Analysis sau.

Người dùng luôn phải biết:

"Tôi đang xem ai?"

trước khi xem:

"Kết quả phân tích là gì?"

---

# 3. Khi nào sử dụng

Sử dụng Pattern này khi hiển thị:

• Hồ sơ lá số

• Hồ sơ khách hàng

• Hồ sơ thành viên

• Hồ sơ tài khoản

• Hồ sơ chuyên gia

• Hồ sơ doanh nghiệp

• Hồ sơ dự án

---

# 4. Không sử dụng

Không dùng cho:

✗ KPI

✗ Dashboard

✗ Analytics

✗ Report

✗ Statistics

✗ Progress

✗ Decision Card

---

# 5. Reading Flow

```
Avatar

↓

Tên

↓

Thông tin cơ bản

↓

Metadata

↓

Quick Action
```

Người dùng phải đọc theo đúng thứ tự này.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

○ Avatar

Nguyễn Văn A

Nam • Dương Nam

──────────────────────────────────────────────

Ngày sinh

Giờ sinh

Mã lá số

Phiên bản

Trạng thái

──────────────────────────────────────────────

Xem hồ sơ →

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
IdentityCard

├── Avatar

├── Primary Information
│
│ ├── Full Name
│ ├── Gender
│ └── Additional Info
│
├── Metadata
│
│ ├── Birth Date
│ ├── Birth Time
│ ├── Chart ID
│ ├── Version
│ └── Status
│
└── Action Link
```

---

# 8. Information Hierarchy

Ưu tiên hiển thị:

★★★★★

Tên

★★★★☆

Avatar

★★★★☆

Metadata

★★★☆☆

Action

Không đảo thứ tự.

---

# 9. Avatar

Hình tròn.

48 px.

Có viền mảnh.

Không Shadow.

Không hiệu ứng.

Nếu không có ảnh:

Hiển thị Avatar mặc định.

---

# 10. Full Name

Font

24 px

Weight

700

Là thành phần nổi bật nhất.

---

# 11. Secondary Information

Ví dụ:

```
Nam

Dương Nam
```

Font

14 px

Weight

400

Màu trung tính.

---

# 12. Metadata

Metadata hiển thị theo cột.

Ví dụ:

Ngày sinh

Giờ sinh

Mã lá số

Phiên bản

Trạng thái

Không hiển thị theo đoạn văn.

---

# 13. Status

Luôn dùng Pill.

Ví dụ:

```
Hoàn tất
```

Màu Semantic.

Không dùng Badge vuông.

---

# 14. Quick Action

Ví dụ

```
Xem hồ sơ →
```

Là Link.

Không phải Button.

---

# 15. White Space

Padding

20 px

Khoảng cách giữa Block

16 px

Khoảng cách Metadata

20 px

Ưu tiên khoảng trắng.

---

# 16. Typography

Tên

24 px

700

Thông tin phụ

14 px

400

Metadata Label

12 px

500

Metadata Value

15 px

600

Action

14 px

600

---

# 17. Color

Background

White

Border

1 px

Shadow

Soft

Không Gradient.

Không Glass.

---

# 18. Accessibility

Contrast đạt WCAG AA.

Avatar có alt text.

Status có aria-label.

Action keyboard focus.

---

# 19. Responsive

Desktop

Horizontal Layout

Tablet

Compact Horizontal

Mobile

Vertical Stack

Không thay đổi Reading Flow.

---

# 20. Những điều KHÔNG được phép

Không dùng:

✗ KPI

✗ Progress Bar

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Animation

✗ Gradient

✗ Glass Effect

---

# 21. Các màn hình sử dụng

Đã áp dụng:

✓ S00 — Thông tin bối cảnh

Có thể tái sử dụng:

✓ Hồ sơ khách hàng

✓ Hồ sơ chuyên gia

✓ Hồ sơ tài khoản

✓ Hồ sơ nhân viên

✓ Hồ sơ doanh nghiệp

---

# 22. Design Principles

Identity

>

Decoration

Information

>

Effects

Reading Speed

>

Visual Complexity

Consistency

>

Creativity

---

# 23. Reusability

Pattern này phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

CRM

Mobile App

Desktop App

Không tạo biến thể mới nếu không thực sự cần thiết.

---

# 24. Freeze Statement

PATTERN_01_IDENTITY_CARD.md là tài liệu chuẩn duy nhất mô tả Identity Card của BTE Platform.

Mọi màn hình sử dụng Identity Card phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

PATTERN_01_IDENTITY_CARD.md là Single Source of Truth.