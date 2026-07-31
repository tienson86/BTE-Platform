# Design Order — Fundamental Knowledge

**Module:** `knowledge/bazi/01_fundamental_knowledge`  
**Path:** `design/DESIGN_ORDER.md`  
**Version:** V1.0.0  
**Status:** Framework Ready — Await Academic Design  

---

## Purpose

Track the official design sequence of every Knowledge Record (planning level).

Populated from Inventory + Ownership Matrix + Pack definitions only.

No academic content.

---

## Status legend

| Column | Values |
|--------|--------|
| Academic Status | Not Started / In Design / Complete / Blocked / N/A |
| Review Status | Pending / In Review / Approved / Rejected |
| JSON Status | None / Draft / Validated / N/A (link-only) / Blocked |
| Freeze Status | No / Candidate / Frozen |

---

## Design sequence

| Design Order | Planning ID | Record Name | Owner | Dependencies | Academic Status | Review Status | JSON Status | Freeze Status | Notes |
|--------------|-------------|-------------|-------|--------------|-----------------|---------------|-------------|---------------|-------|
| 01 | `FND-INV-001` | Yin and Yang | `knowledge_canon/05_yin_yang` | — | Not Started | Pending | N/A (link-only) | No | PACK_01 |
| 02 | `FND-INV-010` | Wu Xing / Five Elements (system) | `knowledge_canon/01_five_elements` | FND-INV-001 | Not Started | Pending | N/A (link-only) | No | PACK_01 + PACK_02 |
| 03 | `FND-INV-011` | Wood | `knowledge_canon/01_five_elements` | FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 04 | `FND-INV-012` | Fire | `knowledge_canon/01_five_elements` | FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 05 | `FND-INV-013` | Earth | `knowledge_canon/01_five_elements` | FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 06 | `FND-INV-014` | Metal | `knowledge_canon/01_five_elements` | FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 07 | `FND-INV-015` | Water | `knowledge_canon/01_five_elements` | FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 08 | `FND-INV-016` | Generating Cycle | `knowledge_canon/01_five_elements` | FND-INV-011…015 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 09 | `FND-INV-017` | Controlling Cycle | `knowledge_canon/01_five_elements` | FND-INV-011…015 | Not Started | Pending | N/A (link-only) | No | PACK_02 |
| 10 | `FND-INV-020` | Heavenly Stems | `knowledge_canon/02_heavenly_stems` | FND-INV-001; FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 11 | `FND-INV-021` | Jia | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 12 | `FND-INV-022` | Yi | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 13 | `FND-INV-023` | Bing | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 14 | `FND-INV-024` | Ding | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 15 | `FND-INV-025` | Wu (Stem) | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 16 | `FND-INV-026` | Ji | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 17 | `FND-INV-027` | Geng | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 18 | `FND-INV-028` | Xin | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 19 | `FND-INV-029` | Ren | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 20 | `FND-INV-030` | Gui | `knowledge_canon/02_heavenly_stems` | FND-INV-020 | Not Started | Pending | N/A (link-only) | No | PACK_03 |
| 21 | `FND-INV-040` | Earthly Branches | `knowledge_canon/03_earthly_branches` | FND-INV-001; FND-INV-010 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 22 | `FND-INV-041` | Zi | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 23 | `FND-INV-042` | Chou | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 24 | `FND-INV-043` | Yin | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 25 | `FND-INV-044` | Mao | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 26 | `FND-INV-045` | Chen | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 27 | `FND-INV-046` | Si | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 28 | `FND-INV-047` | Wu (Branch) | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 29 | `FND-INV-048` | Wei | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 30 | `FND-INV-049` | Shen | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 31 | `FND-INV-050` | You | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 32 | `FND-INV-051` | Xu | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 33 | `FND-INV-052` | Hai | `knowledge_canon/03_earthly_branches` | FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_04 |
| 34 | `FND-INV-060` | Hidden Stems | `knowledge_canon/04_hidden_stems` | FND-INV-020; FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_05 |
| 35 | `FND-INV-061` | Hidden Stem Mapping Principle | `knowledge_canon/04_hidden_stems` | FND-INV-060 | Not Started | Pending | N/A (link-only) | No | PACK_05 |
| 36 | `FND-INV-080` | Seasonal Qi | `knowledge_canon/15_seasonal_qi` | FND-INV-010; FND-INV-040 | Not Started | Pending | N/A (link-only) | No | PACK_06 |
| 37 | `FND-INV-081` | Twelve Growth Phases | `TODO_REVIEW` | TODO_REVIEW | Blocked | Pending | Blocked | No | PACK_07 — ownership TODO_REVIEW |
| 38 | `FND-INV-070` | Four Pillars | `bazi/01_fundamental_knowledge` | FND-INV-020; FND-INV-040 | Not Started | Pending | None | No | No design pack yet |
| 39 | `FND-INV-071` | Year Pillar | `bazi/01_fundamental_knowledge` | FND-INV-070 | Not Started | Pending | None | No | No design pack yet |
| 40 | `FND-INV-072` | Month Pillar | `bazi/01_fundamental_knowledge` | FND-INV-070 | Not Started | Pending | None | No | No design pack yet |
| 41 | `FND-INV-073` | Day Pillar | `bazi/01_fundamental_knowledge` | FND-INV-070 | Not Started | Pending | None | No | No design pack yet |
| 42 | `FND-INV-074` | Hour Pillar | `bazi/01_fundamental_knowledge` | FND-INV-070 | Not Started | Pending | None | No | No design pack yet |
| 43 | `FND-INV-075` | Day Master | `bazi/01_fundamental_knowledge` | FND-INV-073 | Not Started | Pending | None | No | No design pack yet |
| 44 | `FND-INV-076` | Stem–Branch Pair | `bazi/01_fundamental_knowledge` | FND-INV-020; FND-INV-040 | Not Started | Pending | None | No | No design pack yet |
| 45 | `FND-INV-077` | Sexagenary Cycle | `bazi/01_fundamental_knowledge` | FND-INV-076 | Not Started | Pending | None | No | No design pack yet |
| 46 | `FND-INV-082` | Month Command | `bazi/01_fundamental_knowledge` | FND-INV-072; FND-INV-080 | Not Started | Pending | None | No | No design pack yet |
| 47 | `FND-INV-002` | Qi | `TODO_REVIEW` | TODO_REVIEW | Blocked | Pending | Blocked | No | Ownership TODO_REVIEW |
| 48 | `FND-INV-003` | Cosmological Correspondence Principle | `TODO_REVIEW` | TODO_REVIEW | Blocked | Pending | Blocked | No | Ownership TODO_REVIEW |
| 49 | `FND-INV-090` | BaZi Fundamental Terminology Set | `knowledge/terminology` | Foundation TERM-* | N/A | Pending | N/A (TERM not KNO) | No | Foundation link-only |
| 50 | `FND-INV-091` | Classical Theoretical Principle (placeholder) | `TODO_REVIEW` | TODO_REVIEW | Blocked | Pending | Blocked | No | Placeholder / TODO_REVIEW |

---

## Counts

| Metric | Value |
|--------|-------|
| Total sequenced rows | 50 |
| In PACK_01–07 | 37 |
| Unpacked / later packs | 13 |
| Blocked (TODO_REVIEW) | 4 (+ PACK_07 ownership) |

---

## Related

- `KNOWLEDGE_INVENTORY.md`
- `../../MODULE_OWNERSHIP_MATRIX.md`
- `DESIGN_PROGRESS.md`
- `PACK_READINESS_REPORT.md`
