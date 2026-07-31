# ID Allocation Report

**Sprint:** Fundamental Architecture Resolution V1.0  
**Date:** 2026-07-31  

---

## Policy in force (proposed)

Per ADR-0001 / `GLOBAL_KNOWLEDGE_ID_POLICY.md`:

- Knowledge IDs are **globally sequential**
- **No module-level ID ranges** going forward
- Planning IDs (`FND-INV-*`) never become Knowledge IDs by renaming
- Reference IDs remain Foundation-owned (`REF-*`)

---

## Allocation actions this sprint

| Action | Result |
|--------|--------|
| Issue new `KNO-*` | **None** (architecture sprint only) |
| Bind Planning ID → Knowledge ID | **None** |
| Invent academic IDs | **Forbidden / not done** |

All Pack 01/02 Expected Knowledge ID cells remain:

`PENDING_GLOBAL_ALLOCATOR`

---

## Namespace separation (examples)

```text
FND-INV-001     planning
KNO-000001      knowledge (example number only)
REF-000001      reference (example number only)
```

Numeric suffixes are independent across namespaces.

---

## Legacy collision watchlist (informational; Canon locked)

| Topic | Note |
|-------|------|
| Canon INDEX reserved ranges | Provisional legacy under new global policy |
| Existing draft Canon `KNO-*` usage | Do not remap in this sprint |
| BaZi `module_owned` rows | Await Global Allocator before Phase 4 |

---

## Next allocator steps (after Architecture Approval)

1. Name Global Allocator owner  
2. Define “next free KNO” discovery against all existing records  
3. Bind Pack 02 `module_owned` rows first (recommended)  
4. Update inventory Expected Knowledge ID columns  
