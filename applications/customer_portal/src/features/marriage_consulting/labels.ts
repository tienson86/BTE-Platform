/**
 * Deterministic TV-01 customer labels. Presentation mapping only.
 */

export const PRODUCT_TITLE = "Tư vấn hôn nhân";
export const FAMILY_LABEL = "Tư vấn";
export const PERSON_A_LABEL = "Người A";
export const PERSON_B_LABEL = "Người B";
export const SUBMIT_LABEL = "Phân tích hôn nhân";
export const HERO_EYEBROW = "Tương hợp hôn nhân";

export const OVERALL_STATE_LABEL: Record<string, string> = {
  supportive: "Tương hợp tốt",
  balanced: "Cân bằng",
  mixed: "Vừa có điểm thuận, vừa có điểm cần điều chỉnh",
  pressured: "Có nhiều điểm cần lưu ý",
  critical: "Cần thận trọng",
  insufficient: "Chưa đủ dữ liệu",
};

export const OVERALL_STATE_HEADLINE: Record<string, string> = {
  supportive: "Tương hợp tốt",
  balanced: "Nền tảng tương đối cân bằng",
  mixed: "Hai người vừa có điểm hợp, vừa có điểm cần điều chỉnh",
  pressured: "Có nhiều điểm cần lưu ý",
  critical: "Cần thận trọng với các điểm then chốt",
  insufficient: "Chưa đủ dữ liệu để kết luận tổng thể",
};

export const CONFIDENCE_LABEL: Record<string, string> = {
  high: "Độ tin cậy cao",
  medium: "Khá tin cậy",
  reference_only: "Mang tính tham khảo",
};

export const PRIORITY_LABEL: Record<string, string> = {
  critical: "Then chốt",
  high: "Ưu tiên cao",
  medium: "Nên thực hiện",
  low: "Tham khảo / bổ trợ",
  reference: "Tham khảo / bổ trợ",
};

export const DOMAIN_TITLE: Record<string, string> = {
  five_elements: "Ngũ hành",
  stem_branch: "Can Chi",
  ten_gods: "Thập thần",
  interaction: "Tương tác",
  finance: "Tài chính",
  family: "Gia đình",
  children: "Con cái",
  luck: "Nhịp thời điểm",
  overall: "Tổng thể",
};

export const OPTIONAL_DOMAINS = ["interaction", "family", "children"] as const;

export const CUSTOMER_ERROR: Record<string, string> = {
  VALIDATION_ERROR: "Thiếu thông tin bắt buộc.",
  person_required: "Thiếu thông tin bắt buộc.",
  person_a_gender_required: "Thiếu thông tin bắt buộc.",
  person_b_gender_required: "Thiếu thông tin bắt buộc.",
  person_a_birth_date_required: "Ngày sinh chưa hợp lệ.",
  person_b_birth_date_required: "Ngày sinh chưa hợp lệ.",
  person_a_gender_invalid: "Thiếu thông tin bắt buộc.",
  person_b_gender_invalid: "Thiếu thông tin bắt buộc.",
  NOT_FOUND: "Không tìm thấy hồ sơ tư vấn.",
  CONFLICT: "Yêu cầu chưa thể hoàn tất lúc này.",
  INTERNAL_ERROR: "Không thể hoàn tất phân tích lúc này.",
};

export const FIELD_ERROR = {
  gender: "Vui lòng chọn giới tính.",
  birth_date: "Vui lòng nhập ngày sinh dương lịch.",
};

export const WARNING_NOTE: Record<string, string> = {
  BIRTH_TIME_UNKNOWN:
    "Chưa có giờ sinh. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
  DOMAIN_UNAVAILABLE: "Một số phần chưa đủ dữ liệu để luận riêng.",
  TIMING_UNAVAILABLE: "Phần nhịp thời điểm chưa đủ dữ liệu nên không hiển thị.",
  TIMEZONE_UNSPECIFIED:
    "Múi giờ chưa được ghi nhận. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
};

export const LIMITATION_NOTE: Record<string, string> = {
  birth_time_unknown:
    "Chưa có giờ sinh của một người. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
  timezone_unspecified:
    "Múi giờ chưa được ghi nhận. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
  birth_place_unknown:
    "Nơi sinh chưa được ghi nhận. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
  children_unsupported: "Hiện chưa đủ dữ liệu để kết luận về việc nuôi dạy con chung.",
  insufficient_comparison_evidence:
    "Một số phần so sánh chưa đủ dữ liệu nên được giữ ở mức tham khảo.",
};

export const FORBIDDEN_SCORE_PATTERN = /(?:\d+\s*\/\s*100|\d+\s*%|Grade\s*[A-E]|--\s*\/\s*100)/i;
export const FORBIDDEN_ID_PATTERN = /\b(?:EV-\d{4}|F-\d{4})\b/;
