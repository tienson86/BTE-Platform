# Knowledge Inventory — Fundamental Knowledge

> **Document ID:** BAZI-FND-INVENTORY-001  
> **Module:** `knowledge/bazi/01_fundamental_knowledge`  
> **Version:** V1.0.0  
> **Status:** Draft (Phase 1 Complete)  
> **Document Type:** Knowledge Inventory  
> **Language:** English  

---

# 1. Purpose

This inventory lists every Knowledge Record planned for the Fundamental Knowledge module.

It is a **planning and tracking** document only.

It does **not** contain academic definitions, classical exegesis, or populated JSON records.

---

# 2. Development Phases (Module Gate)

| Phase | Name | Status |
|-------|------|--------|
| 1 | `KNOWLEDGE_INVENTORY.md` | **Complete** |
| 2 | Design each Knowledge Record (field-level specs) | Pending Architecture / Academic start |
| 3 | Academic Review of designs | Pending |
| 4 | Generate JSON per approved specs | Pending |
| 5 | Validation (schema / reference / relationship / terminology) | Pending |
| 6 | Freeze Module V1.0 | Pending |
| 7 | Transfer to `02_strength_knowledge` | Pending |

**Stop after Phase 1 until Architecture Review authorizes Phase 2.**

---

# 3. Ownership Rules

Per `FUNDAMENTAL_SPEC.md`: foundational concepts exist in **one location only**.

| Ownership | Meaning |
|-----------|---------|
| `canon_link` | Concept owned by Knowledge Canon; BaZi module cites / depends on Canon `KNO-*` — do not duplicate |
| `module_owned` | Concept is BaZi Fundamental–scoped; record will live under this module’s `knowledge_records/` |
| `todo_architecture` | Ownership unclear — Architecture Review must decide |

Knowledge IDs for `module_owned` rows are **not allocated** in Phase 1.

Use:

`TODO_ALLOCATE`

until Architecture assigns a BaZi Knowledge ID range that does not collide with Canon ranges.

---

# 4. Inventory Index

Local planning keys use:

```text
FND-INV-NNN
```

These are **not** Knowledge IDs.

---

## 4.1 Cosmology and polarity

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-001 | Yin and Yang | Cosmological Concept | `canon_link` | Canon range `KNO-000400–000499` | P0 | Planned (link) |
| FND-INV-002 | Qi | Cosmological Concept | `todo_architecture` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-003 | Cosmological Correspondence Principle | Classical Principle | `todo_architecture` | `TODO_ALLOCATE` | P2 | Planned |

---

## 4.2 Five Elements (Wu Xing)

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-010 | Five Elements | Fundamental Concept | `canon_link` | Canon `01_five_elements` (`KNO-000001–000099`) | P0 | Planned (link) |
| FND-INV-011 | Wood | Fundamental Classification | `canon_link` | Canon Wood record (e.g. `KNO-000001` when Official) | P0 | Planned (link) |
| FND-INV-012 | Fire | Fundamental Classification | `canon_link` | Canon Fire | P0 | Planned (link) |
| FND-INV-013 | Earth | Fundamental Classification | `canon_link` | Canon Earth | P0 | Planned (link) |
| FND-INV-014 | Metal | Fundamental Classification | `canon_link` | Canon Metal | P0 | Planned (link) |
| FND-INV-015 | Water | Fundamental Classification | `canon_link` | Canon Water | P0 | Planned (link) |
| FND-INV-016 | Generating Cycle | Fundamental Relationship | `canon_link` / `todo_architecture` | Prefer Canon relationships; BaZi wrapper only if approved | P1 | Planned |
| FND-INV-017 | Controlling Cycle | Fundamental Relationship | `canon_link` / `todo_architecture` | Prefer Canon relationships; BaZi wrapper only if approved | P1 | Planned |

---

## 4.3 Heavenly Stems

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-020 | Heavenly Stems | Fundamental Concept | `canon_link` | Canon `02_heavenly_stems` (`KNO-000100–000199`) | P0 | Planned (link) |
| FND-INV-021 | Jia | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-022 | Yi | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-023 | Bing | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-024 | Ding | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-025 | Wu | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-026 | Ji | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-027 | Geng | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-028 | Xin | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-029 | Ren | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |
| FND-INV-030 | Gui | Fundamental Classification | `canon_link` | Canon stem records | P1 | Planned (link) |

---

