# 12 — Capability API Contract · Career & Business

Version: 1.0  
Status: **DESIGN ONLY — Future public capability contract**  
Date: 2026-08-08  
Depends on: `09`, `10`, Retrieval Contract `bte.commercial_knowledge.retrieval.v1`, Pack 05 NarrativeResult  
Scope: **Documentation only — no API implementation**  

---

## 1. Purpose

Define the future **public capability contract** so Product, Portal, Report, and external clients can call Domain 01 as services — without exposing raw Knowledge Units or Engine internals.

```
Client
  ↓ Capability Request
Capability Service (future)
  ↓ uses Adapter + Narrative (existing)
Commercial Bundle + NarrativeResult
  ↓ Capability Response
Portal / Report / Future APIs
```

This is **not** a new Engine. It orchestrates existing Commercial Knowledge + Narrative.

---

## 2. Contract identity

| Field | Value |
|-------|-------|
| Contract id | `bte.capability.domain01.career_business.v1` |
| Version | `1.0.0-design` |
| Compatibility | Additive fields in minor; breaking = major |
| Transport (future) | HTTPS JSON (exact routes Product-owned) |

---

## 3. Capability operations (logical)

| Operation id | Capability | Future route sketch |
|--------------|------------|---------------------|
| `career.selection.assess` | CAP-D1-CA-SEL | `POST /v1/capabilities/career/selection` |
| `career.transition.plan` | CAP-D1-CA-CHG | `POST /v1/capabilities/career/transition` |
| `career.promotion.assess` | CAP-D1-CA-PRO | `POST /v1/capabilities/career/promotion` |
| `career.leadership.assess` | CAP-D1-CA-LED | `POST /v1/capabilities/career/leadership` |
| `career.management.assess` | CAP-D1-CA-MGT | `POST /v1/capabilities/career/management` |
| `career.development.plan` | CAP-D1-CA-DEV | `POST /v1/capabilities/career/development` |
| `business.entrepreneurship.assess` | CAP-D1-BU-ENP | `POST /v1/capabilities/business/entrepreneurship` |
| `business.partnership.assess` | CAP-D1-BU-PTR | `POST /v1/capabilities/business/partnership` |
| `business.team.assess` | CAP-D1-BU-TEM | `POST /v1/capabilities/business/team` |
| `decision.timing.assess` | CAP-D1-TM-DEC | `POST /v1/capabilities/decision/timing` |

Routes are illustrative — **not implemented**.

---

## 4. Request model (logical)

```text
CapabilityRequest
  contract_id: string
  capability_id: CAP-D1-*
  operation_id: string
  run_id: string
  scenario_id: CS-* | default
  locale: string                  # default vi
  analysis_ref: AnalysisResult | analysis_bag
  interpretation_ref: InterpretationResult | null  # read-only
  options:
    include_narrative: bool       # default true
    include_bundle: bool          # default true
    include_trace: bool           # default true
    maturity_min: 1..5            # optional gate
```

### 4.1 Validation rules

| Rule | Error |
|------|-------|
| Unknown capability_id | `capability_not_found` |
| analysis_ref missing | `analysis_required` |
| Scenario forbidden for capability | `scenario_unsupported` |
| Requested maturity above available | `capability_immature` (or degrade — Product policy) |

---

## 5. Response model (logical)

```text
CapabilityResponse
  contract_id: string
  capability_id: string
  operation_id: string
  run_id: string
  status: complete | partial | degraded | failed
  maturity_level: 1..5
  decision_posture: prepare | advance | stage | defer | mitigate_first | null
  summary:                      # capability-facing short fields
    headline: string
    primary_action: string
    caution: string | null
  commercial_knowledge_bundle: CommercialKnowledgeBundle | null
  narrative_result: NarrativeResult | null
  portal_projection:            # optional thin view
    executive_summary: ...
    recommendation: ...
    warning: ...
  report_projection: null       # reserved
  traceability:
    knowledge_unit_ids: string[]
    decision_ids: string[]
    evidence_signal_keys: string[]
    chain: knowledge_unit → evidence → interpretation_enrichment → narrative → portal → api
  errors: CapabilityError[]
  metadata:
    domain: DOMAIN-01
    wave_1_1_used: bool
    domain_units_used: string[]
```

### 5.1 Status meanings

| Status | Meaning |
|--------|---------|
| `complete` | Required domain Knowledge + Narrative for capability present |
| `partial` | Some slots insufficient; honest thin areas |
| `degraded` | Fell back to Wave 1.1 only |
| `failed` | Hard error (validation / pipeline) |

---

## 6. Error handling

| Code | HTTP sketch | When |
|------|-------------|------|
| `capability_not_found` | 404 | Unknown id |
| `analysis_required` | 400 | Missing analysis |
| `scenario_unsupported` | 400 | Bad scenario for capability |
| `capability_immature` | 409 or 200+degraded | Below maturity_min |
| `bundle_empty` | 200 partial | No KU matched |
| `narrative_failed` | 500 | Composer failure |
| `ethics_blocked` | 422 | Guaranteed-outcome style request flags |

Errors must never return raw KU CSV rows or Rule DB dumps.

---

## 7. Traceability requirements

Every successful response must preserve:

```
Capability
  → Decision id(s)
  → Knowledge Unit id(s) + versions
  → Evidence / signal keys
  → Narrative component refs
  → Portal section refs
  → API operation id
```

Aligns with Commercial Bundle traceability chain; capability layer adds `capability_id` + `operation_id`.

---

## 8. Extensibility

| Extension | Rule |
|-----------|------|
| New capability | New CAP id + operation; minor if additive catalog |
| New bundle fields | Additive only |
| New posture enum | Minor if clients ignore unknown |
| Breaking rename of operation | Major version bump |
| Direct KU authoring via API | **Forbidden** |

---

## 9. Non-goals of this contract

- Replacing orchestrator pipeline  
- Exposing Score/Pattern Engine internals  
- Implementing HTTP handlers in this sprint  
- Portal/UI redesign  

---

## 10. Example (illustrative only)

**Request:** `career.selection.assess` with analysis bag + `scenario_id=CS-CA`  

**Response (happy):** `status=complete`, `maturity_level=3`, bundle with identity/useful_god/recommendations, NarrativeResult Exec+Rec filled, `knowledge_unit_ids` includes Wave 1.1 + KU-CN-CA-000001 + KU-AC-CA-000001.

---

## 11. Stop line

API contract documented — **not implemented**. Roadmap → `13`.

---

END
