# TV-01 — MARRIAGE CONSULTING
## 10_ACCEPTANCE_CHECKLIST.md

**Document ID:** TV-01-10

**Module:** TV-01_MARRIAGE

**Product:** BTE Platform

**Document Type:** Acceptance Checklist

**Status:** DRAFT FOR PRODUCT OWNER REVIEW

**Version:** 1.0

---

# 1. Purpose

Tài liệu này định nghĩa tiêu chuẩn nghiệm thu cuối cùng của module:

TV-01 — Marriage Consulting.

Đây là Release Gate cuối cùng trước khi:

- Freeze
- Production
- Commercial Release

TV-01 kế thừa:

COMMON/12_ACCEPTANCE_STANDARD.md

và chỉ bổ sung các Acceptance Rule đặc thù của Marriage Consulting.

---

# 2. Acceptance Philosophy

PASS không có nghĩa:

Build thành công.

PASS không có nghĩa:

UI đẹp.

PASS có nghĩa:

Module tuân thủ toàn bộ Consulting Framework.

---

# 3. Architecture Gate

- [ ] Tuân thủ COMMON Architecture.
- [ ] Không tạo Engine riêng.
- [ ] Không duplicate Canonical Mathematics.
- [ ] Không duplicate Decision Mathematics.
- [ ] Không duplicate Decision Engine.
- [ ] Chỉ sử dụng Marriage Policy.
- [ ] Chỉ sử dụng Report Profile.
- [ ] Chỉ sử dụng UI Layout Profile.

PASS khi tất cả đều đúng.

---

# 4. Runtime Gate

- [ ] Runtime đúng Pipeline.
- [ ] Không Skip Stage.
- [ ] Decision sau Finding.
- [ ] Recommendation sau Decision.
- [ ] Narrative sau Recommendation.
- [ ] Report sau Narrative.
- [ ] Presentation sau Report.

---

# 5. Decision Gate

- [ ] Marriage Policy được áp dụng.
- [ ] Decision đúng Decision Mathematics.
- [ ] Decision Explainable.
- [ ] Decision Deterministic.
- [ ] Decision Traceable.

---

# 6. Evidence Gate

- [ ] Evidence Atom hợp lệ.
- [ ] Evidence Chain hợp lệ.
- [ ] Evidence Graph hợp lệ.
- [ ] Resolution đúng.
- [ ] Không Orphan Evidence.

---

# 7. Finding Gate

- [ ] Finding được tạo từ Evidence.
- [ ] Không Finding tự sinh.
- [ ] Finding có Conditions.
- [ ] Finding có Confidence.
- [ ] Finding Traceable.

---

# 8. Recommendation Gate

- [ ] Recommendation sinh từ Decision.
- [ ] Có Objective.
- [ ] Có Priority.
- [ ] Có Timing.
- [ ] Có Expected Outcome.
- [ ] Có Source Decision.

---

# 9. Report Gate

- [ ] Executive Summary.
- [ ] Compatibility Hero.
- [ ] Domain Story.
- [ ] Recommendation Section.
- [ ] Appendix.
- [ ] Story Flow đúng.

---

# 10. UI Gate

- [ ] Hero hiển thị đầu tiên.
- [ ] Executive Summary sau Hero.
- [ ] Domain Cards đúng thứ tự.
- [ ] Recommendation rõ ràng.
- [ ] Progressive Disclosure.
- [ ] Responsive.
- [ ] Accessibility.

---

# 11. API Gate

- [ ] API Contract đúng.
- [ ] Resource Model đúng.
- [ ] Error Model đúng.
- [ ] Warning Model đúng.
- [ ] Version Bundle trả về.
- [ ] Expert Mode hoạt động.

---

# 12. Validation Gate

- [ ] Request Validation.
- [ ] Business Validation.
- [ ] Explainability Validation.
- [ ] Runtime Validation.
- [ ] Policy Validation.

---

# 13. Testing Gate

- [ ] Unit Tests PASS.
- [ ] Integration Tests PASS.
- [ ] Decision Tests PASS.
- [ ] Recommendation Tests PASS.
- [ ] Narrative Tests PASS.
- [ ] Report Tests PASS.
- [ ] Journey Tests PASS.
- [ ] Golden Dataset PASS.
- [ ] Regression PASS.

---

# 14. Explainability Gate

Kiểm tra chuỗi:

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

Nếu chuỗi bị đứt.

↓

FAIL.

---

# 15. Determinism Gate

Input giống nhau.

↓

Decision giống nhau.

↓

PASS.

---

# 16. Version Gate

- [ ] Version Bundle đầy đủ.
- [ ] Marriage Policy Version.
- [ ] Decision Mathematics Version.
- [ ] Narrative Version.
- [ ] Report Version.
- [ ] Presentation Version.

---

# 17. Performance Gate

- [ ] Runtime ổn định.
- [ ] Memory ổn định.
- [ ] Không Regression Performance.
- [ ] Không hy sinh Correctness để tăng tốc.

---

# 18. Security Gate

- [ ] Không sửa Canonical Truth.
- [ ] Không bypass Decision.
- [ ] Không bypass Validation.
- [ ] Không bypass Version.

---

# 19. Customer Experience Gate

- [ ] Story Flow tự nhiên.
- [ ] Không lặp ý.
- [ ] Không ngôn ngữ cực đoan.
- [ ] Recommendation rõ ràng.
- [ ] Kết luận dễ hiểu.
- [ ] Không lộ thuật ngữ kỹ thuật khi không cần.

---

# 20. Expert Mode Gate

- [ ] Evidence Graph.
- [ ] Finding Graph.
- [ ] Decision Trace.
- [ ] Version Bundle.
- [ ] Confidence.
- [ ] Rule References.

---

# 21. Commercial Gate

- [ ] Có thể dùng để tư vấn khách hàng thật.
- [ ] Có thể xuất Report.
- [ ] Có thể lưu History.
- [ ] Có thể Audit.
- [ ] Có thể Reproduce Decision.

---

# 22. Freeze Gate

TV-01 chỉ được FREEZE khi:

- [ ] COMMON Framework PASS.
- [ ] TV-01 Architecture PASS.
- [ ] TV-01 Runtime PASS.
- [ ] TV-01 Policy PASS.
- [ ] TV-01 Report PASS.
- [ ] TV-01 API PASS.
- [ ] TV-01 UI PASS.
- [ ] TV-01 Validation PASS.
- [ ] TV-01 Testing PASS.
- [ ] Commercial Gate PASS.

Nếu bất kỳ mục nào FAIL.

↓

TV-01 chưa được Freeze.

---

# 23. Final Acceptance Statement

TV-01 chỉ được coi là hoàn thành khi:

- Decision đúng.
- Recommendation đúng.
- Narrative đúng.
- Report đúng.
- UI đúng.
- Explainable.
- Deterministic.
- Traceable.
- Reproducible.
- Commercial Ready.

---

# 24. Release Approval

Product Owner:

□ PASS

□ FAIL

Ngày:

_____________________

Phiên bản:

_____________________

Người kiểm tra:

_____________________

---

# 25. Status

TV-01-10

STATUS:

FREEZE READY

END OF TV-01 MARRIAGE CONSULTING