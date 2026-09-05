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
  readonly available: boolean;
  readonly displayWeight: string;
  readonly weight: string;
  readonly classification: string;
  readonly rating: string;
  readonly summary: string;
  readonly interpretation: string;
  readonly detailHref: string;
};

export type IdentityStatusView = {
  readonly analysisId: string;
  readonly version: string;
  readonly analyzedAt: string;
  readonly confidence: string;
  readonly cungPhi: string;
  readonly menhQuai: string;
  readonly hanhCung: string;
  readonly nhomTrach: string;
  readonly tietKhi: string;
  readonly tamNguyen: string;
  readonly cuuVan: string;
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

export type OverviewEvidenceKey =
  | "day-master"
  | "strength"
  | "pattern"
  | "useful-god"
  | "favorable-god"
  | "avoid-god";

export type OverviewEvidenceView = {
  readonly label: string;
  readonly value: string;
  readonly key: OverviewEvidenceKey;
};

export type OverviewView = {
  readonly title: string;
  readonly subtitle: string;
  readonly insight: string;
  readonly insightSource: string;
  readonly summary: string;
  readonly summarySource: string;
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

export type TenGodCommercialView = {
  readonly name: string;
  readonly pillarLabel: string;
  readonly insight: string;
  readonly capability: string;
  readonly income: string;
  readonly career: string;
  readonly risk: string;
  readonly recommendation: string;
};

export type TenGodCombinationView = {
  readonly title: string;
  readonly members: readonly string[];
  readonly insight: string;
  readonly capability: string;
  readonly income: string;
  readonly career: string;
  readonly leadership: string;
  readonly growth: string;
  readonly risk: string;
  readonly recommendation: string;
};

export type TenGodDetailedView = {
  readonly name: string;
  readonly statusLabel: string;
  readonly roleLabel: string;
  readonly positives: readonly string[];
  readonly risks: readonly string[];
  readonly conditions: readonly string[];
  readonly unresolved: boolean;
  readonly fallback: string;
};

export type TenGodRelationView = {
  readonly name: string;
  readonly stateLabel: string;
  readonly mechanism: string;
  readonly condition: string;
  readonly unresolved: boolean;
  readonly fallback: string;
};

export type TenGodEcosystemRoleView = {
  readonly label: string;
  readonly unresolved: boolean;
};

export type TenGodEcosystemView = {
  readonly unresolved: boolean;
  readonly fallback: string;
  readonly driver: TenGodEcosystemRoleView;
  readonly support: TenGodEcosystemRoleView;
  readonly bottleneck: TenGodEcosystemRoleView;
  readonly blocked: TenGodEcosystemRoleView;
  readonly suppressed: TenGodEcosystemRoleView;
  readonly excessive: TenGodEcosystemRoleView;
  readonly deficient: TenGodEcosystemRoleView;
  readonly missing: TenGodEcosystemRoleView;
  readonly flow: string;
  readonly flowQuality: string;
};

export type TenGodsView = {
  readonly title: string;
  readonly available: boolean;
  readonly featured: readonly string[];
  readonly visible: readonly TenGodsPlacementView[];
  readonly hidden: readonly TenGodsPlacementView[];
  readonly hiddenNames: readonly string[];
  readonly distribution: readonly TenGodsPresenceView[];
  readonly combination: TenGodCombinationView | null;
  readonly hiddenSupport: string;
  readonly commercial: readonly TenGodCommercialView[];
  readonly detailed: readonly TenGodDetailedView[];
  readonly relations: readonly TenGodRelationView[];
  readonly ecosystem: TenGodEcosystemView | null;
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
  readonly purity: string;
  readonly patternStrength: string;
  readonly integrity: string;
  readonly grade: string;
};

export type ShenShaItemView = {
  readonly name: string;
  readonly placement: string;
  readonly meaning: string;
  readonly chartRelevance: string;
  readonly evidence: string;
  readonly category: string;
  readonly stateLabel: string;
  readonly explanation: string;
};

export type ShenShaGroupView = {
  readonly heading: string;
  readonly items: readonly ShenShaItemView[];
};

export type ShenShaClusterView = {
  readonly name: string;
  readonly stateLabel: string;
  readonly explanation: string;
  readonly warning: boolean;
  readonly unresolved: boolean;
};

export type ShenShaEcosystemView = {
  readonly dominant: string;
  readonly dominantUnresolved: boolean;
  readonly supporting: string;
  readonly warning: string;
  readonly unresolvedLabel: string;
  readonly clusters: readonly ShenShaClusterView[];
};

export type ShenShaView = {
  readonly title: string;
  readonly available: boolean;
  readonly grouped: boolean;
  readonly groups: readonly ShenShaGroupView[];
  readonly items: readonly ShenShaItemView[];
  readonly summary: string;
  readonly note: string;
  readonly usePack07: boolean;
  readonly ecosystem: ShenShaEcosystemView | null;
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

export type InterpretationZoneId = "observation" | "reasoning" | "impact" | "recommendation";

export type InterpretationZoneView = {
  readonly id: InterpretationZoneId;
  readonly label: string;
  readonly body: string;
  readonly extra: string;
  readonly source: string;
};

export type InterpretationView = {
  readonly title: string;
  readonly available: boolean;
  readonly lead: string;
  readonly leadExtra: string;
  readonly leadSource: string;
  readonly zones: readonly InterpretationZoneView[];
  readonly closing: string;
  readonly closingSource: string;
  readonly emptyMessage: string;
};

export type ActionItemView = {
  readonly title: string;
  readonly detail: string;
  readonly domain: string;
  readonly source: string;
};

export type ActionPlanView = {
  readonly title: string;
  readonly available: boolean;
  readonly emptyMessage: string;
  readonly priority: ActionItemView | null;
  readonly actions: readonly ActionItemView[];
  readonly extraActions: readonly ActionItemView[];
  readonly warnings: readonly ActionItemView[];
  readonly watch: readonly ActionItemView[];
};

export type LifeDomainId =
  | "marriage"
  | "children"
  | "health"
  | "career"
  | "finance"
  | "property";

export type LifeDomainView = {
  readonly id: LifeDomainId;
  readonly title: string;
  readonly insight: string;
  readonly tendency: string;
  readonly strength: string;
  readonly opportunity: string;
  readonly risk: string;
  readonly recommendation: string;
};

export type LifeConsultingView = {
  readonly title: string;
  readonly available: boolean;
  readonly domains: readonly LifeDomainView[];
};
