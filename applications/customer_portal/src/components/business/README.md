# Business Components (WP-0004 … WP-0007)

Presentation components for Commercial UI V3 business screens.
Compose Shared Components only. Consume presentation ViewModels only.

## Executive Summary (WP-0004)

- ExecutiveHero
- RecommendationPanel
- ExecutiveOverview
- ExecutiveHighlights
- SummaryGlance
- HeroBackground
- HeroActions

## Four Pillars (WP-0005)

- FourPillarsChart
- PillarColumn
- PillarHeader
- HeavenlyStemCell
- EarthlyBranchCell
- HiddenStemGroup
- NaYinPanel
- LifeStagePanel
- ChartMetadata
- ChartLegend

## Executive Insight (WP-0006)

- ExecutiveInsightHero
- InsightSection
- OpportunityPanel
- RiskPanel
- RecommendationPanel (reused from WP-0004 — frozen)
- InsightSummary
- ExecutiveConclusion

## Metrics (WP-0007)

- MetricsSummary
- MetricSection
- MetricCard (public alias: `BusinessMetricCard` — Shared already exports `MetricCard`)
- MetricIndicator
- MetricExplanation
- ConfidencePanel
- BalancePanel

## Rules

- No Base Component imports (Shared only).
- No analysis, scoring, calculation, API, or Knowledge Engine access.
- Support Loading / Ready / Empty / Unavailable / Error via presentation status.
- Public imports via barrel only.
