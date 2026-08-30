# NARRATIVE V2 — DATA MODEL

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Tài liệu này định nghĩa toàn bộ Data Model của Narrative V2.

Data Model là cầu nối giữa:

```
Canonical Analysis

↓

Narrative Builders

↓

Customer Narrative
```

Mọi Builder của Narrative V2 phải sử dụng các object được định nghĩa tại đây.

Không Builder nào được tự định nghĩa model riêng.

---

# 2. Design Principles

Narrative Data Model phải tuân thủ các nguyên tắc sau.

## 2.1 Immutable

Builder không được sửa dữ liệu đầu vào.

Mỗi Builder tạo object mới.

---

## 2.2 Deterministic

Cùng:

```
Canonical Analysis

+

Knowledge Version

+

Narrative Version
```

↓

luôn sinh cùng một Narrative.

---

## 2.3 Traceable

Mọi Narrative đều truy ngược được:

```
Narrative

↓

Knowledge

↓

Evidence

↓

Canonical Analysis
```

---

## 2.4 Customer Safe

Presentation Object không được chứa:

- JSON
- Rule IDs
- Engine IDs
- Debug
- Internal Metadata

---

# 3. Data Model Overview

```
CanonicalAnalysis
        ↓
EvidenceContext
        ↓
ReasoningContext
        ↓
KnowledgeContext
        ↓
CommercialRewriteContext
        ↓
OverviewSummary
        ↓
InterpretationNarrative
        ↓
ActionPlanNarrative
        ↓
CommercialNarrative
        ↓
NarrativeV2Result
```

---

# 4. CanonicalAnalysis

Narrative không sở hữu CanonicalAnalysis.

Narrative chỉ đọc.

```
CanonicalAnalysis

identity

bazi

strength

temperature

pattern

useful_god

five_elements

ten_gods

shensha

luck

calendar

score

metadata
```

Đây là input duy nhất.

---

# 5. EvidenceContext

Purpose

Thu thập Evidence.

```
EvidenceContext

identity

strength

pattern

useful_god

temperature

five_elements

ten_gods

shensha

luck

references
```

EvidenceContext không có:

- câu
- giải thích
- recommendation

---

# 6. EvidenceItem

Một Evidence nhỏ nhất.

```
EvidenceItem

id

domain

label

value

confidence

references

metadata
```

Ví dụ

```
domain

strength

label

Thân

value

Thân vượng
```

---

# 7. ReasoningContext

ReasoningContext kết nối nhiều Evidence.

```
ReasoningContext

observations

reasonings

impacts

boundaries
```

Ví dụ

```
Observation

Nội lực tốt.

Reasoning

Do thân vượng.

Impact

Chịu trách nhiệm tốt.
```

---

# 8. Observation

```
Observation

title

content

references

confidence
```

Đây chưa phải customer sentence cuối.

---

# 9. ReasoningNode

```
ReasoningNode

cause

effect

evidence

knowledge

trace
```

Ví dụ

```
Cause

Strength

↓

Effect

Nội lực.
```

---

# 10. KnowledgeContext

KnowledgeContext chứa toàn bộ tri thức đã Resolve.

```
KnowledgeContext

summary

interpretation

actions

warnings

commercial

references
```

KnowledgeContext chỉ chứa tri thức Approved.

---

# 11. KnowledgeItem

```
KnowledgeItem

id

domain

priority

customer_text

technical_text

references
```

technical_text

không render.

---

# 12. CommercialRewriteContext

Commercial Rewrite không sinh tri thức.

Commercial Rewrite chỉ đổi ngôn ngữ.

```
CommercialRewriteContext

technical

semantic

customer

style
```

---

# 13. RewriteItem

```
RewriteItem

source

semantic

customer

style

references
```

Ví dụ

```
Technical

Thân vượng.

↓

Customer

Bạn có nội lực tốt.
```

---

# 14. OverviewSummary

Đầu ra cho Card Overview.

```
OverviewSummary

headline

summary

identity

balance

conclusion

references
```

Không chứa:

JSON

Engine

Debug

---

# 15. InterpretationNarrative

```
InterpretationNarrative

overview

observation

reasoning

meaning

impact

recommendation

closing

references
```

Đây là Narrative đầy đủ.

`meaning` is a canonical formula stage. Presentation must copy it when present.

Revision N-IMP-09A: restored `meaning` on the public Interpretation Presentation contract. Continuous consulting prose is owned by ConsultingNarrative (`flow`) and published as Presentation `consulting_flow`.

---

# 16. InterpretationBlock

```
InterpretationBlock

title

content

references

priority
```

Ví dụ

```
Quan sát

...

```

---

# 17. ActionPlanNarrative

```
ActionPlanNarrative

top_priority

actions

warnings

current_period

references
```

---

# 18. ActionItem

```
ActionItem

title

description

domain

priority

references
```

Ví dụ

```
title

Giữ nền hiện tại.

description

...
```

---

# 19. WarningItem

```
WarningItem

title

description

severity

references
```

