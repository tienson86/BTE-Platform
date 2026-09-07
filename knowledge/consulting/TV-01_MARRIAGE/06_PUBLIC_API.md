# TV-01 — MARRIAGE CONSULTING
## 06_PUBLIC_API.md

Document ID: TV-01-06

Module: TV-01_MARRIAGE

Product: BTE Platform

Document Type: Public API Specification

Status: DRAFT FOR PRODUCT OWNER REVIEW

Version: 1.0

---

# 1. Purpose

Tài liệu này định nghĩa Public API của module:

TV-01 — Marriage Consulting.

API không định nghĩa:

- Canonical Engine;
- Decision Engine;
- Narrative Engine.

API chỉ công bố:

Contract giữa Client và Consulting Framework.

Public resource chính:

Marriage Assessment.

---

# 2. API Philosophy

API không trả về:

Raw Truth.

API trả về:

Marriage Assessment Resource.

Client không cần biết Framework nội bộ.

TV-01 không công bố Decision Resource như mặt hàng mặc định.

---

# 3. Resource Model

TV-01 công bố các Resource:

Marriage Consultation

Marriage Report

Marriage Summary

Marriage History

Không công bố:

Evidence Graph

Finding Graph

Rule Engine

---

# 4. Endpoint Overview

POST

/api/v1/consulting/marriage

↓

Tạo Consultation mới.

---

GET

/api/v1/consulting/marriage/{consultation_id}

↓

Lấy Decision đầy đủ.

---

GET

/api/v1/consulting/marriage/{consultation_id}/summary

↓

Executive Summary.

---

GET

/api/v1/consulting/marriage/{consultation_id}/report

↓

Report Profile.

---

GET

/api/v1/consulting/marriage/history

↓

Danh sách Consultation.

---

# 5. POST /consulting/marriage

Request:

Person A

Person B

Options

Response:

Consultation ID

Status

Decision Version

---

# 6. Request Object

Request gồm:

person_a

person_b

options

Không chứa:

Decision.

Không chứa:

Evidence.

---

# 7. Person Object

Person:

Full Name

Gender

Birth Date

Birth Time

Birth Place

Reuse Birth Input Contract của BTE.

---

# 8. Options

Options gồm:

Language

Audience

Reading Level

Expert Mode

Luck Window

Không cho phép:

Override Policy.

---

# 9. Consultation Resource

Consultation gồm:

Consultation ID

Created Time

Version Bundle

Decision Status

Summary

---

# 10. Assessment Resource

Assessment Resource gồm:

Marriage Assessment

Six Answers

Recommendation

Narrative

Confidence

Metadata

Không trả:

Decision nội bộ mặc định.

Evidence mặc định.

Finding Graph.

---

# 11. Summary Resource

Summary chỉ gồm:

Six Assessment Answers

Headline

Top Strengths

Top Risks

Action Summary

---

# 12. Report Resource

Report trả về:

Report Model

Không trả:

PDF.

Renderer quyết định.

---

# 13. History Resource

History:

Consultation ID

Date

Score

Grade

Status

---

# 14. Response Envelope

Mọi Response:

Status

Data

Warnings

Errors

Version Bundle

---

# 15. Status Codes

SUCCESS

PARTIAL

FAILED

Không dùng riêng HTTP Status để biểu diễn nghiệp vụ.

---

# 16. Error Model

Error gồm:

Code

Stage

Message

Retryable

Trace ID

---

# 17. Warning Model

Warning gồm:

Code

Description

Affected Domain

---

# 18. Explainability API

Nếu:

expert=true

API trả thêm:

Decision Trace

Finding Trace

Evidence References

Version Bundle

---

# 19. Customer Mode

Mặc định:

Không trả:

Evidence Graph

Rule IDs

Internal States

---

# 20. Idempotency

POST phải hỗ trợ:

Idempotency Key.

Không tạo Consultation trùng.

---

# 21. Pagination

History:

Cursor-based Pagination.

Không dùng Offset mặc định.

---

# 22. Filtering

History hỗ trợ:

Date

Grade

Status

Language

---

# 23. Versioning

API Version

độc lập

Decision Version.

Ví dụ.

API:

v1

Decision:

marriage.policy.v2

---

# 24. Compatibility

API phải:

Backward Compatible.

Không Silent Break.

---

# 25. Security

Không trả:

Internal Rule IDs

trừ Expert Mode.

---

# 26. Performance

API phải hỗ trợ:

Async Consultation.

Polling.

Future Callback.

---

# 27. Future Extension

TV-02

TV-03

TV-04

đều dùng cùng API Pattern.

---

# 28. Anti-patterns

Không trả:

Canonical Truth trực tiếp.

Không trả:

Evidence Graph mặc định.

Không trả:

Decision Engine State.

---

# 29. Framework Statement

Public API là:

Contract.

Không phải:

Implementation.

---

# 30. Freeze Conditions

FREEZE khi:

- [ ] Resource Model.
- [ ] Endpoint Model.
- [ ] Error Model.
- [ ] Warning Model.
- [ ] Versioning.
- [ ] Expert Mode.
- [ ] Customer Mode.
- [ ] Idempotency.
- [ ] Backward Compatibility.

---

# 31. Status

TV-01-06

STATUS:

FREEZE READY