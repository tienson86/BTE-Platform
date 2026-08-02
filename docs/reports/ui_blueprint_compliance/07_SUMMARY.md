# UI Blueprint V1.1 — Compliance Audit Summary

**Status:** AUDIT PASS (documentation complete) — **no UI code changed**  
**Date:** 2026-08-02  
**Scope:** Result UI Tiers 1–6 vs Blueprint V1.1 Final Freeze  
**Runtime:** Out of scope (already PASS — not continued)

---

## Tier verdicts

| Tier | Name | Verdict | Highest-priority gaps |
|------|------|---------|------------------------|
| 1 | Executive Hero | PASS + WARN | FirstRec below fold; metrics 2×3 vs 1×6 |
| 2 | Four Pillars | PASS + WARN | Extra DayMasterRelation; cells ≠ `--` |
| 3 | Metrics | WARN / layout FAIL | Not 2×2 ChartBand; unbound SummaryMetricGrid; EN chrome |
| 4 | Analysis | WARN | Extra Thân; IA split; wrong default-expand; pattern-rules essay |
| 5 | Interpretation | WARN | Chapter set vs B.3; TOC always on; Exec duplicates Ch.1 |
| 6 | Knowledge | WARN | EN Insight/Expert; sources ≠ EvidenceRow; EN in `discussion.js` |

---

## What is đúng Blueprint

- Tier 1: QualityVerdict + FirstRecommendation present; no hero essay dump; soft grammar; VI identity
- Tier 2: Four-column pillar matrix; stem/branch/hidden/ten-god rows; soft table grammar
- Tier 3: Gauge / Elements / TenGods content modules exist; soft chart cards
- Tier 4: Explainable analysis card shell; soft accordion grammar
- Tier 5: TOC + chapters document shell; soft document typography
- Tier 6: Knowledge workspace path Insight → … → Related; soft workspace grammar

---

## What is khác / sai Blueprint (needs UI fix sprint)

### Critical
1. **T3-02** — Desktop ChartBand not 2×2  
2. **T3-03** — Unbound SummaryMetricGrid  
3. **T4-05** — Pattern-rules essay in Priority·Knowledge  
4. **T6-04** — Hard-coded EN in `discussion.js`

### Major
5. **T1-03** — FirstRecommendation below fold  
6. **T2-03** — Extra DayMasterRelation on Tier 2  
7. **T3-04** — EN “Score payload” chrome  
8. **T4-02** — Extra Thân block  
9. **T4-03** — Useful/Relations IA split  
10. **T4-04** — Wrong default-expand  
11. **T5-02** — Chapters ≠ B.3  
12. **T5-04** — Exec duplicates Chapter 1  
13. **T6-02** — Expert sources not EvidenceRow  
14. **T6-03** — EN Insight/Expert labels  

### Minor
15. **T1-04** — Metrics 2×3 vs glance row  
16. **T1-07** — Hero secondaries  
17. **T2-04** — Missing cells not `--`  
18. **T3-05** — Order interrupted by summary grid  
19. **T5-03** — TOC always visible  

---

## Master findings table

