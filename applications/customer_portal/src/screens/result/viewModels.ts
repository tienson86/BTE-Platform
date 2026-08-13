/**
 * Result Page presentation ViewModels — Sprint A + Sprint B.
 * UI consumes these models only — never raw engine payloads.
 */

import type { PreviewList, PreviewText } from "../../presentation";

export type ContextZoneViewModel = {
  readonly title: string;
  /** Customer-facing identity question label. */
  readonly identityLabel: string;
  readonly profileName: string;
  readonly profileMeta: string;
  readonly birthDate: string;
  readonly birthLunar: string;
  readonly birthTime: string;
  readonly chartId: string;
  readonly status: string;
  readonly analyzedAt: string;
  readonly cungPhi: string;
  readonly menhQuai: string;
  readonly nhomTrach: string;
};

export type ExecutiveSummaryViewModel = {
  readonly title: string;
  readonly headline: PreviewText;
  /** Supporting bullets (≤4). */
  readonly points: PreviewList<string>;
  /** Closing consulting line when available. */
  readonly conclusion: PreviewText | null;
  readonly hasMore: boolean;
  readonly primaryCtaLabel: string;
  readonly secondaryCtaLabel: string;
};

export type CoreIndicatorsViewModel = {
  readonly title: string;
  readonly items: PreviewList<{
    readonly label: string;
    readonly value: string;
    readonly color: string;
  }>;
  readonly hasMore: boolean;
  /** Priority 3 — omit from hero when false. */
  readonly visible: boolean;
};

export type DestinyDirectionViewModel = {
  readonly title: string;
  /** Single-question responsibility: career direction. */
  readonly questionLabel: string;
  readonly items: PreviewList<{
    readonly question: string;
    readonly answer: PreviewText;
  }>;
  readonly cta: string;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

export type FiveElementsViewModel = {
  readonly title: string;
  readonly rows: PreviewList<{
    readonly name: string;
    readonly element: string;
    readonly pct: number;
    readonly count: number | null;
    readonly status: string;
  }>;
  readonly summary: PreviewText;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

export type StrengthAnalysisViewModel = {
  readonly title: string;
  readonly level: string;
  readonly score: string;
  readonly percent: number;
  readonly insight: PreviewText;
  readonly factors: PreviewList<{ readonly text: string; readonly tone: string }>;
  readonly cta: string;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

export type TenGodsAnalysisViewModel = {
  readonly title: string;
  readonly gods: PreviewList<{
    readonly name: string;
    readonly score: string;
    readonly color: string;
  }>;
  readonly cta: string;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

export type RadarChartViewModel = {
  readonly title: string;
  readonly axes: readonly {
    readonly name: string;
    readonly pct: number;
    readonly element: string;
  }[];
  readonly summary: PreviewText;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

export type LuckTimelineViewModel = {
  readonly title: string;
  readonly stages: PreviewList<{
    readonly label: string;
    readonly detail: PreviewText;
  }>;
  readonly summary: PreviewText;
  readonly hasMore: boolean;
  readonly visible: boolean;
};

/** LP-005 priority levels — Critical → Low. */
export type RecommendationPriority = "critical" | "high" | "medium" | "low";

export type RecommendationItemViewModel = {
  readonly id: string;
  readonly priority: RecommendationPriority;
  readonly priorityLabel: string;
  readonly action: PreviewText;
  readonly reason: PreviewText;
  readonly benefit: PreviewText;
  readonly detail: PreviewText;
  readonly hasMore: boolean;
};

export type RecommendationZoneViewModel = {
  readonly title: string;
  readonly items: readonly RecommendationItemViewModel[];
  readonly totalCount: number;
  readonly hasMore: boolean;
  readonly viewAllLabel: string;
  readonly visible: boolean;
  readonly primaryCtaLabel: string;
  readonly secondaryCtaLabel: string;
};

/** LP-006 interpretation block — Observation → Explanation → Impact → Suggestion. */
export type InterpretationBlockViewModel = {
  readonly id: string;
  readonly title: string;
  readonly observation: PreviewText;
  readonly explanation: PreviewText;
  readonly impact: PreviewText;
  readonly suggestion: PreviewText;
  readonly hasMore: boolean;
};

export type InterpretationZoneViewModel = {
  readonly title: string;
  readonly blocks: readonly InterpretationBlockViewModel[];
  readonly expandLabel: string;
  readonly collapseLabel: string;
  readonly visible: boolean;
};

/** LP-007 knowledge sections. */
export type KnowledgeSectionKind =
  | "terminology"
  | "references"
  | "theory"
  | "appendix";

export type KnowledgeSectionViewModel = {
  readonly id: string;
  readonly kind: KnowledgeSectionKind;
  readonly title: string;
  readonly definition: PreviewText;
  readonly reference: PreviewText;
  readonly detail: PreviewText;
  readonly hasMore: boolean;
  readonly defaultOpen: boolean;
};

export type KnowledgeZoneViewModel = {
  readonly title: string;
  readonly sections: readonly KnowledgeSectionViewModel[];
  readonly visible: boolean;
};

export type ChartPillarViewModel = {
  readonly label: string;
  readonly stem: string;
  readonly branch: string;
  readonly napAm: string;
  readonly hiddenStems: string;
  readonly tenGod: string;
  readonly growthStage: string;
};

export type ChartDetailViewModel = {
  readonly title: string;
  readonly pillars: readonly ChartPillarViewModel[];
  readonly visible: boolean;
};

export type ShenShaViewModel = {
  readonly title: string;
  readonly items: readonly string[];
  readonly visible: boolean;
};

export type ResultPageViewModel = {
  readonly analysisId: string;
  readonly chart: ChartDetailViewModel;
  readonly shenSha: ShenShaViewModel;
  readonly context: ContextZoneViewModel;
  readonly executive: ExecutiveSummaryViewModel;
  readonly indicators: CoreIndicatorsViewModel;
  readonly destiny: DestinyDirectionViewModel;
  readonly fiveElements: FiveElementsViewModel;
  readonly strength: StrengthAnalysisViewModel;
  readonly tenGods: TenGodsAnalysisViewModel;
  readonly radar: RadarChartViewModel;
  readonly timeline: LuckTimelineViewModel;
  readonly recommendations: RecommendationZoneViewModel;
  readonly interpretation: InterpretationZoneViewModel;
  readonly knowledge: KnowledgeZoneViewModel;
};
