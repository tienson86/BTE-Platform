# NARRATIVE V2 — TEST STRATEGY

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Test Strategy định nghĩa chiến lược kiểm thử chính thức của Narrative V2.

Narrative không chỉ cần:

- đúng về dữ liệu.

Narrative còn phải:

- đúng Meaning;
- đúng Language;
- đúng Grammar;
- đúng Customer Experience.

Mọi Builder của Narrative V2 đều phải được kiểm thử theo tài liệu này.

---

# 2. Mission

Narrative Testing trả lời:

> Narrative này có đáng để Publish hay chưa?

Không chỉ:

> Có chạy hay không?

---

# 3. Testing Philosophy

Narrative được kiểm thử theo bốn cấp.

```
Correct

↓

Understandable

↓

Consistent

↓

Commercial
```

Chỉ đúng thôi chưa đủ.

---

# 4. Test Architecture

```
Canonical Analysis

↓

Evidence Tests

↓

Reasoning Tests

↓

Knowledge Tests

↓

Rewrite Tests

↓

Grammar Tests

↓

Template Tests

↓

Narrative Tests

↓

Presentation Tests

↓

Acceptance Tests
```

---

# 5. Test Pyramid

```
Acceptance

↑

Narrative

↑

Rewrite

↑

Knowledge

↑

Reasoning

↑

Evidence
```

Unit nhiều.

Acceptance ít.

---

# 6. Unit Tests

Kiểm thử:

- Builder
- Validator
- Rewrite
- Sentence Selection

---

# 7. Integration Tests

Kiểm thử:

```
Evidence

↓

Reasoning

↓

Rewrite
```

Hoạt động đúng.

---

# 8. Narrative Tests

Narrative đầy đủ.

Overview.

Interpretation.

Action.

Commercial.

---

# 9. Presentation Tests

Dashboard.

PDF.

DOCX.

cùng Narrative.

---

# 10. Acceptance Tests

Đây là cấp cao nhất.

Khách hàng đọc.

↓

Hiểu.

---

# 11. Evidence Tests

Kiểm tra.

Evidence.

Đúng.

Đủ.

Không Duplicate.

---

# 12. Reasoning Tests

Reasoning.

Không bỏ Evidence.

Không sai Logic.

---

# 13. Knowledge Tests

Knowledge.

Resolve đúng.

Không Draft.

Không Legacy.

---

# 14. Rewrite Tests

Rewrite.

Không đổi Meaning.

Không sinh Meaning mới.

---

# 15. Grammar Tests

Grammar.

Đúng.

```
Observation

↓

Reasoning

↓

Meaning

↓

Impact

↓

Decision

↓

Action

↓

Closing
```

---

# 16. Template Tests

Slot.

Đúng.

Không thiếu.

---

# 17. Language Tests

Language Standard.

Đúng.

Không Technical.

---

# 18. Customer Safety Tests

Không:

Prediction.

Không:

Fear.

Không:

Hung/Cát.

---

# 19. Duplicate Tests

Không:

Overview.

↓

Interpretation.

↓

Action.

lặp.

---

# 20. Conversation Tests

Narrative.

Đọc.

↓

Giống.

Một cuộc tư vấn.

Không giống.

Report.

---

# 21. Golden Dataset

Narrative sử dụng:

Golden Cases.

Ví dụ.

```
CASE-0001

CASE-0002

CASE-0003
```

---

# 22. Snapshot Tests

Snapshot.

Narrative.

Nếu đổi.

↓

Review.

---

# 23. Semantic Regression

Kiểm tra.

Meaning.

Có đổi không.

---

# 24. Rewrite Regression

Rewrite.

Có đổi.

Language.

Không đổi.

Meaning.

---

# 25. Grammar Regression

Grammar.

Có còn đúng.

Conversation.

---

# 26. Template Regression

Template.

Có đổi Slot.

Không.

---

# 27. Cross Output Tests

Dashboard.

PDF.

DOCX.

↓

Cùng Narrative.

---

# 28. Consumer Tests

Dashboard.

Không Rewrite.

PDF.

Không Rewrite.

DOCX.

Không Rewrite.

---

# 29. Builder Tests

Summary.

Interpretation.

Action.

Commercial.

Builder độc lập.

---

# 30. Validation Tests

Validator.

PASS.

WARNING.

FAIL.

Đúng.

---

# 31. Runtime Tests

Runtime.

Đúng thứ tự.

---

# 32. Performance Tests

Narrative.

Deterministic.

---

