# Knowledge Deprecation Policy

**Component:** Knowledge Governance Center  
**Version:** V1.0.0  
**Status:** Frozen (Deprecation Policy Specification)

---

# 1. Purpose

This document defines deprecation and retirement policy for Knowledge Layer subjects.

---

# 2. Lifecycle States

```text
Draft → Validated → Published → Deprecated → Retired
```

Optional archival retention may follow retirement according to retention policy.

---

# 3. Deprecation Principles

- Deprecation is announced before retirement
- Deprecated versions remain resolvable during compatibility windows
- Successors must be declared
- New production bindings should warn or reject according to policy
- Historical KnowledgeReferences remain explainable

---

# 4. Deprecation Package

A deprecation action shall include:

| Item | Requirement |
|------|-------------|
| Subject identity / version | Exact |
| Reason | Why deprecated |
| Successor | Replacement identity/version |
| Compatibility window | Start/end or duration policy |
| Consumer impact | Affected engines/modules |
| Migration notes | How to move |
| Notification record | Evidence of notice |

---

# 5. Retirement Rules

Retired subjects:

- reject new production bindings
- remain readable for historical resolution per retention policy
- must not be selected by default ResolveVersion policies

---

# 6. Applicability

Deprecation policy applies to:

- Knowledge Modules and Assets
- Registry/Loader/SDK specification versions where contracts retire
- Compatibility Matrix entries that are superseded
- Engine-supported SDK ranges no longer maintained

---

# 7. Emergency Withdrawal

If a published version is critically defective:

1. quarantine / deprecate immediately under emergency approval
2. block new production bindings
3. publish corrected successor
4. complete retrospective review and audit

Integrity fail-closed behavior remains mandatory.

---

# 8. Acceptance Criteria

Deprecation Policy is accepted when states, principles, package contents, retirement rules, and emergency withdrawal controls are complete.
