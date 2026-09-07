# TV-01 — TƯ VẤN HÔN NHÂN
## 02_RUNTIME_PIPELINE.md

**Document ID:** TV-01-02  
**Module:** TV-01_MARRIAGE  
**Product:** BTE Platform  
**Document Type:** Runtime Pipeline Specification  
**Status:** DRAFT FOR PRODUCT OWNER REVIEW  
**Version:** 1.0  
**Language:** Vietnamese  
**Directory:** `knowledge/consulting/TV-01_MARRIAGE/`

---

# 1. Mục đích tài liệu

Tài liệu này định nghĩa pipeline runtime canonical cho module:

> **TV-01 — Tư vấn hôn nhân**

Mục tiêu là xác định rõ:

- request đi vào hệ thống theo thứ tự nào;
- dữ liệu của Người A và Người B được xử lý ra sao;
- những Engine nào được gọi;
- thời điểm nào bắt đầu Marriage Consulting Layer;
- Evidence được tạo ở đâu;
- Decision được tổng hợp ở đâu;
- Assessment được chiếu ở đâu;
- Score được tính ở đâu;
- Narrative được tạo ở đâu;
- lỗi và missing data được xử lý ở đâu;
- kết quả nào là canonical;
- kết quả nào chỉ là presentation.

Runtime phải tuân thủ các contract đã chốt tại:

- `00_SCOPE_AND_PRODUCT_REQUIREMENTS.md`
- `01_DATA_MODEL.md`

---

# 2. Runtime principle

TV-01 sử dụng nguyên tắc:

```text
Birth Input
    ↓
Canonical BTE Analysis
    ↓
Marriage Evidence
    ↓
Marriage Decision
          /                \
Marriage Assessment    Recommendation
          \                /
                 Narrative
                    ↓
               Presentation
```

Không cho phép:

```text
Birth Input
    ↓
Marriage Narrative
```

hoặc:

```text
Birth Input
    ↓
Compatibility Score
```

mà không qua canonical analysis và evidence.

---

# 3. Runtime boundary

TV-01 bắt đầu tại điểm:

```text
Canonical Analysis A
+
Canonical Analysis B
```

TV-01 không sở hữu:

- Calendar calculation;
- Four Pillars calculation;
- Strength;
- Pattern;
- Useful God;
- Ten Gods;
- Luck;
- Shen Sha;
- Feng Shui canonical calculation.

TV-01 chỉ orchestration các engine hiện có và sau đó tạo relationship analysis.

---

# 4. High-level pipeline

```text
MarriageConsultationRequest
          │
          ▼
[01] Request Validation
          │
          ▼
[02] Birth Input Normalization
          │
          ├───────────────┐
          ▼               ▼
[03A] Analyze A      [03B] Analyze B
          │               │
          ▼               ▼
Canonical A         Canonical B
          │               │
          └───────┬───────┘
                  ▼
[04] Canonical Contract Validation
                  │
                  ▼
[05] Snapshot Builder
                  │
                  ▼
[06] Relationship Context Builder
                  │
                  ▼
[07] Evidence Builder
                  │
                  ▼
[08] Evidence Validation
                  │
                  ▼
[09] Domain Decision Engine
                  │
                  ▼
[10] Cross-Domain Resolver
                  │
                  ▼
[11] Overall Decision
                  │
                  ▼
[12] Score Engine
                  │
                  ▼
[13] Confidence Engine
                  │
        /                    \
[14A] Assessment Projector   [14] Recommendation Builder
        \                    /
                  │
                  ▼
[15] Timing Analysis
                  │
                  ▼
[16] Decision Validation
                  │
                  ▼
[17] Narrative Composer
                  │
                  ▼
[18] Presentation Adapter
                  │
                  ▼
[19] Persistence / History
                  │
                  ▼
Marriage Consultation Result
```

---

# 5. Stage 01 — Request Validation

Input:

```ts
MarriageConsultationRequest
```

Phải kiểm tra tối thiểu:

- có Person A;
- có Person B;
- gender hợp lệ;
- birth date hợp lệ;
- birth time nếu có thì đúng format;
- birth place nếu có thì đúng schema;
- A và B không bị thiếu toàn bộ identity;
- options hợp lệ.

Request invalid:

> STOP pipeline.

Không được cố chạy tiếp bằng dữ liệu mặc định.

---

# 6. Không auto-default gender

Không được:

```text
missing gender
→ male
```

hoặc:

```text
invalid gender
→ female
```

Gender phải tuân thủ canonical contract.

Nếu thiếu:

```text
VALIDATION_ERROR
```

---

# 7. Không auto-default birth time

Nếu birth time không có:

```text
birth_time = null
```

