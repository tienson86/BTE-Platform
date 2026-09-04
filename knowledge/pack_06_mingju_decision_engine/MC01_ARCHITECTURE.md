# MC-01 — MỆNH CỤC DECISION ENGINE ARCHITECTURE

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Status:** DESIGN DRAFT  
**Language:** Canonical IDs in English, customer-facing interpretation in Vietnamese.

---

# 1. PURPOSE

MC-01 transforms the raw BaZi analytical result into a structured
assessment of the chart's Mệnh Cục.

The engine MUST NOT merely return a pattern name such as:

- Chính Quan cách
- Thiên Tài cách
- Thực Thần cách
- Thương Quan cách
- Tòng cách

The pattern name is only one input.

MC-01 must answer the higher-level questions:

1. Cách cục gì?
2. Cách có thành hay không?
3. Cách có thuần hay tạp?
4. Cách mạnh hay yếu?
5. Có bị phá không?
6. Nếu bị phá thì có cứu không?
7. Mức độ hoàn chỉnh của cấu trúc?
8. Tiềm năng thành tựu thuộc lĩnh vực nào?
9. Khả năng tài vận như thế nào?
10. Khả năng quan vận / quản trị / làm chủ thế nào?
11. Điều kiện nào làm mệnh cục phát huy?
12. Điều kiện nào làm mệnh cục suy giảm?

MC-01 is therefore a:

> Structured BaZi Decision Engine

rather than a simple Pattern Classification Engine.

---

# 2. CORE PRINCIPLE

## 2.1 Pattern is not destiny

A chart MUST NOT be rated solely from the pattern label.

Example:

