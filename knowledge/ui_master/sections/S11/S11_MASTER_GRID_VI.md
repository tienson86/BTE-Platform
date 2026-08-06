# BTE Platform

# S11 — BÁO CÁO TỔNG KẾT

# S11_MASTER_GRID_VI.md

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

S11

Tên

Báo cáo tổng kết

---

# 1. Mục đích

Tài liệu này quy định toàn bộ Grid System, Typography, White Space, Alignment và Information Hierarchy của Section S11.

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

≈ 620–700 px

Khuyến nghị

≈ 660 px

Không vượt

720 px.

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

Executive Summary Card

↓

Divider

↓

Điểm mạnh

↓

Divider

↓

Điểm cần lưu ý

↓

Divider

↓

Khuyến nghị hành động

↓

Divider

↓

Xem báo cáo đầy đủ
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

# 6. Executive Summary Card

```
┌─────────────────────────────────────┐

KẾT LUẬN TỔNG QUAN

Bạn có nền tảng mệnh cục khá tốt.
Khả năng phát triển ổn định nếu
phát huy năng lực lãnh đạo và
duy trì sự cân bằng cảm xúc.

└─────────────────────────────────────┘
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

140–180 px

Không vượt

190 px.

---

# 7. Executive Summary Typography

Tiêu đề

```
KẾT LUẬN TỔNG QUAN
```

16 px

700

BTE Red

Margin Bottom

10 px

---

Nội dung

15 px

400

Neutral700

Line Height

24 px

Tối đa

5 dòng.

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

# 9. Block Title

Áp dụng cho

```
✓ ĐIỂM MẠNH

⚠ ĐIỂM CẦN LƯU Ý

➜ KHUYẾN NGHỊ HÀNH ĐỘNG
```

Typography

13 px

700

Margin Bottom

10 px

Icon

16 px

Khoảng cách

8 px

---

# 10. Information List

Typography

14 px

400

Neutral700

Line Height

22 px

Gap giữa Item

8 px

Tối đa

5 Item / Block.

Không vượt.

---

# 11. Strength Block

Icon

✓

Màu

Green

Không đổi màu theo dữ liệu.

---

# 12. Attention Block

Icon

•

hoặc

⚠

Màu

Orange

Không dùng đỏ cảnh báo mạnh.

---

# 13. Recommendation Block

Icon

→

Màu

Blue

Khuyến nghị luôn là hành động.

Không mô tả lý thuyết.

---

# 14. Footer Link

```
Xem báo cáo phân tích đầy đủ →
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

# 15. White Space

Header

↓

16 px

Executive Card

↓

14 px

Divider

↓

14 px

Strength

↓

14 px

Divider

↓

14 px

Attention

↓

14 px

Divider

↓

14 px

Recommendation

↓

16 px

Divider

↓

16 px

Footer

Spacing đồng đều.

---

# 16. Information Density

★★★★★

Executive Summary

★★★★★

Kết luận

★★★★☆

Điểm mạnh

★★★★☆

Điểm cần lưu ý

★★★★☆

Khuyến nghị

★★☆☆☆

Footer

Executive Summary luôn nổi bật nhất.

---

# 17. Alignment

Executive Summary

Left

---

Danh sách

Left

---

Footer

Center

Không thay đổi.

---

# 18. Maximum Content

Executive Summary

5 dòng

---

Danh sách

5 mục

---

Footer

1 dòng

Nếu vượt

↓

Rút gọn.

Không tăng chiều cao Card.

---

# 19. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có báo cáo tổng kết.

Vui lòng hoàn thành phân tích trước.
```

Không để khoảng trắng.

---

# 20. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 21. Grid Redline

```
20

┌──────────────────────────────┐

Header

16

Executive Summary

14

Divider

14

Strength

14

Divider

14

Attention

14

Divider

14

Recommendation

16

Divider

16

Footer

20

└──────────────────────────────┘
```

Đây là Redline chuẩn.

---

# 22. Design Tokens

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

# 23. Những điều KHÔNG được phép

✗ Pie Chart

✗ Gauge

✗ KPI

✗ Dashboard

✗ Rule

✗ JSON

✗ Debug

✗ Accordion

✗ Tabs

✗ Progress Bar

✗ Điểm số mới

---

# 24. QA Checklist

PASS nếu

✓ Executive Summary nổi bật.

✓ Reading Flow đúng.

✓ Danh sách cân đối.

✓ Divider đúng.

✓ Không Scroll.

✓ Đồng bộ Desktop Canonical.

---

# 25. Mapping

Nguồn dữ liệu

```
Interpretation Engine

↓

Executive Summary

↓

Strengths

↓

Warnings

↓

Recommendations

↓

S11
```

UI chỉ hiển thị.

Không tính toán.

---

# 26. Freeze Statement

S11_MASTER_GRID_VI.md là tài liệu chuẩn quy định toàn bộ Grid System của Section S11.

Frontend phải tuân thủ:

- Grid
- Typography
- White Space
- Divider
- Alignment
- Responsive

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S11_MASTER_GRID_VI.md là Single Source of Truth cho Grid của Section S11.**