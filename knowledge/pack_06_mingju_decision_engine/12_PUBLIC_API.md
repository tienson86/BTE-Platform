# MC-01 — PUBLIC API

**Project:** BTE-Platform  
**Pack:** `pack_06_mingju_decision_engine`  
**Module:** MC-01  
**Document:** `12_PUBLIC_API.md`  
**Status:** DESIGN DRAFT  
**Schema target:** `bte.mingju.decision.v1`  
**Composer target:** `bte.mingju.composer.v1`

---

# 1. PURPOSE

This document defines the public runtime API contract for MC-01 — Mệnh Cục Decision Engine.

It defines:

- canonical entry points
- canonical input context
- canonical result
- composer entry point
- versioning
- status behavior
- partial/unresolved handling
- error behavior
- orchestration boundaries
- frontend/report ownership rules
- serialization requirements
- deterministic runtime expectations

The public API must expose one stable interface for all downstream consumers.

---

# 2. CORE PRINCIPLE

MC-01 must have one canonical public entry point.

Canonical architecture:

```text
Upstream Engines
      ↓
MingJuContext Adapter
      ↓
MC-01 Decision Engine
      ↓
MingJuDecisionResult
      ↓
Decision Composer
      ↓
MingJuComposedDecision
      ↓
Portal / Report / PDF / DOCX

Downstream consumers MUST NOT reconstruct Mệnh Cục logic independently.
3. OWNERSHIP
Upstream engines own
Calendar truth
BaZi truth
Five Elements
Ten Gods
Day Master Strength
Temperature / Điều Hậu
Pattern identity
Useful God
Relations
MC-01 owns
Pattern normalization
Purity
Pattern Strength
Support synthesis
Damage
Rescue
Structural Integrity
Grade
Achievement Profile
Wealth Profile
Career Profile
Decision trace
Decision Composer owns
Headline
Executive summary
Strengths
Risks
Conditions
Customer-facing wording
4. PUBLIC ENTRY POINTS
Recommended canonical functions:
build_mingju_context(...)
analyze_mingju(...)
compose_mingju_decision(...)
Preferred external usage:
context = build_mingju_context(...)
result = analyze_mingju(context)
composed = compose_mingju_decision(result)
5. PRIMARY PUBLIC FUNCTION
Recommended signature:
def analyze_mingju(
    context: MingJuContext,
    *,
    ruleset_version: str | None = None,
) -> MingJuDecisionResult:
    ...
This is the canonical MC-01 calculation entry point.
6. COMPOSER PUBLIC FUNCTION
Recommended:
def compose_mingju_decision(
    result: MingJuDecisionResult,
    *,
    locale: str = "vi",
    mode: MingJuComposerMode = MingJuComposerMode.COMMERCIAL,
    composer_version: str | None = None,
) -> MingJuComposedDecision:
    ...
Composer must never receive raw BaZi facts as a substitute for MingJuDecisionResult.
7. CONTEXT BUILDER
Recommended:
def build_mingju_context(
    *,
    chart: object,
    five_elements: object,
    ten_gods: object,
    strength: object,
    temperature: object,
    pattern: object,
    useful_god: object,
    relations: object | None = None,
    metadata: object | None = None,
) -> MingJuContext:
    ...
The builder normalizes upstream contracts.
It does NOT perform MC-01 decision logic.
8. WHY A CONTEXT BUILDER IS REQUIRED
Without a normalized context, MC-01 could become tightly coupled to many upstream payload shapes.
Bad:
purity.py reads pattern engine directly
damage.py reads portal adapter
wealth.py reads report payload
career.py reads frontend model
Correct:
all upstream sources
      ↓
MingJuContext
      ↓
all MC-01 stages
9. MINGJU CONTEXT
Canonical conceptual model:
class MingJuContext:
    chart: ChartContext
    five_elements: FiveElementsContext
    ten_gods: TenGodsContext
    strength: StrengthContext
    temperature: TemperatureContext
    pattern: PatternInputContext
    useful_god: UsefulGodContext
    relations: RelationsContext | None
    metadata: MingJuContextMetadata
10. CONTEXT METADATA
Recommended:
class MingJuContextMetadata:
    analysis_id: str | None
    source_versions: dict[str, str]
    input_completeness: float
    hour_pillar_available: bool
    warnings: list[str]
Metadata is informational.
It must not become a hidden inference source.
11. CONTEXT VERSIONING
Recommended:
bte.mingju.context.v1
Expose:
context_schema_version
This allows adapter changes without breaking engine semantics.
12. CONTEXT NORMALIZATION
Context builder may normalize:
aliases
enum names
nullability
field shapes
ordering
source version metadata
It MUST NOT:
recalculate upstream truth
change pattern
change Day Master strength
change Useful God
change temperature state
invent relations
13. REQUIRED INPUT DOMAINS
Minimum required inputs for structural Phase 1:
chart
ten_gods
strength
pattern
Recommended full input:
chart
five_elements
ten_gods
strength
temperature
pattern
useful_god
relations
14. REQUIRED VS OPTIONAL INPUTS
Recommended policy:
Required
chart.day_master
chart.four_pillars
pattern
strength
ten_gods
Optional but strongly recommended
temperature
useful_god
relations
five_elements
Missing optional inputs may produce:
partial
partially_resolved
lower confidence
warnings
15. MISSING HOUR PILLAR
The public API must support:
hour_pillar = null
if the upstream chart contract permits unknown birth hour.
This should NOT automatically produce:
invalid_input
Instead:
status = partial
or a lower-confidence result when analysis can proceed.
16. INVALID INPUT
Examples:
missing Day Master
malformed pillar
unsupported pattern ID
invalid Strength enum
confidence outside allowed range
contradictory canonical source states
Expected result:
status = invalid_input
The API should not silently repair semantic errors.
17. ROOT RESULT
Canonical public result:
class MingJuDecisionResult:
    schema_version: str
    ruleset_version: str
    context_schema_version: str
    status: MingJuDecisionStatus

    pattern: PatternDecision
    purity: PatternPurityResult
    pattern_strength: PatternStrengthResult

    support: PatternSupportResult
    damage: PatternDamageResult
    rescue: PatternRescueResult

    useful_god_compatibility: UsefulGodCompatibilityResult
    climate_compatibility: ClimateCompatibilityResult

    integrity: StructuralIntegrityResult
    grade: PatternGradeResult

    achievement: AchievementProfile
    wealth: WealthProfile
    career: CareerProfile

    confidence: ConfidenceResult
    warnings: list[MingJuWarning]
    trace: list[MingJuTraceEvent]
18. ROOT RESULT STATUS
Allowed:
complete
partial
unresolved
insufficient_evidence
invalid_input
19. COMPLETE
Use when:
all mandatory stages completed
core structural decision resolved
Downstream optional dimensions may still have lower confidence,
but result is materially complete.
20. PARTIAL
Use when:
core Mệnh Cục structure resolved
but one or more non-critical stages are incomplete
Examples:
Career partially unresolved
Useful-God compatibility unavailable
missing hour pillar
21. UNRESOLVED
Use when:
valid input exists
but the core structural decision cannot be resolved
Examples:
primary pattern unresolved
follow/transformation conflict unresolved
critical Damage/Rescue relation unresolved
22. INSUFFICIENT EVIDENCE
Use when required analytical evidence is missing.
Example:
Pattern Engine output absent
Ten Gods unavailable
Different from:
valid evidence but conflicting
which is usually unresolved.
23. INVALID INPUT
Use only for malformed or contract-invalid data.
This is not the same as a difficult chart.
24. PARTIAL RESULT POLICY
A partial result should still expose resolved stages.
Example:
{
  "status": "partial",

  "pattern": {
    "state": "resolved",
    "primary": "zheng_guan"
  },

  "integrity": {
    "state": "resolved"
  },

  "career": {
    "state": "partially_resolved"
  }
}
Do not discard valid work just because one downstream model is incomplete.
25. UNRESOLVED CORE POLICY
If core structural Integrity is unresolved:
grade = UNRESOLVED
Achievement / Wealth / Career should generally be:
unresolved
or clearly low-confidence partial results.
They MUST NOT appear confidently resolved.
26. STAGE RESULT POLICY
Each major stage should expose:
state
confidence
evidence_ids
This allows downstream callers to understand partiality.
27. PUBLIC API DOES NOT THROW FOR NORMAL UNCERTAINTY
Normal analytical uncertainty should be returned as structured state.
Do not throw exceptions for:
unresolved pattern
missing optional relation
low confidence
conflicting evidence
Exceptions are for technical/runtime failure,
not domain uncertainty.
28. TECHNICAL EXCEPTIONS
Potential typed exceptions:
MingJuContractError
MingJuVersionError
MingJuRuleExecutionError
MingJuSerializationError
These represent software failures.
29. DOMAIN UNCERTAINTY IS DATA
Examples:
pattern unresolved
damage relation uncertain
grade unresolved
These belong inside MingJuDecisionResult.
30. RULESET VERSION
Canonical initial version:
bte.mingju.rules.v1
analyze_mingju() should resolve ruleset deterministically.
No implicit random or environment-dependent rule selection.
31. DEFAULT RULESET
Recommended:
DEFAULT_MINGJU_RULESET = "bte.mingju.rules.v1"
The default version must be explicit and testable.
32. UNSUPPORTED RULESET
If requested:
bte.mingju.rules.v999
and unavailable:
Raise or return a typed version error.
Do not silently fall back to another ruleset.
33. SCHEMA VERSION
Initial result schema:
bte.mingju.decision.v1
This must appear in every serialized result.
34. COMPOSER OUTPUT MODEL
Canonical conceptual object:
class MingJuComposedDecision:
    composer_version: str
    message_catalog_version: str
    locale: str
    mode: str
    state: AnalysisState

    headline: ComposedSection
    executive_summary: list[ComposedSection]
    structural_summary: list[ComposedSection]

    strengths: list[ComposedSection]
    risks: list[ComposedSection]
    conditions_for_success: list[ComposedSection]
    conditions_to_avoid: list[ComposedSection]

    achievement_summary: list[ComposedSection]
    wealth_summary: list[ComposedSection]
    career_summary: list[ComposedSection]

    technical_summary: list[ComposedSection]
    confidence_note: ComposedSection | None
35. COMPOSER MODE ENUM
Recommended:
dashboard
commercial
technical
report
No consumer should create its own independent composition mode.
36. PUBLIC ORCHESTRATOR CONTRACT
Recommended orchestration:
def run_mingju_stage(
    analysis: CanonicalAnalysisResult,
) -> MingJuDecisionResult:
    context = build_mingju_context(...)
    return analyze_mingju(context)
Then:
decision = run_mingju_stage(analysis)
analysis.mingju = decision
37. ORCHESTRATOR OWNERSHIP
Orchestrator owns:
when MC-01 runs
which upstream results are passed
where result is attached
MC-01 owns:
how Mệnh Cục is inferred
38. ORCHESTRATOR MUST NOT REWRITE RESULT
Forbidden:
result = analyze_mingju(...)
if result.grade == "B":
    result.grade = "A"
No orchestration-level semantic patching.
39. RECOMMENDED PIPELINE POSITION
Recommended:
Calendar
↓
BaZi
↓
Five Elements
↓
Ten Gods
↓
Strength
↓
Temperature
↓
Pattern
↓
Useful God
↓
Relations
↓
MC-01
↓
Interpretation / Consulting
↓
Report
Exact runtime integration may depend on current BTE pipeline.
40. MC-01 SHOULD NOT RUN BEFORE REQUIRED FACTS
Do not run MC-01 before:
Pattern
Strength
Ten Gods
are available.
Otherwise only insufficient_evidence is valid.
41. CANONICAL ANALYSIS ATTACHMENT
Recommended field:
analysis.mingju
or:
analysis.mingju_decision
Choose one stable path and freeze it.
Preferred:
mingju
for concise public contract.
42. PROPOSED CANONICAL RESULT SHAPE
Example:
{
  "analysis_id": "CASE-0001",

  "mingju": {
    "schema_version": "bte.mingju.decision.v1",
    "ruleset_version": "bte.mingju.rules.v1",
    "status": "complete",

    "pattern": {},
    "purity": {},
    "pattern_strength": {},
    "support": {},
    "damage": {},
    "rescue": {},
    "integrity": {},
    "grade": {},
    "achievement": {},
    "wealth": {},
    "career": {},
    "confidence": {},
    "warnings": [],
    "trace": []
  }
}
43. COMPOSED RESULT ATTACHMENT
Recommended optional field:
analysis.mingju_composed
or generate composition on demand.
Preferred architecture:
canonical structured result stored
composer output generated from result
Do not store only prose.
44. STRUCTURED RESULT IS PRIMARY TRUTH
Storage priority:
MingJuDecisionResult
must be considered canonical.
Composed prose may be regenerated.
45. COMPOSER OUTPUT MAY BE CACHEABLE
Because Composer is deterministic:
same result
+ same composer version
+ same message catalog
+ same locale
+ same mode
=
same output
Therefore composition may be cached safely.
46. FRONTEND CONTRACT
Frontend may display:
mingju.pattern
mingju.purity
mingju.pattern_strength
mingju.damage
mingju.rescue
mingju.integrity
mingju.grade
mingju.achievement
mingju.wealth
mingju.career
But frontend MUST NOT calculate:
Grade
Integrity
wealth summary
career summary
independently.
47. FRONTEND PRESENTATION ONLY
Allowed frontend logic:
format percentage
map enum to Vietnamese label
show/hide optional sections
responsive layout
visual bars/stars
Forbidden frontend logic:
if authority > 70 and grade == A → "làm quan"
That belongs to Composer or engine.
48. REPORT ENGINE CONTRACT
Report Engine should consume:
mingju
mingju_composed
when available.
It MUST NOT recalculate Mệnh Cục logic from:
ten_gods
strength
pattern
49. PDF/DOCX PARITY
PDF and DOCX must use the same:
MingJuDecisionResult
MingJuComposedDecision
No report-specific re-interpretation.
50. CONSULTING ENGINE CONTRACT
Commercial Consulting may consume MC-01 outputs as evidence.
Example:
wealth_retention = low
career.autonomy_need = high
But Consulting must not overwrite canonical MC-01 truth.
51. INTERPRETATION ENGINE CONTRACT
Existing Interpretation Engine may consume:
MingJuDecisionResult
as a high-level structural source.
Recommended direction:
MC-01 structured truth
→ Interpretation
rather than:
Interpretation guesses Mệnh Cục independently
52. PUBLIC READ API
Potential public serialization function:
def serialize_mingju_result(
    result: MingJuDecisionResult,
) -> dict:
    ...
Serialization must be deterministic.
53. PUBLIC COMPOSER SERIALIZATION
Recommended:
def serialize_mingju_composed(
    result: MingJuComposedDecision,
) -> dict:
    ...
54. SERIALIZATION RULES
Use:
stable English IDs
stable enum values
deterministic arrays
explicit null
version fields
bounded precision
Do not serialize:
Python object repr
non-deterministic sets
random IDs
localized enum identity
55. NULL POLICY
Canonical distinction:
null
means:
not computed / unresolved / unavailable
while:
0
means:
computed minimum
This distinction must survive serialization.
56. EMPTY COLLECTION POLICY
Example:
"damage": {
  "state": "resolved",
  "findings": []
}
means:
no meaningful Damage detected
But:
"damage": {
  "state": "unresolved",
  "findings": []
}
does NOT mean no Damage.
57. EVIDENCE REFERENCES
Public result should preserve evidence IDs.
Example:
"evidence_ids": [
  "E-MC-DMG-001"
]
This allows technical trace without duplicating all upstream payloads.
58. TRACE POLICY
Trace may be included fully in:
technical/admin payload
and optionally omitted or reduced in customer payload.
But canonical stored result should preserve trace.
59. TRACE SERIALIZATION
Recommended deterministic order:
sequence ASC
No sorting by display text.
60. PUBLIC CUSTOMER PAYLOAD
A reduced customer DTO MAY be introduced later.
Example:
MingJuCustomerView
But it must be derived from canonical result.
It must not become a second source of truth.
61. CUSTOMER VIEW EXAMPLE
Potential fields:
pattern_label
grade
integrity_label
purity_percent
pattern_strength_percent
damage_summary
rescue_summary
achievement_highlights
wealth_summary
career_summary
This is presentation-only.
62. INTERNAL TECHNICAL PAYLOAD
Technical/admin mode may expose:
rule IDs
evidence
trace
confidence factors
warnings
residual damage
Customer UI need not show all of this.
63. API RESPONSE VERSIONING
If exposed through HTTP API,
recommended wrapper:
{
  "version": "1",
  "data": {
    "mingju": {}
  }
}
But MC-01 schema version inside payload remains authoritative.
64. HTTP ENDPOINT — OPTIONAL FUTURE
If MC-01 ever receives a dedicated endpoint:
POST /api/v1/mingju/analyze
it should accept canonical upstream analysis or normalized context.
However BTE V1.0 should preferably run MC-01 inside the main analysis pipeline.
65. DO NOT CREATE A SECOND ANALYSIS PATH
Avoid architecture:
/api/v1/analyze
and separately:
/api/v1/mingju/analyze
with different logic.
If a dedicated endpoint exists,
it should call the same core analyze_mingju().
66. PUBLIC FUNCTION DETERMINISM
Given:
same MingJuContext
same ruleset version
must produce:
same MingJuDecisionResult
Byte-identical serialization is desirable where practical.
67. NO EXTERNAL I/O INSIDE CORE ENGINE
analyze_mingju() must not depend on:
web requests
database lookup
LLM
current date
customer profile service
random numbers
Core engine should be pure/deterministic where possible.
68. NO CURRENT-TIME DEPENDENCY
Natal MC-01 result must not change because execution happens in:
2026
2027
2030
Current time is irrelevant.
69. NO LUCK INPUT IN NATAL API
MingJuContext should NOT contain:
current_luck_cycle
current_year
for the natal structural result.
Future activation engine should use a separate API.
70. FUTURE ACTIVATION API
Possible future function:
def analyze_mingju_activation(
    natal: MingJuDecisionResult,
    luck_context: LuckActivationContext,
) -> MingJuActivationResult:
    ...
This must remain separate from natal MC-01.
71. NATAL RESULT IMMUTABILITY
Recommended practice:
MingJuDecisionResult
should be treated as immutable after creation.
Downstream modules should not mutate it.
72. COPY / ADAPT, DO NOT MUTATE
If UI or Report needs another shape:
canonical result
→ adapter/view model
not:
canonical result mutated for UI
73. API INPUT OWNERSHIP CHECK
Before building context,
validate that upstream modules own the source fields.
Examples:
Strength → Strength Engine
Pattern → Pattern Engine
Useful God → Useful God Engine
No duplicated ownership.
74. API WARNING MODEL
Warnings may include:
missing_hour_pillar
low_pattern_confidence
relation_data_incomplete
useful_god_unavailable
temperature_unavailable
special_pattern_rule_missing
75. WARNING DOES NOT ALWAYS CHANGE STATUS
Example:
missing_hour_pillar
may still allow:
status = complete
if all relevant structural stages remain sufficiently resolved.
Status logic should be rule-driven.
76. ERROR RESPONSE PRINCIPLE
If the core function is used behind HTTP,
technical failures should map cleanly.
Example:
400
→ invalid canonical input

409
→ unsupported/incompatible version

500
→ internal rule execution failure
Exact HTTP mapping belongs to integration layer.
77. DOMAIN UNRESOLVED SHOULD NOT RETURN HTTP 500
A difficult chart is not a server error.
Return:
200
status = unresolved
when the request is technically valid.
78. API CONTRACT INVARIANT
A technically valid chart with unresolved Mệnh Cục must still serialize correctly.
79. VERSION COMPATIBILITY
Context adapter should verify compatibility between upstream versions.
Example:
Pattern Engine v2
Strength Engine v1
may be compatible.
But if semantic incompatibility is known,
MC-01 must reject explicitly.
80. SOURCE VERSION MAP
Recommended:
{
  "source_versions": {
    "bazi": "bte.bazi.v2",
    "strength": "bte.strength.v1",
    "pattern": "bte.pattern.v2",
    "useful_god": "bte.useful_god.v1"
  }
}
This supports audits.
81. VALUE HASH
Optional technical metadata:
source_hash
may allow:
input → result
audit without duplicating full input.
82. RESULT HASH
Future:
decision_hash
could support snapshot verification.
If implemented, hashing must use normalized deterministic serialization.
83. IDEMPOTENCY
Calling:
analyze_mingju(context)
multiple times must not create different IDs or ordering.
Avoid random UUIDs in result.
84. ID GENERATION
Evidence/findings IDs should be deterministic where possible.
Example source:
rule_id + target + evidence signature
rather than random UUID.
Exact scheme may be defined during implementation.
85. THREAD SAFETY
Core rule execution should avoid shared mutable global state.
Ruleset registries may be read-only after initialization.
86. CACHE SAFETY
Because result is deterministic,
cache key may conceptually be:
normalized_context_hash
+
ruleset_version
Composer cache key:
decision_hash
+
composer_version
+
message_catalog_version
+
locale
+
mode
87. PERFORMANCE TARGET
MC-01 should operate entirely in-memory from provided context.
No external network/database dependencies.
Performance target can be finalized later.
Correctness and explainability have priority over micro-optimization.
88. OBSERVABILITY
Runtime may log:
analysis_id
schema_version
ruleset_version
status
grade
integrity_state
execution_time
warning_count
Do not log sensitive customer biography unnecessarily.
89. DEBUG MODE
Optional debug output may expose:
matched_rule_ids
stage timings
evidence counts
deduplication decisions
This should not alter the result.
90. PUBLIC API UNIT TESTS
Must cover:
complete result
partial result
unresolved result
insufficient evidence
invalid input
unsupported ruleset
missing hour pillar
serialization determinism
composer determinism
91. CONTEXT ADAPTER TESTS
Test:
canonical upstream payload
legacy aliases
null optional fields
unknown pattern IDs
invalid Strength state
source-version preservation
92. ROOT RESULT TESTS
Verify required fields:
schema_version
ruleset_version
status
pattern
purity
pattern_strength
damage
rescue
integrity
grade
achievement
wealth
career
confidence
warnings
trace
93. COMPOSER API TESTS
Verify:
same result → same composition
mode differences only affect presentation depth
locale does not change analytical truth
unresolved result cannot generate resolved language
94. FRONTEND CONTRACT TESTS
Frontend adapter tests should ensure:
does not derive Grade
does not derive Integrity
does not derive wealth/career conclusion
Only maps canonical data.
95. REPORT CONTRACT TESTS
Report must use:
mingju
mingju_composed
and preserve parity with /result.
96. RUNTIME SNAPSHOT
Recommended snapshot should cover:
CASE-0001
plus multiple structural Golden Cases.
One chart is not enough.
97. API GOLDEN CASE
Example:
{
  "case_id": "MC-API-001",

  "expected": {
    "schema_version": "bte.mingju.decision.v1",
    "ruleset_version": "bte.mingju.rules.v1",
    "status": "complete"
  }
}
98. UNRESOLVED API GOLDEN CASE
{
  "case_id": "MC-API-UNRESOLVED-001",

  "expected": {
    "status": "unresolved",
    "grade.grade": "UNRESOLVED"
  }
}
99. INVALID INPUT TEST
Example:
Day Master = unsupported value
Expected:
invalid_input
or typed contract exception,
according to final runtime convention.
100. PUBLIC API INVARIANTS
API-01
analyze_mingju() is the canonical decision entry point.
API-02
All MC-01 stages consume normalized MingJuContext.
API-03
Frontend must not reproduce MC-01 inference.
API-04
Report must not reproduce MC-01 inference.
API-05
Composer cannot receive raw input as substitute for canonical result.
API-06
Unresolved domain state is not a runtime exception.
API-07
Natal MC-01 does not consume Luck data.
API-08
Result must expose schema and ruleset version.
API-09
Serialization must be deterministic.
API-10
Same context + same ruleset = same result.
API-11
Downstream modules must not mutate canonical result.
API-12
Structured result remains primary truth over prose.
101. FAILURE CONDITIONS
Public API implementation FAILS if it:
1. exposes multiple competing MC-01 calculation entry points
2. lets UI calculate Grade
3. lets Report calculate Mệnh Cục independently
4. passes raw Pattern/Ten Gods directly to Composer for new inference
5. hides unresolved states
6. converts analytical uncertainty into exceptions
7. silently changes ruleset
8. uses luck/current-year data in natal API
9. uses biography
10. returns non-deterministic ordering
11. mutates canonical upstream data
12. stores only prose without structured result
13. allows version mismatch silently
14. creates different dashboard/report truth
102. RECOMMENDED PYTHON MODULE STRUCTURE
Future implementation:
engines/
└── mingju/
    ├── __init__.py
    ├── api.py
    ├── models.py
    ├── context.py
    ├── adapters.py
    ├── engine.py
    ├── composer.py
    ├── serialization.py
    ├── versions.py
    └── rules/
103. api.py
Recommended exports:
build_mingju_context
analyze_mingju
compose_mingju_decision
serialize_mingju_result
serialize_mingju_composed
This is the only intended public import surface.
104. INTERNAL MODULES
Downstream code SHOULD NOT import:
purity.py
damage.py
rescue.py
grade.py
wealth.py
career.py
directly.
Those are internal implementation details.
105. PUBLIC EXPORT POLICY
Recommended:
from engines.mingju.api import (
    analyze_mingju,
    build_mingju_context,
    compose_mingju_decision,
)
Not:
from engines.mingju.damage import ...
outside MC-01.
106. ORCHESTRATOR INTEGRATION EXAMPLE
Conceptual:
context = build_mingju_context(
    chart=analysis.bazi,
    five_elements=analysis.five_elements,
    ten_gods=analysis.ten_gods,
    strength=analysis.strength,
    temperature=analysis.temperature,
    pattern=analysis.pattern,
    useful_god=analysis.useful_god,
    relations=analysis.relations,
)

analysis.mingju = analyze_mingju(context)

analysis.mingju_composed = compose_mingju_decision(
    analysis.mingju,
    locale="vi",
    mode="commercial",
)
107. STORAGE RECOMMENDATION
Persist:
MingJuDecisionResult
with analysis result.
Optional:
MingJuComposedDecision
may also be persisted for exact report reproducibility.
108. RECOMPOSITION POLICY
If only wording changes:
same MingJuDecisionResult
+
new Composer version
→ recomposed narrative
No need to rerun analytical engine.
109. RULESET CHANGE POLICY
If MC-01 rules change:
new ruleset
→ rerun MingJuDecisionResult
Do not reuse old structural result under new ruleset label.
110. SCHEMA MIGRATION POLICY
Breaking output changes require:
bte.mingju.decision.v2
Do not silently reinterpret fields inside V1.
111. MESSAGE CATALOG CHANGE
Changing Vietnamese wording only:
bte.mingju.messages.vi.v1
→ v2
does not require decision schema change.
112. API ACCEPTANCE CHECKLIST
Before Public API freeze confirm:
one public engine entry point
one normalized context
one canonical result shape
one composer entry point
explicit versions
structured uncertainty
deterministic serialization
frontend presentation-only
report presentation-only
no luck leakage
no biography fitting
no duplicate engine logic
113. ARCHITECTURAL DECISION
Canonical rule:
MC-01 MUST EXPOSE ONE STRUCTURED, VERSIONED, DETERMINISTIC PUBLIC CONTRACT.

And:
ALL DOWNSTREAM PRESENTATION LAYERS MUST CONSUME THAT CONTRACT RATHER THAN RECONSTRUCTING MỆNH CỤC LOGIC.

114. FINAL PUBLIC FLOW
Canonical Upstream Facts
        ↓
MingJuContext
        ↓
analyze_mingju()
        ↓
MingJuDecisionResult
        ↓
compose_mingju_decision()
        ↓
MingJuComposedDecision
        ↓
Portal
Report
PDF
DOCX
Consulting
115. FREEZE TARGET
Before proceeding to Validation Rules, freeze:
MingJuContext boundary
public function names
MingJuDecisionResult ownership
MingJuComposedDecision ownership
status semantics
partial/unresolved behavior
version semantics
serialization policy
Orchestrator integration boundary
frontend boundary
report boundary
natal/luck boundary
determinism
immutability policy
116. NEXT DOCUMENT
Next:
13_VALIDATION_RULES.md
Purpose:
- define cross-model invariants
- validate references between Evidence / Damage / Rescue / Trace
- validate score ranges
- validate unresolved-state consistency
- validate Grade vs Integrity
- validate Wealth score direction
- validate Achievement / Career dependencies
- validate no double-counting metadata
- validate version compatibility
- validate deterministic ordering
- define fail-fast vs warning-only conditions

Sau file này, kiến trúc MC-01 đã có **đường chạy public khá rõ**: các engine cũ đưa facts vào `MingJuContext` → chỉ `analyze_mingju()` được quyền suy luận → trả một `MingJuDecisionResult` → Composer diễn đạt → UI/PDF/DOCX chỉ hiển thị.

Bước tiếp theo chúng ta làm `13_VALIDATION_RULES.md`. File đó sẽ rất quan trọng trước khi triển khai code, vì nó sẽ khóa các điều bất biến kiểu **Rescue bắt buộc phải trỏ đến Damage có thật, Grade không thể resolved khi Integrity unresolved, volatility không được hiểu ngược chiều, và frontend không được tự sinh kết luận**.