# PACK 07 — SYSTEM CONSISTENCY ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-21  
**Document:** `21_SYSTEM_CONSISTENCY_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `20_CANONICAL_RUNTIME_CONTRACT.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially `13_VALIDATION_RULES.md`  
**Schema target:** `bte.detailed_interpretation.system_consistency.v1`  
**Related schemas:**

- `bte.detailed_interpretation.runtime_contract.v1`
- `bte.detailed_interpretation.result.v1`
- `bte.detailed_interpretation.composer.v1`
- `bte.mingju.decision.v1`

This document defines the canonical **System Consistency Engine**.

Architecture listed `21_VALIDATION_RULES.md` for validation-layer tables. DI-20 pointed to that name for `RuntimeContractValidation` details. This Product Owner target authors `21_SYSTEM_CONSISTENCY_ENGINE.md` as the **global reasoning-continuity engine** across Truth → Meaning → Runtime → Presentation. Architecture and DI-01–DI-20 remain immutable.

This document does **not** invent a second runtime contract.

Stage-level validators in DI-01–DI-20 remain the owners of **local validity**. This engine owns **global consistency**.

This document does **not** implement runtime.

---

# 1. PURPOSE

Create the canonical:

```text
SYSTEM CONSISTENCY ENGINE
```

Purpose:

Validate consistency across the **entire** reasoning chain.

This engine validates:

```text
Truth
      ↓
Meaning
      ↓
Domains
      ↓
Temporal
      ↓
Optimization
      ↓
Narrative
      ↓
Runtime Contract
      ↓
Portal
      ↓
Export
      ↓
API
```

It does **not** validate one module in isolation.

A locally valid Ten Gods finding, a locally valid Domain, and a locally valid Narrative can still form a globally contradictory system. That contradiction is this engine’s subject.

---

# 2. CORE PRINCIPLE

Frozen:

```text
LOCAL VALIDITY
      ≠
GLOBAL CONSISTENCY.
```

Every stage may be individually correct, yet the final system may still contradict itself.

The engine validates:

```text
Reasoning continuity.
```

Continuity means:

```text
MC-01 structural IDs
      = Pack 07 meaning references
      = Domain natal states
      = Optimization consumed priorities
      = Narrative consumed priorities
      = CanonicalRuntimeResult assembled objects
      = Portal / PDF / DOCX / API / Consulting projections
```

Never:

```text
Many truths
Many Patterns
Many Grades
Many domain scores
Many optimization rankings
```

---

# 3. SCOPE

In scope:

1. ConsistencyGraph
2. Consistency layers L0–L4
3. Cross-stage and consumer consistency rules
4. ConsistencyResult / ConsistencyReport
5. ConsistencyError / ConsistencyWarning
6. Trace
7. Diagnostic ConsistencyScore
8. Pattern / Grade / domain / optimization / narrative / runtime / presentation rules
9. Golden consistency cases and negative proofs
10. Acceptance invariants SYS-01 … SYS-10

Out of scope:

```text
implementing the validator
rewriting MC-01 validation
replacing DI-01–DI-20 stage validators
PDF layout / CSS
Portal component design
LLM judging of “sounds consistent”
a second CanonicalRuntimeResult
```

Relation to architecture validation concept:

```text
Input Contract Validation          → stage / context (not this engine’s primary job)
Stage-Level Validation             → each DI module
Cross-Stage Validation             → THIS engine
Reference Integrity Validation     → THIS engine
Semantic Invariant Validation      → THIS engine
Serialization Validation           → L0 / L4 contract shape
Determinism Validation             → SYS-10 + L4
Portal / Report / PDF / DOCX       → L3 / L4
```

`RuntimeContractValidation` (DI-20) is the **contract-shape subset** of L0 and L4. This engine **consumes** it. It does not publish a competing contract.

---

# 4. NON-SCOPE

This engine MUST NOT:

