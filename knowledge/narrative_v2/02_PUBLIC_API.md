# NARRATIVE V2 — PUBLIC API

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Tài liệu này định nghĩa Public API của Narrative V2.

Public API không phải REST API.

Public API là contract giữa:

```
Narrative V2

↓

Portal

↓

Report Engine

↓

PDF

↓

DOCX

↓

External API
```

Public API định nghĩa:

- input
- output
- lifecycle
- ownership
- compatibility

Không mô tả UI.

Không mô tả Engine.

---

# 2. Design Goals

Narrative Public API phải đạt các mục tiêu sau:

✓ Deterministic

✓ Stable

✓ Customer-safe

✓ Versioned

✓ Reusable

✓ Backward Compatible

---

# 3. Public Architecture

```
Canonical Analysis

↓

Narrative V2

↓

Public API

↓

Dashboard

PDF

DOCX

REST API

Mobile
```

Mọi consumer đều đọc cùng một Public API.

---

# 4. Public Philosophy

Narrative chỉ publish:

```
Customer Meaning
```

Không publish:

- Engine logic
- Rule IDs
- JSON debug
- Internal objects

---

# 5. Public Input

Narrative chỉ có một input chính thức.

```
CanonicalAnalysis
```

Narrative không nhận:

- UI Model
- Report Model
- PDF Model
- Legacy Payload

---

# 6. Public Output

Output duy nhất:

```
NarrativeV2Result
```

Không publish:

Builder Object

Knowledge Object

Evidence Context

Reasoning Context

Commercial Rewrite Context

---

# 7. Public Contract

```
NarrativeV2Result

status

overview

interpretation

action_plan

commercial

metadata
```

Đây là contract duy nhất.

---

# 8. Overview API

```
OverviewSummary

headline

summary

identity

balance

conclusion
```

Dashboard

↓

Overview Card

PDF

↓

Overview Section

---

# 9. Interpretation API

```
InterpretationNarrative

overview

observation

reasoning

meaning

impact

recommendation

closing
```

Public Presentation contract (N-IMP-09A):

```
InterpretationPresentation

overview

observation

reasoning

meaning

impact

recommendation

closing

consulting_flow
```

`meaning` is copied from InterpretationNarrative.

`consulting_flow` is copied from ConsultingNarrative.flow.

Structured fields and consulting flow coexist. Consumers must not regenerate either.

Không expose:

Engine reasoning.

Conversation trace.

Consulting style ids.

---

# 10. Action Plan API

```
ActionPlanNarrative

top_priority

actions

warnings

current_period
```

Action phải là customer-facing.

---

# 11. Commercial API

```
CommercialNarrative

career

finance

relationship

health

leadership
```

Optional.

---

# 12. Metadata API

```
NarrativeMetadata

version

status

language

created_at
```

Không render.

---

# 13. Status API

Status chuẩn:

```
complete

partial

insufficient

invalid
```

Ý nghĩa:

complete

↓

Narrative đầy đủ.

partial

↓

Thiếu optional.

insufficient

↓

Không đủ dữ liệu.

invalid

↓

Không publish.

---

# 14. Builder APIs

Narrative Builder chỉ expose:

```
build_overview()

build_interpretation()

build_action_plan()

build_commercial()

build_narrative()
```

Không expose internal Builder.

---

# 15. Overview Builder API

```
build_overview(

CanonicalAnalysis

)

↓

OverviewSummary
```

---

# 16. Interpretation Builder API

```
build_interpretation(

CanonicalAnalysis

)

↓

InterpretationNarrative
```

---

# 17. Action Builder API

```
build_action_plan(

CanonicalAnalysis

)

↓

ActionPlanNarrative
```

---

# 18. Commercial Builder API

```
build_commercial(

CanonicalAnalysis

)

↓

CommercialNarrative
```

---

# 19. Master Builder API

```
build_narrative(

CanonicalAnalysis

)

↓

NarrativeV2Result
```

Đây là API chính.

---

# 20. Consumer APIs

Các Consumer chỉ được gọi:

```
NarrativeV2Result
```

Không gọi Builder.

Không đọc Context.

---

# 21. Dashboard API

Dashboard chỉ đọc:

