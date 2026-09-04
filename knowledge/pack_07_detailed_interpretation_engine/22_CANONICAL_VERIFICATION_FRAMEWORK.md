# PACK 07 — CANONICAL VERIFICATION FRAMEWORK

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-22  
**Document:** `22_CANONICAL_VERIFICATION_FRAMEWORK.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `21_SYSTEM_CONSISTENCY_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially `14_TEST_STRATEGY.md`  
**Schema target:** `bte.detailed_interpretation.verification.v1`  
**Related schemas:**

- `bte.detailed_interpretation.system_consistency.v1`
- `bte.detailed_interpretation.runtime_contract.v1`
- `bte.detailed_interpretation.composer.v1`
- `bte.mingju.decision.v1`

This document defines the canonical **Canonical Verification Framework**.

Architecture listed `22_TEST_STRATEGY.md` for the test pyramid. DI-21 pointed to that name. This Product Owner target authors `22_CANONICAL_VERIFICATION_FRAMEWORK.md` as the **end-to-end reasoning verification** envelope: Truth → Meaning → Optimization → Narrative → Runtime → Presentation → Commercial. Architecture and DI-01–DI-21 remain immutable.

This document does **not** invent a second runtime contract.

This document does **not** replace the System Consistency Engine (DI-21). Consistency proves ID continuity. This framework **verifies the whole reasoning chain**, including commercial quality.

This document does **not** implement runtime.

Isolated unit tests remain useful in later implementation. They are **not sufficient** for this framework’s acceptance.

---

# 1. PURPOSE

Create the canonical:

```text
CANONICAL VERIFICATION FRAMEWORK
```

Purpose:

Verify the **entire reasoning chain**.

Not isolated modules.

Not isolated unit tests.

The framework validates that:

```text
Truth
      ↓
Meaning
      ↓
Optimization
      ↓
Narrative
      ↓
Runtime
      ↓
Presentation
```

remain logically consistent.

It also verifies that the customer-facing commercial cut of that chain is clear, actionable, non-contradictory, prioritized, and useful — without becoming a second truth.

---

# 2. CORE PRINCIPLE

Frozen:

```text
Correct modules
      ≠
Correct system.
```

The framework verifies **end-to-end reasoning**.

A passing Ten Gods module, a passing Domain module, and a passing PDF renderer can still fail this framework if:

```text
Pattern does not reach Executive Summary
Top actions do not match Optimization
PDF meaning diverges from Portal
Temporal wording rewrites Natal
Commercial copy hides the bottleneck
```

Architecture rule (extended here):

```text
TEST THE REASONING CONTRACT,
NOT ONLY THE FINAL ANSWER.
```

---

# 3. SCOPE

In scope:

1. Verification levels V0–V5
2. Reasoning chain and continuity
3. VerificationGraph
4. CanonicalVerificationResult / CanonicalVerificationReport
5. Quality rules (narrative, explanation, action, executive, domain, temporal, runtime, export, consulting)
6. Commercial checks
7. Golden end-to-end cases
8. Negative proofs
9. Acceptance invariants CVF-01 … CVF-10

Out of scope:

```text
implementing pytest suites
rewriting MC-01 14_TEST_STRATEGY.md
replacing DI-21 ConsistencyGraph
isolated rule-unit catalogs as acceptance
PDF layout / CSS
Portal component tests as the only bar
LLM-as-judge of “sounds good”
a second CanonicalRuntimeResult
editing Golden Dataset expected prose to make tests pass
```

Relation to architecture test pyramid:

```text
Rule / Stage unit tests              → necessary later; not this framework’s bar
Cross-stage contract tests           → V0–V2 + DI-21
Golden Dataset tests                 → this framework
Negative / adversarial tests         → this framework
Metamorphic tests                    → this framework (natal vs luck, projection parity)
Serialization / determinism          → V3 + CVF-10
Orchestrator integration             → V3
Portal / PDF / DOCX parity           → V3–V5
Live runtime acceptance              → later implementation; this document freezes the bar
```

Relation to DI-21:

