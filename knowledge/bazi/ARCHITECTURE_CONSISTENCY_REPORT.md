# Architecture Consistency Report

**Sprint:** Fundamental Architecture Resolution V1.0  
**Date:** 2026-07-31  
**Status:** Draft for Architecture Approval  

---

## Verdict

Architecture decision pack is **internally consistent** and aligned with Inventory Phase 1 constraints.  
Open items remain only where explicitly marked `TODO_REVIEW` / legacy Canon range reconciliation.

---

## Consistency matrix

| Topic | Decision source | Inventory alignment | Result |
|-------|-----------------|---------------------|--------|
| Global sequential `KNO-*` | ADR-0001 + ID Policy | Replaces module-range `TODO_ALLOCATE` wording | Consistent |
| Planning keys ≠ Knowledge IDs | ADR-0007 | `FND-INV-*` remain planning-only | Consistent |
| Single Source of Truth | ADR-0002 | No duplicate Canon concepts in BaZi JSON | Consistent |
| Canon link-only | ADR-0004 | Wu Xing / stems / branches / hidden / seasonal | Consistent |
| Cross-module refs by ID | ADR-0005 | Matches citation + inventory rules | Consistent |
| Lifecycle | ADR-0006 | Matches Fundamental Phase 1–7 gate | Consistent |
| Ownership matrix covers all INV rows | Ownership Matrix | 44/44 rows | Consistent |
| Pack 01 ⊆ inventory | Phase 2 Plan | Yes | Consistent |
| No academic JSON created | Sprint rules | Confirmed | Consistent |
| Locked modules unmodified | Sprint rules | Confirmed | Consistent |

---

## Known tensions (documented, not silently “fixed”)

1. **Legacy Canon reserved ranges** vs **global sequential policy** — Canon INDEX ranges are locked historical provisional; reconciliation deferred.  
2. **Existing draft Canon record IDs** (e.g. Wood draft) vs future allocator — do not reassign in this sprint.  
3. **Inventory §7** still mentions “BaZi Knowledge ID allocation range” — superseded by ADR-0001; treat inventory sentence as outdated pending inventory edit authorization.

---

## Files produced

| File | Role |
|------|------|
| `knowledge/ARCHITECTURE_DECISIONS.md` | ADR-0001…0007 |
| `knowledge/bazi/MODULE_OWNERSHIP_MATRIX.md` | Ownership |
| `knowledge/bazi/GLOBAL_KNOWLEDGE_ID_POLICY.md` | ID namespaces |
| `knowledge/bazi/PHASE2_DESIGN_PLAN.md` | Pack 01/02 plan |
