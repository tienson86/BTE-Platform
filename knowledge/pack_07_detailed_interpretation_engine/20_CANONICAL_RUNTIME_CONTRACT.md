# PACK 07 — CANONICAL RUNTIME CONTRACT

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-20  
**Document:** `20_CANONICAL_RUNTIME_CONTRACT.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `19_NARRATIVE_COMPOSER_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially `12_PUBLIC_API.md`  
**Schema target:** `bte.detailed_interpretation.runtime_contract.v1`  
**Related schemas:**

- `bte.detailed_interpretation.context.v1`
- `bte.detailed_interpretation.result.v1`
- `bte.detailed_interpretation.composer.v1`
- `bte.mingju.decision.v1`

This document defines the **single canonical runtime contract** used by every consumer of Pack 07.

Architecture listed `20_PUBLIC_API.md` to freeze function signatures. DI-19 pointed to that name. This Product Owner target authors `20_CANONICAL_RUNTIME_CONTRACT.md` as the **published result contract** plus conceptual API/export/consulting projections. Architecture and DI-01–DI-19 remain immutable.

Exact HTTP paths and Python signatures are conceptual. This document does **not** implement runtime.

---

# 1. PURPOSE

Define the single canonical runtime contract for every consumer of Pack 07.

This contract becomes the only runtime truth for:

```text
Portal
PDF
DOCX
API
AI Consulting
Future Mobile
Future Desktop
Future integrations
```

Downstream consumers MUST NOT reconstruct detailed interpretation independently.

---

# 2. CORE PRINCIPLE

Frozen:

```text
ONE ANALYSIS
      ↓
ONE CONTRACT
      ↓
MANY PRESENTATIONS
```

Never:

```text
Many contracts
      ↓
Many truths
```

Parity (architecture):

```text
CanonicalRuntimeResult
= shared source for Portal / Report / PDF / DOCX / Consulting / API
```

Labels may differ by density. Meaning must not.

---

# 3. SCOPE

In scope:

1. CanonicalRuntimeResult / CanonicalAnalysisResult
2. Contract layers and ownership
3. Identity vs MC-01 reference vs Pack 07 layers
4. No-duplication rules
5. Consumer and presentation boundaries
6. CanonicalExportModel / CanonicalAPIModel / CanonicalConsultingModel
7. History, analysis_id, immutability
8. Versioning
9. RuntimeContractValidation (concept; details DI-21)
10. Conceptual publish/analyze/compose entry points
11. Golden, negative tests, invariants

Out of scope:

```text
implementing services
HTTP framework choice
PDF layout
validation rule tables          → 21_VALIDATION_RULES.md
test cases in code              → later test strategy
rewriting MC-01 API
```

---

# 4. NON-SCOPE

This contract MUST NOT:

1. Recalculate MC-01 or Pack 07 engines
2. Duplicate Pattern / Grade / Integrity into Pack 07 objects
3. Put CSS, grid, typography, or card layout in analytical layers
4. Let Portal/PDF/DOCX/API mutate published truth
5. Let Narrative or Optimization write back Pattern or Grade
6. Store fragmented sub-results as the historical source of truth
7. Invent a second analysis_id per surface
8. Mix natal rewrite from luck at the contract root

---

# 5. CANONICAL RUNTIME MODEL

Canonical published object:

```text
CanonicalRuntimeResult
```

Alias (same object family):

```text
CanonicalAnalysisResult
```

Purpose:

```text
Represent the complete interpreted chart
as one immutable published analysis.
```

It is the assembly of already-computed layers. It is not a new calculator.

---

# 6. CONTRACT LAYERS

Canonical layers:

```text
Identity
      ↓
MC-01 Structural Truth          # reference
      ↓
Detailed Interpretation         # Pack 07 structured findings
      ↓
Life Domains
      ↓
Temporal
      ↓
Optimization
      ↓
Narrative
```

No presentation data belongs inside analytical layers.

Forbidden inside `mc01` / `interpretation` / `domains` / `temporal` / `optimization`:

```text
font
color token
card collapsed
PDF page break
React component name
```

Those belong only to presentation adapters that **read** the contract.

---

# 7. ROOT OBJECT

```text
CanonicalAnalysisResult / CanonicalRuntimeResult

  identity
  chart                         # identity-only chart handle; not a second BaZi engine
  mc01                          # reference (see §9)
  interpretation                # Pack 07 structured interpretation
  domains
  temporal
  optimization
  narrative
  metadata
```

Optional attachments (not second truths):

```text
mc01_snapshot                 # immutable byte-stable copy of referenced MingJuDecisionResult
context_ref                   # DetailedInterpretationContext id/hash
```