```text
Chính Quan cách
does NOT automatically imply:
Quan vận cao
Phú quý
Thành công
The engine must continue evaluating the full structure.
Canonical inference:
Pattern
    ↓
Purity
    ↓
Pattern Strength
    ↓
Support
    ↓
Damage
    ↓
Rescue
    ↓
Useful-God Compatibility
    ↓
Climate / Temperature Compatibility
    ↓
Structural Integrity
    ↓
Pattern Grade
    ↓
Achievement Profiles
    ↓
Final Decision
3. SEPARATION OF CONCERNS
MC-01 MUST NOT recalculate upstream canonical engines.
It consumes their published outputs.
Upstream truth remains owned by:
Calendar Engine
      ↓
BaZi Engine
      ↓
Five Elements
      ↓
Ten Gods
      ↓
Strength Engine
      ↓
Temperature Engine
      ↓
Pattern Engine
      ↓
Useful God Engine
MC-01 begins AFTER these facts are available.
MC-01 is responsible for:
SYNTHESIS
+
DECISION
+
EXPLANATION
not base-calendar or BaZi computation.
4. INPUT DOMAINS
MC-01 may consume the following canonical evidence.
4.1 Identity of chart
- Day Master
- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
4.2 Five Elements
- elemental distribution
- season / month command
- root support
- generating relationships
- controlling relationships
- drain relationships
4.3 Ten Gods
- visible Ten Gods
- hidden Ten Gods
- root status
- exposed stems
- dominant Ten Gods
- conflicting Ten Gods
4.4 Day Master Strength
Examples:
extremely_weak
very_weak
weak
balanced
strong
very_strong
extremely_strong
MC-01 MUST consume canonical Strength output.
It MUST NOT create an independent second strength calculation.
4.5 Pattern
Consume canonical Pattern Engine output:
main_pattern
secondary_pattern
special_pattern
follow_pattern
combination_pattern
pattern_confidence
when available.
4.6 Temperature / Điều Hậu
Consume:
temperature_state
climate_need
warming_need
cooling_need
dryness
humidity
according to published upstream contract.
4.7 Useful God
Consume:
useful_god
favorable_gods
unfavorable_gods
reasoning evidence
MC-01 MUST distinguish:
Pattern requirement
from:
Useful God requirement
They may agree or conflict.
That conflict is meaningful evidence.
4.8 Stem/Branch relations
When canonically available:
- 合 Hợp
- 冲 Xung
- 刑 Hình
- 害 Hại
- 破 Phá
- self-punishment
- combination transformation
- clash activation
- root destruction
These relationships may influence Damage or Rescue.
5. NON-INPUTS
The following MUST NOT determine the natal Mệnh Cục grade directly:
- customer biography
- known wealth
- known job title
- current income
- subjective consultant opinion
- manually entered desired conclusion
Observed life events MAY later be used for validation,
but never as hidden inference input.
6. MC-01 DECISION PIPELINE
Canonical pipeline:
MCContext
   │
   ├── Pattern Recognition
   │
   ├── Purity Analysis
   │
   ├── Pattern Strength Analysis
   │
   ├── Support Analysis
   │
   ├── Damage Analysis
   │
   ├── Rescue Analysis
   │
   ├── Useful-God Compatibility
   │
   ├── Climate Compatibility
   │
   ├── Structural Integrity
   │
   ├── Grade Decision
   │
   ├── Achievement Model
   │
   ├── Wealth Model
   │
   ├── Authority / Career Model
   │
   └── Decision Composer
   │
   ▼
MingJuDecisionResult
7. LAYER 1 — PATTERN RECOGNITION
Pattern Recognition identifies the structural family.
Examples:
Chính Quan
Thất Sát
Chính Tài
Thiên Tài
Chính Ấn
Thiên Ấn
Thực Thần
Thương Quan
Kiến Lộc
Dương Nhẫn
Tòng Tài
Tòng Quan Sát
Tòng Nhi
Tòng Vượng
Hóa Khí
Special Combination
MC-01 SHOULD reuse Pattern Engine results.
If Pattern Engine cannot determine a valid pattern:
pattern_state = unresolved
MC-01 MUST NOT fabricate one.
8. LAYER 2 — PATTERN PURITY
Purity describes how cleanly the pattern's governing structure is expressed.
Example dimensions:
primary deity dominance
competing deity interference
mixed Quan/Sát
mixed Tài structures
hidden contradictory forces
stem exposure
root consistency
Canonical score:
purity_score: 0..100
Suggested interpretation bands:
90–100  very_pure
75–89   pure
60–74   moderately_pure
40–59   mixed
20–39   heavily_mixed
0–19    structurally_impure
These thresholds remain CONFIGURABLE until golden-case validation.
9. LAYER 3 — PATTERN STRENGTH
Pattern Strength is NOT Day Master Strength.
It measures whether the forces forming the pattern have sufficient structural power.
Possible evidence:
month command support
root depth
stem exposure
season support
element generation
branch support
multiple roots
deity continuity
Output:
pattern_strength_score: 0..100
Classification example:
very_weak
weak
moderate
strong
very_strong
10. LAYER 4 — SUPPORT
Support identifies factors that help the pattern function.
Examples:
For Chính Quan:
Tài sinh Quan
Ấn hộ Quan
Quan có căn
Quan đắc lệnh
Day Master capable of receiving Quan
For Thực Thần:
Nhật chủ đủ lực sinh Thực
Thực có căn
Thực sinh Tài
không bị Kiêu đoạt Thực
Support events MUST be explicit evidence records.
Example:
{
  "rule_id": "MC-SUPPORT-...",
  "factor": "...",
  "weight": 0.0,
  "evidence": []
}
11. LAYER 5 — DAMAGE
Damage evaluates mechanisms that weaken or break the pattern.
Potential damage families:
direct controlling deity
harmful Ten-God interaction
loss of root
clash
punishment
destructive combination
excessive mixed structure
seasonal incompatibility
useful-god conflict
Examples:
Thương Quan kiến Quan
Kiêu thần đoạt Thực
Tỷ Kiếp đoạt Tài
Quan Sát hỗn tạp
Tài nhiều thân nhược
Sát mạnh thân nhược
Ấn quá vượng làm nghẽn tiết
Every damage finding MUST expose:
damage_id
severity
source
target
evidence
Severity:
minor
moderate
major
critical
12. LAYER 6 — RESCUE
A damaged structure MUST NOT automatically become a failed pattern.
The engine must inspect whether another structure resolves or reduces the damage.
Examples:
Thương Quan kiến Quan
    +
Ấn chế Thương
    =
rescue candidate
Thất Sát quá mạnh
    +
Ấn hóa Sát
    =
rescue candidate
Tỷ Kiếp đoạt Tài
    +
Quan chế Tỷ Kiếp
    =
rescue candidate
Rescue has:
rescue_strength
rescue_reliability
damage_offset
Rescue MUST NOT erase Damage history.
Both must remain visible for explanation.
13. LAYER 7 — USEFUL GOD COMPATIBILITY
MC-01 must evaluate whether the structure's needs are consistent with:
Dụng Thần
Hỷ Thần
Kỵ Thần
Example:
Pattern requires Hỏa
Useful God = Hỏa
This is strong structural agreement.
But:
Pattern benefits from Kim
Temperature urgently requires Hỏa
This is a multi-objective conflict.
The engine MUST retain the conflict rather than force a false binary answer.
Possible output:
compatibility_score
agreement_factors
conflict_factors
14. LAYER 8 — CLIMATE COMPATIBILITY
Điều Hậu can override simplistic elemental conclusions.
Example:
Day Master structurally strong
BUT chart extremely cold
The engine MUST retain:
structural strength
and
climate requirement
as separate dimensions.
MC-01 MUST NOT interpret:
strong element = automatically unfavorable
weak element = automatically favorable
15. LAYER 9 — STRUCTURAL INTEGRITY
Structural Integrity combines:
Purity
Pattern Strength
Support
Damage
Rescue
Useful-God compatibility
Climate compatibility
Output:
integrity_score: 0..100
This is the primary basis for "thành cách / bại cách".
Suggested state model:
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
IMPORTANT:
"failed" MUST require strong evidence.
Do not classify a chart as bại cách merely because one negative relation exists.
16. LAYER 10 — PATTERN GRADE
Grade is a customer-friendly summary of structural quality.
Proposed scale:
SS
S
A
B
C
D
However:
Grade MUST NOT initially be mapped directly to:
rich
poor
powerful
ordinary
until validated.
Canonical meaning should first remain:
SS = exceptional structural integrity
S  = very high structural integrity
A  = strong structure
B  = workable / conditional structure
C  = substantially compromised
D  = severely compromised
This distinction is critical.
Structural quality is not the same as realized social status.
17. ACHIEVEMENT MODEL
MC-01 may generate separate potentials instead of one universal "success score".
Initial dimensions:
authority
management
entrepreneurship
wealth_creation
wealth_retention
academic
technical
creative
public_visibility
stability
independence
Each dimension:
score: 0..100
confidence: 0..1
evidence[]
The score MUST be based on documented rules.
No random weighting.
18. AUTHORITY / QUAN VẬN MODEL
Quan vận MUST NOT equal simply "Quan exists".
Potential evidence includes:
Quan/Sát quality
Quan/Sát root
Quan/Sát purity
Tài → Quan support
Ấn relationship
Day Master capacity
Thương Quan interference
rescue
structure integrity
Output examples:
authority_potential
institutional_career_potential
leadership_potential
discipline_structure
The customer wording may later use:
Khả năng quản lý
Khả năng giữ chức vụ
Khả năng làm việc trong hệ thống
Khả năng lãnh đạo
Avoid deterministic claims such as:
"chắc chắn làm quan"
19. WEALTH MODEL
Wealth potential MUST NOT equal "Tài tinh nhiều".
Evaluate at least:
wealth star quality
wealth roots
wealth exposure
Day Master ability to carry wealth
Tỷ/Kiếp pressure
Thực/Thương generation
Quan protection
wealth usefulness
wealth as favorable/unfavorable force
Separate outputs:
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
This separation is required because:
kiếm tiền giỏi
is not equivalent to:
giữ tiền giỏi
20. ENTREPRENEURSHIP MODEL
Potential signals may include:
Tài
Thực/Thương
Tỷ/Kiếp
leadership structure
risk profile
independence
resource mobilization
The engine MUST distinguish:
business aptitude
from:
wealth potential
A person may have strong entrepreneurial tendencies but poor wealth retention.
21. CAREER MODEL
Career recommendations are downstream interpretations.
They MUST NOT be generated from one Ten God alone.
Recommended model:
primary_work_style
secondary_work_style
institutional_fit
entrepreneurial_fit
technical_fit
academic_fit
creative_fit
leadership_fit
Only after this structured model exists should customer wording be composed.
22. NATAL VS LUCK
MC-01 must distinguish:
Natal Capacity
from:
Luck Activation
Natal chart answers:
What potential exists?
Luck cycles answer:
When can it activate?
Therefore:
Mệnh cục grade
MUST NOT change every Đại Vận.
Later modules may compute:
activation_score_by_luck_cycle
but the natal structure remains stable.
23. DECISION RESULT MODEL
Conceptual output:
{
  "schema_version": "bte.mingju.decision.v1",

  "pattern": {
    "primary": null,
    "secondary": [],
    "confidence": 0.0
  },

  "purity": {
    "score": 0,
    "state": null,
    "evidence": []
  },

  "pattern_strength": {
    "score": 0,
    "state": null,
    "evidence": []
  },

  "support": [],

  "damage": [],

  "rescue": [],

  "useful_god_compatibility": {
    "score": 0,
    "agreements": [],
    "conflicts": []
  },

  "climate_compatibility": {
    "score": 0,
    "evidence": []
  },

  "integrity": {
    "score": 0,
    "state": null
  },

  "grade": {
    "value": null,
    "confidence": 0.0
  },

  "achievement": {
    "authority": null,
    "management": null,
    "entrepreneurship": null,
    "wealth_creation": null,
    "wealth_retention": null,
    "academic": null,
    "technical": null,
    "creative": null,
    "public_visibility": null,
    "stability": null
  },

  "decision": {
    "headline": null,
    "summary": [],
    "strengths": [],
    "risks": [],
    "conditions_for_success": [],
    "conditions_to_avoid": []
  },

  "trace": []
}
This is conceptual only.
The exact dataclass / Pydantic contract will be defined in 01_DATA_MODEL.md.
24. EXPLAINABILITY REQUIREMENT
Every significant decision MUST be traceable.
Example:
authority_potential = 82
is unacceptable without evidence.
It should be explainable as:
+ Chính Quan đắc lệnh
+ Quan có căn
+ Tài sinh Quan
+ Ấn hỗ trợ
- Thương Quan lộ
+ Có Ấn chế Thương
Each conclusion therefore requires:
rule_id
input facts
effect
weight
result
MC-01 MUST support deterministic audit.
25. CONFIDENCE
Score and confidence are separate.
Example:
authority_score = 85
confidence = 0.53
means:
The model sees strong authority signals,
but evidence is incomplete or conflicting.
Confidence factors MAY include:
input completeness
pattern confidence
conflicting rules
unresolved transformations
unknown hour pillar
Do not fake confidence.
26. UNKNOWN / UNRESOLVED
MC-01 must support uncertainty explicitly.
Valid states include:
unknown
unresolved
insufficient_evidence
conflicting_evidence
The engine MUST prefer:
insufficient evidence
over an unsupported strong conclusion.
27. RULE DESIGN
Rules SHOULD be stored independently from presentation text.
Conceptual rule:
rule_id
domain
conditions
positive_effects
negative_effects
weight
priority
exceptions
references
explanation_key
Do not embed long Vietnamese interpretation paragraphs directly in calculation rules.
28. ENGINE VS COMPOSER
Strict separation:
Decision Engine
returns structured facts.
Decision Composer
turns facts into customer-facing language.
Example engine result:
damage:
- type: hurting_officer_attacks_officer
  severity: moderate

rescue:
- type: seal_controls_hurting_officer
  strength: strong
Composer may produce:
"Mệnh cục có dấu hiệu Thương Quan chế Quan,
nhưng được Ấn tinh hỗ trợ nên mức phá cách được giảm đáng kể."
Calculation must never depend on wording.
29. CUSTOMER PRESENTATION
The dedicated Mệnh Cục card MAY eventually show:
MỆNH CỤC

Chính Quan cách

Grade: A

Độ thuần
86%

Độ hoàn chỉnh
82%

Trạng thái
Thành cách có điều kiện

Quan vận
★★★★☆

Quản trị
★★★★☆

Kinh doanh
★★★☆☆

Tài vận
★★★★☆

Ổn định
★★★★★
Detailed interpretation appears below.
UI is NOT part of MC-01 core calculation.
30. SAFETY AGAINST OVERCLAIMING
MC-01 should use probabilistic / potential wording.
Prefer:
có lợi thế
có thiên hướng
tiềm năng cao
điều kiện thuận lợi
cấu trúc hỗ trợ
Avoid deterministic statements:
chắc chắn giàu
nhất định làm quan
số nghèo
không thể thành công
The engine evaluates structural potential, not guaranteed life outcomes.
31. VERSIONING
Initial canonical schema:
bte.mingju.decision.v1
Ruleset:
bte.mingju.rules.v1
Composer:
bte.mingju.composer.v1
All three MUST be independently versionable.
32. DETERMINISM
Given identical canonical inputs and identical rule version:
MC-01(input) == MC-01(input)
always.
No:
- LLM randomness
- external web knowledge
- hidden customer profile
- runtime subjective adjustment
inside the decision engine.
LLM may later explain the deterministic result,
but MUST NOT replace the canonical decision.
33. INITIAL IMPLEMENTATION BOUNDARY
MC-01 Phase 1 MUST focus on:
Pattern
Purity
Pattern Strength
Support
Damage
Rescue
Integrity
Grade
Trace
DO NOT implement final wealth/career scoring until the structural model has passed validation.
Recommended phases:
MC-01A Structural Foundation
MC-01B Purity & Strength
MC-01C Damage & Rescue
MC-01D Integrity & Grade
MC-01E Achievement Model
MC-01F Wealth Model
MC-01G Authority Model
MC-01H Career Model
MC-01I Composer
MC-01J Runtime Integration
34. VALIDATION STRATEGY
MC-01 cannot be validated with one chart.
Required validation families:
Strong Day Master
Weak Day Master
Balanced Day Master

Pure Chính Quan
Mixed Quan/Sát
Thương Quan kiến Quan
Sát Ấn tương sinh
Thực Thần sinh Tài
Kiêu thần đoạt Thực
Tỷ Kiếp đoạt Tài

Tòng Tài
Tòng Quan
Tòng Nhi
Tòng Vượng

Cold chart
Hot chart
Dry chart
Wet chart

Pattern damaged
Pattern rescued
Pattern unresolved
Each family should contain multiple Golden Cases.
35. GOLDEN CASE PRINCIPLE
Golden Cases MUST store:
input pillars
canonical upstream facts
expected structural findings
accepted alternatives
forbidden conclusions
expert notes
Do NOT store only:
expected grade = A
because this hides the reasoning.
We test the inference chain.
36. FAILURE CONDITIONS
MC-01 must FAIL validation if it:
1. recalculates Day Master strength inconsistently with Strength Engine
2. overwrites Pattern Engine truth silently
3. declares a grade without trace
4. maps one pattern directly to wealth/authority
5. treats element count as full useful-god reasoning
6. treats one damaging factor as automatic failed pattern
7. ignores rescue mechanisms
8. ignores Điều Hậu
9. changes natal grade according to current Đại Vận
10. generates unsupported deterministic life claims
37. ACCEPTANCE PRINCIPLE
MC-01 is accepted only when:
Same facts
→ Same reasoning
→ Same grade
→ Explainable trace
and domain experts can inspect:
Why did the engine conclude this?
without needing to read source code.
38. ARCHITECTURAL DECISION
The central rule of MC-01 is frozen:
MỆNH CỤC IS A STRUCTURAL DECISION,
NOT A SINGLE PATTERN LABEL.

Final inference:
Mệnh cục
=
Pattern identity
+ Purity
+ Pattern strength
+ Supporting structure
- Structural damage
+ Rescue
+ Useful-God compatibility
+ Climate compatibility
→ Structural integrity
→ Grade
→ Domain potentials
This architecture is the canonical foundation for all later MC-01 work.
39. NEXT DOCUMENT
Next:
01_DATA_MODEL.md
It will freeze:
- enums
- evidence objects
- score objects
- damage records
- rescue records
- trace model
- grade model
- final MingJuDecisionResult
- serialization contract

### Có một điểm tôi muốn chúng ta khóa ngay

Tôi cố ý **chưa đưa công thức kiểu `Purity × 20% + Strength × 30%...` vào kiến trúc**.

Nếu chốt trọng số quá sớm, chúng ta rất dễ tạo ra một engine nhìn có vẻ khoa học nhưng thực chất là **các con số do mình tự đặt**.

Trình tự đúng sẽ là:

**định nghĩa hiện tượng → xác định rule → lập Golden Cases → kiểm chứng chuyên gia → sau đó mới hiệu chỉnh weight.**

Và có một thay đổi quan trọng so với ý tưởng ban đầu: **SS/S/A/B/C/D trước tiên chỉ đại diện cho chất lượng cấu trúc mệnh cục**, chưa được phép dịch thẳng thành “đại phú”, “đại quý”, “nghèo”. Giàu, quan, kinh doanh, học thuật... phải được các model phía sau suy luận riêng. Như vậy mới tránh lỗi rất phổ biến là thấy một “cách đẹp” rồi kết luận người đó chắc chắn giàu.

Bước tiếp theo chúng ta nên làm ngay **`01_DATA_MODEL.md`** để khóa cấu trúc dữ liệu trước khi viết bất kỳ rule Mệnh Cục nào.