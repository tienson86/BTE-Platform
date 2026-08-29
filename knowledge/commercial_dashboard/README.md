# COMMERCIAL DASHBOARD
# DESIGN SPECIFICATION
# README

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục đích

Thư mục này định nghĩa toàn bộ tiêu chuẩn thiết kế của giao diện thương mại (Commercial Dashboard) cho BTE Platform.

Đây là nguồn tham chiếu duy nhất (Single Source of Truth) cho:

- Portal
- Dashboard
- PDF
- DOCX
- Mobile
- Tablet

Mọi giao diện của BTE đều phải tuân theo tài liệu trong thư mục này.

Không được tự ý thay đổi bố cục hoặc nội dung hiển thị nếu chưa cập nhật đặc tả.

---

# 2. Mục tiêu

Commercial Dashboard không phải màn hình kỹ thuật.

Đây là màn hình tư vấn thương mại dành cho khách hàng cuối.

Mục tiêu của Dashboard là:

- giúp khách hàng hiểu lá số trong 30 giây đầu;
- giúp chuyên gia tư vấn có công cụ trình bày trực quan;
- chuyển toàn bộ kết quả phân tích thành thông tin dễ hiểu;
- thống nhất trải nghiệm giữa Portal, PDF và DOCX.

Dashboard không nhằm hiển thị toàn bộ dữ liệu của Engine.

Dashboard chỉ hiển thị những thông tin có giá trị đối với việc ra quyết định.

---

# 3. Triết lý thiết kế

Commercial Dashboard được xây dựng theo các nguyên tắc sau.

## 3.1 Dashboard là trung tâm

Portal là giao diện chuẩn.

PDF là bản in của Dashboard.

DOCX là phiên bản chỉnh sửa của Dashboard.

Không tồn tại nhiều giao diện độc lập.

Mọi nền tảng phải đọc cùng một Presentation Model.

---

## 3.2 Một màn hình = Một nhiệm vụ

Ví dụ

Trang chủ

→ xem ngày tốt/xấu.

Chọn ngày tốt

→ tìm ngày phù hợp.

Xem lá số

→ nhập thông tin.

Kết quả

→ xem toàn bộ phân tích.

Không có màn hình thực hiện nhiều nhiệm vụ cùng lúc.

---

## 3.3 Một Card = Một quyết định

Mỗi Card chỉ trả lời một câu hỏi.

Ví dụ

Card Tổng quan

→ Tôi là người như thế nào?

Card Ngũ hành

→ Tôi thiếu gì?

Card Đại vận

→ Giai đoạn hiện tại là cơ hội hay phòng thủ?

Card Hành động

→ Tôi nên làm gì tiếp theo?

Không nhồi nhiều thông điệp vào cùng một Card.

---

## 3.4 Ít dữ liệu nhập nhất

Người dùng chỉ nhập những thông tin bắt buộc.

Hệ thống tự tính:

- Âm lịch
- Can Chi
- Tứ Trụ
- Thập thần
- Đại vận
- Ngũ hành
- Thần sát
- Dụng thần
- Điều hậu
- ...

Không yêu cầu khách hàng nhập dữ liệu mà hệ thống có thể tự tính.

---

## 3.5 Hiển thị giá trị, không hiển thị thuật toán

Dashboard không trình bày:

- điểm tính toán nội bộ;
- mã Engine;
- Rule ID;
- Debug;
- Contract;
- JSON;
- Condition.

Dashboard chỉ trình bày kết luận phục vụ tư vấn.

---

# 4. Đối tượng sử dụng

Commercial Dashboard phục vụ ba nhóm người dùng.

## Khách hàng

Muốn hiểu lá số nhanh.

Không cần kiến thức Bát Tự.

---

## Chuyên gia

Muốn tư vấn nhanh.

Có thể mở từng Card để giải thích chi tiết.

---

## Doanh nghiệp

Muốn sử dụng Dashboard như báo cáo phân tích.

Có thể in trực tiếp thành PDF.

---

# 5. Navigation chuẩn

