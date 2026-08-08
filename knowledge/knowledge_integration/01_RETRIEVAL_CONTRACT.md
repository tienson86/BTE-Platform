# 01 — Retrieval Contract

Version: 1.0  
Status: **OFFICIAL — Retrieval Contract (design)**  
Date: 2026-08-08  
Depends on: EPIC 2 `09_KNOWLEDGE_RETRIEVAL_MODEL.md`, Wave 1.1 units  
Scope: Contract specification only — no runtime  

---

## 1. Purpose

Define the official **Retrieval Contract** between:

- Production pipeline (Analysis + scenario context)  
- Commercial Knowledge corpus (Knowledge Units)  
- Narrative consumption (typed evidence / Narrative-ready payload)  

Implementations in Phase B **must** obey this contract.

---

## 2. Contract name & version

| Field | Value |
|-------|-------|
| Contract id | `bte.commercial_knowledge.retrieval.v1` |
| Version | `1.0.0` |
| Compatibility | Additive fields allowed in minor; breaking = major |

---

## 3. Inputs

### 3.1 Required inputs

| Input | Type | Source | Notes |
|-------|------|--------|-------|
| `analysis_signals` | structured map | AnalysisResult / RuleContext projection | Facts only — Adapter never invents |
| `scenario_id` | CS-* or `default` | Product / orchestrator | Default = CS-ID + CS-LT light + CS-MD light profile |
| `allow_list_status` | enum set | Config | e.g. `{published}` or `{published, approved}` per Product |

### 3.2 Optional inputs

| Input | Type | Source |
|-------|------|--------|
| `decision_id` | DS-* | Decision overlay |
| `interpretation_hints` | section ids present | InterpretationResult **read-only** (no IE code change) |
| `ethics_scope` | flags | Product policy |
| `locale` | string | Default commercial VI |
| `target_components` | Pack 05 ids | Restrict retrieval (Exec/Rec for Wave 1.1) |
| `max_units_per_kind` | int | Cap dumps |

### 3.3 Knowledge Unit filters (applied to corpus)

| Filter | Rule |
|--------|------|
| Status | Only statuses in `allow_list_status` |
| Condition | `applicable_conditions` match `analysis_signals` |
| Scenario | Unit scenarios empty OR intersect request scenario/default profile |
| Ethics | Unit ethics_flags ⊆ allowed ethics_scope |
| Component | Unit `narrative_targets` intersect `target_components` (when set) |
| Confidence | Unit `confidence` ≥ unit `confidence_requirement` **and** analysis confidence gate if provided |
| Contradiction | Drop if Analysis conflicts (policy `drop_if_analysis_conflicts`) |

### 3.4 Priority & ranking inputs

| Signal | Use |
|--------|-----|
| Unit `priority` | Higher preferred |
| Required vs optional for scenario profile | Required first |
| Slot fill need | Prefer units filling empty Exec/Rec slots |
| Pair integrity | Prefer MT when RK selected (future); Wave 1.1: honor `paired_unit_ids` boost |

---

## 4. Fallback

| Situation | Fallback |
|-----------|----------|
| No scenario | `default` profile |
| No KU matches | Empty bundle; Narrative uses existing insufficient path |
| Strength unit fails condition | Omit strengths commercial text (do not invent) |
| Weakness unit fails condition | Omit weaknesses commercial text |
| Useful god absent | Omit KU-UG-001 and KU-RC-001 |
| Bundle partial | `bundle_status=partial`; Narrative may be `partial_insufficient` |
| Status not allowed (still awaiting_review) | **No retrieval** until Product allow-list includes unit |

**Wave 1.1 note:** Units remain `awaiting_review`. Contract supports retrieval only after allow-list includes them (typically after `approved`/`published`).

---

## 5. Outputs

### 5.1 Commercial Knowledge Bundle

Logical object `CommercialKnowledgeBundle v1`:

| Field | Meaning |
|-------|---------|
| `contract_id` | `bte.commercial_knowledge.retrieval.v1` |
| `bundle_id` | Run-scoped id |
| `scenario_id` | Echo |
| `bundle_status` | `complete` \| `partial` \| `empty` |
| `selected_units[]` | Ordered KU summaries (id, version, kind, evidence_kind, priority, score) |
| `dropped_units[]` | id + reason (condition_fail, status, conflict, dedupe, …) |
| `trace` | signal ids used; ranking notes (non-prod optional) |

### 5.2 Narrative-ready payload

Logical object `NarrativeKnowledgePayload v1` (derived from bundle):

| Field | Meaning |
|-------|---------|
| `evidence_units[]` | Typed commercial evidence for Narrative input adapter |
| Each evidence unit | `evidence_kind`, `text` (bound placeholders), `knowledge_unit_id`, `version`, `component_targets[]`, `trace_refs` |

Binding: replace `{placeholders}` from `analysis_signals` only.  
Unbound required placeholder → drop that unit (fallback), never leave raw `{...}` in customer text.

---

## 6. Evidence kinds (Wave 1.1 mapping)

| KU | evidence_kind | Primary components |
|----|---------------|--------------------|
| KU-ID-001 | identity | executive_summary, observation, conclusion |
| KU-ST-001 | strength | executive_summary, observation, reasoning, conclusion |
| KU-WK-001 | weakness | executive_summary, warning, conclusion |
| KU-UG-001 | explanation | executive_summary, reasoning, impact, recommendation |
| KU-RC-001 | action | recommendation, executive_summary, conclusion |

---

## 7. Non-responsibilities

Retrieval Contract does **not**:

- Change Analysis scores  
- Modify Interpretation Engine  
- Compose NarrativeResult (Narrative Composer does)  
- Publish Knowledge Units  
- Author new KU content  

---

## 8. Stop line

Retrieval Contract defined. No runtime.

---

END
