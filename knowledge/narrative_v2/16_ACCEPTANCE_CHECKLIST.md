# NARRATIVE V2 — ACCEPTANCE CHECKLIST

Version: V2.0

Status: CANONICAL

Owner: Product Owner

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Acceptance Checklist là cổng kiểm duyệt cuối cùng trước khi Narrative được phép Publish.

Narrative chỉ được Release khi vượt qua toàn bộ Checklist này.

Checklist không thay thế:

- Validation;
- Testing.

Checklist là bước đánh giá cuối cùng của Product Owner.

---

# 2. Mission

Checklist trả lời duy nhất một câu hỏi:

> Narrative này đã đủ chất lượng để khách hàng đọc hay chưa?

Nếu chưa.

↓

Không Publish.

---

# 3. Acceptance Philosophy

Một Narrative được coi là hoàn thành khi:

✓ đúng;

✓ dễ hiểu;

✓ nhất quán;

✓ hữu ích;

✓ đáng tin.

Không chỉ:

✓ chạy.

---

# 4. Acceptance Flow

```
Implementation

↓

Validation

↓

Testing

↓

Acceptance

↓

Release
```

Không đảo thứ tự.

---

# 5. Architecture Checklist

□ Narrative tuân thủ Architecture.

□ Không vi phạm Dependency.

□ Không Builder nào làm sai trách nhiệm.

□ Không Consumer Compose.

PASS

↓

YES / NO

---

# 6. Data Model Checklist

□ Đúng Data Model.

□ Không Object thừa.

□ Không Object sai Ownership.

□ Không sửa CanonicalAnalysis.

PASS

↓

YES / NO

---

# 7. Public API Checklist

□ Đúng Public API.

□ Không Breaking Change.

□ Không thêm Field ngoài Contract.

□ Không đổi Meaning.

PASS

↓

YES / NO

---

# 8. Pipeline Checklist

□ Đúng Runtime Sequence.

□ Không bỏ Stage.

□ Không chạy sai thứ tự.

□ Validation luôn trước Publish.

PASS

↓

YES / NO

---

# 9. Presentation Checklist

□ Dashboard đọc Presentation.

□ PDF đọc Presentation.

□ DOCX đọc Presentation.

□ Không Compose.

PASS

↓

YES / NO

---

# 10. Summary Checklist

□ Executive Summary.

□ Có Insight.

□ Không Action.

□ Không Prediction.

□ Đọc trong 30 giây.

PASS

↓

YES / NO

---

# 11. Interpretation Checklist

□ Có Observation.

□ Có Reasoning.

□ Có Meaning.

□ Có Impact.

□ Có Recommendation.

□ Có Closing.

PASS

↓

YES / NO

---

# 12. Action Checklist

□ Có Decision.

□ Có Priority.

□ Có Action.

□ Có Warning.

□ Không Prediction.

PASS

↓

YES / NO

---

# 13. Rewrite Checklist

□ Không đổi Meaning.

□ Đúng Language.

□ Đúng Grammar.

□ Đúng Template.

PASS

↓

YES / NO

---

# 14. Language Checklist

□ Không Technical.

□ Không Engine.

□ Không JSON.

□ Không Rule.

□ Không Matcher.

PASS

↓

YES / NO

---

# 15. Sentence Checklist

□ Đúng Sentence.

□ Không Duplicate.

□ Đúng Category.

□ Đúng Priority.

PASS

↓

YES / NO

---

# 16. Grammar Checklist

□ Đúng Flow.

□ Có Transition.

□ Có Closing.

□ Không nhảy ý.

PASS

↓

YES / NO

---

# 17. Template Checklist

□ Đúng Slot.

□ Không Slot thừa.

□ Không Slot thiếu.

PASS

↓

YES / NO

---

# 18. Safety Checklist

□ Không Prediction.

□ Không Fear.

□ Không Hung/Cát.

□ Không Tuyệt đối.

PASS

↓

YES / NO

---

# 19. Customer Checklist

□ Khách hàng hiểu.

□ Không cần biết Bát Tự.

□ Không cần biết Rule.

□ Không cần biết Engine.

PASS

↓

YES / NO

---

# 20. Commercial Checklist

□ Có giá trị.

□ Có Insight.

□ Có Action.

□ Không giáo trình.

PASS

↓

YES / NO

---

# 21. Duplicate Checklist

□ Summary.

Không lặp.

Interpretation.

□ Interpretation.

Không lặp.

Action.

PASS

↓

YES / NO

---

# 22. Traceability Checklist

□ Narrative.

↓

Knowledge.

↓

Evidence.

↓

Canonical.

PASS

↓

YES / NO

---

# 23. Performance Checklist

□ Deterministic.

□ Reusable.

□ Serializable.

PASS

↓

YES / NO

---

# 24. Runtime Checklist

□ Runtime.

Đúng.

□ Freeze.

Đúng.

□ Publish.