Portal V1 sử dụng ba màn hình chính.

## Trang chủ

Xem ngày tốt/xấu.

---

## Chọn ngày tốt

Tìm ngày phù hợp theo mục đích.

---

## Xem lá số

Nhập:

- Họ tên
- Giới tính
- Ngày sinh
- Giờ sinh
- Nơi sinh

↓

Phân tích lá số

↓

Kết quả Dashboard.

Báo cáo và Lịch sử không nằm trong Portal khách hàng.

Hai chức năng này thuộc hệ thống quản trị (Admin Portal).

---

# 6. Kiến trúc Presentation

Engine

↓

Canonical Analysis

↓

Commercial Knowledge

↓

Commercial Composer

↓

Presentation Adapter

↓

Commercial Dashboard

↓

PDF

↓

DOCX

Presentation không được tự tính toán.

Presentation chỉ hiển thị dữ liệu đã được chuẩn hóa.

---

# 7. Quy tắc thiết kế Card

Mỗi Card phải được mô tả trong một tài liệu riêng.

Mỗi Card bắt buộc phải định nghĩa:

- mục tiêu;
- dữ liệu đầu vào;
- dữ liệu hiển thị;
- thông điệp chính;
- hành động người dùng sau khi xem Card;
- mapping sang PDF;
- mapping sang Mobile.

Không được tạo Card mới nếu chưa có đặc tả.

---

# 8. Danh sách Screen

01_SCREEN_VIEW_CHART.md

Màn hình nhập thông tin.

---

02_SCREEN_RESULT_DASHBOARD.md

Dashboard kết quả.

---

# 9. Danh sách Card

01_CARD_FOUR_PILLARS.md

02_CARD_OVERVIEW.md

03_CARD_BAZI.md

04_CARD_FIVE_ELEMENTS.md

05_CARD_TEN_GODS.md

06_CARD_PATTERN.md

07_CARD_SHENSHA.md

08_CARD_LUCK.md

09_CARD_INTERPRETATION.md

10_CARD_ACTION_PLAN.md

---

# 10. Quy tắc phát triển

Không sửa giao diện trực tiếp.

Mọi thay đổi phải:

Specification

↓

Review

↓

Approve

↓

Implementation

↓

Acceptance

Không làm ngược quy trình.

---

# 11. Acceptance

Commercial Dashboard được coi là hoàn thành khi:

- Portal và PDF hiển thị cùng nội dung;
- mọi Card đều có đặc tả;
- mọi dữ liệu đều truy được về Engine;
- khách hàng có thể hiểu kết quả trong vòng 30 giây đầu;
- chuyên gia có thể sử dụng Dashboard để tư vấn trực tiếp.

---

# 12. Tầm nhìn

Commercial Dashboard là giao diện chuẩn của toàn bộ hệ sinh thái BTE.

Trong tương lai:

- Phong Thủy
- Chọn ngày
- Sim phong thủy
- Cân Xương
- Mai Hoa
- Kỳ Môn

đều sử dụng cùng triết lý thiết kế này.

Dashboard là lớp trình bày thống nhất của toàn bộ BTE Platform.
---

# 13. DESIGN PRINCIPLES

Design Principles là các nguyên tắc nền tảng của Commercial Dashboard.

Đây là những nguyên tắc **không được phá vỡ** trong toàn bộ vòng đời phát triển của BTE Platform.

Mọi thiết kế mới phải tuân thủ các nguyên tắc dưới đây trước khi được triển khai.

---

## DP-01 Dashboard First

Dashboard là giao diện chuẩn.

PDF và DOCX chỉ là các hình thức xuất bản của Dashboard.

Không thiết kế PDF trước rồi mới chuyển sang Dashboard.

Mọi dữ liệu phải được trình bày trên Dashboard trước.

Sau đó mới ánh xạ (mapping) sang:

- PDF
- DOCX
- Mobile
- Tablet

Dashboard luôn là nguồn tham chiếu chính của toàn bộ Presentation Layer.

---

