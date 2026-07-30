# Rule Review Guide

**Document:** RULE_REVIEW_GUIDE  
**Module:** knowledge/rule_database  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Rule Database framework records before Official publication.

Complements Governance procedures without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts rule metadata and placeholders |
| Domain Reviewer | Checks domain fit and priority placement |
| Knowledge Reviewer | Checks Knowledge / Terminology links |
| Traceability Reviewer | Checks REF / Sentence / Related Rules links |
| Approver | Sets Status to Official |

---

## Preconditions

- Rule ID allocated from the correct domain range
- File created from domain or root template
- No duplicate title/identity collision in domain INDEX
- Domain matches directory

---

## Review Steps

### Step 1 — Identity

- [ ] ID format valid (`RUL-NNNNNN`)
- [ ] ID not reused
- [ ] Title clear and unique within domain

### Step 2 — Decision Semantics

- [ ] Condition present for Official status
- [ ] Outcome present for Official status
- [ ] Atomic scope (one decision unit)
- [ ] Priority declared when conflicts are possible

### Step 3 — Mapping

- [ ] Knowledge Links valid when present
- [ ] Terminology / Reference / Sentence Links valid when present
- [ ] Related Rules valid when present
- [ ] No invented IDs

### Step 4 — Quality and Traceability

- [ ] Passes `RULE_QUALITY_STANDARD.md`
- [ ] Traceability level adequate for Status
- [ ] Edge cases handled per `EDGE_CASES.md`

### Step 5 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes / registry |
| Request changes | Remain Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official rules |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Rule ID | RUL-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Framework Phase Note

No rule content reviews occur in V1.0.0 scaffolding.
