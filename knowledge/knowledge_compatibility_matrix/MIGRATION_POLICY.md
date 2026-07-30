# Knowledge Compatibility Migration Policy

**Component:** Knowledge Compatibility Matrix  
**Version:** V1.0.0  
**Status:** Frozen (Migration Policy Specification)

---

# 1. Purpose

This document defines migration requirements when compatibility cannot be preserved by additive upgrade alone.

---

# 2. When Migration Is Required

Migration is required when:

- a subject issues a MAJOR version with breaking semantics
- a required dependency is removed or redirected incompatibly
- classification identities change such that evidence dependents break
- SDK/Loader/Registry contracts break for engines
- matrix status becomes CompatibleWithMigration or Incompatible for current production pairs

---

# 3. Migration Artifacts

Every migration shall provide:

| Artifact | Requirement |
|----------|-------------|
| Migration Notes | What changed and why |
| Impact Statement | Affected modules, assets, engines |
| Compatibility Matrix Delta | Old/new statuses and ranges |
| Version Mapping | Old version → successor version |
| Dual-Run Window | Optional period where old and new are both resolvable |
| Rollback Set | Last known Compatible set |
| Consumer Notification | Declared consumers informed |

---

# 4. CompatibleWithMigration Rules

Status CompatibleWithMigration means:

- co-selection is allowed only after governed migration steps are applied;
- automatic silent resolution to the new pair is forbidden until migration acknowledgment policy is satisfied;
- dual-run may be used to reduce cutover risk.

---

# 5. Incompatible Migration Path

For Incompatible pairs:

1. publish successor versions
2. update matrix (old pair Incompatible; new pair Compatible)
3. migrate consumers to successors
4. deprecate old versions
5. retire old versions after window

No production traffic may continue on Incompatible pairs.

---

# 6. Layer-Specific Migration Notes

## Knowledge Modules / Assets

Preserve KnowledgeReferences where possible; if identities break, provide mapping tables and MAJOR bump dependents.

## Registry / Loader / SDK

Migrate in control-plane order; engines must not be pointed at broken intermediate stacks.

## Analysis / Interpretation / Report Engines

Migrate SDK client contracts first; then module ranges; verify stage/module pairs and explainability KnowledgeReferences.

---

# 7. Dual-Run and Freeze

During dual-run, each request still freezes one Compatible snapshot set.

A single request must not mix old and new Incompatible identities.

---

# 8. Completion Criteria

Migration is complete when:

- all declared consumers bind to successor Compatible ranges;
- old Incompatible versions no longer accept new production bindings;
- matrix and changelog records are published;
- rollback set remains documented for the retention window.

---

# 9. Acceptance Criteria

Migration Policy is accepted when triggers, artifacts, status handling, layer notes, and completion criteria are complete.
