# BTE Platform

# S01 Blueprint — Identity & Decision Panel

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

S01 là trái tim của Portal BTE.

Đây là nơi hệ thống trả lời những câu hỏi quan trọng nhất trước khi người dùng đi vào chi tiết kỹ thuật.

Identity & Decision Panel không phải nơi trình bày dữ liệu.

Đây là nơi trình bày **kết luận cấp cao**.

---

# 2. Business Goal

Sau khi xem S01, người dùng phải hiểu ngay:

- Tôi là ai?
- Tôi mạnh hay yếu?
- Điều gì quan trọng nhất?
- Tôi nên chú ý điều gì tiếp theo?

Nếu người dùng phải kéo xuống S03 hoặc S04 mới trả lời được các câu hỏi này thì Blueprint thất bại.

---

# 3. User Questions

S01 phải trả lời đầy đủ bốn câu hỏi:

### Q1

Tôi là ai?

### Q2

Lá số của tôi đang ở trạng thái nào?

### Q3

Điều gì quan trọng nhất?

### Q4

Tôi nên đọc tiếp phần nào?

Đây là bốn câu hỏi bắt buộc.

---

# 4. Decision Goal

Người dùng phải hoàn thành một quyết định:

"Tôi đã hiểu bức tranh tổng thể."

Sau đó lựa chọn:

- Đọc sâu hơn.
- Xuất báo cáo.
- Chia sẻ kết quả.
- Quay lại Dashboard.

---

# 5. Reading Goal

Thời gian mục tiêu:

≤15 giây.

Reading Flow:

```
Identity

↓

Condition

↓

Decision

↓

Supporting Information

↓

Primary Action
```

Không được có hai điểm bắt đầu.

---

# 6. Information Architecture

## Zone A — Identity

Hiển thị:

- Nhật Chủ
- Ngũ Hành
- Âm Dương

Không hiển thị dữ liệu phụ.

---

## Zone B — Condition

Hiển thị:

- Thân Vượng / Thân Nhược
- Điểm đánh giá
- Độ tin cậy

---

## Zone C — Decision Support

Hiển thị:

### What

Điều quan trọng nhất.

### Why

Nguyên nhân ngắn gọn.

### Next

Bước nên đọc tiếp.

---

## Zone D — Supporting

Hiển thị:

- Cách Cục
- Dụng Thần
- Hỷ Thần
- Kỵ Thần

Dạng Chip hoặc Badge.

Không phải bảng.

---

## Zone E — Quick Actions

- Xuất PDF
- In
- Chia sẻ
- Phân tích lại

Nếu chưa khả dụng:

Hiển thị Disabled.

Không ẩn.

---

# 7. Visual Hierarchy

Thứ tự ưu tiên:

```
Nhật Chủ

↓

Thân

↓

Decision

↓

Dụng Thần

↓

Metadata

↓

Actions
```

Không có thành phần nào được vượt Nhật Chủ.

---

# 8. Layout Blueprint

Desktop

```
+-----------------------------------------------------------+

Identity

|

Condition

---------------------------

Decision Panel

---------------------------

Supporting Chips

---------------------------

Quick Actions

+-----------------------------------------------------------+
```

Tablet

Identity

↓

Condition

↓

Decision

↓

Supporting

↓

Actions

Mobile

Stack hoàn toàn.

Không chia hai cột.

---

# 9. Component Composition

Cho phép:

- Identity Hero
- Decision Panel
- Badge
- Chip
- Button
- Divider
- Confidence Badge

Không cho phép:

- Chart
- Table
- Timeline
- Accordion
- Long Paragraph

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Nhật Chủ | Chart.DayMaster |
| Ngũ Hành | Chart.DayMaster.Element |
| Âm Dương | Chart.DayMaster.YinYang |
| Thân | Analysis.Strength.Level |
| Điểm | Analysis.Strength.Score |
| Confidence | Analysis.Confidence |
| Dụng Thần | Analysis.UsefulGod |
| Hỷ Thần | Analysis.FavorableGod |
| Kỵ Thần | Analysis.UnfavorableGod |
| Cách Cục | Analysis.Pattern |
| Decision | Interpretation.ExecutiveSummary |

---

# 11. Typography Rules

Identity

→ Display

Condition

→ HeadingPrimary

Decision

→ HeadingPrimary

Supporting

→ Body

Metadata

→ Caption

---

# 12. Interaction Rules

Cho phép:

- Tooltip.
- Copy.
- Xuất PDF.
- Chia sẻ.
- Điều hướng đến Section liên quan.

Không:

- Chỉnh sửa dữ liệu.
- Sửa kết luận.
- Mở Dialog dài.

