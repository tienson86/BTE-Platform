# COMMERCIAL DASHBOARD
# 00_NAVIGATION
# CANONICAL PORTAL NAVIGATION V1.0

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

TV1-B07A amendment (approved): the live Customer Portal header
exposes a fourth primary item, "Tư vấn hôn nhân" → `/marriage-consulting`.
This is a visible primary nav item, not a dropdown and not a header-action.
The original three destinations and routes are unchanged.

---

# 1. Mục đích

Tài liệu này định nghĩa cấu trúc điều hướng (Navigation) chính thức của Customer Portal.

Đây là nguồn tham chiếu duy nhất cho:

- Header Navigation
- Routing
- Sidebar (nếu có)
- Mobile Navigation
- Điều hướng giữa các màn hình

Mọi thay đổi Navigation đều phải cập nhật tài liệu này trước khi triển khai.

---

# 2. Triết lý điều hướng

Customer Portal chỉ phục vụ khách hàng.

Navigation phải:

- đơn giản;
- dễ hiểu;
- ít mục;
- không chứa chức năng quản trị.

Khách hàng không cần nhìn thấy:

- Báo cáo
- Lịch sử
- Quản trị
- Debug
- System

Các chức năng này thuộc Admin Portal.

---

# 3. Navigation chính

Portal V1 có 4 màn hình chính (TV1-B07A).

```
Trang chủ
↓

Chọn ngày tốt
↓

Xem lá số
↓

Tư vấn hôn nhân
```

Không dùng dropdown / grouped navigation cho ticket này.
Không thêm mục quản trị.

---

# 4. Trang chủ

Tên hiển thị:

```
Trang chủ
```

Ý nghĩa:

```
Xem ngày tốt / xấu
```

Đây là Landing Page của toàn bộ Portal.

Route:

```
/
```

Hoặc

```
/home
```

Tùy kiến trúc hiện tại.

---

# 5. Chức năng Trang chủ

Trang chủ hiển thị:

- Lịch tháng
- Ngày tốt
- Ngày xấu
- Tiết khí
- Can Chi
- Âm lịch
- Thông tin ngày

Người dùng có thể chọn một ngày để xem chi tiết.

Không hiển thị Dashboard Bát Tự.

---

# 6. Chọn ngày tốt

Tên hiển thị:

```
Chọn ngày tốt
```

Route:

```
/good-date
```

Mục tiêu:

Tìm ngày phù hợp theo mục đích.

Ví dụ:

- Khai trương
- Động thổ
- Cưới hỏi
- Ký hợp đồng
- Xuất hành
- Nhập trạch

Người dùng chọn mục đích.

Hệ thống trả về danh sách ngày phù hợp.

---

# 7. Xem lá số

Tên hiển thị:

```
Xem lá số
```

Route:

```
/view-chart
```

Đây là màn hình nhập dữ liệu.

Không hiển thị kết quả.

Không hiển thị Dashboard.

Người dùng nhập:

- Họ tên
- Giới tính
- Ngày sinh
- Giờ sinh
- Nơi sinh

↓

PHÂN TÍCH LÁ SỐ

---

# 7A. Tư vấn hôn nhân (TV1-B07A)

Tên hiển thị:

```
Tư vấn hôn nhân
```

Route:

```
/marriage-consulting
```

Đây là mục điều hướng chính thứ tư, được duyệt cho TV1-B07A.

Không thay thế Trang chủ, Chọn ngày tốt, hoặc Xem lá số.

Không dùng dropdown.

---

# 8. Luồng xem lá số

```
Xem lá số

↓

Nhập thông tin

↓

PHÂN TÍCH LÁ SỐ

↓

Loading

↓

Dashboard kết quả
```

Không mở cửa sổ mới.

Không Popup.

Không Tab mới.

---

# 9. Dashboard kết quả

Dashboard KHÔNG phải menu.

Dashboard là kết quả của hành động:

```
PHÂN TÍCH LÁ SỐ
```

Người dùng không vào Dashboard nếu chưa có dữ liệu.

Dashboard chỉ tồn tại sau khi phân tích thành công.

---

# 10. Điều hướng Dashboard

Từ Dashboard người dùng có thể:

- Quay lại Xem lá số
- Phân tích lá số khác
- Chia sẻ
- In
- Xuất PDF

Không quay về Landing Page nếu không cần.

---

# 11. Header Navigation

```
------------------------------------------------------------

Logo

Trang chủ

Chọn ngày tốt

Xem lá số

Tư vấn hôn nhân

[ Dark ]

[ Thông báo ]

[ Hồ sơ ]

------------------------------------------------------------
```

Không hiển thị:

- Báo cáo
- Lịch sử

---

# 12. User Menu

Menu người dùng:

- Hồ sơ
- Đổi mật khẩu
- Đăng xuất

Không chứa:

- Báo cáo
- Lịch sử
- Admin

---

# 13. Admin Portal

Các chức năng sau thuộc Admin:

- Báo cáo
- Lịch sử
- Quản lý khách hàng
- Quản lý dữ liệu
- Quản lý Export
- Quản lý Knowledge
- Nhật ký hệ thống

Không hiển thị trong Customer Portal.

---

# 14. Navigation Rules

Rule 1

Không quá 4 menu chính (TV1-B07A approved fourth item: Tư vấn hôn nhân).

---

Rule 2

Dashboard không phải menu.

Dashboard là kết quả.

---

Rule 3

Một màn hình chỉ có một nhiệm vụ.

---

Rule 4

Không hiển thị chức năng quản trị.

---

Rule 5

Không yêu cầu người dùng học Navigation.

Navigation phải tự nhiên.

---

# 15. Routing

```
/

↓

Trang chủ
```

```
/good-date

↓

Chọn ngày tốt
```

```
/analyze

↓

Xem lá số
```

```
/marriage-consulting

↓

Tư vấn hôn nhân
```

```
/result/{analysis_id}

↓

Dashboard kết quả
```

Dashboard không được truy cập trực tiếp nếu chưa có dữ liệu.

---

# 16. Mobile Navigation

Mobile giữ nguyên 4 mục:

- Trang chủ
- Chọn ngày tốt
- Xem lá số
- Tư vấn hôn nhân

Dashboard mở toàn màn hình.

Không tạo Navigation riêng.

---

# 17. Acceptance Checklist

✓ Chỉ có 4 menu chính (TV1-B07A: Tư vấn hôn nhân is the approved fourth item).

✓ Dashboard không phải menu.

✓ Báo cáo không xuất hiện.

✓ Lịch sử không xuất hiện.

✓ Admin tách riêng.

✓ Điều hướng không quá 2 bước để đến Dashboard.

✓ Không có màn hình Welcome riêng.

✓ Landing Page là Xem ngày tốt / xấu.

---

# 18. Future Expansion

Navigation V1 được phép mở rộng.

TV1-B07A is the approved architecture decision for a fourth
primary item: Tư vấn hôn nhân → `/marriage-consulting`.

Further modules should still prefer grouping under existing items
rather than adding more primary menu entries without a new decision.
