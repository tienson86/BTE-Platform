# BTE Platform

# S02 Blueprint — Overview & Actions

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Screen

BaZi Result

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_SCREEN_SPECIFICATIONS.md

---

# 1. Purpose

S02 là lớp Overview & Actions của Portal.

Sau khi người dùng đã hiểu:

- Tôi là ai (S01)
- Tôi đang ở trạng thái nào (S01)

S02 cung cấp:

- bối cảnh của phiên phân tích
- các hành động có thể thực hiện
- điều hướng tới các phần phân tích

S02 không được lặp lại Identity hoặc Decision.

---

# 2. Business Goal

S02 giúp người dùng:

- xác nhận đây là đúng kết quả đang làm việc
- thực hiện các thao tác với kết quả
- chuyển nhanh đến các phần cần xem

S02 không tạo ra kết luận mới.

---

# 3. User Questions

S02 phải trả lời:

✓ Đây là phiên phân tích nào?

✓ Tôi có thể làm gì với kết quả này?

✓ Tôi nên đi đâu tiếp theo?

✓ Có những phần phân tích nào?

---

# 4. Decision Goal

Sau khi xem S02 người dùng phải quyết định:

- Xuất báo cáo
- Chia sẻ
- In
- Phân tích lại
- Điều hướng tới một Section cụ thể

Không đưa ra quyết định nghiệp vụ mới.

---

# 5. Reading Goal

≤10 giây.

Reading Flow

```
Overview

↓

Actions

↓

Section Navigation

↓

Continue Reading
```

Không được chen dữ liệu Bát Tự.

---

# 6. Information Architecture

## Zone A — Analysis Overview

Hiển thị:

- Tên phiên phân tích
- Ngày phân tích
- Phiên bản Engine
- Trạng thái
- Người tạo (nếu có)

---

## Zone B — Quick Actions

Cho phép:

- Xuất PDF
- In
- Chia sẻ
- Sao chép liên kết
- Phân tích lại

---

## Zone C — Section Navigation

Danh sách Section:

- Four Pillars
- Element Balance
- Strength
- Ten Gods
- ShenSha
- Interpretation

Có thể sử dụng TOC hoặc Navigation Card.

---

## Zone D — Analysis Metadata

Thông tin phụ:

- Analysis ID
- Engine Version
- Dataset Version
- Knowledge Version

Đặt cuối cùng.

---

# 7. Visual Hierarchy

Visual Priority

```
Overview

↓

Quick Actions

↓

Section Navigation

↓

Metadata
```

Quick Actions phải dễ thấy nhưng không cạnh tranh với Hero của S01.

---

# 8. Layout Blueprint

Desktop

```
+-----------------------------------------------------------+

Analysis Overview

------------------------------------------------------------

Quick Actions

------------------------------------------------------------

Section Navigation

------------------------------------------------------------

Metadata

+-----------------------------------------------------------+
```

Tablet

Overview

↓

Actions

↓

Navigation

↓

Metadata

Mobile

Stack hoàn toàn.

---

# 9. Component Composition

Cho phép:

- Section Header
- Button
- Icon Button
- Badge
- Chip
- Breadcrumb
- TOC
- Divider

Không cho phép:

- Hero
- Progress Chart
- Four Pillars
- Score Card
- Long Text

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Analysis Name | Analysis.Name |
| Analysis Date | Analysis.GeneratedAt |
| Engine Version | Analysis.EngineVersion |
| Dataset Version | Analysis.DatasetVersion |
| Knowledge Version | Analysis.KnowledgeVersion |
| Status | Analysis.Status |
| Analysis ID | Analysis.Id |

Actions chỉ gọi API tương ứng.

Không xử lý nghiệp vụ.

---

# 11. Typography Rules

Overview

→ HeadingPrimary

Action Labels

→ BodyPrimary

Navigation

→ BodyPrimary

Metadata

→ Caption

Không sử dụng Display Typography.

---

# 12. Interaction Rules

Cho phép:

- Xuất PDF
- In
- Chia sẻ
- Sao chép Link
- Điều hướng Section
- Quay Dashboard

Không:

- Chỉnh dữ liệu
- Chỉnh kết luận
- Chỉnh hồ sơ

---

# 13. Responsive Behaviour

