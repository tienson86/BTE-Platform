# NARRATIVE V2 — PIPELINE

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Tài liệu này định nghĩa Runtime Pipeline chính thức của Narrative V2.

Pipeline quy định:

- thứ tự thực thi;
- quyền sở hữu dữ liệu;
- luồng xử lý;
- validation;
- publish.

Mọi Narrative Builder đều phải tuân theo Pipeline này.

Không Builder nào được bỏ qua bước.

---

# 2. Design Principles

Pipeline phải:

✓ Deterministic

✓ Stateless

✓ Traceable

✓ Reusable

✓ Testable

✓ Immutable

---

# 3. Overall Pipeline

```
Canonical Analysis
        ↓
Evidence Builder
        ↓
Reasoning Builder
        ↓
Knowledge Resolver
        ↓
Commercial Rewrite
        ↓
Overview Builder
        ↓
Interpretation Builder
        ↓
Action Builder
        ↓
Commercial Builder
        ↓
Narrative Validator
        ↓
Narrative V2 Result
```

Pipeline luôn chạy theo đúng thứ tự trên.

---

# 4. Runtime Philosophy

Pipeline chỉ có một hướng.

```
Truth

↓

Meaning

↓

Communication
```

Không được:

```
Communication

↓

Truth
```

Narrative không bao giờ sửa Canonical Analysis.

---

# 5. Stage 1

## Evidence Builder

Input

```
CanonicalAnalysis
```

Output

```
EvidenceContext
```

Purpose

Thu thập Evidence.

Không giải thích.

---

## Input

```
identity

bazi

strength

pattern

temperature

useful_god

five_elements

ten_gods

shensha

luck
```

---

## Output

```
EvidenceContext
```

---

## Validation

Evidence đầy đủ?

Nếu thiếu:

```
partial
```

---

# 6. Stage 2

## Reasoning Builder

Input

```
EvidenceContext
```

Output

```
ReasoningContext
```

Purpose

Kết nối Evidence.

Ví dụ

```
Strength

+

Pattern

↓

Reasoning
```

---

Không tạo:

Recommendation.

---

# 7. Stage 3

## Knowledge Resolver

Input

```
ReasoningContext
```

Output

```
KnowledgeContext
```

Purpose

Resolve tri thức Approved.

Nguồn

```
Interpretation Knowledge

Consulting Knowledge

Sentence Library

Template Library
```

---

Không:

Gọi Internet.

Không:

LLM.

---

# 8. Stage 4

## Commercial Rewrite

Input

```
KnowledgeContext
```

Output

```
CommercialRewriteContext
```

Purpose

Rewrite.

Không đổi nghĩa.

Ví dụ

```
Technical

↓

Commercial
```

---

Validation

Meaning giữ nguyên?

---

# 9. Stage 5

## Overview Builder

Input

```
CommercialRewriteContext
```

Output

```
OverviewSummary
```

Purpose

Sinh:

Overview.

---

# 10. Stage 6

## Interpretation Builder

Input

```
CommercialRewriteContext
```

Output

```
InterpretationNarrative
```

Structure

```
Observation

↓

Reasoning

↓

Impact

↓

Recommendation
```

---

# 11. Stage 7

## Action Builder

Input

```
CommercialRewriteContext
```

Output

```
ActionPlanNarrative
```

Structure

```
Top Priority

↓

Actions

↓

Warnings

↓

Current Period
```

---

# 12. Stage 8

## Commercial Builder

Input

```
CommercialRewriteContext
```

Output

```
CommercialNarrative
```

Domains

```
Career

Finance

Relationship

Health

Leadership
```

Optional.

---

# 13. Stage 9

## Narrative Validator

Input

```
Overview

Interpretation

Action

Commercial
```

Output

Validated Narrative.

---

Validator kiểm tra

Schema

↓

Knowledge

↓

Safety

↓

Style

↓

Duplicate

↓

Publish

---

# 14. Stage 10