severity

chỉ internal.

Không render.

---

# 20. CommercialNarrative

```
CommercialNarrative

career

finance

relationship

health

leadership

references
```

Đây là optional.

---

# 21. NarrativeMetadata

```
NarrativeMetadata

version

knowledge_version

rewrite_version

language

status

created_at
```

Không render.

---

# 22. NarrativeTrace

```
NarrativeTrace

evidence

reasoning

knowledge

rewrite
```

Debug only.

---

# 23. NarrativeReference

```
NarrativeReference

domain

source

knowledge_id

evidence_id
```

Không render.

---

# 24. NarrativeStatus

```
complete

partial

insufficient

invalid
```

---

# 25. NarrativeV2Result

Đây là output chuẩn.

```
NarrativeV2Result

status

overview

interpretation

action_plan

commercial

metadata

trace
```

Dashboard

↓

đọc object này.

PDF

↓

đọc object này.

DOCX

↓

đọc object này.

API

↓

đọc object này.

---

# 26. Ownership

| Object | Owner |
|----------|--------|
| CanonicalAnalysis | Engine |
| EvidenceContext | Narrative |
| ReasoningContext | Narrative |
| KnowledgeContext | Narrative |
| CommercialRewriteContext | Narrative |
| OverviewSummary | Narrative |
| InterpretationNarrative | Narrative |
| ActionPlanNarrative | Narrative |
| CommercialNarrative | Narrative |
| NarrativeV2Result | Narrative |

---

# 27. Data Flow

```
CanonicalAnalysis

↓

EvidenceContext

↓

ReasoningContext

↓

KnowledgeContext

↓

CommercialRewrite

↓

Overview

↓

Interpretation

↓

ActionPlan

↓

NarrativeV2Result
```

Không Builder nào được bỏ qua Pipeline.

---

# 28. Object Lifecycle

```
Create

↓

Validate

↓

Rewrite

↓

Publish

↓

Freeze
```

Object sau Publish không được sửa.

---

# 29. Validation Rules

Mọi Object phải kiểm tra:

Schema

↓

References

↓

Customer Safety

↓

Duplicate

↓

Style

↓

Publish

---

# 30. Serialization

NarrativeV2Result phải serialize được sang:

Dashboard

PDF

DOCX

API

JSON

không cần Adapter riêng.

---

# 31. Versioning

Narrative Object phải ghi:

```
Narrative Version

Knowledge Version

Presentation Version
```

---

# 32. Extension Rules

Không sửa object cũ.

Chỉ mở rộng.

Ví dụ

```
ActionItem

↓

ActionItemV2
```

nếu cần.

---

# 33. Backward Compatibility

Narrative V2 phải đọc được:

Pack05

Commercial Consulting

Legacy Narrative

cho tới khi Legacy retire.

---

# 34. Performance

Object không chứa dữ liệu dư.

Không copy toàn CanonicalAnalysis.

Chỉ giữ phần Narrative cần.

---

# 35. Freeze Rules

Sau khi Product Owner Freeze.

Không Builder nào được tự thêm field.

Mọi thay đổi phải sửa:

```
01_DATA_MODEL.md
```

trước.

---

# 36. Canonical Data Model Summary

```
CanonicalAnalysis

↓

EvidenceContext

↓

ReasoningContext

↓

KnowledgeContext

↓

CommercialRewriteContext

↓

OverviewSummary

↓

InterpretationNarrative

↓

ActionPlanNarrative

↓

CommercialNarrative

↓

NarrativeV2Result
```

Đây là Data Model chính thức của Narrative V2.

# 37. Object Responsibility Matrix

Narrative V2 được thiết kế theo nguyên tắc:

> **Một Object chỉ có một trách nhiệm duy nhất.**

Mỗi Object chỉ được phép thực hiện đúng vai trò của mình.

Không Object nào được thực hiện trách nhiệm của Object khác.

Điều này giúp:

- tránh trùng lặp logic;
- tránh UI tự sinh Narrative;
- tránh Builder tự tính Astrology;
- tránh Knowledge bị phân tán;
- đảm bảo toàn bộ hệ thống có thể kiểm thử độc lập.

---

## 37.1 Responsibility Matrix

| Object | Đọc Canonical | Dùng Knowledge | Reasoning | Rewrite | Customer-facing | Render trực tiếp |
|----------|:------------:|:--------------:|:---------:|:-------:|:---------------:|:----------------:|
| CanonicalAnalysis | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| EvidenceContext | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| ReasoningContext | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| KnowledgeContext | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| CommercialRewriteContext | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| OverviewSummary | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| InterpretationNarrative | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ActionPlanNarrative | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CommercialNarrative | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| NarrativeV2Result | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 37.2 Responsibility Definition

### CanonicalAnalysis

Chịu trách nhiệm duy nhất:

- lưu giữ sự thật đã được Astrology Engine tính toán.

Không được:

- giải thích;
- rewrite;
- viết câu;
- recommendation.

---

