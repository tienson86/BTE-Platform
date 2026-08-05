# BTE Platform

# MASTER_LAYOUT

---

Version

1.0.0

Status

MASTER

Module

UI_MASTER

Document

MASTER_LAYOUT

Owner

Product Owner

---

# 1. Purpose

MASTER_LAYOUT định nghĩa bố cục (Layout) chuẩn của toàn bộ BTE Portal Desktop.

Đây là tài liệu quan trọng nhất của Master UI.

Nó quyết định:

- bố cục tổng thể
- vị trí từng Section
- quan hệ giữa các vùng
- hướng đọc
- nhịp điều hướng

MASTER_LAYOUT là nguồn sự thật duy nhất cho toàn bộ Desktop Portal.

---

# 2. Design Goal

Portal phải trả lời câu hỏi của người dùng theo đúng thứ tự:

Tôi là ai?

↓

Lá số của tôi thế nào?

↓

Điều gì quan trọng nhất?

↓

Tại sao?

↓

Tôi nên làm gì?

↓

Muốn học thêm ở đâu?

Layout phải phục vụ hành trình này.

Không phục vụ việc trình diễn dữ liệu.

---

# 3. Canonical Portal Structure

```
Header

↓

Sidebar + TOC

↓

S00 Context Header

↓

S01 Identity & Decision

↓

S02 Overview

↓

S03 Four Pillars

↓

S04 Element Balance

↓

S05 Strength

↓

S06 Ten Gods

↓

S07 ShenSha

↓

S08 Interpretation

↓

Learning Panel

↓

Footer
```

Thứ tự này là bất biến.

---

# 4. Desktop Master Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Header                                                             72 px   │
├──────────────┬─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S00 Context Header                                          │
│              │                                                             │
│ Sidebar      ├─────────────────────────────────────────────────────────────┤
│ 280 px       │                                                             │
│              │ S01 Identity & Decision                                     │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S02 Overview                                                │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S03 Four Pillars                                            │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S04 Element Balance                                         │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S05 Strength                                                │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S06 Ten Gods                                                │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S07 ShenSha                                                 │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ S08 Interpretation                                          │
│              │                                                             │
│              ├─────────────────────────────────────────────────────────────┤
│              │                                                             │
│              │ Learning Panel                                              │
│              │                                                             │
└──────────────┴─────────────────────────────────────────────────────────────┘
```

---

# 5. Header Layout

Header luôn chia thành ba vùng.

```
LOGO

Navigation

User Area
```

Không được thay đổi.

Navigation luôn nằm giữa.

User Area luôn nằm bên phải.

---

# 6. Sidebar Layout

Sidebar là vùng điều hướng.

Không phải vùng hiển thị dữ liệu.

Sidebar luôn gồm:

```
Title

↓

Navigation Tree

↓

Utility

↓

Version
```

Sidebar luôn cố định.

---

# 7. Main Content Layout

Main Content luôn gồm:

```
Section Header

↓

Section Body

↓

Section Footer (nếu có)
```

Không có Section nào được thiếu Header.

---

# 8. S00 Context Header

Luôn nằm đầu tiên.

Không có Hero.

Không có Decision.

Không có Interpretation.

Chỉ hiển thị:

- Hồ sơ
- Mã lá số
- Thời gian sinh
- Phiên bản
- Trạng thái
- Liên kết hồ sơ

---

# 9. S01 Identity & Decision

Là Hero thực sự của Portal.

Desktop luôn gồm ba vùng:

```
Identity

↓

Condition

↓

Decision Support
```

Identity luôn lớn nhất.

Decision luôn dễ nhìn thứ hai.

---

# 10. S02 Overview

Mục tiêu:

Xác nhận tổng quan lá số.

Không luận giải.

Không phân tích sâu.

---

# 11. S03 Four Pillars

Desktop:

4 Card ngang.

```
Year

Month

Day

Hour
```

Day luôn nổi bật nhất.

---

# 12. S04 Element Balance

Desktop:

```
Chart

|

Summary
```

Song song.

Không Stack.

---

# 13. S05 Strength

Desktop:

```
Strength

|

Evidence
```

Song song.

Evidence luôn ở bên phải.

---

# 14. S06 Ten Gods

Desktop:

Grid.

Không List.

Không Accordion.

---

# 15. S07 ShenSha

Desktop:

Grid hoặc Category.

Không dùng Table.

Không dùng List dài.

---

# 16. S08 Interpretation

Desktop:

Một cột đọc.

Không chia nhiều cột.

Không dùng Card nhỏ.

Đây là khu vực đọc dài.

---

# 17. Learning Panel

Learning luôn ở cuối.

Không xuất hiện giữa Portal.

Có thể mở bằng:

Drawer

hoặc

Accordion.

Không phải một Hero mới.

---

# 18. Layout Hierarchy

Portal luôn đọc theo:

```
Header

↓

Navigation

↓

Context

↓

Identity

↓

Decision

↓

Evidence

↓

Interpretation

↓

Learning
```

Không được đảo.

---

# 19. Visual Weight

Desktop phân bổ trọng lượng:

| Layer | Weight |
|--------|--------|
| Header | Low |
| Sidebar | Medium |
| S00 | High |
| S01 | Highest |
| S02 | Medium |
| S03 | High |
| S04 | High |
| S05 | High |
| S06 | Medium |
| S07 | Medium |
| S08 | High |
| Learning | Low |

Không có Section nào vượt S01.

---

# 20. Cursor Rules

Cursor phải:

- dựng đúng Master Layout.
- không tự đổi thứ tự.
- không tự gộp Section.
- không chia Section.
- không tạo Layout mới.

Nếu Master Layout và Code khác nhau:

Master Layout luôn đúng.

---

# 21. Product Owner Checklist

□ Header đúng.

□ Sidebar đúng.

□ S00 đúng.

□ S01 đúng.

□ S02 đúng.

□ S03 đúng.

□ S04 đúng.

□ S05 đúng.

□ S06 đúng.

□ S07 đúng.

□ S08 đúng.

□ Learning đúng.

□ Reading Flow đúng.

□ Decision Flow đúng.

□ Không có Legacy Layout.

PASS khi toàn bộ đạt yêu cầu.

---

# Appendix A — Layout Dependency

```
Business

↓

Reading Flow

↓

Decision Flow

↓

Master Grid

↓

Master Layout

↓

Component Tree

↓

React
```

Không được đảo thứ tự.

---

# Appendix B — Section Responsibility

| Section | Responsibility |
|----------|----------------|
| S00 | Context |
| S01 | Identity + Decision |
| S02 | Overview |
| S03 | Structure |
| S04 | Balance |
| S05 | Strength |
| S06 | Relationships |
| S07 | Auxiliary Signals |
| S08 | Interpretation |
| Learning | Knowledge |

Mỗi Section chỉ có một trách nhiệm chính.

---

# Appendix C — Golden Layout Principles

MASTER_LAYOUT của BTE Platform tuân thủ 10 nguyên tắc:

1. Context trước Identity.
2. Identity trước Analysis.
3. Decision trước Evidence.
4. Evidence trước Interpretation.
5. Interpretation trước Learning.
6. Một Section — Một mục tiêu.
7. Không đảo Reading Flow.
8. Không chèn Hero mới.
9. Không phá Grid.
10. Layout phục vụ Business, không phục vụ hiệu ứng.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | MASTER | Initial Master Layout |