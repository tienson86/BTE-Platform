# BTE Platform

# S09 — HƯỚNG DẪN PHONG THỦY

# S09_MASTER_ANNOTATION_VI.md

---

Phiên bản

1.0.0

Trạng thái

CANONICAL

Ngôn ngữ

Tiếng Việt

Module

Desktop Canonical UI

Section

S09

Tên

Hướng dẫn phong thủy

---

# 1. Mục đích

Tài liệu này mô tả ý nghĩa của từng vùng giao diện (Annotation) trong Section S09.

Đây là tài liệu dành cho:

- Product Owner
- UI/UX Designer
- Frontend Developer
- QA Engineer
- Cursor AI

Mục tiêu là giúp tất cả thành viên trong dự án hiểu:

- Mỗi vùng giao diện dùng để làm gì.
- Người dùng sẽ đọc theo trình tự nào.
- Vai trò của từng khối thông tin.
- Mối liên hệ giữa các khối.

Tài liệu này **không mô tả**:

- Grid
- CSS
- Typography
- Khoảng cách

Các nội dung đó được quy định trong `S09_MASTER_GRID_VI.md`.

---

# 2. Tổng quan giao diện

```
┌────────────────────────────────────────────────────────────┐
│ (A) Header                                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (B) Executive Guidance                                     │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (C) Màu sắc phù hợp                                        │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (D) Ngũ hành nên tăng cường                                │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (E) Hướng phù hợp                                          │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (F) Khuyến nghị bố trí                                     │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (G) Đọc hướng dẫn đầy đủ →                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

Đây là cấu trúc chuẩn của Desktop Canonical.

---

# 3. (A) Header

## Vai trò

Hiển thị tên Section.

Ví dụ

```
S09 — HƯỚNG DẪN PHONG THỦY
```

Đây là điểm bắt đầu của phần ứng dụng phong thủy sau khi người dùng đã hoàn thành việc đọc luận giải tổng hợp.

---

## Không dùng để

✗ Hiển thị điểm số

✗ Hiển thị KPI

✗ Hiển thị thống kê

✗ Hiển thị trạng thái

---

# 4. (B) Executive Guidance

## Vai trò

Đây là vùng quan trọng nhất của S09.

Executive Guidance giúp người dùng hiểu ngay:

```
Tôi nên áp dụng phong thủy theo hướng nào?
```

Đây là phần tổng kết ngắn gọn trước khi đi vào từng nhóm khuyến nghị.

---

## Nội dung

Executive Guidance gồm:

- Tiêu đề
- Một đoạn tổng kết

Khoảng:

60–100 từ.

---

## Không dùng để

✗ Giải thích phong thủy chuyên sâu.

✗ Trình bày lý thuyết.

✗ Hiển thị Rule.

✗ Trích dẫn dữ liệu kỹ thuật.

---

# 5. (C) Màu sắc phù hợp

## Vai trò

Giúp người dùng nhận biết nhanh các màu sắc nên ưu tiên trong cuộc sống hằng ngày.

Ví dụ:

```
✓ Xanh dương

✓ Đen

✓ Trắng
```

---

## Ý nghĩa

Đây là khuyến nghị mang tính ứng dụng.

Không phải quy định bắt buộc.

---

# 6. (D) Ngũ hành nên tăng cường

## Vai trò

Hiển thị các hành nên bổ sung nhằm hỗ trợ cân bằng mệnh cục.

Ví dụ

```
✓ Thủy

✓ Kim
```

---

## Mục tiêu

Người dùng hiểu:

```
Nên tăng cường yếu tố nào?
```

Không trình bày nguyên lý sinh khắc.

---

# 7. (E) Hướng phù hợp

## Vai trò

Hiển thị các phương hướng phù hợp theo kết quả phân tích.

Ví dụ

```
✓ Bắc

✓ Tây Bắc

✓ Tây
```

---

## Không dùng để

✗ Thay thế tư vấn phong thủy nhà ở.

✗ Xác định vị trí cụ thể.

✗ Phân tích mặt bằng.

---

# 8. (F) Khuyến nghị bố trí

## Vai trò

Đưa ra các gợi ý đơn giản, dễ áp dụng.

Ví dụ

```
• Tăng ánh sáng tự nhiên

