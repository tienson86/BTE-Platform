# 03 — Rule Coverage Report

Version: 1.0  
Status: **AUDIT COMPLETE — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Depends on: `01_KNOWLEDGE_COVERAGE_AUDIT.md`  

---

## 1. Purpose

Audit every Rule Database package and classify:

| Status | Meaning |
|--------|---------|
| **Implemented** | Populated and consumed by production engines |
| **Partial** | Populated but thin, overlapping, or incompletely consumed |
| **Missing** | Domain expected; no usable rules |
| **Obsolete / orphan** | Content exists but not on the V1 commercial pipeline |

No rule content is modified in this epic.

---

## 2. Rule surfaces (three layers)

BTE currently has **three** rule-related surfaces. They must not be confused.

| Layer | Location | Role in V1 |
|-------|----------|------------|
| **A. Operational CSV** | `database/11–15_*`, `01_du_lieu_goc`, `02_quan_he`, `05_phan_tich` | **Primary runtime** for Score / supporting engines |
| **B. Interpretation CSV** | `database/interpretation_rules/` | Partial runtime (ten_gods, luck wired; others largely orphan) |
| **C. Knowledge Rule Database** | `knowledge/rule_database/` | JSON `*_rules` packs + empty framework domains |

---

## 3. Layer A — Operational CSV packages

Approximate row counts from inventory (2026-08-08):

| Package | Files | Rows (approx.) | Status | Notes |
|---------|------:|---------------:|--------|-------|
| `database/01_du_lieu_goc` | 20 | 602 | **Implemented** | Fundamentals (stems, branches, calendar, …) |
| `database/02_quan_he` | 20 | 338 | **Implemented** | Combinations, clashes, punishments, harms, ten gods relations |
| `database/09_hidden_stems` | 1 | 12 | **Partial** | Thin |
| `database/11_temperature` | 9 | 55 | **Implemented** | Season/temperature engines |
| `database/12_strength` | 10 | 54 | **Implemented** | Strength engine |
| `database/13_useful_god` | 8 | 41 | **Implemented** | Useful god engine |
| `database/14_pattern` | 7 | 70 | **Implemented** | Pattern engine |
| `database/15_score_engine` | 59 | 445 | **Implemented** | Weights + dimension scores |
| `database/05_phan_tich/01_nhat_chu` | 4 | 10 | **Partial** | Thin day-master analysis |
| `database/05_phan_tich/02_sinh_khac_can_chi` | 6 | 69 | **Implemented** | Generation/control |
| `database/05_phan_tich/03_than_vuong_than_nhuoc` | 20 | 502 | **Implemented** | Strength / ten-gods scoring support |
| `database/05_phan_tich/04_cach_cuc` | 11 | 226 | **Partial** | Overlaps `14_pattern`; verify SSOT |
| `database/05_phan_tich/05_dung_than` | 9 | 132 | **Partial** | Overlaps `13_useful_god` |
| `database/05_phan_tich/06_hy_than_ky_than` | 5 | 74 | **Partial** | Favorable/unfavorable gods |
| `database/05_phan_tich/07_than_sat` | 24 | 255 | **Implemented** | Shensha |
| `database/05_phan_tich/08_hon_nhan` | 8 | 107 | **Obsolete / orphan** | No engine consumer found |
| `database/05_phan_tich/09_tu_tuc` | 8 | 147 | **Obsolete / orphan** | Children rules unwired |
| `database/05_phan_tich/10_tai_van` | 14 | 984 | **Obsolete / orphan** | Career/wealth-style; unwired |
| `database/05_phan_tich/11_dai_van` | 9 | 80 | **Implemented** | Luck interpreter support |

**Layer A summary:** Structural calculation **Implemented**. Life-topic packs **Orphan** despite large row counts.

---

## 4. Layer B — Interpretation rules

| File | Rows | Status | Consumer |
|------|-----:|--------|----------|
| `ten_gods_rules.csv` | 13 | **Implemented** | Ten-gods interpreter |
| `luck_rules.csv` | 14 | **Implemented** | Luck interpreter |
| `useful_god_rules.csv` | 12 | **Partial / orphan*** | Not Pack 03 primary path (*separate local copies may exist elsewhere) |
| `five_elements_rules.csv` | 11 | **Obsolete / orphan** | Unwired to Pack 03 loaders |
| `day_master_rules.csv` | 10 | **Obsolete / orphan** | Unwired |
| `bazi_basic_rules.csv` | 14 | **Obsolete / orphan** | Unwired |
| `career_rules.csv` | 12 | **Obsolete / orphan** | Unwired |
| `wealth_rules.csv` | 12 | **Obsolete / orphan** | Unwired |
| `marriage_rules.csv` | 14 | **Obsolete / orphan** | Unwired |
| `health_rules.csv` | 13 | **Obsolete / orphan** | Unwired |
| `fengshui_rules.csv` | 14 | **Obsolete / orphan** | Unwired |
| `rule_category.csv` | 14 | Meta | Taxonomy support |
| `rule_schema.csv` | 1 | Meta | Schema |

\*Treat as **orphan for commercial Narrative path** until mapped and validated.

---

## 5. Layer C — Knowledge Rule Database

### 5.1 Operational JSON packs (`*_rules`)

