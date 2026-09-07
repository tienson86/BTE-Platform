# TV-01 — MARRIAGE CONSULTING
## 07_UI_LAYOUT.md

Document ID: TV-01-07

Module: TV-01_MARRIAGE

Product: BTE Platform

Document Type: UI Layout Profile

Status: DRAFT FOR PRODUCT OWNER REVIEW

Version: 1.0

---

# 1. Purpose

Tài liệu này định nghĩa UI Layout Profile của module TV-01.

UI Layout không định nghĩa:

- HTML
- CSS
- Component Framework
- React
- Vue
- Tailwind

UI Layout chỉ định nghĩa:

- Information Architecture
- Customer Journey
- Layout Hierarchy
- Progressive Disclosure
- Component Arrangement

---

# 2. UI Philosophy

UI không được thiết kế theo:

Data-first.

UI phải thiết kế theo:

Customer-first.

Khách hàng không muốn xem:

Can Chi

↓

Ngũ hành

↓

Thập thần

Khách hàng muốn biết:

"Tôi có hợp người này không?"

↓

"Tại sao?"

↓

"Cần làm gì?"

---

# 3. Customer Journey

UI luôn theo hành trình.

Landing

↓

Compatibility

↓

Understanding

↓

Details

↓

Action

↓

Confidence

↓

Appendix

Không được đảo thứ tự.

---

# 4. Layout Principles

Mỗi màn hình luôn:

Summary First

↓

Details Later

↓

Evidence Last

Không hiển thị toàn bộ dữ liệu cùng lúc.

---

# 5. Screen Hierarchy

Level 1

Compatibility Hero

Level 2

Executive Summary

Level 3

Domain Cards

Level 4

Recommendations

Level 5

Evidence

Level 6

Audit

---

# 6. Hero Section

Hero luôn đứng đầu.

Hiển thị:

Compatibility Score

Grade

Headline

Top Strengths

Top Risks

CTA

---

# 7. Executive Summary

Hiển thị:

Một đoạn ngắn.

Không quá 200 từ.

Giúp khách hàng hiểu:

Kết luận.

---

# 8. Domain Cards

Mỗi Domain.

↓

Một Card.

Card gồm:

Title

State

Summary

Expand

Không hiển thị tất cả.

---

# 9. Domain Order

Five Elements

↓

Stem / Branch

↓

Ten Gods

↓

Interaction

↓

Finance

↓

Family

↓

Children

↓

Timing

↓

Recommendation

---

# 10. Progressive Disclosure

Collapsed

↓

Expanded

↓

Expert

Khách hàng phổ thông.

↓

Không nhìn thấy Evidence.

---

# 11. Expert Mode

Expert Mode hiển thị:

Evidence

Finding

Confidence

Version

Decision Trace

Rule Trace

---

# 12. Recommendation Panel

Recommendation luôn hiển thị:

Priority

Timing

Action

Expected Outcome

Không chỉ Paragraph.

---

# 13. Confidence Panel

Hiển thị:

Confidence

Reason

Limitations

Không chỉ phần trăm.

---

# 14. Decision Panel

Hiển thị:

Decision State

Không hiển thị:

Internal Graph.

---

# 15. Evidence Panel

Ẩn mặc định.

Chỉ mở:

Expert Mode.

---

# 16. Mobile Layout

Mobile.

↓

Một cột.

Hero

↓

Summary

↓

Cards

↓

Recommendations

↓

Appendix

---

# 17. Tablet Layout

Hai cột.

Hero toàn chiều ngang.

---

# 18. Desktop Layout

Dashboard.

Hero.

↓

Executive Summary.

↓

Domain Grid.

↓

Recommendations.

↓

Appendix.

---

# 19. Responsive Rules

Layout thay đổi.

Information không đổi.

---

# 20. Visual Priority

Mức ưu tiên.

Hero

↓

Summary

↓

Recommendations

↓

Domains

↓

Evidence

↓

Audit

---

# 21. Expand Rules

Mỗi Card.

↓

Expand độc lập.

Không Expand toàn bộ.

---

# 22. Visual Consistency

TV-01

TV-02

TV-03

TV-04

phải dùng cùng Design Language.

---

# 23. Component Library

Reuse:

Hero Card

Decision Card

Recommendation Card

Timeline Card

Confidence Card

Appendix Card

Không tạo Component riêng nếu đã tồn tại.

---

# 24. Accessibility

UI phải hỗ trợ:

Keyboard

Screen Reader

Responsive

Contrast

Không dùng màu làm nguồn thông tin duy nhất.

---

# 25. Empty State

Nếu Domain không có dữ liệu.

↓

Giải thích lý do.

Không hiển thị ô trống.

---

# 26. Loading State

Loading.

↓

Skeleton.

Không Spinner toàn màn hình nếu không cần.

---

# 27. Error State

Error.

↓

Thông báo rõ:

Stage.

Reason.

Retry.

Không hiển thị Stack Trace.

---

# 28. UI Independence

Layout.

↓

Không thay đổi:

Decision.

Recommendation.

Narrative.

---

# 29. Anti-patterns

Sai.

Evidence

↓

Landing.

Sai.

Raw Truth

↓

Customer.

Sai.

100% dữ liệu

↓

Một màn hình.

---

# 30. Framework Statement

TV-01 UI Layout

không định nghĩa UI Framework.

TV-01 chỉ định nghĩa:

Customer Journey.

---

# 31. Freeze Conditions

FREEZE khi:

- [ ] Customer Journey.
- [ ] Hero.
- [ ] Summary.
- [ ] Domain Cards.
- [ ] Recommendation Panel.
- [ ] Progressive Disclosure.
- [ ] Expert Mode.
- [ ] Responsive.
- [ ] Accessibility.
- [ ] COMMON Presentation Standard được kế thừa.

---

# 32. Status

TV-01-07

STATUS:

FREEZE READY