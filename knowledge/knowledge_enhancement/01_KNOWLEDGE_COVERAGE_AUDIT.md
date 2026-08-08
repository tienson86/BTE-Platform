# 01 — Knowledge Coverage Audit

Version: 1.0  
Status: **AUDIT COMPLETE — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Scope: Documentation only — no runtime, engine, Foundation, Design System, or UI changes  

---

## 1. Purpose

Determine whether the current BTE Knowledge Base supports **commercial-grade BaZi consultation**.

This audit inventories every knowledge domain and rates:

| Dimension | Meaning |
|-----------|---------|
| Schema / structure | Folders, specs, templates exist |
| Operational rules | Engine-loadable CSV/JSON used for calculation |
| Explainable knowledge | Consultant-facing classical/modern explanations |
| Narrative evidence | Content sufficient to fill Pack 05 sections |
| Production readiness | Safe for commercial consultation copy |

**Architecture is frozen.** This epic does not propose architecture changes.

---

## 2. Executive verdict

| Layer | Verdict |
|-------|---------|
| Calculation / analysis rule data | **Strong** — structural domains are production-usable |
| Knowledge infrastructure (governance, references, schemas) | **Ready** — Foundation freeze stands |
| Explainable knowledge corpus (`database/20_knowledge`, BaZi academic records) | **Empty / blueprint** — 0% content rows |
| Commercial Interpretation evidence | **Thin** — Pack 04 library ≈ 11 sentences |
| Pack 05 Narrative structure | **Production-ready** |
| Pack 05 live consultation richness | **Not commercial-grade** (G6 / CQ-1) |

**Overall commercial knowledge readiness: ~35%**

BTE can score and structure a chart. BTE cannot yet reliably explain, advise, and warn at consultant depth on every run.

---

## 3. Inventory scope

### 3.1 Knowledge surfaces audited

| Surface | Path | Role |
|---------|------|------|
| Classical Knowledge Base | `database/20_knowledge/` | Explainable corpus (future Knowledge Expert) |
| Operational analysis DB | `database/11–15_*`, `01_du_lieu_goc`, `02_quan_he`, `05_phan_tich` | Score / Pattern / Strength / … |
| Interpretation rules | `database/interpretation_rules/` | Prose / matching rules |
| Knowledge Rule Database | `knowledge/rule_database/` | Framework + JSON operational packs |
| BaZi Knowledge Blueprint | `knowledge/bazi/` | Module scaffolds + fundamental KR markdown |
| Numbered knowledge packs | `knowledge/01–09_*_knowledge/` | Spec / architecture docs |
| Pack 02 analytical knowledge | `knowledge/pack_02_analytical_knowledge/` | Analysis design specs |
| Knowledge Canon | `knowledge/knowledge_canon/` | Canonical concept records |
| Sentence Library | `knowledge/sentence_library/` | Framework only |
| References / Terminology | `knowledge/references/`, `knowledge/terminology/` | Citation SSOT |
| Narrative / Content Quality docs | `knowledge/architecture/pack_05_*`, `knowledge/releases/v1/content_quality/` | Narrative quality bar |

### 3.2 Domains inventoried

Structural, relational, life-topic, and specialty domains listed in §4.

---

## 4. Domain coverage matrix

### Scoring legend

| Score | Label | Definition |
|------:|-------|------------|
| 0–19% | Missing | No usable content for commercial consultation |
| 20–39% | Scaffold | Specs / empty schemas / blueprints only |
| 40–59% | Partial | Rules or docs exist; explanations/evidence thin or unwired |
| 60–79% | Implemented | Rules wired; explainable knowledge incomplete |
| 80–100% | Production | Rules + explanations + narrative evidence commercially usable |

**Coverage %** below is a composite of: structure (15%) + operational rules (35%) + explainable knowledge (25%) + narrative evidence (25%).

### 4.1 Structural / analytical domains

