# Architecture Decision Records — Knowledge Layer

> **Document ID:** BTE-ADR-INDEX-001  
> **Path:** `knowledge/ARCHITECTURE_DECISIONS.md`  
> **Version:** V1.0.0  
> **Status:** Draft — Awaiting Architecture Approval  
> **Scope:** Knowledge architecture only (no academic content)  

---

## Index

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | Global Knowledge ID Policy | Proposed |
| ADR-0002 | Single Source of Truth | Proposed |
| ADR-0003 | Module Ownership Rules | Proposed |
| ADR-0004 | Canon Link Policy | Proposed |
| ADR-0005 | Cross Module Reference Policy | Proposed |
| ADR-0006 | Knowledge Lifecycle | Proposed |
| ADR-0007 | Inventory Planning Keys | Proposed |

---

# ADR-0001 — Global Knowledge ID Policy

## Status

Proposed

## Context

Inventory Phase 1 used provisional per-domain ID ranges (via Canon INDEX documents) and `TODO_ALLOCATE` for BaZi module-owned concepts. This creates collision risk and ambiguous ownership of the allocator.

## Decision

1. Knowledge IDs (`KNO-NNNNNN`) are **globally sequential**.
2. **No module** may reserve or allocate its own private ID range.
3. A single Global Knowledge ID Allocator (process/registry) issues the next free `KNO-*`.
4. Planning / inventory keys never become Knowledge IDs by renaming.
5. Reference IDs (`REF-*`) and Terminology IDs (`TERM-*`) remain separate namespaces (Foundation).

## Consequences

- Legacy per-module “Reserved Range” notes in locked Canon INDEX files are **historical / provisional** until reconciled under this ADR (Canon files remain locked; reconciliation is a future authorized change).
- BaZi inventory rows keep `TODO_ALLOCATE` until the global allocator assigns IDs.
- Design docs may state **Expected Knowledge ID = PENDING_GLOBAL_ALLOCATOR**.

## See also

`knowledge/bazi/GLOBAL_KNOWLEDGE_ID_POLICY.md`

---

# ADR-0002 — Single Source of Truth

## Status

Proposed

## Context

The same concept (e.g. Wood, Jia, Zi) could appear in Knowledge Canon and BaZi Fundamental inventories.

## Decision

1. Each academic concept has **exactly one** authoritative Knowledge Record location.
2. Downstream modules **link** to that record; they do not rewrite it.
3. If a concept already belongs to Knowledge Canon, BaZi modules treat it as `canon_link`.
4. Duplicate Official records for the same concept are forbidden.

## Consequences

- BaZi `01_fundamental_knowledge` owns only BaZi-specific structural concepts (e.g. Four Pillars, Day Master) unless Architecture reassigns ownership.
- Canon remains SSOT for Wu Xing, stems, branches, hidden stems, yin-yang domain concepts already placed there.

---

# ADR-0003 — Module Ownership Rules

## Status

Proposed

## Context

Inventory used `canon_link`, `module_owned`, and `todo_architecture`.

## Decision

| Owner type | Rule |
|------------|------|
| Knowledge Canon module | Authors and freezes the canonical record |
| BaZi knowledge module | Authors records only for concepts assigned in the Ownership Matrix |
| Knowledge Foundation | Owns REF / TERM / citation / governance infrastructure — not academic KNO content |
| Consumer modules | May reference owned records; may not redefine them |

Ownership is recorded in:

`knowledge/bazi/MODULE_OWNERSHIP_MATRIX.md`

Uncertain rows remain `TODO_REVIEW` until Architecture Approval.

## Consequences

- Strength / temperature / pattern / etc. modules consume fundamentals; they do not own Yin Yang or Wu Xing definitions.

---

# ADR-0004 — Canon Link Policy

## Status

Proposed

## Context

Many Fundamental inventory rows are concepts already scoped to Knowledge Canon directories.

## Decision

1. `canon_link` means: **no duplicate JSON** under `knowledge/bazi/**/knowledge_records/` for that concept.
2. BaZi design packs may include Canon-linked concepts as **dependency designs** (relationship / usage notes only).
3. JSON generation for Canon-owned concepts happens only under authorized Canon sprints (locked here).
4. BaZi records that need Canon concepts MUST cite Canon `KNO-*` in relationships after IDs exist.

## Consequences

- Phase 2 Pack 01 is primarily dependency / link design for Canon concepts plus any approved module-owned structural companions.
- Phase 4 JSON under BaZi Fundamental applies only to `module_owned` rows with allocated IDs.

---

# ADR-0005 — Cross Module Reference Policy

## Status

Proposed

## Context

Modules must share concepts without free-text-only Official coupling.

## Decision

1. Cross-module academic links MUST use Knowledge IDs (`KNO-*`).
2. Bibliographic evidence MUST use Reference IDs (`REF-*`) from the Foundation Reference Library.
3. Terminology MUST use Foundation canonical terms (`TERM-*`) where registered.
4. Relationship entries MUST use approved relationship types from module specs (e.g. Depends On, Related To).
5. Invented IDs are validation errors.

## Consequences

- Title-only Official citations are invalid.
- Broken `KNO-*` / `REF-*` links block Official promotion.

---

# ADR-0006 — Knowledge Lifecycle

## Status

Proposed

## Context

Need a uniform lifecycle across Canon and BaZi knowledge modules.

## Decision

```text
Inventory (planning)
  → Design (Phase 2)
  → Academic Review (Phase 3)
  → JSON Authoring (Phase 4)
  → Validation (Phase 5)
  → Official / Freeze (Phase 6)
  → Deprecated → Archived (as needed)
```

Record status values:

`draft` → `review` → `official` → `deprecated` → `archived`

Governance Foundation entry docs apply (read-only).

## Consequences

- No skipping Academic Review for Official promotion.
- Freeze is a module gate, not a substitute for per-record Official status.

---

# ADR-0007 — Inventory Planning Keys

## Status

Proposed

## Context

Inventory introduced `FND-INV-NNN` keys.

## Decision

1. Inventory / planning keys (`FND-INV-*`, future `STR-INV-*`, etc.) are **planning identifiers only**.
2. They MUST NOT appear as `identity.knowledge_id` in JSON records.
3. Mapping is many-to-one over time: one planning key eventually binds to at most one Knowledge ID.
4. Chain (conceptual):

```text
FND-INV-001          (planning)
    ↓
KNO-NNNNNN           (knowledge identity — globally allocated)
    ↓
REF-NNNNNN           (bibliographic citation — Foundation library)
```

`FND-INV-001` does **not** imply `KNO-000001`. Numbers are independent namespaces.

## Consequences

- Design plans track Planning ID and Expected Knowledge ID separately.
- Renaming a planning key does not change an issued Knowledge ID.

---

## Approval

| Role | Decision | Date |
|------|----------|------|
| Architecture | Pending | — |
| Academic Lead | Pending | — |
| Implementation | Prepared V1.0.0 draft | 2026-07-31 |
