/**
 * BaZi Result ViewModel types + mock fixture (Canonical UI / ADR-006).
 * Presentation only — no API / Engine coupling until Sprint 01.5 after UI Freeze.
 */

export type PresentationStatus = "ready" | "loading" | "empty" | "error";

export type BaZiProfile = {
  readonly fullName: string;
  readonly gender: string;
  readonly solarBirthDate: string;
  readonly lunarBirthDate: string;
  readonly birthTime: string;
  readonly birthPlace: string;
  /** Profile.Avatar — optional; initials used when absent. */
  readonly avatarUrl?: string;
};

export type BaZiChartMetadata = {
  readonly chartId: string;
  readonly createdAt: string;
  /** When analysis last completed (S00). */
  readonly analyzedAt: string;
  readonly engineVersion: string;
  readonly ruleDatabaseVersion: string;
  readonly interpretationVersion: string;
  readonly analysisStatus: string;
};

export type BaZiQuickAction = {
  readonly id: string;
  readonly label: string;
  readonly ariaLabel: string;
  readonly enabled: boolean;
};

export type PillarKind = "year" | "month" | "day" | "hour";

export type BaZiPillar = {
  readonly kind: PillarKind;
  readonly label: string;
  readonly heavenlyStem: string;
  readonly earthlyBranch: string;
  readonly hiddenStems: readonly string[];
  readonly naYin: string;
  readonly twelveStage: string;
};

export type FiveElementId = "kim" | "moc" | "thuy" | "hoa" | "tho";

export type BaZiFiveElement = {
  readonly id: FiveElementId;
  readonly name: string;
  readonly score: number;
  readonly percentage: number;
  readonly strength: string;
};

export type BaZiTenGod = {
  readonly id: string;
  readonly name: string;
  readonly count: number;
  readonly score: number;
  readonly strength: string;
  readonly descriptionPreview: string;
};

export type BaZiStrength = {
  readonly score: number;
  readonly maxScore: number;
  readonly label: string;
  readonly level: string;
  readonly confidence: number;
  readonly summary: string;
};

export type BaZiExecutiveMetric = {
  readonly id: string;
  readonly label: string;
  readonly value: string;
  readonly hint: string;
};

export type BaZiSpiritRole = "dung" | "hy" | "ky";

export type BaZiSpiritGod = {
  readonly id: string;
  readonly role: BaZiSpiritRole;
  readonly roleLabel: string;
  readonly name: string;
  readonly element: string;
};

export type BaZiExecutiveSummary = {
  readonly title: string;
  readonly verdict: string;
  readonly level: string;
  readonly confidence: number;
  readonly summary: string;
  readonly highlights: readonly string[];
  readonly metrics: readonly BaZiExecutiveMetric[];
  /** Hero — Nhật Chủ stem (largest signal). */
  readonly dayMaster: string;
  readonly dayMasterHint: string;
  readonly element: string;
  readonly elementHint: string;
  readonly yinYang: string;
  readonly yinYangHint: string;
  /** Display value for Thân — avoid duplicating exact Strength badge text. */
  readonly strengthGlance: string;
  readonly strengthHint: string;
  readonly dungThan: string;
  readonly hyThan: string;
  readonly kyThan: string;
  readonly pattern: string;
  readonly overallGrade: string;
  readonly recommendation: string;
};

export type BaZiShenShaItem = {
  readonly id: string;
  readonly name: string;
  readonly tone: string;
  readonly note: string;
  readonly present: boolean;
};

export type BaZiInterpretationBlock = {
  readonly title: string;
  readonly paragraphs: readonly string[];
};

export type BaZiKnowledgeItem = {
  readonly id: string;
  readonly title: string;
  readonly reference: string;
};

