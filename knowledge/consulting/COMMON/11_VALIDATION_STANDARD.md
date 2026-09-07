# COMMON — CONSULTING FRAMEWORK

# 11_VALIDATION_STANDARD.md

Document ID: COMMON-11

Version: 1.0

Status: DRAFT

---

# 1. Purpose

Định nghĩa Validation Standard.

Validation là hệ thống kiểm chứng toàn bộ Consulting Framework.

Validation không chỉ kiểm tra Input.

Validation kiểm tra mọi Layer.

---

# 2. Validation Philosophy

Validation trả lời:

"Kết quả này có hợp lệ không?"

Không trả lời:

"Kết quả này có đẹp không?"

---

# 3. Validation Layers

Framework Validation gồm:

Input Validation

Truth Validation

Evidence Validation

Finding Validation

Decision Validation

Assessment Validation

Recommendation Validation

Narrative Validation

Presentation Validation

---

# 4. Validation Pipeline

Input

↓

Truth

↓

Evidence

↓

Finding

↓

Decision

        /        \
Assessment      Recommendation
        \        /
         Narrative

↓

Presentation

Mỗi bước đều có Validation riêng.

---

# 5. Input Validation

Kiểm tra:

Schema

Required Fields

Formats

Canonical Types

---

# 6. Truth Validation

Kiểm tra:

Canonical Contract

Version

Completeness

Consistency

---

# 7. Evidence Validation

Kiểm tra:

Source

Traceability

Confidence

Context

Direction

Graph Integrity

---

# 8. Finding Validation

Kiểm tra:

Supporting Evidence

Conflicting Evidence

State

Severity

Conditions

---

# 9. Decision Validation

Kiểm tra:

Decision State

Profile

Priority

Dependency

Consistency

---

# 10. Recommendation Validation

Kiểm tra:

Action Type

Objective

Priority

Timing

Conditions

Decision Reference

---

# 11. Narrative Validation

Kiểm tra:

Không thêm Decision mới

Không thay Score

Không thay Grade

Không tạo Recommendation

Không tạo Finding

---

# 12. Presentation Validation

Kiểm tra:

Không mất thông tin

Không đổi Decision

Không đổi Recommendation

Layout đúng

Renderer đúng

---

# 13. Explainability Validation

Framework luôn kiểm tra:

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

Nếu chuỗi đứt.

↓

Validation Fail.

---

# 14. Determinism Validation

Cùng:

Truth

Profile

Version

↓

Decision

phải giống nhau.

---

# 15. Version Validation

Version Bundle

phải đồng nhất.

Không được:

Truth v1

Decision v2

Narrative v5

không tương thích.

---

# 16. Graph Validation

Evidence Graph

Finding Graph

Decision Graph

đều phải:

Connected

Consistent

Acyclic nếu yêu cầu

Không có Orphan Node

---

# 17. Integrity Validation

Framework kiểm tra:

Missing References

Broken References

Duplicate IDs

Dangling Objects

---

# 18. Anti-pattern Validation

Framework phải phát hiện:

Decision từ Truth.

Narrative từ Truth.

Recommendation từ Evidence.

Renderer sửa Decision.

---

# 19. Validation Severity

Framework chuẩn hóa:

Info

Warning

Error

Critical

---

# 20. Validation Result

Validation luôn trả:

Status

Errors

Warnings

Diagnostics

Trace

---

# 21. Validation Independence

Validation

không phụ thuộc:

Renderer

LLM

Theme

UI

---

# 22. Validation Statement

Validation không chỉ kiểm tra dữ liệu.

Validation bảo vệ toàn bộ Framework.

---

# 23. Freeze

FREEZE khi:

- [ ] Layer Validation.
- [ ] Explainability.
- [ ] Determinism.
- [ ] Traceability.
- [ ] Graph Integrity.
- [ ] Version Validation.
- [ ] Anti-pattern Detection.

---

# 24. Status

COMMON-11

STATUS

FREEZE READY