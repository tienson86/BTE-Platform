/**
 * BaZi Result mock data (Wave 3 / ADR-006).
 * Presentation-only. Replace with Analysis Engine bindings later.
 */

export type PresentationStatus = "ready" | "loading" | "empty" | "error";

export type BaZiProfile = {
  readonly fullName: string;
  readonly gender: string;
  readonly solarBirthDate: string;
  readonly lunarBirthDate: string;
  readonly birthTime: string;
  readonly birthPlace: string;
};

export type BaZiChartMetadata = {
  readonly chartId: string;
  readonly createdAt: string;
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

export type BaZiResultLabels = {
  readonly pageTitle: string;
  readonly profileHeading: string;
  readonly metadataHeading: string;
  readonly actionsHeading: string;
  readonly pillarsTitle: string;
  readonly fiveElementsTitle: string;
  readonly tenGodsTitle: string;
  readonly strengthTitle: string;
  readonly fieldFullName: string;
  readonly fieldGender: string;
  readonly fieldSolar: string;
  readonly fieldLunar: string;
  readonly fieldBirthTime: string;
  readonly fieldBirthPlace: string;
  readonly fieldCreatedAt: string;
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
};

export const BAZI_RESULT_LABELS: BaZiResultLabels = {
  pageTitle: "Kết Quả Bát Tự",
  profileHeading: "Thông tin người xem",
  metadataHeading: "Thông tin lá số",
  actionsHeading: "Thao tác",
  pillarsTitle: "Tứ Trụ",
  fiveElementsTitle: "Ngũ Hành",
  tenGodsTitle: "Thập Thần",
  strengthTitle: "Thân Vượng Nhược",
  fieldFullName: "Họ tên",
  fieldGender: "Giới tính",
  fieldSolar: "Dương lịch",
  fieldLunar: "Âm lịch",
  fieldBirthTime: "Giờ sinh",
  fieldBirthPlace: "Nơi sinh",
  fieldCreatedAt: "Ngày lập lá số",
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
  engineVersion: "1.0.0",
  ruleDatabaseVersion: "1.0.0",
  interpretationVersion: "1.0.0-ui",
  analysisStatus: "Hoàn tất (mock)",
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
};
