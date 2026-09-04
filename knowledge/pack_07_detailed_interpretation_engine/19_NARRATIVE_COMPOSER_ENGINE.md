# PACK 07 — NARRATIVE COMPOSER ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-19  
**Document:** `19_NARRATIVE_COMPOSER_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `18_LIFE_OPTIMIZATION_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.composer.v1`  
**Message catalog:** `bte.detailed_interpretation.messages.vi.v1`  
**Depends on schemas:**

- `bte.mingju.decision.v1`
- `bte.mingju.composer.v1`                    # consume, do not overwrite
- `bte.detailed_interpretation.evidence_priority.v1`
- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.temporal_activation.v1`
- `bte.detailed_interpretation.life_optimization.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1`

This document defines the canonical **Narrative Composer Engine**.

It transforms structured evidence into coherent narrative.

Composer does **NOT** infer.

Composer organizes, prioritizes (by consuming rank), explains, and communicates.

Architecture listed `19_INTERPRETATION_COMPOSER.md`. DI-18 pointed to the same name. This Product Owner target authors `19_NARRATIVE_COMPOSER_ENGINE.md`. Architecture and DI-01–DI-18 remain immutable.

MC-01 Decision Composer remains responsible for the **Mệnh Cục executive summary**. This Composer is responsible for **detailed Pack 07 narrative**. They must not contradict each other.

---

# 1. PURPOSE

Create the canonical **Narrative Composer Engine**.

Purpose:

```text
Transform structured evidence into coherent narrative.
```

```text
Composer does NOT infer.
Composer organizes.
Composer prioritizes.          # by consuming Evidence Priority, not by inventing rank
Composer explains.
Composer communicates.
```

The customer-facing language is Vietnamese.

Engine analytical IDs remain English.

Calculation must never depend on wording.

---

# 2. CORE PRINCIPLE

Frozen:

```text
Truth
      ↓
Meaning
      ↓
Narrative
```

NOT:

```text
Narrative
      ↓
Truth
```

Strict separation (architecture / MC-01 spirit):

```text
Detailed Interpretation Engines
= determine structured findings

Narrative Composer
= communicates findings
```

Forbidden:

```text
Composer sees Chính Quan → "sẽ làm quan lớn"
Composer sees Hồng Loan → "năm nay kết hôn"
Composer sees low recovery → "bệnh gan"
Composer sees Career High + Relationship Low → "cuộc sống hỗn hợp, trung bình"
```

---

# 3. SCOPE

In scope:

1. NarrativeGraph and NarrativeBlock
2. Story flow
3. Narrative layers (Commercial, Technical, Expert, Executive)
4. Executive summary, strengths, risks, opportunities, actions
5. Domain narratives
6. Temporal summary
7. Optimization integration
8. Priority consumption (no rerank)
9. Confidence / uncertainty language
10. Deduplication
11. Contradiction preservation
12. Output modes: Portal, PDF, DOCX, Consulting, API from one graph
13. Golden, negative tests, invariants

Out of scope:

```text
Public API signatures                 → 20_PUBLIC_API.md
recalculating any engine
LLM as canonical composer
Portal layout / typography
rewriting MC-01 Composer
runtime code
```

---

# 4. NON-SCOPE

The Narrative Composer MUST NOT:

1. Calculate Pattern, Purity, Strength, Damage, Rescue, Integrity, or Grade
2. Recalculate Achievement / Wealth / Career
3. Rerank Evidence Priority
4. Invent Ten God combinations, domains, or actions
5. Promote Shen Sha over structure
6. Rewrite natal conclusions from luck
7. Use biography
8. Add medical, marital, or wealth guarantees
9. Create PDF-only conclusions that Portal does not have
10. Hide uncertainty
11. Ignore bottlenecks
12. Duplicate the same evidence as multiple independent claims
13. Average Career High and Relationship Low
14. Receive raw BaZi facts as a substitute for structured Pack 07 / MC-01 results
15. Invent Top 3 actions missing from `LifeOptimizationResult`

---

# 5. INPUTS

Consume:

```text
MC-01                         MingJuDecisionResult
                              (+ MC-01 composed Mệnh Cục summary if present, read-only)
Evidence Priority             EvidencePriorityResult
Domains                       DomainInterpretationSet
                              + detailed Authority / Career / Wealth / Relationship / Legacy / Vitality
Temporal                      TemporalActivationResult
                              + LuckActivation / LuckInteraction as already packaged
Optimization                  LifeOptimizationResult
```