Pipeline vẫn có thể chạy partial analysis nếu Core Engine hỗ trợ.

Không được tự gán:

```text
12:00
00:00
```

hoặc giờ bất kỳ.

---

# 8. Stage 02 — Birth Input Normalization

Normalization chỉ làm:

- chuẩn hóa format ngày;
- chuẩn hóa format giờ;
- chuẩn hóa timezone;
- chuẩn hóa birth place;
- mapping UI gender → canonical gender;
- trim customer display text.

Không được:

- tính Bát Tự;
- đổi ngày âm;
- suy luận Can Chi;
- tính Strength;
- tính Useful God.

Đó là trách nhiệm của Core Engine.

---

# 9. Normalized request

Output của Stage 02:

```ts
NormalizedMarriageRequest
```

Conceptually:

```ts
interface NormalizedMarriageRequest {
  person_a: CanonicalBirthInput;
  person_b: CanonicalBirthInput;
  options: ResolvedMarriageOptions;
}
```

---

# 10. Stage 03A / 03B — Canonical Analysis

Hai người phải được phân tích độc lập.

```text
Person A
  ↓
Canonical BTE Pipeline
```

và:

```text
Person B
  ↓
Canonical BTE Pipeline
```

Không được ghép hai người vào cùng một BaZi Engine request.

---

# 11. Canonical BTE pipeline

TV-01 phải reuse runtime hiện hành của BTE.

Conceptually:

```text
Calendar
   ↓
BaZi
   ↓
Strength
   ↓
Temperature
   ↓
Pattern
   ↓
Useful God
   ↓
Ten Gods
   ↓
Luck
   ↓
Shen Sha
   ↓
Other canonical analysis
```

Tên stage thực tế phải bind với runtime thật.

Không duplicate implementation chỉ vì TV-01 cần dữ liệu.

---

# 12. Parallel execution

Nếu kiến trúc runtime cho phép:

```text
Analyze A
Analyze B
```

có thể chạy song song.

Ví dụ:

```text
Promise.all
```

hoặc async equivalent.

Điều kiện:

- không làm thay đổi determinism;
- không chia sẻ mutable state;
- không làm lẫn analysis ID;
- không để result A overwrite result B.

---

# 13. Stage 03 output

Output:

```text
CanonicalAnalysisA
CanonicalAnalysisB
```

Mỗi result phải có:

```text
analysis_id
canonical version
```

nếu runtime hiện tại hỗ trợ.

---

# 14. Failure policy tại canonical stage

Nếu Person A fail:

```text
A analysis failed
```

thì Marriage pipeline phải fail.

Nếu Person B fail:

```text
B analysis failed
```

thì Marriage pipeline phải fail.

Không được tạo Marriage result với một bên thiếu toàn bộ canonical analysis.

---

# 15. Partial canonical result

Trường hợp giờ sinh thiếu nhưng Core Engine vẫn trả partial result:

pipeline có thể tiếp tục.

Phải truyền xuống:

```text
availability
limitations
confidence
```

Không coi partial result là full-quality result.

---

# 16. Stage 04 — Canonical Contract Validation

Trước khi TV-01 đọc dữ liệu, phải xác nhận contract đầu ra hợp lệ.

Kiểm tra tối thiểu:

- analysis ID;
- pillars;
- day master;
- five elements;
- strength;
- useful god nếu required;
- ten gods nếu required;
- luck nếu include_luck = true;
- version metadata nếu available.

---

# 17. Contract mismatch

Nếu runtime BTE thay contract:

```text
useful_god.useful
```

thành format khác mà adapter chưa cập nhật:

TV-01 phải:

```text
CONTRACT_ERROR
```

Không được silent fallback sang path cũ hoặc tạo dữ liệu giả.

---

# 18. Stage 05 — Snapshot Builder

Input:

```text
Canonical A
Canonical B
```

Output:

```text
MarriageCanonicalSnapshot A
MarriageCanonicalSnapshot B
```

Snapshot Builder chỉ:

- select;
- normalize;
- reference;
- bind.

Không tạo interpretation mới.

---

# 19. Snapshot requirement

Snapshot phải preserve:

```text
source_analysis_id
```

và các version cần thiết.

Ví dụ:

```text
MarriageCanonicalSnapshot
  └── source_analysis_id
```

Đây là điểm truy nguồn bắt buộc.

---

# 20. Stage 06 — Relationship Context Builder

Sau khi có hai snapshot:

```text
Snapshot A
+
Snapshot B
```

tạo:

```ts
MarriageRelationshipContext
```

Conceptually:

```ts
interface MarriageRelationshipContext {
  person_a: MarriageCanonicalSnapshot;
  person_b: MarriageCanonicalSnapshot;

  options: ResolvedMarriageOptions;

  available_domains: MarriageDomain[];

  limitations: string[];

  runtime_meta: RuntimeMeta;
}
```

---

# 21. Relationship Context không phải Evidence

Context chỉ tập hợp dữ liệu cần thiết.

Không được tạo conclusion ở đây.

Ví dụ:

Context có thể chứa:

```text
A useful god = fire
B fire distribution = ...
```

nhưng chưa được kết luận:

```text
B supports A
```

cho tới Evidence Builder.

---

# 22. Stage 07 — Evidence Builder

Đây là stage bắt đầu logic chuyên biệt của TV-01.

Input:

```text
MarriageRelationshipContext
```

Output:

```text
MarriageEvidence[]
```

Evidence Builder phải chạy theo rule catalog đã version hóa.

---

# 23. Evidence Builder responsibilities

Có thể tạo evidence cho:

- Five Elements;
- Useful God;
- Pattern interaction;
- Stem interaction;
- Branch interaction;
- Ten Gods interaction;
- Role complement;
- Finance tendency;
- Family dynamics;
- Luck alignment;
- Shen Sha support;
- Feng Shui reference.

Không phải tất cả evidence đều phải tạo trong V1 đầu tiên.

---

# 24. Evidence Builder không tính final score

Evidence Builder chỉ tạo:

```text
evidence
```

Không được:

```text
evidence
→ compatibility score
```

ngay trong cùng stage.

---

# 25. Evidence directionality

Phải bảo toàn:

```text
A_TO_B
B_TO_A
MUTUAL
SHARED
```

Ví dụ:

```text
B supports useful god of A
```

không được tự đổi thành:

```text
mutual support
```

---

# 26. Stage 08 — Evidence Validation

Mỗi evidence phải được validate.

Kiểm tra:

- evidence_id tồn tại;
- domain hợp lệ;
- evidence_type hợp lệ;
- source refs hợp lệ;
- source analysis tồn tại;
- source path tồn tại;
- confidence hợp lệ;
- significance hợp lệ;
- subject hợp lệ;
- rule_id hợp lệ nếu có.

---

# 27. Invalid evidence policy

Nếu evidence không trace được:

```text
DROP?
```

Không được silent drop.

Phải theo policy rõ ràng:

```text
critical evidence invalid
→ fail stage
```

```text
optional secondary evidence invalid
→ mark limitation + continue
```

Policy cụ thể sẽ chốt ở Validation document.

---

# 28. Stage 09 — Domain Decision Engine

Evidence được chia theo domain:

```text
five_elements
stem_branch
ten_gods
interaction
finance
family
children
luck
```

Mỗi domain chạy:

```text
Evidence
   ↓
Rule Resolution
   ↓
Finding
   ↓
Domain Decision
```

---

# 29. Domain isolation

Mỗi domain phải có khả năng test độc lập.

Ví dụ:

```text
Five Elements Decision
```

không cần Narrative.

```text
Finance Decision
```

không cần UI.

Điều này giúp test chính xác từng lớp.

---

# 30. Domain availability

Trước khi chạy một domain:

```text
check required data
```

Nếu không đủ dữ liệu:

```text
availability = false
score = null
grade = null
```

Không tự gán:

```text
score = 50
```

---

# 31. Domain finding generation

Stage này tạo:

```text
MarriageFinding[]
```

Finding phải từ evidence.

Contract:

> No evidence → no finding.

---

# 32. Conflict resolution trong domain

Có thể xuất hiện:

```text
positive evidence
+
negative evidence
```

Decision Engine phải resolve bằng:

- significance;
- strength;
- dependency;
- rescue;
- damage;
- confidence;
- context.

Không dùng số lượng evidence để quyết định.

---

# 33. Stage 10 — Cross-Domain Resolver

Sau khi có domain decisions:

```text
Five Elements
Stem/Branch
Ten Gods
Interaction
Finance
Family
Children
Luck
```

hệ thống phải xem xét quan hệ chéo.

Ví dụ:

```text
Ten Gods pressure
+
Luck activation
→ Family risk amplified
```

hoặc:

```text
Branch clash
+
Strong support evidence
→ negative effect reduced
```

---

# 34. Cross-domain resolver không được phá factual truth

Resolver có thể:

- amplify;
- reduce;
- condition;
- prioritize.

Không được sửa source evidence.

Evidence immutable sau Stage 08.

---

# 35. Stage 11 — Overall Decision

Input:

```text
Domain Decisions
Cross-domain relationships
```

Output:

```text
MarriageOverallDecision
```

Overall Decision xác định:

