# I18N Guide

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Locale: `vi` only for Result V2

---

## 1. Catalog (`vi`)

### Page / CTA

| Key | Value |
|-----|-------|
| i18n.page.loading | Đang chuẩn bị tư vấn |
| i18n.page.offline | Chưa thể kết nối. Thử lại sau. |
| i18n.cta.primary | Bắt đầu theo định hướng này |
| i18n.cta.secondary | Xem sâu sự nghiệp |
| i18n.cta.loading | Đang xử lý |
| i18n.error.page | Không thể hiển thị buổi tư vấn. |
| i18n.error.retry | Thử tải lại buổi tư vấn |
| i18n.error.retry_section | Thử lại phần này |
| i18n.error.back_summary | Quay lại tóm tắt tư vấn |
| i18n.empty.page | Chưa có dữ liệu tư vấn để hiển thị. |
| i18n.empty.recommendations | Chưa có định hướng cụ thể trong buổi này. |
| i18n.empty.domain | Chưa có luận giải cho {domain} trong buổi tư vấn này. |

### Sections

| Key | Value |
|-----|-------|
| i18n.section.summary.title | Tóm tắt tư vấn |
| i18n.section.recommendation.title | Định hướng chính |
| i18n.section.warnings.title | Lưu ý quan trọng |
| i18n.section.charts.title | Biểu đồ minh họa |
| i18n.section.technical.title | Chi tiết kỹ thuật |
| i18n.section.knowledge.title | Kiến thức bổ sung |
| i18n.section.appendix.title | Phụ lục |
| i18n.nav.skip | Đến nội dung tư vấn |

### Fields / expand

| Key | Value |
|-----|-------|
| i18n.field.why | Vì sao |
| i18n.field.expected_result | Kết quả kỳ vọng |
| i18n.field.action | Việc cần làm |
| i18n.expand.more | Xem thêm |
| i18n.expand.less | Thu gọn |
| i18n.expand.analysis | Xem phân tích chi tiết |
| i18n.expand.analysis_less | Thu gọn phân tích |
| i18n.expand.table | Xem bảng số liệu |
| i18n.expand.table_less | Ẩn bảng số liệu |
| i18n.expand.technical | Xem chi tiết kỹ thuật |
| i18n.expand.technical_less | Ẩn chi tiết kỹ thuật |
| i18n.expand.knowledge | Đọc thêm |
| i18n.expand.knowledge_less | Ẩn kiến thức bổ sung |
| i18n.expand.knowledge_item | Đọc tiếp |

### Domain / status / technical labels

| Key | Value |
|-----|-------|
| i18n.domain.career | Sự nghiệp |
| i18n.domain.wealth | Tài chính |
| i18n.domain.relationship | Quan hệ |
| i18n.domain.health | Sức khỏe |
| i18n.domain.luck | Vận trình |
| i18n.status.ready | Sẵn sàng tư vấn |
| i18n.status.partial | Tư vấn một phần |
| i18n.status.in_progress | Đang hoàn thiện |
| i18n.status.error | Không thể hiển thị phần này |
| i18n.technical.calendar | Lịch |
| i18n.technical.pillars | Tứ trụ |
| i18n.technical.timezone | Múi giờ |
| i18n.technical.schema | Phiên bản phân tích |
| i18n.technical.ids | Mã hồ sơ |
| i18n.technical.metadata | Thông tin kỹ thuật bổ sung |

---

## 2. Rules

- Result V2 ships `vi` only  
- No English fallback strings on screen  
- Interpolation `{domain}` uses domain i18n values  
- Do not load i18n from Knowledge packages  

---

## 3. Stop line

This catalog is the chrome SoT for PX-2.

END
