# BTE Platform

# S07 — THẦN SÁT

# S07_MASTER_ANNOTATION_VI.md

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

S07

Tên

Thần Sát

---

# 1. Mục đích

Tài liệu này mô tả ý nghĩa của từng vùng giao diện (Annotation) trong Section S07.

Đây là tài liệu để:

- Designer
- Frontend
- Cursor
- QA
- Product Owner

hiểu được:

- từng vùng dùng để làm gì;
- người dùng sẽ đọc như thế nào;
- mỗi thành phần có vai trò gì.

Tài liệu này **không mô tả Layout**.

Tài liệu này **không mô tả Grid**.

---

# 2. Tổng quan giao diện

```
┌──────────────────────────────────────────────┐
│                  (A) Header                   │
├──────────────────────────────────────────────┤
│             (B) CÁT TINH (5)                 │
│                                              │
│ ✓ Thiên Ất Quý Nhân                          │
│ ✓ Thiên Đức Quý Nhân                         │
│ ✓ Nguyệt Đức Quý Nhân                        │
│ ✓ Văn Xương                                  │
│ ✓ Hoa Cái                                    │
├──────────────────────────────────────────────┤
│            (C) HUNG TINH (5)                │
│                                              │
│ ✕ Kiếp Sát                                  │
│ ✕ Không Vong                                │
│ ✕ Cô Thần                                   │
│ ✕ Quả Tú                                    │
│ ✕ Đại Hao                                   │
├──────────────────────────────────────────────┤
│        (D) Tóm tắt nhanh                     │
├──────────────────────────────────────────────┤
│      (E) Xem toàn bộ →                       │
└──────────────────────────────────────────────┘
```

---

# 3. (A) Header

## Vai trò

Hiển thị tên Section.

Ví dụ

```
S07 — THẦN SÁT
```

Header giúp người dùng biết:

"Tôi đang xem nhóm thông tin nào."

---

## Không dùng để

✗ Hiển thị thống kê

✗ Hiển thị điểm số

✗ Hiển thị biểu tượng lớn

---

# 4. (B) Khối CÁT TINH

## Vai trò

Hiển thị toàn bộ các Thần Sát mang ý nghĩa hỗ trợ.

Đây là vùng người dùng sẽ nhìn đầu tiên sau Header.

---

## Người dùng cần hiểu ngay

```
Có bao nhiêu Cát tinh?

↓

Là những Cát tinh nào?
```

---

## Thành phần

```
Tiêu đề

↓

Danh sách
```

Không có thêm cấp thông tin.

---

## Ví dụ

```
🟢 CÁT TINH (5)

✓ Thiên Ất Quý Nhân

✓ Thiên Đức Quý Nhân

✓ Nguyệt Đức Quý Nhân

✓ Văn Xương

✓ Hoa Cái
```

---

# 5. (C) Khối HUNG TINH

## Vai trò

Hiển thị các Thần Sát cần lưu ý.

Không nhằm gây lo lắng.

Không đánh giá tốt xấu tuyệt đối.

---

## Người dùng cần hiểu

```
Có những Hung tinh nào?

↓

Có cần xem kỹ không?
```

---

## Ví dụ

```
🔴 HUNG TINH (5)

✕ Kiếp Sát

✕ Không Vong

✕ Cô Thần

✕ Quả Tú

✕ Đại Hao
```

---

# 6. (D) Tóm tắt nhanh

## Vai trò

Đây là Executive Summary.

Không phải luận giải.

Ví dụ

```
Có 5 Cát tinh và 5 Hung tinh.

Nên xem chi tiết để đánh giá mức độ ảnh hưởng.
```

---

## Mục tiêu

Người dùng không cần đếm.

Hệ thống đếm giúp.

---

# 7. (E) Xem toàn bộ

## Vai trò

Điều hướng tới màn hình:

Chi tiết Thần Sát.

Không mở Popup.

Không mở Tooltip.

Không dùng Button lớn.

---

## Ví dụ

