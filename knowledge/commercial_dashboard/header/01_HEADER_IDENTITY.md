# COMMERCIAL DASHBOARD
# HEADER 01
# IDENTITY HEADER
# THẺ ĐỊNH DANH LÁ SỐ

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Identity Header là phần đầu tiên của Dashboard.

Đây không phải là một Card phân tích.

Đây là khu vực nhận diện (Identity Layer) của toàn bộ Dashboard.

Nhiệm vụ của Header là:

- xác nhận đúng lá số;
- hiển thị thông tin nền tảng;
- tạo niềm tin trước khi người dùng bước vào phần phân tích.

Header không đưa ra:

- kết luận;
- luận giải;
- khuyến nghị.

Các nội dung đó thuộc Dashboard Body.

---

# 2. Vai trò

Identity Header trả lời duy nhất một câu hỏi:

> "Đây là lá số của ai?"

Dashboard Body mới trả lời:

> "Lá số này nói lên điều gì?"

Hai nhiệm vụ này tuyệt đối không được trộn lẫn.

---

# 3. Kiến trúc

Identity Header gồm bốn vùng thông tin.

```
┌──────────────────────────────────────────────────────────────────────────────┐

A                     B                           C                    D

Identity         Four Pillars              Foundation             Status

└──────────────────────────────────────────────────────────────────────────────┘
```

Tỷ lệ Desktop:

```
15%

45%

20%

20%
```

Header không được vượt quá khoảng 20–22% chiều cao của Dashboard.

---

# 4. Vùng A — Identity

Đây là vùng xác nhận người được phân tích.

Hiển thị:

- Họ và tên
- Giới tính
- Ngày sinh dương lịch
- Ngày sinh âm lịch
- Giờ sinh
- Nơi sinh

Đây là nhóm dữ liệu nhận diện.

Không có dữ liệu phân tích.

---

# 5. Vùng B — Four Pillars

Đây là trung tâm của Header.

Hiển thị đúng cấu trúc truyền thống.

```
            Năm

Tháng

Ngày

Giờ

Thiên Can

Địa Chi
```

Ngay dưới bảng:

### Nhật Chủ

Ví dụ:

```
CANH KIM

Dương Kim
```

Nhật Chủ luôn được nhấn mạnh.

Đây là trung tâm của toàn bộ lá số.

---

# 6. Vùng C — Foundation

Đây là nhóm thông tin nền.

Bao gồm:

- Nạp Âm
- Cung Phi
- Mệnh Quái
- Nhóm Trạch
- Tiết khí

Đây là các thông tin khách hàng thường muốn biết ngay.

Không hiển thị dưới dạng bảng lớn.

Ưu tiên trình bày dạng Badge hoặc Key–Value.

---

# 7. Vùng D — Analysis Status

Đây là vùng dành cho việc theo dõi và kiểm chứng.

Hiển thị:

- Mã phân tích
- Phiên bản Engine
- Ngày phân tích
- Thời gian tạo báo cáo
- Độ tin cậy phân tích (nếu có)

Đây không phải vùng dành cho tư vấn.

Kích thước nhỏ hơn các vùng còn lại.

---

# 8. Quy tắc hiển thị

Header luôn hiển thị đầy đủ.

Không Collapse.

Không Accordion.

Không Tab.

Header luôn xuất hiện ở đầu Dashboard.

---

# 9. Không hiển thị

Identity Header không hiển thị:

- Ngũ Hành
- Thập Thần
- Mệnh Cục
- Đại Vận
- Thần Sát
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Luận giải
- Khuyến nghị

Các nội dung này thuộc Dashboard Body.

---

# 10. Visual Hierarchy

Ưu tiên thị giác:

1. Nhật Chủ
2. Tứ Trụ
3. Thông tin cá nhân
4. Foundation
5. Status

Không để Status nổi bật hơn Nhật Chủ.

Không để Foundation nổi bật hơn Tứ Trụ.

---

# 11. Responsive

## Desktop

Hiển thị đủ bốn vùng trên một hàng.

## Tablet

A + B

↓

C + D

## Mobile

A

↓

B

↓

C

↓

D

Giữ nguyên thứ tự.

---

# 12. PDF Mapping

PDF phải giữ nguyên cấu trúc Header.

Không chuyển sang dạng văn bản thuần.

Header luôn nằm ở đầu báo cáo.

---

# 13. Accessibility

- Nhật Chủ có kích thước chữ lớn nhất trong Header.
- Tiêu đề từng vùng rõ ràng.
- Khoảng trắng đủ để phân biệt bốn vùng.
- Không dùng màu sắc làm phương tiện phân biệt duy nhất.

---

# 14. Customer Value

Sau khi nhìn Identity Header trong khoảng 10 giây, khách hàng phải biết:

✓ Đây đúng là lá số của mình.

✓ Nhật Chủ là gì.

✓ Tứ Trụ ra sao.

✓ Thuộc Cung Phi và Nhóm Trạch nào.

Đây là nền tảng để tiếp tục đọc Dashboard.

---

# 15. Design Principles

Identity Header tuân thủ:

- Dashboard First
- One Source of Truth
- Confidence Before Complexity
- First Impression Moment

Identity Header không dùng để phân tích.

Identity Header dùng để tạo niềm tin.

---

# 16. Acceptance Checklist

□ Header nằm trên cùng của Dashboard.

□ Không cao quá 20–22% chiều cao màn hình Desktop.

□ Có đủ bốn vùng A–B–C–D.

□ Nhật Chủ là điểm nhấn thị giác lớn nhất.

□ Tứ Trụ hiển thị đúng dạng truyền thống.

□ Foundation hiển thị ngắn gọn.

□ Status nhỏ gọn và không gây mất tập trung.

□ Portal, PDF và DOCX sử dụng cùng cấu trúc Header.

□ Không chứa dữ liệu phân tích hay khuyến nghị.