Nothing else.

“Nothing else” means:

```text
no CRM biography
no known income / marriage / illness
no raw pillar dictionary as a second engine
no LLM world knowledge
no frontend card state
```

DI-07 stated Composer consumes ranking **only from** Evidence Priority. That freeze stands: this Composer **does not rerank**.

Domain, Temporal, and Optimization objects are legal inputs because they already embed ranked `evidence_ids`. They are meaning / action projections of that ranked evidence, not a second ranking engine.

If Composer needs a fact that is in none of these objects, **fix the upstream engine**, not Composer.

Composer must never receive raw BaZi as a substitute for `DetailedInterpretationResult` (architecture).

---

# 6. OUTPUT

Canonical:

```text
NarrativeResult
```

and:

```text
NarrativeGraphResult
```

Recommended architecture alias (same object family):

```text
DetailedComposedInterpretation
```

Do not fork a second composer schema.

---

# 7. NARRATIVE GRAPH

Canonical:

```text
NarrativeGraph
```

**Nodes** (block types):

```text
executive_summary
strength
risk
opportunity
bottleneck
action
temporal
supporting_evidence
domain_section
optimization_section
closing_summary
```

**Edges:**

```text
supports
explains
qualifies
contrasts
expands
summarizes
```

Example:

```text
executive_summary  summarizes   strength + risk + action
strength           explains     authority domain
risk               qualifies    wealth creation
creation_strength  contrasts    retention_risk
action             supports     retention bottleneck
temporal           qualifies    natal wealth strength
```

Portal / PDF / DOCX / Consulting / API render this **same graph**. They may hide nodes by layer/mode. They must not add nodes.

---

# 8. EXECUTIVE SUMMARY

Top-level narrative.

Should answer:

```text
Who is this chart?
What matters most?
What should be prioritized?
```

Sources:

```text
MC-01 Pattern / Integrity / Grade (wording must not contradict MC-01 Composer)
DI-07 ranked_domains and P0 findings
Life Optimization Top 1–3 if present
```

Must lead with P0 structure, not Shen Sha.

Must not be “làm quan lớn” from Chính Quan name.

If Pattern is unresolved, the executive summary MUST say uncertainty. Do not fake a type.

Executive **layer** (§14) is a one-minute cut of this node, not a different truth.

---

# 9. STORY FLOW

Recommended order:

```text
Executive
      ↓
Strength
      ↓
Risk
      ↓
Opportunity
      ↓
Life Domains
      ↓
Temporal
      ↓
Optimization
      ↓
Summary
```

Composer MUST follow this flow for the default detailed narrative.

A layer may **compress** sections (Executive layer may stop after Executive + Top 3). It MUST NOT reorder P0 below Shen Sha or put Optimization before risks when those risks are P0 bottlenecks.

Life Domains follow `EvidencePriorityResult.ranked_domains` / DomainInterpretationSet.order, not an aesthetic template.

---

# 10. NARRATIVE PRIORITY

Must consume Evidence Priority Engine.

Composer must not rerank evidence.

```text
ranked_domains + within-tier rank
      ↓
section order and sentence order
```

Forbidden:

```text
sort by star count
lead with Hồng Loan
drop P0 Damage because Rescue exists
promote P4 blocked cluster into the headline
rerank domains because luck is loud
```

---

# 11. NARRATIVE LAYERS

Support at least:

```text
commercial
technical
expert
executive
```

These are **density / vocabulary modes** on one NarrativeGraph.

They are not four different analyses.

Architecture `ComposerMode.COMMERCIAL` plus compact/standard/detailed maps as:

```text
executive     ≈ compact one-minute
commercial    ≈ customer commercial (default)
technical     ≈ standard structural vocabulary
expert        ≈ detailed + Pattern / Damage / Rescue / chains / trace
```

Frontend may choose a layer. Frontend may not invent a fifth truth.

---

# 12. COMMERCIAL LAYER

Simple. Action-oriented. Customer friendly.

Uses capability / fit / condition language.

Avoids unexplained jargon (unless a label map exists).

Still must keep splits (creation vs retention).

