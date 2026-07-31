# Design Rules — Fundamental Knowledge

**Path:** `design/DESIGN_RULES.md`  
**Version:** V1.0.0  
**Status:** Official Framework (process only)  

---

## 1. Purpose

Define process rules for Academic Design.  
No academic knowledge is defined here.

---

## 2. Naming rules

| Asset | Rule |
|-------|------|
| Design file | `<PLANNING-ID>_DESIGN.md` under pack `records/` |
| Planning ID | `FND-INV-NNN` (immutable in inventory) |
| Knowledge ID | `KNO-NNNNNN` only after Global Allocator |
| Canonical Name | Title Case; singular; stable |
| Pack folders | `PACK_NN` zero-padded |

Do not use Planning IDs as Knowledge IDs.

---

## 3. Document lifecycle

```text
Template copy
  → Draft design
  → Technical Review
  → Academic Review
  → Approved design
  → (optional) Compiler input
  → Frozen design (with module freeze)
```

Statuses: `Not Started` → `In Design` → `Design Complete` → `Approved` → `Frozen`

---

## 4. Review workflow

1. Author completes `RECORD_DESIGN_TEMPLATE` sections (structure + authorized academic text only when Design phase allows)  
2. Technical Review: IDs, links, checklist, no invented REF/TERM/KNO  
3. Academic Review: scholarly accuracy (when content exists)  
4. Update pack `REVIEW.md` and `DESIGN_PROGRESS.md`  

---

## 5. Approval workflow

| Gate | Approver |
|------|----------|
| Technical | Technical Reviewer |
| Academic | Academic Reviewer |
| Compilation authorization | Governance / module owner |
| Official JSON write | After compiler gates pass |

Blocked ownership (`TODO_REVIEW`) cannot be Approved for Official JSON.

---

## 6. Freeze workflow

1. All pack records Design Complete + Academic Approved (or link-only design notes complete)  
2. `DESIGN_ORDER.md` / `DESIGN_PROGRESS.md` show Freeze Candidate  
3. Module Freeze decision recorded  
4. No silent redesign of frozen designs without MAJOR change process  

---

## 7. Version policy

| Asset | Versioning |
|-------|------------|
| Design framework docs | Semantic MAJOR.MINOR.PATCH |
| Individual design files | Track in Governance Notes + revision table when content exists |
| Knowledge Records (future) | Record metadata.version |

Breaking process changes require MAJOR bump of this document.

---

## 8. Prohibitions

- Inventing academic content outside Academic Design authorization  
- Generating JSON from incomplete designs  
- Modifying Foundation / Architecture / schemas in Design phase  
- Duplicating Canon-owned concepts as BaZi Official JSON  
