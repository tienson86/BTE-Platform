# NARRATIVE V2 — VALIDATION RULES

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Validation Rules định nghĩa toàn bộ quy tắc kiểm tra Narrative trước khi Publish.

Không có Narrative nào được Publish nếu chưa vượt qua Validation.

Validation là cổng kiểm soát chất lượng cuối cùng của Narrative V2.

---

# 2. Mission

Validation trả lời:

> Narrative này có đủ chất lượng để khách hàng đọc hay chưa?

Validation không sửa Narrative.

Validation chỉ:

PASS

hoặc

FAIL.

---

# 3. Validation Philosophy

Narrative đúng không có nghĩa là Narrative được Publish.

Narrative chỉ được Publish khi:

✓ đúng

✓ dễ hiểu

✓ an toàn

✓ nhất quán

✓ có thể hành động

---

# 4. Validation Position

```
Evidence
        ↓
Reasoning
        ↓
Knowledge
        ↓
Rewrite
        ↓
Builders
        ↓
Validation
        ↓
Publish
```

Validation luôn chạy sau tất cả Builder.

---

# 5. Validation Formula

```
Schema

↓

Semantic

↓

Language

↓

Grammar

↓

Template

↓

Safety

↓

Duplicate

↓

Presentation

↓

Publish
```

Không được bỏ Stage.

---

# 6. Validation Categories

Validation gồm:

- Schema Validation
- Semantic Validation
- Language Validation
- Grammar Validation
- Template Validation
- Rewrite Validation
- Customer Safety Validation
- Duplicate Validation
- Presentation Validation
- Publish Validation

---

# 7. Schema Validation

Kiểm tra:

✓ Object tồn tại

✓ Field đúng

✓ Type đúng

✓ Version đúng

Nếu sai.

↓

FAIL.

---

# 8. Semantic Validation

Kiểm tra:

Meaning có thay đổi không.

Ví dụ.

```
Thân vượng

↓

Bạn có nội lực tốt.
```

PASS.

---

```
Thân vượng

↓

Bạn chắc chắn thành công.
```

FAIL.

---

# 9. Language Validation

Kiểm tra:

Language Standard.

Không:

- kỹ thuật
- Engine
- JSON

---

# 10. Grammar Validation

Kiểm tra.

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

Không được thiếu.

---

# 11. Template Validation

Kiểm tra:

Slot.

Order.

Structure.

---

# 12. Rewrite Validation

Rewrite.

Có giữ Meaning không?

Không đổi.

↓

PASS.

---

# 13. Customer Safety Validation

Không:

Prediction.

Không:

Fear.

Không:

Absolute.

---

# 14. Duplicate Validation

Không lặp.

Overview.

Interpretation.

Action.

---

# 15. Presentation Validation

Không:

JSON.

Rule.

Engine.

Debug.

---

# 16. Publish Validation

Kiểm tra.

✓ Narrative đầy đủ.

↓

Publish.

---

# 17. Validation Objects

Validator nhận:

```
NarrativeV2Presentation
```

Không đọc UI.

---

# 18. Validation Scope

Validation kiểm tra:

Overview.

Interpretation.

Action.

Commercial.

---

# 19. Validation Status

```
pass

warning

fail
```

---

# 20. Hard Fail Rules

Các lỗi sau luôn FAIL:

- JSON
- Engine ID
- Rule ID
- Meaning Changed
- Missing Required Block
- Invalid Grammar

---

# 21. Soft Warning Rules

Ví dụ.

```
Đoạn quá dài.
```

↓

Warning.

Không Fail.

---

# 22. Schema Rules

Object.

Không đúng Schema.

↓

FAIL.

---

# 23. Meaning Rules

Một Meaning.

↓

Một Meaning.

Không Rewrite.

↓

Meaning mới.

---

# 24. Language Rules

Không dùng:

```
Matcher

Priority

Rule

JSON
```

---

# 25. Style Rules

Style.

Theo:

Language Standard.

---

# 26. Grammar Rules

Không được:

Observation

↓

Action.

Không Reasoning.

---

# 27. Decision Rules

Action.

Không có Decision.

↓

FAIL.

---

# 28. Action Rules

Action.

Không Generic.

Không Prediction.

---

# 29. Recommendation Rules

Recommendation.

Không Action.

---

# 30. Summary Rules

Summary.

Không Action.