1. Recalculate Pattern, Grade, Integrity, Achievement, Wealth Profile, or Career Profile
2. Reinterpret Ten Gods, Shen Sha, Domains, Temporal, Optimization, or Narrative
3. Invent missing findings to “make the chain look complete”
4. Collapse `unresolved` into a fake resolved state
5. Treat presentation order as analytical rank
6. Use biography or known life outcomes as consistency evidence
7. Expose ConsistencyScore to customers
8. Replace MC-01 `13_VALIDATION_RULES.md`
9. Mutate `CanonicalRuntimeResult` while reporting
10. Allow Portal, PDF, DOCX, API, or Consulting to become a second analysis path

Unknown `contract_version` / `schema_version` / `ruleset_version` fails closed (architecture). Domain uncertainty is not a consistency error.

---

# 5. CONSISTENCY GRAPH

Canonical:

```text
ConsistencyGraph
```

One graph per published `analysis_id`.

The graph is diagnostic. It does not become a second interpretation object.

## 5.1 Nodes

Required nodes:

```text
MC-01
Interpretation
Domains
Temporal
Optimization
Narrative
Runtime Contract
Portal
PDF
DOCX
API
```

Required consumer extensions (same analysis, not extra truths):

```text
Consulting
Export                          # CanonicalExportModel; PDF/DOCX/PPT/HTML projections
History                         # stored CanonicalRuntimeResult
```

Internal sub-nodes (owned by Interpretation / Domains; not parallel truths):

```text
EvidencePriority                # DI-07; consumed by Domains / Optimization / Narrative
DetailedAuthority               # DI-12
DetailedCareer                  # DI-13
DetailedWealth                  # DI-14
DetailedRelationship            # DI-15
DetailedLegacy                  # DI-16
DetailedVitality                # DI-17
```

Forbidden extra nodes:

```text
PortalPattern
PdfGrade
ApiWealthScore
ConsultingRewrite
```

## 5.2 Edges

```text
depends_on
references
supports
must_match
inherits
```

Meaning:

```text
depends_on     target must exist and be valid before source is judged
references     source cites target IDs; must resolve
supports       source explains target without replacing it
must_match     identified fields must be byte-stable / ID-identical
inherits       projection may omit; remaining fields must match source
```

Canonical spine:

```text
MC-01
  ←references— Interpretation
  ←must_match— Runtime Contract.mc01
Interpretation
  ←depends_on— Domains
  ←depends_on— EvidencePriority
Domains
  ←depends_on— Optimization
  ←depends_on— Temporal            # activation of domains; natal domains unchanged
  ←must_match— DetailedAuthority / Career / Wealth / Relationship / Legacy / Vitality
EvidencePriority
  ←depends_on— Optimization
  ←depends_on— Narrative
Temporal
  ←supports— Narrative.temporal
Optimization
  ←depends_on— Narrative
  ←must_match— Runtime Contract.optimization
Narrative
  ←must_match— Runtime Contract.narrative
Runtime Contract
  ←inherits— Portal
  ←inherits— PDF
  ←inherits— DOCX
  ←inherits— API
  ←inherits— Consulting
  ←inherits— Export
  ←must_match— History
```

There is **one** ConsistencyGraph family. Adapters do not build a second graph with different IDs.

---

# 6. CONSISTENCY LAYERS

Suggested and frozen:

```text
L0    Structural
L1    Semantic
L2    Narrative
L3    Presentation
L4    Runtime
```

These are **diagnostic layers**, not customer sections.

They are distinct from verdicts in §37 (`PASS` … `FAIL_CRITICAL`).

Evaluation order:

```text
L0
      ↓
L1
      ↓
L2
      ↓
L4                    # contract + consumer read path
      ↓
L3                    # presentation projections of the same contract
```

L3 is last among consumer checks because presentation may hide nodes only after analytical identity is proven.

If L0 fails critical, later layers still collect remaining critical mismatches when safe. They must not “repair” L0.

---

# 7. L0 STRUCTURAL CONSISTENCY

Verify structural IDs remain identical through the chain.

Must remain identical:

```text
Pattern
Integrity
Grade
Achievement
Career Profile
Wealth Profile
```

Also L0:

```text
analysis_id
mingju_result_id
mc01.content_hash
Damage / Rescue / Support / Purity / Pattern Strength IDs
Useful God identity as consumed (not recalculated)
```