## 4.4 Earthly Branches

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-040 | Earthly Branches | Fundamental Concept | `canon_link` | Canon `03_earthly_branches` (`KNO-000200–000299`) | P0 | Planned (link) |
| FND-INV-041 | Zi | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-042 | Chou | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-043 | Yin | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-044 | Mao | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-045 | Chen | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-046 | Si | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-047 | Wu (Branch) | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-048 | Wei | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-049 | Shen | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-050 | You | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-051 | Xu | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |
| FND-INV-052 | Hai | Fundamental Classification | `canon_link` | Canon branch records | P1 | Planned (link) |

---

## 4.5 Hidden Stems

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-060 | Hidden Stems | Fundamental Concept | `canon_link` | Canon `04_hidden_stems` (`KNO-000300–000399`) | P0 | Planned (link) |
| FND-INV-061 | Hidden Stem Mapping Principle | Fundamental Relationship | `todo_architecture` | Link Canon vs module-owned mapping record | P1 | Planned |

---

## 4.6 BaZi structural foundations (module-owned candidates)

These are BaZi chart-structure concepts. Exact academic field designs belong to Phase 2.

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-070 | Four Pillars | Fundamental Concept | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-071 | Year Pillar | Fundamental Classification | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-072 | Month Pillar | Fundamental Classification | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-073 | Day Pillar | Fundamental Classification | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-074 | Hour Pillar | Fundamental Classification | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-075 | Day Master | Fundamental Concept | `module_owned` | `TODO_ALLOCATE` | P0 | Planned |
| FND-INV-076 | Stem–Branch Pair | Fundamental Concept | `module_owned` | `TODO_ALLOCATE` | P1 | Planned |
| FND-INV-077 | Sexagenary Cycle | Fundamental Concept | `module_owned` | `TODO_ALLOCATE` | P1 | Planned |

---

## 4.7 Seasonal Qi and growth phases

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-080 | Seasonal Qi | Fundamental Concept | `canon_link` | Canon `15_seasonal_qi` (`KNO-001400–001499`) | P1 | Planned (link) |
| FND-INV-081 | Twelve Growth Phases | Fundamental Concept | `todo_architecture` | `TODO_ALLOCATE` or new Canon domain | P1 | Planned |
| FND-INV-082 | Month Command | Fundamental Concept | `module_owned` | `TODO_ALLOCATE` | P1 | Planned |

---

## 4.8 Terminology and classical principles (placeholders)

| Inv ID | Canonical Name | Category | Ownership | Proposed / Linked KNO | Phase 2 Priority | Record Status |
|--------|----------------|----------|-----------|------------------------|------------------|---------------|
| FND-INV-090 | BaZi Fundamental Terminology Set | Terminology | `todo_architecture` | Prefer Foundation `TERM-*`; record only if needed | P2 | Planned |
| FND-INV-091 | Classical Theoretical Principle (placeholder slot) | Classical Principle | `todo_architecture` | Split into named principles in Phase 2 | P2 | Placeholder |

---

# 5. Counts

| Class | Count |
|-------|-------|
| Inventory rows | 44 |
| `canon_link` (primary) | majority of element/stem/branch/hidden/seasonal rows |
| `module_owned` candidates | 9 |
| `todo_architecture` | several — must resolve before Official JSON |
| Populated `knowledge_records/*.json` | **0** |

---

# 6. Explicit exclusions (do not inventory here)

Per module scope, do **not** add inventory rows for:

- Strength evaluation
- Temperature analysis
- Patterns
- Useful God
- Ten Gods interpretation
- Combinations / clashes / punishments / harms (as analytical modules)
- ShenSha interpretation
- Luck interpretation
- Marriage / career / wealth / health / children analysis
- Scoring / engines / prompts

---

# 7. Phase 2 entry criteria

Architecture / Academic owners MUST confirm before Phase 2 designs:

1. BaZi Knowledge ID allocation range (`TODO_ALLOCATE` resolution)
2. Ownership decisions for every `todo_architecture` row
3. Whether generating/controlling cycles are Canon-only or allow BaZi wrappers
4. Whether Twelve Growth Phases belong in Canon or this module
5. Priority order for first design pack (recommended: FND-INV-070…075 first)

---

# 8. Related documents

- `README.md`
- `FUNDAMENTAL_SPEC.md`
- `FIELD_GUIDE.md`
- `validation.md`
- `MODULE_SPEC.md`
- `knowledge/knowledge_canon/*/INDEX.md` (Canon ID ranges)
- `knowledge/references/` (Foundation — frozen)
- `knowledge/terminology/` (Foundation — frozen)

---

# 9. Revision

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-07-31 | Phase 1 inventory created — planning only, no academic JSON |
