# 03 — Case Review Workflow

Version: 1.0  
Status: **OFFICIAL — Case Review Workflow**  
Date: 2026-08-08  
Depends on: `01`, `02`, `04`, `05`  
Scope: Documentation only — process definition, no runtime  

---

## 1. Purpose

Define the official human workflow for evaluating consulting quality on real cases before commercial release.

```
Case
  ↓
Narrative
  ↓
Human Review
  ↓
Revision
  ↓
Approval
```

---

## 2. Workflow stages

### Stage 0 — Case selection

| Item | Rule |
|------|------|
| Input | Birth data / analysis case id + scenario (`default` or CS-*) |
| Knowledge | Wave 1.1 allow-list only |
| Output | Case brief: expected signals (day master, strength band, useful god, risks) |
| Exit | Case has known Analysis expectations recorded |

Do not invent expected commercial prose before Narrative exists.

### Stage 1 — Narrative generation

| Item | Rule |
|------|------|
| Actor | Pipeline (Analysis → Interpretation → Commercial Adapter → Narrative) |
| Output | NarrativeResult (+ optional `commercial_knowledge_bundle`) |
| Constraint | No manual rewrite of engine outputs at this stage |
| Exit | NarrativeResult available to reviewers |

### Stage 2 — Human Review

| Item | Rule |
|------|------|
| Actor | Consultant Reviewer (primary); optional Knowledge Reviewer; Product on blockers |
| Method | Follow `02_CONSULTANT_REVIEW_GUIDE.md` |
| Artifact | Completed `04_CONSULTING_SCORECARD.md` instance + defect list |
| Exit | Status ∈ {Approve, Revise, Reject, Escalate} |

### Stage 3 — Revision

| Item | Rule |
|------|------|
| Trigger | Review status = Revise |
| Allowed revision types | Knowledge Unit fix (follow EPIC 3 process), Adapter/merge guidance ticket, case fixture correction, documentation note |
| Forbidden | Changing Analysis meaning to “make copy nice”; Foundation/UI redesign; inventing Wave 1.2 content |
| Exit | New Narrative generated or defect closed with rationale |

### Stage 4 — Approval

| Item | Rule |
|------|------|
| Actor | Consultant Reviewer + Product (for commercial gate) |
| Check | Scorecard meets `05_ACCEPTANCE_CRITERIA.md` |
| Output | Case marked consulting-approved for the release set |
| Exit | Approval recorded with scorecard version and reviewer names |

---

## 3. Roles and responsibilities

| Role | Responsibilities | Must not |
|------|------------------|----------|
| **Case Owner** | Select cases; record expected Analysis signals; track revision tickets | Rewrite Narrative by hand as “truth” |
| **Consultant Reviewer** | Score dimensions; find consulting defects; recommend Approve/Revise/Reject | Change frozen engines or Foundation |
| **Knowledge Reviewer** | Confirm Wave 1.1 claims / KU defects; route EPIC 3 revisions | Publish units without Product |
| **Engineering Liaison** | Triage accuracy bugs vs merge bugs | “Fix” by editing Golden Dataset / snapshots |
| **Product Reviewer** | Commercial release gate; ethics/scope decisions | Demand out-of-scope Wave 1.2 content mid-gate |

---

## 4. Decision outcomes

| Outcome | When | Next |
|---------|------|------|
| **Approve** | Meets acceptance criteria (`05`) | Include in commercial case set |
| **Revise** | Fixable consulting/knowledge/merge defects | Stage 3 → regenerate Stage 1–2 |
| **Reject** | Case unsuitable (bad fixture) or systemic failure | Drop from release set or open epic |
| **Escalate** | Ethics / legal / Product policy ambiguity | Product Reviewer |

Maximum revision loops before Escalate: **3** (configurable by Product).

---

## 5. Exit criteria by stage

| Stage | Exit criteria |
|-------|---------------|
| Case selection | Expected Analysis signals documented |
| Narrative | NarrativeResult produced; run id recorded |
| Human Review | Scorecard complete; severity-tagged defects listed |
| Revision | Each Major/Blocker has owner + resolution note |
| Approval | `05` minimums met; Product sign-off for release set |

---

## 6. Case set for commercial release (recommended)

Until Product expands:

| Set | Intent |
|-----|--------|
| Strong + useful god | Identity / Strength / UG / RC path |
| Weak + useful god | Identity / Weakness / UG / RC path |
| Useful god absent | Confirm UG/RC correctly omitted; no invention |
| Insufficient / thin evidence | Trustworthiness / insufficient honesty |

Exact fixture list is Product-owned; this workflow defines process only.

---

## 7. Artifacts to retain

For each approved case:

1. Case id / birth inputs (or anonymized fixture id)  
2. NarrativeResult snapshot reference (do not edit Golden Dataset to force pass)  
3. Completed scorecard  
4. Defect log (open/closed)  
5. Approver names + date  
6. Knowledge wave id (`W-P0-1.1-CORE`)  

---

## 8. Relationship to engineering tests

| Layer | Purpose |
|-------|---------|
| Module / golden tests | Correctness & regression of engines |
| Consulting Quality review | Human commercial fitness |

Passing automated tests is **necessary but not sufficient** for commercial release.

---

## 9. Stop line

Workflow defined. No tooling implementation in Sprint A.

---

END
