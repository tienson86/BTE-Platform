# COMMON — CONSULTING FRAMEWORK

# 09_REPORT_STANDARD.md

Document ID: COMMON-09

Version: 1.0

Status: DRAFT

---

# 1. Purpose

Định nghĩa Report Standard.

Report là tầng Document của Consulting Framework.

Report không phải:

PDF.

DOCX.

HTML.

Report là:

Semantic Document.

---

# 2. Report Philosophy

Report trả lời:

"Thông tin nên được tổ chức như thế nào."

Không trả lời:

"Hiển thị như thế nào."

---

# 3. Report Definition

Report là:

Một tài liệu có cấu trúc.

Report luôn được tạo từ:

Assessment

Recommendation

Narrative

---

# 4. Report Pipeline

Decision

        /        \
Assessment      Recommendation
        \        /
         Narrative

↓

Report Model

↓

Renderer

↓

Output

---

# 5. Report Model

Report Model gồm:

Sections

Blocks

Charts

Tables

Cards

Highlights

Appendix

Metadata

---

# 6. Report Sections

Framework chuẩn hóa:

Assessment

Detailed Analysis

Recommendations

Action Plan

Appendix

Assessment không phải Executive Summary.

Assessment là Question Answers.

Recommendations là sibling, không derive từ Assessment.

---

# 7. Section Object

Section gồm:

Title

Summary

Content

Blocks

Visibility

Priority

---

# 8. Block Object

Block là đơn vị nhỏ nhất.

Ví dụ.

Paragraph

Table

Chart

Metric

Timeline

Callout

Image

Diagram

---

# 9. Report Metadata

Report luôn có:

Version

Profile

Language

Generated Time

Analysis IDs

Decision IDs

---

# 10. Report Independence

Report

không phụ thuộc:

PDF

DOCX

HTML

Renderer.

---

# 11. Render Pipeline

Report Model

↓

Renderer

↓

Output

Renderer có thể thay.

Report Model không đổi.

---

# 12. Multi-format

Framework hỗ trợ:

PDF

DOCX

HTML

Markdown

JSON

Voice Script

Dashboard

---

# 13. Report Version

Report có Version riêng.

---

# 14. Report Explainability

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

# 15. Report Anti-patterns

Sai.

Decision

↓

PDF

Sai.

Narrative

↓

PDF

Sai.

Renderer

↓

Decision

---

# 16. Report Statement

Report là:

Semantic Document.

PDF chỉ là một cách Render.

---

# 17. Freeze

FREEZE khi:

- [ ] Semantic Document.
- [ ] Section Model.
- [ ] Block Model.
- [ ] Metadata.
- [ ] Multi-format.
- [ ] Renderer Independence.
- [ ] Explainability.

---

# 18. Status

COMMON-09

STATUS

FREEZE READY