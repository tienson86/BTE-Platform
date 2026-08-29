# NARRATIVE V2 — RUNTIME SEQUENCE

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Tài liệu này định nghĩa Runtime Sequence chính thức của Narrative V2.

Nếu:

- Architecture định nghĩa hệ thống gồm những gì.
- Pipeline định nghĩa các Stage.

thì Runtime Sequence trả lời:

> **Điều gì thực sự xảy ra từ lúc khách hàng bấm "Phân tích lá số" cho tới khi Dashboard xuất hiện.**

Runtime Sequence là "dòng chảy sống" của Narrative.

---

# 2. Runtime Philosophy

Narrative không chạy độc lập.

Narrative luôn chạy sau Canonical Analysis.

Runtime chuẩn:

```
Customer

↓

Analyze

↓

Canonical Analysis

↓

Narrative

↓

Presentation

↓

Dashboard
```

Không có đường tắt.

---

# 3. Runtime Entry

Runtime bắt đầu tại:

```
POST /api/v1/analyze
```

Narrative không được gọi trực tiếp từ:

- Dashboard
- PDF
- DOCX
- Mobile

Narrative chỉ được gọi từ Orchestrator.

---

# 4. Overall Runtime Sequence

```text
Customer
        │
        ▼
Submit Analyze Request
        │
        ▼
Analysis Orchestrator
        │
        ▼
Canonical Analysis
        │
        ▼
Narrative Runtime
        │
        ▼
NarrativeV2Result
        │
        ▼
ResultStore
        │
        ├───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼
Dashboard             PDF             DOCX
        │
        ▼
Customer
```

Narrative chỉ chạy **một lần**.

---

# 5. Runtime Stage 1 — Canonical Analysis

Input:

```
AnalyzeRequest
```

Output:

```
CanonicalAnalysis
```

Owner:

Astrology Engines.

Narrative chưa bắt đầu.

---

# 6. Runtime Stage 2 — Narrative Entry

Input:

```
CanonicalAnalysis
```

Output:

```
NarrativeRuntimeContext
```

Narrative Runtime được khởi tạo.

Không Builder nào chạy trước bước này.

---

# 7. Runtime Stage 3 — Evidence Builder

```
CanonicalAnalysis

↓

EvidenceContext
```

Purpose:

Thu thập toàn bộ Evidence.

Không viết câu.

Không Knowledge.

---

# 8. Runtime Stage 4 — Reasoning Builder

```
EvidenceContext

↓

ReasoningContext
```

Purpose:

Kết nối các Evidence.

Không Recommendation.

---

# 9. Runtime Stage 5 — Knowledge Resolver

```
ReasoningContext

↓

KnowledgeContext
```

Purpose:

Resolve toàn bộ tri thức Approved.

Nguồn:

- Interpretation Knowledge
- Commercial Knowledge
- Sentence Library
- Template Library

Không Internet.

Không LLM.

---

# 10. Runtime Stage 6 — Commercial Rewrite

```
KnowledgeContext

↓

CommercialRewriteContext
```

Purpose:

Technical

↓

Customer Language

Không đổi nghĩa.

---

# 11. Runtime Stage 7 — Summary Builder

```
CommercialRewriteContext

↓

OverviewSummary
```

Sinh Executive Summary.

---

# 12. Runtime Stage 8 — Interpretation Builder

```
CommercialRewriteContext

↓

InterpretationNarrative
```

Sinh toàn bộ Interpretation.

---

# 13. Runtime Stage 9 — Action Builder

```
CommercialRewriteContext

+

InterpretationNarrative

↓

ActionPlanNarrative
```

Sinh Decision.

↓

Action.

---

# 14. Runtime Stage 10 — Commercial Builder

```
CommercialRewriteContext

↓

CommercialNarrative
```

Sinh:

Career

Finance

Relationship

Leadership

Health

nếu được yêu cầu.

---

# 15. Runtime Stage 11 — Presentation Contract

Tất cả Builder output được hợp nhất.

```
Overview

+

Interpretation

+

Action

+

Commercial

↓

NarrativeV2Presentation
```

Đây là Presentation Contract duy nhất.

---

# 16. Runtime Stage 12 — Validation

Narrative Validator chạy.

Kiểm tra:

✓ Schema

✓ Customer Safety

✓ Duplicate

✓ Style

✓ Traceability

✓ Version

Nếu FAIL.

↓

Không Publish.

---

# 17. Runtime Stage 13 — Freeze

Sau Validation.

Narrative được Freeze.

Không Builder nào được sửa.

```
NarrativeV2Presentation

↓

Frozen
```

---

# 18. Runtime Stage 14 — Publish

Publish:

```
NarrativeV2Result
```

Đây là Runtime Output cuối cùng.

---

# 19. Runtime Stage 15 — ResultStore

ResultStore lưu:

```
CanonicalAnalysis

+

NarrativeV2Result
```

Hai object độc lập.

Không merge.

---

# 20. Runtime Stage 16 — Consumer

Consumer chỉ đọc.

```
NarrativeV2Presentation
```

Dashboard.

↓

Render.

PDF.

↓

Render.

DOCX.

↓

Render.

Không compose.

---

# 21. Runtime Timeline

```
Analyze

↓

Canonical

↓

Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Summary

↓

Interpretation

↓

Action

↓

Commercial

↓

Presentation

↓

Validation

↓

Freeze

↓

Publish

↓

ResultStore

↓

Dashboard
```

---

# 22. Runtime Ownership

| Runtime Step | Owner |
|--------------|-------|
| Canonical Analysis | Engines |
| Evidence | Narrative |
| Reasoning | Narrative |
| Knowledge | Narrative |
| Rewrite | Narrative |
| Builders | Narrative |
| Validation | Narrative |
| Publish | Narrative |
| ResultStore | Platform |
| Dashboard | Portal |