| Package | Rules (STATS) | Status | Notes |
|---------|--------------:|--------|-------|
| `01_strength_rules` | ~45 | **Partial** | JSON present; runtime uses CSV primarily |
| `02_season_rules` | 46 | **Partial** | Documented 100% family coverage in STATS; not primary CSV path |
| `03_temperature_rules` | 56 | **Partial** | Same |
| `04_pattern_rules` | 68 | **Partial** | Same |
| `05_special_case_rules` | 66 | **Partial** | Same |
| `06_follow_pattern_rules` | 51 | **Partial** | Same |
| `07_combination_rules` | 61 | **Partial** | Same |
| `08_priority_rules` | 69 | **Partial** | Same |

These packs are **content-rich for knowledge/analysis design**, but V1 production engines load **`database/` CSVs**. Classification **Partial** = valuable, not obsolete, not the sole SSOT for runtime.

### 5.2 Framework domains (scaffolding)

| Domain | Content records | Status |
|--------|-----------------|--------|
| `01_strength` | 0 | **Missing** (scaffold) |
| `02_season` | 0 | **Missing** (scaffold) |
| `03_temperature` | 0 | **Missing** (scaffold) |
| `04_patterns` | 0 | **Missing** (scaffold) |
| `05_useful_gods` | 0 | **Missing** (scaffold) |
| `06_ten_gods` | 0 | **Missing** (scaffold) |
| `07_combinations` | 0 | **Missing** (scaffold) |
| `08_clashes` | 0 | **Missing** (scaffold) |
| `09_transformations` | 0 | **Missing** (scaffold) |
| `10_shensha` | 0 | **Missing** (scaffold) |
| `11_luck_cycles` | 0 | **Missing** (scaffold) |
| `12_special_cases` | 0 | **Missing** (scaffold) |
| `registry/` | Scaffold | **Partial** |

Per `EDGE_CASES.md`: framework domains are scaffolding; do not confuse with `*_rules/`.

---

## 6. Classical knowledge schema (not calculation rules)

| Package | Status |
|---------|--------|
| `database/20_knowledge/*.csv` (20 files) | **Missing content** (schema Implemented) |

Not a calculation rule DB — included because commercial consultation treats it as the explainable rule/knowledge corpus.

---

## 7. Coverage by BaZi consultation domain

| Domain | Best rule source | Coverage status |
|--------|------------------|-----------------|
| Five Elements | `01_du_lieu_goc` + score wuxing | Implemented |
| Ten Gods | score + interp + `03_than_vuong…` | Implemented |
| Strength | `12_strength` + score | Implemented |
| Season | temperature/season CSVs + JSON pack | Implemented / Partial |
| Temperature | `11_temperature` + JSON pack | Implemented |
| Useful God | `13_useful_god` + score | Implemented |
| Patterns / Special Structures | `14_pattern` + JSON packs | Implemented |
| Follow patterns | JSON `06_follow_pattern_rules` + pattern CSVs | Partial |
| Combinations | `02_quan_he` + JSON pack | Implemented |
| Clash / Punishment / Harm | `02_quan_he` | Implemented |
| Transformations | Framework empty; special cases partial | **Missing / Partial** |
| Shensha | `07_than_sat` + score | Implemented |
| Luck | `11_dai_van` + luck score + luck_rules | Implemented |
| Career | `10_tai_van` + career_rules | **Orphan** |
| Wealth | `10_tai_van` + wealth_rules | **Orphan** |
| Marriage | `08_hon_nhan` + marriage_rules | **Orphan** |
| Children | `09_tu_tuc` | **Orphan** |
| Health | health_rules + health star | **Orphan / Partial** |
| Parents | — | **Missing** |
| Education | — | **Missing** |
| Priority / conflict resolution | JSON `08_priority_rules` + score normalize | Partial |

---

## 8. Aggregate counts

| Classification | Packages / files (approx.) |
|----------------|----------------------------|
| Implemented (runtime) | ~15 structural packages |
| Partial | ~10 (overlaps, JSON packs, thin packs) |
| Missing | Parents, Education, Transformations (framework), framework domains |
| Obsolete / orphan | Life-domain `05_phan_tich` 08–10 + most `interpretation_rules` |

| Metric | Value |
|--------|------:|
| Operational CSV data rows (selected DBs) | ~4,200+ |
| Orphan life-domain rows (`08`+`09`+`10`) | ~1,238 |
| Interpretation rule rows | 154 |
| JSON `*_rules` total (STATS sum) | ~462 |
| `20_knowledge` content rows | **0** |

**Insight:** BTE is not short of calculation rules. BTE is short of **wired consultation rules** and **explainable knowledge**.

---

## 9. Recommendations (analysis only — no changes)

1. Treat **CSV under `database/11–15_*` + `02_quan_he`** as runtime SSOT for structural scoring.  
2. Inventory orphan packs for **wire / migrate / retire** decisions (future epic).  
3. Do not duplicate JSON pack content into CSV without mapping policy.  
4. Expand consultation quality via evidence/sentences + `20_knowledge`, not by inventing parallel score rules.  
5. Mark Parents / Education as greenfield knowledge + rule packages when prioritized.

---

## 10. Stop line

Rule coverage report complete. **No rule files modified.**

---

END
