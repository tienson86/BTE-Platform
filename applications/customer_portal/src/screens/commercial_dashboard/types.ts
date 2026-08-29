/**
 * UI-03 Commercial Dashboard view models. Presentation only.
 */

export type IdentityPillarView = {
  readonly stem: string;
  readonly branch: string;
  readonly canChi: string;
  readonly napAm: string;
  readonly cungPhi: string;
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

export type FiveElementKey = "wood" | "fire" | "earth" | "metal" | "water";

export type FiveElementRowView = {
  readonly key: FiveElementKey;
  readonly label: string;
  readonly count: number | null;
};

export type FiveElementsView = {
  readonly title: string;
  readonly available: boolean;
  readonly sectionHeading: string;
  readonly balanceStatus: string;
  readonly rows: readonly FiveElementRowView[];
  readonly mostPresent: string;
  readonly leastPresent: string;
  readonly comment: string;
};

export type TenGodsPillarKey = "year" | "month" | "day" | "hour";

export type TenGodsPlacementView = {
  readonly pillar: TenGodsPillarKey;
  readonly pillarLabel: string;
  readonly stem: string;
  readonly tenGod: string;
  readonly isDayMaster: boolean;
};

export type TenGodsPresenceView = {
  readonly name: string;
  readonly visible: boolean;
  readonly hidden: boolean;
};

export type TenGodsView = {
  readonly title: string;
  readonly available: boolean;
  readonly featured: readonly string[];
  readonly visible: readonly TenGodsPlacementView[];
  readonly hidden: readonly TenGodsPlacementView[];
  readonly hiddenNames: readonly string[];
  readonly distribution: readonly TenGodsPresenceView[];
  readonly summary: string;
};

export type PatternView = {
  readonly title: string;
  readonly available: boolean;
  readonly primary: string;
  readonly status: string;
  readonly secondary: string;
  readonly formation: readonly string[];
  readonly summary: string;
};

export type ShenShaItemView = {
  readonly name: string;
  readonly placement: string;
  readonly meaning: string;
  readonly category: string;
};

export type ShenShaGroupView = {
  readonly heading: string;
  readonly items: readonly ShenShaItemView[];
};

export type ShenShaView = {
  readonly title: string;
  readonly available: boolean;
  readonly grouped: boolean;
  readonly groups: readonly ShenShaGroupView[];
  readonly items: readonly ShenShaItemView[];
  readonly summary: string;
  readonly note: string;
};

export type LuckCycleView = {
  readonly ganZhi: string;
  readonly yearRange: string;
  readonly ageRange: string;
  readonly isCurrent: boolean;
};

export type LuckView = {
  readonly title: string;
  readonly available: boolean;
  readonly current: LuckCycleView | null;
  readonly direction: string;
  readonly startAge: string;
  readonly cycles: readonly LuckCycleView[];
  readonly next: LuckCycleView | null;
  readonly trend: string;
};
