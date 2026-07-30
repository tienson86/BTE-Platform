# Sentence Review Guide

**Document:** SENTENCE_REVIEW_GUIDE  
**Module:** knowledge/sentence_library  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Sentence Library framework records before Official publication.

Complements Governance procedures without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts sentence metadata and template placeholders |
| Domain Reviewer | Checks domain fit and category |
| Editorial Reviewer | Checks tone, style, language clarity |
| Traceability Reviewer | Checks Knowledge / Rule / Reference links |
| Approver | Sets Status to Official |

---

## Preconditions

- Sentence ID allocated from the correct domain range
- File created from domain or root template
- No duplicate title/identity collision in domain INDEX
- Domain matches directory

---

## Review Steps

### Step 1 — Identity

- [ ] ID format valid (`SEN-NNNNNN`)
- [ ] ID not reused
- [ ] Title clear and unique within domain

### Step 2 — Communicative Contract

- [ ] Category / Tone / Style / Language declared
- [ ] Template present for Official status
- [ ] Variables list complete vs placeholders
- [ ] Conditions present for Official status

### Step 3 — Mapping

- [ ] Knowledge Links valid when present
- [ ] Rule Links valid when present
- [ ] Reference Links valid when present
- [ ] No invented IDs

### Step 4 — Quality and Traceability

- [ ] Passes `SENTENCE_QUALITY_STANDARD.md`
- [ ] Traceability level adequate for Status
- [ ] Edge cases handled per `EDGE_CASES.md`

### Step 5 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes / registry |
| Request changes | Remain Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official sentences |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Sentence ID | SEN-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Framework Phase Note

No sentence content reviews occur in V1.0.0 scaffolding.
