# Knowledge Loader Governance

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines governance for Knowledge Loader behavior and change control.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| Knowledge Loader | Loader Owner |
| Knowledge Registry | Registry Owner |
| Knowledge Standards (Architecture / KMS / KAS) | Knowledge Standards Owner |
| Runtime Engines | Engine Owners |

---

# 3. Governance Principles

- Engines consume knowledge only through Loader
- Loader consumes catalog authority only through Registry
- Correctness and integrity outrank convenience
- Loader policy changes are versioned and reviewed
- No ad hoc semantic bypasses in production

---

# 4. Policy Control

Governed Loader policies include:

- default LoadMode by consumer class
- cache retention classes
- version selection precedence
- allowed substitute recovery rules
- visibility of non-published statuses

Policy changes require review and versioned release notes.

---

# 5. Approval Workflow for Loader Spec Changes

```text
Propose
  │
  ▼
Review (Standards + Registry + Engine representatives)
  │
  ▼
Approve
  │
  ▼
Publish Loader Spec Version
```

---

# 6. Incident Governance

Integrity or compatibility incidents require:

- quarantine of affected cache entries
- consumer notification
- root-cause record
- corrective Reload / Refresh procedures

---

# 7. Acceptance Criteria

Governance is effective when ownership, policy control, approval, and incident controls are enforced.