Still must not guarantee outcomes.

---

# 13. TECHNICAL LAYER

Uses structural terms.

Shows mechanisms:

```text
Output → Wealth
Tài sinh Quan (only if confirmed)
bottleneck
leakage
activation vs capability
```

Does not recalculate those mechanisms.

---

# 14. EXPERT LAYER

May expose:

```text
Pattern
Integrity
Damage
Rescue
Chains
Evidence
Trace
```

Still must not invent IDs.

Still must not contradict MC-01.

Trace IDs are attachable to every major block.

---

# 15. EXECUTIVE LAYER

Maximum **one-minute** summary.

Typically:

```text
executive_summary
+ top strengths (few)
+ top risks (few)
+ top actions (≤3 from Life Optimization)
```

Must still include P0 bottleneck if one exists.

Must not omit unresolved Pattern.

---

# 16. NARRATIVE BLOCK

Canonical:

```text
NarrativeBlock
```

Fields:

```text
block_id
block_type
priority                      # copied from EPR / Optimization; not recomputed
title                         # message key
summary                       # message key or composed string from keys
details                       # optional expansion keys
evidence_ids[]
trace_ids[]
confidence
qualifiers[]                  # uncertainty / condition keys
layer_visibility              # which layers include this block
```

Vietnamese text is produced from message keys + locale catalog.

Do not store free-form LLM paragraphs as canonical truth.

---

# 17. TOP STRENGTHS

Automatically generated from:

```text
Evidence Priority (composer_visible strengths / driver / support groups)
Domains (strengths[] / driver)
```

Order follows EPR, not “most flattering first”.

Do not turn a high-confidence Shen Sha into Top Strength above Pattern.

---

# 18. TOP RISKS

From:

```text
Damage
Leakage
Bottlenecks
Stress
Optimization avoid / P0 safety
```

Rescue does not delete Damage from Top Risks. Both may appear: risk + condition.

---

# 19. TOP OPPORTUNITIES

From:

```text
Drivers
Activation (temporal, labeled as activation)
Career
Wealth
Legacy
Optimization develop / opportunity actions
```

Peak luck is opportunity of **expression**, not a new natal strength.

---

# 20. TOP ACTIONS

Consume Life Optimization Engine.

```text
top_priorities[] from LifeOptimizationResult
```

Composer MUST NOT invent a fourth action to fill a template.

Composer MUST NOT drop contraindications.

If Optimization is `unresolved` / `not_evaluated`, the Optimization section is omitted or states insufficient plan — not generic life-coach advice.

---

# 21. TEMPORAL SUMMARY

Summarize **current activation**.

Not fate.

Must keep layers:

```text
natal_layer
activation_layer
situation_layer                 # DI-10 Life Situation if present
```

Example meaning (keys, not slogans):

```text
strong natal authority
weak current expression
```

Forbidden:

```text
because this year is bad, natal authority is low
will marry this year
Grade becomes S
```

If temporal is `not_evaluated`, skip the Temporal section. Natal narrative remains complete.

---

# 22. DOMAIN NARRATIVES

One section each (when the domain is resolved in the set):

```text
Authority
Career
Wealth
Relationship
Legacy
Vitality
```

Additional DI-08 domains (Leadership, Management, Creative, Academic, Learning, Personal Growth, Children, Health) may appear as subsections or supporting blocks if EPR ranks them and the selected layer includes them.

Do not invent a domain the set did not emit.

Each domain section MUST:

```text
follow that domain's detailed result
keep splits (Wealth creation vs retention)
keep Authority ≠ Career ≠ Leadership ≠ Management
not predict office / marriage / children count / disease
attach evidence_ids
```

Order = ranked_domains, not this list’s aesthetic order.

---

# 23. NARRATIVE TONE

```text
Professional
Evidence-based
No exaggeration
No mysticism
```

Forbidden tone:

```text
Thiên mệnh đã định
Quý nhân đảm bảo
Chắc chắn giàu
Số làm quan
```

Consultant, not calculator-mystic (Brand / Experience Principles: trust → understanding → action).

---

# 24. NO CONTRADICTIONS HIDDEN

If:

```text
Career High
Relationship Low
```

Both remain.

Composer explains the trade-off **using DI-10 / OptimizationConflict if present**.

