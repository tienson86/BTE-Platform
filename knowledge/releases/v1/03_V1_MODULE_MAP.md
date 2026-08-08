# 03 — BTE V1 Module Map

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Complete module map for BTE V1: responsibility, dependencies, public API, consumers, and status.

Status legend:

| Status | Meaning |
|--------|---------|
| **Active** | In production path |
| **Frozen** | Contract frozen; bugfix OK; no redesign without review |
| **Deprecated** | Still present; prefer successor; removal tracked |

---

## 2. Knowledge & Rules

| Module | Responsibility | Dependencies | Public API | Consumers | Status |
|--------|----------------|--------------|------------|-----------|--------|
| Rule Database (`database/` / knowledge CSVs) | Business rules | — | Loaders only | All engines via loaders | Active · Frozen schema rules |
| Knowledge packs (`knowledge/`) | Specs, golden, architecture | — | Documents | Humans / CI docs | Active · Foundation frozen separately |

---

## 3. Engines

| Module | Responsibility | Dependencies | Public API | Consumers | Status |
|--------|----------------|--------------|------------|-----------|--------|
| `engines/calendar_engine` | Calendar computation | Rule/calendar data | Calendar Engine / service | Orchestrator, BaZi | Active · Frozen |
| `engines/bazi_engine` | Chart / pillars | Calendar | BaZi Engine / models | Orchestrator, Score, UI | Active · Frozen |
| `engines/pattern_engine` (+ `engines/pattern`) | Pattern recognition | BaZi, Strength, Temperature | Pattern result | RuleContext, UI | Active |
| `engines/strength_engine` | Day-master strength | BaZi | Strength result | Pattern, Score, UI | Active |
| `engines/temperature_engine` | Temperature / climate | BaZi | Temperature result | Pattern | Active |
| `engines/useful_god_engine` | Dụng thần | Analysis peers | Useful god result | Score labels, UI | Active |
| `engines/score_engine` | Scoring / AnalysisResult | Chart + rules | `ScoreEngine`, `AnalysisResult`, … | Interpretation, Orchestrator | Active · Complete · Frozen |
| `engines/luck_engine` | Luck / đại vận context | Chart | LuckContext | Interpretation | Active |
| `engines/feng_shui_engine` | Feng shui / quái | Calendar / chart | Feng shui result | Orchestrator (soft), UI | Active (soft-fail) |
| `engines/context_engine` | Context helpers | Peers | Context APIs | Analysis path | Active |
| `engines/interpretation_engine` | InterpretationResult | Analysis + rules | `InterpretationEngine`, Pack 04 path | Narrative, Report, API | Active · Complete · Frozen |
| `engines/narrative_engine` | NarrativeTree + NarrativeResult (+ WP7 prose path) | Analysis + Interpretation | `NarrativeEngine.compose_tree`, `compose_narrative_result`, … | API `narrative_result_truth` | Active · Complete · Frozen |
| `engines/report_engine` | Report formatting / delivery markdown | Interpretation / analysis views | `ReportEngine` | Orchestrator delivery `narrative` | Active · **Not redesigned** |
| `engines/analysis_engine` | Analysis orchestration helpers | Peers | Analysis Engine | Internal / legacy paths | Active / legacy overlap — see deprecation |

---

## 4. Application

| Module | Responsibility | Dependencies | Public API | Consumers | Status |
|--------|----------------|--------------|------------|-----------|--------|
| `applications/api/services/orchestrator.py` | Stage pipeline | Engines | `OrchestratorService.analyze` / stage stops | HTTP routes | Active · Frozen order |
| `applications/api/services/narrative_result_truth.py` | Serialize Pack 05 NarrativeResult | NarrativeEngine public API | `build_narrative_result_dict` | Orchestrator | Active |
| `applications/api/routes/v1.py` | `/calendar` … `/analyze` | Orchestrator | REST | Portal, clients | Active |
| Auth / Cases / Customers / License / Admin | Product ops | App services | REST | Portal / admin | Active |

---

## 5. Portal (Customer)

| Module | Responsibility | Dependencies | Public API | Consumers | Status |
|--------|----------------|--------------|------------|-----------|--------|
| `adapters/narrativeResultAdapter.ts` | Pack 05 DTO helpers | API DTO | `asNarrativeResult`, `hasUsableNarrativeResult` | Canonical / Result / BaZi adapters | Active · Official helper |
| `adapters/canonicalDesktopAdapter.ts` | Analysis → Canonical Desktop VM | DTO + narrative helper | `adaptAnalysisToCanonicalDesktop` | Result boot, analyze service | Active · Official |
| `screens/result/adapters/resultPresentationAdapter.ts` | Canonical → Result Page VM | Canonical VM | `adaptResultPageViewModel` | PortalPage | Active · Official |
| `adapters/baziResultAdapter.ts` | Analysis → BaZi Result VM | DTO + narrative helper | `adaptAnalysisToBaZiResult` | BaZi screen / hook | Active · **Deprecated path** (parallel) |
| `adapters/dashboardAdapter.ts` | Dashboard VM | DTO | `adaptDashboardViewModel` | Dashboard surfaces | Active |
| `adapters/contentGuards.ts` | Commercial text gating | — | Guards / extractors | Adapters | Active |
| Result Page zones/cards | Layout Patterns LP-00x | Result VM | Screen components | End user | Active · Architecture frozen |
| `BaZiResultScreen` | Wave-3 result UI | BaZi VM | Screen | Legacy/parallel | Deprecated (parallel) |
| WP-0004 Executive / WP-0009 Consultation screens | Pack 06 presentation | Own ViewModels | Screens | Optional surfaces | Active · Not on NarrativeResult yet |
| Foundation / Design System CSS & packs | Tokens, components | — | UI packages | All screens | **Frozen V1.0** |

---

## 6. Architecture Knowledge Packs

| Pack | Topic | Status |
|------|-------|--------|
| Pack 01 | Calendar Engine | Frozen docs |
| Pack 02 | BaZi Engine | Frozen docs |
| Pack 03 | Score Engine | Complete |
| Pack 04 | Interpretation Engine | Complete |
| Pack 05 Narrative | Narrative Engine A–D2 | Complete · Frozen |
| Pack 05 Report | Report Engine architecture | Spec present · implementation not redesigned |
| UI Foundation / Design System | Presentation law | **Frozen V1.0** |

---

## 7. Ownership Summary

```
Rules     → Database owners
Facts     → Calendar / BaZi / Score owners
Evidence  → Interpretation owners
Prose     → Narrative owners
Wire      → API / Orchestrator owners
UX map    → Portal adapter owners
Pixels    → Foundation / Result Page owners
```

---

END