Rules:

```text
SYS-L0-01  Runtime Contract.mc01 references the same mingju_result_id used by all Pack 07 stages.
SYS-L0-02  Optional mc01_snapshot hash equals mc01.content_hash.
SYS-L0-03  No Pack 07 object stores a writable copy of Pattern / Grade / Integrity.
SYS-L0-04  Temporal objects do not rewrite natal MC-01 fields.
SYS-L0-05  Duplicate Pattern / Grade keys across layers are ConsistencyError critical.
```

L0 does not ask whether Pattern is “correct astrology.” It asks whether every consumer still sees the **same** Pattern.

---

# 8. L1 SEMANTIC CONSISTENCY

Verify:

```text
Meaning never contradicts Truth.
```

Interpretation (DI-01–DI-07) may explain, expand, correlate, and prioritize.

It MUST NOT:

```text
elect a new Pattern
invert Grade
declare Integrity healthy when MC-01 is damaged
treat Shen Sha as structural driver
rewrite Day Master Strength
rewrite Useful God identity
```

Domain engines (DI-08, DI-12–DI-17) must consume MC-01 profiles and Evidence Priority.

If MC-01 Wealth creation is high and retention is low, meaning MUST NOT become “tài vận toàn diện tốt”.

If MC-01 Grade is A and authority is high, meaning MUST NOT call the natal structure weak because an annual is hard.

`unresolved` truth MUST remain `unresolved` in meaning. High-confidence fake resolution is L1 critical.

---

# 9. L2 NARRATIVE CONSISTENCY

Verify:

```text
Narrative does not contradict
      Domains
      Optimization
      Priority
```

Narrative (DI-19) consumes. It does not infer, rerank, or invent.

Rules:

```text
SYS-L2-01  NarrativeGraph node evidence_ids resolve to Interpretation / Domains / Temporal / Optimization / MC-01.
SYS-L2-02  Executive summary does not promote a P4/P5 finding above P0/P1.
SYS-L2-03  Top actions come only from LifeOptimizationResult.
SYS-L2-04  Domain narrative state matches published domain natal state.
SYS-L2-05  Commercial / technical / expert / executive are projections of one graph.
SYS-L2-06  Narrative does not write Pattern, Grade, or domain scores.
SYS-L2-07  Natal and luck remain two layers in wording posture.
```

Elaboration is allowed (`explains` / `expands`). Rewrite is not.

---

# 10. L3 PRESENTATION CONSISTENCY

Verify:

```text
Portal
PDF
DOCX
show identical canonical meaning.
```

Presentation order may differ.

Meaning may not.

Allowed:

```text
hide
collapse
expand
reorder visually
density / layer cut (commercial vs expert)
```

Forbidden:

```text
rewrite
reinterpret
rerank
add findings
drop a P0 claim while showing a P2 claim as if primary
different Pattern / Grade / domain state per surface
```

Labels may differ by density (DI-20). Canonical IDs must match.

---

# 11. L4 RUNTIME CONSISTENCY

Verify:

```text
Runtime consumers read CanonicalRuntimeResult.
No recalculation.
```

Consumers:

```text
Portal
PDF
DOCX
API
Consulting
Export
History
Future Mobile / Desktop
```

Each consumer MUST:

```text
carry the same analysis_id
read published objects
not call Pack 07 engines again for that analysis_id
not call MC-01 again to “refresh” Pattern for that analysis_id
```

A new luck window or ruleset produces a **new** `analysis_id`. It does not mutate the old contract.

---

# 12. CONSISTENCY RESULT

Define:

```text
ConsistencyResult
```

```text
ConsistencyResult
  analysis_id
  contract_content_hash
  graph                         # ConsistencyGraph
  verdict                       # §22
  layers
    L0
    L1
    L2
    L3
    L4
  errors[]                      # ConsistencyError
  warnings[]                    # ConsistencyWarning
  score                         # ConsistencyScore; diagnostic only
  trace_id
  engine_version
  created_at                    # audit; not an analytical input
```