export type BaZiResultLabels = {
  readonly pageTitle: string;
  readonly contextTitle: string;
  readonly contextProfilePrefix: string;
  readonly contextChartPrefix: string;
  readonly contextAnalysisPrefix: string;
  readonly contextDetailLink: string;
  readonly contextReanalyzeLink: string;
  readonly executiveTitle: string;
  readonly overviewTitle: string;
  readonly profileHeading: string;
  readonly metadataHeading: string;
  readonly actionsHeading: string;
  readonly pillarsTitle: string;
  readonly fiveElementsTitle: string;
  readonly tenGodsTitle: string;
  readonly strengthTitle: string;
  readonly shenShaTitle: string;
  readonly interpretationTitle: string;
  readonly knowledgeTitle: string;
  readonly fieldFullName: string;
  readonly fieldGender: string;
  readonly fieldSolar: string;
  readonly fieldLunar: string;
  readonly fieldBirthTime: string;
  readonly fieldBirthPlace: string;
  readonly fieldBirthSummary: string;
  readonly fieldCreatedAt: string;
  readonly fieldAnalyzedAt: string;
  readonly fieldAnalysisVersion: string;
  readonly fieldEngine: string;
  readonly fieldRules: string;
  readonly fieldInterpretation: string;
  readonly fieldChartId: string;
  readonly stem: string;
  readonly branch: string;
  readonly hidden: string;
  readonly naYin: string;
  readonly twelveStage: string;
  readonly score: string;
  readonly confidence: string;
  readonly summary: string;
  readonly level: string;
  readonly distributionSummary: string;
  readonly dayMaster: string;
};

export const BAZI_RESULT_LABELS: BaZiResultLabels = {
  pageTitle: "Kết Quả Bát Tự",
  contextTitle: "Ngữ cảnh lá số",
  contextProfilePrefix: "Hồ sơ",
  contextChartPrefix: "Mã",
  contextAnalysisPrefix: "Phân tích",
  contextDetailLink: "Chi tiết hồ sơ",
  contextReanalyzeLink: "Phân tích lại",
  executiveTitle: "Tóm Tắt Điều Hành",
  overviewTitle: "Tổng Quan Lá Số",
  profileHeading: "Thông tin người xem",
  metadataHeading: "Thông tin lá số",
  actionsHeading: "Thao tác",
  pillarsTitle: "Tứ Trụ",
  fiveElementsTitle: "Ngũ Hành",
  tenGodsTitle: "Thập Thần",
  strengthTitle: "Thân Vượng Nhược",
  shenShaTitle: "Thần Sát",
  interpretationTitle: "Luận Giải",
  knowledgeTitle: "Tri Thức",
  fieldFullName: "Họ tên",
  fieldGender: "Giới tính",
  fieldSolar: "Dương lịch",
  fieldLunar: "Âm lịch",
  fieldBirthTime: "Giờ sinh",
  fieldBirthPlace: "Nơi sinh",
  fieldBirthSummary: "Ngày giờ sinh",
  fieldCreatedAt: "Ngày lập lá số",
  fieldAnalyzedAt: "Thời điểm phân tích",
  fieldAnalysisVersion: "Phiên bản phân tích",
  fieldEngine: "Engine Version",
  fieldRules: "Rule Database Version",
  fieldInterpretation: "Interpretation Version",
  fieldChartId: "Mã lá số",
  stem: "Thiên Can",
  branch: "Địa Chi",
  hidden: "Tàng Can",
  naYin: "Nạp Âm",
  twelveStage: "Trường Sinh",
  score: "Điểm tổng",
  confidence: "Độ tin cậy",
  summary: "Mô tả ngắn",
  level: "Mức độ",
  distributionSummary: "Phân bố tổng quan",
  dayMaster: "Nhật Chủ",
};

export const BAZI_MOCK_PROFILE: BaZiProfile = {
  fullName: "Nguyễn Văn Minh",
  gender: "Nam",
  solarBirthDate: "15/08/1990",
  lunarBirthDate: "25/06/Canh Ngọ",
  birthTime: "09:30",
  birthPlace: "Hà Nội, Việt Nam",
};