```text
ConsistencyResult FAIL_CRITICAL / FAIL_MAJOR
      → CanonicalVerificationResult cannot PASS

Consistency PASS
      → still run V2 quality, V4 meaning parity, V5 commercial checks
```

This framework **consumes** `ConsistencyResult`. It does not re-implement ID matching as a competing engine.

---

# 4. NON-SCOPE

This framework MUST NOT:

1. Recalculate MC-01 or Pack 07 engines
2. Treat string contains (`"công chức"`) as a passing proof
3. Use biography or known outcomes as expected truth
4. Collapse `unresolved` into a fake resolved Golden
5. Let commercial usefulness override Pattern / Grade
6. Allow presentation order to count as analytical rank
7. Publish a second `analysis_id` per surface
8. Replace SYS-01 … SYS-18 or CRC-01 … CRC-12
9. Make `ConsistencyScore` customer-facing
10. Require UI screenshots as the only Golden truth

Unknown versions fail closed.

Domain uncertainty is not a verification failure if every layer honestly remains `unresolved`.

---

# 5. VERIFICATION LEVELS

Canonical levels:

```text
V0    Truth Verification
V1    Semantic Verification
V2    Narrative Verification
V3    Runtime Verification
V4    Presentation Verification
V5    Commercial Verification
```

Mapping to DI-21 layers (diagnostic, not a second truth):

```text
V0  ↔  L0 Structural          + Useful God / Five Elements / Authority identity
V1  ↔  L1 Semantic
V2  ↔  L2 Narrative           + narrative quality (duplication, bottlenecks, P0)
V3  ↔  L4 Runtime
V4  ↔  L3 Presentation
V5      Commercial quality of the same contract (no new facts)
```

Evaluation order:

```text
V0
      ↓
V1
      ↓
V2
      ↓
V3
      ↓
V4
      ↓
V5
```

If V0 fails critical, later levels still collect remaining critical mismatches when safe. They must not “repair” Truth.

These six levels are frozen. Do not invent V6 as a second commercial truth.

---

# 6. V0 TRUTH VERIFICATION

Verify the following remain **canonical** (referenced, not forked):

```text
Pattern
Integrity
Grade
Achievement
Career Profile
Wealth Profile
Authority
Useful God
Five Elements
```

Rules:

```text
CVF-V0-01  MC-01 Pattern / Integrity / Grade IDs are the only structural IDs in the chain.
CVF-V0-02  Achievement / Career Profile / Wealth Profile are read from MC-01.
CVF-V0-03  Authority natal identity matches MC-01 Achievement.authority + DI-12 DetailedAuthorityResult.
CVF-V0-04  Useful God identity is consumed, not recalculated (DI-18).
CVF-V0-05  Five Elements identity / climate context is consumed, not recalculated.
CVF-V0-06  Damage remains when Rescue exists; Rescue does not delete Damage (MC-01 + DI-21).
CVF-V0-07  mingju_result_id and content_hash are stable for the analysis_id.
```

V0 does not re-score Pattern. It verifies that Pack 07 still **points at** the same Pattern.

Mismatch of Pattern or Grade: **critical**.

---

# 7. V1 SEMANTIC VERIFICATION

Verify:

```text
Pack 07 never changes Truth.
Meaning must remain consistent.
```

```text
CVF-V1-01  Interpretation explains MC-01; it does not elect a new Pattern.
CVF-V1-02  Shen Sha cannot occupy P0 structural role.
CVF-V1-03  Creation high / retention low must not become “tài vận toàn diện tốt”.
CVF-V1-04  Grade A + high authority must not be called natal-weak because an annual is hard.
CVF-V1-05  unresolved remains unresolved; no fake high-confidence resolution.
CVF-V1-06  Dictionary vocabulary cannot override structure.
CVF-V1-07  MC-01 recorded Useful God vs Pattern conflict is retained, not collapsed.
```

Meaning changing Truth: **critical**.

---

# 8. V2 NARRATIVE VERIFICATION

Verify:

```text
Narrative never contradicts Meaning.
```

