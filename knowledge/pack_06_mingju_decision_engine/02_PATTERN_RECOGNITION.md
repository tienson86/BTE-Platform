# MC-01 — PATTERN RECOGNITION

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `02_PATTERN_RECOGNITION.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`

---

# 1. PURPOSE

This document defines how MC-01 consumes, normalizes, validates, and interprets Pattern Engine output.

Pattern Recognition is the first structural stage of MC-01.

Its purpose is NOT to recalculate the BaZi pattern.

Its purpose is to convert upstream Pattern Engine truth into a stable, auditable `PatternDecision` that later MC-01 stages can safely consume.

Canonical flow:

```text
Pattern Engine
      ↓
Pattern Input Adapter
      ↓
Validation
      ↓
Normalization
      ↓
Precedence Resolution
      ↓
Conflict Detection
      ↓
PatternDecision
      ↓
Purity / Strength / Damage / Rescue

2. CORE PRINCIPLE
The Pattern Engine owns pattern identity.
MC-01 owns structural synthesis.
Therefore:
Pattern Engine
= What pattern is this chart?

MC-01
= How good, pure, stable, damaged, rescued, and usable is that pattern?
MC-01 MUST NOT silently replace upstream pattern truth.
3. OWNERSHIP BOUNDARY
Pattern Engine owns
- main pattern
- secondary pattern
- special pattern
- follow pattern
- combination pattern
- pattern confidence
- pattern evidence
- pattern precedence logic already published upstream
MC-01 owns
- normalized pattern identity
- structural interpretation
- purity
- pattern strength
- support
- damage
- rescue
- compatibility
- integrity
- grade
- achievement implications
4. FORBIDDEN BEHAVIOR
MC-01 MUST NOT:
1. re-run the Pattern Engine internally
2. derive a new pattern from Ten Gods independently
3. override main pattern because another pattern “looks more convincing”
4. promote a secondary pattern into primary without an explicit upstream rule
5. demote a special pattern because customer wording is inconvenient
6. convert unresolved pattern into a guessed common pattern
7. use customer biography to choose between competing patterns
8. change pattern according to Đại Vận
9. change pattern because current life outcome disagrees
10. collapse all special structures into ordinary Ten-God patterns
5. INPUT CONTRACT
MC-01 consumes a normalized PatternInputContext.
Conceptual fields:
state
main_pattern
secondary_patterns
special_pattern
follow_pattern
combination_pattern
confidence
evidence
source_schema_version
source_ruleset_version
Possible source payload example:
{
  "main_pattern": "zheng_guan",
  "secondary_patterns": [
    "zheng_yin"
  ],
  "special_pattern": null,
  "follow_pattern": null,
  "combination_pattern": null,
  "confidence": 0.91
}
6. PATTERN INPUT STATE
Allowed source states:
resolved
partially_resolved
unresolved
conflicting_evidence
insufficient_evidence
invalid
MC-01 must preserve source uncertainty.
Example:
Pattern Engine = unresolved
must remain:
PatternDecision.state = unresolved
unless a future explicit upstream contract supplies a valid resolution.
7. CANONICAL PATTERN FAMILIES
MC-01 recognizes the following structural families.
7.1 Standard Ten-God Pattern Family
zheng_guan
qi_sha
zheng_cai
pian_cai
zheng_yin
pian_yin
shi_shen
shang_guan
These represent the principal conventional pattern families.
7.2 Root / Prosperity Pattern Family
jian_lu
yang_ren
These must not be forced into standard Ten-God pattern families.
7.3 Follow Pattern Family
cong_cai
cong_guan_sha
cong_er
cong_wang
Possible future additions:
cong_qiang
cong_shi
only if upstream Pattern Engine formally supports them.
7.4 Transformation Pattern Family
hua_qi
A transformed structure must remain distinct from ordinary combination evidence.
7.5 Combination / Special Structure Family
special_combination
This category is reserved for formally recognized non-standard pattern structures.
It MUST NOT become a generic bucket for unknown charts.
8. PATTERN FAMILY ENUM
Recommended enum:
standard
root_prosperity
follow
transformation
special
unresolved
Each pattern ID maps to exactly one family.
Example:
zheng_guan → standard
jian_lu → root_prosperity
cong_cai → follow
hua_qi → transformation
special_combination → special
9. PRIMARY PATTERN
primary is the main structural identity consumed by downstream MC-01 stages.
It should normally correspond to upstream:
main_pattern
unless upstream explicitly marks a higher-priority special structure.
MC-01 must not independently choose another pattern.
10. SECONDARY PATTERNS
Secondary patterns represent structurally meaningful but non-primary patterns.
Examples:
main = zheng_guan
secondary = zheng_yin
or:
main = shi_shen
secondary = pian_cai
Secondary patterns may influence:
- Purity
- Support
- Damage
- Achievement profile
- Career profile
but must not automatically dilute the main pattern.

11. SPECIAL PATTERN
special_pattern indicates that a chart matches a formally defined special structure.
Special pattern handling must distinguish:
special pattern present
from:
special pattern dominant
These are not equivalent.
Upstream contract must determine whether special structure:
supplements
overrides
or coexists with
the normal main pattern.
MC-01 cannot invent this precedence.
12. FOLLOW PATTERN
Follow patterns require strict handling.
Examples:
cong_cai
cong_guan_sha
cong_er
cong_wang
A follow pattern MUST NOT be treated as:
ordinary weak chart
or:
ordinary strong chart
The downstream logic for:
- Useful God compatibility
- Pattern Strength
- Support
- Damage
- Grade
may differ materially.
Therefore MC-01 must preserve:
pattern_family = follow
explicitly.
13. TRANSFORMATION PATTERN
Transformation patterns such as:
hua_qi
must not be inferred merely because a stem combination exists.
Pattern Engine must already determine:
transformation_valid = true
or equivalent.
MC-01 consumes the result.
If transformation conditions remain unresolved:
state = unresolved
must be preserved.
14. COMBINATION PATTERN
Combination evidence and Combination Pattern are different.
Example:
branch combination exists
does NOT automatically mean:
combination_pattern exists
MC-01 must distinguish:
relation evidence
from:
formal pattern identity
15. PATTERN PRECEDENCE
Pattern precedence MUST remain deterministic.
Recommended conceptual order:
1. Valid transformation structure
2. Valid follow structure
3. Valid formally recognized special structure
4. Root / prosperity structure
5. Standard Ten-God structure
6. Unresolved
IMPORTANT:
This list is architectural guidance only.
The actual precedence MUST match the frozen Pattern Engine rules.
MC-01 must not introduce a second competing precedence system.
16. PRECEDENCE SOURCE
PatternDecision SHOULD expose:
precedence_source
Possible values:
pattern_engine
normalized_pattern_engine
none
Never:
mc01_override
unless a future version explicitly defines such behavior.
17. PATTERN NORMALIZATION
MC-01 may normalize aliases.
Example upstream aliases:
chinh_quan
zhengguan
zheng_guan
may normalize to:
zheng_guan
Normalization is allowed only for representation.
Normalization MUST NOT alter semantic meaning.
18. PATTERN LABEL MAPPING
Canonical engine IDs remain English/stable IDs.
Customer-facing Vietnamese labels belong to a mapping layer.
Example:
zheng_guan → Chính Quan cách
qi_sha → Thất Sát cách
zheng_cai → Chính Tài cách
pian_cai → Thiên Tài cách
zheng_yin → Chính Ấn cách
pian_yin → Thiên Ấn cách
shi_shen → Thực Thần cách
shang_guan → Thương Quan cách
jian_lu → Kiến Lộc cách
yang_ren → Dương Nhẫn cách
cong_cai → Tòng Tài cách
cong_guan_sha → Tòng Quan Sát cách
cong_er → Tòng Nhi cách
cong_wang → Tòng Vượng cách
hua_qi → Hóa Khí cách
Do not store customer-facing Vietnamese labels as canonical pattern identity.
19. PATTERN DECISION MODEL
Canonical result:
PatternDecision
Fields:
state
primary
primary_family
secondary
special
follow
combination
confidence
precedence_source
source
evidence_ids
warnings
Conceptual example:
{
  "state": "resolved",
  "primary": "zheng_guan",
  "primary_family": "standard",
  "secondary": [
    "zheng_yin"
  ],
  "special": null,
  "follow": null,
  "combination": null,
  "confidence": 0.92,
  "precedence_source": "pattern_engine",
  "source": "canonical_pattern_engine",
  "evidence_ids": [
    "E-MC-PATTERN-001"
  ],
  "warnings": []
}
20. PATTERN CONFIDENCE
Pattern confidence:
0.0 .. 1.0
MC-01 must consume upstream confidence where available.
MC-01 MUST NOT automatically convert:
pattern_confidence = 0.65
into:
pattern_confidence = 1.0
simply because normalization succeeded.
21. CONFIDENCE BANDS
Suggested interpretation:
0.90–1.00 very_high
0.75–0.89 high
0.60–0.74 medium
0.40–0.59 low
0.00–0.39 very_low
These bands are descriptive only.
They do not change upstream confidence.
22. LOW CONFIDENCE HANDLING
If pattern confidence is low:
confidence < threshold
MC-01 may continue structural analysis,
but downstream modules must inherit uncertainty.
Example:
pattern confidence = 0.48

purity result = 82
must not produce:
overall confidence = 0.95
without justification.
23. UNRESOLVED PATTERN
Valid unresolved result:
{
  "state": "unresolved",
  "primary": null,
  "primary_family": "unresolved",
  "secondary": [],
  "confidence": 0.31
}
Downstream behavior:
Purity → unresolved or partial
Pattern Strength → unresolved or partial
Integrity → unresolved
Grade → UNRESOLVED
unless the relevant downstream stage explicitly supports pattern-independent analysis.
24. PARTIALLY RESOLVED PATTERN
Example:
Pattern family known
but exact primary pattern unresolved
Possible result:
{
  "state": "partially_resolved",
  "primary": null,
  "primary_family": "standard",
  "secondary": [
    "zheng_guan",
    "qi_sha"
  ]
}
This may occur when Quan/Sát structure remains genuinely mixed.
MC-01 must preserve ambiguity.
25. CONFLICTING PATTERN EVIDENCE
Pattern conflicts can occur when upstream evidence supports multiple incompatible candidates.
Example:
Candidate A = Chính Quan
Candidate B = Thất Sát
without sufficient precedence resolution.
The result should be:
state = conflicting_evidence
not arbitrary selection.
26. CONFLICT RECORD
Recommended structure:
PatternConflict
Fields:
conflict_id
candidate_patterns
conflict_type
severity
evidence_ids
resolution_state
Possible conflict types:
primary_competition
special_vs_standard
follow_vs_standard
transformation_uncertain
mixed_guan_sha
mixed_wealth
other
27. QUAN / SÁT MIXING
Quan/Sát mixed structure requires special treatment.
It must not be simplified into:
Quan exists
or:
Sát exists
MC-01 should preserve evidence such as:
zheng_guan present
qi_sha present
both structurally meaningful
Later Purity and Damage stages determine whether this constitutes:
mixed_guan_sha
and how serious the mixing is.
Pattern Recognition only records identity/conflict.
28. WEALTH MIXING
Similarly:
zheng_cai
+
pian_cai
does not automatically mean:
impure
Pattern Recognition records the coexistence.
Purity decides whether the mixture structurally damages purity.
29. YIN MIXING
The same principle applies to:
zheng_yin
+
pian_yin
Do not classify damage at Pattern Recognition stage.
30. OUTPUT MIXING
Likewise:
shi_shen
+
shang_guan
can be structurally meaningful.
Recognition records.
Purity/Damage interpret later.
31. MAIN VS DOMINANT
Important distinction:
main_pattern
is not necessarily:
most abundant Ten God
and not necessarily:
highest numerical Ten-God count
Pattern identity must follow structural rules.
MC-01 must never infer main pattern from simple counts.
32. MAIN VS USEFUL GOD
Pattern identity and Useful God are independent.
Example:
main_pattern = zheng_guan
useful_god = fire
The pattern is not renamed:
fire pattern
Useful God may support or conflict with pattern needs,
but it does not replace pattern identity.
33. MAIN VS DAY MASTER STRENGTH
Pattern identity must not be rewritten based solely on:
Day Master strong
or:
Day Master weak
Strength is contextual evidence for whether a pattern can function.
It is not itself a pattern label.
34. PATTERN STABILITY
Natal pattern identity is stable.
It MUST NOT change because:
- current year changes
- current Đại Vận changes
- current career changes
- current income changes
- relationship status changes
Luck cycles may activate or suppress the expression of the natal pattern,
but do not rewrite natal pattern identity.
35. PATTERN EVIDENCE
Each resolved pattern should reference upstream evidence.
Possible evidence sources:
month_command
visible_ten_god
hidden_ten_god
root
season
stem_exposure
branch_structure
pattern_rule
special_condition
follow_condition
transformation_condition
MC-01 stores evidence references,
not duplicate calculations.
36. PATTERN SOURCE TRACE
Example trace:
TR-MC-001
stage = pattern
action = normalize_pattern
input = pattern.main_pattern = "zheng_guan"
output = PatternDecision.primary = "zheng_guan"

TR-MC-002
stage = pattern
action = preserve_pattern_confidence
input = 0.92
output = 0.92
Pattern Recognition must be auditable even if it appears simple.
37. INVALID PATTERN INPUT
Examples of invalid input:
unknown unsupported pattern ID
main_pattern = multiple scalar values
confidence > 1
follow pattern stored as standard pattern
contradictory resolved/unresolved flags
MC-01 should return:
status = invalid_input
or raise a typed validation failure according to runtime contract.
38. UNKNOWN PATTERN ID
If upstream introduces an unknown ID:
pattern = "new_future_pattern"
MC-01 MUST NOT silently map it to:
special_combination
Preferred behavior:
state = unresolved
warning = unsupported_pattern_id
until schema support is added.
39. SPECIAL PATTERN PRECEDENCE
Special structures require explicit metadata.
Recommended upstream fields:
special_pattern
special_pattern_valid
special_pattern_priority
special_pattern_confidence
If unavailable, MC-01 must not infer precedence from pattern name alone.
40. FOLLOW PATTERN VALIDATION
For a follow pattern:
cong_cai
cong_guan_sha
cong_er
cong_wang
MC-01 should expect upstream evidence indicating that the follow condition has already been validated.
Example:
follow_condition_passed = true
If upstream only reports:
candidate_follow_pattern
MC-01 must not promote it to resolved.
41. TRANSFORMATION VALIDATION
For:
hua_qi
MC-01 should expect explicit upstream confirmation that transformation requirements are satisfied.
Merely having:
heavenly_stem_combination = true
is insufficient.
42. PATTERN CANDIDATES
Optional future model:
PatternCandidate
Fields:
pattern_id
family
score
confidence
evidence_ids
rejection_reasons
This is useful when Pattern Engine exposes ranked candidates.
MC-01 may preserve the candidates for audit,
but should still consume the upstream chosen primary pattern.
43. REJECTED PATTERN CANDIDATES
Rejected candidates can be valuable evidence.
Example:
cong_cai rejected because Day Master retains meaningful root
This may later help explain why the chart is not a follow pattern.
MC-01 should preserve such rejection evidence when available.
44. PATTERN REJECTION MODEL
Optional:
PatternRejection
Fields:
pattern_id
reason_codes
evidence_ids
confidence
Example:
{
  "pattern_id": "cong_cai",
  "reason_codes": [
    "day_master_has_root",
    "support_not_fully_removed"
  ]
}
45. PATTERN NORMALIZATION TABLE
Initial table:
Canonical ID	Family	Vietnamese Display
zheng_guan	standard	Chính Quan cách
qi_sha	standard	Thất Sát cách
zheng_cai	standard	Chính Tài cách
pian_cai	standard	Thiên Tài cách
zheng_yin	standard	Chính Ấn cách
pian_yin	standard	Thiên Ấn cách
shi_shen	standard	Thực Thần cách
shang_guan	standard	Thương Quan cách
jian_lu	root_prosperity	Kiến Lộc cách
yang_ren	root_prosperity	Dương Nhẫn cách
cong_cai	follow	Tòng Tài cách
cong_guan_sha	follow	Tòng Quan Sát cách
cong_er	follow	Tòng Nhi cách
cong_wang	follow	Tòng Vượng cách
hua_qi	transformation	Hóa Khí cách
special_combination	special	Đặc cách / Tổ hợp đặc biệt
unresolved	unresolved	Chưa đủ căn cứ xác định


Display wording may be refined later.
Canonical IDs must remain stable.
46. LEGACY ALIAS POLICY
Legacy aliases may be accepted only in the input adapter.
Example:
chinh_quan
chinhquan
zhengguan
normalize to:
zheng_guan
The canonical result must never emit legacy aliases.
47. SOURCE VERSIONING
PatternDecision should preserve:
source_schema_version
source_ruleset_version
when available.
This is important because changes in Pattern Engine rules may alter pattern identity in future releases.
48. PATTERN ENGINE MIGRATION
If Pattern Engine changes schema:
v1 → v2
MC-01 should use an adapter layer.
Do not rewrite all downstream MC-01 stages to read multiple upstream schemas.
Canonical flow:
Pattern Engine v1
        ↓
Adapter
        ↓

Pattern Engine v2
        ↓
Adapter
        ↓

PatternInputContext
        ↓
MC-01
49. PATTERN DECISION INVARIANTS
P-01
Resolved primary pattern must have a valid canonical ID.
P-02
Resolved primary pattern must have a family.
P-03
primary = null cannot coexist with:
state = resolved
P-04
Follow pattern must map to family:
follow
P-05
Transformation pattern must map to family:
transformation
P-06
MC-01 may normalize pattern naming,
but cannot change pattern semantics.
P-07
Pattern confidence cannot be increased without explicit derived-confidence justification.
P-08
Natal pattern identity must not depend on luck-cycle input.
P-09
Unknown pattern IDs must not be silently classified.
P-10
Pattern Recognition must not perform Purity or Damage scoring.
50. PATTERN RECOGNITION VS PURITY
Strict boundary:
Pattern Recognition asks:
What structural pattern exists?
Purity asks:
How cleanly is that pattern expressed?
Example:
primary pattern = Chính Quan
Recognition stops there.
It does NOT decide:
Quan Sát hỗn tạp
→ purity -20
That belongs to 03_PATTERN_PURITY.md.
51. PATTERN RECOGNITION VS PATTERN STRENGTH
Recognition:
Chính Quan cách
Pattern Strength:
Quan có lực hay không?
These must remain separate.
A chart may have:
Chính Quan cách
but:
pattern_strength = weak
52. PATTERN RECOGNITION VS DAMAGE
Recognition records:
primary = zheng_guan
secondary = shang_guan
Damage later evaluates whether:
Thương Quan kiến Quan
is structurally active and damaging.
Do not classify it prematurely.
53. PATTERN RECOGNITION VS GRADE
There is no direct mapping:
zheng_guan → A
pian_cai → B
qi_sha → C
This is strictly forbidden.
Pattern identity is categorical.
Grade is structural.
54. PATTERN FAMILY AND DOWNSTREAM POLICY
Pattern family may determine which downstream rule families apply.
Example:
standard
→ standard purity rules

follow
→ follow-structure purity rules

transformation
→ transformation integrity rules
This is allowed.
But the family itself does not determine grade.
55. FOLLOW STRUCTURE SPECIAL RULE PATH
Follow structures should eventually use a dedicated evaluation branch:
Follow Pattern
    ↓
Follow Validity
    ↓
Follow Purity
    ↓
Counter-force Detection
    ↓
Damage / Rescue
    ↓
Integrity
Do not force follow structures through all ordinary Day Master balance assumptions.
56. TRANSFORMATION STRUCTURE SPECIAL RULE PATH
Transformation structures should similarly support:
Transformation Validity
    ↓
Transformation Completion
    ↓
Residual Original Qi
    ↓
Disruptive Forces
    ↓
Integrity
Exact rules belong to later documents.
57. ROOT PROSPERITY STRUCTURE PATH
For:
jian_lu
yang_ren
later MC-01 stages must consider that strong root/self-force is part of the pattern itself.
It must not automatically be treated as excessive support.
58. MIXED STRUCTURE POLICY
Some charts are genuinely mixed.
MC-01 must support:
primary
+
secondary
+
conflict
without forcing a false “pure single pattern” identity.
Example:
primary = zheng_guan
secondary = qi_sha
conflict = mixed_guan_sha
This is a valid structural state.
59. UNRESOLVED IS A VALID RESULT
The engine must treat:
unresolved
as a legitimate conclusion.
It is better to return:
Chưa đủ căn cứ xác định cách cục chính.
than to choose a pattern merely to fill the UI.
60. CUSTOMER DISPLAY POLICY
Customer display may show:
Mệnh cục chính:
Chính Quan cách
and optionally:
Cấu trúc phụ:
Chính Ấn
If unresolved:
Mệnh cục:
Chưa đủ căn cứ xác định chắc chắn
Do not expose internal ambiguity as fake certainty.
61. EXPLANATION SUPPORT
PatternDecision should allow later explanation such as:
"Chính Quan được xác định là cấu trúc chính theo Pattern Engine.
Chính Ấn xuất hiện như cấu trúc hỗ trợ.
Không phát hiện đặc cách hoặc tòng cách có độ tin cậy đủ cao."
The composer may generate this from structured facts.
62. GOLDEN DATASET REQUIREMENTS
Pattern Recognition golden cases must cover:
pure standard pattern
standard + secondary
mixed Quan/Sát
root prosperity
follow pattern
failed follow candidate
transformation pattern
failed transformation candidate
special structure
unresolved
low confidence
unknown ID
63. GOLDEN CASE FORMAT
Example:
{
  "case_id": "MC-PATTERN-001",

  "input": {
    "main_pattern": "zheng_guan",
    "secondary_patterns": [
      "zheng_yin"
    ],
    "confidence": 0.92
  },

  "expected": {
    "state": "resolved",
    "primary": "zheng_guan",
    "primary_family": "standard",
    "secondary": [
      "zheng_yin"
    ],
    "confidence": 0.92
  }
}
64. NEGATIVE GOLDEN CASE
Example:
{
  "case_id": "MC-PATTERN-NEG-001",

  "input": {
    "main_pattern": null,
    "candidate_patterns": [
      "zheng_guan",
      "qi_sha"
    ],
    "confidence": 0.45
  },

  "forbidden": {
    "state": "resolved"
  }
}
The engine must not invent a primary.
65. ACCEPTED ALTERNATIVES
Where expert tradition legitimately permits multiple interpretations,
golden cases may define accepted alternatives.
Example:
{
  "accepted_primary": [
    "zheng_guan",
    "qi_sha"
  ],
  "required_state": "conflicting_evidence"
}
This is preferable to forcing artificial certainty.
66. VALIDATION CHECKLIST
Pattern Recognition passes only if:
- canonical IDs are stable
- aliases normalize correctly
- unknown IDs are rejected safely
- unresolved state is preserved
- confidence is preserved
- family mapping is deterministic
- no luck-cycle dependency exists
- no customer biography dependency exists
- Pattern Engine remains owner of pattern identity
- no Purity logic leaks into this stage
- no Grade logic leaks into this stage
- trace is generated
- serialization order is deterministic
67. IMPLEMENTATION BOUNDARY
This document does NOT yet define:
- purity scoring
- pattern strength scoring
- damage scoring
- rescue scoring
- integrity formula
- grade thresholds
- achievement scores
Those belong to later MC-01 documents.
68. INITIAL IMPLEMENTATION COMPONENTS
Recommended future modules:
engines/mingju/
├── pattern_adapter.py
├── pattern_normalizer.py
├── pattern_decision.py
└── pattern_types.py
Responsibilities:
pattern_adapter
→ read upstream contract

pattern_normalizer
→ normalize IDs

pattern_decision
→ build PatternDecision

pattern_types
→ enums / mappings
Do not implement until contracts are approved.
69. ARCHITECTURAL DECISION
Pattern Recognition is a normalization and ownership-boundary stage.
Canonical rule:
MC-01 MUST TRUST,
VALIDATE,
NORMALIZE,
AND EXPLAIN
PATTERN ENGINE OUTPUT.

MC-01 MUST NOT SECRETLY REPLACE IT.
70. FINAL INFERENCE BOUNDARY
Pattern Engine
        ↓
"What pattern is present?"

MC-01 Pattern Recognition
        ↓
"Normalize and preserve that structural identity"

MC-01 Purity
        ↓
"How clean is it?"

MC-01 Pattern Strength
        ↓
"How much structural power does it have?"

MC-01 Damage / Rescue
        ↓
"Is it broken and can it recover?"

MC-01 Integrity
        ↓
"Does the structure hold together?"

MC-01 Grade
        ↓
"What is the structural quality?"
This boundary is mandatory.
71. FREEZE TARGET
Before proceeding to Purity, freeze:
canonical pattern IDs
pattern families
normalization policy
precedence ownership
unresolved handling
confidence handling
follow-pattern handling
transformation-pattern handling
PatternDecision shape
72. NEXT DOCUMENT
Next:
03_PATTERN_PURITY.md
Purpose:
- define what “thuần” means structurally
- distinguish pure vs mixed pattern
- define positive purity factors
- define negative purity factors
- define Quan/Sát mixing
- define Tài mixing
- define Ấn mixing
- define Thực/Thương mixing
- define root consistency
- define stem exposure
- define hidden interference
- establish Purity scoring without confusing Purity with Pattern Strength

Có một điểm rất quan trọng chúng ta vừa khóa ở file này: **Pattern Recognition không phải nơi đánh giá cách tốt hay xấu**. Nó chỉ trả lời đúng câu hỏi **“cách gì?”**. Các câu hỏi **“thuần không, mạnh không, có phá không, thành cách hay không”** phải để các tầng sau xử lý.

Bước tiếp theo nên làm luôn **`03_PATTERN_PURITY.md`**. Đây sẽ là file bắt đầu đi vào logic chuyên môn thật sự, đặc biệt là các trường hợp **Quan Sát hỗn tạp, Tài hỗn, Ấn hỗn, Thực–Thương cùng hiện, lộ can, có căn, tạp khí**.