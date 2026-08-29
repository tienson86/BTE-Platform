# COMMERCIAL DASHBOARD
# 04_MOBILE_LAYOUT
# MOBILE PRESENTATION SPECIFICATION

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Tài liệu này định nghĩa cách Commercial Dashboard hiển thị trên Mobile.

Mobile sử dụng cùng:

- Navigation logic
- Presentation Model
- Identity Header
- Cards
- Content hierarchy
- Business meaning

với Desktop.

Mobile không tạo một phiên bản nội dung riêng.

---

# 2. Nguyên tắc nền tảng

Desktop

↓

Tablet

↓

Mobile

chỉ thay đổi:

- chiều rộng;
- số cột;
- thứ tự xếp khối;
- cách trình bày bảng;
- kích thước typography;
- khoảng cách.

Không thay đổi:

- nội dung;
- kết luận;
- thứ tự nhận thức;
- nguồn dữ liệu;
- tên Card;
- ý nghĩa nghiệp vụ.

---

# 3. One Source of Truth

Mobile phải đọc cùng một Presentation Model với Desktop.

Không được:

- tạo Mobile ViewModel có semantic khác;
- tính lại dữ liệu;
- compose lại nội dung;
- rút gọn kết luận bằng logic riêng;
- tự tạo khuyến nghị.

Canonical flow:

```
Canonical Analysis

↓

Commercial Composer

↓

Presentation Model

├── Desktop
├── Mobile
├── PDF
└── DOCX
```

---

# 4. Navigation Mobile

Customer Portal V1 chỉ có ba chức năng chính:

- Trang chủ
- Chọn ngày tốt
- Xem lá số

Không hiển thị:

- Báo cáo
- Lịch sử
- Admin

---

# 5. Mobile Navigation Pattern

Trên màn hình nhỏ, Header Desktop được chuyển thành Navigation Mobile.

Ưu tiên:

```
BTE

[ Menu ]
```

Menu mở:

```
Trang chủ

Chọn ngày tốt

Xem lá số
```

Không tạo thêm chức năng.

Không nhét toàn bộ menu Desktop lên một hàng.

---

# 6. Trang chủ Mobile

Trang chủ vẫn là:

> Xem ngày tốt / xấu

Thứ tự:

```
Header

↓

Tháng / điều hướng lịch

↓

Calendar

↓

Ngày đang chọn

↓

Thông tin ngày

↓

Chi tiết
```

Không thay đổi nghiệp vụ so với Desktop.

Calendar phải ưu tiên khả năng chạm.

Không thu nhỏ nguyên Calendar Desktop đến mức khó sử dụng.

---

# 7. Chọn ngày tốt Mobile

Form hiển thị một cột.

Ví dụ:

```
CHỌN NGÀY TỐT

Mục đích

[................]

Khoảng thời gian

[................]

Thông tin liên quan

[................]

[ TÌM NGÀY TỐT ]
```

Không đặt nhiều field cạnh nhau trên Mobile.

Một hàng = một nhiệm vụ nhập.

---

# 8. Xem lá số Mobile

`SCREEN 01 — VIEW CHART` giữ đủ năm trường:

- Họ và tên
- Giới tính
- Ngày sinh
- Giờ sinh
- Nơi sinh

Layout:

```
XEM LÁ SỐ

Họ tên
[................]

Giới tính
[ Nam ] [ Nữ ]

Ngày sinh
[................]

Giờ sinh
[................]

Nơi sinh
[................]

Lưu ý:
Giờ sinh và nơi sinh càng chính xác
thì kết quả luận giải càng đáng tin cậy.

[ PHÂN TÍCH LÁ SỐ ]
```

Không chia hai cột.

CTA chiếm gần toàn chiều rộng.

---

# 9. Bazi Dashboard Mobile

Dashboard sử dụng một cột duy nhất.

Không giữ Grid Desktop bằng cách thu nhỏ.

Canonical order:

```
Identity Header

↓

Overview

↓

BaZi

↓

Five Elements

↓

Ten Gods

↓

Pattern

↓

ShenSha

↓

Luck

↓

Interpretation

↓

Action Plan
```

