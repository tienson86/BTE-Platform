# NARRATIVE V2 — PRESENTATION CONTRACT

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Presentation Contract là hợp đồng chính thức giữa Narrative V2 và toàn bộ Consumer.

Presentation Contract quy định:

- Narrative được phép publish dữ liệu gì.
- Consumer được phép đọc dữ liệu gì.
- Consumer tuyệt đối không được tự tạo thêm dữ liệu gì.

Presentation Contract là điểm kết thúc của Narrative V2.

Không có Consumer nào được đọc trực tiếp:

- Canonical Analysis
- Evidence
- Reasoning
- Knowledge
- Rewrite

Mọi Consumer đều phải đọc:

```
NarrativeV2Presentation
```

---

# 2. Design Philosophy

Presentation Contract tồn tại để đảm bảo:

```
One Narrative

↓

Many Consumers
```

Dashboard

↓

PDF

↓

DOCX

↓

REST

↓

Mobile

đều phải sử dụng cùng một Narrative.

---

# 3. Overall Architecture

```
Canonical Analysis

↓

Narrative Pipeline

↓

NarrativeV2Presentation

↓

Dashboard

PDF

DOCX

REST

Mobile
```

Presentation Contract là tầng duy nhất mà Consumer nhìn thấy.

---

# 4. Core Principles

Presentation Contract tuân theo các nguyên tắc sau.

## Principle 1

Customer-safe only.

Không publish:

- Rule IDs
- Engine IDs
- Debug
- JSON
- Internal Objects
- Runtime metadata

---

## Principle 2

Deterministic.

Cùng Narrative.

↓

Cùng Presentation.

---

## Principle 3

Presentation only.

Không chứa:

Reasoning Engine.

Không chứa:

Knowledge Engine.

---

## Principle 4

Immutable.

Sau Publish.

Không Consumer nào được sửa.

---

# 5. Root Presentation Object

Output duy nhất.

```
NarrativeV2Presentation

status

overview

interpretation

action_plan

commercial

metadata
```

Đây là Presentation Object duy nhất.

---

# 6. Overview Contract

```
OverviewPresentation

headline

summary

identity

balance

conclusion
```

Ý nghĩa

headline

↓

Điều nổi bật nhất.

summary

↓

Giải thích ngắn.

identity

↓

Nhật Chủ.

Thân.

Mệnh Cục.

balance

↓

Dụng Thần.

Điều Hậu.

conclusion

↓

Kết luận ngắn.

---

Không được:

lặp Interpretation.

---

# 7. Interpretation Contract

```
InterpretationPresentation

overview

observation

reasoning

impact

recommendation

closing
```

Dashboard.

PDF.

DOCX.

đều đọc object này.

---

Không expose:

Engine.

---

# 8. Observation Contract

```
Observation

title

content

references
```

Customer-facing.

---

# 9. Reasoning Contract

```
Reasoning

title

content

references
```

Purpose

Giải thích.

Không Recommendation.

---

# 10. Impact Contract

```
Impact

title

content

references
```

Purpose

Ảnh hưởng.

Không Action.

---

# 11. Recommendation Contract

```
Recommendation

title

content

references
```

Purpose

Khuyến nghị.

Không Action Plan.

---

# 12. Closing Contract

```
Closing

content
```

Đây là câu kết.

Không Summary.

---

# 13. Action Plan Contract

```
ActionPlanPresentation

top_priority

actions

warnings

current_period
```

---

# 14. Top Priority

```
TopPriority

title

description
```

Một.

Không nhiều.

---

# 15. Action Item

```
ActionItem

title

description

category
```

Không chứa:

Engine.

---

# 16. Warning Contract

```
Warning

title

description
```

Không dùng:

Hung.

Cát.

---

# 17. Current Period Contract

```
CurrentPeriod

title

description
```

Nếu Narrative không publish.

↓

Không render.

---

# 18. Commercial Contract

```
CommercialPresentation

career

finance

relationship

health

leadership
```

Optional.

---

# 19. Metadata Contract

```
PresentationMetadata

status

language

version

created_at
```

Không render.

---

# 20. Contract Ownership

| Contract | Owner |
|-----------|--------|
| Overview | Overview Builder |
| Interpretation | Interpretation Builder |
| Action | Action Builder |
| Commercial | Commercial Builder |
| Metadata | Narrative |

Không Consumer nào sở hữu Contract.

---

# 21. Field Ownership

| Field | Builder |
|---------|---------|
| headline | Overview |
| summary | Overview |
| observation | Interpretation |
| reasoning | Interpretation |
| impact | Interpretation |
| recommendation | Interpretation |
| closing | Interpretation |
| top_priority | Action |
| actions | Action |
| warnings | Action |
| current_period | Action |
| career | Commercial |
| finance | Commercial |
| relationship | Commercial |
| health | Commercial |
| leadership | Commercial |

Builder nào sinh.

Builder đó sở hữu.

---

# 22. Consumer Rules

Dashboard

↓

Read only.

PDF

↓

Read only.

DOCX

↓

Read only.

REST

↓

Read only.

Không Consumer nào:

- rewrite;
- compose;
- suy luận;
- sửa.

---

# 23. Serialization Rules

Presentation phải serialize được sang:

JSON

Dashboard

PDF

DOCX

REST

Mobile

Không Adapter riêng.

---

# 24. Empty State Rules

Nếu Narrative thiếu.

Overview

↓

Không render.

Interpretation

↓

Không render.

Action

↓

Không render.

Không Consumer nào tự sinh nội dung.

---

# 25. Validation Rules

Presentation Validator phải kiểm tra:

✓ Schema

✓ Customer Safety