| Domain | Structure | Ops rules | Explainable KB | Narrative evidence | Coverage % | Production readiness | Missing knowledge |
|--------|-----------|-----------|----------------|--------------------|-----------:|----------------------|-------------------|
| Five Elements | Yes | Strong (`01_du_lieu_goc`, score wuxing) | Schema empty; Canon Wood only | Thin | **55%** | Calculation ready; explanation partial | Classical texts, modern interpretations, edge cases |
| Yin / Yang | Yes | Base data present | Schema empty | Thin | **45%** | Partial | Dedicated explainable corpus |
| Ten Gods | Yes | Strong + interpreter wired | Schema empty; blueprint | Thin (13 interp rules) | **62%** | Analysis ready; consultation partial | Full god meanings, relationships, examples |
| Hidden Stems | Yes | Present (`09_hidden_stems`, tang can) | Schema empty | Thin | **50%** | Analysis partial | Activation explanations |
| Growth Stage (Trường sinh) | Yes | Base tables | Schema empty | Thin | **48%** | Analysis partial | Stage narratives |
| Na Yin | Yes | Base data | Schema empty | Minimal | **40%** | Low commercial use | Modern interpretation |
| Strength | Yes | Strong (`12_strength`, score) | Blueprint only | Partial via AnalysisResult | **68%** | Analysis production | Consultant wording, edge cases |
| Season | Yes | Present (via temperature/season) | Blueprint / KR notes | Partial | **58%** | Analysis ready | Season–useful-god narrative bridges |
| Temperature | Yes | Present (`11_temperature`) | Blueprint | Partial | **58%** | Analysis ready | Balance guidance prose |
| Useful God | Yes | Strong (`13_useful_god`) | Blueprint | Partial (action evidence) | **65%** | Analysis production | Priority explanations, practical advice |
| Patterns / Special Structures | Yes | Strong (`14_pattern`, pattern JSON packs) | Blueprint | Partial | **65%** | Analysis production | Pattern story templates, broken/follow narratives |
| Shensha | Yes | Strong (`05_phan_tich/07_than_sat`) | Blueprint | Partial | **60%** | Analysis ready | Star meanings, caution language |
| Luck (Đại vận / lưu niên) | Yes | Strong (`11_dai_van`, luck score) | Blueprint | Partial | **60%** | Analysis ready | Period guidance, timing language |
| Combinations | Yes | Strong (`02_quan_he` hop) | Blueprint | Partial | **58%** | Analysis ready | Combination outcomes in prose |
| Clash / Punishment / Harm | Yes | Strong (xung/hình/hại/phá) | Blueprint / Canon empty | Partial | **55%** | Analysis ready | Risk narratives, mitigation |
| Harmony (hợp / hội) | Yes | Covered under combinations | Blueprint | Partial | **55%** | Analysis ready | Positive-outcome language |
| Transformations | Scaffold | Limited / framework domain empty | Missing | Missing | **22%** | Not ready | Full transform doctrine + rules alignment |
| Personality | Stub | Indirect via day master / ten gods | Missing module | Stub interpreters | **25%** | Not ready | Personality knowledge pack |

### 4.2 Life-topic domains

| Domain | Structure | Ops rules | Explainable KB | Narrative evidence | Coverage % | Production readiness | Missing knowledge |
|--------|-----------|-----------|----------------|--------------------|-----------:|----------------------|-------------------|
| Career | BaZi blueprint | Orphan-rich (`10_tai_van`, career_rules) | 0 rows | Not in Pack 05 path | **35%** | Rules exist, unwired | Wiring + commercial sentences |
| Wealth | BaZi blueprint | Orphan-rich (`10_tai_van` ~984 rows) | 0 rows | Not in Pack 05 path | **38%** | Rules exist, unwired | Wiring + explanations |
| Marriage | BaZi blueprint | Orphan (`08_hon_nhan` ~107) | 0 rows | Not in Pack 05 path | **32%** | Rules exist, unwired | Wiring + ethical guidance |
| Children | BaZi blueprint | Orphan (`09_tu_tuc` ~147) | 0 rows | Not in Pack 05 path | **30%** | Rules exist, unwired | Wiring + careful language |
| Health | BaZi blueprint | Thin (health_rules, health star) | 0 rows | Not in Pack 05 path | **28%** | Not commercial | Medical-safe explanations |
| Parents | Schema only (`17_parents`) | Missing dedicated ops pack | 0 rows | Missing | **12%** | Missing | Module + rules + prose |
| Education | Missing | Missing | Missing | Missing | **5%** | Missing | Entire domain |
| Feng Shui (hint) | Schema + interp rules | Unwired | 0 rows | Missing | **25%** | Out of core V1 narrative | Scope decision |

### 4.3 Cross-cutting knowledge assets

