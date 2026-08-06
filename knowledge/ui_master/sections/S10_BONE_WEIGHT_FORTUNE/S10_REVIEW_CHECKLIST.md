# BTE Platform

# S10 — CÂN XƯƠNG ĐOÁN MỆNH

# S10_REVIEW_CHECKLIST.md

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

Tài liệu này là Checklist chính thức dùng để kiểm định chất lượng của Section S10 trước khi chuyển sang trạng thái **FROZEN**.

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
S10 — CÂN XƯƠNG ĐOÁN MỆNH
```

☐ Font đúng Design System

☐ Màu đúng BTE Red

☐ Không Icon dư

☐ Không Badge

☐ Không KPI

☐ Không Dashboard

---

# 4. Kiểm tra Decision Card

Đây là vùng quan trọng nhất của S10.

## PASS nếu

☐ Có Decision Card

☐ Nền đúng `#FFF8EF`

☐ Border Radius đúng

☐ Border đúng Design System

☐ Shadow đúng Enterprise UI

☐ Tổng lượng nổi bật nhất

☐ Mức đánh giá rõ ràng

☐ Có nhận định ngắn

☐ Không có Progress Bar

☐ Không có KPI

☐ Không có Dashboard

☐ Người dùng hiểu kết quả trong dưới 10 giây

---

# 5. Kiểm tra Tổng lượng

## PASS nếu

☐ Hiển thị đúng định dạng

```
4 LƯỢNG 3 CHỈ
```

☐ Font 32 px

☐ Đúng màu BTE Red

☐ Căn giữa

☐ Là điểm nhấn lớn nhất

☐ Không bị cắt dòng

---

# 6. Kiểm tra Mức đánh giá

## PASS nếu

☐ Hiển thị đúng

Ví dụ

```
MỆNH TỐT
```

☐ Font đúng

☐ Căn giữa

☐ Không sử dụng màu sắc gây hiểu lầm

☐ Có thể đọc rõ ở khoảng cách thông thường

---

# 7. Kiểm tra Bài ca cân xương

## PASS nếu

☐ Có tiêu đề

```
📜 BÀI CA CÂN XƯƠNG
```

☐ Hiển thị nguyên văn dữ liệu

☐ Không tự chỉnh sửa nội dung

☐ Không tự rút gọn

☐ Không thêm diễn giải

☐ Tối đa 8 dòng hiển thị

☐ Dễ đọc

---

# 8. Kiểm tra Luận giải

## PASS nếu

☐ Có tiêu đề

```
📖 LUẬN GIẢI
```

☐ Nội dung dễ hiểu

☐ Tối đa 100 từ

☐ Không trình bày học thuật

☐ Không có Rule

☐ Không có JSON

☐ Không lặp lại nguyên văn bài ca

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
Đọc luận giải đầy đủ →
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

☐ Tổng lượng 32 px

☐ Mức đánh giá 22 px

☐ Nhận định 14 px

☐ Tiêu đề Section 13 px

☐ Bài ca 15 px Italic

☐ Luận giải 14 px

☐ Link 14 px

☐ Font Weight đúng

---

# 12. Kiểm tra White Space

## PASS nếu

☐ Padding đúng 20 px

☐ Decision Card cân đối

☐ Divider đúng khoảng cách

☐ Khoảng cách giữa các Block đồng đều

☐ Không có khoảng trắng dư

☐ Không bị dồn nội dung

---

# 13. Kiểm tra Information Hierarchy

## PASS nếu

★★★★★ Decision Card

★★★★★ Tổng lượng

★★★★☆ Mức đánh giá

★★★★☆ Bài ca

★★★★☆ Luận giải

★★☆☆☆ Link

Decision Card luôn nổi bật nhất.

---

# 14. Kiểm tra Reading Flow

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

Đọc luận giải đầy đủ
```

## PASS nếu

☐ Không gây nhầm lẫn

☐ Luồng đọc tự nhiên

☐ Không phải đọc lại

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

☐ Dữ liệu đúng từ Bone Weight Fortune Engine

☐ Không tự sinh dữ liệu

☐ Không mâu thuẫn với các Section khác

☐ Không chứa nội dung mê tín cực đoan

☐ Không đưa ra khẳng định tuyệt đối về số mệnh

☐ Nội dung mang tính tham khảo và định hướng

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

☐ Decision First

☐ Recognition > Reading

☐ Simplicity > Complexity

☐ Practical > Academic

☐ Enterprise UI

---

# 20. Kiểm tra Pattern

## PASS nếu

☐ Đúng PATTERN_05_DECISION_CARD

☐ Đúng PATTERN_08_KNOWLEDGE_CARD

☐ Đúng PATTERN_10_REPORT_BLOCK

☐ Không vi phạm Design System

---

# 21. Kiểm tra Canonical

Đối chiếu với:

```
S10_CANONICAL.png
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
01_s10_only.png
```

## PASS nếu

☐ Chỉ hiển thị S10

☐ Độ phân giải chuẩn

☐ Không crop lỗi

☐ Không che nội dung

---

# 23. Điều kiện Freeze

S10 chỉ được Freeze khi:

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

- Khả năng truyền đạt kết quả Cân Xương Đoán Mệnh.
- Khả năng người dùng hiểu ngay kết quả.
- Tính nhất quán với Desktop Canonical UI.
- Chất lượng trải nghiệm.
- Khả năng mở rộng trong tương lai mà không thay đổi kiến trúc.

Nếu người dùng có thể hiểu kết quả trong vài giây và nắm được ý nghĩa tổng quát mà không cần tra cứu bảng cân xương thì S10 đã hoàn thành mục tiêu.

---

# 25. Freeze Statement

S10_REVIEW_CHECKLIST.md là tài liệu kiểm định chất lượng chính thức của Section S10.

Mọi phiên bản Frontend phải vượt qua Checklist này trước khi được phép Freeze.

Nếu có khác biệt giữa cảm quan và Checklist thì:

**S10_REVIEW_CHECKLIST.md là tiêu chuẩn đánh giá cuối cùng của Section S10.**