`ConsistencyResult` is **not** part of customer-facing narrative.

It MUST NOT be required for Portal rendering of a published contract. Publication gating uses it. Customers see analysis, not validator internals.

---

# 13. CONSISTENCY REPORT

Define:

```text
ConsistencyReport
```

```text
ConsistencyReport
  analysis_id
  verdict
  summary                       # structured IDs, not Vietnamese marketing copy
  errors_by_severity
  warnings_by_code
  layer_status
    L0 / L1 / L2 / L3 / L4
  node_status{}                 # per ConsistencyGraph node
  unmatched_fields[]
  consumer_parity
    portal
    pdf
    docx
    api
    consulting
    export
  golden_case_id                # if run against a golden fixture
```

The report is for engineering, QA, and release gates.

It is not a customer “độ tin cậy” widget.

---

# 14. CONSISTENCY ERROR

Introduce:

```text
ConsistencyError
```

```text
ConsistencyError
  source                        # graph node
  target                        # graph node
  rule                          # e.g. SYS-L0-03, SYS-PATTERN-01
  severity                      # critical | major | minor
  layer                         # L0 … L4
  field_path                    # JSON-like path
  expected                      # canonical ID / hash / enum
  actual
  trace                         # ConsistencyTrace
```

Every error MUST expose `trace`.

Missing trace is itself a consistency failure (SYS-09).

---

# 15. CONSISTENCY WARNING

Warnings for:

```text
presentation differences
confidence wording
optional omissions
```

```text
ConsistencyWarning
  source
  target
  rule
  layer
  field_path
  note_id                       # structured; Composer may later word it
  trace
```

Warning examples:

```text
PDF omits expert-layer nodes that Portal expert mode shows
commercial layer hides P3 supporting detail
confidence wording is softer than expert layer but IDs match
optional DI-08 supporting domain not_evaluated
temporal.status = not_evaluated because luck was not requested
```

Warnings MUST NOT be used to hide Pattern / Grade mismatch.

---

# 16. PATTERN CONSISTENCY

```text
Pattern must remain identical through all stages.
```

```text
SYS-PATTERN-01  MC-01 Pattern ID = Interpretation references = Narrative Pattern wording target = Runtime mc01 = all consumers.
SYS-PATTERN-02  Narrative may name and explain Pattern. It may not elect another Pattern.
SYS-PATTERN-03  Optimization may not treat Pattern as an action it can rewrite.
SYS-PATTERN-04  Luck activation may not replace natal Pattern.
SYS-PATTERN-05  Shen Sha cannot occupy Pattern’s structural role (DI-07 P0 floor).
```

Mismatch severity: **critical**.

---

# 17. GRADE CONSISTENCY

```text
Grade must remain identical.
```

```text
SYS-GRADE-01  Grade ID / band is read only from MC-01.
SYS-GRADE-02  No Pack 07 object publishes a second Grade.
SYS-GRADE-03  Optimization cannot change Grade.
SYS-GRADE-04  Narrative cannot change Grade.
SYS-GRADE-05  Temporal hardship cannot lower natal Grade.
```

Mismatch severity: **critical**.

---

# 18. AUTHORITY CONSISTENCY

```text
Authority must remain identical.
Narrative may elaborate. Not rewrite.
```

Identical means:

```text
MC-01 Achievement.authority structural score / state
      = DI-08 domain_id authority natal state / priority
      = DI-12 DetailedAuthorityResult natal object
      = Runtime domains.authority
      = Narrative authority nodes’ referenced IDs
      = consumer projections
```

Narrative may add `explains` / `expands` nodes. It may not change `DetailedAuthorityResult.state`.

Authority ≠ Leadership ≠ Management ≠ Career (DI-08 / DI-12). Collapsing them into one “success” score is **major**.

---

# 19. CAREER CONSISTENCY

```text
Career must remain identical.
```

```text
MC-01 Career Profile
      = DI-08 career natal state
      = DI-13 DetailedCareerResult natal object
      = Runtime domains.career
      = Narrative career references
```

Career fit explanations must not become job titles.

