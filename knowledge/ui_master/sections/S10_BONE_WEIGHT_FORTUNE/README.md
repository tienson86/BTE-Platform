# BTE Platform

# S10 — CÂN XƯƠNG ĐOÁN MỆNH

## README.md

---

Version

1.0.0

Status

DESIGN

Module

Desktop Canonical UI

Section

S10

Name

Cân Xương Đoán Mệnh

Owner

BTE Platform

Related Engine

Bone Weight Fortune Engine

---

# 1. Mục tiêu

S10 là Section hiển thị kết quả của hệ thống **Cân Xương Đoán Mệnh (稱骨算命)**.

Đây là một hệ thống luận mệnh độc lập với Bát Tự, sử dụng tổng trọng lượng của:

- Năm sinh
- Tháng sinh
- Ngày sinh
- Giờ sinh

để xác định tổng lượng (lượng/chỉ), từ đó tra cứu bài ca cân xương và đưa ra luận giải tương ứng.

Trong Desktop Canonical UI V1, S10 chỉ trình bày **kết quả cuối cùng**, không trình bày quá trình tính toán.

---

# 2. Vai trò trong Customer Portal

Luồng trải nghiệm của Desktop Canonical:

```
S01
Thông tin bản mệnh

↓

S02
Tổng quan

↓

S03
Tứ Trụ

↓

S04
Ngũ hành

↓

S05
Sức mạnh mệnh cục

↓

S06
Thập thần

↓

S07
Thần sát

↓

S08
Luận giải tổng hợp

↓

S09
Cung Phi / Quái Mệnh & Nhóm Trạch

↓

S10
Cân Xương Đoán Mệnh

↓

S11
...
```

S10 là phần bổ sung thêm một góc nhìn luận mệnh truyền thống để người dùng tham khảo.

---

# 3. Triết lý thiết kế

S10 phải trả lời nhanh ba câu hỏi:

- Tôi được bao nhiêu lượng?
- Mức đánh giá của lượng này là gì?
- Ý nghĩa tổng quát ra sao?

Người dùng không cần hiểu cách tính lượng.

Người dùng chỉ cần hiểu kết quả.

---

# 4. Những câu hỏi mà S10 phải trả lời

Sau khi đọc S10, người dùng phải biết:

✓ Tổng lượng cân xương.

✓ Mức đánh giá.

✓ Bài ca cân xương.

✓ Ý nghĩa tổng quát.

✓ Có thể đọc tiếp luận giải đầy đủ nếu muốn.

---

# 5. Vai trò của Bone Weight Fortune Engine

```
Ngày giờ sinh

↓

Bone Weight Fortune Engine

↓

Bone Weight Result

↓

S10
```

S10 không thực hiện tính toán.

Chỉ hiển thị kết quả đã được Engine trả về.

---

# 6. Phạm vi hiển thị

S10 chỉ hiển thị:

- Tổng lượng.
- Mức đánh giá.
- Bài ca cân xương.
- Luận giải ngắn.
- Liên kết xem đầy đủ.

Không hiển thị:

- Bảng tra trọng lượng.
- Công thức tính.
- Điểm từng trụ.
- Rule.
- Debug.
- Thuật toán.

---

# 7. Đối tượng sử dụng

S10 dành cho:

- Người dùng phổ thông.
- Người quan tâm đến Cân Xương Đoán Mệnh.
- Khách hàng doanh nghiệp.

Không yêu cầu kiến thức về thuật số.

---

# 8. Nguyên tắc nội dung

Mọi nội dung phải:

- Ngắn gọn.
- Dễ hiểu.
- Không thần bí hóa.
- Không tuyệt đối hóa.
- Không tạo cảm giác định mệnh.

Đây là thông tin tham khảo trong tổng thể hệ thống luận giải của BTE.

---

# 9. Executive Summary

Dashboard chỉ hiển thị:

- Kết quả.
- Bài ca.
- Luận giải tóm tắt.

Không thay thế báo cáo Cân Xương Đoán Mệnh đầy đủ.

---

# 10. Khả năng mở rộng

Desktop Canonical V1 chỉ triển khai:

- Kết quả cân xương.
- Bài ca.
- Luận giải ngắn.

Các tính năng như:

- Phân tích từng lượng.
- So sánh nhiều lá số.
- Giải thích chi tiết từng câu thơ.

sẽ được xem xét ở các phiên bản sau và **không nằm trong phạm vi của tài liệu này**.

---

# 11. Mục tiêu UX

Người dùng cần:

✓ Biết ngay kết quả.

✓ Hiểu ý nghĩa.

✓ Không phải đọc nhiều.

✓ Có thể đọc tiếp nếu muốn.

---

# 12. Acceptance Criteria

PASS khi:

✓ Tổng lượng nổi bật.

✓ Bài ca dễ đọc.

✓ Luận giải ngắn gọn.

✓ Không có dữ liệu kỹ thuật.

✓ Đồng bộ với Desktop Canonical UI.

---

# 13. Relationship

S10 sử dụng dữ liệu từ:

```
Bone Weight Fortune Engine
```

S10 độc lập với:

- Bát Tự.
- Thập thần.
- Thần sát.
- Cung Phi.

Đây là một hệ thống luận mệnh bổ sung trong BTE Platform.

---

# 14. Design Decision Record

S10 không được thiết kế như một tài liệu nghiên cứu.

S10 là **Executive Bone Weight Fortune Card**.

Triết lý thiết kế:

```
Tổng lượng

↓

Mức đánh giá

↓

Bài ca

↓

Luận giải

↓

Đọc đầy đủ
```

Người dùng phải hiểu được kết quả trong vòng vài giây.

---

# 15. Single Source of Truth

README.md định nghĩa:

- Vai trò.
- Phạm vi.
- Mục tiêu.
- Triết lý.
- Trải nghiệm người dùng.

Các tài liệu:

- S10_MASTER_LAYOUT.md
- S10_MASTER_GRID_VI.md
- S10_MASTER_ANNOTATION_VI.md

phải tuân thủ hoàn toàn tài liệu này.

---

# 16. Freeze Policy

README.md không quy định:

- Layout.
- Grid.
- Typography.
- Spacing.
- Màu sắc.

Các nội dung này sẽ được định nghĩa trong các tài liệu thiết kế tiếp theo.

README.md là tài liệu nền tảng của toàn bộ Section S10 và chỉ được thay đổi khi có quyết định chính thức về phạm vi sản phẩm.