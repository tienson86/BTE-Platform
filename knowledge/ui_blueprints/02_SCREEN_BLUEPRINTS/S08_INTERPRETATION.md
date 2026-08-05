# BTE Platform

# S08 Blueprint — Interpretation

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

S08 là tầng cuối cùng của Portal.

Đây là nơi toàn bộ Evidence:

- Four Pillars
- Element Balance
- Strength
- Ten Gods
- ShenSha

được tổng hợp thành Interpretation.

Interpretation không phải:

- dữ liệu

không phải

- thống kê

không phải

- Rule Engine

Interpretation là sản phẩm cuối cùng người dùng nhận được.

---

# 2. Business Goal

Sau khi đọc S08, người dùng phải hiểu:

- Tôi là người như thế nào.
- Điều gì quan trọng nhất.
- Điều gì nên ưu tiên.
- Điều gì cần lưu ý.
- Tôi nên làm gì tiếp theo.

Đây là Business Value lớn nhất của BTE.

---

# 3. User Questions

S08 phải trả lời:

✓ Tôi là người như thế nào?

✓ Điều gì nổi bật nhất?

✓ Điểm mạnh là gì?

✓ Điểm cần chú ý là gì?

✓ Điều gì nên ưu tiên?

✓ Tôi nên đọc gì tiếp?

Không trả lời:

- Rule Engine hoạt động thế nào.
- Công thức tính.
- JSON.
- Debug.

---

# 4. Decision Goal

Sau S08,

người dùng phải có thể:

✓ Hiểu chính mình.

✓ Có hành động tiếp theo.

Ví dụ:

- Xuất PDF.
- Chia sẻ.
- Đặt lịch tư vấn.
- Xem Đại Vận.
- Xem Lưu Niên.
- Đọc Knowledge.

Interpretation phải dẫn tới Decision.

---

# 5. Reading Goal

≤60 giây.

Reading Flow

```
Executive Interpretation

↓

Strengths

↓

Watch Points

↓

Priorities

↓

Action Plan

↓

Continue Learning
```

Không bắt đầu bằng đoạn văn dài.

---

# 6. Information Architecture

## Zone A — Executive Interpretation

Một đoạn tóm tắt.

3–6 câu.

Trả lời:

"Tổng quan lá số."

Đây là nội dung quan trọng nhất.

---

## Zone B — Strengths

Hiển thị:

3–5 điểm mạnh.

Ví dụ:

- Tư duy phân tích tốt.
- Có khả năng tổ chức.
- Khả năng học hỏi cao.

Không giải thích dài.

---

## Zone C — Watch Points

Hiển thị:

3–5 điều cần lưu ý.

Ví dụ:

- Dễ bảo thủ.
- Thiếu linh hoạt.
- Cần cân bằng Hỏa.

Không tạo cảm giác tiêu cực.

---

## Zone D — Priorities

Hiển thị:

Điều quan trọng nhất.

Ví dụ:

- Củng cố Kim.
- Tăng Hỏa.
- Phát huy Chính Quan.

Dạng Priority Card.

Không phải đoạn văn.

---

## Zone E — Action Plan

Hiển thị:

Các hành động gợi ý.

Ví dụ:

- Xem Đại Vận.
- Xem Lưu Niên.
- Tải PDF.
- Học thêm.

Interpretation phải kết thúc bằng hành động.

---

# 7. Visual Hierarchy

```
Executive Summary

↓

Priorities

↓

Strengths

↓

Watch Points

↓

Action Plan
```

Executive luôn lớn nhất.

---

# 8. Layout Blueprint

Desktop

```
+------------------------------------------------------+

Executive Interpretation

-------------------------------------------------------

Priorities

-------------------------------------------------------

Strengths

-------------------------------------------------------

Watch Points

-------------------------------------------------------

Action Plan

+------------------------------------------------------+
```

Tablet

Executive

↓

Priority

↓

Strengths

↓

Watch Points

↓

Actions

Mobile

Stack.

---

# 9. Component Composition

Cho phép:

- Summary Panel
- Priority Card
- Bullet List
- Badge
- Callout
- Recommendation Card
- CTA Button
- Divider

Không:

- Table
- Hero Banner
- Progress Chart
- Rule Tree
- JSON

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Executive | Interpretation.Executive |
| Strengths | Interpretation.Strengths |
| Watch Points | Interpretation.WatchPoints |
| Priorities | Interpretation.Priorities |
| Action Plan | Interpretation.Actions |
| Confidence | Interpretation.Confidence |

---

# 11. Typography Rules

Executive

→ Display Small / Heading Primary

Priority

→ Heading Secondary

Strength

→ Body Primary

Watch Point

→ Body Primary

Action

→ Body Secondary

Không có đoạn văn quá dài.

---

# 12. Interaction Rules

Cho phép:

