# BTE Platform

# S09 — HƯỚNG DẪN PHONG THỦY

# S09_REVIEW_CHECKLIST.md

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

Tài liệu này là Checklist chính thức dùng để kiểm định chất lượng của Section S09 trước khi chuyển sang trạng thái **FROZEN**.

Checklist được sử dụng bởi:

- Product Owner
- UI/UX Designer
- Frontend Developer
- QA Engineer
- Cursor AI

Một bản triển khai chỉ được coi là hoàn thành khi toàn bộ Checklist đều đạt PASS.

---

# 2. Quy trình Review

Thực hiện theo đúng trình tự:

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

☐ Hiển thị đúng

```
S09 — HƯỚNG DẪN PHONG THỦY
```

☐ Font đúng Design System

☐ Màu đúng BTE Red

☐ Không Icon dư

☐ Không Badge

☐ Không KPI

☐ Không Dashboard

---

# 4. Kiểm tra Executive Guidance

Đây là vùng quan trọng nhất của S09.

## PASS nếu

☐ Có Executive Card

☐ Nền đúng `#FFF8EF`

☐ Border Radius đúng

☐ Có tiêu đề

```
HƯỚNG DẪN TỔNG QUAN
```

☐ Nội dung từ 60–100 từ

☐ Không quá 5 dòng hiển thị

☐ Không có thuật ngữ kỹ thuật

☐ Không có Rule

☐ Không có JSON

☐ Người dùng hiểu nội dung trong dưới 20 giây

---

# 5. Kiểm tra Khối Màu sắc phù hợp

## PASS nếu

☐ Có tiêu đề

```
🟥 MÀU SẮC PHÙ HỢP
```

☐ Tối đa 5 mục

☐ Mỗi dòng gồm:

```
✓

Tên màu
```

☐ Không Badge

☐ Không Chip

☐ Không diễn giải dài

☐ Không xuống quá 2 dòng

---

# 6. Kiểm tra Khối Ngũ hành nên tăng cường

## PASS nếu

☐ Có tiêu đề

```
🟩 NGŨ HÀNH NÊN TĂNG CƯỜNG
```

☐ Tối đa 3 mục

☐ Nội dung rõ ràng

☐ Không giải thích học thuật

☐ Không dùng biểu đồ

---

# 7. Kiểm tra Khối Hướng phù hợp

## PASS nếu

☐ Có tiêu đề

```
🧭 HƯỚNG PHÙ HỢP
```

☐ Tối đa 4 mục

☐ Dễ đọc

☐ Không có bản đồ

☐ Không có La bàn

☐ Không có sơ đồ

---

# 8. Kiểm tra Khối Khuyến nghị bố trí

## PASS nếu

☐ Có tiêu đề

```
🏡 KHUYẾN NGHỊ BỐ TRÍ
```

☐ Tối đa 4 mục

☐ Nội dung thực tế

☐ Có thể áp dụng ngay

☐ Không luận giải dài

☐ Không mang tính tuyệt đối

---

# 9. Kiểm tra Divider

## PASS nếu

☐ Divider đúng vị trí

☐ Độ dày 1 px

☐ Inset đúng Design System

☐ Khoảng cách đồng đều

☐ Không chạm mép Card

---

# 10. Kiểm tra Link

## PASS nếu

☐ Hiển thị đúng

```
Đọc hướng dẫn đầy đủ →
```

☐ Là Text Link

☐ Không Button

☐ Không nền

☐ Không Shadow

☐ Hover đúng Design System

☐ Điều hướng đúng

---

# 11. Kiểm tra Typography

## PASS nếu

☐ Header 16 px

☐ Executive Title 13 px

☐ Executive Caption 12 px (nếu có)

☐ Executive Body 14 px

☐ Section Title 13 px

☐ Item 14 px

☐ Link 14 px

☐ Font Weight đúng

---

# 12. Kiểm tra White Space

## PASS nếu

☐ Padding đúng 20 px

☐ Executive Card cân đối

☐ Divider đúng khoảng cách

☐ Các Block đều nhau

☐ Không bị dồn

