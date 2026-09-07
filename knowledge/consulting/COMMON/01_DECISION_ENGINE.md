# COMMON — CONSULTING FRAMEWORK

# 01_DECISION_ENGINE.md

Document ID: COMMON-01

Version: 1.0

Status: DRAFT

---

# 1. Purpose

Tài liệu này định nghĩa kiến trúc của Decision Engine.

Decision Engine là thành phần trung tâm của Consulting Framework.

Nó có nhiệm vụ:

- tiếp nhận Canonical Truth đã được chuẩn hóa;
- xây dựng Evidence;
- tổng hợp Findings;
- xác định Structural State;
- xác định Domain State;
- tạo Decision Result.

Decision Engine không chịu trách nhiệm:

- tính Bát Tự;
- tính Strength;
- tính Pattern;
- tính Useful God;
- sinh Narrative;
- render UI.

---

# 2. Decision Engine Vision

Decision Engine được xây dựng như một Semantic Engine.

Nó không phải:

Rule Engine đơn thuần.

Nó cũng không phải:

Score Engine.

Decision Engine là một hệ thống:

Semantic Resolution Engine.

Mọi kết luận đều phải có:

Evidence.

Mọi Evidence đều phải có:

Canonical Truth.

---

# 3. Runtime Position

```
Canonical Mathematics
        │
        ▼
Canonical Truth

══════════════════════

Decision Engine

══════════════════════

Decision Result

══════════════════════

Narrative Framework
```

Decision Engine nằm hoàn toàn giữa:

Truth

và

Narrative.

---

# 4. Responsibilities

Decision Engine chỉ có sáu nhiệm vụ.

1.

Evidence Extraction

↓

2.

Evidence Resolution

↓

3.

Finding Resolution

↓

4.

Structural Resolution

↓

5.

Domain Resolution

↓

6.

Decision Resolution

Không nhiều hơn.

---

# 5. Non Responsibilities

Decision Engine tuyệt đối không:

- đọc Birth Input;
- tính Calendar;
- tính Four Pillars;
- tính Strength;
- tính Useful God;
- tạo Prompt;
- gọi GPT;
- render HTML.

---

# 6. Internal Pipeline

```
Canonical Truth
        │
        ▼
Evidence Builder
        │
        ▼
Evidence Graph
        │
        ▼
Evidence Resolver
        │
        ▼
Finding Builder
        │
        ▼
Finding Graph
        │
        ▼
Structural State Resolver
        │
        ▼
Domain State Resolver
        │
        ▼
Decision Builder
        │
        ▼
Decision Result
```

Đây là pipeline bất biến.

---

# 7. Evidence Builder

Input

↓

Canonical Truth

Output

↓

Evidence Graph

Evidence Builder chỉ tạo Evidence.

Không được tạo Finding.

---

# 8. Evidence Graph

Evidence không tồn tại độc lập.

Evidence tạo thành Graph.

Ví dụ.

```
Useful God Support
         │
         ├────────┐
         │        │
Pattern   Branch
         │
         ▼
Evidence Graph
```

Decision Engine luôn làm việc trên Graph.

Không làm việc trên danh sách tuyến tính.

---

# 9. Evidence Resolver

Evidence Resolver có nhiệm vụ:

- hợp nhất;
- loại trùng;
- xử lý xung đột;
- xác định dependency;
- xác định damage;
- xác định rescue.

Output

↓

Resolved Evidence.

---

# 10. Finding Builder

Finding Builder nhận:

Resolved Evidence.

↓

Sinh Findings.

Một Finding

không phải

một Evidence.

Một Finding

là

một kết luận ngữ nghĩa.

---

# 11. Finding Graph

Finding cũng tạo thành Graph.

Ví dụ.

```
Finding A

↓

Finding B

↓

Finding C
```

Có dependency.

---

# 12. Structural State Resolver

Finding

↓

Structural State.

Ví dụ.

```
Supportive

Balanced

Mixed

Pressured

Critical
```

Structural State

mới là Truth của Decision.

Không phải Score.

---

# 13. Domain State Resolver

Sau khi có Structural State.

Framework xác định:

Domain State.

Ví dụ.

Finance

↓

Supportive

Family

↓

Mixed

Marriage

↓

Strong

---

# 14. Decision Builder

Decision Builder nhận:

Domain States

+

Decision Profile

↓

Decision Result.

Decision Builder

không đọc

Canonical Truth.

Điều này tránh duplicate logic.

---

# 15. Decision Result

Decision Result gồm:

- Structural States;
- Domain States;
- Findings;
- Confidence;
- Metadata.

Decision Result không chứa Assessment.

Decision Result không chứa Recommendation.

Assessment Projector đọc Decision Result.

Recommendation Engine đọc Decision Result.

Không engine nào được đọc output của engine kia.

Score

không phải

Decision.

Score chỉ là Projection.

---

# 16. Engine Contracts

Decision Engine công bố một Contract duy nhất.

Input:

Canonical Truth.

Output:

Decision Result.

Không có API riêng cho:

Marriage.

Career.

Partner.

---

# 17. Engine Invariants

Decision Engine luôn tuân thủ:

Truth

↓

Evidence

↓

Finding

↓

Structural State

↓

Domain State

↓

Decision

Không được bỏ bước.

---

# 18. Graph Principle

Decision Engine

không xử lý:

List.

Decision Engine

xử lý:

Graph.

Đây là nguyên tắc cốt lõi.

---

# 19. Explainability

Decision Result

phải truy được:

Decision

↓

Structural State

↓

Finding

↓

Evidence

↓

Canonical Truth

---

# 20. Determinism

Cùng:

Canonical Truth

↓

Decision Result

phải giống nhau.

Không phụ thuộc:

LLM.

Prompt.

Temperature.

---

# 21. Versioning

Decision Engine

có version riêng.

Decision Profile

có version riêng.

Rule Catalog

có version riêng.

Không được gộp.

---

# 22. Future Extension

Muốn tạo:

TV-01

TV-02

TV-03

TV-04

↓

chỉ thay:

Decision Profile.

Decision Engine

không đổi.

---

# 23. Core Statement

Decision Engine

không quyết định

dựa trên

Rule.

Decision Engine

quyết định

dựa trên

Resolved Semantic State.

Đây là điểm khác biệt lớn nhất.

---

# 24. Freeze Conditions

Decision Engine chỉ FREEZE khi:

- [ ] Không phụ thuộc Canonical Engine.
- [ ] Không phụ thuộc Narrative.
- [ ] Có Graph Architecture.
- [ ] Có Structural State.
- [ ] Có Domain State.
- [ ] Có Explainability.
- [ ] Có Determinism.
- [ ] Có Versioning.

---

# 25. Status

COMMON-01

STATUS:

DRAFT

Next:

COMMON-02_DECISION_MATHEMATICS.md