Đúng.

PASS

↓

YES / NO

---

# 25. Builder Checklist

□ Summary Builder.

PASS.

□ Interpretation Builder.

PASS.

□ Action Builder.

PASS.

□ Commercial Builder.

PASS.

---

# 26. Consumer Checklist

□ Dashboard.

PASS.

□ PDF.

PASS.

□ DOCX.

PASS.

□ REST.

PASS.

---

# 27. Validation Checklist

□ Schema.

PASS.

□ Semantic.

PASS.

□ Grammar.

PASS.

□ Safety.

PASS.

---

# 28. Test Checklist

□ Unit.

PASS.

□ Integration.

PASS.

□ Snapshot.

PASS.

□ Regression.

PASS.

□ Acceptance.

PASS.

---

# 29. Executive Summary Checklist

□ Đọc.

↓

Hiểu.

↓

Tin.

↓

Muốn đọc tiếp.

PASS

↓

YES / NO

---

# 30. Interpretation Checklist

□ Có mạch.

□ Có giải thích.

□ Có Meaning.

□ Không giáo trình.

PASS

↓

YES / NO

---

# 31. Action Checklist

□ Biết làm gì.

□ Biết ưu tiên.

□ Không chung chung.

PASS

↓

YES / NO

---

# 32. Language Checklist

□ Một giọng văn.

□ Không lẫn.

□ Không kỹ thuật.

PASS

↓

YES / NO

---

# 33. Rewrite Checklist

□ Dễ hiểu hơn.

□ Không đổi Meaning.

PASS

↓

YES / NO

---

# 34. Product Owner Review

Product Owner phải trả lời:

Narrative này.

Có giống:

Một chuyên gia.

đang tư vấn.

không?

Nếu:

Không.

↓

FAIL.

---

# 35. Customer Review

Khách hàng đọc.

↓

Có hiểu.

↓

Có Action.

↓

Có niềm tin.

Nếu:

Không.

↓

FAIL.

---

# 36. Release Checklist

□ Dashboard.

PASS.

□ PDF.

PASS.

□ DOCX.

PASS.

□ REST.

PASS.

□ Mobile.

PASS.

---

# 37. Quality Gate

Narrative.

Chỉ được Release khi:

Tất cả.

Critical.

PASS.

---

# 38. Acceptance Matrix

| Layer | PASS |
|--------|------|
| Architecture | □ |
| Data | □ |
| API | □ |
| Pipeline | □ |
| Summary | □ |
| Interpretation | □ |
| Action | □ |
| Rewrite | □ |
| Language | □ |
| Validation | □ |

---

# 39. Release Decision

Nếu.

Critical.

PASS.

↓

Release.

Nếu.

Critical.

FAIL.

↓

Reject.

---

# 40. Final Checklist

Product Owner chỉ cần trả lời.

```
Narrative này.

Mình có sẵn sàng gửi cho khách hàng thật không?
```

Nếu:

Không.

↓

Không Publish.

---

# 41. Narrative Quality Gate

Narrative chỉ được phép Publish khi đồng thời đạt bốn tầng chất lượng.

```
Correct

↓

Understandable

↓

Useful

↓

Trustworthy
```

Thiếu một tầng.

↓

Không Publish.

---

# 42. Product Owner Questions

Trước khi Release, Product Owner phải trả lời:

1.

Khách hàng có hiểu không?

2.

Khách hàng có tin không?

3.

Khách hàng có biết mình nên làm gì không?

4.

Narrative có giống một buổi tư vấn thật không?

5.

Nếu chính mình là khách hàng, mình có hài lòng không?

Nếu bất kỳ câu nào trả lời:

Không.

↓

Release bị chặn.

---

# 43. Acceptance Matrix

| Tiêu chí | PASS |
|-----------|:---:|
| Correctness | □ |
| Clarity | □ |
| Consistency | □ |
| Commercial Value | □ |
| Customer Experience | □ |
| Reusability | □ |
| Maintainability | □ |
| Traceability | □ |

Tất cả phải PASS.

---

# 44. Release Governance

Không ai được phép bỏ qua Acceptance Checklist.

Ngay cả khi:

- Test PASS.
- Validation PASS.
- UI đẹp.

Narrative vẫn không được Publish nếu Product Owner chưa PASS.

Acceptance Checklist là cổng kiểm duyệt cuối cùng.

---

# 45. Final Acceptance Principle

Narrative V2 không được Release vì:

"Code đã chạy."

Narrative V2 chỉ được Release khi:

- hệ thống nói đúng;
- khách hàng hiểu đúng;
- chuyên gia đồng ý;
- Product Owner sẵn sàng chịu trách nhiệm Publish.

> **Một Narrative chỉ thực sự hoàn thành khi Product Owner sẵn sàng đặt tên của mình lên đó và gửi cho khách hàng.**

Đó là tiêu chuẩn cao nhất của Narrative V2.