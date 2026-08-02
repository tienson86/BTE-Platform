# COMPONENT MAP

| Field | Value |
|-------|--------|
| **Document** | `COMPONENT_MAP.md` |
| **Version** | `1.1.0` |
| **Status** | Final Freeze — Blueprint V1.1 (logical components — not code yet) |

---

## Purpose

Catalogue every **logical UI component** required to implement the Result IA and related screens.

- **Input** = props / view-model fields (presentation data only)
- **Output** = rendered region / events
- **Purpose** = why it exists
- **Dependency** = other components or data adapters (no engines)
- **Layer** = Atomic | Composite | Layout | Business (presentation) — Addendum D

| Layer | Definition |
|-------|------------|
| **Atomic** | No domain orchestration |
| **Composite** | Combines atomics for one UI job |
| **Layout** | Page regions / chrome |
| **Business (presentation)** | Binds ResultStore/view-model — **no engine logic** |

Bindings: [18_BINDING_INDEX.md](18_BINDING_INDEX.md).

---

## Page shells (Layout)

| Component | Purpose | Must never hide |
|-----------|---------|-----------------|
| ResultPage | Chrome + NavigationRail + ReportStream | — |
| DashboardPage | Orient; recent; CTA Analyze | **CTA Analyze** |
| AnalyzePage | Birth intake → Result | — |
| ReportsPage | Preview/export; page-1 follows Result spine | Empty state |
| HistoryPage / ProfilePage / LoginPage | Secondary flows | — |

---

## Navigation & chrome

| Component | Layer | Notes |
|-----------|-------|-------|
| ResultChrome | Layout | Title, meta, actions |
| NavigationRail | Layout | Canonical name (not NavRail) |
| RailItem | Atomic | Anchor control |
| ReadingProgress | Atomic | 0–1 or steps 1–6 |
| ScrollSpyController | Business | Updates active rail |

---

## Tier 1 — Executive

| Component | Layer | Purpose |
|-----------|-------|---------|
| ExecutiveHero | Composite | Dominant first surface |
| DayMasterDisplay | Composite | Largest identity |
| QualityVerdictCaption | Atomic | Calm quality/confidence (Addendum A) |
| FirstRecommendation | Composite | Hero callout or Unavailable |
| SummaryMetric | Atomic | Hero metrics only (not dashboard MetricCard) |
| StrengthWeaknessPanel | Composite | Score lists only |

---

## Tier 2 — Pillars

| Component | Layer |
|-----------|-------|
| PillarGrid | Composite |
| PillarColumn | Composite |
| PillarRow | Atomic |

---

## Tier 3 — Charts

| Component | Layer |
|-----------|-------|
| ChartBand | Layout |
| ElementRadar | Composite |
| StrengthGauge | Composite |
| DistributionBars | Composite |
| TenGodBars | Composite |
| ChartEmpty | Atomic |

---

## Tier 4 — Analysis

| Component | Layer |
|-----------|-------|
| AnalysisStack | Composite |
| AnalysisSection | Composite |
| RelationMatrix | Composite |
| KnowledgeStatusPanel | Composite |

---

## Tier 5 — Interpretation (document)

| Component | Layer | Purpose |
|-----------|-------|---------|
| InterpretationDocument | Composite | Owns Tier 5 |
| InterpretationTOC | Composite | Required if ≥2 chapters available |
| InterpretationChapter | Composite | H2 + body (+ callout/refs) |
| ReportCallout | Atomic | Insight/caution |
| ReportReferenceList | Atomic | Citations when present |

`InterpretationSection` = allowed alias of `InterpretationChapter`.

---

## Tier 6 — Knowledge

| Component | Layer |
|-----------|-------|
| KnowledgeStack | Composite |
| KnowledgeEvidencePanel | Composite |
| KnowledgeExpertPane | Composite |
| ConversationPane / AnswerPane / SourcesPane | Composite |
| NarrativeFallback | Composite |

---

## Shared primitives (Atomic unless noted)

EmptyState, UnavailableBlock, ErrorPanel, StatusBadge, MetricCard (dashboard only), Icon, Skeleton, FormSection (Composite), FieldError.

---

## ReportViewModelAdapter

| | |
|--|--|
| **Layer** | Business (presentation) |
| **Purpose** | Payload → view model per Binding Index |
| **Must not** | Call engines; invent values |

---

## Version

`1.1.0`
