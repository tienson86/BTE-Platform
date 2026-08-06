# BTE Platform

# S01_MASTER_GRID_VI

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

Master Grid Specification

---

# 1. Mục đích

Tài liệu này mô tả **lưới bố cục (Grid)** của Section S01.

Đây là tiêu chuẩn duy nhất để:

- Thiết kế UI
- Lập trình Frontend
- Kiểm tra Review
- So sánh Pixel Perfect

Tài liệu này **không mô tả dữ liệu nghiệp vụ**.

Chỉ mô tả:

- Grid
- Kích thước
- Khoảng cách
- Vùng hiển thị
- Cấu trúc không gian

---

# 2. Nguyên tắc Grid

S01 sử dụng:

**Grid bất đối xứng (Asymmetrical Grid)**

Mục tiêu:

- Cột trái chứa dữ liệu nhận diện.
- Cột phải chứa dữ liệu định hướng.

Điều này tạo cảm giác:

- cân bằng
- dễ đọc
- không giống bảng dữ liệu

---

# 3. Cấu trúc Grid

```
┌──────────────────────────────────────────────────────────────────────┐
│                         S01 - THÔNG TIN & ĐỊNH HƯỚNG                │
├──────────────────────────────┬───────────────────────────────────────┤
│                              │                                       │
│                              │                                       │
│                              │                                       │
│         CỘT TRÁI             │            CỘT PHẢI                  │
│           58%                │              42%                     │
│                              │                                       │
│                              │                                       │
│                              │                                       │
├──────────────────────────────┴───────────────────────────────────────┤
└──────────────────────────────────────────────────────────────────────┘
```

---

# 4. Tỷ lệ

Desktop

```
Cột trái

58%

Cột phải

42%
```

Không được:

- 50 / 50
- 60 / 40
- 70 / 30

---

# 5. Safe Area

```
┌──────────────────────────────────────┐

24 px

┌──────────────────────────────────┐

      Nội dung

└──────────────────────────────────┘

24 px

└──────────────────────────────────────┘
```

Khoảng cách an toàn xung quanh Section:

**24 px**

---

# 6. Khoảng cách giữa hai cột

```
LEFT

│

24 px

│

RIGHT
```

Column Gap

**24 px**

Không thay đổi.

---

# 7. Cột trái

Bao gồm đúng:

```
Thông tin bản mệnh

↓

24 px

↓

Điều kiện mệnh cục
```

Không thêm thành phần khác.

---

# 8. Cột phải

Bao gồm:

```
Định hướng cuộc đời

↓

12 px

↓

Định hướng cuộc đời

↓

12 px

↓

Định hướng cuộc đời

↓

20 px

↓

Nút hành động
```

---

# 9. Grid của Thông tin bản mệnh

```
┌──────────────────────────────┐

ICON

↓

Nhật Chủ

↓

Ngũ hành

↓

Badge

└──────────────────────────────┘
```

Padding

20 px

---

# 10. Grid Điều kiện mệnh cục

```
Mùa sinh

Giá trị

Badge

────────────────────

Cục mệnh

Giá trị

Badge

────────────────────

Thân cư

Giá trị

Badge
```

Luôn đúng:

3 hàng.

---

# 11. Grid Định hướng

```
┌──────────────────────┐

Icon

↓

Tiêu đề

↓

Mô tả

└──────────────────────┘
```

Có đúng:

3 Card.

---

# 12. Grid CTA

```
┌──────────────────────┐

Xem luận giải chi tiết →

└──────────────────────┘
```

CTA luôn:

- nằm cuối cột phải
- rộng bằng cột phải
- không vượt ra ngoài Grid

---

# 13. Khoảng cách dọc

```
Identity

↓

24 px

↓

Condition

↓

24 px
```

```
Guidance 01

↓

12 px

↓

Guidance 02

↓

12 px

↓

Guidance 03

↓

20 px

↓

CTA
```

---

# 14. Padding chuẩn

| Thành phần | Padding |
|------------|---------:|
| Padding ngoài Section | 24 px |
| Padding Card | 20 px |
| Padding Badge | 12 px |
| Padding CTA | 16 px |

---

# 15. Kích thước tối thiểu

| Thành phần | Quy định |
|------------|----------|
| Card Identity | Không thấp hơn 120 px |
| Guidance Card | Đồng đều chiều cao |
| CTA | Không thấp hơn 44 px |

---

# 16. Căn lề

Cột trái

- Căn trái

Cột phải

- Căn trái

Badge

- Căn giữa

CTA

- Căn giữa

---

# 17. Không gian trắng

Khoảng trắng là một thành phần thiết kế.

Không được:

- nhồi thêm nội dung
- kéo giãn Card
- thêm Divider không cần thiết

Ưu tiên:

```
Không gian trắng

>

Đường viền

>

Trang trí
```

---

# 18. Các vùng Grid

```
┌──────────────────────────────────────────────────────┐

A

Thông tin bản mệnh

────────────────────────────

B

Điều kiện mệnh cục

────────────────────────────

C

Định hướng 1

────────────────────────────

D

Định hướng 2

────────────────────────────

E

Định hướng 3

────────────────────────────

F

CTA

└──────────────────────────────────────────────────────┘
```

Các vùng A → F là cố định.

---

# 19. Quy tắc Responsive

Desktop là chuẩn.

Tablet:

- giữ nguyên tỷ lệ
- giảm khoảng cách

Mobile:

- chuyển thành một cột
- giữ nguyên thứ tự đọc

Không thay đổi:

- Information Hierarchy
- Reading Flow

---

# 20. Những điều không được phép

Không được:

✗ Đổi tỷ lệ hai cột

✗ Đưa CTA xuống cuối toàn Section

✗ Chia đều 50 / 50

✗ Chèn thêm Card

✗ Thêm hàng

✗ Thêm cột

✗ Thêm khoảng trắng bất thường

✗ Thêm Divider trang trí

---

# 21. Tiêu chí đạt chuẩn

Một Grid đạt chuẩn khi:

✓ Hai cột đúng tỷ lệ

✓ Khoảng cách đúng

✓ Không có vùng chết

✓ CTA đúng vị trí

✓ Các Card căn chỉnh đều

✓ Khớp Canonical Desktop

---

# 22. Tài liệu tham chiếu

Ưu tiên theo thứ tự:

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

S01_MASTER_ANNOTATION_VI.png

↓

5.

S01_REVIEW_CHECKLIST.md

---

# 23. Freeze Statement

S01_MASTER_GRID_VI.md là tài liệu chuẩn mô tả lưới bố cục của Section S01.

Mọi thiết kế, lập trình và kiểm thử phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**S01_MASTER_GRID_VI.md được ưu tiên làm chuẩn triển khai.**