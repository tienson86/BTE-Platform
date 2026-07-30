# Knowledge SDK Version Resolution

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Version Resolution Specification)

---

# 1. Purpose

This document defines ResolveVersion behavior exposed by the Knowledge SDK.

---

# 2. ResolveVersion()

ResolveVersion selects an exact module or asset version for consumer binding.

Inputs:

- identity (module_id or asset_id + module_id)
- version constraints / range / explicit version
- consumer context
- resolution policy

Outputs:

- VersionResolution including exact version, status, and KnowledgeReference

---

# 3. Selection Precedence (Logical)

Deterministic precedence shall consider, in governed order:

1. explicit exact version if provided and eligible
2. consumer-compatible published range
3. recommended published version within range where declared
4. deprecation policy (allow/deny deprecated)
5. fail if ambiguous or unsatisfiable

Exact precedence profile is a governed policy; outcomes must be deterministic for identical inputs and catalog revision.

---

# 4. Compatibility Resolution Collaboration

Version selection must satisfy Compatibility Resolution constraints for:

- requested consumer engine range
- required dependency targets
- standards ranges (KMS/KAS) where declared

---

# 5. Freeze After Selection

Once selected versions enter a KnowledgeSession, they remain frozen for that request.

Later ResolveVersion calls in the same request must not silently change already bound subjects.

---

# 6. Error Conditions

- VersionResolutionError
- CompatibilityError
- NotFound
- AuthorizationError

---

# 7. Acceptance Criteria

Version Resolution is accepted when inputs/outputs, deterministic precedence, compatibility gating, and freeze rules are complete.