| Asset | Present | Content status | Notes |
|-------|---------|----------------|-------|
| `database/20_knowledge` (20 topic CSVs) | Yes | **0 data rows** | Schema 100%, content 0% |
| `knowledge/bazi` academic JSON | Structure yes | **0** in `knowledge_records/` | Fundamental KR markdown only (~15) |
| Knowledge Canon domains | 19 domains | **Wood only** populated | Citation ID remapping debt |
| Sentence Library | Framework | Empty of real sentences | Explicit non-goal of framework release |
| Pack 04 sentence library | Wired | **~11 sentences / ~12 rules** | Primary bottleneck for Narrative |
| References (classics) | 7/7 seed | Draft status | Chapter support empty |
| Terminology | Seed present | Small seed | Expansion needed for life topics |

---

## 5. Aggregated coverage

| Domain group | Domains | Avg coverage | Readiness |
|--------------|--------:|-------------:|-----------|
| Structural / analytical | 18 | **54%** | Calculation strong; explanation partial |
| Life topics | 8 | **26%** | Mostly orphan rules or missing |
| Explainable classical corpus | 20 files | **0% content** | Schema-only |
| Narrative commercial path | 7 sections | Structure **~90%** / depth **~40%** | G6 blocked |

**Weighted commercial readiness (consultation product):**

| Weight | Component | Score |
|-------:|-----------|------:|
| 25% | Structural analysis knowledge usable in product | 70 |
| 20% | Life-domain consultation knowledge | 26 |
| 25% | Explainable classical corpus | 5 |
| 30% | Narrative evidence sufficiency | 40 |
| | **Composite** | **≈ 35%** |

---

## 6. Production readiness summary

| Capability | Ready? | Evidence |
|------------|--------|----------|
| Build Four Pillars chart | Yes | Calendar + BaZi engines |
| Score strength / pattern / useful god / … | Yes | Score Engine + operational CSVs |
| Emit InterpretationResult sections | Yes | Pack 04 pipeline |
| Compose NarrativeResult (7 sections) | Yes | Pack 05 D1/D2 |
| Produce consultant-grade Executive Summary every run | **No** | CQ-3 / G6 |
| Produce specific Recommendations | **No** | CQ-4 |
| Produce Warnings with mitigation | **Partial** | CQ-5 |
| Cite classical knowledge with modern interpretation | **No** | `20_knowledge` empty |
| Deliver marriage / career / wealth consultation modules | **No** | Unwired / empty explainable KB |
| Claim commercial-grade BaZi consultation | **Not yet** | Composite ~35% |

---

## 7. What is already strong (do not rebuild)

1. **Operational structural rule CSVs** under `database/11–15_*`, `02_quan_he`, parts of `05_phan_tich`.
2. **Knowledge governance / references / terminology infrastructure** (Foundation freeze).
3. **BaZi module blueprint structure** (14 modules) — ready for content population.
4. **Pack 05 Narrative grammar** and Content Quality standards (Release B).
5. **JSON rule packs** in `knowledge/rule_database/*_rules/` for season/temperature/pattern/… (documentary + analysis-engine layer; not primary runtime CSV path).

---

## 8. Critical missing knowledge (top)

1. Populated `database/20_knowledge` rows for high-frequency consultation topics.
2. Commercial sentence / evidence units for Pack 04 → Pack 05 (identity, strength, weakness, action, risk, implication).
3. Wiring or deliberate retirement of orphan life-domain rules (`08_hon_nhan`, `09_tu_tuc`, `10_tai_van`, most `interpretation_rules`).
4. Knowledge Canon population beyond Wood + citation remapping.
5. Parents / Education domains (absent).
6. Transformation doctrine as first-class explainable + rule-aligned knowledge.
7. Practical guidance examples and edge-case narratives for Useful God / Pattern / Luck.

---

## 9. Related documents in this epic

| File | Focus |
|------|-------|
| `02_KNOWLEDGE_GAP_ANALYSIS.md` | Gap taxonomy |
| `03_RULE_COVERAGE_REPORT.md` | Rule package audit |
| `04_EVIDENCE_COVERAGE_REPORT.md` | Evidence vs Narrative needs |
| `05_NARRATIVE_SUPPORT_REPORT.md` | Pack 05 support map |
| `06_PRIORITY_EXPANSION_PLAN.md` | P0 / P1 / P2 |
| `07_KNOWLEDGE_ENHANCEMENT_ROADMAP.md` | Official roadmap |

---

## 10. Stop line

Audit complete. **Do not expand knowledge content until this package is reviewed.**

---

END
