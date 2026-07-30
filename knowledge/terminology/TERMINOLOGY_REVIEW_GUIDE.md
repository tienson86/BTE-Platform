# Terminology Review Guide

**Document:** TERMINOLOGY_REVIEW_GUIDE  
**Module:** knowledge/terminology  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define review procedure for Terminology Framework records before Official publication.

This guide complements Governance Terminology Registration without modifying Governance V1.0.

---

## Roles

| Role | Responsibility |
|------|----------------|
| Author | Drafts metadata and definition |
| Domain Reviewer | Checks domain placement and doctrinal fit |
| Editorial Reviewer | Checks language clarity and style |
| Traceability Reviewer | Checks References / Related IDs |
| Approver | Moves Status to Official |

---

## Preconditions

- Terminology ID allocated in `TERMINOLOGY_INDEX.md`
- File created from domain or root template
- No duplicate English / Chinese identity found in indexes
- Domain matches directory

---

## Review Steps

### Step 1 — Identity Check

- [ ] ID format valid (`TERM-NNNNNN`)
- [ ] ID not reused
- [ ] English unique within domain (or justified alias relationship)
- [ ] Chinese / Traditional / Simplified consistent

### Step 2 — Definition Check

- [ ] Definition present and non-circular
- [ ] Definition does not invent unverified doctrine as fact
- [ ] Aliases listed without conflicting Official definitions

### Step 3 — Classification Check

- [ ] Category appropriate
- [ ] Domain correct
- [ ] School set or explicitly `Unspecified`

### Step 4 — Usage and Examples

- [ ] Usage guidance present for Official status
- [ ] Examples do not contradict definition
- [ ] Placeholder examples removed before Official

### Step 5 — Traceability Check

- [ ] References use valid `REF-*` IDs when present
- [ ] Related Terms use valid `TERM-*` IDs when present
- [ ] Knowledge / Rules / Sentences IDs valid when present
- [ ] No invented IDs

### Step 6 — Quality Gate

- [ ] Passes `TERMINOLOGY_QUALITY_STANDARD.md`
- [ ] Edge cases handled per `EDGE_CASES.md`
- [ ] Mapping rules respected per `TERMINOLOGY_MAPPING_STANDARD.md`

### Step 7 — Decision

| Outcome | Action |
|---------|--------|
| Approve | Status → Official; update indexes |
| Request changes | Status remains Draft/Review with comments |
| Reject | Return to Draft with reason |
| Deprecate | Only for previously Official terms |

---

## Review Record (Suggested)

| Field | Value |
|-------|-------|
| Term ID | TERM-NNNNNN |
| Reviewer | |
| Date | YYYY-MM-DD |
| Outcome | Approve / Changes / Reject |
| Notes | |

---

## Non-Goals

- Does not modify Governance procedures text
- Does not authorize Reference Framework edits
- Does not populate term content in framework phase
