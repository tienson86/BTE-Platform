# 13. INFORMATION VISUALIZATION

Version: V1.0

Status: DESIGN FOUNDATION

Module:

knowledge/ui_system/

---

# 1. Purpose

Tài liệu này định nghĩa toàn bộ nguyên tắc trực quan hóa dữ liệu (Information Visualization) của BTE Platform.

Mục tiêu của Visualization không phải là "trang trí Dashboard".

Mục tiêu là:

> Giúp khách hàng hiểu nhanh hơn những gì Narrative đang muốn truyền đạt.

Visualization luôn đóng vai trò hỗ trợ Narrative.

Visualization không thay thế Narrative.

---

# 2. Core Philosophy

Narrative giải thích bằng ngôn ngữ.

Visualization giải thích bằng hình ảnh.

Hai thành phần phải hỗ trợ lẫn nhau.

Không được mâu thuẫn.

---

# 3. Design Goals

Visualization phải đạt:

- Dễ hiểu
- Trung thực
- Đẹp
- Nhất quán
- Không gây hiểu nhầm
- Hỗ trợ tư vấn

Không được:

- quá nhiều màu
- quá nhiều hiệu ứng
- quá nhiều biểu đồ
- gây cảm giác "dashboard kỹ thuật"

---

# 4. Visualization Hierarchy

Không phải mọi dữ liệu đều cần biểu đồ.

Ưu tiên:

Level 1

Insight

↓

Level 2

Relationship

↓

Level 3

Evidence

↓

Level 4

Metadata

---

# 5. Visualization Selection Matrix

| Loại dữ liệu | Visualization |
|--------------|---------------|
| Thành phần | Bar |
| Phân bố | Stacked Bar |
| Xu hướng | Timeline |
| Quy trình | Flow Diagram |
| Quan hệ | Relationship Diagram |
| So sánh | Comparison Grid |
| Mức độ | Progress Bar |
| Thứ tự | Timeline |
| Phân cấp | Tree |

Không sử dụng Pie Chart mặc định.

Radar Chart chỉ khi thực sự cần.

3D Chart bị cấm.

---

# 6. Five Elements Visualization

Five Elements không phải biểu đồ thống kê.

Đây là Balance Visualization.

Hiển thị:

- Mộc
- Hỏa
- Thổ
- Kim
- Thủy

theo đúng thứ tự Ngũ Hành.

Không sắp xếp theo giá trị lớn nhất.

Không dùng Pie.

Không dùng Radar.

Biểu đồ ưu tiên:

Horizontal Balance Bars.

Hiển thị:

- số lượng
- màu hành
- nhãn

Narrative giải thích ý nghĩa.

Biểu đồ chỉ thể hiện phân bố.

---

# 7. BaZi Visualization

BaZi là cấu trúc.

Không phải bảng.

Hiển thị:

Thiên Can

↓

Địa Chi

↓

Tàng Can

↓

Thập Thần

↓

Trường Sinh

Quan hệ giữa các tầng phải nhìn thấy ngay.

Không chỉ đọc được.

---

# 8. Ten Gods Visualization

Không biểu diễn "điểm".

Không biểu diễn "xếp hạng".

Hiển thị:

Lộ Can

↓

Tàng Can

↓

Quan hệ

Nếu sau này có Capability Map,

đó là lớp Visualization,

không phải dữ liệu.

---

# 9. Pattern Visualization

Pattern nên hiển thị:

Formation Flow

Ví dụ:

Nguyệt Lệnh

↓

Thông Căn

↓

Lộ Can

↓

Thành Cách

Flow này giúp khách hàng hiểu:

"Mệnh Cục hình thành như thế nào."

Không thay Narrative.

---

# 10. Luck Visualization

Đại Vận không phải bảng.

Đại Vận là Timeline.

Hiển thị:

Khởi vận

↓

10 Đại Vận

↓

Hiện tại

↓

Tiếp theo

Current luôn nổi bật.

Không dùng bảng thuần.

---

# 11. ShenSha Visualization

Thần Sát không dùng biểu đồ.

Ưu tiên:

Tag

↓