| ID | Blueprint Requirement | Current UI | Severity | Fix Recommendation |
|----|----------------------|------------|----------|-------------------|
| T1-01 | QualityVerdict primary ≤2 lines | Present, primary weight | — | Keep |
| T1-02 | FirstRecommendation ≤2 lines | Present | — | Keep |
| T1-03 | FirstRecommendation above the fold | Often below fold after metric grid | **Major** | Compact R3; place R4 under verdict / two-column hero |
| T1-04 | Metric glance as single strip | 2×3 tile wrap | **Minor** | Desktop single-row chips |
| T1-05 | No long essay in Hero | No essay dump | — | Keep |
| T1-06 | Identity Title·Gender·Date·Place | Present when payload allows | — | Keep |
| T1-07 | R3 only six primary glances | Optional secondaries add height | **Minor** | Move secondaries to Tier 3 |
| T2-01 | Four-column pillar workspace | Implemented | — | Keep |
| T2-02 | Stem/Branch/Hidden/TenGods rows | Present | — | Keep |
| T2-03 | Matrix-only Tier 2 (no relation essay) | Extra DayMasterRelation block | **Major** | Remove from Tier 2 |
| T2-04 | Missing cell → `--` | Unavailable / prose text | **Minor** | Render `--` only |
| T2-05 | No expert essay in matrix | Cells short-label | — | Keep |
| T3-01 | Gauge / Elements / TenGods | Modules exist | — | Keep |
| T3-02 | Desktop 2×2 ChartBand | Not 2×2 composition | **Critical** | CSS grid 2×2 ≥lg |
| T3-03 | No unbound summary clutter | Unbound SummaryMetricGrid | **Critical** | Remove or fully bind + demote |
| T3-04 | VI-only customer chrome | EN “Score payload” | **Major** | i18n keys; drop EN labels |
| T3-05 | Order Metrics→Gauge→Elements→TenGods | Interrupted by summary grid | **Minor** | Enforce after T3-03 |
| T4-01 | Explainable analysis blocks | Present | — | Keep |
| T4-02 | No extra Thân block in Tier 4 IA | Extra Thân card | **Major** | Remove/relocate |
| T4-03 | Useful grouped; Relations matrix | Split Dụng/Hỷ/Kỵ + Relations | **Major** | Regroup per wireframe |
| T4-04 | Default-expand primary four | Wrong expand set | **Major** | Expand only primary four |
| T4-05 | No pattern-rules essay in Priority | Essay injected | **Critical** | Short bullets only; long → T5/T6 |
| T5-01 | TOC + chapters document | Shell present | — | Keep |
| T5-02 | Chapters align B.3 | Titles/order diverge | **Major** | Remap to B.3 |
| T5-03 | TOC gated by availableCount | TOC always on | **Minor** | Gate visibility |
| T5-04 | No exec↔Ch.1 full duplicate | Duplicate narrative | **Major** | Teaser XOR Ch.1 body |
| T6-01 | Insight→Evidence→…→Related | Workspace present | — | Keep |
| T6-02 | Sources as EvidenceRow | Ad-hoc Expert list | **Major** | EvidenceRow components |
| T6-03 | VI pane chrome | EN Insight/Expert | **Major** | `report.knowledge.*` VI |
| T6-04 | No hard-coded EN in presenters | EN in `discussion.js` | **Critical** | i18n all strings |

---

## Recommended fix order (next sprint — do not implement now)

1. T4 default-expand primary four; L4 section IA (Relations matrix; Useful grouped)  
2. T4 stop pattern-rules essay in Priority·Knowledge  
3. T3 restore desktop 2×2 ChartBand; drop/limit SummaryMetricGrid  
4. T5 dedupe exec vs Ch.1; TOC on availableCount; align B.3 titles  
5. T6 i18n Expert + EvidenceRow in sources pane; fix `discussion.js` EN  
6. T2 remove DayMasterRelation; cell miss → `--`  
7. T1 FirstRec above fold / metric row layout  

---

## Evidence index (illustrations)

| Tier | Preview |
|------|---------|
| 1 | `docs/reports/ui_sprint01_executive_hero/preview/` |
| 2 | `docs/reports/ui_sprint02_four_pillars/preview/` |
| 3 | `docs/reports/ui_sprint03_metrics/preview/` |
| 4 | `docs/reports/ui_sprint04_analysis/preview/` |
| 5 | `docs/reports/ui_sprint05_interpretation/preview/` |
| 6 | `docs/reports/ui_sprint06_knowledge/preview/` |

Per-tier detail: `01_EXECUTIVE_HERO.md` … `06_KNOWLEDGE.md`

---

## Audit PASS criteria

| Criterion | Met? |
|-----------|------|
| UI khác Blueprint listed | Yes — Critical/Major/Minor table |
| UI đúng Blueprint listed | Yes — “What is đúng” + Keep rows |
| UI cần sửa listed | Yes — fix order + Fix Recommendation column |
| No code/CSS/layout changes in this sprint | Yes |

**Sprint result: AUDIT PASS** — ready for UI fix sprint (separate).
