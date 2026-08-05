# BTE Platform

# Portal Design Philosophy

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On:

- BTE_UI_BIBLE.md

Applies To:

- Portal UI
- Analysis UI
- Future Portal Modules

---

# 1. Purpose

Tài liệu này định nghĩa triết lý thiết kế của Portal BTE.

Nó giải thích:

- Portal là gì.
- Portal không phải là gì.
- Vì sao Information Architecture được tổ chức như hiện tại.
- Vì sao Reading Flow được thiết kế theo thứ tự hiện nay.
- Vì sao từng quyết định UI được đưa ra.

Đây là tài liệu định hướng tư duy.

Không phải tài liệu mô tả Component.

Không phải tài liệu Layout.

Không phải tài liệu CSS.

---

# 2. Portal Is Not A Dashboard

Sai lầm phổ biến nhất khi thiết kế Portal phân tích là biến nó thành Dashboard.

Dashboard tập trung vào:

- Widget
- KPI
- Card
- Chart
- Số liệu

Trong khi Portal BTE tập trung vào:

- Con người
- Quyết định
- Luận giải
- Giải thích
- Hành động

Portal không bán dữ liệu.

Portal bán sự hiểu biết.

---

# 3. Portal Is A Professional Analysis Workspace

Portal BTE là không gian làm việc của một chuyên gia phân tích.

Người dùng không đến để:

- xem thật nhiều số liệu.

Người dùng đến để:

- hiểu bản thân.
- hiểu lá số.
- hiểu nguyên nhân.
- biết điều nên làm.

Toàn bộ thiết kế phải phục vụ mục tiêu này.

---

# 4. Decision Before Details

Portal luôn hiển thị:

Điều quan trọng nhất

↓

Giải thích

↓

Chi tiết

Không bao giờ làm ngược lại.

Ví dụ:

Không hiển thị 10 Thập Thần trước.

Không hiển thị toàn bộ Tứ Trụ trước.

Không hiển thị toàn bộ Thần Sát trước.

Những dữ liệu đó chỉ có ý nghĩa khi người dùng đã hiểu bức tranh tổng thể.

---

# 5. Reading Before Interaction

Portal ưu tiên đọc.

Không ưu tiên thao tác.

Người dùng phải đọc được.

Sau đó mới tương tác.

Điều này khác hoàn toàn Dashboard quản trị.

---

# 6. Identity Is The Entry Point

Mọi quá trình phân tích bắt đầu từ:

"Tôi là ai?"

Do đó:

Identity luôn đứng trước Analysis.

Identity luôn đứng trước Interpretation.

Identity luôn đứng trước Knowledge.

---

# 7. Decision Support

Portal không dừng ở việc hiển thị kết quả.

Portal phải giúp người dùng:

What?

↓

Why?

↓

Next?

Đây là khác biệt lớn nhất giữa BTE và các phần mềm xem lá số truyền thống.

---

# 8. Progressive Disclosure

Không phải toàn bộ kiến thức đều xuất hiện ngay.

Portal tiết lộ thông tin theo từng lớp.

Layer 1

Identity

↓

Layer 2

Condition

↓

Layer 3

Decision

↓

Layer 4

Evidence

↓

Layer 5

Interpretation

↓

Layer 6

Learning

Điều này giúp giảm Cognitive Load.

---

# 9. Information Before Decoration

Thiết kế đẹp không phải mục tiêu.

Thiết kế rõ ràng mới là mục tiêu.

Mọi yếu tố trang trí chỉ tồn tại nếu:

- tăng khả năng đọc.
- tăng khả năng hiểu.

Nếu không,

phải loại bỏ.

---

# 10. Visual Hierarchy Is Business Hierarchy

Kích thước không quyết định mức độ quan trọng.

Mà mức độ quan trọng của nghiệp vụ mới quyết định kích thước.

Ví dụ:

Nhật Chủ

>

Thập Thần

Dụng Thần

>

Metadata

Khuyến nghị

>

Chi tiết kỹ thuật

---

# 11. Information Density

Portal hướng tới:

High Information Density

Low Cognitive Load

Không tạo giao diện:

- quá nhiều khoảng trắng.
- quá nhiều Card.
- quá nhiều vùng trống.

Thông tin phải dày nhưng dễ đọc.

---

# 12. Consistency Across Devices

Desktop

Tablet

Mobile

có thể khác bố cục.

Nhưng:

- Reading Flow
- Decision Flow
- Information Hierarchy

không được thay đổi.

---

# 13. One Portal Language

Toàn bộ Portal phải nói cùng một ngôn ngữ.

Không được tồn tại:

- màn hình kiểu Dashboard.
- màn hình kiểu Report.
- màn hình kiểu Admin.
- màn hình kiểu Spreadsheet.

Người dùng luôn cảm thấy:

"Tôi đang ở cùng một sản phẩm."

---

# 14. Trust Before Beauty

Người dùng tin vào:

- cấu trúc rõ ràng.
- giải thích hợp lý.
- luận giải nhất quán.

Không tin vì:

- màu sắc.
- animation.
- hiệu ứng.

UI phải tạo cảm giác chuyên nghiệp trước khi tạo cảm giác đẹp.

---

# 15. Learning Is Optional

Learning không phải bước bắt buộc.

Người dùng có thể hoàn thành mục tiêu mà không cần mở Learning Panel.

Learning chỉ hỗ trợ:

- tìm hiểu thêm.
- nghiên cứu sâu.
- giải thích thuật ngữ.

---

# 16. AI-Friendly Design

Portal được thiết kế để:

- AI triển khai đúng.
- nhiều lập trình viên cùng phát triển.
- mở rộng lâu dài.

Do đó:

mọi quyết định thiết kế đều phải được mô tả bằng tài liệu.

Không phụ thuộc vào trí nhớ.

---

# 17. Anti-Patterns

Không được:

- Thiết kế theo Dashboard Admin.
- Thiết kế theo báo cáo PDF.
- Thiết kế theo Spreadsheet.
- Thiết kế theo Data Table.
- Thiết kế theo Card Gallery.

Nếu người dùng phải tìm thông tin,

Portal thất bại.

Thông tin quan trọng phải tự xuất hiện đúng thời điểm.

---

# 18. Design Validation

Mọi thiết kế Portal phải trả lời được:

✓ Người dùng biết mình đang xem ai?

✓ Người dùng hiểu kết quả trong 10 giây?

✓ Người dùng biết điều gì quan trọng nhất?

✓ Người dùng biết nên làm gì tiếp?

✓ Người dùng có muốn đọc sâu hơn?

Nếu bất kỳ câu nào trả lời "Không",

thiết kế cần được xem xét lại.

---

# 19. Relationship

Tài liệu này là nền tảng cho:

- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_USER_JOURNEY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- Toàn bộ Screen Blueprints

---

# 20. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Portal Design Philosophy |