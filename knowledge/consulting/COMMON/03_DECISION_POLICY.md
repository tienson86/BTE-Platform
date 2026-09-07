# COMMON — CONSULTING FRAMEWORK
# 03_DECISION_POLICY.md

**Document ID:** COMMON-03

**Product:** BTE Platform

**Module:** Consulting Framework

**Document Type:** Decision Policy Specification

**Status:** DRAFT FOR PRODUCT OWNER REVIEW

**Version:** 1.0

---

# 1. Purpose

Tài liệu này định nghĩa **Decision Policy Framework** của toàn bộ BTE Consulting.

Decision Policy là tầng nằm giữa:

Decision Mathematics

và

Decision Engine.

Decision Policy chịu trách nhiệm:

- xác định mục tiêu tối ưu của bài toán;
- lựa chọn Evidence cần sử dụng;
- xác định mức độ ưu tiên;
- xác định cách Resolution;
- xác định Decision Strategy.

Decision Policy không phải:

- Rule Engine;
- Score Engine;
- Configuration File;
- Prompt.

---

# 2. Policy Philosophy

Decision Mathematics trả lời:

"Làm thế nào để biến đổi Truth thành Decision."

Decision Policy trả lời:

"Đối với bài toán này, Decision nào là tối ưu."

Do đó:

Mathematics

=

Transformation

Policy

=

Optimization Strategy

---

# 3. Policy Definition

Decision Policy là:

> Một tập hợp các Objective, Priority, Constraint và Resolution Strategy dùng để hướng dẫn Decision Engine tạo ra Decision phù hợp với mục tiêu của từng bài toán.

Policy không phải tập hợp các câu lệnh IF...THEN.

Policy là mô hình định hướng Decision.

---

# 4. Objective-first Principle

Framework không bắt đầu từ Rule.

Framework luôn bắt đầu từ:

Objective.

Ví dụ.

Marriage

↓

Relationship Stability

Family Harmony

Mutual Growth

Career

↓

Achievement

Authority

Growth

Business

↓

Trust

Profit

Execution

Risk Control

---

# 5. Policy Pipeline

Objective

↓

Policy Context

↓

Evidence Selection

↓

Priority Resolution

↓

Decision Resolution

↓

Decision Result

---

# 6. Policy Context

Policy không đọc toàn bộ Canonical Truth.

Policy chỉ được nhìn thấy:

Policy Context.

Policy Context là tập dữ liệu mà Policy được phép sử dụng.

Ví dụ.

Marriage Policy.

↓

Useful God

Ten Gods

Interaction

Family

Children

Luck

Career Policy.

↓

Pattern

Authority

Output

Luck

Finance

---

# 7. Evidence Selection

Policy xác định:

Evidence nào quan trọng.

Evidence nào không cần.

Evidence nào chỉ dùng tham khảo.

Decision Engine không tự quyết định điều này.

---

# 8. Evidence Priority

Mỗi Policy phải định nghĩa:

Primary Evidence

Secondary Evidence

Reference Evidence

Priority chỉ thuộc Policy.

Không thuộc Mathematics.

---

# 9. Policy Hierarchy

Framework hỗ trợ nhiều tầng Policy.

Base Policy

↓

Marriage Policy

↓

Expert Marriage Policy

↓

Enterprise Marriage Policy

Mọi Policy đều kế thừa.

---

# 10. Policy Inheritance

Policy không được Copy.

Policy phải Inherit.

Policy chỉ Override phần khác biệt.

Mọi thành phần còn lại kế thừa từ Policy cha.

---

# 11. Policy Composition

Framework cho phép ghép nhiều Policy.

Ví dụ.

Marriage

+

Business

↓

Marriage Business Policy

Composition không tạo Framework mới.

---

# 12. Policy Override

Policy con chỉ được Override:

- Priority
- Objective
- Constraint
- Resolution Strategy

Không được Override:

Decision Mathematics.

---

# 13. Policy Constraints

Policy có thể khai báo:

Required Domains

Optional Domains

Forbidden Domains

Required Evidence

Optional Evidence

Constraint không được vi phạm Architecture.

---

# 14. Policy Resolution

Decision Engine luôn thực hiện:

Decision Mathematics

↓

Decision Policy

↓

Decision Result

Không bao giờ:

Policy

↓

Truth

---

# 15. Policy Strategy

Policy định nghĩa:

- ưu tiên;
- giới hạn;
- mức chấp nhận;
- mục tiêu tối ưu.

Policy không định nghĩa:

Narrative.

---

# 16. Domain Policy

Mỗi Domain có Policy riêng.

Ví dụ.

Finance Policy

Family Policy

Career Policy

Children Policy

Sau đó được tổng hợp thành:

Module Policy.

---

# 17. Module Policy

TV-01

↓

Marriage Policy

TV-02

↓

Business Policy

TV-03

↓

Career Policy

TV-04

↓

Child Planning Policy

Module không tự tạo Decision Engine.

---

# 18. Objective Function

Mỗi Policy phải khai báo:

Primary Objective

Secondary Objective

Optimization Direction

Trade-off Strategy

Đây là phần quan trọng nhất của Policy.

---

# 19. Optimization Strategy

Policy luôn tối ưu:

Objective.

Không tối ưu:

Score.

Score chỉ là Projection.

---

# 20. Trade-off

Policy phải định nghĩa:

Nếu hai mục tiêu xung đột.

Ví dụ.

Family

vs

Career

↓

ưu tiên gì?

Điều này không thuộc Mathematics.

---

# 21. Policy Independence

Policy không phụ thuộc:

Narrative

UI

Report

PDF

LLM

---

# 22. Policy Version

Policy có Version riêng.

Ví dụ.

marriage.policy.v1

marriage.policy.v2

Không được Silent Update.

---

# 23. Policy Compatibility

Decision Mathematics

không cần sửa

khi thêm Policy mới.

Framework luôn giữ:

Backward Compatibility.

---

# 24. Policy Validation

Policy phải được kiểm tra:

- đầy đủ Domain;
- đầy đủ Objective;
- Priority hợp lệ;
- không Override Mathematics;
- không vi phạm Architecture.

---

# 25. Policy Contract

Input:

Decision Context

Output:

Decision Strategy

Policy không sinh Decision.

Policy chỉ hướng dẫn Engine.

---

# 26. Policy Responsibility

Policy chịu trách nhiệm:

"What is important?"

Engine chịu trách nhiệm:

"How to resolve?"

Mathematics chịu trách nhiệm:

"How transformation works?"

---

# 27. Policy Anti-patterns

Không được:

IF A THEN B

IF X THEN Y

Hard-code điểm.

Hard-code Narrative.

Hard-code Prompt.

Policy chỉ mô tả chiến lược.

---

# 28. Policy Extensibility

Framework phải cho phép tạo Policy mới mà không sửa:

Decision Mathematics

Decision Engine

Narrative Framework

---

# 29. Policy Explainability

Mọi Decision phải biết:

Decision

↓

Policy

↓

Objective

↓

Evidence

↓

Truth

Policy luôn nằm trong chuỗi Explainability.

---

# 30. Policy Framework Statement

Decision Policy không phải Rule.

Decision Policy là:

Optimization Strategy.

Đây là nguyên lý cốt lõi của toàn bộ BTE Consulting Framework.

---

# 31. Freeze Conditions

COMMON-03 chỉ được FREEZE khi:

- [ ] Objective-first.
- [ ] Policy Context rõ ràng.
- [ ] Evidence Selection tách khỏi Engine.
- [ ] Có Policy Hierarchy.
- [ ] Có Policy Inheritance.
- [ ] Có Policy Composition.
- [ ] Có Policy Override.
- [ ] Có Policy Version.
- [ ] Không phụ thuộc Narrative.
- [ ] Không phụ thuộc Mathematics.
- [ ] Không phải Rule Engine.

---

# 32. Final Statement

Decision Mathematics xác định:

"Decision được tạo như thế nào."

Decision Policy xác định:

"Decision nào là tối ưu."

Decision Engine thực thi:

Decision Mathematics

+

Decision Policy

↓

Decision Result.

---

# 33. Status

COMMON-03

STATUS:

**FREEZE READY**

Next:

COMMON-04

EVIDENCE_MODEL.md