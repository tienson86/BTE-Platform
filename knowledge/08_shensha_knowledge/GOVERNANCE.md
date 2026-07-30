# ShenSha Knowledge Governance

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines governance for ShenSha Knowledge.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| ShenSha Knowledge | ShenSha Domain Owner |
| Fundamental references | Fundamental Domain Owner |
| ShenSha Engine | ShenSha Engine Owner |

---

# 3. Review Process

Review shall confirm:

- KMS / KAS / Knowledge Architecture conformance
- complete V1.0 ShenSha domain coverage
- no runtime logic in assets
- no repository-path contracts
- no illegal redefinition of Fundamental Knowledge
- no Strength / Temperature / Pattern / Useful God / Ten Gods / Combination recomputation ownership leakage
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
- ShenSha Engine consumer notification plan

---

# 8. Compatibility Policy

ShenSha Knowledge shall remain compatible with declared Fundamental Knowledge and ShenSha Engine ranges, or explicitly increment MAJOR when incompatible.

---

# 9. Acceptance Criteria

Governance is effective when ownership, review, approval, change control, deprecation, and migration controls are enforced.
