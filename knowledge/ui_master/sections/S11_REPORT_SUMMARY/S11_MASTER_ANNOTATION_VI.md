# BTE Platform

# S11 — BÁO CÁO TỔNG KẾT

# S11_MASTER_ANNOTATION_VI.md

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

S11

Tên

Báo cáo tổng kết

---

# 1. Mục đích

Tài liệu này mô tả ý nghĩa của từng vùng giao diện (Annotation) trong Section S11.

Đây là tài liệu dành cho:

- Product Owner
- UI/UX Designer
- Frontend Developer
- QA Engineer
- Cursor AI

Mục tiêu của tài liệu là giúp mọi thành viên hiểu:

- Vai trò của từng khối giao diện.
- Thứ tự tiếp nhận thông tin của người dùng.
- Ý nghĩa của từng thành phần.
- Quan hệ giữa S11 và toàn bộ Dashboard.

Tài liệu này **không quy định**:

- Grid
- Typography
- CSS
- Design Tokens

Các nội dung trên được quy định tại:

```
S11_MASTER_GRID_VI.md
```

---

# 2. Tổng quan giao diện

```
┌──────────────────────────────────────────────────────┐
│ (A) Header                                           │
├──────────────────────────────────────────────────────┤
│                                                      │
│ (B) Executive Summary Card                           │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ (C) Điểm mạnh                                        │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ (D) Điểm cần lưu ý                                   │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ (E) Khuyến nghị hành động                            │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ (F) Xem báo cáo phân tích đầy đủ →                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Đây là cấu trúc chuẩn của Desktop Canonical UI.

---

# 3. (A) Header

## Vai trò

Hiển thị tên Section.

Ví dụ:

```
S11 — BÁO CÁO TỔNG KẾT
```

Header giúp người dùng nhận biết đây là phần kết luận cuối cùng của toàn bộ báo cáo.

---

## Không dùng để

✗ Hiển thị điểm số

✗ Hiển thị kết quả phân tích

✗ Hiển thị KPI

✗ Hiển thị biểu đồ

---

# 4. (B) Executive Summary Card

## Vai trò

Đây là vùng quan trọng nhất của S11.

Card này phải trả lời ngay:

> **"Tóm lại lá số này như thế nào?"**

Người dùng phải hiểu được bức tranh tổng thể chỉ sau vài giây.

---

## Thành phần

Executive Summary Card gồm:

```
KẾT LUẬN TỔNG QUAN

↓

Đoạn tóm tắt

(4–5 dòng)
```

Ví dụ:

```
KẾT LUẬN TỔNG QUAN

Bạn có nền tảng mệnh cục khá tốt.
Có năng lực phát triển bền vững.
Nên phát huy điểm mạnh và
duy trì sự cân bằng cảm xúc.
```

---

## Vai trò UX

Executive Summary **không lặp lại** nội dung của S08.

Đây là phần:

**Kết luận cuối cùng** của toàn bộ Dashboard.

---

# 5. (C) Điểm mạnh

## Vai trò

Tóm tắt các ưu điểm nổi bật nhất.

Ví dụ:

```
✓ Lãnh đạo

✓ Quyết đoán

✓ Trách nhiệm

✓ Kiên trì
```

---

## Mục tiêu

Người dùng biết:

"Mình nên phát huy điều gì?"

---

## Không dùng để

✗ Phân tích học thuật

✗ Chấm điểm

✗ Giải thích Rule

---

# 6. (D) Điểm cần lưu ý

## Vai trò

Hiển thị những điểm cần cải thiện.

Ví dụ:

```
⚠ Dễ nóng vội

⚠ Thiếu kiên nhẫn

⚠ Cần cân bằng Ngũ hành
```

---

## Mục tiêu

Giúp người dùng nhận biết:

"Mình nên cẩn trọng điều gì?"

---

## Không dùng để

✗ Cảnh báo tiêu cực

✗ Khẳng định tuyệt đối

✗ Nội dung gây lo lắng

---

# 7. (E) Khuyến nghị hành động

## Vai trò

Đây là phần chuyển từ:

**Kết quả**

↓

**Hành động**

Ví dụ:

```
→ Phát triển kỹ năng quản lý.

→ Tăng yếu tố Thủy trong môi trường sống.