export const BAZI_MOCK_METADATA: BaZiChartMetadata = {
  chartId: "BZ-2026-0805-001",
  createdAt: "05/08/2026 14:22",
  analyzedAt: "05/08/2026 14:28",
  engineVersion: "1.0.0",
  ruleDatabaseVersion: "1.0.0",
  interpretationVersion: "1.0.0",
  analysisStatus: "Đã phân tích",
};

export const BAZI_MOCK_ACTIONS: readonly BaZiQuickAction[] = [
  {
    id: "pdf",
    label: "Xuất PDF",
    ariaLabel: "Xuất PDF — chưa khả dụng",
    enabled: false,
  },
  {
    id: "print",
    label: "In",
    ariaLabel: "In — chưa khả dụng",
    enabled: false,
  },
  {
    id: "share",
    label: "Chia sẻ",
    ariaLabel: "Chia sẻ — chưa khả dụng",
    enabled: false,
  },
  {
    id: "reanalyze",
    label: "Phân tích lại",
    ariaLabel: "Phân tích lại — chưa khả dụng",
    enabled: false,
  },
] as const;

export const BAZI_MOCK_PILLARS: readonly BaZiPillar[] = [
  {
    kind: "year",
    label: "Năm",
    heavenlyStem: "Canh",
    earthlyBranch: "Ngọ",
    hiddenStems: ["Đinh", "Kỷ"],
    naYin: "Lộ Bàng Thổ (placeholder)",
    twelveStage: "Đế Vượng (placeholder)",
  },
  {
    kind: "month",
    label: "Tháng",
    heavenlyStem: "Giáp",
    earthlyBranch: "Thân",
    hiddenStems: ["Canh", "Nhâm", "Tuất"],
    naYin: "Đại Khê Thủy (placeholder)",
    twelveStage: "Bệnh (placeholder)",
  },
  {
    kind: "day",
    label: "Ngày",
    heavenlyStem: "Bính",
    earthlyBranch: "Dần",
    hiddenStems: ["Giáp", "Bính", "Tuất"],
    naYin: "Furnace Fire (placeholder)",
    twelveStage: "Trường Sinh (placeholder)",
  },
  {
    kind: "hour",
    label: "Giờ",
    heavenlyStem: "Ất",
    earthlyBranch: "Tỵ",
    hiddenStems: ["Bính", "Canh", "Tuất"],
    naYin: "Tuyền Trung Thủy (placeholder)",
    twelveStage: "Quan Đới (placeholder)",
  },
] as const;

export const BAZI_MOCK_FIVE_ELEMENTS: readonly BaZiFiveElement[] = [
  { id: "kim", name: "Kim", score: 18, percentage: 18, strength: "Trung bình" },
  { id: "moc", name: "Mộc", score: 22, percentage: 22, strength: "Khá" },
  { id: "thuy", name: "Thủy", score: 15, percentage: 15, strength: "Yếu" },
  { id: "hoa", name: "Hỏa", score: 28, percentage: 28, strength: "Mạnh" },
  { id: "tho", name: "Thổ", score: 17, percentage: 17, strength: "Trung bình" },
] as const;