✓ Duplicate

✓ Serialization

✓ Required Fields

✓ Version

---

# 26. Customer Safety Rules

Presentation không được chứa:

- JSON
- Rule IDs
- Knowledge IDs
- source_unit_ids
- Debug
- Runtime
- Engine
- Matcher

---

# 27. Duplicate Rules

Overview

↓

không lặp.

Interpretation.

Interpretation

↓

không lặp.

Action.

Action

↓

không lặp.

Commercial.

---

# 28. Presentation Status

```
complete

partial

insufficient

invalid
```

---

# 29. Version Rules

Presentation Version.

Ví dụ

```
bte.presentation.v2
```

Consumer luôn biết.

---

# 30. Compatibility

Minor

↓

Backward Compatible.

Major

↓

Migration.

---

# 31. Traceability

Presentation giữ:

references.

Customer không nhìn thấy.

Internal.

---

# 32. Freeze Rules

Sau Freeze.

Không Builder nào được:

tự thêm field.

Muốn sửa.

↓

Update.

```
04_PRESENTATION_CONTRACT.md
```

↓

Review.

↓

Freeze.

↓

Code.

---

# 33. Presentation Lifecycle

```
Narrative

↓

Presentation

↓

Validation

↓

Freeze

↓

Publish

↓

Consumer
```

Consumer không sửa.

---

# 34. Allowed Consumers

✓ Dashboard

✓ PDF

✓ DOCX

✓ REST

✓ Mobile

Không:

Engine.

---

# 35. Forbidden Consumer Actions

Consumer không được:

- rewrite;
- summarize;
- compose;
- infer;
- calculate.

Consumer chỉ render.

---

# 36. Contract Matrix

| Contract | Builder | Consumer | Editable |
|-----------|----------|----------|----------|
| Overview | Overview Builder | Dashboard/PDF/DOCX | ✗ |
| Interpretation | Interpretation Builder | Dashboard/PDF/DOCX | ✗ |
| Action | Action Builder | Dashboard/PDF/DOCX | ✗ |
| Commercial | Commercial Builder | Dashboard/PDF/DOCX | ✗ |
| Metadata | Narrative | Internal | ✗ |

---

# 37. Presentation Flow

```
Overview Builder

↓

Overview Contract

↓

Dashboard

PDF

DOCX

REST
```

Interpretation.

Action.

Commercial.

đều giống.

---

# 38. Acceptance Criteria

Presentation Contract đạt khi:

✓ Dashboard không compose.

✓ PDF không compose.

✓ DOCX không compose.

✓ REST không compose.

✓ Một Narrative.

↓

Nhiều Consumer.

---

# 39. Final Principle

Presentation Contract không phải là dữ liệu.

Presentation Contract là lời hứa giữa Narrative và Consumer.

Narrative chịu trách nhiệm:

- nói đúng.

Presentation Contract chịu trách nhiệm:

- nói thống nhất.

Consumer chịu trách nhiệm:

- trình bày.

Không thành phần nào được làm thay trách nhiệm của thành phần khác.

---

# 40. Presentation Contract Summary

```
Narrative

↓

Presentation Contract

↓

Dashboard

PDF

DOCX

REST

Mobile
```

Presentation Contract là nguồn dữ liệu duy nhất mà Consumer được phép đọc.

Không Consumer nào được đọc trực tiếp:

Canonical Analysis.

Không Consumer nào được đọc trực tiếp:

Knowledge.

Không Consumer nào được đọc trực tiếp:

Reasoning.

---

# 41. Presentation Stability Policy

Presentation Contract là cam kết giữa Narrative và toàn bộ hệ sinh thái BTE.

Sau khi đã Freeze:

- Không được đổi tên field đã publish.
- Không được đổi ý nghĩa field.
- Không được xóa field trong cùng Major Version.
- Field mới chỉ được thêm theo hướng backward-compatible.
- Consumer phải bỏ qua field mới mà không lỗi.
- Mọi thay đổi Presentation Contract phải cập nhật tài liệu này trước khi code.

Quy trình bắt buộc:

Presentation Contract

↓

Review

↓

Freeze

↓

Implementation

Không được code trước rồi mới cập nhật tài liệu.

---

# 42. Presentation Responsibility Matrix

| Thành phần | Sinh dữ liệu | Rewrite | Render | Chỉnh sửa |
|------------|:------------:|:-------:|:------:|:---------:|
| Narrative Builder | ✓ | ✓ | ✗ | ✓ |
| Presentation Contract | ✓ | ✗ | ✗ | ✗ |
| Dashboard | ✗ | ✗ | ✓ | ✗ |
| PDF | ✗ | ✗ | ✓ | ✗ |
| DOCX | ✗ | ✗ | ✓ | ✗ |
| REST API | ✗ | ✗ | ✓ | ✗ |

Điều này khóa hoàn toàn trách nhiệm:

Narrative sinh.

Presentation chuẩn hóa.

Consumer chỉ hiển thị.

---

# 43. Closing Principle

Presentation Contract không tồn tại để phục vụ Dashboard.

Presentation Contract tồn tại để toàn bộ hệ sinh thái BTE cùng nói một ngôn ngữ.

Nếu Dashboard, PDF, DOCX và API hiển thị khác nhau, Presentation Contract đã thất bại.

Nếu tất cả cùng đọc một Narrative và cùng truyền đạt một ý nghĩa thống nhất, Presentation Contract đã hoàn thành nhiệm vụ.

> **Consumer có thể thay đổi giao diện.**
>
> **Narrative có thể cải thiện câu chữ.**
>
> **Nhưng Presentation Contract không được phá vỡ lời hứa đã công bố.**