- headline findings;
- top strengths;
- top risks;
- top conditions;
- domain score inputs;
- overall decision state.

---

# 36. Overall Decision chưa phải customer text

Ví dụ factual result:

```text
headline_finding_ids = [...]
risk_finding_ids = [...]
```

Chưa được tạo:

> Hai bạn rất hợp nhau.

Customer prose chỉ xuất hiện tại Narrative stage.

---

# 37. Stage 12 — Score Engine

Score Engine nhận:

```text
Marriage Decision Profile
+
Domain Decisions
+
Cross-domain state
```

và tạo:

```text
domain scores
overall score
grade
```

Chi tiết trọng số chưa định nghĩa trong file này.

Sẽ được chốt tại:

`03_DECISION_PROFILE.md`

và:

`04_SCORE_ENGINE.md`

---

# 38. Score Engine invariant

Không được:

```text
Lục hợp +10
Xung -10
Nạp âm +5
```

rồi cộng trực tiếp.

Score phải dựa trên Decision state.

---

# 39. Score clamp

Final score phải thuộc:

```text
0 <= score <= 100
```

Nếu calculation vượt range:

```text
runtime error or controlled clamp
```

Cách cuối cùng sẽ được định nghĩa tại Score Engine document.

---

# 40. Stage 13 — Confidence Engine

Confidence được tính độc lập với compatibility score.

Input có thể gồm:

- birth data quality;
- engine coverage;
- evidence confidence;
- evidence conflict;
- missing hour;
- missing domains.

Output:

```text
MarriageConfidenceResult
```

---

# 41. Confidence invariant

Không được:

```text
high compatibility = high confidence
```

Hai khái niệm độc lập.

---

# 42. Missing hour impact

Nếu một hoặc hai người thiếu giờ sinh:

Confidence Engine phải biết.

Ví dụ:

```text
hour-dependent evidence unavailable
```

Các domain bị ảnh hưởng phải giảm confidence tương ứng.

Không nhất thiết giảm toàn bộ score.

---

# 42A. Stage 14A — Assessment Projector

Input:

```text
MarriageDecisionResult
```

Output:

```text
MarriageAssessment
```

Contract:

Question-driven projection của Decision.

Không đọc Recommendation.

Không tạo Recommendation.

Song song với Stage 14.

Cả hai chỉ consume Decision.

Phải trả lời đúng sáu câu:

Q1 Overall Compatibility

Q2 Mutual Support

Q3 Personality Balance

Q4 Marriage Stability

Q5 Children

Q6 Overall Marriage Assessment

Public contract là Assessment.

Decision Result không công bố mặc định.

Chi tiết:

`03A_ASSESSMENT_PROFILE.md`

---

# 43. Stage 14 — Recommendation Builder

Input:

```text
MarriageDecisionResult
Findings
Overall Decision
Timing
```

Output:

```text
MarriageRecommendation[]
```

Contract:

> No finding → no recommendation.

---

# 44. Recommendation generation

Recommendation Builder chỉ được tạo action từ:

```text
source_decision_id
source_finding_ids
```

Không được đọc MarriageAssessment.

Không được chứa compatibility conclusions.

---

# 45. Stage 15 — Timing Analysis

Nếu:

```text
include_luck = true
```

thì chạy Timing Analysis.

Input:

```text
Luck A
Luck B
Marriage Context
Marriage Findings
```

Output:

```text
MarriageTimingResult
```

---

# 46. Timing analysis V1

V1 ưu tiên:

```text
Đại vận A
+
Đại vận B
+
Lưu niên trong window nếu cần
```

Không cần scan toàn bộ cuộc đời mặc định.

Window lấy từ:

```text
MarriageConsultationOptions
```

---

# 47. Timing result

Mỗi period có thể được phân loại:

```text
supportive
stable
mixed
sensitive
```

Không sử dụng wording cực đoan trong factual enum.

---

# 48. Timing does not rewrite natal result

Natal compatibility:

```text
immutable
```

Timing chỉ là:

```text
activation layer
```

Ví dụ:

```text
Natal = tương hợp tốt
2029 = sensitive period
```

không có nghĩa:

```text
Natal compatibility changed
```

---

# 49. Stage 16 — Decision Validation

Trước khi Narrative chạy, toàn bộ factual result phải validate.

Kiểm tra:

- no orphan evidence;
- no orphan finding;
- no orphan recommendation;
- score range;
- confidence range;
- valid grade;
- valid domain availability;
- version bundle;
- source references;
- timing references;
- deterministic metadata.

---

# 50. Narrative không được chạy trên invalid Decision Result

Nếu Stage 16 fail:

> STOP.

Không được cố tạo customer report từ factual result lỗi.

---

# 51. Stage 17 — Narrative Composer