# 33. Serialization Tests

Narrative.

Serialize.

JSON.

Dashboard.

PDF.

DOCX.

---

# 34. Traceability Tests

Narrative.

↓

Knowledge.

↓

Evidence.

↓

Canonical.

---

# 35. Failure Tests

Knowledge thiếu.

↓

Partial.

Validation fail.

↓

Reject.

---

# 36. Negative Tests

Ví dụ.

JSON.

↓

FAIL.

Rule ID.

↓

FAIL.

Prediction.

↓

FAIL.

---

# 37. Test Matrix

| Test | Mục tiêu |
|--------|----------|
| Schema | Đúng cấu trúc |
| Evidence | Đúng dữ liệu |
| Reasoning | Đúng Logic |
| Rewrite | Đúng Meaning |
| Grammar | Đúng dòng tư duy |
| Template | Đúng cấu trúc |
| Language | Đúng ngôn ngữ |
| Safety | Đúng chuẩn khách hàng |
| Duplicate | Không lặp |
| Presentation | Đúng Contract |

---

# 38. Automation Strategy

Tất cả Narrative Tests.

Tự động.

Golden.

Snapshot.

Regression.

---

# 39. Manual Review

Narrative.

Được đọc.

Bởi.

Product Owner.

Không chỉ.

CI.

---

# 40. Release Gate

Narrative chỉ được Release khi:

✓ Unit.

PASS.

✓ Integration.

PASS.

✓ Narrative.

PASS.

✓ Customer Safety.

PASS.

✓ Acceptance.

PASS.

---

# 41. Narrative Quality Matrix

Narrative không được đánh giá chỉ bằng:

"Đúng."

Narrative được đánh giá theo năm tiêu chí:

| Tiêu chí | Câu hỏi cần trả lời |
|----------|----------------------|
| Correctness | Meaning có đúng với Canonical Analysis không? |
| Clarity | Khách hàng phổ thông có hiểu không? |
| Consistency | Có thống nhất với Language Standard và các Builder khác không? |
| Commercial Value | Có giúp khách hàng ra quyết định tốt hơn không? |
| Reusability | Có dùng lại được cho Dashboard, PDF, DOCX và API không? |

Một Narrative chỉ được coi là đạt khi đồng thời đạt cả năm tiêu chí trên.

---

# 42. Test Coverage Matrix

| Layer | Unit | Integration | Snapshot | Regression | Acceptance |
|--------|:----:|:-----------:|:---------:|:----------:|:----------:|
| Evidence | ✓ | ✓ | ✗ | ✓ | ✗ |
| Reasoning | ✓ | ✓ | ✗ | ✓ | ✗ |
| Knowledge | ✓ | ✓ | ✗ | ✓ | ✗ |
| Rewrite | ✓ | ✓ | ✓ | ✓ | ✓ |
| Summary | ✓ | ✓ | ✓ | ✓ | ✓ |
| Interpretation | ✓ | ✓ | ✓ | ✓ | ✓ |
| Action | ✓ | ✓ | ✓ | ✓ | ✓ |
| Presentation | ✓ | ✓ | ✓ | ✓ | ✓ |

Mỗi layer phải có chiến lược kiểm thử phù hợp với vai trò của nó.

---

# 43. Golden Narrative Policy

Golden Cases là tiêu chuẩn bất biến của Narrative V2.

Mỗi Golden Case phải lưu:

- Canonical Analysis
- Narrative Output
- Presentation Output
- Expected Meaning
- Approved Review

Mọi thay đổi Narrative đều phải được so sánh với Golden Cases trước khi Publish.

Nếu Golden Case thay đổi:

↓

Bắt buộc Product Owner Review.

---

# 44. Test Governance

Không được:

- sửa Snapshot để test PASS;
- bỏ qua Regression;
- Publish khi Acceptance chưa đạt.

Quy trình bắt buộc:

Implementation

↓

Validation

↓

Testing

↓

Product Review

↓

Release

Không đảo thứ tự.

---

# 45. Final Test Principle

Narrative V2 không được coi là đúng chỉ vì:

- code chạy;
- test xanh;
- JSON hợp lệ.

Narrative chỉ được coi là hoàn thành khi:

- chuyên gia đọc thấy đúng;
- khách hàng đọc thấy dễ hiểu;
- Product Owner chấp nhận Publish.

> **Test Strategy không tồn tại để chứng minh Narrative hoạt động.**

> **Test Strategy tồn tại để chứng minh Narrative xứng đáng được khách hàng đọc.**