☐ Không có khoảng trắng dư

---

# 13. Kiểm tra Information Hierarchy

## PASS nếu

★★★★★ Executive Guidance

★★★★☆ Màu sắc phù hợp

★★★★☆ Ngũ hành nên tăng cường

★★★★☆ Hướng phù hợp

★★★★☆ Khuyến nghị bố trí

★★☆☆☆ Link

Executive Guidance luôn nổi bật nhất.

---

# 14. Kiểm tra Reading Flow

Người dùng phải đọc theo:

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

## PASS nếu

☐ Không gây nhầm lẫn

☐ Không phải đọc lại

☐ Luồng đọc tự nhiên

---

# 15. Kiểm tra Responsive

## Desktop

☐ Không Scroll

☐ Không vỡ Layout

---

## Tablet

☐ Không tràn

☐ Không lệch

---

## Mobile

☐ Không cuộn ngang

☐ Reading Flow giữ nguyên

---

# 16. Kiểm tra Accessibility

## PASS nếu

☐ Contrast đạt WCAG AA

☐ Không dùng màu là tín hiệu duy nhất

☐ Keyboard Focus hoạt động

☐ Screen Reader đọc đúng

---

# 17. Kiểm tra Nội dung

## PASS nếu

☐ Phù hợp với Feng Shui Guidance Engine

☐ Không tự sinh dữ liệu

☐ Không mâu thuẫn với S08

☐ Không lặp nội dung

☐ Không mang tính mê tín

☐ Không khẳng định tuyệt đối

---

# 18. Kiểm tra Performance

## PASS nếu

☐ Render nhanh

☐ Không Animation

☐ Không Lag

☐ Không Scroll bất thường

---

# 19. Kiểm tra Design Principles

## PASS nếu

☐ Executive Guidance > Detail

☐ Recognition > Reading

☐ Practical > Theory

☐ Action > Explanation

☐ Enterprise UI

---

# 20. Kiểm tra Pattern

## PASS nếu

☐ Đúng PATTERN_06_INFORMATION_LIST

☐ Đúng PATTERN_07_STATUS_PANEL

☐ Đúng PATTERN_10_REPORT_BLOCK

☐ Không vi phạm Design System

---

# 21. Kiểm tra Canonical

Đối chiếu với:

```
S09_CANONICAL.png
```

## PASS nếu

☐ Layout giống

☐ Grid giống

☐ Typography giống

☐ White Space giống

☐ Information Hierarchy giống

☐ Reading Flow giống

---

# 22. Kiểm tra Screenshot

Bắt buộc có:

```
01_s09_only.png
```

## PASS nếu

☐ Chỉ hiển thị S09

☐ Độ phân giải chuẩn

☐ Không crop lỗi

☐ Không che nội dung

---

# 23. Điều kiện Freeze

S09 chỉ được Freeze khi:

☐ README PASS

☐ MASTER_LAYOUT PASS

☐ MASTER_GRID_VI PASS

☐ MASTER_ANNOTATION_VI PASS

☐ Screenshot PASS

☐ Product Owner phê duyệt

☐ Không còn Critical Issue

---

# 24. Design Decision Record

Checklist này không đánh giá giao diện đẹp hay xấu.

Checklist đánh giá:

- Khả năng hướng dẫn người dùng.
- Khả năng áp dụng thực tế.
- Tính nhất quán với Desktop Canonical.
- Chất lượng trải nghiệm.
- Khả năng mở rộng trong tương lai mà không thay đổi kiến trúc.

Nếu người dùng có thể đọc và áp dụng các hướng dẫn trong vòng vài phút thì S09 đã hoàn thành mục tiêu.

---

# 25. Freeze Statement

S09_REVIEW_CHECKLIST.md là tài liệu kiểm định chất lượng chính thức của Section S09.

Mọi phiên bản Frontend phải vượt qua Checklist này trước khi được phép Freeze.

Nếu có khác biệt giữa cảm quan và Checklist thì:

**S09_REVIEW_CHECKLIST.md là tiêu chuẩn đánh giá cuối cùng của Section S09.**