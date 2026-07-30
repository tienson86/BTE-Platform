# Role Definitions

**Module:** `knowledge/governance`  
**Document:** ROLE_DEFINITIONS  
**Version:** V1.0.0  
**Status:** Official Foundation (Freeze Candidate)  

---

## 1. Purpose

Define ownership and responsibilities for Knowledge Foundation assets.

---

## 2. Roles

| Role | Primary responsibility |
|------|------------------------|
| Knowledge Author | Draft records, docs, and metadata; mark uncertainty as `TODO_REVIEW` |
| Technical Reviewer | Structure, IDs, JSON validity, cross-links, naming, directory consistency |
| Academic Reviewer | Scholarly accuracy of bibliographic and terminology content |
| Governance Owner | Policy compliance, approval, release authorization |
| Platform Maintainer | Automation hooks, validators, CI wiring (no academic invention) |

---

## 3. Responsibilities by asset

| Asset | Author | Technical Review | Academic Review | Approval |
|-------|--------|------------------|-----------------|----------|
| Reference Library | Author | Required | Required for Official promotion | Governance Owner |
| Terminology Library | Author | Required | Required for Official promotion | Governance Owner |
| Citation Rules | Author | Required | Optional (mechanics only) | Governance Owner |
| Governance docs | Governance Owner | Required | Optional | Governance Owner |

---

## 4. Separation of duties

1. Author of a change SHOULD NOT be the sole Approver for Official promotion.
2. Technical Review does not replace Academic Review for classical metadata.
3. Academic Review does not waive Technical validation failures.
4. Locked modules (`schema`, `knowledge_canon`, `rule_database`, engines, applications, tests) are out of scope for Foundation-only authors unless separately authorized.

---

## 5. Ownership (Foundation V1.0)

| Module | Owning team (logical) |
|--------|------------------------|
| `knowledge/references` | Knowledge Foundation / Reference Owners |
| `knowledge/terminology` | Knowledge Foundation / Terminology Owners |
| `knowledge/citation_rules` | Knowledge Foundation |
| `knowledge/governance` | Governance Owners |

---

## 6. Related documents

- `REVIEW_PROCESS.md`
- `CHANGE_POLICY.md`
- `RELEASE_POLICY.md`
- `architecture/07_GOVERNANCE_ROLES.md`
