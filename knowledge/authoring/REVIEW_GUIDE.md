# Review Guide

**Document:** REVIEW_GUIDE  
**Version:** 1.0.0  
**Status:** Specification  
**Aligns with:** `knowledge/governance/review_workflow.json`, `knowledge/templates/review_template.md`

---

## 1. Review workflow

```text
draft
  → RV-01 Submit for review
      → RV-02 Academic review
      → RV-03 Technical review   (MAY parallel with academic)
      → RV-04 Governance review
  → approved
  → publication workflow (freeze → indexes → release)
```

Rejection returns the record to `draft` with written findings.

---

## 2. Roles

| Role | Focus |
|------|-------|
| Knowledge Author | Completeness, honesty, `TODO_REVIEW` |
| Academic Reviewer | Definition accuracy, sources, assertions |
| Technical Reviewer | Schema shape, IDs, relationships, graph, compiler readiness |
| Governance Owner | Policy, approval matrix, freeze/release readiness |
| Release Manager | Publication gates (after approval) |

Separation of duties: Author SHOULD NOT be sole Approver for official promotion.

---

## 3. What authors prepare before submit

1. [CHECKLIST.md](CHECKLIST.md) complete.
2. Review package draft from `knowledge/templates/review_template.md` (optional but recommended).
3. List open `TODO_REVIEW` items explicitly.
4. Confirm no invented `SRC-*`.

---

## 4. Academic review focus

- Canonical Definition clarity and scope honesty
- Assertion ↔ source traceability
- Bibliography integrity
- Terminology consistency
- No over-confident contested claims

Scorecard: `knowledge/quality/academic_scorecard.json`

---

## 5. Technical review focus

- Section mapping to KR schema
- ID patterns and enums
- Relationship types and duplicate/cycle risks
- Graph node type correctness
- Compiler compatibility notes

Scorecard: `knowledge/quality/technical_scorecard.json`

---

## 6. Governance review focus

- Approval matrix transitions
- Freeze/release policy readiness
- Change requests when touching frozen content
- Golden checklist if promotion requested

Scorecard: `knowledge/quality/governance_scorecard.json`

---

## 7. Findings format

Reference checklist IDs:

```text
[RC-020] FAIL — primary_source_ids includes unknown SRC-009999
[GR-006] FAIL — high-confidence assertion still TODO_REVIEW
```

Include severity (`error` / `warning`) and a concrete fix hint.

---

## 8. Outcomes

| Outcome | Meaning |
|---------|---------|
| approved (stage) | Stage gate passed |
| waived | Allowed only with rationale (e.g. fixture) |
| rejected | Return to draft |
| conditionally approved | Minor fixes before freeze/publish |

Overall publish recommendations follow scorecard bands (see quality scorecards).
