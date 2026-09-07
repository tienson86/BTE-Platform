# TV-01 — TƯ VẤN HÔN NHÂN
## 01_DATA_MODEL.md

**Document ID:** TV-01-01  
**Module:** TV-01_MARRIAGE  
**Product:** BTE Platform  
**Document Type:** Data Model Specification  
**Status:** DRAFT FOR PRODUCT OWNER REVIEW  
**Version:** 1.0  
**Language:** Vietnamese  
**Directory:** `knowledge/consulting/TV-01_MARRIAGE/`

---

# 1. Mục đích tài liệu

Tài liệu này định nghĩa mô hình dữ liệu canonical cho module:

> **TV-01 — Tư vấn hôn nhân**

Mục tiêu của Data Model là bảo đảm:

- TV-01 không tự tính lại dữ liệu Bát Tự;
- mọi dữ liệu đầu vào đều truy được về canonical analysis của BTE;
- mọi kết luận đều có evidence;
- score, grade, finding và narrative được tách biệt;
- dữ liệu có thể sử dụng đồng nhất cho UI, API, History, PDF và DOCX;
- cùng một input và cùng version phải tạo cùng một factual result;
- hệ thống có khả năng mở rộng sang TV-02, TV-03, TV-04 sau này.

---

# 2. Nguyên tắc thiết kế

TV-01 sử dụng mô hình:

