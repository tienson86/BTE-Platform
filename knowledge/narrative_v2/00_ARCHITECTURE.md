# NARRATIVE V2 — ARCHITECTURE

**Commercial Narrative Architecture for BTE Platform**

Version: V2.0  
Status: DESIGN / PRE-IMPLEMENTATION  
Owner: BTE Platform  
Module: `knowledge/narrative_v2/`

---

# 1. Purpose

Tài liệu này định nghĩa kiến trúc chuẩn của **Narrative V2** cho BTE Platform.

Narrative V2 là lớp chịu trách nhiệm chuyển:

- kết quả phân tích Bát Tự đã được canonical hóa,
- tri thức đã được phê duyệt,
- reasoning đã được xác định,

thành nội dung mà khách hàng có thể:

- đọc,
- hiểu,
- đối chiếu,
- và hành động.

Narrative V2 **không phải Astrology Engine**.

Narrative V2 không tính:

- Tứ Trụ,
- Nhật Chủ,
- Thân vượng / nhược,
- Ngũ Hành,
- Thập Thần,
- Mệnh Cục,
- Dụng Thần,
- Thần Sát,
- Đại Vận.

Các kết quả trên phải được cung cấp bởi Canonical Analysis.

Narrative V2 chỉ chịu trách nhiệm:

