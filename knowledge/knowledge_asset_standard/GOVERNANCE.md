# Governance

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines governance for Knowledge Assets: review, approval, change control, deprecation, and migration.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| Knowledge Asset Standard | Platform Architecture |
| Knowledge Module | Domain Owner |
| Knowledge Asset | Owning Knowledge Module Domain Owner |
| Runtime Engines | Engine Domain Owners |

---

# 3. Review Workflow

Publication candidates shall be reviewed for:

- KAS conformance
- KMS conformance
- Knowledge Architecture conformance
- taxonomy correctness
- cross-reference integrity
- validation and quality gate passage
- absence of repository-path contracts

---

# 4. Approval Workflow

```text
Draft
  │
  ▼
Validate
  │
  ▼
Review
  │
  ▼
Approve
  │
  ▼
Publish
```

Published status requires recorded approval.

---

# 5. Change Control

Published assets are immutable.

Corrections require new versions, validation, approval, and changelog updates through the owning module.

---

# 6. Deprecation

Deprecated assets shall:

- remain readable during compatibility windows
- advertise successors
- reject new bindings
- retain audit history

---

# 7. Migration

Breaking changes require:

- MAJOR version increment
- migration notes
- compatibility impact statement
- dataset updates
- consumer notification plan

---

# 8. Separation Enforcement

Governance prohibits:

- business knowledge inside Runtime Engines
- engine algorithms inside Knowledge Assets
- path-coupled public contracts
- unpublished asset consumption in production

---

# 9. Acceptance Criteria

Governance is effective when ownership, approvals, audits, and separation rules are enforced for every published asset.