Không thay đổi thứ tự.

---

# 10. Identity Header Mobile

Desktop Identity Header gồm bốn vùng:

- A — Identity
- B — Four Pillars
- C — Foundation
- D — Status

Mobile chuyển thành:

```
A — Identity

↓

B — Four Pillars

↓

C — Foundation

↓

D — Status
```

Không đặt bốn vùng cạnh nhau.

---

# 11. Identity Priority

Thứ tự thị giác Mobile:

1. Họ tên
2. Tứ Trụ
3. Nhật Chủ
4. Nạp Âm
5. Cung Phi
6. Mệnh Quái
7. Nhóm Trạch
8. Metadata

Analysis Status luôn nhỏ nhất.

Không để Metadata chiếm phần đầu màn hình.

---

# 12. Tứ Trụ Mobile

Tứ Trụ không được biến thành danh sách văn bản dài.

Phải giữ cấu trúc bốn trụ:

```
       Năm   Tháng   Ngày   Giờ

Can

Chi
```

Nếu chiều rộng không đủ:

- giảm spacing;
- giảm kích thước chữ hợp lý;
- cho phép horizontal scroll nội bộ trong bảng nếu thật sự cần.

Không chuyển thành:

```
Năm: ...
Tháng: ...
Ngày: ...
Giờ: ...
```

nếu làm mất cấu trúc Tứ Trụ.

---

# 13. Overview Mobile

Thứ tự:

```
Insight

↓

Nhật Chủ

Thân

Mệnh Cục

↓

Dụng Thần

Điều Hậu

↓

Quick Conclusion
```

Không đưa toàn bộ Evidence thành bảng.

Insight phải đọc được ngay trong phần đầu viewport.

---

# 14. BaZi Mobile

BaZi Card sử dụng Progressive Disclosure.

Mặc định:

```
Thiên Can

Địa Chi

Nạp Âm
```

Sau đó:

```
[ Xem chi tiết ]
```

Mở thêm:

- Tàng Can
- Thập Thần
- Trường Sinh

Điều này giúp khách hàng phổ thông không bị quá tải.

---

# 15. Five Elements Mobile

Thứ tự:

```
Balance Indicator

↓

Five Elements Chart

↓

Element Summary

↓

Overall Comment
```

Biểu đồ phải responsive.

Không cần người dùng zoom.

Không làm legend quá nhỏ.

---

# 16. Ten Gods Mobile

Thứ tự:

```
Nhóm năng lực nổi bật

↓

Top Ten Gods

↓

Distribution

↓

Personality Summary

↓

Balance Comment
```

Nếu toàn bộ 10 Thập Thần quá dài:

Distribution có thể cuộn hoặc mở rộng.

Không bỏ dữ liệu.

---

# 17. Pattern Mobile

Thứ tự:

```
Mệnh Cục chính

↓

Trạng thái

↓

Mệnh Cục phụ

↓

Quá trình hình thành

↓

Summary
```

Formation nên hiển thị dạng vertical flow.

Ví dụ:

```
Nguyệt lệnh Sửu

↓

Kỷ đắc khí

↓

Mậu lộ can

↓

Chính Ấn Cách

↓

Đắc cách
```

Mobile phù hợp với vertical flow hơn horizontal diagram.

---

# 18. ShenSha Mobile

Các nhóm hiển thị theo accordion hoặc stacked sections:

```
Quý Nhân & Hỗ trợ

↓

Học tập & Danh tiếng

↓

Quan hệ & Tình cảm

↓

Di chuyển & Biến động

↓

Điều cần lưu ý
```

Mỗi mục hiển thị tên + ý nghĩa ngắn.

Không dùng bảng Có / Không.

---

# 19. Luck Mobile

Current Luck luôn hiển thị trước.

```
ẤT TỴ

2022–2031

35–44 tuổi
```

Timeline chuyển thành dạng ngang có scroll hoặc vertical roadmap.

Ưu tiên vertical roadmap trên Mobile:

```
Nhâm Dần

↓

Quý Mão

↓

Giáp Thìn

↓

● Ất Tỵ
  HIỆN TẠI

↓

Bính Ngọ
```