Chip

↓

Grouped List

Nếu có nhiều hơn 8 mục,

gom nhóm.

Không dùng điểm.

---

# 12. Overview Visualization

Overview là Hero.

Không có biểu đồ lớn.

Chỉ:

Insight

↓

Executive Summary

↓

Top Priority

↓

Supporting Metrics

Overview không cạnh tranh với phần phân tích.

---

# 13. Action Visualization

Action không phải Bullet List.

Ưu tiên:

Priority Card

↓

Action Cards

↓

Warnings

↓

Current Period

Mỗi Action nên là một Card nhỏ.

---

# 14. Relationship Visualization

Dùng khi cần giải thích quan hệ.

Ví dụ:

Pattern

↓

Strength

↓

Useful God

↓

Decision

↓

Action

Không dùng cho khách hàng mặc định.

Narrative Studio có thể dùng.

---

# 15. Timeline Visualization

Áp dụng cho:

- Đại Vận
- Release
- Certification History
- Golden History

Timeline phải đọc từ trái sang phải.

Current luôn nổi bật.

---

# 16. Comparison Visualization

Áp dụng:

Pack05

↓

Narrative V2

Hoặc:

Golden

↓

Current

Side-by-side.

Không dùng Overlay.

---

# 17. Color Rules

Visualization sử dụng Color System của UI-13.

Màu không mang ý nghĩa Tốt/Xấu.

Màu chỉ mang:

- phân loại
- trạng thái
- hành

Không dùng đỏ = xấu.

Không dùng xanh = tốt.

---

# 18. Motion Rules

Animation chỉ hỗ trợ nhận thức.

Không dùng animation để gây chú ý.

Transition:

120ms

200ms

320ms

theo UI-13.

---

# 19. Accessibility

Biểu đồ phải đọc được khi:

- không phân biệt màu
- phóng to
- màn hình nhỏ

Không dựa hoàn toàn vào màu.

Luôn có Label.

---

# 20. Responsive Strategy

Desktop

→ đầy đủ

Tablet

→ rút gọn

Mobile

→ ưu tiên Narrative trước Visualization

Không ép biểu đồ vào màn hình nhỏ.

---

# 21. Anti-patterns

Không dùng:

- 3D Charts
- Gauge
- Speedometer
- Donut quá nhiều
- Radar mặc định
- Heatmap cho khách hàng
- Biểu đồ chỉ để "đẹp"

Mọi Visualization đều phải có giá trị giải thích.

---

# 22. Validation Rules

Một Visualization đạt chuẩn khi:

✓ Trung thực với dữ liệu

✓ Không làm thay đổi Meaning

✓ Hỗ trợ Narrative

✓ Đọc được trong 3 giây

✓ Không cần giải thích cách đọc

---

# 23. Information Before Decoration

BTE là hệ thống tư vấn.

Không phải triển lãm đồ họa.

Ưu tiên:

Hiểu

↓

Tin

↓

Đẹp

Không ưu tiên:

Đẹp

↓

Khó hiểu

---

# 24. Single Visualization Principle

Một Card

↓

Một thông điệp trực quan chính.

Không cố hiển thị nhiều biểu đồ trong cùng một Card.

---

# 25. Narrative First Principle

Visualization luôn phục vụ Narrative.

Không Narrative nào được viết để giải thích cho biểu đồ.

Biểu đồ được tạo ra để hỗ trợ Narrative.

---

# 26. Visual Trust Principle

Khách hàng phải cảm nhận:

- dữ liệu rõ ràng;
- biểu đồ trung thực;
- bố cục khoa học;
- sản phẩm chuyên nghiệp.

Visualization không nhằm gây ấn tượng bằng hiệu ứng.

Visualization nhằm tăng niềm tin vào kết quả tư vấn.

---

# 27. Final Principle

Information Visualization tồn tại để giúp khách hàng hiểu nhanh hơn.

Không phải để Dashboard đẹp hơn.

Một Visualization thành công là khi khách hàng:

- nhìn nhanh;
- hiểu đúng;
- tin tưởng Narrative;

mà không cần học cách đọc biểu đồ.