# Metadata Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Metadata Specification)

---

# 1. Purpose

This document defines mandatory metadata for Knowledge Assets and related control records.

---

# 2. Scope

Metadata is both:

- a Knowledge Asset type
- a cross-cutting requirement on all other assets

---

# 3. Mandatory Metadata Fields

| Field | Requirement |
|-------|-------------|
| author | Creator identity |
| reviewer | Reviewer identity |
| created | Creation timestamp |
| modified | Last modification timestamp |
| version | Version identity |
| compatibility | Compatibility declarations |
| status | Draft / Validated / Published / Deprecated |
| references | Related assets / modules / approvals |

---

# 4. Extended Metadata

Optional but recommended fields include:

- owners
- locale support
- integrity_reference
- approval_reference
- change_summary
- tags / categories

---

# 5. Consistency Rules

- Metadata version must align with owning module package policy.
- Status must match lifecycle governance.
- References must resolve.
- Modified timestamp must not precede created timestamp.

---

# 6. Validation Requirements

Validate completeness, referential integrity, and status legality.

---

# 7. Acceptance Criteria

Metadata is accepted when all mandatory fields are present, consistent, and path-independent.