### EvidenceContext

Chịu trách nhiệm:

- chọn các Evidence cần cho Narrative.

Không được:

- reasoning;
- kết luận;
- rewrite.

---

### ReasoningContext

Chịu trách nhiệm:

- kết nối Evidence thành lập luận.

Không được:

- viết theo văn phong khách hàng;
- commercial rewrite.

---

### KnowledgeContext

Chịu trách nhiệm:

- cung cấp tri thức đã được phê duyệt.

Không được:

- thay đổi Canonical Analysis;
- tạo Narrative mới.

---

### CommercialRewriteContext

Chịu trách nhiệm:

- chuyển ngôn ngữ chuyên môn thành ngôn ngữ khách hàng.

Không được:

- thay đổi ý nghĩa;
- tạo thêm tri thức;
- suy luận ngoài Evidence.

---

### OverviewSummary

Chịu trách nhiệm:

- tạo phần tóm tắt đầu tiên của Dashboard.

Không được:

- lặp Interpretation;
- thay Action Plan.

---

### InterpretationNarrative

Chịu trách nhiệm:

- giải thích toàn bộ lá số.

Không được:

- tạo hành động cụ thể;
- thay Commercial Consulting.

---

### ActionPlanNarrative

Chịu trách nhiệm:

- chuyển Recommendation thành hành động.

Không được:

- suy luận từ raw Astrology;
- tự tạo Action.

---

### CommercialNarrative

Chịu trách nhiệm:

- sinh Narrative theo từng lĩnh vực:

    - Career
    - Finance
    - Relationship
    - Health
    - Leadership
    - Business

Không được:

- thay Overall Interpretation.

---

### NarrativeV2Result

Chịu trách nhiệm:

- publish toàn bộ Narrative.

Không được:

- rewrite;
- reasoning;
- bổ sung dữ liệu.

---

# 37.3 Allowed Dependency Matrix

Narrative V2 chỉ cho phép phụ thuộc theo một chiều.

```
CanonicalAnalysis
        ↓
EvidenceContext
        ↓
ReasoningContext
        ↓
KnowledgeContext
        ↓
CommercialRewriteContext
        ↓
OverviewSummary
        ↓
InterpretationNarrative
        ↓
ActionPlanNarrative
        ↓
CommercialNarrative
        ↓
NarrativeV2Result
```

Không được phép phụ thuộc ngược.

Ví dụ:

```
ActionPlan

↓

Reasoning
```

là **không hợp lệ**.

---

# 37.4 Forbidden Responsibilities

Các hành vi dưới đây bị cấm.

## UI

Không được:

- rewrite;
- reasoning;
- sinh Recommendation;
- suy luận Astrology.

---

## Builder

Không được:

- gọi Engine;
- tính lại Bát Tự;
- tạo Rule mới.

---

## Knowledge

Không được:

- thay Engine;
- tính toán;
- sửa Canonical Truth.

---

## Commercial Rewrite

Không được:

- thay đổi ý nghĩa;
- thêm tri thức;
- suy diễn.

---

# 37.5 Responsibility Validation

Narrative Validator phải kiểm tra:

✓ Object có đúng trách nhiệm không.

✓ Có vượt phạm vi không.

✓ Có dùng sai Dependency không.

✓ Có tạo Narrative ngoài Pipeline không.

Nếu phát hiện Object vi phạm Responsibility Matrix:

```
status = invalid
```

và không được publish.

---

# 37.6 Architectural Principle

Mỗi Object chỉ nên trả lời đúng **một câu hỏi**.

| Object | Câu hỏi phải trả lời |
|----------|----------------------|
| CanonicalAnalysis | Điều gì là sự thật? |
| EvidenceContext | Evidence nào quan trọng? |
| ReasoningContext | Tại sao lại như vậy? |
| KnowledgeContext | Có tri thức nào hỗ trợ? |
| CommercialRewriteContext | Khách hàng sẽ hiểu câu này như thế nào? |
| OverviewSummary | Điều gì quan trọng nhất? |
| InterpretationNarrative | Lá số này nói gì? |
| ActionPlanNarrative | Nên làm gì tiếp theo? |
| CommercialNarrative | Áp dụng theo từng lĩnh vực như thế nào? |
| NarrativeV2Result | Công bố Narrative cuối cùng. |

Nếu một Object trả lời nhiều hơn một câu hỏi trên, kiến trúc đã bắt đầu bị pha trộn và cần được xem xét lại.

---

# 37.7 Final Responsibility Principle

Toàn bộ Narrative V2 phải tuân thủ nguyên tắc sau:

> **Một Object – Một Trách Nhiệm – Một Đầu Ra.**

Đây là quy tắc nền tảng giúp:

- Narrative luôn đơn giản;
- Builder luôn độc lập;
- UI luôn thuần Presentation;
- Engine luôn giữ quyền quyết định sự thật;
- toàn bộ BTE Platform có thể mở rộng lâu dài mà không làm mất tính nhất quán của kiến trúc.