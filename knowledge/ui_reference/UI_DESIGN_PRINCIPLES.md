# BTE Platform V1.0

# UI Design Principles

---

# Purpose

Đây là tài liệu định nghĩa các nguyên tắc thiết kế UI/UX của BTE Platform.

Mọi màn hình mới phải tuân thủ các nguyên tắc này trước khi được triển khai.

---

# Principle 01 — Information Before Decoration

Ưu tiên khả năng đọc và hiểu thông tin hơn hiệu ứng hoặc trang trí.

Một giao diện đẹp nhưng khó hiểu không đạt yêu cầu.

---

# Principle 02 — Executive Summary First

Thông tin quan trọng nhất luôn nằm ở phần đầu.

Người dùng phải hiểu kết quả tổng quan trong vài giây đầu.

---

# Principle 03 — Progressive Disclosure

Hiển thị theo từng tầng:

- Tóm tắt
- Phân tích
- Luận giải
- Kiến thức

Không hiển thị toàn bộ dữ liệu cùng lúc.

---

# Principle 04 — One Screen, One Primary Goal

Mỗi màn hình chỉ có một mục tiêu chính.

Ví dụ:

- Dashboard → Tổng quan.
- BaZi Result → Kết quả phân tích.
- Report → Báo cáo.

Không trộn nhiều mục tiêu trên cùng một màn hình.

---

# Principle 05 — Visual Hierarchy

Thông tin quan trọng phải nổi bật hơn thông tin phụ.

Kích thước, khoảng trắng và màu sắc phải phản ánh mức độ ưu tiên.

---

# Principle 06 — White Space is Functional

Khoảng trắng không phải khoảng trống.

Khoảng trắng giúp người dùng đọc nhanh và giảm tải nhận thức.

---

# Principle 07 — Design System First

Chỉ sử dụng Component Library và Design System của BTE.

Không tạo component mới nếu có thể tái sử dụng.

---

# Principle 08 — Consistency

Typography, màu sắc, icon, spacing và card phải thống nhất trên toàn bộ Portal.

---

# Principle 09 — Responsive by Default

Mọi màn hình phải được thiết kế cho:

- Desktop
- Laptop
- Tablet
- Mobile

Không coi Responsive là bước sửa lỗi sau cùng.

---

# Principle 10 — Accessibility

UI phải hỗ trợ:

- Keyboard Navigation
- Focus State
- ARIA
- Contrast
- Touch Target

---

# Principle 11 — Performance Aware

Không tạo giao diện gây render dư hoặc phụ thuộc vào dữ liệu không cần thiết.

---

# Principle 12 — Commercial Product Mindset

Đây là sản phẩm thương mại.

Mọi quyết định thiết kế phải ưu tiên:

- Dễ hiểu
- Dễ sử dụng
- Dễ bán
- Dễ mở rộng

---

# Principle 13 — Canonical UI

`CANONICAL_PORTAL_UI.md` là nguồn tham chiếu chính thức.

Mọi màn hình mới phải tương thích với Canonical UI.

---

# Principle 14 — Evolution Without Fragmentation

Được phép cải tiến giao diện.

Không được tạo thêm một phong cách thiết kế mới.

Mọi cải tiến phải hòa nhập với hệ thống hiện có.

---

# Principle 15 — Documentation Before Implementation

Trước khi thay đổi lớn về UI:

1. Cập nhật tài liệu.
2. Cập nhật ảnh tham chiếu (nếu cần).
3. Được Product Owner phê duyệt.
4. Sau đó mới triển khai.