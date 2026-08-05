# BTE Platform

# S06 Blueprint — Ten Gods

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

S06 trình bày bức tranh tổng quan về Thập Thần trong lá số.

Đây là Relationship Layer đầu tiên của Portal.

Mục tiêu của S06 là giúp người dùng hiểu:

- Thập Thần nào xuất hiện.
- Mức độ nổi bật của từng Thập Thần.
- Vai trò tương đối của từng nhóm quan hệ.

S06 không đưa ra luận giải.

Không đánh giá tốt/xấu.

Không kết luận vận mệnh.

---

# 2. Business Goal

Sau khi xem S06, người dùng phải hiểu:

- Những Thập Thần nào nổi bật.
- Những Thập Thần nào yếu hoặc không xuất hiện.
- Cấu trúc quan hệ tổng thể của lá số.

S06 đóng vai trò cầu nối giữa Evidence và Interpretation.

---

# 3. User Questions

S06 phải trả lời:

✓ Tôi có những Thập Thần nào?

✓ Thập Thần nào chiếm ưu thế?

✓ Thập Thần nào rất ít hoặc không có?

✓ Quan hệ nào đáng chú ý?

Không trả lời:

- Tốt hay xấu.
- Có nên làm gì.
- Dụng Thần.
- Luận giải nghề nghiệp.
- Luận giải hôn nhân.

---

# 4. Decision Goal

Sau khi xem S06 người dùng phải hiểu:

"Tôi đã biết cấu trúc Thập Thần của mình."

↓

Tiếp tục:

S07 ShenSha

---

# 5. Reading Goal

≤30 giây.

Reading Flow

```
Ten Gods Summary

↓

Highlighted Gods

↓

All Ten Gods

↓

Relationship Notes

↓

Continue
```

Không bắt đầu bằng bảng 10 Thần.

---

# 6. Information Architecture

## Zone A — Ten Gods Summary

Hiển thị:

- Tổng số Thập Thần xuất hiện
- Nhóm nổi bật
- Nhận xét trung lập (1 câu)

---

## Zone B — Highlighted Gods

Hiển thị 2–3 Thập Thần nổi bật nhất.

Mỗi mục gồm:

- Tên
- Mức độ
- Điểm
- Vai trò

Không diễn giải.

---

## Zone C — Complete Ten Gods

Hiển thị đầy đủ:

- Chính Quan
- Thất Sát
- Chính Ấn
- Thiên Ấn
- Tỷ Kiên
- Kiếp Tài
- Thực Thần
- Thương Quan
- Chính Tài
- Thiên Tài

Mỗi mục:

- Count
- Score
- Strength

---

## Zone D — Relationship Notes

Hiển thị:

2–5 ghi chú ngắn.

Ví dụ:

"Chính Quan nổi bật."

"Tỷ Kiên xuất hiện nhiều."

Không viết luận giải.

---

# 7. Visual Hierarchy

```
Summary

↓

Highlighted Gods

↓

Complete List

↓

Relationship Notes
```

Danh sách đầy đủ không được nổi bật hơn Summary.

---

# 8. Layout Blueprint

Desktop

```
+------------------------------------------------------+

Ten Gods Summary

-------------------------------------------------------

Highlighted Gods

-------------------------------------------------------

10 Gods Grid

-------------------------------------------------------

Relationship Notes

+------------------------------------------------------+
```

Tablet

Summary

↓

Highlights

↓

Grid

↓

Notes

Mobile

Summary

↓

Highlights

↓

Stack

↓

Notes

---

# 9. Component Composition

Cho phép:

- StatCard
- Badge
- Chip
- ScoreBar
- ProgressBar
- Tooltip
- Divider

Không:

- Pie Chart
- Radar Chart
- Hero
- Timeline
- Accordion

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Summary | Analysis.TenGods.Summary |
| Highlighted Gods | Analysis.TenGods.Highlighted |
| God Name | Analysis.TenGods.Items.Name |
| Count | Analysis.TenGods.Items.Count |
| Score | Analysis.TenGods.Items.Score |
| Strength | Analysis.TenGods.Items.Strength |
| Notes | Analysis.TenGods.Notes |

---

# 11. Typography Rules

Summary

→ HeadingPrimary

Highlighted God

→ HeadingSecondary

God Name

→ BodyPrimary

Notes

