# BTE Platform

# S07 — THẦN SÁT

# S07_REVIEW_CHECKLIST.md

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

Tài liệu này là Checklist chính thức để đánh giá chất lượng giao diện S07 trước khi Freeze.

Checklist này được sử dụng bởi:

- Product Owner
- UI Designer
- Frontend Developer
- QA Engineer
- Cursor AI

Chỉ khi toàn bộ Checklist đạt PASS thì S07 mới được phép chuyển sang trạng thái **FROZEN**.

---

# 2. Quy trình Review

Quy trình Review luôn thực hiện theo đúng thứ tự sau:

```
README

↓

MASTER_LAYOUT

↓

MASTER_GRID_VI

↓

MASTER_ANNOTATION_VI

↓

Frontend

↓

Screenshot

↓

Review

↓

Freeze
```

Không được bỏ qua bất kỳ bước nào.

---

# 3. Kiểm tra Header

## PASS nếu

☐ Hiển thị đúng:

```
S07 — THẦN SÁT
```

☐ Font đúng Design System

☐ Màu đúng BTE Red

☐ Không có Icon dư

☐ Không có Badge

☐ Không có thống kê trên Header

---

# 4. Kiểm tra Executive Summary

## PASS nếu

☐ Có dòng tổng quan

Ví dụ

```
Có 10 Thần Sát được kích hoạt

5 Cát tinh • 5 Hung tinh
```

☐ Không quá 2 dòng

☐ Dễ đọc

☐ Không giống Dashboard KPI

---

# 5. Kiểm tra nhóm CÁT TINH

## PASS nếu

☐ Tiêu đề rõ ràng

☐ Có hiển thị số lượng

Ví dụ

```
🟢 CÁT TINH (5)
```

☐ Icon màu xanh

☐ Danh sách căn trái

☐ Không có Badge

☐ Không có Progress

☐ Không có Pie Chart

☐ Không có KPI

---

# 6. Kiểm tra Item Cát tinh

## PASS nếu

☐ Mỗi dòng chỉ chứa:

```
✓

Tên Thần Sát
```

☐ Không xuống quá 2 dòng

☐ Không bị cắt chữ

☐ Khoảng cách đều nhau

☐ Không lệch hàng

---

# 7. Kiểm tra nhóm HUNG TINH

## PASS nếu

☐ Tiêu đề rõ ràng

☐ Có số lượng

Ví dụ

```
🔴 HUNG TINH (5)
```

☐ Icon đỏ

☐ Không dùng màu khác

☐ Danh sách căn trái

---

# 8. Kiểm tra Item Hung tinh

## PASS nếu

☐ Chỉ gồm

```
✕

Tên
```

☐ Không quá 2 dòng

☐ Không lệch

☐ Không có Badge

☐ Không có Tooltip

---

# 9. Kiểm tra Divider

## PASS nếu

☐ Divider đúng vị trí

☐ Độ dày 1 px

☐ Không quá đậm

☐ Khoảng cách đúng Grid

---

# 10. Kiểm tra Footer Summary

## PASS nếu

☐ Có Summary

☐ Không quá 2 dòng

☐ Nội dung ngắn gọn

☐ Không luận giải

Ví dụ

```
Có 5 Cát tinh và 5 Hung tinh.

Nên xem chi tiết để đánh giá mức độ ảnh hưởng.
```

---

# 11. Kiểm tra Link

## PASS nếu

☐ Có đúng

```
Xem toàn bộ →
```

☐ Không dùng Button

☐ Không có nền

☐ Không có Shadow

☐ Căn giữa

☐ Hover đúng chuẩn

---

# 12. Kiểm tra White Space

## PASS nếu

☐ Padding đều

☐ Header cách Body đúng

☐ Divider đúng khoảng cách

☐ Footer đúng khoảng cách

☐ Không bị dồn

☐ Không bị thừa khoảng trắng

---

# 13. Kiểm tra Typography

