# Knowledge Compatibility Upgrade Policy

**Component:** Knowledge Compatibility Matrix  
**Version:** V1.0.0  
**Status:** Frozen (Upgrade Policy Specification)

---

# 1. Purpose

This document defines how upgrades are performed across Knowledge Modules, Assets, SDK, Registry, Loader, and Runtime Engines without violating compatibility.

---

# 2. Upgrade Principles

- Prefer additive MINOR/PATCH upgrades within Compatible ranges
- Preserve SDK as the sole engine knowledge interface across upgrades
- Upgrade dependencies before dependents when required contracts expand
- Never skip compatibility validation
- Record matrix updates before production cutover

---

# 3. Upgrade Order (Control Plane)

Recommended order for V1.x compatible upgrades:

```text
1. Knowledge Standards (Architecture / KMS / KAS) if needed
2. Knowledge Registry
3. Knowledge Loader
4. Knowledge SDK
5. Knowledge Modules / Assets
6. Analysis Engine
7. Interpretation Engine
8. Report Engine
```

Dependents upgrade only after required dependency targets are Compatible.

---

# 4. Upgrade Classes

| Class | When | Matrix Action |
|-------|------|---------------|
| PATCH | Backward-compatible correction | Usually no range change; notes optional |
| MINOR | Backward-compatible addition | Extend ranges if needed; keep Compatible |
| MAJOR | Breaking change | New MAJOR identities; mark old pairs Incompatible or CompatibleWithMigration |

---

# 5. Knowledge Module / Asset Upgrades

- Publish new module/asset versions first in Registry
- Update Compatibility Matrix entries for Fundamental / evidence / consumer ranges
- Switch SDK resolution defaults only after Validate Compatibility passes
- Keep prior Published versions resolvable during compatibility windows

---

# 6. Engine Upgrades

- Engines may upgrade independently only within declared SDK Compatible range
- If an engine requires new SDK APIs, upgrade SDK first (MINOR/MAJOR as appropriate)
- Stage-module pairing must remain Compatible after engine upgrade

---

# 7. Rollback Rules

Rollback is allowed only to a previously Compatible co-selection set.

Rollback must not invent ad hoc mixed versions absent from the matrix.

---

# 8. Production Cutover Checklist

1. Matrix entries published
2. Registry catalog revision includes new versions
3. Loader/SDK Validate Compatibility succeeds
4. Golden/validation evidence for upgraded modules where required
5. Consumer notification recorded
6. Rollback Compatible set identified

---

# 9. Acceptance Criteria

Upgrade Policy is accepted when principles, order, classes, rollback, and cutover checklist are complete.
