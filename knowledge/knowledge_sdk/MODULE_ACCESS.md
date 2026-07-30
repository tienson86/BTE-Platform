# Knowledge SDK Module Access

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Module Access Specification)

---

# 1. Purpose

This document defines engine-facing access to Knowledge Modules through the SDK.

---

# 2. GetModule()

GetModule returns a declarative ModuleView.

Preconditions:

- consumer authorized
- module version resolved or explicitly provided
- KnowledgeSession bound (for materialised access)
- integrity/compatibility gates passed via Loader

ModuleView exposes:

- module_id / version / domain
- status
- asset inventory summaries / handles
- metadata summary
- KnowledgeReferences

ModuleView does not expose execution hooks.

---

# 3. FindModule()

FindModule queries Registry-backed catalog identity.

It may return catalog metadata without loading full module content.

Production engines that require content must follow with session bind + GetModule.

---

# 4. ListModules()

ListModules returns filtered module summaries for discovery and administration-aware consumers.

Default engine visibility is Published modules unless policy authorizes otherwise.

---

# 5. Session Binding

Module content access is bound to KnowledgeSession freeze guarantees.

Changing module version mid-request requires an explicit new session bind or governed reload path; silent replacement is forbidden.

---

# 6. Error Conditions

Module Access may raise:

- NotFound
- AuthorizationError
- VersionResolutionError
- CompatibilityError
- IntegrityError
- SessionStateError

---

# 7. Acceptance Criteria

Module Access is accepted when Get/Find/List semantics, session freeze rules, and non-execution guarantees are complete.