Input:

```text
MarriageAssessment
MarriageDecisionResult
```

Output:

```text
MarriageNarrativeResult
```

Narrative Composer được phép:

- chọn wording;
- chọn câu nối;
- nhóm findings;
- tránh lặp;
- điều chỉnh độ dài;
- tạo customer-friendly explanation.

---

# 52. Narrative Composer không được

Không được:

- tự tính lại Bát Tự;
- tự tạo evidence;
- tự tạo finding;
- thay score;
- thay grade;
- thay confidence;
- thêm risk không tồn tại;
- bỏ critical finding vì “không đẹp”.

---

# 53. Narrative binding rule

Narrative phải bind từ:

```text
finding_id
recommendation_id
domain
priority
confidence
```

Nếu không có finding ID:

> Không được sinh kết luận mới.

---

# 54. Stage 18 — Presentation Adapter

Input:

```text
Decision Result
+
Narrative Result
```

Output:

```text
MarriagePresentationResult
```

Adapter chịu trách nhiệm:

- format score;
- map enum;
- map gender;
- map element;
- layout model;
- customer labels;
- summary cards;
- mobile/desktop data shape nếu cần.

---

# 55. Presentation Adapter không sửa logic

Không được:

```text
grade B
→ display A
```

hoặc:

```text
score 72
→ display 80
```

vì lý do UI.

---

# 56. Stage 19 — Persistence

Sau khi factual result hợp lệ:

```text
MarriageDecisionResult
```

phải có thể lưu.

Persistence tối thiểu:

```text
consultation_id
person_a_analysis_id
person_b_analysis_id
score
grade
confidence
versions
created_at
```

Full payload tùy storage architecture.

---

# 57. Persistence ordering

Khuyến nghị:

```text
Decision Result validated
        ↓
Persist canonical result
        ↓
Persist presentation cache optional
```

Không để:

```text
UI rendering failure
```

làm mất canonical result nếu factual analysis đã hoàn thành.

---

# 58. consultation_id creation

`consultation_id` phải được tạo trước khi final persistence.

Có thể tạo tại:

```text
request orchestration
```

hoặc:

```text
decision initialization
```

nhưng phải stable trong toàn request.

---

# 59. Idempotency

Nếu runtime hỗ trợ idempotency key:

cùng request retry không nên tạo duplicate consultation không cần thiết.

Chi tiết sẽ nằm ở API document.

---

# 60. Runtime orchestration object

Khuyến nghị có một orchestrator riêng:

```text
MarriageConsultationOrchestrator
```

Trách nhiệm:

- validate request;
- call BTE analysis A/B;
- build snapshots;
- run evidence;
- run decision;
- run score;
- run narrative;
- persist;
- return result.

---

# 61. Orchestrator không chứa business rules chi tiết

Không được viết:

```text
if branch clash then -10
```

trực tiếp trong Orchestrator.

Business rules phải nằm ở:

```text
Decision Profile
Rule Catalog
Score Engine
```

---

# 62. Recommended runtime components

Conceptually:

```text
MarriageConsultationOrchestrator
MarriageRequestValidator
MarriageSnapshotBuilder
MarriageContextBuilder
MarriageEvidenceBuilder
MarriageEvidenceValidator
MarriageDomainDecisionEngine
MarriageCrossDomainResolver
MarriageOverallDecisionEngine
MarriageScoreEngine
MarriageConfidenceEngine
MarriageRecommendationBuilder
MarriageTimingEngine
MarriageDecisionValidator
MarriageNarrativeComposer
MarriagePresentationAdapter
MarriageRepository
```

Tên implementation có thể khác nhưng trách nhiệm phải rõ.

---

# 63. Dependency direction

Đúng:

```text
Orchestrator
   ↓
Components
   ↓
Core BTE contracts
```

Không đúng:

```text
Core BaZi Engine
   ↓
TV-01 Marriage
```

Core Engine không được phụ thuộc module tư vấn.

---

# 64. Runtime dependency graph

```text
BTE Core
   ↑
   │
Marriage Snapshot
   ↑
   │
Evidence
   ↑
   │
Decision
   ↑
   │
Score / Confidence
   ↑
   │
Narrative
   ↑
   │
Presentation
```

Dependency chỉ đi theo một hướng.

---

# 65. Runtime state

Không sử dụng mutable global state.

Mỗi consultation phải có:

```ts
MarriageRuntimeContext
```

riêng.

---

# 66. MarriageRuntimeContext

Conceptually:

```ts
interface MarriageRuntimeContext {
  consultation_id: string;

  request: NormalizedMarriageRequest;

  analysis_a?: CanonicalAnalysis;
  analysis_b?: CanonicalAnalysis;

  snapshot_a?: MarriageCanonicalSnapshot;
  snapshot_b?: MarriageCanonicalSnapshot;

  evidence?: MarriageEvidence[];

  domain_results?: MarriageDomainResults;

  overall?: MarriageOverallDecision;

  timing?: MarriageTimingResult;

  recommendations?: MarriageRecommendation[];

  confidence?: MarriageConfidenceResult;

  versions: MarriageVersionBundle;

  warnings: RuntimeWarning[];

  timings?: StageTiming[];
}
```

---

# 67. Runtime context không phải API contract

RuntimeContext là orchestration/internal object.

Không expose trực tiếp cho customer API.

---

# 68. Stage timing

Nên hỗ trợ đo:

```text
validation_ms
analysis_a_ms
analysis_b_ms
evidence_ms
decision_ms
score_ms
narrative_ms
total_ms
```

để debug performance.

Không cần hiển thị cho customer.

---

# 69. Logging

Log phải có:

```text
consultation_id
stage
status
duration
error_code
```

Không log dữ liệu nhạy cảm không cần thiết.

---

# 70. Traceability

Mỗi runtime execution nên trace được:

```text
consultation_id
  ↓
analysis_id A
analysis_id B
  ↓
evidence IDs
  ↓
finding IDs
  ↓
recommendation IDs
```

---

# 71. Error classes

Runtime nên phân loại lỗi:

```text
VALIDATION_ERROR
CANONICAL_ANALYSIS_ERROR
CANONICAL_CONTRACT_ERROR
EVIDENCE_ERROR
DECISION_ERROR
SCORE_ERROR
CONFIDENCE_ERROR
NARRATIVE_ERROR
PERSISTENCE_ERROR
INTERNAL_ERROR
```

---

# 72. Error handling principle

Không biến mọi lỗi thành:

```text
500 Internal Server Error
```

API layer sau này phải có error mapping phù hợp.

---

# 73. Warning vs Error

Ví dụ:

Thiếu giờ sinh:

```text
warning / limitation
```

không nhất thiết là fatal error.

Canonical contract thiếu field required:

```text
error
```

---

# 74. Optional subsystem failure

Ví dụ Shen Sha optional fail:

nếu TV-01 profile cho phép:

```text
warning
continue
```

và:

```text
confidence adjusted
```

Không được giả lập Shen Sha result.

---

# 75. Required subsystem failure

Ví dụ:

```text
BaZi A missing
```

hoặc:

```text
Useful God required but canonical result malformed
```

nếu profile yêu cầu:

```text
STOP
```

---

# 76. Retry policy

Không retry business-rule failures.

Có thể retry:

- transient persistence failure;
- transient network/service failure nếu kiến trúc distributed.

Không retry:

```text
invalid birth date
invalid canonical contract
```

---

# 77. Determinism

Cùng:

```text
Normalized Request
Canonical A
Canonical B
Rule Catalog Version
Decision Profile Version
Score Model Version
```

phải tạo cùng:

```text
Evidence
Findings
Scores
Grade
Recommendations
```

---

# 78. Narrative determinism

Narrative có thể:

- deterministic;
- hoặc controlled variation.

Nhưng factual result không được thay đổi.

Nếu Narrative dùng AI model sau này:

```text
AI = presentation only
```

không phải decision authority.

---

# 79. Cache strategy

Có thể cache:

```text
Canonical Analysis A
Canonical Analysis B
```

nếu analysis IDs/data inputs giống nhau.

Không nên cache Marriage Result chỉ theo birth dates.

Cache key phải bao gồm:

```text
canonical analysis IDs
profile version
score version
rule version
options
```

---

# 80. Cache invalidation

Nếu:

```text
Decision Profile version changes
```

thì old Marriage cache không được reuse như current result.

---

# 81. Version capture point

Version bundle phải resolve trước khi Decision stages bắt đầu.

Ví dụ:

```text
module_version
decision_profile_version
score_model_version
rule_catalog_version
```

Không được thay version giữa một runtime execution.

---

# 82. Atomic version rule

Một consultation phải chạy bằng một version bundle duy nhất.

Không được:

```text
half rules v1
half rules v2
```

trong cùng result.

---

# 83. Security boundary

TV-01 không cần expose raw internal evidence cho customer UI mặc định.

Nhưng evidence phải tồn tại để:

- audit;
- testing;
- expert mode;
- report trace.

---

# 84. Expert mode

Sau này có thể có:

```text
expert=true
```

để hiển thị:

- evidence;
- rule ID;
- confidence;
- source refs.

Không nằm trong UI V1 bắt buộc.

---

# 85. Pipeline mode

