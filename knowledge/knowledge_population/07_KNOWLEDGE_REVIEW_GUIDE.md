# 07 — Knowledge Review Guide

Version: 1.0  
Status: **OFFICIAL — Golden Review Workflow**  
Date: 2026-08-08  
Depends on: `02_REVIEW_PROCESS.md`, `06_GOLDEN_KNOWLEDGE_STANDARD.md`  
Scope: Documentation only  

---

## 1. Purpose

Finalize the official review workflow for Knowledge Units, including **Product Review** as the last human gate before Publish Decision.

This guide supersedes informal review order where it conflicts, and **extends** `02` with Product Review + Golden checks.

---

## 2. Official review order

```
Technical Review
        ↓
Knowledge Review
        ↓
Commercial Review
        ↓
Narrative Review
        ↓
Product Review
        ↓
Publish Decision
```

All stages sequential per unit (or RK+MT pair package).  
Fail at any stage → return to Draft (or hold) with recorded reasons.

---

## 3. Technical Review

| Attribute | Definition |
|-----------|------------|
| **Goals** | Schema integrity; signal conditions; no Rule DB duplication; pairing; ids/version |
| **Owner** | Technical Reviewer |
| **Checklist** | See §3.1 |
| **Approval requirements** | All checklist items Pass; no HF-01…HF-12 tech-related fails |
| **Escalation** | Architect if catalog id conflict, schema extension needed, or signal contract undefined |

### 3.1 Checklist

- [ ] `knowledge_unit_id` stable and documented  
- [ ] Required logical fields present  
- [ ] `condition` references Analysis concepts (contract noted if not yet wired)  
- [ ] No thresholds/weights copied from Rule Database  
- [ ] `evidence_kind` / narrative_targets / usage valid  
- [ ] Pair ids coherent  
- [ ] Placeholders documented with bind sources  
- [ ] Render-agnostic (no UI/layout coupling)  
- [ ] Version + review_status coherent  

---

## 4. Knowledge Review

| Attribute | Definition |
|-----------|------------|
| **Goals** | BaZi correctness; explainability; ethics; classical/modern consistency |
| **Owner** | Knowledge Reviewer (domain expert) |
| **Checklist** | See §4.1 |
| **Approval requirements** | Correct + Explainable Golden criteria Pass; ethics Pass |
| **Escalation** | Academic board / Architect if classical REF dispute or doctrine conflict |

### 4.1 Checklist

- [ ] Body consistent with conditions  
- [ ] No analytical contradiction  
- [ ] Classical paraphrase labeled honestly (not fake verbatim)  
- [ ] Ethics flags correct  
- [ ] Granularity atomic  
- [ ] Not academic filler  
- [ ] Calm weakness/risk language  

---

## 5. Commercial Review

| Attribute | Definition |
|-----------|------------|
| **Goals** | Customer value; brand voice; priority fit; actionability |
| **Owner** | Commercial Reviewer |
| **Checklist** | See §5.1 |
| **Approval requirements** | Commercially valuable + Professional + Actionable Pass |
| **Escalation** | Product if scope/tier dispute (P0 vs P2) |

### 5.1 Checklist

- [ ] Real consultation problem  
- [ ] Improves Exec/Rec/Warning/Impact as claimed  
- [ ] Consultant voice  
- [ ] Action specificity (if Action kind)  
- [ ] No return guarantees / doom  
- [ ] `commercial_value` accurate  

---

## 6. Narrative Review

| Attribute | Definition |
|-----------|------------|
| **Goals** | Pack 05 fitness; Content Quality bar; no composer invention needed |
| **Owner** | Narrative Reviewer |
| **Checklist** | See §6.1 |
| **Approval requirements** | Narrative-friendly + Natural Pass; CQ shape for claimed slots |
| **Escalation** | Narrative architect if component mapping would require Pack 05 change (must reject unit instead) |

### 6.1 Checklist

- [ ] evidence_kind ↔ narrative_targets coherent  
- [ ] Exec-targeted units support briefing slots  
- [ ] Recommendation-targeted units have Action/Reason/Next shape  
- [ ] Warning targets have caution tone; Risk kinds have mitigation path  
- [ ] No technical residue likely to be filtered empty  
- [ ] Does not require new Narrative sections  

---

## 7. Product Review

| Attribute | Definition |
|-----------|------------|
| **Goals** | Product readiness: wave priority, customer risk, publish timing, alias/catalog policy |
| **Owner** | Product Owner / Product Reviewer |
| **Checklist** | See §7.1 |
| **Approval requirements** | Explicit Pass for this wave; known gaps accepted or blocked |
| **Escalation** | Leadership if ethics/legal or go-to-market conflict |

### 7.1 Checklist

- [ ] Wave still matches commercial roadmap  
- [ ] Customer-facing risk acceptable  
- [ ] Id/catalog alias policy accepted  
- [ ] Publish now vs approve-and-hold decided  
- [ ] Wiring dependency acknowledged (if runtime not ready)  
- [ ] No unauthorized scope (extra units, engine asks)  

---

## 8. Publish Decision

| Attribute | Definition |
|-----------|------------|
| **Goals** | Move to Published or hold at Approved / return for revision |
| **Owner** | Knowledge Ops (with Product Pass required) |
| **Checklist** | All five reviews Pass; manifest ready; pairs co-batched |
| **Approval requirements** | Written Publish Decision: PUBLISH / HOLD / REVISION REQUIRED |
| **Escalation** | Architect if supersession/deprecation conflict |

### Outcomes

| Decision | Meaning |
|----------|---------|
| **PUBLISH** | `review_status=published`; production-eligible |
| **HOLD (Approved)** | Content accepted; not production-eligible yet |
| **REVISION REQUIRED** | Return to Draft with blocking issues |

---

## 9. Golden Reference designation

Separate from Publish:

| Step | Owner |
|------|-------|
| Score unit via `08` | Reviewers collectively |
| Meet Golden threshold | Required |
| Record in `09`-style reference notes | Knowledge Ops |

A Published unit may later be promoted to Golden Reference after live use.

---

## 10. Stop line

Review guide finalized.  
No units modified in this document sprint.

---

END
