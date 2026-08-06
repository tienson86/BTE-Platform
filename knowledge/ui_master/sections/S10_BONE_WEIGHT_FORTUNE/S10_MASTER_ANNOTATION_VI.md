# BTE Platform

# S10 — CÂN XƯƠNG ĐOÁN MỆNH

# S10_MASTER_ANNOTATION_VI.md

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

S10

Tên

Cân Xương Đoán Mệnh

---

# 1. Mục đích

Tài liệu này mô tả ý nghĩa của từng vùng giao diện (Annotation) trong Section S10.

Đây là tài liệu dành cho:

- Product Owner
- UI/UX Designer
- Frontend Developer
- QA Engineer
- Cursor AI

Mục tiêu giúp toàn bộ nhóm phát triển hiểu:

- Vai trò của từng khối giao diện.
- Trình tự người dùng tiếp nhận thông tin.
- Ý nghĩa của từng thành phần.
- Quan hệ giữa giao diện và Bone Weight Fortune Engine.

Tài liệu này **không quy định**:

- Grid
- Typography
- CSS
- Spacing

Các nội dung này được định nghĩa trong:

```
S10_MASTER_GRID_VI.md
```

---

# 2. Tổng quan giao diện

```
┌────────────────────────────────────────────────────────────┐
│ (A) Header                                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (B) Decision Card                                          │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (C) Bài ca cân xương                                       │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (D) Luận giải                                              │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ (E) Đọc luận giải đầy đủ →                                 │
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
S10 — CÂN XƯƠNG ĐOÁN MỆNH
```

Header giúp người dùng nhận biết đây là phần kết quả của hệ thống Cân Xương Đoán Mệnh.

---

## Không dùng để

✗ Hiển thị lượng.

✗ Hiển thị đánh giá.

✗ Hiển thị Rule.

✗ Hiển thị KPI.

---

# 4. (B) Decision Card

## Vai trò

Đây là vùng quan trọng nhất của S10.

Decision Card phải trả lời ngay:

```
Tôi được bao nhiêu lượng?

Mức đánh giá là gì?
```

Đây là phần người dùng nhìn đầu tiên.

---

## Thành phần

Decision Card gồm:

```
★★★★★

↓

Tổng lượng

↓

Mức đánh giá

↓

Nhận định ngắn
```

Ví dụ

```
★★★★★

4 LƯỢNG 3 CHỈ

MỆNH TỐT

Thuộc nhóm có hậu vận ổn định.
```

---

## Ý nghĩa

Không phải điểm số.

Không phải KPI.

Đây là kết quả cuối cùng của Bone Weight Fortune Engine.

---

# 5. (C) Bài ca cân xương

## Vai trò

Hiển thị nguyên văn bài ca tương ứng với tổng lượng.

Ví dụ

```
📜 BÀI CA CÂN XƯƠNG

Thân mang phúc khí trời ban,

Công danh thuận lợi,

Gia đạo bình an...
```

---

## Mục tiêu

Người dùng đọc được nguyên văn bài ca truyền thống.

Không phân tích.

Không giải thích.

Không rút gọn.

---

# 6. (D) Luận giải

## Vai trò

Diễn giải ý nghĩa của bài ca bằng ngôn ngữ hiện đại.

Ví dụ

```
📖 LUẬN GIẢI

Bạn là người có số mệnh khá tốt.

Trung vận thuận lợi.

Hậu vận ổn định...
```

---

## Mục tiêu

Giúp người dùng:

Hiểu ý nghĩa.

Không cần tự diễn giải thơ.

---

## Không dùng để

✗ Giải thích từng câu thơ.

✗ Phân tích học thuật.

✗ Trình bày thuật toán.

---

# 7. (E) Đọc luận giải đầy đủ

## Vai trò

Điều hướng tới báo cáo Cân Xương Đoán Mệnh chi tiết.

Dashboard chỉ hiển thị:

Executive Summary.

Report hiển thị đầy đủ.

---

## Hiển thị

```
Đọc luận giải đầy đủ →
```

Không Button.

Không nền.

Không Shadow.

---

# 8. Reading Flow

Người dùng phải đọc theo:

```
Header

↓

Decision Card

↓

Bài ca

↓

Luận giải

↓

Đọc đầy đủ
```

Đây là Reading Flow chuẩn.

---

# 9. Information Hierarchy

★★★★★

Decision Card

★★★★★

Tổng lượng

★★★★☆

Bài ca

★★★★☆

Luận giải

★★☆☆☆

Liên kết

Decision Card luôn nổi bật nhất.

---

# 10. Ý nghĩa màu sắc

## Đỏ BTE

Header

Tổng lượng

Footer Link

---

## Neutral Dark

Mức đánh giá

---

## Neutral

Nhận định

Luận giải

---

## Kem nhạt (#FFF8EF)

Decision Card

Màu sắc chỉ hỗ trợ nhận biết.

Không mang ý nghĩa tốt/xấu.

---

# 11. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có kết quả Cân Xương Đoán Mệnh.

Vui lòng hoàn thành phân tích trước.
```

Không để Card trống.

---

# 12. Relationship

```
Ngày sinh

↓

Bone Weight Fortune Engine

↓

BoneWeightResult

↓

S10
```

S10 không thực hiện tính toán.

Chỉ hiển thị dữ liệu.

---

# 13. User Experience Goal

Sau khi đọc S10, người dùng phải biết:

✓ Tổng lượng.

✓ Mức đánh giá.

✓ Nội dung bài ca.

✓ Ý nghĩa tổng quát.

Nếu người dùng phải tự tra bảng cân xương thì S10 chưa đạt mục tiêu.

---

# 14. Design Decision Record

S10 không được thiết kế như:

- Bảng tra lượng.
- Công cụ tính.
- Tài liệu học thuật.

S10 là:

```
Executive Bone Weight Fortune Card
```

Triết lý:

```
Kết quả

↓

Ý nghĩa

↓

Chi tiết
```

---

# 15. Mapping với Design Pattern

S10 sử dụng:

- PATTERN_05_DECISION_CARD
- PATTERN_08_KNOWLEDGE_CARD
- PATTERN_10_REPORT_BLOCK

Không sử dụng Pattern khác.

---

# 16. QA Review

PASS khi

✓ Decision Card nổi bật.

✓ Tổng lượng dễ nhìn.

✓ Bài ca dễ đọc.

✓ Luận giải dễ hiểu.

✓ Reading Flow tự nhiên.

✓ Không có dữ liệu kỹ thuật.

---

# 17. Nội dung nghiệp vụ

Decision Card phản ánh:

- Tổng lượng.
- Mức đánh giá.

Bài ca phản ánh:

- Văn bản truyền thống.

Luận giải phản ánh:

- Giải thích hiện đại.

Ba phần không được trùng lặp nội dung.

---

# 18. Canonical Consistency

S10 phải đồng bộ với:

- S08 — Luận giải tổng hợp.
- S09 — Cung Phi / Quái Mệnh & Nhóm Trạch.

Tuy nhiên,

S10 có Decision Card là điểm nhấn chính thay vì Executive Summary.

---

# 19. Freeze Statement

S10_MASTER_ANNOTATION_VI.md là tài liệu chuẩn mô tả ý nghĩa của từng vùng giao diện trong Section S10.

Tất cả:

- Thiết kế UI
- Ảnh Canonical
- Frontend
- QA Review

đều phải tuân thủ tài liệu này.

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S10_MASTER_ANNOTATION_VI.md là Single Source of Truth cho Annotation của Section S10.**