Có thể định nghĩa runtime mode:

```text
full
summary
decision_only
```

nhưng V1 chỉ cần `full` nếu muốn giữ đơn giản.

Không tối ưu sớm khi chưa có nhu cầu.

---

# 86. Full runtime sequence

```text
POST Marriage Request
        │
        ▼
Validate Request
        │
        ▼
Normalize
        │
        ├─────────────────────┐
        ▼                     ▼
Run BTE A                 Run BTE B
        │                     │
        ▼                     ▼
Validate A                Validate B
        │                     │
        └──────────┬──────────┘
                   ▼
             Build Snapshots
                   │
                   ▼
         Build Relationship Context
                   │
                   ▼
              Build Evidence
                   │
                   ▼
             Validate Evidence
                   │
                   ▼
             Domain Decisions
                   │
                   ▼
            Cross-Domain Resolve
                   │
                   ▼
             Overall Decision
                   │
                   ▼
                Scoring
                   │
                   ▼
              Confidence
                   │
                   ▼
            Recommendations
                   │
                   ▼
             Timing Analysis
                   │
                   ▼
            Validate Decision
                   │
                   ▼
            Persist Canonical
                   │
                   ▼
             Compose Narrative
                   │
                   ▼
            Presentation Adapter
                   │
                   ▼
              Return Result
```

---

# 87. Persistence trước hay sau Narrative

Khuyến nghị V1:

```text
Decision validated
   ↓
Persist canonical factual result
   ↓
Narrative
   ↓
Presentation
```

Lý do:

Narrative failure không được làm mất factual Marriage Decision.

Nếu cần, Narrative có thể regenerate sau.

---

# 88. Narrative failure policy

Nếu factual result đã thành công nhưng Narrative fail:

có thể trả:

```text
status = PARTIAL
```

và cho phép retry Narrative.

Không được recompute Marriage Decision chỉ vì Narrative lỗi.

---

# 89. Presentation failure policy

Tương tự:

```text
Decision = valid
Narrative = valid
Presentation = fail
```

thì canonical result vẫn phải tồn tại.

---

# 90. Persistence failure policy

Nếu canonical persistence là requirement bắt buộc:

```text
Decision complete
Persistence fail
```

API có thể trả controlled error.

Nhưng không được recompute silently nhiều lần mà tạo duplicate IDs.

---

# 91. Runtime output states

Khuyến nghị:

```ts
type MarriageRuntimeStatus =
  | "SUCCESS"
  | "PARTIAL"
  | "FAILED";
```

---

# 92. SUCCESS

```text
Decision valid
Persistence successful
Narrative successful
Presentation successful
```

---

# 93. PARTIAL

Ví dụ:

```text
Decision valid
Persistence successful
Narrative unavailable
```

hoặc optional subsystem unavailable.

Không dùng PARTIAL cho canonical data corruption.

---

# 94. FAILED

Ví dụ:

```text
invalid request
canonical analysis fail
decision validation fail
```

---

# 95. Runtime response envelope

Conceptually:

```ts
interface MarriageRuntimeResponse {
  status: MarriageRuntimeStatus;

  consultation_id?: string;

  result?: MarriageDecisionResult;

  presentation?: MarriagePresentationResult;

  warnings?: RuntimeWarning[];

  error?: RuntimeError;
}
```

Chi tiết public API sẽ chốt tại `06_PUBLIC_API.md`.

---

# 96. RuntimeWarning

```ts
interface RuntimeWarning {
  code: string;

  stage: string;

  message_key?: string;

  technical_detail?: string;
}
```

Customer text không nhất thiết lấy trực tiếp từ `technical_detail`.

---

# 97. RuntimeError

```ts
interface RuntimeError {
  code: string;

  stage: string;

  retryable: boolean;

  technical_detail?: string;
}
```

Không expose stack trace ra customer API.

---

# 98. Testing hooks

Mỗi stage chính nên test được độc lập:

```text
request validation
snapshot
evidence
domain decision
cross-domain
score
confidence
recommendation
timing
narrative
presentation
```

Không chỉ test end-to-end.

---

# 99. Golden pipeline requirement

Golden Case phải có snapshot ít nhất tại:

```text
Canonical A/B
Evidence
Domain Findings
Overall Decision
Score
Confidence
Recommendations
Presentation
```

để phát hiện stage nào regression.

---

# 100. Runtime invariants

Các invariant bắt buộc:

> Canonical A/B phải tồn tại trước Marriage Evidence.

> Evidence phải tồn tại trước Finding.

> Finding phải tồn tại trước Decision.
> Assessment phải tồn tại sau Decision.
> Recommendation phải tồn tại sau Decision.
> Assessment và Recommendation độc lập.
> Recommendation không chứa compatibility conclusions.

