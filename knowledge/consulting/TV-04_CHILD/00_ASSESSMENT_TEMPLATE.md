# TV-04 — CHILD
## 00_ASSESSMENT_TEMPLATE.md

**Document ID:** TV-04-00

**Module:** TV-04_CHILD

**Product:** BTE Platform

**Document Type:** Reusable Assessment Template

**Status:** DRAFT TEMPLATE — NOT A PRODUCT BUILD

**Version:** 1.0

**Depends on:** COMMON/06_ASSESSMENT_MODEL.md

---

# 1. Purpose

Tài liệu này khóa Question Set Assessment của TV-04.

TV-04 chưa được implement trong ticket này.

Template này chỉ định nghĩa câu hỏi khách hàng mà Assessment phải trả lời.

Không được công bố Decision trực tiếp.

---

# 2. Product Question

Khách hàng mua:

Child Assessment

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

# 4. TV-04 Question Set

TV-04 Assessment MUST trả lời đúng sáu câu hỏi sau.

## Q1 Child planning

Đánh giá hoạch định con cái ở mức hài hòa / hỗ trợ gia đình.

Cấm dự đoán fertility.

Cấm dự đoán số con.

## Q2 Timing

Giai đoạn thuận / nhạy nếu Evidence hỗ trợ.

Không phải lịch sinh cụ thể nếu không có Canonical support.

## Q3 Parent support

Cha mẹ hỗ trợ cấu trúc nuôi dưỡng thế nào.

Hướng:

Parent → Child context

không suy diễn y khoa.

## Q4 Family balance

Cân bằng gia đạo liên quan con cái.

## Q5 Risks

Rủi ro chính.

Yếu tố cứu giải chính.

Không biến thành action plan.

## Q6 Overall child assessment

Tóm tắt:

Planning

Timing

Parent support

Family balance

Risks

Overall conclusion

---

# 5. Public Surface

Report / UI bắt đầu bằng:

Child Assessment

Six cards.

Detailed Analysis collapsed by default.

Recommendations after Assessment.

---

# 6. Freeze Note

Question Set này là reusable template.

Thay đổi câu hỏi = tăng Question Set Version.

Không implement runtime trong ticket R1.