## Narrative Publisher

Input

Validated Narrative.

Output

```
NarrativeV2Result
```

Đây là object cuối.

---

# 15. Runtime Sequence

```
POST

↓

Analysis

↓

Narrative

↓

ResultStore

↓

Portal

↓

Report

↓

PDF

↓

DOCX
```

---

# 16. Pipeline Diagram

```
Canonical Analysis

↓

Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Overview

↓

Interpretation

↓

Action

↓

Commercial

↓

Validation

↓

Publish
```

---

# 17. Ownership

| Stage | Owner |
|---------|--------|
| Evidence | Narrative |
| Reasoning | Narrative |
| Knowledge | Narrative |
| Rewrite | Narrative |
| Overview | Narrative |
| Interpretation | Narrative |
| Action | Narrative |
| Commercial | Narrative |
| Validation | Narrative |

Engine chỉ cung cấp CanonicalAnalysis.

---

# 18. Allowed Dependencies

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
```

Không phụ thuộc ngược.

---

# 19. Forbidden Dependencies

Overview

↓

Engine

✗

---

Action

↓

Strength

✗

---

UI

↓

Knowledge

✗

---

PDF

↓

Builder

✗

---

# 20. Builder Independence

Overview Builder.

Không biết:

Dashboard.

Interpretation Builder.

Không biết:

PDF.

Action Builder.

Không biết:

DOCX.

Builder chỉ sinh Object.

---

# 21. Rewrite Independence

Commercial Rewrite.

Không biết:

UI.

Không biết:

HTML.

Không biết:

CSS.

Rewrite chỉ đổi ngôn ngữ.

---

# 22. Validation Pipeline

```
Schema

↓

Evidence

↓

Knowledge

↓

Semantic

↓

Safety

↓

Duplicate

↓

Presentation

↓

Publish
```

---

# 23. Error Handling

Nếu Stage lỗi.

Không publish.

Ví dụ

```
Knowledge

↓

missing
```

↓

```
partial
```

---

Không:

Crash.

---

# 24. Partial Pipeline

Pipeline được phép

```
partial
```

Ví dụ

```
Overview

✓

Interpretation

✓

Action

missing
```

↓

Publish.

---

# 25. Retry Policy

Knowledge lỗi.

↓

Retry.

Rewrite lỗi.

↓

Retry.

Builder lỗi.

↓

Retry.

Validation fail.

↓

Reject.

---

# 26. Runtime Trace

Pipeline phải trace được.

```
Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Builder
```

Không render.

---

# 27. Performance

Pipeline không:

Scan toàn Knowledge.

Pipeline dùng:

Index.

Resolver.

Cache.

---

# 28. Cache

Cache

```
Evidence

Knowledge

Rewrite
```

Không cache:

CanonicalAnalysis.

---

# 29. Determinism

Input giống.

↓

Output giống.

Không Random.

---

# 30. Pipeline Status

```
running

↓

partial

↓

complete

↓

invalid
```

---

# 31. Runtime Events

```
NarrativeStarted

EvidenceBuilt

ReasoningBuilt

KnowledgeResolved

RewriteCompleted

OverviewBuilt

InterpretationBuilt

ActionBuilt

CommercialBuilt

ValidationPassed

NarrativePublished
```

Internal only.

---

# 32. Parallel Execution

Được phép song song:

Overview

Interpretation

Action

Commercial

Sau Rewrite.

Không trước Rewrite.

---

# 33. Synchronization Point

Pipeline chỉ đồng bộ tại:

```
CommercialRewrite

↓

Builders
```

Builder không chạy trước Rewrite.

---

# 34. Consumer Flow

```
Narrative

↓

Dashboard

↓

PDF

↓

DOCX

↓