Portal MUST NOT rewrite Career.

Severity: structural profile mismatch = **major**; if it implies a new Pattern/Grade = **critical**.

---

# 20. WEALTH CONSISTENCY

```text
Wealth must remain identical.
```

```text
MC-01 Wealth Profile (creation / retention / expansion as owned)
      = DI-08 wealth natal state
      = DI-14 DetailedWealthResult natal object
      = Runtime domains.wealth
      = Narrative wealth references
```

Creation ≠ retention ≠ expansion. Flattening to one “tài vận tốt” is L1/L2 **major** (architecture: forbidden comprehensive-good wording).

PDF MUST NOT rewrite Wealth.

---

# 21. RELATIONSHIP CONSISTENCY

```text
Relationship must remain identical.
```

```text
DI-08 relationship natal state
      = DI-15 detailed relationship natal object
      = Runtime domains.relationship
      = Narrative relationship references
```

Hồng Loan ≠ marriage. Compatibility ≠ stability. Narrative must not collapse the pipeline into a wedding prediction.

Biography cannot be used to “correct” relationship state.

---

# 22. LEGACY CONSISTENCY

```text
Legacy must remain identical.
```

```text
DI-16 DetailedLegacyResult natal object
      = Runtime domains.legacy
      = Narrative legacy references
```

Legacy is lasting value (DI-16). It is broader than biological children.

DI-08 `children` may support Legacy. It MUST NOT publish a second competing Legacy score.

---

# 23. VITALITY CONSISTENCY

```text
Vitality must remain identical.
```

```text
DI-17 DetailedVitalityResult natal object
      = Runtime domains.vitality
      = Narrative vitality references
```

Vitality is capacity / stress / recovery / resilience (DI-17). Health is downstream.

DI-08 `health` may support Vitality. It MUST NOT diagnose disease or publish a second vitality score.

Narrative MUST NOT turn vitality into medical claims.

---

# 24. OPTIMIZATION CONSISTENCY

```text
Optimization must consume Domains.
Never invent priorities.
```

```text
SYS-OPT-01  LifeOptimizationResult exists once in the contract.
SYS-OPT-02  Action priority consumes DI-07; no natal rerank (OPT-19).
SYS-OPT-03  Targets / bottlenecks resolve to published domain IDs.
SYS-OPT-04  Top-N actions in Narrative equal Optimization Top-N, same order.
SYS-OPT-05  Optimization cannot write Pattern or Grade.
SYS-OPT-06  Natal vs temporal plans remain separate.
SYS-OPT-07  Shen Sha never Action Driver.
SYS-OPT-08  Empty Optimization ≠ invented life-coach list in Narrative or Portal.
```

Optimization contradicting Domains: **major**.

Optimization rewriting Grade: **critical**.

---

# 25. NARRATIVE CONSISTENCY (RULES)

```text
Narrative must consume Priority.
Never rerank.
```

Repeats DI-19 NAR-01 … NAR-15 as **system** checks, not a second composer.

Additional system checks:

```text
SYS-NAR-01  One NarrativeGraph per analysis_id.
SYS-NAR-02  Layer cuts hide nodes; they do not add nodes.
SYS-NAR-03  MC-01 Composer Mệnh Cục summary is not overwritten.
SYS-NAR-04  No duplicated claim presented as a new finding in a later section.
```

Narrative inventing facts: **critical**.

Narrative reranking: **critical**.

---

# 26. RUNTIME CONTRACT CONSISTENCY

```text
Runtime Contract must preserve all canonical objects.
```

```text
CanonicalRuntimeResult
  identity
  mc01
  interpretation
  domains
  temporal
  optimization
  narrative
  metadata
```

```text
SYS-CRC-01  One contract (CRC-01).
SYS-CRC-02  One analysis_id through identity, metadata, export, API, consulting, history (CRC-02).
SYS-CRC-03  No duplicated writable Pattern / Grade / Domains / Optimization / Narrative (CRC-03).
SYS-CRC-04  Views are projections (CRC-12).
SYS-CRC-05  History stores CanonicalRuntimeResult, not PDF text as truth (CRC-11).
```