---

# 13. Responsive Behaviour

Desktop

8+4 Layout.

Tablet

Stack.

Mobile

Một cột.

Reading Flow không thay đổi.

---

# 14. Accessibility

- Hero đọc đầu tiên.
- Keyboard theo Reading Flow.
- Status có text.
- Tooltip truy cập bằng bàn phím.
- Semantic Heading.

---

# 15. Anti-Patterns

Không được:

❌ Hero chỉ là Card đẹp.

❌ Nhật Chủ quá nhỏ.

❌ Decision nằm dưới fold.

❌ Metadata nổi hơn Decision.

❌ Quick Action chiếm nhiều chú ý hơn kết luận.

❌ Quá nhiều Badge.

❌ Hiển thị Thập Thần tại S01.

❌ Đưa Four Pillars vào Hero.

---

# 16. Screenshot Acceptance

Cursor phải cung cấp:

1. Desktop Full

2. Desktop Zoom (S01)

3. Tablet

4. Mobile

5. Focus Map

6. Design Rationale

Không đủ bộ screenshot thì không review.

---

# 17. Cursor Implementation Rules

Cursor phải tuân thủ Blueprint tuyệt đối.

Không được:

- đổi thứ tự Zone
- thêm Card mới
- sáng tạo Hero
- thêm Chart
- thêm hiệu ứng không có trong Blueprint

Nếu dữ liệu chưa có:

dùng Placeholder đúng cấu trúc.

Không tự nghĩ thêm nội dung.

---

# 18. Product Owner Review Checklist

Business

□ Trả lời đúng 4 câu hỏi.

Decision

□ Người dùng hiểu điều quan trọng nhất.

Reading

□ ≤15 giây.

Hierarchy

□ Identity nổi bật nhất.

Layout

□ Đúng Blueprint.

Responsive

□ Desktop
□ Tablet
□ Mobile

Visual

□ Không giống Dashboard.
□ Không giống PDF.

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Identity | 20 |
| Decision | 20 |
| Reading Flow | 20 |
| Hierarchy | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S01 nhận Context từ S00.

S01 dẫn người dùng tới:

- S03 Four Pillars
- S04 Element Balance
- S05 Strength

Decision Support tại S01 phải đóng vai trò "bản đồ" cho toàn bộ Portal.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Identity & Decision Panel Blueprint |

bổ sung 5 phụ lục cho S01
Đây là phần mình cho là có giá trị nhất đối với Cursor.
Appendix A – Identity Priority Matrix
Thành phần	Priority
Nhật Chủ	10
Thân Vượng/Nhược	9
What	9
Why	8
Next	8
Dụng Thần	7
Hỷ/Kỵ Thần	6
Cách Cục	6
Quick Actions	4
Metadata	2


Appendix B – Wireframe ASCII (chi tiết)
┌────────────────────────────────────────────────────────────┐
│  NHẬT CHỦ (Hero)          │  THÂN: VƯỢNG   • Grade A       │
│  Kim • Dương             │  Confidence: 92%              │
├────────────────────────────────────────────────────────────┤
│ WHAT: Điều quan trọng nhất                                │
│ WHY : Vì sao có kết luận này                              │
│ NEXT: Nên xem tiếp S03 hoặc S05                           │
├────────────────────────────────────────────────────────────┤
│ Dụng Thần │ Hỷ Thần │ Kỵ Thần │ Cách Cục                  │
├────────────────────────────────────────────────────────────┤
│ [Xuất PDF] [In] [Chia sẻ] [Phân tích lại]                 │
└────────────────────────────────────────────────────────────┘

Appendix C – Focus Map
1. Nhật Chủ
      ↓
2. Thân
      ↓
3. What
      ↓
4. Why
      ↓
5. Next
      ↓
6. Dụng/Hỷ/Kỵ
      ↓
7. Quick 

Appendix D – Commercial Success Criteria
S01 đạt yêu cầu khi:
Người dùng hiểu bức tranh tổng thể trong ≤15 giây.
Không cần đọc Four Pillars vẫn biết tình trạng chung.
Có thể quyết định đọc sâu hoặc xuất báo cáo.
Hero tạo được điểm nhấn rõ ràng nhưng không lấn át Decision Panel.

Appendix E – Common Mistakes

Liệt kê những lỗi đã gặp trong các vòng review trước:
Hero giống banner quảng cáo.
Card nào cũng có trọng số như nhau.
Metadata quá nổi.
Quick Actions chiếm vị trí của Decision.
Decision bị đẩy xuống dưới fold.
Dùng quá nhiều màu sắc hoặc badge gây nhiễu.