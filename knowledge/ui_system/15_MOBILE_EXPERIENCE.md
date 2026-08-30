# 15. MOBILE EXPERIENCE

Version: V1.0

Status: DESIGN FOUNDATION

Module:

knowledge/ui_system/

---

# 1. Purpose

Tài liệu này định nghĩa toàn bộ trải nghiệm Mobile của BTE Platform.

Mobile Experience không phải là:

Desktop được thu nhỏ.

Mobile Experience là:

Một sản phẩm được thiết kế riêng cho màn hình nhỏ.

Mục tiêu của Mobile là:

Giúp khách hàng hiểu nhanh điều quan trọng nhất và biết mình nên làm gì tiếp theo.

---

# 2. Core Philosophy

Desktop được thiết kế cho:

Phân tích.

Mobile được thiết kế cho:

Ra quyết định.

Hai trải nghiệm không giống nhau.

Desktop ưu tiên:

Chi tiết.

Mobile ưu tiên:

Điều quan trọng nhất.

---

# 3. Reading Model

Desktop

↓

Đọc toàn bộ Dashboard.

↓

20–30 phút.

---

Mobile

↓

Lướt.

↓

30–60 giây.

↓

Ra quyết định.

Không giả định khách hàng sẽ đọc toàn bộ.

---

# 4. Mobile First Principle

Không bắt đầu từ Desktop.

Không:

Desktop

↓

Responsive.

Mà:

Customer Goal

↓

Mobile Layout.

Responsive chỉ là kỹ thuật.

Mobile Experience là sản phẩm.

---

# 5. Decision Hierarchy

Thứ tự đọc trên Mobile:

1.

Top Priority

↓

2.

Executive Insight

↓

3.

Action Plan

↓

4.

Interpretation

↓

5.

Current Luck

↓

6.

Supporting Analysis

↓

7.

Evidence

Khác hoàn toàn Desktop.

---

# 6. Progressive Disclosure

Không hiển thị tất cả.

Hiển thị:

Điều cần biết trước.

↓

Chi tiết khi khách hàng yêu cầu.

Ưu tiên:

Expand.

Accordion.

Bottom Sheet.

Không mở toàn bộ mặc định.

---

# 7. Thumb Zone Principle

Các thành phần tương tác chính phải nằm trong vùng thao tác thuận tiện của ngón tay.

Ví dụ:

- Expand
- Xem thêm
- Xem chi tiết
- Điều hướng

Không đặt ở vị trí khó chạm.

---

# 8. Scroll Rhythm

Một màn hình.

↓

Một thông điệp.

Không:

Card

Card

Card

Card

Card

Liên tục.

Ưu tiên:

Section

↓

Khoảng nghỉ

↓

Section

↓

Khoảng nghỉ

Khách hàng phải cảm thấy nhịp đọc tự nhiên.

---

# 9. Information Density

Desktop

100%.

Mobile

≈60%.

Ẩn:

Metadata.

Technical Reference.

Chi tiết phụ.

Không ẩn:

Executive Summary.

Top Priority.

Action.

---

# 10. Hero Strategy

Hero luôn nằm trên cùng.

Bao gồm:

Executive Insight.

Top Priority.

Không hiển thị toàn bộ Dashboard trước Hero.

---

# 11. Executive Summary

Executive Summary luôn xuất hiện trước:

Interpretation.

Action.

Evidence.

Khách hàng phải hiểu:

"Lá số này nói gì?"

trước khi thấy:

"Tại sao?"

---

# 12. Action First

Sau Executive.

Hiển thị ngay:

Top Priority.

↓

Action.

↓

Warnings.

Mobile ưu tiên:

Việc cần làm.

Không ưu tiên:

Chi tiết kỹ thuật.

---

# 13. Interpretation Strategy

Chỉ hiển thị:

consulting_flow.

Chi tiết:

Observation.

Reasoning.

Meaning.

Impact.

Recommendation.

↓

Expand.

Không mở mặc định.

---

# 14. Evidence Strategy

Evidence luôn đứng sau Narrative.

Mobile không bắt đầu bằng:

BaZi.

Five Elements.

Ten Gods.

Evidence chỉ xuất hiện khi khách hàng muốn xem sâu hơn.

---

# 15. Visual Hierarchy

Level 1

Hero

Executive Summary

Top Priority

---

Level 2