Không bắt người dùng đọc bảng 10 dòng.

---

# 20. Interpretation Mobile

Interpretation là Card đọc dài.

Thứ tự:

```
Tổng kết

↓

Điểm mạnh

↓

Điểm cần lưu ý

↓

Cơ hội

↓

Thách thức

↓

Kết luận
```

Mỗi section tách rõ.

Không đặt hai cột.

Không dùng font quá nhỏ để cố nhét nội dung.

---

# 21. Action Plan Mobile

Action Plan luôn là Card cuối cùng.

Thứ tự:

```
Top Priorities

↓

Nên làm

↓

Nên hạn chế

↓

Công việc

↓

Tài chính

↓

Quan hệ

↓

Sức khỏe

↓

Roadmap

↓

Final Message
```

Roadmap ưu tiên dạng vertical.

Ví dụ:

```
HÔM NAY
  ↓
30 NGÀY
  ↓
3 THÁNG
  ↓
1 NĂM
```

---

# 22. Card Width

Mọi Card Mobile:

```
width: 100%
```

trong content container.

Không đặt hai Card phân tích cạnh nhau.

Khoảng cách giữa các Card phải rõ hơn khoảng cách giữa các section nội bộ.

---

# 23. Spacing

Mobile ưu tiên khoảng trắng.

Không giảm spacing quá mức chỉ để nhìn thấy nhiều nội dung hơn.

Nguyên tắc:

```
Screen margin
>
Card internal padding vừa đủ
>
Section spacing rõ ràng
```

Mục tiêu:

- dễ đọc;
- dễ chạm;
- không tạo cảm giác chật.

---

# 24. Typography

Phân cấp phải rõ:

```
Screen Title

↓

Card Title

↓

Insight

↓

Section Title

↓

Body

↓

Metadata
```

Không để tất cả cùng cỡ chữ.

Metadata luôn nhỏ nhất.

Không dùng font quá nhỏ cho dữ liệu Bát Tự.

---

# 25. Touch Targets

Mọi tương tác Mobile phải có vùng chạm đủ lớn.

Bao gồm:

- menu;
- date selector;
- accordion;
- timeline;
- xem chi tiết;
- CTA.

Không tạo control nhỏ chỉ phù hợp chuột Desktop.

---

# 26. Progressive Disclosure

Mobile được phép ẩn Detail sau:

```
Xem chi tiết
```

nhưng không được ẩn:

- Insight;
- Conclusion;
- Current Luck;
- Action Priority.

Những thông tin quan trọng phải xuất hiện mặc định.

---

# 27. Không dùng Hover

Mobile không có Hover.

Mọi dữ liệu quan trọng không được phụ thuộc vào:

- hover tooltip;
- mouseover;
- hidden label.

Nếu Desktop dùng Hover để hỗ trợ, Mobile phải có phương thức tương đương bằng Tap hoặc hiển thị trực tiếp.

---

# 28. Charts

Biểu đồ phải:

- fit chiều rộng;
- có nhãn đọc được;
- không yêu cầu pinch zoom;
- không crop;
- không overflow ngoài Card.

Nếu biểu đồ quá phức tạp:

ưu tiên phiên bản Mobile đơn giản hơn về hình thức,

nhưng dữ liệu và ý nghĩa phải giống Desktop.

---

# 29. Tables

Không cố giữ bảng Desktop nếu bảng trở nên khó đọc.

Ưu tiên theo thứ tự:

1. Responsive table.
2. Horizontal scroll nội bộ.
3. Stacked rows.

Không được bỏ column dữ liệu quan trọng chỉ để vừa màn hình.

---

# 30. Sticky Elements

Có thể dùng Sticky Header nhỏ cho:

- Back
- Tên lá số
- Menu

Không để sticky element che nội dung.

Không tạo nhiều sticky toolbar.

---

# 31. CTA

CTA chính phải rõ.

Ví dụ:

```
PHÂN TÍCH LÁ SỐ
```

Không có nhiều nút cạnh tranh trên Mobile.

Các action phụ như:

- In
- Chia sẻ
- Xuất PDF

có thể đưa vào Action Menu.

---

# 32. Mobile Dashboard Actions

