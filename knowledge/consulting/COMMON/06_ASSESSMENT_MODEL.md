# COMMON — CONSULTING FRAMEWORK

# 06_ASSESSMENT_MODEL.md

Document ID: COMMON-06

Version: 1.0

Status: DRAFT FOR PRODUCT OWNER REVIEW

---

# 1. Purpose

Định nghĩa Assessment Model của toàn bộ Consulting Framework.

Assessment là tầng công bố kết quả ngữ nghĩa cho khách hàng.

Assessment trả lời:

"Câu trả lời là gì?"

Recommendation trả lời:

"Nên làm gì?"

Assessment không phải Decision.

Assessment không phải Recommendation.

Assessment không phải Narrative.

Assessment là:

Executive Interpretation của một Decision đã hoàn tất.

---

# 2. Architecture Position

Assessment đứng giữa Decision và Recommendation.

Canonical pipeline:

```
Truth
        │
        ▼
Evidence
        │
        ▼
Finding
        │
        ▼
Decision
        │
        ▼
Assessment
        │
        ▼
Recommendation
        │
        ▼
Narrative
        │
        ▼
Report
        │
        ▼
Presentation
```

Assessment là public semantic contract.

Decision là internal semantic contract.

Khách hàng không mua Evidence.

Khách hàng không mua Finding.

Khách hàng không mua Decision.

Khách hàng mua Decision Assessment.

---

# 3. Assessment Philosophy

Assessment trả lời câu hỏi nghiệp vụ của khách hàng.

Recommendation trả lời hành động của khách hàng.

Hai tầng này không được trộn.

## 3.1 Assessment never contains action plans

Assessment không chứa:

- việc cần làm;
- kế hoạch hành động;
- bước thực thi;
- lời khuyên "nên / không nên làm".

## 3.2 Recommendation never contains compatibility conclusions

Recommendation không chứa:

- kết luận tương hợp;
- kết luận hỗ trợ lẫn nhau;
- kết luận ổn định;
- kết luận tổng thể của Assessment.

Nếu một câu vừa là kết luận vừa là hành động:

↓

FAIL.

Phải tách thành:

Assessment Object

và

Recommendation Object.

---

# 4. Assessment Model

Assessment là phép chiếu (Projection) của Decision.

```
Decision
        │
        ▼
Assessment Projector
        │
        ▼
Assessment Result
```

Assessment phải:

- đọc Decision đã hoàn tất;
- trả lời đúng bộ câu hỏi của module;
- giữ nguyên Evidence;
- giữ nguyên Finding;
- giữ nguyên Decision.

Assessment không được:

- tạo Decision;
- sửa Decision;
- đổi Evidence;
- đổi Finding;
- đổi Score;
- đổi Grade;
- đổi Canonical Truth.

Nếu Decision thay đổi.

Assessment phải thay đổi.

Nếu Assessment thay đổi mà Decision không đổi.

↓

FAIL.

Đó không phải Assessment.

Đó là Decision mới trá hình.

---

# 5. Assessment Objects

Assessment Result gồm:

Assessment ID

Module ID

Question Set ID

Answers

Overall Assessment

Support Status

Confidence

Explainability Trace

Source Decision ID

Version Bundle

Metadata

Mỗi Answer là một Assessment Answer Object.

---

# 6. Assessment Answer Object

Mỗi câu trả lời khách hàng là một Object riêng.

Assessment Answer gồm:

Question ID

Question Label

Answer State

Answer Level

Direction

Headline

Explanation

Support Status

Main Risk

Main Rescue

Source Decision References

Source Finding References

Confidence

Version

Score là optional.

Score không phải Answer.

Nếu module không công bố Score.

Answer vẫn hợp lệ.

---

# 7. Assessment Projection

Projection là ánh xạ:

```
Decision Domains
        │
        ▼
Customer Questions
```

Không phải ánh xạ:

```
Customer Questions
        │
        ▼
Decision Domains
```

Decision hoàn tất trước.

Câu hỏi khách hàng được trả lời sau.

Mỗi Answer phải truy được về:

một hoặc nhiều Domain Decision

và

một hoặc nhiều Finding

và

một hoặc nhiều Evidence.

Không có Answer mồ côi.

Không có Answer từ Narrative.

Không có Answer từ Recommendation.

---

# 8. Assessment Categories

Framework chuẩn hóa bốn nhóm Assessment.

Không module nào được invent category ngoài các nhóm này mà không mở rộng COMMON.

## 8.1 Compatibility Assessment

Trả lời mức độ phù hợp / tương hợp.

Dùng cho:

TV-01 Marriage

TV-02 Business Cooperation

## 8.2 Capacity Assessment

Trả lời năng lực / vai trò / phù hợp nghề.

Dùng cho:

TV-03 Career

## 8.3 Stability Assessment

Trả lời khả năng ổn định, rủi ro chính, yếu tố cứu giải.

Dùng cho:

TV-01 Marriage

TV-02 Business

TV-04 Child

## 8.4 Overall Assessment

Tổng kết executive.

Mọi module phải có Overall Assessment.

Overall Assessment không được copy nguyên Decision Summary.

Overall Assessment phải trả lời đúng câu hỏi tổng thể của module.

---

# 9. Question Set Contract

Mỗi Consulting Module phải công bố:

một Question Set đóng.

Question Set:

- hữu hạn;
- đánh số;
- không đổi thứ tự công bố;
- versioned.

TV-01 Question Set:

Q1 Overall Compatibility

Q2 Mutual Support

Q3 Personality Balance

Q4 Marriage Stability

Q5 Children

Q6 Overall Marriage Assessment