If no interaction finding exists, state both facts without inventing “career causes divorce”.

Do not collapse into “cuộc sống trung bình”.

---

# 25. NO DUPLICATION

Repeated evidence appears **once** as a claim.

Later sections may **reference** (`explains` / `expands` edges) that claim. They must not restate it as a new independent finding.

Example:

```text
P0 hurting_officer_attacks_officer
appears in Top Risks
Authority section expands it
Wealth section must not introduce a second “Quan bị phá” as if new
```

Causal groups from DI-07 / DI-02 must stay merged.

---

# 26. EXPLANATION MODEL

Every major statement answers **Why?**

Weak:

```text
Tài vận khá.
```

Required direction:

```text
Khả năng tạo tiền khá mạnh because Output generates Wealth and Wealth has root,
but retention is weaker because Peer pressure remains significant.
```

`because` must bind `evidence_ids`.

If no why is available, do not emit the claim. Fix upstream.

---

# 27. CONFIDENCE LANGUAGE

```text
High confidence → strong wording
Low confidence → qualified wording
```

Examples (catalog, not hard-coded prose in engine):

```text
high     → rõ / có lực / ổn định (still not “chắc chắn”)
moderate → khá / có điều kiện
low      → thiên hướng / chưa đủ bằng chứng
unresolved → chưa kết luận được
```

Never use high-confidence wording on a low-confidence block.

Never use “chắc chắn” for life events.

---

# 28. UNCERTAINTY

Explicitly supported.

Never fake certainty.

Unresolved Pattern, missing hour, missing luck, unresolved Health Domain must remain visible in the appropriate layer.

Expert layer shows why. Executive layer still must not invent a Pattern.

---

# 29. CUSTOMER QUESTIONS

Narrative should naturally answer:

```text
Who am I?
What am I strongest at?
Where are my bottlenecks?
Why?
What should I do?
What should I avoid?
When should I act?
```

“When” = temporal activation / optimization time_scope, **not** marriage year or death year.

If temporal is not evaluated, say that timing is not in this report — do not guess.

---

# 30. NARRATIVE GRAPH RESULT

Canonical:

```text
NarrativeGraphResult
```

```text
schema_version
nodes[]                       # NarrativeBlock
edges[]
layer                         # requested layer
locale
story_flow_order[]
dedup_groups[]
confidence
trace_ids[]
```

---

# 31. NARRATIVE RESULT

Canonical:

```text
NarrativeResult
```

Fields:

```text
schema_version
executive_summary
strengths[]
risks[]
opportunities[]
domains{}
temporal
optimization
closing_summary
confidence
trace[]
graph                         # NarrativeGraphResult
mc01_summary_ref              # optional pointer; do not mutate
warnings[]
```

`closing_summary` restates priorities and conditions. It MUST NOT introduce new facts.

---

# 32. OUTPUT MODES

Support:

```text
Portal
PDF
DOCX
Consulting
API
```

All from **one** NarrativeGraph.

Parity (architecture):

```text
PDF/DOCX MUST NOT re-interpret Ten Gods from dictionary text
Portal MUST NOT compute a different luck rewrite than PDF
Labels may differ by density, not by meaning
unresolved stays unresolved on all surfaces
MC-01 summary and Pack 07 detail must not contradict
```

Consulting mode may default to Expert layer. It still cannot infer.

---

# 33. MESSAGE CATALOG

```text
bte.detailed_interpretation.messages.vi.v1
```

Keys bind to finding IDs / action IDs.

Calculation never depends on catalog wording.

LLM may expand presentation **after** canonical composition. LLM MUST NOT replace canonical Composer determinism.

---

# 34. MC-01 COMPOSER BOUNDARY

```text
MC-01 Composer
= Mệnh Cục headline / executive structural summary

Pack 07 Narrative Composer
= detailed domain / temporal / optimization narrative
```

If MC-01 says Grade A and authority high, Pack 07 must not say the structure is weak because an annual is hard.

If MC-01 wealth creation high / retention low, Pack 07 must not say “tài vận toàn diện tốt”.

Do not overwrite Narrative V2 / Commercial Consulting contracts. Those consume this graph; they do not invent a parallel narrative engine.

---

# 35. CONFIDENCE AND TRACE

Every major NarrativeBlock requires:

