# BTE Platform

# S07 — THẦN SÁT

# S07_MASTER_GRID_VI.md

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

# 1. Mục tiêu

Tài liệu này quy định toàn bộ hệ thống lưới (Grid System), khoảng cách (Spacing), kích thước (Sizing) và căn chỉnh (Alignment) của Section S07.

Đây là tài liệu kỹ thuật dùng để:

- Designer
- Frontend
- Cursor
- AI Coding Agent

triển khai giao diện theo đúng chuẩn Desktop Canonical.

Không mô tả nghiệp vụ.

Không mô tả luận giải.

---

# 2. Kích thước Card

Chiều rộng

Theo Grid Desktop.

Chiều cao

≈ 340–380 px

Không vượt quá 400 px.

Nếu dữ liệu nhiều hơn:

Scroll nội bộ.

Không kéo dài Card.

---

# 3. Padding

Padding ngoài

20 px

Padding trên

20 px

Padding dưới

20 px

Padding trái

20 px

Padding phải

20 px

Không thay đổi.

---

# 4. Header

Chiều cao Header

24 px

Khoảng cách Header → Nội dung

16 px

Căn trái.

Không căn giữa.

---

# 5. Bố cục tổng thể

```
Header

↓

Cát tinh

↓

Divider

↓

Hung tinh

↓

Divider

↓

Footer Summary

↓

Link
```

Đọc theo chiều dọc.

Không chia cột.

---

# 6. Grid của Cát tinh

```
✓ Thiên Ất Quý Nhân

✓ Thiên Đức Quý Nhân

✓ Nguyệt Đức Quý Nhân

✓ Văn Xương

✓ Hoa Cái
```

Mỗi dòng:

Chiều cao

28 px

Khoảng cách giữa các dòng

8 px

---

# 7. Grid của Hung tinh

```
✕ Kiếp Sát

✕ Không Vong

✕ Cô Thần

✕ Quả Tú

✕ Đại Hao
```

Thông số giống Cát tinh.

Không khác.

---

# 8. Khoảng cách giữa hai nhóm

```
CÁT TINH

↓

16 px

↓

Divider

↓

16 px

↓

HUNG TINH
```

Không giảm.

---

# 9. Divider

Chiều cao

1 px

Màu

Neutral 200

Margin Top

16 px

Margin Bottom

16 px

---

# 10. Item

Một Item gồm:

```
Icon

↓

Tên
```

Không có thành phần thứ ba.

---

# 11. Icon

Kích thước

12 px

Khoảng cách tới chữ

8 px

Căn giữa theo chiều dọc.

---

# 12. Typography

Tiêu đề Section

16 px

700

---

Tiêu đề nhóm

13 px

700

---

Tên Thần Sát

14 px

500

---

Summary

13 px

500

---

Link

14 px

600

---

# 13. Footer Summary

Ví dụ

```
Có 5 Cát tinh và 5 Hung tinh.
```

Margin Top

16 px

Margin Bottom

16 px

Không xuống dòng nếu có thể.

---

# 14. Link

```
Xem toàn bộ →
```

Căn giữa.

Margin Top

16 px

Không Button.

Không Icon lớn.

---

# 15. Chiều cao Item

Tối thiểu

28 px

Tối đa

36 px

Nếu tên dài:

Cho phép xuống 2 dòng.

Không cắt chữ.

---

# 16. Danh sách dài

Nếu:

>10 Cát tinh

hoặc

>10 Hung tinh

↓

Hiển thị Scroll nội bộ.

Chiều cao Card giữ nguyên.

---

# 17. Empty State

Không có dữ liệu

↓

```
Không phát hiện Thần Sát phù hợp.
```

Không để khoảng trắng.

---

# 18. Alignment

Toàn bộ Item:

Căn trái.

Icon và chữ thẳng hàng.

Không căn giữa.

---

# 19. White Space

```
Header

16 px

↓

Group

16 px

↓

Divider

16 px

↓

Footer

16 px

↓

Link
```

Spacing đồng nhất.

---

# 20. Information Density

Mật độ:

Trung bình.

Không quá dày.

Không quá thưa.

Người dùng phải đọc được toàn bộ Section trong dưới 10 giây.

---

# 21. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Không chia nhiều cột.

---

# 22. Design Tokens

Padding

20

Radius

12

Border

1

Divider

1

Item Gap

8

Section Gap

16

Shadow

Enterprise Shadow

Không thay đổi.

---

# 23. Redline chuẩn

```
20

┌──────────────────────────────┐

20   Header

16

Group

16

Divider

16

Group

16

Footer

16

Link

20

└──────────────────────────────┘
```

Đây là Redline chuẩn.

---

# 24. Grid Rules

Không được:

✗ Căn giữa danh sách.

✗ Chia thành hai cột.

✗ Thêm Badge.

✗ Thêm Progress.

✗ Thêm KPI.

✗ Thêm Pie Chart.

---

# 25. Review Checklist

PASS khi:

✓ Khoảng cách đồng nhất.

✓ Divider đúng vị trí.

✓ Danh sách căn trái.

✓ Icon đồng đều.

✓ Không có Item lệch hàng.

✓ Không phải cuộn ở dữ liệu thông thường.

---

# 26. Mapping

Áp dụng cho:

Desktop Canonical V1

Có thể kế thừa cho:

Tablet

Mobile

Chỉ điều chỉnh Responsive.

Không thay đổi Grid Logic.

---

# 27. Freeze Statement

S07_MASTER_GRID_VI.md là tài liệu chuẩn quy định toàn bộ hệ thống Grid của Section S07.

Mọi triển khai Frontend phải tuân thủ tuyệt đối:

- Padding
- Spacing
- Alignment
- Divider
- Grid
- White Space

Nếu có khác biệt giữa mã nguồn và tài liệu này thì:

**S07_MASTER_GRID_VI.md là Single Source of Truth cho toàn bộ Grid của S07.**