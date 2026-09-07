# COMMON — CONSULTING FRAMEWORK

# 06_ASSESSMENT_MODEL.md

Document ID: COMMON-06

Version: 1.1

Status: DRAFT FOR PRODUCT OWNER REVIEW

---

# 1. Purpose

Định nghĩa Assessment Engine của toàn bộ Consulting Framework.

Assessment không phải Executive Summary.

Assessment không phải Executive Interpretation.

Assessment là:

Question-driven Projection Engine.

Assessment trả lời:

"Khách hàng muốn biết điều gì?"

Recommendation trả lời:

"Khách hàng nên làm gì?"

Narrative giải thích cả hai.

Hai tầng Assessment và Recommendation độc lập.

Không tầng nào được consume tầng kia.

---

# 2. Architecture Position

Decision tách thành hai phép chiếu độc lập.

```
                    Decision
                   /        \
                  /          \
         Assessment      Recommendation
                  \          /
                   \        /
                  Narrative
                      ↓
                   Report
                      ↓
                Presentation
```

Assessment và Recommendation là siblings.

Cả hai chỉ được consume:

Decision.

Assessment must never create Recommendation.

Recommendation must never consume Assessment.

Pipeline bị từ chối:

```
Decision → Assessment → Recommendation → Narrative
```

---

# 3. Assessment Philosophy

Assessment answers customer questions.

Assessment does NOT summarize the report.

Assessment does NOT create action plans.

Recommendation never contains compatibility conclusions.

Assessment never contains action plans.

Nếu một câu vừa là kết luận vừa là hành động:

↓

FAIL.

Phải tách thành hai Object độc lập.

Cả hai truy về cùng Decision.

Không truy về nhau.

---

# 4. Question Engine

Framework project theo:

```
Decision
        │
        ▼
Assessment Question Set
        │
        ▼
Projection Rules
        │
        ▼
Assessment Answers
```

Question Set là public semantic contract.

Framework giữ generic.

Chỉ Question Set đổi theo module.

Không module nào được:

đổi Assessment Engine

để phù hợp sản phẩm.

Chỉ được:

đổi Question Set.

---

# 5. Assessment Engine definition

Assessment Engine nhận:

Decision đã hoàn tất

+

Assessment Question Set

+

Projection Rules

Output:

Assessment Answers

Assessment Engine không được:

- tạo Decision;
- sửa Decision;
- đổi Evidence;
- đổi Finding;
- tạo Recommendation;
- đọc Recommendation;
- tóm tắt Report;
- viết action plan.

Nếu Decision thay đổi.

Assessment phải thay đổi.

Nếu Assessment thay đổi mà Decision không đổi.

↓

FAIL.

Đó không phải Assessment.

Đó là Decision mới trá hình.

---

# 6. Assessment Answer Object

Assessment Answer là object.

Không phải câu văn.

Mỗi Answer phải chứa:

Question ID

Question

Semantic Answer

Confidence

Supporting Findings

Conflicting Findings

Conditions

Limitations

Version

Trace Reference

Score là optional.

Score không phải Semantic Answer.

Headline / customer wording thuộc Narrative.

Không thuộc Assessment Answer bắt buộc.

---

# 7. Assessment Result

Assessment Result gồm:

Assessment ID

Module ID

Question Set ID

Question Set Version

Answers

Source Decision ID

Version Bundle

Metadata

Không chứa Recommendation.

Không chứa Narrative.

Không chứa Report Summary.

---

# 8. Projection Rules

Mỗi Question có Projection Rule.

Projection Rule ánh xạ:

Decision Findings / Domain States

↓

Semantic Answer

cho đúng Question ID.

Decision hoàn tất trước.

Question được trả lời sau.

Không đảo:

```
Question → invent Decision
```

Mỗi Answer phải truy được về:

Decision

Finding

Evidence

Truth

Không có Answer từ Recommendation.

Không có Answer từ Narrative.

Không có Answer mồ côi.

---

# 9. Question Set Contract

Mỗi Consulting Module công bố một Question Set đóng.

Question Set:

- hữu hạn;
- đánh số;
- versioned;
- không đổi thứ tự công bố nếu chưa tăng version.

Framework không định nghĩa sẵn Assessment Categories.

Question Set thay thế Categories.

TV-01, TV-02, TV-03, TV-04 chỉ khác nhau ở Question Set.

---

# 10. Semantic Answer

Semantic Answer dùng mức ngữ nghĩa.

Ví dụ hợp lệ:

Strong Support

Balanced

Mixed

Conflict Dominant

Insufficient Evidence

Unsupported

Không công bố:

Domain State enum nội bộ

Finding Class kỹ thuật

Evidence Type

Rule ID

làm câu trả lời khách hàng.

---

# 11. Directional Questions

Khi Question có chiều:

A → B

B → A

Answer phải giữ hướng.

Không gộp thành một chiều trung tính nếu Decision phân biệt chiều.

Vượng Phu / Vượng Thê

chỉ được điền khi Canonical Evidence hỗ trợ.

Nếu không hỗ trợ:

Limitations ghi unsupported.

Không suy diễn.

---

# 12. Conditions and Limitations

Conditions:

điều kiện Decision cho phép trả lời Question.

Limitations:

phạm vi không được vượt.

Ví dụ hợp lệ:

insufficient_evidence

hour_missing