- Expand / Collapse từng nhóm.
- Copy Interpretation.
- Xuất PDF.
- Chia sẻ.
- Mở Knowledge.
- Điều hướng Đại Vận.

Không:

- Chỉnh sửa Interpretation.
- Debug Engine.

---

# 13. Responsive Behaviour

Desktop

5 khu vực.

Tablet

Stack.

Mobile

Một cột.

CTA luôn cuối.

---

# 14. Accessibility

- Semantic Heading.
- Bullet có Screen Reader.
- CTA có Label.
- Không dùng màu để truyền tải ý nghĩa.
- Focus Order theo Reading Flow.

---

# 15. Anti-Patterns

Không được:

❌ Một đoạn văn dài 2000 chữ.

❌ Chỉ hiển thị dữ liệu.

❌ Không có Executive Summary.

❌ Không có Priority.

❌ Không có CTA.

❌ Lặp lại nội dung S01.

❌ Diễn giải theo kiểu mê tín.

❌ Khẳng định tuyệt đối.

---

# 16. Screenshot Acceptance

Cursor phải gửi:

1.

Desktop Full

2.

Desktop Zoom (S08)

3.

Tablet

4.

Mobile

5.

Expanded State

6.

Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- tự viết Interpretation
- thêm nội dung AI
- thêm Rule
- đổi Reading Flow

Nếu chưa có Engine,

sử dụng Placeholder.

---

# 18. Product Owner Review Checklist

Business

□ Có giá trị thương mại.

Decision

□ Có thể hành động.

Reading

□ Executive đọc đầu tiên.

Hierarchy

□ Priority nổi bật.

Responsive

□ Desktop

□ Tablet

□ Mobile

Commercial

□ Người dùng cảm thấy "đáng tiền".

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Executive Clarity | 20 |
| Decision Support | 20 |
| Reading Flow | 20 |
| Commercial Value | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S08 tổng hợp toàn bộ dữ liệu từ:

- S03 Four Pillars
- S04 Element Balance
- S05 Strength
- S06 Ten Gods
- S07 ShenSha

S08 là đầu ra cuối cùng của Analysis Engine.

Sau S08,

người dùng có thể:

↓

- PDF Report
- Đại Vận
- Lưu Niên
- Tư vấn chuyên sâu
- Knowledge

Interpretation là cầu nối giữa Analysis và Action.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Interpretation Blueprint |

Bổ sung thêm 5 phụ lục

Appendix A — Interpretation Priority Matrix
Thành phần	Priority
Executive Interpretation	10
Priorities	9
Strengths	8
Watch Points	8
Action Plan	7


Appendix B — Canonical Wireframe
┌────────────────────────────────────────────────────────────┐
│ EXECUTIVE INTERPRETATION                                  │
│ "Bạn có nền tảng Kim mạnh, tư duy logic tốt..."            │
├────────────────────────────────────────────────────────────┤
│ ƯU TIÊN HÀNG ĐẦU                                           │
│ • Cân bằng Hỏa                                             │
│ • Phát huy Chính Quan                                      │
├────────────────────────────────────────────────────────────┤
│ ĐIỂM MẠNH                     │ ĐIỂM CẦN LƯU Ý             │
│ • Logic tốt                   │ • Thiếu linh hoạt          │
│ • Kỷ luật                     │ • Dễ bảo thủ               │
├────────────────────────────────────────────────────────────┤
│ HÀNH ĐỘNG TIẾP THEO                                      │
│ [Xuất PDF] [Xem Đại Vận] [Lưu Niên] [Kiến thức]            │
└────────────────────────────────────────────────────────────┘
Appendix C — Reading Path
Executive
      ↓
Priority
      ↓
Strengths
      ↓
Watch Points
      ↓
Action Plan
      ↓
Learning

Appendix D — Interpretation Boundary

S08 chỉ trình bày Interpretation.
Không hiển thị:
Rule Engine.
Công thức tính.
JSON.
Chi tiết từng Rule.
Danh sách đầy đủ Thập Thần.
Danh sách đầy đủ Thần Sát.
Những nội dung đó thuộc các section trước hoặc tầng kỹ thuật.

Appendix E — Commercial Interpretation Principles

Interpretation phải tuân thủ 5 nguyên tắc:
Kết luận trước, bằng chứng sau – không bắt người dùng ghép nối dữ liệu.
Ưu tiên hành động – mỗi phần diễn giải nên dẫn tới một bước tiếp theo rõ ràng.
Ngôn ngữ trung lập, có trách nhiệm – tránh khẳng định tuyệt đối hoặc tạo cảm giác mê tín.
Ngắn gọn nhưng đủ chiều sâu – mỗi ý chính nên có thể đọc và hiểu nhanh, phần mở rộng chỉ hiển thị khi cần.
Nhất quán với toàn bộ Evidence Layer – mọi diễn giải đều phải truy vết được về S03–S07.