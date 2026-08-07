# ANALYSIS_DEPRECATION_LIST.md

Version: 1.0  
Date: 2026-08-07  
Epic: Analysis Experience Unification  
Status: **ACTIVE DEPRECATION REGISTRY** (documentation)  
Action in this epic: **List only — do not delete or refactor**

---

## Legend

| Tag | Meaning |
|-----|---------|
| **DEPRECATED** | Must not receive new features; migrate away |
| **SUPERSEDED** | Replaced by official Result Page; keep until cleanup |
| **LEGACY_ROUTE** | Public or semi-public alternate entry |
| **TEST_ONLY** | Acceptable for regression tests until cleanup |
| **KEEP** | Official — not deprecated |

---

## 1. Official (KEEP)

| Item | Path / Route | Notes |
|------|--------------|-------|
| Result Page body | `src/screens/result/**` | Analysis SSOT UI |
| PortalPage / ResultPage | `src/screens/canonical_desktop/PortalPage.tsx` | Official host |
| Portal chrome | `canonical_desktop/shell/**` | Keep with Result |
| Result entry | `src/entries/resultApp.tsx` | Production mount |
| Result boot | `src/entries/resultBoot.ts` | ResultStore → props |
| Desktop template | `templates/result_desktop.html` | `/result` |
| Canonical adapter | `adapters/canonicalDesktopAdapter.ts` | Official API→VM |
| Result adapter | `screens/result/adapters/resultPresentationAdapter.ts` | Official VM→zones |
| PACK_04 presentation | `src/presentation/**` | Official truncation |
| Hook | `hooks/useCanonicalDesktopResult.ts` | Official data hook |
| Route | `GET /result` | Official analysis view |
| Input route | `GET /analyze` | Keep (not analysis render) |

---

## 2. Routes

| Item | Status | Replacement |
|------|--------|-------------|
| `GET /result` | **KEEP** | — |
| `GET /result?legacy=1` | **LEGACY_ROUTE / DEPRECATED** | `/result` |
| `templates/result_legacy.html` | **DEPRECATED** | `result_desktop.html` |
| `templates/result.html` | **DEPRECATED** (reference) | `result_desktop.html` |
| `/static/js/result.js` (legacy) | **DEPRECATED** | `/static/dist/result.js` |
| `/static/js/presenters/*` | **DEPRECATED** | Result zones + adapters |
| `/static/js/report/*` | **DEPRECATED** | Result visualization cards |

---

## 3. Screens

| Item | Status | Replacement |
|------|--------|-------------|
| `BaZiResultScreen` | **DEPRECATED** | `PortalPage` + Result zones |
| `ExecutiveSummaryScreen` | **SUPERSEDED** | SummaryZone / ExecutiveSummaryCard |
| `FourPillarsScreen` | **SUPERSEDED** | Context / analysis presentation |
| `ExecutiveInsightScreen` | **SUPERSEDED** | Summary / Interpretation zones |
| `MetricsScreen` | **SUPERSEDED** | AnalysisZone metrics |
| `ExplainableAnalysisScreen` | **SUPERSEDED** | InterpretationZone (LP-006) |
| `ConsultationReportScreen` | **DEPRECATED** | Single Result Page journey |
| `AppendixScreen` | **SUPERSEDED** | KnowledgeZone appendix section |
| `S00DesktopScreen` | **DEPRECATED** | Result ContextZone |
| `NavigationScreen` | Not analysis render | Out of scope (shell/nav separately) |
| `DashboardScreen` | Not analysis render | Keep; links should target `/result` |

---

## 4. Canonical Desktop section stack

| Item | Status | Replacement |
|------|--------|-------------|
| `sections/S00`–`S11` | **SUPERSEDED** | `screens/result/zones/*` |
| `rows/Row01`–`Row04` | **SUPERSEDED** | Result `ResultRow` / zones |
| Export of Rows from `canonical_desktop/index` | **SUPERSEDED** | Do not use for new UI |

Note: `CanonicalDesktopViewModel` **data** slices `s00`–`s11` remain **KEEP** as the adapter output feeding Result presentation.

---

## 5. BaZi component tree

