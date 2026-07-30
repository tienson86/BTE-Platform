# Knowledge Review Process

**Module:** `knowledge/governance`  
**Document:** REVIEW_PROCESS  
**Version:** V1.0.0  
**Status:** Official Foundation (Freeze Candidate)  

---

## 1. Purpose

Define the Knowledge Foundation review workflow for:

- Reference Library
- Terminology Library
- Citation artifacts
- Governance foundation documents

---

## 2. Knowledge lifecycle

```text
Draft
  → Technical Review
  → Academic Review
  → Official
  → Deprecated (optional)
  → Archived
```

| State | Meaning |
|-------|---------|
| Draft | Authoring in progress; `TODO_REVIEW` allowed |
| Technical Review | Structure, IDs, JSON, links, naming checked |
| Academic Review | Scholarly / bibliographic accuracy checked |
| Official | Approved for platform use |
| Deprecated | Superseded; retained for compatibility |
| Archived | Read-only historical retention |

---

## 3. Approval workflow

```text
Author creates/updates asset (Draft)
        ↓
Technical Review
        ↓
Academic Review (required for References / Terminology Official promotion)
        ↓
Governance Approval
        ↓
Status → Official
   (or return to Draft with findings)
```

---

## 4. Review checklist

### Technical Review

- [ ] Required files present
- [ ] JSON parses
- [ ] IDs match `REF-` / `TERM-` patterns
- [ ] No duplicate IDs / titles / terms
- [ ] Enums valid
- [ ] Indexes consistent
- [ ] Alias/abbreviation targets resolve
- [ ] Validators PASS (0 errors)
- [ ] Locked modules untouched

### Academic Review

- [ ] No invented bibliographic metadata
- [ ] `TODO_REVIEW` used where uncertain
- [ ] Titles / Chinese / pinyin identity acceptable
- [ ] Citation chapter anchors verified or explicitly deferred
- [ ] No silent ID remapping of published works

### Governance Approval

- [ ] VERSION_POLICY bump correct
- [ ] CHANGELOG updated
- [ ] RELEASE_POLICY gates met
- [ ] Ownership / ROLE_DEFINITIONS respected
- [ ] Consumer impact noted (if any)

---

## 5. Ownership and responsibilities

See `ROLE_DEFINITIONS.md`.

Summary:

| Role | Responsibility |
|------|----------------|
| Author | Draft content and metadata |
| Technical Reviewer | Structure, IDs, validation |
| Academic Reviewer | Scholarly accuracy |
| Governance Owner | Policy compliance and release approval |

---

## 6. Related documents

- `ROLE_DEFINITIONS.md`
- `VERSION_POLICY.md`
- `RELEASE_POLICY.md`
- `CHANGE_POLICY.md`
- `knowledge/FOUNDATION_VALIDATION.md`
- `policies/03_REVIEW_POLICY.md`
- `procedures/02_DOCUMENT_REVIEW.md`
