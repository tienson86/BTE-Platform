# 01 — Pipeline Audit Report

**Epic:** BTE Stabilization V1  
**Date:** 2026-08-08  
**Scope:** Knowledge → Rule → Score → AnalysisResult → Interpretation → PACK_05 (Report) → Portal Adapter → ViewModel → Result Page  
**Method:** Live `OrchestratorService.analyze(1987-01-21 04:30 male)` + static adapter/UI inspection

---

## Pipeline diagram (as implemented)

```
knowledge/ + database/ (CSV rules)
        ↓
Calendar / Bazi / Pattern / Strength / UsefulGod / Score
        ↓
API AnalysisResult bag (dict views)
        ↓
InterpretationEngine (legacy build_from_resolved)
        ↓
PACK_05 ReportEngine.render_from_analysis → portal markdown/html
        ↓
adaptAnalysisToCanonicalDesktop → CanonicalDesktopViewModel
        ↓
adaptResultPageViewModel → ResultPageViewModel
        ↓
Result Page (Zones → Rows → Grid → Cards)
```

**Note:** Design System PACK_05 = Accessibility. Architecture PACK_05 = Report Engine. This audit uses Architecture PACK_05.

---

## Stage status

| Stage | Status | Notes |
|-------|--------|-------|
| Knowledge / Rule Database | **PASS** | Rules load; interpretation `rule_count` path active |
| Calendar | **PASS** | Solar/lunar/term/feng fields present on live run |
| Bazi chart | **PASS** | Pillars, day master, ten_gods list, shensha (8) present |
| Pattern | **PASS** | Live returns `cach_cuc`, `dung_than`, `hy_than`, `ky_than`, `than_vuong_nhuoc` |
| Strength / Useful God | **PASS** | Present; score scale 0–1 vs 0–100 requires portal normalize |
| Score Engine | **PASS** | Live `total_score=51.25`, `grade=D+`, series present (July zero-score issue resolved) |
| AnalysisResult (API bag) | **PARTIAL** | Typed views exist but orchestrator still ships JSON bag + source fingerprints |
| Interpretation Engine | **PARTIAL** | 10 sections produced; many bodies are **rule descriptions**, not commercial narrative |
| PACK_05 Report Engine | **PARTIAL** | Wired; portal report rebuilt from interpretation sections (markdown/html) |
| Portal Adapter (Canonical) | **PASS*** | *Stabilized this epic: no fixture leakage on API path for S08/S10/S07 empty |
| Portal Adapter (BaZi parallel) | **PASS*** | *Stabilized: interpretation / shensha / spirit gods / executive now API-mapped |
| Result Page ViewModel | **PASS*** | *Stabilized: consumes Canonical VM; technical copy gated |
| Result Page UI | **PASS** | Zone architecture frozen; preview/expand present |

\* After stabilization fixes in this epic.

---

## Missing fields

| Field / capability | Where expected | Status |
|--------------------|----------------|--------|
| Bone-weight (Cân Xương) engine | S10 / timeline early luck | **Missing** — shows unavailable copy |
| Commercial narrative sentences | Interpretation sections | **Missing quality** — rule prose often returned |
| Knowledge CMS retrieval | Knowledge zone | **Missing** — uses chart facts only |
| Parallel typed AnalysisResult end-to-end | Engines ↔ API ↔ Portal | **PARTIAL** — multiple AnalysisResult types coexist |

---

## Broken mapping (before → after this epic)

| Issue | Before | After |
|-------|--------|-------|
| S08 strengths/warnings/actions | Fell back to **mock fixture** when title heuristics failed | Uses interpretation sections / unavailable message — **no fixture** |
| S10 bone weight | Always showed **fixture** mệnh tốt content | Unavailable conclusion copy |
| S05 percent | `strength_score` 0.87 → rounded to **1** | Prefer `score.strength_score`; normalize 0–1 → 0–100 |
| BaZi interpretation | Always `BAZI_MOCK_INTERPRETATION` | Mapped from `interpretation.sections` |
| BaZi Dụng/Hỷ/Kỵ/grade | Hardcoded `"—"` / “chờ Interpretation” | Mapped from pattern / useful_god / score |
| Knowledge zone copy | Developer / PACK_06 strings | Chart-derived + unavailable gate |
| Interpretation step labels | English Observation/Explanation… | Vietnamese Quan sát / Giải thích / … |

---

## Placeholder outputs (remaining)

| Location | Kind | Treatment |
|----------|------|-----------|
| Dashboard CMS announcement | Product placeholder | Out of Result pipeline — deferred |
| Footer support | Product placeholder | Deferred |
| Mock data fixtures | Test/demo only | Allowed when `source=mock` |
| S10 / early luck timeline | Engine gap | Shows `Chưa đủ dữ liệu để đưa ra kết luận.` |

---

## Unused outputs

| Output | Status |
|--------|--------|
| Pack 04 `NarrativeInterpretationResult` | Exists but orchestrator uses **legacy** interpretation path |
| Rich ReportEngine internal layout/theme | Portal consumes thin markdown/html from sections |
| Analysis Engine `AnalysisResult` (separate package) | Not the HTTP production bag |

---

## Dead / parallel adapters

| Adapter / UI | Role | Risk |
|--------------|------|------|
| `adaptAnalysisToCanonicalDesktop` | **Production Result path** | Primary |
| `adaptResultPageViewModel` | Result Page presentation | Primary |
| `adaptAnalysisToBaZiResult` | Parallel BaZi Result screen | Still live via `analyzeService` |
| WP-0004 ExecutiveSummaryScreen VM | Alternate executive screen | Parallel; not Result Page |
| Dashboard adapter CMS stubs | Dashboard only | Not Result |

---

## Verdict

| Criterion | Result |
|-----------|--------|
| Pipeline connected end-to-end | **PASS** |
| Score non-zero on live case | **PASS** |
| Interpretation sections present | **PASS** |
| Narrative quality commercial-ready | **FAIL / BLOCKER** |
| Portal mock leakage on API Result path | **PASS** (fixed) |
| Overall stage health | **PARTIAL** — ready for narrative quality epic, not feature expansion |

---

END
