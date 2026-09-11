export const ANALYSIS_TYPES = ["phone_number", "car_plate", "motorcycle_plate"] as const;

export type AnalysisType = (typeof ANALYSIS_TYPES)[number];

export type GoldenPreviewState = {
  analysisType: AnalysisType;
  originalInput: string;
};

export type AnalysisTypeOption = {
  value: AnalysisType;
  label: string;
  support: string;
  fieldLabel: string;
  placeholder: string;
  help: string;
  cta: string;
  emptyMessage: string;
};

export const GOLDEN_PREVIEW_TYPE: AnalysisType = "phone_number";
export const GOLDEN_PREVIEW_INPUT = "0328278786";

export const ANALYSIS_TYPE_COPY: Record<AnalysisType, AnalysisTypeOption> = {
  phone_number: {
    value: "phone_number",
    label: "Số điện thoại",
    support: "Xem cấu trúc năng lượng, tài vận, nguồn tài, dòng tài và năng lượng phần cuối dãy.",
    fieldLabel: "Số điện thoại",
    placeholder: "Ví dụ: 0328278786",
    help: "Nhập đầy đủ số điện thoại đang sử dụng.",
    cta: "PHÂN TÍCH SỐ ĐIỆN THOẠI",
    emptyMessage: "Vui lòng nhập số điện thoại.",
  },
  car_plate: {
    value: "car_plate",
    label: "Biển số ô tô",
    support: "Xem cấu trúc Cát – Hung, tính ổn định, công việc, tài vận và năng lượng kết.",
    fieldLabel: "Biển số ô tô",
    placeholder: "Ví dụ: 30A-123.45",
    help: "Nhập đầy đủ biển số như trên đăng ký hoặc biển xe.",
    cta: "PHÂN TÍCH BIỂN SỐ Ô TÔ",
    emptyMessage: "Vui lòng nhập biển số ô tô.",
  },
  motorcycle_plate: {
    value: "motorcycle_plate",
    label: "Biển số xe máy",
    support: "Phân tích cấu trúc trường khí, mức cân bằng và năng lượng phần cuối biển số.",
    fieldLabel: "Biển số xe máy",
    placeholder: "Ví dụ: 29X1-123.45",
    help: "Nhập đầy đủ biển số xe cần phân tích.",
    cta: "PHÂN TÍCH BIỂN SỐ XE MÁY",
    emptyMessage: "Vui lòng nhập biển số xe máy.",
  },
};

export const ANALYSIS_TYPE_OPTIONS = ANALYSIS_TYPES.map((value) => ANALYSIS_TYPE_COPY[value]);

export const PHONE_FORMAT_ERROR =
  "Số điện thoại chưa đúng định dạng. Vui lòng kiểm tra và nhập lại.";
export const VEHICLE_FORMAT_ERROR =
  "Biển số chưa đúng định dạng. Vui lòng kiểm tra và nhập lại đầy đủ.";
export const MISSING_TYPE_ERROR = "Vui lòng chọn loại số cần phân tích.";

const PHONE_SEPARATORS = /[.\s-]/g;

export function getAnalysisOption(type: AnalysisType): AnalysisTypeOption {
  return ANALYSIS_TYPE_COPY[type];
}

export function isAnalysisType(value: string): value is AnalysisType {
  return (ANALYSIS_TYPES as readonly string[]).includes(value);
}

export function validateCustomerInput(type: AnalysisType | "", raw: string): string | null {
  if (!isAnalysisType(type)) {
    return MISSING_TYPE_ERROR;
  }
  const trimmed = raw.trim();
  if (!trimmed) {
    return ANALYSIS_TYPE_COPY[type].emptyMessage;
  }
  if (type === "phone_number") {
    const compact = trimmed.replace(PHONE_SEPARATORS, "");
    if (!/^\d+$/.test(compact) || !compact.startsWith("0") || compact.length < 9 || compact.length > 11) {
      return PHONE_FORMAT_ERROR;
    }
    return null;
  }
  if (!/[0-9A-Za-z]/.test(trimmed)) {
    return VEHICLE_FORMAT_ERROR;
  }
  return null;
}