A second competing contract for the same `analysis_id` is **critical**.

---

# 27. PORTAL CONSISTENCY

```text
Portal must not mutate data.
```

```text
SYS-PORTAL-01  Portal adapter reads CanonicalRuntimeResult.
SYS-PORTAL-02  Collapsed cards do not delete objects from the contract.
SYS-PORTAL-03  Client-side reorder is visual only.
SYS-PORTAL-04  Portal MUST NOT recalculate interpretation.
SYS-PORTAL-05  Portal MUST NOT rewrite Career, Wealth, Authority, or Pattern.
```

Portal changes Truth: **critical**.

---

# 28. PDF CONSISTENCY

```text
PDF must not mutate data.
```

```text
SYS-PDF-01  PDF consumes CanonicalExportModel projected from the same analysis_id.
SYS-PDF-02  Page breaks / TOC order are presentation.
SYS-PDF-03  PDF MUST NOT recalculate.
SYS-PDF-04  PDF MUST NOT rewrite Wealth or any natal object.
SYS-PDF-05  PDF-only conclusions are forbidden (NAR failure extended).
```

PDF changes Truth: **critical**.

---

# 29. DOCX CONSISTENCY

```text
DOCX must not mutate data.
```

Same rules as PDF with `SYS-DOCX-01` … `SYS-DOCX-05`.

DOCX and PDF may use different section order. Canonical IDs and states must match Portal and API.

---

# 30. API CONSISTENCY

```text
API must expose canonical truth.
```

```text
SYS-API-01  CanonicalAPIModel is a projection of CanonicalRuntimeResult.
SYS-API-02  No endpoint recalculates Pack 07 or MC-01 for a published analysis_id.
SYS-API-03  Two endpoints cannot yield two Patterns for one analysis_id.
SYS-API-04  unresolved serializes; it is not replaced by HTTP-success fiction.
SYS-API-05  API MUST NOT rewrite Domains.
```

API mutates or forks truth: **critical**.

---

# 31. AI CONSULTING CONSISTENCY

Future AI Consulting MUST consume:

```text
Canonical Runtime Contract
```

via `CanonicalConsultingModel` (DI-20).

```text
SYS-CONSULT-01  Dialogue may filter the NarrativeGraph.
SYS-CONSULT-02  Dialogue MUST NOT run a second Pack 07 analysis unless a new analysis_id is created.
SYS-CONSULT-03  Follow-up MUST NOT invent facts absent from the contract.
SYS-CONSULT-04  LLM expansion, if any, stays after canonical composition (architecture).
SYS-CONSULT-05  Consulting MUST NOT mutate History.
```

Consulting is a consumer node on the same ConsistencyGraph.

---

# 32. CONSISTENCY TRACE

Every inconsistency MUST expose trace.

```text
ConsistencyTrace
  analysis_id
  rule
  path[]                        # node → field → evidence_id → upstream id
  mc01_ref
  evidence_ids[]
  domain_ids[]
  narrative_node_ids[]
  consumer                      # portal | pdf | docx | api | consulting | export | none
```

Trace MUST be sufficient to answer:

```text
Which truth object?
Which meaning object?
Which narrative node?
Which consumer projection?
```

No silent mismatch.

---

# 33. CONSISTENCY SCORE

Introduce:

```text
ConsistencyScore
```

Only for diagnostics.

Never customer-facing.

```text
ConsistencyScore
  value                         # 0..100 diagnostic
  layer_scores
    L0 … L4
  formula_id
  not_for_publication: true
```

Score MUST NOT:

```text
replace Grade
appear as “độ chính xác mệnh”
be averaged into domain strength
gate customer copy except via verdict
```

A chart with `unresolved` Pattern may still have a high consistency score if every layer honestly remains unresolved.

---

# 34. CRITICAL ERRORS

Examples:

```text
Pattern mismatch
Grade mismatch
Narrative contradicts Priority
Portal changes Truth
PDF changes Truth
DOCX changes Truth
API changes Truth
two contracts for one analysis_id
Optimization writes Grade
Narrative writes Pattern
mc01_snapshot hash mismatch
natal rewritten by luck at contract root
```

