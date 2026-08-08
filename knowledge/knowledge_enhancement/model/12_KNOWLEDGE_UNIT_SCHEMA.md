# 12 — Knowledge Unit Schema

Version: 1.0  
Status: **SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Depends on: `11_KNOWLEDGE_UNIT_MODEL.md`  
Scope: **Logical schema only** — do not create JSON or CSV in this sprint  

---

## 1. Purpose

Document the official **logical fields** of a Knowledge Unit.

This is the blueprint for future physical stores (`database/20_knowledge`, evidence libraries, etc.).  
Physical column names may differ; **semantics must map 1:1** to these fields.

---

## 2. Identity & descriptive fields

| Logical field | Type (logical) | Purpose |
|---------------|----------------|---------|
| `knowledge_unit_id` | Stable string | Globally unique immutable id (naming in `15`). Primary trace key. |
| `title` | Short string | Human label for authors/reviewers/search — not customer-facing by default. |
| `summary` | Short text | One-sentence advisory gist; used in ranking previews and composition summaries. |
| `body` / `advisory_text` | Text | Consultant-facing advisory content (commercial VI). The reusable meaning payload. |
| `kind` | Enum | Commercial Knowledge kind from `02`: Analytical, Consultation, Practical Guidance, Action, Risk, Mitigation, Life Strategy, Opportunity. |
| `classical_support` | Optional text | Optional classical paraphrase; must not contradict `body`. |
| `modern_interpretation` | Optional text | If split from `body`; otherwise `body` holds modern advisory. |

---

## 3. Domain, scenario, intent

| Logical field | Type | Purpose |
|---------------|------|---------|
| `domain` | CK-* (1..n) | Consultation domain affinity (`01`). Primary domain first. |
| `scenario` | CS-* (0..n) | Scenario affinity (`06`). Empty = structural/general reusable. |
| `decision` | DS-* (0..n) | Optional decision affinity (`08`). |
| `primary_intent` | String/enum | Main consultation problem this unit solves (customer-language). |
| `secondary_intent` | String/enum (0..n) | Additional problems it may help without being the main purpose. |

**Intent vs scenario:** Intent is the problem statement; scenario is the catalog entry point. Both improve retrieval.

---

## 4. Applicability & analytical binding

| Logical field | Type | Purpose |
|---------------|------|---------|
| `applicable_conditions` | Condition expression / structured predicates | When the unit may apply; bound to Analysis/RuleContext signals. |
| `signal_refs` | Ids (0..n) | Explicit analytical signal / rule references (not duplicated rule logic). |
| `contradiction_policy` | Enum | Default `drop_if_analysis_conflicts` (Sprint A principle). |
| `ethics_flags` | Flags | e.g. `sensitive_marriage`, `non_medical`, `no_guaranteed_returns`. |

---

## 5. Evidence & interpretation requirements

| Logical field | Type | Purpose |
|---------------|------|---------|
| `evidence_kind` | Pack 05 kind | identity / strength / weakness / risk / action / explanation / implication / grade. |
| `required_evidence` | Kinds (0..n) | Other evidence that should already exist for this unit to emit safely (e.g. Mitigation requires Risk). |
| `required_interpretation` | Section/theme ids (0..n) | Interpretation focuses that should be commercially usable before relying on this unit. |
| `paired_unit_ids` | KU ids (0..n) | Explicit pairs (Risk↔Mitigation, Action↔Strategy). |

---

## 6. Narrative & consultation goals

| Logical field | Type | Purpose |
|---------------|------|---------|
| `supported_narrative_components` | Pack 05 components (1..n) | executive_summary, observation, reasoning, impact, recommendation, warning, conclusion. |
| `consultation_goals` | Goals (1..n) | What customer outcome this unit advances (e.g. clarify_identity, choose_wait, reduce_risk). |
| `decision_posture` | Optional enum | advance / prepare / wait / protect / reassess (`08`) when Action/Strategy relevant. |

---

## 7. Action / Risk / Opportunity categories

| Logical field | Type | Purpose |
|---------------|------|---------|
| `action_category` | Optional enum | e.g. career_transition, capital_conservation, habit_change, relationship_pacing. |
| `risk_category` | Optional enum | e.g. wealth_clash, authority_strain, timing_hostility, lifestyle_imbalance. |
| `opportunity_category` | Optional enum | e.g. luck_window, role_fit, learning_window, founder_timing. |

