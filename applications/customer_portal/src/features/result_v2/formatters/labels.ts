/**
 * Vietnamese chrome catalog — PX-2 I18N_GUIDE.
 */

import type { ChromeModel, DomainKey, HeroStatus } from "../adapter/PortalResultModel";

export const I18N_VI = {
  "i18n.page.loading": "Đang chuẩn bị tư vấn",
  "i18n.page.offline": "Chưa thể kết nối. Thử lại sau.",
  "i18n.cta.primary": "Bắt đầu theo định hướng này",
  "i18n.cta.secondary": "Xem sâu sự nghiệp",
  "i18n.cta.loading": "Đang xử lý",
  "i18n.error.page": "Không thể hiển thị buổi tư vấn.",
  "i18n.error.retry": "Thử tải lại buổi tư vấn",
  "i18n.error.retry_section": "Thử lại phần này",
  "i18n.error.back_summary": "Quay lại tóm tắt tư vấn",
  "i18n.empty.page": "Chưa có dữ liệu tư vấn để hiển thị.",
  "i18n.empty.recommendations": "Chưa có định hướng cụ thể trong buổi này.",
  "i18n.empty.domain": "Chưa có luận giải cho {domain} trong buổi tư vấn này.",
  "i18n.section.summary.title": "Tóm tắt tư vấn",
  "i18n.section.recommendation.title": "Định hướng chính",
  "i18n.section.warnings.title": "Lưu ý quan trọng",
  "i18n.section.charts.title": "Biểu đồ minh họa",
  "i18n.section.technical.title": "Chi tiết kỹ thuật",
  "i18n.section.knowledge.title": "Kiến thức bổ sung",
  "i18n.section.appendix.title": "Phụ lục",
  "i18n.nav.skip": "Đến nội dung tư vấn",
  "i18n.field.why": "Vì sao",
  "i18n.field.expected_result": "Kết quả kỳ vọng",
  "i18n.field.action": "Việc cần làm",
  "i18n.expand.more": "Xem thêm",
  "i18n.expand.less": "Thu gọn",
  "i18n.expand.analysis": "Xem phân tích chi tiết",
  "i18n.expand.analysis_less": "Thu gọn phân tích",
  "i18n.expand.table": "Xem bảng số liệu",
  "i18n.expand.table_less": "Ẩn bảng số liệu",
  "i18n.expand.technical": "Xem chi tiết kỹ thuật",
  "i18n.expand.technical_less": "Ẩn chi tiết kỹ thuật",
  "i18n.expand.knowledge": "Đọc thêm",
  "i18n.expand.knowledge_less": "Ẩn kiến thức bổ sung",
  "i18n.expand.knowledge_item": "Đọc tiếp",
  "i18n.domain.career": "Sự nghiệp",
  "i18n.domain.wealth": "Tài chính",
  "i18n.domain.relationship": "Quan hệ",
  "i18n.domain.health": "Sức khỏe",
  "i18n.domain.luck": "Vận trình",
  "i18n.status.ready": "Sẵn sàng tư vấn",
  "i18n.status.partial": "Tư vấn một phần",
  "i18n.status.in_progress": "Đang hoàn thiện",
  "i18n.status.error": "Không thể hiển thị phần này",
  "i18n.technical.calendar": "Lịch",
  "i18n.technical.pillars": "Tứ trụ",
  "i18n.technical.timezone": "Múi giờ",
  "i18n.technical.schema": "Phiên bản phân tích",
  "i18n.technical.ids": "Mã hồ sơ",
  "i18n.technical.metadata": "Thông tin kỹ thuật bổ sung",
} as const;

export function t(key: keyof typeof I18N_VI): string {
  return I18N_VI[key];
}

export function domainLabel(key: DomainKey): string {
  return t(`i18n.domain.${key}`);
}

export function interpolateDomain(template: string, key: DomainKey): string {
  return template.replace("{domain}", domainLabel(key));
}

export function statusLabel(status: HeroStatus): string {
  if (status === "partial") return t("i18n.status.partial");
  if (status === "in_progress") return t("i18n.status.in_progress");
  if (status === "error") return t("i18n.status.error");
  return t("i18n.status.ready");
}

export function buildChrome(): ChromeModel {
  return {
    skip: t("i18n.nav.skip"),
    page_loading: t("i18n.page.loading"),
    page_offline: t("i18n.page.offline"),
    cta_loading: t("i18n.cta.loading"),
    error_page: t("i18n.error.page"),
    error_retry: t("i18n.error.retry"),
    error_retry_section: t("i18n.error.retry_section"),
    error_back_summary: t("i18n.error.back_summary"),
    empty_page: t("i18n.empty.page"),
    empty_recommendations: t("i18n.empty.recommendations"),
    empty_domain: t("i18n.empty.domain"),
    section_summary: t("i18n.section.summary.title"),
    section_recommendation: t("i18n.section.recommendation.title"),
    section_warnings: t("i18n.section.warnings.title"),
    section_charts: t("i18n.section.charts.title"),
    section_technical: t("i18n.section.technical.title"),
    section_knowledge: t("i18n.section.knowledge.title"),
    section_appendix: t("i18n.section.appendix.title"),
    field_why: t("i18n.field.why"),
    field_expected_result: t("i18n.field.expected_result"),
    field_action: t("i18n.field.action"),
    expand_more: t("i18n.expand.more"),
    expand_less: t("i18n.expand.less"),
    expand_analysis: t("i18n.expand.analysis"),
    expand_analysis_less: t("i18n.expand.analysis_less"),
    expand_table: t("i18n.expand.table"),
    expand_table_less: t("i18n.expand.table_less"),
    expand_technical: t("i18n.expand.technical"),
    expand_technical_less: t("i18n.expand.technical_less"),
    expand_knowledge: t("i18n.expand.knowledge"),
    expand_knowledge_less: t("i18n.expand.knowledge_less"),
    expand_knowledge_item: t("i18n.expand.knowledge_item"),
    technical_calendar: t("i18n.technical.calendar"),
    technical_pillars: t("i18n.technical.pillars"),
    technical_timezone: t("i18n.technical.timezone"),
    technical_schema: t("i18n.technical.schema"),
    technical_ids: t("i18n.technical.ids"),
    technical_metadata: t("i18n.technical.metadata"),
  };
}
