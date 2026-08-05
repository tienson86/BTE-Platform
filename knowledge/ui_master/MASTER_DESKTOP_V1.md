# BTE Platform

# MASTER_DESKTOP_V1

---

Version

1.0.0

Status

MASTER

Module

UI_MASTER

Document

MASTER_DESKTOP_V1

Owner

Product Owner

Purpose

Canonical Desktop Portal Design

Single Source of Truth for all Desktop UI implementation.

---

# 1. Mission

MASTER_DESKTOP_V1 là giao diện Desktop chuẩn của toàn bộ BTE Platform.

Đây không phải Wireframe.

Không phải Blueprint.

Không phải Prototype.

Đây là giao diện cuối cùng (Master UI) mà mọi lập trình viên và AI phải triển khai giống 100%.

Nếu có khác biệt giữa React và MASTER_DESKTOP_V1:

MASTER_DESKTOP_V1 luôn đúng.

---

# 2. Design Objective

Portal phải giúp người dùng hoàn thành hành trình sau trong lần xem đầu tiên.

```
Context

↓

Identity

↓

Condition

↓

Decision

↓

Evidence

↓

Interpretation

↓

Learning
```

Desktop Layout phải hỗ trợ hành trình này.

Không được hiển thị dữ liệu theo góc nhìn kỹ thuật.

---

# 3. Canonical Desktop Canvas

Reference Resolution

1920 × 1080

Working Width

1440 px

Centered Layout

YES

Sidebar

280 px

Content Width

1160 px

Header Height

72 px

Section Gap

48 px

Card Gap

24 px

Content Padding

32 px

---

# 4. Master Desktop Structure

```
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ Header                                                                             72 px   │
├──────────────┬─────────────────────────────────────────────────────────────────────────────┤
│              │                                                                             │
│              │ S00 Context Header                                                          │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S01 Identity & Decision Panel                                               │
│              │                                                                             │
│ Sidebar      │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S02 Overview & Quick Actions                                                │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S03 Four Pillars                                                            │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S04 Element Balance                                                         │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S05 Strength Analysis                                                       │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S06 Ten Gods                                                                │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S07 ShenSha                                                                 │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ S08 Interpretation                                                          │
│              │                                                                             │
│              │─────────────────────────────────────────────────────────────────────────────│
│              │                                                                             │
│              │ Learning Panel                                                              │
│              │                                                                             │
└──────────────┴─────────────────────────────────────────────────────────────────────────────┘
```

Đây là bố cục Desktop chuẩn.

Không thay đổi.

---

# 5. Reading Flow

Desktop phải tạo được luồng đọc tự nhiên.

```
Header

↓

Context

↓

Identity

↓

Condition

↓

Decision

↓

Overview

↓

Structure

↓

Balance

↓

Strength

↓

Supporting Evidence

↓

Interpretation

↓

Learning
```

Không có nhiều điểm bắt đầu.

Không có nhiều Hero.

---

# 6. First Viewport

Ngay sau khi mở Portal.

Người dùng chỉ nhìn thấy:

```
Header

↓

S00

↓

S01
```

S02 chỉ xuất hiện khi bắt đầu cuộn.

Mọi câu hỏi quan trọng phải được trả lời ngay trong First Viewport.

---

# 7. S00 Context Header

Vai trò

Xác nhận đúng hồ sơ.

Không phân tích.

Không luận giải.

Thông tin:

- Hồ sơ
- Giới tính
- Ngày giờ sinh
- Mã lá số
- Phiên bản
- Trạng thái
- Liên kết hồ sơ

Visual Weight

Medium

---

# 8. S01 Identity & Decision Panel

Đây là Hero duy nhất của Portal.

Bao gồm ba vùng.

```
Identity

↓

Condition

↓

Decision Support
```

Identity luôn lớn nhất.

Decision luôn nổi bật thứ hai.

Không thêm Hero khác.

---

# 9. S02 Overview

Hiển thị:

- thông tin tổng quan
- hành động nhanh
- xuất báo cáo

Không lặp lại S01.

---

# 10. S03 Four Pillars

Desktop

```
Year

Month

Day

Hour
```

Bốn Pillar ngang hàng.

Day Pillar luôn nổi bật.

Không thay đổi thứ tự.

---

