# Combination Knowledge Governance

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines governance for Combination Knowledge.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| Combination Knowledge | Combination Domain Owner |
| Fundamental references | Fundamental Domain Owner |
| Combination Engine | Combination Engine Owner |

---

# 3. Review Process

Review shall confirm:

- KMS / KAS / Knowledge Architecture conformance
- complete V1.0 Combination domain coverage
- no runtime logic in assets
- no repository-path contracts
- no illegal redefinition of Fundamental Knowledge
- no Strength / Temperature / Pattern / Useful God / Ten Gods recomputation ownership leakage
- validation and quality gate passage

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

---

# 5. Change Control

Published assets are immutable within a version.

Corrections require new version publication, validation, approval, and changelog updates.

---

# 6. Deprecation Policy

Deprecated versions shall:

- remain readable during compatibility windows
- advertise successors
- reject new bindings
- retain audit history

---

# 7. Migration Policy

Breaking changes require:

- MAJOR version
- migration notes
- compatibility impact statement
- dataset updates
- Combination Engine consumer notification plan

---

# 8. Compatibility Policy

Combination Knowledge shall remain compatible with declared Fundamental Knowledge and Combination Engine ranges, or explicitly increment MAJOR when incompatible.

---

# 9. Acceptance Criteria

Governance is effective when ownership, review, approval, change control, deprecation, and migration controls are enforced.
