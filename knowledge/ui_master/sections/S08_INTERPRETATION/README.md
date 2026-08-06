# BTE Platform

# S08 — LUẬN GIẢI TỔNG HỢP

## README.md

---

Version

1.0.0

Status

DESIGN

Module

Desktop Canonical UI

Section

S08

Name

Luận giải tổng hợp

Owner

BTE Platform

Related Engine

Interpretation Engine

---

# 1. Mục tiêu

S08 là Section quan trọng nhất của toàn bộ Customer Portal.

Đây là nơi hệ thống chuyển đổi toàn bộ kết quả phân tích kỹ thuật thành ngôn ngữ tự nhiên mà người dùng có thể hiểu ngay.

Khác với các Section trước chỉ hiển thị dữ liệu hoặc chỉ số, S08 trình bày **kết luận tổng hợp**, giúp người dùng nắm được bản chất của lá số chỉ sau vài giây.

S08 không thay thế báo cáo chi tiết.

S08 đóng vai trò **Executive Interpretation** của toàn bộ hệ thống.

---

# 2. Vai trò trong Customer Portal

Luồng trải nghiệm chuẩn:

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
Sức mạnh

↓

S06
Thập thần

↓

S07
Thần sát

↓

S08
LUẬN GIẢI TỔNG HỢP

↓

Báo cáo chi tiết
```

Tất cả dữ liệu trước đó đều hội tụ tại S08.

---

# 3. Triết lý thiết kế

S08 được xây dựng theo nguyên tắc:

**Data → Insight → Decision**

Không hiển thị dữ liệu thô.

Không hiển thị Rule.

Không hiển thị Score.

Không hiển thị Logic.

Chỉ hiển thị kết luận.

---

# 4. Những câu hỏi mà S08 phải trả lời

Người dùng phải hiểu ngay:

✓ Tôi là người như thế nào?

✓ Điểm mạnh nổi bật nhất là gì?

✓ Điểm yếu cần lưu ý là gì?

✓ Điều gì ảnh hưởng lớn nhất đến cuộc đời tôi?

✓ Tôi nên làm gì tiếp theo?

Nếu sau khi đọc S08 người dùng vẫn chưa hiểu lá số thì Section chưa đạt yêu cầu.

---

# 5. Vai trò của Interpretation Engine

S08 là giao diện hiển thị kết quả của:

```
Analysis Engine

↓

Rule Engine

↓

Interpretation Engine

↓

S08
```

S08 không thực hiện bất kỳ phép tính nào.

S08 chỉ trình bày kết quả đã được tổng hợp.

---

# 6. Phạm vi hiển thị

S08 chỉ hiển thị:

- Tổng luận.
- Điểm mạnh.
- Điểm cần lưu ý.
- Gợi ý hành động.
- Liên kết tới luận giải đầy đủ.

Không hiển thị:

- Rule.
- Công thức.
- Điều kiện kích hoạt.
- Điểm số.
- JSON.
- Debug.

---

# 7. Nội dung chính

Section gồm bốn phần:

## 1. Tổng luận

Một đoạn tóm tắt ngắn.

Khoảng:

80–120 từ.

Giúp người dùng hiểu bản chất của lá số.

---

## 2. Điểm mạnh

Ví dụ:

- Khả năng lãnh đạo.
- Quyết đoán.
- Tinh thần trách nhiệm.
- Ý chí mạnh.
- Tư duy chiến lược.

---

## 3. Điểm cần lưu ý

Ví dụ:

- Dễ nóng vội.
- Hỏa quá mạnh.
- Thiếu yếu tố Thủy.
- Khó kiểm soát cảm xúc.

---

## 4. Gợi ý hành động

Ví dụ:

- Phát triển lĩnh vực quản lý.
- Tăng yếu tố Thủy trong môi trường sống.
- Ưu tiên làm việc theo nhóm.
- Kiểm soát cảm xúc trước khi quyết định.

---

# 8. Những điều KHÔNG hiển thị

Không hiển thị:

✗ Luận giải dài nhiều trang.

✗ Toàn bộ báo cáo PDF.

✗ Thống kê.

✗ Biểu đồ.

✗ KPI.

✗ Rule ID.

✗ Engine Output.

---

# 9. Reading Flow

Người dùng đọc theo thứ tự:

```
Header

