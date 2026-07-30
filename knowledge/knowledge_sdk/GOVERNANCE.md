# Knowledge SDK Governance

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines governance for the Knowledge SDK and its engine-facing contracts.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| Knowledge SDK | SDK Owner |
| Knowledge Loader | Loader Owner |
| Knowledge Registry | Registry Owner |
| Knowledge Standards | Knowledge Standards Owner |
| Runtime Engines | Engine Owners |

---

# 3. Governance Principles

- SDK is the only public engine interface to the Knowledge Layer
- SDK contracts are versioned and reviewed
- Semantic bypasses in engines are forbidden
- Correctness and integrity outrank convenience
- Cross-layer changes require multi-owner review

---

# 4. Change Control

Breaking SDK API or semantic changes require MAJOR version increment, migration notes, and engine consumer notification.

Additive compatible APIs may ship in MINOR versions.

---

# 5. Approval Workflow

```text
Propose SDK Change
        │
        ▼
Review (SDK + Loader + Registry + Engine representatives)
        │
        ▼
Approve
        │
        ▼
Publish SDK Spec Version
        │
        ▼
Notify Consumers
```

---

# 6. Policy Governance

Governed SDK policies include:

- default visibility of non-published knowledge
- session freeze/invalidation behavior on Refresh
- privileged cache operation permissions
- retry guidance defaults

---

# 7. Acceptance Criteria

Governance is effective when ownership, change control, approval, and policy controls are enforced.