export const BAZI_MOCK_TEN_GODS: readonly BaZiTenGod[] = [
  {
    id: "zheng-guan",
    name: "Chính Quan",
    count: 2,
    score: 72,
    strength: "Mạnh",
    descriptionPreview: "Quản lý, kỷ luật, trách nhiệm.",
  },
  {
    id: "pian-guan",
    name: "Thiên Quan",
    count: 1,
    score: 48,
    strength: "Trung bình",
    descriptionPreview: "Áp lực, quyết đoán, cạnh tranh.",
  },
  {
    id: "zheng-yin",
    name: "Chính Ấn",
    count: 2,
    score: 80,
    strength: "Mạnh",
    descriptionPreview: "Học vấn, chỗ dựa, trí tuệ.",
  },
  {
    id: "pian-yin",
    name: "Thiên Ấn",
    count: 1,
    score: 55,
    strength: "Trung bình",
    descriptionPreview: "Tư duy độc lập, nghiên cứu.",
  },
  {
    id: "bi-jian",
    name: "Tỷ Kiên",
    count: 1,
    score: 60,
    strength: "Khá",
    descriptionPreview: "Đồng loại, tự lực, ngang hàng.",
  },
  {
    id: "jie-cai",
    name: "Kiếp Tài",
    count: 1,
    score: 42,
    strength: "Yếu",
    descriptionPreview: "Chia sẻ, cạnh tranh tài nguyên.",
  },
  {
    id: "shi-shen",
    name: "Thực Thần",
    count: 2,
    score: 68,
    strength: "Khá",
    descriptionPreview: "Sáng tạo, biểu đạt, tài năng.",
  },
  {
    id: "shang-guan",
    name: "Thương Quan",
    count: 1,
    score: 35,
    strength: "Yếu",
    descriptionPreview: "Phá cách, đổi mới, phản kháng.",
  },
  {
    id: "zheng-cai",
    name: "Chính Tài",
    count: 2,
    score: 70,
    strength: "Mạnh",
    descriptionPreview: "Tài chính ổn định, trách nhiệm.",
  },
  {
    id: "pian-cai",
    name: "Thiên Tài",
    count: 1,
    score: 52,
    strength: "Trung bình",
    descriptionPreview: "Cơ hội, đầu tư, biến động.",
  },
] as const;

export const BAZI_MOCK_STRENGTH: BaZiStrength = {
  score: 82,
  maxScore: 100,
  label: "THÂN VƯỢNG",
  level: "Mạnh",
  confidence: 98,
  summary:
    "Thân được mùa sinh, có nhiều trợ lực, khả năng tự lập cao. (mock — chưa tính từ Engine)",
};

/** Same displayed facts as Strength / Pillars — Canonical Executive Hero. */
export const BAZI_MOCK_EXECUTIVE: BaZiExecutiveSummary = {
  title: "Tóm Tắt Điều Hành",
  verdict: BAZI_MOCK_STRENGTH.label,
  level: BAZI_MOCK_STRENGTH.level,
  confidence: BAZI_MOCK_STRENGTH.confidence,
  summary: BAZI_MOCK_STRENGTH.summary,
  highlights: [
    `Nhật Chủ: ${BAZI_MOCK_PILLARS[2].heavenlyStem} ${BAZI_MOCK_PILLARS[2].earthlyBranch}`,
    `Ngũ Hành nổi bật: Hỏa ${BAZI_MOCK_FIVE_ELEMENTS[3].percentage}%`,
    `Thập Thần mạnh: Chính Ấn, Chính Quan, Chính Tài`,
  ],
  metrics: [
    {
      id: "day-master",
      label: "Nhật Chủ",
      value: BAZI_MOCK_PILLARS[2].heavenlyStem,
      hint: "Hỏa · Dương",
    },
    {
      id: "day-element",
      label: "Ngũ Hành Nhật Chủ",
      value: "Hỏa",
      hint: "Dương Hỏa",
    },
    {
      id: "yin-yang",
      label: "Âm Dương",
      value: "Dương",
      hint: BAZI_MOCK_PROFILE.gender === "Nam" ? "Dương Nam" : "Dương",
    },
    {
      id: "bone-weight",
      label: "Cân Xương Đoán Mệnh",
      value: "4 lượng 8 chỉ",
      hint: "★★★★★ (mock)",
    },
  ],
  dayMaster: BAZI_MOCK_PILLARS[2].heavenlyStem,
  dayMasterHint: "Hỏa · Dương",
  element: "Hỏa",
  elementHint: "Dương Hỏa",
  yinYang: "Dương",
  yinYangHint: BAZI_MOCK_PROFILE.gender === "Nam" ? "Dương Nam" : "Dương",
  strengthGlance: `${BAZI_MOCK_STRENGTH.level} · ${BAZI_MOCK_STRENGTH.score}/${BAZI_MOCK_STRENGTH.maxScore}`,
  strengthHint: "Thân được mùa sinh (mock)",
  dungThan: "Thủy",
  hyThan: "Kim",
  kyThan: "Hỏa",
  pattern: "Chính Tài",
  overallGrade: "B+",
  recommendation: "Ưu tiên bổ Thủy, hạn chế Hỏa quá vượng. (mock — chờ Interpretation)",
};