Any critical error → verdict `FAIL_CRITICAL`.

Result is not publishable as canonical output.

---

# 35. MAJOR ERRORS

Examples:

```text
Optimization contradicts Domains
Authority mismatch
Career mismatch
Wealth creation/retention flattened
Relationship pipeline collapsed into a false marriage claim
Legacy duplicated as a second children score
Vitality duplicated as a medical diagnosis
supporting DI-08 domain published as a second Authority/Career score
Narrative Top actions ≠ Optimization Top actions
```

Any major error (and no critical) → `FAIL_MAJOR`.

Analytical publication is blocked until repaired.

---

# 36. MINOR ERRORS

```text
Presentation wording drift that does not change IDs
Ordering / formatting
Optional layer omitted without claiming it was evaluated
Export missing an expert node that Portal expert mode shows, while commercial IDs match
```

Only minor errors → `FAIL_MINOR`.

CanonicalRuntimeResult may already be valid at L0–L2. The **adapter** fails consistency until wording/order catalogs align. Minor MUST NOT be used for Pattern/Grade drift.

---

# 37. VERDICTS

Frozen verdicts:

```text
PASS
PASS_WITH_WARNINGS
FAIL_MINOR
FAIL_MAJOR
FAIL_CRITICAL
```

```text
FAIL_CRITICAL        any critical error
FAIL_MAJOR           else any major error
FAIL_MINOR           else any minor error
PASS_WITH_WARNINGS   else any warning
PASS                 else
```

Publish gate:

```text
PASS / PASS_WITH_WARNINGS     publish allowed
FAIL_MINOR                    contract publish allowed if L0–L2 / L4 analytical checks passed; presentation adapters blocked
FAIL_MAJOR / FAIL_CRITICAL    do not publish as canonical
```

Do not invent extra verdicts per consumer (`PORTAL_PASS` vs `PDF_PASS` as separate truths). Consumer parity is a report section, not a second analysis.

---

# 38. GOLDEN DATASET

Golden **consistency cases**.

They store the chain, not a final paragraph.

Minimum cases:

```text
complete natal chain: MC-01 → interpretation → six domains → optimization → narrative → contract
same analysis_id across Portal / PDF / DOCX / API projections
creation high / retention low remains split through meaning, narrative, and export
Career High + Relationship Low both preserved
unresolved Pattern remains unresolved in every consumer
luck_cycle + annual present: natal objects identical to natal-only sibling except temporal / new analysis_id
Optimization Top 3 match Narrative Top 3
EvidencePriority P0 Pattern still P0 in executive summary
mc01_snapshot present and hash-identical
optional supporting domains not_evaluated without invention
```

Golden cases MUST include:

```text
upstream facts
MC-01 structural findings
Pack 07 objects
CanonicalRuntimeResult hash
projection hashes (export / api / consulting)
forbidden conclusions
accepted presentation omissions
```

Do not treat Golden Dataset as editable expected prose to make tests pass.

Do not store only PDF screenshots as truth.

---

# 39. NEGATIVE TESTS

Must prove:

```text
Narrative cannot rewrite Pattern.
Optimization cannot rewrite Grade.
Portal cannot rewrite Career.
PDF cannot rewrite Wealth.
API cannot rewrite Domains.
```

Additional required negatives:

```text
DOCX cannot rewrite Authority
Consulting cannot invent a new domain
Export subset cannot add findings
two endpoints cannot yield two Grades
luck cannot lower natal Grade
Shen Sha cannot become Pattern
hidden Portal card still present in contract
FAIL if ConsistencyScore is shown to customers
missing trace is rejected
```

Each negative test MUST emit `ConsistencyError` with source, target, rule, severity, and trace.

---

# 40. ACCEPTANCE INVARIANTS

At minimum:

```text
SYS-01  Truth immutable.
SYS-02  Meaning consistent.
SYS-03  Domains consistent.
SYS-04  Optimization consistent.
SYS-05  Narrative consistent.
SYS-06  Runtime consistent.
SYS-07  Presentation consistent.
SYS-08  No duplicate truth.
SYS-09  Trace required.
SYS-10  Deterministic.
```