If `mc01_snapshot` is attached, its content hash MUST equal `mc01.content_hash`. It is a portable freeze of the **same** MC-01 result, not a rewritten Pattern.

---

# 8. IDENTITY

Contains only immutable chart identity.

No interpretation.

```text
identity
  chart_id
  person_label_ref              # opaque; not biography text required
  birth_civil                   # as already canonical in chart identity
  calendar_system_ref
  gender_or_party_ref           # canonical chart-party only if upstream owns it
  hour_completeness
  timezone_ref                  # consumed; this contract does not convert
```

Forbidden:

```text
identity.occupation
identity.known_wealth
identity.marital_status as inference
identity.health_history
```

---

# 9. MC-01 SECTION

**Reference only. Never duplicate as a second structural engine.**

```text
mc01
  mingju_result_id
  schema_version                # bte.mingju.decision.v1
  ruleset_version
  content_hash
  status                        # copied pointer to MC-01 status
```

Pack 07 layers MUST NOT copy:

```text
Pattern
Purity
Pattern Strength
Damage
Rescue
Integrity
Grade
Achievement scores
Wealth Profile scores
Career Profile scores
```

into `interpretation` or `domains` as independently writable fields.

Consumers that need Grade read `mc01` (or the attached snapshot). They must not read a forked `narrative.grade`.

MC-01 Composer Mệnh Cục summary, if present, is referenced under MC-01 ownership (`bte.mingju.composer.v1`), not rewritten here.

---

# 10. INTERPRETATION SECTION

Contains Pack 07 **structured interpretation**.

No UI formatting.

```text
interpretation
  ten_gods                      # refs to DI-01..04 results
  shen_sha                      # refs to DI-05..06
  evidence_priority             # DI-07
  status
  confidence
  trace_ids[]
```

This is meaning **structure**, not Vietnamese paragraphs.

Narrative lives in `narrative`.

---

# 11. DOMAIN SECTION

```text
domains
  authority                     # DI-12 + DI-08 authority
  career                        # DI-13
  wealth                        # DI-14
  relationship                  # DI-15
  legacy                        # DI-16
  vitality                      # DI-17
```

Each child is the published detailed result (or `not_evaluated` / `unresolved`).

Additional DI-08 domains (leadership, management, creative, academic, learning, personal_growth, children, health) MAY appear as supporting keys. They MUST NOT duplicate Authority/Career/Wealth/Vitality as a second score.

Each domain exists **once**.

---

# 12. TEMPORAL SECTION

```text
temporal
  luck_activation               # DI-09
  luck_interaction              # DI-10
  temporal_activation           # DI-11
  requested_layers[]
  time_windows{}
```

Natal objects in `domains` / `mc01` remain immutable here.

If luck was not requested:

```text
temporal.status = not_evaluated | not_applicable
```

Natal contract may still be complete.

---

# 13. OPTIMIZATION SECTION

```text
optimization
  = LifeOptimizationResult      # DI-18, once
```

Optimization cannot modify Grade, Pattern, or domain natal states.

If not evaluated:

```text
optimization.status = not_evaluated
```

---

# 14. NARRATIVE SECTION

```text
narrative
  graph                         # NarrativeGraph
  result                        # NarrativeResult
  executive_summary
  layers
    commercial
    technical
    expert
    executive                   # one-minute cut of the same graph
```

Narrative cannot modify Pattern or any analytical field.

All layers are projections of one NarrativeGraph (DI-19).

Missing layer = not requested, not a second analysis.

---

# 15. METADATA

```text
metadata
  contract_version              # bte.detailed_interpretation.runtime_contract.v1
  schema_version
  ruleset_version
  composer_version
  analysis_id
  created_at                    # publication timestamp; MUST NOT feed natal calculation
  locale
  requested_layers[]
  confidence_summary
  source_versions{}
  content_hash
```

`created_at` is audit metadata.

Natal MC-01 / Pack 07 natal objects MUST NOT change because `created_at` is 2026 vs 2030 (MC-01 API freeze extended here).

Temporal sections depend on **requested time windows**, not on wall-clock leakage into natal fields.

---

# 16. CONTRACT OWNERSHIP

MC-01 owns:

```text
Pattern
Grade
Integrity
Achievement
Wealth Profile
Career Profile
Damage / Rescue / Support / Purity / Pattern Strength
Useful God compatibility / climate compatibility as MC-01 evaluated them
```

Pack 07 owns:

```text
Meaning
Narrative
Optimization
Temporal explanation
Detailed domain interpretation
```

Upstream engines still own Calendar, BaZi, Five Elements, Strength, Temperature, Useful God identity, luck-cycle construction, Shen Sha detection.

