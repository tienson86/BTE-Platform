# TV-03 — CAREER
## 00_ASSESSMENT_TEMPLATE.md

**Document ID:** TV-03-00

**Module:** TV-03_CAREER

**Product:** BTE Platform

**Document Type:** Reusable Assessment Template

**Status:** DRAFT TEMPLATE — NOT A PRODUCT BUILD

**Version:** 1.0

**Depends on:** COMMON/06_ASSESSMENT_MODEL.md

---

# 1. Purpose

Tài liệu này khóa Question Set Assessment của TV-03.

TV-03 chưa được implement trong ticket này.

Template này chỉ định nghĩa câu hỏi khách hàng mà Assessment phải trả lời.

Không được công bố Decision trực tiếp.

---

# 2. Product Question

Khách hàng mua:

Career Assessment

Không mua:

Evidence

Finding

Decision

---

# 3. Canonical Position

```
                    Decision
                   /        \
         Assessment      Recommendation
```

Assessment = "What does the customer want to know?"

Recommendation = "What should the customer do?"

Hai tầng độc lập.

Cả hai chỉ consume Decision.

---

# 4. TV-03 Question Set

TV-03 Assessment MUST trả lời đúng sáu câu hỏi sau.

## Q1 Career suitability

Phù hợp nghề / hướng nghề đến đâu.

Semantic level.

Score optional.

## Q2 Leadership

Năng lực / xu hướng lãnh đạo.

Không phải action "nên làm sếp".

## Q3 Entrepreneurship

Xu hướng khởi nghiệp / tự chủ.

Không phải kế hoạch mở công ty.

## Q4 Strengths

Điểm mạnh nghề nghiệp executive.

## Q5 Weaknesses

Điểm yếu / điểm nghẽn executive.

Không biến thành checklist việc cần làm.

Việc cần làm thuộc Recommendation.

## Q6 Overall career assessment

Tóm tắt:

Suitability

Leadership

Entrepreneurship

Strengths

Weaknesses

Overall conclusion

---

# 5. Public Surface

Report / UI bắt đầu bằng:

Career Assessment

Six cards.

Detailed Analysis collapsed by default.

Recommendations after Assessment.

---

# 6. Freeze Note

Question Set này là reusable template.

Thay đổi câu hỏi = tăng Question Set Version.

Không implement runtime trong ticket R1.