Trên Dashboard Mobile, không đặt hàng dài nút.

Ưu tiên:

```
[ ⋯ ]
```

mở:

- Chia sẻ
- In
- Xuất PDF
- Xem lá số khác

Không đưa Báo cáo / Lịch sử trở lại Customer Portal.

---

# 33. Performance

Mobile phải ưu tiên:

- render nhanh;
- chart nhẹ;
- không tải asset không cần thiết;
- không block màn hình vì phần Detail phía dưới.

First viewport phải ưu tiên:

- Identity;
- Overview.

---

# 34. Loading Experience

Sau khi bấm Phân tích lá số:

```
Đang lập Tứ Trụ...

↓

Đang phân tích Ngũ Hành...

↓

Đang xác định Mệnh Cục...

↓

Đang xây dựng luận giải...
```

Không chỉ hiển thị:

```
Loading...
```

Loading phải chiếm ít không gian nhưng tạo cảm giác hệ thống đang xử lý thực sự.

---

# 35. Mobile First Impression

Trong viewport đầu tiên sau khi kết quả xuất hiện, người dùng nên thấy tối thiểu:

- Identity cơ bản;
- Tứ Trụ;
- Nhật Chủ;
- phần đầu Overview.

Không để Metadata hoặc toolbar chiếm phần lớn màn hình đầu tiên.

---

# 36. Accessibility

Mobile phải hỗ trợ:

- screen reader labels;
- focus state;
- contrast;
- dynamic text scaling trong giới hạn layout cho phép.

Không dùng màu sắc làm cách truyền đạt duy nhất.

---

# 37. PDF Independence

Mobile layout không ảnh hưởng PDF layout.

Cả hai cùng đọc Presentation Model.

```
Presentation Model

├── Desktop Layout
├── Mobile Layout
└── Print Layout
```

Không:

```
Mobile HTML
↓

PDF
```

PDF là một presentation target riêng.

---

# 38. Breakpoint Philosophy

Không khóa thiết kế vào một thiết bị cụ thể.

Breakpoints chỉ phục vụ chuyển đổi layout.

Các trạng thái cơ bản:

```
Desktop

Tablet

Mobile
```

Không tạo layout riêng cho từng dòng điện thoại.

---

# 39. Content Parity

Mobile phải đạt Content Parity với Desktop.

Nghĩa là:

Desktop có dữ liệu nào có giá trị nghiệp vụ,

Mobile cũng phải truy cập được dữ liệu đó.

Mobile có thể:

- collapse;
- stack;
- scroll;

nhưng không được silently remove.

---

# 40. Acceptance Checklist

□ Customer Portal Mobile chỉ có Trang chủ, Chọn ngày tốt, Xem lá số.

□ Trang chủ vẫn là Xem ngày tốt/xấu.

□ Form Xem lá số có đúng 5 trường.

□ Dashboard sử dụng một cột.

□ Identity nằm đầu tiên.

□ Overview nằm ngay sau Identity.

□ Card order giống Desktop.

□ Tứ Trụ giữ cấu trúc bốn trụ.

□ BaZi hỗ trợ Progressive Disclosure.

□ Ngũ Hành có chart responsive.

□ Ten Gods không bị mất dữ liệu.

□ Pattern có Formation rõ ràng.

□ ShenSha tổ chức theo nhóm ý nghĩa.

□ Đại Vận làm nổi bật vận hiện tại.

□ Interpretation dễ đọc.

□ Action Plan là Card cuối.

□ Không phụ thuộc Hover.

□ Không có horizontal page overflow.

□ Không có text buộc người dùng zoom.

□ Không có logic phân tích trong Mobile layer.

□ Mobile và Desktop dùng cùng Presentation Model.

---

# 41. Nguyên tắc cuối cùng

Mobile không phải phiên bản rút gọn về giá trị.

Mobile chỉ là phiên bản rút gọn về không gian.

Khách hàng sử dụng điện thoại phải nhận được cùng:

- Insight;
- Analysis;
- Conclusion;
- Action

như khi sử dụng Desktop.

Đây là nguyên tắc bắt buộc của Commercial Dashboard V1.0.