| Item | Status | Replacement |
|------|--------|-------------|
| `screens/bazi/*Card.tsx` | **DEPRECATED** | `screens/result/cards/*` |
| `bazi/CoreAnalysisSection` | **DEPRECATED** | AnalysisZone |
| `bazi/SectionGate` | **SUPERSEDED** | ResultPageStatusGate |
| `bazi/mockData.ts` | **TEST_ONLY / DEPRECATED** | Canonical mock + Result VMs |
| `bazi/index.ts` public exports | **DEPRECATED** for product | Tests only |

---

## 6. Business components (analysis-overlapping)

| Item | Status | Notes |
|------|--------|-------|
| `ConsultationReport` | **DEPRECATED** for analysis UX | Use Result Page |
| `ExplainableAnalysis` | **SUPERSEDED** | LP-006 |
| `ExecutiveHero` / `ExecutiveOverview` / `ExecutiveHighlights` / `ExecutiveConclusion` / `ExecutiveInsightHero` | **SUPERSEDED** | SummaryZone |
| `RecommendationPanel` | **SUPERSEDED** | LP-005 |
| `KnowledgeReferencePanel` / `KnowledgeReferenceSection` / `GlossarySection` | **SUPERSEDED** | LP-007 |
| `MetricCard` / `MetricsSummary` / `MetricSection` / `MetricExplanation` | **SUPERSEDED** | AnalysisZone |
| Four-pillars business cells/panels | **SUPERSEDED** | Result context/analysis |
| Appendix business pieces | **SUPERSEDED** | Knowledge appendix |

Non-analysis business utilities (print headers used elsewhere) — review case-by-case in cleanup; not auto-deleted here.

---

## 7. ViewModels & adapters

| Item | Status | Replacement |
|------|--------|-------------|
| `ResultPageViewModel` | **KEEP** | — |
| `CanonicalDesktopViewModel` | **KEEP** | — |
| `BaZiResultViewModel` / `adaptAnalysisToBaZiResult` | **DEPRECATED** | Canonical + Result adapters |
| `createBaZiResultGateViewModel` | **DEPRECATED** | `createCanonicalDesktopGateViewModel` |
| `view_models/executive_summary.ts` | **SUPERSEDED** | Result summary VMs |
| `view_models/four_pillars.ts` | **SUPERSEDED** | Canonical / Result |
| `view_models/executive_insight.ts` | **SUPERSEDED** | Result interpretation/summary |
| `view_models/metrics.ts` | **SUPERSEDED** | Result analysis |
| `view_models/explainable_analysis.ts` | **SUPERSEDED** | Result interpretation |
| `view_models/consultation_report.ts` | **DEPRECATED** | Result Page journey |
| `view_models/appendix.ts` | **SUPERSEDED** | Result knowledge |
| `view_models/navigation.ts` | Keep if used by nav | Not analysis |

---

## 8. Hooks & services

| Item | Status | Replacement |
|------|--------|-------------|
| `useCanonicalDesktopResult` | **KEEP** | — |
| `useBaZiResult` | **DEPRECATED** | `useCanonicalDesktopResult` |
| `AnalyzeService.getCanonicalDesktopViewModel` | **KEEP** | — |
| `AnalyzeService.getBaZiResultViewModel` | **DEPRECATED** | Canonical method (+ wrapper until cleanup) |

---

## 9. Tests (tagged)

| Suite | Status | Note |
|-------|--------|------|
| `canonical_desktop*.test.*` | **KEEP** | Official |
| `result_app_boot.test.ts` | **KEEP** | Official |
| `wave3_bazi_result.test.tsx` | **TEST_ONLY** | Covers deprecated UI |
| `wp_0004`–`wp_0010` screen tests | **TEST_ONLY** | Covers superseded slices |
| `task_003a` using `adaptAnalysisToBaZiResult` | **TEST_ONLY** until adapter migration |

Do not delete tests in this epic.

---

## 10. Enforcement Rules (for future PRs)

1. **No new features** on any **DEPRECATED** or **SUPERSEDED** analysis UI.
2. **No new portal routes** mounting BaZi or WP analysis screens.
3. Bugfixes on deprecated stacks only if production still depends on them; prefer fixing official path.
4. Cleanup / deletion requires a dedicated epic after traffic = 0.

---

## 11. Recommended Official Analysis Flow (summary)

```
/analyze  →  ResultStore  →  /result  →  PortalPage  →  ResultPageBody
```

Everything else on this list is transitional.

---

END