## PASS nếu

☐ Header 16 px

☐ Group Title 13 px

☐ Item 14 px

☐ Summary 13 px

☐ Link 14 px

☐ Không sai Font Weight

---

# 14. Kiểm tra Semantic Color

## PASS nếu

☐ Xanh chỉ dùng cho Cát tinh

☐ Đỏ chỉ dùng cho Hung tinh

☐ Neutral đúng Design System

☐ Không dùng màu ngẫu nhiên

---

# 15. Kiểm tra Reading Flow

Người dùng phải đọc theo:

```
Header

↓

Executive Summary

↓

Cát tinh

↓

Hung tinh

↓

Footer

↓

Xem toàn bộ
```

## PASS nếu

☐ Không bị đảo thứ tự

☐ Không bị phân tán ánh nhìn

---

# 16. Kiểm tra Responsive

## Desktop

☐ Không cuộn

☐ Không vỡ Grid

---

## Tablet

☐ Không tràn

☐ Không lệch

---

## Mobile

☐ Danh sách vẫn dễ đọc

☐ Không phải cuộn ngang

---

# 17. Kiểm tra Accessibility

## PASS nếu

☐ Contrast đạt WCAG AA

☐ Icon không phải tín hiệu duy nhất

☐ Có Label đầy đủ

☐ Keyboard Focus hoạt động

---

# 18. Kiểm tra Data

## PASS nếu

☐ Không Hardcode Logic

☐ Chỉ đọc dữ liệu từ

```
ShenShaResult
```

☐ Không tính toán trên UI

---

# 19. Kiểm tra Performance

## PASS nếu

☐ Render nhanh

☐ Không Animation

☐ Không Lag

☐ Không Scroll bất thường

---

# 20. Kiểm tra Design Principles

## PASS nếu

☐ Recognition > Reading

☐ Grouping > Listing

☐ Summary > Detail

☐ Knowledge > Decoration

☐ Enterprise UI

---

# 21. Kiểm tra Pattern

## PASS nếu

☐ Đúng PATTERN_06_INFORMATION_LIST

☐ Đúng PATTERN_07_STATUS_PANEL

☐ Không vi phạm Design System

---

# 22. Kiểm tra Canonical

So sánh với:

```
S07_CANONICAL.png
```

## PASS nếu

☐ Layout giống

☐ Grid giống

☐ Typography giống

☐ White Space giống

☐ Reading Flow giống

---

# 23. Kiểm tra Screenshot

Screenshot bắt buộc

```
01_s07_only.png
```

## PASS nếu

☐ Chỉ hiển thị S07

☐ Không crop lỗi

☐ Độ phân giải chuẩn

☐ Không che nội dung

---

# 24. Điều kiện Freeze

S07 chỉ được Freeze khi:

☐ README PASS

☐ MASTER_LAYOUT PASS

☐ MASTER_GRID_VI PASS

☐ MASTER_ANNOTATION_VI PASS

☐ Screenshot PASS

☐ Product Owner duyệt

☐ Không còn Issue mức Critical

---

# 25. Design Decision Record

Checklist này không chỉ kiểm tra giao diện đẹp hay xấu.

Checklist đánh giá:

- Khả năng đọc nhanh.
- Khả năng nhận biết.
- Khả năng mở rộng.
- Tính nhất quán với Design System.
- Khả năng tái sử dụng.

Một Section chỉ được coi là hoàn thành khi đáp ứng đầy đủ cả 5 tiêu chí trên.

---

# 26. Freeze Statement

S07_REVIEW_CHECKLIST.md là tài liệu kiểm định chất lượng chính thức của Section S07.

Mọi phiên bản Frontend phải vượt qua Checklist này trước khi được phép Freeze.

Nếu có mâu thuẫn giữa cảm quan và Checklist thì:

**S07_REVIEW_CHECKLIST.md là tiêu chuẩn đánh giá cuối cùng.**