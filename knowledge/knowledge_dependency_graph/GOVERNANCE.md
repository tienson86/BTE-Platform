# Knowledge Dependency Governance

**Component:** Knowledge Dependency Graph  
**Version:** V1.0.0  
**Status:** Frozen (Governance Specification)

---

# 1. Purpose

This document defines ownership and change control for Knowledge Dependency Graph contracts.

---

# 2. Ownership

| Subject | Owner |
|---------|-------|
| Knowledge Dependency Graph | Knowledge Standards Owner |
| Knowledge Modules | Domain Owners |
| Knowledge Assets | Domain Owners (under module ownership) |
| Knowledge Registry | Registry Owner |
| Knowledge Loader | Loader Owner |
| Knowledge SDK | SDK Owner |
| Analysis Engine | Analysis Engine Owner |
| Interpretation Engine | Interpretation Engine Owner |
| Report Engine | Report Engine Owner |

---

# 3. Governance Principles

- Dependency direction rules are constitutional
- Required cycles are forbidden
- Engines access knowledge only through SDK
- Evidence dependencies never transfer domain ownership
- Dependency changes are reviewed for cross-layer impact

---

# 4. Change Control

Proposed dependency changes must include:

- affected edges
- compatibility impact
- version impact (MAJOR/MINOR/PATCH)
- migration notes
- consumer notification plan

Cross-layer edges (Module ↔ SDK ↔ Engine) require multi-owner review.

---

# 5. Approval Workflow

```text
Propose Dependency Change
        │
        ▼
Validate against Architecture / Compatibility / Versioning
        │
        ▼
Review (Standards + affected Domain/Engine/Control-plane owners)
        │
        ▼
Approve
        │
        ▼
Publish Spec / Module / Catalog updates
        │
        ▼
Notify Consumers
```

---

# 6. Audit Requirements

Material dependency changes shall retain:

- proposer / approver identities
- before/after edge sets
- compatibility matrix deltas
- effective versions
- timestamps

---

# 7. Enforcement

Registry publication gates and SDK/Loader Validate / ResolveDependency gates enforce declared dependency and compatibility rules at runtime boundaries.

Governance forbids local engine exceptions that violate the graph.

---

# 8. Acceptance Criteria

Governance is effective when ownership, principles, change control, approval, audit, and enforcement controls are complete.