This contract **assembles** those owned results. It does not steal ownership.

---

# 17. NO DUPLICATION

The contract must never duplicate as parallel writable truths:

```text
Pattern
Grade
Domains
Optimization
Narrative
```

Each exists once.

Forbidden:

```text
domains.authority.grade = S
narrative.pattern.primary = zheng_guan   # writable fork
optimization.new_grade
pdf_model.pattern vs api_model.pattern with different values
```

Allowed:

```text
narrative block evidence_ids pointing at mc01 / domains
export view selecting narrative.executive_summary
```

Pointers and projections are not duplication of truth.

---

# 18. RUNTIME CONSUMERS

```text
Portal        → reads contract
PDF           → reads contract
DOCX          → reads contract
API           → reads contract
Consulting    → reads contract
Mobile/Desktop/future → reads contract
```

No consumer recalculates interpretation.

Forbidden consumer logic:

```text
if zheng_guan and grade == A:
    text = "làm quan lớn"
```

Frontend may map enums to Vietnamese labels from the message catalog already bound in `narrative`. Frontend may not invent conclusions.

---

# 19. PRESENTATION LAYERS

Presentation may:

```text
hide
collapse
expand
reorder visually
```

Never:

```text
rewrite
reinterpret
rerank
```

Visual reorder of cards MUST NOT change `EvidencePriorityResult` or `ranked_domains` inside the contract.

If Portal hides Expert layer, Expert data remains in the published contract for API/Consulting.

---

# 20. EXPORT MODEL

Canonical:

```text
CanonicalExportModel
```

Shared by:

```text
PDF
DOCX
Future PPT
Future HTML
```

```text
CanonicalExportModel
  analysis_id                   # same
  contract_ref
  selected_layer                # commercial | technical | expert | executive
  section_order[]               # presentation order only
  included_block_ids[]          # subset of NarrativeGraph
  locale
```

Export adapters **select** nodes. They MUST NOT compose new findings.

Unresolved domains stay unresolved in PDF. No guessed paragraph in PDF only.

---

# 21. API MODEL

Canonical:

```text
CanonicalAPIModel
```

Purpose: stable machine interface.

Preferred shape: `CanonicalRuntimeResult` itself (or a versioned envelope around it).

```text
CanonicalAPIModel
  analysis_id
  contract                      # CanonicalRuntimeResult
```

Conceptual publish path (architecture; signatures not implementation-frozen):

```text
context = build_detailed_interpretation_context(...)
analyzed = analyze_detailed_interpretation(context)
composed = compose_detailed_interpretation(analyzed)
published = publish_canonical_runtime_result(analyzed, composed, mc01_ref)
```

Composer must never receive raw BaZi as a substitute for analyzed results.

Unknown `contract_version` MUST fail explicitly. Do not silently fall back.

Do not expose two HTTP resources that compute different Pack 07 logic for the same analysis_id.

---

# 22. CONSULTING MODEL

Canonical:

```text
CanonicalConsultingModel
```

Purpose:

```text
AI consulting
human consulting
follow-up dialogue
without re-analysis
```

```text
CanonicalConsultingModel
  analysis_id
  contract_ref
  default_layer = expert
  allowed_operations
    retrieve_block
    retrieve_trace
    retrieve_evidence
    retrieve_optimization_action
  forbidden_operations
    recompute_pattern
    rerank_evidence
    invent_action
    mutate_contract
```

Follow-up dialogue MAY filter the graph. It MUST NOT run a second Pack 07 analysis unless a **new** `analysis_id` is explicitly created from a new context.

LLM consulting, if any, consumes this model **after** canonical composition (DI-19). It must not replace the contract.

---

# 23. HISTORY MODEL

History stores:

```text
CanonicalRuntimeResult
```

not fragmented sub-results as the source of truth.

Allowed indexes:

```text
analysis_id
chart_id
created_at
content_hash
```

Forbidden history design:

```text
store only PDF text
store Portal card JSON as the analysis
rehydrate interpretation from DOCX
```

---

# 24. RESULT IDENTITY

One:

```text
analysis_id
```

through every layer and every consumer.

```text
identity.analysis_id
= metadata.analysis_id
= export.analysis_id
= api.analysis_id
= consulting.analysis_id
= history key
```

A new luck window or ruleset version produces a **new** `analysis_id` (or a child run id that still points at natal `analysis_id` without mutating it). Natal MC-01 id remains the `mingju_result_id` reference.

---

# 25. IMMUTABILITY

After a runtime result is **published**:

```text
Presentation layers must not mutate it.
```

Copy / adapt / view-model (MC-01 API rule):

