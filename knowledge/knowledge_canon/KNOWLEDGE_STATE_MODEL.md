# Knowledge State Model

> **Document ID:** KC-STATE-001
>
> **Module:** `knowledge/knowledge_canon`
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Lifecycle State Model
>
> **Language:** English
>
> **Governance:** Governance V1.0

---

# 1. Purpose

This document defines the lifecycle state model for all Knowledge Assets managed by the BTE Knowledge Canon.

The objective is to standardize how Knowledge Assets are created, reviewed, approved, published, maintained, deprecated, and archived throughout their lifecycle.

---

# 2. Objectives

The state model shall:

- Define the official lifecycle.
- Prevent invalid state transitions.
- Support governance.
- Enable workflow automation.
- Support auditing.
- Preserve historical integrity.
- Maintain backward compatibility.

---

# 3. Scope

This specification applies to:

- Knowledge Assets
- Knowledge Metadata
- Review Workflow
- Publication Workflow
- Governance Workflow

This specification does not apply directly to runtime engine execution.

---

# 4. Design Principles

The lifecycle shall be:

- Deterministic
- Auditable
- Traceable
- Immutable by History
- Governance Controlled
- Machine Readable

---

# 5. Lifecycle Overview

Official lifecycle:

```
Draft
    │
    ▼
In Review
    │
    ▼
Approved
    │
    ▼
Published
    │
    ▼
Deprecated
    │
    ▼
Archived
```

Rejected assets return to **Draft**.

---

# 6. State Definitions

## Draft

Purpose

Initial creation.

Characteristics

- Editable
- Not published
- Not referenced by runtime engines

Allowed Actions

- Edit
- Delete
- Submit for Review

---

## In Review

Purpose

Formal review.

Characteristics

- Locked for structural changes
- Review comments permitted

Allowed Actions

- Review
- Comment
- Approve
- Reject

---

## Approved

Purpose

Ready for publication.

Characteristics

- Content frozen
- Awaiting governance publication

Allowed Actions

- Publish
- Return to Draft (with justification)

---

## Published

Purpose

Official production knowledge.

Characteristics

- Visible to runtime engines
- Available for APIs
- Available to Rule Engine
- Available to Sentence Library

Allowed Actions

- Minor Metadata Update
- Deprecate

---

## Deprecated

Purpose

Knowledge remains valid historically but should no longer be used for new development.

Characteristics

- Historical only
- Searchable
- Traceable

Allowed Actions

- Archive
- Restore (Governance approval)

---

## Archived

Purpose

Permanent historical preservation.

Characteristics

- Read-only
- No modifications
- No runtime usage

Allowed Actions

None.

---

# 7. State Transition Rules

| Current | Next | Allowed |
|----------|------|----------|
| Draft | In Review | Yes |
| Draft | Archived | No |
| In Review | Approved | Yes |
| In Review | Draft | Yes |
| Approved | Published | Yes |
| Approved | Draft | Yes |
| Published | Deprecated | Yes |
| Published | Draft | No |
| Deprecated | Archived | Yes |
| Deprecated | Published | Yes (Governance Approval) |
| Archived | Any | No |

---

# 8. Transition Conditions

## Draft → In Review

Requirements

- Mandatory metadata complete
- Canonical name assigned
- References attached

---

## In Review → Approved

Requirements

- Technical review passed
- Academic review passed
- Validation passed

---

## Approved → Published

Requirements

- Governance approval
- Quality score meets publication threshold
- Traceability complete

---

## Published → Deprecated

Requirements

One or more:

- Better replacement exists
- Knowledge superseded
- Governance decision

---

## Deprecated → Archived

Requirements

- Historical preservation confirmed
- No active dependencies
- Governance approval

---

# 9. Permissions Matrix

| Role | Draft | Review | Approve | Publish | Deprecate | Archive |
|------|:-----:|:------:|:-------:|:--------:|:----------:|:--------:|
| Author | ✔ | | | | | |
| Reviewer | | ✔ | | | | |
| Domain Expert | | ✔ | ✔ | | | |
| Governance | | | ✔ | ✔ | ✔ | ✔ |

---

# 10. Runtime Visibility

| State | Runtime Engine |
|---------|----------------|
| Draft | Hidden |
| In Review | Hidden |
| Approved | Hidden |
| Published | Visible |
| Deprecated | Read Only |
| Archived | Hidden |

Only **Published** assets shall be used by production engines.

---

# 11. API Visibility

| State | API Access |
|---------|-----------|
| Draft | Internal |
| In Review | Internal |
| Approved | Internal |
| Published | Public |
| Deprecated | Public (Deprecated Flag) |
| Archived | Historical API Only |

---

# 12. Version Interaction

State transitions do not change the identifier.

Version updates follow Semantic Versioning.

Example

```
KNO-000120

Version

1.0.0

↓

1.1.0

↓

2.0.0

Identifier remains

KNO-000120
```

---

# 13. Audit Requirements

Every transition shall record:

- Transition ID
- Previous State
- New State
- Timestamp
- User
- Role
- Reason
- Approval

Transition history shall never be deleted.

---

# 14. Event Model

Each state transition generates an event.

Example

```
EVENT

Knowledge Published

↓

Update Registry

↓

Notify Validator

↓

Notify Rule Loader

↓

Notify Search Index

↓

Refresh API Cache
```

---

# 15. Dependency Rules

Published Knowledge Assets may be referenced by:

- Rules
- Sentences
- Reports
- APIs

Draft assets shall never be referenced externally.

---

# 16. Rollback Policy

Rollback is permitted only when:

- Publication error
- Governance decision
- Critical validation failure

Rollback shall preserve complete history.

---

# 17. Exception Handling

Exceptional transitions require Governance approval.

Examples

- Restore Deprecated Asset
- Emergency Withdrawal
- Manual Publication Override

All exceptions shall be audited.

---

# 18. Governance

Lifecycle governance is responsible for:

- State transition approval
- Publication authorization
- Deprecation approval
- Archive authorization

---

# 19. Compliance

All modules shall respect lifecycle states.

No production component may consume assets outside the permitted visibility rules.

---

# 20. Future Extensions

Future versions may introduce:

- Scheduled publication
- Automatic review reminders
- Workflow automation
- Multi-stage approvals
- Electronic signatures
- Distributed governance

---

# 21. Appendix A – Lifecycle Diagram

```
Draft
   │
   ▼
In Review
   │
   ▼
Approved
   │
   ▼
Published
   │
   ▼
Deprecated
   │
   ▼
Archived
```

---

# 22. Appendix B – State Characteristics

| State | Editable | Searchable | Runtime | API | Audit |
|---------|:--------:|:----------:|:-------:|:---:|:-----:|
| Draft | ✔ | ✖ | ✖ | Internal | ✔ |
| In Review | Limited | ✖ | ✖ | Internal | ✔ |
| Approved | ✖ | ✖ | ✖ | Internal | ✔ |
| Published | Metadata Only | ✔ | ✔ | ✔ | ✔ |
| Deprecated | ✖ | ✔ | Read Only | ✔ | ✔ |
| Archived | ✖ | Historical | ✖ | Historical | ✔ |

---

# 23. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| V1.0.0 | Official | Initial lifecycle state model |