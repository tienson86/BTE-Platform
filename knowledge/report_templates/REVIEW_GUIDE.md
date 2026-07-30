# Report Template Review Guide

**Document:** REVIEW_GUIDE  
**Module:** knowledge/report_templates  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Report Template framework records before Official publication.

Complements Governance procedures without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts template metadata and structure |
| Domain Reviewer | Checks domain fit and category |
| Editorial Reviewer | Checks audience, language, section clarity |
| Traceability Reviewer | Checks Knowledge / Rule / Sentence / Reference links |
| Approver | Sets Status to Official |

---

## Preconditions

- Report Template ID allocated from the correct domain range
- File created from domain or root template
- No duplicate identity collision in domain INDEX
- Domain matches directory

---

## Review Steps

### Step 1 — Identity

- [ ] ID format valid (`RPT-NNNNNN`)
- [ ] ID not reused
- [ ] Title clear and unique within domain

### Step 2 — Structure and Audience

- [ ] Structure present for Official
- [ ] Audience / Language / Category coherent
- [ ] No narrative content masquerading as framework structure

### Step 3 — Mapping

- [ ] Knowledge / Rule / Sentence / Reference links valid when present
- [ ] No invented IDs

### Step 4 — Quality and Traceability

- [ ] Passes `QUALITY_STANDARD.md`
- [ ] Traceability level adequate for Status
- [ ] Edge cases handled per `EDGE_CASES.md`

### Step 5 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes / registry |
| Request changes | Remain Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official templates |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Report Template ID | RPT-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Framework Phase Note

No report content reviews occur in V1.0.0 scaffolding.