# 11. S04 Element Balance

Desktop

```
Element Distribution

|

Summary
```

Hai vùng cân bằng.

Không xếp dọc.

---

# 12. S05 Strength

Desktop

```
Strength Score

|

Evidence

|

Recommendation
```

Recommendation luôn nằm sau Evidence.

Không đảo thứ tự.

---

# 13. S06 Ten Gods

Grid.

Mỗi God là một Card.

Không List.

Không Table.

---

# 14. S07 ShenSha

Grid theo nhóm.

Không hiển thị một danh sách dài.

Thông tin phụ luôn đứng sau Ten Gods.

---

# 15. S08 Interpretation

Đây là vùng đọc dài.

Một cột.

Chiều rộng tối ưu cho đọc.

Không chia nhiều cột.

Không tạo Card nhỏ.

---

# 16. Learning Panel

Không nằm trong Reading Flow chính.

Được mở khi cần.

Có thể:

Drawer

Accordion

Panel

Nhưng luôn đứng cuối Portal.

---

# 17. Visual Hierarchy

```
S01

★★★★★

↓

S03

★★★★☆

↓

S04

★★★★☆

↓

S05

★★★★☆

↓

S08

★★★★☆

↓

S00

★★★☆☆

↓

S02

★★★☆☆

↓

S06

★★★☆☆

↓

S07

★★☆☆☆

↓

Learning

★★☆☆☆
```

Không Section nào vượt S01.

---

# 18. Cursor Implementation Contract

Cursor phải:

Rebuild the Desktop UI from scratch.

Reference:

CANONICAL_PORTAL_UI.png

MASTER_DESKTOP_V1.md

Không được:

- cải tiến
- diễn giải
- thay đổi tỷ lệ
- thay đổi Layout
- thay đổi Hierarchy
- thay đổi Grid

Nếu khác Master Desktop:

Master Desktop luôn đúng.

---

# 19. Product Owner Review

Desktop PASS khi:

□ Header đúng

□ Sidebar đúng

□ S00 đúng

□ S01 đúng

□ S02 đúng

□ S03 đúng

□ S04 đúng

□ S05 đúng

□ S06 đúng

□ S07 đúng

□ S08 đúng

□ Learning đúng

□ Reading Flow đúng

□ Decision Flow đúng

□ Visual Hierarchy đúng

□ Không còn dấu vết Legacy UI

---

# 20. Desktop Freeze

Sau khi Product Owner APPROVED.

MASTER_DESKTOP_V1 trở thành:

Desktop Canonical UI.

Từ thời điểm này.

Cursor chỉ được:

Implement.

Không được:

Design.

---

# 21. Master Design Charter

MASTER_DESKTOP_V1 là tài sản thiết kế quan trọng nhất của BTE Platform.

Nó là chuẩn để:

- React
- Vue
- Flutter
- Mobile Web
- PDF Report
- AI Generated UI

đều phải tuân thủ.

Framework có thể thay đổi.

Component Library có thể thay đổi.

Tailwind có thể thay đổi.

Nhưng MASTER_DESKTOP_V1 luôn là giao diện chuẩn của BTE Platform.

---

# Appendix A — Master Design Workflow

```
Business Requirement

↓

Information Architecture

↓

Screen Blueprint

↓

Component Pattern

↓

Responsive Rules

↓

MASTER_DESKTOP_V1

↓

React Implementation

↓

Screenshot Review

↓

Freeze

↓

Release
```

MASTER_DESKTOP_V1 là cầu nối giữa Design và Code.

---

# Appendix B — Canonical Design Rules

1. Một Portal chỉ có một Hero.
2. Một Section chỉ có một mục tiêu.
3. Reading Flow không thay đổi.
4. Decision Flow không thay đổi.
5. Grid không thay đổi.
6. Layout không thay đổi.
7. Component không tự phát sinh.
8. Không triển khai từ Legacy UI.
9. Chỉ triển khai từ Master UI.
10. Master UI luôn có độ ưu tiên cao nhất.

---

# Appendix C — Golden Rule

Nếu ảnh React khác với:

CANONICAL_PORTAL_UI.png

hoặc

MASTER_DESKTOP_V1

thì React sai.

Không sửa Master.

Sửa React.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | MASTER | Initial Canonical Desktop Master |