```
overview

interpretation

action_plan

commercial
```

Không compose.

---

# 22. PDF API

PDF chỉ đọc:

```
NarrativeV2Result
```

Không rewrite.

---

# 23. DOCX API

Giống PDF.

---

# 24. REST API

REST chỉ serialize:

```
NarrativeV2Result
```

Không expose Debug.

---

# 25. Serialization

Narrative phải serialize được sang:

JSON

Dashboard

PDF

DOCX

không cần Adapter mới.

---

# 26. Versioning

Public API phải có version.

Ví dụ

```
bte.narrative.public.v2
```

---

# 27. Compatibility

Minor Version

↓

Backward Compatible.

Major Version

↓

Migration Required.

---

# 28. Public Safety

Không publish:

JSON

Rule IDs

Engine IDs

Confidence Token

Debug

Knowledge IDs

Source IDs

---

# 29. Public Validation

Narrative Validator phải kiểm tra:

✓ Schema

✓ Version

✓ Customer Safety

✓ Serialization

✓ Compatibility

---

# 30. Error Contract

Narrative API chỉ có bốn trạng thái:

```
complete

partial

insufficient

invalid
```

Không throw customer-facing exception.

---

# 31. Ownership

| API | Owner |
|------|-------|
| CanonicalAnalysis | Engine |
| Narrative Builders | Narrative |
| NarrativeV2Result | Narrative |
| Dashboard | Portal |
| PDF | Report |
| DOCX | Report |

---

# 32. Public Lifecycle

```
Create

↓

Validate

↓

Freeze

↓

Publish

↓

Consume
```

Không Consumer nào được sửa.

---

# 33. API Dependency

```
Engine

↓

Narrative

↓

Public API

↓

Consumer
```

Không phụ thuộc ngược.

---

# 34. Allowed Consumers

✓ Dashboard

✓ PDF

✓ DOCX

✓ REST

✓ Mobile

Không:

Engine

---

# 35. Forbidden Usage

Không Consumer nào được:

- rewrite Narrative
- compose Narrative
- sinh Recommendation
- sửa Overview

---

# 36. API Stability

Mọi field publish phải:

- stable
- documented
- versioned

---

# 37. Migration

Legacy:

```
Pack05
```

↓

Narrative V2

↓

Public API

↓

Legacy retire

---

# 38. Acceptance Criteria

Public API đạt khi:

✓ Dashboard đọc được.

✓ PDF đọc được.

✓ DOCX đọc được.

✓ API đọc được.

✓ Không duplicate.

✓ Không expose Debug.

✓ Không expose Engine.

---

# 39. Freeze Rules

Sau Freeze.

Không Builder nào được:

tự thêm field.

Mọi thay đổi phải sửa:

```
02_PUBLIC_API.md
```

trước.

---

# 40. Public API Summary

```
CanonicalAnalysis

↓

build_narrative()

↓

NarrativeV2Result

↓

Dashboard

PDF

DOCX

REST

Mobile
```

Narrative chỉ có **một Public API**.

Không có Dashboard API.

Không có PDF API.

Không có DOCX API.

Tất cả cùng đọc một Narrative.

# 41. API Stability Policy

Narrative Public API là hợp đồng chính thức giữa Narrative V2 và toàn bộ Consumer.

Một khi Public API đã được Product Owner phê duyệt và phát hành, mọi thay đổi đều phải tuân thủ chính sách ổn định dưới đây.

---

# 41.1 Compatibility First

Public API luôn ưu tiên khả năng tương thích.

Mọi thay đổi phải được đánh giá theo nguyên tắc:

```
Existing Consumer

↓

must continue to work.
```

Nếu một Dashboard đang chạy đúng với Public API V2.

Sau khi Narrative nâng cấp:

Dashboard vẫn phải hoạt động.

---

# 41.2 No Breaking Changes

Trong cùng Major Version:

```
V2.x
```

Không được:

- đổi tên field;
- đổi kiểu dữ liệu;
- xóa field đã publish;
- thay đổi ý nghĩa field.

Ví dụ:

Sai:

```
overview.summary

↓

overview.text
```

Sai.

---

Sai:

```
recommendation

string

↓

array
```

