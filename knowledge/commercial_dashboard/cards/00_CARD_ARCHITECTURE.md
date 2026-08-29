# COMMERCIAL DASHBOARD
# CARD ARCHITECTURE
# CARD DESIGN SPECIFICATION

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Tài liệu này định nghĩa kiến trúc chuẩn của mọi Card trong Commercial Dashboard.

Mọi Card đều phải tuân thủ tài liệu này.

Không được tạo Card mới nếu chưa đáp ứng các nguyên tắc dưới đây.

---

# 2. Vai trò của Card

Card là đơn vị hiển thị nhỏ nhất của Dashboard.

Dashboard được cấu thành từ:

Header

↓

Cards

↓

Footer (nếu có)

Card không phải là nơi trình bày toàn bộ dữ liệu.

Card chỉ giải quyết một mục tiêu nghiệp vụ duy nhất.

---

# 3. Một Card = Một câu hỏi

Mỗi Card chỉ được phép trả lời duy nhất một câu hỏi.

Ví dụ:

Overview

↓

"Tôi là người như thế nào?"

Five Elements

↓

"Tôi đang thiếu hay thừa hành nào?"

Luck

↓

"Tôi đang ở vận nào?"

Action Plan

↓

"Tôi nên làm gì?"

Nếu một Card trả lời nhiều hơn một câu hỏi thì Card đó phải được chia nhỏ hoặc điều chỉnh.

---

# 4. Một Card = Một quyết định

Sau khi xem xong một Card.

Người dùng phải đưa ra được một quyết định.

Ví dụ:

Overview

↓

"Tôi là người Thân vượng."

Five Elements

↓

"Tôi cần bổ sung Hỏa."

Luck

↓

"Đây là giai đoạn phát triển."

Action Plan

↓

"Ba việc cần làm ngay."

Card không chỉ hiển thị dữ liệu.

Card phải giúp ra quyết định.

---

# 5. Một Card = Một nguồn dữ liệu

Mỗi Card chỉ được có một nguồn dữ liệu chính.

Ví dụ:

Overview

↓

Canonical Analysis

Five Elements

↓

Five Elements Engine

Ten Gods

↓

Ten Gods Engine

Interpretation

↓

Commercial Composer

Action Plan

↓

Commercial Knowledge

Presentation Layer không được tự tổng hợp dữ liệu từ nhiều nguồn.

Nếu cần tổng hợp.

Việc đó phải diễn ra trước Presentation.

---

# 6. Không chồng chéo

Không Card nào được phép lặp vai trò của Card khác.

Ví dụ:

Overview

Không giải thích Thập thần.

Five Elements

Không kết luận Dụng thần.

Pattern

Không mô tả Đại vận.

Interpretation

Không lặp lại bảng Ngũ hành.

Action Plan

Không trình bày phân tích.

Dashboard phải đọc giống một câu chuyện.

Không phải nhiều Card lặp nội dung.

---

# 7. Cấu trúc chuẩn của một Card

Mọi Card đều sử dụng cùng một cấu trúc.

## 7.1 Header

Tên Card.

Icon (nếu có).

---

## 7.2 Insight

Đây là phần quan trọng nhất.

Trả lời ngay câu hỏi của Card.

Ví dụ:

"Bạn thuộc nhóm Thân vượng."

Người dùng phải hiểu trong vài giây.

---

## 7.3 Evidence

Hiển thị dữ liệu chứng minh cho Insight.

Ví dụ:

- Nhật Chủ
- Ngũ hành
- Mệnh cục

Không giải thích dài.

---

## 7.4 Detail

Thông tin mở rộng.

Chỉ dành cho người muốn tìm hiểu sâu hơn.

---

## 7.5 Footer

Nếu Card có hành động tiếp theo.

Footer hiển thị:

- Xem thêm
- Mở chi tiết

Không phải Card nào cũng cần Footer.

---

# 8. Quy tắc trình bày

Insight luôn nằm trên.

Evidence ở giữa.

Detail ở dưới.

Không đảo thứ tự.

Không bắt đầu Card bằng bảng dữ liệu.

---

# 9. Thứ tự ưu tiên

Một Card phải hiển thị theo đúng trình tự:

Insight

↓

Evidence

↓

Detail

↓

Action (nếu có)

Không làm ngược.

---

# 10. Không hiển thị

Card không được hiển thị:

- Rule ID
- Engine ID
- JSON
- Debug
- Internal Contract
- Raw Score
- Điều kiện kỹ thuật

Đây là dữ liệu của hệ thống.

Không phải của khách hàng.

---

# 11. Nguồn dữ liệu

Presentation Layer chỉ đọc.

Không tính toán.

Không suy luận.

Không sinh dữ liệu mới.

Mọi dữ liệu đều phải truy được về:

Canonical Analysis

hoặc

Commercial Composer

---

# 12. Visual Hierarchy

Mỗi Card có một mức ưu tiên.

Hero

Core

Supporting

Decision

Card không được tự thay đổi cấp ưu tiên.

---

# 13. Kích thước

Không phải Card nào cũng có cùng kích thước.

Hero Card

Lớn.

Analysis Card

Trung bình.

Supporting Card

Nhỏ hơn.

Decision Card

Rộng hơn.

Kích thước phản ánh tầm quan trọng.

---

# 14. Responsive

Desktop

Tablet

Mobile

chỉ thay đổi cách sắp xếp.

Không thay đổi nội dung.

---

# 15. PDF Mapping

Portal

↓

PDF

↓

DOCX

đều dùng cùng Presentation Model.

Không tạo phiên bản Card riêng.

---

# 16. Card Lifecycle

Mỗi Card đều đi qua quy trình:

Specification

↓

Review

↓

Approve

↓

Implementation

↓

Acceptance

Không viết code trước Specification.

---

# 17. Card Classification

Dashboard V1 gồm ba nhóm.

Header

↓

Identity

---

Analysis Cards

- Overview
- BaZi
- Five Elements
- Ten Gods
- Pattern
- ShenSha
- Luck

---

Decision Cards

- Interpretation
- Action Plan

Mọi Card mới phải thuộc một trong ba nhóm này.

---

# 18. Design Rules

Một Card tốt phải:

✓ Trả lời đúng một câu hỏi.

✓ Dẫn đến đúng một quyết định.

✓ Có đúng một nguồn dữ liệu chính.

✓ Không lặp Card khác.

✓ Đọc được trong khoảng 15–30 giây.

✓ Không cần giải thích kỹ thuật.

---

# 19. Acceptance Checklist

□ Một Card chỉ có một nhiệm vụ.

□ Không trùng vai trò với Card khác.

□ Có Insight rõ ràng.

□ Có Evidence chứng minh.

□ Có Detail mở rộng.

□ Có Mapping sang PDF.

□ Có Mapping sang Mobile.

□ Không có dữ liệu kỹ thuật.

□ Không tự tính toán.

□ Không vi phạm Design Principles.

---

# 20. Nguyên tắc cuối cùng

Dashboard không được thiết kế theo cách:

"Nhiều Card = nhiều thông tin."

Dashboard phải được thiết kế theo cách:

"Mỗi Card giúp người dùng hiểu thêm một phần của câu chuyện."

Khi ghép tất cả các Card lại.

Người dùng sẽ hiểu trọn vẹn lá số.

Đó là mục tiêu cuối cùng của Commercial Dashboard.