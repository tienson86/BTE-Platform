# TV-01 — MARRIAGE CONSULTING
## 08_VALIDATION_RULES.md

Document ID: TV-01-08

Module: TV-01_MARRIAGE

Product: BTE Platform

Document Type: Module Validation Rules

Status: DRAFT FOR PRODUCT OWNER REVIEW

Version: 1.0

---

# 1. Purpose

Tài liệu này định nghĩa Business Validation Rules của module TV-01.

Validation Framework được kế thừa từ:

COMMON/11_VALIDATION_STANDARD.md

TV-01 chỉ bổ sung các Rule nghiệp vụ đặc thù của tư vấn hôn nhân.

---

# 2. Validation Philosophy

TV-01 không kiểm tra:

Framework.

TV-01 kiểm tra:

Business Logic.

---

# 3. Validation Scope

TV-01 Validation áp dụng cho:

Marriage Request

Marriage Decision

Marriage Assessment

Marriage Recommendation

Marriage Report

Marriage UI Profile

Không áp dụng cho:

Canonical Mathematics.

---

# 4. Request Validation

Phải có:

Person A

Person B

Gender

Birth Date

Birth Time (nếu có)

Birth Place (nếu có)

---

# 5. Identity Validation

Không cho phép:

Person A

=

Person B

Không cho phép:

Birth Date rỗng.

---

# 6. Birth Data Validation

Thiếu giờ sinh.

↓

Cho phép.

↓

Giảm Confidence.

Không FAIL.

---

# 7. Policy Validation

Marriage Policy phải:

Available.

Compatible.

Version đúng.

---

# 8. Domain Validation

Các Domain bắt buộc:

Five Elements

Stem/Branch

Ten Gods

Interaction

Recommendation

Nếu Domain không đủ dữ liệu.

↓

Availability = false.

Không tự sinh kết quả.

---

# 9. Decision Validation

Decision phải có:

Decision State

Confidence

Recommendation

Version Bundle

---

# 10. Recommendation Validation

Mỗi Recommendation phải có:

Objective

Priority

Timing

Conditions

Source Decision

---

# 11. Report Validation

Report phải có:

Executive Summary

Compatibility Hero

Recommendation

Không thiếu các Section bắt buộc.

---

# 12. UI Validation

Hero luôn đứng đầu.

Recommendation luôn hiển thị.

Evidence chỉ Expert Mode.

---

# 13. Explainability Validation

Decision

↓

Finding

↓

Evidence

↓

Truth

Nếu mất chuỗi.

↓

FAIL.

---

# 14. Expert Validation

Expert Mode mới được:

Rule IDs

Evidence

Decision Trace

---

# 15. Customer Validation

Customer Mode không hiển thị:

Evidence IDs

Internal States

Rule IDs

---

# 16. Compatibility Validation

Marriage Policy

phải tương thích:

Decision Mathematics

Decision Engine

COMMON Version.

---

# 17. Runtime Validation

Pipeline phải đầy đủ.

Không Skip Stage.

---

# 18. Anti-patterns

Không Narrative tạo Decision.

Không Report sửa Decision.

Không UI sửa Recommendation.

---

# 19. Validation Result

PASS

WARNING

FAIL

CRITICAL

---

# 20. Freeze Conditions

FREEZE khi:

- [ ] Request Validation.
- [ ] Identity Validation.
- [ ] Domain Validation.
- [ ] Decision Validation.
- [ ] Recommendation Validation.
- [ ] Report Validation.
- [ ] UI Validation.
- [ ] Explainability.
- [ ] COMMON Validation kế thừa đầy đủ.

---

# 21. Status

TV-01-08

STATUS

FREEZE READY