# BTE Platform

# S04 Blueprint — Element Balance

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

S04 trình bày trạng thái cân bằng Ngũ Hành của lá số.

Đây là tầng Evidence thứ hai trong Portal.

Mục tiêu của S04 không phải là đưa ra kết luận.

Mục tiêu là giúp người dùng hiểu bức tranh phân bố Ngũ Hành để chuẩn bị cho phần phân tích Thân Vượng/Nhược ở S05.

---

# 2. Business Goal

Sau khi xem S04, người dùng phải hiểu:

- Ngũ Hành phân bố như thế nào.
- Hành nào mạnh.
- Hành nào yếu.
- Lá số đang cân bằng hay thiên lệch.

Không kết luận tốt/xấu.

Không kết luận Dụng Thần.

---

# 3. User Questions

S04 phải trả lời:

✓ Ngũ Hành của tôi phân bố ra sao?

✓ Hành nào chiếm ưu thế?

✓ Hành nào thiếu?

✓ Lá số cân bằng hay lệch?

Không trả lời:

- Thân Vượng/Nhược.
- Dụng Thần.
- Hỷ Thần.
- Kỵ Thần.
- Luận giải.

---

# 4. Decision Goal

Sau khi xem S04, người dùng đưa ra đúng một quyết định:

"Tôi đã hiểu trạng thái cân bằng Ngũ Hành."

↓

Tiếp tục đọc S05.

---

# 5. Reading Goal

≤20 giây.

Reading Flow

```
Balance Summary

↓

Five Elements

↓

Comparison

↓

Observation

↓

Continue
```

Người dùng phải hiểu tổng quan trước khi nhìn từng hành.

---

# 6. Information Architecture

## Zone A — Balance Summary

Hiển thị:

- Trạng thái cân bằng (Cân bằng / Thiên Kim / Thiên Mộc...)
- Mức độ cân bằng
- Nhận xét ngắn (1 câu)

---

## Zone B — Five Elements Distribution

Hiển thị:

- Kim
- Mộc
- Thủy
- Hỏa
- Thổ

Mỗi hành gồm:

- Điểm
- Tỷ lệ %
- Thanh mức (Score Bar)

Không sử dụng biểu đồ tròn hoặc radar.

---

## Zone C — Comparison

Hiển thị:

- Hành mạnh nhất
- Hành yếu nhất
- Chênh lệch tương đối

Không đưa khuyến nghị.

---

## Zone D — Observation

Hiển thị:

- Nhận xét trung lập về phân bố.
- Liên kết sang S05.

Không đưa luận giải chi tiết.

---

# 7. Visual Hierarchy

Visual Priority

```
Balance Summary

↓

Strongest Element

↓

Weakest Element

↓

Five Elements

↓

Observation
```

Các hành không được có trọng số thị giác bằng nhau nếu dữ liệu thể hiện sự chênh lệch rõ rệt.

---

# 8. Layout Blueprint

Desktop

```
+-------------------------------------------------------------+

Balance Summary

--------------------------------------------------------------

Kim

Mộc

Thủy

Hỏa

Thổ

--------------------------------------------------------------

Comparison

--------------------------------------------------------------

Observation

+-------------------------------------------------------------+
```

Tablet

Summary

↓

Elements (2+3)

↓

Comparison

↓

Observation

Mobile

Summary

↓

Kim

↓

Mộc

↓

Thủy

↓

Hỏa

↓

Thổ

↓

Observation

---

# 9. Component Composition

Cho phép:

- Section Title
- ScoreBar
- ProgressBar
- StatCard
- Badge
- Chip
- Divider

Không cho phép:

- Pie Chart
- Radar Chart
- Gauge Chart
- Hero
- Table
- Accordion

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Balance Status | Analysis.ElementBalance.Status |
| Balance Score | Analysis.ElementBalance.Score |
| Strongest Element | Analysis.ElementBalance.Strongest |
| Weakest Element | Analysis.ElementBalance.Weakest |
| Kim | Analysis.Elements.Metal |
| Mộc | Analysis.Elements.Wood |
| Thủy | Analysis.Elements.Water |
| Hỏa | Analysis.Elements.Fire |
| Thổ | Analysis.Elements.Earth |

---

# 11. Typography Rules

Balance Summary

→ HeadingPrimary

Element Name

→ HeadingSecondary

Score

→ BodyPrimary