```text
canonical result → adapter / view model
NOT canonical result mutated for UI
```

Patches require a new published result with a new `analysis_id` / `content_hash`.

---

# 26. VERSIONING

Define:

```text
contract_version              # this document’s schema
schema_version                # Pack 07 result family
ruleset_version
composer_version
```

Breaking semantic changes require a new major `contract_version`.

Adapters consume MC-01 by reference rather than renaming MC-01 fields under new Pack 07 names.

---

# 27. CONTRACT VALIDATION

Canonical:

```text
RuntimeContractValidation
```

Concept (details in DI-21), aligned with architecture:

```text
Input Contract Validation
Stage-Level Validation
Cross-Stage Validation
Reference Integrity Validation
Semantic Invariant Validation
Serialization Validation
Determinism Validation
```

Must distinguish technical invalidity from domain uncertainty.

Unknown version → explicit fail.

`unresolved` domains must serialize; they are not HTTP 500 (MC-01 API spirit).

---

# 28. CONTRACT RESULT FIELDS

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

`chart` may sit under `identity` or as a sibling identity-only handle. It is not a second calendar engine.

---

# 29. GOLDEN DATASET

Golden **runtime snapshots** of `CanonicalRuntimeResult` (hashes / fixtures), not PDF screenshots as truth.

Minimum cases:

```text
natal-only complete (temporal not_evaluated)
natal + luck_cycle + annual
unresolved Pattern still serializes
creation/retention split present once
Career High + Relationship Low both present
Optimization Top 3 match optimization section
Narrative evidence_ids resolve to interpretation/domains/mc01
same inputs → same content_hash (excluding created_at if so specified)
```

Do not treat Golden Dataset as editable expected prose to make tests pass.

---

# 30. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Portal cannot alter truth
PDF cannot alter truth
DOCX cannot alter truth
API cannot alter truth
```

Additional:

```text
Consulting dialogue cannot mutate contract
Export subset cannot add findings
two endpoints cannot yield two Patterns for one analysis_id
narrative cannot write Grade
optimization cannot write Grade
mc01 fields not forked into domains
```

---

# 31. ACCEPTANCE INVARIANTS

```text
CRC-01 One contract.
CRC-02 One analysis_id.
CRC-03 No duplicated truth.
CRC-04 Presentation cannot modify.
CRC-05 Narrative cannot modify.
CRC-06 Optimization cannot modify.
CRC-07 Deterministic.
CRC-08 Traceable.
```

Additional:

```text
CRC-09 MC-01 is referenced, not recalculated or forked.
CRC-10 Unknown contract_version fails closed.
CRC-11 History stores CanonicalRuntimeResult.
CRC-12 Views (export/API/consulting) are projections of the same analysis_id.
```

---

# 32. FAILURE CONDITIONS

This specification FAILS if:

```text
Portal recalculates
PDF recalculates
DOCX recalculates
Narrative changes Pattern
Optimization changes Grade
Two conflicting contracts exist
analysis_id differs across PDF and Portal for the same publish
created_at mutates natal MC-01
```

---

# 33. DETERMINISM

```text
Same context + same ruleset + same composer version + same requested layers
= same CanonicalRuntimeResult content_hash
```

`created_at` may differ across publications if explicitly excluded from `content_hash`. Analytical bytes must not.

No LLM in publish path.

No biography.

---

# 34. VERSIONING NAMESPACE

```text
bte.detailed_interpretation.runtime_contract.v1
```

Sits beside, does not replace:

```text
bte.detailed_interpretation.result.v1
bte.detailed_interpretation.composer.v1
bte.mingju.decision.v1
```

---

# 35. FREEZE TARGETS

Frozen:

1. CanonicalRuntimeResult as the one published analysis.
2. CanonicalExportModel / CanonicalAPIModel / CanonicalConsultingModel as projections, not new truths.
3. Contract ownership: MC-01 structural; Pack 07 meaning / narrative / optimization / temporal explanation.
4. Presentation may hide/collapse/expand/reorder visually; never rewrite/reinterpret/rerank.
5. One `analysis_id` through every layer.
6. Immutability after publish.
7. MC-01 reference-only (snapshot only as hash-identical attachment).
8. Invariants CRC-01 … CRC-12.

Not frozen:

- exact HTTP routes
- exact Python dataclasses
- storage engine
- DI-21 validation tables

---

# 36. NEXT DOCUMENT

Next:

```text
21_VALIDATION_RULES.md
```

That document must specify validation layers for this contract and Pack 07 results.

It MUST NOT invent a second runtime contract.

It MUST distinguish technical invalidity from domain uncertainty.

Do not write DI-21 until Product Owner approval.