↓

Tổng luận

↓

Điểm mạnh

↓

Điểm cần lưu ý

↓

Gợi ý hành động

↓

Đọc luận giải đầy đủ
```

Đây là Reading Flow duy nhất.

---

# 10. Đối tượng sử dụng

S08 phục vụ:

- Người mới tìm hiểu Bát Tự.
- Người dùng phổ thông.
- Chuyên gia.
- Khách hàng doanh nghiệp.

Không yêu cầu người dùng có kiến thức chuyên môn.

---

# 11. Nguyên tắc nội dung

Mọi câu văn phải:

- Ngắn gọn.
- Dễ hiểu.
- Chính xác.
- Không phóng đại.
- Không gây lo lắng.
- Không mâu thuẫn với dữ liệu phân tích.

---

# 12. Executive Summary

Dashboard chỉ hiển thị phần tóm tắt.

Nếu người dùng muốn đọc sâu hơn:

```
Đọc luận giải đầy đủ →
```

sẽ chuyển sang màn hình Report.

Dashboard không thay thế Report.

---

# 13. Khả năng mở rộng

Trong tương lai có thể bổ sung:

- AI Rewrite.
- Giải thích theo lĩnh vực.
- Giải thích theo độ tuổi.
- Giải thích theo Đại vận.
- Giải thích theo Lưu niên.
- Giải thích theo ngôn ngữ.

Kiến trúc của S08 phải hỗ trợ mở rộng mà không cần thay đổi bố cục.

---

# 14. Mục tiêu UX

Người dùng phải:

✓ Hiểu được bản chất lá số trong dưới 30 giây.

✓ Không bị quá tải thông tin.

✓ Không phải đọc báo cáo dài.

✓ Có định hướng rõ ràng cho bước tiếp theo.

---

# 15. Design Principles

Interpretation

↓

Decision

↓

Action

Không dừng ở việc mô tả.

Phải dẫn tới hành động.

---

# 16. Acceptance Criteria

PASS khi:

✓ Người dùng hiểu được ý nghĩa của lá số.

✓ Nội dung ngắn gọn.

✓ Có cấu trúc rõ ràng.

✓ Không có dữ liệu kỹ thuật.

✓ Đồng bộ với Desktop Canonical UI.

---

# 17. Relationship với các Section khác

S08 là điểm hội tụ của:

- S03 — Tứ Trụ.
- S04 — Ngũ hành.
- S05 — Sức mạnh Mệnh cục.
- S06 — Thập thần.
- S07 — Thần sát.

Đồng thời là điểm khởi đầu của:

- Report Engine.
- PDF Report.
- AI Explanation.

---

# 18. Design Decision Record

S08 không được thiết kế như một bài viết dài.

S08 là **Executive Interpretation Card**.

Người dùng phải:

- Nhìn nhanh.
- Hiểu nhanh.
- Quyết định nhanh.

Sau đó mới chuyển sang phần luận giải đầy đủ nếu có nhu cầu.

Đây là triết lý cốt lõi của BTE Platform:

**"Hiểu trước – Đào sâu sau."**

---

# 19. Single Source of Truth

README.md là tài liệu định nghĩa:

- Vai trò.
- Phạm vi.
- Triết lý.
- Mục tiêu.
- Luồng trải nghiệm.

Các tài liệu:

- `S08_MASTER_LAYOUT.md`
- `S08_MASTER_GRID_VI.md`
- `S08_MASTER_ANNOTATION_VI.md`

phải tuân thủ định hướng được mô tả trong tài liệu này.

---

# 20. Freeze Policy

README.md không mô tả:

- Layout.
- Typography.
- Grid.
- Khoảng cách.
- Màu sắc.

Các nội dung này sẽ được đặc tả trong các tài liệu thiết kế tiếp theo.

README.md là tài liệu nền tảng của toàn bộ Section S08 và sẽ chỉ được cập nhật khi có thay đổi về mục tiêu sản phẩm hoặc triết lý thiết kế.