REST
```

Consumer không gọi Builder.

---

# 35. Failure Recovery

Nếu Builder fail.

↓

Partial.

Nếu Validation fail.

↓

Reject.

---

# 36. Freeze Point

Freeze xảy ra tại:

```
NarrativeV2Result
```

Sau Freeze.

Không sửa.

---

# 37. Pipeline Extension

Builder mới.

↓

Đăng ký.

↓

Validation.

↓

Publish.

Không sửa Pipeline cũ.

---

# 38. Acceptance Criteria

Pipeline đạt khi:

✓ Deterministic

✓ Traceable

✓ Customer-safe

✓ Builder độc lập

✓ UI không compose

✓ PDF không compose

✓ DOCX không compose

---

# 39. Freeze Rules

Sau Freeze.

Không đổi Stage.

Không đổi thứ tự.

Không thêm Dependency.

Muốn sửa.

↓

Pipeline Revision.

---

# 40. Runtime Summary

```
Truth

↓

Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Narrative

↓

Validation

↓

Publish

↓

Dashboard

PDF

DOCX
```

Đây là Runtime Pipeline chính thức của Narrative V2.

# 41. Pipeline Responsibility Matrix

Narrative Pipeline được thiết kế theo nguyên tắc:

> **Mỗi Stage chỉ có một trách nhiệm duy nhất.**

Không Stage nào được thực hiện công việc của Stage khác.

Điều này đảm bảo:

- Pipeline luôn đơn giản;
- Runtime luôn Deterministic;
- Builder luôn độc lập;
- UI không chứa nghiệp vụ;
- Engine không sinh Narrative.

---

# 41.1 Responsibility Matrix

| Stage | Đọc Canonical | Reasoning | Resolve Knowledge | Rewrite | Sinh Narrative | Validation | Publish |
|---------|:------------:|:---------:|:-----------------:|:-------:|:--------------:|:----------:|:-------:|
| Evidence Builder | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Reasoning Builder | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Knowledge Resolver | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Commercial Rewrite | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Overview Builder | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Interpretation Builder | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Action Builder | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Commercial Builder | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Narrative Validator | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Narrative Publisher | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |

---

# 41.2 Stage Responsibilities

## Evidence Builder

### Được phép

- đọc Canonical Analysis;
- chọn Evidence;
- chuẩn hóa Evidence;
- tạo EvidenceContext.

### Không được phép

- giải thích;
- rewrite;
- viết câu;
- recommendation;
- gọi Knowledge.

---

## Reasoning Builder

### Được phép

- kết nối Evidence;
- tạo Reasoning;
- xác định quan hệ giữa Evidence.

### Không được phép

- viết Narrative;
- rewrite;
- recommendation;
- resolve Knowledge.

---

## Knowledge Resolver

### Được phép

- resolve tri thức Approved;
- nối Knowledge với Evidence;
- chọn đúng Knowledge.

### Không được phép

- tính Bát Tự;
- tạo Narrative;
- rewrite;
- recommendation.

---

## Commercial Rewrite

### Được phép

- đổi ngôn ngữ;
- đơn giản hóa;
- chuẩn hóa câu;
- commercial rewrite.

### Không được phép

- đổi ý nghĩa;
- thêm tri thức;
- thêm Recommendation;
- tạo Action.

---

## Overview Builder

### Được phép

- sinh Overview Summary;
- chọn Insight;
- tạo Headline.

### Không được phép

- sinh Action;
- sinh Commercial Domain;
- rewrite.

---

## Interpretation Builder

### Được phép

- Observation;
- Reasoning;
- Impact;
- Recommendation.

### Không được phép

- Action Plan;
- Commercial Consulting;
- Dashboard Logic.

---

## Action Builder

### Được phép

- Top Priority;
- Action Items;
- Warning;
- Current Period.

### Không được phép

- tính Dụng Thần;
- tính Đại Vận;
- suy luận Astrology;
- rewrite Interpretation.

---

## Commercial Builder

### Được phép

- Career;
- Finance;
- Relationship;
- Health;
- Leadership.

### Không được phép

- sửa Overall Interpretation;
- sửa Overview.

---

## Narrative Validator

### Được phép

- Schema Validation;
- Semantic Validation;
- Style Validation;
- Duplicate Validation;
- Safety Validation.

### Không được phép

- Rewrite;
- sửa Narrative;
- thêm nội dung.

Validator chỉ:

PASS

hoặc

FAIL.

---

## Narrative Publisher

### Được phép

- Freeze;
- Publish;
- Serialize.

### Không được phép

- Rewrite;
- Validation;
- Builder;
- Reasoning.

Publisher chỉ publish.

---

# 41.3 Responsibility Flow

Pipeline chỉ chạy theo một chiều.

```text
Evidence
        ↓
