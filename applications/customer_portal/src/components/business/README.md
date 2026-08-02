# Business Components (WP-0004 … WP-0009)

Presentation components for Commercial UI V3 business screens.
Compose Shared Components only. Consume presentation ViewModels only.

## Executive Summary (WP-0004)

- ExecutiveHero, RecommendationPanel, ExecutiveOverview, ExecutiveHighlights,
  SummaryGlance, HeroBackground, HeroActions

## Four Pillars (WP-0005)

- FourPillarsChart, PillarColumn, PillarHeader, HeavenlyStemCell,
  EarthlyBranchCell, HiddenStemGroup, NaYinPanel, LifeStagePanel,
  ChartMetadata, ChartLegend

## Executive Insight (WP-0006)

- ExecutiveInsightHero, InsightSection, OpportunityPanel, RiskPanel,
  RecommendationPanel (reused), InsightSummary, ExecutiveConclusion

## Metrics (WP-0007)

- MetricsSummary, MetricSection, MetricCard (`BusinessMetricCard`),
  MetricIndicator, MetricExplanation, ConfidencePanel, BalancePanel

## Explainable Analysis (WP-0008)

- ExplainableAnalysis, AnalysisSection, ConclusionPanel, ExplanationPanel,
  EvidencePanel, RuleReferencePanel, ConfidencePanel (reused),
  KnowledgeReferencePanel, RecommendationPanel (reused), AnalysisSummary

## Consultation Report (WP-0009)

- ConsultationReport
- ReportContainer
- ReportHeader
- ReportSection
- ReportFooter
- ReportProgress
- SectionTransition
- TableOfContents
- PrintHeader
- PrintFooter

## Rules

- No Base Component imports (Shared only).
- No analysis, scoring, calculation, API, or Knowledge Engine access.
- Report orchestrates frozen screens; does not reimplement them.
- Support Loading / Ready / Empty / Unavailable / Error via presentation status.
- Public imports via barrel only.