Không Prediction.

---

# 31. Closing Rules

Closing.

Không mở ý mới.

---

# 32. Consumer Rules

Dashboard.

Không Validation.

Narrative Validation.

Chỉ chạy.

Một lần.

---

# 33. Validation Matrix

| Validation | Mục tiêu |
|------------|----------|
| Schema | Đúng cấu trúc |
| Semantic | Đúng ý nghĩa |
| Language | Đúng ngôn ngữ |
| Grammar | Đúng dòng tư duy |
| Template | Đúng bố cục |
| Rewrite | Không đổi Meaning |
| Safety | Không nguy hiểm |
| Duplicate | Không lặp |
| Presentation | Đúng Contract |

---

# 34. Validation Lifecycle

```
Builder

↓

Validation

↓

Freeze

↓

Publish
```

---

# 35. Validator Independence

Validator.

Không Rewrite.

Không Builder.

Không Engine.

---

# 36. Traceability Validation

Narrative.

↓

Knowledge.

↓

Evidence.

↓

Canonical.

Nếu không Trace.

↓

FAIL.

---

# 37. Performance Validation

Validation.

Deterministic.

---

# 38. Validation Events

```
Validation Started

↓

Schema Passed

↓

Semantic Passed

↓

Language Passed

↓

Grammar Passed

↓

Template Passed

↓

Safety Passed

↓

Duplicate Passed

↓

Presentation Passed

↓

Publish Allowed
```

---

# 39. Validation Checklist

Một Narrative đạt khi:

✓ Schema đúng.

✓ Meaning đúng.

✓ Language đúng.

✓ Grammar đúng.

✓ Template đúng.

✓ Safety đúng.

✓ Không Duplicate.

✓ Customer Safe.

---

# 40. Final Validation Principle

Validation không tồn tại để bắt lỗi.

Validation tồn tại để bảo vệ chất lượng Narrative.

Nếu Narrative chưa đủ tốt.

↓

Không Publish.

---

# 41. Validation Responsibility Matrix

| Thành phần | Trách nhiệm |
|------------|-------------|
| Schema Validator | Kiểm tra cấu trúc |
| Semantic Validator | Kiểm tra Meaning |
| Language Validator | Kiểm tra ngôn ngữ |
| Grammar Validator | Kiểm tra dòng tư duy |
| Template Validator | Kiểm tra cấu trúc trình bày |
| Rewrite Validator | Kiểm tra Rewrite |
| Safety Validator | Kiểm tra an toàn |
| Duplicate Validator | Kiểm tra trùng lặp |
| Presentation Validator | Kiểm tra Contract |
| Publish Validator | Quyết định Publish |

---

# 42. Validation Severity Matrix

Validation sử dụng ba mức độ.

| Level | Ý nghĩa | Publish |
|--------|----------|:-------:|
| PASS | Đạt | ✓ |
| WARNING | Có thể Publish | ✓ |
| FAIL | Không Publish | ✗ |

WARNING không được làm thay đổi Meaning.

FAIL luôn chặn Publish.

---

# 43. Validation Decision Tree

Narrative luôn đi qua cây quyết định sau:

```
Schema

↓

Semantic

↓

Language

↓

Grammar

↓

Template

↓

Safety

↓

Duplicate

↓

Presentation

↓

PASS?

↓

Publish

FAIL?

↓

Reject
```

Không có đường tắt.

---

# 44. Validation Governance

Không Validator nào được:

- Rewrite Narrative.
- Tự sửa Meaning.
- Tự thêm Sentence.
- Tự thêm Action.

Validator chỉ có quyền:

PASS

WARNING

FAIL

Mọi sửa chữa phải quay lại đúng Builder tương ứng.

---

# 45. Final Validation Principle

Narrative V2 không đánh giá chất lượng bằng số lượng câu.

Narrative V2 đánh giá chất lượng bằng:

- sự đúng đắn của Meaning;
- sự rõ ràng của ngôn ngữ;
- sự nhất quán của Narrative;
- khả năng giúp khách hàng hiểu và hành động.

Nếu Narrative vượt qua tất cả Validation Rules, nó mới được phép trở thành tiếng nói chính thức của BTE Platform.

> **Engine bảo vệ sự thật.**

> **Narrative bảo vệ sự thấu hiểu.**

> **Validation bảo vệ chất lượng của sự thấu hiểu đó.**