```text
Canonical Person A
       +
Canonical Person B
       ↓
Relationship Evidence
       ↓
Domain Findings
       ↓
Marriage Decision Result
       ↓
Marriage Assessment
       ↓
Narrative / UI / Report

Không cho phép:
Birth Input
   ↓
TV-01 tự tính BaZi riêng
Nguồn sự thật duy nhất:
BTE Canonical Analysis

3. Các tầng dữ liệu
TV-01 chia dữ liệu thành 7 tầng:
L0  Request
L1  Person Reference
L2  Canonical Snapshot
L3  Relationship Evidence
L4  Domain Decision
L5  Overall Decision
L6  Presentation Result
Mỗi tầng có trách nhiệm riêng.
4. L0 — Marriage Consultation Request
Đối tượng request ban đầu:
interface MarriageConsultationRequest {
  person_a: MarriagePersonInput;
  person_b: MarriagePersonInput;

  options?: MarriageConsultationOptions;

  request_meta?: RequestMeta;
}
5. MarriagePersonInput
interface MarriagePersonInput {
  full_name?: string;

  gender: CanonicalGender;

  birth_date: string;

  birth_time?: string | null;

  birth_place?: BirthPlaceInput | null;

  timezone?: string | null;
}
Quy ước:
birth_date = YYYY-MM-DD
birth_time = HH:mm[:ss]
Không sử dụng format hiển thị DD/MM/YYYY trong canonical contract.
UI có thể hiển thị theo chuẩn Việt Nam nhưng adapter phải chuyển về canonical format trước khi gửi request.
6. CanonicalGender
TV-01 phải sử dụng đúng gender contract hiện có của BTE:
type CanonicalGender =
  | "male"
  | "female";
Không tự tạo:
nam
nữ
M
F
1
0
ở tầng canonical.
Các giá trị hiển thị:
male   → Nam
female → Nữ
thuộc Presentation Layer.
7. BirthPlaceInput
interface BirthPlaceInput {
  display_name?: string;

  province?: string;
  city?: string;
  country?: string;

  latitude?: number;
  longitude?: number;
}
TV-01 không tự geocode nếu canonical Birth Input infrastructure của BTE đã có xử lý này.
8. MarriageConsultationOptions
interface MarriageConsultationOptions {
  include_luck?: boolean;

  luck_window?: MarriageLuckWindow;

  include_shen_sha?: boolean;

  include_feng_shui_reference?: boolean;

  narrative_level?: NarrativeLevel;
}
Default V1:
include_luck = true
include_shen_sha = true
include_feng_shui_reference = true
Tuy nhiên các giá trị này chỉ bật/tắt lớp phân tích phụ.
Không được thay đổi canonical natal truth.
9. MarriageLuckWindow
interface MarriageLuckWindow {
  start_year: number;
  end_year: number;
}
Ví dụ:
{
  "start_year": 2026,
  "end_year": 2036
}
Giới hạn window cụ thể sẽ được định nghĩa trong Runtime/Validation specification.
10. L1 — Person Reference
Sau khi mỗi người được chạy qua canonical BTE analysis:
interface MarriagePersonReference {
  person_id?: string;

  analysis_id: string;

  display_name?: string;

  gender: CanonicalGender;

  birth_data_quality: BirthDataQuality;

  canonical_version: CanonicalVersionReference;
}
TV-01 phải lưu analysis_id.
Không được chỉ copy dữ liệu hiển thị mà bỏ mất nguồn analysis.
11. BirthDataQuality
interface BirthDataQuality {
  birth_date_known: boolean;
  birth_time_known: boolean;
  birth_place_known: boolean;

  timezone_resolved: boolean;

  completeness_score: number;

  limitations: string[];
}
completeness_score:
0.0 → 1.0
Không phải compatibility score.
Đây chỉ là chất lượng dữ liệu đầu vào.
12. Trường hợp không biết giờ sinh
Nếu không có giờ sinh:
birth_time_known = false
Không được tạo giờ giả.
Ví dụ không được:
00:00
12:00
23:00
để hoàn thành lá số.
Các field phụ thuộc giờ sinh phải được đánh dấu unavailable.
13. CanonicalVersionReference
interface CanonicalVersionReference {
  calendar_version?: string;
  bazi_version?: string;
  strength_version?: string;
  pattern_version?: string;
  useful_god_version?: string;
  ten_gods_version?: string;
  luck_version?: string;
  shen_sha_version?: string;
}
Mục tiêu:
sau này một kết quả Marriage cũ vẫn xác định được đã dùng Engine version nào.
14. L2 — Canonical Snapshot
TV-01 không cần copy toàn bộ raw canonical result.
Chỉ tạo một snapshot có cấu trúc rõ ràng từ các phần cần thiết.
interface MarriageCanonicalSnapshot {
  person: MarriagePersonReference;

  pillars: PillarSnapshot;

  day_master: DayMasterSnapshot;

  five_elements: FiveElementSnapshot;

  strength: StrengthSnapshot;

  pattern: PatternSnapshot;

  useful_god: UsefulGodSnapshot;

  ten_gods: TenGodSnapshot;

  luck?: LuckSnapshot;

  shen_sha?: ShenShaSnapshot;

  feng_shui?: FengShuiSnapshot;

  source_analysis_id: string;
}
15. PillarSnapshot
interface PillarSnapshot {
  year: PillarValue;
  month: PillarValue;
  day: PillarValue;
  hour?: PillarValue | null;
}
16. PillarValue
interface PillarValue {
  stem: string;
  branch: string;

  can_chi: string;

  hidden_stems?: string[];

  ten_god?: string | null;

  growth_stage?: string | null;

  na_yin?: string | null;
}
TV-01 chỉ đọc các giá trị canonical đã có.
17. DayMasterSnapshot
interface DayMasterSnapshot {
  stem: string;

  element: FiveElement;

  yin_yang: YinYang;
}
18. FiveElement
type FiveElement =
  | "wood"
  | "fire"
  | "earth"
  | "metal"
  | "water";
Presentation mapping:
wood  → Mộc
fire  → Hỏa
earth → Thổ
metal → Kim
water → Thủy
19. YinYang
type YinYang =
  | "yin"
  | "yang";
20. FiveElementSnapshot
interface FiveElementSnapshot {
  distribution: Record<FiveElement, number>;

  normalized?: Record<FiveElement, number>;

  dominant?: FiveElement[];

  weak?: FiveElement[];

  absent?: FiveElement[];
}
Không được tự suy luận:
absent = automatically bad
dominant = automatically bad
TV-01 phải đọc kết hợp với Strength và Useful God.
21. StrengthSnapshot
interface StrengthSnapshot {
  classification: StrengthClass;

  score?: number;

  confidence?: number;

  reasons?: EvidenceReference[];
}
22. StrengthClass
Phải reuse canonical enum hiện có của BTE.
Ví dụ conceptually:
type StrengthClass =
  | "extremely_weak"
  | "weak"
  | "balanced"
  | "strong"
  | "extremely_strong";
Tên enum cuối cùng phải bind theo contract runtime thật của BTE.
TV-01 không được tạo mapping riêng nếu Engine đã có enum khác.
23. PatternSnapshot
interface PatternSnapshot {
  pattern_id?: string;

  pattern_name?: string;

  grade?: string;

  purity?: string;

  status?: string;

  confidence?: number;
}
24. UsefulGodSnapshot
interface UsefulGodSnapshot {
  useful?: ElementOrStemReference[];

  favorable?: ElementOrStemReference[];

  unfavorable?: ElementOrStemReference[];

  temperature_need?: string | null;

  confidence?: number;
}
25. ElementOrStemReference
interface ElementOrStemReference {
  element?: FiveElement;

  stem?: string;

  role?: string;
}
TV-01 phải phân biệt:
Dụng thần
Hỷ thần
Kỵ thần
Không được gom chung thành:
good_elements
bad_elements
26. TenGodSnapshot
interface TenGodSnapshot {
  visible?: TenGodItem[];

  hidden?: TenGodItem[];

  dominant_roles?: string[];

  deficient_roles?: string[];

  structural_findings?: EvidenceReference[];
}
27. TenGodItem
interface TenGodItem {
  name: string;

  source_pillar?: string;

  source_stem?: string;

  visibility?: "visible" | "hidden";

  strength?: number | null;
}
28. LuckSnapshot
interface LuckSnapshot {
  cycles: LuckCycleSnapshot[];

  current_cycle?: LuckCycleSnapshot | null;
}
29. LuckCycleSnapshot
interface LuckCycleSnapshot {
  index: number;

  start_year: number;
  end_year: number;

  can_chi: string;

  stem: string;
  branch: string;

  interpretation_tags?: string[];
}
TV-01 không được tự tính lại Đại vận từ ngày sinh.
30. ShenShaSnapshot
interface ShenShaSnapshot {
  items: ShenShaItem[];
}
31. ShenShaItem
interface ShenShaItem {
  id?: string;

  name: string;

  pillar?: string;

  category?: string;

  polarity?: string;

  confidence?: number;
}
Shen Sha là evidence phụ.
32. FengShuiSnapshot
interface FengShuiSnapshot {
  cung_phi?: string;

  element?: FiveElement;

  group?: string;
}
Ví dụ:
Cung Phi
Hành Cung
Nhóm Trạch
là reference data.
Không phải primary marriage evidence.
33. L3 — Relationship Evidence
Đây là tầng quan trọng nhất của TV-01.
Mọi kết luận phải được xây từ:
interface MarriageEvidence {
  evidence_id: string;

  domain: MarriageDomain;

  evidence_type: MarriageEvidenceType;

  direction: EvidenceDirection;

  significance: EvidenceSignificance;

  confidence: number;

  subject: RelationshipSubject;

  source_refs: EvidenceSourceRef[];

  rule_id?: string;

  description?: string;

  technical_payload?: Record<string, unknown>;
}
34. MarriageDomain
type MarriageDomain =
  | "overall"
  | "five_elements"
  | "stem_branch"
  | "ten_gods"
  | "interaction"
  | "finance"
  | "family"
  | "children"
  | "luck";
Có thể mở rộng nhưng không đổi nghĩa silent trong V1.
35. MarriageEvidenceType
type MarriageEvidenceType =
  | "element_support"
  | "element_conflict"
  | "useful_god_support"
  | "unfavorable_activation"

  | "stem_combination"
  | "stem_control"

  | "branch_combination"
  | "branch_clash"
  | "branch_harm"
  | "branch_punishment"
  | "branch_break"
  | "branch_meeting"

  | "ten_god_support"
  | "ten_god_pressure"
  | "role_complement"
  | "role_conflict"

  | "pattern_support"
  | "pattern_damage"
  | "pattern_rescue"

  | "luck_alignment"
  | "luck_misalignment"

  | "shen_sha_support"
  | "shen_sha_risk"

  | "feng_shui_reference";
Đây là logical taxonomy.
Tên implementation cuối cùng có thể map sang rule catalog sau này.
36. EvidenceDirection
type EvidenceDirection =
  | "positive"
  | "negative"
  | "mixed"
  | "neutral";
Không dùng:
good
bad
vì nhiều evidence phụ thuộc context.
37. EvidenceSignificance
type EvidenceSignificance =
  | "critical"
  | "major"
  | "moderate"
  | "minor";
significance không đồng nghĩa direction.
Ví dụ:
critical + positive
critical + negative
minor + positive
đều hợp lệ.
38. RelationshipSubject
Evidence phải chỉ rõ hướng tác động.
type RelationshipSubject =
  | "A_TO_B"
  | "B_TO_A"
  | "MUTUAL"
  | "SHARED";
Ví dụ:
Người B hỗ trợ Dụng thần của A:
subject = B_TO_A
Không nên ép thành mutual nếu không có bằng chứng ngược lại.
39. EvidenceSourceRef
interface EvidenceSourceRef {
  analysis_id: string;

  person: "A" | "B";

  path: string;

  value?: unknown;
}
Ví dụ:
A.useful_god.useful[0]
B.five_elements.fire
Mục tiêu:
Finding phải truy ngược được tới canonical source.

40. Rule ID
Nếu evidence do Decision Rule tạo:
rule_id = marriage.element.useful_support.v1
Rule ID phải:
- stable;
- versionable;
- human traceable.
Không dùng UUID ngẫu nhiên làm semantic rule identity.
41. Evidence ID
Evidence instance ID có thể theo dạng:
MEV-000001
MEV-000002
hoặc stable hash nếu implementation yêu cầu.
Nhưng phải phân biệt:
rule_id = loại quy tắc
evidence_id = instance kết quả
42. Evidence không đồng nghĩa Finding
Ví dụ:
Evidence 1:
B hỗ trợ Hỷ thần Hỏa của A
Evidence 2:
A và B có một Chi xung ở vị trí quan trọng
Hai evidence này chưa phải customer conclusion.
Decision Engine phải tổng hợp chúng thành Finding.
43. L4 — Domain Decision
Mỗi domain tạo một Decision riêng.
interface MarriageDomainDecision {
  domain: MarriageDomain;

  score?: number;

  grade?: DomainGrade;

  confidence: number;

  findings: MarriageFinding[];

  strengths: string[];

  risks: string[];

  conditions: string[];

  evidence_ids: string[];
}
44. MarriageFinding
interface MarriageFinding {
  finding_id: string;

  domain: MarriageDomain;

  type: FindingType;

  priority: FindingPriority;

  direction: EvidenceDirection;

  confidence: number;

  title_key?: string;

  summary_key?: string;

  evidence_ids: string[];

  recommendation_ids?: string[];

  technical_summary?: string;
}
45. FindingType
type FindingType =
  | "strength"
  | "risk"
  | "bottleneck"
  | "support"
  | "condition"
  | "timing"
  | "mixed";
46. FindingPriority
type FindingPriority =
  | "P0"
  | "P1"
  | "P2"
  | "P3"
  | "P4"
  | "P5";
TV-01 nên reuse Evidence Priority philosophy hiện có của BTE.
Không nhất thiết mọi domain đều có P0.
47. Score của Domain
Mỗi domain có thể có:
0–100
nhưng score phải là output sau Decision Processing.
Không phải tổng trực tiếp của evidence.
Ví dụ không được:
3 positive evidence = +30
2 negative evidence = -20
score = 60
48. DomainGrade
type DomainGrade =
  | "A"
  | "B"
  | "C"
  | "D"
  | "E";
Grade phải map theo score profile đã freeze trong 04_SCORE_ENGINE.md.
Không hard-code trong UI.
49. Các Domain Decision V1
Canonical result dự kiến có:
interface MarriageDomainResults {
  five_elements: MarriageDomainDecision;

  stem_branch: MarriageDomainDecision;

  ten_gods: MarriageDomainDecision;

  interaction: MarriageDomainDecision;

  finance: MarriageDomainDecision;

  family: MarriageDomainDecision;

  children: MarriageDomainDecision;

  luck: MarriageDomainDecision;
}
50. Mối quan hệ giữa các Domain
Không giả định tất cả domain độc lập.
Ví dụ:
five_elements
      ↓
interaction
      ↓
finance
hoặc:
ten_gods
      ↓
family
Do đó Domain Decision có thể reference findings từ domain khác.
51. Cross Domain Reference
interface FindingReference {
  finding_id: string;

  relation:
    | "supports"
    | "amplifies"
    | "reduces"
    | "conflicts"
    | "depends_on";
}
52. L5 — Overall Marriage Decision
interface MarriageDecisionResult {
  consultation_id: string;

  person_a: MarriagePersonReference;

  person_b: MarriagePersonReference;

  canonical_a: MarriageCanonicalSnapshot;

  canonical_b: MarriageCanonicalSnapshot;

  evidence: MarriageEvidence[];

  domains: MarriageDomainResults;

  overall: MarriageOverallDecision;

  recommendations: MarriageRecommendation[]; // internal compatibility only; public recommendations attach after Assessment

  timing?: MarriageTimingResult;

  confidence: MarriageConfidenceResult;

  versions: MarriageVersionBundle;

  created_at: string;
}
MarriageDecisionResult là factual output nội bộ.

Public semantic output là Marriage Assessment. Xem `03A_ASSESSMENT_PROFILE.md`.

interface MarriageAssessment {
  assessment_id: string;

  consultation_id: string;

  question_set_id: "TV-01-QSET-1.0";

  answers: MarriageAssessmentAnswer[];

  overall: MarriageAssessmentAnswer;

  source_decision_id: string;

  confidence: MarriageConfidenceResult;

  versions: MarriageVersionBundle;
}

Đây không được dùng để sửa Decision.
53. MarriageOverallDecision
interface MarriageOverallDecision {
  score: number;

  grade: DomainGrade;

  confidence: number;

  headline_finding_ids: string[];

  strength_finding_ids: string[];

  risk_finding_ids: string[];

  condition_finding_ids: string[];

  domain_scores: Record<MarriageDomain, number>;
}
Không lưu customer prose làm truth ở đây.
54. Overall Score
0–100
Score phải xác định từ:
Marriage Decision Profile
+
Domain Decisions
+
Evidence significance
+
Confidence
+
Cross-domain interaction
Chi tiết không nằm trong Data Model.
Sẽ được định nghĩa ở:
03_DECISION_PROFILE.md
và:
04_SCORE_ENGINE.md
55. MarriageRecommendation
interface MarriageRecommendation {
  recommendation_id: string;

  domain: MarriageDomain;

  priority: FindingPriority;

  source_finding_ids: string[];

  action_type: RecommendationType;

  narrative_key?: string;

  technical_reason?: string;
}
56. RecommendationType
type RecommendationType =
  | "reinforce_strength"
  | "reduce_conflict"
  | "communication"
  | "financial_structure"
  | "family_structure"
  | "timing_awareness"
  | "role_balance"
  | "general";
Recommendation phải có source_finding_ids.
Không có source finding:
Không được publish recommendation.

57. MarriageTimingResult
interface MarriageTimingResult {
  window: MarriageLuckWindow;

  periods: MarriageTimingPeriod[];

  strongest_periods?: string[];

  sensitive_periods?: string[];
}
58. MarriageTimingPeriod
interface MarriageTimingPeriod {
  start_year: number;

  end_year: number;

  status: TimingStatus;

  score?: number;

  confidence: number;

  evidence_ids: string[];

  affected_domains: MarriageDomain[];
}
59. TimingStatus
type TimingStatus =
  | "supportive"
  | "stable"
  | "mixed"
  | "sensitive";
Không sử dụng:
đại hung
đại cát
ly hôn
tai họa
ở factual timing enum.
60. MarriageConfidenceResult
interface MarriageConfidenceResult {
  overall: number;

  data_quality: number;

  evidence_quality: number;

  engine_coverage: number;

  conflicts_penalty?: number;

  level: ConfidenceLevel;

  limitations: string[];
}
61. ConfidenceLevel
type ConfidenceLevel =
  | "high"
  | "medium"
  | "reference_only";
Presentation:
high           → Độ tin cậy cao
medium         → Khá tin cậy
reference_only → Mang tính tham khảo
62. Confidence và Score độc lập
Không được nhầm:
Compatibility Score
với:
Confidence
Ví dụ hoàn toàn hợp lệ:
Compatibility = 84
Confidence = 0.62
Nghĩa là:
kết quả hiện thiên về tương hợp tốt, nhưng dữ liệu đầu vào chưa đủ mạnh để kết luận với độ tin cậy cao.
63. MarriageVersionBundle
interface MarriageVersionBundle {
  module_version: string;

  decision_profile_version: string;

  score_model_version: string;

  rule_catalog_version: string;

  narrative_version?: string;

  canonical_versions: CanonicalVersionReference;
}
64. consultation_id
Mỗi lần phân tích phải có ID riêng:
marriage_consultation_id
Không reuse:
analysis_id của Person A
hoặc:
analysis_id của Person B
Vì:
analysis A
analysis B
marriage consultation
là ba objects khác nhau.
65. L6 — Presentation Result
Customer UI không render trực tiếp từ raw Decision Result.
Phải qua Presentation Adapter:
interface MarriagePresentationResult {
  identity: MarriageIdentityView;

  hero: MarriageHeroView;

  strengths: MarriageFindingView[];

  risks: MarriageFindingView[];

  domains: MarriageDomainView[];

  timing?: MarriageTimingView;

  recommendations: MarriageRecommendationView[];

  confidence: MarriageConfidenceView;

  disclaimer?: string;
}
66. MarriageHeroView
interface MarriageHeroView {
  score_display: string;

  grade_display: string;

  title: string;

  summary: string;

  top_strengths: string[];

  top_risks: string[];
}
Ví dụ:
82 / 100
Tương hợp tốt
Nhưng những chuỗi này thuộc Presentation Layer.
67. Narrative không phải Truth
Không lưu:
"Hai bạn rất hợp nhau..."
làm canonical decision truth.
Canonical truth là:
finding_id
evidence_ids
score
grade
confidence
Narrative Composer mới chuyển chúng thành câu chữ.
68. Narrative Binding
Narrative phải bind theo:
finding_id
recommendation_id
domain
priority
confidence
Không cho phép Composer tự đọc raw pillars rồi sáng tạo kết luận mới.
69. History Record
interface MarriageHistoryRecord {
  consultation_id: string;

  person_a_analysis_id: string;

  person_b_analysis_id: string;

  display_label?: string;

  score: number;

  grade: DomainGrade;

  confidence: number;

  versions: MarriageVersionBundle;

  created_at: string;
}
History list không cần nhúng toàn bộ Decision Result.
70. Full History Payload
Full record có thể lưu:
interface MarriageStoredResult {
  history: MarriageHistoryRecord;

  request: MarriageConsultationRequest;

  result: MarriageDecisionResult;

  presentation?: MarriagePresentationResult;
}
Tùy storage architecture hiện tại của BTE.
71. Deterministic Data Contract
Với:
Request
Canonical A
Canonical B
Decision Profile Version
Rule Catalog Version
Score Model Version
không đổi thì:
Evidence
Findings
Domain Scores
Overall Score
Grade
Recommendations
phải không đổi.
72. ID Stability
Các ID semantic phải stable:
rule_id
finding type
domain
recommendation type
Instance ID có thể khác giữa các request.
Không được dùng customer text làm identity.
73. Data Normalization
Canonical data không dùng chuỗi hiển thị tiếng Việt làm logic key.
Ví dụ không dùng:
"Tương hợp tốt"
"Hỏa"
"Nam"
làm internal enums.
Dùng:
B
fire
male
và map ở presentation.
74. Nullability
Phải phân biệt:
null
unavailable
empty
zero
Ví dụ:
hour pillar = null
nghĩa là không có dữ liệu giờ sinh.
Không được:
hour pillar = {}
rồi coi là dữ liệu hợp lệ.
75. Missing Data Policy
Nếu một domain thiếu đủ dữ liệu:
interface DomainAvailability {
  available: boolean;

  reason?: string;

  required_fields_missing?: string[];
}
Không được tự sinh score mặc định 50.
76. Domain Availability
MarriageDomainDecision nên hỗ trợ:
availability: DomainAvailability;
Nếu:
available = false
thì:
score = null
grade = null
Không giả lập kết quả.
77. Revised MarriageDomainDecision
Canonical shape khuyến nghị:
interface MarriageDomainDecision {
  domain: MarriageDomain;

  availability: DomainAvailability;

  score: number | null;

  grade: DomainGrade | null;

  confidence: number;

  findings: MarriageFinding[];

  evidence_ids: string[];

  cross_domain_refs?: FindingReference[];
}
78. Sensitive Findings
Các chủ đề như:
- ngoại tình;
- bạo lực;
- ly hôn;
- vô sinh;
- bệnh;
- tử vong;
không được tồn tại như deterministic factual enums của TV-01 V1.
Không tạo:
infidelity_risk = 0.8
divorce_score = 74
Nếu một cấu trúc truyền thống liên quan tới bất ổn tình cảm, hệ thống chỉ được diễn giải ở cấp:
relationship_pressure
communication_risk
emotional_instability
có evidence và confidence phù hợp.
79. Data Integrity Rules
Một MarriageDecisionResult hợp lệ phải đáp ứng:
1. Có consultation_id.
2. Có analysis_id của A.
3. Có analysis_id của B.
4. Evidence source phải tồn tại.
5. Finding phải reference evidence hợp lệ.
6. Recommendation phải reference finding hợp lệ.
7. Domain score phải thuộc 0–100 hoặc null.
8. Overall score phải thuộc 0–100.
9. Confidence phải thuộc 0–1.
10. Grade phải thuộc enum đã định nghĩa.
11. Version bundle không được thiếu.
12. Không dùng presentation text làm factual key.
80. Evidence Referential Integrity
Ví dụ:
finding F-001
   ↓
evidence MEV-001
   ↓
source
A.analysis_id
A.useful_god
Nếu MEV-001 không tồn tại:
Result invalid.

Nếu source path không thể trace:
Evidence invalid.

81. Recommendation Referential Integrity
Recommendation
    ↓
Finding
    ↓
Evidence
    ↓
Canonical source
Đây là chuỗi bắt buộc.
82. Serialization
Canonical API serialization:
JSON UTF-8
Không phụ thuộc:
- HTML;
- CSS;
- browser;
- DOCX;
- PDF.
83. Date / Time Standard
Canonical datetime:
ISO 8601
Ví dụ:
2026-09-06T22:30:00+07:00
Không lưu:
06/09/2026 22:30
làm canonical datetime.
84. Numeric Precision
Score:
0–100
Có thể lưu số thực nội bộ.
Ví dụ:
82.4375
Presentation có thể hiển thị:
82
hoặc:
82.4
theo UI Standard.
Không làm tròn trước tầng Decision.
85. Confidence Precision
Confidence:
0.0–1.0
Không lưu:
82%
làm canonical value.
Presentation tự chuyển:
0.82 → 82%
nếu cần.
86. Domain Score Independence
Không yêu cầu:
average(domain scores) = overall score
Overall score có thể sử dụng:
- weights;
- dependencies;
- caps;
- penalties;
- confidence;
- cross-domain effects.
Điều này sẽ được định nghĩa ở Score Engine.
87. Không hard-code customer wording
Data Model không chứa các câu như:
"Đây là cặp đôi trời sinh"
hoặc:
"Hai bạn nên cân nhắc kỹ"
như giá trị logic.
Customer wording thuộc Narrative Catalog.
88. Cross-module Reuse
Các cấu trúc sau nên được thiết kế để sau này có thể chuyển thành COMMON types:
Evidence
Finding
Recommendation
Confidence
Decision Result
Version Bundle
Domain Availability
TV-02, TV-03, TV-04 có thể reuse.
89. Không generic hóa quá sớm
Trong TV-01 V1 vẫn sử dụng các tên rõ nghĩa:
MarriageEvidence
MarriageFinding
MarriageDecisionResult
Không ép toàn bộ thành abstract generic framework trước khi TV-01 chạy ổn định.
Sau khi TV-01 và TV-02 có contract ổn định mới cân nhắc extract vào:
knowledge/consulting/COMMON/
90. Recommended Canonical Object Tree
MarriageConsultationRequest
│
├── person_a
├── person_b
└── options
        │
        ▼
MarriageDecisionResult
│
├── consultation_id
│
├── person_a
├── person_b
│
├── canonical_a
├── canonical_b
│
├── evidence[]
│
├── domains
│   ├── five_elements
│   ├── stem_branch
│   ├── ten_gods
│   ├── interaction
│   ├── finance
│   ├── family
│   ├── children
│   └── luck
│
├── overall
│
├── recommendations[]
│
├── timing
│
├── confidence
│
└── versions
91. Minimal API Result
Nếu API cần chế độ compact:
interface MarriageConsultationSummary {
  consultation_id: string;

  person_a_analysis_id: string;

  person_b_analysis_id: string;

  score: number;

  grade: DomainGrade;

  confidence: number;
}
Full result lấy qua endpoint detail sau này.
92. Example — Simplified Result
Ví dụ minh họa cấu trúc, không phải golden result:
{
  "consultation_id": "MC-20260906-0001",

  "person_a": {
    "analysis_id": "A-001",
    "gender": "male"
  },

  "person_b": {
    "analysis_id": "B-001",
    "gender": "female"
  },

  "overall": {
    "score": 82.4,
    "grade": "B",
    "confidence": 0.91,
    "headline_finding_ids": [
      "MF-001",
      "MF-004"
    ]
  },

  "confidence": {
    "overall": 0.91,
    "data_quality": 1.0,
    "evidence_quality": 0.9,
    "engine_coverage": 0.95,
    "level": "high",
    "limitations": []
  }
}
Không sử dụng sample này làm Golden Dataset.
93. Example — Evidence
{
  "evidence_id": "MEV-001",

  "domain": "five_elements",

  "evidence_type": "useful_god_support",

  "direction": "positive",

  "significance": "major",

  "confidence": 0.94,

  "subject": "B_TO_A",

  "rule_id": "marriage.element.useful_support.v1",

  "source_refs": [
    {
      "analysis_id": "A-001",
      "person": "A",
      "path": "useful_god.useful"
    },
    {
      "analysis_id": "B-001",
      "person": "B",
      "path": "five_elements"
    }
  ]
}
94. Example — Finding
{
  "finding_id": "MF-001",

  "domain": "five_elements",

  "type": "support",

  "priority": "P1",

  "direction": "positive",

  "confidence": 0.92,

  "evidence_ids": [
    "MEV-001",
    "MEV-003"
  ],

  "recommendation_ids": [
    "MR-001"
  ]
}
95. Example — Recommendation
{
  "recommendation_id": "MR-001",

  "domain": "five_elements",

  "priority": "P2",

  "source_finding_ids": [
    "MF-001"
  ],

  "action_type": "reinforce_strength"
}
Narrative Composer mới chuyển thành nội dung khách hàng.
96. Data Model Freeze Conditions
01_DATA_MODEL.md chỉ được FREEZE khi Product Owner xác nhận:
- Request model đúng.
- Person A/B dùng canonical BTE analysis.
- Không tạo Marriage BaZi riêng.
- Missing hour không được giả lập.
- Có canonical snapshot.
- Có Evidence Layer.
- Có Finding Layer.
- Có Domain Decision.
- Có Overall Decision.
- Score và Confidence tách biệt.
- Recommendation trace được về Finding.
- Finding trace được về Evidence.
- Evidence trace được về canonical source.
- Có Domain Availability.
- Có Version Bundle.
- Có History-ready model.
- Có Presentation model riêng.
- Narrative không phải factual truth.
- Có deterministic contract.
- Có khả năng reuse cho Consulting COMMON sau này.
97. Architectural Invariant
Chuỗi dữ liệu bắt buộc:
Canonical Analysis
        ↓
Relationship Evidence
        ↓
Finding
        ↓
Decision
        ↓
Recommendation
        ↓
Narrative
Không được đi tắt:
Canonical Analysis
        ↓
AI Narrative
và cũng không được:
Birth Data
        ↓
Marriage Score
mà không tạo evidence trung gian.
98. Core Data Rule
No evidence → no finding.

No finding → no recommendation.

No canonical source → no evidence.

Ba quy tắc này là nền tảng của Data Model TV-01.
99. Status
TV-01-01 STATUS: DRAFT
Chưa implementation.
Sau khi Product Owner duyệt và FREEZE tài liệu này, bước kế tiếp là:
TV-01 / 02_RUNTIME_PIPELINE.md
Không viết Decision Profile hoặc Score Engine trước khi Data Model được chốt.

Tôi đặc biệt muốn giữ nguyên ba invariant cuối cùng: **`No canonical source → no evidence → no finding → no recommendation`**. Nó giải quyết đúng vấn đề chúng ta từng gặp ở phần luận giải BTE: câu chữ không được phép tự “sáng tác” vượt ra ngoài dữ liệu tính toán. Khi sau này ngôn từ cần làm hay hơn, chúng ta có thể thay Narrative Composer mà **không làm thay đổi kết luận kỹ thuật**.