→ BodySecondary

Metadata

→ Caption

Không sử dụng Display Typography.

---

# 12. Interaction Rules

Cho phép:

- Tooltip giải thích từng Thập Thần.
- Highlight khi hover.
- Mở Learning Panel.
- Điều hướng đến Knowledge.

Không:

- Luận giải trực tiếp.
- Chỉnh sửa dữ liệu.
- Mở Rule Engine.

---

# 13. Responsive Behaviour

Desktop

Grid 5 × 2.

Tablet

Grid 2 × 5.

Mobile

Stack.

Reading Flow giữ nguyên.

---

# 14. Accessibility

- Tooltip truy cập được bằng bàn phím.
- Không dùng màu làm tín hiệu duy nhất.
- Mọi ProgressBar đều có giá trị text.
- Semantic List.

---

# 15. Anti-Patterns

Không được:

❌ Luận giải Thập Thần.

❌ Kết luận nghề nghiệp.

❌ Kết luận hôn nhân.

❌ Đưa Dụng Thần.

❌ Đưa Recommendation.

❌ Chỉ hiển thị bảng dữ liệu.

❌ Làm cả 10 Thập Thần nổi bật như nhau.

---

# 16. Screenshot Acceptance

Cursor phải cung cấp:

1. Desktop Full

2. Desktop Zoom (S06)

3. Tablet

4. Mobile

5. Hover State

6. Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- thêm Hero
- thêm Chart
- đổi Reading Flow
- diễn giải thay Engine

Nếu chưa có dữ liệu:

sử dụng Placeholder đúng Blueprint.

---

# 18. Product Owner Review Checklist

Business

□ Hiểu cấu trúc Thập Thần.

Decision

□ Sẵn sàng sang S07.

Reading

□ Summary đọc trước.

Hierarchy

□ Highlight rõ.

Responsive

□ Desktop

□ Tablet

□ Mobile

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Summary Clarity | 20 |
| Relationship Clarity | 20 |
| Reading Flow | 20 |
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

S06 sử dụng dữ liệu từ:

- Four Pillars
- Strength Analysis

S06 tạo nền tảng cho:

S07 ShenSha

↓

S08 Interpretation

Ten Gods là Relationship Evidence.

Không phải kết luận.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Ten Gods Blueprint |

bổ sung 5 phụ lục

Appendix A – Ten Gods Priority Matrix
Thành phần	Priority
Summary	10
Highlighted Gods	9
Complete List	7
Relationship Notes	5


Appendix B – Canonical Wireframe
┌────────────────────────────────────────────────────────────┐
│ THẬP THẦN                                                  │
│ Nổi bật: Chính Quan • Chính Ấn • Chính Tài                 │
├────────────────────────────────────────────────────────────┤
│ Chính Quan      ████████ 8                                │
│ Chính Ấn        ███████  7                                │
│ Chính Tài       ██████   6                                │
├────────────────────────────────────────────────────────────┤
│ CQ  TS  CA  TA  TK                                         │
│ KT  TT  TQ  CT  TT                                         │
│ (10 ô Thập Thần với Count và Score)                        │
├────────────────────────────────────────────────────────────┤
│ Quan sát: Chính Quan và Chính Ấn chiếm ưu thế.             │
│ → Tiếp tục S07 để xem các Thần Sát liên quan.              │
└────────────────────────────────────────────────────────────┘
Appendix C – Reading Path
Summary
      ↓
Highlighted Gods
      ↓
Complete Ten Gods
      ↓
Relationship Notes
      ↓
S07 ShenSha

Appendix D – Relationship Boundary

S06 chỉ trình bày Relationship Evidence.
Không hiển thị:
Luận giải nghề nghiệp.
Luận giải tài vận.
Luận giải hôn nhân.
Dự đoán tương lai.
Dụng Thần.
Hỷ Thần.
Kỵ Thần.
Các nội dung này thuộc S08 Interpretation.

Appendix E – Common Mistakes
Các lỗi cần tránh:
Hiển thị 10 Thập Thần như một bảng dữ liệu khô cứng.
Không có Summary nên người dùng không biết điều gì nổi bật.
Đưa diễn giải hoặc dự đoán vào S06.
Làm tất cả Thập Thần có trọng số thị giác như nhau.
Không tạo được mối liên hệ giữa S06 và S08.