```text
CVF-V2-01  Every narrative node maps to evidence_ids (DI-19 NAR-01 / NAR-04).
CVF-V2-02  Narrative does not infer or rerank (NAR-02).
CVF-V2-03  One NarrativeGraph serves all modes (NAR-13).
CVF-V2-04  Top actions come only from LifeOptimizationResult (NAR-12).
CVF-V2-05  Natal and luck remain two wording layers (NAR-09).
CVF-V2-06  MC-01 Composer Mệnh Cục summary is not overwritten (NAR-11).
CVF-V2-07  Commercial / technical / expert / executive are cuts of the same graph.
```

Narrative inventing facts or contradicting Meaning: **critical**.

---

# 9. V3 RUNTIME VERIFICATION

Verify:

```text
Portal
PDF
DOCX
API
Consulting
consume identical Runtime Contract.
```

```text
CVF-V3-01  One CanonicalRuntimeResult per analysis_id (CRC-01 / CRC-02).
CVF-V3-02  Consumers read; they do not recalculate (CRC-04).
CVF-V3-03  CanonicalExportModel / CanonicalAPIModel / CanonicalConsultingModel are projections.
CVF-V3-04  History stores CanonicalRuntimeResult, not PDF text as truth (CRC-11).
CVF-V3-05  Two endpoints cannot yield two Patterns for one analysis_id.
CVF-V3-06  ConsistencyResult for this analysis_id is consumed; FAIL_MAJOR/CRITICAL blocks PASS here.
```

Runtime forking truth: **critical**.

---

# 10. V4 PRESENTATION VERIFICATION

Verify:

```text
Presentation may differ visually.
Meaning may not.
```

Allowed:

```text
hide
collapse
expand
reorder visually
density / layer cut
```

Forbidden:

```text
rewrite
reinterpret
rerank
add findings
PDF-only conclusions
Portal-only Pattern
```

```text
CVF-V4-01  Canonical IDs in Portal = PDF = DOCX = API = Consulting for the same analysis_id.
CVF-V4-02  Hidden cards remain in the contract.
CVF-V4-03  Visual order ≠ Evidence Priority order unless the adapter documents it as visual only.
```

Presentation mutating meaning: **critical**.

---

# 11. V5 COMMERCIAL VERIFICATION

Verify the customer receives:

```text
clear
actionable
non-contradictory
prioritized
commercially useful
interpretation
```

Commercial verification is **quality of the same contract**, not a marketing rewrite.

```text
CVF-V5-01  Executive / commercial cut is understandable without inventing facts.
CVF-V5-02  Top strengths, risks, bottlenecks, and actions are visible in the commercial cut when they exist in the contract.
CVF-V5-03  Priorities in the commercial cut match DI-07 / Optimization order.
CVF-V5-04  Actions are conditional and evidence-based; no guaranteed wealth / office / marriage / disease.
CVF-V5-05  Consultant posture: WHY, not a calculator dump, and not a fortune slogan.
CVF-V5-06  Same meaning across Portal / PDF / DOCX commercial cuts (labels may differ by density).
CVF-V5-07  Unresolved is stated as unresolved; it is not sold as certainty.
CVF-V5-08  Commercial usefulness MUST NOT hide P0 Damage or invert Grade.
```

Misleading commercial output: **critical** if it changes Truth or Priority; **major** if it omits a contracted Top bottleneck from the commercial cut while showing a P3 ornament as if primary.

V5 MUST NOT introduce:

```text
job titles as destiny
net-worth promises
medical diagnosis
biography-tuned copy
```

---

# 12. REASONING CHAIN

Canonical chain:

```text
MC-01
      ↓
Meaning
      ↓
Domains
      ↓
Optimization
      ↓
Narrative
      ↓
Runtime
      ↓
Presentation
```

Every link must verify.

Expanded (still one chain):

```text
MC-01 MingJuDecisionResult
      ↓
DI-01–06 interpretation + DI-07 Evidence Priority
      ↓
DI-08 DomainInterpretationSet
      ↓
DI-09–11 Temporal (activation only)
      ↓
DI-12–17 detailed domains
      ↓
DI-18 LifeOptimizationResult
      ↓
DI-19 NarrativeGraph / NarrativeResult
      ↓
DI-20 CanonicalRuntimeResult
      ↓
Portal / PDF / DOCX / API / Consulting projections
      ↓
V5 commercial cut of those projections
```