Reasoning
        ↓
Knowledge
        ↓
Rewrite
        ↓
Overview
        ↓
Interpretation
        ↓
Action
        ↓
Commercial
        ↓
Validation
        ↓
Publish
```

Không Stage nào được:

```
Action

↓

Reasoning
```

Hoặc:

```
Interpretation

↓

Evidence
```

Mọi dependency ngược đều không hợp lệ.

---

# 41.4 Forbidden Responsibilities

Các hành vi sau bị cấm.

## Evidence

Không được:

- sinh câu;
- Recommendation;
- Rewrite.

---

## Reasoning

Không được:

- Commercial Rewrite;
- PDF;
- Dashboard.

---

## Knowledge

Không được:

- tính Astrology;
- sửa Canonical Analysis.

---

## Rewrite

Không được:

- đổi Truth;
- thêm Knowledge;
- tạo Recommendation.

---

## Builder

Không được:

- gọi Engine;
- gọi Calendar;
- tính Bát Tự;
- sửa Canonical.

---

## Validator

Không được:

- sửa dữ liệu;
- rewrite câu;
- thêm Action.

---

## Publisher

Không được:

- Validation;
- Rewrite;
- Builder.

---

# 41.5 Responsibility Validation

Narrative Validator phải kiểm tra:

✓ Stage có đúng Responsibility không.

✓ Có vi phạm Dependency không.

✓ Có Builder nào vượt phạm vi không.

✓ Có Stage nào gọi Engine trực tiếp không.

Nếu phát hiện:

```
Stage

↓

thực hiện Responsibility sai
```

↓

```
Pipeline Status

invalid
```

Không Publish.

---

# 41.6 Pipeline Responsibility Questions

Mỗi Stage chỉ được trả lời đúng **một câu hỏi**.

| Stage | Câu hỏi phải trả lời |
|---------|----------------------|
| Evidence Builder | Evidence nào quan trọng? |
| Reasoning Builder | Tại sao? |
| Knowledge Resolver | Có tri thức nào phù hợp? |
| Commercial Rewrite | Khách hàng sẽ hiểu câu này thế nào? |
| Overview Builder | Điều gì quan trọng nhất? |
| Interpretation Builder | Lá số này nói gì? |
| Action Builder | Nên làm gì tiếp theo? |
| Commercial Builder | Áp dụng theo từng lĩnh vực thế nào? |
| Validator | Narrative có hợp lệ không? |
| Publisher | Narrative có thể công bố chưa? |

Nếu một Stage trả lời nhiều hơn một câu hỏi trên, Pipeline đã bị pha trộn trách nhiệm.

---

# 41.7 Final Pipeline Principle

Narrative Pipeline chỉ hoạt động tốt khi:

- mỗi Stage chỉ làm đúng việc của mình;
- không Stage nào thay Engine;
- không UI nào thay Narrative;
- không Builder nào thay Rewrite;
- không Validator nào sửa dữ liệu.

Nguyên tắc cuối cùng:

> **Một Stage – Một Trách Nhiệm – Một Đầu Ra.**

Khi nguyên tắc này được giữ vững, toàn bộ Narrative V2 sẽ luôn:

- Deterministic;
- Testable;
- Maintainable;
- Reusable;
- Commercial-ready.