Sai.

---

# 41.3 Additive Evolution

Field mới chỉ được thêm theo hướng mở rộng.

Ví dụ:

```
NarrativeV2Result

overview

interpretation

action_plan
```

↓

cho phép thêm:

```
commercial

```

hoặc:

```
metadata
```

Nhưng không được sửa field cũ.

---

# 41.4 Consumer Tolerance

Mọi Consumer phải được thiết kế để:

- bỏ qua field chưa biết;
- không lỗi nếu Narrative có thêm field mới.

Ví dụ:

```
overview

interpretation

action_plan

↓

overview

interpretation

action_plan

commercial
```

Dashboard cũ vẫn chạy.

---

# 41.5 Version Declaration

Mỗi Public API phải khai báo rõ:

```
api_version

narrative_version

knowledge_version
```

Consumer luôn biết mình đang đọc phiên bản nào.

---

# 41.6 Deprecation Policy

Không xóa ngay field cũ.

Quy trình chuẩn:

```
Publish

↓

Deprecated

↓

Migration

↓

Removal
```

Một field chỉ được phép xóa sau khi:

- đã Deprecated;
- Consumer đã Migration;
- Product Owner phê duyệt.

---

# 41.7 Builder Responsibility

Builder không được tự ý thêm field mới.

Mọi field mới phải:

1. được bổ sung vào:

```
02_PUBLIC_API.md
```

2. được Product Owner duyệt;

3. được cập nhật Version.

Sau đó mới được code.

---

# 41.8 Consumer Responsibility

Dashboard

PDF

DOCX

REST

Mobile

không được:

- tự sinh field;
- tự đổi tên field;
- tự sửa ý nghĩa field.

Consumer chỉ đọc.

---

# 41.9 Schema Validation

Narrative Validator phải kiểm tra:

✓ field tồn tại đúng schema

✓ field đúng kiểu

✓ field đúng version

✓ field không deprecated ngoài quy trình

✓ field không bị đổi semantic

Nếu vi phạm:

```
status = invalid
```

Không publish.

---

# 41.10 Semantic Stability

Không chỉ tên field.

Ý nghĩa của field cũng phải ổn định.

Ví dụ:

```
overview.summary
```

luôn có nghĩa:

"Tóm tắt tổng quan."

Không được ở Version sau đổi thành:

"Hành động."

Giữ nguyên Semantic.

---

# 41.11 Documentation First

Không được:

Code trước.

Tài liệu sau.

Quy trình bắt buộc:

```
Public API

↓

Review

↓

Freeze

↓

Implementation
```

---

# 41.12 Freeze Rule

Sau khi Public API Freeze.

Mọi thay đổi phải mở:

```
Narrative Public API Revision
```

Không sửa trực tiếp.

Không commit âm thầm.

---

# 41.13 Compatibility Matrix

| Change | Allowed | Notes |
|----------|:------:|------|
| Thêm field mới | ✓ | Backward compatible |
| Thêm metadata | ✓ | Không ảnh hưởng Consumer |
| Thêm optional object | ✓ | Consumer có thể bỏ qua |
| Đổi tên field | ✗ | Breaking Change |
| Đổi kiểu dữ liệu | ✗ | Breaking Change |
| Xóa field | ✗ | Phải qua Deprecation |
| Đổi ý nghĩa field | ✗ | Semantic Breaking Change |
| Đổi version | ✓ | Theo Version Policy |

---

# 41.14 Final API Principle

Narrative Public API không chỉ là cấu trúc dữ liệu.

Narrative Public API là cam kết ổn định giữa Narrative và toàn bộ hệ sinh thái BTE.

Mọi Builder đều có thể thay đổi.

Mọi Knowledge đều có thể mở rộng.

Mọi UI đều có thể được thiết kế lại.

Nhưng Public API phải luôn giữ lời hứa với Consumer.

Đó là nền tảng để Dashboard, PDF, DOCX, Mobile và API có thể phát triển độc lập mà không phá vỡ lẫn nhau.

**Một Public API tốt không chỉ giúp hệ thống chạy hôm nay.**

**Nó giúp hệ thống vẫn ổn định sau nhiều năm phát triển.**