→ Lựa chọn hướng làm việc phù hợp.
```

---

## Mục tiêu

Sau khi đọc xong,

người dùng biết:

"Mình nên làm gì tiếp theo."

---

## Không dùng để

✗ Nội dung quảng cáo

✗ Chỉ dẫn mê tín

✗ Cam kết kết quả

---

# 8. (F) Xem báo cáo phân tích đầy đủ

## Vai trò

Điều hướng người dùng sang Report đầy đủ.

Dashboard chỉ cung cấp Executive Summary.

Báo cáo chi tiết sẽ chứa:

- Luận giải đầy đủ
- Dữ liệu chi tiết
- Các phân tích chuyên sâu

---

## Hiển thị

```
Xem báo cáo phân tích đầy đủ →
```

Không Button.

Không Shadow.

Không Card.

---

# 9. Reading Flow

Người dùng phải đọc theo đúng thứ tự:

```
Header

↓

Executive Summary

↓

Điểm mạnh

↓

Điểm cần lưu ý

↓

Khuyến nghị

↓

Xem báo cáo đầy đủ
```

Không thay đổi thứ tự này.

---

# 10. Information Hierarchy

★★★★★

Executive Summary

★★★★★

Kết luận

★★★★☆

Điểm mạnh

★★★★☆

Điểm cần lưu ý

★★★★☆

Khuyến nghị

★★☆☆☆

Footer Link

Executive Summary luôn là điểm nhìn đầu tiên.

---

# 11. Ý nghĩa màu sắc

## Đỏ BTE

- Header
- Tiêu đề Executive Summary
- Footer Link

---

## Xanh

Điểm mạnh

---

## Cam

Điểm cần lưu ý

---

## Xanh dương

Khuyến nghị

---

## Kem nhạt (#FFF8EF)

Executive Summary Card

Màu sắc chỉ hỗ trợ phân nhóm thông tin.

Không thể hiện mức độ tốt/xấu.

---

# 12. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có báo cáo tổng kết.

Vui lòng hoàn thành phân tích trước.
```

Không để Block rỗng.

---

# 13. Relationship

```
Analysis Engine

↓

Interpretation Engine

↓

Report Engine

↓

Executive Summary

↓

S11
```

S11 chỉ hiển thị kết quả cuối cùng.

Không tính toán.

Không suy luận.

---

# 14. User Experience Goal

Sau khi đọc S11,

người dùng phải biết:

✓ Lá số tổng thể như thế nào.

✓ Mình mạnh ở đâu.

✓ Điều gì cần lưu ý.

✓ Hành động ưu tiên là gì.

✓ Muốn xem sâu thì đọc báo cáo đầy đủ.

---

# 15. Mapping với Design Pattern

S11 sử dụng:

- PATTERN_05_DECISION_CARD (Executive Summary)
- PATTERN_06_INFORMATION_LIST
- PATTERN_08_KNOWLEDGE_CARD
- PATTERN_10_REPORT_BLOCK

Không tạo Pattern mới.

---

# 16. Nội dung nghiệp vụ

Executive Summary

↓

Kết luận chung.

---

Điểm mạnh

↓

Những yếu tố nên phát huy.

---

Điểm cần lưu ý

↓

Những yếu tố cần cải thiện.

---

Khuyến nghị

↓

Các hành động ưu tiên.

Bốn nhóm thông tin không được trùng lặp.

---

# 17. QA Review

PASS khi

✓ Executive Summary nổi bật.

✓ Reading Flow tự nhiên.

✓ Không có dữ liệu kỹ thuật.

✓ Không lặp lại nguyên văn S08.

✓ Khuyến nghị rõ ràng.

✓ Dashboard tạo cảm giác "đã hoàn thành phân tích".

---

# 18. Canonical Consistency

S11 phải đồng bộ với:

- S08 — Luận giải tổng hợp.
- S09 — Cung Phi / Quái Mệnh & Nhóm Trạch.
- S10 — Cân Xương Đoán Mệnh.

Tuy nhiên,

S11 là **điểm kết thúc** của toàn bộ Dashboard.

Không tạo thêm một vòng phân tích mới.

---

# 19. Design Decision Record

S11 không được thiết kế như:

- Báo cáo kỹ thuật.
- Bảng dữ liệu.
- Tài liệu học thuật.

S11 là:

```
Executive Closing Report
```

Triết lý:

```
Tổng hợp

↓

Kết luận

↓

Hành động

↓

Điều hướng
```

Người dùng phải cảm thấy:

> "Mình đã hiểu bức tranh tổng thể và biết bước tiếp theo."

---

# 20. Freeze Statement

S11_MASTER_ANNOTATION_VI.md là tài liệu chuẩn mô tả ý nghĩa của từng vùng giao diện trong Section S11.

Tất cả:

- Thiết kế UI
- Ảnh Canonical
- Frontend
- QA Review

đều phải tuân thủ tài liệu này.

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S11_MASTER_ANNOTATION_VI.md là Single Source of Truth cho Annotation của Section S11.**