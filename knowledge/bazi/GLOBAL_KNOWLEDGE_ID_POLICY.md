# Global Knowledge ID Policy

> **Document ID:** BAZI-ID-POLICY-001  
> **Path:** `knowledge/bazi/GLOBAL_KNOWLEDGE_ID_POLICY.md`  
> **Version:** V1.0.0  
> **Status:** Draft — Awaiting Architecture Approval  
> **Normative ADR:** ADR-0001, ADR-0007  

---

## 1. Purpose

Define identifier namespaces used across BaZi knowledge planning and platform Knowledge Records.

This policy does **not** allocate academic IDs in this sprint.

---

## 2. Namespaces

| Namespace | Pattern | Purpose |
|-----------|---------|---------|
| Planning / Inventory ID | `FND-INV-NNN` (module-specific prefixes allowed) | Planning only |
| Knowledge ID | `KNO-NNNNNN` | Immutable academic record identity |
| Reference ID | `REF-NNNNNN` | Bibliographic source (Foundation) |
| Terminology ID | `TERM-NNNNNN` | Canonical term (Foundation) |
| Relationship instance | no separate global ID required | Expressed inside record `relationships` pointing at `KNO-*` |

Optional future relationship instance IDs (if introduced) MUST NOT collide with `KNO` / `REF` / `TERM` and require a new ADR.

---

## 3. Planning IDs

- Issued by module inventories (e.g. `KNOWLEDGE_INVENTORY.md`)
- Mutable until Phase 2 design freeze for that row
- NEVER used as `identity.knowledge_id`

---

## 4. Inventory IDs

Inventory IDs are Planning IDs listed in inventory tables.

Synonym in this policy:

`Inventory ID` = `Planning ID`

---

## 5. Knowledge IDs

Rules:

1. Format: `KNO-` + 6 digits  
2. **Globally sequential** across the entire platform  
3. **No allocation by module** and no private reserved ranges going forward  
4. Issued only by the Global Knowledge ID Allocator  
5. Immutable after first Official publication  
6. Until issued: record `PENDING_GLOBAL_ALLOCATOR` / `TODO_ALLOCATE` in plans

### Conceptual binding chain

```text
FND-INV-001          Planning / Inventory ID
        ↓
KNO-000001           Knowledge ID (example only — not implied equality of numeric suffix)
        ↓
REF-000001           Reference ID cited by that Knowledge Record (example)
```

Numeric suffixes across namespaces are **independent**.

`FND-INV-001` does not mean `KNO-000001`.  
`KNO-000001` citing `REF-000001` is coincidence of examples, not a rule.

---

## 6. Reference IDs

- Owned by Foundation Reference Library (`knowledge/references/`) — frozen  
- Knowledge Records cite existing `REF-*`  
- Do not invent Reference IDs inside BaZi modules  

---

## 7. Relationship IDs

- Relationships are structured links to target `KNO-*` (and typed relation names)
- No mandatory separate global `REL-*` namespace in V1.0  
- Bidirectional consistency is a validation concern, not a second ID space  

---

## 8. Version policy

| Asset | Versioning |
|-------|------------|
| This policy document | Semantic `MAJOR.MINOR.PATCH` |
| Knowledge Records | Record `metadata.version` + module CHANGELOG |
| Planning IDs | Not versioned; tracked via inventory revision table |
| Knowledge IDs | Immutable; never reused after Official issue |

Breaking ID policy changes require a new ADR + MAJOR version of this document.

---

## 9. Legacy note (locked Canon)

Historical Canon INDEX “Reserved Range” tables exist under locked Canon modules.

Under ADR-0001 they are **provisional legacy**. Reconciliation requires a future authorized Canon governance sprint. This policy document does not modify Canon files.

---

## 10. Allocator checklist (future)

Before Phase 4 JSON for `module_owned` rows:

1. Confirm Global Allocator process owner  
2. Issue next free `KNO-*`  
3. Bind Planning ID → Knowledge ID in inventory / design plan  
4. Never reuse retired IDs  
