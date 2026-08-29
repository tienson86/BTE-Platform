# COMMERCIAL DASHBOARD
# 03_PDF_MAPPING
# PRESENTATION MAPPING SPECIFICATION

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Tài liệu này định nghĩa cách Dashboard được ánh xạ sang:

- PDF
- DOCX

Commercial Dashboard là nguồn trình bày duy nhất.

PDF và DOCX không được tự thiết kế nội dung.

Chúng chỉ là hai hình thức xuất bản của cùng một Dashboard.

---

# 2. Triết lý

Dashboard là nguồn.

PDF là bản in.

DOCX là bản chỉnh sửa.

Ba nền tảng phải truyền tải cùng một nội dung.

Không tồn tại ba Report khác nhau.

---

# 3. Kiến trúc

```
Canonical Analysis

↓

Commercial Knowledge

↓

Commercial Composer

↓

Presentation Model

↓

Dashboard

↓

PDF

↓

DOCX
```

Presentation Model là nguồn duy nhất.

PDF không được đọc Engine trực tiếp.

DOCX không được đọc Engine trực tiếp.

---

# 4. Mapping Rules

Mọi thành phần Dashboard đều phải ánh xạ sang PDF.

Không được tạo thêm nội dung trong PDF.

Không được bỏ bớt nội dung nếu Dashboard đã hiển thị.

Dashboard là chuẩn.

---

# 5. Header Mapping

Dashboard

↓

Identity Header

↓

PDF

↓

Trang đầu báo cáo

Hiển thị nguyên cấu trúc.

Không chuyển thành đoạn văn.

---

# 6. Card Mapping

## Overview

↓

Section đầu tiên sau Header.

---

## BaZi

↓

Section Bát Tự.

---

## Five Elements

↓

Section Ngũ Hành.

---

## Ten Gods

↓

Section Thập Thần.

---

## Pattern

↓

Section Mệnh Cục.

---

## ShenSha

↓

Section Thần Sát.

---

## Luck

↓

Section Đại Vận.

---

## Interpretation

↓

Luận giải tổng thể.

---

## Action Plan

↓

Kế hoạch hành động.

---

# 7. Thứ tự

Dashboard

↓

PDF

↓

DOCX

giữ nguyên thứ tự.

Không được:

- đổi vị trí Card;
- đổi Heading;
- đổi trình tự đọc.

---

# 8. Nội dung

PDF không được:

- bổ sung Insight mới;
- bổ sung Khuyến nghị mới;
- thay đổi câu chữ.

Presentation Model quyết định nội dung.

---

# 9. Visual Mapping

Portal

↓

Card

↓

PDF

↓

Section

↓

DOCX

↓

Heading

Card không biến thành bảng.

Card không biến thành đoạn văn dài.

Mỗi Card vẫn giữ cấu trúc riêng.

---

# 10. Không được phép

PDF không được:

- tự render từ Engine;
- gọi Commercial Composer lần hai;
- tự tổng hợp dữ liệu;
- thay đổi ngôn ngữ.

PDF chỉ Render.

---

# 11. Typography

Portal

↓

PDF

↓

DOCX

sử dụng cùng:

- Heading hierarchy
- Card title
- Section title
- Paragraph spacing

Không tạo Style riêng.

---

# 12. Hình ảnh

Nếu Dashboard có:

- Radar
- Timeline
- Gauge

PDF phải hiển thị cùng loại.

Không thay bằng bảng số.

---

# 13. Biểu đồ

Dashboard là chuẩn.

PDF giữ nguyên:

- màu sắc;
- tỷ lệ;
- thứ tự.

Không đổi sang dạng khác.

---

# 14. Responsive

Desktop

↓

PDF

Không thay đổi ý nghĩa.

Chỉ thay đổi bố cục nếu cần.

---

# 15. Acceptance Checklist

□ Dashboard và PDF cùng nội dung.

□ Dashboard và DOCX cùng nội dung.

□ Không Card nào mất khi Export.

□ Không Card nào đổi thứ tự.

□ Không có Insight mới.

□ Không có dữ liệu kỹ thuật.

□ PDF chỉ Render.

□ DOCX chỉ Render.

---

# 16. Mapping Matrix

| Dashboard | PDF | DOCX |
|------------|-----|------|
| Identity Header | Identity Header | Identity Header |
| Overview | Overview | Overview |
| BaZi | BaZi | BaZi |
| Five Elements | Five Elements | Five Elements |
| Ten Gods | Ten Gods | Ten Gods |
| Pattern | Pattern | Pattern |
| ShenSha | ShenSha | ShenSha |
| Luck | Luck | Luck |
| Interpretation | Interpretation | Interpretation |
| Action Plan | Action Plan | Action Plan |

---

# 17. One Source of Truth

Commercial Dashboard là nguồn duy nhất.

PDF và DOCX không được tồn tại như hai hệ thống trình bày độc lập.

Mọi thay đổi giao diện phải bắt đầu từ Dashboard.

Dashboard thay đổi.

↓

Presentation Model thay đổi.

↓

PDF thay đổi.

↓

DOCX thay đổi.

Không làm theo chiều ngược lại.

---

# 18. Change Management

Nếu Dashboard bổ sung Card mới.

PDF và DOCX phải Mapping ngay.

Không được để Dashboard và PDF khác nhau.

Nếu Card bị xóa.

PDF và DOCX cũng phải xóa.

Presentation luôn đồng bộ.

---

# 19. Future Compatibility

Khi mở rộng sang:

- Phong Thủy
- Chọn ngày
- Sim phong thủy
- Mai Hoa

mọi Dashboard đều áp dụng cùng nguyên tắc Mapping này.

Không tạo cơ chế Export riêng cho từng module.

---

# 20. Kết luận

Commercial Dashboard là trung tâm của toàn bộ Presentation Layer.

PDF và DOCX chỉ là hai phương thức xuất bản.

Mọi trải nghiệm người dùng đều bắt đầu từ Dashboard và kết thúc bằng Dashboard.