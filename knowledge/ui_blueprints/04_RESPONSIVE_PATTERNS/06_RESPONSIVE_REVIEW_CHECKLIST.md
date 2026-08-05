# BTE Platform

# Responsive Review Checklist

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

06_RESPONSIVE_REVIEW_CHECKLIST

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa tiêu chuẩn review Responsive UI của toàn bộ BTE Platform.

Checklist này được sử dụng để:

- Product Owner Review
- Architecture Review
- UI Review
- Responsive Review
- Commercial Review

Mọi màn hình phải vượt qua Checklist này trước khi được Freeze.

---

# 2. Review Philosophy

Review không dựa trên cảm nhận.

Review dựa trên Checklist.

Một Screen chỉ được đánh giá:

PASS

PASS WITH CHANGES

REJECT

Không sử dụng các nhận xét mơ hồ như:

- "Đẹp hơn"
- "Có vẻ ổn"
- "Tôi thích"

Mọi nhận xét phải tham chiếu đến Blueprint, Pattern hoặc Responsive Rules.

---

# 3. Required Deliverables

Cursor bắt buộc cung cấp:

✓ Desktop Full Screenshot

✓ Desktop Zoom Screenshot

✓ Tablet Screenshot

✓ Mobile Screenshot

Nếu có:

✓ Loading

✓ Empty State

✓ Error State

Không đủ Screenshot:

Không Review.

---

# 4. Desktop Review

Kiểm tra:

□ Layout đúng Blueprint.

□ Reading Flow đúng.

□ Hero đúng.

□ Decision Panel đúng.

□ Sidebar đúng.

□ TOC đúng.

□ White Space đúng.

□ Typography đúng.

□ Không có Overflow.

---

# 5. Tablet Review

Kiểm tra:

□ Layout chuyển đúng.

□ Sidebar thu gọn.

□ Grid đúng.

□ Card đúng.

□ Khoảng cách hợp lý.

□ Không mất thông tin.

□ Không vỡ Layout.

---

# 6. Mobile Review

Kiểm tra:

□ Một cột.

□ Drawer hoạt động.

□ Touch Target đạt chuẩn.

□ Không cuộn ngang.

□ Hero đúng.

□ Decision Panel đúng.

□ CTA dễ bấm.

□ Typography dễ đọc.

---

# 7. Reading Flow Review

Thứ tự phải luôn là:

S00

↓

S01

↓

S02

↓

S03

↓

S04

↓

S05

↓

S06

↓

S07

↓

S08

↓

Learning

Không được thay đổi.

---

# 8. Information Hierarchy Review

Kiểm tra:

□ Hero nổi bật nhất.

□ Decision Panel đứng sau Hero.

□ Summary đúng.

□ Evidence đúng.

□ Interpretation cuối.

□ Learning không chen giữa.

---

# 9. Component Review

Kiểm tra:

□ Hero Pattern.

□ Decision Pattern.

□ Summary Card.

□ Information Card.

□ Metric Card.

□ Evidence Card.

□ Score Bar.

□ Badge.

□ Action Bar.

□ Drawer.

□ Accordion.

Tất cả phải đúng Pattern.

---

# 10. Responsive Review

Kiểm tra:

□ Không đổi Reading Flow.

□ Không đổi Decision Flow.

□ Không đổi Business Meaning.

□ Không ẩn thông tin quan trọng.

□ Không tạo Component mới.

---

# 11. Interaction Review

Kiểm tra:

□ Hover đúng.

□ Tap đúng.

□ Drawer đúng.

□ Tooltip đúng.

□ Keyboard đúng.

□ Focus đúng.

---

# 12. Accessibility Review

Kiểm tra:

□ Keyboard Navigation.

□ Semantic HTML.

□ Screen Reader.

□ Focus Ring.

□ Contrast.

□ Touch Target.

---

# 13. Visual Review

Kiểm tra:

□ Spacing.

□ Alignment.

□ Typography.

□ Grid.

□ Border.

□ Shadow.

□ Color Token.

Không review theo cảm tính.

---

# 14. Commercial UX Review

Kiểm tra:

□ Người mới hiểu trong 5 giây.

□ Hero trả lời đúng câu hỏi.

□ Decision rõ.

□ CTA rõ.

□ Không gây quá tải.

□ Đọc dễ.

---

# 15. Performance Review

Kiểm tra:

□ Không Layout Shift.

□ Không Overflow.

□ Không Render lỗi.

□ Loading đúng.

---

# 16. Responsive Scorecard

| Category | Weight |
|----------|-------:|
| Reading Flow | 20 |
| Information Hierarchy | 20 |
| Responsive Layout | 15 |
| Component Compliance | 15 |
| Accessibility | 10 |
| Commercial UX | 10 |
| Performance | 10 |

Tổng điểm:

100.

---

# 17. Result Classification

95–100

PASS

80–94

PASS WITH CHANGES

Dưới 80

REJECT

Nếu:

Reading Flow sai

hoặc

Decision Flow sai

→ tự động REJECT.

---

# 18. Review Workflow

Cursor

↓

Completion Report

↓

Screenshot Review

↓

Checklist

↓

Issue List

↓

Fix

↓

Review lại

↓

Freeze

Không bỏ qua bước nào.

---

# 19. Product Owner Sign-off

Một Screen chỉ được Freeze khi:

□ Checklist PASS.

□ Screenshot PASS.

□ Responsive PASS.

□ Commercial PASS.

□ Product Owner Approval.

---

# 20. Definition of Done

Responsive Review hoàn thành khi:

✓ Desktop PASS.

✓ Tablet PASS.

✓ Mobile PASS.

✓ Accessibility PASS.

✓ Commercial PASS.

✓ Product Owner ký duyệt.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Review Checklist |

---

# Appendix A — Screenshot Checklist

| Screenshot | Required |
|------------|:--------:|
| Desktop Full | ✓ |
| Desktop Zoom | ✓ |
| Tablet | ✓ |
| Mobile | ✓ |
| Loading | Optional |
| Empty | Optional |
| Error | Optional |

---

# Appendix B — Common Review Mistakes

Không:

❌ Review chỉ Desktop.

❌ Review bằng cảm tính.

❌ Bỏ qua Mobile.

❌ Không xem Zoom Screenshot.

❌ Chỉ xem Completion Report.

---

# Appendix C — Product Owner Review Template

Review Result

PASS / PASS WITH CHANGES / REJECT

Issues

1.

2.

3.

Required Changes

1.

2.

3.

Approval

□ Approved

□ Rejected

---

# Appendix D — Freeze Criteria

Một Screen chỉ được Freeze khi:

✓ Không còn lỗi Critical.

✓ Responsive đạt yêu cầu.

✓ Screenshot đúng Blueprint.

✓ Product Owner ký duyệt.

Sau khi Freeze:

Không được thay đổi UI nếu không có Change Request.

---

# Appendix E — Review Principles

BTE Platform review theo 5 nguyên tắc:

1. Review bằng bằng chứng.
2. Review bằng Blueprint.
3. Review bằng Pattern.
4. Review bằng Screenshot.
5. Review bằng Checklist.

Không review theo cảm xúc.

Mục tiêu cuối cùng là:

**Mọi Screen đều đạt chất lượng nhất quán trước khi Frontend Integration bắt đầu.**