A broken link is a framework failure even if both endpoints pass in isolation.

Temporal sits on the chain as **activation**. It is not a second MC-01.

---

# 13. REASONING TRACE

Every conclusion must support:

```text
why
where
evidence
priority
confidence
```

```text
VerificationTrace
  analysis_id
  conclusion_id
  why                     # reason keys / rule IDs
  where                   # field_path + graph node
  evidence_ids[]
  priority                # DI-07 tier / rank
  confidence
  consumer                # portal | pdf | docx | api | consulting | export | none
```

Missing any of the five for a published major conclusion: **major** (or **critical** if the conclusion is P0 and untraced).

This trace aligns with DI-21 `ConsistencyTrace`. Verification may attach commercial-cut node IDs; it must not invent evidence.

---

# 14. REASONING CONTINUITY

Verify:

```text
Pattern
      ↓
Authority
      ↓
Career
      ↓
Optimization
      ↓
Narrative
```

remains connected.

```text
CVF-RC-01  Authority explanation references the same Pattern / Integrity / Grade that MC-01 published.
CVF-RC-02  Career explanation does not deny Authority / Pattern already decided.
CVF-RC-03  Optimization targets resolve to those domain objects.
CVF-RC-04  Narrative executive and domain sections cite the same IDs.
```

Disconnected chain (Pattern A, Career text as if Pattern B): **critical**.

---

# 15. DOMAIN CONTINUITY

Verify:

```text
Authority
Career
Wealth
Relationship
Legacy
Vitality
```

remain internally consistent.

```text
CVF-DC-01  Each detailed natal result matches DI-08 natal state for the corresponding domain_id (Legacy/Vitality vs children/health: support, not a second score — DI-21).
CVF-DC-02  Authority ≠ Leadership ≠ Management ≠ Career.
CVF-DC-03  Wealth creation ≠ retention ≠ expansion.
CVF-DC-04  Relationship pipeline is not collapsed into marriage prediction.
CVF-DC-05  Legacy is lasting value, not child count.
CVF-DC-06  Vitality is capacity / stress / recovery / resilience, not diagnosis.
CVF-DC-07  Domain vs domain wording does not deny a decided risk (architecture conflict class 8).
```

Internal domain contradiction: **major** (critical if it implies a new Pattern/Grade).

---

# 16. OPTIMIZATION CONTINUITY

Every Action must map to:

```text
Driver
or
Bottleneck
or
Leakage
```

Never random.

```text
CVF-OC-01  Action.reason + evidence_ids resolve to Driver, bottleneck, leakage, or P0 safety.
CVF-OC-02  No padded Top 3 with Shen Sha or symbolic items (DI-18).
CVF-OC-03  Shen Sha never Action Driver.
CVF-OC-04  Natal vs temporal plans remain separate and labeled.
CVF-OC-05  Expansion despite critical leakage without condition fails.
CVF-OC-06  Optimization does not rerank DI-07 natal evidence.
```

Random or reranked actions: **major**; rewriting Grade: **critical**.

---

# 17. NARRATIVE CONTINUITY

Every paragraph must map to:

```text
Evidence.
```

In this framework, “paragraph” means a Composer sentence / NarrativeGraph node / message_key instance — not free UI copy.

```text
CVF-NC-01  No narrative node without evidence_ids.
CVF-NC-02  No duplicated claim presented as a new finding.
CVF-NC-03  Later sections may explains / expands; they must not restated-as-new P0.
```

Unsupported paragraph: **major** (critical if it states a new Pattern).

---

# 18. PRIORITY CONTINUITY

Top priorities must remain Top priorities throughout every layer.

```text
CVF-PC-01  DI-07 P0 remains P0 in Domain priority, Optimization, Narrative executive, and commercial cut.
CVF-PC-02  Narrative does not promote P4/P5 above P0/P1.
CVF-PC-03  Portal / PDF / DOCX commercial cuts do not invert Top 3 actions.
CVF-PC-04  Visual reorder does not change stored ranks.
```

Priority inversion: **critical** for P0; **major** for Top 3 vs P2 ornament swap.

