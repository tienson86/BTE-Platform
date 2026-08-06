# BTE Platform

# S03 — TỨ TRỤ - BÁT TỰ

---

Version

1.0.0

Status

ACTIVE

Module

UI Master

Section

S03 — Tứ Trụ - Bát Tự

Type

Master Section Definition

---

# 1. Mục tiêu

S03 là khu vực hiển thị đầy đủ bốn trụ của lá số Bát Tự.

Đây là phần dữ liệu gốc quan trọng nhất của toàn bộ hệ thống.

Tất cả các phân tích ở các Section phía sau đều được xây dựng từ dữ liệu của S03.

---

# 2. Vai trò trong Portal

```
S00

Thông tin hồ sơ

↓

S01

Thông tin bản mệnh

↓

S02

Tổng quan

↓

S03

Tứ Trụ - Bát Tự

↓

S04...

Phân tích chuyên sâu
```

S03 là nền tảng dữ liệu của toàn bộ Portal.

---

# 3. Mục tiêu trải nghiệm

Sau khi xem S03, người dùng phải hiểu ngay:

- Có bốn trụ.
- Mỗi trụ gồm Thiên Can và Địa Chi.
- Nhật Trụ là trung tâm của lá số.
- Có thể đối chiếu nhanh giữa bốn trụ.

Không cần đọc giải thích.

Chỉ cần nhìn là hiểu cấu trúc.

---

# 4. Vai trò nghiệp vụ

S03 chỉ hiển thị dữ liệu.

Không phân tích.

Không luận giải.

Không chấm điểm.

Không đưa khuyến nghị.

---

# 5. Thành phần

S03 gồm đúng 4 Pillar Card.

```
Năm

↓

Tháng

↓

Ngày (Nhật Chủ)

↓

Giờ
```

Mỗi Pillar Card hiển thị:

- Tên trụ.
- Thiên Can.
- Địa Chi.
- Ngũ hành của Can.
- Ngũ hành của Chi.
- Thời gian tương ứng (năm, tháng, ngày, giờ).

---

# 6. Nhật Trụ

Nhật Trụ là trọng tâm của S03.

Card Nhật Trụ phải nổi bật hơn ba Card còn lại bằng:

- Border nhấn.
- Màu nhấn.
- Nhãn "Nhật Chủ".

Không được thay đổi kích thước Card.

---

# 7. Mục tiêu thị giác

Người dùng phải quét theo thứ tự:

```
Năm

↓

Tháng

↓

Ngày (Nhật Chủ)

↓

Giờ
```

Đồng thời nhận ra ngay:

"Đây là Nhật Trụ."

---

# 8. Quan hệ với các Section khác

S03 là nguồn dữ liệu cho:

- S04 — Cân bằng Ngũ hành.
- S05 — Sức mạnh mệnh cục.
- S06 — Thập Thần.
- S07 — Thần Sát.

Không có dữ liệu nào trong S03 được tự suy diễn.

---

# 9. Tiêu chí hoàn thành

Một S03 đạt chuẩn khi:

✓ Bốn trụ hiển thị cân đối.

✓ Nhật Trụ nổi bật.

✓ Không có nội dung dư thừa.

✓ Dễ đối chiếu giữa các trụ.

✓ Bám sát Canonical Desktop.

---

# 10. Freeze Scope

Desktop là chuẩn.

Tablet và Mobile kế thừa Information Hierarchy.

Không thay đổi:

- Thứ tự bốn trụ.
- Cấu trúc mỗi Pillar Card.
- Nhật Trụ luôn ở vị trí thứ ba.

---

# 11. Deliverables

README.md

↓

S03_MASTER_LAYOUT.md

↓

Cursor Implementation

↓

Review

↓

Freeze

---

# 12. Freeze Statement

S03 là Section hiển thị dữ liệu gốc của lá số Bát Tự và là nền tảng cho toàn bộ hệ thống phân tích của BTE Platform.

Mọi triển khai Frontend và AI Coding Agent phải tuân thủ tài liệu này như tài liệu định nghĩa chính thức của Section S03.