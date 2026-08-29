/**
 * UI-03 Commercial Dashboard view models. Presentation only.
 */

export type IdentityPillarView = {
  readonly stem: string;
  readonly branch: string;
  readonly napAm: string;
};

export type IdentityPersonView = {
  readonly fullName: string;
  readonly gender: string;
  readonly solarBirth: string;
  readonly lunarBirth: string;
  readonly birthTime: string;
  readonly birthPlace: string;
};

export type IdentityFoundationView = {
  readonly cungPhi: string;
  readonly menhQuai: string;
  readonly nhomTrach: string;
  readonly tietKhi: string;
};

export type IdentityStatusView = {
  readonly analysisId: string;
  readonly version: string;
  readonly analyzedAt: string;
  readonly confidence: string;
};

export type IdentityDayMasterView = {
  readonly stem: string;
  readonly element: string;
  readonly yinYang: string;
};

export type IdentityHeaderView = {
  readonly person: IdentityPersonView;
  readonly pillars: {
    readonly year: IdentityPillarView;
    readonly month: IdentityPillarView;
    readonly day: IdentityPillarView;
    readonly hour: IdentityPillarView;
  };
  readonly dayMaster: IdentityDayMasterView;
  readonly foundation: IdentityFoundationView;
  readonly status: IdentityStatusView;
};

export type DashboardCardId =
  | "overview"
  | "bazi"
  | "five-elements"
  | "ten-gods"
  | "pattern"
  | "shensha"
  | "luck"
  | "interpretation"
  | "action-plan";

export type DashboardCardSpan = 4 | 6 | 8 | 12;

export type DashboardCardSpec = {
  readonly id: DashboardCardId;
  readonly title: string;
  readonly span: DashboardCardSpan;
};

export type OverviewEvidenceView = {
  readonly label: string;
  readonly value: string;
  readonly key: "day-master" | "strength" | "pattern" | "useful-god" | "temperature";
};

export type OverviewView = {
  readonly title: string;
  readonly subtitle: string;
  readonly insight: string;
  readonly insightSource: string;
  readonly conclusion: string;
  readonly conclusionSource: string;
  readonly identity: readonly OverviewEvidenceView[];
  readonly balance: readonly OverviewEvidenceView[];
};

export type BaziPillarKey = "year" | "month" | "day" | "hour";

export type BaziHiddenStemView = {
  readonly stem: string;
  readonly tenGod: string;
};

export type BaziPillarView = {
  readonly key: BaziPillarKey;
  readonly label: string;
  readonly stem: string;
  readonly stemElement: string;
  readonly stemYinYang: string;
  readonly branch: string;
  readonly branchElement: string;
  readonly napAm: string;
  readonly tenGod: string;
  readonly hiddenStems: readonly BaziHiddenStemView[];
  readonly truongSinh: string;
  readonly isDayMaster: boolean;
};

export type BaziStructureView = {
  readonly title: string;
  readonly available: boolean;
  readonly pillars: readonly BaziPillarView[];
};