---

# 19. RUNTIME CONTINUITY

```text
CanonicalRuntimeResult
      ↓
Portal
      ↓
PDF
      ↓
DOCX
      ↓
API
      ↓
Consulting
```

must remain identical in **meaning**.

Identical means:

```text
same analysis_id
same mc01.content_hash
same domain natal states
same optimization Top-N IDs and order
same NarrativeGraph IDs
```

not identical CSS.

---

# 20. COMMERCIAL CONTINUITY

Customer should receive:

```text
same meaning
across every presentation.
```

```text
CVF-CC-01  Commercial layer of Portal = commercial projection of PDF/DOCX = API commercial fields.
CVF-CC-02  Expert layer may add density; it must not add facts.
CVF-CC-03  Consulting dialogue may filter; it must not change P0 meaning.
```

---

# 21. NARRATIVE QUALITY

Verify:

```text
No duplication.
No contradiction.
No unsupported statement.
No priority inversion.
No missing bottlenecks.
```

Maps to DI-19 additional bars:

```text
Composer does not infer
Composer does not rerank
Composer does not rewrite natal from luck
Shen Sha does not lead
PDF ≠ Portal meaning is forbidden
empty Optimization ≠ invented life-coach list
low confidence ≠ strong wording
```

Missing contracted P0 bottleneck in executive/commercial cut: **major**.

---

# 22. EXPLANATION QUALITY

Every recommendation answers:

```text
Why?
```

```text
CVF-EQ-01  Recommendation nodes carry reason keys + evidence_ids.
CVF-EQ-02  “Should” without why fails.
CVF-EQ-03  Why must cite Driver / bottleneck / leakage / P0 / Useful God consumption — not color/object superstition as the lead (DI-18).
```

---

# 23. ACTION QUALITY

Every action answers:

```text
What?
Why?
Condition?
Priority?
```

```text
CVF-AQ-01  Action identity (what) is structured, not a slogan.
CVF-AQ-02  Why is present (CVF-EQ).
CVF-AQ-03  Condition / time_scope is present (natal vs temporal; leakage gate).
CVF-AQ-04  Priority matches Optimization order.
CVF-AQ-05  No medical / investment / legal tactics (DI-18).
```

An action missing What / Why / Condition / Priority: **major**.

---

# 24. EXECUTIVE QUALITY

Executive Summary must:

```text
match P0.
```

```text
CVF-XQ-01  Executive leads with P0 structure (Pattern / Integrity / Grade / critical Damage+Rescue), not Shen Sha.
CVF-XQ-02  Executive answers who / what matters / what to prioritize (DI-19).
CVF-XQ-03  Executive layer is a one-minute cut of the same NarrativeGraph, not a different truth.
CVF-XQ-04  If a P0 bottleneck exists, executive must include it.
```

Executive mismatch with P0: **critical**.

---

# 25. DOMAIN QUALITY

Each domain must remain **self-consistent**.

```text
CVF-DQ-01  Driver / support / bottleneck / risk / condition inside a domain do not cancel each other without an explicit retained conflict.
CVF-DQ-02  Conflicts are retained when real (architecture §25).
CVF-DQ-03  Averaging contradictions into a bland paragraph fails.
CVF-DQ-04  Domain confidence cannot exceed supporting MC-01 / evidence confidence.
```

---

# 26. TEMPORAL QUALITY

Temporal must never rewrite Natal.

```text
CVF-TQ-01  Luck activation / interaction / temporal activation do not mutate natal MC-01 or natal domain objects.
CVF-TQ-02  Grade does not change every Đại Vận (MC-01 freeze extended).
CVF-TQ-03  Specificity ≠ dominance (DI-11).
CVF-TQ-04  New luck window → new analysis_id (or child run id); old natal bytes stay immutable.
```

Natal rewrite: **critical**.

---

# 27. RUNTIME QUALITY

Runtime must never fork truth.

```text
CVF-RQ-01  One contract, many presentations (DI-20).
CVF-RQ-02  Adapters copy → view-model; they do not mutate the published result.
CVF-RQ-03  Unknown contract_version fails closed.
```

---

