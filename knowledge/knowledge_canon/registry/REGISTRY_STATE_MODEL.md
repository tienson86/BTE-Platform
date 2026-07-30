# Registry State Model

> **Document ID:** REG-STATE-001
>
> **Version:** V1.0.0
>
> **Status:** Official

---

# 1. Purpose

Defines the lifecycle state model for Registry Records.

---

# 2. Official Lifecycle

Draft

↓

Validated

↓

Approved

↓

Registered

↓

Published

↓

Deprecated

↓

Archived

---

# 3. State Definitions

## Draft

Initial registration.

Editable.

---

## Validated

Metadata validation passed.

---

## Approved

Governance approval completed.

---

## Registered

Official Registry Record created.

Available internally.

---

## Published

Visible to runtime systems.

---

## Deprecated

Historical.

May still resolve references.

---

## Archived

Read-only.

Permanent storage.

---

# 4. Transition Rules

Draft

↓

Validated

↓

Approved

↓

Registered

↓

Published

↓

Deprecated

↓

Archived

Rejected records return to Draft.

---

# 5. Permissions

Author

Create Draft

Reviewer

Validate

Governance

Approve

Registry Service

Register

Administrator

Archive

---

# 6. Runtime Visibility

| State | Discovery |
|--------|-----------|
| Draft | Hidden |
| Validated | Hidden |
| Approved | Hidden |
| Registered | Internal |
| Published | Public |
| Deprecated | Public (Deprecated) |
| Archived | Historical |

---

# 7. Rollback

Rollback allowed only before Published.

Published rollback requires Governance approval.

---

# 8. Compliance

No unpublished Registry Record may be exposed through public APIs.