Additional:

```text
SYS-11  One ConsistencyGraph per analysis_id.
SYS-12  L0–L4 are the only consistency layers.
SYS-13  ConsistencyScore is diagnostic only.
SYS-14  Consulting consumes CanonicalRuntimeResult.
SYS-15  Local stage validity never implies this engine is skipped.
SYS-16  Unknown versions fail closed.
SYS-17  Domain uncertainty is not a consistency error.
SYS-18  CRC-01 … CRC-12 remain binding.
```

Determinism:

```text
Same CanonicalRuntimeResult + same projection bytes
      = same ConsistencyResult verdict, errors, and rule IDs
      (created_at excluded if specified)
```

No LLM in the consistency path.

---

# 41. FAILURE CONDITIONS

This specification FAILS if:

```text
Truth duplicated
Pattern mismatch
Grade mismatch
Optimization reranks
Narrative invents facts
Presentation mutates
API mutates
```

Also FAIL if:

```text
two conflicting contracts exist
Portal / PDF / DOCX / API recalculate
Authority / Career / Wealth natal objects diverge without error
ConsistencyScore becomes customer-facing
this engine publishes a second runtime contract
stage validators are deleted “because SYS exists”
```

---

# 42. OWNERSHIP

MC-01 owns structural truth and MC-01 validation.

Pack 07 stage documents own local result validity.

This engine owns **continuity** across those owned objects and every runtime consumer.

It does not take ownership of Pattern, Grade, or domain calculation.

---

# 43. DETERMINISM AND BIOGRAPHY

Same published contract → same consistency verdict.

Biography, known wealth, known marriage, known job, and known health outcomes are not consistency inputs.

Wall-clock `created_at` must not change natal L0 fields.

---

# 44. VERSIONING

```text
bte.detailed_interpretation.system_consistency.v1
```

Sits beside, does not replace:

```text
bte.detailed_interpretation.runtime_contract.v1
bte.detailed_interpretation.result.v1
bte.detailed_interpretation.composer.v1
bte.mingju.decision.v1
```

Breaking changes to graph nodes, layers L0–L4, or verdict enum require a new major version.

---

# 45. FREEZE TARGET

Frozen:

1. ConsistencyGraph nodes and edges.
2. Layers L0 Structural, L1 Semantic, L2 Narrative, L3 Presentation, L4 Runtime.
3. Rules in this document (Pattern, Grade, domains, optimization, narrative, contract, consumers).
4. ConsistencyResult / ConsistencyReport.
5. ConsistencyError / ConsistencyWarning.
6. ConsistencyTrace required on every inconsistency.
7. Verdicts PASS … FAIL_CRITICAL.
8. ConsistencyScore diagnostic-only.
9. Invariants SYS-01 … SYS-18.

Not frozen:

- exact Python dataclasses
- HTTP of a consistency endpoint
- numeric score formula weights
- Vietnamese warning copy
- DI-22 test case implementations

---

# 46. NEXT DOCUMENT

Next:

```text
22_TEST_STRATEGY.md
```

That document must specify how to test this engine and the Pack 07 reasoning contract.

It MUST test reasoning continuity, not only a final label.

It MUST NOT invent a second runtime contract.

It MUST NOT treat Golden Dataset as editable expected prose.

Architecture also listed `21_VALIDATION_RULES.md`. This Product Owner file is the DI-21 global engine. Stage-level rule tables remain in DI-01–DI-20. Do not edit those documents to retarget filenames.

Do not write DI-22 until Product Owner approval.

---

# 47. COMPLIANCE NOTES

1. One ConsistencyGraph.
2. All runtime consumers covered: Portal, PDF, DOCX, API, Consulting, Export, History.
3. MC-01 Pattern / Integrity / Grade / Achievement / Career / Wealth remain referenced, not forked.
4. Presentation may hide / collapse / expand / reorder; never rewrite / rerank.
5. Next document name is `22_TEST_STRATEGY.md`.