# 28. EXPORT QUALITY

PDF, DOCX, and API must expose **identical meaning**.

```text
CVF-EX-01  CanonicalExportModel and CanonicalAPIModel project the same analysis_id.
CVF-EX-02  TOC / page / field order may differ.
CVF-EX-03  No export-only finding.
CVF-EX-04  Future PPT / HTML inherit this rule (DI-20).
```

---

# 29. CONSULTING QUALITY

Consulting must consume Runtime Contract.

```text
CVF-CQ-01  CanonicalConsultingModel only.
CVF-CQ-02  Follow-up may filter the graph; it may not run a second Pack 07 analysis for the same analysis_id.
CVF-CQ-03  LLM expansion, if any, stays after canonical composition (architecture).
CVF-CQ-04  Consulting cannot invent domains or actions.
```

---

# 30. VERIFICATION GRAPH

Introduce:

```text
VerificationGraph
```

One graph per `analysis_id`.

Diagnostic. Not a second interpretation object. Not a replacement of `ConsistencyGraph`.

## 30.1 Nodes

Required nodes:

```text
Truth
Meaning
Domains
Optimization
Narrative
Runtime
Presentation
Commercial
```

Truth includes MC-01 + consumed Useful God / Five Elements identity.

Presentation includes Portal / PDF / DOCX visual adapters.

Commercial is the customer-cut node over Narrative + Presentation. It has **no independent facts**.

Forbidden extra nodes:

```text
CommercialPattern
MarketingGrade
ConsultingRewrite
```

## 30.2 Edges

```text
verified_by
must_match
```

Canonical spine:

```text
Truth
  —must_match→ Meaning
  —must_match→ Domains
  —verified_by→ V0
Meaning
  —must_match→ Narrative
  —verified_by→ V1
Domains
  —must_match→ Optimization
  —verified_by→ V1 / domain quality
Optimization
  —must_match→ Narrative
  —verified_by→ V2 / action quality
Narrative
  —must_match→ Runtime
  —verified_by→ V2
Runtime
  —must_match→ Presentation
  —verified_by→ V3
Presentation
  —must_match→ Commercial
  —verified_by→ V4
Commercial
  —must_match→ Truth            # commercial cut still names the same Pattern
  —verified_by→ V5
```

`must_match` on Commercial → Truth means IDs and priorities, not that the commercial cut prints every expert field.

There is **one** VerificationGraph family per analysis.

---

# 31. VERIFICATION RESULT

Define:

```text
CanonicalVerificationResult
```

```text
CanonicalVerificationResult
  analysis_id
  contract_content_hash
  consistency_verdict           # consumed from DI-21
  graph                         # VerificationGraph
  verdict                       # §35
  levels
    V0
    V1
    V2
    V3
    V4
    V5
  errors[]
  warnings[]
  traces[]                      # VerificationTrace
  engine_version
  created_at                    # audit only
```

Not customer-facing.

Publication gating may require both `ConsistencyResult` and `CanonicalVerificationResult` at allowed verdicts.

---

# 32. VERIFICATION REPORT

Define:

```text
CanonicalVerificationReport
```

```text
CanonicalVerificationReport
  analysis_id
  verdict
  summary                       # structured IDs
  level_status                  # V0 … V5
  chain_status                  # each reasoning-chain link
  continuity
    reasoning
    domain
    optimization
    narrative
    priority
    runtime
    commercial
  quality
    narrative
    explanation
    action
    executive
    domain
    temporal
    runtime
    export
    consulting
  commercial_checks             # §37
  consumer_parity
    portal
    pdf
    docx
    api
    consulting
  golden_case_id
```

Engineering / QA / release only.

---

# 33. VERIFICATION ERRORS

Examples:

```text
Truth mismatch
Priority mismatch
Narrative contradiction
Presentation inconsistency
Optimization inconsistency
```

Additional:

```text
Executive does not match P0
Action missing Why / Condition
Export-only finding
Consulting invents a domain
Temporal rewrites natal
Commercial cut hides Top bottleneck
```

