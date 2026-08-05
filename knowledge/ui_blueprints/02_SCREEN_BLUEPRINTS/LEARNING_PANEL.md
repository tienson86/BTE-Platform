# BTE Platform

# Blueprint — Learning Panel

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Module

Knowledge Layer

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

Learning Panel là lớp hỗ trợ học tập theo nhu cầu.

Người dùng có thể mở bất kỳ lúc nào để hiểu:

- thuật ngữ
- khái niệm
- nguyên lý

Learning Panel không tham gia Reading Flow chính.

Không làm thay đổi kết quả phân tích.

---

# 2. Business Goal

Learning Panel giúp:

- giảm rào cản với người mới
- tăng niềm tin vào hệ thống
- giúp người dùng học Bát Tự từng bước
- giảm nhu cầu đọc tài liệu bên ngoài

Đây là một tính năng gia tăng giá trị.

Không phải phần bắt buộc của báo cáo.

---

# 3. User Questions

Learning Panel phải trả lời:

✓ Nhật Chủ là gì?

✓ Thập Thần là gì?

✓ Thần Sát là gì?

✓ Dụng Thần là gì?

✓ Vì sao hệ thống dùng khái niệm này?

Không trả lời:

- Lá số của tôi tốt hay xấu.
- Dự đoán tương lai.
- Luận giải cá nhân.

---

# 4. Decision Goal

Sau khi đọc Learning Panel,

người dùng phải:

- hiểu thuật ngữ
- quay lại Interpretation

Learning Panel không thay thế S08.

---

# 5. Reading Goal

Reading Flow

```
Interpretation

↓

Click thuật ngữ

↓

Learning Panel

↓

Đóng

↓

Quay lại đúng vị trí
```

Không điều hướng sang trang mới.

---

# 6. Information Architecture

## Zone A

Thuật ngữ

Ví dụ

Nhật Chủ

---

## Zone B

Định nghĩa ngắn

2–4 câu.

---

## Zone C

Ý nghĩa trong Bát Tự

---

## Zone D

Áp dụng trong lá số hiện tại

Ví dụ:

"Lá số của bạn..."

Không viết luận giải dài.

---

## Zone E

Xem thêm

Liên kết:

- Knowledge Base
- Bài viết
- Glossary

---

# 7. Visual Hierarchy

```
Term

↓

Definition

↓

Meaning

↓

Current Chart

↓

Learn More
```

Không đảo.

---

# 8. Layout Blueprint

Desktop

```
+-----------------------------------------------+

TERM

-----------------------------------------------

Definition

-----------------------------------------------

Meaning

-----------------------------------------------

Current Chart

-----------------------------------------------

Learn More

+-----------------------------------------------+
```

Tablet

Stack.

Mobile

Drawer hoặc Bottom Sheet.

Không Full Page.

---

# 9. Component Composition

Cho phép:

- Drawer
- Side Panel
- Bottom Sheet
- Accordion
- Link
- Tooltip
- Badge

Không:

- Hero
- Dashboard
- Progress
- Score
- Chart

---

# 10. Data Mapping

| UI | Knowledge |
|-----|-----------|
| Term | Glossary.Term |
| Definition | Glossary.Definition |
| Meaning | Glossary.Meaning |
| Example | Glossary.Example |
| Related | Glossary.Related |

Không đọc Rule Engine.

Không đọc Analysis Engine.

---

# 11. Typography Rules

Term

→ Heading Primary

Definition

→ Body Primary

Meaning

→ Body Secondary

Example

→ Body Secondary

Link

→ Caption

Không Display Typography.

---

# 12. Interaction Rules

Cho phép:

- mở từ Tooltip
- mở từ Chip
- mở từ Link
- tìm kiếm thuật ngữ
- chuyển sang thuật ngữ liên quan

Không:

- chỉnh sửa
- bình luận
- Prediction

---

# 13. Responsive Behaviour

Desktop

Right Drawer.

Tablet

Side Panel.

Mobile

Bottom Sheet.

Không chuyển thành trang riêng.

---

# 14. Accessibility

- Keyboard Focus.
- ESC đóng.
- Semantic Dialog.
- Screen Reader.
- Focus quay lại đúng vị trí vừa mở.

---

# 15. Anti-Patterns

Không được:

❌ Mở sang trang mới.

❌ Chặn Reading Flow.