Action

Interpretation

Luck

---

Level 3

Five Elements

Pattern

BaZi

Ten Gods

ShenSha

---

Level 4

Metadata

Appendix

Reference

---

# 16. Component Priority

Luôn ưu tiên:

Một Card lớn.

Thay vì:

Ba Card nhỏ.

Whitespace quan trọng hơn số lượng Card.

---

# 17. Responsive Rules

Không:

Resize.

Mà:

Re-layout.

Ví dụ:

Desktop:

3 cột.

↓

Mobile:

1 cột.

Nhưng:

Hierarchy phải thay đổi.

Không chỉ co chiều rộng.

---

# 18. Motion

Animation chỉ hỗ trợ:

Chuyển trạng thái.

Expand.

Collapse.

Không dùng animation để gây chú ý.

---

# 19. Mobile Navigation

Điều hướng ngắn.

Rõ.

Có thể quay lại.

Không để khách hàng bị lạc trong nhiều tầng thông tin.

---

# 20. Empty States

Không hiển thị:

Khung trống.

Thông báo kỹ thuật.

Ưu tiên:

Giải thích ngắn.

Điều khách hàng có thể làm tiếp theo.

---

# 21. Loading Experience

Hiển thị:

Skeleton.

Không nhấp nháy.

Không nhảy layout.

Không thay đổi vị trí thành phần sau khi tải.

---

# 22. Accessibility

Touch Target ≥ 44px.

Khoảng cách hợp lý.

Font dễ đọc.

Không phụ thuộc màu sắc.

---

# 23. Performance Principle

Mobile phải ưu tiên:

Đọc nhanh.

Tải nhanh.

Cuộn mượt.

Không tải các thành phần phụ trước Hero.

---

# 24. Mobile Trust Principle

Trong 5 giây đầu tiên khách hàng phải biết:

- Tôi là ai?
- Lá số nói gì?
- Việc quan trọng nhất là gì?

Nếu chưa trả lời được ba câu hỏi này, Mobile Experience thất bại.

---

# 25. One Screen Principle

Một màn hình.

↓

Một quyết định.

Không cố truyền nhiều thông tin trên cùng một viewport.

---

# 26. Commercial Principle

Mobile không nhằm:

Hiển thị toàn bộ hệ thống.

Mobile nhằm:

Giúp khách hàng cảm thấy:

- chuyên nghiệp;
- rõ ràng;
- dễ hiểu;
- đáng tin.

---

# 27. Relationship with Desktop

Desktop và Mobile cùng dùng:

Narrative.

Presentation.

Design System.

Khác nhau ở:

Hierarchy.

Interaction.

Reading Flow.

Không khác dữ liệu.

---

# 28. Relationship with Print

Print dành cho:

Lưu trữ.

Mobile dành cho:

Ra quyết định.

Hai trải nghiệm khác nhau.

Không được thiết kế giống nhau.

---

# 29. Validation Checklist

Một Mobile Experience đạt chuẩn khi:

✓ Hiểu trong dưới 1 phút.

✓ Hero xuất hiện đầu tiên.

✓ Top Priority nổi bật.

✓ Action dễ thấy.

✓ Narrative không bị thay đổi.

✓ Evidence không lấn át Executive.

✓ Không cần zoom.

---

# 30. Final Principle

Mobile không tồn tại để hiển thị toàn bộ Dashboard.

Mobile tồn tại để giúp khách hàng:

- hiểu nhanh;
- tin tưởng kết quả;
- biết điều quan trọng nhất;
- biết mình nên làm gì tiếp theo.

Một Mobile Experience thành công là khi khách hàng chỉ cần vài lần cuộn là đã nắm được giá trị chính của toàn bộ báo cáo.

---

# 31. Mobile Trust Principle

Một trải nghiệm Mobile tốt không cố đưa toàn bộ thông tin lên màn hình.

Nó giúp khách hàng nhìn thấy đúng thông tin vào đúng thời điểm.

Sự tin tưởng trên Mobile không đến từ việc hiển thị nhiều hơn.

Nó đến từ:

- đúng thứ tự;
- đúng mức độ ưu tiên;
- đúng nhịp đọc;
- đúng quyết định.

Mobile Experience thành công khi khách hàng có thể đưa ra quyết định đúng mà không cảm thấy quá tải bởi lượng thông tin.