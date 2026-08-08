# 14 — Knowledge Lifecycle

Version: 1.0  
Status: **SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Depends on: `11`, `12`, governance policies (Foundation knowledge governance — not modified)  

---

## 1. Purpose

Define the official lifecycle of a Knowledge Unit from creation to retirement.

```
Draft
  ↓
Technical Review
  ↓
Knowledge Review
  ↓
Commercial Review
  ↓
Approved
  ↓
Published
  ↓
Revised
  ↓
Deprecated
```

Only **Published** units may feed production Narrative / Portal commercial prose.

---

## 2. Stage overview

| Stage | `review_status` value | Production eligible? |
|-------|----------------------|----------------------|
| Draft | `draft` | No |
| Technical Review | `technical_review` | No |
| Knowledge Review | `knowledge_review` | No |
| Commercial Review | `commercial_review` | No |
| Approved | `approved` | No (pre-publish gate) |
| Published | `published` | **Yes** |
| Revised | `revised` (work branch) / new version Draft | Old Published may remain live until replace |
| Deprecated | `deprecated` | No (traces only) |

---

## 3. Draft

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Author creates/edits a KU without production impact |
| **Owner** | Knowledge Author |
| **Required checks** | Schema completeness draft-level (`12`); primary_intent present; not duplicating obvious Official unit |
| **Exit criteria** | Author submits for Technical Review; id reserved; version set (e.g. 0.x or 1.0.0-draft) |

---

## 4. Technical Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Ensure structural correctness and non-duplication of Rule Database |
| **Owner** | Technical Reviewer (Knowledge Engineer / Architect) |
| **Required checks** | All required logical fields present; `applicable_conditions` bound to real signals; no rule thresholds copied; `evidence_kind` valid; pairing metadata if Mitigation; ids/naming per `15`; no render-tech coupling |
| **Exit criteria** | Pass → Knowledge Review; Fail → Draft with notes |

---

## 5. Knowledge Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Ensure BaZi advisory meaning is sound, explainable, non-contradictory |
| **Owner** | Knowledge Reviewer (domain expert) |
| **Required checks** | Consistent with analytical meaning; classical_support (if any) does not contradict body; ethics flags correct; domain/scenario affinity sensible; not academic filler; reusable granularity |
| **Exit criteria** | Pass → Commercial Review; Fail → Draft |

---

## 6. Commercial Review

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Ensure customer value, tone, and Narrative usefulness |
| **Owner** | Commercial / Product Reviewer |
| **Required checks** | Answers real consultation problem; primary/secondary usage correct; supports declared Narrative components; Action specificity / Risk calmness / Mitigation pairing; aligns P0–P2 priorities; brand voice (consultant not calculator); sensitive domains acceptable |
| **Exit criteria** | Pass → Approved; Fail → Draft or Knowledge Review |

---

## 7. Approved

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Content accepted; awaiting publish cut / release bundling |
| **Owner** | Knowledge Release Manager (may be same as Commercial) |
| **Required checks** | All three reviews recorded; supersession links set if replacing; confidence_requirement acknowledged |
| **Exit criteria** | Publish action → Published; or hold in Approved until release train |

Approved units must **not** silently appear in production until Published.

---

## 8. Published

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Live advisory atom available to retrieval/composition |
| **Owner** | Knowledge Ops |
| **Required checks** | Publish timestamp; included in release manifest; discoverable to Narrative path (future implementation) |
| **Exit criteria** | Remains Published until Revised replacement published or Deprecated |

---

## 9. Revised

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Improve or correct a Published unit without losing history |
| **Owner** | Knowledge Author (+ reviewers on re-entry) |
| **Required checks** | New version number; change notes in `author_notes` / changelog; re-enter review from Technical (or Knowledge if typo-only policy allows — default full path for meaning changes) |
| **Exit criteria** | New version Approved → Published; `supersedes` old id/version; old version Deprecated or retained as prior Published per policy |

**Policy default:** Meaning changes require full review path. Typo-only may fast-track Commercial Review only if Technical confirms no semantic change.

---

## 10. Deprecated

| Attribute | Definition |
|-----------|------------|
| **Purpose** | Retire unit from new compositions while preserving traces |
| **Owner** | Knowledge Architect / Ops |
| **Required checks** | Reason recorded; `superseded_by` if any; removed from default retrieval; scenarios relying solely on it get backlog tickets |
| **Exit criteria** | Terminal for production selection; may remain readable for audit |

Never delete Published history required for traceability.

---

## 11. Stage transition diagram

```
        ┌──────────────┐
        │    Draft     │◄──────────────┐
        └──────┬───────┘               │
               ▼                       │
        Technical Review ──fail────────┤
               │                       │
               ▼                       │
        Knowledge Review ──fail────────┤
               │                       │
               ▼                       │
        Commercial Review ─fail────────┘
               │
               ▼
            Approved
               │
               ▼
           Published ──────► Revised (new Draft version)
               │                    │
               ▼                    ▼
          Deprecated         (re-enter reviews)
```

---

## 12. Owners summary

| Stage | Primary owner |
|-------|---------------|
| Draft | Author |
| Technical Review | Technical Reviewer |
| Knowledge Review | Domain Knowledge Reviewer |
| Commercial Review | Product / Commercial Reviewer |
| Approved / Published | Release / Knowledge Ops |
| Revised | Author + reviewers |
| Deprecated | Architect / Ops |

Exact role names may map to existing governance roles without modifying Foundation docs.

---

## 13. Stop line

Lifecycle documented.  
No units moved through lifecycle in this sprint (none created).

---

END