```text
VerificationError
  source                        # VerificationGraph node
  target
  rule                          # e.g. CVF-V0-01
  severity                      # critical | major | minor
  level                         # V0 … V5
  field_path
  expected
  actual
  trace                         # VerificationTrace
```

Every error MUST expose trace (CVF-09).

---

# 34. VERIFICATION WARNINGS

Examples:

```text
Optional omission
Low confidence
Presentation wording
```

Additional:

```text
expert layer omitted in compact PDF while commercial IDs match
temporal not_evaluated because luck was not requested
supporting DI-08 domain not_evaluated
confidence wording softer than expert, IDs match
```

Warnings MUST NOT hide Pattern / Grade / P0 mismatch.

---

# 35. QUALITY LEVELS (VERDICTS)

Suggested and frozen:

```text
PASS
PASS_WITH_WARNINGS
FAIL_MINOR
FAIL_MAJOR
FAIL_CRITICAL
```

Same cascade as DI-21:

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
FAIL_MINOR                    analytical publish allowed if V0–V3 passed; presentation/commercial adapters blocked until catalogs align
FAIL_MAJOR / FAIL_CRITICAL    do not publish as canonical
```

Do not invent a separate commercial verdict that can PASS while V0 fails.

---

# 36. GOLDEN DATASET

Golden **end-to-end verification cases**.

They store the chain, not a final paragraph.

Minimum cases:

```text
full natal chain MC-01 → meaning → six domains → optimization → narrative → contract → projections
creation high / retention low through meaning, narrative, commercial cut, PDF, API
Career High + Relationship Low both visible as Top risks/strengths as contracted
unresolved Pattern: every consumer and commercial cut stay unresolved
P0 Damage + Rescue both present in executive; Damage not deleted
Optimization Top 3 = Narrative Top 3 = commercial Top 3
Authority → Career → Optimization → Narrative connected on one Pattern
luck_cycle + annual: natal objects identical except temporal / new analysis_id
Portal / PDF / DOCX / API / Consulting same analysis_id and meaning hashes
empty Optimization: commercial cut does not invent a life-coach list
low MC-01 confidence: no high-confidence commercial slogans
```

Each Golden case MUST include:

```text
upstream facts
MC-01 structural findings
Pack 07 objects
CanonicalRuntimeResult hash
ConsistencyResult verdict
projection hashes
commercial-cut node IDs (strengths / risks / bottlenecks / actions)
accepted presentation omissions
forbidden conclusions
expert notes
```

Do not store only a final Vietnamese paragraph.

Do not tune expected copy from customer biography.

Do not edit Golden Dataset to make tests pass.

---

# 37. NEGATIVE TESTS

Must prove:

```text
Narrative cannot invent.
Optimization cannot rerank.
Presentation cannot rewrite.
Commercial cannot contradict.
```

Additional required negatives:

```text
Executive cannot lead with Shen Sha over P0
PDF cannot add a finding
API cannot fork Grade
Consulting cannot create a new action
Temporal cannot lower natal Grade
Top 3 cannot be padded
“tài vận toàn diện tốt” cannot pass creation/retention split
screenshot-only Golden cannot pass
string-contains job-title test cannot pass as CVF acceptance
```

Each negative MUST emit `VerificationError` with source, target, rule, severity, and trace.

---

# 38. COMMERCIAL CHECKS

Verify:

```text
Top strengths visible.
Top risks visible.
Top bottlenecks visible.
Top actions visible.
```

```text
CVF-CM-01  If Optimization / Evidence Priority publishes a Top strength, commercial cut includes it (or documents allowed compact omission that does not invert rank).
CVF-CM-02  Top risks visible in commercial cut.
CVF-CM-03  Top bottlenecks visible; P0 bottleneck cannot be omitted from executive.
CVF-CM-04  Top actions visible; IDs match Optimization.
CVF-CM-05  Visibility means structured node / field presence, not a particular font.
```

Compact mode may shorten wording. It may not drop P0 or invert Top 3.

---

# 39. ACCEPTANCE INVARIANTS

At minimum:

```text
CVF-01  Truth preserved.
CVF-02  Meaning preserved.
CVF-03  Domains preserved.
CVF-04  Optimization preserved.
CVF-05  Narrative preserved.
CVF-06  Runtime preserved.
CVF-07  Presentation preserved.
CVF-08  Commercial quality preserved.
CVF-09  Trace required.
CVF-10  Deterministic.
```

Additional:

```text
CVF-11  Levels V0–V5 are complete and ordered.
CVF-12  One VerificationGraph per analysis_id.
CVF-13  Commercial node has no independent facts.
CVF-14  Isolated unit tests are not sufficient acceptance.
CVF-15  SYS-01 … SYS-18 and CRC-01 … CRC-12 remain binding.
CVF-16  Executive matches P0.
CVF-17  Every action maps to Driver or Bottleneck or Leakage.
CVF-18  Unknown versions fail closed.
```

Determinism:

```text
Same CanonicalRuntimeResult + same projection bytes + same ConsistencyResult
      = same CanonicalVerificationResult verdict, errors, and rule IDs
      (created_at excluded if specified)
