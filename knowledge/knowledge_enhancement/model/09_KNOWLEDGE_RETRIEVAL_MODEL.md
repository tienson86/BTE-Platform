# 09 — Knowledge Retrieval Model

Version: 1.0  
Status: **SPRINT B — Consultation Scenario Model**  
Date: 2026-08-08  
Depends on: `06`, `07`, `08`, Sprint A `02`–`03`  
Scope: **Design only** — no retrieval runtime  

---

## 1. Purpose

Define how Narrative **should** retrieve knowledge once content exists.

Target flow:

```
Scenario
    ↓
Commercial Knowledge
    ↓
Evidence
    ↓
Narrative Component
```

This document specifies:

- retrieval priority  
- fallback strategy  
- knowledge ranking  
- conflict handling  
- missing knowledge handling  
- traceability  

It does **not** implement loaders, matchers, or engine changes.

---

## 2. Retrieval context

A retrieval request is logically:

| Input | Source |
|-------|--------|
| `scenario_id` | CS-* (explicit or default) |
| `decision_id` | DS-* optional |
| `analysis_signals` | AnalysisResult / RuleContext |
| `domain_profile` | From `07` (required/optional/conditional) |
| `kind_profile` | From `07` |
| `ethics_scope` | Product + domain flags |
| `locale` | Commercial VI primary |

Output: ordered candidate Commercial Knowledge units → typed Evidence units for Interpretation/Narrative.

---

## 3. Retrieval priority

Apply filters in order:

### P1 — Hard filters

1. Ethics / safety flags allow emission  
2. `signal_condition` matches Analysis signals (no contradiction — Sprint A §2.7)  
3. Unit `status` eligible (Official, or Draft only in non-prod)  
4. Kind ∈ scenario kind profile (required/optional/conditional rules)

### P2 — Scenario fit

5. `consultation_domain` ∈ scenario domain profile  
6. Decision overlay (if DS-*) boosts Action/Risk/Mitigation/Opportunity  

### P3 — Narrative need

7. Prefer units whose `evidence_kind` fills currently empty required slots for target components  
8. Prefer Mitigation units that pair to already-selected Risk ids  

### P4 — Quality

9. Higher `priority` field  
10. Higher `confidence`  
11. Prefer units with REF-* / stronger trace_refs  
12. Prefer reusable Official over one-off drafts  

---

## 4. Ranking model (conceptual)

Score (design formula — not implemented):

```
rank =
  + w_scenario_domain_match
  + w_kind_required_bonus
  + w_evidence_slot_fill
  + w_decision_relevance
  + w_priority
  + w_confidence
  + w_trace_quality
  - w_conflict_penalty
  - w_duplication_penalty
```

**Required kinds** outrank optional.  
**Conditional kinds** activate only when signals present; when active, treat as required.

---

## 5. Fallback strategy

| Situation | Fallback |
|-----------|----------|
| No scenario specified | Default profile: CS-ID + CS-LT light + CS-MD light (`06` §6) |
| Scenario required kind empty | Try parent/general domain units (e.g. CS-CC → CK-CA general Action) |
| Still empty | Use Analytical Knowledge identity/grade substrate only |
| Still empty for slot | Emit approved insufficient for that slot/component |
| Risk without Mitigation | Select generic Mitigation template for that risk family if Official exists; else Warning soft + insufficient mitigation flag |
| Decision scenario without Opportunity | Allow Wait/Prepare Action without claiming Advance |
| Life scenario without Consultation units | Downgrade to structural Analytical Narrative; status partial |

**Never fallback to:** technical rule prose, Portal hard-coded advice, invented claims.

---

## 6. Conflict handling

| Conflict type | Resolution |
|---------------|------------|
| Two Actions contradict (Advance vs Wait) | Prefer Wait/Protect when Risk high; else higher priority Official; else Decision posture rules (`08` §5) |
| Opportunity vs Risk on same signal | Emit both; Recommendation must reconcile via posture (Advance only if Opportunity survives Risk gate) |
| Multi-scenario Action clash | Ethics/safety > Mitigation > scenario-explicit Action > generic |
| Knowledge vs Analysis | Analysis wins; drop knowledge unit |
| Classical quote vs modern advice | Prefer modern advisory unit for Narrative; classical may support Reasoning if consistent |
| Duplicate near-same text | Keep highest rank; suppress duplicates |

Document related knowledge ids when both Risk and Mitigation selected.

---

## 7. Missing knowledge handling

Aligned with Pack 05 honesty and Epic 1 G6:

| Missing | Narrative behavior |
|---------|-------------------|
| Required evidence kind | Component/slot → approved insufficient |
| Entire scenario profile | `partial_insufficient` |
| Optional kind | Omit; do not pad |
| Sensitive domain content | Withhold rather than improvise |

Missing knowledge is a **content backlog signal**, not a license for composer creativity.

---

## 8. Traceability requirements

Every selected unit must produce trace metadata:

| Field | Purpose |
|-------|---------|
| `knowledge_id` | Commercial Knowledge SSOT id |
| `scenario_id` | Why it was in scope |
| `signal_ids` | Analysis bindings |
| `evidence_kind` | Pack 05 kind |
| `component_targets` | Intended Narrative components |
| `rank_debug` (non-prod) | Optional explanation of ranking |

Narrative filled paragraphs retain trace refs (existing Pack 05 expectation).  
Portal/Report must not strip trace in internal/debug channels; customer UI may hide ids.

---

## 9. Component fill algorithm (design)

For each Narrative component in official order:

1. Determine required evidence kinds for active scenario (`07` §8).  
2. Retrieve top-N units per kind (N small; avoid dump).  
3. Prefer diversity across kinds over many of one kind.  
4. Pass to Interpretation binding / Narrative composer inputs.  
5. If underfilled → insufficient path for that component.

Executive Summary additionally requires multi-kind pack (identity + strength/weakness + action) per Content Quality guidelines.

---

## 10. Consumers of retrieval output

| Consumer | Uses retrieval how |
|----------|--------------------|
| Interpretation | Match/bind commercial sentences / evidence |
| Narrative | Compose components from evidence |
| Future Report | Via NarrativeResult only |
| Future AI assistant | Same Commercial Knowledge SSOT + scenario profile |

One retrieval model → many consumers. No parallel advice corpora.

---

## 11. Non-goals (this sprint)

- Implementing retriever services  
- Changing Narrative Engine  
- Populating `database/20_knowledge`  
- Defining SQL/search indexes  

---

## 12. Stop line

Knowledge Retrieval Model (design) complete.  
Await review before implementation epic.

---

END
