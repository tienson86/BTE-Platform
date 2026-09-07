# TV-02 — BUSINESS COOPERATION
## 00_ASSESSMENT_TEMPLATE.md

**Document ID:** TV-02-00

**Module:** TV-02_BUSINESS

**Product:** BTE Platform

**Document Type:** Reusable Assessment Template

**Status:** DRAFT TEMPLATE — NOT A PRODUCT BUILD

**Version:** 1.0

**Depends on:** COMMON/06_ASSESSMENT_MODEL.md

---

# 1. Purpose

Tài liệu này khóa Question Set Assessment của TV-02.

TV-02 chưa được implement trong ticket này.

Template này chỉ định nghĩa câu hỏi khách hàng mà Assessment phải trả lời.

Decision nội bộ của TV-02 sẽ được định nghĩa sau.

Không được công bố Decision trực tiếp.

---

# 2. Product Question

Khách hàng mua:

Business Assessment

Không mua:

Evidence

Finding

Decision

---

# 3. Canonical Position

```
Decision
        │
        ▼
Business Assessment
        │
        ▼
Recommendation
```

Assessment = "What is the answer?"

Recommendation = "What should I do?"

---

# 4. TV-02 Question Set

TV-02 Assessment MUST trả lời đúng sáu câu hỏi sau.

## Q1 Should we cooperate?

Mức độ nên hợp tác.

Semantic level.

Score optional.

## Q2 Who complements whom?

Bổ trợ theo hướng:

A → B

B → A

Không gộp chiều nếu Decision phân biệt chiều.

## Q3 Leadership balance?

Ai dẫn dắt?

Ai bổ trợ vai trò lãnh đạo?

Cân bằng hay lệch?

## Q4 Financial cooperation?

Khả năng hợp tác tài chính.

Rủi ro tiền bạc chính.

## Q5 Business risks?

Rủi ro doanh nghiệp chính.

Yếu tố cứu giải chính.

Không biến thành action plan.

## Q6 Overall business assessment?

Tóm tắt:

Cooperation viability

Complement

Leadership

Finance

Risk

Overall conclusion

---

# 5. Public Surface

Report / UI bắt đầu bằng:

Business Assessment

Six cards.

Detailed Analysis collapsed by default.

Recommendations after Assessment.

---

# 6. Freeze Note

Question Set này là reusable template.

Thay đổi câu hỏi = tăng Question Set Version.

Không implement runtime trong ticket R1.