```text
evidence_ids[]
trace_ids[]
confidence
```

Conceptual chain:

```text
MC-01 / Pack 07 findings
      →
EvidencePriorityResult
      →
Domain / Temporal / Optimization objects
      →
NarrativeGraph nodes
      →
NarrativeResult
      →
Portal / PDF / DOCX / Consulting / API
```

Missing trace is a specification failure (NAR-04).

---

# 36. DETERMINISM

```text
Same MC-01
+ same EvidencePriorityResult
+ same Domains / Temporal / Optimization
+ same composer version
+ same message catalog
+ same locale
+ same layer
= same NarrativeResult
```

No LLM in canonical path.

No biography.

Calling compose twice must not change IDs or ordering.

---

# 37. GOLDEN DATASET REQUIREMENTS

Golden narrative cases at minimum:

```text
Chính Quan Pattern + high authority — no “làm quan”
creation high + retention low — split kept in executive and wealth
Career High + Relationship Low — both kept, trade-off if evidenced
P0 Damage + Rescue — both mentioned, Damage not dropped
unresolved Pattern — uncertainty in executive
Hồng Loan without relationship structure — not marriage headline
annual suppress + natal strong — two-layer wording
Optimization Top 3 match LifeOptimizationResult
Expert layer exposes Damage ID; Commercial does not invent extra claims
same inputs → same narrative
```

---

# 38. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
No contradiction hidden
No duplicated paragraphs / claims
No unsupported claims
No evidence-free recommendations
```

Additional:

```text
Composer does not infer
Composer does not rerank
Composer does not rewrite natal from luck
Shen Sha does not lead
PDF ≠ Portal meaning
empty Optimization ≠ invented life-coach list
low confidence ≠ strong wording
```

---

# 39. ACCEPTANCE INVARIANTS

```text
NAR-01 Composer never infers.
NAR-02 Composer consumes Priority.
NAR-03 Narrative follows Story Flow.
NAR-04 Evidence always traceable.
NAR-05 No contradictions.
NAR-06 No duplicated evidence.
NAR-07 Confidence wording correct.
NAR-08 No biography.
NAR-09 No luck rewrites natal.
NAR-10 Same input + ruleset = same narrative.
```

Additional:

```text
NAR-11 Does not overwrite MC-01 Composer Mệnh Cục summary.
NAR-12 Top actions come only from Life Optimization.
NAR-13 One NarrativeGraph serves all output modes.
NAR-14 Shen Sha cannot lead executive summary.
NAR-15 Unresolved stays unresolved.
```

---

# 40. FAILURE CONDITIONS

This specification FAILS if:

```text
Composer changes MC-01
Composer reranks evidence
Composer invents facts
Composer duplicates evidence
Composer hides uncertainty
Composer ignores bottlenecks
Composer maps Ten God name to profession/marriage/disease
Composer mixes natal and luck into one rewritten score
PDF-only conclusions
```

---

# 41. VERSIONING

```text
bte.detailed_interpretation.composer.v1
bte.detailed_interpretation.messages.vi.v1
```

Do not create a competing narrative engine inside Portal, Report, PDF, DOCX, or Narrative V2.

---

# 42. FREEZE TARGETS

Frozen:

1. NarrativeGraph node/edge types and Story Flow.
2. Layers: commercial, technical, expert, executive.
3. Priority consumption; no rerank.
4. Executive Summary answers who / what matters / what to prioritize.
5. Domain narratives from structured domain results.
6. Optimization integration from LifeOptimizationResult only.
7. Output contract: NarrativeResult + one graph for all modes.
8. No inference; no contradiction collapse; no duplication.
9. Natal / temporal wording stays two-layer.
10. Invariants NAR-01 … NAR-15.
11. Version `bte.detailed_interpretation.composer.v1`.

Not frozen:

- exact Vietnamese catalog strings
- Python dataclasses
- LLM post-expansion
- Public API function signatures (DI-20)

---

# 43. NEXT DOCUMENT

Next:

```text
20_PUBLIC_API.md
```

That document must freeze the public API concept for:

```text
build_detailed_interpretation_context
analyze_detailed_interpretation
compose_detailed_interpretation
```

It MUST NOT let consumers reconstruct interpretation independently.

It MUST NOT change this Composer contract.

Do not write DI-20 until Product Owner approval.
