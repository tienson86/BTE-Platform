import type { PurposeContext } from "./types";

export const PRODUCT_TITLE = "Năng lượng số";
export const SYSTEM_NAME = "Bát Cực Linh Số";
export const SUBMIT_LABEL = "Phân tích";
export const EMPTY_HINT =
  "Nhập dãy số, chọn ngữ cảnh sử dụng, rồi chọn Phân tích. Kết quả chỉ theo hệ thống Bát Cực Linh Số / Năng lượng số.";
export const INTRO =
  "Xem trường khí của dãy số điện thoại, biển số, số định danh, số tài khoản hoặc số nhà theo hệ thống Bát Cực Linh Số.";
export const LOADING_LABEL = "Đang phân tích dãy số…";
export const RETRY_LABEL = "Thử lại";
export const EMPTY_NUMBER_ERROR = "Vui lòng nhập dãy số.";
export const NON_DIGIT_ERROR = "Dãy số chỉ gồm chữ số 0–9.";
export const TOO_LONG_ERROR = "Dãy số vượt quá độ dài cho phép trong V1.";
export const INVALID_CONTEXT_ERROR = "Ngữ cảnh sử dụng chưa được khóa trong V1.";
export const VALIDATION_FALLBACK = "Dữ liệu chưa hợp lệ.";
export const SERVER_FALLBACK = "Không thể hoàn tất phân tích lúc này.";
export const NO_OCCURRENCES = "Không có trường khí Du Niên được khóa cho dãy này trong V1.";
export const NO_PATTERNS = "Không có mẫu đặc biệt được khóa cho dãy này.";
export const STRENGTHS_HEADING = "Mặt hỗ trợ";
export const WATCHOUTS_HEADING = "Mặt cần kiểm soát";

/** Keep in sync with engines.number_energy.constants.MAX_INPUT_DIGITS. */
export const MAX_NUMBER_DIGITS = 128;

export const PURPOSE_LABELS: Record<PurposeContext, string> = {
  generic_number: "Dãy số thông thường",
  phone_number: "Số điện thoại",
  car_plate: "Biển số xe hơi",
  motorbike_plate: "Biển số xe máy",
  id_number: "Số định danh",
  bank_account: "Số tài khoản",
  house_number: "Số nhà",
};

export const FORBIDDEN_PHRASES = [
  "chắc chắn gây bệnh",
  "chắc chắn phá sản",
  "chắc chắn ly hôn",
  "chẩn đoán bệnh",
] as const;
