# ANALYSIS_UNIFICATION_REPORT.md

Version: 1.0  
Date: 2026-08-07  
Epic: Analysis Experience Unification  
Status: **DOCUMENTATION COMPLETE** (no code migration)  
Constraint: Inventory and recommend only — do not migrate, delete, or refactor code in this epic

---

## 1. Objective

Make the **Result Page** (`PortalPage` → `ResultPageBody`) the **single official Analysis Experience** for BTE Customer Portal.

Foundation V1.0 is frozen. Result Page UI V1.0 + Visual Language V2 remain the structural and visual SSOT.

---

## 2. Official Analysis Flow (Recommended)

```
Dashboard (/dashboard)
        ↓
Birth Input (/analyze)
        ↓
ResultStore (session / local)
        ↓
GET /result
        ↓
result_desktop.html → static/dist/result.js
        ↓
PortalPage (shell)
        ↓
ResultPageBody (Zones → Rows → Grid → Cards)
        ↓
adaptResultPageViewModel(CanonicalDesktopViewModel)
        ↓
AnalyzeService → POST /analyze → adaptAnalysisToCanonicalDesktop
```

**Official entry points**

| Step | Route / Module | Status |
|------|----------------|--------|
| Start | `/analyze` | Keep (input, not analysis render) |
| View | `/result` | **Official Analysis Experience** |
| Host | `PortalPage` / `ResultPage` | Official |
| Body | `screens/result/**` | Official (frozen architecture) |
| Data | `CanonicalDesktopViewModel` → `ResultPageViewModel` | Official |

**Not official for end users**

- `/result?legacy=1`
- `BaZiResultScreen`
- WP-0004+ standalone screens / ConsultationReport composition
- `canonical_desktop/sections` + `rows` (superseded by Result zones)
- `screens/s00` experiments

---

## 3. Inventory — Every Analysis UI

### 3.1 Production-mounted Analysis UIs

| ID | Surface | Mount | Role |
|----|---------|-------|------|
| A1 | Result Page V1 + Visual V2 | `/result` → `resultApp.tsx` → `PortalPage` | **Official** |
| A2 | Legacy HTML report | `/result?legacy=1` → `result_legacy.html` + `/static/js/result.js` | Deprecated escape hatch |
| A3 | Legacy template stub | `templates/result.html` | Reference only (commented) |

### 3.2 React Analysis Screens (library / tests — not primary `/result` mount)

| ID | Screen | Path | Notes |
|----|--------|------|-------|
| B1 | `BaZiResultScreen` | `screens/bazi/` | Full alternate analysis layout |
| B2 | `ExecutiveSummaryScreen` | `screens/` | WP-0004 slice |
| B3 | `FourPillarsScreen` | `screens/` | WP-0005 slice |
| B4 | `ExecutiveInsightScreen` | `screens/` | WP-0006 slice |
| B5 | `MetricsScreen` | `screens/` | WP-0007 slice |
| B6 | `ExplainableAnalysisScreen` | `screens/` | WP-0008 slice |
| B7 | `ConsultationReportScreen` | `screens/` | Composes B2–B6 |
| B8 | `AppendixScreen` | `screens/` | WP-0010 slice |
| B9 | `S00DesktopScreen` | `screens/s00/` | Isolated experiment |

### 3.3 Superseded Canonical Desktop section UI

Still in tree; **not** rendered by current `PortalPage` (which uses `ResultPageBody` only):

| ID | Module | Maps to Result concept |
|----|--------|------------------------|
| C1 | `sections/S00`–`S11` | Context / Summary / Analysis / Interpretation / Knowledge |
| C2 | `rows/Row01`–`Row04` | Pre-zone row containers |
| C3 | `shell/PortalChrome` | Still used by PortalPage (keep) |

### 3.4 Non-analysis (out of unification scope)

| Surface | Route | Note |
|---------|-------|------|
| Dashboard | `/dashboard` | May link to `/result`; not analysis render |
| Reports / History / Profile / Login | respective routes | Keep |

---

## 4. Duplicated Routes

| User intent | Official | Duplicate / legacy |
|-------------|----------|-------------------|
| View analysis result | `GET /result` | `GET /result?legacy=1` |
| Same intent (template) | `result_desktop.html` | `result_legacy.html`, `result.html` (reference) |
| Analyze input | `GET /analyze` | — (not duplicate) |

No separate FastAPI routes exist for ExecutiveSummary / FourPillars / BaZiResult — those are React modules without dedicated portal routes today (risk: re-introduction via future mounts).

---

## 5. Duplicated Components (by concern)

