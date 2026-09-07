# TV-01 — MARRIAGE CONSULTING
## 03A_ASSESSMENT_PROFILE.md

**Document ID:** TV-01-03A

**Module:** TV-01_MARRIAGE

**Product:** BTE Platform

**Document Type:** Marriage Assessment Profile

**Status:** DRAFT FOR PRODUCT OWNER REVIEW

**Version:** 1.0

**Depends on:** COMMON/06_ASSESSMENT_MODEL.md

---

# 1. Purpose

Tài liệu này định nghĩa Marriage Assessment Question Set của TV-01.

Marriage Assessment là Question-driven projection của Decision.

Không phải Executive Summary.

TV-01 không còn công bố Decision trực tiếp.

Decision Profile (`03_DECISION_PROFILE.md`) vẫn là hợp đồng nội bộ.

Assessment Profile là hợp đồng khách hàng.

---

# 2. Architecture Position

```
                    Marriage Decision
                   /                 \
         Marriage Assessment    Recommendation
                   \                 /
                         Narrative
                             ↓
                       Report / UI
```

Assessment và Recommendation là siblings.

Cả hai chỉ consume Decision.

Assessment không tạo Recommendation.

Recommendation không consume Assessment.

Assessment không sửa D1–D8.

D1–D8 chuyển xuống Detailed Analysis.

---

# 3. Customer Contract

TV-01 Assessment MUST trả lời đúng sáu câu hỏi sau.

Không thêm.

Không bớt.

Không đổi thứ tự công bố.

---

# 4. Question 1 — Overall Compatibility

Câu hỏi:

How compatible are the two charts?

Assessment trả lời bằng semantic level.

Ví dụ:

Strong Compatibility

Balanced Compatibility

Mixed Compatibility

Conflict Dominant

Insufficient Evidence

Score là optional.

Score không thay thế semantic level.

Không công bố Domain State kỹ thuật thay cho câu trả lời này.

---

# 5. Question 2 — Mutual Support

Câu hỏi:

Who supports whom?

Who benefits more?

Assessment phải giữ hướng:

A → B

B → A

Không được gộp thành một chiều trung tính nếu Decision phân biệt chiều.

Vượng Phu

Vượng Thê

chỉ được công bố nếu Canonical Evidence hỗ trợ.

Nếu không hỗ trợ:

Support Status = unsupported

Không suy diễn nhãn.

---

# 6. Question 3 — Personality Balance

Câu hỏi:

Hai Nhật Chủ và cấu trúc vai trò cân bằng thế nào?

Assessment so sánh:

Day Master A

Day Master B

role structure

và giải thích bằng ngôn ngữ khách hàng:

balance

difference

complement

conflict

Không giảng Can Chi như máy tính.

Không đưa action plan vào câu này.

---

# 7. Question 4 — Marriage Stability

Câu hỏi:

Can the relationship become stable?

Assessment phải chỉ:

main conflict

main risk

main rescue

Main conflict thuộc một trong các nhóm:

money

communication

personality

responsibility

values

role

hoặc nhóm khác đã có Evidence.

Không liệt kê mọi xung đột ngang hàng.

Không biến Stability thành Recommendation.

---

# 8. Question 5 — Children

Câu hỏi:

Hài hòa liên quan con cái / gia đạo thế nào?

Chỉ đánh giá nếu Evidence hỗ trợ.

Cấm:

- dự đoán sinh sản;
- dự đoán số con;
- kết luận "sẽ có / không có con".

Chỉ được trả lời:

parenting compatibility

family support

child-related harmony

Nếu không đủ Evidence:

unsupported

---

# 9. Question 6 — Overall Marriage Assessment

Câu hỏi tổng kết.

Assessment phải tóm tắt:

Relationship

Financial cooperation

Long-term cooperation

Growth potential

Overall conclusion

Overall Marriage Assessment là Question.

Không phải Executive Summary của Report.

Overall không được mâu thuẫn Q1–Q5 vì cùng Decision.

Overall không được chứa action plan.

---

# 10. Marriage Assessment Object

```text
MarriageAssessment
  assessment_id
  consultation_id
  question_set_id = TV-01-QSET-1.0
  answers
    Q1 Overall Compatibility
    Q2 Mutual Support
    Q3 Personality Balance
    Q4 Marriage Stability
    Q5 Children
    Q6 Overall Marriage Assessment
  overall
  confidence
  source_decision_id
  explainability_trace
  versions
```

Mỗi Answer là object, không phải câu văn:

```text
question_id
question
semantic_answer
confidence
supporting_findings
conflicting_findings
conditions
limitations
version
trace_reference
direction?          # bắt buộc với Q2
score?              # optional
```

---

# 11. Projection Rules

Q1 chiếu từ Overall Decision + compatibility structure.

Q2 chiếu từ directional support findings.

Q3 chiếu từ Day Master / role / personality findings.

Q4 chiếu từ conflict / rescue / stability findings.

Q5 chiếu từ children / family findings khi available.

Q6 chiếu từ Overall Decision, không tóm tắt Report, không consume Q1–Q5 như nguồn.

Q6 phải nhất quán với Q1–Q5 vì cùng Decision.

Không Question nào được sinh từ Narrative.

Không Question nào được sinh từ Recommendation.

---

# 12. Detailed Analysis

D1 Five Elements

D2 Stem / Branch

D3 Ten Gods

D4 Interaction

D5 Finance

D6 Family

D7 Children

D8 Luck / Timing

vẫn tồn tại.

Nhưng:

đứng dưới Assessment.

đổi tên section công bố:

Detailed Analysis

Collapsed by default.

Assessment first.

Evidence later.

Detailed Analysis không được đẩy Assessment xuống dưới.

---

# 13. Report Order

Marriage Assessment

↓

Detailed Analysis

↓

Recommendations

↓

Appendix

Không đảo.

---

# 14. UI Order

Top of page:

Marriage Assessment

Six cards.

Q1 Q2 Q3 Q4 Q5 Q6

Only after that:

Detailed Analysis

Recommendations không được chiếm vị trí Assessment.

---

# 15. Boundary Rules

Assessment MUST NOT:

create Decision

modify Decision

change Evidence

change Finding

create Recommendation

read Recommendation

summarize the Report

Recommendation MUST NOT:

consume Assessment

contain compatibility conclusions

contain Vượng Phu / Vượng Thê as a new conclusion

repeat Q6 as an action

---

# 16. Validation

FAIL nếu:

- thiếu một trong sáu câu;
- đổi thứ tự công bố;
- Q2 không có hướng;
- Q5 dự đoán fertility hoặc số con;
- Assessment chứa action plan;
- Assessment đọc hoặc tạo Recommendation;
- Recommendation consume Assessment;
- UI công bố Decision thay Assessment;
- Detailed Analysis đứng trước Assessment.

PASS khi:

sáu câu trả lời đều truy được về Decision đã freeze của cùng consultation.

---

# 17. Status

TV-01-03A

STATUS

DRAFT FOR PRODUCT OWNER REVIEW

Implementation code MUST NOT thay đổi cho đến khi Product Owner phê duyệt.
