export const PRODUCT_TITLE = "Tư vấn hợp tác làm ăn & nghề nghiệp";
export const FAMILY_LABEL = "Tư vấn";
export const PERSON_A_LABEL = "Đối tác A";
export const PERSON_B_LABEL = "Đối tác B";
export const SUBMIT_LABEL = "Phân tích hợp tác";
export const HERO_EYEBROW = "Tương hợp hợp tác";

export const FIELD_ERROR = {
  gender: "Vui lòng chọn giới tính.",
  birth_date: "Vui lòng nhập ngày sinh dương lịch.",
  occupation: "Vui lòng chọn ngành/nghề dự định hợp tác.",
};

export const GENDER_OPTIONS = [
  { value: "", label: "Chọn giới tính" },
  { value: "male", label: "Nam" },
  { value: "female", label: "Nữ" },
] as const;

export const OCCUPATION_OPTIONS = [
  { value: "", label: "Chọn ngành/nghề hợp tác" },
  { value: "retail", label: "Kinh doanh bán lẻ" },
  { value: "ecommerce", label: "Thương mại điện tử" },
  { value: "real_estate", label: "Bất động sản" },
  { value: "finance_investment", label: "Tài chính - đầu tư" },
  { value: "fnb", label: "Nhà hàng - F&B" },
  { value: "manufacturing", label: "Sản xuất" },
  { value: "construction_interior", label: "Xây dựng - nội thất" },
  { value: "technology", label: "Công nghệ - phần mềm" },
  { value: "marketing_media", label: "Marketing - truyền thông" },
  { value: "education_training", label: "Giáo dục - đào tạo" },
  { value: "healthcare", label: "Y tế - chăm sóc sức khỏe" },
  { value: "beauty_spa", label: "Làm đẹp - spa" },
  { value: "logistics", label: "Logistics - vận tải" },
  { value: "agriculture_food", label: "Nông nghiệp - thực phẩm" },
  { value: "consulting_services", label: "Dịch vụ tư vấn" },
  { value: "creative", label: "Nghệ thuật - sáng tạo" },
  { value: "other", label: "Khác" },
] as const;

export function occupationLabel(value: string): string {
  if (!value) return "";
  return OCCUPATION_OPTIONS.find((item) => item.value === value)?.label || "";
}
