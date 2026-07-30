# Knowledge Change Control

**Component:** Knowledge Governance Center  
**Version:** V1.0.0  
**Status:** Frozen (Change Control Specification)

---

# 1. Purpose

This document defines change-control rules for all Knowledge Layer subjects.

---

# 2. Change Principle

```text
Published versions are immutable.
All semantic change creates a new version under review and approval.
```

---

# 3. Change Classes

| Class | Examples | Controls |
|-------|----------|----------|
| Content PATCH | Backward-compatible knowledge correction | Review + Gates + Approval |
| Content MINOR | Additive compatible knowledge | Review + Gates + Approval |
| Content MAJOR | Breaking knowledge semantics | Multi-owner review + Migration + Matrix update |
| Control-Plane Contract | Registry / Loader / SDK API or policy | Standards + layer owners |
| Compatibility / Dependency | Edge or matrix changes | Standards + affected owners |
| Metadata-only | Non-semantic catalog metadata | Governed lightweight review |

---

# 4. Allowed In-Place Updates

For a published version, only non-semantic catalog metadata and lifecycle status transitions may change in place, subject to audit.

Knowledge content, rule semantics, and public contracts do not change in place.

---

# 5. Change Workflow

```text
Propose
  │
  ▼
Classify Change
  │
  ▼
Review
  │
  ▼
Quality Gates
  │
  ▼
Approve
  │
  ▼
Publish New Version / Status Transition
  │
  ▼
Notify Consumers (if material)
  │
  ▼
Audit Record
```

---

# 6. Impact Analysis Requirements

Material changes must identify:

- affected modules/assets
- affected Registry/Loader/SDK contracts
- affected engines
- compatibility impact
- migration/deprecation needs
- rollback Compatible set

---

# 7. Forbidden Changes

- silent production hotfix of published knowledge content without new version
- engine-side embedded knowledge to bypass failed knowledge changes
- undocumented removal of required dependencies
- SDK bypass introduced as a convenience change

---

# 8. Acceptance Criteria

Change Control is accepted when classes, immutability rules, workflow, impact analysis, and forbidden changes are complete.
