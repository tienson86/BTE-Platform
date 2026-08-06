# BTE Platform

# S02 — TỔNG QUAN & HÀNH ĐỘNG

---

Version

1.0.0

Status

ACTIVE

Module

UI Master

Section

S02 — Tổng Quan & Hành Động

Type

Master Section Definition

---

# 1. Mục tiêu

S02 là khu vực giúp người dùng **hiểu nhanh toàn bộ trạng thái của lá số** chỉ trong vài giây.

Nếu S01 trả lời:

> **"Tôi là ai?"**

thì S02 trả lời:

> **"Lá số của tôi đang như thế nào?"**

S02 không đi sâu vào giải thích.

S02 chỉ đưa ra bức tranh tổng quát để người dùng quyết định có cần đọc sâu hơn hay không.

---

# 2. Vai trò trong toàn bộ Portal

```
S00

Thông tin hồ sơ

↓

S01

Thông tin bản mệnh

↓

S02

Tổng quan lá số

↓

S03...

Phân tích chi tiết
```

S02 là cầu nối giữa:

Thông tin

↓

Phân tích.

---

# 3. Mục tiêu trải nghiệm

Sau khi xem S02, người dùng phải trả lời được ngay:

- Lá số mạnh hay yếu?
- Âm dương cân bằng không?
- Thể cục tốt hay xấu?
- Dụng thần là gì?
- Hỷ thần là gì?
- Kỵ thần là gì?

Nếu chưa trả lời được các câu hỏi trên thì S02 chưa đạt.

---

# 4. Vai trò nghiệp vụ

S02 không phân tích.

S02 không luận giải.

S02 chỉ tổng hợp kết quả từ Analysis Engine thành các chỉ số trực quan, dễ hiểu.

Đây là khu vực có tính chất:

**Executive Dashboard**

không phải

**Knowledge Panel**.

---

# 5. Thành phần

S02 gồm đúng 6 Summary Card.

```
┌────────────┬────────────┬────────────┐

Ngũ hành

Âm dương

Thể cục

├────────────┼────────────┼────────────┤

Dụng thần

Hỷ thần

Kỵ thần

└────────────┴────────────┴────────────┘
```

Không thêm Card.

Không bớt Card.

---

# 6. Ý nghĩa từng Card

## Ngũ hành

Hiển thị trạng thái tổng quát của Ngũ hành.

Ví dụ:

- Hỏa vượng
- Kim suy
- Mộc yếu

---

## Âm dương

Hiển thị mức độ cân bằng.

Ví dụ:

- Cân bằng
- Thiên dương
- Thiên âm

---

## Thể cục

Hiển thị chất lượng cấu trúc lá số.

Ví dụ:

- Tốt
- Trung bình
- Yếu

---

## Dụng thần

Hiển thị hành cần bổ sung.

Ví dụ:

- Thủy
- Kim

---

## Hỷ thần

Hiển thị hành hỗ trợ.

Ví dụ:

- Kim, Thủy

---

## Kỵ thần

Hiển thị hành bất lợi.

Ví dụ:

- Hỏa
- Mộc

---

# 7. Quy tắc hiển thị

Mỗi Card chỉ hiển thị:

- Biểu tượng
- Tiêu đề
- Giá trị

Không có:

- Đoạn mô tả dài
- CTA
- Tooltip
- Progress
- Biểu đồ

S02 phải cực kỳ gọn.

---

# 8. Reading Flow

```
Ngũ hành

↓

Âm dương

↓

Thể cục

↓

Dụng thần

↓

Hỷ thần

↓

Kỵ thần
```

Người dùng quét theo hình chữ Z.

---

# 9. Thời gian đọc

Mục tiêu:

5–10 giây.

Nếu cần đọc lâu hơn.

Thiết kế chưa đạt.

---

# 10. Trọng số thị giác

| Thành phần | Mức độ |
|------------|--------|
| Giá trị | ★★★★★ |
| Biểu tượng | ★★★★☆ |
| Tiêu đề | ★★★☆☆ |

Giá trị luôn là điểm nổi bật nhất.

---

# 11. Màu sắc

Màu sắc mang ý nghĩa ngũ hành và trạng thái.

Ví dụ:

- Hỏa → Đỏ
- Thủy → Xanh dương
- Mộc → Xanh lá
- Kim → Xám
- Thổ → Vàng

Semantic:

- Tốt → Xanh lá
- Trung bình → Vàng
- Bất lợi → Đỏ

Không sử dụng màu chỉ để trang trí.

---

# 12. Không hiển thị

S02 không được chứa:

- Giải thích dài
- Luận giải
- Ví dụ
- Khuyến nghị
- Bảng dữ liệu
- KPI
- Biểu đồ

Các nội dung này thuộc các Section phía sau.

---

# 13. Quan hệ với các Section khác

| Section | Vai trò |
|----------|---------|
| S01 | Danh tính bản mệnh |
| **S02** | Tổng quan nhanh |
| S03 | Tứ Trụ - Bát Tự |
| S04 | Cân bằng Ngũ hành |
| S05 | Sức mạnh mệnh cục |

S02 chỉ đóng vai trò "Dashboard".

---

# 14. Tiêu chí hoàn thành

Một S02 đạt chuẩn khi:

✓ Người dùng hiểu ngay trạng thái lá số.

✓ Sáu Card hiển thị cân đối.

✓ Không cần đọc nhiều chữ.

✓ Có thể quét trong dưới 10 giây.

✓ Không tạo cảm giác quá tải.

---

# 15. Freeze Scope

Desktop là chuẩn.

Tablet và Mobile sẽ kế thừa Information Hierarchy.

Không thay đổi:

- Thứ tự 6 Card.
- Ý nghĩa từng Card.
- Màu Semantic.
- Reading Flow.

---

# 16. Deliverables

Section S02 sẽ gồm:

```
README.md

↓

S02_MASTER_LAYOUT.md

↓

Canonical Screenshot

↓

Cursor Implementation

↓

Review

↓

Freeze
```

---

# 17. Freeze Statement

S02 là Dashboard tổng quan của toàn bộ lá số.

Đây là khu vực giúp người dùng nắm bắt trạng thái chính của lá số chỉ trong vài giây trước khi đi vào các phân tích chi tiết.

Mọi triển khai Frontend và AI Coding Agent phải tuân thủ tài liệu này như tài liệu định nghĩa chính thức của Section S02.