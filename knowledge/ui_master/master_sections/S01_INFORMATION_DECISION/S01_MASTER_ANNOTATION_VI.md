# BTE Platform

# S01_MASTER_ANNOTATION_VI

---

Phiên bản

1.0.0

Trạng thái

FROZEN

Module

UI Master

Section

S01 — Thông Tin & Định Hướng

Loại tài liệu

Master Annotation Specification

---

# 1. Mục đích

Tài liệu này mô tả toàn bộ chú thích (Annotation) của Section S01.

Đây là tài liệu dùng để:

- Review UI
- Frontend triển khai
- AI Coding Agent triển khai
- Kiểm tra Pixel Perfect

Không mô tả Business Logic.

Không mô tả API.

Không mô tả Database.

Chỉ mô tả:

- Vai trò từng vùng
- Thứ tự đọc
- Trọng số thị giác
- Luồng nhận thức
- Khoảng cách
- Quy tắc trình bày

---

# 2. Mục tiêu thiết kế

S01 phải giúp người dùng hiểu:

"Tôi là ai?"

↓

"Điểm mạnh của tôi là gì?"

↓

"Tôi nên làm gì?"

↓

"Đọc tiếp ở đâu?"

Toàn bộ quá trình này diễn ra trong khoảng:

30–60 giây.

---

# 3. Bản đồ chú thích

```
┌────────────────────────────────────────────────────────────┐

① THÔNG TIN BẢN MỆNH

② ĐIỀU KIỆN MỆNH CỤC

③ ĐỊNH HƯỚNG CUỘC ĐỜI

④ NÚT HÀNH ĐỘNG

└────────────────────────────────────────────────────────────┘
```

Đây là bốn vùng bắt buộc.

---

# 4. Annotation ①

## THÔNG TIN BẢN MỆNH

Vai trò

Hiển thị danh tính tổng quát của lá số.

Mục tiêu

Giúp người dùng nhận diện ngay Nhật Chủ.

Trọng số thị giác

★★★★★

Đây là vùng nổi bật nhất của S01.

---

# 5. Thành phần Annotation ①

Bao gồm:

```
Biểu tượng

↓

Nhật Chủ

↓

Ngũ hành

↓

Âm dương

↓

Badge

↓

Tính cách
```

Không thêm:

- Progress
- Score
- CTA
- Divider

---

# 6. Quy tắc Nhật Chủ

Nhật Chủ là điểm nhìn đầu tiên.

Ví dụ:

```
Bính Hỏa
```

Luôn là chữ lớn nhất.

Không thành phần nào lớn hơn.

---

# 7. Quy tắc Badge

Badge chỉ dùng để:

- Hỏa vượng
- Kim nhược
- Thân vượng
- ...

Không dùng Badge để trang trí.

Badge phải:

- cùng chiều cao
- cùng Radius
- cùng Padding

---

# 8. Annotation ②

## ĐIỀU KIỆN MỆNH CỤC

Vai trò

Giải thích cơ sở hình thành mệnh cục.

Đây là vùng:

Evidence

không phải

Decision.

---

# 9. Thành phần Annotation ②

Có đúng:

```
Mùa sinh

↓

Cục mệnh

↓

Thân cư
```

Không thêm:

- Đại vận
- Lưu niên
- Điểm số
- Ngũ hành

---

# 10. Quy tắc Bảng điều kiện

Mỗi hàng gồm:

```
Nhãn

↓

Giá trị

↓

Badge
```

Ba hàng phải:

- cùng chiều cao
- cùng khoảng cách

---

# 11. Annotation ③

## ĐỊNH HƯỚNG CUỘC ĐỜI

Vai trò

Biến dữ liệu thành lời khuyên.

Đây là khu vực tạo giá trị lớn nhất cho người dùng.

---

# 12. Thành phần Annotation ③

Có đúng:

Ba Card.

Card 1

```
Bạn là ai?
```

Card 2

```
Thế mạnh của bạn?
```

Card 3

```
Bạn nên làm gì?
```

Không thêm Card.

---

# 13. Quy tắc Card

Mỗi Card gồm:

```
Biểu tượng

↓

Tiêu đề

↓

Mô tả
```

Không có:

Badge

Button

Link

Score

---

# 14. Quy tắc nội dung

Tiêu đề

Ngắn.

Dễ hiểu.

---

Mô tả

Không quá:

2 dòng.

Nếu dài hơn.

Rút gọn.

Không tăng chiều cao Card.

---

# 15. Annotation ④

