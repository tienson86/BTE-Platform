# TV-01 — MARRIAGE CONSULTING
## 09_TEST_STRATEGY.md

Document ID: TV-01-09

Module: TV-01_MARRIAGE

Product: BTE Platform

Document Type: Test Strategy

Status: DRAFT FOR PRODUCT OWNER REVIEW

Version: 1.0

---

# 1. Purpose

Tài liệu này định nghĩa Test Strategy của TV-01.

COMMON đã định nghĩa:

Validation Framework.

TV-01 định nghĩa:

Business Test Strategy.

---

# 2. Testing Philosophy

Testing không kiểm tra:

UI đẹp.

Testing kiểm tra:

Decision đúng.

Recommendation đúng.

Narrative đúng.

---

# 3. Test Pyramid

TV-01 sử dụng:

Unit Test

↓

Component Test

↓

Integration Test

↓

Decision Test

↓

Journey Test

↓

Acceptance Test

---

# 4. Unit Tests

Kiểm tra:

Marriage Policy.

Report Profile.

UI Layout.

Không kiểm tra:

COMMON.

---

# 5. Component Tests

Kiểm tra:

Decision Components.

Recommendation Components.

Report Components.

---

# 6. Integration Tests

Kiểm tra:

TV-01

↓

COMMON.

Không Mock Decision Mathematics.

---

# 7. Decision Tests

Kiểm tra:

Decision State.

Không kiểm tra:

Paragraph.

---

# 8. Recommendation Tests

Kiểm tra:

Action.

Priority.

Timing.

Conditions.

---

# 9. Narrative Tests

Kiểm tra:

Narrative đúng Decision.

Không thêm Decision mới.

Không đổi Recommendation.

---

# 10. Report Tests

Kiểm tra:

Section.

Story Flow.

Ordering.

Không kiểm tra PDF Renderer.

---

# 11. UI Tests

Kiểm tra:

Hero.

Summary.

Domain Cards.

Progressive Disclosure.

---

# 12. Golden Dataset

TV-01 phải có:

Golden Marriage Dataset.

Mỗi Case.

↓

Expected Decision.

Expected Recommendation.

Không so Paragraph.

---

# 13. Snapshot Tests

Snapshot:

Decision.

Recommendation.

Report Model.

Presentation Model.

Không Snapshot HTML.

---

# 14. Explainability Tests

Mọi Decision.

↓

Trace.

↓

Finding.

↓

Evidence.

↓

Truth.

Nếu thiếu.

↓

FAIL.

---

# 15. Determinism Tests

Chạy:

Input giống nhau.

↓

Decision giống nhau.

Không phụ thuộc:

LLM.

---

# 16. Version Tests

Version Bundle.

↓

Decision.

↓

PASS.

Không Silent Upgrade.

---

# 17. Performance Tests

Testing:

Latency.

Memory.

Graph Size.

Không giảm Correctness.

---

# 18. Regression Tests

Mọi Release.

↓

Golden Dataset.

↓

Regression Suite.

↓

PASS.

---

# 19. Business Tests

Marriage.

↓

Compatibility.

↓

Recommendations.

↓

Story Flow.

---

# 20. Customer Journey Tests

Journey:

Landing

↓

Hero

↓

Summary

↓

Domain

↓

Action

↓

Conclusion

Không bị đứt.

---

# 21. Expert Tests

Expert Mode.

↓

Evidence.

↓

Finding.

↓

Decision Trace.

---

# 22. Customer Tests

Customer Mode.

↓

Không hiển thị:

Evidence IDs.

Rule IDs.

---

# 23. Anti-pattern Tests

Framework phải FAIL nếu:

Narrative tạo Decision.

Recommendation không có Source.

Decision không Explainable.

---

# 24. Automation

Toàn bộ Test.

↓

CI.

↓

PASS.

↓

Release.

---

# 25. Coverage

Không đo:

Line Coverage.

Ưu tiên:

Decision Coverage.

Policy Coverage.

Journey Coverage.

---

# 26. Freeze Conditions

FREEZE khi:

- [ ] Unit Tests.
- [ ] Integration Tests.
- [ ] Decision Tests.
- [ ] Recommendation Tests.
- [ ] Narrative Tests.
- [ ] Report Tests.
- [ ] Journey Tests.
- [ ] Explainability Tests.
- [ ] Golden Dataset.
- [ ] Regression Suite.

---

# 27. Status

TV-01-09

STATUS

FREEZE READY