# Phase 2 Design Plan — Fundamental Knowledge

> **Document ID:** BAZI-FND-PHASE2-PLAN-001  
> **Path:** `knowledge/bazi/PHASE2_DESIGN_PLAN.md`  
> **Version:** V1.0.0  
> **Status:** Draft — Awaiting Architecture Approval  
> **Module:** `knowledge/bazi/01_fundamental_knowledge`  

---

## 1. Purpose

Organize the first design packs for Phase 2 (field-level Knowledge Record designs).

This plan does **not** author academic content and does **not** create JSON records.

---

## 2. Phase gate

| Gate | Requirement |
|------|-------------|
| Architecture Approval of ADRs | Required |
| Ownership Matrix acceptance | Required (TODO_REVIEW backlog may remain flagged) |
| Global ID Policy acceptance | Required |
| Academic start of Pack 01 designs | After Architecture Approval |

---

## 3. Pack strategy

| Pack | Focus | JSON under BaZi Fundamental? |
|------|-------|------------------------------|
| Pack 01 | Core cosmology + stems/branches dependencies + Stem–Branch Cycle | Only for `module_owned` rows after ID allocation; Canon rows are link-designs |
| Pack 02 (future) | Four Pillars / Day Master / Month Command | Yes (`module_owned`) |
| Pack 03 (future) | Remaining inventory after TODO_REVIEW cleared | Mixed |

Recommended first structural JSON pack after Pack 01 link designs: **Pack 02** (FND-INV-070…075, 082).

---

## 4. Pack 01 — Core foundations

Scope:

- Yin Yang  
- Wu Xing (Five Elements + five members)  
- Heavenly Stems (system + ten stems)  
- Earthly Branches (system + twelve branches)  
- Hidden Stems (system)  
- Stem–Branch Cycle (Sexagenary Cycle + Stem–Branch Pair)

### 4.1 Pack 01 design rows

| Planning ID | Concept | Expected Knowledge ID | Dependencies | Owner | Review Status | JSON Status |
|-------------|---------|----------------------|--------------|-------|---------------|-------------|
| FND-INV-001 | Yin and Yang | `PENDING_GLOBAL_ALLOCATOR` (Canon-owned when issued) | Foundation REF/TERM | `knowledge_canon/05_yin_yang` | Not started | N/A (Canon / link-only) |
| FND-INV-010 | Five Elements | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-001 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-011 | Wood | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-012 | Fire | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-013 | Earth | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-014 | Metal | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-015 | Water | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-016 | Generating Cycle | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010…015 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-017 | Controlling Cycle | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-010…015 | `knowledge_canon/01_five_elements` | Not started | N/A (link-only) |
| FND-INV-020 | Heavenly Stems | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-001, FND-INV-010 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-021 | Jia | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-022 | Yi | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-023 | Bing | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-024 | Ding | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-025 | Wu (Stem) | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-026 | Ji | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-027 | Geng | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-028 | Xin | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-029 | Ren | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-030 | Gui | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020 | `knowledge_canon/02_heavenly_stems` | Not started | N/A (link-only) |
| FND-INV-040 | Earthly Branches | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-001, FND-INV-010 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-041 | Zi | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-042 | Chou | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-043 | Yin | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-044 | Mao | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-045 | Chen | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-046 | Si | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-047 | Wu (Branch) | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-048 | Wei | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-049 | Shen | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-050 | You | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-051 | Xu | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-052 | Hai | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-040 | `knowledge_canon/03_earthly_branches` | Not started | N/A (link-only) |
| FND-INV-060 | Hidden Stems | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020, FND-INV-040 | `knowledge_canon/04_hidden_stems` | Not started | N/A (link-only) |
| FND-INV-061 | Hidden Stem Mapping Principle | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-060 | `knowledge_canon/04_hidden_stems` | Not started | N/A (link-only) |
| FND-INV-076 | Stem–Branch Pair | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-020, FND-INV-040 | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-077 | Sexagenary Cycle | `PENDING_GLOBAL_ALLOCATOR` | FND-INV-076 | `bazi/01_fundamental_knowledge` | Not started | Not created |

**Pack 01 row count:** 37  

**BaZi JSON-eligible in Pack 01:** FND-INV-076, FND-INV-077 only (after Academic design + global ID issue).

---

## 5. Pack 02 — Preview (not started)

| Planning ID | Concept | Expected Knowledge ID | Owner | Review Status | JSON Status |
|-------------|---------|----------------------|-------|---------------|-------------|
| FND-INV-070 | Four Pillars | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-071 | Year Pillar | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-072 | Month Pillar | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-073 | Day Pillar | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-074 | Hour Pillar | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-075 | Day Master | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |
| FND-INV-082 | Month Command | `PENDING_GLOBAL_ALLOCATOR` | `bazi/01_fundamental_knowledge` | Not started | Not created |

---

## 6. Excluded from Pack 01 until TODO_REVIEW cleared

- FND-INV-002 Qi  
- FND-INV-003 Cosmological Correspondence Principle  
- FND-INV-081 Twelve Growth Phases  
- FND-INV-091 Classical Theoretical Principle (placeholder)  
- FND-INV-090 Terminology set (Foundation-owned; no KNO design pack)

---

## 7. Phase 2 deliverables (when authorized)

For each Pack 01 row:

1. Design note / field map (no full academic essay required at kickoff)  
2. Dependency list confirmed against Ownership Matrix  
3. Review Status updated  
4. Still **no JSON** until Phase 4 authorization  

---

## 8. Related documents

- `knowledge/ARCHITECTURE_DECISIONS.md`  
- `knowledge/bazi/MODULE_OWNERSHIP_MATRIX.md`  
- `knowledge/bazi/GLOBAL_KNOWLEDGE_ID_POLICY.md`  
- `01_fundamental_knowledge/KNOWLEDGE_INVENTORY.md`  