| Concern | Official (Result) | Duplicate (legacy / WP) |
|---------|-------------------|-------------------------|
| Executive summary | `result/cards/SummaryCards` | `bazi/ExecutiveSummaryCard`, `business/Executive*` , `ExecutiveSummaryScreen` |
| Four pillars | (via Context / analysis data) | `bazi/FourPillarsCard`, `business/*Pillar*`, `FourPillarsScreen`, `S03FourPillars` |
| Five elements | `result/cards/AnalysisCards` | `bazi/FiveElementsCard`, `S04ElementBalance` |
| Strength | `StrengthAnalysisCard` | `bazi/StrengthCard`, `S05ChartStrength` |
| Ten gods | `TenGodsAnalysisCard` | `bazi/TenGodsCard`, `S06TenGods` |
| Shen Sha | (knowledge / analysis) | `bazi/ShenShaCard`, `S07ShenSha` |
| Interpretation | `InterpretationCard` (LP-006) | `bazi/InterpretationCard`, `S08Interpretation`, `business/ExplainableAnalysis` |
| Knowledge | `KnowledgeCard` (LP-007) | `bazi/KnowledgeCard`, `business/KnowledgeReference*` |
| Recommendation | `RecommendationCard` (LP-005) | `business/RecommendationPanel`, parts of S11 |
| Status gates | `ResultPageStatusGate` | `bazi/SectionGate`, per-screen loading/empty |
| Report shell | Portal chrome + Result zones | `ConsultationReport`, legacy `rpt-*` HTML |

---

## 6. Duplicated ViewModels

| Layer | Official | Duplicates |
|-------|----------|------------|
| API → Desktop | `CanonicalDesktopViewModel` (`canonicalDesktopAdapter`) | — |
| Desktop → Result | `ResultPageViewModel` (`result/viewModels.ts`) | — |
| Legacy BaZi UI | — | `BaZiResultViewModel` (`baziResultAdapter` / mock bundle) |
| WP slice VMs | — | `view_models/executive_summary`, `four_pillars`, `executive_insight`, `metrics`, `explainable_analysis`, `consultation_report`, `appendix` |
| Fixture | `CANONICAL_DESKTOP_MOCK` | `BAZI_RESULT_MOCK`, per-WP fixtures in tests |

**Overlap:** Many WP ViewModels restate fields already present in `CanonicalDesktopViewModel` slices (`s01`…`s11`) and/or Result zone ViewModels.

---

## 7. Duplicated Presentation Logic

| Capability | Official | Duplicates |
|------------|----------|------------|
| Truncation / preview / hasMore | `presentation/presentationAdapter.ts` + `result/presentation/previewBuilder.ts` | Implicit truncation in business components / legacy JS presenters |
| API adaptation | `adaptAnalysisToCanonicalDesktop` | `adaptAnalysisToBaZiResult` (parallel mapping) |
| Gates | `createCanonicalDesktopGateViewModel` + `ResultPageStatusGate` | `createBaZiResultGateViewModel` + screen-local gates |
| Legacy presenters | — | `static/js/presenters/*`, `static/js/report/*` (legacy result) |
| Hooks | `useCanonicalDesktopResult` | `useBaZiResult` |

---

## 8. Data Path Comparison

### Official

```
AnalyzeChartRequest
→ AnalyzeService.getCanonicalDesktopViewModel
→ adaptAnalysisToCanonicalDesktop
→ useCanonicalDesktopResult
→ adaptResultPageViewModel
→ Result zones / cards
```

### Legacy parallel (still in codebase)

```
AnalyzeChartRequest
→ AnalyzeService.getBaZiResultViewModel
→ adaptAnalysisToBaZiResult
→ useBaZiResult
→ BaZiResultScreen cards
```

### Legacy HTML

```
ResultStore / static JS
→ /result?legacy=1
→ presenters + report JS
```

---

## 9. Findings Summary

| Finding | Severity |
|---------|----------|
| Three analysis render stacks coexist (Result zones, BaZi React, Legacy HTML) | **Critical** |
| Two API adapters for the same `/analyze` payload | **High** |
| WP slice screens duplicate Result zone responsibilities | **High** |
| Canonical `sections`/`rows` orphaned from PortalPage render | **Medium** |
| `/result?legacy=1` still publicly reachable | **Medium** |
| Dashboard already links to `/result` (good) | Info |

---

## 10. Success Criteria (future migration epics)

Unification is complete only when:

1. End users can view analysis **only** via `/result` → Result Page.
2. Legacy query flag is removed or admin-only.
3. No new features land on BaZi / WP slice analysis UIs.
4. Single adapter path: Canonical Desktop → Result ViewModel.
5. Documentation and Cursor rules name Result Page as sole Analysis Experience.

---

## Related Documents

- `ANALYSIS_MIGRATION_PLAN.md`
- `ANALYSIS_DEPRECATION_LIST.md`
- `FOUNDATION_ADOPTION_PLAN.md` (Wave 2)
- `PACK_06` / `PACK_07` / Result freeze reports

---

END