Categories enable retrieval filters and Report/AI faceting without reading full text.

---

## 8. Quality, priority, confidence

| Logical field | Type | Purpose |
|---------------|------|---------|
| `priority` | Int / enum | Selection preference among matching units. |
| `confidence` | 0..1 or enum | Author/knowledge confidence in advisory applicability. |
| `confidence_requirement` | Threshold | Minimum analysis/knowledge confidence needed to emit this unit in production. |
| `commercial_value` | Optional enum | P0/P1/P2 alignment hint for backlog triage. |

---

## 9. Usage metadata (Primary / Secondary)

| Logical field | Type | Purpose |
|---------------|------|---------|
| `primary_usage` | Set | Executive Summary, Recommendation, Warning, Interpretation, Knowledge Panel. |
| `secondary_usage` | Set | Portal, Report, AI Assistant, Search, Mobile, Future APIs. |

### Why required

| Without usage metadata | With usage metadata |
|------------------------|---------------------|
| Teams copy advice into UI strings | One unit → many channels |
| Retrieval cannot prefer Exec vs Warning | Ranking fills the right slots first |
| Report invents long-form | Report reuses Narrative/KU SSOT |
| AI drifts from consultation | AI retrieves same Published units |

---

## 10. Traceability & governance

| Logical field | Type | Purpose |
|---------------|------|---------|
| `traceability` | Object | Bundle of `signal_refs`, `ref_ids` (REF-*/SRC-*), related KU ids, scenario ids used in authoring. |
| `ref_ids` | Bibliography ids | Classical/modern citation anchors. |
| `version` | Semver string | Unit content version. |
| `review_status` | Lifecycle enum | Aligns with `14` (draft…deprecated). |
| `supersedes` / `superseded_by` | KU id optional | Succession links. |
| `author` | String | Authoring ownership. |
| `author_notes` | Text | Non-customer notes for reviewers (edge cases, TODOs). |
| `reviewers` | List | Technical / Knowledge / Commercial reviewers. |
| `approved_at` / `published_at` | Timestamps | Audit. |
| `extension_metadata` | Map | Controlled extensions only; must not smuggle layout/runtime hacks. |

---

## 11. Field purpose map (checklist view)

| Field | Answers |
|-------|---------|
| `knowledge_unit_id` | Which atom is this forever? |
| `title` / `summary` | What is it called / in one line? |
| `body` | What do we advise? |
| `kind` | Which commercial layer? |
| `domain` / `scenario` / `decision` | Where in consultation space? |
| `primary_intent` / `secondary_intent` | What customer problem? |
| `applicable_conditions` | When may it fire? |
| `required_evidence` / `required_interpretation` | What must be true upstream? |
| `supported_narrative_components` | Where may Narrative place it? |
| `consultation_goals` | What outcome does it serve? |
| `action/risk/opportunity_category` | How do we facet it? |
| `confidence` / `confidence_requirement` / `priority` | How strongly / preferentially? |
| `primary_usage` / `secondary_usage` | Who consumes it? |
| `traceability` / `ref_ids` / `version` / `review_status` | How do we govern & prove it? |
| `author_notes` / `extension_metadata` | How do we maintain safely? |

---

## 12. Required vs optional (logical)

| Required for Published | Optional |
|------------------------|----------|
| `knowledge_unit_id`, `title`, `summary`, `body`, `kind` | `classical_support`, `decision` |
| `domain` (≥1) or explicit `structural` | `secondary_intent` |
| `primary_intent` | categories not matching kind |
| `applicable_conditions` | `extension_metadata` |
| `evidence_kind` | `commercial_value` |
| `supported_narrative_components` (≥1) | |
| `primary_usage` (≥1) | `secondary_usage` (recommended) |
| `priority`, `confidence`, `confidence_requirement` | |
| `traceability` (min signal or REF), `version`, `review_status` | |
| `ethics_flags` when domain sensitive | |

---

## 13. Non-goals

- Creating JSON Schema files in this sprint  
- Creating CSV headers in this sprint  
- Binding to a single physical store  

---

## 14. Stop line

Logical schema documented.  
No physical schema files created.

---

END
