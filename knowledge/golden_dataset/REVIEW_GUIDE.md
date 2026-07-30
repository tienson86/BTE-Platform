# Golden Dataset Review Guide

**Document:** REVIEW_GUIDE  
**Module:** knowledge/golden_dataset  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Golden Dataset framework cases before Official publication.

Complements Governance procedures without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts case metadata and placeholders |
| Domain Reviewer | Checks domain fit and category |
| Validation Reviewer | Checks Input/Expected completeness and tolerance |
| Traceability Reviewer | Checks Knowledge / Rule / Sentence / Reference links |
| Approver | Sets Status to Official |

---

## Preconditions

- Dataset ID allocated from the correct domain range
- File created from domain or root template
- No duplicate identity collision in domain INDEX
- Domain matches directory

---

## Review Steps

### Step 1 — Identity

- [ ] ID format valid (`CASE-NNNNNN`)
- [ ] ID not reused
- [ ] Title clear and unique within domain

### Step 2 — Contract

- [ ] Input present for Official
- [ ] Expected Output present for Official
- [ ] Tolerance Policy declared
- [ ] Score section coherent when scoring is in scope

### Step 3 — Mapping

- [ ] Knowledge / Rules / Sentences / References valid when present
- [ ] No invented IDs

### Step 4 — Quality and Traceability

- [ ] Passes `QUALITY_STANDARD.md`
- [ ] Passes `VALIDATION_STANDARD.md`
- [ ] Traceability level adequate for Status
- [ ] Edge cases handled per `EDGE_CASES.md`

### Step 5 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes / registry |
| Request changes | Remain Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official cases |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Dataset ID | CASE-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Framework Phase Note

No dataset content reviews occur in V1.0.0 scaffolding.
