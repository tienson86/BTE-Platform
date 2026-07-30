# Knowledge Review Guide

**Document:** KNOWLEDGE_REVIEW_GUIDE  
**Module:** knowledge/knowledge_canon  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Knowledge Assets before Official publication.

Complements Governance review procedures without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts asset metadata and definition |
| Domain Reviewer | Checks domain fit and doctrinal scope |
| Editorial Reviewer | Checks clarity and consistency |
| Traceability Reviewer | Checks REF / TERM / Rule / Sentence links |
| Approver | Sets Status to Official |

---

## Preconditions

- Knowledge ID allocated from the correct domain range
- File created from domain or root template
- No duplicate canonical identity in domain INDEX
- Domain matches directory

---

## Review Steps

### Step 1 — Identity

- [ ] ID format valid (`KNO-NNNNNN`)
- [ ] ID not reused
- [ ] Canonical Name / English / Chinese coherent

### Step 2 — Definition

- [ ] Definition present and non-circular
- [ ] Atomic scope (one concept)
- [ ] No unverified doctrine presented as settled fact without Evidence

### Step 3 — Classification

- [ ] Domain correct
- [ ] Category appropriate
- [ ] Confidence justified by Evidence

### Step 4 — Mapping

- [ ] Relationships valid when present
- [ ] Terminology Links valid when present
- [ ] Reference Links valid when present
- [ ] Rule / Sentence Links valid when present
- [ ] No invented IDs

### Step 5 — Quality and Traceability

- [ ] Passes `KNOWLEDGE_QUALITY_STANDARD.md`
- [ ] Traceability level adequate for requested Status
- [ ] Edge cases handled per `EDGE_CASES.md`

### Step 6 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes / registry |
| Request changes | Remain Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official assets |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Knowledge ID | KNO-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Framework Phase Note

No Knowledge Asset content reviews occur in V1.0.0 framework scaffolding.