```
Xem toàn bộ →
```

---

# 8. Reading Flow

Người dùng sẽ đọc theo thứ tự

```
Header

↓

Cát tinh

↓

Hung tinh

↓

Tóm tắt

↓

Xem toàn bộ
```

Không có luồng đọc khác.

---

# 9. Information Hierarchy

★★★★★

Header

★★★★☆

Cát tinh

★★★★☆

Hung tinh

★★★☆☆

Tóm tắt

★★☆☆☆

Liên kết

---

# 10. Ý nghĩa màu sắc

## Xanh lá

Thể hiện:

Thông tin hỗ trợ.

Không đồng nghĩa:

100% tốt.

---

## Đỏ

Thể hiện:

Thông tin cần chú ý.

Không đồng nghĩa:

100% xấu.

---

## Xám

Thông tin trung tính.

---

# 11. Ý nghĩa biểu tượng

```
✓
```

Có mặt.

Đã kích hoạt.

---

```
✕

```

Có mặt.

Thuộc nhóm cần lưu ý.

Không biểu thị lỗi.

---

# 12. Empty State

Nếu không có Cát tinh

↓

```
Không phát hiện Cát tinh nổi bật.
```

---

Nếu không có Hung tinh

↓

```
Không phát hiện Hung tinh nổi bật.
```

Không để khoảng trắng.

---

# 13. Danh sách dài

Nếu số lượng lớn hơn giới hạn

↓

Hiển thị thanh cuộn nội bộ.

Không tăng chiều cao Card.

---

# 14. Không hiển thị

S07 không hiển thị

✗ Điều kiện kích hoạt

✗ Công thức

✗ Điểm số

✗ AI Score

✗ Rule ID

✗ JSON

✗ Debug

---

# 15. Relationship

Nguồn dữ liệu

```
Rule Engine

↓

ShenSha Engine

↓

S07
```

S07 chỉ đọc dữ liệu.

Không tính toán.

---

# 16. User Experience Goal

Trong vòng

5 giây

người dùng phải biết

✓ Có bao nhiêu Cát tinh.

✓ Có bao nhiêu Hung tinh.

✓ Tên các Thần Sát nổi bật.

Nếu chưa đạt điều này

↓

Thiết kế chưa đạt.

---

# 17. QA Checklist

PASS khi

✓ Header rõ ràng.

✓ Hai nhóm phân biệt dễ nhìn.

✓ Không phải tự đếm.

✓ Không có biểu đồ.

✓ Không có KPI.

✓ Không có Progress Bar.

✓ Không có Dashboard.

✓ Đọc được trên màn hình 1920×1080.

---

# 18. Design Decision Record

S07 không được thiết kế theo kiểu:

Danh sách 100 Thần Sát.

Lý do:

Người dùng phổ thông không quan tâm toàn bộ cơ sở dữ liệu.

Người dùng quan tâm:

- Điều gì đang hỗ trợ mình?
- Điều gì cần lưu ý?

Vì vậy S07 tổ chức dữ liệu theo **ngữ nghĩa (Semantic Grouping)** thay vì theo **kỹ thuật (Technical Listing)**.

Đây là một quyết định thiết kế cốt lõi của BTE Platform.

---

# 19. Mapping

S07 sử dụng:

- PATTERN_06_INFORMATION_LIST
- PATTERN_07_STATUS_PANEL

Sau khi người dùng xem S07, hệ thống sẽ chuyển sang:

S08 — Luận giải tổng hợp.

---

# 20. Freeze Statement

S07_MASTER_ANNOTATION_VI.md là tài liệu chuẩn mô tả ý nghĩa của từng vùng giao diện trong Section S07.

Mọi bản thiết kế, ảnh chuẩn và mã nguồn phải tuân thủ tài liệu này.

Nếu có khác biệt giữa giao diện triển khai và tài liệu thì:

**S07_MASTER_ANNOTATION_VI.md là Single Source of Truth cho Annotation của S07.**