```

No LLM in the verification path.

No biography.

---

# 40. FAILURE CONDITIONS

This specification FAILS if:

```text
Truth changes.
Meaning changes.
Priority changes.
Optimization changes.
Narrative contradicts.
Presentation mutates.
Commercial output misleading.
```

Also FAIL if:

```text
this framework publishes a second runtime contract
V5 can PASS while Pattern mismatches
Golden Dataset is edited to match bad copy
verification treats module unit tests as end-to-end proof
Consulting becomes a second analysis
Temporal rewrites Natal
```

“Changes” here means **relative to published canonical objects** for that `analysis_id`, not that Product Owner may never version a ruleset. A new ruleset produces a new `analysis_id`.

---

# 41. OWNERSHIP

MC-01 owns structural truth and MC-01 tests.

DI-21 owns global ID / continuity consistency.

This framework owns **end-to-end reasoning verification** and **commercial-cut quality** of the same contract.

It does not take ownership of Pattern calculation or Portal layout.

---

# 42. VERSIONING

```text
bte.detailed_interpretation.verification.v1
```

Sits beside, does not replace:

```text
bte.detailed_interpretation.system_consistency.v1
bte.detailed_interpretation.runtime_contract.v1
bte.detailed_interpretation.composer.v1
bte.mingju.decision.v1
```

Breaking changes to V0–V5, VerificationGraph nodes, or verdict enum require a new major version.

---

# 43. FREEZE TARGET

Frozen:

1. Verification levels V0–V5.
2. Reasoning chain: MC-01 → Meaning → Domains → Optimization → Narrative → Runtime → Presentation.
3. VerificationGraph nodes and edges (`verified_by`, `must_match`).
4. Quality rules in this document (narrative, explanation, action, executive, domain, temporal, runtime, export, consulting).
5. Commercial rules (continuity, V5, commercial checks).
6. CanonicalVerificationResult / CanonicalVerificationReport.
7. Invariants CVF-01 … CVF-18.

Not frozen:

- exact Python dataclasses
- pytest file layout
- HTTP of a verification endpoint
- Vietnamese catalog strings
- DI-23 checklist item numbering in code

---

# 44. NEXT DOCUMENT

Next:

```text
23_ACCEPTANCE_CHECKLIST.md
```

That document must turn this framework, DI-21 consistency, and DI-20 contract into an acceptance checklist.

It MUST NOT invent a second runtime contract.

It MUST NOT weaken V0–V5 or commercial checks.

Architecture listed `22_TEST_STRATEGY.md` and `23_ACCEPTANCE_CHECKLIST.md`. This Product Owner file is the DI-22 verification framework. Do not edit DI-21 to retarget filenames.

Do not write DI-23 until Product Owner approval.

---

# 45. COMPLIANCE NOTES

1. Verification levels V0–V5 all exist, including Commercial Verification (V5).
2. VerificationGraph exists with Truth / Meaning / Domains / Optimization / Narrative / Runtime / Presentation / Commercial.
3. End-to-end chain is the acceptance bar; isolated modules are not enough.
4. MC-01 Pattern / Integrity / Grade / Achievement / Career / Wealth / Authority remain canonical references.
5. Next document name is `23_ACCEPTANCE_CHECKLIST.md`.
