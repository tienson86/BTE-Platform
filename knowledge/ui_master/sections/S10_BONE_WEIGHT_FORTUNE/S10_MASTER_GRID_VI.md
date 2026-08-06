# BTE Platform

# S10 — CÂN XƯƠNG ĐOÁN MỆNH

# S10_MASTER_GRID_VI.md

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

Tài liệu này quy định toàn bộ Grid System, Typography, White Space, Alignment và Information Hierarchy của Section S10.

Đây là tài liệu chuẩn dành cho:

- UI Designer
- Frontend Developer
- QA Engineer
- Cursor AI
- Product Owner

Mọi triển khai phải tuân thủ tuyệt đối.

---

# 2. Kích thước Card

Chiều rộng

Theo Desktop Grid.

Chiều cao

≈ 560–620 px

Khuyến nghị

≈ 590 px

Không vượt

650 px.

Không xuất hiện Scroll.

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

---

# 4. Reading Grid

```
Header

↓

Decision Card

↓

Divider

↓

Bài ca cân xương

↓

Divider

↓

Luận giải

↓

Divider

↓

Đọc luận giải đầy đủ
```

Reading Flow cố định.

Không thay đổi.

---

# 5. Header

Chiều cao

24 px

Margin Bottom

16 px

Căn trái.

---

# 6. Decision Card

```
┌───────────────────────────────┐

★★★★★

4 LƯỢNG 3 CHỈ

MỆNH TỐT

Thuộc nhóm có hậu vận ổn định

└───────────────────────────────┘
```

Padding

18 px

Border Radius

10 px

Border

1 px

Background

#FFF8EF

Shadow

Enterprise Shadow

Margin Bottom

16 px

Chiều cao

170–210 px

Không vượt

220 px.

---

# 7. Decision Card Typography

## Rating

★★★★★

20 px

Center

Margin Bottom

10 px

---

## Tổng lượng

```
4 LƯỢNG 3 CHỈ
```

32 px

700

BTE Red

Center

Margin Bottom

8 px

---

## Mức đánh giá

```
MỆNH TỐT
```

22 px

700

Neutral900

Center

Margin Bottom

8 px

---

## Nhận định

14 px

400

Neutral600

Center

Tối đa

2 dòng.

---

# 8. Divider

Độ dày

1 px

Inset

16 px

Neutral200

Margin Top

14 px

Margin Bottom

14 px

---

# 9. Tiêu đề Section

Áp dụng cho

```
📜 BÀI CA CÂN XƯƠNG

📖 LUẬN GIẢI
```

Typography

13 px

700

Icon

16 px

Khoảng cách Icon → Text

8 px

Margin Bottom

12 px

---

# 10. Bài ca cân xương

Typography

15 px

500

Italic

Center

Line Height

28 px

Tối đa

8 dòng.

Margin Bottom

4 px

Không chia cột.

Không đánh số.

Không Bullet.

---

# 11. Luận giải

Typography

14 px

400

Neutral700

Line Height

22 px

Căn trái.

Tối đa

100 từ.

Không vượt

5 dòng hiển thị.

---

# 12. Footer Link

```
Đọc luận giải đầy đủ →
```

Typography

14 px

600

BTE Red

Center

Margin Top

16 px

Text only.

Không Button.

---

# 13. White Space

Header

↓

16 px

Decision Card

↓

14 px

Divider

↓

14 px

Bài ca

↓

14 px

Divider

↓

14 px

Luận giải

↓

16 px

Divider

↓

16 px

Footer

Spacing đồng đều.

---

# 14. Information Density

★★★★★

Decision Card

★★★★★

Tổng lượng

★★★★☆

Bài ca

★★★★☆

Luận giải

★★☆☆☆

Footer

Decision Card luôn là điểm nổi bật nhất.

---

# 15. Alignment

Decision Card

Center

---

Bài ca

Center

---

Luận giải

Left

---

Footer

Center

Không thay đổi.

---

# 16. Maximum Content

Bài ca

8 dòng

---

Luận giải

100 từ

---

Nhận định

2 dòng

Nếu vượt

↓

Rút gọn.

Không tăng chiều cao Card.

---

# 17. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có kết quả Cân Xương Đoán Mệnh.
```

Không để khoảng trắng.

---

# 18. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 19. Grid Redline

```
20

┌───────────────────────────────┐

Header

16

Decision Card

14

Divider

14

Bài ca

14

Divider

14

Luận giải

16

Divider

16

Footer

20

└───────────────────────────────┘
```

Đây là Redline chuẩn.

---

# 20. Design Tokens

Padding

20

Radius

10

Border

1

Divider

1

Gap

16

Item Gap

8

Shadow

Enterprise Shadow

Không thay đổi.

---

# 21. Những điều KHÔNG được phép

✗ KPI

✗ Dashboard

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Progress Bar

✗ Rule

✗ JSON

✗ Debug

✗ Bảng tra lượng

✗ Công thức tính

✗ Scroll nội bộ

---

# 22. QA Checklist

PASS nếu

✓ Tổng lượng nổi bật.

✓ Decision Card đúng vị trí.

✓ Bài ca căn giữa.

✓ Luận giải dễ đọc.

✓ Divider đúng.

✓ Không Scroll.

✓ Đồng bộ Desktop Canonical.

---

# 23. Mapping

Nguồn dữ liệu

```
BoneWeightResult

↓

Weight

↓

Rating

↓

Verse

↓

Interpretation
```

UI chỉ hiển thị.

Không tính toán.

---

# 24. Freeze Statement

S10_MASTER_GRID_VI.md là tài liệu chuẩn quy định toàn bộ Grid System của Section S10.

Frontend phải tuân thủ:

- Grid
- Typography
- White Space
- Divider
- Alignment
- Responsive

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S10_MASTER_GRID_VI.md là Single Source of Truth cho Grid của S10.**