# BTE Platform

# S07 — THẦN SÁT

## README.md

---

Version

1.0.0

Status

DESIGN

Module

Desktop Canonical UI

Section

S07

Name

Thần Sát

Owner

BTE Platform

---

# 1. Mục tiêu

S07 là khu vực giúp người dùng **nhận biết nhanh các Thần Sát quan trọng** đang xuất hiện trong lá số.

Khác với các tài liệu học thuật truyền thống liệt kê hàng chục hoặc hàng trăm Thần Sát, S07 chỉ trình bày những thông tin thực sự hữu ích đối với việc đọc lá số.

Mục tiêu của Section này là:

- Hiển thị các **Cát tinh** đang có.
- Hiển thị các **Hung tinh** đang có.
- Giúp người dùng đánh giá nhanh mức độ ảnh hưởng.
- Dẫn người dùng sang phần luận giải chi tiết nếu cần.

S07 không thay thế phần luận giải.

S07 chỉ đóng vai trò **Executive Summary** cho hệ thống Thần Sát.

---

# 2. Vai trò trong Customer Portal

S07 nằm sau:

- S06 — Thập Thần

và trước:

- S08 — Luận giải tổng hợp.

Luồng đọc chuẩn:

```
Tứ Trụ

↓

Ngũ hành

↓

Thập thần

↓

THẦN SÁT

↓

Luận giải
```

Điều này giúp người dùng:

Hiểu cấu trúc lá số

↓

Nhận biết các dấu hiệu đặc biệt

↓

Đọc luận giải.

---

# 3. Triết lý thiết kế

S07 tuân thủ triết lý:

**Hiểu trong vài giây.**

Người dùng không cần:

- nhớ tên hàng trăm Thần Sát;
- hiểu công thức tính;
- đọc tài liệu học thuật.

Người dùng chỉ cần biết:

- Có Cát tinh nào?
- Có Hung tinh nào?
- Có gì cần chú ý?

---

# 4. Những câu hỏi mà S07 phải trả lời

Trong vòng 5 giây, người dùng phải trả lời được:

✓ Tôi có bao nhiêu Cát tinh?

✓ Tôi có bao nhiêu Hung tinh?

✓ Những Thần Sát nổi bật là gì?

✓ Có điều gì đáng lưu ý không?

Nếu người dùng vẫn phải đọc toàn bộ danh sách để hiểu thì thiết kế chưa đạt.

---

# 5. Phạm vi hiển thị

S07 không hiển thị toàn bộ cơ sở dữ liệu Thần Sát.

Chỉ hiển thị:

- Các Thần Sát đã kích hoạt.
- Các Thần Sát quan trọng.
- Các Thần Sát có ảnh hưởng đáng kể.

Những Thần Sát còn lại sẽ nằm trong:

```
Xem toàn bộ →
```

---

# 6. Nội dung hiển thị

Section gồm hai nhóm chính:

## Cát tinh

Ví dụ:

- Thiên Ất Quý Nhân
- Thiên Đức Quý Nhân
- Nguyệt Đức Quý Nhân
- Văn Xương
- Hoa Cái

---

## Hung tinh

Ví dụ:

- Kiếp Sát
- Không Vong
- Cô Thần
- Quả Tú
- Đại Hao

Danh sách thực tế sẽ do Analysis Engine cung cấp.

---

# 7. Điều KHÔNG hiển thị

S07 không hiển thị:

✗ Điều kiện kích hoạt

✗ Công thức tính

✗ Điểm số

✗ Xác suất

✗ Giải thích dài

✗ Luận giải

✗ Ví dụ

Tất cả sẽ nằm trong màn hình chi tiết.

---

# 8. Reading Flow

Người dùng sẽ đọc theo thứ tự:

```
Tiêu đề

↓

Cát tinh

↓

Hung tinh

↓

Xem toàn bộ
```

Không có luồng đọc khác.

---

# 9. Pattern sử dụng

S07 sử dụng:

- PATTERN_06_INFORMATION_LIST

- PATTERN_07_STATUS_PANEL

S07 không sử dụng:

- Chart

- KPI

- Progress Bar

- Donut

- Gauge

---

# 10. Relationship với các Section khác

S07 nhận dữ liệu từ:

```
Analysis Engine

↓

ShenSha Engine

↓

S07
```

S07 không tự tính toán.

Chỉ hiển thị kết quả.

---

# 11. Trạng thái dữ liệu

Mỗi Thần Sát chỉ có ba trạng thái:

- Có

- Không có

- Chưa xác định

Không sử dụng thêm trạng thái khác.

---

# 12. Đối tượng người dùng

S07 phục vụ:

- Người mới học Bát Tự.

- Người dùng phổ thông.

- Chuyên gia.

- Người xem nhanh.

Không yêu cầu kiến thức nền.

---

# 13. Khả năng mở rộng

Trong tương lai có thể bổ sung:

- Mức độ ảnh hưởng.

- Phân loại theo lĩnh vực.

- Bộ lọc.

- Tìm kiếm.

- AI Explain.

Tuy nhiên cấu trúc Section vẫn giữ nguyên.

---

# 14. Mục tiêu UX

Người dùng phải:

✓ Nhìn thấy ngay các Cát tinh.

✓ Nhìn thấy ngay các Hung tinh.

✓ Không cần cuộn.

✓ Không cần đọc nhiều.

✓ Không cần hiểu thuật ngữ chuyên sâu.

---

# 15. Design Principles

Less Reading

↓

More Recognition

Information

↓

Knowledge

Knowledge

↓

Interpretation

Interpretation

↓

Decision

---

# 16. Acceptance Criteria

PASS khi:

✓ Người dùng nhận biết được Cát tinh và Hung tinh trong dưới 5 giây.

✓ Không phải đọc danh sách dài.

✓ Không có biểu đồ.

✓ Không có KPI.

✓ Có thể mở rộng.

✓ Đồng bộ với Desktop Canonical UI.

---

# 17. Freeze Policy

README.md chỉ mô tả:

- Vai trò.

- Mục tiêu.

- Triết lý.

Không mô tả:

- Layout.

- Grid.

- Typography.

- Khoảng cách.

Các nội dung đó sẽ nằm trong:

- `S07_MASTER_LAYOUT.md`
- `S07_MASTER_GRID_VI.md`
- `S07_MASTER_ANNOTATION_VI.md`

---

# 18. Design Decision Record

S07 được thiết kế theo hướng:

**Phân nhóm thông tin trước, giải thích sau.**

Thay vì liệt kê toàn bộ Thần Sát theo thứ tự kỹ thuật, giao diện ưu tiên câu hỏi mà người dùng thực sự quan tâm:

- Điều gì đang hỗ trợ tôi?
- Điều gì cần lưu ý?

Cách tổ chức này giúp giảm tải nhận thức, phù hợp với triết lý của BTE Platform:

**"Hiểu nhanh trước, đào sâu sau."**

---

# 19. Single Source of Truth

README.md là tài liệu định nghĩa:

- Vai trò.
- Phạm vi.
- Triết lý.
- Mục tiêu UX.

Mọi tài liệu thiết kế của S07 phải tuân thủ định hướng được mô tả trong tài liệu này.