❌ Viết bài dài hàng nghìn chữ.

❌ Trùng Interpretation.

❌ Luận giải cá nhân.

❌ Dùng Learning thay Knowledge Base.

---

# 16. Screenshot Acceptance

Cursor phải gửi:

1.

Desktop

2.

Tablet

3.

Mobile

4.

Drawer Open

5.

Bottom Sheet

6.

Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- tạo Route mới
- Full Screen
- Hero
- Summary

Learning luôn là:

On-demand Panel.

---

# 18. Product Owner Review Checklist

Business

□ Hỗ trợ học tập.

Reading

□ Không phá Reading Flow.

Interaction

□ Mở/Đóng mượt.

Responsive

□ Desktop

□ Tablet

□ Mobile

Knowledge

□ Nội dung ngắn gọn.

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Learnability | 20 |
| Reading Flow | 20 |
| Interaction | 20 |
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

Learning Panel được gọi từ:

- S01
- S03
- S04
- S05
- S06
- S07
- S08

Learning không được tự xuất hiện.

Learning không thay thế:

Interpretation.

Knowledge Base vẫn là nơi lưu toàn bộ kiến thức đầy đủ.

Learning Panel chỉ hiển thị phần rút gọn.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Learning Panel Blueprint |

Bổ sung thêm 5 phụ lục

Appendix A — Learning Entry Points
Learning Panel chỉ được mở từ các thành phần có ý nghĩa học tập:
Nguồn mở	Ví dụ
Tooltip	Nhật Chủ, Thập Thần, Thần Sát
Chip/Badge	Dụng Thần, Hỷ Thần
Link "Tìm hiểu thêm"	Cuối mỗi section
CTA trong Interpretation	Đọc thêm khái niệm liên quan


Không tự động bật khi tải trang.
Appendix B — Canonical Wireframe
┌─────────────────────────────────────────────────────┐
│ NHẬT CHỦ                                            │
├─────────────────────────────────────────────────────┤
│ Định nghĩa                                          │
│ Nhật Chủ là Thiên Can của trụ Ngày, đại diện cho... │
├─────────────────────────────────────────────────────┤
│ Ý nghĩa trong Bát Tự                                │
│ Là trung tâm để xác định Thập Thần và phân tích...  │
├─────────────────────────────────────────────────────┤
│ Áp dụng với lá số hiện tại                          │
│ Lá số này có Nhật Chủ Canh Kim...                   │
├─────────────────────────────────────────────────────┤
│ Thuật ngữ liên quan                                 │
│ [Thập Thần] [Dụng Thần] [Ngũ Hành]                  │
├─────────────────────────────────────────────────────┤
│ [Mở Knowledge Base đầy đủ]                          │
└─────────────────────────────────────────────────────┘

Appendix C — Knowledge Levels
Learning Panel nên chia nội dung thành 3 cấp độ:
Cấp độ	Nội dung
Level 1	Định nghĩa ngắn (30–60 giây đọc)
Level 2	Giải thích và ví dụ liên quan đến lá số hiện tại
Level 3	Liên kết sang Knowledge Base đầy đủ


Điều này giúp người mới không bị quá tải nhưng người dùng nâng cao vẫn có đường dẫn để nghiên cứu sâu.

Appendix D — Knowledge Boundary

Learning Panel chỉ chứa:
Định nghĩa.
Giải thích khái niệm.
Ví dụ minh họa.
Liên kết kiến thức.
Không chứa:
Kết luận cá nhân.
Khuyến nghị hành động.
Rule Engine.
JSON.
Dự đoán.
Diễn giải thay cho S08.

Appendix E — Blueprint Completion

Với LEARNING_PANEL.md, module 02_SCREEN_BLUEPRINTS được xem là hoàn chỉnh.
Chúng ta đã chuẩn hóa toàn bộ chuỗi trải nghiệm của màn hình kết quả Bát Tự:
S00  Context Verification
        ↓
S01  Identity & Decision
        ↓
S02  Workspace & Actions
        ↓
S03  Structural Evidence
        ↓
S04  Balance Evidence
        ↓
S05  Analytical Evidence
        ↓
S06  Relationship Evidence
        ↓
S07  Contextual Evidence
        ↓
S08  Decision Intelligence / Interpretation
        ↓
Learning Panel (On-demand Knowledge)