• Giữ không gian gọn gàng

• Bổ sung yếu tố nước

• Hạn chế màu nóng
```

---

## Mục tiêu

Giúp người dùng có thể áp dụng ngay mà không cần kiến thức phong thủy chuyên sâu.

---

# 9. (G) Đọc hướng dẫn đầy đủ

## Vai trò

Điều hướng tới màn hình hướng dẫn phong thủy chi tiết.

Dashboard chỉ hiển thị phần tóm tắt.

Report sẽ hiển thị đầy đủ.

---

## Hiển thị

```
Đọc hướng dẫn đầy đủ →
```

Không Button.

Không nền.

Không Icon lớn.

---

# 10. Reading Flow

Người dùng sẽ đọc theo đúng trình tự:

```
Header

↓

Executive Guidance

↓

Màu sắc phù hợp

↓

Ngũ hành nên tăng cường

↓

Hướng phù hợp

↓

Khuyến nghị bố trí

↓

Đọc hướng dẫn đầy đủ
```

Đây là Reading Flow duy nhất.

---

# 11. Information Hierarchy

★★★★★

Executive Guidance

★★★★☆

Màu sắc phù hợp

★★★★☆

Ngũ hành nên tăng cường

★★★★☆

Hướng phù hợp

★★★★☆

Khuyến nghị bố trí

★★☆☆☆

Liên kết

Executive Guidance luôn là điểm nhìn đầu tiên.

---

# 12. Ý nghĩa màu sắc

## Đỏ BTE

Header

Liên kết

---

## Xanh lá

Thông tin nên ưu tiên.

---

## Xanh dương

Thông tin định hướng.

---

## Neutral

Nội dung mô tả.

---

Màu sắc chỉ hỗ trợ nhận biết.

Không phải tín hiệu duy nhất.

---

# 13. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có hướng dẫn phong thủy.

Vui lòng hoàn thành phân tích trước.
```

Không để khoảng trắng.

---

# 14. Relationship

```
Analysis Engine

↓

Interpretation Engine

↓

Feng Shui Guidance Engine

↓

S09
```

S09 không thực hiện tính toán.

Chỉ trình bày dữ liệu đã được tổng hợp.

---

# 15. User Experience Goal

Sau khi đọc S09, người dùng phải biết:

✓ Nên dùng màu gì.

✓ Nên tăng cường hành nào.

✓ Nên ưu tiên hướng nào.

✓ Có thể áp dụng điều gì ngay hôm nay.

Nếu người dùng vẫn phải đọc báo cáo mới hiểu thì S09 chưa đạt mục tiêu.

---

# 16. Design Decision Record

S09 không được thiết kế như một tài liệu phong thủy chuyên sâu.

S09 là một **Executive Guidance Card**.

Triết lý thiết kế:

```
Executive Guidance

↓

Color

↓

Element

↓

Direction

↓

Layout Advice

↓

Full Guidance
```

Điều này giúp người dùng:

- Hiểu nhanh.
- Áp dụng nhanh.
- Không bị quá tải thông tin.

---

# 17. Mapping với Design Pattern

S09 sử dụng:

- PATTERN_06_INFORMATION_LIST
- PATTERN_07_STATUS_PANEL
- PATTERN_10_REPORT_BLOCK

Đảm bảo đồng bộ với toàn bộ Desktop Canonical UI.

---

# 18. QA Review

Một bản triển khai chỉ được coi là đạt khi:

✓ Executive Guidance nổi bật nhất.

✓ Các nhóm thông tin rõ ràng.

✓ Reading Flow tự nhiên.

✓ Không xuất hiện dữ liệu kỹ thuật.

✓ Có liên kết tới hướng dẫn chi tiết.

✓ Không có thành phần ngoài phạm vi V1.

---

# 19. Freeze Statement

S09_MASTER_ANNOTATION_VI.md là tài liệu chuẩn mô tả ý nghĩa của từng vùng giao diện trong Section S09.

Tất cả:

- Thiết kế UI
- Ảnh Canonical
- Frontend
- QA Review

đều phải tuân thủ tài liệu này.

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S09_MASTER_ANNOTATION_VI.md là Single Source of Truth cho Annotation của Section S09.**