Observation

→ BodySecondary

Metadata

→ Caption

Không sử dụng Display Typography.

---

# 12. Interaction Rules

Cho phép:

- Tooltip từng hành.
- Highlight khi hover.
- Mở Learning Panel.
- Điều hướng sang S05.

Không:

- Chỉnh sửa dữ liệu.
- Hiển thị luận giải dài.
- Mở Dialog.

---

# 13. Responsive Behaviour

Desktop

5 thanh ngang.

Tablet

2 + 3.

Mobile

Stack.

Reading Flow giữ nguyên.

---

# 14. Accessibility

- ScoreBar có giá trị bằng text.
- Không dùng màu làm tín hiệu duy nhất.
- Tooltip truy cập bằng bàn phím.
- Semantic List.

---

# 15. Anti-Patterns

Không được:

❌ Kết luận Thân Vượng tại S04.

❌ Hiển thị Dụng Thần.

❌ Hiển thị Hỷ/Kỵ Thần.

❌ Dùng Pie Chart.

❌ Dùng Radar Chart.

❌ Dùng màu sắc quá mạnh làm thay đổi trọng số thông tin.

❌ Lặp lại nội dung của S01.

---

# 16. Screenshot Acceptance

Cursor phải cung cấp:

1. Desktop Full

2. Desktop Zoom (S04)

3. Tablet

4. Mobile

5. Hover State

6. Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- tự thêm biểu đồ mới
- thay đổi Reading Flow
- thêm Hero
- thêm kết luận

Nếu chưa có dữ liệu thật:

sử dụng mock đúng Blueprint.

---

# 18. Product Owner Review Checklist

Business

□ Hiểu trạng thái cân bằng.

Decision

□ Sẵn sàng sang S05.

Reading

□ Summary đọc trước.

Hierarchy

□ Strongest/Weakest rõ.

Responsive

□ Desktop

□ Tablet

□ Mobile

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Balance Clarity | 20 |
| Reading Flow | 20 |
| Information Hierarchy | 20 |
| Responsive | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S04 sử dụng dữ liệu từ:

S03 Four Pillars

↓

Tạo nền tảng cho:

S05 Strength

S04 không đưa ra kết luận cuối cùng.

S04 chỉ giải thích trạng thái phân bố Ngũ Hành.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Element Balance Blueprint |

bổ sung 5 phụ lục

Appendix A – Element Priority Matrix
Thành phần	Priority
Balance Summary	10
Strongest Element	9
Weakest Element	8
Five Elements	7
Observation	5


Appendix B – Canonical Wireframe
┌──────────────────────────────────────────────────────┐
│ Balance: THIÊN KIM                                  │
│ Phân bố Ngũ Hành thiên lệch, Kim chiếm ưu thế.       │
├──────────────────────────────────────────────────────┤
│ Kim   ██████████ 35%                                │
│ Mộc   ████       12%                                │
│ Thủy  ██████     20%                                │
│ Hỏa   ███        10%                                │
│ Thổ   ███████    23%                                │
├──────────────────────────────────────────────────────┤
│ Mạnh nhất: Kim                                      │
│ Yếu nhất : Hỏa                                      │
├──────────────────────────────────────────────────────┤
│ Quan sát: Phân bố có xu hướng thiên Kim.            │
│ → Tiếp tục xem S05 để hiểu ảnh hưởng đến Thân.       │
└──────────────────────────────────────────────────────┘

Appendix C – Reading Path
Balance Summary
      ↓
Strongest / Weakest
      ↓
Five Elements
      ↓
Observation
      ↓
S05 Strength

Appendix D – Evidence Boundary

S04 chỉ trình bày Balance Evidence.
Không hiển thị:
Thân Vượng/Nhược.
Dụng Thần.
Hỷ Thần.
Kỵ Thần.
Thập Thần.
Thần Sát.
Luận giải.
Điều này giúp ranh giới giữa S04 và S05 luôn rõ ràng.

Appendix E – Common Mistakes
Những lỗi cần tránh:
Dùng biểu đồ quá phức tạp khiến người dùng khó so sánh.
Làm cả năm hành nổi bật như nhau, che mất hành mạnh và hành yếu.
Đưa nhận xét mang tính kết luận ("lá số tốt/xấu") vào S04.
Trình bày quá nhiều số liệu mà không có Summary.
Không có liên kết logic sang S05.