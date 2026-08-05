# BTE Platform

# Responsive Pattern — Screen Rules

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

04_RESPONSIVE_SCREEN_RULES

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa hành vi Responsive của từng Screen trong BTE Platform.

Screen Rules kế thừa:

- Breakpoint System
- Responsive Layout Rules
- Responsive Component Rules

Screen Rules không thay đổi:

- Business Flow
- Reading Flow
- Decision Flow

Screen chỉ thay đổi cách sắp xếp Component.

---

# 2. Design Philosophy

Mỗi Screen chỉ có một Business Goal.

Responsive không được làm thay đổi Business Goal đó.

Desktop

↓

Tablet

↓

Mobile

chỉ thay đổi bố cục hiển thị.

Không thay đổi trải nghiệm cốt lõi.

---

# 3. Canonical Screen Order

Thứ tự Screen luôn là:

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

Không được đảo thứ tự.

---

# 4. S00 Context Header

Desktop

Hiển thị đầy đủ Context Strip.

Tablet

Giữ nguyên.

Một số Metadata có thể xuống dòng.

Mobile

Stack theo chiều dọc.

Thông tin bắt buộc:

- Hồ sơ
- Mã lá số
- Ngày sinh
- Trạng thái

Không được ẩn.

---

# 5. S01 Identity & Decision Panel

Desktop

Identity

+

Condition

+

Decision

hiển thị trên cùng viewport.

Tablet

Giữ nguyên Reading Flow.

Cho phép chia thành nhiều hàng.

Mobile

Stack hoàn toàn.

Identity luôn nằm đầu tiên.

Decision luôn nằm sau Condition.

---

# 6. S02 Overview

Desktop

Overview + Actions cùng hàng nếu đủ không gian.

Tablet

Overview trên.

Actions dưới.

Mobile

Vertical Stack.

Action Bar luôn nằm cuối Section.

---

# 7. S03 Four Pillars

Desktop

4 Pillars hiển thị một hàng.

Tablet

2 × 2.

Mobile

1 cột.

Không đổi thứ tự:

Year

↓

Month

↓

Day

↓

Hour

Day Pillar luôn nổi bật.

---

# 8. S04 Element Balance

Desktop

Chart + Summary song song.

Tablet

Chart trên.

Summary dưới.

Mobile

Vertical.

Không được bỏ Summary.

---

# 9. S05 Strength

Desktop

Metric + Evidence cùng màn hình.

Tablet

Stack.

Mobile

Metric trước.

Evidence sau.

Decision không được xuống dưới Evidence.

---

# 10. S06 Ten Gods

Desktop

Grid.

Tablet

2 cột.

Mobile

1 cột.

Accordion chỉ dùng cho nội dung mở rộng.

---

# 11. S07 ShenSha

Desktop

Grid hoặc List.

Tablet

List ưu tiên.

Mobile

List.

Không hiển thị quá nhiều Card trên Mobile.

---

# 12. S08 Interpretation

Desktop

Article Width.

Tablet

Article Width.

Mobile

Full Width.

Không chia nhiều cột.

Không chia đoạn quá nhỏ.

---

# 13. Learning Panel

Desktop

Right Drawer.

Tablet

Right Drawer.

Mobile

Bottom Sheet hoặc Full Height.

Không mở toàn màn hình trên Desktop.

---

# 14. Navigation Rules

Desktop

Top Navigation

+

TOC Sidebar.

Tablet

Top Navigation

+

Collapsed TOC.

Mobile

Top Navigation

+

Drawer TOC.

Navigation luôn truy cập được.

---

# 15. Section Visibility

Responsive không được:

- Ẩn Hero.
- Ẩn Decision.
- Ẩn Interpretation.

Cho phép:

Ẩn Metadata phụ.

Thu gọn nội dung mở rộng.

Chuyển Action vào Overflow.

---

# 16. Screenshot Requirements

Mỗi Screen phải có:

Desktop Full

Desktop Zoom

Tablet

Mobile

Loading (nếu có)

Empty (nếu có)

Error (nếu có)

Đây là tiêu chuẩn bắt buộc để Product Owner review.

---

# 17. Cursor Rules

Cursor không được:

- đổi thứ tự Screen.
- tự thêm Screen.
- tự gộp hai Screen.
- chia Screen thành nhiều trang.

Nếu Responsive chưa được mô tả:

STOP.

Không suy luận.

---

# 18. Product Owner Checklist

□ Reading Flow giữ nguyên.

□ Decision Flow giữ nguyên.

□ Hero đúng vị trí.

□ Four Pillars đúng thứ tự.

□ Action Bar đúng.

□ Navigation đúng.

□ Learning đúng.

□ Responsive nhất quán.

---

# 19. Relationship with Other Modules

Foundation

↓

Layout System

↓

Screen Blueprints

↓

Component Patterns

↓

Responsive Screen Rules

↓

React Implementation

Screen Rules là tầng cuối trước khi triển khai giao diện.

---

# 20. Definition of Done

Một Screen được coi là Responsive hoàn chỉnh khi:

✓ Desktop đạt yêu cầu.

✓ Tablet đạt yêu cầu.

✓ Mobile đạt yêu cầu.

✓ Reading Flow giữ nguyên.

✓ Business Goal không thay đổi.

✓ Screenshot được Product Owner phê duyệt.

✓ Được Freeze.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Screen Rules |

---

# Appendix A — Screen Responsive Matrix

| Screen | Desktop | Tablet | Mobile |
|---------|----------|---------|---------|
| S00 | Context Strip | Wrap | Stack |
| S01 | Horizontal | Mixed | Vertical |
| S02 | Split | Stack | Stack |
| S03 | 4 Columns | 2×2 | 1 Column |
| S04 | Split | Vertical | Vertical |
| S05 | Split | Stack | Stack |
| S06 | Grid | 2 Columns | List |
| S07 | Grid/List | List | List |
| S08 | Article | Article | Full Width |
| Learning | Drawer | Drawer | Bottom Sheet |

---

# Appendix B — Screen Priority

| Screen | Business Priority |
|----------|------------------|
| S01 | Critical |
| S05 | Critical |
| S03 | High |
| S04 | High |
| S08 | High |
| S00 | Medium |
| S02 | Medium |
| S06 | Medium |
| S07 | Medium |
| Learning | Low |

Business Priority không thay đổi theo Responsive.

---

# Appendix C — Responsive Principles

Responsive Screen chỉ được phép thay đổi:

- bố cục
- khoảng cách
- cách nhóm Component

Không được thay đổi:

- Information Hierarchy
- Reading Flow
- Business Meaning
- Decision Flow

Mục tiêu cuối cùng của Responsive là:

**Người dùng trên Desktop, Tablet và Mobile đều nhận được cùng một giá trị, chỉ khác cách trình bày.**