> Decision phải được validate trước Narrative.

> Score không được tính trực tiếp từ raw birth input.

> Narrative không được sửa factual result.

> Presentation không được sửa factual result.

---

# 101. Core runtime contract

```text
Birth Data
   ↓
BTE Truth
   ↓
Marriage Evidence
   ↓
Marriage Decision
   ↓
Marriage Presentation
```

Đây là hướng dữ liệu duy nhất được phép.

---

# 102. Không cho phép reverse dependency

Không được để TV-01 ghi ngược vào:

- BaZi result;
- Strength result;
- Pattern result;
- Useful God result;
- Luck result.

Marriage analysis là derived result.

Canonical natal truth phải immutable.

---

# 103. Runtime scalability

Thiết kế phải hỗ trợ sau này:

```text
TV-02 Business Partner
TV-03 Career
TV-04 Child Planning
```

reuse:

```text
Request
Canonical Snapshot
Evidence
Decision
        /        \
Assessment      Recommendation
Score
Confidence
Narrative
Presentation
```

nhưng TV-01 không cần generic hóa implementation ngay.

---

# 104. Recommended folder responsibility

Conceptually:

```text
consulting/
└── marriage/
    ├── orchestrator
    ├── snapshot
    ├── context
    ├── evidence
    ├── decision
    ├── assessment
    ├── scoring
    ├── confidence
    ├── timing
    ├── recommendation
    ├── narrative
    ├── presentation
    └── repository
```

Đây là định hướng trách nhiệm, không bắt buộc tên thư mục implementation.

---

# 105. Implementation guardrail

Cursor / developer không được:

- tạo Marriage Bazi Calculator;
- copy Strength logic;
- copy Useful God logic;
- hard-code score trong Orchestrator;
- tạo customer prose trong Evidence Builder;
- cho Narrative tự suy luận raw pillars;
- dùng UI làm nguồn sự thật;
- bỏ qua versioning.

---

# 106. Runtime acceptance checklist

`02_RUNTIME_PIPELINE.md` chỉ được FREEZE khi Product Owner xác nhận:

- [ ] Request validation rõ ràng.
- [ ] Person A/B chạy canonical BTE riêng.
- [ ] Có canonical contract validation.
- [ ] Có snapshot layer.
- [ ] Có relationship context.
- [ ] Có evidence builder.
- [ ] Có evidence validation.
- [ ] Có domain decision.
- [ ] Có cross-domain resolver.
- [ ] Có overall decision.
- [ ] Có Assessment Projector.
- [ ] Public contract là Question Set / Assessment Answers.
- [ ] Score tách khỏi Evidence Builder.
- [ ] Confidence tách khỏi score.
- [ ] Recommendation dựa trên Decision, không dựa trên Assessment.
- [ ] Assessment và Recommendation độc lập.
- [ ] Timing là activation layer.
- [ ] Decision validation chạy trước Narrative.
- [ ] Narrative không thay factual result.
- [ ] Presentation không thay factual result.
- [ ] Có persistence/history.
- [ ] Có error/warning model.
- [ ] Missing hour không giả lập.
- [ ] Có deterministic runtime.
- [ ] Có version bundle.
- [ ] Core BTE không phụ thuộc TV-01.

---

# 107. Freeze boundary

Sau khi file này FREEZE:

Có thể sang:

`03_DECISION_PROFILE.md`

Nhưng chưa được implementation TV-01 production nếu:

- Decision Profile chưa chốt;
- Score Engine chưa chốt;
- Validation chưa chốt;
- Acceptance chưa chốt.

---

# 108. Core statement

> **TV-01 Runtime không phải là một Bát Tự Engine thứ hai.**

Nó là:

> **một orchestration và decision pipeline dùng hai kết quả Bát Tự canonical để tạo ra kết quả tư vấn hôn nhân có evidence, score, confidence và recommendation.**

---

# 109. Status

**TV-01-02 STATUS: DRAFT**

Bước tiếp theo sau khi Product Owner duyệt:

`TV-01 / 03_DECISION_PROFILE.md`
```

File này chốt được phần xương sống runtime. Điểm quan trọng nhất là **TV-01 chỉ bắt đầu logic riêng sau khi đã có hai canonical analysis hoàn chỉnh**, còn `Narrative` nằm gần cuối pipeline và tuyệt đối không có quyền tạo thêm kết luận kỹ thuật. Như vậy khi sang `03_DECISION_PROFILE.md`, chúng ta mới bắt đầu định nghĩa thực sự **“hai lá số được đem ra so sánh theo tiêu chí nào và tiêu chí nào quan trọng hơn”**.