---

# 23. Runtime Synchronization

Synchronization Point duy nhất:

```
CommercialRewrite

↓

Builders
```

Sau Rewrite.

Summary.

Interpretation.

Action.

Commercial.

có thể chạy song song.

---

# 24. Parallel Execution

Allowed:

```
Summary

Interpretation

Action

Commercial
```

Parallel.

Không trước Rewrite.

---

# 25. Runtime Trace

Runtime phải trace được:

```
Canonical

↓

Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Builder

↓

Presentation
```

Không render.

---

# 26. Runtime State

Narrative Runtime có bốn trạng thái.

```
running

↓

validating

↓

published

↓

failed
```

Không trạng thái khác.

---

# 27. Failure Recovery

Nếu:

Knowledge fail.

↓

Retry.

Rewrite fail.

↓

Retry.

Builder fail.

↓

Retry.

Validation fail.

↓

Reject.

Không Publish.

---

# 28. Partial Runtime

Cho phép:

```
Overview

✓

Interpretation

✓

Action

missing

Commercial

✓
```

↓

Publish Partial.

Không Crash.

---

# 29. Consumer Sequence

Dashboard.

↓

Overview.

↓

Interpretation.

↓

Action.

↓

Commercial.

Không đọc Builder.

---

# 30. Runtime Cache

Cache:

Knowledge

Rewrite

Sentence

Template

Không Cache:

CanonicalAnalysis.

---

# 31. Runtime Events

```
NarrativeStarted

EvidenceBuilt

ReasoningBuilt

KnowledgeResolved

RewriteCompleted

SummaryBuilt

InterpretationBuilt

ActionBuilt

CommercialBuilt

PresentationBuilt

ValidationPassed

NarrativePublished
```

Internal only.

---

# 32. Runtime Validation

Validator phải kiểm tra.

✓ đúng thứ tự.

✓ đúng Stage.

✓ không Stage bị bỏ.

Nếu:

Summary chạy trước Rewrite.

↓

FAIL.

---

# 33. Runtime Determinism

Input giống.

↓

Output giống.

Không Random.

Không phụ thuộc UI.

---

# 34. Runtime Consumer Rule

Consumer chỉ được:

```
Read
```

Không:

Rewrite.

Compose.

Reasoning.

---

# 35. Runtime Performance

Narrative chỉ chạy một lần.

Dashboard.

PDF.

DOCX.

REST.

đều dùng cùng output.

Không Builder chạy lại.

---

# 36. Runtime Freeze

Sau Publish.

Narrative.

Immutable.

---

# 37. Runtime Sequence Matrix

| Stage | Input | Output |
|--------|-------|--------|
| Evidence | Canonical | Evidence |
| Reasoning | Evidence | Reasoning |
| Knowledge | Reasoning | Knowledge |
| Rewrite | Knowledge | Rewrite |
| Summary | Rewrite | Overview |
| Interpretation | Rewrite | Interpretation |
| Action | Rewrite + Interpretation | Action |
| Commercial | Rewrite | Commercial |
| Validation | Presentation | Validated |
| Publish | Validated | NarrativeV2Result |

---

# 38. Runtime Validation Matrix

Validator kiểm tra:

✓ Stage Order

✓ Dependency

✓ Ownership

✓ Safety

✓ Duplicate

✓ Publish

---

# 39. Acceptance Criteria

Runtime Sequence đạt khi:

✓ Narrative chạy đúng thứ tự.

✓ Builder không bỏ Stage.

✓ Consumer không compose.

✓ Dashboard/PDF/DOCX dùng cùng Presentation.

✓ Chỉ có một Narrative Runtime.

---

# 40. Runtime Principle

Narrative Runtime không phải là tập hợp các Builder độc lập.

Narrative Runtime là một chuỗi xử lý thống nhất.

Mỗi Stage tồn tại vì Stage trước.

Mỗi Stage chuẩn bị cho Stage sau.

Nếu thiếu một Stage.

Narrative sẽ mất tính nhất quán.

---

# 41. Runtime Responsibility Matrix

| Stage | Được phép | Không được phép |
|--------|-----------|-----------------|
| Evidence | Đọc Canonical | Viết câu |
| Reasoning | Giải thích quan hệ | Rewrite |
| Knowledge | Resolve tri thức | Tính Astrology |
| Rewrite | Đổi ngôn ngữ | Đổi ý nghĩa |
| Summary | Sinh Executive Summary | Sinh Action |
| Interpretation | Sinh Narrative | Sinh Action |
| Action | Sinh Decision & Action | Tính Dụng Thần |
| Commercial | Sinh Domain Narrative | Sửa Interpretation |
| Validation | Kiểm tra | Rewrite |
| Publish | Freeze & Publish | Chỉnh sửa |

---

# 42. Runtime Integrity Principle

Không Stage nào được bỏ qua.

Không Stage nào được chạy sai thứ tự.

Không Stage nào được thực hiện trách nhiệm của Stage khác.

Nếu Runtime Pipeline bị phá vỡ.

Narrative sẽ mất:

- tính đúng;
- tính nhất quán;
- khả năng tái sử dụng.

---

# 43. Final Runtime Principle

Narrative V2 không phải là một chuỗi các Builder.

Narrative V2 là một Runtime thống nhất.

Builder chỉ là các mắt xích.

Pipeline chỉ là con đường.

Presentation chỉ là kết quả.

Điều tạo nên Narrative V2 là **Runtime Flow**.

> **Một Narrative tốt không được tạo ra bởi một Builder tốt.**

> **Một Narrative tốt được tạo ra bởi toàn bộ Runtime hoạt động đúng như một hệ thống thống nhất.**