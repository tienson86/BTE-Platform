Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

BaZi Card trình bày cấu trúc đầy đủ của lá số Bát Tự.

Đây là Card kỹ thuật nhất trong toàn bộ Dashboard.

Mục tiêu của Card là:

- trình bày cấu trúc Bát Tự;
- giúp chuyên gia kiểm chứng;
- giúp khách hàng quan sát toàn bộ cấu trúc mệnh.

Card này không đưa ra:

- kết luận;
- khuyến nghị;
- luận giải.

Những nội dung đó thuộc các Card khác.

---

# 2. Vai trò

BaZi Card là Card "Evidence".

Overview nói:

"Tôi là người như thế nào."

BaZi chứng minh:

"Tại sao lại có kết luận đó."

Đây là Card nền tảng của toàn bộ Dashboard.

---

# 3. Business Question

Card chỉ trả lời:

> "Cấu trúc Bát Tự của tôi như thế nào?"

Không trả lời:

- Tôi mạnh hay yếu.
- Tôi nên làm gì.
- Đại vận tốt hay xấu.

---

# 4. Customer Value

Sau khi xem Card này.

Khách hàng phải hiểu:

✓ Lá số gồm bốn trụ.

✓ Nhật Chủ nằm ở đâu.

✓ Thiên Can và Địa Chi gồm những gì.

✓ Tàng Can và Trường Sinh là gì.

Không cần hiểu thuật toán.

Chỉ cần nhận diện cấu trúc.

---

# 5. Dữ liệu đầu vào

Nguồn dữ liệu:

Canonical Analysis

Không lấy dữ liệu từ:

- Commercial Knowledge
- Commercial Composer
- Interpretation

Card không tự tính toán.

---

# 6. Thành phần hiển thị

Card hiển thị đầy đủ sáu tầng dữ liệu.

---

## 6.1 Thiên Can

```
Năm

Tháng

Ngày

Giờ
```

Hiển thị:

- Can
- Ngũ hành
- Âm Dương

---

## 6.2 Địa Chi

Hiển thị:

- Chi
- Ngũ hành
- Âm Dương

---

## 6.3 Nạp Âm

Hiển thị đủ bốn trụ.

Ví dụ:

Lư Trung Hỏa

Bích Thượng Thổ

Lộ Bàng Thổ

Thành Đầu Thổ

Không rút gọn.

---

## 6.4 Tàng Can

Hiển thị đầy đủ từng Chi.

Ví dụ:

Dần

↓

Giáp

Bính

Mậu

Không chỉ hiển thị một Can.

Không Collapse mặc định.

---

## 6.5 Thập Thần

Hiển thị đúng từng trụ.

Ví dụ:

Thất Sát

Kiếp Tài

Nhật Chủ

Thiên Ấn

Không phân tích.

---

## 6.6 Trường Sinh

Hiển thị:

- Trường Sinh
- Mộc Dục
- Quan Đới
- Lâm Quan
...

theo đúng kết quả phân tích.

Không giải thích.

---

# 7. Không hiển thị

BaZi Card không hiển thị:

- Thân vượng
- Dụng thần
- Hỷ thần
- Kỵ thần
- Đại vận
- Ngũ hành
- Luận giải
- Khuyến nghị

---

# 8. Cấu trúc giao diện

```
────────────────────────────

BÁT TỰ

────────────────────────────

           Năm

Tháng

Ngày

Giờ

────────────────────────────

Thiên Can

Địa Chi

────────────────────────────

Nạp Âm

────────────────────────────

Tàng Can

────────────────────────────

Thập Thần

────────────────────────────

Trường Sinh

────────────────────────────
```

Không chia nhiều Card nhỏ.

Đây là một Card duy nhất.

---

# 9. Visual Priority

Mức ưu tiên:

★★★★☆

Đây là Core Analysis Card.

Không phải Hero.

Không phải Decision.

---

# 10. UX Rules

Người dùng có thể đọc từ trên xuống.

Không phải mở Tab.

Không Accordion.

Không Popup.

Không Hover mới thấy dữ liệu.

Toàn bộ cấu trúc phải nhìn thấy ngay.

---

# 11. Presentation Rules

Ưu tiên:

- bảng;
- khoảng trắng;
- căn cột.

Không dùng:

- biểu đồ;
- Gauge;
- Progress.

Đây là Card dữ liệu.

---

# 12. PDF Mapping

Portal

↓

PDF

↓

DOCX

hiển thị giống nhau.

Không đổi thứ tự.

---

# 13. Mobile

Mobile vẫn giữ:

Thiên Can

↓

Địa Chi

↓

Nạp Âm

↓

Tàng Can

↓

Thập Thần

↓

Trường Sinh

Không lược bỏ dữ liệu.

---

# 14. Design Principles

BaZi Card tuân thủ:

- One Source of Truth
- Confidence Before Complexity
- Progressive Disclosure

Đây là Card kiểm chứng.

Không phải Card kết luận.

---

# 15. Acceptance Checklist

□ Có đủ bốn trụ.

□ Có Thiên Can.

□ Có Địa Chi.

□ Có Nạp Âm.

□ Có Tàng Can.

□ Có Thập Thần.

□ Có Trường Sinh.

□ Không có dữ liệu luận giải.

□ Không có khuyến nghị.

□ Portal và PDF giống nhau.