## NÚT HÀNH ĐỘNG

Đây là CTA chính của S01.

Tên:

```
Xem luận giải chi tiết →
```

Không tạo:

CTA phụ.

---

# 16. Quy tắc CTA

CTA luôn:

- cuối cột phải
- rộng bằng cột phải
- nằm sau ba Card

Không:

- Full Width toàn Section
- Đặt dưới Condition

---

# 17. Luồng đọc

```
① Nhật Chủ

↓

② Điều kiện

↓

③ Bạn là ai?

↓

④ Thế mạnh

↓

⑤ Bạn nên làm gì?

↓

⑥ CTA
```

Không thay đổi.

---

# 18. Luồng nhận thức

```
Nhận diện

↓

Hiểu nguyên nhân

↓

Nhận lời khuyên

↓

Hành động
```

Đây là Cognitive Flow.

Không phá vỡ.

---

# 19. Trọng số thị giác

| Thành phần | Mức độ |
|------------|--------|
| Nhật Chủ | ★★★★★ |
| Điều kiện | ★★★★☆ |
| Định hướng | ★★★★☆ |
| CTA | ★★★☆☆ |
| Metadata | ★★☆☆☆ |

---

# 20. Quy tắc khoảng trắng

Khoảng trắng là thành phần thiết kế.

Mục tiêu:

Giúp mắt nghỉ.

Không:

- chèn thêm nội dung
- kéo giãn Card
- giảm khoảng cách để nhét dữ liệu

---

# 21. Quy tắc biểu tượng

Biểu tượng chỉ hỗ trợ nhận diện.

Không được:

- lớn hơn Nhật Chủ
- nhiều màu gây nhiễu
- sử dụng hiệu ứng

Mỗi Card chỉ có:

Một biểu tượng.

---

# 22. Quy tắc màu sắc

Đỏ

Thông tin chính.

---

Xám

Thông tin phụ.

---

Semantic

Chỉ dùng cho Badge.

Không dùng màu để trang trí.

---

# 23. Quy tắc Typography

Thứ tự:

```
Nhật Chủ

↓

Tiêu đề Card

↓

Giá trị

↓

Mô tả

↓

Metadata
```

Không đảo ngược.

---

# 24. Quy tắc khoảng cách

Identity

↓

24 px

↓

Condition

↓

24 px

↓

Guidance

↓

20 px

↓

CTA

Không thay đổi.

---

# 25. Những điều không được phép

Không được:

✗ Thêm Card

✗ Đổi vị trí CTA

✗ Đổi tỷ lệ hai cột

✗ Chia thành một cột

✗ Thêm Progress

✗ Thêm KPI

✗ Thêm Score

✗ Thêm Divider trang trí

✗ Thêm Icon không có ý nghĩa

---

# 26. Review Annotation

Khi review.

Kiểm tra:

□ Nhật Chủ nổi bật nhất.

□ Điều kiện đúng ba hàng.

□ Định hướng đúng ba Card.

□ CTA đúng vị trí.

□ Không có thành phần dư.

□ Luồng đọc đúng.

□ Trọng số thị giác đúng.

---

# 27. Chuyển đổi sang PNG

Tài liệu này sẽ được chuyển thành:

```
S01_MASTER_ANNOTATION_VI.png
```

Ảnh sẽ sử dụng:

- Khung màu đỏ: Vùng nghiệp vụ
- Khung màu xanh: Bố cục
- Khung màu xanh lá: Quy tắc triển khai
- Mũi tên: Luồng đọc
- Số thứ tự (①②③④): Vùng chức năng

Đây là ảnh chú thích chính thức để Frontend và AI Coding Agent triển khai.

---

# 28. Tài liệu tham chiếu

Ưu tiên:

1.

CANONICAL_PORTAL_UI_DESKTOP_V1.png

↓

2.

S01_MASTER_LAYOUT.md

↓

3.

S01_MASTER_GRID_VI.md

↓

4.

S01_MASTER_ANNOTATION_VI.md

↓

5.

S01_REVIEW_CHECKLIST.md

---

# 29. Freeze Statement

S01_MASTER_ANNOTATION_VI.md là tài liệu chuẩn mô tả ý nghĩa, vai trò và quy tắc hiển thị của từng vùng trong Section S01.

Đây là cơ sở để tạo:

- S01_MASTER_ANNOTATION_VI.png
- S01_MASTER_ANNOTATION_EN.png

và là tài liệu bắt buộc phải tuân thủ khi triển khai hoặc đánh giá giao diện S01.