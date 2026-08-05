# BTE Platform V1.0

# Work Package 06 — Four Pillars Card

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP06 |
| Name | Four Pillars Card |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Critical) |
| Estimated | 8–10 giờ |

---

# 1. Goal

Xây dựng khu vực hiển thị Tứ Trụ.

Đây là thành phần quan trọng nhất của toàn bộ giao diện Bát Tự.

Chỉ hiển thị dữ liệu.

Không thực hiện bất kỳ phép tính nào.

---

# 2. Scope

Bao gồm:

- Four Pillars Grid
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Na Yin (placeholder nếu chưa có)
- Trường Sinh (placeholder nếu chưa có)

Không bao gồm:

- Five Elements
- Strength
- Ten Gods
- Interpretation

---

# 3. Layout

```
                 TỨ TRỤ

+---------+---------+---------+---------+

|  Năm    |  Tháng  |  Ngày   |  Giờ    |

+---------+---------+---------+---------+

| Thiên Can |

| Địa Chi |

| Tàng Can |

| Nạp Âm |

| Trường Sinh |

+---------+---------+---------+---------+

```

---

# 4. Data Structure

Mỗi Pillar hiển thị:

- Heavenly Stem
- Earthly Branch
- Hidden Stems
- Na Yin
- Trường Sinh

Không tự tính toán.

Nhận dữ liệu từ API.

Nếu chưa có:

Mock Data.

---

# 5. Visual Rules

Mỗi Pillar phải:

- Kích thước bằng nhau.
- Card đồng nhất.
- Khoảng cách đều.
- Typography thống nhất.

Không dùng màu quá rực.

---

# 6. Future Ready

Thiết kế phải đủ chỗ để bổ sung:

- Thập Thần
- Thập Nhị Trường Sinh
- Tàng Can chi tiết
- Icon Ngũ Hành
- Tooltip giải thích

Không triển khai ở WP này.

Chỉ dự phòng không gian.

---

# 7. UX Rules

- Hover từng Pillar.
- Tooltip khi cần.
- Loading Skeleton.
- Empty State.
- Error State.

---

# 8. Responsive

Desktop

4 cột.

Tablet

2 × 2.

Mobile

4 hàng.

Không overflow.

---

# 9. Component Usage

Chỉ dùng:

- Card
- Badge
- Tooltip
- Divider
- Typography

Không tạo component mới nếu có thể tái sử dụng.

---

# 10. Coding Rules

- Không xử lý business logic.
- Không gọi API trực tiếp.
- Không hardcode dữ liệu.
- Tách FourPillarCard thành component độc lập.

---

# 11. Acceptance Criteria

PASS khi:

- Hiển thị đúng 4 Trụ.
- Responsive đạt yêu cầu.
- Build thành công.
- Không lỗi TypeScript.
- Có Loading, Empty và Error State.

---

# 12. Cursor Instructions

Cursor chỉ xây dựng giao diện Four Pillars.

Không triển khai tính toán.

Không sửa Engine.

Không sửa Rule Database.

Nếu dữ liệu chưa có:

→ sử dụng mock data.

→ ghi TODO để thay bằng dữ liệu thật sau khi tích hợp Analysis Engine.