/** Core analysis spirit gods — presentation mock (Canonical Level 3). */
export const BAZI_MOCK_SPIRIT_GODS: readonly BaZiSpiritGod[] = [
  {
    id: "dung-thuy",
    role: "dung",
    roleLabel: "Dụng Thần",
    name: "Thủy",
    element: "thuy",
  },
  {
    id: "ky-kim",
    role: "ky",
    roleLabel: "Kỵ Thần",
    name: "Kim",
    element: "kim",
  },
  {
    id: "ky-hoa",
    role: "ky",
    roleLabel: "Kỵ Thần",
    name: "Hỏa",
    element: "hoa",
  },
] as const;

export const BAZI_MOCK_SHEN_SHA: readonly BaZiShenShaItem[] = [
  {
    id: "ss-thien-at",
    name: "Thiên Ất Quý Nhân",
    tone: "Cát",
    note: "Placeholder — chờ Rule Database.",
    present: true,
  },
  {
    id: "ss-hoa-cai",
    name: "Hoa Cái",
    tone: "Trung",
    note: "Placeholder — chưa tính từ Engine.",
    present: true,
  },
  {
    id: "ss-van-xuong",
    name: "Văn Xương",
    tone: "Cát",
    note: "Placeholder.",
    present: false,
  },
  {
    id: "ss-dao-hoa",
    name: "Đào Hoa",
    tone: "Trung",
    note: "Placeholder.",
    present: false,
  },
  {
    id: "ss-dich-ma",
    name: "Dịch Mã",
    tone: "Trung",
    note: "Placeholder.",
    present: true,
  },
  {
    id: "ss-hong-loan",
    name: "Hồng Loan",
    tone: "Cát",
    note: "Placeholder.",
    present: false,
  },
] as const;

export const BAZI_MOCK_INTERPRETATION: BaZiInterpretationBlock = {
  title: "Luận Giải",
  paragraphs: [
    BAZI_MOCK_STRENGTH.summary,
    "Chính Ấn và Chính Quan xuất hiện rõ — thiên về học vấn, kỷ luật và trách nhiệm. (mock)",
    "Nội dung luận giải đầy đủ sẽ được nối Interpretation Engine sau khi Portal UI được phê duyệt.",
  ],
};

export const BAZI_MOCK_KNOWLEDGE: readonly BaZiKnowledgeItem[] = [
  {
    id: "kn-1",
    title: "Cơ sở Nhật Chủ",
    reference: "Knowledge Pack — Fundamental Theory (liên kết sau UI Freeze)",
  },
  {
    id: "kn-2",
    title: "Thân Vượng / Thân Nhược",
    reference: "Knowledge Pack — Strength Theory (liên kết sau UI Freeze)",
  },
] as const;

export type BaZiResultMockBundle = {
  readonly status: PresentationStatus;
  readonly errorMessage?: string;
  readonly labels: BaZiResultLabels;
  readonly profile: BaZiProfile;
  readonly metadata: BaZiChartMetadata;
  readonly actions: readonly BaZiQuickAction[];
  readonly pillars: readonly BaZiPillar[];
  readonly fiveElements: readonly BaZiFiveElement[];
  readonly tenGods: readonly BaZiTenGod[];
  readonly strength: BaZiStrength;
  readonly executive: BaZiExecutiveSummary;
  readonly spiritGods: readonly BaZiSpiritGod[];
  readonly shenSha: readonly BaZiShenShaItem[];
  readonly interpretation: BaZiInterpretationBlock;
  readonly knowledge: readonly BaZiKnowledgeItem[];
};

