# BTE Platform

# S09 — HƯỚNG DẪN PHONG THỦY

# S09_MASTER_GRID_VI.md

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

Tài liệu này quy định toàn bộ Grid System, White Space, Alignment, Typography và Spacing của Section S09.

Đây là tài liệu kỹ thuật dành cho:

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

Không xuất hiện thanh cuộn.

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

Executive Guidance

↓

Divider

↓

Màu sắc phù hợp

↓

Divider

↓

Ngũ hành nên tăng cường

↓

Divider

↓

Hướng phù hợp

↓

Divider

↓

Khuyến nghị bố trí

↓

Divider

↓

Đọc hướng dẫn đầy đủ
```

Reading Flow là cố định.

---

# 5. Header

Chiều cao

24 px

Margin Bottom

16 px

Căn trái.

---

# 6. Executive Guidance Card

```
┌─────────────────────────────┐

HƯỚNG DẪN TỔNG QUAN

...

└─────────────────────────────┘
```

Padding

16 px

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

120–150 px

Không vượt

160 px.

---

# 7. Executive Typography

Tiêu đề

13 px

700

BTE Red

---

Phụ đề (nếu có)

12 px

400

Neutral 500

---

Nội dung

14 px

400

Line Height

20 px

Tối đa

5 dòng.

---

# 8. Divider

Độ dày

1 px

Inset

16 px

Neutral 200

Margin Top

14 px

Margin Bottom

14 px

---

# 9. Tiêu đề Section

Áp dụng cho:

```
MÀU SẮC PHÙ HỢP

NGŨ HÀNH NÊN TĂNG CƯỜNG

HƯỚNG PHÙ HỢP

KHUYẾN NGHỊ BỐ TRÍ
```

Typography

13 px

700

Margin Bottom

12 px

Icon

16 px

Khoảng cách Icon → Text

8 px

---

# 10. Danh sách

Mỗi dòng gồm:

```
Icon

↓

Text
```

Chiều cao

28 px

Khoảng cách giữa các dòng

8 px

Không có Badge.

Không có Chip.

Không đánh số.

---

# 11. Khối Màu sắc phù hợp

Ví dụ

```
✓ Xanh dương

✓ Đen

✓ Trắng

✓ Xám

✓ Bạc
```

Tối đa

5 mục.

---

# 12. Khối Ngũ hành nên tăng cường

Ví dụ

```
✓ Thủy

✓ Kim

✓ Mộc
```

Tối đa

3 mục.

---

# 13. Khối Hướng phù hợp

Ví dụ

```
✓ Bắc

✓ Tây Bắc

✓ Tây

✓ Đông Bắc
```

Tối đa

4 mục.

---

# 14. Khối Khuyến nghị bố trí

Ví dụ

```
• Tăng ánh sáng tự nhiên

• Ưu tiên không gian mở

• Bổ sung yếu tố nước

• Hạn chế màu nóng
```

Tối đa

4 mục.

---

# 15. Footer Link

```
Đọc hướng dẫn đầy đủ →
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

# 16. Typography

Header

16 px

700

---

Executive Title

13 px

700

---

Executive Caption

12 px

400

---

Executive Body

14 px

400

---

Section Title

13 px

700

---

Item

14 px

500

---

Footer Link

14 px

600

---

# 17. White Space

Header

↓

16 px

Executive

↓

16 px

Divider

↓

14 px

Section

↓

14 px

Divider

↓

14 px

Section

↓

14 px

Divider

↓

14 px

Section

↓

14 px

Divider

↓

16 px

Footer

Spacing phải đồng đều.

---

# 18. Information Density

Executive Guidance

★★★★★

Màu sắc

★★★★☆

Ngũ hành

★★★★☆

Hướng

★★★★☆

Khuyến nghị

★★★★☆

Footer

★★☆☆☆

Executive luôn nổi bật nhất.

---

# 19. Alignment

Toàn bộ nội dung

Căn trái.

Footer Link

Căn giữa.

Không căn giữa danh sách.

---

# 20. Maximum Content

Executive

100 từ

Màu sắc

5 mục

Ngũ hành

3 mục

Hướng

4 mục

Khuyến nghị

4 mục

Nếu vượt

↓

Rút gọn.

Không kéo dài Card.

---

# 21. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có hướng dẫn phong thủy.
```

Không để khoảng trắng.

---

# 22. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 23. Grid Redline

```
20

┌─────────────────────────────┐

Header

16

Executive

14

Divider

14

Màu sắc

14

Divider

14

Ngũ hành

14

Divider

14

Hướng

14

Divider

14

Khuyến nghị

16

Footer

20

└─────────────────────────────┘
```

Đây là Redline chuẩn.

---

# 24. Design Tokens

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

# 25. Những điều KHÔNG được phép

✗ KPI

✗ Dashboard

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Progress Bar

✗ Radar

✗ Rule ID

✗ JSON

✗ Debug

✗ Accordion

✗ Scroll nội bộ

---

# 26. QA Checklist

PASS nếu

✓ Executive nổi bật.

✓ Không vượt chiều cao chuẩn.

✓ Khoảng cách đồng đều.

✓ Divider đúng vị trí.

✓ Danh sách dễ đọc.

✓ Link đúng chuẩn.

✓ Không xuất hiện thanh cuộn.

---

# 27. Mapping

Nguồn dữ liệu

```
FengShuiGuidanceResult

↓

ExecutiveSummary

↓

RecommendedColors[]

↓

RecommendedElements[]

↓

RecommendedDirections[]

↓

LayoutAdvices[]
```

UI chỉ đọc dữ liệu.

Không xử lý nghiệp vụ.

---

# 28. Freeze Statement

S09_MASTER_GRID_VI.md là tài liệu chuẩn quy định toàn bộ Grid System của Section S09.

Frontend phải tuân thủ:

- Grid
- Padding
- Typography
- White Space
- Divider
- Alignment
- Responsive

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S09_MASTER_GRID_VI.md là Single Source of Truth cho Grid của S09.**