```text
Canonical Truth
        ↓
Reasoning
        ↓
Commercial Communication
        ↓
Customer Narrative
2. Architectural Mission
Narrative V2 giải quyết ba vấn đề lớn của hệ thống hiện tại.
2.1 Technical language leakage
Các output hiện tại có thể chứa:
- thuật ngữ chuyên môn,
- câu kỹ thuật,
- tên Engine,
- rule ids,
- JSON runtime,
- câu dạng diagnostic,
- câu ghép máy móc.
Narrative V2 phải chặn toàn bộ lớp ngôn ngữ đó trước khi tới khách hàng.
2.2 Fragmented narrative
Hiện dữ liệu có thể tồn tại tại nhiều nguồn:
Strength
Pattern
Useful God
Ten Gods
ShenSha
Luck
Narrative Result
Commercial Consulting
Nếu mỗi UI Card tự compose, hệ thống sẽ:
- lặp nội dung,
- mâu thuẫn,
- khó kiểm soát,
- khó tái sử dụng,
- khó đồng bộ PDF/DOCX.
Narrative V2 tạo ra một Narrative Contract duy nhất.
2.3 Technical correctness without customer value
Một câu có thể đúng về thuật toán nhưng không có giá trị với khách hàng.
Ví dụ:
Thân vượng.
là một kết quả kỹ thuật.
Nhưng khách hàng cần hiểu:
Bạn có nội lực tốt và thường có xu hướng tự đảm nhận nhiều trách nhiệm.
Narrative V2 là tầng chuyển đổi giữa hai cấp độ này.

3. Core Architecture
Kiến trúc tổng thể:
┌──────────────────────────────────────┐
│          ASTROLOGY ENGINES           │
│                                      │
│ Calendar                             │
│ BaZi                                 │
│ Strength                             │
│ Temperature                          │
│ Pattern                              │
│ Useful God                           │
│ Ten Gods                             │
│ ShenSha                              │
│ Luck                                 │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       CANONICAL ANALYSIS LAYER       │
│                                      │
│ Published structured truth           │
│ Stable customer-relevant fields      │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          NARRATIVE V2                │
│                                      │
│ 1. Evidence Builder                  │
│ 2. Reasoning Builder                 │
│ 3. Knowledge Resolver                │
│ 4. Commercial Rewrite Engine         │
│ 5. Summary Builder                   │
│ 6. Interpretation Builder            │
│ 7. Action Builder                    │
│ 8. Narrative Validator               │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│      NARRATIVE PRESENTATION CONTRACT │
│                                      │
│ overview_summary                     │
│ interpretation                       │
│ action_plan                          │
│ commercial_sections                  │
│ metadata / traceability              │
└──────────────────┬───────────────────┘
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
   Dashboard      PDF          DOCX
       │
       ▼
      API

4. Architectural Principles
Narrative V2 bắt buộc tuân thủ các nguyên tắc sau.
4.1 Engine owns truth
Engine quyết định:
What is true.

Narrative quyết định:
How truth is communicated.
Narrative không được sửa kết quả Engine.

4.2 Narrative owns customer language
Customer-facing interpretation phải được sinh ở Narrative Layer.
Không được để:
- React,
- HTML template,
- PDF renderer,
- DOCX exporter
tự tạo nghĩa.
4.3 UI is presentation-only
UI chỉ được:
- nhận Narrative Contract,
- render,
- expand/collapse,
- format typography.
UI không được:
- reasoning,
- mapping raw astrology → meaning,
- sinh recommendation,
- ghép narrative.
4.4 One narrative, many outputs
Một Narrative phải dùng chung cho:
Dashboard
PDF
DOCX
API
Mobile

Không có một bản Narrative riêng cho từng surface.
4.5 Evidence first
Không có kết luận nếu không có evidence.
Canonical flow:
Evidence
   ↓
Reasoning
   ↓
Meaning
   ↓
Recommendation
4.6 Commercial rewrite is mandatory
Một câu kỹ thuật không được đi trực tiếp tới customer output nếu:
- khó hiểu,
- nội bộ,
- học thuật,
- không actionable.
Commercial Rewrite phải chuyển nó thành customer language trước khi publish.
5. Narrative Layers
Narrative V2 gồm tám layer logic chính.
5.1 Evidence Builder
Responsibility
Thu thập các dữ liệu canonical cần thiết cho Narrative.
Input
CanonicalAnalysis
Output
NarrativeEvidenceContext
Example evidence
Day Master
Strength
Pattern
Useful God
Temperature
Ten Gods
Five Elements
ShenSha
Luck
Evidence Builder MUST NOT
- giải thích,
- kết luận,
- khuyến nghị,
- sinh prose.
Evidence Builder chỉ tạo context.
5.2 Reasoning Builder
Responsibility
Xác định mối liên hệ logic giữa các evidence đã được publish.
Ví dụ:
Strength
+
Pattern
+
Useful God
↓
Reasoning Context
Purpose
Trả lời:
Vì sao?
Reasoning Builder không trả lời:
Nên làm gì?
Rules
Reasoning phải:
- deterministic,
- traceable,
- không tự thay đổi Engine truth.
5.3 Knowledge Resolver
Responsibility
Tìm tri thức đã được approved phù hợp với evidence và reasoning.
Nguồn có thể gồm:
knowledge/interpretation/
knowledge/consulting_knowledge/
approved domain knowledge
sentence libraries
template libraries
Rules
Knowledge Resolver không được:
- sinh tri thức mới,
- gọi mạng,
- gọi LLM runtime,
- suy diễn ngoài catalog.
5.4 Commercial Rewrite Engine
Đây là layer bắt buộc của Narrative V2.
Responsibility
Chuyển:
Technical Meaning
thành:
Customer Meaning
Example
Technical:
Thân vượng.
Commercial:
Bạn có nội lực tốt và thường chủ động gánh trách nhiệm.
Technical:
Giữ biên hiện có.
Commercial:
Nên phát triển dựa trên nền tảng hiện tại thay vì thay đổi quá đột ngột.
Commercial Rewrite MUST
- giữ nguyên semantic,
- đơn giản hóa ngôn ngữ,
- loại technical jargon khi không cần,
- giữ giọng tư vấn chuyên nghiệp.
Commercial Rewrite MUST NOT
- tạo astrology conclusion mới,
- đổi nghĩa,
- phóng đại,
- tuyệt đối hóa,
- tạo recommendation ngoài nguồn.
5.5 Overview Summary Builder
Responsibility
Sinh:
overview_summary
Purpose
Trả lời:
Trong 15–30 giây đầu, khách hàng cần hiểu điều gì về lá số?
Output
Ngắn.
Không phải report đầy đủ.
Không lặp raw labels.
5.6 Interpretation Builder
Responsibility
Sinh luận giải tổng thể theo cấu trúc:
Observation
Reasoning
Impact
Recommendation
hoặc Presentation Contract tương đương.
Purpose
Giải thích:
Điều gì nổi bật?
Tại sao?
Ảnh hưởng thế nào?
Nên xử lý ra sao?
5.7 Action Builder
Responsibility
Chuyển approved recommendations thành hành động.
Canonical structure:
Top Priority
Recommended Actions
Warnings / Avoid
Current Period Watch
Action Builder MUST NOT
tự tạo action từ:
Useful God
Ten Gods
ShenSha
Luck
Strength
Nếu chưa có approved knowledge/recommendation.
5.8 Narrative Validator
Responsibility
Kiểm tra Narrative trước khi publish.
Validator phải kiểm tra:
- semantic safety,
- source traceability,
- technical leakage,
- duplicate content,
- unsupported conclusion,
- unsupported recommendation,
- empty state,
- customer readability.
Narrative không qua Validator thì không được publish.
6. Canonical Runtime Pipeline
Runtime chuẩn:
Canonical Analysis
        ↓
build_evidence_context()
        ↓
build_reasoning_context()
        ↓
resolve_approved_knowledge()
        ↓
commercial_rewrite()
        ↓
build_overview_summary()
        ↓
build_interpretation()
        ↓
build_action_plan()
        ↓
validate_narrative()
        ↓
NarrativeV2Result
Không stage nào được bỏ qua nếu output đó được publish.
7. Narrative Object Architecture
Narrative V2 sử dụng ba lớp object.
7.1 Internal Evidence Objects
Ví dụ:
EvidenceItem
ReasoningNode
KnowledgeReference
Đây là internal objects.
Không customer-facing.
7.2 Narrative Domain Objects
Ví dụ:
OverviewNarrative
InterpretationNarrative
ActionPlanNarrative
CommercialNarrativeSection
Đây là các object trung gian đã có customer semantics.
7.3 Presentation Objects
Đây là output cho external surfaces.
Ví dụ:
NarrativeV2Presentation
Chỉ chứa customer-safe fields.
8. Builder Architecture
Narrative Builder không phải một function khổng lồ.
Kiến trúc:
NarrativeOrchestrator
        ↓
OverviewSummaryBuilder
InterpretationBuilder
ActionBuilder
CommercialSectionBuilder
Mỗi Builder:
- có input contract riêng,
- output contract riêng,
- validator riêng.
9. Rewrite Architecture
Commercial Rewrite gồm ba bước.
Technical Statement
        ↓
Semantic Normalization
        ↓
Customer Rewrite
        ↓
Style Validation
9.1 Semantic Normalization
Chuẩn hóa ý nghĩa gốc.
Ví dụ:
term
meaning
impact
boundary
9.2 Customer Rewrite
Chuyển semantic sang câu khách hàng.
9.3 Style Validation
Kiểm tra:
- quá kỹ thuật,
- quá dài,
- tuyệt đối,
- mơ hồ,
- sáo rỗng,
- lặp.
10. Presentation Contract
Narrative V2 phải publish một contract duy nhất.
Canonical example:
NarrativeV2Result

status

overview_summary

interpretation

action_plan

commercial_sections

references

metadata
10.1 overview_summary
Customer-safe overview.
10.2 interpretation
Structured narrative:
observation
reasoning
impact
recommendation
closing
10.3 action_plan
Structured action data:
top_priority
actions
warnings
current_period
10.4 commercial_sections
Optional consulting domains.
10.5 references
Internal traceability only.
Không render trực tiếp ra customer UI.
11. Integration Architecture
Narrative V2 tích hợp với hệ thống qua:
Analysis Orchestrator
        ↓
Narrative V2
        ↓
ReportInputV1 / successor
        ↓
Portal
PDF
DOCX
API
Narrative V2 không gọi Portal.
Portal đọc Narrative V2.
12. Runtime Sequence
Canonical runtime:
POST /api/v1/analyze

↓

Orchestrator

↓

Canonical Analysis

↓

Narrative V2

↓

NarrativeV2Result

↓

ResultStore

↓

Customer Portal

↓

Report Engine

↓

PDF / DOCX
Narrative phải hoàn thành trước khi result được publish.
13. Data Ownership
Ownership được khóa như sau.
Data	Owner
Tứ Trụ	BaZi Engine
Strength	Strength Engine
Pattern	Pattern Engine
Useful God	Useful God Engine
Ten Gods	Ten Gods Engine
ShenSha	ShenSha Engine
Luck	Luck Engine
Evidence Context	Narrative V2
Reasoning Context	Narrative V2
Customer Wording	Narrative V2
Commercial Rewrite	Narrative V2
Dashboard Rendering	Customer Portal
PDF Rendering	Report Engine
DOCX Rendering	Report Engine


14. Canonical Rules
Rule 1
Narrative never overwrites engine truth.
Rule 2
UI never creates narrative.
Rule 3
PDF never creates narrative.
Rule 4
DOCX never creates narrative.
Rule 5
All customer text must pass Narrative Validator.
Rule 6
All commercial meanings must have approved source or approved deterministic rewrite rule.
Rule 7
No raw JSON/debug content may enter Presentation Contract.
Rule 8
No internal IDs may enter customer-facing content.
Rule 9
No unsupported astrology conclusion may be introduced.
Rule 10
No unsupported action may be generated.
15. Knowledge Dependency Architecture
Narrative V2 may depend on approved knowledge.
Allowed:
Approved Interpretation Knowledge
Approved Consulting Knowledge
Approved Sentence Library
Approved Template Library
Not allowed:
Draft knowledge
Experimental notes
Legacy undocumented mappings
Frontend dictionaries
Unverified prose
Every knowledge source must have:
status
version
source
domain
semantic scope
16. Traceability Architecture
Narrative V2 phải giữ internal traceability.
Mỗi Narrative block cần có thể truy ngược:
Narrative
↓
Knowledge
↓
Reasoning
↓
Evidence
↓
Canonical Analysis
Traceability không render cho khách hàng.
Nhưng phải có trong internal result/debug object.
17. Deduplication Architecture
Narrative V2 phải loại bỏ nội dung trùng.
Ví dụ:
Overview nói:
Bạn có nội lực tốt.
Interpretation không nên lặp nguyên câu đó.
Thay vào đó Interpretation phải mở rộng:
Nội lực này khiến bạn thường chủ động gánh trách nhiệm...
Deduplication phải hoạt động ở semantic level khi có thể.
18. Progressive Disclosure Architecture
Narrative được chia theo tầng.
Overview
↓
Interpretation
↓
Action Plan
↓
Full Report
Mỗi tầng có độ sâu khác nhau.
Không được đưa nội dung Full Report lên Overview.
19. Error Handling
Narrative V2 phải fail safely.
19.1 Missing evidence
Nếu evidence bắt buộc thiếu:
status = insufficient
Không đoán.
19.2 Missing knowledge
Nếu không có approved knowledge:
bỏ block hoặc dùng approved neutral fallback.
Không tự viết knowledge.
19.3 Unsafe content
Nếu content chứa:
- JSON
- rule id
- debug
- technical dump
Validator loại bỏ.
19.4 Partial Narrative
Narrative có thể:
status = partial
nếu một số block unavailable.
Không cần fail toàn bộ nếu phần còn lại hợp lệ.
20. Narrative Status Model
Recommended status:
complete
partial
insufficient
invalid
complete
Tất cả required blocks hợp lệ.
partial
Một số optional blocks thiếu.
insufficient
Không đủ evidence/knowledge.
invalid
Vi phạm validation.
21. Extension Strategy
Narrative V2 phải mở rộng được cho:
- Career
- Finance
- Relationship
- Health
- Education
- Leadership
- Business
- Luck Periods
nhưng V1 scope phải giữ đúng sản phẩm hiện tại.
Mỗi domain mới phải:
1. có knowledge contract,
2. có builder contract,
3. có validator,
4. có tests.
22. Commercial Domain Architecture
Commercial domain narratives phải được tách khỏi overall interpretation.
Ví dụ:
Overall Interpretation

≠

Career Consulting
Commercial domains có thể:
career
finance
relationship
health
leadership
Nhưng không được tự động chèn tất cả vào Overview.
23. Style Architecture
Narrative V2 phải sử dụng chung:
Sentence Library
Template Library
Style Guide
Không Builder nào được tự định nghĩa style riêng.
24. Sentence Architecture
Một sentence chuẩn nên có dạng:
Subject
+
Meaning
+
Context
Ví dụ:
Bạn có xu hướng làm việc theo hệ thống,
đặc biệt hiệu quả khi nhiệm vụ và trách nhiệm được xác định rõ.
Không phải:
Chính Ấn vượng.
25. Recommendation Architecture
Recommendation phải có cấu trúc:
Action
+
Reason
+
Boundary
Ví dụ:
Nên phát triển dựa trên nền tảng hiện tại,
vì cấu trúc lá số phù hợp với sự tích lũy ổn định;
tránh thay đổi toàn bộ hướng đi trong cùng một thời điểm.
26. Validation Flow
Validation sequence:
Schema Validation
        ↓
Source Validation
        ↓
Semantic Validation
        ↓
Safety Validation
        ↓
Style Validation
        ↓
Duplicate Validation
        ↓
Presentation Validation
27. Testing Strategy
Narrative V2 phải có ít nhất:
- unit tests,
- contract tests,
- golden narrative tests,
- semantic safety tests,
- duplicate tests,
- cross-output parity tests.
27.1 Golden Cases
CASE-0001 phải là Golden Narrative đầu tiên.
Sau đó mở rộng:
CASE-0002
CASE-0003
...
Mỗi Golden Case phải kiểm tra:
- Overview,
- Interpretation,
- Action Plan,
- Customer language,
- Traceability.
28. Cross-Output Parity
Một NarrativeV2Result phải tạo cùng nội dung cốt lõi trên:
Dashboard
PDF
DOCX
API
Không được:
Dashboard A
PDF B
DOCX C
29. Performance Principles
Narrative V2 không nên:
- gọi network,
- gọi external LLM,
- scan toàn knowledge base runtime không kiểm soát.
Knowledge phải:
- index được,
- cache được,
- deterministic.
30. Determinism
Same:
Canonical Analysis
+
Narrative Version
+
Knowledge Version
must produce:
Same Narrative Result
Đây là yêu cầu quan trọng để:
- test,
- audit,
- PDF parity,
- customer support.
31. Versioning
Narrative phải có version riêng.
Ví dụ:
bte.narrative.v2
Knowledge cũng phải có version.
Narrative Result phải record:
narrative_version
knowledge_version
presentation_version
Internal only where appropriate.
32. Backward Compatibility
Narrative V2 không được phá:
Pack 05
Integrated Narrative
Commercial Consulting
ngay ở bước đầu.
Migration phải:
V2 first
↓
Legacy fallback
cho tới khi V2 được freeze.
Sau freeze mới loại legacy nếu Product Owner phê duyệt.
33. Migration Architecture
Migration recommended:
Phase 1
Narrative V2 shadow output

Phase 2
CASE-0001 comparison

Phase 3
Golden Dataset

Phase 4
Dashboard reads V2

Phase 5
PDF/DOCX read V2

Phase 6
Legacy retirement
Không chuyển tất cả cùng lúc.
34. Security and Privacy
Narrative V2 không được:
- log dữ liệu cá nhân không cần thiết,
- expose full internal trace to customer,
- expose debug metadata,
- expose knowledge ids.
Customer output chỉ chứa nội dung cần thiết.
35. Architecture Boundaries
Narrative V2 được phép đọc:
Canonical Analysis
Approved Knowledge
Commercial Consulting
Narrative V2 không được sửa:
Astrology Engines
Calendar
ResultStore Truth
Canonical Analysis
36. Non-Goals
Narrative V2 không nhằm:
- thay thế chuyên gia,
- dự đoán tuyệt đối,
- sinh nội dung tự do,
- trở thành chat engine,
- tạo astrology rules mới.
Narrative V2 là:
Deterministic Customer Communication Layer
37. Acceptance Criteria
Architecture được coi là đạt khi:
- Engine truth và narrative được tách biệt.
- UI không còn compose.
- Overview có source riêng.
- Interpretation có source riêng.
- Action Plan có source riêng.
- Commercial Rewrite là layer riêng.
- Customer text traceable.
- Narrative deterministic.
- Dashboard/PDF/DOCX dùng chung Narrative.
- Không raw Engine language ra customer.
- Không frontend astrology reasoning.
38. Architecture Freeze Rules
Sau khi 00_ARCHITECTURE.md được Product Owner freeze:
Không được thay đổi các nguyên tắc sau nếu chưa mở architecture revision:
Engine owns truth
Narrative owns customer language
UI is presentation-only
Commercial Rewrite is mandatory
One Narrative → many outputs
Evidence → Reasoning → Meaning → Action
Mọi thay đổi lớn phải mở:
NARRATIVE V2 ARCHITECTURE REVISION
Không sửa âm thầm.
39. Canonical Architecture Summary
Narrative V2 được tóm tắt bằng pipeline sau:
ASTROLOGY ENGINES
        ↓
CANONICAL ANALYSIS
        ↓
EVIDENCE BUILDER
        ↓
REASONING BUILDER
        ↓
KNOWLEDGE RESOLVER
        ↓
COMMERCIAL REWRITE
        ↓
SUMMARY BUILDER
        ↓
INTERPRETATION BUILDER
        ↓
ACTION BUILDER
        ↓
NARRATIVE VALIDATOR
        ↓
NARRATIVE V2 RESULT
        ↓
DASHBOARD / PDF / DOCX / API
40. Final Architecture Principle
Narrative V2 không được đánh giá dựa trên việc nó sử dụng bao nhiêu thuật ngữ Bát Tự.
Narrative V2 được đánh giá dựa trên việc nó giúp khách hàng hiểu được bao nhiêu.
Nguyên tắc cuối cùng:
Engine chịu trách nhiệm nói sự thật.
Narrative chịu trách nhiệm làm cho sự thật đó trở nên dễ hiểu.
UI chịu trách nhiệm trình bày nó rõ ràng.

Và toàn bộ kiến trúc Narrative V2 phải tuân theo triết lý cao nhất:
Narrative không tồn tại để chứng minh hệ thống thông minh.
Narrative tồn tại để giúp khách hàng hiểu rõ hơn về chính mình.


Tôi đề nghị **chốt file này trước rồi mới sang `01_DATA_MODEL.md`**, vì `01_DATA_MODEL` phải bám hoàn toàn theo architecture này: đặc biệt là các object `EvidenceContext → ReasoningContext → Rewrite → Overview → Interpretation → ActionPlan → NarrativeV2Result`. Nếu Data Model được làm đúng ngay từ đầu, các Builder phía sau sẽ rất sạch và không lặp lại tình trạng mỗi module tự tạo contract riêng.