TV-02, TV-03, TV-04 Question Set được định nghĩa tại template của từng module.

Không module nào được:

trả lời câu hỏi ngoài Question Set

mà không version Question Set mới.

---

# 10. Semantic Levels

Assessment dùng semantic level, không dùng jargon Decision.

Ví dụ hợp lệ:

Strong Support

Balanced

Mixed

Conflict Dominant

Insufficient Evidence

Unsupported

Ví dụ không hợp lệ khi công bố cho khách hàng:

Domain State enum nội bộ

Finding Class kỹ thuật

Evidence Type

Rule ID

Score có thể đi kèm.

Score không thay thế semantic level.

---

# 11. Directional Assessment

Khi câu hỏi có chiều:

A → B

B → A

Assessment phải giữ hướng.

Không được gộp thành:

"Hai người hỗ trợ nhau."

nếu Decision phân biệt chiều.

Vượng Phu / Vượng Thê

và mọi nhãn tương đương

chỉ được công bố khi Canonical Evidence hỗ trợ.

Nếu không hỗ trợ.

↓

Support Status = unsupported

Không suy diễn.

---

# 12. Unsupported Answers

Không phải câu hỏi nào cũng luôn trả lời được.

Nếu Decision không đủ Evidence:

Answer State = unsupported

hoặc

insufficient_evidence

Không được:

- bịa câu trả lời;
- đoán fertility;
- đoán số con;
- đoán tuyệt đối "sẽ / không sẽ".

Unsupported là kết quả hợp lệ.

---

# 13. Assessment Versioning

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

Cùng Assessment.

Nếu Question Set đổi.

Assessment Version phải tăng.

Không được tái sử dụng Answer ID cũ cho câu hỏi mới.

Chi tiết versioning:

COMMON/12_VERSIONING_STANDARD.md

---

# 14. Assessment Validation

Assessment Validation kiểm tra:

- Decision đã complete trước khi project;
- mọi Answer thuộc Question Set;
- không thiếu Question bắt buộc;
- không có action plan trong Assessment;
- không có compatibility conclusion trong Recommendation;
- mọi Answer có source Decision / Finding;
- directional answers giữ hướng;
- unsupported không bị nâng thành conclusion;
- Overall Assessment không mâu thuẫn Answer thành phần;
- Assessment không sửa Decision.

FAIL nếu Assessment tạo Decision mới.

Chi tiết validation:

COMMON/11_VALIDATION_STANDARD.md

---

# 15. Assessment Explainability

Mọi Assessment Answer phải truy ngược:

```
Customer Answer
        │
        ▼
Assessment Object
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
Canonical Truth
```

Khách hàng nhìn Answer.

Audit nhìn Trace.

Narrative chỉ mô tả Assessment.

Narrative không phải nguồn Explainability.

---

# 16. Public Semantic Contract

Public API, Report, UI, PDF, DOCX

công bố:

Assessment

Không công bố mặc định:

Decision nội bộ

Evidence Graph

Finding Graph

Rule Engine

Decision vẫn tồn tại.

Decision phục vụ:

Audit

Validation

Reproducibility

Internal Explainability

Decision không phải mặt hàng khách hàng đọc đầu tiên.

---

# 17. Relationship to Other Layers

## Decision

Tạo kết luận nội bộ.

Không trả lời câu hỏi khách hàng.

## Assessment

Chiếu Decision thành câu trả lời khách hàng.

Không tạo kết luận mới.

## Recommendation

Sinh hành động từ Assessment.

Không lặp lại kết luận Assessment.

## Narrative

Truyền đạt Assessment và Recommendation.

Không tạo Assessment.

## Report

Sắp xếp:

Assessment

↓

Detailed Analysis

↓

Recommendations

↓

Appendix

## Presentation

Hiển thị Assessment trước.

Detailed Analysis sau.

Collapsed by default nếu là phân tích kỹ thuật.

---

# 18. Assessment Freeze Rules

Assessment Model chỉ được FREEZE khi:

- [ ] Pipeline có Assessment giữa Decision và Recommendation.
- [ ] Assessment là public semantic contract.
- [ ] Decision không còn là mặt hàng công bố mặc định.
- [ ] Assessment không tạo / sửa Decision.
- [ ] Assessment không chứa action plan.
- [ ] Recommendation không chứa compatibility conclusion.
- [ ] Mọi module có Question Set đóng.
- [ ] Projection deterministic.
- [ ] Explainability đầy đủ.
- [ ] Unsupported được mô hình hóa.
- [ ] Versioned.
- [ ] TV-01, TV-02, TV-03, TV-04 dùng cùng Assessment Model.

Sau FREEZE.

Không được:

đưa Decision ra mặt public

thay cho Assessment.

---

# 19. Migration Rules

Implementation chưa được phép chạy cho đến khi Product Owner phê duyệt ticket này.

Khi implementation được mở:

1. Giữ nguyên Canonical Mathematics.
2. Giữ nguyên Decision Mathematics.
3. Giữ nguyên TV-01 Decision runtime hiện tại.
4. Thêm Assessment Projector sau Decision.
5. Chuyển Public API / Report / UI sang Assessment.
6. Recommendation đọc Assessment, không đọc Decision như public contract.
7. D1–D8 chuyển xuống Detailed Analysis.
8. Golden Dataset Decision không sửa.
9. Không expose Decision enum kỹ thuật trên UI chính.

Không được:

viết lại Decision để "trả lời khách hàng".

Đó là trách nhiệm của Assessment.

---

# 20. Status

COMMON-06

STATUS

DRAFT FOR PRODUCT OWNER REVIEW

Next:

COMMON-07

07_RECOMMENDATION_MODEL.md
