/**
 * BZ-UI-03 BaziWorkspaceViewModel — presentation only.
 * Every field is copied or formatted from a canonical analysis source.
 */

import type { TuTruSlotPillar } from "../types";

export type WorkspaceField<T> = {
  readonly value: T | null;
  readonly available: boolean;
  readonly source: string;
};

export type WorkspacePersonView = {
  readonly name: WorkspaceField<string>;
  readonly gender: WorkspaceField<string>;
  readonly solarDate: WorkspaceField<string>;
  readonly lunarDate: WorkspaceField<string>;
  readonly birthTime: WorkspaceField<string>;
  readonly location: WorkspaceField<string>;
  readonly timezone: WorkspaceField<string>;
  readonly analysisId: WorkspaceField<string>;
};

export type WorkspaceOverviewView = {
  readonly strength: WorkspaceField<string>;
  readonly strengthScore: WorkspaceField<string>;
  readonly usefulGod: WorkspaceField<string>;
  readonly favorableGod: WorkspaceField<string>;
  readonly avoidGod: WorkspaceField<string>;
  readonly overallScore: WorkspaceField<number>;
  readonly overallScoreMax: number;
  readonly confidence: WorkspaceField<string>;
};

export type WorkspaceFiveElementRow = {
  readonly id: "wood" | "fire" | "earth" | "metal" | "water";
  readonly name: "Mộc" | "Hỏa" | "Thổ" | "Kim" | "Thủy";
  readonly count: WorkspaceField<number>;
  /** Presentation-only: count / canonical total. Not analytical reweighting. */
  readonly percent: WorkspaceField<number>;
};

export type WorkspaceFiveElementsView = {
  readonly rows: readonly WorkspaceFiveElementRow[];
  readonly observation: WorkspaceField<string>;
  readonly unitTotal: WorkspaceField<number>;
};

export type WorkspaceTenGodRow = {
  readonly name: string;
  readonly count: WorkspaceField<number>;
};

export type WorkspaceTenGodsView = {
  readonly rows: readonly WorkspaceTenGodRow[];
  readonly available: boolean;
};

export type WorkspacePatternView = {
  readonly pattern: WorkspaceField<string>;
  readonly patternClass: WorkspaceField<string>;
  readonly climate: WorkspaceField<string>;
  readonly quality: WorkspaceField<string>;
  readonly summary: WorkspaceField<string>;
};

export type WorkspaceShenShaRow = {
  readonly name: string;
  readonly presence: WorkspaceField<string>;
  readonly catalog: boolean;
};

export type WorkspaceShenShaView = {
  readonly rows: readonly WorkspaceShenShaRow[];
};

export type WorkspaceBoneWeightView = {
  readonly amount: WorkspaceField<string>;
  readonly classification: WorkspaceField<string>;
  readonly interpretation: WorkspaceField<string>;
};

export type WorkspaceLuckCycleView = {
  readonly ganZhi: string;
  readonly ageStart: number | null;
  readonly ageEnd: number | null;
  readonly yearStart: number | null;
  readonly yearEnd: number | null;
  readonly current: boolean;
};

export type WorkspaceLuckView = {
  readonly current: WorkspaceField<string>;
  readonly ageRange: WorkspaceField<string>;
  readonly ganZhi: WorkspaceField<string>;
  readonly currentYear: WorkspaceField<string>;
  readonly currentLiunian: WorkspaceField<string>;
  readonly observation: WorkspaceField<string>;
  readonly cycles: readonly WorkspaceLuckCycleView[];
};

export type WorkspaceInterpretationView = {
  readonly executive: WorkspaceField<string>;
  readonly observe: WorkspaceField<string>;
  readonly reason: WorkspaceField<string>;
  readonly impact: WorkspaceField<string>;
  readonly advice: WorkspaceField<string>;
  readonly summary: WorkspaceField<string>;
  readonly observationId: WorkspaceField<string>;
  readonly reasoningId: WorkspaceField<string>;
  readonly recommendationId: WorkspaceField<string>;
  readonly conclusionId: WorkspaceField<string>;
  readonly sectionKeys: readonly string[];
};

export type WorkspaceActionChipView = {
  readonly id: string;
  readonly label: string;
  readonly available: boolean;
};

export type WorkspaceConclusionView = {
  readonly summary: WorkspaceField<string>;
  readonly overall: WorkspaceField<string>;
  readonly action: WorkspaceField<string>;
  readonly actions: readonly WorkspaceActionChipView[];
};

export type BaziWorkspaceViewModel = {
  readonly analysisId: string;
  readonly person: WorkspacePersonView;
  readonly fourPillars: {
    readonly year: TuTruSlotPillar;
    readonly month: TuTruSlotPillar;
    readonly day: TuTruSlotPillar;
    readonly hour: TuTruSlotPillar;
  };
  readonly overview: WorkspaceOverviewView;
  readonly fiveElements: WorkspaceFiveElementsView;
  readonly tenGods: WorkspaceTenGodsView;
  readonly pattern: WorkspacePatternView;
  readonly shenSha: WorkspaceShenShaView;
  readonly boneWeight: WorkspaceBoneWeightView;
  readonly luck: WorkspaceLuckView;
  readonly interpretation: WorkspaceInterpretationView;
  readonly conclusion: WorkspaceConclusionView;
};