## DP-02 Decision First

Mỗi Card phải giúp người dùng đưa ra một quyết định.

Không tạo Card chỉ để hiển thị dữ liệu.

Ví dụ:

Card Tổng quan

→ Tôi là người như thế nào?

Card Ngũ hành

→ Tôi đang thiếu hành gì?

Card Đại vận

→ Đây là thời kỳ phát triển hay phòng thủ?

Card Hành động

→ Tôi nên làm gì tiếp theo?

Nếu sau khi xem Card mà người dùng vẫn không biết mình cần làm gì thì Card đó chưa đạt yêu cầu.

---

## DP-03 One Source of Truth

Portal

PDF

DOCX

Mobile

Tablet

phải sử dụng cùng một Presentation Model.

Không được tồn tại nhiều nguồn dữ liệu hiển thị khác nhau.

Không cho phép:

Portal hiển thị một kiểu.

PDF hiển thị một kiểu.

DOCX hiển thị một kiểu.

Mọi nền tảng đều đọc từ cùng một nguồn dữ liệu đã được chuẩn hóa.

---

## DP-04 Progressive Disclosure

Hiển thị theo mức độ quan trọng.

Không đưa toàn bộ thông tin lên ngay từ đầu.

Nguyên tắc:

### Level 1

Thông tin quan trọng nhất.

Khách hàng hiểu trong 30 giây.

---

### Level 2

Thông tin phân tích.

Mở khi cần.

---

### Level 3

Thông tin chuyên sâu.

Dành cho chuyên gia.

Không làm khách hàng phổ thông bị quá tải.

---

## DP-05 Commercial Before Technical

Commercial Dashboard phục vụ khách hàng.

Không phục vụ Engine.

Ưu tiên:

- ngôn ngữ dễ hiểu;
- hành động rõ ràng;
- kết luận dễ nhớ;
- trải nghiệm tư vấn.

Không hiển thị:

- Rule ID
- Engine ID
- Debug
- JSON
- Internal Score
- Technical Contract

Mọi thuật toán đều phải được chuyển đổi thành ngôn ngữ tư vấn trước khi hiển thị.

---

## DP-06 Explain Before Detail

Luôn trình bày:

"Kết luận"

trước

"Giải thích".

Ví dụ:

✓ Bạn thuộc nhóm Thân vượng.

↓

Sau đó mới giải thích vì sao.

Không làm ngược lại.

Khách hàng luôn muốn biết kết luận trước.

---

## DP-07 Action Oriented

Mỗi màn hình đều phải dẫn đến hành động tiếp theo.

Ví dụ:

Trang chủ

↓

Xem ngày tốt.

---

Xem lá số

↓

Phân tích lá số.

---

Kết quả

↓

Thực hiện khuyến nghị.

Không để khách hàng xem xong mà không biết bước tiếp theo.

---

## DP-08 Trust Through Transparency

Mọi kết luận đều phải truy vết được về dữ liệu phân tích.

Presentation không được tự tạo nội dung.

Mọi thông tin hiển thị phải có nguồn từ:

- Canonical Analysis
- Commercial Knowledge
- Commercial Composer

Điều này giúp hệ thống:

- minh bạch;
- dễ kiểm chứng;
- dễ bảo trì;
- dễ mở rộng.

---

## DP-09 Consistency Across Products

Cùng một khách hàng.

Cùng một lá số.

Dù xem trên:

- Web
- Mobile
- PDF
- DOCX

thì:

- nội dung;
- thứ tự;
- thông điệp;
- kết luận

phải giống nhau.

Chỉ khác hình thức trình bày.

---

## DP-10 Evolution Without Disruption

Dashboard được phép mở rộng.

Nhưng không được phá vỡ trải nghiệm đã học của người dùng.

Các nguyên tắc sau luôn được giữ:

- vị trí các Screen;
- triết lý các Card;
- luồng sử dụng;
- cách đọc Dashboard.

Tính ổn định của trải nghiệm quan trọng hơn việc thay đổi giao diện.