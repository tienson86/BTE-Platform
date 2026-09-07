# TV-01 — MARRIAGE CONSULTING
## 05_REPORT_PROFILE.md

Document ID: TV-01-05

Module: TV-01_MARRIAGE

Product: BTE Platform

Document Type: Report Profile Specification

Status: DRAFT FOR PRODUCT OWNER REVIEW

Version: 1.0

---

# 1. Purpose

Tài liệu này định nghĩa Report Profile của module:

TV-01 — Marriage Consulting.

Report Profile không định nghĩa:

- Report Engine;
- Report Model;
- Renderer.

Những thành phần trên được kế thừa từ:

COMMON/08_REPORT_STANDARD.md

TV-01 chỉ định nghĩa:

- Story Flow;
- Report Structure;
- Section Configuration;
- Visibility;
- Ordering;
- Customer Experience.

---

# 2. Report Philosophy

Report không phải:

Một tập hợp Section.

Report là:

Một hành trình giúp khách hàng hiểu Decision.

Khách hàng không nên cảm thấy:

"Mình đang đọc dữ liệu."

Khách hàng nên cảm thấy:

"Hệ thống đang giải thích câu chuyện hôn nhân của mình."

---

# 3. Customer Story

TV-01 luôn kể theo trình tự.

Identity

↓

Compatibility

↓

Why

↓

Strengths

↓

Risks

↓

Timing

↓

Action

↓

Conclusion

Không được đổi Story Flow.

---

# 4. Story Principle

Khách hàng luôn phải biết:

Tôi là ai?

↓

Hai người hợp đến đâu?

↓

Vì sao?

↓

Điều gì cần chú ý?

↓

Làm gì?

↓

Kết luận.

Đây là Story chuẩn.

---

# 5. Report Sections

Report mặc định gồm:

Executive Summary

Compatibility Hero

Relationship Overview

Five Elements

Stem / Branch

Ten Gods

Interaction

Finance

Family

Children

Timing

Recommendations

Appendix

---

# 6. Executive Summary

Luôn đứng đầu.

Executive Summary phải trả lời:

- Kết luận chung.
- Điểm mạnh.
- Điểm cần lưu ý.
- Khuyến nghị chính.

Không quá dài.

---

# 7. Compatibility Hero

Hero gồm:

Compatibility Score

Grade

Headline

Compatibility Level

Top Strengths

Top Risks

Đây là phần khách hàng nhìn đầu tiên.

---

# 8. Relationship Overview

Mục tiêu:

Giúp khách hàng hiểu:

Hai người tương hợp theo cấu trúc nào.

Không đi vào kỹ thuật.

---

# 9. Domain Order

Các Domain luôn theo:

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

Không thay đổi thứ tự.

---

# 10. Progressive Disclosure

Thông tin được mở theo từng tầng.

Level 1

Executive Summary

↓

Level 2

Decision

↓

Level 3

Domain

↓

Level 4

Evidence

↓

Level 5

Audit

Khách hàng phổ thông thường chỉ đọc đến Level 2 hoặc 3.

---

# 11. Five Elements Section

Hiển thị:

Decision

↓

Narrative

↓

Visualization

Không hiển thị Raw Canonical Data.

---

# 12. Stem / Branch Section

Hiển thị:

Các Interaction quan trọng.

Không hiển thị toàn bộ Rule.

---

# 13. Ten Gods Section

Hiển thị:

Các Role có ảnh hưởng.

Không trình bày theo kiểu bảng kỹ thuật.

---

# 14. Interaction Section

Tập trung:

- Communication.
- Conflict.
- Cooperation.

Đây là phần khách hàng quan tâm nhất.

---

# 15. Finance Section

Hiển thị:

Financial Compatibility.

Financial Strategy.

Financial Recommendations.

Không dự đoán giàu nghèo tuyệt đối.

---

# 16. Family Section

Hiển thị:

Family Dynamics.

Role Balance.

Family Recommendations.

---

# 17. Children Section

Hiển thị:

Parenting Compatibility.

Child-related Dynamics.

Không dự đoán:

- số con;
- giới tính;
- thời điểm sinh.

---

# 18. Timing Section

Hiển thị:

Supportive Periods

Sensitive Periods

Action Timing

Không làm thay đổi Natal Decision.

---

# 19. Recommendation Section

Recommendation luôn trình bày dưới dạng:

Action Plan.

Không chỉ là:

"Lời khuyên."

---

# 20. Action Plan

Action Plan gồm:

Priority

Timing

Objective

Expected Outcome

Narrative

Không chỉ có Paragraph.

---

# 21. Appendix

Appendix gồm:

Evidence Summary

Methodology

Decision Profile

Version Bundle

Disclaimer

Không hiển thị mặc định.

---

# 22. Expert Mode

Nếu bật:

Expert Mode.

Hiển thị thêm:

Evidence Graph

Finding Graph

Decision Trace

Version Bundle

Confidence

Rule IDs

---

# 23. Customer Mode

Customer Mode mặc định.

Ẩn:

Rule IDs

Graph

Evidence IDs

Audit

Chỉ hiển thị nội dung cần thiết.

---

# 24. Report Personalization

Report thay đổi theo:

Audience

Language

Reading Level

Decision không thay đổi.

---

# 25. Report Ordering

Không được:

Section kỹ thuật

↓

Executive Summary

Luôn:

Summary trước.

Chi tiết sau.

---

# 26. Visualization

Cho phép:

Cards

Charts

Timeline

Heatmap

Radar

Progress

Không thay đổi Decision.

---

# 27. Report Renderer

Report Profile

không biết:

PDF.

DOCX.

HTML.

Renderer tự quyết định.

---

# 28. Report Explainability

Report luôn truy được:

Narrative

↓

Recommendation

↓

Decision

↓

Finding

↓

Evidence

↓

Truth

---

# 29. Anti-patterns

Không được:

Raw Canonical

↓

Customer.

Không được:

Evidence

↓

Customer.

Không được:

Finding

↓

Customer.

Không được:

Decision

↓

PDF trực tiếp.

---

# 30. Report Statement

TV-01 Report Profile

không định nghĩa:

Engine.

TV-01 chỉ định nghĩa:

Customer Story.

Đây là nguyên tắc bất biến.

---

# 31. Freeze Conditions

FREEZE khi:

- [ ] Story Flow hoàn chỉnh.
- [ ] Executive Summary.
- [ ] Hero Section.
- [ ] Domain Order.
- [ ] Progressive Disclosure.
- [ ] Expert Mode.
- [ ] Customer Mode.
- [ ] Explainability.
- [ ] Renderer Independence.
- [ ] COMMON/08 được kế thừa đầy đủ.

---

# 32. Status

TV-01-05

STATUS:

FREEZE READY