export const BAZI_RESULT_MOCK: BaZiResultMockBundle = {
  status: "ready",
  labels: BAZI_RESULT_LABELS,
  profile: BAZI_MOCK_PROFILE,
  metadata: BAZI_MOCK_METADATA,
  actions: BAZI_MOCK_ACTIONS,
  pillars: BAZI_MOCK_PILLARS,
  fiveElements: BAZI_MOCK_FIVE_ELEMENTS,
  tenGods: BAZI_MOCK_TEN_GODS,
  strength: BAZI_MOCK_STRENGTH,
  executive: BAZI_MOCK_EXECUTIVE,
  spiritGods: BAZI_MOCK_SPIRIT_GODS,
  shenSha: BAZI_MOCK_SHEN_SHA,
  interpretation: BAZI_MOCK_INTERPRETATION,
  knowledge: BAZI_MOCK_KNOWLEDGE,
};

/** Build executive tier from existing result facts (no new business data). */
export function buildExecutiveFromResult(input: {
  readonly strength: BaZiStrength;
  readonly pillars: readonly BaZiPillar[];
  readonly fiveElements: readonly BaZiFiveElement[];
  readonly tenGods: readonly BaZiTenGod[];
  readonly gender?: string;
  readonly yinYang?: string;
  readonly dungThan?: string;
  readonly hyThan?: string;
  readonly kyThan?: string;
  readonly pattern?: string;
  readonly overallGrade?: string;
  readonly recommendation?: string;
}): BaZiExecutiveSummary {
  const day = input.pillars.find((p) => p.kind === "day");
  const topElement = [...input.fiveElements].sort(
    (a, b) => b.percentage - a.percentage,
  )[0];
  const topGods = [...input.tenGods]
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map((g) => g.name)
    .join(", ");
  const stem = day?.heavenlyStem ?? "—";
  const unavailable = "Chưa đủ dữ liệu để đưa ra kết luận.";
  const dungThan = input.dungThan?.trim() || unavailable;
  const hyThan = input.hyThan?.trim() || unavailable;
  const kyThan = input.kyThan?.trim() || unavailable;
  const pattern = input.pattern?.trim() || unavailable;
  const overallGrade = input.overallGrade?.trim() || unavailable;
  const recommendation = input.recommendation?.trim() || unavailable;
  const yinYang = input.yinYang?.trim() || "—";

  return {
    title: BAZI_RESULT_LABELS.executiveTitle,
    verdict: input.strength.label,
    level: input.strength.level,
    confidence: input.strength.confidence,
    summary: input.strength.summary || unavailable,
    highlights: [
      day ? `Nhật Chủ: ${day.heavenlyStem} ${day.earthlyBranch}` : "Nhật Chủ: —",
      topElement
        ? `Ngũ Hành nổi bật: ${topElement.name} ${topElement.percentage}%`
        : "Ngũ Hành: —",
      topGods ? `Thập Thần mạnh: ${topGods}` : "Thập Thần: —",
    ],
    metrics: [
      {
        id: "day-master",
        label: "Nhật Chủ",
        value: stem,
        hint: topElement ? `${topElement.name}` : "—",
      },
      {
        id: "day-element",
        label: "Ngũ Hành Nhật Chủ",
        value: topElement?.name ?? "—",
        hint: topElement?.strength ?? "—",
      },
      {
        id: "yin-yang",
        label: "Âm Dương",
        value: yinYang,
        hint: input.gender ?? "—",
      },
      {
        id: "bone-weight",
        label: "Cân Xương Đoán Mệnh",
        value: "—",
        hint: unavailable,
      },
    ],
    dayMaster: stem,
    dayMasterHint: topElement ? `${topElement.name}` : "—",
    element: topElement?.name ?? "—",
    elementHint: topElement?.strength ?? "—",
    yinYang,
    yinYangHint: input.gender ?? "—",
    strengthGlance: `${input.strength.level} · ${input.strength.score}/${input.strength.maxScore}`,
    strengthHint: input.strength.summary || unavailable,
    dungThan,
    hyThan,
    kyThan,
    pattern,
    overallGrade,
    recommendation,
  };
}