children_unsupported

canonical_label_unsupported

Unsupported là Answer hợp lệ.

Không được bịa fertility, số con, hay kết luận tuyệt đối khi Decision không hỗ trợ.

---

# 13. Independent Traceability

Assessment và Recommendation truy ngược độc lập.

```
Assessment Answer
        │
        ▼
Decision
        │
        ▼
Finding
        │
        ▼
Evidence
        │
        ▼
Truth
```

```
Recommendation
        │
        ▼
Decision
        │
        ▼
Finding
        │
        ▼
Evidence
        │
        ▼
Truth
```

Không tồn tại:

```
Recommendation → Assessment → Decision
```

Không tồn tại:

```
Assessment → Recommendation
```

---

# 14. TV-01 Question Set

Question Set ID:

TV-01-QSET-1.0

Q1 Overall Compatibility

Q2 Mutual Support

- A → B
- B → A
- Vượng Phu
- Vượng Thê
- chỉ khi Canonical hỗ trợ

Q3 Personality Balance

Q4 Marriage Stability

Q5 Children

Q6 Overall Marriage Assessment

Overall Marriage Assessment là Question.

Không phải Executive Summary của Report.

---

# 15. TV-02 Question Set

Question Set ID:

TV-02-QSET-1.0

Q1 Should we cooperate?

Q2 Who complements whom?

Q3 Leadership balance?

Q4 Financial cooperation?

Q5 Business risks?

Q6 Overall Business Assessment?

---

# 16. TV-03 Question Set

Question Set ID:

TV-03-QSET-1.0

Q1 Career suitability

Q2 Leadership

Q3 Entrepreneurship

Q4 Strengths

Q5 Weaknesses

Q6 Overall Career Assessment

---

# 17. TV-04 Question Set

Question Set ID:

TV-04-QSET-1.0

Q1 Child Planning

Q2 Timing

Q3 Parent Support

Q4 Family Balance

Q5 Risks

Q6 Overall Child Assessment

---

# 18. Versioning

Assessment Version gồm:

Assessment Model Version

Question Set Version

Projection Version

Source Decision Version

Policy Version

Mathematics Version

Canonical Version

Cùng input.

Cùng version bundle.

↓

Cùng Assessment Answers.

Nếu Question Set đổi.

Question Set Version tăng.

Không tái sử dụng Answer ID cũ cho Question mới.

Chi tiết:

COMMON/12_VERSIONING_STANDARD.md

---

# 19. Validation

Assessment Validation kiểm tra:

- Decision complete trước khi project;
- mọi Answer thuộc Question Set;
- không thiếu Question bắt buộc;
- Answer là object, không phải câu văn thuần;
- đủ fields bắt buộc;
- không chứa action plan;
- không đọc Recommendation;
- không tạo Recommendation;
- directional answers giữ hướng;
- unsupported không bị nâng thành conclusion;
- Trace Reference tới Decision / Finding.

FAIL nếu Assessment tóm tắt Report thay vì trả lời Question.

Chi tiết:

COMMON/11_VALIDATION_STANDARD.md

---

# 20. Public Semantic Contract

Public API, Report, UI công bố:

Question Set

và

Assessment Answers

Không công bố mặc định:

Decision nội bộ

Evidence Graph

Finding Graph

Rule Engine

Decision phục vụ Audit, Validation, Reproducibility.

Question Set là mặt hàng khách hàng đọc.

---

# 21. Relationship to Other Layers

## Decision

Kết luận nội bộ.

Nguồn duy nhất cho Assessment và Recommendation.

## Assessment

Question-driven projection của Decision.

Không tóm tắt Report.

Không tạo hành động.

## Recommendation

Action projection của Decision.

Không consume Assessment.

Không chứa compatibility conclusions.

## Narrative

Giải thích Assessment và Recommendation.

Không tạo Answer.

Không tạo Action.

## Report / Presentation

Sắp xếp hai sibling outputs.

Thứ tự hiển thị không tạo dependency.

---

# 22. Freeze Rules

FREEZE khi:

- [ ] Assessment và Recommendation là siblings.
- [ ] Cả hai chỉ consume Decision.
- [ ] Assessment không tạo Recommendation.
- [ ] Recommendation không consume Assessment.
- [ ] Assessment là Question-driven Projection Engine.
- [ ] Assessment không phải Executive Summary.
- [ ] Assessment Answer là object đủ fields bắt buộc.
- [ ] Question Set là public semantic contract.
- [ ] Traceability độc lập.
- [ ] TV-01 / TV-02 / TV-03 / TV-04 chỉ khác Question Set.

---

# 23. Migration Rules

Không implement cho đến khi Product Owner phê duyệt R1A.

Khi implementation được mở:

1. Giữ Canonical Mathematics.
2. Giữ Decision Mathematics.
3. Giữ TV-01 Decision runtime.
4. Thêm Assessment Engine song song với Recommendation Engine.
5. Cả hai đọc Decision. Không đọc nhau.
6. Narrative consume cả hai.
7. Question Set trở thành public contract.
8. Golden Dataset Decision không sửa.

Không được:

xâu chuỗi Assessment → Recommendation.

---

# 24. Status

COMMON-06

STATUS

DRAFT FOR PRODUCT OWNER REVIEW

Next:

COMMON-07

07_RECOMMENDATION_MODEL.md