Desktop

4 vùng ngang.

Tablet

Stack.

Mobile

Stack.

TOC có thể chuyển thành Drawer.

Reading Flow giữ nguyên.

---

# 14. Accessibility

- Keyboard navigation.
- Focus theo Reading Flow.
- Icon luôn có Label.
- Action có Tooltip.
- Semantic Navigation.

---

# 15. Anti-Patterns

Không được:

❌ Hiển thị Nhật Chủ.

❌ Hiển thị Thân.

❌ Hiển thị Dụng Thần.

❌ Lặp Hero.

❌ Lặp Summary.

❌ Đưa Four Pillars vào S02.

❌ Action nhiều hơn 6.

❌ Metadata nổi hơn Navigation.

---

# 16. Screenshot Acceptance

Cursor phải gửi:

1. Desktop Full

2. Desktop Zoom (S02)

3. Tablet

4. Mobile

5. Action States

6. Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- thiết kế Hero mới
- thêm Card phân tích
- đổi Reading Flow
- thêm Component ngoài Blueprint

Nếu Action chưa hoạt động:

Hiển thị Disabled.

Không ẩn.

---

# 18. Product Owner Review Checklist

Business

□ Đúng vai trò Workspace.

Decision

□ Thực hiện được Action.

Reading

□ Không lặp S01.

Hierarchy

□ Navigation rõ.

Responsive

□ Desktop
□ Tablet
□ Mobile

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Overview Clarity | 20 |
| Action Discoverability | 20 |
| Navigation Clarity | 20 |
| Reading Flow | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S02 nhận đầu vào từ:

S01 Identity & Decision Panel.

S02 điều hướng người dùng tới:

- S03 Four Pillars
- S04 Element Balance
- S05 Strength
- S06 Ten Gods
- S07 ShenSha
- S08 Interpretation

S02 không được thay thế vai trò của TOC toàn cục.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Overview & Actions Blueprint |

bổ sung 5 phụ lục cho S02
Để Cursor triển khai đúng ngay từ đầu, mình đề xuất bổ sung thêm các phụ lục sau.
Appendix A – Workspace Information Priority
Thành phần	Priority
Overview	10
Quick Actions	9
Section Navigation	8
Metadata	4


Appendix B – Workspace Wireframe
┌──────────────────────────────────────────────────────────┐
│ Overview: Phiên phân tích Bát Tự V1.0                    │
│ Engine v1.0 • Dataset v1.0 • Hoàn thành                  │
├──────────────────────────────────────────────────────────┤
│ [PDF] [Print] [Share] [Copy Link] [Re-analyze]           │
├──────────────────────────────────────────────────────────┤
│ Four Pillars | Elements | Strength | Ten Gods | ...      │
├──────────────────────────────────────────────────────────┤
│ Analysis ID • Knowledge Version • Dataset Version        │
└──────────────────────────────────────────────────────────┘
Appendix C – Action Priority
Thứ tự ưu tiên thao tác:
Xuất PDF
Chia sẻ
In
Điều hướng Section
Phân tích lại
Sao chép liên kết
Không đảo thứ tự nếu không có yêu cầu nghiệp vụ.
Appendix D – Navigation Rules
Chỉ điều hướng đến các section S03–S08.
Không điều hướng ngược lên S00 hoặc S01 bằng TOC cục bộ.
Section hiện tại phải được đánh dấu rõ ràng.
Điều hướng không làm mất trạng thái đọc.
Appendix E – Common Mistakes
Những lỗi cần tránh khi triển khai S02:
Biến S02 thành Hero thứ hai.
Lặp lại toàn bộ nội dung của S01.
Đưa quá nhiều nút hành động gây rối.
Trộn Metadata với Quick Actions.
Hiển thị điều hướng như một Dashboard widget thay vì một Workspace Header.
Mình cũng đề xuất một nguyên tắc sẽ áp dụng cho tất cả các Blueprint từ S03 đến S08:
Mỗi section chỉ được trả lời một nhóm câu hỏi nghiệp vụ duy nhất.

Điều này sẽ giữ cho Reading Flow luôn rõ ràng, tránh việc các section chồng chéo nội dung và giúp Cursor triển khai giao diện đúng theo kiến trúc mà chúng ta đã xây dựng.